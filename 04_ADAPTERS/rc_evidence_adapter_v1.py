from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


ADAPTER_VERSION = "RC_EVIDENCE_ADAPTER_v1"

EXPECTED_GATEWAY_VERSION = "ORIGIN_GATEWAY_v1.1"
EXPECTED_RECORD_TYPE = "EVIDENCE_RECORD_STREAM"

RC_ENVIRONMENT_NAME = "RC_ENVIRONMENT"


class AdapterError(Exception):
    pass


@dataclass(frozen=True)
class RCEvidenceState:
    state_id: str
    evidence_id: str
    raw_observation_id: str
    value: Any
    unit: str | None
    channel: str | None
    source: str
    origin_label: str
    evidence_status: str
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)
    adapter_version: str = ADAPTER_VERSION
    provenance_preserved: bool = True
    raw_value_preserved: bool = True
    adapter_interpretation_performed: bool = False


class RCEvidenceAdapter:
    def __init__(self, adapter_name: str = "RC Evidence Adapter v1") -> None:
        self.adapter_name = adapter_name

    def load_evidence_stream(self, input_path: str | Path) -> dict:
        input_path = Path(input_path)

        if not input_path.exists():
            raise AdapterError(f"Evidence stream not found:\n{input_path}")

        return json.loads(input_path.read_text(encoding="utf-8"))

    def validate_evidence_stream(self, stream: dict) -> None:
        if stream.get("gateway_version") != EXPECTED_GATEWAY_VERSION:
            raise AdapterError(
                f"Unexpected gateway_version: {stream.get('gateway_version')}"
            )

        if stream.get("record_type") != EXPECTED_RECORD_TYPE:
            raise AdapterError(
                f"Unexpected record_type: {stream.get('record_type')}"
            )

        records = stream.get("records")

        if not isinstance(records, list):
            raise AdapterError("records must be a list")

        if len(records) == 0:
            raise AdapterError("records list is empty")

    def select_rc_records(self, stream: dict) -> list[dict]:
        records = stream["records"]

        return [
            record
            for record in records
            if record.get("environment") == RC_ENVIRONMENT_NAME
        ]

    def build_rc_state(self, record: dict) -> RCEvidenceState:
        origin = record.get("origin")

        if not isinstance(origin, dict):
            raise AdapterError(
                f"{record.get('evidence_id')} has no origin object"
            )

        if record.get("provenance_preserved") is not True:
            raise AdapterError(
                f"{record.get('evidence_id')} lost provenance"
            )

        if record.get("raw_preserved") is not True:
            raise AdapterError(
                f"{record.get('evidence_id')} lost raw value"
            )

        if record.get("interpretation_performed") is not False:
            raise AdapterError(
                f"{record.get('evidence_id')} was already interpreted before adapter"
            )

        evidence_id = record.get("evidence_id")

        return RCEvidenceState(
            state_id=f"RC_STATE_{evidence_id}",
            evidence_id=evidence_id,
            raw_observation_id=record.get("raw_observation_id"),
            value=record.get("raw_value"),
            unit=record.get("unit"),
            channel=record.get("channel"),
            source=record.get("source"),
            origin_label=origin.get("label"),
            evidence_status=record.get("evidence_status"),
            confidence=origin.get("confidence"),
            metadata=dict(record.get("metadata") or {}),
        )

    def adapt(self, stream: dict) -> list[RCEvidenceState]:
        self.validate_evidence_stream(stream)

        rc_records = self.select_rc_records(stream)

        return [
            self.build_rc_state(record)
            for record in rc_records
        ]

    def export(
        self,
        rc_states: list[RCEvidenceState],
        output_path: str | Path,
    ) -> Path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "adapter_version": ADAPTER_VERSION,
            "adapter_name": self.adapter_name,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "input_record_type": EXPECTED_RECORD_TYPE,
            "output_record_type": "RC_EVIDENCE_STATE_STREAM",
            "environment": RC_ENVIRONMENT_NAME,
            "state_count": len(rc_states),
            "states": [
                asdict(state)
                for state in rc_states
            ],
        }

        output_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return output_path


def main() -> None:
    print("🔌 RC EVIDENCE ADAPTER v1")
    print("=" * 80)

    input_path = (
        Path("..")
        / "07_OUTPUT"
        / "origin_gateway_demo_v1_1.json"
    )

    output_path = (
        Path("..")
        / "07_OUTPUT"
        / "rc_evidence_adapter_demo_v1.json"
    )

    adapter = RCEvidenceAdapter()

    try:
        evidence_stream = adapter.load_evidence_stream(input_path)
        rc_states = adapter.adapt(evidence_stream)
        exported_path = adapter.export(rc_states, output_path)

    except AdapterError as exc:
        print("-" * 80)
        print("ADAPTER FAILED")
        print(exc)
        print("=" * 80)
        sys.exit(1)

    print(f"Adapter:      {adapter.adapter_name}")
    print(f"Version:      {ADAPTER_VERSION}")
    print(f"Input:        {input_path}")
    print(f"RC states:    {len(rc_states)}")
    print(f"Output:       {exported_path}")
    print("-" * 80)

    for state in rc_states:
        print(
            f"{state.state_id}: "
            f"{state.channel}={state.value} {state.unit} "
            f"| {state.origin_label} "
            f"| {state.evidence_status}"
        )

    print("=" * 80)
    print("READY")


if __name__ == "__main__":
    main()
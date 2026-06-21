# ==================================================================================================
# rc_evidence_adapter_v1.py
#
# Difference Retention Laboratory
# RC Evidence Adapter v1.1
#
# Purpose:
#   Convert Evidence Record Stream into RC Evidence State Stream
#   while preserving origin lineage for Retention Analysis.
#
# v1.1:
#   Adds explicit origin_reference and evidence_reference propagation.
#
# Input:
#   ../07_OUTPUT/origin_gateway_demo_v1_1.json
#
# Output:
#   ../07_OUTPUT/rc_evidence_adapter_demo_v1.json
#
# Run:
#   python rc_evidence_adapter_v1.py
# ==================================================================================================

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_INPUT_PATH = PROJECT_ROOT / "07_OUTPUT" / "origin_gateway_demo_v1_1.json"
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "07_OUTPUT" / "rc_evidence_adapter_demo_v1.json"


@dataclass
class RCEvidenceState:
    state_id: str
    evidence_id: str
    raw_observation_id: str
    origin_reference: str
    evidence_reference: str
    value: float
    unit: str
    channel: str
    source: str
    origin_label: str
    evidence_status: str
    confidence: float
    metadata: dict[str, Any]
    adapter_version: str
    provenance_preserved: bool
    raw_value_preserved: bool
    adapter_interpretation_performed: bool


@dataclass
class RCEvidenceStateStream:
    adapter_version: str
    adapter_name: str
    created_at: str
    input_record_type: str
    output_record_type: str
    environment: str
    origin_reference: str
    evidence_reference: str
    lineage_status: str
    state_count: int
    states: list[RCEvidenceState]


class RCEvidenceAdapterV1:
    VERSION = "RC_EVIDENCE_ADAPTER_v1.1"

    def load_json(self, input_path: Path) -> dict[str, Any]:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        with input_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Evidence input must be a JSON object.")

        return data

    def export_json(self, payload: dict[str, Any], output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)

        return output_path

    def now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def get_records(self, evidence_stream: dict[str, Any]) -> list[dict[str, Any]]:
        for key in (
            "records",
            "evidence_records",
            "evidences",
            "items",
            "observations",
        ):
            value = evidence_stream.get(key)

            if isinstance(value, list):
                return [
                    item
                    for item in value
                    if isinstance(item, dict)
                ]

        if "record_type" in evidence_stream or "evidence_id" in evidence_stream:
            return [evidence_stream]

        return []

    def first_meaningful_value(self, source: dict[str, Any], keys: tuple[str, ...]) -> Any:
        for key in keys:
            value = source.get(key)

            if value is None:
                continue

            if isinstance(value, str) and value.strip() == "":
                continue

            return value

        return None

    def extract_origin_reference(self, record: dict[str, Any]) -> str:
        value = self.first_meaningful_value(
            record,
            (
                "origin_reference",
                "origin_id",
                "raw_observation_id",
                "observation_id",
                "source_observation_id",
            ),
        )

        if value is not None:
            return str(value)

        raw_observation = record.get("raw_observation")

        if isinstance(raw_observation, dict):
            value = self.first_meaningful_value(
                raw_observation,
                (
                    "observation_id",
                    "raw_observation_id",
                    "id",
                ),
            )

            if value is not None:
                return str(value)

        return "origin_reference_unavailable"

    def extract_evidence_reference(self, record: dict[str, Any]) -> str:
        value = self.first_meaningful_value(
            record,
            (
                "evidence_reference",
                "evidence_id",
                "record_id",
                "id",
            ),
        )

        if value is not None:
            return str(value)

        return "evidence_reference_unavailable"

    def extract_float(self, record: dict[str, Any], key: str, default: float = 0.0) -> float:
        value = record.get(key, default)

        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def build_state(self, record: dict[str, Any], index: int) -> RCEvidenceState:
        evidence_reference = self.extract_evidence_reference(record)
        origin_reference = self.extract_origin_reference(record)

        evidence_id = (
            evidence_reference
            if evidence_reference != "evidence_reference_unavailable"
            else f"EVIDENCE_RC_{index:03d}"
        )

        raw_observation_id = (
            origin_reference
            if origin_reference != "origin_reference_unavailable"
            else str(record.get("raw_observation_id", f"RC_{index:03d}"))
        )

        return RCEvidenceState(
            state_id=f"RC_STATE_{evidence_id}",
            evidence_id=evidence_id,
            raw_observation_id=raw_observation_id,
            origin_reference=origin_reference,
            evidence_reference=evidence_reference,
            value=self.extract_float(record, "value", 0.0),
            unit=str(record.get("unit", "unknown")),
            channel=str(record.get("channel", "unknown")),
            source=str(record.get("source", "unknown")),
            origin_label=str(record.get("origin_label", record.get("label", "UNKNOWN_ORIGIN"))),
            evidence_status=str(record.get("evidence_status", "UNCLASSIFIED_EVIDENCE")),
            confidence=self.extract_float(record, "confidence", 0.0),
            metadata=dict(record.get("metadata", {})) if isinstance(record.get("metadata", {}), dict) else {},
            adapter_version=self.VERSION,
            provenance_preserved=origin_reference != "origin_reference_unavailable",
            raw_value_preserved="value" in record,
            adapter_interpretation_performed=False,
        )

    def determine_stream_origin_reference(self, states: list[RCEvidenceState]) -> str:
        references = sorted(
            {
                state.origin_reference
                for state in states
                if state.origin_reference != "origin_reference_unavailable"
            }
        )

        if not references:
            return "origin_reference_unavailable"

        if len(references) == 1:
            return references[0]

        return "multiple_origin_references:" + ",".join(references)

    def determine_stream_evidence_reference(self, states: list[RCEvidenceState]) -> str:
        references = sorted(
            {
                state.evidence_reference
                for state in states
                if state.evidence_reference != "evidence_reference_unavailable"
            }
        )

        if not references:
            return "evidence_reference_unavailable"

        if len(references) == 1:
            return references[0]

        return "multiple_evidence_references:" + ",".join(references)

    def determine_lineage_status(self, states: list[RCEvidenceState]) -> str:
        if not states:
            return "NO_STATES"

        preserved_count = sum(
            1
            for state in states
            if state.provenance_preserved
        )

        if preserved_count == len(states):
            return "ORIGIN_LINEAGE_PRESERVED"

        if preserved_count > 0:
            return "ORIGIN_LINEAGE_PARTIAL"

        return "ORIGIN_LINEAGE_BROKEN"

    def adapt(
        self,
        input_path: Path = DEFAULT_INPUT_PATH,
    ) -> RCEvidenceStateStream:
        evidence_stream = self.load_json(input_path)
        records = self.get_records(evidence_stream)

        states = [
            self.build_state(record=record, index=index)
            for index, record in enumerate(records, start=1)
        ]

        return RCEvidenceStateStream(
            adapter_version=self.VERSION,
            adapter_name="RC Evidence Adapter v1.1",
            created_at=self.now(),
            input_record_type=str(evidence_stream.get("record_type", "EVIDENCE_RECORD_STREAM")),
            output_record_type="RC_EVIDENCE_STATE_STREAM",
            environment="RC_ENVIRONMENT",
            origin_reference=self.determine_stream_origin_reference(states),
            evidence_reference=self.determine_stream_evidence_reference(states),
            lineage_status=self.determine_lineage_status(states),
            state_count=len(states),
            states=states,
        )

    def run(
        self,
        input_path: Path = DEFAULT_INPUT_PATH,
        output_path: Path = DEFAULT_OUTPUT_PATH,
    ) -> Path:
        stream = self.adapt(input_path=input_path)
        payload = asdict(stream)

        return self.export_json(payload=payload, output_path=output_path)


def main() -> None:
    adapter = RCEvidenceAdapterV1()
    output_path = adapter.run()

    print("🔌 RC EVIDENCE ADAPTER v1.1")
    print("=" * 80)
    print(f"Input:  {DEFAULT_INPUT_PATH}")
    print(f"Output: {output_path}")
    print("Status: READY")
    print("=" * 80)


if __name__ == "__main__":
    main()
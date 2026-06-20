from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


GATEWAY_VERSION = "ORIGIN_GATEWAY_v1.1"


ORIGIN_DIRECT_MEASUREMENT = "DIRECT_MEASUREMENT"
ORIGIN_INSTRUMENTAL_NOISE = "INSTRUMENTAL_NOISE"
ORIGIN_MODEL_EXTRAPOLATION = "MODEL_EXTRAPOLATION"
ORIGIN_APPROXIMATION = "APPROXIMATION"
ORIGIN_DERIVED_VALUE = "DERIVED_VALUE"
ORIGIN_SIMULATION_OUTPUT = "SIMULATION_OUTPUT"
ORIGIN_UNKNOWN = "UNKNOWN_ORIGIN"


EVIDENCE_STATUS_ACCEPTED = "ACCEPTED_AS_EVIDENCE"
EVIDENCE_STATUS_WEAK = "WEAK_EVIDENCE"
EVIDENCE_STATUS_UNCERTAIN = "UNCERTAIN_EVIDENCE"


ALLOWED_ORIGIN_LABELS = {
    ORIGIN_DIRECT_MEASUREMENT,
    ORIGIN_INSTRUMENTAL_NOISE,
    ORIGIN_MODEL_EXTRAPOLATION,
    ORIGIN_APPROXIMATION,
    ORIGIN_DERIVED_VALUE,
    ORIGIN_SIMULATION_OUTPUT,
    ORIGIN_UNKNOWN,
}


@dataclass(frozen=True)
class RawObservation:
    observation_id: str
    raw_value: Any
    source: str
    environment: str
    timestamp: str | None = None
    unit: str | None = None
    channel: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class OriginLabel:
    label: str
    reason: str
    confidence: float


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    raw_observation_id: str
    raw_value: Any
    source: str
    environment: str
    origin: OriginLabel
    evidence_status: str
    timestamp: str | None = None
    unit: str | None = None
    channel: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    gateway_version: str = GATEWAY_VERSION
    raw_preserved: bool = True
    provenance_preserved: bool = True
    interpretation_performed: bool = False


class OriginGateway:
    def __init__(self, gateway_name: str = "Origin Gateway v1.1") -> None:
        self.gateway_name = gateway_name

    def classify_origin(self, observation: RawObservation) -> OriginLabel:
        metadata = observation.metadata or {}

        explicit_origin = metadata.get("origin_label")

        if explicit_origin in ALLOWED_ORIGIN_LABELS:
            return OriginLabel(
                label=explicit_origin,
                reason="Explicit origin label provided by upstream source.",
                confidence=1.0,
            )

        if metadata.get("is_noise") is True:
            return OriginLabel(
                label=ORIGIN_INSTRUMENTAL_NOISE,
                reason="Observation marked as instrumental noise.",
                confidence=0.9,
            )

        if metadata.get("is_extrapolated") is True:
            return OriginLabel(
                label=ORIGIN_MODEL_EXTRAPOLATION,
                reason="Observation marked as model extrapolation.",
                confidence=0.9,
            )

        if metadata.get("is_approximation") is True:
            return OriginLabel(
                label=ORIGIN_APPROXIMATION,
                reason="Observation marked as approximation.",
                confidence=0.85,
            )

        if metadata.get("is_derived") is True:
            return OriginLabel(
                label=ORIGIN_DERIVED_VALUE,
                reason="Observation marked as derived value.",
                confidence=0.85,
            )

        if metadata.get("is_simulation") is True:
            return OriginLabel(
                label=ORIGIN_SIMULATION_OUTPUT,
                reason="Observation marked as simulation output.",
                confidence=0.9,
            )

        if observation.source and observation.environment:
            return OriginLabel(
                label=ORIGIN_DIRECT_MEASUREMENT,
                reason="Observation has source and environment but no synthetic or derived markers.",
                confidence=0.75,
            )

        return OriginLabel(
            label=ORIGIN_UNKNOWN,
            reason="Origin could not be reliably classified.",
            confidence=0.2,
        )

    def determine_evidence_status(self, origin: OriginLabel) -> str:
        if origin.label == ORIGIN_UNKNOWN:
            return EVIDENCE_STATUS_UNCERTAIN

        if origin.confidence < 0.5:
            return EVIDENCE_STATUS_UNCERTAIN

        if origin.label in {
            ORIGIN_INSTRUMENTAL_NOISE,
            ORIGIN_APPROXIMATION,
            ORIGIN_MODEL_EXTRAPOLATION,
        }:
            return EVIDENCE_STATUS_WEAK

        return EVIDENCE_STATUS_ACCEPTED

    def build_evidence_record(self, observation: RawObservation) -> EvidenceRecord:
        origin = self.classify_origin(observation)
        evidence_status = self.determine_evidence_status(origin)

        return EvidenceRecord(
            evidence_id=f"EVIDENCE_{observation.observation_id}",
            raw_observation_id=observation.observation_id,
            raw_value=observation.raw_value,
            source=observation.source,
            environment=observation.environment,
            timestamp=observation.timestamp,
            unit=observation.unit,
            channel=observation.channel,
            metadata=dict(observation.metadata),
            origin=origin,
            evidence_status=evidence_status,
        )

    def process_batch(self, observations: list[RawObservation]) -> list[EvidenceRecord]:
        return [
            self.build_evidence_record(observation)
            for observation in observations
        ]

    def export(
        self,
        evidence_records: list[EvidenceRecord],
        output_path: str | Path,
    ) -> Path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "gateway_version": GATEWAY_VERSION,
            "gateway_name": self.gateway_name,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "record_type": "EVIDENCE_RECORD_STREAM",
            "evidence_count": len(evidence_records),
            "origin_labels": sorted(ALLOWED_ORIGIN_LABELS),
            "records": [
                asdict(record)
                for record in evidence_records
            ],
        }

        output_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return output_path


def build_demo_observations() -> list[RawObservation]:
    return [
        RawObservation(
            observation_id="RC_001",
            raw_value=4.96,
            source="M830B multimeter",
            environment="RC_ENVIRONMENT",
            unit="V",
            channel="VC",
            metadata={
                "origin_label": ORIGIN_DIRECT_MEASUREMENT,
            },
        ),
        RawObservation(
            observation_id="RC_002",
            raw_value=0.03,
            source="M830B multimeter",
            environment="RC_ENVIRONMENT",
            unit="V",
            channel="OUT1",
            metadata={
                "is_noise": True,
            },
        ),
        RawObservation(
            observation_id="CARBON_001",
            raw_value={
                "structure": "candidate_carbon_lattice",
                "energy": -12.71,
            },
            source="carbon simulation",
            environment="CARBON_ENVIRONMENT",
            unit="simulation_unit",
            metadata={
                "is_simulation": True,
            },
        ),
        RawObservation(
            observation_id="ELECTROLYTE_001",
            raw_value=1.28,
            source="manual estimate",
            environment="ELECTROLYTE_ENVIRONMENT",
            unit="relative_index",
            metadata={
                "is_approximation": True,
            },
        ),
    ]


def main() -> None:
    print("🛡️ ORIGIN GATEWAY v1.1")
    print("=" * 80)

    gateway = OriginGateway()
    raw_observations = build_demo_observations()
    evidence_records = gateway.process_batch(raw_observations)

    output_path = Path("..") / "07_OUTPUT" / "origin_gateway_demo_v1_1.json"
    exported_path = gateway.export(evidence_records, output_path)

    print(f"Gateway:       {gateway.gateway_name}")
    print(f"Version:       {GATEWAY_VERSION}")
    print(f"Evidence:      {len(evidence_records)}")
    print(f"Output:        {exported_path}")
    print("-" * 80)

    for record in evidence_records:
        print(
            f"{record.evidence_id}: "
            f"{record.origin.label} "
            f"| {record.evidence_status} "
            f"| confidence={record.origin.confidence}"
        )

    print("=" * 80)
    print("READY")


if __name__ == "__main__":
    main()
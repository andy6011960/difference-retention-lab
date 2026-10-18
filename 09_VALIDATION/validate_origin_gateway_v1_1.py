from __future__ import annotations

import json
import sys
from pathlib import Path


EXPECTED_GATEWAY_VERSION = "ORIGIN_GATEWAY_v1.1"
EXPECTED_RECORD_TYPE = "EVIDENCE_RECORD_STREAM"

REQUIRED_ORIGIN_LABELS = {
    "DIRECT_MEASUREMENT",
    "INSTRUMENTAL_NOISE",
    "MODEL_EXTRAPOLATION",
    "APPROXIMATION",
    "DERIVED_VALUE",
    "SIMULATION_OUTPUT",
    "UNKNOWN_ORIGIN",
}

REQUIRED_EVIDENCE_STATUSES = {
    "ACCEPTED_AS_EVIDENCE",
    "WEAK_EVIDENCE",
    "UNCERTAIN_EVIDENCE",
}


class ValidationError(Exception):
    pass


class OriginGatewayValidator:
    def __init__(self, json_path: str | Path) -> None:
        self.json_path = Path(json_path)

    def load(self) -> dict:
        if not self.json_path.exists():
            raise ValidationError(f"JSON file not found:\n{self.json_path}")

        return json.loads(
            self.json_path.read_text(encoding="utf-8")
        )

    def validate(self) -> None:
        data = self.load()

        self.validate_header(data)
        self.validate_records(data)

    def validate_header(self, data: dict) -> None:
        if data.get("gateway_version") != EXPECTED_GATEWAY_VERSION:
            raise ValidationError(
                f"Unexpected gateway_version: {data.get('gateway_version')}"
            )

        if data.get("record_type") != EXPECTED_RECORD_TYPE:
            raise ValidationError(
                f"Unexpected record_type: {data.get('record_type')}"
            )

        records = data.get("records")

        if not isinstance(records, list):
            raise ValidationError("records must be a list")

        if len(records) == 0:
            raise ValidationError("records list is empty")

    def validate_records(self, data: dict) -> None:
        records = data["records"]

        for record in records:

            if record.get("raw_preserved") is not True:
                raise ValidationError(
                    f"{record.get('evidence_id')} : raw_preserved != True"
                )

            if record.get("provenance_preserved") is not True:
                raise ValidationError(
                    f"{record.get('evidence_id')} : provenance_preserved != True"
                )

            if record.get("interpretation_performed") is not False:
                raise ValidationError(
                    f"{record.get('evidence_id')} : interpretation_performed must be False"
                )

            origin = record.get("origin")

            if not isinstance(origin, dict):
                raise ValidationError(
                    f"{record.get('evidence_id')} : missing origin object"
                )

            label = origin.get("label")

            if label not in REQUIRED_ORIGIN_LABELS:
                raise ValidationError(
                    f"{record.get('evidence_id')} : invalid origin label {label}"
                )

            confidence = origin.get("confidence")

            if not isinstance(confidence, (int, float)):
                raise ValidationError(
                    f"{record.get('evidence_id')} : confidence is not numeric"
                )

            if confidence < 0.0 or confidence > 1.0:
                raise ValidationError(
                    f"{record.get('evidence_id')} : confidence outside [0,1]"
                )

            status = record.get("evidence_status")

            if status not in REQUIRED_EVIDENCE_STATUSES:
                raise ValidationError(
                    f"{record.get('evidence_id')} : invalid evidence status {status}"
                )


def main() -> None:

    print("🧪 ORIGIN GATEWAY VALIDATOR v1.1")
    print("=" * 80)

    json_path = (
        Path("..")
        / "07_OUTPUT"
        / "origin_gateway_demo_v1_1.json"
    )

    print(f"Input: {json_path}")

    validator = OriginGatewayValidator(json_path)

    try:
        validator.validate()

    except ValidationError as exc:
        print("-" * 80)
        print("VALIDATION FAILED")
        print(exc)
        print("=" * 80)
        sys.exit(1)

    print("-" * 80)
    print("HEADER")
    print("PASS")

    print("-" * 80)
    print("INVARIANTS")
    print("PASS")

    print("-" * 80)
    print("PROVENANCE")
    print("PASS")

    print("-" * 80)
    print("EVIDENCE")
    print("PASS")

    print("=" * 80)
    print("VERDICT: ORIGIN_GATEWAY_V1_1_VALIDATED")


if __name__ == "__main__":
    main()
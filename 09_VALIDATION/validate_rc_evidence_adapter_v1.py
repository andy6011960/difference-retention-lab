from __future__ import annotations

import json
import sys
from pathlib import Path


EXPECTED_ADAPTER_VERSION = "RC_EVIDENCE_ADAPTER_v1"
EXPECTED_INPUT_RECORD_TYPE = "EVIDENCE_RECORD_STREAM"
EXPECTED_OUTPUT_RECORD_TYPE = "RC_EVIDENCE_STATE_STREAM"
EXPECTED_ENVIRONMENT = "RC_ENVIRONMENT"


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


class RCEvidenceAdapterValidator:
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
        self.validate_states(data)

    def validate_header(self, data: dict) -> None:
        if data.get("adapter_version") != EXPECTED_ADAPTER_VERSION:
            raise ValidationError(
                f"Unexpected adapter_version: {data.get('adapter_version')}"
            )

        if data.get("input_record_type") != EXPECTED_INPUT_RECORD_TYPE:
            raise ValidationError(
                f"Unexpected input_record_type: {data.get('input_record_type')}"
            )

        if data.get("output_record_type") != EXPECTED_OUTPUT_RECORD_TYPE:
            raise ValidationError(
                f"Unexpected output_record_type: {data.get('output_record_type')}"
            )

        if data.get("environment") != EXPECTED_ENVIRONMENT:
            raise ValidationError(
                f"Unexpected environment: {data.get('environment')}"
            )

        states = data.get("states")

        if not isinstance(states, list):
            raise ValidationError("states must be a list")

        if len(states) == 0:
            raise ValidationError("states list is empty")

        if data.get("state_count") != len(states):
            raise ValidationError(
                f"state_count mismatch: header={data.get('state_count')} actual={len(states)}"
            )

    def validate_states(self, data: dict) -> None:
        states = data["states"]

        for state in states:
            state_id = state.get("state_id")

            if not state_id:
                raise ValidationError("state without state_id")

            if not state.get("evidence_id"):
                raise ValidationError(f"{state_id}: missing evidence_id")

            if not state.get("raw_observation_id"):
                raise ValidationError(f"{state_id}: missing raw_observation_id")

            if state.get("provenance_preserved") is not True:
                raise ValidationError(f"{state_id}: provenance_preserved != True")

            if state.get("raw_value_preserved") is not True:
                raise ValidationError(f"{state_id}: raw_value_preserved != True")

            if state.get("adapter_interpretation_performed") is not False:
                raise ValidationError(
                    f"{state_id}: adapter_interpretation_performed must be False"
                )

            if state.get("origin_label") not in REQUIRED_ORIGIN_LABELS:
                raise ValidationError(
                    f"{state_id}: invalid origin_label {state.get('origin_label')}"
                )

            if state.get("evidence_status") not in REQUIRED_EVIDENCE_STATUSES:
                raise ValidationError(
                    f"{state_id}: invalid evidence_status {state.get('evidence_status')}"
                )

            confidence = state.get("confidence")

            if not isinstance(confidence, (int, float)):
                raise ValidationError(f"{state_id}: confidence is not numeric")

            if confidence < 0.0 or confidence > 1.0:
                raise ValidationError(f"{state_id}: confidence outside [0, 1]")


def main() -> None:
    print("🧪 RC EVIDENCE ADAPTER VALIDATOR v1")
    print("=" * 80)

    json_path = (
        Path("..")
        / "07_OUTPUT"
        / "rc_evidence_adapter_demo_v1.json"
    )

    print(f"Input: {json_path}")

    validator = RCEvidenceAdapterValidator(json_path)

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
    print("STATES")
    print("PASS")

    print("-" * 80)
    print("PROVENANCE")
    print("PASS")

    print("-" * 80)
    print("ADAPTER BOUNDARY")
    print("PASS")

    print("=" * 80)
    print("VERDICT: RC_EVIDENCE_ADAPTER_V1_VALIDATED")


if __name__ == "__main__":
    main()
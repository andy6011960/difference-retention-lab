from __future__ import annotations

import json
import sys
from pathlib import Path


EXPECTED_RECORD_TYPE = "EXPERIMENT_RUN_RECORD"
EXPECTED_RUNNER_VERSION = "EXPERIMENT_RUNNER_v1"
EXPECTED_INPUT_RECORD_TYPE = "RC_EVIDENCE_STATE_STREAM"
EXPECTED_ENVIRONMENT = "RC_ENVIRONMENT"
EXPECTED_RUN_STATUS = "EXPERIMENT_RECORDED"


class ValidationError(Exception):
    pass


class ExperimentRunnerValidator:
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
        self.validate_run(data)
        self.validate_states(data)

    def validate_header(self, data: dict) -> None:
        if data.get("record_type") != EXPECTED_RECORD_TYPE:
            raise ValidationError(
                f"Unexpected record_type: {data.get('record_type')}"
            )

        if data.get("runner_version") != EXPECTED_RUNNER_VERSION:
            raise ValidationError(
                f"Unexpected runner_version: {data.get('runner_version')}"
            )

        run = data.get("run")

        if not isinstance(run, dict):
            raise ValidationError("Missing run object")

    def validate_run(self, data: dict) -> None:
        run = data["run"]

        if run.get("runner_version") != EXPECTED_RUNNER_VERSION:
            raise ValidationError(
                f"Unexpected run.runner_version: {run.get('runner_version')}"
            )

        if run.get("environment") != EXPECTED_ENVIRONMENT:
            raise ValidationError(
                f"Unexpected environment: {run.get('environment')}"
            )

        if run.get("input_record_type") != EXPECTED_INPUT_RECORD_TYPE:
            raise ValidationError(
                f"Unexpected input_record_type: {run.get('input_record_type')}"
            )

        if run.get("run_status") != EXPECTED_RUN_STATUS:
            raise ValidationError(
                f"Unexpected run_status: {run.get('run_status')}"
            )

        if run.get("provenance_preserved") is not True:
            raise ValidationError("run.provenance_preserved != True")

        if run.get("experiment_interpretation_performed") is not False:
            raise ValidationError(
                "run.experiment_interpretation_performed must be False"
            )

        states = run.get("states")

        if not isinstance(states, list):
            raise ValidationError("run.states must be a list")

        if len(states) == 0:
            raise ValidationError("run.states list is empty")

        if run.get("input_state_count") != len(states):
            raise ValidationError(
                f"input_state_count mismatch: "
                f"header={run.get('input_state_count')} actual={len(states)}"
            )

        accepted = sum(
            1
            for state in states
            if state.get("evidence_status") == "ACCEPTED_AS_EVIDENCE"
        )

        weak = sum(
            1
            for state in states
            if state.get("evidence_status") == "WEAK_EVIDENCE"
        )

        uncertain = sum(
            1
            for state in states
            if state.get("evidence_status") == "UNCERTAIN_EVIDENCE"
        )

        if run.get("accepted_evidence_count") != accepted:
            raise ValidationError(
                f"accepted_evidence_count mismatch: "
                f"header={run.get('accepted_evidence_count')} actual={accepted}"
            )

        if run.get("weak_evidence_count") != weak:
            raise ValidationError(
                f"weak_evidence_count mismatch: "
                f"header={run.get('weak_evidence_count')} actual={weak}"
            )

        if run.get("uncertain_evidence_count") != uncertain:
            raise ValidationError(
                f"uncertain_evidence_count mismatch: "
                f"header={run.get('uncertain_evidence_count')} actual={uncertain}"
            )

    def validate_states(self, data: dict) -> None:
        states = data["run"]["states"]

        for state in states:
            state_id = state.get("state_id")

            if not state_id:
                raise ValidationError("state without state_id")

            if not state.get("evidence_id"):
                raise ValidationError(f"{state_id}: missing evidence_id")

            if not state.get("raw_observation_id"):
                raise ValidationError(f"{state_id}: missing raw_observation_id")

            if not state.get("origin_label"):
                raise ValidationError(f"{state_id}: missing origin_label")

            if not state.get("evidence_status"):
                raise ValidationError(f"{state_id}: missing evidence_status")

            if state.get("provenance_preserved") is not True:
                raise ValidationError(f"{state_id}: provenance_preserved != True")

            if state.get("raw_value_preserved") is not True:
                raise ValidationError(f"{state_id}: raw_value_preserved != True")

            if state.get("adapter_interpretation_performed") is not False:
                raise ValidationError(
                    f"{state_id}: adapter_interpretation_performed must be False"
                )


def main() -> None:
    print("🧪 EXPERIMENT RUNNER VALIDATOR v1")
    print("=" * 80)

    json_path = (
        Path("..")
        / "07_OUTPUT"
        / "experiment_run_record_demo_v1.json"
    )

    print(f"Input: {json_path}")

    validator = ExperimentRunnerValidator(json_path)

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
    print("RUN RECORD")
    print("PASS")

    print("-" * 80)
    print("STATE COUNTS")
    print("PASS")

    print("-" * 80)
    print("PROVENANCE")
    print("PASS")

    print("-" * 80)
    print("RUNNER BOUNDARY")
    print("PASS")

    print("=" * 80)
    print("VERDICT: EXPERIMENT_RUNNER_V1_VALIDATED")


if __name__ == "__main__":
    main()
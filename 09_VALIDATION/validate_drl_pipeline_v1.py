from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


PIPELINE_VALIDATOR_VERSION = "DRL_PIPELINE_VALIDATOR_v1"

EXPECTED_GATEWAY_VERSION = "ORIGIN_GATEWAY_v1.1"
EXPECTED_ADAPTER_VERSION = "RC_EVIDENCE_ADAPTER_v1"
EXPECTED_RUNNER_VERSION = "EXPERIMENT_RUNNER_v1"

EXPECTED_EVIDENCE_RECORD_TYPE = "EVIDENCE_RECORD_STREAM"
EXPECTED_STATE_RECORD_TYPE = "RC_EVIDENCE_STATE_STREAM"
EXPECTED_RUN_RECORD_TYPE = "EXPERIMENT_RUN_RECORD"

EXPECTED_ENVIRONMENT = "RC_ENVIRONMENT"


class PipelineValidationError(Exception):
    pass


class DRLPipelineValidator:
    def __init__(
        self,
        evidence_path: str | Path,
        state_path: str | Path,
        run_path: str | Path,
    ) -> None:
        self.evidence_path = Path(evidence_path)
        self.state_path = Path(state_path)
        self.run_path = Path(run_path)

        self.evidence_stream: dict[str, Any] = {}
        self.state_stream: dict[str, Any] = {}
        self.run_record: dict[str, Any] = {}

    def load_json(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            raise PipelineValidationError(f"File not found:\n{path}")

        return json.loads(path.read_text(encoding="utf-8"))

    def load_all(self) -> None:
        self.evidence_stream = self.load_json(self.evidence_path)
        self.state_stream = self.load_json(self.state_path)
        self.run_record = self.load_json(self.run_path)

    def validate(self) -> None:
        self.load_all()

        self.validate_gateway_layer()
        self.validate_adapter_layer()
        self.validate_runner_layer()
        self.validate_identity_continuity()
        self.validate_provenance_continuity()
        self.validate_interpretation_boundary()
        self.validate_count_conservation()
        self.validate_lab_constitution()

    def validate_gateway_layer(self) -> None:
        if self.evidence_stream.get("gateway_version") != EXPECTED_GATEWAY_VERSION:
            raise PipelineValidationError(
                f"Unexpected gateway_version: {self.evidence_stream.get('gateway_version')}"
            )

        if self.evidence_stream.get("record_type") != EXPECTED_EVIDENCE_RECORD_TYPE:
            raise PipelineValidationError(
                f"Unexpected evidence record_type: {self.evidence_stream.get('record_type')}"
            )

        records = self.evidence_stream.get("records")

        if not isinstance(records, list):
            raise PipelineValidationError("Evidence records must be a list")

        if len(records) == 0:
            raise PipelineValidationError("Evidence records list is empty")

        for record in records:
            evidence_id = record.get("evidence_id")

            if not evidence_id:
                raise PipelineValidationError("Evidence record without evidence_id")

            if not record.get("raw_observation_id"):
                raise PipelineValidationError(f"{evidence_id}: missing raw_observation_id")

            if not isinstance(record.get("origin"), dict):
                raise PipelineValidationError(f"{evidence_id}: missing origin object")

            if not record["origin"].get("label"):
                raise PipelineValidationError(f"{evidence_id}: missing origin.label")

            if not record.get("evidence_status"):
                raise PipelineValidationError(f"{evidence_id}: missing evidence_status")

    def validate_adapter_layer(self) -> None:
        if self.state_stream.get("adapter_version") != EXPECTED_ADAPTER_VERSION:
            raise PipelineValidationError(
                f"Unexpected adapter_version: {self.state_stream.get('adapter_version')}"
            )

        if self.state_stream.get("input_record_type") != EXPECTED_EVIDENCE_RECORD_TYPE:
            raise PipelineValidationError(
                f"Unexpected adapter input_record_type: {self.state_stream.get('input_record_type')}"
            )

        if self.state_stream.get("output_record_type") != EXPECTED_STATE_RECORD_TYPE:
            raise PipelineValidationError(
                f"Unexpected adapter output_record_type: {self.state_stream.get('output_record_type')}"
            )

        if self.state_stream.get("environment") != EXPECTED_ENVIRONMENT:
            raise PipelineValidationError(
                f"Unexpected adapter environment: {self.state_stream.get('environment')}"
            )

        states = self.state_stream.get("states")

        if not isinstance(states, list):
            raise PipelineValidationError("Adapter states must be a list")

        if len(states) == 0:
            raise PipelineValidationError("Adapter states list is empty")

        if self.state_stream.get("state_count") != len(states):
            raise PipelineValidationError(
                f"Adapter state_count mismatch: "
                f"header={self.state_stream.get('state_count')} actual={len(states)}"
            )

        for state in states:
            state_id = state.get("state_id")

            if not state_id:
                raise PipelineValidationError("State without state_id")

            if not state.get("evidence_id"):
                raise PipelineValidationError(f"{state_id}: missing evidence_id")

            if not state.get("raw_observation_id"):
                raise PipelineValidationError(f"{state_id}: missing raw_observation_id")

            if not state.get("origin_label"):
                raise PipelineValidationError(f"{state_id}: missing origin_label")

            if not state.get("evidence_status"):
                raise PipelineValidationError(f"{state_id}: missing evidence_status")

    def validate_runner_layer(self) -> None:
        if self.run_record.get("record_type") != EXPECTED_RUN_RECORD_TYPE:
            raise PipelineValidationError(
                f"Unexpected run record_type: {self.run_record.get('record_type')}"
            )

        if self.run_record.get("runner_version") != EXPECTED_RUNNER_VERSION:
            raise PipelineValidationError(
                f"Unexpected runner_version: {self.run_record.get('runner_version')}"
            )

        run = self.run_record.get("run")

        if not isinstance(run, dict):
            raise PipelineValidationError("Missing run object")

        if run.get("runner_version") != EXPECTED_RUNNER_VERSION:
            raise PipelineValidationError(
                f"Unexpected run.runner_version: {run.get('runner_version')}"
            )

        if run.get("environment") != EXPECTED_ENVIRONMENT:
            raise PipelineValidationError(
                f"Unexpected run environment: {run.get('environment')}"
            )

        if run.get("input_record_type") != EXPECTED_STATE_RECORD_TYPE:
            raise PipelineValidationError(
                f"Unexpected run input_record_type: {run.get('input_record_type')}"
            )

        states = run.get("states")

        if not isinstance(states, list):
            raise PipelineValidationError("Run states must be a list")

        if len(states) == 0:
            raise PipelineValidationError("Run states list is empty")

        if run.get("input_state_count") != len(states):
            raise PipelineValidationError(
                f"Run input_state_count mismatch: "
                f"header={run.get('input_state_count')} actual={len(states)}"
            )

    def evidence_by_id(self) -> dict[str, dict[str, Any]]:
        return {
            record["evidence_id"]: record
            for record in self.evidence_stream["records"]
        }

    def state_by_id(self) -> dict[str, dict[str, Any]]:
        return {
            state["state_id"]: state
            for state in self.state_stream["states"]
        }

    def run_state_by_id(self) -> dict[str, dict[str, Any]]:
        return {
            state["state_id"]: state
            for state in self.run_record["run"]["states"]
        }

    def validate_identity_continuity(self) -> None:
        evidence_index = self.evidence_by_id()
        run_state_index = self.run_state_by_id()

        for state in self.state_stream["states"]:
            state_id = state["state_id"]
            evidence_id = state["evidence_id"]
            raw_observation_id = state["raw_observation_id"]

            if evidence_id not in evidence_index:
                raise PipelineValidationError(
                    f"{state_id}: evidence_id not found in Evidence Stream: {evidence_id}"
                )

            evidence = evidence_index[evidence_id]

            if evidence.get("raw_observation_id") != raw_observation_id:
                raise PipelineValidationError(
                    f"{state_id}: raw_observation_id mismatch between Evidence and State"
                )

            expected_state_id = f"RC_STATE_{evidence_id}"

            if state_id != expected_state_id:
                raise PipelineValidationError(
                    f"{state_id}: invalid state_id, expected {expected_state_id}"
                )

            if state_id not in run_state_index:
                raise PipelineValidationError(
                    f"{state_id}: missing from Experiment Run Record"
                )

            run_state = run_state_index[state_id]

            if run_state.get("evidence_id") != evidence_id:
                raise PipelineValidationError(
                    f"{state_id}: evidence_id mismatch between State Stream and Run Record"
                )

            if run_state.get("raw_observation_id") != raw_observation_id:
                raise PipelineValidationError(
                    f"{state_id}: raw_observation_id mismatch between State Stream and Run Record"
                )

    def validate_provenance_continuity(self) -> None:
        for record in self.evidence_stream["records"]:
            evidence_id = record["evidence_id"]

            if record.get("raw_preserved") is not True:
                raise PipelineValidationError(f"{evidence_id}: raw_preserved != True")

            if record.get("provenance_preserved") is not True:
                raise PipelineValidationError(f"{evidence_id}: provenance_preserved != True")

        for state in self.state_stream["states"]:
            state_id = state["state_id"]

            if state.get("raw_value_preserved") is not True:
                raise PipelineValidationError(f"{state_id}: raw_value_preserved != True")

            if state.get("provenance_preserved") is not True:
                raise PipelineValidationError(f"{state_id}: provenance_preserved != True")

        run = self.run_record["run"]

        if run.get("provenance_preserved") is not True:
            raise PipelineValidationError("Experiment run provenance_preserved != True")

        for state in run["states"]:
            state_id = state["state_id"]

            if state.get("raw_value_preserved") is not True:
                raise PipelineValidationError(
                    f"{state_id} in run: raw_value_preserved != True"
                )

            if state.get("provenance_preserved") is not True:
                raise PipelineValidationError(
                    f"{state_id} in run: provenance_preserved != True"
                )

    def validate_interpretation_boundary(self) -> None:
        for record in self.evidence_stream["records"]:
            evidence_id = record["evidence_id"]

            if record.get("interpretation_performed") is not False:
                raise PipelineValidationError(
                    f"{evidence_id}: interpretation_performed must be False"
                )

        for state in self.state_stream["states"]:
            state_id = state["state_id"]

            if state.get("adapter_interpretation_performed") is not False:
                raise PipelineValidationError(
                    f"{state_id}: adapter_interpretation_performed must be False"
                )

        run = self.run_record["run"]

        if run.get("experiment_interpretation_performed") is not False:
            raise PipelineValidationError(
                "Experiment run interpretation must be False"
            )

        for state in run["states"]:
            state_id = state["state_id"]

            if state.get("adapter_interpretation_performed") is not False:
                raise PipelineValidationError(
                    f"{state_id} in run: adapter_interpretation_performed must be False"
                )

    def validate_count_conservation(self) -> None:
        rc_evidence_records = [
            record
            for record in self.evidence_stream["records"]
            if record.get("environment") == EXPECTED_ENVIRONMENT
        ]

        adapter_states = self.state_stream["states"]
        run_states = self.run_record["run"]["states"]

        if len(rc_evidence_records) != len(adapter_states):
            raise PipelineValidationError(
                f"RC Evidence count does not match Adapter State count: "
                f"evidence={len(rc_evidence_records)} states={len(adapter_states)}"
            )

        if len(adapter_states) != len(run_states):
            raise PipelineValidationError(
                f"Adapter State count does not match Run State count: "
                f"states={len(adapter_states)} run_states={len(run_states)}"
            )

        accepted = sum(
            1
            for state in run_states
            if state.get("evidence_status") == "ACCEPTED_AS_EVIDENCE"
        )

        weak = sum(
            1
            for state in run_states
            if state.get("evidence_status") == "WEAK_EVIDENCE"
        )

        uncertain = sum(
            1
            for state in run_states
            if state.get("evidence_status") == "UNCERTAIN_EVIDENCE"
        )

        run = self.run_record["run"]

        if run.get("accepted_evidence_count") != accepted:
            raise PipelineValidationError("Accepted evidence count mismatch")

        if run.get("weak_evidence_count") != weak:
            raise PipelineValidationError("Weak evidence count mismatch")

        if run.get("uncertain_evidence_count") != uncertain:
            raise PipelineValidationError("Uncertain evidence count mismatch")

    def validate_lab_constitution(self) -> None:
        if len(self.evidence_stream["records"]) == 0:
            raise PipelineValidationError("Constitution failure: no evidence records")

        if len(self.state_stream["states"]) == 0:
            raise PipelineValidationError("Constitution failure: no state records")

        if len(self.run_record["run"]["states"]) == 0:
            raise PipelineValidationError("Constitution failure: no run states")

        if self.run_record["run"].get("run_status") != "EXPERIMENT_RECORDED":
            raise PipelineValidationError(
                "Constitution failure: experiment was not recorded"
            )


def main() -> None:
    print("🧬 DRL PIPELINE VALIDATOR v1")
    print("=" * 80)

    evidence_path = (
        Path("..")
        / "07_OUTPUT"
        / "origin_gateway_demo_v1_1.json"
    )

    state_path = (
        Path("..")
        / "07_OUTPUT"
        / "rc_evidence_adapter_demo_v1.json"
    )

    run_path = (
        Path("..")
        / "07_OUTPUT"
        / "experiment_run_record_demo_v1.json"
    )

    print(f"Evidence: {evidence_path}")
    print(f"States:   {state_path}")
    print(f"Run:      {run_path}")

    validator = DRLPipelineValidator(
        evidence_path=evidence_path,
        state_path=state_path,
        run_path=run_path,
    )

    try:
        validator.validate()

    except PipelineValidationError as exc:
        print("-" * 80)
        print("PIPELINE VALIDATION FAILED")
        print(exc)
        print("=" * 80)
        sys.exit(1)

    print("-" * 80)
    print("ORIGIN")
    print("PASS")

    print("-" * 80)
    print("EVIDENCE")
    print("PASS")

    print("-" * 80)
    print("STATE")
    print("PASS")

    print("-" * 80)
    print("EXPERIMENT")
    print("PASS")

    print("-" * 80)
    print("IDENTITY CONTINUITY")
    print("PASS")

    print("-" * 80)
    print("PROVENANCE CONTINUITY")
    print("PASS")

    print("-" * 80)
    print("INTERPRETATION BOUNDARY")
    print("PASS")

    print("-" * 80)
    print("COUNT CONSERVATION")
    print("PASS")

    print("-" * 80)
    print("LAB CONSTITUTION")
    print("PASS")

    print("=" * 80)
    print("DIFFERENCE RETENTION LABORATORY")
    print("PIPELINE STATUS")
    print("-" * 80)
    print("ORIGIN:        PASS")
    print("EVIDENCE:      PASS")
    print("STATE:         PASS")
    print("EXPERIMENT:    PASS")
    print("CONSTITUTION:  PASS")
    print("=" * 80)
    print("FINAL VERDICT: DRL_PIPELINE_v1_READY")


if __name__ == "__main__":
    main()
from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


RUNNER_VERSION = "EXPERIMENT_RUNNER_v1"

EXPECTED_INPUT_RECORD_TYPE = "RC_EVIDENCE_STATE_STREAM"
EXPECTED_ADAPTER_VERSION = "RC_EVIDENCE_ADAPTER_v1"
EXPECTED_ENVIRONMENT = "RC_ENVIRONMENT"


class ExperimentRunnerError(Exception):
    pass


@dataclass(frozen=True)
class ExperimentRunRecord:
    experiment_id: str
    runner_version: str
    environment: str
    input_record_type: str
    input_state_count: int
    accepted_evidence_count: int
    weak_evidence_count: int
    uncertain_evidence_count: int
    source_adapter_version: str
    created_at: str
    states: list[dict[str, Any]] = field(default_factory=list)
    provenance_preserved: bool = True
    experiment_interpretation_performed: bool = False
    run_status: str = "EXPERIMENT_RECORDED"


class ExperimentRunner:
    def __init__(self, runner_name: str = "Experiment Runner v1") -> None:
        self.runner_name = runner_name

    def load_state_stream(self, input_path: str | Path) -> dict:
        input_path = Path(input_path)

        if not input_path.exists():
            raise ExperimentRunnerError(f"State stream not found:\n{input_path}")

        return json.loads(input_path.read_text(encoding="utf-8"))

    def validate_state_stream(self, stream: dict) -> None:
        if stream.get("adapter_version") != EXPECTED_ADAPTER_VERSION:
            raise ExperimentRunnerError(
                f"Unexpected adapter_version: {stream.get('adapter_version')}"
            )

        if stream.get("output_record_type") != EXPECTED_INPUT_RECORD_TYPE:
            raise ExperimentRunnerError(
                f"Unexpected output_record_type: {stream.get('output_record_type')}"
            )

        if stream.get("environment") != EXPECTED_ENVIRONMENT:
            raise ExperimentRunnerError(
                f"Unexpected environment: {stream.get('environment')}"
            )

        states = stream.get("states")

        if not isinstance(states, list):
            raise ExperimentRunnerError("states must be a list")

        if len(states) == 0:
            raise ExperimentRunnerError("states list is empty")

    def count_statuses(self, states: list[dict[str, Any]]) -> dict[str, int]:
        return {
            "accepted": sum(
                1
                for state in states
                if state.get("evidence_status") == "ACCEPTED_AS_EVIDENCE"
            ),
            "weak": sum(
                1
                for state in states
                if state.get("evidence_status") == "WEAK_EVIDENCE"
            ),
            "uncertain": sum(
                1
                for state in states
                if state.get("evidence_status") == "UNCERTAIN_EVIDENCE"
            ),
        }

    def validate_state_invariants(self, states: list[dict[str, Any]]) -> None:
        for state in states:
            state_id = state.get("state_id")

            if not state_id:
                raise ExperimentRunnerError("state without state_id")

            if state.get("provenance_preserved") is not True:
                raise ExperimentRunnerError(f"{state_id}: provenance lost")

            if state.get("raw_value_preserved") is not True:
                raise ExperimentRunnerError(f"{state_id}: raw value lost")

            if state.get("adapter_interpretation_performed") is not False:
                raise ExperimentRunnerError(
                    f"{state_id}: adapter interpretation already performed"
                )

            if not state.get("evidence_id"):
                raise ExperimentRunnerError(f"{state_id}: missing evidence_id")

            if not state.get("origin_label"):
                raise ExperimentRunnerError(f"{state_id}: missing origin_label")

            if not state.get("evidence_status"):
                raise ExperimentRunnerError(f"{state_id}: missing evidence_status")

    def build_run_record(self, stream: dict) -> ExperimentRunRecord:
        self.validate_state_stream(stream)

        states = stream["states"]
        self.validate_state_invariants(states)

        status_counts = self.count_statuses(states)

        return ExperimentRunRecord(
            experiment_id="EXPERIMENT_RC_EVIDENCE_DEMO_v1",
            runner_version=RUNNER_VERSION,
            environment=stream["environment"],
            input_record_type=stream["output_record_type"],
            input_state_count=len(states),
            accepted_evidence_count=status_counts["accepted"],
            weak_evidence_count=status_counts["weak"],
            uncertain_evidence_count=status_counts["uncertain"],
            source_adapter_version=stream["adapter_version"],
            created_at=datetime.now().isoformat(timespec="seconds"),
            states=[
                dict(state)
                for state in states
            ],
        )

    def export(
        self,
        run_record: ExperimentRunRecord,
        output_path: str | Path,
    ) -> Path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "record_type": "EXPERIMENT_RUN_RECORD",
            "runner_name": self.runner_name,
            "runner_version": RUNNER_VERSION,
            "run": asdict(run_record),
        }

        output_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return output_path


def main() -> None:
    print("🧪 EXPERIMENT RUNNER v1")
    print("=" * 80)

    input_path = (
        Path("..")
        / "07_OUTPUT"
        / "rc_evidence_adapter_demo_v1.json"
    )

    output_path = (
        Path("..")
        / "07_OUTPUT"
        / "experiment_run_record_demo_v1.json"
    )

    runner = ExperimentRunner()

    try:
        stream = runner.load_state_stream(input_path)
        run_record = runner.build_run_record(stream)
        exported_path = runner.export(run_record, output_path)

    except ExperimentRunnerError as exc:
        print("-" * 80)
        print("EXPERIMENT RUNNER FAILED")
        print(exc)
        print("=" * 80)
        sys.exit(1)

    print(f"Runner:       {runner.runner_name}")
    print(f"Version:      {RUNNER_VERSION}")
    print(f"Input:        {input_path}")
    print(f"Output:       {exported_path}")
    print("-" * 80)
    print(f"Experiment:   {run_record.experiment_id}")
    print(f"Environment:  {run_record.environment}")
    print(f"States:       {run_record.input_state_count}")
    print(f"Accepted:     {run_record.accepted_evidence_count}")
    print(f"Weak:         {run_record.weak_evidence_count}")
    print(f"Uncertain:    {run_record.uncertain_evidence_count}")
    print("-" * 80)
    print(f"Status:       {run_record.run_status}")
    print("=" * 80)
    print("READY")


if __name__ == "__main__":
    main()
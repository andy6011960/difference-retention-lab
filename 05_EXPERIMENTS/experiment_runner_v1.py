# ==================================================================================================
# experiment_runner_v1.py
#
# Difference Retention Laboratory
# Experiment Runner v1.1
#
# Purpose:
#   Run a demo experiment from RC Evidence State and produce an Experiment Run Record
#   with explicit Retention Trace.
#
# Input:
#   07_OUTPUT/rc_evidence_adapter_demo_v1.json
#
# Output:
#   07_OUTPUT/experiment_run_record_demo_v1.json
#
# Run:
#   python 05_EXPERIMENTS/experiment_runner_v1.py
# ==================================================================================================

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_INPUT_PATH = PROJECT_ROOT / "07_OUTPUT" / "rc_evidence_adapter_demo_v1.json"
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "07_OUTPUT" / "experiment_run_record_demo_v1.json"


@dataclass
class TransformationStep:
    step_id: str
    step_type: str
    input_reference: str
    output_reference: str
    description: str
    created_at: str


@dataclass
class RetentionTrace:
    trace_type: str
    version: str
    origin_reference: str
    evidence_reference: str
    state_reference: str
    transformation_history: list[TransformationStep]
    environment_snapshot: dict[str, Any]
    retained_elements: list[str]
    missing_elements: list[str]
    retention_ready: bool


@dataclass
class ExperimentRunRecord:
    record_type: str
    version: str
    experiment_id: str
    created_at: str
    input_path: str
    experiment_status: str
    origin_reference: str
    evidence_reference: str
    rc_evidence_state: dict[str, Any]
    transformation_history: list[TransformationStep]
    environment_snapshot: dict[str, Any]
    retention_trace: RetentionTrace
    conclusion: str


class ExperimentRunnerV1:
    VERSION = "EXPERIMENT_RUNNER_v1.1"

    def load_json(self, input_path: Path) -> dict[str, Any]:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        with input_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("RC Evidence State must be a JSON object.")

        return data

    def export_json(self, payload: dict[str, Any], output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)

        return output_path

    def now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def extract_origin_reference(self, rc_state: dict[str, Any]) -> str:
        for key in (
            "origin_reference",
            "origin_id",
            "origin",
            "source_origin",
            "raw_observation_id",
        ):
            value = rc_state.get(key)

            if isinstance(value, str) and value.strip():
                return value.strip()

            if isinstance(value, dict) and value:
                return json.dumps(value, ensure_ascii=False, sort_keys=True)

        evidence_record = rc_state.get("evidence_record")

        if isinstance(evidence_record, dict):
            for key in (
                "origin_reference",
                "origin_id",
                "origin",
                "source_observation",
                "raw_observation",
            ):
                value = evidence_record.get(key)

                if isinstance(value, str) and value.strip():
                    return value.strip()

                if isinstance(value, dict) and value:
                    return json.dumps(value, ensure_ascii=False, sort_keys=True)

        return "origin_reference_unavailable"

    def extract_evidence_reference(self, rc_state: dict[str, Any]) -> str:
        for key in (
            "evidence_reference",
            "evidence_id",
            "evidence_record_id",
            "record_id",
            "id",
        ):
            value = rc_state.get(key)

            if isinstance(value, str) and value.strip():
                return value.strip()

        evidence_record = rc_state.get("evidence_record")

        if isinstance(evidence_record, dict):
            for key in (
                "evidence_reference",
                "evidence_id",
                "record_id",
                "id",
            ):
                value = evidence_record.get(key)

                if isinstance(value, str) and value.strip():
                    return value.strip()

        return "evidence_reference_unavailable"

    def build_environment_snapshot(self, input_path: Path, output_path: Path) -> dict[str, Any]:
        return {
            "project_root": str(PROJECT_ROOT),
            "runner_path": str(Path(__file__).resolve()),
            "input_path": str(input_path),
            "output_path": str(output_path),
            "created_at": self.now(),
            "environment_type": "local_file_system",
            "laboratory": "Difference Retention Laboratory",
        }

    def build_transformation_history(
        self,
        input_path: Path,
        output_path: Path,
    ) -> list[TransformationStep]:
        return [
            TransformationStep(
                step_id="step_001",
                step_type="load_rc_evidence_state",
                input_reference=str(input_path),
                output_reference="in_memory_rc_evidence_state",
                description="Loaded RC Evidence State from adapter output.",
                created_at=self.now(),
            ),
            TransformationStep(
                step_id="step_002",
                step_type="run_demo_experiment",
                input_reference="in_memory_rc_evidence_state",
                output_reference="experiment_run_record",
                description="Executed demo experiment and preserved structural references for retention analysis.",
                created_at=self.now(),
            ),
            TransformationStep(
                step_id="step_003",
                step_type="export_experiment_run_record",
                input_reference="experiment_run_record",
                output_reference=str(output_path),
                description="Exported Experiment Run Record with Retention Trace.",
                created_at=self.now(),
            ),
        ]

    def build_retention_trace(
        self,
        origin_reference: str,
        evidence_reference: str,
        rc_state: dict[str, Any],
        transformation_history: list[TransformationStep],
        environment_snapshot: dict[str, Any],
    ) -> RetentionTrace:
        missing_elements: list[str] = []

        if origin_reference == "origin_reference_unavailable":
            missing_elements.append("origin_reference")

        if evidence_reference == "evidence_reference_unavailable":
            missing_elements.append("evidence_reference")

        if not transformation_history:
            missing_elements.append("transformation_history")

        if not environment_snapshot:
            missing_elements.append("environment_snapshot")

        retained_elements = [
            element
            for element in (
                "origin_reference",
                "evidence_reference",
                "rc_evidence_state",
                "transformation_history",
                "environment_snapshot",
            )
            if element not in missing_elements
        ]

        return RetentionTrace(
            trace_type="retention_trace",
            version="RETENTION_TRACE_v1",
            origin_reference=origin_reference,
            evidence_reference=evidence_reference,
            state_reference="rc_evidence_state",
            transformation_history=transformation_history,
            environment_snapshot=environment_snapshot,
            retained_elements=retained_elements,
            missing_elements=missing_elements,
            retention_ready=len(missing_elements) == 0,
        )

    def run_experiment(
        self,
        input_path: Path = DEFAULT_INPUT_PATH,
        output_path: Path = DEFAULT_OUTPUT_PATH,
    ) -> ExperimentRunRecord:
        rc_state = self.load_json(input_path)

        origin_reference = self.extract_origin_reference(rc_state)
        evidence_reference = self.extract_evidence_reference(rc_state)
        transformation_history = self.build_transformation_history(
            input_path=input_path,
            output_path=output_path,
        )
        environment_snapshot = self.build_environment_snapshot(
            input_path=input_path,
            output_path=output_path,
        )

        retention_trace = self.build_retention_trace(
            origin_reference=origin_reference,
            evidence_reference=evidence_reference,
            rc_state=rc_state,
            transformation_history=transformation_history,
            environment_snapshot=environment_snapshot,
        )

        experiment_status = "COMPLETED"

        if retention_trace.retention_ready:
            conclusion = (
                "Experiment completed with explicit Retention Trace. "
                "The run record is ready for Retention Analysis."
            )
        else:
            conclusion = (
                "Experiment completed, but Retention Trace is incomplete. "
                "The run record remains analyzable, but retention may be partial."
            )

        return ExperimentRunRecord(
            record_type="experiment_run_record",
            version=self.VERSION,
            experiment_id="experiment_run_demo_v1",
            created_at=self.now(),
            input_path=str(input_path),
            experiment_status=experiment_status,
            origin_reference=origin_reference,
            evidence_reference=evidence_reference,
            rc_evidence_state=rc_state,
            transformation_history=transformation_history,
            environment_snapshot=environment_snapshot,
            retention_trace=retention_trace,
            conclusion=conclusion,
        )

    def run(
        self,
        input_path: Path = DEFAULT_INPUT_PATH,
        output_path: Path = DEFAULT_OUTPUT_PATH,
    ) -> Path:
        record = self.run_experiment(
            input_path=input_path,
            output_path=output_path,
        )

        payload = asdict(record)
        return self.export_json(payload=payload, output_path=output_path)


def main() -> None:
    runner = ExperimentRunnerV1()
    output_path = runner.run()

    print("🧪 EXPERIMENT RUNNER v1.1")
    print("=" * 80)
    print(f"Input:  {DEFAULT_INPUT_PATH}")
    print(f"Output: {output_path}")
    print("Status: READY")
    print("=" * 80)


if __name__ == "__main__":
    main()
# ==================================================================================================
# retention_analysis_layer_v1.py
#
# Difference Retention Laboratory
# Retention Analysis Layer v1.1
#
# Purpose:
#   Analyze an Experiment Run Record and determine what was retained:
#   - origin
#   - evidence state
#   - transformation trace
#   - structural metadata
#
# v1.1:
#   Supports both:
#   - flat Experiment Run Record fields
#   - nested retention_trace fields
#
# Input:
#   ../07_OUTPUT/experiment_run_record_demo_v1.json
#
# Output:
#   retention_report_v1.json
#
# Run:
#   python retention_analysis_layer_v1.py
# ==================================================================================================

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_INPUT_PATH = PROJECT_ROOT / "07_OUTPUT" / "experiment_run_record_demo_v1.json"
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "11_RETENTION_ANALYSIS" / "retention_report_v1.json"


@dataclass
class RetentionCheck:
    name: str
    status: str
    score: float
    explanation: str


@dataclass
class RetentionReport:
    report_type: str
    version: str
    created_at: str
    input_path: str
    retention_status: str
    retention_score: float
    checks: list[RetentionCheck]
    conclusion: str


class RetentionAnalysisLayerV1:
    VERSION = "RETENTION_ANALYSIS_LAYER_v1.1"

    def load_json(self, input_path: Path) -> dict[str, Any]:
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        with input_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Experiment Run Record must be a JSON object.")

        return data

    def is_meaningful_value(self, value: Any) -> bool:
        if value is None:
            return False

        if isinstance(value, str):
            if value.strip() == "":
                return False

            if value.strip().endswith("_unavailable"):
                return False

            return True

        if isinstance(value, (list, dict)):
            return len(value) > 0

        return True

    def get_retention_trace(self, record: dict[str, Any]) -> dict[str, Any]:
        retention_trace = record.get("retention_trace")

        if isinstance(retention_trace, dict):
            return retention_trace

        return {}

    def has_non_empty_value(
        self,
        record: dict[str, Any],
        possible_keys: list[str],
    ) -> bool:
        retention_trace = self.get_retention_trace(record)

        for key in possible_keys:
            if self.is_meaningful_value(record.get(key)):
                return True

            if self.is_meaningful_value(retention_trace.get(key)):
                return True

        return False

    def check_origin_preserved(self, record: dict[str, Any]) -> RetentionCheck:
        possible_keys = [
            "origin",
            "origin_record",
            "origin_gateway",
            "source_observation",
            "raw_observation",
            "parent_origin",
            "origin_reference",
        ]

        if self.has_non_empty_value(record, possible_keys):
            return RetentionCheck(
                name="origin_preserved",
                status="HELD",
                score=1.0,
                explanation="Origin reference is present and meaningful.",
            )

        return RetentionCheck(
            name="origin_preserved",
            status="NOT_HELD",
            score=0.0,
            explanation="No meaningful origin reference was found in the experiment run record or retention trace.",
        )

    def check_evidence_state_present(self, record: dict[str, Any]) -> RetentionCheck:
        possible_keys = [
            "evidence",
            "evidence_record",
            "evidence_state",
            "rc_evidence_state",
            "adapter_output",
            "evidence_reference",
            "state_reference",
        ]

        if self.has_non_empty_value(record, possible_keys):
            return RetentionCheck(
                name="evidence_state_present",
                status="HELD",
                score=1.0,
                explanation="Evidence state or evidence reference is present and meaningful.",
            )

        return RetentionCheck(
            name="evidence_state_present",
            status="NOT_HELD",
            score=0.0,
            explanation="No meaningful evidence state or evidence reference was found.",
        )

    def check_transformation_trace_present(self, record: dict[str, Any]) -> RetentionCheck:
        possible_keys = [
            "transformation",
            "transformation_trace",
            "pipeline_trace",
            "steps",
            "events",
            "run_steps",
            "transformation_history",
        ]

        if self.has_non_empty_value(record, possible_keys):
            return RetentionCheck(
                name="transformation_trace_present",
                status="HELD",
                score=1.0,
                explanation="Transformation history is present and meaningful.",
            )

        return RetentionCheck(
            name="transformation_trace_present",
            status="NOT_HELD",
            score=0.0,
            explanation="No meaningful transformation history was found in the experiment run record or retention trace.",
        )

    def check_environment_context_present(self, record: dict[str, Any]) -> RetentionCheck:
        possible_keys = [
            "environment",
            "environment_snapshot",
            "context",
            "run_context",
        ]

        if self.has_non_empty_value(record, possible_keys):
            return RetentionCheck(
                name="environment_context_present",
                status="HELD",
                score=1.0,
                explanation="Environment context is present and meaningful.",
            )

        return RetentionCheck(
            name="environment_context_present",
            status="NOT_HELD",
            score=0.0,
            explanation="No meaningful environment context was found.",
        )

    def check_final_record_valid(self, record: dict[str, Any]) -> RetentionCheck:
        required_minimum_keys = [
            "record_type",
            "version",
        ]

        missing_keys = [
            key
            for key in required_minimum_keys
            if not self.is_meaningful_value(record.get(key))
        ]

        if not missing_keys:
            return RetentionCheck(
                name="final_record_valid",
                status="HELD",
                score=1.0,
                explanation="Experiment run record contains minimum structural metadata.",
            )

        return RetentionCheck(
            name="final_record_valid",
            status="PARTIALLY_HELD",
            score=0.5,
            explanation=f"Experiment run record is readable, but missing metadata keys: {missing_keys}",
        )

    def determine_retention_status(self, checks: list[RetentionCheck]) -> str:
        scores = [check.score for check in checks]

        if all(score >= 1.0 for score in scores):
            return "HELD"

        if any(score > 0.0 for score in scores):
            return "PARTIALLY_HELD"

        return "NOT_HELD"

    def build_conclusion(self, retention_status: str, retention_score: float) -> str:
        if retention_status == "HELD":
            return (
                "Difference retention is preserved. Origin, evidence state, "
                "transformation history, environment context, and structural metadata "
                "remain available for interpretation."
            )

        if retention_status == "PARTIALLY_HELD":
            return (
                "Difference retention is partial. Some structural elements remain available, "
                "but the experiment record does not yet fully preserve the retention chain."
            )

        return (
            "Difference retention is not preserved. The experiment record does not contain "
            "enough structure to support retention analysis."
        )

    def analyze(self, input_path: Path = DEFAULT_INPUT_PATH) -> RetentionReport:
        record = self.load_json(input_path)

        checks = [
            self.check_origin_preserved(record),
            self.check_evidence_state_present(record),
            self.check_transformation_trace_present(record),
            self.check_environment_context_present(record),
            self.check_final_record_valid(record),
        ]

        retention_score = round(
            sum(check.score for check in checks) / len(checks),
            3,
        )

        retention_status = self.determine_retention_status(checks)

        return RetentionReport(
            report_type="retention_report",
            version=self.VERSION,
            created_at=datetime.now().isoformat(timespec="seconds"),
            input_path=str(input_path),
            retention_status=retention_status,
            retention_score=retention_score,
            checks=checks,
            conclusion=self.build_conclusion(retention_status, retention_score),
        )

    def export_report(
        self,
        report: RetentionReport,
        output_path: Path = DEFAULT_OUTPUT_PATH,
    ) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        payload = asdict(report)

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)

        return output_path

    def run(
        self,
        input_path: Path = DEFAULT_INPUT_PATH,
        output_path: Path = DEFAULT_OUTPUT_PATH,
    ) -> Path:
        report = self.analyze(input_path=input_path)
        return self.export_report(report=report, output_path=output_path)


def main() -> None:
    layer = RetentionAnalysisLayerV1()
    output_path = layer.run()

    print("🧠 RETENTION ANALYSIS LAYER v1.1")
    print("=" * 80)
    print(f"Input:  {DEFAULT_INPUT_PATH}")
    print(f"Output: {output_path}")
    print("Status: READY")
    print("=" * 80)


if __name__ == "__main__":
    main()
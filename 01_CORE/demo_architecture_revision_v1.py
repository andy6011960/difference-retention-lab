# ==================================================================================================
# demo_architecture_revision_v1.py
#
# Difference Retention Laboratory
# Demo Architecture Revision v1
#
# Version : 1.3
# Status  : DIAGNOSTIC / NO PHYSICS / NO MUTATION
#
# Назначение:
#   Внешняя ревизия архитектуры Book Environment Core.
#
# ==================================================================================================


from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import json

from demo_environment import build_demo_environment


@dataclass
class RevisionCheck:
    name: str
    passed: bool
    details: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "details": self.details,
        }


@dataclass
class RevisionReport:
    revision_id: str
    core_verdict: str
    gen_2_status: str
    gen_2_verdict: str
    checks: list[RevisionCheck] = field(default_factory=list)

    def passed_count(self) -> int:
        return sum(1 for check in self.checks if check.passed)

    def failed_count(self) -> int:
        return sum(1 for check in self.checks if not check.passed)

    def to_dict(self) -> dict[str, Any]:
        return {
            "revision_id": self.revision_id,
            "core_verdict": self.core_verdict,
            "gen_2_status": self.gen_2_status,
            "gen_2_verdict": self.gen_2_verdict,
            "passed_count": self.passed_count(),
            "failed_count": self.failed_count(),
            "checks": [check.to_dict() for check in self.checks],
        }


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def add_check(
    checks: list[RevisionCheck],
    name: str,
    passed: bool,
    details: str,
) -> None:
    checks.append(
        RevisionCheck(
            name=name,
            passed=passed,
            details=details,
        )
    )


def run_revision() -> RevisionReport:
    checks: list[RevisionCheck] = []

    env = build_demo_environment()

    add_check(checks, "ENVIRONMENT_CREATED", env is not None, "Demo environment was created.")
    add_check(checks, "BOOK_ID_PRESENT", bool(env.book_id), f"book_id={env.book_id}")
    add_check(checks, "TITLE_PRESENT", bool(env.title), f"title={env.title}")

    add_check(
        checks,
        "INVARIANT_PRESENT",
        env.invariant is not None,
        f"invariant={getattr(env.invariant, 'name', '')}",
    )

    add_check(
        checks,
        "INVARIANT_INTERFACE",
        hasattr(env.invariant, "evaluate"),
        "Invariant exposes evaluate(state).",
    )

    add_check(
        checks,
        "PAGES_REGISTERED",
        len(env.pages) == 2,
        f"pages={list(env.pages.keys())}",
    )

    add_check(
        checks,
        "INITIAL_PAGE_SET",
        bool(env.state.page_id) and env.state.page_id in env.pages,
        f"initial_page={env.state.page_id}",
    )

    add_check(
        checks,
        "SPINES_REGISTERED",
        len(env.spines) == 2,
        f"spines={[spine.spine_id for spine in env.spines]}",
    )

    add_check(
        checks,
        "SPINE_ENDPOINTS_VALID",
        all(
            spine.from_page in env.pages and spine.to_page in env.pages
            for spine in env.spines
        ),
        "All spine endpoints point to registered pages.",
    )

    add_check(
        checks,
        "OBSERVER_PRESENT",
        env.observer is not None,
        "Observer object exists.",
    )

    add_check(
        checks,
        "TRANSITION_ENGINE_PRESENT",
        hasattr(env, "transition_engine") and env.transition_engine is not None,
        (
            f"engine={type(env.transition_engine).__name__}"
            if hasattr(env, "transition_engine")
            else "engine=missing"
        ),
    )

    add_check(
        checks,
        "TRANSITION_ENGINE_INTERFACE",
        hasattr(env.transition_engine, "execute_transition")
        if hasattr(env, "transition_engine")
        else False,
        "TransitionEngine exposes execute_transition(...).",
    )

    add_check(
        checks,
        "RETENTION_ENGINE_PRESENT",
        hasattr(env, "retention_engine") and env.retention_engine is not None,
        (
            f"engine={type(env.retention_engine).__name__}"
            if hasattr(env, "retention_engine")
            else "engine=missing"
        ),
    )

    add_check(
        checks,
        "RETENTION_ENGINE_INTERFACE",
        hasattr(env.retention_engine, "evaluate_retention")
        if hasattr(env, "retention_engine")
        else False,
        "RetentionEngine exposes evaluate_retention(...).",
    )

    add_check(
        checks,
        "MEMORY_ENGINE_PRESENT",
        hasattr(env, "memory_engine") and env.memory_engine is not None,
        (
            f"engine={type(env.memory_engine).__name__}"
            if hasattr(env, "memory_engine")
            else "engine=missing"
        ),
    )

    add_check(
        checks,
        "MEMORY_ENGINE_INTERFACE",
        hasattr(env.memory_engine, "remember")
        if hasattr(env, "memory_engine")
        else False,
        "MemoryEngine exposes remember(...).",
    )

    add_check(
        checks,
        "TOPOLOGY_ENGINE_PRESENT",
        hasattr(env, "topology_engine") and env.topology_engine is not None,
        (
            f"engine={type(env.topology_engine).__name__}"
            if hasattr(env, "topology_engine")
            else "engine=missing"
        ),
    )

    add_check(
        checks,
        "TOPOLOGY_ENGINE_INTERFACE",
        hasattr(env.topology_engine, "validate")
        if hasattr(env, "topology_engine")
        else False,
        "TopologyEngine exposes validate(...).",
    )

    if hasattr(env, "topology_engine"):
        topology_report = env.topology_engine.validate(
            pages=env.pages,
            spines=env.spines,
        )

        add_check(
            checks,
            "TOPOLOGY_VALID",
            topology_report.valid,
            topology_report.details,
        )
    else:
        add_check(
            checks,
            "TOPOLOGY_VALID",
            False,
            "TopologyEngine missing.",
        )

    add_check(
        checks,
        "JOURNAL_PRESENT",
        env.journal is not None,
        "Journal object exists.",
    )

    add_check(
        checks,
        "STATE_PRESENT",
        env.state is not None,
        "BookState object exists.",
    )

    final_state = env.run(max_steps=30)

    add_check(
        checks,
        "RUN_COMPLETED",
        final_state is not None,
        "Demo run completed.",
    )

    add_check(
        checks,
        "FINAL_STATE_ALIVE",
        final_state.alive is True,
        f"alive={final_state.alive}",
    )

    add_check(
        checks,
        "TAU_I_EXPECTED",
        final_state.tau_i == 30.0,
        f"tau_i={final_state.tau_i}",
    )

    add_check(
        checks,
        "TRANSITIONS_EXPECTED",
        final_state.transition_count == 7,
        f"transition_count={final_state.transition_count}",
    )

    add_check(
        checks,
        "ORIENTATION_SWITCHES_EXPECTED",
        final_state.orientation_switch_count == 21,
        f"orientation_switch_count={final_state.orientation_switch_count}",
    )

    add_check(
        checks,
        "OBSERVER_SNAPSHOTS_EXPECTED",
        len(env.observer.snapshots) == 30,
        f"snapshots={len(env.observer.snapshots)}",
    )

    add_check(
        checks,
        "MEMORY_RECORDS_EXPECTED",
        len(env.memory_engine.trace.records) == 30
        if hasattr(env, "memory_engine")
        else False,
        (
            f"records={len(env.memory_engine.trace.records)}"
            if hasattr(env, "memory_engine")
            else "records=missing"
        ),
    )

    add_check(
        checks,
        "JOURNAL_EVENTS_PRESENT",
        len(env.journal.events) > 0,
        f"events={len(env.journal.events)}",
    )

    output_path = Path("output") / "demo_architecture_revision_v1.json"
    exported_environment_path = Path("output") / "book_environment_demo_revision_v1.json"

    env.export(exported_environment_path)

    add_check(
        checks,
        "ENVIRONMENT_EXPORT_CREATED",
        exported_environment_path.exists(),
        f"export={exported_environment_path}",
    )

    all_passed = all(check.passed for check in checks)

    core_verdict = (
        "CORE_GEN_1_READY"
        if all_passed
        else "CORE_GEN_1_NOT_READY"
    )

    gen_2_status = (
        "GEN_2_PROGRESS_4_OF_4"
        if all_passed
        else "GEN_2_PROGRESS_BLOCKED"
    )

    gen_2_verdict = (
        "CORE_GEN_2_READY"
        if all_passed
        else "CORE_GEN_2_NOT_READY"
    )

    report = RevisionReport(
        revision_id="DEMO_ARCHITECTURE_REVISION_v1_3",
        core_verdict=core_verdict,
        gen_2_status=gen_2_status,
        gen_2_verdict=gen_2_verdict,
        checks=checks,
    )

    ensure_dir(output_path.parent)

    output_path.write_text(
        json.dumps(report.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return report


def main() -> None:
    print("🔍 DEMO ARCHITECTURE REVISION v1.3")
    print("=" * 80)

    report = run_revision()

    for check in report.checks:
        marker = "✅" if check.passed else "❌"
        print(f"{marker} {check.name}: {check.details}")

    print("-" * 80)
    print(f"PASSED:        {report.passed_count()}")
    print(f"FAILED:        {report.failed_count()}")
    print(f"CORE VERDICT:  {report.core_verdict}")
    print(f"GEN 2 STATUS:  {report.gen_2_status}")
    print(f"GEN 2 VERDICT: {report.gen_2_verdict}")
    print("=" * 80)

    if (
        report.core_verdict == "CORE_GEN_1_READY"
        and report.gen_2_status == "GEN_2_PROGRESS_4_OF_4"
        and report.gen_2_verdict == "CORE_GEN_2_READY"
    ):
        print("READY")
    else:
        print("NOT READY")


if __name__ == "__main__":
    main()
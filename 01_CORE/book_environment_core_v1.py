# ==================================================================================================
# book_environment_core_v1.py
#
# Difference Retention Laboratory
# Book Environment Core v1.2
#
# Version : 1.2
# Status  : ARCHITECTURAL CORE / NO PHYSICS
#
# Requires:
#   state.py
#   page.py
#   journal.py
#   invariant.py
#
# Назначение:
#   Универсальное ядро книги сред удерживаемого различия.
#
# Принцип:
#   Ядро больше не содержит собственной реализации Invariant.
#   Invariant вынесен в invariant.py и является отдельным архитектурным объектом.
#
# ==================================================================================================


from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Callable
import json

from state import BookState
from page import Page
from journal import Journal, now_iso
from invariant import BaseInvariant, InvariantResult
from observer import Observer
from spine import Spine
from transition_engine import TransitionEngine
from retention_engine import RetentionEngine
from memory_engine import MemoryEngine
from topology_engine import TopologyEngine


# ==================================================================================================
# UTILITIES
# ==================================================================================================


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


# ==================================================================================================
# BOOK ENVIRONMENT
# ==================================================================================================


@dataclass
class BookEnvironment:
    book_id: str
    title: str
    invariant: BaseInvariant

    pages: dict[str, Page] = field(default_factory=dict)
    spines: list[Spine] = field(default_factory=list)

    journal: Journal = field(default_factory=Journal)
    observer: Observer = field(default_factory=Observer)
    transition_engine: TransitionEngine = field(default_factory=TransitionEngine)
    retention_engine: RetentionEngine = field(default_factory=RetentionEngine)
    memory_engine: MemoryEngine = field(default_factory=MemoryEngine)
    topology_engine: TopologyEngine = field(default_factory=TopologyEngine)

    state: BookState = field(default_factory=BookState)

    def register_page(self, page: Page, initial: bool = False) -> None:
        if page.page_id in self.pages:
            raise ValueError(f"Page already registered: {page.page_id}")

        self.pages[page.page_id] = page

        self.journal.record(
            event_type="PAGE_REGISTERED",
            message=f"Page registered: {page.page_id}",
            data={
                "page_id": page.page_id,
                "title": page.title,
                "description": page.description,
                "parameters": page.parameters,
            },
        )

        if initial:
            self.state.page_id = page.page_id
            self.state.previous_page_id = ""

            self.journal.record(
                event_type="INITIAL_PAGE_SET",
                message=f"Initial page set: {page.page_id}",
                data={"page_id": page.page_id},
            )

    def register_spine(self, spine: Spine) -> None:
        if spine.from_page not in self.pages:
            raise ValueError(f"Spine source page not registered: {spine.from_page}")

        if spine.to_page not in self.pages:
            raise ValueError(f"Spine target page not registered: {spine.to_page}")

        self.spines.append(spine)

        self.journal.record(
            event_type="SPINE_REGISTERED",
            message=f"Spine registered: {spine.spine_id}",
            data={
                "spine_id": spine.spine_id,
                "from_page": spine.from_page,
                "to_page": spine.to_page,
                "description": spine.description,
            },
        )

    def initialize_state(
        self,
        delta: float,
        dt: float = 1.0,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if not self.state.page_id:
            raise ValueError("Cannot initialize state: no initial page set.")

        initial_page_id = self.state.page_id

        self.state.reset_runtime(
            delta=delta,
            dt=dt,
            metadata=metadata,
        )

        self.state.page_id = initial_page_id
        self.state.previous_page_id = ""

        self.journal.record(
            event_type="STATE_INITIALIZED",
            message="Book state initialized.",
            data=self.state.to_dict(),
        )

    def step(self) -> BookState:
        if not self.state.alive:
            return self.state

        topology_report = self.topology_engine.validate(
            pages=self.pages,
            spines=self.spines,
        )

        if not topology_report.valid:
            self.state.mark_dead()

            self.journal.record(
                event_type="TOPOLOGY_INVALID",
                message=topology_report.details,
                data=topology_report.to_dict(),
            )

            return self.state

        current_page = self._current_page()

        old_orientation = self.state.orientation

        self.state = current_page.step(self.state)

        if self.state.orientation != old_orientation:
            self.journal.record(
                event_type="ORIENTATION_SWITCH",
                message="Orientation changed during local page dynamics.",
                data={
                    "step_index": self.state.step_index,
                    "time": self.state.time,
                    "from_orientation": old_orientation,
                    "to_orientation": self.state.orientation,
                    "delta": self.state.delta,
                    "page_id": self.state.page_id,
                },
            )

        transition_result = self.transition_engine.execute_transition(
            state=self.state,
            pages=self.pages,
            spines=self.spines,
        )

        self.state = transition_result.state

        if transition_result.occurred:
            self.journal.record(
                event_type="PAGE_TRANSITION",
                message=transition_result.details,
                data={
                    "spine_id": transition_result.spine_id,
                    "from_page": transition_result.from_page,
                    "to_page": transition_result.to_page,
                    "step_index": self.state.step_index,
                    "time": self.state.time,
                    "delta": self.state.delta,
                    "orientation": self.state.orientation,
                    "orientation_changed": transition_result.orientation_changed,
                    "book_age": self.state.book_age,
                    "page_age": self.state.page_age,
                },
            )

        invariant_result = self.invariant.evaluate(self.state)

        retention_result = self.retention_engine.evaluate_retention(
            state=self.state,
            invariant_result=invariant_result,
        )

        self.state = retention_result.state

        if not retention_result.retained:
            self.journal.record(
                event_type="INVARIANT_LOST",
                message=retention_result.reason,
                data={
                    "step_index": self.state.step_index,
                    "time": self.state.time,
                    "delta": retention_result.value,
                    "value": retention_result.value,
                    "threshold": retention_result.threshold,
                },
            )

        self.memory_engine.remember(
            state=self.state,
            invariant_result=invariant_result,
            transition_result=transition_result,
            retention_result=retention_result,
        )

        self.observer.observe(
            self.state,
            invariant_result,
        )

        self.state.advance_time()

        return self.state

    def run(self, max_steps: int = 100) -> BookState:
        self.journal.record(
            event_type="RUN_STARTED",
            message="Book environment run started.",
            data={"max_steps": max_steps},
        )

        for _ in range(max_steps):
            if not self.state.alive:
                break

            self.step()

        self.journal.record(
            event_type="RUN_FINISHED",
            message="Book environment run finished.",
            data={
                "final_state": self.state.to_dict(),
                "snapshots_count": len(self.observer.snapshots),
                "events_count": len(self.journal.events),
            },
        )

        return self.state

    def export(self, output_path: str | Path) -> Path:
        output_path = Path(output_path)
        ensure_dir(output_path.parent)

        data = {
            "book_id": self.book_id,
            "title": self.title,
            "exported_at": now_iso(),
            "invariant": {
                "name": self.invariant.name,
                "threshold": self.invariant.threshold,
            },
            "pages": {
                page_id: {
                    "page_id": page.page_id,
                    "title": page.title,
                    "description": page.description,
                    "parameters": page.parameters,
                }
                for page_id, page in self.pages.items()
            },
            "spines": [
                {
                    "spine_id": spine.spine_id,
                    "from_page": spine.from_page,
                    "to_page": spine.to_page,
                    "description": spine.description,
                }
                for spine in self.spines
            ],
            "final_state": self.state.to_dict(),
            "observer": self.observer.to_dict(),
            "journal": self.journal.to_dict(),
        }

        output_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return output_path

    def _current_page(self) -> Page:
        if self.state.page_id not in self.pages:
            raise ValueError(f"Current page not registered: {self.state.page_id}")

        return self.pages[self.state.page_id]

# ==================================================================================================
# SELF TEST
# ==================================================================================================


def main() -> None:
    from demo_environment import build_demo_environment

    print("📘 BOOK ENVIRONMENT CORE v1.2")
    print("=" * 80)

    env = build_demo_environment()
    final_state = env.run(max_steps=30)

    output_path = Path("output") / "book_environment_demo_v1_2.json"
    exported = env.export(output_path)

    print(f"Book:        {env.title}")
    print(f"Final page:  {final_state.page_id}")
    print(f"Alive:       {final_state.alive}")
    print(f"tau_I:       {final_state.tau_i}")
    print(f"delta:       {final_state.delta:.6f}")
    print(f"orientation: {final_state.orientation}")
    print(f"book_age:    {final_state.book_age}")
    print(f"page_age:    {final_state.page_age}")
    print(f"transitions: {final_state.transition_count}")
    print(f"switches:    {final_state.orientation_switch_count}")
    print(f"Output:      {exported}")
    print("=" * 80)
    print("READY")


if __name__ == "__main__":
    main()
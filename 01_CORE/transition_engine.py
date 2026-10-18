# ==================================================================================================
# transition_engine.py
#
# Difference Retention Laboratory
# Transition Engine v1
#
# Version : 1.0
# Status  : CORE PROCESS ENGINE / NO PHYSICS
#
# Назначение:
#   Движок переходов между страницами Book Environment.
#
# Принцип:
#   TransitionEngine не выполняет локальную динамику страниц.
#   TransitionEngine не вычисляет инварианты.
#   TransitionEngine не наблюдает и не пишет журнал.
#
#   Его единственная обязанность:
#       найти допустимый Spine
#       и реализовать переход через него.
#
# ==================================================================================================


from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from state import BookState
from page import Page
from spine import Spine


# ==================================================================================================
# TRANSITION RESULT
# ==================================================================================================


@dataclass
class TransitionResult:
    occurred: bool
    spine_id: str
    from_page: str
    to_page: str
    orientation_changed: bool
    state: BookState
    details: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "occurred": self.occurred,
            "spine_id": self.spine_id,
            "from_page": self.from_page,
            "to_page": self.to_page,
            "orientation_changed": self.orientation_changed,
            "state": self.state.to_dict(),
            "details": self.details,
        }


# ==================================================================================================
# TRANSITION ENGINE
# ==================================================================================================


@dataclass
class TransitionEngine:
    name: str = "TRANSITION_ENGINE_v1"

    def find_triggered_spine(
        self,
        state: BookState,
        spines: list[Spine],
    ) -> Spine | None:
        for spine in spines:
            if spine.from_page != state.page_id:
                continue

            if spine.is_triggered(state):
                return spine

        return None

    def execute_transition(
        self,
        state: BookState,
        pages: dict[str, Page],
        spines: list[Spine],
    ) -> TransitionResult:
        triggered_spine = self.find_triggered_spine(
            state=state,
            spines=spines,
        )

        if triggered_spine is None:
            return TransitionResult(
                occurred=False,
                spine_id="",
                from_page=state.page_id,
                to_page=state.page_id,
                orientation_changed=False,
                state=state,
                details="No transition triggered.",
            )

        if triggered_spine.to_page not in pages:
            raise ValueError(
                f"Transition target page not registered: {triggered_spine.to_page}"
            )

        old_page = state.page_id
        old_orientation = state.orientation

        state = triggered_spine.transition(state)

        return TransitionResult(
            occurred=True,
            spine_id=triggered_spine.spine_id,
            from_page=old_page,
            to_page=state.page_id,
            orientation_changed=state.orientation != old_orientation,
            state=state,
            details=f"Transition executed: {old_page} -> {state.page_id}",
        )
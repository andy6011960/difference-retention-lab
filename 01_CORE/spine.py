# ==================================================================================================
# spine.py
#
# Difference Retention Laboratory
# Spine Module v1
#
# Version : 1.0
# Status  : CORE MODULE / NO PHYSICS
#
# Назначение:
#   Переходы между страницами Book Environment.
#
# Принцип:
#   Spine не является страницей и не является средой.
#   Spine — это условие перехода и действие перехода.
#
# ==================================================================================================


from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from state import BookState


# ==================================================================================================
# TYPES
# ==================================================================================================


BoundaryCondition = Callable[[BookState], bool]
TransitionAction = Callable[[BookState], BookState]


# ==================================================================================================
# SPINE
# ==================================================================================================


@dataclass
class Spine:
    spine_id: str
    from_page: str
    to_page: str
    condition: BoundaryCondition
    action: TransitionAction | None = None
    description: str = ""

    def is_triggered(self, state: BookState) -> bool:
        return self.condition(state)

    def transition(self, state: BookState) -> BookState:
        if self.action is not None:
            state = self.action(state)

        state.mark_page_transition(self.to_page)

        return state
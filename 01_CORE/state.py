# ==================================================================================================
# state.py
#
# Difference Retention Laboratory
# Book Environment State v1
#
# Version : 1.0
# Status  : CORE MODULE / NO PHYSICS
#
# Назначение:
#   Универсальное состояние книги среды удерживаемого различия.
#
# Принцип:
#   State не знает физику.
#   State хранит только текущее положение среды в книге:
#       - время
#       - страница
#       - различие
#       - ориентация
#       - tau_I
#       - счётчики
#       - возраст книги
#       - возраст страницы
#       - metadata
#
# ==================================================================================================


from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any
import copy


@dataclass
class BookState:
    step_index: int = 0
    time: float = 0.0
    dt: float = 1.0

    page_id: str = ""
    previous_page_id: str = ""

    alive: bool = True

    delta: float = 0.0
    previous_delta: float = 0.0

    orientation: int = 0
    previous_orientation: int = 0

    tau_i: float = 0.0

    transition_count: int = 0
    orientation_switch_count: int = 0

    book_age: float = 0.0
    page_age: float = 0.0

    metadata: dict[str, Any] = field(default_factory=dict)

    def clone(self) -> "BookState":
        return copy.deepcopy(self)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def reset_runtime(
        self,
        delta: float,
        dt: float = 1.0,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.step_index = 0
        self.time = 0.0
        self.dt = dt

        self.alive = True

        self.delta = delta
        self.previous_delta = delta

        self.orientation = self.compute_orientation(delta)
        self.previous_orientation = self.orientation

        self.tau_i = 0.0

        self.transition_count = 0
        self.orientation_switch_count = 0

        self.book_age = 0.0
        self.page_age = 0.0

        self.metadata = metadata or {}

    def advance_time(self) -> None:
        self.step_index += 1
        self.time += self.dt
        self.book_age += self.dt
        self.page_age += self.dt

    def mark_page_transition(self, new_page_id: str) -> None:
        self.previous_page_id = self.page_id
        self.page_id = new_page_id
        self.transition_count += 1
        self.page_age = 0.0

    def update_delta(self, new_delta: float) -> None:
        self.previous_delta = self.delta
        self.previous_orientation = self.orientation

        self.delta = new_delta
        self.orientation = self.compute_orientation(new_delta)

        if self.orientation != self.previous_orientation:
            self.orientation_switch_count += 1

    def mark_invariant_preserved(self) -> None:
        self.tau_i += self.dt

    def mark_dead(self) -> None:
        self.alive = False

    @staticmethod
    def compute_orientation(delta: float) -> int:
        if delta > 0:
            return 1

        if delta < 0:
            return -1

        return 0
# ==================================================================================================
# page.py
#
# Difference Retention Laboratory
# Book Environment Page v1
#
# Version : 1.0
# Status  : CORE MODULE / NO PHYSICS
#
# Назначение:
#   Универсальная страница книги среды удерживаемого различия.
#
# Принцип:
#   Page не знает физику.
#   Page знает только:
#       - собственный ID
#       - название
#       - описание
#       - параметры
#       - локальную функцию шага
#       - локальные возможности
#       - счётчик посещений
#
# ==================================================================================================


from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Callable

from state import BookState


LocalStepFunction = Callable[[BookState], BookState]


@dataclass
class Page:
    page_id: str
    title: str
    description: str = ""

    local_step: LocalStepFunction | None = None

    parameters: dict[str, Any] = field(default_factory=dict)
    capabilities: list[str] = field(default_factory=list)

    visit_count: int = 0
    total_time: float = 0.0

    def step(self, state: BookState) -> BookState:
        self.visit_count += 1
        self.total_time += state.dt

        if self.local_step is None:
            return state

        return self.local_step(state)

    def has_capability(self, capability: str) -> bool:
        return capability in self.capabilities

    def to_dict(self) -> dict[str, Any]:
        return {
            "page_id": self.page_id,
            "title": self.title,
            "description": self.description,
            "parameters": dict(self.parameters),
            "capabilities": list(self.capabilities),
            "visit_count": self.visit_count,
            "total_time": self.total_time,
        }

    @classmethod
    def passive(
        cls,
        page_id: str,
        title: str,
        description: str = "",
        parameters: dict[str, Any] | None = None,
        capabilities: list[str] | None = None,
    ) -> "Page":
        return cls(
            page_id=page_id,
            title=title,
            description=description,
            local_step=None,
            parameters=parameters or {},
            capabilities=capabilities or [],
        )
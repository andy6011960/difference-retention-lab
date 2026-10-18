# ==================================================================================================
# observer.py
#
# Difference Retention Laboratory
# Observer Module v1
#
# Version : 1.0
# Status  : CORE MODULE / NO PHYSICS
#
# Назначение:
#   Наблюдатель состояния Book Environment.
#
# Принцип:
#   Observer ничего не меняет в среде.
#   Он только фиксирует снимки состояния после проверки инварианта.
#
# ==================================================================================================


from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

from state import BookState
from invariant import InvariantResult


# ==================================================================================================
# OBSERVER
# ==================================================================================================


@dataclass
class Observer:
    snapshots: list[dict[str, Any]] = field(default_factory=list)

    def observe(self, state: BookState, invariant_result: InvariantResult) -> None:
        self.snapshots.append(
            {
                "step_index": state.step_index,
                "time": state.time,
                "dt": state.dt,
                "page_id": state.page_id,
                "previous_page_id": state.previous_page_id,
                "alive": state.alive,
                "delta": state.delta,
                "previous_delta": state.previous_delta,
                "orientation": state.orientation,
                "previous_orientation": state.previous_orientation,
                "tau_i": state.tau_i,
                "transition_count": state.transition_count,
                "orientation_switch_count": state.orientation_switch_count,
                "book_age": state.book_age,
                "page_age": state.page_age,
                "invariant": asdict(invariant_result),
                "metadata": dict(state.metadata),
            }
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshots_count": len(self.snapshots),
            "snapshots": self.snapshots,
        }
# ==================================================================================================
# retention_engine.py
#
# Difference Retention Laboratory
# Retention Engine v1
#
# Version : 1.0
# Status  : CORE PROCESS ENGINE / NO PHYSICS
#
# Назначение:
#   Движок удержания среды.
#
# Принцип:
#   RetentionEngine не вычисляет инвариант.
#   RetentionEngine не выполняет локальную динамику.
#   RetentionEngine не выполняет переходы.
#   RetentionEngine не наблюдает и не пишет журнал.
#
#   Его единственная обязанность:
#       интерпретировать результат проверки инварианта
#       как продолжение жизни среды
#       или потерю удержания.
#
# ==================================================================================================


from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from state import BookState
from invariant import InvariantResult


# ==================================================================================================
# RETENTION RESULT
# ==================================================================================================


@dataclass
class RetentionResult:
    retained: bool
    alive: bool
    value: float
    threshold: float
    state: BookState
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "retained": self.retained,
            "alive": self.alive,
            "value": self.value,
            "threshold": self.threshold,
            "state": self.state.to_dict(),
            "reason": self.reason,
        }


# ==================================================================================================
# RETENTION ENGINE
# ==================================================================================================


@dataclass
class RetentionEngine:
    name: str = "RETENTION_ENGINE_v1"

    def evaluate_retention(
        self,
        state: BookState,
        invariant_result: InvariantResult,
    ) -> RetentionResult:
        if invariant_result.preserved:
            state.mark_invariant_preserved()

            return RetentionResult(
                retained=True,
                alive=state.alive,
                value=invariant_result.value,
                threshold=invariant_result.threshold,
                state=state,
                reason=invariant_result.reason,
            )

        state.mark_dead()

        return RetentionResult(
            retained=False,
            alive=state.alive,
            value=invariant_result.value,
            threshold=invariant_result.threshold,
            state=state,
            reason=invariant_result.reason,
        )
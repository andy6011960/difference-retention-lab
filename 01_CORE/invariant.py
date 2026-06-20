# ==================================================================================================
# invariant.py
#
# Difference Retention Laboratory
# Invariant Module v1
#
# Version : 1.0
# Status  : CORE MODULE / NO PHYSICS
#
# Назначение:
#     Универсальная система проверки инвариантов среды.
#
# Принцип:
#     Invariant ничего не знает о физике.
#     Он умеет только оценивать:
#
#         сохранён инвариант
#         или
#         потерян.
#
# ==================================================================================================

from __future__ import annotations

from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

from state import BookState


# ==================================================================================================
# RESULT
# ==================================================================================================


@dataclass
class InvariantResult:
    preserved: bool
    value: float
    threshold: float
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)


# ==================================================================================================
# ABSTRACT INVARIANT
# ==================================================================================================


class BaseInvariant(ABC):

    name: str

    @abstractmethod
    def evaluate(self, state: BookState) -> InvariantResult:
        pass


# ==================================================================================================
# DELTA INVARIANT
# ==================================================================================================


@dataclass
class DeltaInvariant(BaseInvariant):

    name: str = "DELTA_RETENTION_INVARIANT"

    threshold: float = 0.01

    def evaluate(self, state: BookState) -> InvariantResult:

        value = abs(state.delta)

        preserved = value >= self.threshold

        if preserved:

            reason = (
                "Invariant preserved: "
                "|delta| >= threshold."
            )

        else:

            reason = (
                "Invariant lost: "
                "|delta| < threshold."
            )

        return InvariantResult(
            preserved=preserved,
            value=value,
            threshold=self.threshold,
            reason=reason,
        )
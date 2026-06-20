# ==================================================================================================
# memory_engine.py
#
# Difference Retention Laboratory
# Memory Engine v1
#
# Version : 1.0
# Status  : CORE PROCESS ENGINE / NO PHYSICS
#
# Назначение:
#   Движок памяти среды.
#
# Принцип:
#   MemoryEngine не является журналом.
#   MemoryEngine не является наблюдателем.
#   MemoryEngine не выполняет локальную динамику.
#   MemoryEngine не выполняет переходы.
#   MemoryEngine не решает, жива ли среда.
#
#   Его обязанность:
#       сохранять значимые следы выполнения,
#       пригодные для последующей интерпретации.
#
# ==================================================================================================


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from state import BookState
from invariant import InvariantResult
from transition_engine import TransitionResult
from retention_engine import RetentionResult


# ==================================================================================================
# MEMORY RECORD
# ==================================================================================================


@dataclass
class MemoryRecord:
    step_index: int
    time: float
    page_id: str
    delta: float
    orientation: int
    tau_i: float
    retained: bool
    alive: bool
    transition_occurred: bool
    transition_spine_id: str
    transition_from_page: str
    transition_to_page: str
    invariant_value: float
    invariant_threshold: float
    reason: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "step_index": self.step_index,
            "time": self.time,
            "page_id": self.page_id,
            "delta": self.delta,
            "orientation": self.orientation,
            "tau_i": self.tau_i,
            "retained": self.retained,
            "alive": self.alive,
            "transition_occurred": self.transition_occurred,
            "transition_spine_id": self.transition_spine_id,
            "transition_from_page": self.transition_from_page,
            "transition_to_page": self.transition_to_page,
            "invariant_value": self.invariant_value,
            "invariant_threshold": self.invariant_threshold,
            "reason": self.reason,
            "metadata": dict(self.metadata),
        }


# ==================================================================================================
# MEMORY TRACE
# ==================================================================================================


@dataclass
class MemoryTrace:
    records: list[MemoryRecord] = field(default_factory=list)

    def append(self, record: MemoryRecord) -> None:
        self.records.append(record)

    def to_dict(self) -> dict[str, Any]:
        return {
            "records_count": len(self.records),
            "records": [
                record.to_dict()
                for record in self.records
            ],
        }


# ==================================================================================================
# MEMORY ENGINE
# ==================================================================================================


@dataclass
class MemoryEngine:
    name: str = "MEMORY_ENGINE_v1"
    trace: MemoryTrace = field(default_factory=MemoryTrace)

    def remember(
        self,
        state: BookState,
        invariant_result: InvariantResult,
        transition_result: TransitionResult,
        retention_result: RetentionResult,
    ) -> MemoryRecord:
        reason = retention_result.reason

        if transition_result.occurred:
            reason = f"{transition_result.details} | {retention_result.reason}"

        record = MemoryRecord(
            step_index=state.step_index,
            time=state.time,
            page_id=state.page_id,
            delta=state.delta,
            orientation=state.orientation,
            tau_i=state.tau_i,
            retained=retention_result.retained,
            alive=retention_result.alive,
            transition_occurred=transition_result.occurred,
            transition_spine_id=transition_result.spine_id,
            transition_from_page=transition_result.from_page,
            transition_to_page=transition_result.to_page,
            invariant_value=invariant_result.value,
            invariant_threshold=invariant_result.threshold,
            reason=reason,
            metadata=dict(state.metadata),
        )

        self.trace.append(record)

        return record

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "trace": self.trace.to_dict(),
        }
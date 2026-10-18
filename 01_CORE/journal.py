# ==================================================================================================
# journal.py
#
# Difference Retention Laboratory
# Book Environment Journal v1
#
# Version : 1.0
# Status  : CORE MODULE / NO PHYSICS
#
# Назначение:
#   Журнал событий книги среды удерживаемого различия.
#
# Принцип:
#   Journal не управляет средой.
#   Journal только фиксирует события и сохраняет происхождение изменений.
#
# ==================================================================================================


from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


@dataclass
class JournalEvent:
    timestamp: str
    event_type: str
    message: str
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Journal:
    events: list[JournalEvent] = field(default_factory=list)

    def record(
        self,
        event_type: str,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> None:
        self.events.append(
            JournalEvent(
                timestamp=now_iso(),
                event_type=event_type,
                message=message,
                data=data or {},
            )
        )

    def count(self) -> int:
        return len(self.events)

    def filter_by_type(self, event_type: str) -> list[JournalEvent]:
        return [
            event
            for event in self.events
            if event.event_type == event_type
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "events_count": len(self.events),
            "events": [
                event.to_dict()
                for event in self.events
            ],
        }
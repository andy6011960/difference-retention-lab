from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class Signal:
    signal_id: str
    signal_type: str
    description: str
    source: str
    time_range: str | None = None
    file_ref: str | None = None


@dataclass
class Tension:
    tension_id: str
    description: str
    observed_change: str
    research_question: str | None = None


@dataclass
class Invariant:
    invariant_id: str
    name: str
    value: str
    description: str | None = None


@dataclass
class Rupture:
    rupture_id: str
    time_mark: str
    description: str
    linked_signals: list[str] = field(default_factory=list)
    confidence: float | None = None


@dataclass
class Interpretation:
    model_name: str
    description: str
    confidence: float | None = None
    linked_ruptures: list[str] = field(default_factory=list)


@dataclass
class ODFEvent:
    event_id: str
    title: str
    origin: str
    tension: Tension | None = None
    description: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    signals: list[Signal] = field(default_factory=list)
    invariants: list[Invariant] = field(default_factory=list)
    ruptures: list[Rupture] = field(default_factory=list)
    interpretation: Interpretation | None = None
    notes: list[str] = field(default_factory=list)

    def set_tension(self, tension: Tension) -> None:
        self.tension = tension

    def add_signal(self, signal: Signal) -> None:
        self.signals.append(signal)

    def add_invariant(self, invariant: Invariant) -> None:
        self.invariants.append(invariant)

    def add_rupture(self, rupture: Rupture) -> None:
        self.ruptures.append(rupture)

    def set_interpretation(self, interpretation: Interpretation) -> None:
        self.interpretation = interpretation

    def add_note(self, note: str) -> None:
        self.notes.append(note)

    def origin_check(self) -> dict[str, Any]:
        missing: list[str] = []

        if not self.event_id:
            missing.append("event_id")

        if not self.title:
            missing.append("title")

        if not self.origin:
            missing.append("origin")

        if self.tension is None:
            missing.append("tension")

        if not self.signals:
            missing.append("signals")

        if not self.invariants:
            missing.append("invariants")

        return {
            "event_id": self.event_id,
            "complete": len(missing) == 0,
            "missing": missing,
            "principle": "Every data stream must preserve its connection to the event that produced it.",
        }

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self, ensure_ascii: bool = False, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=ensure_ascii, indent=indent)

    def save_json(self, output_path: str | Path) -> Path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_json(), encoding="utf-8")
        return path

    def to_markdown(self) -> str:
        lines: list[str] = []

        lines.append(f"# ODF EVENT: {self.event_id}")
        lines.append("")
        lines.append(f"## {self.title}")
        lines.append("")
        lines.append(f"**Created at:** {self.created_at}")
        lines.append("")
        lines.append("## ORIGIN")
        lines.append("")
        lines.append(self.origin)
        lines.append("")

        if self.description:
            lines.append("## DESCRIPTION")
            lines.append("")
            lines.append(self.description)
            lines.append("")

        lines.append("## TENSION")
        lines.append("")
        if self.tension:
            lines.append(f"**ID:** {self.tension.tension_id}")
            lines.append("")
            lines.append(f"**Description:** {self.tension.description}")
            lines.append("")
            lines.append(f"**Observed change:** {self.tension.observed_change}")
            lines.append("")
            if self.tension.research_question:
                lines.append(f"**Research question:** {self.tension.research_question}")
                lines.append("")
        else:
            lines.append("No tension defined.")
            lines.append("")

        lines.append("## SIGNALS")
        lines.append("")
        if self.signals:
            for signal in self.signals:
                lines.append(f"### {signal.signal_id}")
                lines.append("")
                lines.append(f"- Type: {signal.signal_type}")
                lines.append(f"- Source: {signal.source}")
                lines.append(f"- Description: {signal.description}")
                if signal.time_range:
                    lines.append(f"- Time range: {signal.time_range}")
                if signal.file_ref:
                    lines.append(f"- File reference: {signal.file_ref}")
                lines.append("")
        else:
            lines.append("No signals defined.")
            lines.append("")

        lines.append("## INVARIANTS")
        lines.append("")
        if self.invariants:
            for invariant in self.invariants:
                lines.append(f"### {invariant.invariant_id}")
                lines.append("")
                lines.append(f"- Name: {invariant.name}")
                lines.append(f"- Value: {invariant.value}")
                if invariant.description:
                    lines.append(f"- Description: {invariant.description}")
                lines.append("")
        else:
            lines.append("No invariants defined.")
            lines.append("")

        lines.append("## RUPTURES")
        lines.append("")
        if self.ruptures:
            for rupture in self.ruptures:
                lines.append(f"### {rupture.rupture_id}")
                lines.append("")
                lines.append(f"- Time mark: {rupture.time_mark}")
                lines.append(f"- Description: {rupture.description}")
                if rupture.linked_signals:
                    lines.append(f"- Linked signals: {', '.join(rupture.linked_signals)}")
                if rupture.confidence is not None:
                    lines.append(f"- Confidence: {rupture.confidence}")
                lines.append("")
        else:
            lines.append("No ruptures defined.")
            lines.append("")

        lines.append("## INTERPRETATION")
        lines.append("")
        if self.interpretation:
            lines.append(f"**Model:** {self.interpretation.model_name}")
            lines.append("")
            lines.append(self.interpretation.description)
            lines.append("")
            if self.interpretation.confidence is not None:
                lines.append(f"**Confidence:** {self.interpretation.confidence}")
                lines.append("")
            if self.interpretation.linked_ruptures:
                lines.append(f"**Linked ruptures:** {', '.join(self.interpretation.linked_ruptures)}")
                lines.append("")
        else:
            lines.append("No interpretation defined.")
            lines.append("")

        lines.append("## ORIGIN CHECK")
        lines.append("")
        check = self.origin_check()
        lines.append(f"**Complete:** {check['complete']}")
        lines.append("")
        if check["missing"]:
            lines.append(f"**Missing:** {', '.join(check['missing'])}")
        else:
            lines.append("**Missing:** none")
        lines.append("")
        lines.append(f"**Principle:** {check['principle']}")
        lines.append("")

        if self.notes:
            lines.append("## NOTES")
            lines.append("")
            for note in self.notes:
                lines.append(f"- {note}")
            lines.append("")

        return "\n".join(lines)

    def save_markdown(self, output_path: str | Path) -> Path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_markdown(), encoding="utf-8")
        return path


def build_event_graph(event: ODFEvent) -> dict[str, Any]:
    return {
        "event": event.event_id,
        "origin": event.origin,
        "tension": event.tension.tension_id if event.tension else None,
        "signals": [signal.signal_id for signal in event.signals],
        "invariants": [invariant.invariant_id for invariant in event.invariants],
        "ruptures": [rupture.rupture_id for rupture in event.ruptures],
        "interpretation": event.interpretation.model_name if event.interpretation else None,
        "edges": _build_edges(event),
    }


def _build_edges(event: ODFEvent) -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []

    if event.tension:
        edges.append({
            "from": event.event_id,
            "to": event.tension.tension_id,
            "type": "has_tension",
        })

    for signal in event.signals:
        edges.append({
            "from": event.event_id,
            "to": signal.signal_id,
            "type": "produces_signal",
        })

    for invariant in event.invariants:
        edges.append({
            "from": event.event_id,
            "to": invariant.invariant_id,
            "type": "preserves_invariant",
        })

    for rupture in event.ruptures:
        edges.append({
            "from": event.event_id,
            "to": rupture.rupture_id,
            "type": "contains_rupture",
        })

        for signal_id in rupture.linked_signals:
            edges.append({
                "from": rupture.rupture_id,
                "to": signal_id,
                "type": "observed_in_signal",
            })

    if event.interpretation:
        edges.append({
            "from": event.event_id,
            "to": event.interpretation.model_name,
            "type": "has_interpretation",
        })

        for rupture_id in event.interpretation.linked_ruptures:
            edges.append({
                "from": event.interpretation.model_name,
                "to": rupture_id,
                "type": "explains_rupture",
            })

    return edges


def save_event_graph(event: ODFEvent, output_path: str | Path) -> Path:
    graph = build_event_graph(event)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path
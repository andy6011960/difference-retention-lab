import json
from pathlib import Path
from typing import Any


def load_event(json_path: str | Path) -> dict[str, Any]:
    path = Path(json_path)

    if not path.exists():
        raise FileNotFoundError(f"ODF event file not found: {path}")

    return json.loads(path.read_text(encoding="utf-8"))


def show_process(event: dict[str, Any]) -> None:
    print("ODF NAVIGATOR v0.1")
    print("=" * 60)

    print()
    print("PROCESS")
    print("-" * 60)
    print(event.get("event_id", "UNKNOWN_EVENT"))
    print(event.get("title", ""))

    print()
    print("ORIGIN")
    print("-" * 60)
    print(event.get("origin", "No origin defined."))

    print()
    print("TENSION")
    print("-" * 60)
    tension = event.get("tension")

    if tension:
        print(f"ID: {tension.get('tension_id', 'UNKNOWN_TENSION')}")
        print(f"Description: {tension.get('description', '')}")
        print(f"Observed change: {tension.get('observed_change', '')}")
        if tension.get("research_question"):
            print(f"Research question: {tension.get('research_question')}")
    else:
        print("No tension defined.")

    print()
    print("SIGNALS")
    print("-" * 60)
    signals = event.get("signals", [])

    if signals:
        print(f"Total streams: {len(signals)}")
        print()
        for signal in signals:
            print(f"- {signal.get('signal_id', 'UNKNOWN_SIGNAL')}")
            print(f"  type: {signal.get('signal_type', '')}")
            print(f"  source: {signal.get('source', '')}")
            if signal.get("time_range"):
                print(f"  time: {signal.get('time_range')}")
    else:
        print("No signals defined.")

    print()
    print("INVARIANTS")
    print("-" * 60)
    invariants = event.get("invariants", [])

    if invariants:
        for invariant in invariants:
            print(
                f"- {invariant.get('name', 'unknown')} = "
                f"{invariant.get('value', '')}"
            )
    else:
        print("No invariants defined.")

    print()
    print("RUPTURES")
    print("-" * 60)
    ruptures = event.get("ruptures", [])

    if ruptures:
        for rupture in ruptures:
            print(f"- {rupture.get('time_mark', 'unknown time')}")
            print(f"  {rupture.get('description', '')}")

            linked_signals = rupture.get("linked_signals", [])
            if linked_signals:
                print(f"  linked signals: {', '.join(linked_signals)}")

            if rupture.get("confidence") is not None:
                print(f"  confidence: {rupture.get('confidence')}")
    else:
        print("No ruptures defined.")

    print()
    print("INTERPRETATION")
    print("-" * 60)
    interpretation = event.get("interpretation")

    if interpretation:
        print(f"Model: {interpretation.get('model_name', '')}")
        print(interpretation.get("description", ""))

        if interpretation.get("confidence") is not None:
            print(f"Confidence: {interpretation.get('confidence')}")

        linked_ruptures = interpretation.get("linked_ruptures", [])
        if linked_ruptures:
            print(f"Linked ruptures: {', '.join(linked_ruptures)}")
    else:
        print("No interpretation defined.")

    print()
    print("ODF PRINCIPLE")
    print("-" * 60)
    print("Every data stream must preserve its connection to the event that produced it.")

    print()
    print("=" * 60)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    default_event_path = base_dir / "output" / "odf_event_skif_demo.json"

    event = load_event(default_event_path)
    show_process(event)


if __name__ == "__main__":
    main()
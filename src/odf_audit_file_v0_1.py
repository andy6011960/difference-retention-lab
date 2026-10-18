import argparse
import json
from pathlib import Path
from typing import Any


def load_event(json_path: str | Path) -> dict[str, Any]:
    path = Path(json_path)

    if not path.exists():
        raise FileNotFoundError(f"ODF event file not found: {path}")

    return json.loads(path.read_text(encoding="utf-8"))


def audit_event(event: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []

    event_id = event.get("event_id")
    origin = event.get("origin")
    tension = event.get("tension")
    signals = event.get("signals", [])
    invariants = event.get("invariants", [])
    ruptures = event.get("ruptures", [])
    interpretation = event.get("interpretation")

    signal_ids = {
        signal.get("signal_id")
        for signal in signals
        if signal.get("signal_id")
    }

    rupture_ids = {
        rupture.get("rupture_id")
        for rupture in ruptures
        if rupture.get("rupture_id")
    }

    if not event_id:
        issues.append("Missing event_id.")

    if not origin:
        issues.append("Missing origin.")

    if not tension:
        issues.append("Missing tension.")

    if not signals:
        issues.append("Missing signals.")

    if not invariants:
        issues.append("Missing invariants.")

    for signal in signals:
        signal_id = signal.get("signal_id", "UNKNOWN_SIGNAL")

        if not signal.get("signal_id"):
            issues.append("Signal without signal_id.")

        if not signal.get("source"):
            issues.append(f"Signal {signal_id} has no source.")

        if not signal.get("description"):
            warnings.append(f"Signal {signal_id} has no description.")

    for rupture in ruptures:
        rupture_id = rupture.get("rupture_id", "UNKNOWN_RUPTURE")
        linked_signals = rupture.get("linked_signals", [])

        if not linked_signals:
            warnings.append(f"Rupture {rupture_id} has no linked signals.")

        for linked_signal_id in linked_signals:
            if linked_signal_id not in signal_ids:
                issues.append(
                    f"Rupture {rupture_id} links to missing signal {linked_signal_id}."
                )

    if interpretation:
        linked_ruptures = interpretation.get("linked_ruptures", [])

        if not linked_ruptures:
            warnings.append("Interpretation has no linked ruptures.")

        for linked_rupture_id in linked_ruptures:
            if linked_rupture_id not in rupture_ids:
                issues.append(
                    f"Interpretation links to missing rupture {linked_rupture_id}."
                )
    else:
        warnings.append("No interpretation defined.")

    return {
        "event_id": event_id,
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "warnings": warnings,
        "counts": {
            "signals": len(signals),
            "invariants": len(invariants),
            "ruptures": len(ruptures),
            "has_tension": tension is not None,
            "has_interpretation": interpretation is not None,
        },
        "principle": "Loss of origin produces loss of interpretability.",
    }


def print_audit_report(report: dict[str, Any], source_path: str | Path) -> None:
    print("ODF AUDIT FILE v0.1")
    print("=" * 60)

    print(f"Source: {source_path}")
    print(f"Event:  {report.get('event_id')}")
    print(f"Status: {report.get('status')}")

    print()
    print("COUNTS")
    print("-" * 60)
    counts = report.get("counts", {})
    print(f"Signals:            {counts.get('signals')}")
    print(f"Invariants:         {counts.get('invariants')}")
    print(f"Ruptures:           {counts.get('ruptures')}")
    print(f"Has tension:        {counts.get('has_tension')}")
    print(f"Has interpretation: {counts.get('has_interpretation')}")

    print()
    print("ISSUES")
    print("-" * 60)
    issues = report.get("issues", [])
    if issues:
        for issue in issues:
            print(f"- {issue}")
    else:
        print("None")

    print()
    print("WARNINGS")
    print("-" * 60)
    warnings = report.get("warnings", [])
    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("None")

    print()
    print("ODF PRINCIPLE")
    print("-" * 60)
    print(report.get("principle"))

    print()
    print("=" * 60)


def save_audit_report(report: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


def build_default_report_path(source_path: str | Path) -> Path:
    path = Path(source_path)
    return path.with_name(f"{path.stem}_audit_report.json")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit any ODF event JSON file."
    )

    parser.add_argument(
        "event_json",
        help="Path to ODF event JSON file.",
    )

    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Optional path for audit report JSON.",
    )

    args = parser.parse_args()

    source_path = Path(args.event_json)
    event = load_event(source_path)
    report = audit_event(event)

    if args.output:
        report_path = Path(args.output)
    else:
        report_path = build_default_report_path(source_path)

    print_audit_report(report, source_path)
    save_audit_report(report, report_path)

    print(f"Audit report saved: {report_path}")


if __name__ == "__main__":
    main()
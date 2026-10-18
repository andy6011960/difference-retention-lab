import json
from pathlib import Path
from typing import Any


def load_graph(graph_path: str | Path) -> dict[str, Any]:
    path = Path(graph_path)

    if not path.exists():
        raise FileNotFoundError(f"ODF graph file not found: {path}")

    return json.loads(path.read_text(encoding="utf-8"))


def group_edges_by_source(edges: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = {}

    for edge in edges:
        source = edge.get("from", "UNKNOWN_SOURCE")
        grouped.setdefault(source, []).append(edge)

    return grouped


def show_graph(graph: dict[str, Any]) -> None:
    event_id = graph.get("event", "UNKNOWN_EVENT")
    edges = graph.get("edges", [])
    grouped_edges = group_edges_by_source(edges)

    print("ODF EVENT GRAPH VIEWER v0.1")
    print("=" * 60)

    print()
    print("EVENT")
    print("-" * 60)
    print(event_id)

    print()
    print("GRAPH SUMMARY")
    print("-" * 60)
    print(f"Origin:         {graph.get('origin')}")
    print(f"Tension:        {graph.get('tension')}")
    print(f"Signals:        {len(graph.get('signals', []))}")
    print(f"Invariants:     {len(graph.get('invariants', []))}")
    print(f"Ruptures:       {len(graph.get('ruptures', []))}")
    print(f"Interpretation: {graph.get('interpretation')}")
    print(f"Edges:          {len(edges)}")

    print()
    print("EDGES")
    print("-" * 60)

    if not edges:
        print("No edges defined.")
    else:
        for source, source_edges in grouped_edges.items():
            print(source)
            for edge in source_edges:
                edge_type = edge.get("type", "UNKNOWN_EDGE")
                target = edge.get("to", "UNKNOWN_TARGET")
                print(f"  -> {edge_type} -> {target}")
            print()

    print("ODF PRINCIPLE")
    print("-" * 60)
    print("A process is preserved when its data streams remain linked through origin, tension, invariants and ruptures.")

    print()
    print("=" * 60)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    graph_path = base_dir / "output" / "odf_event_skif_graph.json"

    graph = load_graph(graph_path)
    show_graph(graph)


if __name__ == "__main__":
    main()
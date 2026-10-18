import sys
import json
from pathlib import Path

# Добавляем папку src в пути поиска Python, чтобы он видел ядро
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from odf_core_v0_1 import (
    Invariant, Interpretation, ODFEvent, Rupture, Signal, Tension, save_event_graph
)

def load_opxrd_pattern(pattern_path: str | Path) -> dict:
    path = Path(pattern_path)
    if not path.exists():
        raise FileNotFoundError(f"opXRD pattern file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def parse_embedded_json(value) -> dict:
    if isinstance(value, dict):
        return value
    if not isinstance(value, str):
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}

def get_peak_summary(two_theta_values: list, intensities: list) -> dict:
    if not two_theta_values or not intensities:
        return {"has_peak": False, "peak_two_theta": None, "peak_intensity": None, "points": 0}
    
    usable_length = min(len(two_theta_values), len(intensities))
    two_theta_values = two_theta_values[:usable_length]
    intensities = intensities[:usable_length]
    max_index = max(range(usable_length), key=lambda index: intensities[index])
    
    return {
        "has_peak": True,
        "peak_two_theta": two_theta_values[max_index],
        "peak_intensity": intensities[max_index],
        "points": usable_length,
    }

def build_opxrd_real_event(pattern_path: str | Path) -> ODFEvent:
    pattern_path = Path(pattern_path)
    raw = load_opxrd_pattern(pattern_path)

    two_theta_values = raw.get("two_theta_values", [])
    intensities = raw.get("intensities", [])

    label = parse_embedded_json(raw.get("label"))
    metadata = parse_embedded_json(raw.get("metadata"))
    xray_info = parse_embedded_json(label.get("xray_info"))

    institution = metadata.get("institution", "unknown institution")
    contributor_name = metadata.get("contributor_name", "unknown contributor")
    original_file_format = metadata.get("original_file_format", "unknown format")
    measurement_date = metadata.get("measurement_date")
    xrdpattern_version = metadata.get("xrdpattern_version", "unknown version")
    primary_wavelength = xray_info.get("primary_wavelength", "unknown wavelength")
    phases = label.get("phases", [])
    is_simulated = label.get("is_simulated")

    peak_summary = get_peak_summary(two_theta_values, intensities)

    event = ODFEvent(
        event_id="EVENT_OPXRD_LBNL_PATTERN_0_0",
        title="opXRD real experimental powder XRD pattern",
        origin=f"Real open experimental pXRD data from opXRD dataset, source file: {pattern_path}",
        description="ODF real-world validation case based on an open experimental powder X-ray diffraction pattern."
    )

    event.set_tension(
        Tension(
            tension_id="TENSION_CRYSTAL_STRUCTURE_OBSERVATION_001",
            description="The internal structure of a material is observed indirectly through the distribution of diffraction intensities.",
            observed_change="Variation of intensity over the two-theta axis, including peaks, background changes and possible structural signatures.",
            research_question="What material structure or phase configuration produced the observed experimental diffraction pattern?"
        )
    )

    event.add_signal(
        Signal(
            signal_id="SIGNAL_XRD_PATTERN_001",
            signal_type="experimental_powder_xrd_pattern",
            description=f"Real pXRD signal with {len(two_theta_values)} two-theta values and {len(intensities)} intensity values.",
            source="opXRD / LBNL",
            file_ref=str(pattern_path)
        )
    )

    event.add_invariant(Invariant(invariant_id="INVARIANT_DATASET_001", name="dataset", value="opXRD"))
    event.add_invariant(Invariant(invariant_id="INVARIANT_INSTITUTION_001", name="institution", value=str(institution)))
    
    if peak_summary["has_peak"]:
        event.add_rupture(
            Rupture(
                rupture_id="RUPTURE_MAX_INTENSITY_PEAK_001",
                time_mark=f"two_theta={peak_summary['peak_two_theta']}",
                description="Maximum intensity point detected in the real experimental XRD signal.",
                linked_signals=["SIGNAL_XRD_PATTERN_001"],
                confidence=1.0
            )
        )

    model_name = "opxrd_phase_label_interpretation" if phases else "interpretation_pending"
    confidence = 0.8 if phases else None
    linked_ruptures = ["RUPTURE_MAX_INTENSITY_PEAK_001"] if peak_summary["has_peak"] else []

    event.set_interpretation(
        Interpretation(
            model_name=model_name,
            description="Phase interpretation state based on the original label.",
            confidence=confidence,
            linked_ruptures=linked_ruptures
        )
    )

    return event

def main():
    base_dir = Path(__file__).resolve().parent.parent
    pattern_path = base_dir / "opxrd" / "LBNL" / "LBNL-A" / "pattern_group_0_0.json"
    output_dir = base_dir / "output"

    event = build_opxrd_real_event(pattern_path)
    
    json_path = output_dir / "odf_real_case_opxrd.json"
    md_path = output_dir / "odf_real_case_opxrd.md"
    graph_path = output_dir / "odf_real_case_opxrd_graph.json"

    event.save_json(json_path)
    event.save_markdown(md_path)
    save_event_graph(event, graph_path)

    print("ODF REAL CASE opXRD v0.1")
    print("=" * 60)
    print(f"Source: {pattern_path}")
    print(f"Event:  {event.event_id}")
    print(f"Origin check: {event.origin_check()}")
    print("-" * 60)
    print(f"JSON:  {json_path}")
    print(f"MD:    {md_path}")
    print(f"GRAPH: {graph_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
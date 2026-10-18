import sys
import json
from pathlib import Path

# Добавляем папку src в пути поиска Python, чтобы он видел ядро
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from odf_core_v0_1 import (
    Invariant, Interpretation, ODFEvent, Rupture, Signal, Tension, save_event_graph
)
from odf_origin_auditor_v0_1 import audit_event, print_audit_report, save_audit_report

def parse_xy_file(file_path):
    """Читает простой текстовый файл .xy (угол интенсивность)"""
    two_theta = []
    intensities = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            line = line.replace(',', ' ')
            parts = line.split()
            if len(parts) >= 2:
                try:
                    two_theta.append(float(parts[0]))
                    intensities.append(float(parts[1]))
                except ValueError:
                    continue
    return two_theta, intensities

def main():
    # base_dir теперь указывает на корень проекта (на уровень выше examples)
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "data_zenodo" / "zenodo_cdo.xy"
    output_dir = base_dir / "output"
    
    print(f"Читаем файл: {data_path}")
    two_theta, intensities = parse_xy_file(data_path)
    
    if not two_theta or not intensities:
        print("❌ Ошибка: не удалось прочитать данные из файла.")
        return

    usable_length = min(len(two_theta), len(intensities))
    max_index = max(range(usable_length), key=lambda i: intensities[i])
    peak_2theta = two_theta[max_index]
    peak_intensity = intensities[max_index]

    event = ODFEvent(
        event_id="EVENT_ZENODO_CDO_001",
        title="CdO XRD pattern from Zenodo",
        origin=f"Real open experimental data from Zenodo (record 18522088), file: {data_path.name}",
        description="ODF validation case using a plain .xy text format XRD dataset."
    )

    event.set_tension(
        Tension(
            tension_id="TENSION_CRYSTAL_STRUCTURE_OBSERVATION_002",
            description="Internal crystal structure observed via X-ray diffraction.",
            observed_change="Intensity variation over two-theta axis.",
            research_question="What structure produced this diffraction pattern?"
        )
    )

    event.add_signal(
        Signal(
            signal_id="SIGNAL_XRD_CDO_001",
            signal_type="experimental_xrd_xy_format",
            description=f"XRD signal with {len(two_theta)} points in .xy format.",
            source="Zenodo",
            file_ref=str(data_path)
        )
    )

    event.add_invariant(
        Invariant(
            invariant_id="INVARIANT_FORMAT_001",
            name="file_format",
            value=".xy",
            description="Plain text two-column format."
        )
    )

    event.add_rupture(
        Rupture(
            rupture_id="RUPTURE_MAX_PEAK_001",
            time_mark=f"two_theta={peak_2theta}",
            description=f"Maximum intensity peak detected at {peak_intensity}.",
            linked_signals=["SIGNAL_XRD_CDO_001"],
            confidence=1.0
        )
    )

    event.set_interpretation(
        Interpretation(
            model_name="interpretation_pending",
            description="Phase interpretation pending. ODF preserves the signal and peak feature.",
            confidence=None,
            linked_ruptures=["RUPTURE_MAX_PEAK_001"]
        )
    )

    json_path = output_dir / "odf_real_case_zenodo.json"
    md_path = output_dir / "odf_real_case_zenodo.md"
    graph_path = output_dir / "odf_real_case_zenodo_graph.json"

    event.save_json(json_path)
    event.save_markdown(md_path)
    save_event_graph(event, graph_path)

    event_dict = json.loads(json_path.read_text(encoding="utf-8"))
    report = audit_event(event_dict)
    
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТ АУДИТА ВТОРОГО КЕЙСА (ZENODO .XY):")
    print_audit_report(report)
    
    save_audit_report(report, output_dir / "odf_real_case_zenodo_audit.json")

if __name__ == "__main__":
    main()
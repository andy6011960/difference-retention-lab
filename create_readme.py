from pathlib import Path

readme_content = """# Ontological Data Flow (ODF) Core v0.1

**Preserving the origin of scientific data.**

Modern experimental science increasingly studies processes (chemical reactions, phase transitions, material deformation) rather than static objects. While FAIR principles help preserve access to data, the origin of the process that produced the data is often lost. 

ODF (Ontological Data Flow) is a prototype framework that shifts the basic unit of data storage from the **file** to the **event**. 

> **Principle:** Every data stream must preserve its connection to the event that produced it.

## Core Entities
ODF structures data around six main entities:
*   **EVENT**: The observed process (e.g., a chemical reaction).
*   **TENSION**: The investigated change or research question.
*   **SIGNAL**: The data stream (e.g., XRD pattern, video, spectra).
*   **INVARIANT**: Parameters that preserve the identity of the process.
*   **RUPTURE**: A significant change or structural feature in the signal.
*   **INTERPRETATION**: The scientific model, including its absence (`PENDING`).

## Validation Status
ODF v0.1 has been tested on two independent real-world datasets, proving format independence:
1.  **opXRD (LBNL, USA)**: Real experimental powder XRD data in complex `.json` format.
2.  **CdO (Zenodo)**: Real experimental XRD data in simple two-column `.xy` text format.

**Important distinction:** 
In ODF v0.1, a `PASS` status means **STRUCTURAL PASS** — the ODF wrapper is valid, all links between signals, ruptures, and interpretations are intact. 
*ODF v0.1 does not perform automatic scientific interpretation. `PASS` does not mean a new physical discovery was made.*

## How to run (in 3 commands)
Ensure you have Python 3 installed. ODF has no external dependencies (uses only the standard library).

1. Open PowerShell in the project root folder:
   ```bash
   cd E:\\SINTEZ_ONTOLOGY_V2\\ODF_CORE_v0_1
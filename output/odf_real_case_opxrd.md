# ODF EVENT: EVENT_OPXRD_LBNL_PATTERN_0_0

## opXRD real experimental powder XRD pattern

**Created at:** 2026-10-18T16:06:23

## ORIGIN

Real open experimental pXRD data from opXRD dataset, source file: E:\SINTEZ_ONTOLOGY_V2\ODF_CORE_v0_1\opxrd\LBNL\LBNL-A\pattern_group_0_0.json

## DESCRIPTION

ODF real-world validation case based on an open experimental powder X-ray diffraction pattern.

## TENSION

**ID:** TENSION_CRYSTAL_STRUCTURE_OBSERVATION_001

**Description:** The internal structure of a material is observed indirectly through the distribution of diffraction intensities.

**Observed change:** Variation of intensity over the two-theta axis, including peaks, background changes and possible structural signatures.

**Research question:** What material structure or phase configuration produced the observed experimental diffraction pattern?

## SIGNALS

### SIGNAL_XRD_PATTERN_001

- Type: experimental_powder_xrd_pattern
- Source: opXRD / LBNL
- Description: Real pXRD signal with 459 two-theta values and 459 intensity values.
- File reference: E:\SINTEZ_ONTOLOGY_V2\ODF_CORE_v0_1\opxrd\LBNL\LBNL-A\pattern_group_0_0.json

## INVARIANTS

### INVARIANT_DATASET_001

- Name: dataset
- Value: opXRD

### INVARIANT_INSTITUTION_001

- Name: institution
- Value: Molecular Foundry Division, Lawrence Berkeley National Laboratory, Berkeley, California 94710, United States, and Sutter-Fella group

## RUPTURES

### RUPTURE_MAX_INTENSITY_PEAK_001

- Time mark: two_theta=29.02024247646219
- Description: Maximum intensity point detected in the real experimental XRD signal.
- Linked signals: SIGNAL_XRD_PATTERN_001
- Confidence: 1.0

## INTERPRETATION

**Model:** interpretation_pending

Phase interpretation state based on the original label.

**Linked ruptures:** RUPTURE_MAX_INTENSITY_PEAK_001

## ORIGIN CHECK

**Complete:** True

**Missing:** none

**Principle:** Every data stream must preserve its connection to the event that produced it.

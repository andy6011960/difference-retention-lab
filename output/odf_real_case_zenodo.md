# ODF EVENT: EVENT_ZENODO_CDO_001

## CdO XRD pattern from Zenodo

**Created at:** 2026-10-18T16:08:48

## ORIGIN

Real open experimental data from Zenodo (record 18522088), file: zenodo_cdo.xy

## DESCRIPTION

ODF validation case using a plain .xy text format XRD dataset.

## TENSION

**ID:** TENSION_CRYSTAL_STRUCTURE_OBSERVATION_002

**Description:** Internal crystal structure observed via X-ray diffraction.

**Observed change:** Intensity variation over two-theta axis.

**Research question:** What structure produced this diffraction pattern?

## SIGNALS

### SIGNAL_XRD_CDO_001

- Type: experimental_xrd_xy_format
- Source: Zenodo
- Description: XRD signal with 4013 points in .xy format.
- File reference: E:\SINTEZ_ONTOLOGY_V2\ODF_CORE_v0_1\data_zenodo\zenodo_cdo.xy

## INVARIANTS

### INVARIANT_FORMAT_001

- Name: file_format
- Value: .xy
- Description: Plain text two-column format.

## RUPTURES

### RUPTURE_MAX_PEAK_001

- Time mark: two_theta=32.78619
- Description: Maximum intensity peak detected at 3163.0.
- Linked signals: SIGNAL_XRD_CDO_001
- Confidence: 1.0

## INTERPRETATION

**Model:** interpretation_pending

Phase interpretation pending. ODF preserves the signal and peak feature.

**Linked ruptures:** RUPTURE_MAX_PEAK_001

## ORIGIN CHECK

**Complete:** True

**Missing:** none

**Principle:** Every data stream must preserve its connection to the event that produced it.

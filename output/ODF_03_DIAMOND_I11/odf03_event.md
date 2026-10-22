# ODF EVENT: ODF-03-DIAMOND-I11-ASP

## Diamond I11 Project M: source-preserving contrast between Asp conditions

**Created at:** 2026-10-22T10:09:53

## ORIGIN

Diamond Light Source I11, Project M, proposal EE15723-1, published dataset https://doi.org/10.5281/zenodo.7871450; local XYE files and workbook verified by SHA256 baseline.

## DESCRIPTION

Two XRD diffraction patterns from the Asp worksheet correspond to experimental-condition values 0 and 0.1. Silicon file is retained as a separately identified standard, with no asserted direct calibration link.

## TENSION

**ID:** T-ASP-0-TO-0.1

**Description:** Relationship between changed recorded condition and distinct XRD profile/fit outcomes.

**Observed change:** Asp worksheet condition value 0 -> 0.1; two distinct source files.

**Research question:** Can ODF retain the documented provenance of both profiles and their analytical outcomes?

## SIGNALS

### S-578412

- Type: XRD_XYE_WITH_WORKBOOK_CONTEXT
- Source: https://doi.org/10.5281/zenodo.7871450 / ProjectM_DiffractionData.xlsx / Asp / 578412-mythen_summed.xye
- Description: Asp worksheet row 4; condition=0.0 (unit unspecified); points=22508; Rwp=6.3161%; SHA256=12317867B92CE27D5A309212A8160ED543AF2BEBC7A7BB4914D96D59D6E7EF6E
- File reference: 578412-mythen_summed.xye

### S-578413

- Type: XRD_XYE_WITH_WORKBOOK_CONTEXT
- Source: https://doi.org/10.5281/zenodo.7871450 / ProjectM_DiffractionData.xlsx / Asp / 578413-mythen_summed.xye
- Description: Asp worksheet row 5; condition=0.1 (unit unspecified); points=22508; Rwp=6.0403%; SHA256=EB54644F1E09363D35BDA5ECA06A1B2DAA71FEDA9AAD85FBFB9FE15A2BF3CA1D
- File reference: 578413-mythen_summed.xye

### S-SILICON-578401

- Type: SEPARATELY_DOCUMENTED_SILICON_STANDARD_XYE
- Source: https://doi.org/10.5281/zenodo.7871450 / 578401-mythen_summedSILICON640C.xye
- Description: Silicon standard XYE, 22508 points; SHA256=6D1806FC791FD162036735FBFA2679B445D25F5F5CC3A289AB346A729C16C2F8; relationship to Asp collection is unverified.
- File reference: 578401-mythen_summedSILICON640C.xye

## INVARIANTS

### INV-REFERENTIAL-ORIGIN

- Name: Source-file identity retained
- Value: 2/2 Asp references matched exact Excel filenames; 4/4 SHA256 baseline
- Description: Workbook relation and file checks were independently validated before event creation.

### INV-EXPERIMENT-CONTEXT

- Name: Asp provenance context
- Value: Asp: condition 0 -> 0.1; same experimental-group worksheet
- Description: Does not assert repeated observations of the same specimen or causal effect.

## RUPTURES

No ruptures defined.

## INTERPRETATION

**Model:** Provenance-preserving structural comparison (not phase identification)

Experimental-condition values and reported fit metrics differ. This run audits source relationships and does not infer a new physical phase, causal mechanism, or undocumented chronology.

## ORIGIN CHECK

**Complete:** True

**Missing:** none

**Principle:** Every data stream must preserve its connection to the event that produced it.

## NOTES

- No physical rupture/emergence claimed; rupture list intentionally empty.
- ODF core origin_check validates required fields only; stricter source and linkage checks are runner-level.
- The negative control modifies an in-memory copy of the reference key, never original files.

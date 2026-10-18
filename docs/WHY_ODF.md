# WHY ODF

## Why Ontological Data Flow is needed

FAIR helps preserve access to data.

ODF helps preserve the origin of the process that produced the data.

---

## 1. The problem

Modern experimental science increasingly studies processes rather than isolated objects.

Examples:

- chemical reactions;
- phase transitions;
- material deformation;
- structural failure;
- time-resolved evolution of matter.

Such experiments produce large streams of data:

- images;
- spectra;
- sensor logs;
- time series;
- metadata;
- control logs.

The files can be stored.

The metadata can be preserved.

But the process that produced them can become difficult to reconstruct.

---

## 2. The limitation of file-centered thinking

A file is not the experiment.

A dataset is not the process.

A metadata record is not the origin of interpretation.

When data streams are disconnected from the event that produced them, the researcher may still have access to the files but lose the structure of the observed process.

This creates a risk:

data remain available,

but their interpretability decreases.

---

## 3. The ODF principle

Every data stream must preserve its connection to the event that produced it.

Loss of origin produces loss of interpretability.

---

## 4. What ODF adds

ODF adds a process layer above data storage.

Basic ODF structure:

text
EVENT
├── TENSION
├── SIGNALS
├── INVARIANTS
├── RUPTURES
└── INTERPRETATION

ODF does not replace existing data principles.

ODF complements them.

It makes explicit:

what event produced the data;
what change or tension was being observed;
which signals belong to the same process;
which invariants preserve experimental identity;
where ruptures or significant changes appear;
how interpretation is linked to observed features.
5. FAIR and ODF

FAIR answers:

Can the data be found?
Can the data be accessed?
Can the data interoperate?
Can the data be reused?

ODF asks:

Can the process be reconstructed?
Can the origin of the signal be preserved?
Can different data streams be linked through one event?
Can interpretation remain connected to observed features?

## 6. Why this matters

For installations and datasets that generate large experimental flows, the main future bottleneck may not be storage alone.

The bottleneck may be interpretation.

ODF is designed to reduce the time between:

data acquisition
↓
process reconstruction
↓
scientific interpretation

data acquisition
↓
process reconstruction
↓
scientific interpretation

## 7. Current status

ODF_CORE_v0.1 is a working prototype.

Implemented components:

ODF core model;
SKIF demonstration case;
process navigator;
origin auditor;
event graph viewer;
universal audit file tool;
real opXRD validation case.

Validated cases:

ODF_CASE_SKIF
Status: PASS

ODF_REAL_CASE_opXRD
Status: PASS

## 8. Short formulation

FAIR preserves scientific data.

ODF preserves the origin of scientific processes.
# ODF EVENT: EVENT_SKIF_EXPLOSION_001

## SKIF explosion chamber process observation demo

**Created at:** 2026-06-09T20:54:42

## ORIGIN

SKIF explosion chamber: experimental observation of a metal sample under shock loading.

## DESCRIPTION

Demo ODF event for illustrating how multiple experimental data streams can be connected to one observed process rather than stored as isolated files.

## TENSION

**ID:** TENSION_SHOCK_STRUCTURAL_FAILURE_001

**Description:** Shock loading of a metallic sample and subsequent structural degradation.

**Observed change:** Growth of internal stress followed by local rupture and loss of structural connectivity.

**Research question:** At what moment does the sample transition from reversible deformation to irreversible structural damage?

## SIGNALS

### SIGNAL_XRAY_001

- Type: xray_series
- Source: synchrotron_xray_diagnostics
- Description: Time-resolved X-ray image sequence of the sample during shock loading.
- Time range: 0.00-25.00 microseconds
- File reference: experiment_001/xray/xray_series_001.dat

### SIGNAL_VIDEO_001

- Type: high_speed_video
- Source: high_speed_camera
- Description: High-speed optical video of external deformation and visible fracture development.
- Time range: 0.00-25.00 microseconds
- File reference: experiment_001/video/high_speed_video_001.mp4

### SIGNAL_PRESSURE_001

- Type: pressure_sensor
- Source: pressure_sensor_array
- Description: Pressure profile of the shock wave during the experiment.
- Time range: 0.00-25.00 microseconds
- File reference: experiment_001/pressure/pressure_profile_001.csv

### SIGNAL_STRAIN_001

- Type: strain_sensor
- Source: strain_sensor_array
- Description: Local strain measurements from the sample surface and fixture points.
- Time range: 0.00-25.00 microseconds
- File reference: experiment_001/strain/strain_profile_001.csv

## INVARIANTS

### INVARIANT_SAMPLE_001

- Name: sample
- Value: Ti-6Al-4V
- Description: Material sample identity preserved across all data streams.

### INVARIANT_FACILITY_001

- Name: facility
- Value: SKIF
- Description: Experimental facility where the event is observed.

### INVARIANT_SERIES_001

- Name: experiment_series
- Value: EXP-2026-A
- Description: Experimental series identifier linking related tests.

### INVARIANT_TIMEBASE_001

- Name: shared_timebase
- Value: microsecond synchronized timeline
- Description: Common temporal frame used to connect signals from different instruments.

## RUPTURES

### RUPTURE_LOCAL_DAMAGE_001

- Time mark: 12.37 microseconds
- Description: First visible local damage zone appears in the sample structure.
- Linked signals: SIGNAL_XRAY_001, SIGNAL_VIDEO_001, SIGNAL_STRAIN_001
- Confidence: 0.86

### RUPTURE_CONNECTIVITY_LOSS_001

- Time mark: 18.41 microseconds
- Description: Loss of structural connectivity becomes observable across multiple signals.
- Linked signals: SIGNAL_XRAY_001, SIGNAL_PRESSURE_001, SIGNAL_STRAIN_001
- Confidence: 0.91

## INTERPRETATION

**Model:** shock_induced_structural_transition

The event is interpreted as a shock-induced structural transition: a process in which accumulated internal stress produces local damage, followed by loss of connectivity in the material structure.

**Confidence:** 0.91

**Linked ruptures:** RUPTURE_LOCAL_DAMAGE_001, RUPTURE_CONNECTIVITY_LOSS_001

## ORIGIN CHECK

**Complete:** True

**Missing:** none

**Principle:** Every data stream must preserve its connection to the event that produced it.

## NOTES

- ODF demo principle: the experiment is represented as one process event, not as a folder of disconnected files.
- Each signal preserves its origin through EVENT_SKIF_EXPLOSION_001 and remains linked to tension, invariants and ruptures.

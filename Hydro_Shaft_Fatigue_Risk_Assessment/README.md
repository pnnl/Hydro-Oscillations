# Data_Center_Hydro_Risk_Assessment

EMT models in PSCAD for studying hydro-generator shaft fatigue risk arising from persistent sub-synchronous active-power oscillations induced by large AI data center loads.

## Overview

PSCAD case studies characterizing hydro-generator shaft fatigue risk from sub-synchronous active-power oscillations induced by AI data center loads, in both time domain and frequency domain.

## Folder Contents

| File | Type | Purpose |
|---|---|---|
| `DML_Components` | PSCAD component library | Shared library of custom models (data center load models, hydro-generator/turbine-governor models, measurement/control blocks, etc.) referenced by both case files below. Must be added as a library project before compiling/running the other two files. |
| `hydro_grid_AI_load_freq.pscx` | PSCAD case | Simulates dynamic response of a multi-mass hydro-generator connected to an AI data center load |
| `hydro_grid_AI_load_TF.pscx` | PSCAD case | Simulates the time-series data for evaluating the transfer function of a multi-mass hydro-generator model |

## Case File Details

### `hydro_grid_AI_load_freq.pscx` — Time-Domain Simulation

Run this file to simulate the dynamic response of a multi-mass hydro-generator connected to an AI data center load.

<ol type="a">
<li>The AI training load is modeled to represent a bi-periodic square-wave workload profile. Users can configure the base load, amplitude of load fluctuation, and frequencies and duty cycle of the bi-periodic square wave.</li>
<li>The electrical parameters of the generator to be configured in the synchronous machine model. The defaults are configured for a salient pole machine with parameters from [1].</li>
<li>The machine speed, generator and turbine inertias, shaft stiffness and damping can be configured in the multi-mass component of the machine model. Example parameter values for three generator units Unit A, GC-7, GC-19, are listed in Table 1.</li>
</ol>
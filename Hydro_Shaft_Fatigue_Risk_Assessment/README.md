# Data_Center_Hydro_Risk_Assessment

EMT models in PSCAD for studying hydro-generator shaft fatigue risk arising from persistent sub-synchronous active-power oscillations induced by large AI data center loads.

## Overview

PSCAD case studies characterizing hydro-generator shaft fatigue risk from sub-synchronous active-power oscillations induced by AI data center loads, in both time domain and frequency domain.

## Folder Contents

| File | Type | Purpose |
|---|---|---|
| `DML_Components` | PSCAD component library | Shared library of custom models (data center load models, hydro-generator models etc.) referenced by both case files below. Must be added as a library project before compiling/running the other two files. |
| `hydro_grid_AI_load_freq` | PSCAD case  | Base model coupling an AI data center load to a hydro-generator grid. Used to simulate AI-load-induced active-power oscillations and directly observe the resulting generator shaft torque response in the time domain. |
| `hydro_grid_AI_load_TF` | PSCAD case  | Modified version of the base model used to derive system transfer functions and for frequency scanning. |



# EMT Models for Studying the Impact of Load-Induced High-Frequency Oscillations on Hydropower Units

EMT models in PSCAD for studying hydro-generator shaft fatigue risk arising from persistent high-frequency active-power oscillations induced by large AI data center loads.

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
<li>The AI training load <a href="#ref1">[1]</a> is modeled to represent a bi-periodic square-wave workload profile. Users can configure the base load, amplitude of load fluctuation, and frequencies and duty cycle of the bi-periodic square wave.
<p align="center">
  <img src="figures/Hydro_AI_freq.png" alt="PSCAD Model" width="600">
</p>
<p align="center"><em>Fig. 1: PSCAD model - Multi-mass Hydro with AI data center load.</em></p></li>
<li>The electrical parameters of the generator to be configured in the synchronous machine model. The defaults are configured for a salient pole machine with parameters from <a href="#ref2">[2]</a>.</li>
<li>The machine speed, generator and turbine inertias, shaft stiffness and damping can be configured in the multi-mass component of the machine model. Example parameter values for three generator units Unit A, GC-7, GC-19, are listed in Table 1 [3].</li>
</ol>


<div align="center">

**Table 1: PSCAD multi-mass torsional shaft model parameters**

| Design Parameter | Units | Unit A | GC-7 | GC-19 |
|---|---|---|---|---|
| Generator rating | MVA | 500  | 60  | 715  |
| Rated speed | rpm | 150  | 200  | 72  |
| Turbine inertia | kg·m² | 1.68 × 10⁶ | 90.6 × 10³ | 8428 × 10³ |
| Generator inertia | kg·m² | 33.75 × 10⁶ | 0.653 × 10⁶ | 107 × 10⁶ |
| Shaft spring constant | Nm/rad | 18.66 × 10⁹ | 0.208 × 10⁹ | 12.09 × 10⁹ |
| Turbine damping | Nm·s/rad | 5.01 × 10⁶ | 1.37 × 10⁵ | 12.6 × 10⁶ |

</div>

---

### `hydro_grid_AI_load_TF.pscx` — Frequency-Domain (Transfer Function) Analysis

Run this file to simulate the time-series data for evaluating the transfer function of a multi-mass hydro-generator model.


<ol type="a">
<li>This model injects unit-amplitude sinusoidal active-power oscillation at the generator terminal. The responses of the generator-turbine shaft torque and active power generated to this injected signal is captured in this study.</li>
<li>The oscillation frequency (f_osc) must be swept manually over the desired range. Each frequency is simulated individually - responses (torques and active powers) should be recorded and saved before proceeding to the next.</li>
<li>Following post processing including detrending to remove steady state offset, observed oscillation amplitudes are used to compute the corresponding transfer-function magnitudes.</li>
</ol>

> **Note:** The model and files are tested with PSCAD version 5.0.1.

## References

<a id="ref1"></a>[1] B. A. Ross and J. D. Follum, "Data Center Model Library for Electromagnetic Transient Analysis (PSCAD)," *IEEE Dataport*, 2026.

<a id="ref2"></a>[2] J. Bladh, P. Sundqvist, and L. U, "Torsional Stability of Hydropower Units Under Influence of Subsynchronous Oscillations," *IEEE Trans. on Power Syst.*, vol. 28, no. 4, 2013.

[3] Eilts, L. E., and Eugene Campbell. Shaft torsional oscillations of hydrogenerators. No. PB-102155. Bureau of Reclamation, Denver, CO (USA), 1979.

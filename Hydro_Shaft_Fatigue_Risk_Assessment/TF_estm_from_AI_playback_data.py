# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 16:52:25 2026

Transfer-function estimation between:
    Input:  Te
    Output: Tm

Estimated transfer function:
    H(f) = Tm(f) / Te(f)

Methods:
    1. Direct FFT division
    2. H1 cross-spectral estimator

@author: chat694
"""

# ============================================================
# IMPORT PACKAGES
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.signal import detrend, welch, csd


# ============================================================
# 1. USER CONFIGURATION
# ============================================================

FILE_PATH = Path("playback_load_GC7_1.xlsx")
SHEET_NAME = "Sheet1"

# Time interval used for transfer-function estimation
START_TIME = 10.0       # seconds
END_TIME = 60.0         # seconds

# Detrending method:
# "constant" removes the mean operating value.
# "linear" removes the mean and a linear trend.
DETREND_TYPE = "constant"

# Frequency range displayed in the transfer-function plots
MIN_FREQUENCY = 5.0     # Hz
MAX_FREQUENCY = 20.0    # Hz

# Welch/H1 estimator settings
WELCH_SEGMENT_SECONDS = 10.0
WELCH_OVERLAP_FRACTION = 0.50

# Direct FFT division is ignored where the input spectrum is
# smaller than this fraction of its maximum.
FFT_INPUT_THRESHOLD = 1e-4

# H1 calculation is ignored where the input PSD is very small.
H1_INPUT_THRESHOLD = 1e-10

# Coherence reference level
COHERENCE_THRESHOLD = 0.8


# ============================================================
# 2. READ THE EXCEL FILE
# ============================================================

data = pd.read_excel(
    FILE_PATH,
    sheet_name=SHEET_NAME
)

# Remove leading and trailing spaces from column names
data.columns = data.columns.astype(str).str.strip()

# Remove columns that are completely empty.
# This removes the empty "pu" column in the supplied workbook.
data = data.dropna(axis=1, how="all")

print("Columns retained from the workbook:")

for column_number, column_name in enumerate(data.columns):
    print(f"  Column {column_number}: {column_name}")


# ============================================================
# 3. IDENTIFY TIME, INPUT, AND OUTPUT COLUMNS
# ============================================================

# First retained column: time
time_column = data.columns[0]

# Last retained column: Te, used as plant input
te_column = data.columns[-1]

# Second-last retained column: Tm, used as plant output
tm_column = data.columns[-2]

print("\nSignals selected:")
print(f"  Time:   {time_column}")
print(f"  Input:  {te_column} (Te)")
print(f"  Output: {tm_column} (Tm)")
print("  Transfer function: H(f) = Tm(f)/Te(f)")


# Convert the selected columns to numeric values.
# Non-numeric cells, if present, become NaN.
selected_data = pd.DataFrame({
    "time": pd.to_numeric(data[time_column], errors="coerce"),
    "Te": pd.to_numeric(data[te_column], errors="coerce"),
    "Tm": pd.to_numeric(data[tm_column], errors="coerce")
})

# Remove rows containing invalid or missing values
selected_data = selected_data.dropna(
    subset=["time", "Te", "Tm"]
).reset_index(drop=True)


# ============================================================
# 4. SELECT THE DESIRED TIME SEGMENT
# ============================================================

if END_TIME <= START_TIME:
    raise ValueError("END_TIME must be greater than START_TIME.")

available_start = selected_data["time"].min()
available_end = selected_data["time"].max()

if START_TIME < available_start or END_TIME > available_end:
    raise ValueError(
        f"Requested interval [{START_TIME}, {END_TIME}] s is outside "
        f"the available interval "
        f"[{available_start}, {available_end}] s."
    )

time_mask = (
    (selected_data["time"] >= START_TIME)
    & (selected_data["time"] <= END_TIME)
)

segment = selected_data.loc[time_mask].copy()

if len(segment) < 2:
    raise ValueError(
        "The selected time interval contains fewer than two samples."
    )

# Extract time-domain signals
time = segment["time"].to_numpy(dtype=float)
Te_raw = segment["Te"].to_numpy(dtype=float)
Tm_raw = segment["Tm"].to_numpy(dtype=float)


# ============================================================
# 5. CHECK THE TIME STEP
# ============================================================

time_steps = np.diff(time)
dt = np.median(time_steps)
sampling_frequency = 1.0 / dt

maximum_time_step_error = np.max(
    np.abs(time_steps - dt)
)

print("\nSelected time segment:")
print(f"  Start time:         {time[0]:.6f} s")
print(f"  End time:           {time[-1]:.6f} s")
print(f"  Number of samples:  {len(time)}")
print(f"  Median time step:   {dt:.9f} s")
print(f"  Sampling frequency: {sampling_frequency:.3f} Hz")
print(f"  Maximum dt error:   {maximum_time_step_error:.3e} s")

# FFT and spectral estimation require uniformly sampled data.
if not np.allclose(
    time_steps,
    dt,
    rtol=1e-5,
    atol=1e-10
):
    raise ValueError(
        "The selected data are not uniformly sampled. "
        "Resampling is required before transfer-function estimation."
    )


# ============================================================
# 6. DETREND INPUT AND OUTPUT SIGNALS
# ============================================================

# Te is the plant input
Te_detrended = detrend(
    Te_raw,
    type=DETREND_TYPE
)

# Tm is the plant output
Tm_detrended = detrend(
    Tm_raw,
    type=DETREND_TYPE
)

# Short names used in the transfer-function calculations
u = Te_detrended        # Input: delta Te
y = Tm_detrended        # Output: delta Tm


print("\nDetrended signals:")
print(f"  Mean of detrended Te: {np.mean(u):.6e}")
print(f"  Mean of detrended Tm: {np.mean(y):.6e}")
print(f"  RMS of detrended Te:  {np.sqrt(np.mean(u**2)):.6e}")
print(f"  RMS of detrended Tm:  {np.sqrt(np.mean(y**2)):.6e}")


# ============================================================
# 7. PLOT DETRENDED INPUT AND OUTPUT
# ============================================================

fig, axes = plt.subplots(
    nrows=2,
    ncols=1,
    figsize=(11, 7),
    sharex=True
)

axes[0].plot(
    time,
    u,
    color="tab:blue",
    linewidth=1.0
)

axes[0].set_ylabel(r"Detrended $T_e$")
axes[0].set_title(
    rf"Plant Input: $\Delta T_e(t)$, "
    rf"{START_TIME:g}–{END_TIME:g} s"
)
axes[0].grid(True, alpha=0.3)


axes[1].plot(
    time,
    y,
    color="tab:red",
    linewidth=1.0
)

axes[1].set_xlabel("Time (s)")
axes[1].set_ylabel(r"Detrended $T_m$")
axes[1].set_title(
    rf"Plant Output: $\Delta T_m(t)$, "
    rf"{START_TIME:g}–{END_TIME:g} s"
)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# ============================================================
# 8. METHOD 1: DIRECT FFT ESTIMATION
# ============================================================

number_of_samples = len(u)

# Apply the same Hann window to the input and output.
# This reduces spectral leakage caused by the boundaries of
# the selected time interval.
fft_window = np.hanning(number_of_samples)

u_windowed = u * fft_window
y_windowed = y * fft_window

# One-sided FFTs
U = np.fft.rfft(u_windowed)
Y = np.fft.rfft(y_windowed)

frequency_fft = np.fft.rfftfreq(
    number_of_samples,
    d=dt
)

# Input-spectrum magnitude normalized by its maximum
input_fft_magnitude = np.abs(U)

if np.max(input_fft_magnitude) == 0:
    raise ValueError(
        "The detrended Te input is zero. "
        "The transfer function cannot be estimated."
    )

normalized_input_spectrum = (
    input_fft_magnitude
    / np.max(input_fft_magnitude)
)

# Only divide at frequencies where Te has sufficient energy
valid_fft = (
    normalized_input_spectrum >= FFT_INPUT_THRESHOLD
)

# Initialize the frequency response with NaN values
H_fft = np.full(
    U.shape,
    np.nan + 1j * np.nan,
    dtype=complex
)

# Direct FFT transfer-function estimate
H_fft[valid_fft] = Y[valid_fft] / U[valid_fft]

gain_fft = np.abs(H_fft)

print("\nDirect FFT estimator:")
print(
    f"  Frequency resolution: "
    f"{sampling_frequency / number_of_samples:.6f} Hz"
)
print(
    f"  Valid FFT bins: "
    f"{np.count_nonzero(valid_fft)} of {len(valid_fft)}"
)


# ============================================================
# 9. METHOD 2: H1 SPECTRAL ESTIMATOR
# ============================================================

# Number of samples in each Welch segment
nperseg = int(
    round(
        WELCH_SEGMENT_SECONDS
        * sampling_frequency
    )
)

nperseg = min(
    nperseg,
    number_of_samples
)

if nperseg < 8:
    raise ValueError(
        "The selected Welch segment is too short."
    )

# Number of overlapping samples
noverlap = int(
    round(
        WELCH_OVERLAP_FRACTION
        * nperseg
    )
)

noverlap = min(
    noverlap,
    nperseg - 1
)

welch_frequency_resolution = (
    sampling_frequency / nperseg
)

print("\nWelch/H1 estimator settings:")
print(f"  Segment length:       {nperseg} samples")
print(
    f"  Segment duration:     "
    f"{nperseg / sampling_frequency:.3f} s"
)
print(
    f"  Frequency resolution: "
    f"{welch_frequency_resolution:.6f} Hz"
)
print(f"  Overlap:              {noverlap} samples")


# ------------------------------------------------------------
# Input auto-power spectral density
# ------------------------------------------------------------

frequency_h1, Suu = welch(
    u,
    fs=sampling_frequency,
    window="hann",
    nperseg=nperseg,
    noverlap=noverlap,
    detrend=False,
    scaling="density"
)


# ------------------------------------------------------------
# Output auto-power spectral density
# ------------------------------------------------------------

_, Syy = welch(
    y,
    fs=sampling_frequency,
    window="hann",
    nperseg=nperseg,
    noverlap=noverlap,
    detrend=False,
    scaling="density"
)


# ------------------------------------------------------------
# Input-output cross-power spectral density
# ------------------------------------------------------------

# scipy.signal.csd(u, y) evaluates a cross-spectrum
# proportional to conjugate(U)*Y.
_, Suy = csd(
    u,
    y,
    fs=sampling_frequency,
    window="hann",
    nperseg=nperseg,
    noverlap=noverlap,
    detrend=False,
    scaling="density"
)


# ------------------------------------------------------------
# Calculate H1 = Suy/Suu
# ------------------------------------------------------------

valid_h1 = (
    Suu > np.max(Suu) * H1_INPUT_THRESHOLD
)

H_h1 = np.full(
    Suu.shape,
    np.nan + 1j * np.nan,
    dtype=complex
)

H_h1[valid_h1] = (
    Suy[valid_h1]
    / Suu[valid_h1]
)

gain_h1 = np.abs(H_h1)


# ------------------------------------------------------------
# Calculate magnitude-squared coherence
# ------------------------------------------------------------

coherence = np.full(
    Suu.shape,
    np.nan,
    dtype=float
)

coherence_denominator = Suu * Syy

valid_coherence = (
    coherence_denominator > 0
)

coherence[valid_coherence] = (
    np.abs(Suy[valid_coherence])**2
    / coherence_denominator[valid_coherence]
)

# Limit small numerical errors to the physical range [0, 1]
coherence = np.clip(
    coherence,
    0.0,
    1.0
)


# ============================================================
# 10. SELECT THE 5–20 Hz FREQUENCY RANGE
# ============================================================

fft_plot_mask = (
    (frequency_fft >= MIN_FREQUENCY)
    & (frequency_fft <= MAX_FREQUENCY)
    & np.isfinite(gain_fft)
)

h1_plot_mask = (
    (frequency_h1 >= MIN_FREQUENCY)
    & (frequency_h1 <= MAX_FREQUENCY)
    & np.isfinite(gain_h1)
)

if not np.any(fft_plot_mask):
    raise ValueError(
        "No valid direct-FFT estimates were found in the "
        f"{MIN_FREQUENCY}–{MAX_FREQUENCY} Hz range. "
        "Try reducing FFT_INPUT_THRESHOLD."
    )

if not np.any(h1_plot_mask):
    raise ValueError(
        "No valid H1 estimates were found in the "
        f"{MIN_FREQUENCY}–{MAX_FREQUENCY} Hz range."
    )


# Extract the selected frequency responses
f_fft_plot = frequency_fft[fft_plot_mask]
H_fft_plot = H_fft[fft_plot_mask]
gain_fft_plot = gain_fft[fft_plot_mask]

f_h1_plot = frequency_h1[h1_plot_mask]
H_h1_plot = H_h1[h1_plot_mask]
gain_h1_plot = gain_h1[h1_plot_mask]
coherence_plot = coherence[h1_plot_mask]


# Calculate phase only after selecting valid frequency bins.
# This avoids propagating NaN values through np.unwrap().
phase_fft_plot = (
    np.unwrap(np.angle(H_fft_plot))
    * 180.0 / np.pi
)

phase_h1_plot = (
    np.unwrap(np.angle(H_h1_plot))
    * 180.0 / np.pi
)


# ============================================================
# 11. REPORT PEAK GAINS
# ============================================================

fft_peak_index = np.nanargmax(gain_fft_plot)
h1_peak_index = np.nanargmax(gain_h1_plot)

print(
    "\nDirect FFT peak in selected frequency range:"
)
print(
    f"  Frequency: {f_fft_plot[fft_peak_index]:.4f} Hz"
)
print(
    f"  Gain:      {gain_fft_plot[fft_peak_index]:.6f}"
)

print(
    "\nH1 peak in selected frequency range:"
)
print(
    f"  Frequency: {f_h1_plot[h1_peak_index]:.4f} Hz"
)
print(
    f"  Gain:      {gain_h1_plot[h1_peak_index]:.6f}"
)
print(
    f"  Coherence: {coherence_plot[h1_peak_index]:.6f}"
)


# ============================================================
# 12. PLOT TRANSFER-FUNCTION ESTIMATES
# ============================================================

fig, axes = plt.subplots(
    nrows=3,
    ncols=1,
    figsize=(11, 10),
    sharex=True
)


# ------------------------------------------------------------
# Transfer-function gain
# ------------------------------------------------------------

axes[0].plot(
    f_fft_plot,
    gain_fft_plot,
    color="tab:blue",
    linewidth=1.0,
    alpha=0.75,
    label=r"Direct FFT: $T_m/T_e$"
)

axes[0].plot(
    f_h1_plot,
    gain_h1_plot,
    color="tab:red",
    linewidth=2.0,
    label=r"$H_1=S_{T_eT_m}/S_{T_eT_e}$"
)

axes[0].set_ylabel(
    r"Gain, $|T_m/T_e|$"
)
axes[0].set_title(
    "Estimated Plant Transfer Function"
)
axes[0].grid(True, alpha=0.3)
axes[0].legend()


# ------------------------------------------------------------
# Transfer-function phase
# ------------------------------------------------------------

axes[1].plot(
    f_fft_plot,
    phase_fft_plot,
    color="tab:blue",
    linewidth=1.0,
    alpha=0.75,
    label="Direct FFT"
)

axes[1].plot(
    f_h1_plot,
    phase_h1_plot,
    color="tab:red",
    linewidth=2.0,
    label=r"$H_1$ estimator"
)

axes[1].set_ylabel(
    "Phase (degrees)"
)
axes[1].grid(True, alpha=0.3)
axes[1].legend()


# ------------------------------------------------------------
# Magnitude-squared coherence
# ------------------------------------------------------------

axes[2].plot(
    f_h1_plot,
    coherence_plot,
    color="tab:green",
    linewidth=2.0
)

axes[2].axhline(
    COHERENCE_THRESHOLD,
    color="black",
    linestyle="--",
    linewidth=1.2,
    label=(
        f"Coherence = "
        f"{COHERENCE_THRESHOLD}"
    )
)

axes[2].set_xlabel(
    "Frequency (Hz)"
)
axes[2].set_ylabel(
    r"Coherence, $\gamma^2$"
)
axes[2].set_ylim(
    0.0,
    1.05
)
axes[2].grid(True, alpha=0.3)
axes[2].legend()

# Apply the requested frequency range to all subplots
axes[2].set_xlim(
    MIN_FREQUENCY,
    MAX_FREQUENCY
)

plt.tight_layout()
plt.show()


# ============================================================
# 13. OPTIONAL: PLOT GAIN IN DECIBELS
# ============================================================

gain_fft_db = 20.0 * np.log10(
    np.maximum(gain_fft_plot, 1e-15)
)

gain_h1_db = 20.0 * np.log10(
    np.maximum(gain_h1_plot, 1e-15)
)

plt.figure(
    figsize=(11, 5)
)

plt.plot(
    f_fft_plot,
    gain_fft_db,
    color="tab:blue",
    linewidth=1.0,
    alpha=0.75,
    label="Direct FFT"
)

plt.plot(
    f_h1_plot,
    gain_h1_db,
    color="tab:red",
    linewidth=2.0,
    label=r"$H_1$ estimator"
)

plt.xlim(
    MIN_FREQUENCY,
    MAX_FREQUENCY
)

plt.xlabel(
    "Frequency (Hz)"
)

plt.ylabel(
    r"Gain, $20\log_{10}|T_m/T_e|$ (dB)"
)

plt.title(
    "Estimated Plant Transfer-Function Gain"
)

plt.grid(
    True,
    alpha=0.3
)

plt.legend()
plt.tight_layout()
plt.show()
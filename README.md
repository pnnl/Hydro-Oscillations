# Grid Oscillations and Dynamics Assessment Considering Hydropower Operations

## Overview

This repository contains outputs from a PNNL project that aims to:
- Understand if/how different hydrological conditions impact grid stability
- Understand how the dynamics of emerging grid technologies affect hydropower operations

## Repository Structure

| Folder | Description |
|---|---|
| `Hydro_Shaft_Fatigue_Risk_Assessment` | This folder contains EMT models of a multi-mass hydroelectric generator connected to a AI-training data center via a short transmission line and an infinite bus. The models help study how forced oscillations induced by AI-training loads can get translated to oscillations in generator output power, electrical torque, and shaft torque, and how the risk of oscillation amplification changes with oscillation frequency and distance from load. See folder README for details.  |
| `Hydrological_Modeling` | This folder contains PSLF versions of the WECC 240-bus and Nordic 44-bus grid models, where the governor models of the hydroelectric generators have been modified to represent varying water head levels. Three different hydrological scenarios have been represented for each grid model. Additionally, automation scripts are provided to generate cases representing these varying conditions. The models will be helpful for analyzing how water level variation impacts stability in hydropower-rich grids. See folder README for details. |

Each folder contains its own README with detailed description, methodology, and usage instructions.

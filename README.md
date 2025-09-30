# Hydro-Oscillations
Grid Oscillations and Dynamics Assessment Considering Hydropower Operations

## Scripts to Automate Modeling of Hydrological Conditions using PSLF
Set of codes for accurately modeling the water head variation in hydro power plants is provided. Specifically four files are needed.
1) Preprocessed Input csv creation  (Python)
2) Modifying power flow for new hydrological condition (EPCL)
3) Break Insertion for different hydrological conditions (EPCL)
4) Channel to csv converter (EPCL plot)

## Nordic 44 Examples
Folder Named Nordic_44_PSLF_Files has three subfolders containing examples of modeling different hydrological conditions.
1) C1_N44_5300 - Break insertion using base case PSLF files
2) C1_N44_5300 - Break insertion for WH = 0.8, HR = 20%
3) C3_N44_5300 - Break insertion for WH = 0.7, HR = 20%

<p align="justify"> Logic explained in Automated Script subsection is used to create these examples. The break insertion is carried out at bus 5300 in the Nordic 44 test system. A 500 MW load which was originally out of service was brought in-service and back to out-of-service after 0.5 seconds as part of break insertion test. The subsequent output files can be used for the modal analysis.</p>

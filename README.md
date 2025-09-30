# Hydro-Oscillations
Grid Oscillations and Dynamics Assessment Considering Hydropower Operations

## Scripts to Automate Modeling of Hydrological Conditions using PSLF
<p align="justify"> This section explains the set of scripts designed to automate modeling the hydrological conditions for hydro power plants for power system simulations. Specifically two hydrological parameters are varied in this study - <b> Water Head (WH)</b>  and <b>Head Room (HR)</b> . WH denotes the height difference (vertical distance) between the water surface at the reservoir and water level at the turbine outlet, reported in pu. HR on the other hand is an electrical quanitity and is denoted using the percentage difference between maximum active power a machine can produce (Pmax) and the machine active power output (Pgen).GE PSLF (Positive Sequence Load Flow) software was used to model these hydrological conditions. The hydrological condition modeling is implemented using a set of four scripts as explained below. </p>

1. Preprocessed Input csv creation  (Python)
2. Modifying power flow for new hydrological condition (EPCL)
3. Brake Insertion for different hydrological conditions (EPCL)
4. Channel to csv converter (EPCL plot)

The python file "1_WHV_Input_CSV_Generation.py" implements step 1 - Preprocessed Input csv creation. This file extracts the hydro generators data of the test system, derates the generators, and calculates the new power output for hydro generator based on the WH and HR parameter values. 

EPCL script "2_Modifying_PowerFlow_for_WHV.p" is used to modify the power flow case in step 2. This script sets the new Pgen and Pmax values calculated in step 1, for one hydro generator at a time and runs a governor power flow each time for re-dispatch. The output of this step is a new power flow file (.sav extension) which will be used in the subsequent step.

EPCL script "3_WHV_hdam_var_Break_Insertion.p" takes in the modified power flow case as input and sets the appropriate parameters for changing water heads in hydro governor models (hdam parameter in hygov model). Following this a brake insertion test is carried out. The outputs of this test is saved as channel file (.chf).

Finally,  "4_CHF_to_CSV_WECC_240_PSLF_plot.p" helps in converting the channels file created into a csv file. This file calls "4b_WECC_240_Channels_List.txt", hence it must be placed in the same directory.

## Nordic 44 Bus System Examples
Folder Named Nordic_44_PSLF_Files has three subfolders containing examples of modeling different hydrological conditions.
1) C1_N44_5300 - brake insertion using base case PSLF files
2) C1_N44_5300 - brake insertion for WH = 0.8, HR = 20%
3) C3_N44_5300 - brake insertion for WH = 0.7, HR = 20%

<p align="justify"> Logic explained in Automated Script subsection is used to create these examples. The brake insertion is carried out at bus 5300 in the Nordic 44 test system. A 500 MW load which was originally out of service was brought in-service and back to out-of-service after 0.5 seconds as part of brake insertion test. The subsequent output files can be used for the modal analysis.</p>

## WECC 240 Bus System Examples
Folder Named WECC_240_PSLF_Files has three subfolders containing examples of modeling different hydrological conditions.
1) C1_WECC240_1302 - brake insertion using base case PSLF files
2) C1_WECC240_1302 - brake insertion for WH = 0.8, HR = 20%
3) C3_WECC240_1302 - brake insertion for WH = 0.7, HR = 20%

<p align="justify">  The brake insertion is carried out at bus 1302 in the WECC 240 bus test system. A 1000 MW load which was originally out of service was brought in-service and back to out-of-service after 0.5 seconds as part of brake insertion test. The subsequent output files can be used for the modal analysis.</p>

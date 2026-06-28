### This file creates the neccessary input csv files to PSLF scripts for Hydrological Conditions Varying and Break Insertion Test

# Imprting neccessary libraries
import numpy as np
import pandas as pd


##################################################################################
########### Part I - Creating Input for Modifying PowerFlow part #################
##################################################################################


# Input to this file is the Generation data of Test system under consideration - extracted from PSLF without any modification
df = pd.read_csv('MiniWECC240_Gens_Data_csv_preprocessing_input.csv', sep="\t", engine="python", header=None)
Gen_Data_np = df.values

# Identifying the Hydro Generators
Hydro_gen_indices = df[df.iloc[:, 3].str.contains("H")].index.tolist() ## for example test system, all hydro generators have "H" in Gen ID, if different logic, change accordingly
N44_Hydro_Bus_Numbers = df.values[Hydro_gen_indices, 0]
print(df.values[Hydro_gen_indices, 0])

################################################################
################################################################
################################################################
### Parameters of this study
Headroom_rho = 10/100 ## Head room = Pgen/ Pmax, denoted by HR in readme
Water_head_H = 0.7 ## Water Head = pu height of water in reservoir
################################################################
################################################################
################################################################
pmax_col = 27      # Column index for Pmax_old (from PSLF Gen data)
pgen_col = 8     # Column index for Pgen_old (from PSLF Gen data)

# --- Mask for Hydro rows ---
mask = np.char.find(Gen_Data_np[:, 3].astype(str), "H") >= 0
type_col = np.where(mask, 'H', 'N').reshape(-1, 1)

# --- Extract original values ---
Pmax_old = Gen_Data_np[:, pmax_col].astype(float).copy()
Pgen_old = Gen_Data_np[:, pgen_col].astype(float).copy()

# --- Derating + Updating operating conditions - Update only Hydro rows ---
Pmax_new = Pmax_old.copy()
Pmax_new[mask] = Pmax_old[mask] * (Water_head_H ** 1.5)
print(Pmax_new[mask][0])
Pgen_new = Pgen_old.copy()
Pgen_new[mask] = Pmax_new[mask] * (1 - Headroom_rho)
print(Pgen_new[mask][0])
for k in range(len(Pgen_old)):
    if(Pgen_new[k]>Pgen_old[k]):
        Pgen_new[k] = Pgen_old[k]

# --- Creating output file ---
Output = np.hstack([
    Gen_Data_np[:, 0].reshape(-1, 1),  # Bus number
    type_col,                          # H/N flag
    Gen_Data_np[:, 1:6],               # Original columns 1 to 5
    Pgen_old.reshape(-1, 1),           # Original Pgen
    Pmax_old.reshape(-1, 1),           # Original Pmax
    Pgen_new.reshape(-1, 1),           # New Pgen
    Pmax_new.reshape(-1, 1)            # New Pmax
])

# Save the csv file needed for modifying powerflow
df_out = pd.DataFrame(Output[mask])
df_out.iloc[:,2] = df_out.iloc[:,2].str.replace(" ", "")
Header = ['Bus_number', 'Hydro or not', 'Bus name','Voltage level', 'ID', 'Status', 'BL', 'Pgen_old', 'Pmax_old', 'Pgen_new', 'Pmax_new']
df_out.to_csv('WHV_S1_NewOC_'+str(Water_head_H)+'_HR_'+str(Headroom_rho)+'perc_corr_WECC240.csv', header = None, index=False)

##################################################################################
########### Part II - Creating Input for Dynamic hdam variation part #############
##################################################################################


Data_hydro_gens_modified_np = Output[mask]
Last_column_num = Data_hydro_gens_modified_np.shape[1]
Data_hydro_gens_modified_np_new = np.hstack((Data_hydro_gens_modified_np, (Data_hydro_gens_modified_np[:,9]/Data_hydro_gens_modified_np[:,10]).reshape(-1,1) ))

# np_out = np.hstack((Data_hydro_gens_modified_np_new[:,0:6], Data_hydro_gens_modified_np_new[:,-1].reshape(-1,1)))
hdam_para = Water_head_H
hdam_vector = np.zeros((Data_hydro_gens_modified_np_new.shape[0], 1))


## Setting the new hdam parameter for all participating hydro generators
for k in range(Data_hydro_gens_modified_np_new.shape[0]):
    if( (Data_hydro_gens_modified_np[k,9]/Data_hydro_gens_modified_np[k,10]) > (Water_head_H-0.02)) and ((Data_hydro_gens_modified_np[k,9]/Data_hydro_gens_modified_np[k,10]) < (Water_head_H+0.02)):
        hdam_vector[k] = hdam_para
    else:
        hdam_vector[k] = 1
        

np_out = np.hstack((Data_hydro_gens_modified_np_new[:,0:6], (hdam_vector).reshape(-1,1)))

### saving the csv file to use for Dynamic hdam variation
df_out = pd.DataFrame(np_out)
df_out.iloc[:,2] = df_out.iloc[:,2].str.replace(" ", "")
df_out.to_csv('WHV_S2_Varying_hdam_'+str(Water_head_H)+'_HR_'+str(Headroom_rho)+'perc_corr_WECC240.csv', header = None, index=False)


    
    



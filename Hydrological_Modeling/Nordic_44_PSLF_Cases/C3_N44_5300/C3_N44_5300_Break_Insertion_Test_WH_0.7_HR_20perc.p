/* Setting the working directory*/
@ret = change_dir("C:\Users\varg349\OneDrive - PNNL\Antos_Files\2. GridODA - WPTO\Water Head Variation Study\Data Gen - N44\BreakInsertion_N44_b5300")


dim #Bus_number[50]
dim *Hydro_flag[50][32]
dim *Bus_names[50][32]
dim #Voltage_level[50]
dim *Unit_ID[50]
dim *Status[50]
dim *BL[50]
dim #WH[50]
dim #FLN[50]

dypar[0].omegao = 2*50*3.141592

$dyn = "N44_Statnett_PSS2A_Kg_2_a.dyd"
$rep = "pslf_DYD_hdam_change.rep"
$rep1 = "pslf_Init_hdam_change.rep"

@num_total_gens = 80
@num_hydro_gens = 50


@return = getf("N44_Statnett_GE_origi_BI_Load_b5300_L_500_MW_C9.sav")   /*loading the sav case after making hydro units update in the powerflow*/
solpar[0].tapadj = 0 
solpar[0].swsadj = 0 
solpar[0].psadj  = 0
solpar[0].dccadj = 0
@return=robustsoln("<0>")
@return = psds()
@return = rdyd($dyn,$rep,1,1,1)



for @i=0 to @num_hydro_gens-1
	#FLN[@i] = 1
next

$Data = "N44_Hydro_Gens_Latest_Water_Head_DynFile_Input_WH_0p7_HR_20perc.csv"  /*comment the above line and need to use this line for the base case scenario where head value for all the hydro units is 1 pu*/
@ret=setinput($Data)

logterm("Successfully read the csv file!","<")

/* Setting the individual variables from the read csv input $Data */


for @i=0 to @num_hydro_gens-1
	@ret1=input($Data, #Bus_number[@i], *Hydro_flag[@i], *Bus_names[@i], #Voltage_level[@i], *Unit_ID[@i], *Status[@i], #WH[@i])
next




@count = 0
@count1 = 0



for @i = 0 to @num_hydro_gens-1
	if (#FLN[@i] = 1)
		@count = @count+1
		@ret4 = setmodpar(1,#Bus_number[@i],-1,*Unit_ID[@i],0,"hygov","hdam",#WH[@i])	

		logterm(@ret4," is the return 4 value <")

		
		if ((@ret4 = 0)) 
			@count1 = @count1+1
		endif
	endif
next

logterm(@count," is the total no of gens that are supposed to be updated <")
logterm(@count1," is the total no of gens updated <")


$channels_INIT_errors = "N44_WH_HR_var_C9_5300.chf"

logterm("Setting dynamic parameters")
dypar[0].accfy = 0.8
dypar[0].itfymx = 50
dypar[0].tolfy = 0.0001

logterm("Initializing dynamic simulation")


@return = init($channels_INIT_errors,$rep1,1,1)

dypar[0].nplot = 1 
dypar[0].nscreen = 200 
dypar[0].tpause = 5
@return = run()


logterm("Running flat run till 5s")
@return = run()


logterm("Inserting the break - load index 3")
load[16].st = 1

logterm("Running dynamic simulation till 5.5 s")
dypar[0].tpause = 5.5
@return = run()

logterm("Removing the break - load index 3")
load[16].st = 0

logterm("Running dynamic simulation till 75s")
dypar[0].tpause = 75

@return = run()


logterm("The end","<")





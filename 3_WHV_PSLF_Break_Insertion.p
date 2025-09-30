/* Setting the working directory*/
@ret = change_dir("D:\AV\MiniWECC240_PSLFv22_SD\Case14_WECC240_WH_0p8_HR_0p1_BI_4101")


dim #Bus_number[25]
dim *Hydro_flag[25][32]
dim *Bus_names[25][32]
dim #Voltage_level[25]
dim *Unit_ID[25]
dim *Status[25]
dim *BL[25]
dim #WH[25]
dim #FLN[25]

dypar[0].omegao = 2*60*3.141592

$dyn = "240bus_MiniWECC_PSLF_dyd.dyd"
$rep = "pslf_DYD_hdam_change.rep"
$rep1 = "pslf_Init_hdam_change.rep"

@num_total_gens = 146
@num_hydro_gens = 25


@return = getf("WECC240_newOC_C14.sav")   /*loading the sav case after making hydro units update in the powerflow*/
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

$Data = "WHV_S2_Varying_hdam_0.8_HR_0.1perc_corr_WECC240.csv"  /*comment the above line and need to use this line for the base case scenario where head value for all the hydro units is 1 pu*/
@ret=setinput($Data)

logterm("Successfully read the csv file!","<")

/* Setting the individual variables from the read csv input $Data */


for @i=0 to @num_hydro_gens-1
	@ret1=input($Data, #Bus_number[@i], *Hydro_flag[@i], *Bus_names[@i], #Voltage_level[@i], *Unit_ID[@i], *Status[@i], #WH[@i])
	logterm(#Voltage_level[@i]," are the voltage levels <")
	logterm(*Unit_ID[@i]," are the unit ID <")
next




@count = 0
@count1 = 0



for @i = 0 to @num_hydro_gens-1
	if (#FLN[@i] = 1)
		@count = @count+1
		@ret4 = setmodpar(1,#Bus_number[@i],-1,*Unit_ID[@i],0,"hygov","hdam",#WH[@i])	
		
		logterm(#Bus_number[@i]," is the bus number <")
		logterm(*Unit_ID[@i]," is the unit ID <")
		logterm(#WH[@i]," is the new WH value <")
	
		logterm(@ret4," is the return 4 value <")

		
		if ((@ret4 = 0)) 
			@count1 = @count1+1
		endif
	endif
next

logterm(@count," is the total no of gens that are supposed to be updated <")
logterm(@count1," is the total no of gens updated <")


$channels_INIT_errors = "WECC240_WH_HR_var_C14_L_4101.chf"

logterm("Setting dynamic parameters")
dypar[0].accfy = 0.8
dypar[0].itfymx = 25
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
load[99].st = 1

logterm("Running dynamic simulation till 5.5 s")
dypar[0].tpause = 5.5
@return = run()

logterm("Removing the break - load index 3")
load[99].st = 0

logterm("Running dynamic simulation till 75s")
dypar[0].tpause = 75

@return = run()


logterm("The end","<")





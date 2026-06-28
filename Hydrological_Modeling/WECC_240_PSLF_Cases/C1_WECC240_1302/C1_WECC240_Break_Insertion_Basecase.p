/* Setting the working directory*/
@ret = change_dir("D:\AV\MiniWECC240_PSLFv22_SD\Case1_WECC240_BaseCase_BI_1302")


dypar[0].omegao = 2*60*3.141592

$dyn = "240bus_MiniWECC_PSLF_dyd.dyd"
$rep = "pslf_DYD_hdam_change.rep"
$rep1 = "pslf_Init_hdam_change.rep"


@return = getf("240bus_MiniWECC_PSLF_sav_L_1302_1000MW.sav")   /*loading the sav case after making hydro units update in the powerflow*/
solpar[0].tapadj = 0 
solpar[0].swsadj = 0 
solpar[0].psadj  = 0
solpar[0].dccadj = 0
@return=robustsoln("<0>")
@return = psds()
@return = rdyd($dyn,$rep,1,1,1)



$channels_INIT_errors = "WECC240_Basecase_C1_L_1302.chf"

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


logterm("Inserting the break - load index 9")
load[9].st = 1

logterm("Running dynamic simulation till 5.5 s")
dypar[0].tpause = 5.5
@return = run()

logterm("Removing the break - load index 9")
load[9].st = 0

logterm("Running dynamic simulation till 75s")
dypar[0].tpause = 75

@return = run()


logterm("The end","<")





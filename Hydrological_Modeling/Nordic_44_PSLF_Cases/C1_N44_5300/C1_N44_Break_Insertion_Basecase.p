/* Setting the working directory*/
@ret = change_dir("C:\Users\varg349\OneDrive - PNNL\Antos_Files\2. GridODA - WPTO\Water Head Variation Study\Data Gen - N44\BreakInsertion_N44_b5300")


dypar[0].omegao = 2*50*3.141592

$dyn = "N44_Statnett_PSS2A_Kg_2_a.dyd"
$rep = "pslf_DYD_hdam_change.rep"
$rep1 = "pslf_Init_hdam_change.rep"


@return = getf("N44_Statnett_GE_origi_BI_Load_b5300_L_500_MW.sav")   /*loading the sav case after making hydro units update in the powerflow*/
solpar[0].tapadj = 0 
solpar[0].swsadj = 0 
solpar[0].psadj  = 0
solpar[0].dccadj = 0
@return=robustsoln("<0>")
@return = psds()
@return = rdyd($dyn,$rep,1,1,1)



$channels_INIT_errors = "C7_Basecase_BI_N44_5300.chf"

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





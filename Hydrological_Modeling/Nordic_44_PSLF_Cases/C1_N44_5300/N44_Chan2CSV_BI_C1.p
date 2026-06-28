@ret = change_dir("C:\Users\varg349\OneDrive - PNNL\Antos_Files\2. GridODA - WPTO\Water Head Variation Study\Data Gen - N44\BreakInsertion_N44_b5300") /*change this to local user directory where the sav and dyd files are located*/

@headerflag = 1 
@selFlag = 1

$name1 = "C7_Basecase_BI_N44_5300.csv"
$name7 = "C7_Basecase_BI_N44_5300.chf"
	
@ret = getp($name7)
@ret = chan2csv(@headerflag,@selFlag,"Channels_txt_N44_f_Vm_Va_Pg.txt",$name1)
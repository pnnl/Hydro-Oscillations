@ret = change_dir("D:\AV\MiniWECC240_PSLFv22_SD\Case3_WECC240_WH_0p7_HR_0p2_BI_1302") /*change this to local user directory where the sav and dyd files are located*/

@headerflag = 1 
@selFlag = 1

$name1 = "WECC240_WH_HR_var_C3_L_1302.csv"
$name7 = "WECC240_WH_HR_var_C3_L_1302.chf"
	
@ret = getp($name7)
@ret = chan2csv(@headerflag,@selFlag,"WECC_240_all_channels_txt_Vm_Va_Pg_f.txt",$name1)
@ret = change_dir("D:\AV\MiniWECC240_PSLFv22_SD\Case14_WECC240_WH_0p8_HR_0p1_BI_4101") /*change this to local user directory where the sav and dyd files are located*/

@headerflag = 1 
@selFlag = 1

$name1 = "WECC240_out.csv"
$name7 = "WECC240_out.chf"
	
@ret = getp($name7)
@ret = chan2csv(@headerflag,@selFlag,"WECC_240_all_channels_txt_Vm_Va_Pg_f.txt",$name1)
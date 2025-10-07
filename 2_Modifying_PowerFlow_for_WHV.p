/* Setting the working directory*/
@ret = change_dir("D:\AV\MiniWECC240_PSLFv22_SD\Case14_WECC240_WH_0p8_HR_0p1_BI_4101")


/* Initializing varaibles with dimension*/
/* 25 is the total number of hydro gneerators in this example*/
dim #Bus_number[25]
dim *Hydro_flag[25][32]
dim *Bus_names[25][32]
dim #Voltage_level[25]
dim *Unit_ID[25]
dim *Status[25]
dim *BL[25]
dim #PGen_old[25]
dim #PMax_old[25]
dim #PGen_new[25]
dim #PMax_new[25]

@iteration = 1
/* Read the sav file */
logterm("Reading the sav file!")
$original_sav = "240bus_MiniWECC_PSLF_sav_L_4101" 
$original_sav_final	 =  $original_sav+ ".sav"
@return = getf($original_sav_final)
logterm("Successfully read the sav file!")

/* Read csv file with modified Pgen and Pmax values for Hydro gens */
logterm("Reading the csv file with modified Pgen Pmax info for Hydro!")
$Data = "WHV_S1_NewOC_0.8_HR_0.1perc_corr_WECC240.csv" 
@ret=setinput($Data)
logterm(@ret,"<")
logterm("Successfully read  ~~ the csv file!","<")


/* Setting the individual variables from the read csv input $Data */
@num_total_gens = 146
@num_hydro_gens = 25
for @i=0 to @num_hydro_gens
	@ret1=input($Data, #Bus_number[@i], *Hydro_flag[@i], *Bus_names[@i], #Voltage_level[@i], *Unit_ID[@i], *Status[@i], *BL[@i], #PGen_old[@i], #PMax_old[@i], #PGen_new[@i], #PMax_new[@i])
	/*logterm(@ret1,"<")*/
next



@temp_var = 1
logterm(#Bus_number[0],"<")
logterm(*Bus_names[0],"<")
logterm(*Unit_ID[0],"<")
logterm(*Hydro_flag[0],"<")
logterm(#Voltage_level[0],"<")
logterm(*Status[0],"<")
logterm(*BL[0],"<")




/* Iterate through each generator, for hydro generators set flag = 1 and for all others dispatch_flag = 1 */	
for @i=0 to @num_total_gens
	@flag = 0
	for @j = 0 to @num_hydro_gens-1
		@bn1 = #Bus_number[@j]
		@bus_index1 = bix(@bn1)			
		if (@bus_index1 = gens[@i].ibgen)
			@flag = 1
		endif
	next
	/*if (@flag != 1 and gens[@i].baseload_flag = 0)*/
	if (@flag != 1)  /*assuming no base load flag constraint*/
		gens[@i].dispatch_flag = 1
	else
		gens[@i].dispatch_flag = 0
	endif
next





/* Saving the sav file iteration = 1 */	
logbuf($iteration_number,@iteration)
$updated_sav = $original_sav  + $iteration_number 
$updated_sav = $updated_sav + ".sav"
@return = savf($updated_sav)


	
/*Start of powerflow update from Hydro units based on water data*/
@k =1
@counter = 1
@counter1 = 1 /*no of hydro generators being updated causing divergence during powerflow solution*/																							
@pgen_change = 0
@net_pgen_change = 0





logterm("<")
logterm($updated_sav,"<")
logterm("<")


/*For every hydro generator, run the for loop*/
for @i=0 to @num_hydro_gens	-1
	logterm(@i," the instant of for loop <")
	@flag4 =0   
	logterm(@k," is the Loop number <")
	logterm(#PGen_new[@i]," is the Pgen new <")
	logterm(*Unit_ID[@i]," is the Generator ID value  <")
	
	@h7 = @k 
	@k = @k + 1
		
	if (#PGen_new[@i] >= 0) 
		@return = getf($updated_sav)
		@b =  #PGen_new[@i]
		@bn = #Bus_number[@i]
		@bus_index = bix(@bn)
		/*@area = busd[abs(@bus_index)].area*/
		@indx = 0
		
		for @j = 0 to @num_total_gens
			@gbus = gens[@indx].ibgen /*bus index of the bus at which the generator is connected*/
			@indx = @indx + 1
			
			@k1 = rec_index( 1,3,#Bus_number[@i],-1,*Unit_ID[@i],0, -1)
			if (@k1 != -1) 
				if (gens[@k1].st = 1)
					if ((@bus_index = @gbus) and (gens[@k1].id = *Unit_ID[@i]))
						
						logterm(@k1,"<")
						logterm(@i,"<")
						logterm(@j,"<")
						logterm(@gbus,"<")
						logterm(@bus_index,"<")
						logterm(gens[@k1].id,"<")
						logterm(*Unit_ID[@i],"<")
						logterm(@indx,"<")
						
						
						@P_G_old = gens[@k1].pgen 
						logterm("inside part", "<")
						
						logterm(busd[@gbus].busnam, "<")
						logterm(*Unit_ID[@i],"<")
						
						logterm(@k1,"<")
						logterm(@gbus,"<")
						logterm(@bus_index,"<")
						logterm(gens[@k1].id,"<")
						logterm(*Unit_ID[@i],"<")
						
						gens[@k1].pgen = #PGen_new[@i]
						gens[@k1].pmin = #PGen_new[@i]
						gens[@k1].pmax = #PMax_new[@i]
						
						@incr = -(#PGen_new[@i] - @P_G_old)
						@pgen_change = @pgen_change + abs(@incr)
						
						@net_pgen_change = @net_pgen_change + @incr
						@deltp = @incr    /*compensating rest of the generators*/
						
						logterm(@P_G_old," is the pgen from old powerflow <")
							
						logterm(@incr," is the amount of Pgen changed <")
						
						@rdopt = 0
						@govpf = 1
						@rdbl = 0
						@arswing = 0
						@dispnegunits = 0
						@maxiter = 25
						@prflag = 1
						@ret = redisp(@deltp, @rdopt, @govpf, @rdbl, @arswing,@dispnegunits, @maxiter, @prflag) /*running governor power flow*/
					
						solpar[0].tapadj = 0 
						solpar[0].swsadj = 0 
						solpar[0].psadj  = 0
						solpar[0].dccadj = 0
						
						solpar[0].itnrmx = 100
				            
						if (@h7 <= 25)
							@return2=solnv("<0>")
						endif
						
						if (@return2 < 0)
							
								logterm(@i," is the skipped loop number <")
								@counter1 = @counter1+1
						
						
								quitfor
						
						else
							@flag4 = 1

							
				
							@counter = @counter+1
				
							@return = savf($updated_sav)
			
							quitfor
					
						endif
						
					endif
				endif
			endif
		next
		logterm(@indx,"<")
		logterm(@gbus,"<")
	endif
	

		
next

@return = savf("WECC240_newOC.sav") /*saving the updated sav file*/

@ret=close($Data)	

logterm("End Flag!","<")


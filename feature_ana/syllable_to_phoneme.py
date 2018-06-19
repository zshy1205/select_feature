def separatePinyin(pinyin):
	tone = 1
	initial = ''
	final = ''
	# special handing of pinyin conversion
	if (pinyin[0] == 'y'):
	
		final_temp = list(pinyin);
		final_temp[0] = 'i';
		#	 ya->ia, yan->ian, yang->iang, yao->iao, ye->ie, yo->io, yong->iong, you->iou
		#	 yi->i, yin->in, ying->ing
		#	 yu->v, yuan->van, yue->ve, yun->vn
		if (len(final_temp) >= 2 and final_temp[1] == 'u'):
			final_temp[1] = 'v';
		if (len(final_temp)>= 2 and (final_temp[1] == 'i' or final_temp[1] == 'v')):
			final_temp= final_temp[1:];
		'''
		if (final == "io"):
		{
			#	 final = "iou";	
		}
		'''
		for i in final_temp:
			final += i
		initial = "0";
	
	elif (pinyin[0] == 'w'):
	
		#	 wa->ua, wo->uo, wai->uai, wei->uei, wan->uan, wen->uen, wang->uang, weng->ueng
		#	 wu->u
		#	 change 'w' to 'u', except 'wu->u'
		final_temp = list(pinyin);
		final_temp[0] = 'u';
		if (len(pinyin) >= 2 and pinyin[1] == 'u'):
		
			final_temp = pinyin[1:];
		
		for i in final_temp:
			final += i
		initial = "0";
	
	else:
	
		#	 initial should not be empty
		flag = False
		aeiouv = 'aeiouv'
		for i in range(len(pinyin)):
			if aeiouv.find(pinyin[i]) != -1:
				flag = True
				initial = pinyin[:i];
				final = pinyin[i:];
				break
		if not flag:
			return 
		retroflex = False
		#print('initial: ', initial)
		#print('final: ', final)
		if (final[len(final)-1] == 'r'):
		
			retroflex = True;
			final = final[:-1];
		
		#	 special handling of final
		if (final == "i"):
		
			if (initial == "z" or initial == "c" or initial == "s"):
			
				#	 the final of "zi, ci, si" should be "-i"
				final = "ii";
			
			elif (initial == "zh" or initial == "ch" or initial == "sh" or initial == "r"):
			
				#	 the final of "zhi, chi, shi, ri" should be "-I"
				final = "iii";
			
		
		elif (final[0] == 'u' and (initial == "j" or  initial == "q" or initial == "x")):
		
			#	 ju->jv, jue->jve, juan->jvan, jun->jvn,
			#	 qu->qv, que->qve, quan->qvan, qun->qvn,
			#	 xu->xv, xue->xve, xuan->xvan, xun->xvn
			#	 change all 'u' to 'v'
			#final[0] = 'v';
			final = 'v' + final[1:]
		
		elif (final == "ui"):
		
			#	 when there is initial
			#	 ui->uei
			final = "uei";
		
		elif (final == "iu"):
		
			#	 when there is initial
			#	 iu->iou
			final = "iou";
		
		elif (final == "un"):
		
			#	 when there is initial
			#	 un->uen
			final = "uen";
		
		if (retroflex):
		
			final += "r";
		
		if (initial == ""):
		
			initial = "0";
		
	

	if (len(final) > 0 and final[len(final)-1] == 'r'):
	
		if (final == "er"):
		
			#	printf (".%s.%s.%d.\n", initial.c_str(), final.c_str(), tone);
			if (initial == "0" and tone == 4):
			
				final = "ar";
			
		
		elif (final == "iir" or final == "iiir" or final == "enr"):
		
			final = "eir";
		
		elif (final == "air" or final == "anr"):
		
			final = "ar";
		
		elif (final == "ianr"):
		
			final = "iar";
		
		elif (final == "inr"):
		
			final = "ir";
		
		elif (final == "uair" or final == "uanr"):
		
			final = "uar"
		
		elif (final == "uenr"):
		
			final = "ueir";
		
		elif (final == "vnr"):
		
			final = "vr";
		
	elif (initial == "0" and final == "o"):
	
		final = "ou";
	
	return initial,final;


import pinyin_split2 as ps
for x,v in ps.trans.items():
	initial,final = separatePinyin(x)
	initial += '_'
	initial += final

	if ps.trans[x] != initial:
		print(x, "  ", v, "  ", initial)
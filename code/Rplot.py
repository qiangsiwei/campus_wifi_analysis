# -*- coding: utf-8 -*- 

import fileinput

user = {}
for line in fileinput.input("../data/select/select_a"):
	mac = line.strip().split(" ")[0]
	user[mac] = True
fileinput.close()

with open("../data/plot/R_trace_all","w") as f:
	f.write("mac time dura\n")
	for line in fileinput.input("../data/feature/trace_all_statistic_filter"):
		part = line.strip().split(" ")
		mac, objs = part[0], part[3:]
		if user.has_key(mac):
			for one in objs:
				tag, rto = one.split("@")[0], str(int(one.split("@")[1].split(",")[0])/42)
				if tag in ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]:
					f.write(mac+" "+tag+" "+rto+"\n")
	fileinput.close()

with open("../data/plot/R_trace_online","w") as f:
	f.write("mac time dura\n")
	for line in fileinput.input("../data/feature/trace_online_statistic_filter"):
		part = line.strip().split(" ")
		mac, objs = part[0], part[3:]
		if user.has_key(mac):
			for one in objs:
				tag, rto = one.split("@")[0], str(int(one.split("@")[1].split(",")[0])/42)
				if tag in ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]:
					f.write(mac+" "+tag+" "+rto+"\n")
	fileinput.close()
	
jac = {}
for line in fileinput.input("../data/jaccount/jaccount_taged"):
	part = line.strip().split(" ")
	dev, mac, sex, sta, col, age = part[0], part[1], part[2], part[3], part[4], int(part[5])
	if dev == "mobile":
		jac[mac] = {'sex':sex, 'sta':sta, 'col':col, 'age':age}
		if sex == "男性":
			jac[mac]['sex'] = "Male"
		elif sex == "女性":
			jac[mac]['sex'] = "Female"
		if age <= 20:
			jac[mac]['age'] = "<=20"
		elif age > 20 and age <=22 :
			jac[mac]['age'] = "21~22"
		elif age > 22:
			jac[mac]['age'] = ">=23"
		if col == "电子信息与电气工程学院":
			jac[mac]['col'] = "TOP1"
		elif col == "机械与动力工程学院":
			jac[mac]['col'] = "TOP2"
		elif col == "材料科学与工程学院":
			jac[mac]['col'] = "TOP3"
		elif col == "船舶海洋与建筑工程学院":
			jac[mac]['col'] = "TOP4"
		elif col == "安泰经济与管理学院":
			jac[mac]['col'] = "TOP5"
fileinput.close()

with open("../data/plot/R_trace_all_cor","w") as f:
	f.write("mac Acad Adm Ath Cant Hosp Lib Soc Supp Teach Other sex age\n")
	for line in fileinput.input("../data/feature/trace_all_statistic_filter"):
		part = line.strip().split(" ")
		mac, objs, user = part[0], part[3:], {"Acad":"0","Adm":"0","Ath":"0","Cant":"0","Hosp":"0","Lib":"0","Soc":"0","Supp":"0","Teach":"0","Other":"0"}
		for one in objs:
			tag, rto = one.split("@")[0], one.split("@")[1].split(",")[0]
			if tag in ["Acad","Adm","Ath","Cant","Hosp","Lib","Soc","Supp","Teach","Other"]:
				user[tag] = rto
		f.write(mac+' '+user['Acad']+' '+user['Adm']+' '+user['Ath']+' '+user['Cant']+' '+user['Hosp']+' '+user['Lib']+' '+user['Soc']+' '+user['Supp']+' '+user['Teach']+' '+user['Other']+' '+jac[mac]['sex']+' '+jac[mac]['age']+'\n')
	fileinput.close()

with open("../data/plot/R_trace_online_cor","w") as f:
	f.write("mac Acad Adm Ath Cant Hosp Lib Soc Supp Teach Other sex age\n")
	for line in fileinput.input("../data/feature/trace_online_statistic_filter"):
		part = line.strip().split(" ")
		mac, objs, user = part[0], part[3:], {"Acad":"0","Adm":"0","Ath":"0","Cant":"0","Hosp":"0","Lib":"0","Soc":"0","Supp":"0","Teach":"0","Other":"0"}
		for one in objs:
			tag, rto = one.split("@")[0], one.split("@")[1].split(",")[0]
			if tag in ["Acad","Adm","Ath","Cant","Hosp","Lib","Soc","Supp","Teach","Other"]:
				user[tag] = rto
		f.write(mac+' '+user['Acad']+' '+user['Adm']+' '+user['Ath']+' '+user['Cant']+' '+user['Hosp']+' '+user['Lib']+' '+user['Soc']+' '+user['Supp']+' '+user['Teach']+' '+user['Other']+' '+jac[mac]['sex']+' '+jac[mac]['age']+'\n')
	fileinput.close()

# 1:renren, 2:baidu, 3:sina, 4:taobao, 5:qq
mapping = {'1':'1','2':'1','3':'1','27':'1','46':'1','64':'1','69':'1',\
'5':'2','6':'2','21':'2','22':'2','26':'2','60':'2','63':'2','70':'2','77':'2','80':'2','93':'2','98':'2',\
'11':'3','15':'3','16':'3','17':'3','23':'3','24':'3','28':'3','29':'3','51':'3','82':'3','84':'3',\
'19':'4','23':'4','36':'4','39':'4','42':'4','56':'4','57':'4','58':'4','59':'4',\
'20':'5','31':'5','41':'5','45':'5','48':'5','86':'5',\
}
with open("../data/plot/R_trace_http_cor","w") as f:
	f.write("mac renren baidu sina taobao qq sex age\n")
	for line in fileinput.input("../data/feature/trace_http_statistic_filter"):
		part = line.strip().split(" ")
		mac, objs, user = part[0], part[3:], {"renren":0,"baidu":0,"sina":0,"taobao":0,"qq":0}
		for one in objs:
			tag, rto = one.split("@")[0], int(one.split("@")[1].split(",")[1])
			if len(tag.split("+")) == 2 and tag.split("+")[0] == "WD" and ":" in tag:
				tag = tag.split("+")[1]
				hst, typ = tag.split(":")[0], tag.split(":")[1]
				if mapping.has_key(hst):
					top = mapping[hst]
					if top == "1":
						user['renren'] += rto
					elif top == "2":
						user['baidu'] += rto
					elif top == "3":
						user['sina'] += rto
					elif top == "4":
						user['taobao'] += rto
					elif top == "5":
						user['qq'] += rto
		f.write(mac+' '+str(user['renren'])+' '+str(user['baidu'])+' '+str(user['sina'])+' '+str(user['taobao'])+' '+str(user['qq'])+' '+jac[mac]['sex']+' '+jac[mac]['age']+'\n')
	fileinput.close()

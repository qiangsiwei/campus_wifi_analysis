# -*- coding: utf-8 -*- 

import fileinput

FILE_IN = "../data/feature/trace_all_statistic_filter_feature"
# FILE_IN = "../data/feature/trace_http_statistic_filter_feature"
# FILE_IN = "../data/feature/trace_online_statistic_filter_feature"
# FILE_IN = "../data/feature/keywords_normalize"

jac = {}
for line in fileinput.input("../data/jaccount/jaccount_taged"):
	part = line.strip().split(" ")
	dev, mac, sex, sta, col, age = part[0], part[1], part[2], part[3], part[4], part[5]
	if dev == "mobile":
		jac[mac] = {'sex':sex, 'sta':sta, 'col':col, 'age':int(age)}
fileinput.close()

user = {}
for line in fileinput.input("../data/select/select_a"):
	mac = line.strip().split(" ")[0]
	user[mac] = True
fileinput.close()

cnt0, cnt1 = 0, 0
with open(FILE_IN+"_sex","w") as f:
	for line in fileinput.input(FILE_IN):
		part = line.strip().split(" ")
		mac, sex, feat = part[0], jac[part[0]]['sex'], " ".join(part[2:])
		if user.has_key(mac):
			if sex == "男性":
				sex = 0
				cnt0 += 1
			elif sex == "女性":
				sex = 1
				cnt1 += 1
			if sex in [0,1]:
				f.write(mac+' '+str(sex)+' '+feat+'\n')
	fileinput.close()
	print cnt0, cnt1

cnt0, cnt1, cnt2 = 0, 0, 0
with open(FILE_IN+"_age","w") as f:
	for line in fileinput.input(FILE_IN):
		part = line.strip().split(" ")
		mac, age, feat = part[0], jac[part[0]]['age'], " ".join(part[2:])
		if user.has_key(mac):
			if age in [17,18,19,20]:
				age = 0
				cnt0 += 1
			elif age in [21,22]:
				age = 1
				cnt1 += 1
			else:
				age = 2
				cnt2 += 1
			f.write(mac+' '+str(age)+' '+feat+'\n')
	fileinput.close()
	print cnt0, cnt1, cnt2

cnt0, cnt1, cnt2, cnt3, cnt4 = 0, 0, 0, 0, 0
with open(FILE_IN+"_col","w") as f:
	for line in fileinput.input(FILE_IN):
		part = line.strip().split(" ")
		mac, col, feat = part[0], jac[part[0]]['col'], " ".join(part[2:])
		if user.has_key(mac):
			if col == "电子信息与电气工程学院":
				col = 0
				cnt0 += 1
			elif col == "机械与动力工程学院":
				col = 1
				cnt1 += 1
			elif col == "材料科学与工程学院":
				col = 2
				cnt2 += 1
			elif col == "船舶海洋与建筑工程学院":
				col = 3
				cnt3 += 1
			elif col == "安泰经济与管理学院":
				col = 4
				cnt4 += 1
			if col in [0,1,2,3,4]:
				f.write(mac+' '+str(col)+' '+feat+'\n')
	fileinput.close()
	print cnt0, cnt1, cnt2, cnt3, cnt4

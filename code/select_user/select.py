# -*- coding: utf-8 -*- 

import fileinput

set1, set2, set3, set4 = [], [], [], []
for line in fileinput.input("../feature/trace_all_statistic_filter_feature"):
	mac = line.strip().split(" ")[0]
	set1.append(mac)
for line in fileinput.input("../feature/trace_online_statistic_filter_feature"):
	mac = line.strip().split(" ")[0]
	set2.append(mac)
for line in fileinput.input("../feature/trace_http_statistic_filter_feature"):
	mac = line.strip().split(" ")[0]
	set3.append(mac)
for line in fileinput.input("../feature/normalize"):
	mac = line.strip().split(" ")[0]
	set4.append(mac)
set_a = set(set1) & set(set2) & set(set3) & set(set4)
set_b = set(set1) | set(set2) | set(set3) | set(set4)
print len(set_a)
print len(set_b)
file_a = open("select_a","w")
for one in set_a:
	file_a.write(one+'\n')
file_b = open("select_b","w")
for one in set_b:
	file_b.write(one+'\n')

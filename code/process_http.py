# -*- coding: utf-8 -*-  

import glob
import gzip
import math
import time
import fileinput

mapping_host = {}
i = 0
for line in fileinput.input("../data/host/http_host"):
	i += 1
	http_host = line.strip().split(" ")[1]
	mapping_host[http_host] = str(i)
	if i == 1000:
		fileinput.close()
fileinput.close()

mapping_type = {}
i = 0
for line in fileinput.input("../data/host/http_type"):
	i += 1
	http_type = line.strip().split(" ")[1]
	mapping_type[http_type] = str(i)
	if i == 20:
		fileinput.close()
fileinput.close()

mapping = {}
for line in fileinput.input("../data/ap/apclass"):
	part = line.strip().split(" ")
	cls, ap = part[0], part[1]
	mapping[ap] = cls
fileinput.close()

with open("../data/feature/trace_http","w") as f:
	for filename in sorted(glob.glob(r"../data/http/2013*")):
		print filename
		for line in gzip.open(filename):
			part = line.strip().split(" ")
			mac, ap, st, http_host, http_type = part[0], part[1], int(part[3][0:10]), part[9], part[-1]
			bd = "-".join(ap.split("-")[0:-2])
			if mapping.has_key(bd) and mapping_host.has_key(http_host) and mapping_type.has_key(http_type):
				cl, tm, http_host, http_type = mapping[bd], time.gmtime(st+8*3600), mapping_host[http_host], mapping_type[http_type]
				dy, wd, hr = tm.tm_yday, tm.tm_wday, tm.tm_hour
				wd = 1 if 0<=wd and wd<5 else 2
				ss = 1 if 0<=hr and hr<6 else 2 if 6<=hr and hr<12 else 3 if 12<=hr and hr<18 else 4
				f.write(mac+' '+str(dy)+' '+str(wd)+' '+str(ss)+' '+str(hr)+' '+cl+' '+bd+' '+ap+' '+http_host+' '+http_type+'\n')

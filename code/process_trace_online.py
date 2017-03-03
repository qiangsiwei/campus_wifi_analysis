# -*- coding: utf-8 -*-  

from __future__ import division
import math
import time
import fileinput

def params(t1, t2, rt1, rt2):
	tm = time.gmtime((t1+t2)/2+8*3600)
	dy, wd, hr, dr = tm.tm_yday, tm.tm_wday, tm.tm_hour, t2-t1
	wd = 1 if 0<=wd and wd<5 else 2
	ss = 1 if 0<=hr and hr<6 else 2 if 6<=hr and hr<12 else 3 if 12<=hr and hr<18 else 4
	rt1, rt2 = max(t1, rt1), min(t2, rt2)
	rdr = rt2-rt1 if rt2-rt1>0 else 0 
	return dy, wd, ss, hr, dr, rdr

mapping = {}
for line in fileinput.input("../data/trace/all"):
	part = line.strip().split(" ")
	if len(part) == 6:
		mac, ap, st, ft = part[0].replace(":",""), part[1], int(part[2]), int(part[3])
		key = mac+' '+ap+' '+str(st)+' '+str(ft)
		mapping[key] = {'mac':mac, 'ap':ap, 'st':st, 'ft':ft, 'rst':0, 'rft':0}
fileinput.close()

for line in fileinput.input("../data/trace/online"):
	part = line.strip().split(" ")
	key, rst, rft = " ".join(part[0:4]), int(part[6]), int(part[7])
	if mapping.has_key(key):
		mapping[key]['rst'], mapping[key]['rft'] = rst, rft
fileinput.close()

mapping_ap = {}
for line in fileinput.input("../data/ap/apclass"):
	part = line.strip().split(" ")
	cls, ap = part[0], part[1]
	mapping_ap[ap] = cls
fileinput.close()

with open("../data/feature/trace_online","w") as f:
	for k,v in mapping.iteritems():
		mac, ap, st, ft, rst, rft = v['mac'], v['ap'], v['st'], v['ft'], v['rst'], v['rft']
		ca, cb = int(math.ceil(st/3600)), int(math.floor(ft/3600))
		bd = "-".join(ap.split("-")[0:-2])
		if mapping_ap.has_key(bd):
			cl = mapping_ap[bd]
			if ca > cb:
				if st>ft or rst>rft:
					print st, ft, rst, rft
				dy, wd, ss, hr, dr, rdr = params(st, ft, rst, rft)
				f.write(mac+' '+str(dy)+' '+str(wd)+' '+str(ss)+' '+str(hr)+' '+cl+' '+bd+' '+ap+' '+str(dr)+' '+str(rdr)+'\n')
			else:
				dy, wd, ss, hr, dr, rdr = params(st, ca*3600, rst, rft)
				f.write(mac+' '+str(dy)+' '+str(wd)+' '+str(ss)+' '+str(hr)+' '+cl+' '+bd+' '+ap+' '+str(dr)+' '+str(rdr)+'\n')
				for i in range(ca, cb):
					dy, wd, ss, hr, dr, rdr = params(i*3600, (i+1)*3600, rst, rft)
					f.write(mac+' '+str(dy)+' '+str(wd)+' '+str(ss)+' '+str(hr)+' '+cl+' '+bd+' '+ap+' '+str(dr)+' '+str(rdr)+'\n')
				dy, wd, ss, hr, dr, rdr = params(cb*3600, ft, rst, rft)
				f.write(mac+' '+str(dy)+' '+str(wd)+' '+str(ss)+' '+str(hr)+' '+cl+' '+bd+' '+ap+' '+str(dr)+' '+str(rdr)+'\n')

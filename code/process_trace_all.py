# -*- coding: utf-8 -*- 

from __future__ import division
import math
import time
import fileinput

def params(t1, t2):
	tm = time.gmtime((t1+t2)/2+8*3600)
	dy, wd, hr, dr = tm.tm_yday, tm.tm_wday, tm.tm_hour, t2-t1
	wd = 1 if 0<=wd and wd<5 else 2
	ss = 1 if 0<=hr and hr<6 else 2 if 6<=hr and hr<12 else 3 if 12<=hr and hr<18 else 4
	return dy, wd, ss, hr, dr

mapping = {}
for line in fileinput.input("../data/ap/apclass"):
	part = line.strip().split(" ")
	cls, ap = part[0], part[1]
	mapping[ap] = cls
fileinput.close()

with open("../data/feature/trace_all","w") as f:
	for line in fileinput.input("../data/trace/all"):
		part = line.strip().split(" ")
		mac, ap, st, ft = part[0], part[1], int(part[2]), int(part[3])
		ca, cb = int(math.ceil(st/3600)), int(math.floor(ft/3600))
		bd = "-".join(ap.split("-")[0:-2])
		if mapping.has_key(bd):
			cl = mapping[bd]
			if ca > cb:
				dy, wd, ss, hr, dr = params(st, ft)
				f.write(mac+' '+str(dy)+' '+str(wd)+' '+str(ss)+' '+str(hr)+' '+cl+' '+bd+' '+ap+' '+str(dr)+'\n')
			else:
				dy, wd, ss, hr, dr = params(st, ca*3600)
				f.write(mac+' '+str(dy)+' '+str(wd)+' '+str(ss)+' '+str(hr)+' '+cl+' '+bd+' '+ap+' '+str(dr)+'\n')
				for i in range(ca, cb):
					dy, wd, ss, hr, dr = params(i*3600, (i+1)*3600)
					f.write(mac+' '+str(dy)+' '+str(wd)+' '+str(ss)+' '+str(hr)+' '+cl+' '+bd+' '+ap+' '+str(dr)+'\n')
				dy, wd, ss, hr, dr = params(cb*3600, ft)
				f.write(mac+' '+str(dy)+' '+str(wd)+' '+str(ss)+' '+str(hr)+' '+cl+' '+bd+' '+ap+' '+str(dr)+'\n')
	fileinput.close()

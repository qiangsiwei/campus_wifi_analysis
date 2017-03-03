# -*- coding: utf-8 -*-  

import glob
import gzip
import fileinput

mapping = {}

for line in fileinput.input("../data/trace/all"):
	part = line.strip().split(" ")
	if len(part) == 6:
		mac, ap, st, ft, dr, ip = part[0].replace(":",""), part[1], int(part[2]), int(part[3]), int(part[4]), part[5]
		if not mapping.has_key(mac):
			mapping[mac] = []
		mapping[mac].append({'ap':ap,'st':st,'ft':ft,'dr':dr,'min':ft,'max':st})
	
for filename in glob.glob(r"../data/http/2013*"):
	print filename
	for line in gzip.open(filename):
		part = line.strip().split(" ")
		mac, tm = part[0], int(part[3][0:10])
		if mapping.has_key(mac):
			for item in mapping[mac]:
				if item['st']<=tm and item['ft']>=tm:
					if tm<item['min']:
						item['min'] = tm
					if tm>item['max']:
						item['max'] = tm
					break

with open('../data/trace/online', 'w') as f:
	for key, value in mapping.iteritems():
		for item in sorted(value, key=lambda k: k['st'], reverse=False):
			if item['max']-item['min']>0:
				f.write(key+' '+item['ap']+' '+str(item['st'])+' '+str(item['ft'])+' '+str(item['dr'])+' '\
						+ip+' '+str(item['min'])+' '+str(item['max'])+' '+str(item['max']-item['min'])+'\n')

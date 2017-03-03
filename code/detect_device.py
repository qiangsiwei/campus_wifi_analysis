# -*- coding: utf-8 -*-  

import glob
import fileinput

mapping = {}

for filename in sorted(glob.glob(r"../data/http/2013*")):
	print filename
	for line in fileinput.input(filename):
		part = line.strip().split(" ")
		mac, ua = part[0], " ".join(part[11:]).lower()
		if not mapping.has_key(mac):
			mapping[mac] = {'windows':0, 'ios':0, 'android':0, 'winphone':0}
		if 'iphone' in ua or 'ipad' in ua or 'ipod' in ua or 'cfnetwork' in ua:
			mapping[mac]['ios'] += 1
		if 'android' in ua or 'apache-httpclient' in ua:
			mapping[mac]['android'] += 1
		if 'windows phone' in ua or 'windows ce' in ua:
			mapping[mac]['winphone'] += 1

with open("../data/device/device","w") as f:
	for k,v in mapping.iteritems():
		if v['ios']>=v['android'] and v['ios']>=v['winphone']:
			f.write('android '+k+'\n')
		if v['android']>=v['ios'] and v['android']>=v['winphone']:
			f.write('ios '+k+'\n')
		if v['winphone']>=v['ios'] and v['winphone']>=v['android']:
			f.write('winphone '+k+'\n')

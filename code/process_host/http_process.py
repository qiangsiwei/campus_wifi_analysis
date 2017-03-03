# -*- coding: utf-8 -*- 

import fileinput
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

basedir = "../../data/host"

array = []
for line in fileinput.input("{0}/http_host".format(basedir)):
	part = line.strip().split(" ")
	cnt, info = int(part[0]), " ".join(part[1:])
	array.append(cnt)
fileinput.close()
total = sum(array)

f = open("{0}/http_host_ratio".format(basedir),"w")
f.write('n ratio\n0 0.0\n')
c, t = 0, 0
for line in fileinput.input("{0}/http_host".format(basedir)):
	c += 1
	part = line.strip().split(" ")
	cnt = int(part[0])
	t += cnt
	if c%10 == 0:
		f.write(str(c)+' '+str(float(t)/total)+'\n')
	if c == 1000:
		break
fileinput.close()
f.close()

array = []
for line in fileinput.input("{0}/http_type".format(basedir)):
	part = line.strip().split(" ")
	cnt, info = int(part[0]), " ".join(part[1:])
	array.append(cnt)
fileinput.close()
total = sum(array)

f = open("{0}/http_type_ratio".format(basedir),"w")
f.write('n ratio\n0 0.0\n')
c, t = 0, 0
for line in fileinput.input("{0}/http_type".format(basedir)):
	c += 1
	part = line.strip().split(" ")
	cnt = int(part[0])
	t += cnt
	if c%2 == 0:
		f.write(str(c)+' '+str(float(t)/total)+'\n')
	if c == 20:
		break
fileinput.close()
f.close()

f = open("{0}/http_host_top".format(basedir),"w")
f.write('ratio host\n')
c = 0
for line in fileinput.input("{0}/http_host".format(basedir)):
	c += 1
	part = line.strip().split(" ")
	cnt, info = int(part[0]), " ".join(part[1:])
	f.write(str(float(cnt)*100/total)+' '+info+'\n')
	if c == 10:
		break
fileinput.close()
f.close()

f = open("{0}/http_type_top".format(basedir),"w")
f.write('ratio typee\n')
c = 0
for line in fileinput.input("{0}/http_type".format(basedir)):
	c += 1
	part = line.strip().split(" ")
	cnt, info = int(part[0]), " ".join(part[1:])
	f.write(str(float(cnt)*100/total)+' '+info+'\n')
	if c == 10:
		break
fileinput.close()
f.close()

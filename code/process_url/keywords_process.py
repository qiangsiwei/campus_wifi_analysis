# -*- coding: utf-8 -*- 

import fileinput

basedir = "../../data/url"

wordmapping = {}
for line in fileinput.input("{0}/keywords_segmented".format(basedir)):
	words = line.strip().split(" ")[1:]
	for word in words:
		if len(word.decode('utf-8')) >= 2:
			if not wordmapping.has_key(word):
				wordmapping[word] = 0
			wordmapping[word] = wordmapping[word]+1
fileinput.close()

f = open("{0}/keywords_frequency".format(basedir),"w")
for line in fileinput.input("{0}/keywords_segmented".format(basedir)):
	part = line.strip().split(" ")
	mac, words, mapping = part[0], part[1:], {}
	for word in words:
		if wordmapping.has_key(word) and wordmapping[word] >= 5:
			if not mapping.has_key(word):
				mapping[word] = 0
			mapping[word] = mapping[word]+1
	array = []
	for k,v in mapping.iteritems():
		array.append({'k':k,'v':v})
	array = sorted(array, key=lambda k: k['v'], reverse=True)
	f.write(mac)
	for item in array:
		f.write(' '+item['k']+','+str(item['v']))
	f.write('\n')
fileinput.close()
f.close()

glob = {}
for line in fileinput.input("{0}/keywords_frequency".format(basedir)):
	words = line.strip().split(" ")[1:]
	for word in words:
		key = word.split(",")[0]
		if not glob.has_key(key):
			glob[key] = 1
		glob[key] = glob[key]+1
fileinput.close()
array = []
for k,v in glob.iteritems():
	if v >= 10 and v <= 550:
		array.append(k)

jaccounts = {}
for line in fileinput.input("../../data/jaccount/jaccount_taged"):
	part = line.strip().split(" ")
	mac, sex = part[1], part[2]
	jaccounts[mac] = {"男性":0,"女性":1}[sex]
fileinput.close()

f = open("{0}/keywords_normalize".format(basedir),"w")
for line in fileinput.input("{0}/keywords_frequency".format(basedir)):
	part = line.strip().split(" ")
	mac, words, mapping = part[0], part[1:], {}
	for word in words:
		key, val = word.split(",")[0], int(word.split(",")[1])
		mapping[key] = val
	out, total = [], 0
	for item in array:
		if mapping.has_key(item):
			total += 1
			out.append(str(mapping[item]))
		else:
			out.append("0")
	if total>50:
		f.write(mac+' '+str(jaccounts[mac])+' '+" ".join(out)+'\n')
fileinput.close()
f.close()

mapping, wordmapping = {}, {}
for line in fileinput.input("{0}/keywords_frequency".format(basedir)):
	part = line.strip().split(" ")
	mac, words = part[0], part[1:]
	mapping[mac] = len(words)
	for item in words:
		word, freq = item.split(",")[0], int(item.split(",")[1])
		if not wordmapping.has_key(word):
			wordmapping[word] = {'a':0, 'b':0}
		wordmapping[word]['a'] += 1
		wordmapping[word]['b'] += freq

print wordmapping

array = []
for k,v in mapping.iteritems():
	array.append({'k':k,'v':v})
array = sorted(array, key=lambda k: k['v'], reverse=True)
with open("{0}/keywords_mac_statistic".format(basedir),"w") as f:
	f.write("w c\n")
	for c, item in enumerate(array):
		f.write(str(c+1)+' '+str(item['v'])+'\n')

array = []
for k,v in wordmapping.iteritems():
	array.append({'k':k,'a':v['a'],'b':v['b']})
array = sorted(array, key=lambda k: k['a'], reverse = True)
with open("{0}/keywords_frequency_statistic".format(basedir),"w") as f:
	f.write("p n\n")
	for c, item in enumerate(array):
		f.write(str(c+1)+' '+str(item['a'])+'\n')
# 		
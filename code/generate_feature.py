# -*- coding: utf-8 -*-  

import fileinput

def generate(name = ""):
	with open("../data/feature_set/feature_{0}".format(name),"w") as f:
		N = 0
		tags1 = ['cnt','sum','min','max','avg','med','std']
		tags2 = ['cnt','sum','max','avg']
		for tag in tags1:
			N += 1
			f.write(str(N)+' '+"tot"+'_'+tag+'\n')
		for line in fileinput.input("../data/feature/trace_http_statistic_filter"):
			glob = line.strip().split(" ")[3:89]
			for item in glob:
				for tag in tags2:
					N += 1
					f.write(str(N)+' '+item.split("@")[0]+'_'+tag+'\n')
			break
		fileinput.close()
		mapping = {}
		for line in fileinput.input("../data/feature/trace_{0}_statistic_filter".format(name)):
			for item in line.strip().split(" ")[89:]:
				key = item.split("@")[0]
				if not mapping.has_key(key):
					mapping[key] = 0
				mapping[key] += 1
		fileinput.close()
		array = []
		for k,v in mapping.iteritems():
			array.append({'k':k,'v':v})
		array = sorted(array, key=lambda k: k['v'], reverse = True)
		for item in array:
			for tag in tags2:
				N += 1
				f.write(str(N)+' '+item['k']+'_'+tag+'\n')

if __name__ == "__main__":
	generate("all")
	generate("online")
	generate("http")

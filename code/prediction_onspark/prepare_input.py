# -*- coding: utf-8 -*- 

import fileinput
import numpy as np
from sklearn import preprocessing

task = "sex"

classList, docList = [], []
for line in fileinput.input("trace_all_statistic_filter_feature_{0}".format(task)):
	part = line.strip().split(" ")
	mac, cls, feat = part[0], float(part[1]), part[2:]
	array = []
	for f in feat:
		array.append(float(f))
	classList.append(cls)
	docList.append(array)
fileinput.close()
docList, classList = np.array(docList), np.array(classList)
min_max_scaler = preprocessing.MinMaxScaler()
docList = min_max_scaler.fit_transform(docList)

with open("feature_semantic_{0}".format(task),"w") as f;
	for i in range(len(classList)):
		f.write(str(classList[i]))
		for j in range(len(docList[i])):
			f.write(" ")
			f.write("%.3f" %docList[i][j])
		f.write("\n")

with open("feature_semantic_{0}_hdfs".format(task),"w") as f:
	for line in fileinput.input("feature_semantic_{0}".format(task)):
		part = line.strip().split(" ")[0:10]
		f.write(" ".join(part)+"\n")
	
# -*- coding: utf-8 -*- 

import random
import fileinput
import numpy as np
import pyspark.mllib.classification as cl
from pyspark import SparkContext

# training
sc = SparkContext('local', 'Predict_Age')
# sc = SparkContext('spark://127.0.0.1:7077', 'Predict_Age')

# 实例个数
cnt = 400

docList, docList_spatial, docList_cyber, docList_semantic = [], [], [], []

docList_spatial_0,docList_spatial_1,docList_spatial_2 = [],[],[]
# for line in fileinput.input("feature_spatial_age"):
for line in sc.textFile("hdfs://127.0.0.1:9000/feature_spatial_age_hdfs").take(cnt):
	part = line.strip().split(" ")
	array = []
	for f in part:
		array.append(float(f))
	docList_spatial.append(array)
	if float(part[0]) == 0.0:
		docList.append(0)
		docList_spatial_0.append(array)
	if float(part[0]) == 1.0:
		docList.append(1)
		docList_spatial_1.append(array)
	if float(part[0]) == 2.0:
		docList.append(2)
		docList_spatial_2.append(array)
docList_spatial_0v1 = []
for one in docList_spatial_0:
	s = [0.0]
	s.extend(one[1:])
	docList_spatial_0v1.append(s)
for one in docList_spatial_1:
	s = [1.0]
	s.extend(one[1:])
	docList_spatial_0v1.append(s)
docList_spatial_0v2 = []
for one in docList_spatial_0:
	s = [0.0]
	s.extend(one[1:])
	docList_spatial_0v2.append(s)
for one in docList_spatial_2:
	s = [1.0]
	s.extend(one[1:])
	docList_spatial_0v2.append(s)
docList_spatial_1v2 = []
for one in docList_spatial_1:
	s = [0.0]
	s.extend(one[1:])
	docList_spatial_1v2.append(s)
for one in docList_spatial_2:
	s = [1.0]
	s.extend(one[1:])
	docList_spatial_1v2.append(s)
docList_spatial_0v1,docList_spatial_0v2,docList_spatial_1v2 = np.array(docList_spatial_0v1),np.array(docList_spatial_0v2),np.array(docList_spatial_1v2)
svm_spatial_0v1,svm_spatial_0v2,svm_spatial_1v2 = cl.SVMWithSGD.train(sc.parallelize(docList_spatial_0v1)),cl.SVMWithSGD.train(sc.parallelize(docList_spatial_0v2)),cl.SVMWithSGD.train(sc.parallelize(docList_spatial_1v2))

docList_cyber_0,docList_cyber_1,docList_cyber_2 = [],[],[]
# for line in fileinput.input("feature_cyber_age"):
for line in sc.textFile("hdfs://127.0.0.1:9000/feature_cyber_age_hdfs").take(cnt):
	part = line.strip().split(" ")
	array = []
	for f in part:
		array.append(float(f))
	docList_cyber.append(array)
	if float(part[0]) == 0.0:
		docList_cyber_0.append(array)
	if float(part[0]) == 1.0:
		docList_cyber_1.append(array)
	if float(part[0]) == 2.0:
		docList_cyber_2.append(array)
docList_cyber_0v1 = []
for one in docList_cyber_0:
	s = [0.0]
	s.extend(one[1:])
	docList_cyber_0v1.append(s)
for one in docList_cyber_1:
	s = [1.0]
	s.extend(one[1:])
	docList_cyber_0v1.append(s)
docList_cyber_0v2 = []
for one in docList_cyber_0:
	s = [0.0]
	s.extend(one[1:])
	docList_cyber_0v2.append(s)
for one in docList_cyber_2:
	s = [1.0]
	s.extend(one[1:])
	docList_cyber_0v2.append(s)
docList_cyber_1v2 = []
for one in docList_cyber_1:
	s = [0.0]
	s.extend(one[1:])
	docList_cyber_1v2.append(s)
for one in docList_cyber_2:
	s = [1.0]
	s.extend(one[1:])
	docList_cyber_1v2.append(s)
docList_cyber_0v1,docList_cyber_0v2,docList_cyber_1v2 = np.array(docList_cyber_0v1),np.array(docList_cyber_0v2),np.array(docList_cyber_1v2)
svm_cyber_0v1,svm_cyber_0v2,svm_cyber_1v2 = cl.SVMWithSGD.train(sc.parallelize(docList_cyber_0v1)),cl.SVMWithSGD.train(sc.parallelize(docList_cyber_0v2)),cl.SVMWithSGD.train(sc.parallelize(docList_cyber_1v2))

docList_semantic_0,docList_semantic_1,docList_semantic_2 = [],[],[]
# for line in fileinput.input("feature_semantic_age"):
for line in sc.textFile("hdfs://127.0.0.1:9000/feature_semantic_age_hdfs").take(cnt):
	part = line.strip().split(" ")
	array = []
	for f in part:
		array.append(float(f))
	docList_semantic.append(array)
	if float(part[0]) == 0.0:
		docList_semantic_0.append(array)
	if float(part[0]) == 1.0:
		docList_semantic_1.append(array)
	if float(part[0]) == 2.0:
		docList_semantic_2.append(array)
docList_semantic_0v1 = []
for one in docList_semantic_0:
	s = [0.0]
	s.extend(one[1:])
	docList_semantic_0v1.append(s)
for one in docList_semantic_1:
	s = [1.0]
	s.extend(one[1:])
	docList_semantic_0v1.append(s)
docList_semantic_0v2 = []
for one in docList_semantic_0:
	s = [0.0]
	s.extend(one[1:])
	docList_semantic_0v2.append(s)
for one in docList_semantic_2:
	s = [1.0]
	s.extend(one[1:])
	docList_semantic_0v2.append(s)
docList_semantic_1v2 = []
for one in docList_semantic_1:
	s = [0.0]
	s.extend(one[1:])
	docList_semantic_1v2.append(s)
for one in docList_semantic_2:
	s = [1.0]
	s.extend(one[1:])
	docList_semantic_1v2.append(s)
docList_semantic_0v1,docList_semantic_0v2,docList_semantic_1v2 = np.array(docList_semantic_0v1),np.array(docList_semantic_0v2),np.array(docList_semantic_1v2)
nb_semantic_0v1,nb_semantic_0v2,nb_semantic_1v2 = cl.NaiveBayes.train(sc.parallelize(docList_semantic_0v1)),cl.NaiveBayes.train(sc.parallelize(docList_semantic_0v2)),cl.NaiveBayes.train(sc.parallelize(docList_semantic_1v2))

# testing
with open("result_age.txt","w")
	for rd in xrange(cnt):
		pred = round(float(svm_spatial_0v1.predict(np.array(docList_spatial[rd][1:]))+svm_cyber_0v1.predict(np.array(docList_cyber[rd][1:]))+nb_semantic_0v1.predict(np.array(docList_semantic[rd][1:])))/3)
		if pred == 0:
			pred = round(float(svm_spatial_0v2.predict(np.array(docList_spatial[rd][1:]))+svm_cyber_0v2.predict(np.array(docList_cyber[rd][1:]))+nb_semantic_0v2.predict(np.array(docList_semantic[rd][1:])))/3)
			if pred == 0:
				pred = 0
			else:
				pred = 2
		else:
			pred = round(float(svm_spatial_1v2.predict(np.array(docList_spatial[rd][1:]))+svm_cyber_1v2.predict(np.array(docList_cyber[rd][1:]))+nb_semantic_1v2.predict(np.array(docList_semantic[rd][1:])))/3)
			if pred == 0:
				pred = 1
			else:
				pred = 2
		f.write(str(rd)+" "+str(docList[rd])+" "+str(pred)+"\n")

# -*- coding: utf-8 -*- 

import fileinput
import numpy as np
from sklearn import svm
from sklearn import tree
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import pipeline
from sklearn import ensemble
from sklearn import linear_model
from sklearn import preprocessing
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import LeaveOneOut

with open("../../data/prediction/precision_sex","w") as f:
	docList, classList, errorCount, totCount = [], [], 0, 0
	for line in fileinput.input("../../data/prediction/prediction_sex"):
		part = line.strip().split(" ")
		cls, feat = int(part[0]), part[1:]
		feats = []
		classList.append(cls)
		for one in feat:
			feats.append(float(one))
		pred = -1
		if max(feats[6:]) > 0.9998:#url
			if feats[6] == max(feats[6:]):pred = 0
			if feats[7] == max(feats[6:]):pred = 1
		elif max(feats[4:6]) > 0.65:#http
			if feats[4] == max(feats[4:6]):pred = 0
			if feats[5] == max(feats[4:6]):pred = 1
		elif max(feats[0:2]) > 0.70:#all
			if feats[0] == max(feats[0:2]):pred = 0
			if feats[1] == max(feats[0:2]):pred = 1
		elif max(feats[2:4]) > 0.75:#online
			if feats[2] == max(feats[2:4]):pred = 0
			if feats[3] == max(feats[2:4]):pred = 1
		else:
			sum_list = []
			sum_list.append(feats[0]+feats[2]+feats[4]+feats[6])
			sum_list.append(feats[1]+feats[3]+feats[5]+feats[7])
			if sum_list[0] == max(sum_list):pred = 0
			if sum_list[1] == max(sum_list):pred = 1
		f.write(str(cls)+' '+str(pred)+'\n')
	# 	if not pred == -1:
	# 		totCount += 1
	# 		if not pred == cls:
	# 			errorCount += 1
	# print totCount, errorCount
		if not pred == cls:
			errorCount += 1
	fileinput.close()
	print 'the accurate rate is: ', 1-float(errorCount)/len(classList)

with open("../../data/prediction/precision_age","w") as f:
	docList, classList, errorCount, totCount = [], [], 0, 0
	for line in fileinput.input("../../data/prediction/prediction_age"):
		part = line.strip().split(" ")
		cls, feat = int(part[0]), part[1:]
		feats = []
		classList.append(cls)
		for one in feat:
			feats.append(float(one))
		pred = -1
		if max(feats[0:3]) > 0.57:#all
			if feats[0] == max(feats[0:3]):pred = 0
			if feats[1] == max(feats[0:3]):pred = 1
			if feats[2] == max(feats[0:3]):pred = 2
		elif max(feats[3:6]) > 0.92:#online
			if feats[3] == max(feats[3:6]):pred = 0
			if feats[4] == max(feats[3:6]):pred = 1
			if feats[5] == max(feats[3:6]):pred = 2
		elif max(feats[6:9]) > 0.92:#http
			if feats[6] == max(feats[6:9]):pred = 0
			if feats[7] == max(feats[6:9]):pred = 1
			if feats[8] == max(feats[6:9]):pred = 2
		elif max(feats[9:]) > 0.9995:#url
			if feats[9] == max(feats[9:]):pred = 0
			if feats[10] == max(feats[9:]):pred = 1
			if feats[11] == max(feats[9:]):pred = 2
		else:
			sum_list = []
			sum_list.append(feats[0]+feats[3]+feats[6]+feats[9])
			sum_list.append(feats[1]+feats[4]+feats[7]+feats[10])
			sum_list.append(feats[2]+feats[5]+feats[8]+feats[11])
			if sum_list[0] == max(sum_list):pred = 0
			if sum_list[1] == max(sum_list):pred = 1
			if sum_list[2] == max(sum_list):pred = 2
		f.write(str(cls)+' '+str(pred)+'\n')
	# 	if not pred == -1:
	# 		totCount += 1
	# 		if not pred == cls:
	# 			errorCount += 1
	# print totCount, errorCount
		if not pred == cls:
			errorCount += 1
	fileinput.close()
	print 'the accurate rate is: ', 1-float(errorCount)/len(classList)

with open("../../data/prediction/precision_col","w") as f:
	docList, classList, errorCount, totCount = [], [], 0, 0
	for line in fileinput.input("../../data/prediction/prediction_col"):
		part = line.strip().split(" ")
		cls, feat = int(part[0]), part[1:]
		feats = []
		classList.append(cls)
		for one in feat:
			feats.append(float(one))
		pred = -1
		if max(feats[0:5]) > 0.60:#all
			if feats[0] == max(feats[0:5]):pred = 0
			if feats[1] == max(feats[0:5]):pred = 1
			if feats[2] == max(feats[0:5]):pred = 2
			if feats[3] == max(feats[0:5]):pred = 3
			if feats[4] == max(feats[0:5]):pred = 4
		elif max(feats[5:10]) > 0.60:#online
			if feats[5] == max(feats[5:10]):pred = 0
			if feats[6] == max(feats[5:10]):pred = 1
			if feats[7] == max(feats[5:10]):pred = 2
			if feats[8] == max(feats[5:10]):pred = 3
			if feats[9] == max(feats[5:10]):pred = 4
		elif max(feats[10:15]) > 0.90:#http
			if feats[10] == max(feats[10:15]):pred = 0
			if feats[11] == max(feats[10:15]):pred = 1
			if feats[12] == max(feats[10:15]):pred = 2
			if feats[13] == max(feats[10:15]):pred = 3
			if feats[14] == max(feats[10:15]):pred = 4
		elif max(feats[15:]) > 0.9995:#url
			if feats[15] == max(feats[15:]):pred = 0
			if feats[16] == max(feats[15:]):pred = 1
			if feats[17] == max(feats[15:]):pred = 2
			if feats[18] == max(feats[15:]):pred = 3
			if feats[19] == max(feats[15:]):pred = 4
		else:
			sum_list = []
			sum_list.append(feats[0]+feats[5]+feats[10]+feats[15])
			sum_list.append(feats[1]+feats[6]+feats[11]+feats[16])
			sum_list.append(feats[2]+feats[7]+feats[12]+feats[17])
			sum_list.append(feats[3]+feats[8]+feats[13]+feats[18])
			sum_list.append(feats[4]+feats[9]+feats[14]+feats[19])
			if sum_list[0] == max(sum_list):pred = 0
			if sum_list[1] == max(sum_list):pred = 1
			if sum_list[2] == max(sum_list):pred = 2
			if sum_list[3] == max(sum_list):pred = 3
			if sum_list[4] == max(sum_list):pred = 4
		f.write(str(cls)+' '+str(pred)+'\n')
	# 	if not pred == -1:
	# 		totCount += 1
	# 		if not pred == cls:
	# 			errorCount += 1
	# print totCount, errorCount
		if not pred == cls:
			errorCount += 1
	fileinput.close()
	print 'the accurate rate is: ', 1-float(errorCount)/len(classList)

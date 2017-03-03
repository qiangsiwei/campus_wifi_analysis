# -*- coding: utf-8 -*- 

import fileinput
import numpy as np
from sklearn import svm
from sklearn import tree
from sklearn import feature_selection
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import pipeline
from sklearn import ensemble
from sklearn import linear_model
from sklearn import preprocessing
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import LeaveOneOut

user = {}
for line in fileinput.input("../../data/select/select_a"):
	mac = line.strip().split(" ")[0]
	user[mac] = True
cnt_0, cnt_1 = 0, 0
docMap_1, docMap_2, docMap_3, docMap_4, classMap = {}, {}, {}, {}, {}
for line in fileinput.input("../../data/feature/trace_all_statistic_filter_feature_sex"):
	part = line.strip().split(" ")
	mac, sex, feat = part[0], int(part[1]), part[2:]
	if user.has_key(mac):
		if sex == 0:
			cnt_0 += 1
		if sex == 1:
			cnt_1 += 1
		array = []
		for f in feat:
			array.append(float(f))
		docMap_1[mac] = array
		classMap[mac] = sex
fileinput.close()
print cnt_0, cnt_1
for line in fileinput.input("../../data/feature/trace_online_statistic_filter_feature_sex"):
	part = line.strip().split(" ")
	mac, sex, feat = part[0], int(part[1]), part[2:]
	if user.has_key(mac):
		array = []
		for f in feat:
			array.append(float(f))
		docMap_2[mac] = array
fileinput.close()
for line in fileinput.input("../../data/feature/trace_http_statistic_filter_feature_sex"):
	part = line.strip().split(" ")
	mac, sex, feat = part[0], int(part[1]), part[2:]
	if user.has_key(mac):
		array = []
		for f in feat:
			array.append(float(f))
		docMap_3[mac] = array
fileinput.close()
for line in fileinput.input("../../data/feature/keywords_normalize_sex"):
	part = line.strip().split(" ")
	mac, feat = part[0], part[1:]
	if user.has_key(mac):
		array = []
		for f in feat:
			array.append(float(f))
		docMap_4[mac] = array
fileinput.close()

docList_1, docList_2, docList_3, docList_4, classList = [], [], [], [], []
# print len(user.keys()), len(docMap_1.keys()), len(docMap_2.keys()), len(docMap_3.keys()), len(docMap_4.keys())
for k,v in user.iteritems():
	if k in docMap_1 and k in docMap_2 and k in docMap_3 and k in docMap_4 and k in classMap:
		docList_1.append(docMap_1[k])
		docList_2.append(docMap_2[k])
		docList_3.append(docMap_3[k])
		docList_4.append(docMap_4[k])
		classList.append(classMap[k])

docList_1, docList_2, docList_3, docList_4, classList = np.array(docList_1), np.array(docList_2), np.array(docList_3), np.array(docList_4), np.array(classList)
min_max_scaler = preprocessing.MinMaxScaler()
docList_1, docList_2, docList_3 = min_max_scaler.fit_transform(docList_1), min_max_scaler.fit_transform(docList_2), min_max_scaler.fit_transform(docList_3)

cnt, errorCount = 0, 0
loo = LeaveOneOut(len(classList))
trainingdoc, trainingclass = [], []

with open("../../data/prediction/prediction_sex","w") as f:
	for train, test in loo:
		cnt += 1
		print cnt
		trainingdoc_1, trainingdoc_2, trainingdoc_3, trainingdoc_4, trainingclass, testingdoc_1, testingdoc_2, testingdoc_3, testingdoc_4, testingclass\
		= docList_1[train], docList_2[train], docList_3[train], docList_4[train], classList[train], docList_1[test], docList_2[test], docList_3[test], docList_4[test], classList[test]
		clf_1 = pipeline.Pipeline([
		  ('feature_selection', linear_model.LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1, class_weight='auto', random_state=None)),
	      ('classification', svm.SVC(kernel='linear', class_weight='auto', probability=True))
		])
		clf_2 = pipeline.Pipeline([
		  ('feature_selection', linear_model.LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1, class_weight='auto', random_state=None)),
	      ('classification', svm.SVC(kernel='linear', class_weight='auto', probability=True))
		])
		clf_3 = pipeline.Pipeline([
		  ('feature_selection', linear_model.LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1, class_weight='auto', random_state=None)),
	      ('classification', svm.SVC(kernel='linear', class_weight='auto', probability=True))
		])
		gnb = MultinomialNB()
		clf_1.fit(trainingdoc_1, trainingclass)
		clf_2.fit(trainingdoc_2, trainingclass)
		clf_3.fit(trainingdoc_3, trainingclass)
		gnb.fit(trainingdoc_4, trainingclass)
		docList_final = []
		for one in train:
			res_1 = clf_1.predict_proba(docList_1[one])[0]
			res_2 = clf_2.predict_proba(docList_2[one])[0]
			res_3 = clf_3.predict_proba(docList_3[one])[0]
			res_4 = gnb.predict_proba(docList_4[one])[0]
			array = [res_1[0], res_1[1], res_2[0], res_2[1], res_3[0], res_3[1], res_4[0], res_4[1]]
			docList_final.append(array)
		res_1 = clf_1.predict_proba(testingdoc_1)[0]
		res_2 = clf_2.predict_proba(testingdoc_2)[0]
		res_3 = clf_3.predict_proba(testingdoc_3)[0]
		res_4 = gnb.predict_proba(testingdoc_4)[0]
		print testingclass[0], res_1[0], res_2[0], res_3[0], res_4[0]
		f.write(str(testingclass[0])+' '+str(round(res_1[0],5))+' '+str(round(res_1[1],5))\
									   +' '+str(round(res_2[0],5))+' '+str(round(res_2[1],5))\
									   +' '+str(round(res_3[0],5))+' '+str(round(res_3[1],5))\
									   +' '+str(round(res_4[0],5))+' '+str(round(res_4[1],5))+'\n')

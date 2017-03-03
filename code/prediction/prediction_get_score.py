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

def func0(task):
	find_1 = {}
	for line in fileinput.input("../../data/feature_set/feature_all"):
		part = line.strip().split(" ")
		num, sem = int(part[0]), part[1]
		find_1[num] = sem
	fileinput.close()
	find_2 = {}
	for line in fileinput.input("../../data/feature_set/feature_online"):
		part = line.strip().split(" ")
		num, sem = int(part[0]), part[1]
		find_2[num] = sem
	fileinput.close()
	find_3 = {}
	for line in fileinput.input("../../data/feature_set/feature_http"):
		part = line.strip().split(" ")
		num, sem = int(part[0]), part[1]
		find_3[num] = sem
	fileinput.close()
	find_h = {}
	i = 0
	for line in fileinput.input("../../data/host/http_host"):
		i += 1
		hst = line.strip().split(" ")[1].replace("\"","")
		find_h[i] = hst
		if i == 1000:
			fileinput.close()
	find_t = {}
	i = 0
	for line in fileinput.input("../../data/host/http_type"):
		i += 1
		typ = line.strip().split(" ")[1]
		find_t[i] = typ
		if i == 20:
			fileinput.close()
	######
	user = {}
	for line in fileinput.input("../../data/select/select_a"):
		mac = line.strip().split(" ")[0]
		user[mac] = True
	fileinput.close()
	_set = []
	docList, classList = [], []
	for line in fileinput.input("../../data/feature/trace_all_statistic_filter_feature_"+task):
		part = line.strip().split(" ")
		mac, sex, feat = part[0], int(part[1]), part[2:]
		# print len(feat)
		if user.has_key(mac):
			_list = []
			for f in feat:
				_list.append(float(f))
			docList.append(_list)
			classList.append(sex)
	fileinput.close()
	docList, classList = np.array(docList), np.array(classList)
	min_max_scaler = preprocessing.MinMaxScaler()
	docList = min_max_scaler.fit_transform(docList)
	selector = feature_selection.SelectPercentile(percentile=100)
	selector.fit(docList, classList)
	scores = -np.log10(selector.pvalues_)
	c = 0
	for one in list(scores):
		c += 1
		# if one == one:
		# 	_set.append({'f':'all','p':c,'s':one})
		# else:
		# 	_set.append({'f':'all','p':c,'s':0})
	docList, classList = [], []
	for line in fileinput.input("../../data/feature/trace_online_statistic_filter_feature_"+task):
		part = line.strip().split(" ")
		mac, sex, feat = part[0], int(part[1]), part[2:]
		if user.has_key(mac):
			_list = []
			for f in feat:
				_list.append(float(f))
			docList.append(_list)
			classList.append(sex)
	fileinput.close()
	docList, classList = np.array(docList), np.array(classList)
	min_max_scaler = preprocessing.MinMaxScaler()
	docList = min_max_scaler.fit_transform(docList)
	selector = feature_selection.SelectPercentile(percentile=100)
	selector.fit(docList, classList)
	scores = -np.log10(selector.pvalues_)
	c = 0
	for one in list(scores):
		c += 1
		# if one == one:
		# 	_set.append({'f':'online','p':c,'s':one})
		# else:
		# 	_set.append({'f':'online','p':c,'s':0})
	docList, classList = [], []
	for line in fileinput.input("../../data/feature/trace_http_statistic_filter_feature_"+task):
		part = line.strip().split(" ")
		mac, sex, feat = part[0], int(part[1]), part[2:]
		if user.has_key(mac):
			_list = []
			for f in feat:
				_list.append(float(f))
			docList.append(_list)
			classList.append(sex)
	fileinput.close()
	docList, classList = np.array(docList), np.array(classList)
	min_max_scaler = preprocessing.MinMaxScaler()
	docList = min_max_scaler.fit_transform(docList)
	selector = feature_selection.SelectPercentile(percentile=100)
	selector.fit(docList, classList)
	scores = -np.log10(selector.pvalues_)
	c = 0
	for one in list(scores):
		c += 1
		if one == one:
			_set.append({'f':'http','p':c,'s':one})
		else:
			_set.append({'f':'http','p':c,'s':0})
	_set = sorted(_set, key=lambda k: k['s'], reverse = True)[0:500]
	with open("../../data/feature_set/feature_set_http_"+task+"_500","w") as f:
		cc = 0
		for one in _set:
			info = ""		
			if one['f'] == 'all':
				info = find_1[one['p']]
				# if info.split("_")[0].split("+")[0] in ["Acad","Adm","Ath","Cant","Hosp","Lib","Soc","Supp","Teach","Other"]:
				# print one['s'], one['f'], info
				cc += 1
				f.write(str(cc)+' '+str(one['s'])+'\n')
			if one['f'] == 'online':
				info = find_2[one['p']]
				# if info.split("_")[0].split("+")[0] in ["Acad","Adm","Ath","Cant","Hosp","Lib","Soc","Supp","Teach","Other"]:
				# print one['s'], one['f'], info
				cc += 1
				f.write(str(cc)+' '+str(one['s'])+'\n')
			if one['f'] == 'http':
				info = find_3[one['p']]
				if ":" in info:
					ss = info.split("_")[0].split("+")[-1].split(":")
					hst, typ = find_h[int(ss[0])], find_t[int(ss[1])]
					info = "+".join(info.split("+")[:-1])+'+'+hst+':'+typ
				# print one['s'], one['f'], info
				cc += 1
				f.write(str(cc)+' '+str(one['s'])+'\n')

def func1():
	user = {}
	for line in fileinput.input("../../data/select/select_a"):
		mac = line.strip().split(" ")[0]
		user[mac] = True
	fileinput.close()
	docList, classList = [], []
	for line in fileinput.input("../../data/feature/trace_http_statistic_filter_feature_sex"):
		part = line.strip().split(" ")
		mac, sex, feat = part[0], int(part[1]), part[2:]
		# print len(feat)
		if user.has_key(mac):
			_list = []
			for f in feat:
				_list.append(float(f))
			docList.append(_list)
			classList.append(sex)
	fileinput.close()
	docList, classList = np.array(docList), np.array(classList)
	min_max_scaler = preprocessing.MinMaxScaler()
	docList = min_max_scaler.fit_transform(docList)
	cnt, errorCount = 0, 0
	loo = LeaveOneOut(len(classList))
	trainingdoc, trainingclass = [], []
	for train, test in loo:
		cnt += 1
		print cnt
		trainingdoc, trainingclass, testingdoc, testingclass = docList[train], classList[train], docList[test], classList[test]
		# clf = svm.SVC(kernel='rbf', class_weight='auto')
		clf = pipeline.Pipeline([
			# ('feature_selection', feature_selection.SelectKBest(k=10)),
		  	('feature_selection', svm.LinearSVC(penalty="l1", dual=False)),
		  	# ('feature_selection', linear_model.LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1, class_weight='auto', random_state=None)),
		  	('classification', tree.DecisionTreeClassifier())
		  	# ('classification', ensemble.RandomForestClassifier())
		  	# ('classification', SGDClassifier(loss="hinge", penalty="l2"))
		  	# ('classification', svm.SVC(kernel='linear', class_weight='auto'))
		  	# ('classification', GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0))			
		])
		clf.fit(trainingdoc, trainingclass)
		for i in range(len(testingdoc)):
			if not testingclass[i] == clf.predict(testingdoc[i])[0]:
				errorCount += 1
	print 'the error rate is: ',float(errorCount)/len(classList)

def func2():
	user = {}
	for line in fileinput.input("../../data/select/select_a"):
		mac = line.strip().split(" ")[0]
		user[mac] = True
	fileinput.close()
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
			_list = []
			for f in feat:
				_list.append(float(f))
			docMap_1[mac] = _list
			classMap[mac] = sex
	fileinput.close()
	print cnt_0, cnt_1
	for line in fileinput.input("../../data/feature/trace_online_statistic_filter_feature_sex"):
		part = line.strip().split(" ")
		mac, sex, feat = part[0], int(part[1]), part[2:]
		if user.has_key(mac):
			_list = []
			for f in feat:
				_list.append(float(f))
			docMap_2[mac] = _list
	fileinput.close()
	for line in fileinput.input("../../data/feature/trace_http_statistic_filter_feature_sex"):
		part = line.strip().split(" ")
		mac, sex, feat = part[0], int(part[1]), part[2:]
		if user.has_key(mac):
			_list = []
			for f in feat:
				_list.append(float(f))
			docMap_3[mac] = _list
	fileinput.close()
	for line in fileinput.input("../../data/feature/keywords_normalize_sex"):
		part = line.strip().split(" ")
		mac, sex, feat = part[0], int(part[1]), part[2:]
		if user.has_key(mac):
			_list = []
			for f in feat:
				_list.append(float(f))
			docMap_4[mac] = _list
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
	# file = open("../../data/prediction/result","w")
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
			_list = [res_1[0], res_1[1], res_2[0], res_2[1], res_3[0], res_3[1], res_4[0], res_4[1]]
			docList_final.append(_list)
		res_1 = clf_1.predict_proba(testingdoc_1)[0]
		res_2 = clf_2.predict_proba(testingdoc_2)[0]
		res_3 = clf_3.predict_proba(testingdoc_3)[0]
		res_4 = gnb.predict_proba(testingdoc_4)[0]
		testing_final = [res_1[0], res_1[1], res_2[0], res_2[1], res_3[0], res_3[1], res_4[0], res_4[1]]
		print testing_final
	# 	# clf_final = tree.DecisionTreeClassifier()
	# 	clf_final = SGDClassifier(loss="log", penalty="l1")#log,l1
	# 	# clf_final = svm.SVC(kernel='linear', class_weight = 'auto')
	# 	# clf_final = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
	# 	clf_final.fit(docList_final, trainingclass)
	# 	print testingclass[0], clf_final.predict(testing_final)[0]
	# 	if not testingclass[0] == clf_final.predict(testing_final)[0]:
	# 		errorCount += 1
	# print 'the accurate rate is: ', 1-float(errorCount)/len(classList)
		# print testingclass[0], res_1[0], res_2[0], res_3[0], res_4[0]
		# file.write(str(testingclass[0])+' '+str(res_1[0])+' '+str(res_1[1])+' '+str(res_1[2])+' '+str(res_1[3])+' '+str(res_1[4])\
		# 							   +' '+str(res_2[0])+' '+str(res_2[1])+' '+str(res_2[2])+' '+str(res_2[3])+' '+str(res_2[4])\
		# 							   +' '+str(res_3[0])+' '+str(res_3[1])+' '+str(res_3[2])+' '+str(res_3[3])+' '+str(res_3[4])\
		# 							   +' '+str(res_4[0])+' '+str(res_4[1])+' '+str(res_4[2])+' '+str(res_4[3])+' '+str(res_4[4])+'\n')
	# 	if not testingclass == res:
	# 		errorCount += 1
	# print 'the error rate is: ',float(errorCount)/len(classList)

if __name__ == "__main__":
	func0(task="sex")
	func1()
	func2()

# linear svc, svm linear          0.366379310345
# linear svc, svm rbf             0.379310344828
# linear svc, RF 10 gini          0.379310344828
# linear svc, RF 10 entropy       0.375000000000
# Logistic, svm linear            0.329741379310
# Logistic, svm rbf               0.821120689655
# Logistic, RF 10 gini            0.342672413793
# Logistic, RF 10 entropy         0.340517241379
# Logistic, l1, svm linear        0.383620689655
# Logistic, dual, svm linear      0.329741379310
# Logistic, C=0.1, svm linear     0.340517241379
# Logistic, svm linear simple     0.323275862069
# Logistic, svm linear partial0   0.357758620690
# Logistic, svm linear partial1   0.353448275862

# online               67.0%
# Logistic, svm linear            0.329741379310
# Logistic, RF 10 entropy         0.340517241379

# all                  72.0%
# Logistic, svm linear            0.280172413793
# Logistic, RF 10 entropy         0.316810344828

# http                 74.5%
# Logistic, svm linear            0.245689655172
# Logistic, RF 10 entropy         0.290948275862

# url                  80.2%
# 2,500 0.198275862069

# stochastic gradient descent    85.2%

# gender   2   464   85.2%
# age      3   464   84.3%
# degree   2   461   99.1%
# college  5   283   86.2%

# male 278 female 186
# 18-20 301 21-22 109 23+ 54
# 1 128 2 70 3 30 4 28 5 27
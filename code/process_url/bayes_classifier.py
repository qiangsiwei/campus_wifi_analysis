# -*- coding: utf-8 -*- 

import fileinput
from numpy import *

def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec

def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = ones(numWords); p1Num = ones(numWords) 
    p0Denom = 2.0; p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num/p1Denom)
    p0Vect = log(p0Num/p0Denom)
    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else: 
        return 0

basedir = "../../data/url"

stop = {}
for line in fileinput.input("{0}/stopwords".format(basedir)):
    stop[line.strip()] = True
fileinput.close()

featset, glob = {}, {}
for line in fileinput.input("{0}/keywords_frequency".format(basedir)):
    words = line.strip().split(" ")[1:]
    for word in words:
        key = word.split(",")[0]
        if not glob.has_key(key):
            glob[key] = 1
        glob[key] = glob[key]+1
fileinput.close()

for c, (k, _) in enumerate(glob.iteritems()):
    featset[c] = k

user = {}
for line in fileinput.input("../../data/select/select_a"):
    mac = line.strip().split(" ")[0]
    user[mac] = True
fileinput.close()

task, docList, classList = "age", [], []
for line in fileinput.input("{0}/keywords_normalize_{1}".format(basedir,task)):
    part = line.strip().split(" ")
    mac, sex, feat = part[0], int(part[1]), part[2:]
    if user.has_key(mac):
        lst = []
        for f in feat:
            if int(f)>0:
                lst.append(1)
            else:
                lst.append(0)
        docList.append(lst)
        classList.append(sex)

numTrainDocs = len(docList)
numWords = len(docList[0])
p0Num = ones(numWords); p1Num = ones(numWords) 
p0Denom, p1Denom = 0, 0
for i in range(numTrainDocs):
    if classList[i] == 0:
        p0Num += docList[i]
        p0Denom += sum(docList[i])
    elif classList[i] == 1:
        p1Num += docList[i]
        p1Denom += sum(docList[i])
p1 = p0Num/p0Denom
p2 = p1Num/p1Denom

array = []
for i in range(0,len(p1)):
    array.append({'p1':p1[i],'p2':p2[i],'s':p1[i]+p2[i],'w':featset[i]})
array = sorted(array, key=lambda k: k['s'], reverse = True)[0:500]

with open("{0}/bayes_{1}".format(basedir,task),"w") as f:
    f.write("wd C1 C2\n")
    for item in array:
      if not stop.has_key(item['w']):
          f.write(item['w']+' '+str(item['p1'])+' '+str(item['p2'])+'\n')

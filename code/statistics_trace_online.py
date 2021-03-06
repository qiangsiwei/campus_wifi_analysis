# -*- coding: utf-8 -*- 

import gzip
import fileinput

def func1():
    class StatsI:
        def __init__(self, sequence):
            self.sequence = [int(item) for item in sequence]
        def sum(self):
            if len(self.sequence) < 1:
                return None
            else:
                return sum(self.sequence)
        def cnt(self):
            return len(self.sequence)
        def min(self):
            if len(self.sequence) < 1:
                return None
            else:
                return min(self.sequence)
        def max(self):
            if len(self.sequence) < 1:
                return None
            else:
                return max(self.sequence)
        def avg(self):
            if len(self.sequence) < 1:
                return None
            else:
                return sum(self.sequence) / len(self.sequence)    
        def med(self):
            if len(self.sequence) < 1:
                return None
            else:
                self.sequence.sort()
                return self.sequence[len(self.sequence) // 2]
        def std(self):
            if len(self.sequence) < 1:
                return None
            else:
                avg = self.avg()
                sdsq = sum([(i - avg) ** 2 for i in self.sequence])
                stdev = (sdsq / (len(self.sequence) - 1)) ** .5
                return stdev

    class StatsF:
        def __init__(self, sequence):
            self.sequence = [float(item) for item in sequence]
        def sum(self):
            if len(self.sequence) < 1:
                return None
            else:
                return sum(self.sequence)
        def cnt(self):
            return len(self.sequence)
        def min(self):
            if len(self.sequence) < 1:
                return None
            else:
                return min(self.sequence)
        def max(self):
            if len(self.sequence) < 1:
                return None
            else:
                return max(self.sequence)
        def avg(self):
            if len(self.sequence) < 1:
                return None
            else:
                return sum(self.sequence) / len(self.sequence)    
        def med(self):
            if len(self.sequence) < 1:
                return None
            else:
                self.sequence.sort()
                return self.sequence[len(self.sequence) // 2]
        def std(self):
            if len(self.sequence) < 1:
                return None
            else:
                avg = self.avg()
                sdsq = sum([(i - avg) ** 2 for i in self.sequence])
                stdev = (sdsq / (len(self.sequence) - 1)) ** .5
                return stdev

    mapping, glob = {}, {}
    for line in gzip.open("../data/feature/trace_online.gz"):
        part = line.strip().split(" ")
        mac, dy, wd, ss, hr, cl, bd, dr, rdr = part[0].replace(":",""), part[1], part[2], part[3], part[4], part[5], part[6], int(part[8]), int(part[9])
        wd = {'1':'WD','2':'WE'}[wd]
        ss = {'1':'A','2':'B','3':'C','4':'D'}[ss]
        if not mapping.has_key(mac):
            mapping[mac] = {}
        if not glob.has_key(mac):
            glob[mac] = {}
        if not glob[mac].has_key(dy):
            glob[mac][dy] = 0
        glob[mac][dy] = glob[mac][dy]+dr
        array = [wd, ss, hr, cl, bd, wd+'+'+ss, wd+'+'+hr,\
                cl+'+'+wd, cl+'+'+ss, cl+'+'+hr, cl+'+'+wd+'+'+ss, cl+'+'+wd+'+'+hr,\
                bd+'+'+wd, bd+'+'+ss, bd+'+'+hr, bd+'+'+wd+'+'+ss, bd+'+'+wd+'+'+hr]
        for one in array:
            if not mapping[mac].has_key(one):
                mapping[mac][one] = {}   
            if not mapping[mac][one].has_key(dy):
                mapping[mac][one][dy] = {'tm':[],'rt':[]}    
            if dr>0:
                mapping[mac][one][dy]['tm'].append(dr)
                mapping[mac][one][dy]['rt'].append(float(rdr)/dr)

    jac = {}
    for line in fileinput.input("../data/jaccount/jaccount_taged"):
        part = line.strip().split(" ")
        dev, mac, sex = part[0], part[1], part[2]
        if dev == "mobile":
            jac[mac] = {'sex':sex}
    fileinput.close()

    with open('../data/feature/trace_online_statistic', 'w') as f:
        for k,v in mapping.iteritems():
            if jac.has_key(k):
                array = []
                for x,y in glob[k].iteritems():
                    array.append(y)
                if len(array) >= 2:
                    stats = StatsI(array)
                    _cnt, _sum, _min, _max, _avg, _med, _std = stats.cnt(), stats.sum(), stats.min(), stats.max(), stats.avg(), stats.med(), stats.std()
                    f.write(k+' '+jac[k]['sex']+' tot@'+str(_cnt)+','+str(_sum)+','+str(_min)+','+str(_max)+','+str(_avg)+','+str(_med)+','+str(int(_std)))
                    for p,q in v.iteritems():
                        array1, array2 = [], []
                        for x,y in q.iteritems():
                            if len(y['tm'])>0:
                                array1.append(sum(y['tm']))
                                array2.append(sum(y['rt'])/len(y['rt']))
                        if len(array1) >= 2:
                            stats1, stats2 = StatsI(array1), StatsF(array2)
                            f.write(' '+p+'@'+str(stats1.cnt())+','+str(stats1.sum())+',%.4f,'%(float(stats1.cnt())/_cnt)+'%.4f,'%(float(stats1.sum())/_sum)+str(stats1.min())+','+str(stats1.max())+','+str(stats1.avg())+','+str(stats1.med())+','+str(int(stats1.std()))+\
                            		   ','+str(stats2.min())+','+str(stats2.max())+','+str(stats2.avg())+','+str(stats2.med()))
                    f.write('\n')

############################################################################################

def func2():
    with open("../data/feature/trace_online_statistic_filter","w") as f:
        for line in fileinput.input("../data/feature/trace_online_statistic"):
            part = line.strip().split(" ")
            mac, sex, tot, feat = part[0], {"男性":0, "女性":1}[part[1]], part[2], part[3:]
            array_0, array_p, array_1, array_2, array_3, array_4, array_5, array_6, array_7, array_8, array_9, array_10 = {}, {}, [], [], [], [], [], [], [], [], [], []
            for one in feat:
                objs = one.split("@")
                chars, ints = objs[0].split("+"), objs[1].split(",")
                if len(chars) == 1:
                    if chars[0] in ["WD","WE","A","B","C","D","0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]:
                        array_0[chars[0]] = ints[1]+","+str(int(float(ints[2])*1000))+","+str(int(float(ints[3])*1000))+","+ints[4]+","+ints[5]+","+ints[6]+","+ints[7]+","+str(int(float(ints[8])*1000))+","+str(int(float(ints[9])*1000))+","+str(int(float(ints[10])*1000))+","+str(int(float(ints[11])*1000))+","+str(int(float(ints[12])*1000))
                    else:
                        array_p[chars[0]] = str(int(float(ints[2])*1000))+","+str(int(float(ints[3])*1000))+","+ints[4]+","+ints[5]+","+ints[6]+","+ints[7]+","+str(int(float(ints[8])*1000))+","+str(int(float(ints[9])*1000))+","+str(int(float(ints[10])*1000))+","+str(int(float(ints[11])*1000))+","+str(int(float(ints[12])*1000))
                if len(chars) == 2 and chars[0] in ["WD","WE"] and chars[1] in ["A","B","C","D"]:
                    array_0["+".join(chars)] = str(int(float(ints[2])*1000))+","+str(int(float(ints[3])*1000))+","+ints[4]+","+ints[5]+","+ints[6]+","+ints[7]+","+str(int(float(ints[8])*1000))+","+str(int(float(ints[9])*1000))+","+str(int(float(ints[10])*1000))+","+str(int(float(ints[11])*1000))+","+str(int(float(ints[12])*1000))
                if len(chars) == 2 and chars[0] in ["WD","WE"] and chars[1] in ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]:
                    array_0["+".join(chars)] = str(int(float(ints[2])*1000))+","+str(int(float(ints[3])*1000))+","+ints[4]+","+ints[5]+","+ints[6]+","+ints[7]+","+str(int(float(ints[8])*1000))+","+str(int(float(ints[9])*1000))+","+str(int(float(ints[10])*1000))+","+str(int(float(ints[11])*1000))+","+str(int(float(ints[12])*1000))
                if len(chars) == 2 and chars[1] in ["WD","WE"]:
                    if chars[0] in ["Acad","Adm","Ath","Cant","Hosp","Lib","Soc","Supp","Teach","Other"]:
                        array_1.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000),'rt1':int(float(ints[9])*1000),'rt2':int(float(ints[10])*1000),'rt3':int(float(ints[11])*1000),'rt4':int(float(ints[12])*1000)})
                    else:
                        array_2.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000),'rt1':int(float(ints[9])*1000),'rt2':int(float(ints[10])*1000),'rt3':int(float(ints[11])*1000),'rt4':int(float(ints[12])*1000)})
                if len(chars) == 2 and chars[1] in ["A","B","C","D"]:
                    if chars[0] in ["Acad","Adm","Ath","Cant","Hosp","Lib","Soc","Supp","Teach","Other"]:
                        array_3.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000),'rt1':int(float(ints[9])*1000),'rt2':int(float(ints[10])*1000),'rt3':int(float(ints[11])*1000),'rt4':int(float(ints[12])*1000)})
                    else:
                        array_4.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000),'rt1':int(float(ints[9])*1000),'rt2':int(float(ints[10])*1000),'rt3':int(float(ints[11])*1000),'rt4':int(float(ints[12])*1000)})
                if len(chars) == 2 and chars[1] in ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]:
                    if chars[0] in ["Acad","Adm","Ath","Cant","Hosp","Lib","Soc","Supp","Teach","Other"]:
                        array_5.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000),'rt1':int(float(ints[9])*1000),'rt2':int(float(ints[10])*1000),'rt3':int(float(ints[11])*1000),'rt4':int(float(ints[12])*1000)})
                    else:
                        array_6.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000),'rt1':int(float(ints[9])*1000),'rt2':int(float(ints[10])*1000),'rt3':int(float(ints[11])*1000),'rt4':int(float(ints[12])*1000)})
                if len(chars) == 3 and chars[1] in ["WD","WE"] and chars[2] in ["A","B","C","D"]:
                    if chars[0] in ["Acad","Adm","Ath","Cant","Hosp","Lib","Soc","Supp","Teach","Other"]:
                        array_7.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000),'rt1':int(float(ints[9])*1000),'rt2':int(float(ints[10])*1000),'rt3':int(float(ints[11])*1000),'rt4':int(float(ints[12])*1000)})
                    else:
                        array_8.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000),'rt1':int(float(ints[9])*1000),'rt2':int(float(ints[10])*1000),'rt3':int(float(ints[11])*1000),'rt4':int(float(ints[12])*1000)})
                if len(chars) == 3 and chars[1] in ["WD","WE"] and chars[2] in ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]:
                    if chars[0] in ["Acad","Adm","Ath","Cant","Hosp","Lib","Soc","Supp","Teach","Other"]:
                        array_9.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000),'rt1':int(float(ints[9])*1000),'rt2':int(float(ints[10])*1000),'rt3':int(float(ints[11])*1000),'rt4':int(float(ints[12])*1000)})
                    else:
                        array_10.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000),'rt1':int(float(ints[9])*1000),'rt2':int(float(ints[10])*1000),'rt3':int(float(ints[11])*1000),'rt4':int(float(ints[12])*1000)})
            array_1_cnt, array_1_avg = sorted(array_1, key=lambda k: k['cnt'], reverse = True)[0:10],  sorted(array_1, key=lambda k: k['avg'], reverse = True)[0:10]
            for tmp in array_1_cnt:
                if not tmp in array_1_avg:
                    array_1_avg.append(tmp)
            array_2_cnt, array_2_avg = sorted(array_2, key=lambda k: k['cnt'], reverse = True)[0:30], sorted(array_2, key=lambda k: k['avg'], reverse = True)[0:30]
            for tmp in array_2_cnt:
                if not tmp in array_2_avg:
                    array_2_avg.append(tmp)
            array_3_cnt, array_3_avg = sorted(array_3, key=lambda k: k['cnt'], reverse = True)[0:10],  sorted(array_3, key=lambda k: k['avg'], reverse = True)[0:10]
            for tmp in array_3_cnt:
                if not tmp in array_3_avg:
                    array_3_avg.append(tmp)
            array_4_cnt, array_4_avg = sorted(array_4, key=lambda k: k['cnt'], reverse = True)[0:30], sorted(array_4, key=lambda k: k['avg'], reverse = True)[0:30]
            for tmp in array_4_cnt:
                if not tmp in array_4_avg:
                    array_4_avg.append(tmp)
            array_5_cnt, array_5_avg = sorted(array_5, key=lambda k: k['cnt'], reverse = True)[0:10],  sorted(array_5, key=lambda k: k['avg'], reverse = True)[0:10]
            for tmp in array_5_cnt:
                if not tmp in array_5_avg:
                    array_5_avg.append(tmp)
            array_6_cnt, array_6_avg = sorted(array_6, key=lambda k: k['cnt'], reverse = True)[0:30], sorted(array_6, key=lambda k: k['avg'], reverse = True)[0:30]
            for tmp in array_6_cnt:
                if not tmp in array_6_avg:
                    array_6_avg.append(tmp)
            array_7_cnt, array_7_avg = sorted(array_7, key=lambda k: k['cnt'], reverse = True)[0:10],  sorted(array_7, key=lambda k: k['avg'], reverse = True)[0:10]
            for tmp in array_7_cnt:
                if not tmp in array_7_avg:
                    array_7_avg.append(tmp)
            array_8_cnt, array_8_avg = sorted(array_8, key=lambda k: k['cnt'], reverse = True)[0:30], sorted(array_8, key=lambda k: k['avg'], reverse = True)[0:30]
            for tmp in array_8_cnt:
                if not tmp in array_8_avg:
                    array_8_avg.append(tmp)
            array_9_cnt, array_9_avg = sorted(array_9, key=lambda k: k['cnt'], reverse = True)[0:10],  sorted(array_9, key=lambda k: k['avg'], reverse = True)[0:10]
            for tmp in array_9_cnt:
                if not tmp in array_9_avg:
                    array_9_avg.append(tmp)
            array_10_cnt, array_10_avg = sorted(array_10, key=lambda k: k['cnt'], reverse = True)[0:30], sorted(array_10, key=lambda k: k['avg'], reverse = True)[0:30]
            for tmp in array_10_cnt:
                if not tmp in array_10_avg:
                    array_10_avg.append(tmp)
            array = []
            for key in ["WD","WE","A","B","C","D","0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]:
                if array_0.has_key(key):
                    array.append(key+"@"+array_0[key])
                else:
                    array.append(key+"@0,0,0,0,0,0,0,0,0,0,0")
            for key1 in ["WD","WE"]:
                for key2 in ["A","B","C","D"]:
                    key = key1+"+"+key2
                    if array_0.has_key(key):
                        array.append(key+"@"+array_0[key])
                    else:
                        array.append(key+"@0,0,0,0,0,0,0,0,0,0,0")
            for key1 in ["WD","WE"]:
                for key2 in ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]:
                    key = key1+"+"+key2
                    if array_0.has_key(key):
                        array.append(key+"@"+array_0[key])
                    else:
                        array.append(key+"@0,0,0,0,0,0,0,0,0,0,0")
            for k,v in array_p.iteritems():
                array.append(k+'@'+v)
            for one in array_1_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std'])+","+str(one['rt1'])+","+str(one['rt2'])+","+str(one['rt3'])+","+str(one['rt4']))
            for one in array_2_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std'])+","+str(one['rt1'])+","+str(one['rt2'])+","+str(one['rt3'])+","+str(one['rt4']))
            for one in array_3_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std'])+","+str(one['rt1'])+","+str(one['rt2'])+","+str(one['rt3'])+","+str(one['rt4']))
            for one in array_4_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std'])+","+str(one['rt1'])+","+str(one['rt2'])+","+str(one['rt3'])+","+str(one['rt4']))
            for one in array_5_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std'])+","+str(one['rt1'])+","+str(one['rt2'])+","+str(one['rt3'])+","+str(one['rt4']))
            for one in array_6_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std'])+","+str(one['rt1'])+","+str(one['rt2'])+","+str(one['rt3'])+","+str(one['rt4']))
            for one in array_7_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std'])+","+str(one['rt1'])+","+str(one['rt2'])+","+str(one['rt3'])+","+str(one['rt4']))
            for one in array_8_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std'])+","+str(one['rt1'])+","+str(one['rt2'])+","+str(one['rt3'])+","+str(one['rt4']))
            for one in array_9_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std'])+","+str(one['rt1'])+","+str(one['rt2'])+","+str(one['rt3'])+","+str(one['rt4']))
            for one in array_10_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std'])+","+str(one['rt1'])+","+str(one['rt2'])+","+str(one['rt3'])+","+str(one['rt4']))
            f.write(mac+' '+str(sex)+' '+tot+' '+" ".join(array)+'\n')
        fileinput.close()

############################################################################################

def func3():
    mapping = {}
    for line in fileinput.input("../data/feature/trace_online_statistic_filter"):
    	for one in line.strip().split(" ")[89:]:
    		key = one.split("@")[0]
    		if not mapping.has_key(key):
    			mapping[key] = 0
    		mapping[key] += 1
    fileinput.close()

    array = []
    for k,v in mapping.iteritems():
    	array.append({'k':k,'v':v})
    array = sorted(array, key=lambda k: k['v'], reverse = True)[0:1500]

    with open("../data/feature/trace_online_statistic_filter_feature","w") as f:
        for line in fileinput.input("../data/feature/trace_online_statistic_filter"):
            part = line.strip().split(" ")
            mac, sex, tot, glob, feat = part[0], part[1], part[2], part[3:89], part[89:]
            sets = {}
            for one in feat:	
                objs = one.split("@")
                chars, ints = objs[0], objs[1]
                cc = ints.split(",")
                tp = " ".join([cc[0],cc[1],cc[3],cc[4]])
                sets[chars] = tp
            outs = []
            tt = int(tot.split("@")[1].split(",")[0])
            outs.append(tot.split("@")[1].replace(","," "))
            for one in glob:
                cc = ints.split(",")
                tp = " ".join([cc[0],cc[1],cc[3],cc[4]])
                outs.append(tp)
            cnt = 0
            for one in array:
                if sets.has_key(one['k']):
                    outs.append(sets[chars])
                    cnt += 1
                else:
                    outs.append("0 0 0 0")
            f.write(mac+' '+sex+' '+" ".join(outs)+'\n')
        fileinput.close()

if __name__ == "__main__":
    func1()
    func2()
    func3()

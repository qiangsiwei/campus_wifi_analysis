# -*- coding: utf-8 -*- 

import gzip
import fileinput

def func1():
    class Stats:
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

    mapping, glob = {}, {}
    for line in gzip.open("../data/feature/trace_http.gz"):
    	part = line.strip().split(" ")
    	mac, dy, wd, ss, hr, cl, bd, mk = part[0].replace(":",""), part[1], part[2], part[3], part[4], part[5], part[6], part[8]+":"+part[9]
    	wd = {'1':'WD','2':'WE'}[wd]
    	ss = {'1':'A','2':'B','3':'C','4':'D'}[ss]
    	if not mapping.has_key(mac):
    		mapping[mac] = {}
    	if not glob.has_key(mac):
    		glob[mac] = {}
    	if not glob[mac].has_key(dy):
    		glob[mac][dy] = 0
    	glob[mac][dy] += 1
    	array = [wd+'+'+mk, ss+'+'+mk, hr+'+'+mk, cl+'+'+mk, bd+'+'+mk, wd+'+'+ss+'+'+mk, wd+'+'+hr+'+'+mk,\
                cl+'+'+wd+'+'+mk, cl+'+'+ss+'+'+mk, cl+'+'+hr+'+'+mk, cl+'+'+wd+'+'+ss+'+'+mk, cl+'+'+wd+'+'+hr+'+'+mk,\
                bd+'+'+wd+'+'+mk, bd+'+'+ss+'+'+mk, bd+'+'+hr+'+'+mk, bd+'+'+wd+'+'+ss+'+'+mk, bd+'+'+wd+'+'+hr+'+'+mk]
    	for one in array:
    		if not mapping[mac].has_key(one):
    			mapping[mac][one] = {}
    		if not mapping[mac][one].has_key(dy):
    			mapping[mac][one][dy] = 0
    		mapping[mac][one][dy] += 1

    jac = {}
    for line in fileinput.input("../data/jaccount/jaccount_taged"):
        part = line.strip().split(" ")
        dev, mac, sex = part[0], part[1], part[2]
        if dev == "mobile":
            jac[mac] = {'sex':sex}
    fileinput.close()

    with open('../data/feature/trace_http_statistic', 'w') as f:
        for k,v in mapping.iteritems():
            if jac.has_key(k):
                array = []
                for x,y in glob[k].iteritems():
                    array.append(y)
                if len(array) >= 2:
                    stats = Stats(array)
                    _cnt, _sum, _min, _max, _avg, _med, _std = stats.cnt(), stats.sum(), stats.min(), stats.max(), stats.avg(), stats.med(), stats.std()
                    f.write(k+' '+jac[k]['sex']+' tot@'+str(_cnt)+','+str(_sum)+','+str(_min)+','+str(_max)+','+str(_avg)+','+str(_med)+','+str(int(_std)))
                    for p,q in v.iteritems():
                        array = []
                        for x,y in q.iteritems():
                            array.append(y)
                        if len(array) >= 2:
                            stats = Stats(array)
                            f.write(' '+p+'@'+str(stats.cnt())+','+str(stats.sum())+',%.4f,'%(float(stats.cnt())/_cnt)+'%.4f,'%(float(stats.sum())/_sum)+str(stats.min())+','+str(stats.max())+','+str(stats.avg())+','+str(stats.med())+','+str(int(stats.std())))
                    f.write('\n')

############################################################################################

def func2():
    with open("../data/feature/trace_http_statistic_filter","w") as f:
        for line in fileinput.input("../data/feature/trace_http_statistic"):
            part = line.strip().split(" ")
            mac, sex, tot, feat = part[0], {"男性":0, "女性":1}[part[1]], part[2], part[3:]
            array_0, array_1, array_2, array_3, array_4, array_5, array_6, array_7, array_8, array_9, array_10 = {}, [], [], [], [], [], [], [], [], [], []
            for one in feat:
                objs = one.split("@")
                chars, ints = objs[0].split("+"), objs[1].split(",")
                if len(chars) == 2:
                    array_0["+".join(chars)] = str(int(float(ints[2])*1000))+","+str(int(float(ints[3])*1000))+","+ints[4]+","+ints[5]+","+ints[6]+","+ints[7]+","+str(int(float(ints[8])*1000))
                if len(chars) == 3 and chars[0] in ["WD","WE"] and chars[1] in ["A","B","C","D"]:
                    array_0["+".join(chars)] = str(int(float(ints[2])*1000))+","+str(int(float(ints[3])*1000))+","+ints[4]+","+ints[5]+","+ints[6]+","+ints[7]+","+str(int(float(ints[8])*1000))
                if len(chars) == 3 and chars[0] in ["WD","WE"] and chars[1] in ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]:
                    array_0["+".join(chars)] = str(int(float(ints[2])*1000))+","+str(int(float(ints[3])*1000))+","+ints[4]+","+ints[5]+","+ints[6]+","+ints[7]+","+str(int(float(ints[8])*1000))
                if len(chars) == 3 and chars[1] in ["WD","WE"]:
                    if chars[0] in ["Acad","Adm","Ath","Cant","Hosp","Lib","Soc","Supp","Teach","Other"]:
                        array_1.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000)})
                    else:
                        array_2.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000)})
                if len(chars) == 3 and chars[1] in ["A","B","C","D"]:
                    if chars[0] in ["Acad","Adm","Ath","Cant","Hosp","Lib","Soc","Supp","Teach","Other"]:
                        array_3.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000)})
                    else:
                        array_4.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000)})
                if len(chars) == 3 and chars[1] in ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]:
                    if chars[0] in ["Acad","Adm","Ath","Cant","Hosp","Lib","Soc","Supp","Teach","Other"]:
                        array_5.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000)})
                    else:
                        array_6.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000)})
                if len(chars) == 4 and chars[1] in ["WD","WE"] and chars[2] in ["A","B","C","D"]:
                    if chars[0] in ["Acad","Adm","Ath","Cant","Hosp","Lib","Soc","Supp","Teach","Other"]:
                        array_7.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000)})
                    else:
                        array_8.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000)})
                if len(chars) == 4 and chars[1] in ["WD","WE"] and chars[2] in ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]:
                    if chars[0] in ["Acad","Adm","Ath","Cant","Hosp","Lib","Soc","Supp","Teach","Other"]:
                        array_9.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000)})
                    else:
                        array_10.append({'k':"+".join(chars),'cnt':int(float(ints[2])*1000),'sum':int(float(ints[3])*1000),'min':int(ints[4]),'max':int(ints[5]),'avg':int(ints[6]),'med':int(ints[7]),'std':int(float(ints[8])*1000)})
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
            for k,v in array_0.iteritems():
                array.append(k+'@'+v)
            for one in array_1_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std']))
            for one in array_2_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std']))
            for one in array_3_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std']))
            for one in array_4_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std']))
            for one in array_5_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std']))
            for one in array_6_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std']))
            for one in array_7_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std']))
            for one in array_8_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std']))
            for one in array_9_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std']))
            for one in array_10_avg:
                array.append(one['k']+"@"+str(one['cnt'])+","+str(one['sum'])+","+str(one['min'])+","+str(one['max'])+","+str(one['avg'])+","+str(one['med'])+","+str(one['std']))
            f.write(mac+' '+str(sex)+' '+tot+' '+" ".join(array)+'\n')
        fileinput.close()

############################################################################################

def func3():
    mapping = {}
    for line in fileinput.input("../data/feature/trace_http_statistic_filter"):
        for one in line.strip().split(" ")[3:]:
            key = one.split("@")[0]
            if not mapping.has_key(key):
                mapping[key] = 0
            mapping[key] += 1
    fileinput.close()

    array = []
    for k,v in mapping.iteritems():
        array.append({'k':k,'v':v})
    array = sorted(array, key=lambda k: k['v'], reverse = True)[0:2000]

    with open("../data/feature/trace_http_statistic_filter_feature","w") as f:
        for line in fileinput.input("../data/feature/trace_http_statistic_filter"):
            part = line.strip().split(" ")
            mac, sex, tot, feat = part[0], part[1], part[2], part[3:]
            sets = {}
            for one in feat:    
                objs = one.split("@")
                chars, ints = objs[0], objs[1]
                sets[chars] = ints.replace(",", " ")
            outs = []
            tt = int(tot.split("@")[1].split(",")[0])
            outs.append(tot.split("@")[1].replace(","," "))
            cnt = 0
            for one in array:
                if sets.has_key(one['k']):
                    outs.append(sets[chars])
                    cnt += 1
                else:
                    outs.append("0 0 0 0 0 0 0")
            if tt>=20 and cnt > 200:
                f.write(mac+' '+sex+' '+" ".join(outs)+'\n')
        fileinput.close()

if __name__ == "__main__":
    func1()
    func2()
    func3()

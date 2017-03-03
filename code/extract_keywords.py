# -*- coding: utf-8 -*-  

import re
import glob
import gzip
import urllib
import urlparse
import fileinput
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

mapping = {}
device = {}
for line in fileinput.input("../data/jaccount/jaccount_taged"):
	part = line.strip().split(" ")
	dev, mac = part[0], part[1]
	if dev == "mobile":
		device[mac] = True
		mapping[mac] = {}

zhPattern = re.compile(ur'[\u4e00-\u9fa5]+')
for filename in glob.glob(r"../data/http/2013*"):
	print filename
	for line in gzip.open(filename):
		part = line.strip().split(" ")
		mac, url = part[0], part[7]
		params = urlparse.parse_qs(urlparse.urlparse(urllib.unquote(url)).query)
		for k,v in params.iteritems():
			if not k in ["ref","referer","referrer"]:
				try:
					ct = v[0].decode('utf8')
					match = zhPattern.search(ct)
					if match: 
						if not mapping[mac].has_key(match.group()):
							mapping[mac][match.group()] = True
				except:
					continue
					
with open('../data/url/keywords', 'w') as f:
	for k,v in mapping.iteritems():
		f.write(k)
		for w in sorted(v.keys()):
			f.write(' '+w)
		f.write('\n')

#!/usr/bin/python Python 2.7.13
#Transform multiple json files into single csv format.

import glob2 as glob
import pandas as pd
import json
import simplejson

paths=glob.glob("/home/dev-cory/scrayping/data/*.json")
print (paths)
i = 1
df = pd.DataFrame()
for path in paths:
		with open(path) as f:
			#print(path)
			#print(type(f))
			
			try:
				data=json.load(f)
				for key in data.keys():
					df.loc[i,key]=data[key]
			except ValueError as e:
				print "Could not load {}, invalid JSON".format({})
			'''
			try:
				data = json.load(f)
				for key in data.keys():
					df.loc[i,key] = data[key]
			except ValueError as e:
				print "Could not load {}, invalid JSON".format({})
				'''
		i = i + 1
		#df = pd.read_json(path)

df=df.drop([''],axis=1)
df.to_csv('/home/dev-cory/scrayping/data/file.csv',index_label='key_id')
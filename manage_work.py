#!/usr/bin/python Python 2.7.13
#Manage scrapying loop for all checker symbols

import subprocess
from time import sleep
from numpy import random
import pandas as pd

#checkers = ['tsla','CAT']

checkers = ['NLSN','TSLA','SCOR','AAPL','MSFT','GOOG','AMZN','ORCL','T','OMC','TWTR','BA','BAC','BRK.A','BRK.B','GS','GM','tsla','CAT','FIT','CVX','BABA','NFLX','DIS','PG','FB','SBUX','NVDA','ACN','GE','ADBE','NKE','KO','XOM','LLY','QCOM','HSBC','^DJI','CVX','VZ','V']

for checker in checkers:
	#cmd = './yahoo_scrayping.py'
	cmd = '/home/dev-cory/scrayping/scrayping.py'
	#subprocess.call(['python',cmd,checker],shell=False)
	try:
			#subsub=subprocess.check_output(['python',cmd,checker],shell=False)s
			#print(type(subsub))
			#df_s = pd.read_json(subsub)
			#print(subsub)
			subprocess.call(['python',cmd,checker],shell=False)
			
	except subprocess.CalledProcessError as e:
		 print e.returncode
		 print e.output
	sleep(int(60*random.rand()))

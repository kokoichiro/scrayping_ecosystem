from lxml import html  
import requests
from exceptions import ValueError
from time import sleep
import json
import argparse
from collections import OrderedDict
from time import sleep
import datetime

def parse(ticker):
	url = "http://finance.yahoo.com/quote/%s?p=%s"%(ticker,ticker)
	response = requests.get(url, verify=False)
	print "Parsing %s"%(url)
	sleep(4)
	parser = html.fromstring(response.text)
	summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr')
	summary_data = OrderedDict()
	other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(ticker)
	summary_json_response = requests.get(other_details_json_link)
	try:
		json_loaded_summary =  json.loads(summary_json_response.text)
		current_price = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["currentPrice"]['raw']
		free_cash_flow = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["freeCashflow"]['raw']
		return_on_asset = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["returnOnAssets"]['raw']
		operating_margins = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["operatingMargins"]['raw']
		week_change = json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]["52WeekChange"]['raw']
		free_cash_flow = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["freeCashflow"]['raw']
		y_Target_Est = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["targetMeanPrice"]['raw']
		industry = json_loaded_summary["quoteSummary"]["result"][0]["summaryProfile"]["industry"]
		total_debt = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["totalDebt"]['raw']
		total_cash = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["totalCash"]['raw']
		gross_profits = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["grossProfits"]['raw']
		#previous_close = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["previousClose"]['raw']
		earnings_list = json_loaded_summary["quoteSummary"]["result"][0]["calendarEvents"]['earnings']
		eps = json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]["trailingEps"]['raw']
		date_time = str(datetime.datetime.now())
		datelist = []
		for i in earnings_list['earningsDate']:
			datelist.append(i['fmt'])
		earnings_date = ' to '.join(datelist)
		for table_data in summary_table:
			raw_table_key = table_data.xpath('.//td[@class="C(black)"]//text()')
			raw_table_value = table_data.xpath('.//td[contains(@class,"Ta(end)")]//text()')
			table_key = ''.join(raw_table_key).strip()
			table_value = ''.join(raw_table_value).strip()
			summary_data.update({table_key:table_value})
		summary_data.update({'Date Time':date_time,'1y Target Est':y_Target_Est,'Current Price':current_price , 'Total Debt':total_debt, 'Total Cash':total_cash, 'Gross Profits':gross_profits, 'Free Cash Flow':free_cash_flow ,'ROA':return_on_asset,'Operating Margin':operating_margins,'Free Cash Flow':free_cash_flow, 'EPS (TTM)':eps,'Earnings Date':earnings_date,'ticker':ticker,'url':url})
		return summary_data
	except ValueError:
		print "Failed to parse json response"
		return {"error":"Failed to parse json response"}
		
if __name__=="__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('ticker',help = '')
	args = argparser.parse_args()
	ticker = args.ticker
	print "Fetching data for %s"%(ticker)
	scraped_data = parse(ticker)
	print "Writing data to output file"
	with open('%s-summary.json'%(ticker),'w') as fp:
	 	json.dump(scraped_data,fp,indent = 4)
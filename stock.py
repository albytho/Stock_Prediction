import requests
import csv
import numpy as np 
import codecs 
from sklearn.svm import SVR 
from contextlib import closing 
import matplotlib.pyplot as plt

dates = []
prices = []
currentDate = 0
currentStock = 0

def get_data(stock_name):
	dates[:] = []
	prices[:] = []
	url = 'http://www.google.com/finance/historical?q=NASDAQ%3A'+stock_name+'&output=csv%27&output=csv'
	with closing(requests.get(url, stream=True)) as r:
		reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'))
		reader.__next__()
		num = 0;

		index = 1
		for row in reader:
			dates.append(int(row[0].split('-')[0]))
			prices.append(float(row[1]))
			index = index + 1
			if index is 21:
				break;
			
		index = index-1
		for i in range(len(dates)):
			dates[i] = index - i

	return

def predict_prices(dates,prices,x):
	dates = np.reshape(dates,(len(dates),1))
	
	svr_rbf = SVR(kernel='rbf',C=1e3, gamma=0.1)
	svr_rbf.fit(dates,prices)
	

	return svr_rbf.predict(x)[0]

stocks = []
elapsed_prediction_times = []
while True:
	stock_name = input()

	if len(stock_name) == 0:
		break
	else:
		time = input()
		stocks.append(stock_name)
		elapsed_prediction_times.append(float(time))


for index, stock in enumerate(stocks):
	get_data(stock)
	print(predict_prices(dates,prices,20+elapsed_prediction_times[index]))



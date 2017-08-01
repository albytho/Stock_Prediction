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

	svr_lin = SVR(kernel='linear',C=1e3)
	svr_lin.fit(dates,prices)
	
	svr_poly = SVR(kernel='poly',C=1e3, degree = 2)
	svr_poly.fit(dates,prices)
	
	svr_rbf = SVR(kernel='rbf',C=1e3, gamma=0.1)
	svr_rbf.fit(dates,prices)
	

	return svr_rbf.predict(x)[0]

get_data("TSLA")
print(dates)
print(prices)
print(predict_prices(dates,prices,21))

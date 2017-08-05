import requests
import csv
import numpy as np 
import codecs 
from sklearn.svm import SVR 
from contextlib import closing 
import matplotlib.pyplot as plt
import tweepy
from textblob import TextBlob

dates = []
prices = []
currentDate = 0
currentStock = 0

consumer_key = 'ZT3teoSauRNfVkIvaBWg1CGBH'
consumer_secret = 'qWwBp5BFAGubIeHKKSqKGCgFGXMG5AE2rAzm4LWIjJZ8uUmOy0'

access_token = '128648452-aCcCcHoM8EhGud0F6DgQ98tOS5mcAhMMEEXaEauz'
access_token_secret = 'EuNSIt3SEQw1IDPEEPiTii5s2OHzticaWzUIG8EIWMSnj'

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

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
			if index is 201:
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
	public_tweets = api.search(stock)
	analysis = 0
	count = 0
	for tweet in public_tweets:
		count = count + 1
		analysis = analysis + TextBlob(tweet.text).sentiment.polarity

	if count > 0:
		analysis = analysis/count

	get_data(stock)

	print('Stock Name:  ', end='')
	print(stock)

	print('Twitter Opinion of Stock:  ', end='')
	print(analysis)

	print('Predicted Price after '+str(elapsed_prediction_times[index])+' days:  ', end='')
	print(predict_prices(dates,prices,200+elapsed_prediction_times[index]))
	print("\n",end='')



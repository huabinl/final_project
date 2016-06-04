# COMP90055 Computing Project, Semester 1 2016
# Author: Huabin Liu (ID. 658274)

import json
import tweepy
import time
from textblob import TextBlob
from tweepy import AppAuthHandler
from tweepy.cursor import Cursor
import settings
import couchdb
import logging

# This function is for searching tweets in Melbourne via Twitter Search API
def search(db, api):
	try:
		geo = settings.geocode
		for status in Cursor(api.search, geocode=geo, lang='en', count=100).items():
			# avoid duplicated tweets
			if status.id_str not in db:
				tweet = status._json
				# add datetime field
				if 'created_at' in tweet and tweet['created_at']:
					timestamp = time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
					weekday = time.strftime('%A', timestamp)
					date = time.strftime('%Y-%m-%d', timestamp)
					hour = timestamp.tm_hour
					minute = timestamp.tm_min
					second = timestamp.tm_sec
					period = 0
					if hour > 7 and hour < 10:
						period = 1
					if hour > 16 and hour < 20:
						period = 2
					tweet['datetime'] = {'date': date, 'hour': hour, 'minute': minute, 'second': second, 'weekday': weekday, 'period': period}
				else:
					tweet['datetime'] = None
				# add sentiment field
				blob = TextBlob(tweet['text'])
				tweet['sentiment'] = {"polarity": blob.sentiment.polarity, "subjectivity": blob.sentiment.subjectivity}
				blob = TextBlob(tweet['text'], analyzer=NaiveBayesAnalyzer())
				tweet['sentiment']['classification'] = blob.sentiment.classification
				tweet['sentiment']['pos'] = blob.sentiment.p_pos
				tweet['sentiment']['neg'] = blob.sentiment.p_neg
				# store a tweet in db
				db[tweet['id_str']] = tweet
	# error handling
	except tweepy.TweepError as e:
		print 'ERROR: ' + str(e)
		logging.error('ERROR: ' + str(e))

def main():
	logging.basicConfig(filename='search_harvest.log', filemode='w', level=logging.DEBUG)

	# access database
	couch = couchdb.Server(settings.database_address)
	db = couch[settings.database]

	# application-only authentication
	auth = AppAuthHandler(settings.consumer_key1, settings.consumer_secret1)
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

	# start twitter harvester
	print 'start'
	logging.info('start harvesting')
	search(db, api)
	logging.info('finish harvesting')
	print 'finished'

if __name__ == '__main__':
	main()	

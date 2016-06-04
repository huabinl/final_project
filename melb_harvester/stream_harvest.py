# COMP90055 Computing Project, Semester 1 2016
# Author: Huabin Liu (ID. 658274)

import json
import time
import tweepy
from textblob import TextBlob
from tweepy.streaming import StreamListener
from tweepy import Stream, OAuthHandler
import couchdb
import settings
import logging

# This class is for gathering tweets in Melbourne via Twitter Streaming API
class TwitterStreamListener(StreamListener):
	def __init__(self, db):
		self.db = db

	def on_data(self, data):
		try:
			tweet = json.loads(data)
		except Exception:
			tweet = None
		# avoid duplicated tweets
		if tweet and tweet['id_str'] not in self.db:
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
			# store a tweet in database
			self.db[tweet['id_str']] = tweet
		return True

	# error handling
	def on_error(self, status_code):
		logging.error('error:' + str(status_code))
		print 'error:' + str(status_code)
		if status_code == 420:
			time.sleep(900)
		return False

	# timeout handling
	def on_timeout(self):
		logging.error('timeout')
		print 'timeout'
		return False

def main():
	logging.basicConfig(filename='melb_harvest.log', filemode='w', level=logging.DEBUG)

	# access database
	couch = couchdb.Server(settings.database_address)
	try:
		db = couch.create(settings.database)
	except couchdb.http.PreconditionFailed as e:
		db = couch[settings.database]

	# OAuth
	auth = OAuthHandler(settings.consumer_key, settings.consumer_secret)
	auth.set_access_token(settings.access_token, settings.access_secret)

	# start twitter harvester
	print 'start'
	listener = TwitterStreamListener(db)
	logging.info('start harvesting')
	while True:
		stream = Stream(auth, listener)
		stream.filter(locations=settings.melbourne)

if __name__ == '__main__':
	main()
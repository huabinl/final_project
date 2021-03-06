# COMP90055 Computing Project, Semester 1 2016
# Author: Huabin Liu (ID. 658274)

import csv
import json
import tweepy
import time
import geocoder
from textblob import TextBlob
from tweepy import AppAuthHandler
from tweepy.cursor import Cursor
import threading
import settings
import couchdb
import logging

# This class is a thread of twitter harvester
class Harvest(threading.Thread):
	def __init__(self, api, db, start_index, end_index):
		threading.Thread.__init__(self)
		self.api = api
		self.db = db
		self.start_index = start_index
		self.end_index = end_index

	# This function is for searching tweets on main roads of Melbourne via Twitter Search API
	def search(self, row):
		geo = row['latitude'] + ',' + row['longitude'] + ',' + row['radius'] + 'km'
		for i in range(3):
			try:
				for status in Cursor(self.api.search, geocode=geo, count=100).items():
					tweet = status._json
					# avoid duplicated tweets
					if tweet['id_str'] not in db:
						# add city field through Google Maps Geocoding API
						if 'geo' not in tweet or not tweet['geo']:
							tweet['geo'] = {'Type': 'Point', 'coordinates': [float(tweet['road_info']['coordinates']['latitude']), float(tweet['road_info']['coordinates']['longitude'])]}
						g = geocoder.google(tweet['geo']['coordinates'], method='reverse')
						tweet['city'] = g.city
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
						# add road info field
						tweet['road_info'] = {'road_name': row['road_name'], 'coordinates': {'latitude': row['latitude'], 'longitude': row['longitude'], 'radius': row['radius']}}
						# add sentiment field
						blob = TextBlob(tweet['text'])
						tweet['sentiment'] = {"polarity": blob.sentiment.polarity, "subjectivity": blob.sentiment.subjectivity}
						blob = TextBlob(tweet['text'], analyzer=NaiveBayesAnalyzer())
						tweet['sentiment']['classification'] = blob.sentiment.classification
						tweet['sentiment']['pos'] = blob.sentiment.p_pos
						tweet['sentiment']['neg'] = blob.sentiment.p_neg
						db[tweet['id_str']] = tweet
				break
			# error handling
			except tweepy.TweepError as e:
				print 'ERROR: ' + str(e)
				logging.error("ERROR: " + str(e))

	def run(self):
		logging.basicConfig(filename='road_harvest.log', filemode='w', level=logging.DEBUG)
		logging.info('start harvesting')

		# start twitter harvester
		print 'start'
		while True:
			with open(settings.csv) as csvfile:
				reader = csv.DictReader(csvfile)
				for i, row in enumerate(reader):
					if i in range(self.start_index, self.end_index):
						self.search(row)
		

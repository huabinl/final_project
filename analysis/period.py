# COMP90055 Computing Project, Semester 1 2016
# Author: Huabin Liu (ID. 658274)

import couchdb
import urllib
import settings
import logging

# count the number of tweets sent in Melbourne based on period
def period_tweet_count(db):
	doc = {}
	map_fun = '''function(doc) {
		emit(doc.datetime.period, 1);
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		doc[row.key] = row.value
	return doc

# count the sentiment of tweets sent in Melbourne based on period
def period_tweet_sentiment(db):
	doc = {}
	map_fun = '''function(doc) {
		emit(doc.datetime.period, doc.sentiment.polarity);
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		doc[row.key] = row.value
	return doc

# count the number of tweets sent on main roads of Melbourne based on period
def period_road_count(db):
	doc = {}
	map_fun = '''function(doc) {
		emit(doc.datetime.period, 1);
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		doc[row.key] = row.value
	return doc

# count the sentiment of tweets sent on main roads of Melbourne based on period
def period_road_sentiment(db):
	doc = {}
	map_fun = '''function(doc) {
		emit(doc.datetime.period, doc.sentiment.polarity);
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		doc[row.key] = row.value
	return doc

# count the number of tweets sent in traffic jam of Melbourne based on period
def period_congestion_count(db):
	doc = {}
	map_fun = '''function(doc) {
		if (doc.congestion === true) {
			emit(doc.datetime.period, 1);
		}
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		doc[row.key] = row.value
	return doc

# count the sentiment of tweets sent in traffic jam of Melbourne based on period
def period_congestion_sentiment(db):
	doc = {}
	map_fun = '''function(doc) {
		if (doc.congestion === true) {
			emit(doc.datetime.period, doc.sentiment.polarity);
		}
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		doc[row.key] = row.value
	return doc

# calculate the sentiment value on average
def process_sentiment(tweets, sentiment):
	for key in sentiment:
		if sentiment.get(key) != 0:
			sentiment[key] = sentiment.get(key) / float(tweets[key])
	return sentiment

def main():
	# access databases
	couch = couchdb.Server(settings.database_address)
	db = couch[settings.database]
	couch_melb = couchdb.Server(settings.database_address_melb)
	db_melb = couch_melb[settings.database_melb]
	try:
		db_period = couch.create('period')
	except couchdb.http.PreconditionFailed as e:
		db_period = couch['period']

	# analyse tweets for each period
	print 'start'
	tweet_melb = period_tweet_count(db_melb)
	sentiment_melb = process_sentiment(tweet_melb, period_tweet_sentiment(db_melb))
	tweet_road = period_road_count(db)
	sentiment_road = process_sentiment(tweet_road, period_road_sentiment(db))
	tweet_congestion = period_congestion_count(db)
	sentiment_congestion = process_sentiment(tweet_congestion, period_congestion_sentiment(db))

	for period in settings.period:
		doc = {}
		doc['tweet_melb'] = tweet_melb.get(period, 0)
		doc['sentiment_melb'] = sentiment_melb.get(period, 0)
		doc['tweet_road'] = tweet_road.get(period, 0)
		doc['sentiment_road'] = sentiment_road.get(period, 0)
		doc['tweet_congestion'] = tweet_congestion.get(period, 0)
		doc['sentiment_congestion'] = sentiment_congestion.get(period, 0)
		period_id = str(period)
		if period_id in db_period:
			del db_period[period_id]
		db_period[period_id] = doc
		print 'finished'

if __name__ == '__main__':
	main()
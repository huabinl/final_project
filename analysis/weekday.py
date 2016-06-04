# COMP90055 Computing Project, Semester 1 2016
# Author: Huabin Liu (ID. 658274)

import couchdb
import urllib
from collections import Counter
import settings
import logging

# count the number of tweets sent in Melbourne based on weekday
def weekday_tweet_count(db):
	doc = {}
	map_fun = '''function(doc) {
		emit(doc.datetime.weekday, 1);
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		doc[row.key] = row.value
	return doc

# count the sentiment of tweets sent in Melbourne based on weekday
def weekday_tweet_sentiment(db):
	doc = {}
	map_fun = '''function(doc) {
		emit(doc.datetime.weekday, doc.sentiment.polarity);
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		doc[row.key] = row.value
	return doc

# count the number of tweets sent on main roads of Melbourne based on weekday
def weekday_road_count(db):
	doc = {}
	map_fun = '''function(doc) {
		emit(doc.datetime.weekday, 1);
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		doc[row.key] = row.value
	return doc

# count the sentiment of tweets sent on main roads of Melbourne based on weekday
def weekday_road_sentiment(db):
	doc = {}
	map_fun = '''function(doc) {
		emit(doc.datetime.weekday, doc.sentiment.polarity);
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		doc[row.key] = row.value
	return doc

# count the number of tweets sent in traffic jam of Melbourne based on weekday
def weekday_congestion_count(db):
	doc = {}
	map_fun = '''function(doc) {
		if (doc.congestion === true) {
			emit(doc.datetime.weekday, 1);
		}
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		doc[row.key] = row.value
	return doc

# count the sentiment of tweets sent in traffic jam of Melbourne based on weekday
def weekday_congestion_sentiment(db):
	doc = {}
	map_fun = '''function(doc) {
		if (doc.congestion === true) {
			emit(doc.datetime.weekday, doc.sentiment.polarity);
		}
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		doc[row.key] = row.value
	return doc

# find al region with tweets sent for a given weekday and hour
def weekday_region_count(db):
	doc = {}
	map_fun = '''function(doc) {
		emit([doc.datetime.weekday, doc.datetime.hour, doc.city], 1);
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group_level=3).rows:
		if row.key[0] not in doc:
			doc[row.key[0]] = {}
		if row.key[1] not in doc[row.key[0]]:
			doc[row.key[0]][row.key[1]] = {}
		doc[row.key[0]][row.key[1]][row.key[2]] = row.value
	return doc

# calculate the difference in number of tweets sent for each region between the current hour and a pervious hour
def calc_region_diff(weekday_region):
	doc = {}
	for weekday in weekday_region:
		doc[weekday] = {}
		for i in range(7, 23):
			doc[weekday][i] = {}
			regions = set(weekday_region[weekday][i - 1].keys() + weekday_region[weekday][i].keys())
			for region in regions:
				doc[weekday][i][region] = weekday_region[weekday][i].get(region, 0) - weekday_region[weekday][i - 1].get(region, 0)
	return doc

# find the top 5 suburbs with maximum tweets growth/reduction for a given weekday and hour
def calc_rank(region_diff):
	top_5 = {}
	bottom_5 = {}
	for weekday in region_diff:
		top_5[weekday] = {}
		bottom_5[weekday] = {}
		for hour in region_diff[weekday]:
			top_5[weekday][hour] = {}
			bottom_5[weekday][hour] = {}
			tmp_result = Counter(region_diff[weekday][hour]).most_common()
			for i in range(1 , 6):
				top_5[weekday][hour][tmp_result[i][0]] = tmp_result[i][1]
			for i in range(-5, 0):
				bottom_5[weekday][hour][tmp_result[i][0]] = tmp_result[i][1]
	return top_5, bottom_5

# store each tweet with important info for a given weekday and hour
def weekday_hour_tweet(db):
	map_fun = '''function(doc) {
		emit(doc.id_str, {latitude: doc.geo.coordinates[0], longitude: doc.geo.coordinates[1], weekday: doc.datetime.weekday, hour: doc.datetime.hour});
	}'''

	tweets = {}
	for row in db.query(map_fun).rows:
		weekday = row.value['weekday']
		hour = row.value['hour']
		if weekday not in tweets:
			tweets[weekday] = {}
		if hour not in tweets[weekday]:
			tweets[weekday][hour] = [{'latitude': row.value['latitude'], 'longitude': row.value['longitude']}]
		else:
			tweets[weekday][hour].append({'latitude': row.value['latitude'], 'longitude': row.value['longitude']})
	return tweets

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
		db_weekday = couch.create('weekday')
	except couchdb.http.PreconditionFailed as e:
		db_weekday = couch['weekday']
	try:
		db_weekday_map = couch.create('weekday_map')
	except couchdb.http.PreconditionFailed as e:
		db_weekday_map = couch['weekday_map']

	id_map = {'Monday': '1', 'Tuesday':'2', 'Wednesday':'3', 'Thursday':'4', 'Friday':'5', 'Saturday':'6', 'Sunday':'7'}

	# analyse tweets for each weekday 
	print 'start'
	tweet_melb = weekday_tweet_count(db_melb)
	sentiment_melb = process_sentiment(tweet_melb, weekday_tweet_sentiment(db_melb))
	tweet_road = weekday_road_count(db)
	sentiment_road = process_sentiment(tweet_road, weekday_road_sentiment(db))
	tweet_congestion = weekday_congestion_count(db)
	sentiment_congestion = process_sentiment(tweet_congestion, weekday_congestion_sentiment(db))
	tweet_region = weekday_region_count(db)
	region_diff = calc_region_diff(tweet_region)
	top5_region, bottom5_region = calc_rank(region_diff)
	hour_tweet = weekday_hour_tweet(db)

	for day in settings.weekday:
		doc_id = id_map[day]
		doc = {}
		doc['tweet_melb'] = tweet_melb.get(day, 0)
		doc['sentiment_melb'] = sentiment_melb.get(day, 0)
		doc['tweet_road'] = tweet_road.get(day, 0)
		doc['sentiment_road'] = sentiment_road.get(day, 0)
		doc['tweet_congestion'] = tweet_congestion.get(day, 0)
		doc['sentiment_congestion'] = sentiment_congestion.get(day, 0)
		if doc_id in db_weekday:
			del db_weekday[doc_id]
		db_weekday[doc_id] = doc

		doc = {}
		doc['top_5'] = top5_region.get(day, {})
		doc['bottom_5'] = bottom5_region.get(day, {})
		doc['hour_tweet'] = hour_tweet.get(day, {})
		if doc_id in db_weekday_map:
			del db_weekday_map[doc_id]
		db_weekday_map[doc_id] = doc
	print 'finished'

if __name__ == '__main__':
	main()
# COMP90055 Computing Project, Semester 1 2016
# Author: Huabin Liu (ID. 658274)

import datetime
import math
import re
from sklearn.cluster import DBSCAN
import couchdb
import urllib
from collections import Counter
import settings

# build a hour-ids dictionary for a given date
def calc_ids(db):
	map_fun = '''function(doc) {
		if (doc.datetime.date === "2016-05-31") {
			emit(doc.id_str, doc.datetime.hour);
		}
	}'''

	ids = {}
	for row in db.query(map_fun).rows:
		key = row.value
		if key in ids:
			ids.get(key).append(row.key)
		else:
			ids[key] = [row.key]
	return ids

# calculate the spatial distance of two tweets
def calc_space_distance(lat_start, long_start, lat_end, long_end):
	rad_lat = math.radians(lat_start) - math.radians(lat_end)
	rad_long = math.radians(long_start) - math.radians(long_end)
	param = 2 * math.asin(math.sqrt(math.pow(math.sin(rad_lat / 2), 2) + math.cos(math.radians(lat_start)) * math.cos(math.radians(lat_end)) * math.pow(math.sin(rad_long / 2), 2)))
	distance = param * settings.earth_radius
	return distance

# calculate the time distance of two tweets
def calc_time_distance(time_start, time_end): #
	start = datetime.timedelta(hours=time_start['hour'], minutes=time_start['minute'], seconds=time_start['second']).total_seconds()
	end = datetime.timedelta(hours=time_end['hour'], minutes=time_end['minute'], seconds=time_end['second']).total_seconds()
	return abs(start - end)

# identify traffic congestion using DBSCAN algorithm
def calc_cluster(db, ids):
	length = len(ids)
	matrix = [[0.0 for x in range(length)] for y in range(length)] 
	for i in range(length):
		for j in range(i + 1, length):
			doc1 = db[ids[i]]
			doc2 = db[ids[j]]
			dist_space = calc_space_distance(doc1['geo']['coordinates'][0], doc1['geo']['coordinates'][1], doc2['geo']['coordinates'][0], doc2['geo']['coordinates'][1])
			dist_time = calc_time_distance(doc1['datetime'], doc2['datetime'])
			matrix[i][j] = dist_space * 0.5 + dist_time * 0.5
			matrix[j][i] = matrix[i][j]
	return DBSCAN(eps=600, min_samples=6, metric='precomputed').fit_predict(matrix)

# count the number of tweets sent in Melbourne based on hour for a given date
def date_tweet_count(db):
	doc = {}
	map_fun = '''function(doc) {
		if (doc.datetime.date === "2016-05-31") {
			emit(doc.datetime.hour, 1);
		}
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	overall = 0
	for row in db.query(map_fun, reduce_fun, group=True).rows:
		overall += row.value
		doc[row.key] = row.value
	doc['all'] = overall
	return doc

# count the sentiment of tweets sent in Melbourne based on hour for a given date
def date_tweet_sentiment(db):
	doc = {}
	map_fun = '''function(doc) {
		if (doc.datetime.date === "2016-05-31") {
			emit(doc.datetime.hour, doc.sentiment.polarity);
		}
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	overall = 0
	for row in db.query(map_fun, reduce_fun, group=True).rows:
		overall += row.value
		doc[row.key] = row.value
	doc['all'] = overall
	return doc

# count the number of tweets sent on main roads of Melbourne based on hour for a given date
def date_road_count(db):
	doc = {}
	map_fun = '''function(doc) {
		if (doc.datetime.date === "2016-05-31") {
			emit(doc.datetime.hour, 1);
		}
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	overall = 0
	for row in db.query(map_fun, reduce_fun, group=True).rows:
		overall += row.value
		doc[row.key] = row.value
	doc['all'] = overall
	return doc

# count the sentiment of tweets sent on main roads of Melbourne based on hour for a given date
def date_road_sentiment(db):
	doc = {}
	map_fun = '''function(doc) {
		if (doc.datetime.date === "2016-05-31") {
			emit(doc.datetime.hour, doc.sentiment.polarity);
		}
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	overall = 0
	for row in db.query(map_fun, reduce_fun, group=True).rows:
		overall += row.value
		doc[row.key] = row.value
	doc['all'] = overall
	return doc

# count the number of tweets sent in traffic jam of Melbourne based on hour for a given date
def date_congestion_count(db):
	doc = {}
	map_fun = '''function(doc) {
		if (doc.datetime.date === "2016-05-31" && doc.congestion === true) {
			emit(doc.datetime.hour, 1);
		}
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	overall = 0
	for row in db.query(map_fun, reduce_fun, group=True).rows:
		overall += row.value
		doc[row.key] = row.value
	doc['all'] = overall
	return doc

# count the sentiment of tweets sent in traffic jam of Melbourne based on hour for a given date
def date_congestion_sentiment(db):
	doc = {}
	map_fun = '''function(doc) {
		if (doc.datetime.date === "2016-05-31" && doc.congestion === true) {
			emit(doc.datetime.hour, doc.sentiment.polarity);
		}
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	overall = 0
	for row in db.query(map_fun, reduce_fun, group=True).rows:
		overall += row.value
		doc[row.key] = row.value
	doc['all'] = overall
	return doc

# find the top 10 busiest roads for a given date
def date_top_road(db):
	doc = {}
	map_fun = '''function(doc) {
		if (doc.datetime.date === "2016-05-31") {
			emit(doc.road_info.road_name, 1);
		}
	}'''

	reduce_fun = '''function(keys, values) {
		return sum(values);
	}'''

	for row in db.query(map_fun, reduce_fun, group=True).rows:
		doc[row.key] = row.value
	streets = Counter(doc).most_common(10)
	top_10 = {}
	for street in streets:
		top_10[street[0]] = street[1]
	return top_10

# store each tweet with important info for a given date
def date_road_tweet(db):
	map_fun = '''function(doc) {
		if (doc.datetime.date === "2016-05-31") {
			emit(doc.id_str, {latitude: doc.geo.coordinates[0], longitude: doc.geo.coordinates[1], time: doc.created_at, congestion: doc.congestion, road: doc.road_info.road_name, user:doc.user.screen_name,text:doc.text, sentiment:doc.sentiment.polarity, hour:doc.datetime.hour, minute:doc.datetime.minute});
		}
	}'''

	tweets = []
	for row in db.query(map_fun).rows:
		doc = row.value
		minute_to_hour = doc['minute'] / float(60)
		doc['timeline'] = doc['hour'] + minute_to_hour
		tweets.append(doc)
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
		db_date = couch.create('date')
	except couchdb.http.PreconditionFailed as e:
		db_date = couch['date']

	print 'start'
	date = '2016-05-31'
	if date in db_date:
		del db_date[date]

	# add congestion filed for a given date
	all_ids = calc_ids(db)
	for key in all_ids:
		ids = all_ids[key]
		result = calc_cluster(db, ids)
		for i in range(len(ids)):
			doc = db[ids[i]]
			if result[i] == -1:
				doc['congestion'] = False
			else:
				doc['congestion'] = True
			db[ids[i]] = doc

	# analyse tweets for a given date 
	doc = {}
	doc['tweet_melb'] = date_tweet_count(db_melb)
	doc['sentiment_melb'] = process_sentiment(doc.get('tweet_melb'), date_tweet_sentiment(db_melb))
	doc['tweet_road'] = date_road_count(db)
	doc['sentiment_road'] = process_sentiment(doc.get('tweet_road'), date_road_sentiment(db))
	doc['tweet_congestion'] = date_congestion_count(db)
	doc['sentiment_congestion'] = process_sentiment(doc.get('tweet_congestion'), date_congestion_sentiment(db))
	doc['top_road'] = date_top_road(db)
	doc['tweets'] = date_road_tweet(db)
	db_date[date] = doc
	print 'finished'

if __name__ == '__main__':
	main()
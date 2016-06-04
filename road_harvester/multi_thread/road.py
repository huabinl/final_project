# COMP90055 Computing Project, Semester 1 2016
# Author: Huabin Liu (ID. 658274)

import csv
import tweepy
import settings
import road_harvest
from tweepy import AppAuthHandler
import couchdb

def main():
	# access database
	couch = couchdb.Server(settings.database_address)
	try:
		db = couch.create(settings.database)
	except couchdb.http.PreconditionFailed as e:
		db = couch[settings.database]

	# application-only authentication for all key-pairs
	apis = []
	for app in settings.apps:
		auth = AppAuthHandler(app['consumer_key'], app['consumer_secret'])
		api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
		apis.append(api)

	rows_total = row_count()
	apis_total = len(apis)

	# initialize and start all harvester threads
	for i in range(apis_total):
		start, end = calc_boundary(i, rows_total, apis_total)
		road_harvest.thread = road_harvest.Harvest(apis[i], db, start, end)
		road_harvest.thread.start()

# allocate the task for each thread
def calc_boundary(rank, rows_size, apis_size):
	start = rank * rows_size // apis_size
	end = (rank + 1) * rows_size // apis_size
	return start, end

# count all rows in the task file
def row_count():
	count = 0
	with open(settings.csv, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			count += 1
		return count - 1

if __name__ == '__main__':
	main()
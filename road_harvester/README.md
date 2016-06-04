RoadHarvester
======
- Tweepy, Textblob, Geocoder and Couchdb libraries are needed to be installed in advance.
- Command to run single-thread version: python harvest.py     
- Command to run multi-thread version: python road.py

##Description
This folder contains two sub-folders for different versions of road tweets harvester. Nearly 67,000 requests need be sent to the Twitter Search API to harvest all tweets along the main roads of Melbourne. One single harvester takes more than 1 day and a half (i.e. 37 hours and 14 minutes) to traverse the whole search set, while multi-threading harvesters only take less than 6 hours (7 threads are used in the project).

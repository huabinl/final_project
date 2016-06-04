MelbourneHarvester
======
- Tweepy, Textblob, and Couchdb libraries are needed to be installed before.
- Commands to run: python stream_harvest.py     
python search_harvest.py

##Description
This folder contains two tweets harvesters: a realtime one and a back-up one. Realtime tweets harvester, which connects to Twitter Streamming API, is the major harvester to gather tweets sent in Greater Melbourne area. And the back-up harvester connects to Twitter Search API. It is used to search for the past tweets that missed once some error occurs in realtime harvester.

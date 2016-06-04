# COMP90055 Computing Project, Semester 1 2016
# Author: Huabin Liu (ID. 658274)

from flask import render_template, request
from app import app
import couchdb
import json

@app.route('/')
@app.route('/dashboard')
def dashboard():
	return render_template("dashboard.html")

@app.route('/map')
def roadmap():
	return render_template("map.html")

@app.route('/heatmap')
def heatmap():
	return render_template("heatmap.html")

@app.route('/doc')
def doc():
	return render_template("doc.html")

@app.route('/date/<day>')
def date(day):
	couch = couchdb.Server('http://115.146.89.53:5984/')

	db = couch['date']
	data = db[day]
	return json.dumps(data)

@app.route('/hourdata')
def hour():
	couch = couchdb.Server('http://115.146.89.53:5984/')

	db = couch['hour']
	data=[]
	for id in db:
		data.append(db[id])
	return json.dumps(data)

@app.route('/weekdaydata')
def weekday():
	couch = couchdb.Server('http://115.146.89.53:5984/')

	db = couch['weekday']
	data=[]
	for id in db:
		data.append(db[id])
	return json.dumps(data)

@app.route('/perioddata')
def period():
	couch = couchdb.Server('http://115.146.89.53:5984/')

	db = couch['period']
	data=[]
	for id in db:
		data.append(db[id])
	return json.dumps(data)

@app.route('/alldate')
def all_date():
	couch = couchdb.Server('http://115.146.89.53:5984/')

	db = couch['date']
	data=[]
	for id in db:
		data.append(id)
	return json.dumps(data)

@app.route('/mapdata/<weekday>')
def weekday_map(weekday):
	couch = couchdb.Server('http://115.146.89.53:5984/')

	db = couch['weekday_map']
	data = db[weekday]
	return json.dumps(data)

Computing Project
================

##Overview
This repository contains the source of my Computing Project (COMP90055) in University of Melbourne. It is a 25 credit points subject. This system is mainly written in Python, and now deployed across three instances in NeCTAR Research Cloud (https://www.nectar.org.au/)
- Supervisor: Professor Richard Sinnott
- Author: Huabin Liu (ID: 658274)  
- Email: huabinl@student.unimelb.edu.au
- Web Service URL: http://115.146.89.254/
- Video Demo Link: https://youtu.be/7wzAJwOsgmI/
- Github Souce Code: https://github.com/huabinl/final_project

##Purposes
This project has two main purposes. One is to integrate sentiment analysis with transport information, and discover interesting behaviour patterns based on Twitter data gathered in Melbourne. The second is detecting traffic flow on tweets harvested from the road network in Melbourne. This project is specifically targeted to the Greater Melbourne area, but the methodology behind it is general enough to be extended to other Australian cities.

##Services
- Targeted twitter harvesters (Collecting tweets sent in Melbourne, and tweets sent on main roads of Melbourne)
- Web services for transport rrelated tweets, congestion indentification, sentiment analysis and traffic flow detection
- Front-end data visualisation service

##Components
- Twitter Harvesters (for Streamming API and Search API)
- A PSMA Data Preprocessor
- Data analysers (for hour, period, date (a DBSCAN clustering calculator included) and weekday)
- Web Service

There are individual README files in component folders.

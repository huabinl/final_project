# COMP90055 Computing Project, Semester 1 2016
# Author: Huabin Liu (ID. 658274)

import json
import csv
import math
import settings

# calculate the distace between two points
def calc_distance(lat_start, long_start, lat_end, long_end):
	rad_lat = math.radians(lat_start) - math.radians(lat_end)
	rad_long = math.radians(long_start) - math.radians(long_end)
	param = 2 * math.asin(math.sqrt(math.pow(math.sin(rad_lat / 2), 2) + math.cos(math.radians(lat_start)) * math.cos(math.radians(lat_end)) * math.pow(math.sin(rad_long / 2), 2)))
	distance = param * settings.earth_radius
	return distance

# for a given road, calculate all subcells for further search, and write the result in a csv file
def calc_cell(name, road_type, coordinates, csv_writer):
	num = len(coordinates)
	lat_start = coordinates[0][1]
	long_start = coordinates[0][0]
	lat_end = coordinates[num - 1][1]
	long_end = coordinates[num - 1][0]
	max_distance = calc_distance(lat_start, long_start, lat_end, long_end)
	block = int(max_distance / settings.cell_distance) + 1
	lat0 = (lat_end - lat_start) / block
	long0 = (long_end - long_start) / block
	for i in range(0, block):
		cur_lat = lat_start + i * lat0
		cur_long = long_start + i * long0
		csv_writer.writerow({'road_name': name, 'latitude': cur_lat, 'longitude': cur_long, 'radius': settings.cell_distance / 1000.0})

# read and process the PSMA road network data
def read_road_file(file_path, road_type, csv_writer):
	with open(file_path) as data_file:    
		data = json.load(data_file)
		points = []
		for feature in data['features']:
			if feature['properties']['subtype_cd'] == road_type:
				calc_cell(feature['properties']['full_name'], road_type, feature['geometry']['coordinates'], csv_writer)

def main():
	with open('road.csv', 'w') as csvfile:
		fieldnames = ['road_name', 'latitude', 'longitude', 'radius']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
	
		read_road_file('road.json', 1, writer)
		read_road_file('mainroad.json', 2, writer)
		read_road_file('mainroad.json', 3, writer)

if __name__ == '__main__':
	main()


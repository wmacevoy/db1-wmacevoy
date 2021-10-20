#!/usr/bin/env python

import csv
import sample
import collector
import location
import filters

def createRecord(row):
    print(f"createRecord({row})")

    collectorName = row['collector']
    collectorRow=collector.select_collector_by_name(collectorName)
    if collectorRow == None:
        collectorId=collector.insert_collector({'name': collectorName, 'email': 'miss@ing'})
    else:
        collectorId=collectorRow['id']
    locationName = row['location']
    locationRow=location.select_location_by_name(locationName)
    if locationRow == None:
        raise ValueError(f"location {locationName} not in database.")
    locationId=collectorRow['id']
    covidPPM=filters.dbReal(row['covidPPM'])
    if covidPPM < 0:
        raise ValueError(f"invalid covid ppm value.")
    sample.insert_sample({
        sample.COL_COVID_PPM: covidPPM, 
        sample.COL_COLLECTOR_ID: collectorId, 
        sample.COL_LOCATION_ID : locationId})
    
dataFile='sample covid data - Sheet1.csv'
with open(dataFile) as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        createRecord(row)

#!/usr/bin/env python

import config
import csv
import sample
import collector
import location
import filters
import sys

def createRecord(row,db=config.DB_NAME):
    print(f"createRecord({row})")

    collectorName = row['collector'] if 'collector' in row else row['tester']
    collectorRow=collector.select_collector_by_name(collectorName,db)
    if collectorRow == None:
        collectorId=collector.insert_collector({
            'name': collectorName, 
            'email': 'miss@ing'},db)
    else:
        collectorId=collectorRow['id']
    locationName = row['location']
    locationRow=location.select_location_by_name(locationName,db)
    if locationRow == None:
        raise ValueError(f"location {locationName} not in database.")
    locationId=locationRow['id']
    covidPPM=filters.dbReal(row['covidPPM'])
    if covidPPM < 0:
        raise ValueError(f"invalid covid ppm value.")
    sampleId=sample.insert_sample({
        sample.COL_COVID_PPM: covidPPM, 
        sample.COL_COLLECTOR_ID: collectorId, 
        sample.COL_LOCATION_ID : locationId},db)
    return (sampleId, collectorId, locationId)

def csvImport(csvFileName,db=config.DB_NAME):
    with open(csvFileName) as csvFile:
        data = csv.DictReader(csvFile)
        for row in data:
            createRecord(row,db)

if __name__ == '__main__':
    for file in sys.argv[1:]:
        csvImport(file)

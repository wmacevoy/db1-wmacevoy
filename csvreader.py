#!/usr/bin/env python

import csv
import sample
import collector
import location

def createRecord(row):
    collectorName = row['collector']
    collectorRow=collector.select_collector_by_name(collectorName)
    if collectorRow == None:
        collectorId=collector.insert_collector({'name': collectorName, 'email': 'miss@ing'})
    else:
        collectorId=collectorRow['id']
    
dataFile='sample covid data - Sheet1.csv'
with open(dataFile) as csvfile:
    data = csv.DictReader(csvfile)
    createRecord(row)

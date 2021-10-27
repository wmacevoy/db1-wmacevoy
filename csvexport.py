#!/usr/bin/env python

import config
import csv
import sample
import collector
import location
import filters
import sys


import sample


def csvExport(location_name,csvFileName,db=config.DB_NAME):
    (min,max)=sample.select_min_and_max_by_location_name(location_name,db)
    minRows=sample.select_rows_by_location_and_sample_range(location_name,min-0.0001,min+0.0001,db)
    maxRows=sample.select_rows_by_location_and_sample_range(location_name,max-0.0001,max+0.0001,db)
    allRows=minRows.copy()
    allRows.extend(maxRows)
    with open(csvFileName,"w") as csvFile:
        writer=csv.DictWriter(csvFile,['id', 'covidPPM','collector','location'])
        writer.writeheader()

        for row in allRows:
            sampleId = row[0]
            sampleRow = sample.select_sample_by_id(sampleId,db)
            locationId = sampleRow['locationID']
            collectorId = sampleRow['collectorID']
            locationRow = location.select_location_by_id(locationId,db)
            collectorRow = collector.select_collector_by_id(collectorId,db)
            
            writer.writerow({'id': sampleId, 
                'covidPPM': sampleRow['covidPPM'],
                 'collector': collectorRow['name'], 
                 'location': locationRow['name']})


if __name__ == '__main__':
    location_name=sys.argv[1]
    for file in sys.argv[2:]:
        csvExport(location_name,file)

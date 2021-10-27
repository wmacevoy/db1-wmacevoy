#!/usr/bin/env python

import config
import csv
import sample
import collector
import location
import filters
import sys


import sample


def csvExport(csvFileName,db=config.DB_NAME):
    (min,max)=sample.select_min_and_max_by_location_name(locationName,db)
    minRows=sample.select_rows_by_location_and_sample_range(locationName,min-0.0001,min+0.0001,db)
    maxRows=sample.select_rows_by_location_and_sample_range(locationName,min-0.0001,min+0.0001,db)
    allRows=minRows.copy()
    allRows.extend(maxRows)
    with open(csvFileName) as csvFile:
        writer=csv.DictWriter(csvFile,['id', 'covidPPM','collector','location'])
        writer.writeheader()
        

        for row in allRows:
            sampleId = row[0]
            sample = sample.select_sample_by_id(sampleId,db)
            locationId = sample['locationId']
            collectorId = sample['collectorId']
            location = location.select_location_by_id(locationId,db)
            collector = collector.select_collector_by_id(collectorId,db)
            
            writer.writerow({'id': sampleId, 
                'covidPPM': sample['covidPPM'],
                 'collector': collector['name'], 
                 'location': location['name']})


if __name__ == '__main__':
    for file in sys.argv[1:]:
        csvExport(file)

#!/usr/bin/env python
import random

import sample
import location
import collector

def clean():
    sample.drop_sample_table()
    location.drop_location_table()
    collector.drop_collector_table()

def create():
    sample.create_sample_table()
    location.create_location_table()
    collector.create_collector_table()

def setup():
    clean()
    create()

    aliceId = collector.insert_collector({
        collector.COL_NAME: 'alice',
        collector.COL_EMAIL: 'alice@peeps.com'
    })

    bobId = collector.insert_collector({
        collector.COL_NAME: 'bob',
        collector.COL_EMAIL: 'bob@peeps.com'
    })

    ucId = location.insert_location({
        location.COL_NAME: 'uc',
        location.COL_LATITUDE: 3.14,
        location.COL_LONGITUDE: 33.33
    })

    confluenceId = location.insert_location({
        location.COL_NAME: 'confluence',
        location.COL_LATITUDE: 21.22,
        location.COL_LONGITUDE: 44.44
    })
    

    for test in range(1000):
        if test % 4 in [0,1]:
            collectorId = aliceId
        else:
            collectorId = bobId
        if test % 4 in [0,2]:
            locationId = ucId
        else:
            locationId = confluenceId
        covidPPM = random.random()
        sample.insert_sample({
            sample.COL_COVID_PPM: covidPPM,
            sample.COL_LOCATION_ID: locationId,
            sample.COL_COLLECTOR_ID: collectorId
        })

if __name__ == '__main__':
    print ('setup()')
    setup()
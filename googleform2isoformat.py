#!/usr/bin/env python

from datetime import datetime

def googleform2sqllitedatetime(formTime):
    try:
        dt = datetime.strptime(formTime, '%m/%d/%Y %H:%M:%S.%f')
    except ValueError:
        dt = datetime.strptime(formTime, '%m/%d/%Y %H:%M:%S')
    iso = dt.isoformat()
    return iso

formTime="11/2/2021 16:16:14"
dbTime="2021-11-02T16:16:14"

result=googleform2sqllitedatetime(formTime)

if (dbTime != result):
    raise ValueError(result)

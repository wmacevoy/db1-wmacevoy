#!/usr/bin/env python

import datetime
# import dateutil.parser
import pytz

def googleform2sqllitedatetime(formTime):
#     dt = dateutil.parser.parse(formTime)
    dt = datetime.datetime.strptime(formTime,"%m/%d/%Y %H:%M:%S")
    iso = dt.isoformat()
    return iso

formTime="11/2/2021 16:16:14"
dbTime="2021-11-02T16:16:14"

result=googleform2sqllitedatetime(formTime)

if (dbTime != result):
    raise ValueError(result)

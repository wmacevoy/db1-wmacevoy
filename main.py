#!/usr/bin/env python

import sample

results=sample.select_sample_id_by_location_name('uc')
min=None
max=None
for row in results:
    sample_id=row[0]
    location_id=row[1]
    sample_row=sample.select_sample_by_id(sample_id)
    if min == None or min['covidPPM'] > sample_row['covidPPM']:
        min = sample_row
    if max == None or max['covidPPM'] < sample_row['covidPPM']:
        max = sample_row

print(f"min: {min}")
print(f"max: {max}")
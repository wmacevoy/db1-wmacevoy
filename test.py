#!/usr/bin/env python

import sample
import location
import collector
import test_csvimport

def test():
    sample.test_sample()
    location.test_location()
    collector.test_collector()
    test_csvimport.test_csvimport_row()

test()
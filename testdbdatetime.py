#!/usr/bin/env python3

import os
from unittest import TestCase, main

from dbdatetime import DbDateTime

class TestDatetime(TestCase):
    TEST_DATE=2458794.810185185

    def testNow(self):
        dt = DbDateTime()
        result = dt.now()
        self.assertEqual(result,float(result))
        self.assertEqual(dt.datetime(result,"+1 day"),result+1.0)

    def testFormat(self):
        dt = DbDateTime()
        testJulianDate = 2458794.810185185
        expect = '2019-11-07 07:26:40 utc'
        result=dt.format(testJulianDate)
        self.assertEqual(expect,result)


if __name__ == '__main__':
    main()

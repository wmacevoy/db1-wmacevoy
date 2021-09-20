#!/usr/bin/env python

import sqlite3;

DB_NAME="covid.db"
DB_TEST_NAME="covid-test.db"

def drop_sample_table(db=DB_NAME):
    print("drop_sample_table()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = """
    drop table if exists sample
    """
    cursor.execute(sql)
    connection.commit()
    connection.close()

def create_sample_table(db=DB_NAME):
    print("create_sample_table()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = """
    create table if not exists sample (
        id integer primary key,
        covidPPM real,
        locationID integer,
        collectorID integer
    )
    """
    cursor.execute(sql)
    connection.commit()
    connection.close()

def dbInteger(value, nullable = False):
    return int(value) if not nullable or value != None else None

def dbReal(value, nullable = False):
    return float(value) if not nullable or value != None else None

def dbString(value, nullable = False):
    return str(value) if not nullable or value != None else None

def dbShift(value, nullable = False):
    strValue=dbString(value,nullable)
    if strValue in ['day','evening','night']:
        return strValue
    else:
        raise ValueError('value ' + strValue + ' is not day eveninig or night.')
    
def integerOrNull(value):
    return int(value) if value != None else None

def realOrNull(value):
    return float(value) if value != None else None

def insert_sample(values,db=DB_NAME):
    print("insert_sample()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = """
      insert into sample (covidPPM, collectorID, locationID)
      values (:covidPPM, :collectorID, :locationID)
      """
    params = {'covidPPM': realOrNull(values['covidPPM']), 
        'locationID': integerOrNull(values['locationID']), 
        'collectorID': integerOrNull(values['collectorID']) }
    cursor.execute(sql,params)
    connection.commit()
    connection.close()
    return cursor.lastrowid

def select_sample_by_id(id,db=DB_NAME):
    print("select_sample_by_id()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = """
      select collectorID, covidPPM, locationID from sample
      where (ID = :ID)
      """
    params = {'ID': dbInteger(id)}
    cursor.execute(sql,params)
    response=cursor.fetchone()
    if response != None:
        return {
            'ID' : dbInteger(id),
            'collectorID': response[0],
            'covidPPM': response[1],
            'locationID': response[2]
        }
    else:
        return None
    connection.close()

def test_sample():
    drop_sample_table(DB_TEST_NAME)
    create_sample_table(DB_TEST_NAME)
    id1=insert_sample({'covidPPM': '3.14', 'locationID': 1, 'collectorID': 2},DB_TEST_NAME)
    id2=insert_sample({'covidPPM': 5.00, 'locationID': 13, 'collectorID': 22},DB_TEST_NAME)
    row1=select_sample_by_id(id1,DB_TEST_NAME)
    row2=select_sample_by_id(id2,DB_TEST_NAME)
    rowNone=select_sample_by_id(32984057,DB_TEST_NAME)
    if rowNone != None:
        raise ValueError('not none')
    if row1['ID'] != id1:
        raise ValueError('id1 id wrong:' + str(row1['ID']))
    if row1['covidPPM'] != 3.14:
        raise ValueError('id1 sample wrong.')
    if row2['locationID'] != 13:
        raise ValueError('id2 location wrong.')
    if row2['collectorID'] != 22:
        raise ValueError('id2 collector wrong.')
def main():
    test_sample()


main()
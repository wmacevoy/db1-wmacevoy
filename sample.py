import sqlite3
import config
import filters
import generic

TABLE_NAME="sample"

def drop_sample_table(db=config.DB_NAME):
    generic.drop_table(TABLE_NAME,db)

def create_sample_table(db=config.DB_NAME):
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


def insert_sample(values,db=config.DB_NAME):
    print("insert_sample()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = """
      insert into sample (covidPPM, collectorID, locationID)
      values (:covidPPM, :collectorID, :locationID)
      """
    params = {'covidPPM': filters.realOrNull(values['covidPPM']), 
        'locationID': filters.integerOrNull(values['locationID']), 
        'collectorID': filters.integerOrNull(values['collectorID']) }
    cursor.execute(sql,params)
    connection.commit()
    connection.close()
    return cursor.lastrowid

def select_sample_by_id(id,db=config.DB_NAME):
    print("select_sample_by_id()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = """
      select collectorID, covidPPM, locationID from sample
      where (ID = :ID)
      """
    params = {'ID': filters.dbInteger(id)}
    cursor.execute(sql,params)
    response=cursor.fetchone()
    if response != None:
        return {
            'ID' : filters.dbInteger(id),
            'collectorID': response[0],
            'covidPPM': response[1],
            'locationID': response[2]
        }
    else:
        return None
    connection.close()

def test_sample():
    db=config.DB_TEST_NAME
    drop_sample_table(db)
    create_sample_table(db)
    id1=insert_sample({'covidPPM': '3.14', 'locationID': 1, 'collectorID': 2},db)
    id2=insert_sample({'covidPPM': 5.00, 'locationID': 13, 'collectorID': 22},db)
    row1=select_sample_by_id(id1,db)
    row2=select_sample_by_id(id2,db)
    rowNone=select_sample_by_id(32984057,db)
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

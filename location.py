import sqlite3
import config
import filters
import generic

TABLE_NAME="location"
COL_ID="id"
COL_NAME="name"
COL_LATITUDE="latitude"
COL_LONGITUDE="longitude"

def drop_location_table(db=config.DB_NAME):
    generic.drop_table(TABLE_NAME,db)

def create_location_table(db=config.DB_NAME):
    print("create_location_table()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
    create table if not exists {TABLE_NAME} (
        {COL_ID} integer primary key,
        {COL_NAME} text not null,
        {COL_LATITUDE} real not null,
        {COL_LONGITUDE} real not null
    )
    """
    print("sql=" + sql)
    cursor.execute(sql)
    connection.commit()
    connection.close()


def insert_location(values,db=config.DB_NAME):
    print(f"insert_location()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
      insert into {TABLE_NAME} ({COL_NAME}, {COL_LATITUDE}, {COL_LONGITUDE})
      values (:{COL_NAME}, :{COL_LATITUDE}, :{COL_LONGITUDE})
      """
    params = {COL_NAME: filters.dbString(values[COL_NAME]), 
        COL_LATITUDE: filters.dbReal(values[COL_LATITUDE]), 
        COL_LONGITUDE: filters.dbReal(values[COL_LONGITUDE]) }
    cursor.execute(sql,params)
    connection.commit()
    connection.close()
    return cursor.lastrowid

def select_location_by_id(id,db=config.DB_NAME):
    print("select_location_by_id()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
      select name, latitude, longitude from {TABLE_NAME}
      where (ID = :ID)
      """
    params = {'ID': filters.dbInteger(id)}
    cursor.execute(sql,params)
    response=cursor.fetchone()
    if response != None:
        return {
            'ID' : filters.dbInteger(id),
            'name': response[0],
            'latitude': response[1],
            'longitude': response[2]
        }
    else:
        return None
    connection.close()

def test_location():
    db=config.DB_TEST_NAME
    drop_location_table(db)
    create_location_table(db)
    id1=insert_location({
        'name': 'uc', 
        'latitude': 3.14, 
        'longitude': 7.77})
    id2=insert_location({
        'name': 'confluence', 
        'latitude': 4.13, 
        'longitude': 9.01})
    row1=select_location_by_id(id1,db)
    row2=select_location_by_id(id2,db)
    rowNone=select_location_by_id(32984057,db)
    if rowNone != None:
        raise ValueError('not none')
    if row1['ID'] != id1:
        raise ValueError('id1 id wrong:' + str(row1['ID']))
    if row1['name'] != 'uc':
        raise ValueError('id1 location wrong.')
    if row2['latitude'] != 4.13:
        raise ValueError('id2 location wrong.')
    if row2['longitude'] != 9.01:
        raise ValueError('id2 location wrong.')

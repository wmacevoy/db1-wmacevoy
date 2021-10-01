import sqlite3
import config
import filters
import generic

TABLE_NAME="collector"
COL_ID="id"
COL_NAME="name"
COL_EMAIL="email"

def drop_collector_table(db=config.DB_NAME):
    generic.drop_table(TABLE_NAME,db)

def create_collector_table(db=config.DB_NAME):
    print("create_collector_table()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
    create table if not exists {TABLE_NAME} (
        {COL_ID} integer primary key,
        {COL_NAME} text not null,
        {COL_EMAIL} text not null
    )
    """
    print("sql=" + sql)
    cursor.execute(sql)
    connection.commit()
    connection.close()


def insert_collector(values,db=config.DB_NAME):
    print(f"insert_collector(values={values},db={db})")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
      insert into {TABLE_NAME} ({COL_NAME}, {COL_EMAIL})
      values (:{COL_NAME}, :{COL_EMAIL})
      """
    params = {COL_NAME: filters.dbString(values[COL_NAME]), 
        COL_EMAIL: filters.dbString(values[COL_EMAIL]) }
    cursor.execute(sql,params)
    connection.commit()
    connection.close()
    return cursor.lastrowid

def select_collector_by_id(id,db=config.DB_NAME):
    print("select_collector_by_id()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
      select {COL_NAME}, {COL_EMAIL} from {TABLE_NAME}
      where ({COL_ID} = :{COL_ID})
      """

    print('sql='+sql)
    params = {COL_ID: filters.dbInteger(id)}
    cursor.execute(sql,params)
    response=cursor.fetchone()
    if response != None:
        return {
            COL_ID : filters.dbInteger(id),
            COL_NAME: response[0],
            COL_EMAIL: response[1]
        }
    else:
        return None
    connection.close()

def test_collector():
    db=config.DB_TEST_NAME
    drop_collector_table(db)
    create_collector_table(db)
    id1=insert_collector({
        'name': 'alice', 
        'email': 'alice@peeps.com'},db) 
    id2=insert_collector({
        'name': 'bob', 
        'email': 'bob@peeps.com'},db)
    row1=select_collector_by_id(id1,db)
    row2=select_collector_by_id(id2,db)
    rowNone=select_collector_by_id(32984057,db)
    if rowNone != None:
        raise ValueError('not none')
    if row1['id'] != id1:
        raise ValueError('id1 id wrong:' + str(row1['ID']))
    if row1['name'] != 'alice':
        raise ValueError('id1 name wrong.')
    if row2['email'] != 'bob@peeps.com':
        raise ValueError('id2 email wrong.')

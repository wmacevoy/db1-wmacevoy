import sqlite3
import config
import filters

def drop_table(tableName,db=config.DB_NAME):
    print("drop_table()")
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    sql = f"""
    drop table if exists {tableName}
    """
    cursor.execute(sql)
    connection.commit()
    connection.close()

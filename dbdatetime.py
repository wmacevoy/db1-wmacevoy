import sqlite3

class DbDateTime:
    def __init__(self):
        self._db = None

    @property
    def db(self):
        if self._db == None:
            self._db = sqlite3.connect(":memory:")
        return self._db

    def datetime(self,time,modifier=None):
        if modifier != None:
            parameters=(time,modifier)
            sql = "select julianday(datetime(?,?))"
        else:
            parameters=(time,)
            sql = "select julianday(datetime(?))"
        cursor = self.db.execute(sql,parameters)
        return (list(cursor))[0][0]

    def format(self,julianday,format='%Y-%m-%d %H:%M:%S utc'):
        parameters=(format,julianday)
        sql = "select strftime(?,?)"
        cursor = self.db.execute(sql,parameters)
        return (list(cursor))[0][0]

    def now(self):
        return self.datetime('now')

import mysql.connector

class Database():
    def __init__(self, host, port, database, table, isInnoDB, user, password):
        config = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }
        self.TABLE = table
        self.ISINNODB = isInnoDB
        try:
            self.cnn = mysql.connector.connect(**config)
            self.cur = self.cnn.cursor()
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                raise # username & password wrong.
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                raise # database doesn't exist.
            else:
                raise
    
    def __del__(self):
        if self.ISINNODB:
            self.cnn.commit()
        self.cur.close()
        self.cnn.close()
    
    def _execute(self, sql):
        try:
            self.cur.execute(sql)
        except mysql.connector.Error as e:
            if e.errno==1062:
                raise DatabaseError(1, e)
            raise DatabaseError(-1, e)
    
    def create_table(self):
        SQL_CREATE_TABLE = '''CREATE TABLE %s \
            (id BIGINT Unsigned NOT NULL, \
            token CHAR(64) NOT NULL, secret CHAR(50) NOT NULL, \
                name CHAR(15), enabled BIT default 1, \ 
            PRIMARY KEY (id) )''' % \
            (self.TABLE)
        self._execute(SQL_CREATE_TABLE)
    
    
    def delete_user(self, id):
        SQL_DELETE_USER = '''DELETE FROM %s WHERE id=%d''' % \
                            (self.TABLE, id)
        self._execute(SQL_DELETE_USER)
        
    def disable_user(self, id):
        SQL_DISABLE_USER = '''UPDATE %s SET enabled=0 WHERE id=%d''' % \
            (self.TABLE, id)
        self._execute(SQL_DISABLE_USER)
    
    def enable_user(self, id):
        SQL_ENABLE_USER = '''UPDATE %s SET enabled=1 WHERE id=%d''' % \
            (self.TABLE, id)
        self._execute(SQL_ENABLE_USER)
    
    def insert_user(self, id, name, token, secret):
        SQL_INSERT_USER = '''INSERT INTO %s (id, token, secret, name, enabled) \
            VALUES (%d, "%s", "%s", "%s", 1)''' % \
            (self.TABLE, id, token, secret, name)
        self._execute(SQL_INSERT_USER)
    
    def query_all(self):
        SQL_QUERY_ALL = '''SELECT * FROM %s''' % (self.TABLE)
        self._execute(SQL_QUERY_ALL)
        li = []
        for o in self.cur:
            li.append(DatabaseUser(o[0], o[1], o[2], o[3], o[4]))
        return li
    
    def query_enabled(self):
        SQL_QUERY_ENABLED = '''SELECT * FROM %s WHERE enabled=1''' % (self.TABLE)
        self._execute(SQL_QUERY_ENABLED)
        li = []
        for o in self.cur:
            li.append(DatabaseUser(o[0], o[1], o[2], o[3], o[4]))
        return li
    
    def update_name(self, id, name):
        SQL_UPDATE_NAME = '''UPDATE %s SET name="%s" WHERE id=%d''' % \
            (self.TABLE, name, id)
        self._execute(SQL_UPDATE_NAME)
    
    def update_user(self, id, name, token, secret):
        SQL_UPDATE_USER = '''UPDATE %s \
            SET name="%s", token="%s", secret="%s" \
            WHERE id=%d''' % \
            (self.TABLE, name, token, secret, id)
        self._execute(SQL_UPDATE_USER)
    

class DatabaseUser():
    def __init__(self, id, token, secret, name, enabled):
        self.id = id
        self.token = token
        self.secret = secret
        self.name = name
        self.enabled = enabled
    

ERROR_MESSAGE = {
    0: 'Anything is OK.',
    1: 'User already exist.',
    7: 'Critical!',
}
class DatabaseError(Exception):
    def __init__(self, code=0, e=None):
        self.code = code
        self.message = ERROR_MESSAGE.get(code, 'Invalid Error Code.')
        if e:
            self.errno = e.errno
            self.sqlstate = e.sqlstate
            self.sqlmsg = e.msg
        else:
            self.errno = None
            self.sqlstate = None
            self.sqlmsg = None


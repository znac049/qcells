import mysql.connector
import logger
import dataclasses
import types

from recordSet import *

class coreSQL:
    def __init__(self, user, password, database, host='localhost'):
        self.db_conn = None
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.tables = []

        self.connect()
        print(self.db_conn)
        self.get_list_of_tables()

    def connect(self):
        self.db_conn = mysql.connector.connect(**self.config)

    def is_connected(self):
        return self.db_conn != None

    def has_table(self, table_name):
        if table_name in self.tables:
            return True
        return False

    def query(self, sql, params=None):
        data = []

        with self.db_conn.cursor() as cursor:
            cursor.execute(sql)

            return recordSet(cursor)

    def insert(self, sql, values):
        with self.db_conn.cursor() as cursor:
            try:
                # print("SQL:", sql, values)
                affected_count = cursor.execute(sql, values)
                self.db_conn.commit()
                return cursor.lastrowid
            except MySQLdb.IntegrityError:
                printf("SQL ERROR")

        return -1

    def get_list_of_tables(self):
        self.tables = []
        if self.is_connected():
            rst = self.query("SHOW TABLES")
            col = rst.nameOf(0)
            for row in rst:
                self.tables += [row[col],]

    def describe_table(self, table_name):
        if not self.has_table(table_name):
            return None

        # The table exists
        return self.query("DESCRIBE {}".format(table_name))

    
    def create_table(self, table_name, table_dataclass):
        print(f"Create table {table_name}")
        for fld in dataclasses.fields(table_dataclass):
            print(fld)
            ft = fld.type
            if ft == int:
                print("INT")
            elif ft == str:
                print("BLOB/STR")
            else:
                print("DUNNO")

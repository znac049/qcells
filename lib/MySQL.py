import mysql.connector
import time
import logging

class MySQLException(Exception):
    pass

class MySQL:
    def __init__(self):
        self.conn = None
        self.logger = logging.getLogger(__name__)

    def connect(self, config, attempts=3, delay=2):
        attempt = 1
        # Implement a reconnection routine
        while attempt < attempts + 1:
            try:
                self.conn = mysql.connector.connect(**config)
                return True
            except (mysql.connector.Error, IOError) as err:
                if (attempts is attempt):
                    # Attempts to reconnect failed; returning None
                    self.logger.info("Failed to connect, exiting without a connection: %s", err)
                    return False
                self.logger.info(
                    "Connection failed: %s. Retrying (%d/%d)...",
                    err,
                    attempt,
                    attempts-1,
                )
                # progressive reconnect delay
                time.sleep(delay ** attempt)
                attempt += 1
        return False
    
    def isConnected(self):
        return self.conn and self.conn.is_connected()
    
    def query(self, sql, params=()):
        if self.isConnected():
            with self.conn.cursor() as cursor:
                result = cursor.execute(sql, params)
                rows = cursor.fetchall();
                return rows
        return None
    
    def querySingleton(self, sql, params=()):
        rows = self.query(sql, params)
        n_records = len(rows)
        if n_records > 1:
            raise MySQLException("Too many records returned. Was expecting 1 but got {}".format(n_records))
        elif n_records < 1:
            raise MySQLException("no records returned where 1 was expected")

        return rows[0]

import psycopg2
from psycopg2.extras import RealDictCursor


# Класс DB с базовым функционалом

class DB:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None


    def connect(self):
        try:
            self.connection = psycopg2.connect(
                database=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )

            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print(f"CONNECTED TO: '{self.dbname}' ON: {self.host}:{self.port}")

        except Exception as e:
            print(f"Connection error: {e}")


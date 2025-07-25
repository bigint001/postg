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

    # connection to DB
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

    # create table
    def create_table(self, schema: str):
        try:
            self.cursor.execute(schema)
            self.connection.commit()
            print(f"[+] Table created successfully (or already exists)")
        except Exception as e:
            print(f"[!] Error creating table: {e}")
            self.connection.rollback()

    # method insert
    def insert(self, table: str, data: dict):
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(['%s'] * len(data))
            values = list(data.values())

            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

            with self.connection.cursor() as cursor:
                cursor.execute(query, values)
                self.connection.commit()
            print(f"[✓] Inserted into {table}: {data}")
            return True

        except Exception as e:
                print(f"[!] Error inserting into {table}: {e}")
                return False

    # method select
    def select(self, table: str, filters: dict = None):
        try:
            query = f"SELECT * FROM {table}"
            params = []

            if filters:
                conditions = []
                for key, value in filters.items():
                    conditions.append(f"{key} = %s")
                    params.append(value)
                where_clause = " AND ".join(conditions)
                query += f" WHERE {where_clause}"

            cursor = self.connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()

            return result
        except Exception as e:
            print(f"Error selecting from {table}: {e}")
            return []

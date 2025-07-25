import os
from dotenv import load_dotenv
from postg.postg import DB

load_dotenv()

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

schema_users = """ 
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);"""

def main():
    db = DB(
        dbname=db_name,
        user=db_user,
        password=db_pass,
        host=db_host,
        port=db_port
    )
    db.connect()
    db.create_table(schema_users)

    select_users = db.select("users")
    print(select_users)


if __name__ == "__main__":
    main()
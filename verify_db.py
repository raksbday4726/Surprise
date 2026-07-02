import os

import pymysql
from dotenv import load_dotenv

load_dotenv()

host = os.environ.get('MYSQL_HOST', 'localhost')
port = int(os.environ.get('MYSQL_PORT', 3306))
user = os.environ.get('MYSQL_USER', 'root')
password = os.environ.get('MYSQL_PASSWORD', '')
db_name = os.environ.get('MYSQL_DATABASE', 'birthday_universe')

print(f"Attempting to connect to MySQL database '{db_name}' on {host}:{port} as user '{user}'...")

try:
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db_name,
    )
    print("------------------------------------------")
    print("🎉 SUCCESS! Database connection verified.")
    print("------------------------------------------")
    conn.close()
except Exception as e:
    print("------------------------------------------")
    print("❌ CONNECTION FAILED!")
    print(f"Error Details: {e}")
    print("------------------------------------------")
    print("\nPlease verify that:")
    print("1. Your MySQL server is running.")
    print("2. You have created the database 'birthday_universe'.")
    print("3. The credentials (MYSQL_USER, MYSQL_PASSWORD) in your .env file match your MySQL Server setup.")


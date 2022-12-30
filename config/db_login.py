import mysql.connector
from config import settings

db = mysql.connector.connect(
    host=settings.MYSQL_HOST,
    user=settings.MYSQL_USER,
    password=settings.MYSQL_PASSWORD,
    database=settings.MYSQL_DB,
    port=settings.MYSQL_PORT
)

db.autocommit = True
import mysql.connector
from config import settings

db = mysql.connector.connect(
    host=settings.MYSQL_ADDON_HOST,
    user=settings.MYSQL_ADDON_USER,
    password=settings.MYSQL_ADDON_PASSWORD,
    database=settings.MYSQL_ADDON_DB,
    port=settings.MYSQL_PORT,
)

db.autocommit = True
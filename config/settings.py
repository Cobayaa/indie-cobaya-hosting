from dotenv import load_dotenv
import os

load_dotenv() 

MYSQL_ADDON_HOST = os.environ.get('MYSQL_ADDON_HOST')
MYSQL_ADDON_USER = os.environ.get('MYSQL_ADDON_USER')
MYSQL_ADDON_PASSWORD = os.environ.get('MYSQL_ADDON_PASSWORD')
MYSQL_ADDON_DB = os.environ.get('MYSQL_ADDON_DB')
MYSQL_PORT = os.environ.get('MYSQL_PORT')


SMTP_EMAIL=os.environ.get('SMTP_EMAIL')
SMTP_PASSWORD=os.environ.get('SMTP_PASSWORD')

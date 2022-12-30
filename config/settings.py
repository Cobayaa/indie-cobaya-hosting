from dotenv import load_dotenv
import os

load_dotenv() 

MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_DB = os.environ.get('MYSQL_DB')
MYSQL_PORT = os.environ.get('MYSQL_PORT')


SMTP_EMAIL=os.environ.get('SMTP_EMAIL')
SMTP_PASSWORD=os.environ.get('SMTP_PASSWORD')

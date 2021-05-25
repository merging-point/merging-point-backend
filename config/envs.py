import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get(
    "SECRET_KEY", 't6p&4yojr&qu$8-@exk#(ptj9agmo6@+_1x5xjzs4_latwayhg')

DEBUG = os.environ.get("DEBUG", "true")

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "1234")
DB_NAME = os.environ.get("DB_NAME", "database")
X_NCP_APIGW_API_KEY_ID = os.envrion.get("X_NCP_APIGW_API_KEY_ID")
X_NCP_APIGW_API_KEY = os.environ.get("X_NCP_APIGW_API_KEY")
import os
from dotenv import load_dotenv

ENV = os.getenv("APP_ENV", "development")

if ENV == "production":
    load_dotenv(".env.production")
else:
    load_dotenv(".env.development")

DB_TYPE = os.getenv("DB_TYPE")

DB_PATH = os.getenv("DB_PATH")

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

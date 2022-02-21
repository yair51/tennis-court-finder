import os
from dotenv import load_dotenv
load_dotenv()
print("ran it")

class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dfal;dfkad adf")
    if os.getenv("APP_SETTINGS") == "Config":
        SQLALCHEMY_DATABASE_URI = "postgresql" + os.getenv("DATABASE_URL")[8:]
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class StagingConfig(Config):
    if os.getenv("APP_SETTINGS") == "StagingConfig":
        SQLALCHEMY_DATABASE_URI = "postgresql" + os.getenv("DATABASE_URL")[8:]

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    # using the uri, the url is just a filler
    #SQLALCHEMY_DATABASE_URI = os.getenv()
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///database.db")
    print(SQLALCHEMY_DATABASE_URI)
    print('hello')
    FLASK_APP = "main.py"
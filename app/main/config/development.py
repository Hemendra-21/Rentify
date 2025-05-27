import os 
from .api_config import ApiConfig

class DevelopmentConfig(ApiConfig):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

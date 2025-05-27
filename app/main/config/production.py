import os
from .api_config import ApiConfig

class ProductionConfig(ApiConfig):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "prod-secret-key")

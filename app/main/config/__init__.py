# loads config based on FLASK_ENV 

import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("FLASK_ENV", "development").lower()

if env == "production":
    from .production import ProductionConfig as Config
elif env == "testing":
    from .testing import TestingConfig as Config
else:
    from .development import DevelopmentConfig as Config

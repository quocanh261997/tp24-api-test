import os
from typing import List

from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()


# Configuration variables
class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.api_key: str = os.getenv("API_KEY")
        self.database_url: str = os.getenv("DATABASE_URL")
        self.allowed_origins: List[str] = os.getenv("ALLOWED_ORIGINS").split(",")
        self.api_prefix: str = os.getenv("API_PREFIX")


config_instance = Config()

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_ENV: str = os.getenv("APP_ENV", "development")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REPORT_SAVE_PATH: str = os.getenv("REPORT_SAVE_PATH", "./reports")
    ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/tiff"]

settings = Settings()
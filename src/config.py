import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SENTRY_DSN = os.getenv("SENTRY_DSN")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    FS_STORE_DIR_PATH = os.getenv("FS_STORE_DIR_PATH", "../data")

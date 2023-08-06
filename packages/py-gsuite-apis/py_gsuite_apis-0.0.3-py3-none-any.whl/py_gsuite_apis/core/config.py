import logging
import os
from functools import lru_cache

from pydantic import BaseSettings


logger = logging.getLogger("uvicorn")


class SettingsFromEnv(BaseSettings):
    class Config:
        env_file = ".env"


class GoogleApiSettings(BaseSettings):
    SCOPE: str
    BUILD: str
    VERSION: str


class GoogleSettings(SettingsFromEnv):
    GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_FILENAME: str = os.getenv(
        "GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_FILENAME",
        "google-service-account-credentials.json"
        # None,
    )
    GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_FILEPATH: str = os.getenv(
        "GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_FILEPATH", None,
    )
    SLIDES: GoogleApiSettings = GoogleApiSettings(
        SCOPE="https://www.googleapis.com/auth/presentations", BUILD="slides", VERSION="v1",
    )
    DRIVE: GoogleApiSettings = GoogleApiSettings(
        SCOPE="https://www.googleapis.com/auth/drive", BUILD="drive", VERSION="v3",
    )
    SHEETS: GoogleApiSettings = GoogleApiSettings(
        SCOPE="https://www.googleapis.com/auth/spreadsheets", BUILD="sheets", VERSION="v4",
    )


class Settings(GoogleSettings):
    pass


@lru_cache()
def get_config() -> BaseSettings:
    logger.info("Loading config settings from the environment...")
    return Settings()


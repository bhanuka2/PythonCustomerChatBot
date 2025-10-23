import os

from pydantic.v1 import BaseSettings


class settings(BaseSettings):

    DATABASE_URL : str
    OPENAPI_KEY : str

def get_settings() -> settings:
    return settings()

settings = get_settings()
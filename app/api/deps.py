import os

from dotenv import load_dotenv
from fastapi import Request, HTTPException, Header
from typing_extensions import Annotated

from app.core.config import config_instance

load_dotenv()


# Dependency to extract the DB session
def get_db(request: Request):
    return request.state.db


# Dependency to verify the API key
def get_api_key(x_api_key: Annotated[str, Header()] = None):
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="API Key is missing")
    elif x_api_key != config_instance.api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

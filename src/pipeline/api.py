import logging
import os
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.pipeline.models import CanineObservation

app = FastAPI(title="EthoPipe API")
security = HTTPBasic()
logger = logging.getLogger(__name__)


@app.middleware("http")
async def add_security_headers(request: Request, call_next) -> Response:
    """Enforce defense-in-depth HTTP security response headers."""
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "0"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    return response


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    expected_username = os.getenv("API_USERNAME")
    expected_password = os.getenv("API_PASSWORD")

    if not expected_username or not expected_password:
        logger.error("Authentication credentials are not configured on the server")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = expected_username.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = expected_password.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/")
def read_root() -> dict:
    return {"message": "EthoPipe API is running"}


@app.post("/ingest")
def ingest_incident(
    data: CanineObservation,
    username: Annotated[str, Depends(get_current_username)],
) -> dict:
    return {
        "status": "valid",
        "incident": data.model_dump(by_alias=True),
    }

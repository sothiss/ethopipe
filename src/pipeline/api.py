import logging
import os
import secrets
from typing import Annotated, Any

import sentry_sdk
import sentry_sdk.ai
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

from src.pipeline.agent import run_ethopipe_agent
from src.pipeline.models import CanineObservation

# Initialize Sentry with Agent Tracing, Full Tracing, and Prompt PII capture
SENTRY_DSN = os.getenv(
    "SENTRY_DSN",
    "https://90d85028235d5b5f06f950aa8a641af4@o4511706250084352.ingest.us.sentry.io/4512046640136192",
)

sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=1.0,
    send_default_pii=True,
    environment=os.getenv("SENTRY_ENVIRONMENT", "production"),
)

app = FastAPI(title="EthoPipe API")
security = HTTPBasic()
logger = logging.getLogger(__name__)


@app.middleware("http")
async def conversation_tracking_middleware(request: Request, call_next) -> Response:
    """Extracts X-Conversation-ID header to group requests in Conversations."""
    conv_id = request.headers.get("X-Conversation-ID")
    if conv_id:
        sentry_sdk.ai.set_conversation_id(conv_id)
    return await call_next(request)


@app.middleware("http")
async def add_security_headers(request: Request, call_next) -> Response:
    """Security middleware adding defense-in-depth headers to responses."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; frame-ancestors 'none'"
    )
    response.headers["Referrer-Policy"] = "no-referrer"
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
    # Set user context in Sentry
    sentry_sdk.set_user({"username": credentials.username})
    return credentials.username


class AgentRunRequest(BaseModel):
    prompt: str
    incident_data: dict[str, Any] | None = None
    conversation_id: str | None = None


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


@app.post("/agent/run")
def run_agent(
    payload: AgentRunRequest,
    username: Annotated[str, Depends(get_current_username)],
) -> dict:
    """Executes agent run with Sentry Agent Tracing and conversation tracking."""
    return run_ethopipe_agent(
        prompt=payload.prompt,
        incident_data=payload.incident_data,
        conversation_id=payload.conversation_id,
        user_id=username,
    )


@app.get("/debug-sentry")
def trigger_sentry_test_error(
    username: Annotated[str, Depends(get_current_username)],
    message: str = "verification-test",
):
    """Deliberate endpoint for verifying real end-to-end Sentry error ingestion."""
    raise RuntimeError(f"Deliberate Sentry test error: {message}")

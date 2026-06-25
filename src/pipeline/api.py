from fastapi import FastAPI

from src.pipeline.models import EthologicalIncident

app = FastAPI(title="EthoPipe API")


@app.get("/")
def read_root() -> dict:
    return {"message": "EthoPipe API is running"}


@app.post("/ingest")
def ingest_incident(data: EthologicalIncident) -> dict:
    return {
        "status": "valid",
        "incident": data.model_dump(),
    }
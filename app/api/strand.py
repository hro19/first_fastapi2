"""API endpoints for interacting with a basic Strand agent."""

from functools import lru_cache

from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel

router = APIRouter()

try:  # Attempt to import the SDK; allow API to load even if missing.
    from strands import Agent
except ImportError as import_error:  # pragma: no cover - environment dependent
    Agent = None  # type: ignore[assignment]
    _import_error = import_error
else:
    _import_error = None


class AgentRequest(BaseModel):
    """Request payload for the Strand agent."""

    prompt: str = "Tell me about agentic AI"


class AgentResponse(BaseModel):
    """Response returned by the Strand agent endpoint."""

    answer: str


@lru_cache(maxsize=1)
def _get_agent() -> "Agent":
    """Return a cached Agent instance, raising if the SDK is unavailable."""

    if Agent is None:
        raise RuntimeError(
            "The 'strands' package is not installed. Install it to use this endpoint."
        ) from _import_error
    return Agent()


@router.post("/strand/basic", response_model=AgentResponse)
async def run_basic_agent(request: AgentRequest) -> AgentResponse:
    """Execute the basic Strand agent with the provided prompt."""

    try:
        basic_agent = _get_agent()
        answer = await run_in_threadpool(basic_agent, request.prompt)
    except Exception as exc:  # pragma: no cover - defensive against runtime errors
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return AgentResponse(answer=answer)

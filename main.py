"""Production entry point for the education data agent."""

import uuid
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.api.routers.query_router import query_router
from app.core.context import set_req_id
from app.core.lifespan import lifespan


app = FastAPI(
    title="教育数据智能问数 Agent",
    version="0.1.0",
    description="通过自然语言查询教育经营与教学指标的只读问数服务。",
    lifespan=lifespan,
)
app.include_router(query_router)


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "education-data-agent"}


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    set_req_id(request_id)
    response = await call_next(request)
    response.headers["X-Request-Id"] = request_id
    return response


# Keep this catch-all mount after the API routes so ``/health`` and ``/api``
# continue to be handled by FastAPI when a production frontend build exists.
frontend_dist = Path(__file__).resolve().parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)

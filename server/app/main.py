import asyncio

import redis
from fastapi import FastAPI, Request

from app.models import NodeStats, StakerStats
from app.settings import settings
from app.utils import fetch_subgraph_data

app = FastAPI()
cache = redis.Redis(host="redis", port=settings.redis_port)

# Global state for reusable services
app.state.cache = cache


@app.get("/api/v1/status", status_code=200)
async def get_status():
    return


@app.get("/v1/node/stats", status_code=200, response_model=NodeStats)
async def get_node_stats(req: Request):
    cache = req.app.state.cache
    return NodeStats()


@app.get("/v1/staker/stats", status_code=200, response_model=StakerStats)
async def get_staker_stats(req: Request):
    cache = req.app.state.cache
    return StakerStats()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(fetch_subgraph_data(settings.subgraph_sleep_sec))

import asyncio
import logging
import pickle

import redis
from fastapi import FastAPI, Request

from app.models import NodeStats, StakerStats
from app.settings import settings
from app.utils import fetch_subgraph_data

app = FastAPI()
cache = redis.Redis(host="redis", port=settings.redis_port)
logging.basicConfig(level=logging.INFO)

# Global state for reusable services
app.state.cache = cache


@app.get("/v1/status", status_code=200)
async def get_status():
    return


@app.get("/v1/node/stats", status_code=200, response_model=NodeStats)
async def get_node_stats(req: Request):
    stats = req.app.state.cache.get(settings.redis_node_stats_key)
    stats = pickle.loads(stats)
    return NodeStats(**stats)


@app.get("/v1/staker/stats", status_code=200, response_model=StakerStats)
async def get_staker_stats(req: Request):
    stats = req.app.state.cache.get(settings.redis_staker_stats_key)
    stats = pickle.loads(stats)
    return StakerStats(**stats)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(fetch_subgraph_data(cache, settings.subgraph_sleep_sec))

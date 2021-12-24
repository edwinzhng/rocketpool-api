import asyncio
import logging
import pickle
from typing import Dict

from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from humps import decamelize
from redis import Redis

from app.queries import latest_stats_query, staker_balance_query
from app.settings import settings

SUBGRAPH_BASE_URL = "https://gateway.thegraph.com/api"
SUBGRAPH_API_URL = "subgraphs/id/0xa508c16666c5b8981fa46eb32784fccc01942a71-3"


async def fetch_subgraph_data(cache: Redis, sleep_sec: int):
    """Updates Redis cache with new subgraph data if available"""
    url = f"{SUBGRAPH_BASE_URL}/{settings.subgraph_api_key}/{SUBGRAPH_API_URL}"
    transport = AIOHTTPTransport(
        url=url, headers={"Content-type": "application/json",},
    )

    while True:
        async with Client(
            transport=transport, fetch_schema_from_transport=False,
        ) as session:
            try:
                data = await session.execute(latest_stats_query)
                data = data["rocketPoolProtocols"][0]
                node_stats = data["lastNetworkNodeBalanceCheckPoint"]
                staker_stats = data["lastNetworkStakerBalanceCheckPoint"]

                reth_apy = await _compute_reth_apy(session, staker_stats)
                staker_stats["rethApy"] = reth_apy
                node_stats = _transform_stats(node_stats)
                staker_stats = _transform_stats(staker_stats)

                # Save stats to Redis
                if node_stats and staker_stats:
                    cache.set(settings.redis_node_stats_key, node_stats)
                    cache.set(settings.redis_staker_stats_key, staker_stats)
            except Exception as e:
                logging.info(e)

        await asyncio.sleep(sleep_sec)


async def _compute_reth_apy(session, latest_staker_stats):
    num_lookback_checkpoints = 2
    last_staker_checkpoint_id = latest_staker_stats["previousCheckpointId"]

    for _ in range(num_lookback_checkpoints):
        prev_data = await session.execute(
            staker_balance_query,
            variable_values={"checkpointId": last_staker_checkpoint_id},
        )
        prev_stats = prev_data["networkStakerBalanceCheckpoint"]
        last_staker_checkpoint_id = prev_stats["previousCheckpointId"]

    # Calculate time period
    block_time_diff = int(latest_staker_stats["blockTime"]) - int(
        prev_stats["blockTime"]
    )
    seconds_per_year = 365 * 24 * 60 * 60
    compounding_periods = seconds_per_year / block_time_diff

    # Compute APY
    current_rate = float(latest_staker_stats["rETHExchangeRate"])
    prev_rate = float(prev_stats["rETHExchangeRate"])
    reth_yield = current_rate / prev_rate
    apy = 100 * ((reth_yield ** compounding_periods) - 1)
    return apy


def _transform_stats(stats: Dict):
    """Transform all stat keys to match the API response models"""
    new_stats = {}
    for key in stats.keys():
        new_key = _key_to_snake_case(key)
        new_stats[new_key] = stats[key]
    return pickle.dumps(new_stats)


def _key_to_snake_case(key: str):
    """Transform key to snake case with abbreviations"""
    if key.startswith("rETH"):
        key = "reth" + key[4:]
    key = key.replace("RETH", "Reth")
    key = key.replace("RPL", "Rpl")
    key = key.replace("ETH", "Eth")
    key = key.replace("ODAO", "Odao")
    return decamelize(key)

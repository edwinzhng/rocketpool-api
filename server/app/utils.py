import asyncio

import aiohttp


async def fetch_subgraph_data(sleep_sec):
    """Updates Redis cache with new subgraph data if available"""
    while True:
        
        await asyncio.sleep(sleep_sec)

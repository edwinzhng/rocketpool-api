import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    redis_port: int = os.environ.get("REDIS_PORT")
    subgraph_api_key: str = os.environ.get("SUBGRAPH_API_KEY")
    subgraph_sleep_sec: int = os.environ.get("SUBGRAPH_UPDATE_SLEEP_SEC")
    redis_node_stats_key: str = "RP_NODE_STATS"
    redis_staker_stats_key: str = "RP_STAKER_STATS"


settings = Settings()

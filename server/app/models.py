from humps import camelize
from pydantic import BaseModel, Field


def to_camel_case(field: str):
    return camelize(field)


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel_case
        allow_population_by_field_name = True


class NodeStats(CamelModel):
    nodes_registered: int
    oracle_nodes_registered: int
    rpl_staked: int
    effective_rpl_staked: int
    minimum_effective_rpl: int
    maximum_effective_rpl: int
    minimum_effective_rpl_new_minipool: int
    maximum_effective_rpl_new_minipool: int
    total_rpl_slashed: int
    total_odao_rewards_claimed: int
    total_node_rewards_claimed: int
    average_total_odao_rewards_claimed: int
    average_odao_reward_claim: int
    average_node_total_rewards_claimed: int
    average_node_reward_claim: int
    rpl_price_in_eth: int
    average_rpl_price_in_eth: int
    queued_minipools: int
    staking_minipools: int
    staking_unbonded_minipools: int
    withdrawable_minipools: int
    total_finalized_minipools: int
    average_fee_for_active_minipools: int
    new_minipool_fee: int
    block: int
    block_time: int


class StakerStats(CamelModel):
    staker_eth_actively_staking: int
    staker_eth_waiting_in_deposit_pool: int
    staker_eth_in_rocket_eth_contract: int
    staker_eth_in_protocol: int
    total_staker_eth_rewards: int
    total_stakers_with_eth_rewards: int
    average_staker_eth_rewards: int
    stakers_with_an_reth_balance: int
    total_reth_supply: int
    reth_exchange_rate: int
    reth_apy: float = Field(
        description="Average rETH APY in percent, based on the last 3 subgraph checkpoints"
    )
    block: int
    block_time: int

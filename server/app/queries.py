from gql import gql

latest_stats_query = gql(
    """
    query protocolMetrics {
        rocketPoolProtocols {
            lastNetworkNodeBalanceCheckPoint {
                previousCheckpointId
                nodesRegistered
                oracleNodesRegistered
                rplStaked
                effectiveRPLStaked
                minimumEffectiveRPL
                maximumEffectiveRPL
                minimumEffectiveRPLNewMinipool
                maximumEffectiveRPLNewMinipool
                totalRPLSlashed
                totalODAORewardsClaimed
                totalNodeRewardsClaimed
                averageTotalODAORewardsClaimed
                averageODAORewardClaim
                averageNodeTotalRewardsClaimed
                averageNodeRewardClaim
                rplPriceInETH
                averageRplPriceInETH
                queuedMinipools
                stakingMinipools
                stakingUnbondedMinipools
                withdrawableMinipools
                totalFinalizedMinipools
                averageFeeForActiveMinipools
                newMinipoolFee
                block
                blockTime
            }
            lastNetworkStakerBalanceCheckPoint {
                previousCheckpointId
                stakerETHActivelyStaking
                stakerETHWaitingInDepositPool
                stakerETHInRocketETHContract
                stakerETHInProtocol
                totalStakerETHRewards
                totalStakersWithETHRewards
                averageStakerETHRewards
                stakersWithAnRETHBalance
                totalRETHSupply
                rETHExchangeRate
                block
                blockTime
            }
        }
    }
    """
)

staker_balance_query = gql(
    """
    query stakerBalance($checkpointId: ID!) {
        networkStakerBalanceCheckpoint(id: $checkpointId) {
            id
            previousCheckpointId
            rETHExchangeRate
            blockTime
        }
    }
    """
)

import random

simulations = []

count = 10
win_rate = 0.62
risk_reward = 5
balance_limit = 1000000
start_balance = 1000
stop_distance = 0.005
liquidity_limit = 5000000

def run_simulation():
    balance = start_balance
    equity_curve = []
    last_trade_winner = False
    while balance < balance_limit:
        num = random.randrange(1, 100)
        risk = 0.1
        # if the last trade was a winner we'll risk more of our account balance to compound returns aggressively
        if last_trade_winner is True:
            risk = 0.25
        # check the $ risk would not exceed the realistic liquidity of the market
        dollar_risk = risk * balance
        position_size = dollar_risk / 0.005
        if position_size > liquidity_limit:
            dollar_risk = liquidity_limit * 0.005
        if num < (win_rate * 100):
            # winning trade
            balance = round(balance + (risk_reward * dollar_risk))
            last_trade_winner = True
        else:
            # losing trade
            balance = round(balance - dollar_risk)
            last_trade_winner = False
        equity_curve.append(balance)
    return equity_curve

def build_stats(simulations):
    stats = []
    for sim in simulations:
        trades = len(sim)
        months = trades / 8
        stats.append({
            'trades': trades,
            'months': months
        })
    return stats

def run():
    for i in range(0, count):
        simulations.append(run_simulation())
    # TODO - measure the risk adjusted returns of each equity curve, and analyse the variance
    stats = build_stats(simulations)
    print(stats)

run()

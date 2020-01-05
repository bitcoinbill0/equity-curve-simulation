import random
import statistics
import numpy as np
import pandas as pd
import pprint
import matplotlib.pyplot as plt
import numpy as np

pp = pprint.PrettyPrinter(indent=4)

simulations = []

count = 10
win_rate = 0.5
risk_reward = 3
balance_limit = 1000000
start_balance = 1000
stop_distance = 0.005
liquidity_limit = 5000000
normal_risk = 0.1
increased_risk = 0.25
trades_per_week = 2

def run_simulation():
    balance = start_balance
    equity_curve = [start_balance]
    last_trade_winner = False
    while balance < balance_limit:
        num = random.randrange(1, 100)
        risk = normal_risk
        # if the last trade was a winner we'll risk more of our account balance to compound returns aggressively
        if last_trade_winner is True:
            risk = increased_risk
        # check the $ risk would not exceed the realistic liquidity of the market
        dollar_risk = risk * balance
        position_size = dollar_risk / stop_distance
        if position_size > liquidity_limit:
            dollar_risk = liquidity_limit * stop_distance
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
        months = trades / trades_per_week / 4
        sharpe_ratio = round((sim[-1] - start_balance) / np.std(sim), 1)
        stats.append({
            'trades': trades,
            'months': months,
            'sharpe_ratio': sharpe_ratio,
            'equity_curve': sim
        })
    return stats

def run():
    for i in range(0, count):
        simulations.append(run_simulation())

    stats = build_stats(simulations)

    sharpe_ratios = list(map(lambda x: x['sharpe_ratio'], stats))
    trades = list(map(lambda x: x['trades'], stats))

    sharpe_ratio_mean = round(statistics.mean(sharpe_ratios), 1)
    sharpe_ratio_stdev = round(np.std(sharpe_ratios), 1)
    sharpe_ratio_min = round(min(sharpe_ratios), 1)
    sharpe_ratio_max = round(max(sharpe_ratios), 1)

    trades_mean = round(statistics.mean(trades), 1)
    trades_stdev = round(np.std(trades), 1)
    trades_min = round(min(trades), 1)
    trades_max = round(max(trades), 1)

    pp.pprint({
        'sharpe_ratio_mean': sharpe_ratio_mean,
        'sharpe_ratio_stdev': sharpe_ratio_stdev,
        'sharpe_ratio_min': sharpe_ratio_min,
        'sharpe_ratio_max': sharpe_ratio_max,
        'trades_mean': trades_mean,
        'trades_stdev': trades_stdev,
        'trades_min': trades_min,
        'trades_max': trades_max
    })

    n = 0
    for item in stats:
        plt.plot(item['equity_curve'])
        plt.savefig('plots/plot' + str(n) + '.png')
        n = n + 1

run()

simulations = []

count = 10
win_rate = 0.62
risk_reward = 5
balance_limit = 1000000
start_balance = 1000

def run_simulation():
    balance = start_balance
    equity_curve = []
    while balance < balance_limit:
        # TODO - use random number generator to simulate trading outcome
        balance = balance_limit
    return equity_curve

def run():
    for i in range(0, count):
        simulations.append(run_simulation())

run()

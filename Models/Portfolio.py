from .Position import Position
import numpy as np
import plotly.graph_objs as go

class Portfolio:

    def __init__(self):
        self.portfolio = []
        self.bigger_strike = 0

    # Add a new position in the portfolio
    def add_position(self, quantity, direction, option_type, strike, spot, volatility, time_to_maturity, riskfree):
        self.bigger_strike = max(self.bigger_strike, strike)
        position = Position(quantity, direction, option_type, strike, spot, volatility, time_to_maturity, riskfree)
        self.portfolio.append(position)

    # Empty portfolio
    def reset_portfolio(self):
        self.portfolio = []

    # Portfolio payoff graph
    def compute_pnl(self):
        S = np.linspace(1, 2 * max(100, self.bigger_strike), 500)
        total_payoff = np.zeros_like(S)

        traces = []
        for curr_position in self.portfolio:
            payoff = curr_position.get_payoffs(S)
            total_payoff += payoff
            traces.append(go.Scatter(x=S, y=payoff, mode='lines', line=dict(width=1), name=f'{curr_position.direction} {curr_position.option_type} K={curr_position.option.strike}'))

        traces.append(go.Scatter(x=S, y=total_payoff, mode='lines', name="Total", line=dict(width=4, color="black")))
        return traces
    
    def compute_prices_at_date(self, curr_time_to_maturity):
        S = np.linspace(1, 2 * max(100, self.bigger_strike), 500)
        total_prices = np.zeros_like(S)

        traces = []
        for curr_position in self.portfolio:
            prices = curr_position.get_prices_at_date(curr_time_to_maturity, S)
            total_prices += prices
            
        traces.append(go.Scatter(x=S, y=total_prices, mode='lines', name="Total", line=dict(width=4, color="black")))
        return traces

    # Portfolio description
    def get_portfolio_positions(self):
        return [f"{curr_position.direction} {curr_position.option_type} | Strike={curr_position.option.strike} | Initial price={round(curr_position.option.compute_initial_price(), 2)} | Q={curr_position.quantity}" 
            for curr_position in self.portfolio]
    
    def get_greeks_data(self):
        greeks_data = {
            "delta": 0,
            "gamma": 0,
            "theta": 0,
            "vega": 0,
            "rho": 0
        }
        for curr_position in self.portfolio:
            curr_greeks = curr_position.get_greeks()
            for greek in greeks_data.keys():
                greeks_data[greek] += float(curr_greeks[greek])
        return [greeks_data]
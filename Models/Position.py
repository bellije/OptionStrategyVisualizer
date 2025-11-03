from .OptionFactory import option_factory

class Position:
    # TODO: switch to Long and Short types
    direction_sign = {"Long": 1, "Short": -1}

    def __init__(self, quantity, direction, option_type, strike, spot, volatility, time_to_maturity, risk_free_rate):
        self.quantity = quantity
        self.direction = direction
        self.option_type = option_type
        self.option = option_factory(option_type, strike, spot, volatility, time_to_maturity, risk_free_rate)

    def get_pnl_at_date(self, time_to_maturity, prices):
        option_prices = []
        for curr_price in prices:
            option_prices.append(self.direction_sign[self.direction] * self.quantity * self.option.compute_pnl_at_date(time_to_maturity, curr_price))
        return option_prices
    
    def get_payoffs(self, prices):
        return self.direction_sign[self.direction] * self.quantity * self.option.compute_payoffs(prices)
    
    def get_greeks(self):
        return {
            "delta": self.direction_sign[self.direction] * self.quantity * self.option.compute_delta(),
            "gamma": self.direction_sign[self.direction] * self.quantity * self.option.compute_gamma(),
            "theta": self.direction_sign[self.direction] * self.quantity * self.option.compute_theta(),
            "vega": self.direction_sign[self.direction] * self.quantity * self.option.compute_vega(),
            "rho": self.direction_sign[self.direction] * self.quantity * self.option.compute_rho()
        }
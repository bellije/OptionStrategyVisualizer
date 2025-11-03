from math import sqrt
from scipy.stats import norm

class Option:

    def __init__(self, strike, spot, time_to_maturity, volatility, risk_free):
        self.strike = strike 
        self.spot = spot 
        self.time_to_maturity = time_to_maturity 
        self.volatility = volatility 
        self.risk_free = risk_free

    # Prices computations

    def compute_initial_price(self):
        raise NotImplementedError
    
    def compute_current_price(self, curr_time_to_maturity, curr_price):
        raise NotImplementedError
    
    def compute_pnl_at_date(self, curr_time_to_maturity, curr_price):
        raise NotImplementedError
    
    def compute_payoffs(self, prices):
        raise NotImplementedError
    
    # Greeks computations

    def compute_delta(self):
        raise NotImplementedError
    
    def compute_gamma(self):
        return (1/(self.spot * self.volatility * sqrt(self.time_to_maturity))) * norm.pdf(self.d1())
    
    def compute_theta(self):
        raise NotImplementedError
    
    def compute_vega(self):
        return 0.01 * self.spot * sqrt(self.time_to_maturity) * norm.pdf(self.d1())

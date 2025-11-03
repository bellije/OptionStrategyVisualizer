from .Option import Option
from math import sqrt, log, exp
from scipy.stats import norm
import numpy as np

class Call(Option):

    # Usefull functions

    def d1(self, curr_time_to_maturity=None, curr_price = None):
        if curr_time_to_maturity == None:
            curr_time_to_maturity = self.time_to_maturity
        if curr_price == None:
            curr_price = self.spot
        return (log(curr_price/self.strike) + (self.risk_free + 0.5 * self.volatility**2) * curr_time_to_maturity) / (self.volatility * sqrt(curr_time_to_maturity))

    def d2(self, curr_time_to_maturity = None, curr_price = None):
        if curr_time_to_maturity == None:
            curr_time_to_maturity = self.time_to_maturity
        if curr_price == None:
            curr_price = self.spot
        return self.d1(curr_time_to_maturity, curr_price) - self.volatility * sqrt(curr_time_to_maturity)

    # Initialization

    def __init__(self, strike, spot, time_to_maturity, volatility, risk_free):
        super().__init__(strike, spot, time_to_maturity, volatility, risk_free)

    # Prices computations
        
    def compute_initial_price(self):
        return self.spot * norm.cdf(self.d1()) - self.strike * exp(-self.risk_free * self.time_to_maturity) * norm.cdf(self.d2())
    
    def compute_current_price(self, curr_time_to_maturity, curr_price):
        return curr_price * norm.cdf(self.d1(curr_time_to_maturity, curr_price)) - self.strike * exp(-self.risk_free * curr_time_to_maturity) * norm.cdf(self.d2(curr_time_to_maturity, curr_price))
    
    def compute_pnl_at_date(self, curr_time_to_maturity, curr_price):
        return self.compute_current_price(curr_time_to_maturity, curr_price) - self.compute_initial_price()
    
    def compute_payoffs(self, prices):
        return np.maximum(prices - self.strike, 0) - self.compute_initial_price()

    # Greeks computation
    
    def compute_delta(self):
        return norm.cdf(self.d1())
    
    def compute_gamma(self):
        return super().compute_gamma()
    
    def compute_theta(self):
        a = ((self.spot * self.volatility)/(2 * sqrt(self.time_to_maturity))) * norm.pdf(self.d1())
        b = self.risk_free * self.strike * exp(- self.risk_free * self.time_to_maturity) * norm.cdf(self.d2())
        return (-a - b)/365
    
    def compute_vega(self):
        return super().compute_vega()
    
    def compute_rho(self):
        return 0.01 * self.strike * self.time_to_maturity * exp(- self.risk_free * self.time_to_maturity) * norm.cdf(self.d2())
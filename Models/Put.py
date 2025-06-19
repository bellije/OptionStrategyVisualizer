from .Option import Option
from math import sqrt, log, exp
from scipy.stats import norm
import numpy as np

class Put(Option):

    @property
    def d1(self):
        return (log(self.spot/self.strike) + (self.risk_free + 0.5 * self.volatility**2) * self.time_to_maturity) / (self.volatility * sqrt(self.time_to_maturity))

    @property
    def d2(self):
        return self.d1 - self.volatility * sqrt(self.time_to_maturity)

    def __init__(self, strike, spot, time_to_maturity, volatility, risk_free):
        super().__init__(strike, spot, time_to_maturity, volatility, risk_free)
        
    def compute_price(self):
        return self.strike * exp(-self.risk_free * self.time_to_maturity) * norm.cdf(- self.d2) - self.spot * norm.cdf(-self.d1)

    def compute_delta(self):
        return norm.cdf(self.d1) - 1
    
    def compute_gamma(self):
        return super().compute_gamma()
    
    def compute_theta(self):
        a = ((self.spot * self.volatility)/(2 * sqrt(self.time_to_maturity))) * norm.pdf(self.d1)
        b = self.risk_free * self.strike * exp(- self.risk_free * self.time_to_maturity) * norm.cdf(-self.d2)
        return (-a + b)/365
    
    def compute_vega(self):
        return super().compute_vega()
    
    def compute_rho(self):
        return -0.01 * self.strike * self.time_to_maturity * exp(- self.risk_free * self.time_to_maturity) * norm.cdf(- self.d2)
    
    def compute_payoffs(self, prices):
        return np.maximum(self.strike - prices, 0) - self.compute_price()
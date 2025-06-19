from .Option import Option
from .Call import Call
from .Put import Put

def option_factory(option_type, strike, spot, volatility, time_to_maturity, risk_free_rate) -> Option:
    if option_type == "Call":
        return Call(strike, spot, time_to_maturity, volatility, risk_free_rate)
    elif option_type == "Put":
        return Put(strike, spot, time_to_maturity, volatility, risk_free_rate)
    else:
        raise Exception("Not a valid option type")
from Models.Portfolio import Portfolio
from Models.Call import Call
from Models.Put import Put
import pytest

class TestPortfolio:

    @pytest.fixture(autouse=True)
    def setup(self):

        self.portfolio = Portfolio()
        self.portfolio.add_position(1, "Long", "Call", 100, 100, 0.1, 1, 0.05)
        self.portfolio.add_position(2, "Long", "Put", 100, 100, 0.1, 1, 0.05)

        yield

    def test_add_position(self):
        self.portfolio.add_position(1, "Short", "Call", 120, 100, 0.1, 1, 0.05)

        assert (len(self.portfolio.portfolio) == 3)
        assert (self.portfolio.bigger_strike == 120)
        assert (type(self.portfolio.portfolio[0].option) == Call)
        assert (self.portfolio.portfolio[0].quantity == 1)
        assert (self.portfolio.portfolio[0].direction == "Long")
        assert (self.portfolio.portfolio[0].option_type == "Call")
        assert (type(self.portfolio.portfolio[1].option) == Put)
        assert (self.portfolio.portfolio[1].quantity == 2)
        assert (self.portfolio.portfolio[1].direction == "Long")
        assert (self.portfolio.portfolio[1].option_type == "Put")
        assert (type(self.portfolio.portfolio[2].option) == Call)
        assert (self.portfolio.portfolio[2].quantity == 1)
        assert (self.portfolio.portfolio[2].direction == "Short")
        assert (self.portfolio.portfolio[2].option_type == "Call")


    def test_reset_portfolio(self):
        self.portfolio.reset_portfolio()

        assert(len(self.portfolio.portfolio) == 0)


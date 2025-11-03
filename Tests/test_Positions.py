import pytest
import numpy as np
from Models.Position import Position

class TestPosition:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.position_long_call = Position(1, "Long", "Call", 100, 100, 0.1, 1, 0.05)
        self.double_position_long_call = Position(2, "Long", "Call", 100, 100, 0.1, 1, 0.05)
        self.position_short_call = Position(1, "Short", "Call", 100, 100, 0.1, 1, 0.05)
        self.double_position_short_call = Position(2, "Short", "Call", 100, 100, 0.1, 1, 0.05)
        self.position_long_put = Position(1, "Long", "Put", 100, 100, 0.1, 1, 0.05)
        self.double_position_long_put = Position(2, "Long", "Put", 100, 100, 0.1, 1, 0.05)
        self.position_short_put = Position(1, "Short", "Put", 100, 100, 0.1, 1, 0.05)
        self.double_position_short_put = Position(2, "Short", "Put", 100, 100, 0.1, 1, 0.05)
        yield

    def test_get_prices_at_date(self):
        S = np.array([90, 100, 110])

        # We compute for each position
        prices_long_call = self.position_long_call.get_pnl_at_date(300/365, S)
        prices_double_long_call = self.double_position_long_call.get_pnl_at_date(300/365, S)
        prices_short_call = self.position_short_call.get_pnl_at_date(300/365, S)
        prices_double_short_call = self.double_position_short_call.get_pnl_at_date(300/365, S)
        prices_long_put = self.position_long_put.get_pnl_at_date(300/365, S)
        prices_double_long_put = self.double_position_long_put.get_pnl_at_date(300/365, S)
        prices_short_put = self.position_short_put.get_pnl_at_date(300/365, S)
        prices_double_short_put = self.double_position_short_put.get_pnl_at_date(300/365, S)

        # We compare to the results (results - ((th. price - init. price)))
        assert np.all(abs(prices_long_call - (np.array([1.185232, 5.913492, 14.29624]) - 6.804963)) < 1e-4)
        assert np.all(abs(prices_double_long_call - 2*(np.array([1.185232, 5.913492, 14.29624]) - 6.804963)) < 1e-4)
        assert np.all(abs(prices_short_call - (np.array([-1.185232, -5.913492, -14.29624]) + 6.804963)) < 1e-4)
        assert np.all(abs(prices_double_short_call - 2*(np.array([-1.185232, -5.913492, -14.29624]) + 6.804963)) < 1e-4)
        assert np.all(abs(prices_long_put - (np.array([7.158942, 1.887202, 0.26995]) - 1.927905)) < 1e-4)
        assert np.all(abs(prices_double_long_put - 2*(np.array([7.158942, 1.887202, 0.26995]) - 1.927905)) < 1e-4)
        assert np.all(abs(prices_short_put - (np.array([-7.158942, -1.887202, -0.26995]) + 1.927905)) < 1e-4)
        assert np.all(abs(prices_double_short_put - 2*(np.array([-7.158942, -1.887202, -0.26995]) + 1.927905)) < 1e-4)
    
    def test_get_payoffs(self):
        S = np.array([90, 100, 110])

        # We compute for each position
        payoffs_long_call = self.position_long_call.get_payoffs(S)
        payoffs_double_long_call = self.double_position_long_call.get_payoffs(S)
        payoffs_short_call = self.position_short_call.get_payoffs(S)
        payoffs_double_short_call = self.double_position_short_call.get_payoffs(S)
        payoffs_long_put = self.position_long_put.get_payoffs(S)
        payoffs_double_long_put = self.double_position_long_put.get_payoffs(S)
        payoffs_short_put = self.position_short_put.get_payoffs(S)
        payoffs_double_short_put = self.double_position_short_put.get_payoffs(S)

        # We compare to the results (results - ((th. price - init. price)))
        assert np.all(abs(payoffs_long_call - (np.array([0, 0, 10]) - 6.804963)) < 1e-4)
        assert np.all(abs(payoffs_double_long_call - 2*(np.array([0, 0, 10]) - 6.804963)) < 1e-4)
        assert np.all(abs(payoffs_short_call - (np.array([0, 0, -10]) + 6.804963)) < 1e-4)
        assert np.all(abs(payoffs_double_short_call - 2*(np.array([0, 0, -10]) + 6.804963)) < 1e-4)
        assert np.all(abs(payoffs_long_put - (np.array([10, 0, 0]) - 1.927905)) < 1e-4)
        assert np.all(abs(payoffs_double_long_put - 2*(np.array([10, 0, 0]) - 1.927905)) < 1e-4)
        assert np.all(abs(payoffs_short_put - (np.array([-10, 0, 0]) + 1.927905)) < 1e-4)
        assert np.all(abs(payoffs_double_short_put - 2*(np.array([-10, 0, 0]) + 1.927905)) < 1e-4)

    def test_get_greeks(self):
        S = np.array([90, 100, 110])

        # We compute for each position
        greeks_long_call = self.position_long_call.get_greeks()
        greeks_double_long_call = self.double_position_long_call.get_greeks()
        greeks_short_call = self.position_short_call.get_greeks()
        greeks_double_short_call = self.double_position_short_call.get_greeks()
        greeks_long_put = self.position_long_put.get_greeks()
        greeks_double_long_put = self.double_position_long_put.get_greeks()
        greeks_short_put = self.position_short_put.get_greeks()
        greeks_double_short_put = self.double_position_short_put.get_greeks()

        # We compare to the results (results - quant. * ((th. price - init. price)))
        assert np.all(abs(np.array(list(greeks_long_call.values())) - (np.array([0.70884, 0.034294,-0.013476, 0.342944, 0.640791]))) < 1e-4)
        assert np.all(abs(np.array(list(greeks_double_long_call.values())) - 2*(np.array([0.70884, 0.034294,-0.013476, 0.342944, 0.640791]))) < 1e-4)
        assert np.all(abs(np.array(list(greeks_short_call.values())) - (-np.array([0.70884, 0.034294, -0.013476, 0.342944, 0.640791]))) < 1e-4)
        assert np.all(abs(np.array(list(greeks_double_short_call.values())) - 2*(-np.array([0.70884, 0.034294, -0.013476, 0.342944, 0.640791]))) < 1e-4)
        assert np.all(abs(np.array(list(greeks_long_put.values())) - (np.array([-0.29116, 0.034294, -0.000445, 0.342944, -0.310439]))) < 1e-4)
        assert np.all(abs(np.array(list(greeks_double_long_put.values())) - 2*(np.array([-0.29116, 0.034294, -0.000445, 0.342944, -0.310439]))) < 1e-4)
        assert np.all(abs(np.array(list(greeks_short_put.values())) - (-np.array([-0.29116, 0.034294, -0.000445, 0.342944, -0.310439]))) < 1e-4)
        assert np.all(abs(np.array(list(greeks_double_short_put.values())) - 2*(-np.array([-0.29116, 0.034294, -0.000445, 0.342944, -0.310439]))) < 1e-4)

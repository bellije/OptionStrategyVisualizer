
import pytest
import numpy as np
from Models.Call import Call

class TestCall:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.call = Call(100, 100, 1, 0.1, 0.05)
        yield

    def test_compute_initial_price(self):
        price = self.call.compute_initial_price()
        assert (abs(price - 6.804963) < 1e-05)
        

    def test_compute_current_price(self):
        price = self.call.compute_current_price(300/365, 110)
        assert (abs(price - 14.29624) < 1e-05)

    def test_compute_pnl_at_date(self):
        pnl = self.call.compute_pnl_at_date(300/365, 110)
        assert (abs(pnl - (14.29624 - 6.804963)) < 1e-05)

    def test_compute_payoffs(self):
        S = np.linspace(1, 2 * 100, 500)
        payoffs = self.call.compute_payoffs(S)
        comparison_payoffs = np.maximum(0, S - 100) - 6.804963
        assert np.all(abs(payoffs - comparison_payoffs) < 1e-5)

    def test_compute_delta(self):
        delta = self.call.compute_delta()
        assert (abs(delta - 0.70884) < 1e-5)

    def test_compute_gamma(self):
        gamma = self.call.compute_gamma()
        assert (abs(gamma - 0.034294) < 1e-5)

    def test_compute_theta(self):
        theta = self.call.compute_theta()
        assert (abs(theta + 0.013476) < 1e-5)

    def test_compute_vega(self):
        vega = self.call.compute_vega()
        assert (abs(vega - 0.342944) < 1e-5)

    def test_compute_rho(self):
        rho = self.call.compute_rho()
        assert (abs(rho - 0.640791) < 1e-5)

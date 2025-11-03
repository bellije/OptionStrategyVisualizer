
import pytest
import numpy as np
from Models.Put import Put

class TestCall:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.put = Put(100, 100, 1, 0.1, 0.05)
        yield

    def test_compute_initial_price(self):
        price = self.put.compute_initial_price()
        assert (abs(price - 1.927905) < 1e-05)
        

    def test_compute_current_price(self):
        price = self.put.compute_current_price(300/365, 110)
        assert (abs(price - 0.26995) < 1e-05)

    def test_compute_pnl_at_date(self):
        pnl = self.put.compute_pnl_at_date(300/365, 110)
        assert (abs(pnl - (0.26995 - 1.927905)) < 1e-05)

    def test_compute_payoffs(self):
        S = np.linspace(1, 2 * 100, 500)
        payoffs = self.put.compute_payoffs(S)
        comparison_payoffs = np.maximum(0, 100 - S) - 1.927905
        assert np.all(abs(payoffs - comparison_payoffs) < 1e-5)

    def test_compute_delta(self):
        delta = self.put.compute_delta()
        assert (abs(delta - -0.29116) < 1e-5)

    def test_compute_gamma(self):
        gamma = self.put.compute_gamma()
        assert (abs(gamma - 0.034294) < 1e-5)

    def test_compute_theta(self):
        theta = self.put.compute_theta()
        assert (abs(theta - -0.000445) < 1e-5)

    def test_compute_vega(self):
        vega = self.put.compute_vega()
        assert (abs(vega - 0.342944) < 1e-5)

    def test_compute_rho(self):
        rho = self.put.compute_rho()
        assert (abs(rho - -0.310439) < 1e-5)

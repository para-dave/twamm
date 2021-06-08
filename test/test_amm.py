import numpy as np

from amm import *


def test_simple_cpmm():
    amm = AMM(2, 2)
    # x * y = 4, so if we put in 2 x, we should get out 1 y so that 4 * 1 = 4
    res = amm.trade([1,1],0)
    assert amm.x_reserves == 4
    assert amm.y_reserves == 1
    assert np.allclose(res.x_out, [0.])
    assert np.allclose(res.y_out, [0.5, 0.5])

    # Redo with infinitessimal
    amm = AMM(2, 2)
    # x * y = 4, so if we put in 2 x, we should get out 1 y so that 4 * 1 = 4
    res = amm.infinitesimal_trade([1, 1], 0)
    assert np.allclose(amm.x_reserves, 4)
    assert np.allclose(amm.y_reserves, 1)
    assert np.allclose(res.x_out, [0.])
    assert np.allclose(res.y_out, [0.5, 0.5])


def test_easy_two_way():
    amm = AMM(2, 3)
    # If we put in 2 x and 3 y, since it's the same as the AMM
    # price, the AMM shouldn't participate at all
    res = amm.infinitesimal_trade(2, 3)
    assert np.allclose(amm.x_reserves, 2)
    assert np.allclose(amm.y_reserves, 3)
    assert np.allclose(res.x_out, [2.])
    assert np.allclose(res.y_out, [3.])


def test_infinitesimal_trade():
    x_start = 100
    y_start = 1
    amm = AMM(x_start, y_start)
    x_in = 50
    y_in = 100
    res = amm.infinitesimal_trade(x_in, y_in)

    # Conservation of shares
    assert np.allclose(amm.x_reserves + res.x_out, x_start + x_in)
    assert np.allclose(amm.y_reserves + res.y_out, y_start + y_in)

    # Verify same as multiple repeated trades
    num_steps = 10000
    dupe_amm = AMM(x_start, y_start)
    for i in range(num_steps):
        dupe_amm.trade(x_in/num_steps, 0)
        dupe_amm.trade(0, y_in/num_steps)

    assert np.allclose(amm.x_reserves, dupe_amm.x_reserves, rtol=1e-3, atol=1e-3)
    assert np.allclose(amm.y_reserves, dupe_amm.y_reserves, rtol=1e-3, atol=1e-3)


if __name__ == "__main__":
    test_simple_cpmm()
    test_easy_two_way()
    test_infinitesimal_trade()

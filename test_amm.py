from amm import *


def test_simple_uniswap():
    amm = AMM(2, 2)
    # x * y = 4, so if we put in 2 x, we should get out 1 y so that 4 * 1 = 4
    res = amm.trade([1,1],0)
    assert amm.x_reserves == 4
    assert amm.y_reserves == 1
    assert np.allclose(res.x_out, [0.])
    assert np.allclose(res.y_out, [0.5, 0.5])


def test_easy_two_way():
    amm = AMM(2, 3)
    # If we put in 2 x and 3 y, since it's the same as the AMM
    # price, the AMM shouldn't participate at all
    res = amm.trade(2, 3)
    assert amm.x_reserves == 2
    assert amm.y_reserves == 3
    assert np.allclose(res.x_out, [2.])
    assert np.allclose(res.y_out, [3.])


def test_active_two_way():
    amm = AMM(2, 3)
    # If we put in 2 x and 1 y, the x inflow pool gets half of y,
    # and the y inflow pool gets 1/4 of x
    res = amm.trade(2, 1)
    assert amm.x_reserves == 3
    assert amm.y_reserves == 2
    assert np.allclose(res.x_out, [1.])
    assert np.allclose(res.y_out, [2.])




if __name__ == "__main__":
    test_simple_uniswap()
    test_easy_two_way()
    test_active_two_way()

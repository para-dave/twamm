from amm import *

def test_simple_uniswap():
    amm = AMM(2, 2)
    # x * y = 4, so if we put in 2 x, we should get out 1 y so that 4 * 1 = 4
    res = amm.trade([1,1],0)
    assert amm.x_reserves == 4
    assert amm.y_reserves == 1
    assert np.allclose(res.x_out, [0.])
    assert np.allclose(res.y_out, [0.5, 0.5])


if __name__ == "__main__":
    test_simple_uniswap()
from arbitrageur import *
from amm import AMM


def test_do_arb():
    amm = AMM(1, 1)
    arbitrageur = Arbitrageur(amm)
    arbitrageur.do_arb(4)

    assert amm.instantaneous_y_price() == 4

    arbitrageur.do_arb(0.25)
    assert amm.instantaneous_y_price() == 0.25



if __name__ == "__main__":
    test_do_arb()
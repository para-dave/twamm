from arbitrageur import *
from twamm import TWAMM


def test_do_arb():
    twamm = TWAMM(1, 1)
    arbitrageur = Arbitrageur(twamm)
    arbitrageur.do_arb(0, 4)

    assert twamm.amm.instantaneous_y_price() == 4

    arbitrageur.do_arb(0, 0.25)
    assert twamm.amm.instantaneous_y_price() == 0.25


if __name__ == "__main__":
    test_do_arb()
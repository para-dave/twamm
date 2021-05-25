from whale_order import *


def test_whale_order():
    order = WhaleOrder(8, 2)

    assert order.qty_in_per_block == 4

    order.update_after_fill(3)
    assert order.blocks_left == 1
    assert order.qty_filled == 3

    order.update_after_fill(2)
    assert order.blocks_left == 0
    assert order.qty_filled == 5

    check_works = False
    try:
        order.update_after_fill(2)
    except AssertionError:
        check_works = True
    assert check_works


if __name__ == "__main__":
    test_whale_order()


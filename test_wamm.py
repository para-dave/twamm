from wamm import *


def test_get_order_inputs():
    wamm = WAMM(1,1)
    expired = WhaleOrder(200, 1)
    expired.update_after_fill(1)
    orders = [WhaleOrder(1,1), WhaleOrder(6,2), expired]
    inputs = wamm.get_order_inputs(orders)
    assert np.allclose(inputs, [1, 3, 0])


def test_process_fills():
    wamm = WAMM(1, 1)
    expired = WhaleOrder(200, 1)
    expired.update_after_fill(1)
    orders = [WhaleOrder(1, 1), WhaleOrder(6, 2), expired]
    wamm.process_fills(orders, [1,2,0])

    assert orders[0].qty_filled == 1
    assert not orders[0].is_live()

    assert orders[1].qty_filled == 2
    assert orders[1].blocks_left == 1

    assert orders[2].qty_filled == 1


def test_trade_batch():
    wamm = WAMM(2,3)
    wamm.add_x_order(WhaleOrder(2, 1))
    wamm.add_y_order(WhaleOrder(1, 1))
    wamm.trade_batch()

    assert wamm.x_orders[0].qty_filled == 2
    assert wamm.y_orders[0].qty_filled == 1
    assert wamm.last_y_price == 1


if __name__ == "__main__":
    test_get_order_inputs()
    test_process_fills()
    test_trade_batch()

from amm import AMM


class TWAMM:
    def __init__(self, x, y):
        self.amm = AMM(x, y)

        self.x_orders = []
        self.y_orders = []

    def add_x_order(self, order):
        self.x_orders.append(order)

    def add_y_order(self, order):
        self.y_orders.append(order)

    def virtual_trade_batch(self):
        x_in = self.get_order_inputs(self.x_orders)
        y_in = self.get_order_inputs(self.y_orders)

        res = self.amm.infinitesimal_trade(x_in, y_in)

        self.process_fills(self.x_orders, res.y_out)
        self.process_fills(self.y_orders, res.x_out)

    def get_order_inputs(self, whale_orders):
        return [order.qty_in_per_block if order.is_live() else 0 for order in whale_orders]

    def process_fills(self, whale_orders, fill_quantities):
        for order, quantity in zip(whale_orders, fill_quantities):
            if order.is_live():
                order.update_after_fill(quantity)
            else:
                assert quantity == 0

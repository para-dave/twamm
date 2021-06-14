from amm import AMM

def process_virtual_trades_first(method):
    def wrapper(self, block_number, *args, **kwargs):
        self.process_virtual_trades(block_number)
        return method(self, block_number, *args, **kwargs)
    return wrapper


class TWAMM:
    def __init__(self, x, y, block_number=0):
        self.amm = AMM(x, y)

        self.block_number = block_number

        self.x_orders = []
        self.y_orders = []

    @process_virtual_trades_first
    def add_x_order(self, block_number, order):
        self.x_orders.append(order)

    @process_virtual_trades_first
    def add_y_order(self, block_number, order):
        self.y_orders.append(order)

    def process_virtual_trades(self, block_number):
        self.block_number = block_number
        pass

    def virtual_trade_batch(self):
        x_in = self.get_order_inputs(self.x_orders)
        y_in = self.get_order_inputs(self.y_orders)

        res = self.amm.infinitesimal_trade(x_in, y_in)

        self.process_fills(self.x_orders, res.y_out)
        self.process_fills(self.y_orders, res.x_out)

    def get_order_inputs(self, long_term_orders):
        return [order.qty_in_per_block if order.is_live() else 0 for order in long_term_orders]

    def process_fills(self, whale_orders, fill_quantities):
        for order, quantity in zip(whale_orders, fill_quantities):
            if order.is_live():
                order.update_after_fill(quantity)
            else:
                assert quantity == 0

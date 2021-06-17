from amm import AMM


def process_virtual_trades_first(method):
    def wrapper(self, block_number, *args, **kwargs):
        self.process_virtual_trades(block_number)
        return method(self, block_number, *args, **kwargs)

    return wrapper


class TWAMM:
    def __init__(self, x, y, last_block_seen=-1):
        self.amm = AMM(x, y)

        self.last_block_seen = last_block_seen

        self.x_orders = []
        self.y_orders = []

    @process_virtual_trades_first
    def add_x_order(self, block_number, order):
        self.x_orders.append(order)

    @process_virtual_trades_first
    def add_y_order(self, block_number, order):
        self.y_orders.append(order)

    @process_virtual_trades_first
    def trade_with_internal_amm(self, block_number, x, y):
        return self.amm.trade(x, y)

    def process_virtual_trades(self, block_number):
        # Just do one virtual trade batch for every block between the last one we've seen and this one
        # Note this is *not* how we would do things on chain: this requires one calculation per block,
        # whereas to save gas we'd just do one calculation for the entire period, plus one additional calculation
        # for any block during which a long-term order expired.
        for block in range(self.last_block_seen, block_number):
            self.virtual_trade_batch()

        self.last_block_seen = block_number

    def virtual_trade_batch(self):
        x_in = self.get_order_inputs(self.x_orders)
        y_in = self.get_order_inputs(self.y_orders)

        res = self.amm.infinitesimal_trade(x_in, y_in)

        self.process_fills(self.x_orders, res.y_out)
        self.process_fills(self.y_orders, res.x_out)

    def get_order_inputs(self, long_term_orders):
        return [
            order.qty_in_per_block if order.is_live() else 0
            for order in long_term_orders
        ]

    def process_fills(self, whale_orders, fill_quantities):
        for order, quantity in zip(whale_orders, fill_quantities):
            if order.is_live():
                order.update_after_fill(quantity)
            else:
                assert quantity == 0

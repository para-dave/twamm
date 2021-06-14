class Arbitrageur():
    def __init__(self, twamm):
        self.twamm = twamm
        self.x_balance = 0
        self.y_balance = 0
        self.price_before_arb = None

    def do_arb(self, block_number, true_price):
        x_to_spend, y_to_spend = self.find_arb(block_number, true_price)
        self.x_balance -= x_to_spend
        self.y_balance -= y_to_spend
        res = self.twamm.trade_with_internal_amm(block_number, x_to_spend, y_to_spend)

        self.x_balance += res.x_out
        self.y_balance += res.y_out

    def get_x_profit(self, true_price):
        return float(self.x_balance + true_price * self.y_balance)

    # assuming no fee
    def find_arb(self, block_number, true_y_price):
        # Advance TWAMM to the current block
        # An arbitrageur obviously wouldn't do this on-chain. Instead they'd calculate the state themselves off-chain
        # based on the block number.
        self.twamm.process_virtual_trades(block_number)

        amm = self.twamm.amm

        self.price_before_arb = amm.instantaneous_y_price()

        # see https://research.paradigm.xyz/LP_Wealth.pdf
        if true_y_price > amm.x_reserves / amm.y_reserves:
            x_to_spend = max(
                amm.x_reserves * ((true_y_price * amm.y_reserves/amm.x_reserves) ** (1/2)-1),
                0)
            return [x_to_spend, 0]
        elif true_y_price < amm.x_reserves / amm.y_reserves:
            y_to_spend = max(
                amm.y_reserves * ((1/true_y_price * amm.x_reserves/amm.y_reserves) ** (1/2)-1),
                0)
            return [0, y_to_spend]
        else:
            return [0, 0]


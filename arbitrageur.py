class Arbitrageur():
    def __init__(self, amm):
        self.amm = amm
        self.x_balance = 0
        self.y_balance = 0

    def do_arb(self, true_price):
        x_to_spend, y_to_spend = self.find_arb(true_price)
        self.x_balance -= x_to_spend
        self.y_balance -= y_to_spend
        res = self.amm.trade(x_to_spend, y_to_spend)

        self.x_balance += res.x_out
        self.y_balance += res.y_out

    def get_x_profit(self, true_price):
        return self.x_balance + true_price * self.y_balance

    # see https://research.paradigm.xyz/LP_Wealth.pdf
    # assuming no fee
    def find_arb(self, true_y_price):
        if true_y_price > self.amm.x_reserves / self.amm.y_reserves:
            x_to_spend = max(
                self.amm.x_reserves * ((true_y_price * self.amm.y_reserves/self.amm.x_reserves) ** (1/2)-1),
                0)
            return [x_to_spend, 0]
        elif true_y_price < self.amm.x_reserves / self.amm.y_reserves:
            y_to_spend = max(
                self.amm.y_reserves * ((1/true_y_price * self.amm.x_reserves/self.amm.y_reserves) ** (1/2)-1),
                0)
            return [0, y_to_spend]
        else:
            return [0, 0]


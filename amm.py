import numpy as np


class TradeResult:
    def __init__(self, x_out, y_out):
        self.x_out = x_out
        self.y_out = y_out


class AMM:
    def __init__(self, x, y):
        self.x_reserves = x
        self.y_reserves = y

    def trade(self, x_in, y_in):
        # always convert for convenience
        x_in = np.array(x_in)
        y_in = np.array(y_in)

        total_x = self.x_reserves + x_in.sum()
        total_y = self.y_reserves + y_in.sum()

        # Trading all of x for all of y and divvying up shares accordingly
        self_x_share = self.x_reserves / total_x
        self_y_share = self.y_reserves / total_y

        x_in_shares = x_in / total_x
        y_in_shares = y_in / total_y

        # Update
        self.x_reserves = self_y_share * total_x
        self.y_reserves = self_x_share * total_y

        return TradeResult(y_in_shares * total_x, x_in_shares * total_y)

if __name__ == "__main__":
    pass

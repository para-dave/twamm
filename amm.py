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

        # This actually all works just fine if both x_in and y_in are nonzero,
        # but for the purposes of this simulation we're only
        # simulating one-way trades, and using this function for convenience
        # so this is to make sure we're not simulating the wrong thing anywhere
        assert np.sum(x_in) == 0 or np.sum(y_in) == 0

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

        x_out = y_in_shares * total_x
        y_out = x_in_shares * total_y

        return TradeResult(x_out, y_out)

    def infinitesimal_trade(self, x_in, y_in):
        # always convert for convenience
        x_in = np.array(x_in)
        y_in = np.array(y_in)

        # Need to check for one-sided orders to avoid math error
        if np.sum(x_in) == 0 or np.sum(y_in) == 0:
            return self.trade(x_in, y_in)

        k = self.x_reserves * self.y_reserves
        c = (np.sqrt(self.x_reserves * np.sum(y_in)) - np.sqrt(self.y_reserves * np.sum(x_in))) / \
            (np.sqrt(self.x_reserves * np.sum(y_in)) + np.sqrt(self.y_reserves * np.sum(x_in)))
        exponent = 2*np.sqrt(np.sum(x_in)*np.sum(y_in)/k)
        end_x_sum = np.sqrt(k*np.sum(x_in)/np.sum(y_in))*(np.exp(exponent)+c)/\
            (np.exp(exponent)-c)
        end_y_sum = k/end_x_sum

        x_out_sum = self.x_reserves - end_x_sum + np.sum(x_in)
        y_out_sum = self.y_reserves - end_y_sum + np.sum(y_in)

        # Update
        self.x_reserves = end_x_sum
        self.y_reserves = end_y_sum

        x_out = x_out_sum * y_in/np.sum(y_in)
        y_out = y_out_sum * x_in/np.sum(x_in)

        return TradeResult(x_out, y_out)

    def instantaneous_y_price(self):
        return float(self.x_reserves / self.y_reserves)

if __name__ == "__main__":
    pass

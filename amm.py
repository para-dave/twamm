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

        l = np.sqrt(self.x_reserves * self.y_reserves)
        sqrt_p_ratio = np.sqrt(np.sum(y_in) / np.sum(x_in))
        c = (1 - self.y_reserves / (l * sqrt_p_ratio)) / (1 + self.y_reserves / (l * sqrt_p_ratio))
        end_y_sum = sqrt_p_ratio * l * (np.exp(2 * np.sum(x_in) * sqrt_p_ratio / l) - c) / (
                np.exp(2 * np.sum(x_in) * sqrt_p_ratio / l) + c)
        end_x_sum = l ** 2 / end_y_sum

        x_out_sum = self.x_reserves - end_x_sum + np.sum(x_in)
        y_out_sum = self.y_reserves - end_y_sum + np.sum(y_in)

        # Update
        self.x_reserves = end_x_sum
        self.y_reserves = end_y_sum

        x_out = x_out_sum * y_in/np.sum(y_in)
        y_out = y_out_sum * x_in/np.sum(x_in)

        return TradeResult(x_out, y_out)

    def instantaneous_y_price(self):
        return self.x_reserves / self.y_reserves

if __name__ == "__main__":
    pass

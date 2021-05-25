class WhaleOrder:
    def __init__(self, qty_in, blocks_lifespan):
        self.qty_in = qty_in
        self.blocks_lifespan = blocks_lifespan
        self.qty_in_per_block = qty_in / blocks_lifespan

        # Ongoing stats
        self.blocks_left = blocks_lifespan
        self.qty_filled = 0

    def update_after_fill(self, qty_filled):
        assert self.is_live()

        self.qty_filled += qty_filled
        self.blocks_left -= 1

    def is_live(self):
        return self.blocks_left > 0

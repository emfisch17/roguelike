class Tile:
    """
    A tile on a map that may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # If a tile is blocked, it also blocks sight by default
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

        self.explored = False

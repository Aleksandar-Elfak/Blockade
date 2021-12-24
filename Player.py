class Player:
    green_leftover = None
    blue_leftover = None
    pc = None

    def __init__(self, wall, pc):
        self.green_leftover = wall
        self.blue_leftover = wall
        self.pc = pc

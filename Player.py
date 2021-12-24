class Player:
    green_leftover = None
    blue_leftover = None
    pc = None
    sign = None

    def __init__(self, wall, pc, sign):
        self.green_leftover = wall
        self.blue_leftover = wall
        self.pc = pc
        self.sign = sign

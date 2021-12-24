from Board import Board
from Player import Player

# ⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆


class Game:
    board = None
    player_x = None
    player_o = None
    currentPlayer = None
    round_num = 0
    state = None

    def __init__(
        self, row, column, start_x1, start_x2, start_o1, start_o2, num_wall, pc
    ):
        self.board = Board(row, column, start_x1, start_x2, start_o1, start_o2)
        # kompjuter i covek
        # self.player_x = Player(num_wall, True if pc == "X" or pc == "x" else False, "X")
        # self.player_o = Player(num_wall, True if pc == "O" or pc == "o" else False, "O")
        # dva coveka
        self.player_x = Player(num_wall, True, "X")
        self.player_o = Player(num_wall, True, "O")
        self.currentPlayer = self.player_x
        self.saveState()

    def showBoard(self):
        self.board.showBoard()

    def saveState(self):
        state = {
            "matrix": self.board.matrix,
            "X": self.board.current_x1,
            "x": self.board.current_x2,
            "o": self.board.current_o1,
            "O": self.board.current_o2,
            "xGreenWall": self.player_x.green_leftover,
            "xBlueWall": self.player_x.blue_leftover,
            "oGreenWall": self.player_o.green_leftover,
            "oBlueWall": self.player_o.blue_leftover,
        }

    def isEnd(self):
        return self.board.isEnd()

    def validParameters(self, pawn, move, wall):
        move = move.split(sep=" ")

        if len(move) != 2:
            print("Invalid number of parametars.")
            return False

        if wall != None:
            wall = wall.split(" ")

            if len(wall) != 3:
                print("Invalid number of parametars.")
                return False  # suvisno

            if wall[0] != "G" and wall[0] != "B":
                print("Wall must be G or B.")
                return False

            if (wall[0] == "G" and self.currentPlayer.green_leftover == 0) or (
                wall[0] == "B" and self.currentPlayer.blue_leftover == 0
            ):
                print("You have no walls remaining.")
                return False

        if not (self.round_num % 2 == 0 and (pawn == "X" or pawn == "x")):
            if not (self.round_num % 2 == 1 and (pawn == "O" or pawn == "o")):
                print("Non valid pawn picked.")
                return False

        parms = self.board.validParameters(move, wall)
        if False == parms:
            return False
        else:
            return parms

    def validMove(self, pawn, move, wall):
        return self.board.validMove(pawn, move, wall)

    def aiMove(self):
        print("AI MOVE")

    def reduceWall(self, wall):
        if wall[0] == "G":
            self.currentPlayer.green_leftover -= 1
        else:
            self.currentPlayer.blue_leftover -= 1

    def humanMove(self):

        pawn = input("Select your pawn: ")
        move = input("Input coordinates of you move: ")
        wallNum = True
        wall = None
        if not (
            self.currentPlayer.blue_leftover + self.currentPlayer.green_leftover == 0
        ):
            wall = input(
                "Input G or B for color of the wall and coordinates where to place it: "
            )
        else:
            wallNum = False

        params = self.validParameters(pawn, move, wall)

        if params == False:
            return False

        move = params[0]
        wall = params[1]

        if not self.validMove(pawn, move, wall):
            return False

        self.board.changeState(pawn, move, wall)

        if wallNum:
            self.reduceWall(wall)

        self.saveState()

        self.showBoard()

        return True

    def makeAMove(self):
        if self.currentPlayer.pc:
            return self.humanMove()
        else:
            return self.aiMove()

    def play(self):
        self.showBoard()
        while self.isEnd() == False:

            print(
                "Round: "
                + str(self.round_num + 1)
                + " It's player "
                + self.currentPlayer.sign
                + "'s turn."
            )

            while self.makeAMove() == False:
                print("")

            self.round_num += 1
            if self.round_num % 2 == 0:
                self.currentPlayer = self.player_x
            else:
                self.currentPlayer = self.player_o

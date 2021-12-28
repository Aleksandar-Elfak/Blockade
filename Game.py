from Board import Board
from Player import Player
import copy

# ⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆


class Game:
    board = None
    player_x = None
    player_o = None
    currentPlayer = None
    round_num = 0

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

    def showBoard(self, state):
        self.board.showBoard(state)

    def possibleMoves(self, state):
        pawn1 = None
        pawn2 = None
        BlueLeftover = None
        GreenLeftover = None
        if state["CP"] == "X":
            pawn1 = "X"
            pawn2 = "x"
            BlueLeftover = state["xBlueWall"]
            GreenLeftover = state["xGreenWall"]
        else:
            pawn1 = "O"
            pawn2 = "o"
            BlueLeftover = state["oBlueWall"]
            GreenLeftover = state["oGreenWall"]

        jumps1 = [
            (state[pawn1][0] - 2, state[pawn1][1]),
            (state[pawn1][0] + 2, state[pawn1][1]),
            (state[pawn1][0], state[pawn1][1] - 2),
            (state[pawn1][0], state[pawn1][1] + 2),
            (state[pawn1][0] + 2, state[pawn1][1] + 2),
            (state[pawn1][0] + 2, state[pawn1][1] - 2),
            (state[pawn1][0] - 2, state[pawn1][1] + 2),
            (state[pawn1][0] - 2, state[pawn1][1] - 2),
            (state[pawn1][0] + 4, state[pawn1][1]),
            (state[pawn1][0] - 4, state[pawn1][1]),
            (state[pawn1][0], state[pawn1][1] + 4),
            (state[pawn1][0], state[pawn1][1] - 4),
        ]

        jumps2 = [
            (state[pawn2][0] - 2, state[pawn2][1]),
            (state[pawn2][0] + 2, state[pawn2][1]),
            (state[pawn2][0], state[pawn2][1] - 2),
            (state[pawn2][0], state[pawn2][1] + 2),
            (state[pawn2][0] + 2, state[pawn2][1] + 2),
            (state[pawn2][0] + 2, state[pawn2][1] - 2),
            (state[pawn2][0] - 2, state[pawn2][1] + 2),
            (state[pawn2][0] - 2, state[pawn2][1] - 2),
            (state[pawn2][0] + 4, state[pawn2][1]),
            (state[pawn2][0] - 4, state[pawn2][1]),
            (state[pawn2][0], state[pawn2][1] + 4),
            (state[pawn2][0], state[pawn2][1] - 4),
        ]

        walls = []
        if BlueLeftover > 0 or GreenLeftover > 0:
            for row in range(0, len(state["matrix"]) - 2, 2):
                for column in range(0, len(state["matrix"][row]) - 2, 2):
                    if BlueLeftover > 0:
                        walls.append(("B", row, column))
                    if GreenLeftover > 0:
                        walls.append(("G", row, column))

        for jump in jumps1:
            if BlueLeftover > 0 or GreenLeftover > 0:
                for wall in walls:
                    if self.validMove(pawn1, jump, wall, state):
                        yield (pawn1, jump, wall)
            else:
                if self.validMove(pawn1, jump, None, state):
                    yield (pawn1, jump, None)

        for jump in jumps2:
            if BlueLeftover > 0 or GreenLeftover > 0:
                for wall in walls:
                    if self.validMove(pawn2, jump, wall, state):
                        yield (pawn2, jump, wall)
            else:
                if self.validMove(pawn1, jump, None, state):
                    yield (pawn2, jump, None)

    def playAIMove(self, pawn, jump, wall, state):
        self.board.playAIMove(pawn, jump, wall, state)

    def getState(self):
        return {
            "matrix": copy.deepcopy(self.board.matrix),
            "X": self.board.current_x1,
            "x": self.board.current_x2,
            "O": self.board.current_o1,
            "o": self.board.current_o2,
            "xGreenWall": self.player_x.green_leftover,
            "xBlueWall": self.player_x.blue_leftover,
            "oGreenWall": self.player_o.green_leftover,
            "oBlueWall": self.player_o.blue_leftover,
            "CP": self.currentPlayer.sign,
        }

    def possibleStates(self):
        state = self.getState()

        for move in self.possibleMoves(state):
            posState = copy.deepcopy(state)
            self.playAIMove(move[0], move[1], move[2], posState)
            yield posState

    def isEndAI(self):
        return  # todo later

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

    def validMove(self, pawn, move, wall, state, pc=False):
        if pc:
            return self.board.validMove(pawn, move, wall, state, True)
        return self.board.validMove(pawn, move, wall, state)

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

        if not self.validMove(pawn, move, wall, self.getState(), True):
            return False

        self.board.changeState(pawn, move, wall)

        if wallNum:
            self.reduceWall(wall)

        self.showBoard(self.getState())

        return True

    def makeAMove(self):
        if self.currentPlayer.pc:
            return self.humanMove()
        else:
            return self.aiMove()

    def play(self):
        self.showBoard(self.getState())
        while self.isEnd() == False:
            #for s in self.possibleStates():  # predak min-maxa
                # self.showBoard(s)
                #None

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

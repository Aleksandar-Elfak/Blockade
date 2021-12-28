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
    ai = None

    def __init__(
        self, row, column, start_x1, start_x2, start_o1, start_o2, num_wall, pc, ai
    ):
        self.board = Board(row, column, start_x1, start_x2, start_o1, start_o2)
        # kompjuter i covek
        # self.player_x = Player(num_wall, True if pc == "X" or pc == "x" else False, "X")
        # self.player_o = Player(num_wall, True if pc == "O" or pc == "o" else False, "O")
        # dva coveka
        self.player_x = Player(num_wall, True, "X")
        self.player_o = Player(num_wall, False, "O")
        # self.player_o = Player(num_wall, True, "O")
        self.currentPlayer = self.player_x
        self.ai = ai

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

    def playAIMove(self, move, state):
        return self.board.playAIMove(move[0], move[1], move[2], state)

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

    def possibleStates(self, state):

        for move in self.possibleMoves(state):
            posState = copy.deepcopy(state)
            self.playAIMove(move[0], move[1], move[2], posState)
            yield posState

    def isEnd(self, state):
        return self.board.isEnd(state)

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
        move = self.MinMax(self.getState(), True, 1, (None, -1), (None, 1001))
        self.board.changeState(move[0][0], move[0][1], move[0][2])
        self.showBoard(self.getState())
        return True

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
            print(
                "Round: "
                + str(self.round_num + 1)
                + " It's player "
                + self.currentPlayer.sign
                + "'s turn."
            )
            return self.humanMove()
        else:
            return self.aiMove()

    def gradeState(self, state):
        finish = None
        start = None
        pawns = None
        enemy = None
        end = self.isEnd(state)

        if self.ai == "X":
            finish = (self.board.start_o1, self.board.start_o2)
            start = (self.board.start_x1, self.board.start_x2)
            pawns = (state["X"], state["x"])
            enemy = (state["O"], state["o"])
            if end == "X":
                return 1000
            if end == "O":
                return 0
        else:
            finish = (self.board.start_x1, self.board.start_x2)
            start = (self.board.start_o1, self.board.start_o2)
            pawns = (state["O"], state["o"])
            enemy = (state["X"], state["x"])
            if end == "X":
                return 0
            if end == "O":
                return 1000

        return (
            100
            - min(
                abs((pawns[0][0] - finish[0][0]) + (pawns[0][1] - finish[0][1])),
                abs((pawns[1][0] - finish[0][0]) + (pawns[1][1] - finish[0][1])),
                abs((pawns[0][0] - finish[1][0]) + (pawns[0][1] - finish[1][1])),
                abs((pawns[1][0] - finish[1][0]) + (pawns[1][1] - finish[1][1])),
            )
            + max(
                abs((enemy[0][0] - start[0][0]) + (enemy[0][1] - start[0][1])),
                abs((enemy[1][0] - start[0][0]) + (enemy[1][1] - start[0][1])),
                abs((enemy[0][0] - start[1][0]) + (enemy[0][1] - start[1][1])),
                abs((enemy[1][0] - start[1][0]) + (enemy[1][1] - start[1][1])),
            )
        )

    def MinMax(self, state, npc, depth, alpha, beta, move=None):
        winner = self.isEnd(state)
        if winner != False:
            return (move, self.gradeState(state))

        if depth == 0:
            return (move, self.gradeState(state))

        ps = list(self.possibleMoves(state))

        if ps is None or len(ps) == 0:
            return (move, self.gradeState(state))

        if npc:
            for s in ps:
                alpha = max(
                    alpha,
                    self.MinMax(
                        self.playAIMove(s, copy.deepcopy(state)),
                        True if npc == False else False,
                        depth - 1,
                        alpha,
                        beta,
                        s,
                    ),
                    key=lambda x: x[1],
                )
                if alpha[1] >= beta[1]:
                    return beta
            return alpha
        else:
            for s in ps:
                beta = min(
                    beta,
                    self.MinMax(
                        self.playAIMove(s, copy.deepcopy(state)),
                        True if npc == False else False,
                        depth - 1,
                        alpha,
                        beta,
                        s,
                    ),
                    key=lambda x: x[1],
                )
                if beta[1] <= alpha[1]:
                    return alpha
            return beta

    def play(self):
        self.showBoard(self.getState())
        winner = False
        while winner == False:

            while self.makeAMove() == False:
                print("")

            self.round_num += 1
            if self.round_num % 2 == 0:
                self.currentPlayer = self.player_x
            else:
                self.currentPlayer = self.player_o

            winner = self.isEnd(self.getState())

        if winner == "X":
            print("Player X has won.")
        else:
            print("Player O has won.")

import threading
from Board import Board
from Player import Player
import copy
import time
from threading import Thread

# ⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆⋆

verticalWall = "ǁ"
horisontalWall = "═"


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
        self.player_x = Player(num_wall, True if pc == "X" or pc == "x" else False, "X")
        self.player_o = Player(num_wall, True if pc == "O" or pc == "o" else False, "O")
        # dva coveka
        # self.player_x = Player(num_wall, True, "X")
        # self.player_o = Player(num_wall, False, "O")
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
                    valid = self.validMove(pawn1, jump, wall, state)
                    if valid == 10:
                        break
                    elif valid:
                        yield (pawn1, jump, wall)
            else:
                if self.validMove(pawn1, jump, None, state) == True:
                    yield (pawn1, jump, None)

        for jump in jumps2:
            if BlueLeftover > 0 or GreenLeftover > 0:
                for wall in walls:
                    valid = self.validMove(pawn2, jump, wall, state)
                    if valid == 10:
                        break
                    elif valid:
                        yield (pawn2, jump, wall)
            else:
                if self.validMove(pawn2, jump, None, state) == True:
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
                print("You have no walls of that color remaining.")
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
            return (
                True
                if self.board.validMove(pawn, move, wall, state, True) == True
                else False
            )
        return self.board.validMove(pawn, move, wall, state)

    def aiMove(self):
        # print(str(round(time.time() * 1000)) + " Start")
        move = self.MinMax(self.getState(), True, 1, (None, -1), (None, 1001))
        # print(str(round(time.time() * 1000)) + " End")
        self.board.changeState(move[0][0], move[0][1], move[0][2])
        if move[0][2] != None:
            self.reduceWall(move[0][2][0])
        print()
        print("AI's Blue walls left: " + str(self.currentPlayer.blue_leftover))
        print("AI's Green walls left: " + str(self.currentPlayer.green_leftover))
        self.showBoard(self.getState())
        return True

    def reduceWall(self, wall):
        if wall[0] == "G":
            self.currentPlayer.green_leftover -= 1
        else:
            self.currentPlayer.blue_leftover -= 1

    def humanMove(self):
        print("Blue walls left: " + str(self.currentPlayer.blue_leftover))
        print("Green walls left: " + str(self.currentPlayer.green_leftover))
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

    simpleMatrixThread = [None, None, None, None, None, None, None, None, None]
    heurThread = [None, None, None, None, None, None, None, None, None]

    def transformMatrix(self, state, finish, start, i):
        matrix = []
        for x in range(0, len(state["matrix"])):
            matrix.append([])
            for y in range(0, len(state["matrix"][x])):
                matrix[x].append(
                    0
                    if (
                        state["matrix"][x][y] == verticalWall
                        or state["matrix"][x][y] == horisontalWall
                    )
                    else 1
                )
        matrix[start[0]][start[1]] = 2
        matrix[finish[0]][finish[1]] = 3

        self.simpleMatrixThread[i] = (
            matrix,
            finish,
            start,
        )

    def astar(self, matrix, finish, start, index):

        width = len(matrix[0])
        height = len(matrix)

        heuristic = lambda i, j: abs(finish[0] - i) + abs(finish[1] - j)
        comp = lambda state: state[2] + state[3]  # get the total cost

        # small variation for easier code, state is (coord_tuple, previous, path_cost, heuristic_cost)
        fringe = [((start[0], start[1]), list(), 0, heuristic(start[0], start[1]))]
        visited = {}  # empty set
        # maybe limit to prevent too long search
        while True:
            # get first state (least cost)
            state = fringe[0]
            fringe.pop(0)

            # goal check
            (i, j) = state[0]
            if matrix[i][j] == 3:
                path = [state[0]] + state[1]
                path.reverse()
                self.heurThread[index] = path
                return

            # set the cost (path is enough since the heuristic won't change)
            visited[(i, j)] = state[2]

            # explore neighbor
            neighbor = list()
            if i > 1 and matrix[i - 1][j] > 0:  # top
                neighbor.append((i - 2, j))
            if i < height - 2 and matrix[i + 1][j] > 0:
                neighbor.append((i + 2, j))
            if j > 1 and matrix[i][j - 1] > 0:
                neighbor.append((i, j - 2))
            if j < width - 2 and matrix[i][j + 1] > 0:
                neighbor.append((i, j + 2))

            for n in neighbor:
                next_cost = state[2] + 1
                if n in visited and visited[n] <= next_cost:
                    continue
                fringe.append(
                    (n, [state[0]] + state[1], next_cost, heuristic(n[0], n[1]))
                )

            # resort the list (SHOULD use a priority queue here to avoid re-sorting all the time)
            fringe.sort(key=comp)
        state = fringe[0]
        (i, j) = state[0]

        path = [state[0]] + state[1]
        path.reverse()
        self.heurThread[index] = path

    def gradeState(self, state):
        self.transformMatrix(state, self.board.start_x1, state["O"], 1)
        self.transformMatrix(state, self.board.start_x1, state["o"], 2)
        self.transformMatrix(state, self.board.start_x2, state["O"], 3)
        self.transformMatrix(state, self.board.start_x2, state["o"], 4)
        self.transformMatrix(state, self.board.start_o1, state["X"], 5)
        self.transformMatrix(state, self.board.start_o1, state["x"], 6)
        self.transformMatrix(state, self.board.start_o2, state["X"], 7)
        self.transformMatrix(state, self.board.start_o2, state["x"], 8)

        self.astar(
            self.simpleMatrixThread[1][0],
            self.simpleMatrixThread[1][1],
            self.simpleMatrixThread[1][2],
            1,
        )
        self.astar(
            self.simpleMatrixThread[2][0],
            self.simpleMatrixThread[2][1],
            self.simpleMatrixThread[2][2],
            2,
        )
        self.astar(
            self.simpleMatrixThread[3][0],
            self.simpleMatrixThread[3][1],
            self.simpleMatrixThread[3][2],
            3,
        )
        self.astar(
            self.simpleMatrixThread[4][0],
            self.simpleMatrixThread[4][1],
            self.simpleMatrixThread[4][2],
            4,
        )
        self.astar(
            self.simpleMatrixThread[5][0],
            self.simpleMatrixThread[5][1],
            self.simpleMatrixThread[5][2],
            5,
        )
        self.astar(
            self.simpleMatrixThread[6][0],
            self.simpleMatrixThread[6][1],
            self.simpleMatrixThread[6][2],
            6,
        )
        self.astar(
            self.simpleMatrixThread[7][0],
            self.simpleMatrixThread[7][1],
            self.simpleMatrixThread[7][2],
            7,
        )
        self.astar(
            self.simpleMatrixThread[8][0],
            self.simpleMatrixThread[8][1],
            self.simpleMatrixThread[8][2],
            8,
        )
        shortYA = min(
            len(self.heurThread[1]),
            len(self.heurThread[3]),
        )

        shortYB = min(
            len(self.heurThread[2]),
            len(self.heurThread[4]),
        )

        shortXA = min(
            len(self.heurThread[5]),
            len(self.heurThread[7]),
        )

        shortXB = min(
            len(self.heurThread[6]),
            len(self.heurThread[8]),
        )

        # print(str(shortX) + " " + str(shortY))
        if state["CP"] == "O":
            return (
                500
                - min(shortXA, shortXB) * 1.1
                - max(shortXA, shortXB) * 0.15
                + min(shortYA, shortYB)
                + max(shortYA, shortYB) * 0.1
            )
        else:
            return (
                500
                - min(shortYA, shortYB) * 1.1
                - max(shortYA, shortYB) * 0.15
                + min(shortXA, shortXB)
                + max(shortXA, shortXB) * 0.1
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
                pass

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

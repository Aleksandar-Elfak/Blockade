import copy
import time

verticalWall = "ǁ"
horisontalWall = "═"


class Board:
    row = 0
    column = 0
    start_x1 = None
    start_o1 = None
    current_x1 = None
    current_o1 = None
    start_x2 = None
    start_o2 = None
    current_x2 = None
    current_o2 = None
    matrix = None
    tmpMatrix = None

    def __init__(self, row, column, start_x1, start_x2, start_o1, start_o2):
        self.row = row * 2 - 1
        self.column = column * 2 - 1
        self.start_x1 = self.adjustIndex(start_x1)
        self.start_o1 = self.adjustIndex(start_o1)
        self.start_x2 = self.adjustIndex(start_x2)
        self.start_o2 = self.adjustIndex(start_o2)
        self.current_x1 = self.adjustIndex(start_x1)
        self.current_o1 = self.adjustIndex(start_o1)
        self.current_x2 = self.adjustIndex(start_x2)
        self.current_o2 = self.adjustIndex(start_o2)
        self.matrix = [
            [" " if y % 2 == 0 else "|" for y in range(0, column * 2 - 1)]
            if x % 2 == 0
            else ["—" if y % 2 == 0 else " " for y in range(0, column * 2 - 1)]
            for x in range(0, row * 2 - 1)
        ]
        self.matrix[self.start_x1[0]][self.start_x1[1]] = "X"
        self.matrix[self.start_o1[0]][self.start_o1[1]] = "O"
        self.matrix[self.start_x2[0]][self.start_x2[1]] = "x"
        self.matrix[self.start_o2[0]][self.start_o2[1]] = "o"

    def adjustIndex(self, index):
        marking = {
            "1": 0,
            "2": 1,
            "3": 2,
            "4": 3,
            "5": 4,
            "6": 5,
            "7": 6,
            "8": 7,
            "9": 8,
            "A": 9,
            "B": 10,
            "C": 11,
            "D": 12,
            "E": 13,
            "F": 14,
            "G": 15,
            "H": 16,
            "I": 17,
            "J": 18,
            "K": 19,
            "L": 20,
            "M": 21,
            "N": 22,
            "O": 23,
            "P": 24,
            "Q": 25,
            "R": 26,
            "S": 27,
        }

        adjustedIndex = (
            marking.get(index[0]) * 2 if marking.get(index[0]) != None else -1,
            marking.get(index[1]) * 2 if marking.get(index[1]) != None else -1,
        )

        return adjustedIndex

    def isEnd(self, state):
        if (
            state["X"] == self.start_o1
            or state["X"] == self.start_o2
            or state["x"] == self.start_o1
            or state["x"] == self.start_o2
        ):
            return "X"
        if (
            state["O"] == self.start_x1
            or state["O"] == self.start_x2
            or state["o"] == self.start_x1
            or state["o"] == self.start_x2
        ):
            return "O"
        return False

    def showBoard(self, state):
        marking = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
        ]
        print("")

        for i in range(0, self.column // 2 + 1):
            if i == 0:
                print("  ", end="")
            print(marking[i], end=" ")
        print("")

        for i in range(0, self.column // 2 + 1):
            if i == 0:
                print("  ", end="")
            print("═", end=" ")
        print("")

        for x in range(0, self.row):
            if x % 2 == 0:
                for y in range(0, self.column):
                    if y == 0:
                        print(marking[x // 2], end="ǁ")
                    print(state["matrix"][x][y], end="")
                print("ǁ" + str(marking[x // 2]))
            else:
                for y in range(0, self.column):
                    if y == 0:
                        print("  ", end="")
                    print(state["matrix"][x][y], end="")
                print("")

        for i in range(0, self.column // 2 + 1):
            if i == 0:
                print("  ", end="")
            print("═", end=" ")
        print("")

        for i in range(0, self.column // 2 + 1):
            if i == 0:
                print("  ", end="")
            print(marking[i], end=" ")
        print("")

    def playAIMove(self, pawn, jump, wall, state):
        currentPosition = None
        if pawn == "X":
            currentPosition = state["X"]
            state["X"] = jump
        elif pawn == "x":
            currentPosition = state["x"]
            state["x"] = jump
        elif pawn == "O":
            currentPosition = state["O"]
            state["O"] = jump
        elif pawn == "o":
            currentPosition = state["o"]
            state["o"] = jump

        state["matrix"][jump[0]][jump[1]] = pawn

        if currentPosition == self.start_x1 or currentPosition == self.start_x2:
            state["matrix"][currentPosition[0]][currentPosition[1]] = "⋆"
        else:
            if currentPosition == self.start_o1 or currentPosition == self.start_o2:
                state["matrix"][currentPosition[0]][currentPosition[1]] = "0"
            else:
                state["matrix"][currentPosition[0]][currentPosition[1]] = " "

        if wall != None:
            if wall[0] == "G":
                state["matrix"][wall[1]][wall[2] + 1] = verticalWall
                state["matrix"][wall[1] + 2][wall[2] + 1] = verticalWall
                if pawn == "x" or pawn == "X":
                    state["xGreenWall"] -= 1
                else:
                    state["oGreenWall"] -= 1
            else:
                state["matrix"][wall[1] + 1][wall[2]] = horisontalWall
                state["matrix"][wall[1] + 1][wall[2] + 2] = horisontalWall
                if pawn == "x" or pawn == "X":
                    state["xBlueWall"] -= 1
                else:
                    state["oBlueWall"] -= 1

        state["CP"] = "X" if state["CP"] == "O" else "O"
        return state

    def changeState(self, pawn, move, wall):
        currentPosition = None
        if pawn == "X":
            currentPosition = self.current_x1
            self.current_x1 = move
        elif pawn == "x":
            currentPosition = self.current_x2
            self.current_x2 = move
        elif pawn == "O":
            currentPosition = self.current_o1
            self.current_o1 = move
        elif pawn == "o":
            currentPosition = self.current_o2
            self.current_o2 = move

        self.matrix[move[0]][move[1]] = pawn

        if currentPosition == self.start_x1 or currentPosition == self.start_x2:
            self.matrix[currentPosition[0]][currentPosition[1]] = "⋆"
        else:
            if currentPosition == self.start_o1 or currentPosition == self.start_o2:
                self.matrix[currentPosition[0]][currentPosition[1]] = "0"
            else:
                self.matrix[currentPosition[0]][currentPosition[1]] = " "

        if wall != None:

            if wall[0] == "G":
                self.matrix[wall[1]][wall[2] + 1] = "ǁ"
                self.matrix[wall[1] + 2][wall[2] + 1] = "ǁ"
            else:
                self.matrix[wall[1] + 1][wall[2]] = "═"
                self.matrix[wall[1] + 1][wall[2] + 2] = "═"

    def validParameters(self, move, wall):
        adjustedMove = self.adjustIndex(move)
        if adjustedMove[0] == -1 or adjustedMove[1] == -1:
            print("Invalid input[a1]: Pawn coordinates are not valid.")
            return False

        # provera indeksa u obliku broja
        if not (adjustedMove[0] != None and adjustedMove[0] < self.row):
            print("Invalid input[a3]: Pawn coordinates are not valid.")
            return False

        if not (adjustedMove[1] != None and adjustedMove[1] < self.column):
            print("Invalid input[a4]: Pawn coordinates are not valid.")
            return False

        adjustedWall = None

        if wall != None:
            adjustedWall = self.adjustIndex((wall[1], wall[2]))
            if adjustedWall[0] == -1 or adjustedWall[1] == -1:
                print("Invalid input[a2]: Wall coordinates are not valid.")
                return False
            adjustedWall = (wall[0], adjustedWall[0], adjustedWall[1])

            if not (adjustedWall[1] != None and adjustedWall[1] < self.row - 2):
                print("Invalid input[a5]: Wall coordinates are not valid.")
                return False

            if not (adjustedWall[2] != None and adjustedWall[2] < self.column - 2):
                print("Invalid input[a6]: Wall coordinates are not valid.")
                return False

        return (adjustedMove, adjustedWall)

    def getPath(self, currentPosition, targetPosition):
        putanja = list()
        # da li se krecemo vertikalno
        if currentPosition[1] == targetPosition[1]:
            if currentPosition[0] > targetPosition[0]:
                return [
                    (currentPosition[0] - 1, currentPosition[1]),
                    (currentPosition[0] - 3, currentPosition[1]),
                    (currentPosition[0] - 4, currentPosition[1]),
                ]
            else:
                return [
                    (currentPosition[0] + 1, currentPosition[1]),
                    (currentPosition[0] + 3, currentPosition[1]),
                    (currentPosition[0] + 4, currentPosition[1]),
                ]
        # da li se krecemo horizontalno
        elif currentPosition[0] == targetPosition[0]:
            if currentPosition[1] > targetPosition[1]:
                return [
                    (currentPosition[0], currentPosition[1] - 1),
                    (currentPosition[0], currentPosition[1] - 3),
                    (currentPosition[0], currentPosition[1] - 4),
                ]
            else:
                return [
                    (currentPosition[0], currentPosition[1] + 1),
                    (currentPosition[0], currentPosition[1] + 3),
                    (currentPosition[0], currentPosition[1] + 4),
                ]
        # da li se krecemo dijagonalno
        # dole doseno
        if (currentPosition[0] + 2 == targetPosition[0]) and (
            currentPosition[1] + 2 == targetPosition[1]
        ):
            return [
                (currentPosition[0] + 1, currentPosition[1]),
                (currentPosition[0] + 2, currentPosition[1] + 1),
                (currentPosition[0] + 1, currentPosition[1] + 2),
                (currentPosition[0], currentPosition[1] + 1),
            ]
        # dole levo
        elif (currentPosition[0] + 2 == targetPosition[0]) and (
            currentPosition[1] - 2 == targetPosition[1]
        ):
            return [
                (currentPosition[0] + 1, currentPosition[1]),
                (currentPosition[0] + 2, currentPosition[1] - 1),
                (currentPosition[0] + 1, currentPosition[1] - 2),
                (currentPosition[0], currentPosition[1] - 1),
            ]
        # gore desno
        elif (currentPosition[0] - 2 == targetPosition[0]) and (
            currentPosition[1] + 2 == targetPosition[1]
        ):
            return [
                (currentPosition[0] - 1, currentPosition[1]),
                (currentPosition[0] - 2, currentPosition[1] + 1),
                (currentPosition[0] - 1, currentPosition[1] + 2),
                (currentPosition[0], currentPosition[1] + 1),
            ]
        # gore levo
        elif (currentPosition[0] - 2 == targetPosition[0]) and (
            currentPosition[1] - 2 == targetPosition[1]
        ):
            return [
                (currentPosition[0] - 1, currentPosition[1]),
                (currentPosition[0] - 2, currentPosition[1] - 1),
                (currentPosition[0] - 1, currentPosition[1] - 2),
                (currentPosition[0], currentPosition[1] - 1),
            ]

    def validMove(self, pawn, move, wall, state, pc=False):
        if move[0] < 0 or move[0] >= self.row or move[1] < 0 or move[1] >= self.column:
            return 10

        valid = None
        currentPosition = (
            state["X"]
            if pawn == "X"
            else state["x"]
            if pawn == "x"
            else state["O"]
            if pawn == "O"
            else state["o"]
        )

        # uzimaju se ciljna stanja trenutnog igraca radi lakse provere
        finish = None
        if pawn == "X" or pawn == "x":
            finish = (self.start_o1, self.start_o2)
        else:
            finish = (self.start_x1, self.start_x2)

        # da li se na nasem putu nalazi zid
        # da li se krecemo horizontalno

        # da li se na move vec nalazi neki igrac
        # da li se nalazi neka oznaka na tom mestu u matrici
        if (
            state["matrix"][move[0]][move[1]] == "x"
            or state["matrix"][move[0]][move[1]] == "X"
            or state["matrix"][move[0]][move[1]] == "o"
            or state["matrix"][move[0]][move[1]] == "O"
        ) and (move != finish[0] and move != finish[1]):
            if pc:
                print("Invalid move[d]: Pawn can not be moved on a taken space.")
            return 10

        statePath = copy.deepcopy(state)
        # provera da li je slobodno mesto za zid
        if wall != None:
            if wall[0] == "G":
                if (
                    state["matrix"][wall[1]][wall[2] + 1] == "ǁ"
                    or state["matrix"][wall[1] + 2][wall[2] + 1] == "ǁ"
                ):
                    if pc:
                        print("Invalid move[a]: There is already a wall on that spot.")
                    return False
            else:
                if (
                    state["matrix"][wall[1] + 1][wall[2]] == "═"
                    or state["matrix"][wall[1] + 1][wall[2] + 2] == "═"
                ):
                    if pc:
                        print("Invalid move[b]: There is already a wall on that spot.")
                    return False

        # pokusaj pomeranja za jedno polje

        # pomeranje van opsega
        if abs(currentPosition[0] - move[0]) + abs(currentPosition[1] - move[1]) == 2:
            if (
                (move[0] == 0 and currentPosition[0] == 2)
                or (move[0] == self.row - 1 and currentPosition[0] == self.row - 3)
                or (move[1] == 0 and currentPosition[1] == 2)
                or (
                    move[1] == self.column - 1 and currentPosition[1] == self.column - 3
                )
            ):
                return 10

            path = self.getPath(currentPosition, move)
            if (
                state["matrix"][path[0][0]][path[0][1]] == "═"
                or state["matrix"][path[0][0]][path[0][1]] == "ǁ"
            ):
                if pc:
                    print("Invalid move[e]: Pawn is blocked by a wall.")
                return 10

            # da li je sledece polje zapravo ciljno polje
            if move == finish[0] or move == finish[1]:
                self.playAIMove(pawn, move, wall, statePath)
                if wall != None:
                    if self.blockedPath(statePath, wall) == False:
                        # print(str(round(time.time() * 1000)) + " flood end")
                        if pc:
                            print("Invalid move[c]: Path to the finish is blocked.")
                        return False
                    # print(str(round(time.time() * 1000)) + " flood end")
                return True

            if (
                state["matrix"][path[1][0]][path[1][1]] == "═"
                or state["matrix"][path[1][0]][path[1][1]] == "ǁ"
            ):
                if pc:
                    print("Invalid move[f]: Pawn can not be moved only one space.")
                return 10

            # da li se na dva polja nalazi protivnicki igrac
            if (
                path[2] == state["X"]
                or path[2] == state["x"]
                or path[2] == state["O"]
                or path[2] == state["o"]
            ):
                self.playAIMove(pawn, move, wall, statePath)
                if wall != None:
                    if self.blockedPath(statePath, wall) == False:
                        # print(str(round(time.time() * 1000)) + " flood end")
                        if pc:
                            print("Invalid move[c]: Path to the finish is blocked.")
                        return False
                    # print(str(round(time.time() * 1000)) + " flood end")
                return True
            if pc:
                print("Invalid move[g]: Pawn can not be moved only one space.")
            return 10

        # da li se pomeramo za dva mesta
        if abs(currentPosition[0] - move[0]) + abs(currentPosition[1] - move[1]) != 4:
            if pc:
                print("Invalid move[h]: Pawn must be moved two spaces.")
            return 10

        path = self.getPath(currentPosition, move)

        if (
            state["matrix"][path[0][0]][path[0][1]] != "═"
            and state["matrix"][path[0][0]][path[0][1]] != "ǁ"
            and state["matrix"][path[1][0]][path[1][1]] != "═"
            and state["matrix"][path[1][0]][path[1][1]] != "ǁ"
        ):
            self.playAIMove(pawn, move, wall, statePath)
            if wall != None:
                if self.blockedPath(statePath, wall) == False:
                    # print(str(round(time.time() * 1000)) + " flood end")
                    if pc:
                        print("Invalid move[c]: Path to the finish is blocked.")
                    return False
                # print(str(round(time.time() * 1000)) + " flood end")
            return True

        if len(path) == 4:
            if (
                # todo smani provere na samo neophodne
                state["matrix"][path[2][0]][path[2][1]] != "═"
                and state["matrix"][path[2][0]][path[2][1]] != "ǁ"
                and state["matrix"][path[3][0]][path[3][1]] != "═"
                and state["matrix"][path[3][0]][path[3][1]] != "ǁ"
            ):
                self.playAIMove(pawn, move, wall, statePath)
                if wall != None:
                    if self.blockedPath(statePath, wall) == False:
                        # print(str(round(time.time() * 1000)) + " flood end")
                        print()
                        if pc:
                            print("Invalid move[c]: Path to the finish is blocked.")
                        return False
                    # print(str(round(time.time() * 1000)) + " flood end")
                return True

        if pc:
            print("Invalid move[i]: Pawn's jump is blocked by a wall.")
        return 10

    def blockedPath(self, state, wall):
        # pawnX == result[0]
        # pawnO == result[1]
        # targetX == result[2]
        # targetO == result[3]
        # oblast u koju se nalazi cilj za 0

        # print(str(round(time.time() * 1000)) + " flood start")

        if wall[0] == "G":
            num = 0
            if wall[1] == 0:
                num += 1

            if wall[1] != self.row - 3:
                if (
                    state["matrix"][wall[1] + 3][wall[2]] == horisontalWall
                    or state["matrix"][wall[1] + 3][wall[2] + 2] == horisontalWall
                    or state["matrix"][wall[1] + 4][wall[2] + 1] == verticalWall
                ):
                    num += 1

            if wall[1] == self.row - 3:
                num += 1

            if wall[1] != 0:
                if (
                    state["matrix"][wall[1] - 1][wall[2]] == horisontalWall
                    or state["matrix"][wall[1] - 1][wall[2] + 2] == horisontalWall
                    or state["matrix"][wall[1] - 2][wall[2] + 1] == verticalWall
                ):
                    num += 1

            if (
                state["matrix"][wall[1] + 1][wall[2]] == horisontalWall
                or state["matrix"][wall[1] + 1][wall[2] + 2] == horisontalWall
            ):
                num += 1

            if num < 2:
                return True

        elif wall[0] == "B":
            num = 0
            if wall[2] == 0:
                num += 1

            if wall[2] != self.column - 3:
                if (
                    state["matrix"][wall[1]][wall[2] + 3] == verticalWall
                    or state["matrix"][wall[1] + 2][wall[2] + 3] == verticalWall
                    or state["matrix"][wall[1] + 1][wall[2] + 4] == horisontalWall
                ):
                    num += 1

            if wall[2] == self.column - 3:
                num += 1

            if wall[2] != 0:
                if (
                    state["matrix"][wall[1]][wall[2] - 1] == verticalWall
                    or state["matrix"][wall[1] + 2][wall[2] - 1] == verticalWall
                    or state["matrix"][wall[1] + 1][wall[2] - 2] == horisontalWall
                ):
                    num += 1

            if (
                state["matrix"][wall[1]][wall[2] + 1] == verticalWall
                or state["matrix"][wall[1] + 2][wall[2] + 1] == verticalWall
            ):
                num += 1

            if num < 2:
                return True

        result = self.floodFill(self.start_x1, state)

        # da li su u oblast u koju se nalazi cilj za 0 svi pesaci i ciljevi oxa
        if result[3] == 2 and result[1] == 2:
            # da li su u oblast u koju se nalazi cilj za 0 svi pesaci i ciljevi ixa
            if result[0] == 2 and result[2] == 2:
                return True  # stanje je validno ( ima putanje za svakog pesaka )
            # da li je u oblast u koju se nalazi cilj za 0 zarobljen neki element ixa
            elif result[0] > 0 or result[2] > 0:
                return False
            # u oblast u koju se nalazi cilj za 0 ne postoji ni jedan element ixa
            else:
                # oblast u koju se nalazi cilj za x
                result = self.floodFill(self.start_o1, state)
                # da li su svi elementi ixa u oblasti gde se nalazi cilj za x
                if result[0] == 2 and result[2] == 2:
                    return True
        return False

    def floodFill(self, start, state):
        # pawnX = 0
        # pawnO = 0
        # targetX = 0
        # targetO = 0

        result = [0, 0, 0, 0]
        # obradi start
        # inkrementira odgovarajuce brojace
        if start == state["X"] or start == state["x"]:
            result[0] = result[0] + 1
        if start == state["O"] or start == state["o"]:
            result[1] = result[1] + 1
        if start == self.start_o1 or start == self.start_o2:
            result[2] = result[2] + 1
        if start == self.start_x1 or start == self.start_x2:
            result[3] = result[3] + 1
        state["matrix"][start[0]][start[1]] = "!"

        # self.showBoard(state)
        # rekurzivno pozivanje za okolna polja
        # levo
        if (
            start[1] - 2 >= 0
            and state["matrix"][start[0]][start[1] - 2] != "!"
            and state["matrix"][start[0]][start[1] - 1] != verticalWall
        ):
            result = list(
                map(
                    lambda x, y: x + y,
                    result,
                    self.floodFill((start[0], start[1] - 2), state),
                )
            )

        # desno
        if (
            start[1] + 2 < self.column
            and state["matrix"][start[0]][start[1] + 2] != "!"
            and state["matrix"][start[0]][start[1] + 1] != verticalWall
        ):
            result = list(
                map(
                    lambda x, y: x + y,
                    result,
                    self.floodFill((start[0], start[1] + 2), state),
                )
            )

        # gore
        if (
            start[0] - 2 >= 0
            and state["matrix"][start[0] - 2][start[1]] != "!"
            and state["matrix"][start[0] - 1][start[1]] != horisontalWall
        ):
            result = list(
                map(
                    lambda x, y: x + y,
                    result,
                    self.floodFill((start[0] - 2, start[1]), state),
                )
            )

        # dole
        if (
            start[0] + 2 < self.row
            and state["matrix"][start[0] + 2][start[1]] != "!"
            and state["matrix"][start[0] + 1][start[1]] != horisontalWall
        ):
            result = list(
                map(
                    lambda x, y: x + y,
                    result,
                    self.floodFill((start[0] + 2, start[1]), state),
                )
            )

        # gore levo
        if (
            start[0] - 2 >= 0
            and start[1] - 2 >= 0
            and state["matrix"][start[0] - 2][start[1] - 2] != "!"
        ):
            path = self.getPath(start, (start[0] - 2, start[1] - 2))

            if (
                state["matrix"][path[0][0]][path[0][1]] != horisontalWall
                and state["matrix"][path[1][0]][path[1][1]] != verticalWall
            ) or (
                state["matrix"][path[2][0]][path[2][1]] != horisontalWall
                and state["matrix"][path[3][0]][path[3][1]] != verticalWall
            ):

                result = list(
                    map(
                        lambda x, y: x + y,
                        result,
                        self.floodFill((start[0] - 2, start[1] - 2), state),
                    )
                )
        # gore desno
        if (
            start[0] - 2 >= 0
            and start[1] + 2 < self.column
            and state["matrix"][start[0] - 2][start[1] + 2] != "!"
        ):
            path = self.getPath(start, (start[0] - 2, start[1] + 2))

            if (
                state["matrix"][path[0][0]][path[0][1]] != horisontalWall
                and state["matrix"][path[1][0]][path[1][1]] != verticalWall
            ) or (
                state["matrix"][path[2][0]][path[2][1]] != horisontalWall
                and state["matrix"][path[3][0]][path[3][1]] != verticalWall
            ):

                result = list(
                    map(
                        lambda x, y: x + y,
                        result,
                        self.floodFill((start[0] - 2, start[1] + 2), state),
                    )
                )

        # dole levo
        if (
            start[0] + 2 < self.row
            and start[1] - 2 >= 0
            and state["matrix"][start[0] + 2][start[1] - 2] != "!"
        ):
            path = self.getPath(start, (start[0] + 2, start[1] - 2))

            if (
                state["matrix"][path[0][0]][path[0][1]] != horisontalWall
                and state["matrix"][path[1][0]][path[1][1]] != verticalWall
            ) or (
                state["matrix"][path[2][0]][path[2][1]] != horisontalWall
                and state["matrix"][path[3][0]][path[3][1]] != verticalWall
            ):

                result = list(
                    map(
                        lambda x, y: x + y,
                        result,
                        self.floodFill((start[0] + 2, start[1] - 2), state),
                    )
                )
        # dole desno
        if (
            start[0] + 2 < self.row
            and start[1] + 2 < self.column
            and state["matrix"][start[0] + 2][start[1] + 2] != "!"
        ):
            path = self.getPath(start, (start[0] + 2, start[1] + 2))

            if (
                state["matrix"][path[0][0]][path[0][1]] != horisontalWall
                and state["matrix"][path[1][0]][path[1][1]] != verticalWall
            ) or (
                state["matrix"][path[2][0]][path[2][1]] != horisontalWall
                and state["matrix"][path[3][0]][path[3][1]] != verticalWall
            ):

                result = list(
                    map(
                        lambda x, y: x + y,
                        result,
                        self.floodFill((start[0] + 2, start[1] + 2), state),
                    )
                )

        return result

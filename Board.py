import copy

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
            for x in range(0, row * 2)
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

    def isEnd(self):
        if (
            self.current_x1 == self.start_o1
            or self.current_x1 == self.start_o2
            or self.current_x2 == self.start_o1
            or self.current_x2 == self.start_o2
        ):
            print("")
            print("Player X won!")
            print("")
            return True
        if (
            self.current_o1 == self.start_x1
            or self.current_o1 == self.start_x2
            or self.current_o2 == self.start_x1
            or self.current_o2 == self.start_x2
        ):
            print("")
            print("Player O won!")
            print("")
            return True
        return False

    def showBoard(self):
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
                    print(self.matrix[x][y], end="")
                print("ǁ" + str(marking[x // 2]))
            else:
                for y in range(0, self.column):
                    if y == 0:
                        print("  ", end="")
                    print(self.matrix[x][y], end="")
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
        adjustedWall = self.adjustIndex((wall[1], wall[2]))
        if adjustedWall[0] == -1 or adjustedWall[1] == -1:
            print("Invalid input[a2]: Wall coordinates are not valid.")
            return False
        adjustedWall = (wall[0], adjustedWall[0], adjustedWall[1])

        # provera indeksa u obliku broja
        if not (adjustedMove[0] != None and adjustedMove[0] < self.row):
            print("Invalid input[a3]: Pawn coordinates are not valid.")
            return False

        if not (adjustedMove[1] != None and adjustedMove[1] < self.column):
            print("Invalid input[a4]: Pawn coordinates are not valid.")
            return False

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
                (currentPosition[0] - 1, currentPosition[1] - 2),
                (currentPosition[0] - 2, currentPosition[1] - 1),
                (currentPosition[0], currentPosition[1] - 1),
            ]

    def validMove(self, pawn, move, wall):

        currentPosition = (
            self.current_x1
            if pawn == "X"
            else self.current_x2
            if pawn == "x"
            else self.current_o1
            if pawn == "O"
            else self.current_o2
        )

        # uzimaju se ciljna stanja trenutnog igraca radi lakse provere
        finish = None
        if pawn == "X" or pawn == "x":
            finish = (self.start_o1, self.start_o2)
        else:
            finish = (self.start_x1, self.start_x2)

        # provera da li je slobodno mesto za zid
        if wall != None:
            self.tmpMatrix = copy.deepcopy(self.matrix)

            if wall[0] == "G":
                if (
                    self.matrix[wall[1]][wall[2] + 1] == "ǁ"
                    or self.matrix[wall[1] + 2][wall[2] + 1] == "ǁ"
                ):
                    print("Invalid move[a]: There is already a wall on that spot.")
                    return False
                self.tmpMatrix[wall[1]][wall[2] + 1] = verticalWall
                self.tmpMatrix[wall[1] + 2][wall[2] + 1] = verticalWall
            else:
                if (
                    self.matrix[wall[1] + 1][wall[2]] == "═"
                    or self.matrix[wall[1] + 1][wall[2] + 2] == "═"
                ):
                    print("Invalid move[b]: There is already a wall on that spot.")
                    return False
                self.tmpMatrix[wall[1] + 1][wall[2]] = horisontalWall
                self.tmpMatrix[wall[1] + 1][wall[2] + 2] = horisontalWall

            if self.blockedPath() == False:
                print("Invalid move[c]: Path to the finish is blocked.")
                return False

        # da li se na nasem putu nalazi zid
        # da li se krecemo horizontalno

        # da li se na move vec nalazi neki igrac
        # da li se nalazi neka oznaka na tom mestu u matrici
        if (
            self.matrix[move[0]][move[1]] == "x"
            or self.matrix[move[0]][move[1]] == "X"
            or self.matrix[move[0]][move[1]] == "o"
            or self.matrix[move[0]][move[1]] == "O"
        ) and (move != finish[0] and move != finish[1]):
            print("Invalid move[d]: Pawn can not be moved on a taken space.")
            return False

        # pokusaj pomeranja za jedno polje
        if abs(currentPosition[0] - move[0]) + abs(currentPosition[1] - move[1]) == 2:

            path = self.getPath(currentPosition, move)
            if (
                self.matrix[path[0][0]][path[0][1]] == "═"
                or self.matrix[path[0][0]][path[0][1]] == "ǁ"
            ):
                print("Invalid move[e]: Pawn is blocked by a wall.")
                return False

            # da li je sledece polje zapravo ciljno polje
            if move == finish[0] or move == finish[1]:
                return True

            if (
                self.matrix[path[1][0]][path[1][1]] == "═"
                or self.matrix[path[1][0]][path[1][1]] == "ǁ"
            ):
                print("Invalid move[f]: Pawn can not be moved only one space.")
                return False

            # da li se na dva polja nalazi protivnicki igrac
            if (
                path[2] == self.current_o1
                or path[2] == self.current_o2
                or path[2] == self.current_x1
                or path[2] == self.current_x2
            ):
                return True
            print("Invalid move[g]: Pawn can not be moved only one space.")
            return False

        # da li se pomeramo za dva mesta
        if abs(currentPosition[0] - move[0]) + abs(currentPosition[1] - move[1]) != 4:
            print("Invalid move[h]: Pawn must be moved two spaces.")
            return False

        path = self.getPath(currentPosition, move)

        if (
            self.matrix[path[0][0]][path[0][1]] != "═"
            and self.matrix[path[0][0]][path[0][1]] != "ǁ"
            and self.matrix[path[1][0]][path[1][1]] != "═"
            and self.matrix[path[1][0]][path[1][1]] != "ǁ"
        ):
            return True

        if len(path) == 4:
            if (
                # todo smani provere na samo neophodne
                self.matrix[path[2][0]][path[2][1]] != "═"
                and self.matrix[path[2][0]][path[2][1]] != "ǁ"
                and self.matrix[path[3][0]][path[3][1]] != "═"
                and self.matrix[path[3][0]][path[3][1]] != "ǁ"
            ):
                return True

        print("Invalid move[i]: Pawn's jump is blocked by a wall.")
        return False

    def blockedPath(self):
        # pawnX == result[0]
        # pawnO == result[1]
        # targetX == result[2]
        # targetO == result[3]

        # oblast u koju se nalazi cilj za 0
        result = self.floodFill(self.start_x1)

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
                result = self.floodFill(self.start_o1)
                # da li su svi elementi ixa u oblasti gde se nalazi cilj za x
                if result[0] == 2 and result[2] == 2:
                    return True
        return False

    def floodFill(self, start):
        # pawnX = 0
        # pawnO = 0
        # targetX = 0
        # targetO = 0

        result = [0, 0, 0, 0]
        # obradi start
        # inkrementira odgovarajuce brojace
        if start == self.current_x1 or start == self.current_x2:
            result[0] = result[0] + 1
        if start == self.current_o1 or start == self.current_o2:
            result[1] = result[1] + 1
        if start == self.start_o1 or start == self.start_o2:
            result[2] = result[2] + 1
        if start == self.start_x1 or start == self.start_x2:
            result[3] = result[3] + 1
        self.tmpMatrix[start[0]][start[1]] = "!"

        # rekurzivno pozivanje za okolna polja
        # levo
        if (
            start[1] - 2 >= 0
            and self.tmpMatrix[start[0]][start[1] - 2] != "!"
            and self.tmpMatrix[start[0]][start[1] - 1] != verticalWall
        ):
            result = list(
                map(
                    lambda x, y: x + y, result, self.floodFill((start[0], start[1] - 2))
                )
            )

        # desno
        if (
            start[1] + 2 < self.column
            and self.tmpMatrix[start[0]][start[1] + 2] != "!"
            and self.tmpMatrix[start[0]][start[1] + 1] != verticalWall
        ):
            result = list(
                map(
                    lambda x, y: x + y, result, self.floodFill((start[0], start[1] + 2))
                )
            )

        # gore
        if (
            start[0] - 2 >= 0
            and self.tmpMatrix[start[0] - 2][start[1]] != "!"
            and self.tmpMatrix[start[0] - 1][start[1]] != horisontalWall
        ):
            result = list(
                map(
                    lambda x, y: x + y, result, self.floodFill((start[0] - 2, start[1]))
                )
            )

        # dole
        if (
            start[0] + 2 < self.row
            and self.tmpMatrix[start[0] + 2][start[1]] != "!"
            and self.tmpMatrix[start[0] + 1][start[1]] != horisontalWall
        ):
            result = list(
                map(
                    lambda x, y: x + y, result, self.floodFill((start[0] + 2, start[1]))
                )
            )

        # gore levo
        if (
            start[0] - 2 >= 0
            and start[1] - 2 >= 0
            and self.tmpMatrix[start[0] - 2][start[1] - 2] != "!"
        ):
            path = self.getPath(start, (start[0] - 2, start[1] - 2))

            if (
                self.tmpMatrix[path[0][0]][path[0][1]] != horisontalWall
                and self.tmpMatrix[path[1][0]][path[1][1]] != verticalWall
            ) or (
                self.tmpMatrix[path[2][0]][path[2][1]] != horisontalWall
                and self.tmpMatrix[path[3][0]][path[3][1]] != verticalWall
            ):

                result = list(
                    map(
                        lambda x, y: x + y,
                        result,
                        self.floodFill((start[0] - 2, start[1] - 2)),
                    )
                )
        # gore desno
        if (
            start[0] - 2 >= 0
            and start[1] + 2 < self.column
            and self.tmpMatrix[start[0] - 2][start[1] + 2] != "!"
        ):
            path = self.getPath(start, (start[0] - 2, start[1] + 2))

            if (
                self.tmpMatrix[path[0][0]][path[0][1]] != horisontalWall
                and self.tmpMatrix[path[1][0]][path[1][1]] != verticalWall
            ) or (
                self.tmpMatrix[path[2][0]][path[2][1]] != horisontalWall
                and self.tmpMatrix[path[3][0]][path[3][1]] != verticalWall
            ):

                result = list(
                    map(
                        lambda x, y: x + y,
                        result,
                        self.floodFill((start[0] - 2, start[1] + 2)),
                    )
                )

        # dole levo
        if (
            start[0] + 2 < self.row
            and start[1] - 2 >= 0
            and self.tmpMatrix[start[0] + 2][start[1] - 2] != "!"
        ):
            path = self.getPath(start, (start[0] + 2, start[1] - 2))

            if (
                self.tmpMatrix[path[0][0]][path[0][1]] != horisontalWall
                and self.tmpMatrix[path[1][0]][path[1][1]] != verticalWall
            ) or (
                self.tmpMatrix[path[2][0]][path[2][1]] != horisontalWall
                and self.tmpMatrix[path[3][0]][path[3][1]] != verticalWall
            ):

                result = list(
                    map(
                        lambda x, y: x + y,
                        result,
                        self.floodFill((start[0] + 2, start[1] - 2)),
                    )
                )
        # dole desno
        if (
            start[0] + 2 < self.row
            and start[1] + 2 < self.column
            and self.tmpMatrix[start[0] + 2][start[1] + 2] != "!"
        ):
            path = self.getPath(start, (start[0] + 2, start[1] + 2))

            if (
                self.tmpMatrix[path[0][0]][path[0][1]] != horisontalWall
                and self.tmpMatrix[path[1][0]][path[1][1]] != verticalWall
            ) or (
                self.tmpMatrix[path[2][0]][path[2][1]] != horisontalWall
                and self.tmpMatrix[path[3][0]][path[3][1]] != verticalWall
            ):

                result = list(
                    map(
                        lambda x, y: x + y,
                        result,
                        self.floodFill((start[0] + 2, start[1] + 2)),
                    )
                )

        return result

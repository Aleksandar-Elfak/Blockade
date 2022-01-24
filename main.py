from Game import Game
from Player import Player

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


def tryParse(par):
    try:
        return int(par)
    except ValueError:
        return -1


def startGame():

    boardRow = tryParse(input("Input number of rows: "))
    if boardRow < 7 or boardRow > 22:
        print("Invalid rows")
        return False
    boardColumn = tryParse(input("Input number of columns: "))
    if boardColumn < 10 or boardColumn > 28:
        print("Invalid columns")
        return False

    X = input("Position of X: ")
    if not validParameters(X, marking, boardRow, boardColumn):
        print("invalid position")
        return False
    x = input("Position of x: ")
    if not validParameters(x, marking, boardRow, boardColumn):
        print("invalid position")
        return False
    O = input("Position of O: ")
    if not validParameters(O, marking, boardRow, boardColumn):
        print("invalid position")
        return False
    o = input("Position of o: ")
    if not validParameters(o, marking, boardRow, boardColumn):
        print("invalid position")
        return False
    walls = tryParse(input("Number of walls: "))
    if walls < 0 or walls > 18:
        print("Invalid number")
        return False
    player = input("Choose X or O: ")
    if not (player == "X" or player == "x"):
        if not (player == "O" or player == "o"):
            print("You must choose X or O")
            return False
    ai = None
    if player == "X" or player == "x":
        ai = "O"
    else:
        ai = "X"

    game = Game(
        boardRow,
        boardColumn,
        X.split(" "),
        x.split(" "),
        O.split(" "),
        o.split(" "),
        walls,
        player,
        ai,
    )
    # game = Game(7, 10, ("2", "2"), ("2", "9"), ("6", "2"), ("6", "9"), 6, "x", "O")
    game.play()


def validParameters(pos, marking, boardRow, boardColumn):
    tmpPos = pos.split(" ")
    if (
        len(tmpPos) != 2
        or marking.get(tmpPos[0]) == None
        or marking.get(tmpPos[0]) >= boardRow
        or marking.get(tmpPos[1]) == None
        or marking.get(tmpPos[1]) >= boardColumn
    ):
        return False
    return True


startGame()

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
        self.player_x = Player(num_wall, True if pc == "X" or pc == "x" else False)
        self.player_o = Player(num_wall, True if pc == "O" or pc == "o" else False)
        self.currentPlayer = self.player_x
        self.saveState()

    def showBoard(self):
        self.board.showBoard()
    
    def saveState(self):
        state = {
            "matrix" : self.board.matrix,
            "X" : self.board.current_x1,
            "x" : self.board.current_x2,
            "o" : self.board.current_o1,
            "O" : self.board.current_o2,
            "xGreenWall" : self.player_x.green_leftover,
            "xBlueWall" : self.player_x.blue_leftover,
            "oGreenWall" : self.player_o.green_leftover,
            "oBlueWall" : self.player_o.blue_leftover,
        }

    def isEnd(self, player):
        return self.board.isEnd(player)

    def validParameters(self, pawn, move, wall):
        move = move.split(sep=" ")

        if len(move) != 2:
            return -1

        if wall != None:
            wall = wall.split(" ")

            if len(wall) != 3:
                return -1
            wall = [wall[0], wall[1], wall[2]]  # suvisno

            if wall[0] != "G" and wall[0] != "B":
                return False

            if (wall[0] == "G" and self.currentPlayer.green_leftover == 0) or (
                wall[0] == "B" and self.currentPlayer.blue_leftover == 0
            ):
                return False

        if not (self.round_num % 2 == 0 and (pawn == "X" or pawn == "x")):
            if not (self.round_num % 2 == 1 and (pawn == "O" or pawn == "o")):
                print("Losa figura")
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
            return -1

        move = params[0]
        wall = params[1]

        if not self.validMove(pawn, move, wall):
            print("Invalid move.")
            return -1

        self.board.changeState(pawn, move, wall)

        if wallNum:
            self.reduceWall(wall)

        self.saveState()

        self.showBoard()

    def makeAMove(self):
        if self.currentPlayer.pc:
            self.humanMove()
        else:
            self.aiMove()

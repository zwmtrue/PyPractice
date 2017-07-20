#A tic tac board 3X3
import random
class game(object):
    def __init__(self):
        self.board = ["-"]*9

    def move(self, n, symbol):
        """this method takes in a move"""
        if not (0 <= n-1 < len(self.board)): return
        self.board[n - 1] = symbol

    def showboard(self):
        """print a 3X3 board"""
        row = ""
        for n in range(len(self.board)):
            s = self.board[n]
            row += s
            if (n + 1) % 3 == 0:
                row += "\n"
            else:
                row +="|"
        return row
    def isboardfull(self):
        """checks if the board is full"""
        moves = 0
        for s in self.board:
            if s != "-":
                moves += 1
        return moves == len(self.board)

    def ai_move(self):
        """ make a move for ai symbol O

        """
        try:
            n = 0








game1 = game()
print game1.showboard()
game1.move(1, "X")
print game1.showboard()
print game1.isboardfull()
while not game1.isboardfull():
    game1.ai_move()
    print game1.showboard()
print game1.showboard()




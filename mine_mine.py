#/usr/bin/python2
"""
A console game for mine sweeper, inspired by various tutorials online
"""

import random
class game(object):
    """
    A board obj
    """
    def __init__(self, n_col, n_row, n_mines):
        self.col = n_col
        self.row = n_row
        self.board = [[' '] * self.col for c in range(self.row)]
        #this is the board shows with every move
        self.mines = [[0] * self.col for c in range(self.row)]
        self.n_mines = n_mines
        self.adj_mines = [[0] * self.col for c in range(self.row)]
        self.setmines(self.n_mines)
        #0 IS safe, 1 is mine
        self.helpmsg = "please select a cell between: rows 1-" +\
                       str(self.row) + " and columns a-" + chr(ord('a') + self.col - 1) + " and type your selection. For example, to select cell a1 type \'a1\' if you want to flag the cell, add a letter \'f\' to the end, e.g. \'a1f\' "


        self.correctly_marked = 0
        self.cor_mark_lst = []
        self.wrong_loc_lst = []
        self.to_continue = True

    def in_range(self, r, c):
        return 0 <= r < self.row and 0 <= c < self.col

    def showboard(self,alt_board):
        """ print board"""
        grid_h = '   ' + (4 * self.col * '-') + '-'
        label_h = '     '
        for i in range(self.col):
            label_h = label_h + chr((ord('a') + i)) + '   '

        print(label_h + '\n' + grid_h)
        for r, i in enumerate(self.adj_mines):
            row = '{0:2} |'.format(r + 1)
            #row number

            for c in range(self.col):
                if alt_board is None:
                    row = row + ' ' + self.board[r][c] + ' |'
                elif alt_board.lower() == "final":
                    if self.board[r][c] == u"\u2691":
                        if self.mines[r][c] == 1:#flag and mine
                            row = row + ' ' + u'\u2713' + ' |' #Check
                        else:#flag and not mine
                            row = row + u"\u2691" + ' X|'#Flag and X
                    else:
                        if self.mines[r][c] == 1:#not flag and mine
                            row = row + ' ' + u"\U0001F4A3" + ' |'#Bomb
                        else:#not flag and not mine
                            row = row + ' ' + str(self.adj_mines[r][c]) + ' |'#same old
                else:#alt_board supplied
                    row = row + ' ' + str(alt_board[r][c]) + ' |'

            print(row + '{0:2}'.format(r + 1) + '\n' + grid_h)
        print(label_h)

    def setmines(self, n_mines):
        minelist = []
        while len(minelist) < n_mines:
            r, c = random.randint(0, self.row - 1), random.randint(0, self.col - 1)
            if [r, c] not in minelist:
                minelist.append([r, c])

        for r, c in minelist:
            self.mines[r][c] = 1
            r_lst = [r - 1, r - 1, r - 1,     r,     r, r + 1, r + 1, r + 1]
            c_lst = [c - 1,     c, c + 1, c - 1, c + 1, c - 1,     c, c + 1]
            for n in range(len(r_lst)):
                if self.in_range(r_lst[n],c_lst[n]):
                    try:
                        self.adj_mines[r_lst[n]][c_lst[n]] += 1
                    except IndexError:
                        print r_lst[n], c_lst[n]

    def dfs(self, r, c):
        """on correct mark, make all neighbour non-mine blocks visible """
        if not self.in_range(r, c): return
        if self.board[r][c] != ' ': return
        self.board[r][c] = str(self.adj_mines[r][c])
        if self.adj_mines[r][c] != 0:
            return

        self.dfs(r + 1, c)
        self.dfs(r, c + 1)
        self.dfs(r - 1, c)
        self.dfs(r, c - 1)

    def parse_input(self):
        """take input, validate, update board"""
        ip_str = raw_input("To show help message, please type \'help\', "
                           "to quit, type \'quit\'. \n")
        if ip_str is None or len(ip_str) > 4:
            print self.helpmsg
            return
        elif len(ip_str) == 4:
            if ip_str.lower() == "help":
                print self.helpmsg
                return
            elif ip_str.lower() == "quit":
                print "Bye"
                exit(0)
            else:
                print self.helpmsg
                return
        c, r, flag = int(ord(ip_str[0]) - ord('a')), int(ip_str[1]) - 1, False
        if len(ip_str) == 3:
            flag = True
        if not self.in_range(r, c):
            print "Input exceeds board sizes!\n", self.helpmsg
            return

        if self.board[r][c] != ' ':
            print "This is cell is already explored, try another one!"
            return

        if not flag:
            if self.mines[r][c] == 1:
                print "Game Over!"
                self.to_continue = False
            else:
                print "Good choice! All known safe zone revealed!"
                self.dfs(r, c)
        else:
            self.board[r][c] = u"\u2691" #flag
            if self.mines[r][c] == 1:
                self.correctly_marked += 1
        return

    def solved(self):
        return self.correctly_marked == self.n_mines




if __name__ == "__main__":
    while True:
        difficulty = raw_input("Welcome to Mine\n Select a difficulty level:\n 1: Easy\n 2: Medium\n 3: Hard\n 0: Quit\n")

        if len(difficulty) == 0 or len(difficulty) > 1:
            print "Invalid difficulty, please select again!"
            continue
        else:
            try:
                difficulty = int(difficulty)
            except ValueError:
                print "Invalid difficulty, please select again!"
                continue
            if 0 > difficulty or difficulty > 3:
                print "Invalid difficulty, please select again!"
                continue
            if difficulty == 1:
                game1 = game(8, 8, 8)
            elif difficulty == 2:
                game1 = game(16, 16, 32)
            elif difficulty == 3:
                game1 = game(32,32, 96)
            else:
                print "Bye!"
                exit(0)
            print game1.helpmsg

            while game1.to_continue and (not game1.solved()):
                game1.showboard(None)
                print "Please enter or flag a new cell."
                game1.parse_input()

            game1.showboard("final")
            sel = raw_input("To start a another game, type \'more\';\n to quit, hit \'Enter\'.\n")
            if "more" == sel.lower():
                continue
            else:
                print "Bye!"
                exit(0)






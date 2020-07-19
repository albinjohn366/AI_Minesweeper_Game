# MINESWEEPER GAME OUTLOOK
import random


class Minesweeper:
    mine_number = None

    def __init__(self, height=8, width=8, mines=15):
        self.mine_number = dict()
        self.full_set = set()
        self.height = height
        self.width = width
        self.mines = set()
        self.board = []
        self.mine_length = mines

    def board_setting(self):
        # Considering there are no mines in the board
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
                self.full_set.add((i, j))
            self.board.append(row)

        # Putting in mines in random spaces
        while True:
            if len(self.mines) == self.mine_length:
                break
            x = random.randint(0, self.height - 1)
            y = random.randint(0, self.width - 1)
            self.mines.add((x, y))
            self.board[x][y] = True

        # Numbering the cells with respect to mines
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) in self.mines:
                    continue
                mine_count = 0
                for i1 in range(i - 1, i + 2):
                    for j1 in range(j - 1, j + 2):
                        try:
                            if (i1, j1) == (i, j):
                                continue
                            elif i1 < 0 or j1 < 0:
                                continue
                            if self.board[i1][j1]:
                                mine_count += 1
                        except IndexError:
                            pass
                self.mine_number[(i, j)] = mine_count

    # Printing the board with numbers
    def print_board_with_num(self):
        for i in range(self.height):
            print('--' * self.width + '-')
            for j in range(self.width):
                if self.board[i][j]:
                    print('|X', end='')
                else:
                    print('|{}'.format(self.mine_number[(i, j)]), end='')
            print('|')
        print('--' * self.width + '-')

    # Printing the board without numbers
    def print_board(self, cells=None, mine_cell=None):
        if mine_cell is None:
            mine_cell = []
        for i in range(self.height):
            print('--' * self.width + '-')
            for j in range(self.width):
                if (i, j) in mine_cell:
                    print('|X', end='')
                elif (i, j) in cells:
                    print('|{}'.format(self.mine_number[(i, j)]), end='')
                else:
                    print('| ', end='')

            print('|')
        print('--' * self.width + '-')

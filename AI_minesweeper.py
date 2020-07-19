# AI FOR FINDING SOLUTION

from minesweeper_graphical_representation import *


def ai_operation_bridge(mine_number, cells, full_set, mines, mine_cells):
    global game
    global sentence
    guess = None
    game = Minesweeper()
    game.full_set = full_set
    game.mine_number = mine_number
    sentence = AI(cells)
    sentence.cells = cells
    sentence.mine_cell = mine_cells
    game.mines = mines
    while True:
        if guess in game.mines:
            sentence.cells.add(tuple(guess))
            result_text = 'AI guessed it wrong'
            result = (sentence.cells, sentence.mine_cell, result_text)
            return result
        elif guess:
            sentence.cells.add(tuple(guess))
        try:

            sentence.operations()
            if sentence.mine_cell == game.mines:
                result_text = 'AI won'
                result = (sentence.cells, sentence.mine_cell, result_text)
                return result
        except RecursionError:
            guess = sentence.guess()


class Sentence:
    cells = None
    mid_value = None
    neighbors = set()
    connections = dict()
    explored_cells = []
    mine_cell = set()
    explored_sets = []

    def __init__(self, cell):
        self.cells = set(cell)

    # Defining relation knowledge
    def knowledge(self):
        for sett in self.connections.keys():
            if sett in self.explored_sets:
                continue
            else:
                self.explored_sets.append(sett)

            if self.connections[sett] == 0:
                self.is_safe(sett)
                del self.connections[sett]
                return
            elif len(sett) == self.connections[sett]:
                self.is_mine(sett)
                return

            for subset in self.connections.keys():
                if sett == subset:
                    continue
                elif set(subset).issubset(set(sett)):
                    new_set = tuple(set(sett) - set(subset))
                    new_value = self.connections[sett] - self.connections[
                        subset]
                    del self.connections[sett]
                    self.connections[new_set] = new_value
                    return
                elif set(sett).issubset(set(subset)):
                    new_set = tuple(set(subset) - set(sett))
                    new_value = self.connections[subset] - self.connections[
                        sett]
                    del self.connections[subset]
                    self.connections[new_set] = new_value
                    return

    # Defining the knowledge that we know is safe
    def is_safe(self, safe):
        self.cells = self.cells.union(safe)

    # Defining the knowledge that we know is mine
    def is_mine(self, mine):
        self.mine_cell = self.mine_cell.union(mine)


class AI(Sentence):

    # Finding neighbors
    def find_neighbors(self, value_0):
        self.neighbors.clear()
        (i, j) = value_0
        self.mid_value = game.mine_number[value_0]

        if self.mid_value == 0:
            self.explored_cells.append(value_0)

        for i1 in range(i - 1, i + 2):
            for j1 in range(j - 1, j + 2):
                if (i1, j1) in self.mine_cell:
                    self.mid_value -= 1
                    continue
                elif (i1, j1) == (i, j) or (i1, j1) in self.cells:
                    continue
                elif i1 < 0 or j1 < 0 or i1 > 7 or j1 > 7:
                    continue
                self.neighbors.add((i1, j1))

        # If the cell is completely explored
        if not self.neighbors:
            self.explored_cells.append(value_0)
        self.connections[tuple(self.neighbors)] = self.mid_value

    # Performing operations for the known knowledge
    def operations(self):
        for value in self.cells:
            if value in self.explored_cells:
                continue
            self.find_neighbors(value)
        if len(self.cells) + len(self.mine_cell) < 64:
            self.knowledge()
            self.operations()

    # AI needs to guess when there is no clue
    def guess(self):
        guess = (game.full_set - self.cells - self.mine_cell).pop()
        return guess


if __name__ == '__main__':
    pass
    # cells = []
    # game = Minesweeper()
    # game.board_setting()
    #
    # while True:
    #     if len(cells) == 30:
    #         break
    #     x = random.randint(0, 7)
    #     y = random.randint(0, 7)
    #     if (x, y) in game.mines:
    #         continue
    #     cells.append((x, y))
    #
    # sentence = AI(cells)
    # game.print_board(cells, None)
    #
    # while True:
    #     try:
    #         sentence.operations()
    #         print()
    #         game.print_board(sentence.cells, sentence.mine_cell)
    #         if game.mines == sentence.mine_cell:
    #             print('You win')
    #         break
    #     except RecursionError:
    #         sentence.guess()

import tkinter

from AI_minesweeper import *
from my_minesweeper import *
from PIL import ImageTk, Image


# Opening random cells initially
def random_cells():
    open_cell = []
    while True:
        if len(open_cell) == 30:
            break
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        if (x, y) in game.mines:
            continue
        open_cell.append((x, y))
    return open_cell


# Loading images from path
def load_image(path, width_cell, height_cell):
    img = Image.open(path).resize((width_cell - 8, height_cell - 15),
                                  Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)


class Tkinter():
    def __init__(self, h, w, ch, cw):
        self.flag_frame = dict()
        self.flag = dict()
        self.new_frame = dict()
        self.button = dict()
        self.height = h
        self.width = w
        self.cell_height = ch
        self.cell_width = cw
        self.main_window = tkinter.Tk()
        self.main_window.title('MineSweeper')
        self.main_window.geometry('{}x{}+360+60'.format(width, height))
        self.flag_image = load_image('flag.png', self.cell_width,
                                     self.cell_height)
        self.mine_image = load_image('mine.png', self.cell_width,
                                     self.cell_height)

        self.main_window.rowconfigure(8, weight=1)

    # Printing the hidden values
    def hidden_layer(self):
        for value in sorted(list(game.full_set)):
            (row, column) = value
            frame = tkinter.Frame(self.main_window, relief='sunken',
                                  borderwidth=3,
                                  width=self.cell_width + 2,
                                  height=self.cell_height - 5,
                                  bg='red')
            frame.grid(row=row, column=column)

            if value in game.mine_number.keys():
                tkinter.Label(self.main_window, text=game.mine_number[value],
                              font=(None, 12),
                              bg='red').grid(row=row, column=column)

            if value in game.mines:
                tkinter.Label(frame, image=self.mine_image).grid(
                    row=0, column=0)

    # Adding button layer
    def final_frame_and_buttons(self):
        for value in sorted(list(game.full_set)):
            (row, column) = value
            self.new_frame[value] = tkinter.Frame(self.main_window,
                                                  width=self.cell_width,
                                                  background='grey',
                                                  height=self.cell_height - 5)
            self.new_frame[value].grid(row=row, column=column)

        for value in self.new_frame.keys():
            self.button[value] = tkinter.Button(self.new_frame[value],
                                                bg='grey', width=4, height=2,
                                                text='[]',
                                                relief='raised',
                                                borderwidth=3,
                                                command=lambda v=value:
                                                self.button_action(v))
            self.button[value].grid(row=0, column=0)
            self.button[value].bind('<Button-3>', lambda event, v=value:
            self.right_button(v))

    # Right click action
    def right_button(self, value):
        row, column = value
        self.flag_frame[value] = tkinter.Frame(self.main_window)
        self.flag_frame[value].grid(row=row, column=column)
        self.flag[value] = tkinter.Label(self.flag_frame[value],
                                         image=self.flag_image, width=33,
                                         height=36)
        self.flag[value].grid(row=0, column=0)
        self.flag[value].bind('<Button-3>',
                              lambda event, v=value: self.flag_destroy(v))

    # Removing flag
    def flag_destroy(self, value):
        self.flag_frame[value].destroy()

    # Defining button action
    def button_action(self, value):
        if value in game.mines:
            for value in game.mines:
                self.new_frame[value].destroy()
        else:
            self.new_frame[value].destroy()
            sentence.cells.add(value)

    # Defining action for known safe cells
    def known_cells_removal(self):
        for value in sentence.cells:
            self.new_frame[value].destroy()

    # Creating game control buttons
    def game_control(self):
        tkinter.Frame(self.main_window, bg='grey', height=60, width=320).grid(
            row=8, column=0, columnspan=8)
        new_game_button = tkinter.Button(self.main_window, text='Start\nGame',
                                         bg='green', borderwidth=3,
                                         command=self.known_cells_removal)
        new_game_button.grid(row=8, column=0, columnspan=2)
        global ai_button
        ai_button = tkinter.Button(self.main_window, text='Ask\nAI', bg='red',
                                   width=5, borderwidth=3,
                                   command=self.ai_operation)
        ai_button.grid(row=8, column=6, columnspan=2)

    def result_frame(self, text):
        tkinter.Label(self.main_window, text=text, bg='grey').grid(row=8,
                                                                   column=2,
                                                                   columnspan=4)

    # Passing information to AI
    def ai_operation(self):
        ai_button.configure(state='disabled')
        result = ai_operation_bridge(game.mine_number, sentence.cells,
                                     game.full_set, game.mines,
                                     sentence.mine_cell)
        sentence.cells, sentence.mine_cell, result_text = result
        self.known_cells_removal()
        self.mine_cell_marking()
        self.result_frame(result_text)

    # Marking mine cells founded by AI
    def mine_cell_marking(self):
        for value in sentence.mine_cell:
            row, column = value
            tkinter.Label(self.main_window, image=self.flag_image,
                          width=33, height=37).grid(row=row, column=column)


if __name__ == '__main__':
    game = Minesweeper()
    game.board_setting()

    height = 400
    width = 320
    cell_height = int(height / game.height - 2)
    cell_width = int(width / game.width - 2)
    cells = random_cells()

    sentence = AI(cells)
    viewer = Tkinter(height, width, cell_height, cell_width)
    viewer.hidden_layer()
    viewer.final_frame_and_buttons()
    viewer.game_control()

    viewer.main_window.mainloop()

import pygame
import sys
import time
from AI_minesweeper import *

pygame.init()


def result(res_text):
    smallest_font = pygame.font.Font(my_font, 15)
    result_text = smallest_font.render(res_text, True, RED)
    result_text_rect = result_text.get_rect()
    result_text_rect.center = (width * (3 / 4) + 50, height * (3 / 4))
    window.blit(result_text, result_text_rect)


# Colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)

# Defining screen
size = (width, height) = (600, 400)
window = pygame.display.set_mode(size)
window.fill(BLACK)

# Setting icon and name
icon = pygame.image.load('mine.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Minesweeper')

# Fonts
my_font = 'OpenSans-Regular.ttf'
small_font = pygame.font.Font(my_font, 20)
medium_font = pygame.font.Font(my_font, 28)
large_font = pygame.font.Font(my_font, 40)

# Board Size
board_padding = 20
board_width = int((2 / 3) * width - (board_padding * 2))
board_height = int(height - (board_padding * 2) - 20)
cell_width = int(board_width / 8)
cell_height = int(board_height / 8)
board_origin = (board_padding, board_padding)

# Class Minesweeper
game = Minesweeper()
game.board_setting()

# Random cell view
cells = []
flag_cell = []


def random_cells(cell):
    while True:
        if len(cell) >= 30:
            break
        a = random.randint(0, 7)
        b = random.randint(0, 7)
        if (a, b) in game.mines:
            continue
        cell.append((a, b))
    return cell


# Class Sentence
sentence = AI(cells)

# Images
mine_image = pygame.transform.scale(pygame.image.load('mine.png'),
                                    (cell_width, cell_height))
flag_image = pygame.transform.scale(pygame.image.load('flag.png'),
                                    (cell_width, cell_height))

# Initialisation
instructions = True
lost = False
play_game_action = True
ask_ai_action = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    if instructions:
        # Title
        title = large_font.render('Play Minesweeper', True, WHITE)
        title_rect = title.get_rect()
        title_rect.center = (int(width / 2), 50)
        window.blit(title, title_rect)

        # Start Game Box
        start_game_box = pygame.Rect(width / 4, height * (3 / 4), width / 2, 70)
        start_game_text = medium_font.render('Start Game', True, BLACK)
        start_game_text_rect = start_game_text.get_rect()
        start_game_text_rect.center = start_game_box.center
        pygame.draw.rect(window, WHITE, start_game_box)
        window.blit(start_game_text, start_game_text_rect)

        # Rules
        rules = ['Click a cell to reveal it',
                 'Flag a cell that you think is mine',
                 'Find all mines']
        row_height = 150
        for rule in rules:
            row = small_font.render(rule, True, WHITE)
            row_rect = row.get_rect()
            row_rect.center = (width / 2, row_height)
            window.blit(row, row_rect)
            row_height += 30

        # Checking the position where the mouse is pressed
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            x, y = pygame.mouse.get_pos()
            if start_game_box.collidepoint(x, y):
                instructions = False
                time.sleep(0.3)
                window.fill(BLACK)
        pygame.display.update()
        continue

    # Board rectangle
    board = pygame.Rect(board_origin[0], board_origin[1], board_width + 3,
                        board_height)
    pygame.draw.rect(window, WHITE, board)

    # Hidden numbers and mines
    unit_cell = dict()
    for i in range(0, 8):
        for j in range(0, 8):
            # Finding the current position
            cell_position = (board_origin[0] + (j * cell_width) + 2,
                             board_origin[0] + (i * cell_height) + 2)

            # Determining the rectangle frame
            cell = pygame.Rect(cell_position[0], cell_position[1],
                               cell_width - 1, cell_height - 1)
            pygame.draw.rect(window, GREY, cell)

            # Marking mines
            if (i, j) in game.mines:
                window.blit(mine_image, cell)
            else:
                text = small_font.render(str(game.mine_number[(i, j)]), True,
                                         BLACK)
                text_rect = text.get_rect()
                text_rect.center = cell.center
                window.blit(text, text_rect)

            # Hiding unknown cells
            if (i, j) not in sentence.cells:
                unit_cell[(i, j)] = pygame.Rect(cell_position[0],
                                                cell_position[1],
                                                cell_width - 1, cell_height - 1)
                pygame.draw.rect(window, GREY, unit_cell[(i, j)])

            # Adding flags
            if (i, j) in flag_cell:
                window.blit(flag_image, unit_cell[(i, j)])

    if not lost:
        # Play game button
        play_game_rect = pygame.Rect(width * (3 / 4) - 10, height / 4, 120, 50)
        play_game_text = small_font.render('Play Game', True, BLACK)
        play_game_text_rect = play_game_text.get_rect()
        play_game_text_rect.center = play_game_rect.center
        pygame.draw.rect(window, WHITE, play_game_rect)
        window.blit(play_game_text, play_game_text_rect)

        # Ask AI button
        ask_ai_rect = pygame.Rect(width * (3 / 4) - 10, height * (1 / 2), 120, 50)
        ask_ai_text = small_font.render('Ask AI', True, BLACK)
        ask_ai_text_rect = ask_ai_text.get_rect()
        ask_ai_text_rect.center = ask_ai_rect.center
        pygame.draw.rect(window, WHITE, ask_ai_rect)
        window.blit(ask_ai_text, ask_ai_text_rect)

        # Checking if mouse is pressed
        left, _, right = pygame.mouse.get_pressed()

        # If Play Game Button is pressed
        if left == 1 and play_game_action:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if play_game_rect.collidepoint(mouse_x, mouse_y):
                sentence.cells = sentence.cells.union(*[random_cells(cells)])
                play_game_action = False
                ask_ai_action = True

        # If any of the hidden cells are pressed
        if left == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for key, value in unit_cell.items():
                if value.collidepoint(mouse_x, mouse_y):
                    if key not in game.mines and key not in flag_cell:
                        sentence.cells.add(key)
                        del unit_cell[key]
                        break
                    if key not in flag_cell and key in game.mines:
                        sentence.cells = sentence.cells.union(tuple(game.mines))
                        result("""YOU LOST""")
                        lost = True
                        break

        # If AI button is pressed
        if left == 1 and ask_ai_action:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if ask_ai_rect.collidepoint(mouse_x, mouse_y):
                result_ai = ai_operation_bridge(game.mine_number,
                                             sentence.cells, game.full_set,
                                             game.mines, sentence.mine_cell)
                sentence.cells, sentence.mine_cell, result_txt = result_ai
                result(result_txt)
                for item in sentence.cells:
                    if item in flag_cell:
                        flag_cell.remove(item)
                for item in sentence.mine_cell:
                    flag_cell.append(item)
                ask_ai_action = False

        # If Right click is done
        if right == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for key, value in unit_cell.items():
                if value.collidepoint(mouse_x, mouse_y):
                    if key not in flag_cell:
                        flag_cell.append(key)
                        break
                    else:
                        flag_cell.remove(key)
                        break
            time.sleep(0.1)
    pygame.display.update()

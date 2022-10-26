from random import *

class GameParts(object):
    my_board = 'my board'
    enemy_board = 'enemy board'

class Kletka(object):
    empty_kletka = ("0")
    ship_kletka =("■")
    destroyed_kletka = ("x")
    miss_kletka = ("T")

class Board(object):
    def __init__(self, size=6):
        self.my_board = [[Kletka.empty_kletka for _ in range(size)] for _ in range(size)]
        self.enemy_board = [[Kletka.empty_kletka for _ in range(size)] for _ in range(size)]

    def get_game_part(self, element):
        if element == GameParts.my_board:
            return self.my_board
        if element == GameParts.enemy_board:
            return self.enemy_board

    def draw_board(self, element):
        board = self.get_game_part(element)

        for x in range(-1, self.size):
            for y in range(-1, self.size):
                if x == -1 and y == -1:
                    print("  ", end="")
                    continue
                if x == -1 and y >= 0:
                    print(y + 1, end=" ")
                    continue
                if x >= 0 and y == -1:
                    print([x], end='') #Обозначение рядов
                    continue
                print(" " + str(board[x][y]), end='') #Обозначение строк
            print("")
        print("")



    def check_ship_fits(self, ship, element):

        board = self.get_game_part(element)

        if ship.x + ship.height - 1 >= self.size or ship.x < 0 or ship.y + ship.width - 1 >= self.size or ship.y < 0:
            return False

        x = ship.x
        y = ship.y
        width = ship.width
        height = ship.height

        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                if str(field[p_x][p_y]) == Cell.miss_cell:
                    return False

        for p_x in range(x - 1, x + height + 1):
            for p_y in range(y - 1, y + width + 1):
                if p_x < 0 or p_x >= len(field) or p_y < 0 or p_y >= len(field):
                    continue
                if str(field[p_x][p_y]) in (Cell.ship_cell, Cell.destroyed_ship):
                    return False

        return True






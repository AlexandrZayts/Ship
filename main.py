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
                    print(Game.letters[x], end='')
                    continue
                print(" " + str(board[x][y]), end='')
            print("")

    print("")
    def check_ship_pos(self, ship, element):
        board = self.get_game_part(element)
        if ship.x + ship.height - 1 >= self.size or ship.x < 0 or ship.y + ship.width - 1 >= self.size or ship.y < 0:
            return False
        x = ship.x
        y = ship.y
        width = ship.width
        height = ship.height
        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                if str(board[p_x][p_y]) == Cell.miss_cell:
                    return False

        for p_x in range(x - 1, x + height + 1):
            for p_y in range(y - 1, y + width + 1):
                if p_x < 0 or p_x >= len(board) or p_y < 0 or p_y >= len(board):
                    continue
                if str(board[p_x][p_y]) in (Kletka.ship_kletka, Kletka.destroyed_kletka):
                    return False
        return True
    def add_ship_to_board(self, ship, element):

        board = self.get_game_part(element)

        x, y = ship.x, ship.y
        width, height = ship.width, ship.height

        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                board[p_x][p_y] = ship
    def recalculate_my_board(self, available_ships):
        self.my_board = [[1 for _ in range(self.size)] for _ in range(self.size)]

        for x in range(self.size):
            for y in range(self.size):
                if self.enemy_board[x][y] == Kletka.destroyed_kletka:

                    self.my_board[x][y] = 0

                    if x - 1 >= 0:
                        if y - 1 >= 0:
                            self.my_board[x - 1][y - 1] = 0
                        self.my_board[x - 1][y] *= 50
                        if y + 1 < self.size:
                            self.my_board[x - 1][y + 1] = 0

                    if y - 1 >= 0:
                        self.my_board[x][y - 1] *= 50
                    if y + 1 < self.size:
                        self.my_board[x][y + 1] *= 50

                    if x + 1 < self.size:
                        if y - 1 >= 0:
                            self.my_board[x + 1][y - 1] = 0
                        self.my_board[x + 1][y] *= 50
                        if y + 1 < self.size:
                            self.my_board[x + 1][y + 1] = 0
        for ship_size in available_ships:
            ship = Ship(ship_size, 1, 1, 0)
            for x in range(self.size):
                for y in range(self.size):
                    if self.enemy_board[x][y] in (Kletka.destroyed_kletka, Kletka.miss_kletka) or self.my_board[x][y] == 0:
                        self.my_board[x][y] = 0
                        continue
                    for rotation in range(0, 4):
                        ship.set_position(x, y, rotation)
                        if self.check_ship_fits(ship, GameParts.enemy_board):
                            self.my_board[x][y] += 1

class Game(object):
    letters = ("1", "2", "3", "4", "5", "6")
    ships_all = [1, 1, 1, 2, 2, 3]
    board_size = 6
    def __init__(self):
        self.players = []
        self.first_player = None #Я
        self.second_player = None #Компьютер
        self.status = "Игра не началась"
    def start_game(self):
        self.first_player = self.players[0]
        self.second_player = self.players[1]
    def switch_players(self):
        self.first_player, self.second_player = self.second_player, self.first_player
    def game_status(self):
        if self.status == 'Игра не началась' and len(self.players) >= 2:
            self.status = 'Игра в процессе'
            self.start_game()
            return True
        if self.status == 'Игра в процессе' and len(self.second_player.ships) == 0:
            self.status = 'Конец игры'
            return True
    def add_player(self, player):
        player.board = Board(Game.board_size)
        player.enemy_ships = list(Game.ships_all)
        self.ships_setup(player)

        self.players.append(player)
    def ships_setup(self, player):
        for ship_size in Game.ships_all:
            ship = Ship(ship_size, 0, 0, 0)

    def draw(self):
        if not self.first_player.is_ai:
            self.first_player.board.draw_board(GameParts.my_board)
            self.first_player.board.draw_board(GameParts.enemy_board)
        for line in self.first_player:
            print(line)
class Player(object):

    def __init__(self, name, is_ai, skill, auto_ship):
        self.name = name
        self.is_ai = is_ai
        self.auto_ship_setup = auto_ship
        self.skill = skill
        self.message = []
        self.ships = []
        self.enemy_ships = []
        self.board = None
    def get_input(self, input_type):
        if input_type == "shot":
            if self.is_ai:
                if self.skill == 0:
                    x, y = randrange(0, self.board.size), randrange(0, self.board.size)
            else:
                user_input = input().upper().replace(" ", "")
                x, y = user_input[0].upper(), user_input[1:]
                if x not in Game.letters or not y.isdigit() or int(y) not in range(1, Game.board_size + 1):
                    print('Неправильная клетка для выстрела')
                    return 500, 0
                x = Game.letters.index(x)
                y = int(y) - 1
            return x, y
    def make_shot(self, target_player):
        sx, sy = self.get_input('shot')
        if sx + sy == 500 or self.board.enemy_board[sx][sy] != Kletka.empty_kletka:
            return 'retry'
        shot_res = target_player.receive_shot((sx, sy))
        if shot_res == 'miss':
            self.board.enemy_board[sx][sy] = Kletka.miss_kletka
        if shot_res == 'get':
            self.board.enemy_board[sx][sy] = Kletka.destroyed_kletka
        self.board.recalculate_my_board(self.enemy_ships)
        return shot_res

    # здесь игрок будет принимать выстрел
    # как и в жизни игрок должен отвечать (возвращать) результат выстрела
    # попал (return "get") промазал (return "miss") или убил корабль (тогда возвращаем целиком корабль)
    # так проще т.к. сразу знаем и координаты корабля и его длину
    def receive_shot(self, shot):

        sx, sy = shot

        if type(self.board.my_board[sx][sy]) == Ship:
            ship = self.board.my_board[sx][sy]
            ship.hp -= 1

            if ship.hp <= 0:
                self.board.mark_destroyed_ship(ship, GameParts.my_board)
                self.ships.remove(ship)
                return ship

            self.board.my_board[sx][sy] = Kletka.destroyed_kletka
            return 'get'

        else:
            self.board.my_board[sx][sy] = Kletka.miss_kletka
            return 'miss'

class Ship:
    def __init__(self, size, x, y, rotation):
        self.size = size
        self.hp = size
        self.x = x
        self.y = y
        self.rotation = rotation
        self.set_rotation(rotation)

    def __str__(self):
        return Kletka.ship_kletka

    def set_position(self, x, y, r):
        self.x = x
        self.y = y
        self.set_rotation(r)

    def set_rotation(self, r):
        self.rotation = r
        if self.rotation == 0:
            self.width = self.size
            self.height = 1
        elif self.rotation == 1:
            self.width = 1
            self.height = self.size
        elif self.rotation == 2:
            self.y = self.y - self.size + 1
            self.width = self.size
            self.height = 1
        elif self.rotation == 3:
            self.x = self.x - self.size + 1
            self.width = 1
            self.height = self.size
if __name__ == '__main__':
    players = []
    players.append(Player(name='Игрок', is_ai=False, auto_ship=True, skill=1))
    players.append(Player(name='Компьютер', is_ai=True, auto_ship=True, skill=1))
    game = Game()
    while True:
        game.status_check()
        if game.status == "Игра не началась":
            game.add_player(players.pop(0))
        if game.status == 'Игра в процессе':
           print("Введите клетку для выстрела x и y: ")
           game.draw()
           shot_result = game.first_player.make_shot(game.second_player)
            if shot_result == 'get':
                game.switch_players()
                print("Вы не попали, ход противника")
                continue
            elif shot_res == 'miss':
                print("Вы попали по кораблю противника введите для следующего выстрела клетку x и y : ")
                continue
            elif shot_res == 'get':
                print("Противник попал по вашему кораблю, ожидайте свой ход")
                continue
            elif shot_res == 'miss':
                game.switch_players()
                print("Противник не попал, ваш ход, введите клетку для выстрела x и y: ")
                continue
            else
               print("Непредвиденная ситуация")


        if game.status == 'Конец игры':
            game.second_player.board.draw_board(FieldPart.my_board)
            game.first_player.board.draw_board(FieldPart.my_board)
            print('Это был последний корабль, {}'.format(game_status))
            break

    input('')
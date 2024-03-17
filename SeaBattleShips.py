import random

class Ship:
    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.coordinates = []
        self.hits = 0
    def check_hit(self, hit_x, hit_y):
        if (hit_x, hit_y) in self.coordinates:
            print(f"Попадание! {self.name} корабль был подбит.")
            self.coordinates.remove((hit_x, hit_y))
            if not self.coordinates:
                print(f"Корабль {self.name} был потоплен.")
            return True
        else:
            return False

    def hit(self):
        self.hits += 1

    def is_sunk(self):
        return self.hits == self.length


class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [['O' for _ in range(size)] for _ in range(size)]
        self.ships = []

    def is_valid_coordinates(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def place_ship(self, ship, coordinates, orientation):
        ship_coordinates = []
        x, y = coordinates

        for i in range(ship.length):
            if orientation == 'horizontal':
                if not self.is_valid_coordinates(x + i, y):
                    return False
                if self.grid[y][x + i] != 'O':
                    return False
                ship_coordinates.append((x + i, y))
            elif orientation == 'vertical':
                if not self.is_valid_coordinates(x, y + i):
                    return False
                if self.grid[y + i][x] != 'O':
                    return False
                ship_coordinates.append((x, y + i))
            else:
                return False

        for coord in ship_coordinates:
            self.grid[coord[1]][coord[0]] = 'X'

        ship.coordinates = ship_coordinates
        self.ships.append(ship)
        return True

    def hide_ships(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == "X":
                    self.grid[row][col] = "O"

    def display_grid(self):
        colors = {
            'O': '\033[94mO\033[0m',
            'X': '\033[91mX\033[0m',
            'V': '\033[92mV\033[0m'
        }

        board = "     0 1 2 3 4 5 6 7 8 9\n"
        for i in range(self.size):
            row = f"{i}  |"
            for j in range(self.size):
                color = colors.get(self.grid[i][j], '\033[92mV\033[0m')
                row += f" {color}"
            board += row + "\n"
        print(board)
    def check_hit(self, coordinates):
        x, y = coordinates

        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            print("Выстрел за пределами доски!")
            return False

        if self.grid[y][x] == 'X':
            print("Попадание!")
            self.grid[y][x] = ' V'
            self.check_sunk_ships()
            return True
        elif self.grid[y][x] == 'O' or self.grid[y][x] == 'M':
            print("Мимо!")
            self.grid[y][x] = 'M'
            return False
        else:
            print("Вы уже заняли эту позицию.")
            return False

    def check_sunk_ships(self):
        for ship in self.ships:
            if all(self.grid[y][x] == 'H' for x, y in ship.coordinates):
                print(f"Корабль '{ship.name}' потоплен!")
    def all_ships_sunk(self):
        for ship in self.ships:
            if not ship.is_sunk():
                return False
        return True

    def check_game_over(self):
        if self.all_ships_sunk():
            print("Игра окончена. Все корабли потоплены!")

class ComputerPlayer():
    def __init__(self):
        pass


    def attack(self, enemy_board):
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        coordinates = (x, y)
        print(f"Ход компьютера: {coordinates}")
        enemy_board.check_hit(coordinates)


class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board(10)

    def attack(self, enemy_board):
        while True:
            try:
                x = int(input("Введите координату столбца для атаки: "))
                y = int(input("Введите координату строки для атаки:  "))
                coordinates = (x, y)
                if x < 0 or x >= 10 or y < 0 or y >= 10:
                    print("Некоректные координаты. Повторите попытку")
                    continue

                if enemy_board.check_hit(coordinates):
                    print('Вы попали по кораблю, ваш ход продолжается')
                    while coordinates == self.board.check_hit('X'):
                        x = int(input("Введите координату столбца для атаки: "))
                        y = int(input("Введите координату строки для атаки:  "))
                        coordinates = (x, y)

                else:
                    print('Вы промахнулись, ваш ход завершается')
                    break
            except ValueError:
                pass

        enemy_board.display_grid()
class Game:
    def __init__(self):
        self.player = Player("Player")
        self.player_board = Board(10)
        self.computer_board = Board(10)
        self.computer_player = ComputerPlayer()

    def place_ships(self):
        ship_names = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
        ship_lengths = [5, 4, 3, 3, 2]

        for i in range(5):
            player_ship = Ship(ship_names[i], ship_lengths[i])
            computer_ship = Ship(ship_names[i], ship_lengths[i])

            player_coordinates = (random.randint(0, 9), random.randint(0, 9))
            computer_coordinates = (random.randint(0, 9), random.randint(0, 9))

            player_orientation = random.choice(['horizontal', 'vertical'])
            computer_orientation = random.choice(['horizontal', 'vertical'])

            while not self.player_board.place_ship(player_ship, player_coordinates, player_orientation):
                player_coordinates = (random.randint(0, 9), random.randint(0, 9))
                player_orientation = random.choice(['horizontal', 'vertical'])

            while not self.computer_board.place_ship(computer_ship, computer_coordinates, computer_orientation):
                computer_coordinates = (random.randint(0, 9), random.randint(0, 9))
                computer_orientation = random.choice(['horizontal', 'vertical'])

    def play_game(self):
        print("Начнем игру!")
        self.place_ships()

        current_player = 1
        while not self.player_board.all_ships_sunk() and not self.computer_board.all_ships_sunk():
            print("\nХод игрока", current_player)
            if current_player == 1:
                print("\nВаша доска:")
                self.player_board.display_grid()
                print("\nДоска компьютера:")
                self.computer_board.hide_ships()
                self.computer_board.display_grid()


                print("\nВаш ход:")
                hit_result = self.player.attack(self.computer_board)
                while hit_result == "HIT":
                    print("\nПродолжайте ход после попадания!")
                    hit_result = self.player.attack(self.computer_board)
                    self.player_board.check_sunk_ships()

            else:
                self.computer_player.attack(self.player_board)
            current_player = 2 if current_player == 1 else 1

        if self.player_board.all_ships_sunk():
            print("\nКомпьютер победил!")
        else:
            print("\nВы победили!")

game = Game()
game.play_game()

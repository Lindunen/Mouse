'''
файл содержит данные о классе Level игры кошки-мышки
'''
import pygame
import random
from cat import Cat

class Level:
    '''уровень игры'''

    def __init__(self):
        '''инициализируем переменные класса'''
        sizeW = 25
        sizeH = 20
        self.width = sizeW
        self.height = sizeH
        self.get_coins = 0 # счётчик монеток
        self.move_timer = 0 # останавливаем кота
        self.buff = False # флаг остановлен ли кот
        # создаем матрицу - это и есть карта уровня, разные числовые значения отвечают за разные объекты
        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]
        # загружаем спрайты
        self.ground_image = pygame.image.load("ground.png")
        self.wall_image = pygame.image.load("wall.png")
        self.obstacle_image = pygame.image.load("obstacle.png")
        self.coin_image = pygame.image.load("coin.png")
        self.cheese_image = pygame.image.load("cheese.png")
        self.mouse_image = pygame.image.load("mouse.png")
        self.cat_image = pygame.image.load("cat.png")
        self.exit_image = pygame.image.load("exit.png")
        # задаём позицию игрока, кота, выхода
        self.player_pos = (self.width - 2, self.height - 2)
        self.cat_pos = (2, 2)
        self.exit_pos = (1, 1)

    def generate(self):
        '''генерация стен вокруг края уровня'''
        for x in range(self.width):
            self.grid[0][x] = 1
            self.grid[self.height - 1][x] = 1
        for y in range(self.height):
            self.grid[y][0] = 1
            self.grid[y][self.width - 1] = 1

        # размещение выхода
        exit_placed = False
        while not exit_placed:
            x = 1
            y = 1
            self.grid[y][x] = 5  # выход
            self.exit_pos = (x, y)
            exit_placed = True

        # генерация объектов (препятствий, монет, сыра и выхода)
        num_obstacles = int((self.width * self.height) // 15)
        num_coins = 3
        num_cheese = 2
        x_range = range(1, self.width - 1)
        y_range = range(1, self.height - 1)

        # генерация препятствий
        i = 0
        while i != num_obstacles:
            x = random.choice(x_range)
            y = random.choice(y_range)
            if self.grid[y][x] == 0 and x != 2 and y != 2 and x != self.width - 2 and x != self.height - 2: # генерим препятствия только на земле и осталвяем свободными клетки игрока и кота
                self.grid[y][x] = 2  # препятствие
                i += 1

        # генерация монет
        i = 0
        while i != num_coins:
            x = random.choice(x_range)
            y = random.choice(y_range)
            if self.grid[y][x] == 0:
                self.grid[y][x] = 3  # монета
                i += 1

        # генерация сыра
        i = 0
        while i != num_cheese:
            x = random.choice(x_range)
            y = random.choice(y_range)
            if self.grid[y][x] == 0:
                self.grid[y][x] = 4  # сыр
                i += 1

    def draw(self, screen):
        '''отрисовываем землю'''
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 0:
                    screen.blit(self.ground_image, (x * 32, y * 32))

        # отрисовываем остальные объекты на земле (спрайт объекта поверх спрайта земли)
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 1: # стена
                    screen.blit(self.wall_image, (x * 32, y * 32))
                elif self.grid[y][x] == 2: # препятствие (дерево/куст)
                    screen.blit(self.ground_image, (x * 32, y * 32))
                    screen.blit(self.obstacle_image, (x * 32, y * 32))
                elif self.grid[y][x] == 3: # монетка
                    screen.blit(self.ground_image, (x * 32, y * 32))
                    screen.blit(self.coin_image, (x * 32, y * 32))
                elif self.grid[y][x] == 4: # сыр
                    screen.blit(self.ground_image, (x * 32, y * 32))
                    screen.blit(self.cheese_image, (x * 32, y * 32))
                elif self.grid[y][x] == 5: # выход
                    screen.blit(self.ground_image, (x * 32, y * 32))
                    screen.blit(self.exit_image, (x * 32, y * 32))
                elif self.grid[y][x] == 6: # игрок (мышка)
                    screen.blit(self.ground_image, (x * 32, y * 32))
                    screen.blit(self.mouse_image, (x * 32, y * 32))
                elif self.grid[y][x] == 7: # враг (кот)
                    screen.blit(self.ground_image, (x * 32, y * 32))
                    screen.blit(self.cat_image, (x * 32, y * 32))

    def move_player(self, dx, dy):
        '''dx, dy принимают значения в зависимости от нажатой стрелки на клавиатуре (это происходит в цикле while, обработка событий)'''
        x = self.player_pos[0] + dx
        y = self.player_pos[1] + dy
        # прибавили к позиции игрока шаг в зависимости от нажатой стрелки и проверяем что там находится - если стена или препятствие - шагнуть не сможем
        if self.grid[y][x] == 0 or self.grid[y][x] == 5 or self.grid[y][x] == 7: # если земля, выход или кот - шагаем туда (хотя наступать на кота нежелательно, но и ограничивать игрока не будем)
            self.grid[self.player_pos[1]][self.player_pos[0]] = 0 # там где стоял игрок оставляем спрайт земли
            self.player_pos = (x, y)
            self.grid[y][x] = 6 # куда шагнул - записываем в матрицу
            return True
        elif self.grid[y][x] == 3: # если монетка, то шагаем и подбираем её
            self.get_coins += 1
            self.grid[self.player_pos[1]][self.player_pos[0]] = 0
            self.player_pos = (x, y)
            self.grid[y][x] = 6
        elif self.grid[y][x] == 4: # если бафф, то ставим флаг и вызываем функцию, которая застопит кота
            self.buff = True
            self.isBuff()
            self.grid[self.player_pos[1]][self.player_pos[0]] = 0
            self.player_pos = (x, y)
            self.grid[y][x] = 6
        else:
            return False # если шагнуть не получилось - остались на месте

    def move_cat(self):
        '''движения кота'''
        if self.move_timer > 0: # если мышь подобрала бафф, то кот пропускает ходы
            self.move_timer -= 1
            return
        # Получаем текущие позиции кота и мыши
        cat_pos = self.get_cat_pos()
        mouse_pos = self.get_player_pos()
        # Ищем кратчайший путь до мыши
        next_pos = Cat.find_shortest_path(self,cat_pos, mouse_pos)
        # Если путь не найден, кот остается на месте
        if next_pos is None:
            return
        # Заменяем клетку, на которой стоял кот, на 0
        self.grid[cat_pos[1]][cat_pos[0]] = 0
        # Заменяем клетку, на которую встал кот, на 7
        self.grid[next_pos[1]][next_pos[0]] = 7
        # Обновляем позицию кота
        self.set_cat_pos(next_pos)

    def get_player_pos(self):
        '''получение актуальной позиции игрока'''
        return self.player_pos

    def get_exit_pos(self):
        '''получение актуальной позиции выхода'''
        return self.exit_pos

    def set_cat_pos(self, pos):
        '''установка позиции кота'''
        self.cat_pos = pos

    def get_cat_pos(self):
        '''получение актуальной позиции кота'''
        return self.cat_pos

    def isBuff(self):
        '''если подобрали бафф, то устанавливаем, что кот пропустит 3 хода'''
        if (self.buff == True):
            self.move_timer = 3
            self.buff = False # флаг убираем

    def isDie(self):
        '''проверка на смерть игрока (смерть - позиция кота и игрока совпали)'''
        cat_pos = self.get_cat_pos()
        mouse_pos = self.get_player_pos()
        if cat_pos == mouse_pos: # если да, то устанавливаем флаг
            GameOver = True
            return GameOver
        else:
            GameOver = False
            return GameOver

    def isWin(self):
        '''проверка на победу (позиция игрока = позиции выхода)'''
        exit_pos = self.get_exit_pos()
        mouse_pos = self.get_player_pos()
        if exit_pos == mouse_pos:
            WinGame = True
            return WinGame # возвращаем да, если мышка убежала
        else:
            WinGame = False
            return WinGame
import pygame, random, sys, os
from pygame.locals import *
pygame.init()

# задаём размер экрана
screen_width = 800
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# название в шапке игры (левый верхний угол экрана
pygame.display.set_caption('Mouse and Cat')

# переменная для отслеживания проигрыша
GameOver = False

# создаём шрифт
font = pygame.font.SysFont(None, 30)

# прикольная мышка-курсор
new_cursor = pygame.image.load("cursor.png")
new_cursor = pygame.transform.scale(new_cursor, (64, 64))
pygame.mouse.set_visible(False)

class Menu:
    def __init__(self, screen_width, screen_height):
        # инициализируем кнопки, переменные
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.difficulty = "easy"
        self.speed = 3
        self.start_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 100, 200, 45)
        self.font = pygame.font.Font(None, 30)
        self.diff_input_rect = pygame.Rect(self.screen_width // 2, self.screen_height // 2 - 25, 100, 23)
        self.mouse_pos = None
        self.slow_button = None
        self.medium_button = None
        self.fast_button = None

    def draw(self, screen):
        #отрисовываем фон
        menu_bg = pygame.image.load("menu_bg1.jpg")
        screen.blit(menu_bg, (0, 0))

        #первая часть надписей
        diff_text = self.font.render("Difficulty: ", True, (255, 255, 255))
        screen.blit(diff_text, (self.screen_width // 2 - 100, self.screen_height // 2 - 25))
        pygame.draw.rect(screen, (255, 255, 255), self.diff_input_rect, 2)
        speed_text = self.font.render("Cat speed: ", True, (255, 255, 255))
        screen.blit(speed_text, (self.screen_width // 2 - 100, self.screen_height // 2 + 25))

        #кнопка простого уровня
        self.slow_button = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 50, 60, 40)
        pygame.draw.rect(screen, (255, 255, 255), self.slow_button, 2)
        slow_text = self.font.render("Slow", True, (255, 255, 255))
        screen.blit(slow_text, (self.screen_width // 2 - 94, self.screen_height // 2 + 60))

        #кнопка среднего уровня
        self.medium_button = pygame.Rect(self.screen_width // 2 - 35, self.screen_height // 2 + 50, 100, 40)
        pygame.draw.rect(screen, (255, 255, 255), self.medium_button, 2)
        medium_text = self.font.render("Medium", True, (255, 255, 255))
        screen.blit(medium_text, (self.screen_width // 2 - 23, self.screen_height // 2 + 60))

        #кнопка сложного уровня
        self.fast_button = pygame.Rect(self.screen_width // 2 + 70, self.screen_height // 2 + 50, 55, 40)
        pygame.draw.rect(screen, (255, 255, 255), self.fast_button, 2)
        fast_text = self.font.render("Fast", True, (255, 255, 255))
        screen.blit(fast_text, (self.screen_width // 2 + 77, self.screen_height // 2 + 60))

        #старт
        start_button = self.font.render("Press F to start", True, (255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 255), self.start_button_rect, 2)
        screen.blit(start_button, (self.screen_width // 2 - 70, self.screen_height // 2 + 110))

    def handle_events(self, event):
        # отслеживаем нажатия мыши на экране меню (для реагирования на кнопки изменения сложности, запуска игры)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_pos = pygame.mouse.get_pos()  # получаем позицию мыши (не игровой, положение курсора находим)
            if self.start_button_rect.collidepoint(self.mouse_pos):  # если нажали на кнопку запуска игры (можно не f, а просто мышью нажать)
                return True
            # регулируем сложность в зависимости от нажатой кнопки
            elif self.slow_button.collidepoint(self.mouse_pos):
                self.speed = 3
                self.difficulty = "easy"
            elif self.medium_button.collidepoint(self.mouse_pos):
                self.speed = 2
                self.difficulty = "medium"
            elif self.fast_button.collidepoint(self.mouse_pos):
                self.speed = 1
                self.difficulty = "hard"
        # при нажатии f запускаем игру
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                return True
        return False

class Level:
    def __init__(self):
        # инициализируем переменный класса
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
        # генерация стен вокруг края уровня
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
        # сначала отрисовываем землю
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
        # dx, dy принимают значения в зависимости от нажатой стрелки на клавиатуре (это происходит в цикле while, обработка событий)
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
        if self.move_timer > 0: # если мышь подобрала бафф, то кот пропускает ходы
            self.move_timer -= 1
            return
        # Получаем текущие позиции кота и мыши
        cat_pos = self.get_cat_pos()
        mouse_pos = self.get_player_pos()
        # Ищем кратчайший путь до мыши
        next_pos = Cat.find_shortest_path(level,cat_pos, mouse_pos)
        # Если путь не найден, кот остается на месте
        if next_pos is None:
            return
        # Заменяем клетку, на которой стоял кот, на 0
        self.grid[cat_pos[1]][cat_pos[0]] = 0
        # Заменяем клетку, на которую встал кот, на 7
        self.grid[next_pos[1]][next_pos[0]] = 7
        # Обновляем позицию кота
        self.set_cat_pos(next_pos)

    def get_player_pos(self): # функция для получения актуальной позиции игрока
        return self.player_pos

    def get_exit_pos(self): # для получения актуальной позиции выхода
        return self.exit_pos

    def set_cat_pos(self, pos): # устанавливаем позицию кота
        self.cat_pos = pos

    def get_cat_pos(self): # получем актуальную позицию кота
        return self.cat_pos

    def isBuff(self): # если подобрали бафф, то устанавливаем, что кот пропустит 3 хода
        if (self.buff == True):
            self.move_timer = 3
            self.buff = False # флаг убираем

    def isDie(self): # проверка на смерть игрока (смерть - позиция кота и игрока совпали)
        cat_pos = self.get_cat_pos()
        mouse_pos = self.get_player_pos()
        if cat_pos == mouse_pos: # если да, то устанавливаем флаг
            GameOver = True
            return GameOver
        else:
            GameOver = False
            return GameOver

    def isWin(self): # проверка на победу (позиция игрока = позиции выхода)
        exit_pos = self.get_exit_pos()
        mouse_pos = self.get_player_pos()
        if exit_pos == mouse_pos:
            WinGame = True
            return WinGame # возвращаем да, если мышка убежала
        else:
            WinGame = False
            return WinGame

class Mouse:
    def __init__(self, level):
        # инициализируем поля
        self.level = level
        self.image = pygame.image.load("mouse.png")
        self.GameOver = False

    def draw(self, screen):
        # отрисовываем мышку на нужном месте
        x, y = self.level.get_player_pos()
        screen.blit(self.image, (x*32, y*32))

class Cat:
    def __init__(self, level, player_pos):
        # инициализируем переменные
        self.level = level
        self.player_pos = player_pos
        self.image = pygame.image.load("cat.png")
        self.pos = (2, 2)
        self.player_pos = player_pos
        self.move_timer = 0

    def draw(self, screen):
        # отрисовываем кота
        x, y = self.pos
        screen.blit(self.image, (x*32, y*32))

    def find_shortest_path(level, cat_pos, mouse_pos):
        # Создаем матрицу для хранения расстояний до каждой клетки
        distances = [[float('inf') for _ in range(level.width)] for _ in range(level.height)]
        # Начальная клетка имеет расстояние 0
        distances[cat_pos[1]][cat_pos[0]] = 0
        # Очередь для обхода всех соседних клеток
        queue = [cat_pos]
        # Матрица для хранения путей до каждой клетки
        paths = [[None for _ in range(level.width)] for _ in range(level.height)]
        while queue:
            # Берем первую клетку из очереди
            current_pos = queue.pop(0)
            # Проверяем все соседние клетки
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                x, y = current_pos[0] + dx, current_pos[1] + dy
                # Если клетка находится в пределах карты и можно по ней двигаться
                if 0 <= x < level.width and 0 <= y < level.height and level.grid[y][x] in [6, 4, 3, 0]:
                    # Вычисляем расстояние до этой клетки
                    new_distance = distances[current_pos[1]][current_pos[0]] + 1
                    # Если это новый путь до этой клетки, то добавляем ее в очередь и обновляем расстояние и путь
                    if new_distance < distances[y][x]:
                        distances[y][x] = new_distance
                        paths[y][x] = current_pos
                        queue.append((x, y))
        # Если путь до мыши не найден, возвращаем None
        if paths[mouse_pos[1]][mouse_pos[0]] is None:
            return None
        # Иначе находим следующий ход кота
        current_pos = mouse_pos
        while paths[current_pos[1]][current_pos[0]] != cat_pos:
            current_pos = paths[current_pos[1]][current_pos[0]]
        return current_pos

class Exit:
    def __init__(self, screen):
        # Загрузка изображений
        self.loose_image = pygame.image.load('exit_image.jpg')
        # Получение размеров экрана
        self.screen_rect = screen.get_rect()
        # Размещение изображений на экране
        self.loose_rect = self.loose_image.get_rect(center=self.screen_rect.center)

    def show(self, screen):
        # Отображение изображений на экране
        screen.blit(self.loose_image, self.loose_rect)

class Loose:
    def __init__(self, screen):
        # Загрузка изображений
        self.loose_image = pygame.image.load('loose.jpg')
        # Получение размеров экрана
        self.screen_rect = screen.get_rect()
        # Размещение изображений на экране
        self.loose_rect = self.loose_image.get_rect(center=(self.screen_rect.center))

    def show(self, screen):
        # Отображение изображений на экране
        screen.blit(self.loose_image, self.loose_rect)

    def quit_game(self):
        # закрываем игру
        python = sys.executable
        os.execl(python, python, *sys.argv)


# создаём экземпляры классов и инициализируем
menu = Menu(screen_width, screen_height)
menu.__init__(screen_width, screen_height)
level = Level()
level.__init__()
mouse = Mouse(level)
cat = Cat(level, (level.width - 1, level.height - 1))
exit = Exit(screen)
exit.__init__(screen)
loose = Loose(screen)
loose.__init__(screen)


# создаём флаги и таймер - он будет регулировать скорость передвижения кота
WinGame = False
tick = 0
running = True
is_menu_active = True # активно ли меню

# основной игровой цикл
while running:
    for event in pygame.event.get(): # если нажимали крестик - выходим
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()

        # Обработка событий для меню
        if is_menu_active:
            if menu.handle_events(event):
                is_menu_active = False

        # Обработка событий для игры
        else:
            if event.type == KEYDOWN and GameOver == False and WinGame == False:
                if event.key == K_UP:
                    level.move_player(0, -1)  # стрелка 'up' означает (0, -1) dx, dy
                elif event.key == K_DOWN:
                    level.move_player(0, 1)  # стрелка 'down' означает (0, 1) dx, dy
                elif event.key == K_LEFT:
                    level.move_player(-1, 0)  # стрелка 'left' означает (-1, 0) dx, dy
                elif event.key == K_RIGHT:
                    level.move_player(1, 0)  # стрелка 'right' означает (1, 0) dx, dy
            elif event.type == KEYDOWN: # по кнопочке R можно закрыть игру на этапе экрана победы или поражения
                if event.key == pygame.K_r:
                    loose.quit_game() # вызываем закрытие игры

    # если меню работает, отрисовываем его и меняем сложность в зависимости от нажатых кнопок
    if is_menu_active:
        menu.draw(screen)
        diff_change = font.render(menu.difficulty, True, (255, 255, 255))
        screen.blit(diff_change, (menu.screen_width // 2 + 12, menu.screen_height // 2 - 22))
        # две строчки ниже - видоизменение курсора в меню. Удалите и их тоже, если курсор не понравился
        pos = pygame.mouse.get_pos()
        screen.blit(new_cursor, pos)

    elif (level.isDie() == True): # если умерли, вызываем картинку
        loose.show(screen)
        GameOver = True
    elif (level.isWin() == True):# если выиграли - вызываем другую картинку
        exit.show(screen)
        WinGame = True
    else:
        # перемещения кота раз в несколько тиков программы (зависит от сложности)
        tick += 1
        if (tick % (menu.speed * 15) == 1):
            level.move_cat()

        # при запуске при первом же тике (итерации) генерируем уровень
        if tick == 1:
            level.generate()

        level.draw(screen) # отрисовываем уровень
        mouse.draw(screen) # отрисовываем мышку

    text_surface = font.render('Собрано монет:' + str(level.get_coins), False, (0, 0, 0)) # вверху всегда обновляем надпись кол - ва собранных монеток
    screen.blit(text_surface, (300, 5)) # размещаем надпись сверху посередине, чтоб не мешала играть

    pygame.display.update() # обновляем картинку на экране

pygame.quit() # закрываем игру
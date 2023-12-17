'''
файл содержит информацию о классе Cat игры кошки-мышки
'''
import pygame

class Cat:
    '''постановка кота и подсчет его местонахождения'''

    def __init__(self, level, player_pos):
        '''инициализируем переменные'''
        self.level = level
        self.player_pos = player_pos
        self.image = pygame.image.load("cat.png")
        self.pos = (2, 2)
        self.player_pos = player_pos
        self.move_timer = 0

    def draw(self, screen):
        '''отрисовываем кота'''
        x, y = self.pos
        screen.blit(self.image, (x*32, y*32))

    def find_shortest_path(level, cat_pos, mouse_pos):
        '''Создаем матрицу для хранения расстояний до каждой клетки'''
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
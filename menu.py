'''
файл содержит класс Menu для игры в кошки-мышки
'''
import pygame


class Menu:
    '''Класс для работы с меню игры'''

    def __init__(self, screen_width, screen_height):
        '''инициализируем кнопки, переменные'''
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

    def draw(self, screen:pygame.Surface):
        '''отрисовывает меню'''
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
        '''отслеживаем нажатия мыши на экране меню (для реагирования на кнопки изменения сложности, запуска игры)'''
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

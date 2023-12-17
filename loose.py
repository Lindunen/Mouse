'''
файл содержит информацию о классе Loose игры кошки-мышки
'''
import pygame, sys, os

class Loose:
    def __init__(self, screen):
        '''инициализируем переменные'''
        # Загрузка изображений
        self.loose_image = pygame.image.load('loose.jpg')
        # Получение размеров экрана
        self.screen_rect = screen.get_rect()
        # Размещение изображений на экране
        self.loose_rect = self.loose_image.get_rect(center=(self.screen_rect.center))

    def show(self, screen):
        '''отображение изображений на экране'''
        screen.blit(self.loose_image, self.loose_rect)

    def quit_game(self):
        '''закрываем игру'''
        python = sys.executable
        os.execl(python, python, *sys.argv)
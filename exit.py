'''
файл содержит информацию о классе exit игры кошки-мышки
'''
import pygame

class Exit:
    '''изображение выхода'''

    def __init__(self, screen):
        '''получение картинки выхода, инициализируем переменные'''
        #Загрузка изображений
        self.loose_image = pygame.image.load('exit_image.jpg')
        # Получение размеров экрана
        self.screen_rect = screen.get_rect()
        # Размещение изображений на экране
        self.loose_rect = self.loose_image.get_rect(center=self.screen_rect.center)

    def show(self, screen):
        '''Отображение изображений на экране'''
        screen.blit(self.loose_image, self.loose_rect)
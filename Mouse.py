'''
файл содержит данные о классе Mouse игры кошки-мышки
'''
import pygame

class Mouse:
    '''постановка мыши'''
    def __init__(self, level):
        '''инициализируем поля'''
        self.level = level
        self.image = pygame.image.load("mouse.png")
        self.GameOver = False

    def draw(self, screen):
        '''отрисовываем мышку на нужном месте'''
        x, y = self.level.get_player_pos()
        screen.blit(self.image, (x*32, y*32))
        
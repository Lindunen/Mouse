import pygame, sys
from pygame.locals import *
from menu import Menu
from level import Level
from mouse import Mouse
from cat import Cat
from exit import Exit
from loose import Loose

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

# создаём экземпляры классов и инициализируем
menu = Menu(screen_width, screen_height)
level = Level()
mouse = Mouse(level)
cat = Cat(level, (level.width - 1, level.height - 1))
exit = Exit(screen)
loose = Loose(screen)


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
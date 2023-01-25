import pygame
import os
import sys
import pygame_gui
import random

from pygame_gui.elements import UIButton
# ------------------------------------Бибилиотеки---------------------------------------------------

# --------------------------------Основная часть кода-----------------------------------------------
# Загрузка изображения


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f'Файл с рисунком "{fullname}" не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is None:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


# Завершение отдельной части кода
def terminate():
    pygame.quit()
    sys.exit()


# Начало игры
def start_screen():
    pygame.display.set_caption('Стартовое окно')
    rules = ['Правила игры', "Стреляй, громи, кроши", "Цель: убить противника",
             'Кнопка "Start 2 player"',
             'Отвечает за игру вдвоём',
             'Кнопка "Start 1 player"',
             'Отвечает за игру с ботом']
    fon = pygame.transform.scale(load_image('fon.jpg'), (600, 350))
    screen.blit(fon, (0, 300))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    manager = pygame_gui.UIManager((600, 600))
    button_layout_rect_start_2player = pygame.Rect(280, 150, 150, 40)
    button_layout_rect_rules = pygame.Rect(280, 200, 150, 40)
    button_start_2player = UIButton(relative_rect=button_layout_rect_start_2player,
                                    text='Start 2 player',
                                    manager=manager
                                    )
    button_start_1player = UIButton(relative_rect=button_layout_rect_rules,
                                    text='Start 1 player',
                                    manager=manager
                                    )
    for line in rules:
        line_rendered = font.render(line, 1, pygame.Color('white'))
        line_rect = line_rendered.get_rect()
        text_coord += 5
        line_rect.top = text_coord - 10
        line_rect.x = 10
        text_coord += line_rect.height + 10
        screen.blit(line_rendered, line_rect)
    while True:
        global running_1player, running_2player
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button_start_2player:
                    running_2player = True
                    return
                if event.ui_element == button_start_1player:
                    running_1player = True
                    return
            manager.process_events(event)
        manager.update(FPS)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


# Конец игры
def outro(text):
    screen.fill((0, 0, 0))
    for el in all_sprites:
        el.rect.x = 5000
        el.kill()
    for el in player_group:
        el.rect.x = 5000
        el.kill()
    for el in box_group:
        el.rect.x = 5000
        el.kill()
    for el in shell_group:
        el.rect.x = 5000
        el.kill()
    for el in red_bots_group:
        el.rect.x = 5000
        el.kill()
    for el in blue_bots_group:
        el.rect.x = 5000
        el.kill()
    screen_out = pygame.display.set_mode(size)
    pygame.display.set_caption('Конец игры')
    screen_out.fill((0, 0, 0))
    rules = ['Конец игры', "", text, '...',
             '...']
    fon = pygame.transform.scale(load_image('fon.jpg'), (600, 350))
    screen_out.blit(fon, (0, 300))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in rules:
        line_rendered = font.render(line, 1, pygame.Color('white'))
        line_rect = line_rendered.get_rect()
        text_coord += 10
        line_rect.top = text_coord
        line_rect.x = 10
        text_coord += line_rect.height
        screen_out.blit(line_rendered, line_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                screen_out.fill((0, 0, 0))
                start_screen()
                return
        pygame.display.flip()
        clock.tick(FPS)


# Загрузка уровня
def load_level(filename):
    with open(filename, 'r') as file:
        map_level = list(map(str.strip, file.readlines()))
        max_width = max(map(len, map_level))
        return map_level


# Класс плитки
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'wall1' or tile_type == 'wall2' or tile_type == 'wall3' or \
           tile_type == 'wall4' or tile_type == 'wall5' or tile_type == 'wall6' or \
           tile_type == 'wall7' or tile_type == 'wall8' or tile_type == 'wall9' or \
           tile_type == 'corner1' or tile_type == 'corner2' or tile_type == 'corner3' or \
           tile_type == 'corner4' or tile_type == 'bush' or tile_type == 'cactus':
            self.add(box_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction=1):
        super().__init__(player_group, all_sprites)
        self.direction = direction
        self.image = pygame.transform.rotate(player_image, 90 * self.direction)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x + 5, tile_height * pos_y + 5)

    def shoot(self, aim):
        Shell(self.rect.x, self.rect.y, self.direction, aim)
        shot_sound.play()


class RedBot(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(red_bots_group, all_sprites)
        self.image = pygame.transform.rotate(bot_r_image, 90 * 2)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x + 5, tile_height * pos_y + 5)
        self.dir = random.choice([('x', -1, 2), ('x', 1, 4), ('y', -1, 1), ('y', 1, 3)])
        self.k = 0
        self.rel = random.randint(25, 41)

    def update(self):
        self.k += 1
        for i in range(5):
            if self.dir[0] == 'x':
                self.rect.x += self.dir[1]
                if pygame.sprite.spritecollideany(self, box_group):
                    self.rect.x -= (self.dir[1] * 7)
                    self.dir = random.choice([('x', -1, 2), ('x', 1, 4), ('y', -1, 1), ('y', 1, 3)])
                self.image = pygame.transform.rotate(bot_r_image, 90 * self.dir[2])
            if self.dir[0] == 'y':
                self.rect.y += self.dir[1]
                if pygame.sprite.spritecollideany(self, box_group):
                    self.rect.y -= (self.dir[1] * 7)
                    self.dir = random.choice([('x', -1, 2), ('x', 1, 4), ('y', -1, 1), ('y', 1, 3)])
                self.image = pygame.transform.rotate(bot_r_image, 90 * self.dir[2])
        if self.k == self.rel:
            self.k = 0
            self.shoot()

    def shoot(self):
        Shell(self.rect.x, self.rect.y, self.dir[2], 'player1')
        shot_sound.play()


class BlueBot(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(blue_bots_group, all_sprites)
        self.image = bot_b_image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x + 5, tile_height * pos_y + 5)
        self.dir = random.choice([('x', -1, 2), ('x', 1, 4), ('y', -1, 1), ('y', 1, 3)])
        self.k = 0
        self.rel = random.randint(25, 41)

    def update(self):
        self.k += 1
        for i in range(5):
            if self.dir[0] == 'x':
                self.rect.x += self.dir[1]
                if pygame.sprite.spritecollideany(self, box_group):
                    self.rect.x -= (self.dir[1] * 7)
                    self.dir = random.choice([('x', -1, 2), ('x', 1, 4), ('y', -1, 1), ('y', 1, 3)])
                self.image = pygame.transform.rotate(bot_b_image, 90 * self.dir[2])
            if self.dir[0] == 'y':
                self.rect.y += self.dir[1]
                if pygame.sprite.spritecollideany(self, box_group):
                    self.rect.y -= (self.dir[1] * 7)
                    self.dir = random.choice([('x', -1, 2), ('x', 1, 4), ('y', -1, 1), ('y', 1, 3)])
                self.image = pygame.transform.rotate(bot_b_image, 90 * self.dir[2])
        if self.k == self.rel:
            self.k = 0
            self.shoot()

    def shoot(self):
        Shell(self.rect.x, self.rect.y, self.dir[2], 'player')
        shot_sound.play()


# Класс пули
class Shell(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, aim):
        super().__init__(shell_group, all_sprites)
        self.aim = aim
        self.x = x
        self.y = y
        self.dir = direction
        self.image = pygame.transform.rotate(shell_image, 90 * self.dir)
        self.rect = self.image.get_rect()
        if self.dir == 1:
            self.rect = self.rect.move(x + 14, y - 12)
        if self.dir == 2:
            self.rect = self.rect.move(x - 14, y + 12)
        if self.dir == 3:
            self.rect = self.rect.move(x + 12, y + 33)
        if self.dir == 4:
            self.rect = self.rect.move(x + 33, y + 14)

    def update(self):
        for i in range(15):
            if self.dir == 1:
                self.rect.y -= 1
            if self.dir == 2:
                self.rect.x -= 1
            if self.dir == 3:
                self.rect.y += 1
            if self.dir == 4:
                self.rect.x += 1
            boom_image = load_image('boom.png', -1)
            boom_image = pygame.transform.rotate(boom_image, 90 * self.dir)
            if pygame.sprite.spritecollideany(self, box_group):
                if self.dir == 1:
                    screen.blit(boom_image, (self.rect.x - 21, self.rect.y - 3))
                if self.dir == 2:
                    screen.blit(boom_image, (self.rect.x - 3, self.rect.y - 21))
                if self.dir == 3:
                    screen.blit(boom_image, (self.rect.x - 21, self.rect.y - 23))
                if self.dir == 4:
                    screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                break
            if self.aim == 'player1' and pygame.sprite.collide_mask(self, player1):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                player1.rect.y = 5000
                player1.kill()
                break
            if self.aim == 'player' and pygame.sprite.collide_mask(self, player):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                player.rect.y = 5000
                player.kill()
                break
            if self.aim == 'player1' and len(blue_bots_group.sprites()) >= 1 and \
                    pygame.sprite.collide_mask(self, blue_bots_group.sprites()[0]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                blue_bots_group.sprites()[0].rect.y = 5000
                blue_bots_group.sprites()[0].kill()
                break
            if self.aim == 'player1' and len(blue_bots_group.sprites()) >= 2 and \
                    pygame.sprite.collide_mask(self, blue_bots_group.sprites()[1]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                blue_bots_group.sprites()[1].rect.y = 5000
                blue_bots_group.sprites()[1].kill()
                break
            if self.aim == 'player1' and len(blue_bots_group.sprites()) >= 3 and \
                    pygame.sprite.collide_mask(self, blue_bots_group.sprites()[2]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                blue_bots_group.sprites()[2].rect.y = 5000
                blue_bots_group.sprites()[2].kill()
                break
            if self.aim == 'player1' and len(blue_bots_group.sprites()) >= 4 and \
                    pygame.sprite.collide_mask(self, blue_bots_group.sprites()[3]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                blue_bots_group.sprites()[3].rect.y = 5000
                blue_bots_group.sprites()[3].kill()
                break
            if self.aim == 'player1' and len(blue_bots_group.sprites()) >= 5 and \
                    pygame.sprite.collide_mask(self, blue_bots_group.sprites()[4]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                blue_bots_group.sprites()[4].rect.y = 5000
                blue_bots_group.sprites()[4].kill()
                break
            if self.aim == 'player' and len(red_bots_group.sprites()) >= 1 and \
                    pygame.sprite.collide_mask(self, red_bots_group.sprites()[0]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                red_bots_group.sprites()[0].rect.y = 5000
                red_bots_group.sprites()[0].kill()
                break
            if self.aim == 'player' and len(red_bots_group.sprites()) >= 2 and \
                    pygame.sprite.collide_mask(self, red_bots_group.sprites()[1]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                red_bots_group.sprites()[1].rect.y = 5000
                red_bots_group.sprites()[1].kill()
                break
            if self.aim == 'player' and len(red_bots_group.sprites()) >= 3 and \
                    pygame.sprite.collide_mask(self, red_bots_group.sprites()[2]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                red_bots_group.sprites()[2].rect.y = 5000
                red_bots_group.sprites()[2].kill()
                break
            if self.aim == 'player' and len(red_bots_group.sprites()) >= 4 and \
                    pygame.sprite.collide_mask(self, red_bots_group.sprites()[3]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                red_bots_group.sprites()[3].rect.y = 5000
                red_bots_group.sprites()[3].kill()
                break
            if self.aim == 'player' and len(red_bots_group.sprites()) >= 5 and \
                    pygame.sprite.collide_mask(self, red_bots_group.sprites()[4]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                explosion_sound.play()
                self.kill()
                red_bots_group.sprites()[4].rect.y = 5000
                red_bots_group.sprites()[4].kill()
                break


# Генерация уровней
def generate_level(level):
    new_player, x, y = None, None, None
    new_player1, x1, y1 = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                Tile('sand', x, y)
                if new_player is not None:
                    new_player1 = Player(x, y)
                else:
                    new_player = Player(x, y)
            elif level[y][x] == 'p':
                Tile('sand', x, y)
                RedBot(x, y)
            elif level[y][x] == 'l':
                Tile('sand', x, y)
                BlueBot(x, y)
            elif level[y][x] == 'q':
                Tile('wall1', x, y)
            elif level[y][x] == 'w':
                Tile('wall2', x, y)
            elif level[y][x] == 'e':
                Tile('wall3', x, y)
            elif level[y][x] == 'r':
                Tile('wall4', x, y)
            elif level[y][x] == 't':
                Tile('wall5', x, y)
            elif level[y][x] == 'y':
                Tile('wall6', x, y)
            elif level[y][x] == 'u':
                Tile('wall7', x, y)
            elif level[y][x] == 'i':
                Tile('wall8', x, y)
            elif level[y][x] == 'o':
                Tile('wall9', x, y)
            elif level[y][x] == 'a':
                Tile('corner1', x, y)
            elif level[y][x] == 's':
                Tile('corner2', x, y)
            elif level[y][x] == 'd':
                Tile('corner3', x, y)
            elif level[y][x] == 'f':
                Tile('corner4', x, y)
            elif level[y][x] == 'c':
                Tile('cactus', x, y)
            elif level[y][x] == 'b':
                Tile('bush', x, y)
            elif level[y][x] == 'g':
                Tile('sand', x, y)
    return new_player, new_player1


# Запуск заставки и описание групп спрайтов
while True:
    pygame.init()
    size = width, height = 1200, 1000
    screen = pygame.display.set_mode(size)
    FPS = 12
    running_2player = False
    running_1player = False
    clock = pygame.time.Clock()

    shot_sound = pygame.mixer.Sound('data/tankovyiy-vyistrel.ogg')
    explosion_sound = pygame.mixer.Sound('data/370b925a30aca01.ogg')

    tile_images = {
        'wall1': load_image('wall1.jpg'),
        'wall2': load_image('wall2.jpg'),
        'wall3': load_image('wall3.jpg'),
        'wall4': load_image('wall4.jpg'),
        'wall5': load_image('wall5.jpg'),
        'wall6': load_image('wall6.jpg'),
        'wall7': load_image('wall7.jpg'),
        'wall8': load_image('wall8.jpg'),
        'wall9': load_image('wall9.jpg'),
        'corner1': load_image('corner1.jpg'),
        'corner2': load_image('corner2.jpg'),
        'corner3': load_image('corner3.jpg'),
        'corner4': load_image('corner4.jpg'),
        'cactus': load_image('cactus.jpg'),
        'bush': load_image('bush.jpg'),
        'sand': load_image('sand.jpg')
    }
    player_image = load_image('tank.png')
    player_image = pygame.transform.scale(player_image, (41, 41))
    player_image = pygame.transform.rotate(player_image, 270)
    bot_r_image = load_image('r_tank.png', -1)
    bot_r_image = pygame.transform.scale(bot_r_image, (41, 41))
    bot_r_image = pygame.transform.rotate(bot_r_image, 270)
    bot_b_image = load_image('b_tank.png', -1)
    bot_b_image = pygame.transform.scale(bot_b_image, (41, 41))
    bot_b_image = pygame.transform.rotate(bot_b_image, 270)
    shell_image = load_image('shell.png', -1)
    shell_image = pygame.transform.scale(shell_image, (19, 15))
    tile_width = tile_height = 50

    start_screen()

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    box_group = pygame.sprite.Group()
    shell_group = pygame.sprite.Group()
    red_bots_group = pygame.sprite.Group()
    blue_bots_group = pygame.sprite.Group()
    player = None
    player1 = None
    pygame.display.set_caption('Танчики')

    # Игровой цикл для 2 игроков
    if running_2player:
        player1, player = generate_level(load_level('level3.txt'))
    while running_2player:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    player1.shoot('player')
                if event.key == pygame.K_RSHIFT:
                    player.shoot('player1')
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_UP]:
            player.rect.y -= 5
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.y += 5
            player.direction = 1
        if pressed_keys[pygame.K_DOWN]:
            player.rect.y += 5
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.y -= 5
            player.direction = 3
        if pressed_keys[pygame.K_LEFT]:
            player.rect.x -= 5
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.x += 5
            player.direction = 2
        if pressed_keys[pygame.K_RIGHT]:
            player.rect.x += 5
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.x -= 5
            player.direction = 4
        if pressed_keys[pygame.K_w]:
            player1.rect.y -= 5
            if pygame.sprite.spritecollideany(player1, box_group):
                player1.rect.y += 5
            player1.direction = 1
        if pressed_keys[pygame.K_s]:
            player1.rect.y += 5
            if pygame.sprite.spritecollideany(player1, box_group):
                player1.rect.y -= 5
            player1.direction = 3
        if pressed_keys[pygame.K_a]:
            player1.rect.x -= 5
            if pygame.sprite.spritecollideany(player1, box_group):
                player1.rect.x += 5
            player1.direction = 2
        if pressed_keys[pygame.K_d]:
            player1.rect.x += 5
            if pygame.sprite.spritecollideany(player1, box_group):
                player1.rect.x -= 5
            player1.direction = 4
        player.image = pygame.transform.rotate(player_image, 90 * player.direction)
        player1.image = pygame.transform.rotate(player_image, 90 * player1.direction)
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        shell_group.draw(screen)
        # blue_bots_group.draw(screen)
        # red_bots_group.draw(screen)
        clock.tick(FPS)
        shell_group.update()
        # red_bots_group.update()
        # blue_bots_group.update()
        pygame.display.flip()
        check_game_over = True
        if player not in player_group and player1 not in player_group:
            outro('Ничья')
            check_game_over = False
        elif player not in player_group:
            outro('Победил синий игрок')
            check_game_over = False
        elif player1 not in player_group:
            outro('Победил красный игрок')
            check_game_over = False
        if not check_game_over:
            check_game_over = True
            running_2player = False

    # Игровой цикл для 1 игрока
    if running_1player:
        player1, player = generate_level(load_level('level3.txt'))
        player1.kill()
    while running_1player:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT:
                    player.shoot('player1')
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_UP]:
            player.rect.y -= 5
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.y += 5
            player.direction = 1
        if pressed_keys[pygame.K_DOWN]:
            player.rect.y += 5
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.y -= 5
            player.direction = 3
        if pressed_keys[pygame.K_LEFT]:
            player.rect.x -= 5
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.x += 5
            player.direction = 2
        if pressed_keys[pygame.K_RIGHT]:
            player.rect.x += 5
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.x -= 5
            player.direction = 4
        player.image = pygame.transform.rotate(player_image, 90 * player.direction)
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        shell_group.draw(screen)
        blue_bots_group.draw(screen)
        clock.tick(FPS)
        shell_group.update()
        blue_bots_group.update()
        pygame.display.flip()
        check_game_over = True
        if player not in player_group and len(blue_bots_group) == 0:
            outro('Ничья')
            check_game_over = False
        elif player not in player_group:
            outro('Вы проиграли...')
            check_game_over = False
        elif len(blue_bots_group) == 0:
            outro('Вы победили!')
            check_game_over = False
        if not check_game_over:
            check_game_over = True
            running_1player = False

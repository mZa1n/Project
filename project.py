import pygame
import os
import sys
import pygame_gui
import random
import sqlite3

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
        elif colorkey == -2:
            colorkey = (183, 185, 182)
        image.set_colorkey(colorkey)
    return image


# Завершение отдельной части кода
def terminate():
    pygame.quit()
    sys.exit()


# Начало игры
def start_screen():
    screen.fill((0, 0, 0))
    pygame.display.set_caption('Стартовое окно')
    rules = ['Правила игры', "Стреляй, громи, кроши", "Цель: убить противника",
             'Кнопка "2 player mode"',
             'Отвечает за игру вдвоём',
             'Кнопка "1 player mode"',
             'Отвечает за игру с ботом']
    fon = pygame.transform.scale(load_image('fon.jpg'), (1100, 610))
    screen.blit(fon, (0, 300))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    manager = pygame_gui.UIManager((600, 600))
    button_layout_rect_start_2player = pygame.Rect(280, 150, 150, 40)
    button_layout_rect_rules = pygame.Rect(280, 200, 150, 40)
    button_layout_rect_instruction = pygame.Rect(280, 250, 150, 40)
    button_start_2player = UIButton(relative_rect=button_layout_rect_start_2player,
                                    text='2 players mode',
                                    manager=manager
                                    )
    button_start_1player = UIButton(relative_rect=button_layout_rect_rules,
                                    text='1 player mode',
                                    manager=manager
                                    )
    button_instruction = UIButton(relative_rect=button_layout_rect_instruction,
                                  text='Instruction',
                                  manager=manager)
    for line in rules:
        line_rendered = font.render(line, 1, pygame.Color('white'))
        line_rect = line_rendered.get_rect()
        text_coord += 5
        line_rect.top = text_coord - 10
        line_rect.x = 10
        text_coord += line_rect.height + 10
        screen.blit(line_rendered, line_rect)
    while True:
        global running_2player
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button_start_2player:
                    running_2player = True
                    return
                if event.ui_element == button_start_1player:
                    choosing_mode()
                    return
                if event.ui_element == button_instruction:
                    instruction()
                    return
            manager.process_events(event)
        manager.update(FPS)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def choosing_mode():
    pygame.display.set_mode((500, 500))
    screen.fill((100, 255, 120))
    pygame.display.set_caption('Выбор режима')
    manager = pygame_gui.UIManager((1200, 1200))
    button_layout_rect_vs_bots = pygame.Rect(50, 180, 150, 40)
    button_layout_rect_vs_towers = pygame.Rect(300, 180, 150, 40)
    button_layout_rect_exit = pygame.Rect(170, 300, 150, 40)
    button_vs_bots = UIButton(relative_rect=button_layout_rect_vs_bots,
                                    text='Vs bots',
                                    manager=manager
                                    )
    button_vs_towers = UIButton(relative_rect=button_layout_rect_vs_towers,
                                    text='Vs towers',
                                    manager=manager
                                    )
    button_exit = UIButton(relative_rect=button_layout_rect_exit,
                                text='Exit',
                                manager=manager
                                )
    while True:
        global running_1player, running_vs_towers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button_vs_bots:
                    pygame.display.set_mode(size)
                    running_1player = True
                    return
                if event.ui_element == button_vs_towers:
                    pygame.display.set_mode(size)
                    running_vs_towers = True
                    return
                if event.ui_element == button_exit:
                    pygame.display.set_mode(size)
                    start_screen()
                    return
            manager.process_events(event)
        manager.update(FPS)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


# Руководство по использованию
def instruction():
    screen.fill((0, 0, 0))
    pygame.display.set_caption('Инструкция')
    rules = ['Управление:', 'Первый игрок управляет танком на "wasd" и производит выстрел на "e"',
             'Второй игрок управляет танком на стрелочки и производит выстрел на правый шифт',
             'Нажав на кнопку "2 player mode", вы начнете игру со своим другом',
             'Нажав на кнопку "1 player mode", выберите режим игры:',
             'Vs bots - игра против ботов',
             'Ваша команда зелёная, команда противников синяя',
             'Ваша задача - убить всех врагов',
             'Vs towers - игра против башен',
             'Ваша команда зелёная, команда противников синяя',
             'Ваша задача - убить все три башни, которые расположены на карте'
             'После победы или поражение, вам следует нажать любую клавишу мыши для продолжения']
    fon = pygame.transform.scale(load_image('fon.jpg'), (1100, 610))
    screen.blit(fon, (0, 300))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    manager = pygame_gui.UIManager((1200, 1200))
    button_layout_rect_close = pygame.Rect(800, 210, 150, 40)
    button_close = UIButton(relative_rect=button_layout_rect_close,
                            text='Exit',
                            manager=manager
                            )
    for line in rules:
        line_rendered = font.render(line, 1, pygame.Color('green'))
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
                if event.ui_element == button_close:
                    start_screen()
                    return
            manager.process_events(event)
        manager.update(FPS)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


# Конец игры
def outro(text, players_number):
    con = sqlite3.connect('match_results.db')
    cur = con.cursor()
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
    if players_number == 2:
        n = cur.execute("""SELECT all_games FROM results""").fetchall()[0][0]
        rules = ['Конец игры', "", text,
                 'Итоговый счёт:',
                 f'Красные: {cur.execute("SELECT red_this_game FROM results").fetchall()[0][0]}',
                 f'Синие: {cur.execute("""SELECT blue_this_game FROM results""").fetchall()[0][0]}',
                 f'Общий процент побед красного: '
                 f'{(cur.execute("""SELECT red FROM results""").fetchall()[0][0] / n * 100):.2f}%',
                 f'Общий процент побед синего: '
                 f'{(cur.execute("""SELECT blue FROM results""").fetchall()[0][0] / n * 100):.2f}%',
                 'Для выхода в главное меню нажмите пробел']
    if players_number == 1:
        rules = ['Конец игры', "", text, 'Для выхода в главное меню нажмите пробел']
    fon = pygame.transform.scale(load_image('fon.jpg'), (1100, 610))
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen_out.fill((0, 0, 0))
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


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = width // 2 - (target.rect.x + target.rect.w // 2)
        self.dy = height // 2 - (target.rect.y + target.rect.h // 2)


class DamagedTower(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(box_group, all_sprites, tiles_group)
        self.image = load_image('damaged_tower_image.png', -1)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos_x, pos_y)


class Tower(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tower_group, box_group, tiles_group, all_sprites)
        self.frames = []
        self.cut_sheet(load_image('tower_image.png', -1), 11, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(pos_x * tile_width, pos_y * tile_height)
        self.hp = 5
        self.rel = 50
        self.k = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.hp <= 0:
            DamagedTower(self.rect.x, self.rect.y)
            self.kill()
        self.k += 1
        if self.k == self.rel:
            self.k = 0
            Shell(self.rect.x + 25, self.rect.y - 25, 1, 'player')
            Shell(self.rect.x - 10, self.rect.y - 10, 2, 'player')
            Shell(self.rect.x + 25, self.rect.y + 70, 3, 'player')
            Shell(self.rect.x + 70, self.rect.y - 10, 4, 'player')
            pygame.mixer.Channel(1).play(shot_sound)


class DamageBoost(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(boost_group, all_sprites)
        self.image = load_image('damage_boost_box.png', -1)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        if pygame.sprite.collide_mask(self, player1):
            BoostEffect('player1', 'damage')
            player1.shell_damage += 1
            self.kill()
        if pygame.sprite.collide_mask(self, player):
            BoostEffect('player', 'damage')
            player.shell_damage += 1
            self.kill()


class SpeedBoost(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(boost_group, all_sprites)
        self.image = load_image('speed_boost_box.png', -1)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        if pygame.sprite.collide_mask(self, player1):
            BoostEffect('player1', 'speed')
            player1.speed = 8
            self.kill()
        if pygame.sprite.collide_mask(self, player):
            BoostEffect('player', 'speed')
            player.speed = 8
            self.kill()


class BoostEffect(pygame.sprite.Sprite):
    def __init__(self, player_name, boost_name):
        super().__init__(effects_group, all_sprites)
        self.player_name = player_name
        self.frames = []
        if boost_name == 'damage':
            self.cut_sheet(load_image('damage_boost.png', -1), 3, 1)
        elif boost_name == 'speed':
            self.cut_sheet(load_image('speed_boost.png', -1), 3, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        if self.player_name == 'player':
            self.rect = self.rect.move(player.rect.x, player.rect.y)
        if self.player_name == 'player1':
            self.rect = self.rect.move(player1.rect.x, player1.rect.y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        pygame.mixer.Channel(3).play(effect_sound)
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.player_name == 'player':
            self.rect.x = player.rect.x - 3
            self.rect.y = player.rect.y - 3
        if self.player_name == 'player1':
            self.rect.x = player1.rect.x - 3
            self.rect.y = player1.rect.y - 3


class Mine(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(mines_group, all_sprites)
        if random.randint(0, 1) == 1:
            self.image = load_image('mine.png')
        else:
            self.image = load_image('sand.jpg')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos_x * tile_width, pos_y * tile_height)

    def update(self):
        if pygame.sprite.collide_mask(self, player):
            screen.blit(pixel_boom_image, (self.rect.x, self.rect.y))
            explosion_sound.play()
            player.hp -= 2
            player.update()
            self.kill()
        if pygame.sprite.collide_mask(self, player1):
            screen.blit(pixel_boom_image, (self.rect.x, self.rect.y))
            explosion_sound.play()
            player1.hp -= 2
            player1.update()
            self.kill()
        for el in blue_bots_group.sprites():
            if pygame.sprite.collide_mask(el, self):
                screen.blit(pixel_boom_image, (self.rect.x, self.rect.y))
                explosion_sound.play()
                el.hp -= 2
                el.check_hp()
                self.kill()
        for el in red_bots_group.sprites():
            if pygame.sprite.collide_mask(el, self):
                screen.blit(pixel_boom_image, (self.rect.x, self.rect.y))
                explosion_sound.play()
                el.hp -= 2
                el.check_hp()
                self.kill()


class DamagedTank(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction):
        super().__init__(box_group, all_sprites, tiles_group)
        self.image = pygame.transform.rotate(damaged_player_image, (direction - 1) * 90)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos_x, pos_y)

    def update(self):
        if pygame.sprite.collide_mask(self, player):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    player.rect.x = (player.rect.x + (i * 50)) // 50 * 50
                    player.rect.y = (player.rect.y + (j * 50)) // 50 * 50
                    if pygame.sprite.spritecollideany(player, box_group) or player.rect.x <= 0 or \
                            player.rect.x >= width or player.rect.y <= 0 or player.rect.y >= height:
                        player.rect.x -= (i * 50)
                        player.rect.y -= (j * 50)
                    else:
                        return
        if pygame.sprite.collide_mask(self, player1):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    player1.rect.x = (player1.rect.x + (i * 50)) // 50 * 50
                    player1.rect.y = (player1.rect.y + (j * 50)) // 50 * 50
                    if pygame.sprite.spritecollideany(player1, box_group) or player1.rect.x <= 0 or\
                            player1.rect.x >= width or player1.rect.y <= 0 or \
                            player1.rect.y >= height:
                        player1.rect.x -= (i * 50)
                        player1.rect.y -= (j * 50)
                    else:
                        return
        for el in blue_bots_group.sprites():
            if pygame.sprite.collide_mask(self, el):
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        el.rect.x = (el.rect.x + (i * 50)) // 50 * 50
                        el.rect.y = (el.rect.y + (j * 50)) // 50 * 50
                        if pygame.sprite.spritecollideany(el, box_group) or el.rect.x <= 0 or \
                                el.rect.x >= width or el.rect.y <= 0 or el.rect.y >= height:
                            el.rect.x -= (i * 50)
                            el.rect.y -= (j * 50)
                        else:
                            return
        for el in red_bots_group.sprites():
            if pygame.sprite.collide_mask(self, el):
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        el.rect.x = (el.rect.x + (i * 50)) // 50 * 50
                        el.rect.y = (el.rect.y + (j * 50)) // 50 * 50
                        if pygame.sprite.spritecollideany(el, box_group) or el.rect.x <= 0 or \
                                el.rect.x >= width or el.rect.y <= 0 or el.rect.y >= height:
                            el.rect.x -= (i * 50)
                            el.rect.y -= (j * 50)
                        else:
                            return


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction=1):
        super().__init__(player_group, all_sprites)
        self.direction = direction
        self.image = pygame.transform.rotate(player_image, 90 * self.direction)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x + 5, tile_height * pos_y + 5)
        self.hp = 10
        self.shell_damage = 1
        self.speed = 5

    # Функция, отвечающая за выстрел игрока
    def shoot(self, aim):
        Shell(self.rect.x, self.rect.y, self.direction, aim)
        pygame.mixer.Channel(1).play(shot_sound)

    def update(self):
        if self.hp <= 0:
            DamagedTank(self.rect.x, self.rect.y, self.direction)
            self.rect.x = self.rect.y = 5000
            self.kill()


# Класс красных ботов
class RedBot(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(red_bots_group, all_sprites)
        self.image = pygame.transform.rotate(bot_r_image, 90 * 2)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x + 5, tile_height * pos_y + 5)
        self.dir = random.choice([('x', -1, 2), ('x', 1, 4), ('y', -1, 1), ('y', 1, 3)])
        self.k = 0
        self.hp = 1
        self.rel = random.randint(25, 41)

    # Функция, отвечающая за перемещение бота
    def update(self):
        self.k += 1
        pygame.mixer.Channel(2).play(tank_sound)
        for i in range(5):
            if self.dir[0] == 'x':
                self.rect.x += self.dir[1]
                if random.choice([0] * 150 + [1]) == 1:
                    self.dir = random.choice([('y', -1, 1), ('y', 1, 3)])
                if pygame.sprite.spritecollideany(self, box_group):
                    self.rect.x -= (self.dir[1] * 7)
                    self.dir = random.choice([('y', -1, 1), ('y', 1, 3)])
                self.image = pygame.transform.rotate(bot_r_image, 90 * self.dir[2])
            if self.dir[0] == 'y':
                self.rect.y += self.dir[1]
                if random.choice([0] * 150 + [1]) == 1:
                    self.dir = random.choice([('x', -1, 2), ('x', 1, 4)])
                if pygame.sprite.spritecollideany(self, box_group):
                    self.rect.y -= (self.dir[1] * 7)
                    self.dir = random.choice([('x', -1, 2), ('x', 1, 4)])
                self.image = pygame.transform.rotate(bot_r_image, 90 * self.dir[2])
        if self.k == self.rel:
            self.k = 0
            self.shoot()

    def check_hp(self):
        if self.hp <= 0:
            DamagedTank(self.rect.x, self.rect.y, self.dir[2])
            self.rect.x = self.rect.y = 5000
            self.kill()

    # Функция, отвечающая за выстрел бота
    def shoot(self):
        Shell(self.rect.x, self.rect.y, self.dir[2], 'player1')
        pygame.mixer.Channel(1).play(shot_sound)


# Класс синих ботов
class BlueBot(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(blue_bots_group, all_sprites)
        self.image = bot_b_image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x + 5, tile_height * pos_y + 5)
        self.dir = random.choice([('x', -1, 2), ('x', 1, 4), ('y', -1, 1), ('y', 1, 3)])
        self.k = 0
        self.hp = 1
        self.rel = random.randint(25, 41)

    # Функция, отвечающая за перемещение бота
    def update(self):
        self.k += 1
        pygame.mixer.Channel(2).play(tank_sound)
        for i in range(5):
            if self.dir[0] == 'x':
                self.rect.x += self.dir[1]
                if random.choice([0] * 150 + [1]) == 1:
                    self.dir = random.choice([('y', -1, 1), ('y', 1, 3)])
                if pygame.sprite.spritecollideany(self, box_group):
                    self.rect.x -= (self.dir[1] * 7)
                    self.dir = random.choice([('y', -1, 1), ('y', 1, 3)])
                self.image = pygame.transform.rotate(bot_b_image, 90 * self.dir[2])
            if self.dir[0] == 'y':
                self.rect.y += self.dir[1]
                if random.choice([0] * 150 + [1]) == 1:
                    self.dir = random.choice([('x', -1, 2), ('x', 1, 4)])
                if pygame.sprite.spritecollideany(self, box_group):
                    self.rect.y -= (self.dir[1] * 7)
                    self.dir = random.choice([('x', -1, 2), ('x', 1, 4)])
                self.image = pygame.transform.rotate(bot_b_image, 90 * self.dir[2])
        if self.k == self.rel:
            self.k = 0
            self.shoot()

    def check_hp(self):
        if self.hp <= 0:
            DamagedTank(self.rect.x, self.rect.y, self.dir[2])
            self.rect.x = self.rect.y = 5000
            self.kill()

    # Функция, отвечающая за выстрел бота
    def shoot(self):
        Shell(self.rect.x, self.rect.y, self.dir[2], 'player')
        pygame.mixer.Channel(1).play(shot_sound)


# Класс пули
class Shell(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, aim):
        super().__init__(shell_group, all_sprites)
        self.aim = aim
        self.x = x
        self.y = y
        self.dir = direction
        self.distance = 0
        self.image = pygame.transform.rotate(shell_image, 90 * self.dir)
        self.rect = self.image.get_rect()
        if self.dir == 1:
            self.rect = self.rect.move(x + 12, y - 8)
        if self.dir == 2:
            self.rect = self.rect.move(x - 10, y + 14)
        if self.dir == 3:
            self.rect = self.rect.move(x + 14, y + 31)
        if self.dir == 4:
            self.rect = self.rect.move(x + 31, y + 12)

    # Функция, отвечающая за перемещение пули
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
            self.distance += 1
            boom_image = load_image('boom.png', -1)
            boom_image = pygame.transform.rotate(boom_image, 90 * self.dir)
            if pygame.sprite.spritecollideany(self, tower_group) and self.aim == 'player1':
                for el in tower_group.sprites():
                    if pygame.sprite.collide_rect(self, el):
                        if self.dir == 1 or self.dir == 3:
                            screen.blit(pixel_boom_image, (self.rect.x - 15, self.rect.y))
                        if self.dir == 2 or self.dir == 4:
                            screen.blit(pixel_boom_image, (self.rect.x, self.rect.y - 15))
                        self.kill()
                        explosion_sound.play()
                        el.hp -= 1
                        el.update()
                        return
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
                player1.hp -= player.shell_damage
                player1.update()
                break
            if self.aim == 'player' and pygame.sprite.collide_mask(self, player):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                player.hp -= player1.shell_damage
                player.update()
                break
            if self.aim == 'player1' and len(blue_bots_group.sprites()) >= 1 and \
                    pygame.sprite.collide_mask(self, blue_bots_group.sprites()[0]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                if min(self.dir, blue_bots_group.sprites()[0].dir[2]) + 2 != \
                        max(self.dir, blue_bots_group.sprites()[0].dir[2]):
                    blue_bots_group.sprites()[0].hp -= random.choice([player.shell_damage, 0])
                    blue_bots_group.sprites()[0].check_hp()
                break
            if self.aim == 'player1' and len(blue_bots_group.sprites()) >= 2 and \
                    pygame.sprite.collide_mask(self, blue_bots_group.sprites()[1]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                if min(self.dir, blue_bots_group.sprites()[1].dir[2]) + 2 != \
                        max(self.dir, blue_bots_group.sprites()[1].dir[2]):
                    blue_bots_group.sprites()[1].hp -= random.choice([player.shell_damage, 0])
                    blue_bots_group.sprites()[1].check_hp()
                break
            if self.aim == 'player1' and len(blue_bots_group.sprites()) >= 3 and \
                    pygame.sprite.collide_mask(self, blue_bots_group.sprites()[2]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                if min(self.dir, blue_bots_group.sprites()[2].dir[2]) + 2 != \
                        max(self.dir, blue_bots_group.sprites()[2].dir[2]):
                    blue_bots_group.sprites()[2].hp -= random.choice([player.shell_damage, 0])
                    blue_bots_group.sprites()[2].check_hp()
                break
            if self.aim == 'player1' and len(blue_bots_group.sprites()) >= 4 and \
                    pygame.sprite.collide_mask(self, blue_bots_group.sprites()[3]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                if min(self.dir, blue_bots_group.sprites()[3].dir[2]) + 2 != \
                        max(self.dir, blue_bots_group.sprites()[3].dir[2]):
                    blue_bots_group.sprites()[3].hp -= random.choice([player.shell_damage, 0])
                    blue_bots_group.sprites()[3].check_hp()
                break
            if self.aim == 'player1' and len(blue_bots_group.sprites()) >= 5 and \
                    pygame.sprite.collide_mask(self, blue_bots_group.sprites()[4]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                if min(self.dir, blue_bots_group.sprites()[4].dir[2]) + 2 != \
                        max(self.dir, blue_bots_group.sprites()[4].dir[2]):
                    blue_bots_group.sprites()[4].hp -= random.choice([player.shell_damage, 0])
                    blue_bots_group.sprites()[4].check_hp()
                break
            if self.aim == 'player' and len(red_bots_group.sprites()) >= 1 and \
                    pygame.sprite.collide_mask(self, red_bots_group.sprites()[0]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                if min(self.dir, red_bots_group.sprites()[0].dir[2]) + 2 != \
                        max(self.dir, red_bots_group.sprites()[0].dir[2]):
                    red_bots_group.sprites()[0].hp -= random.choice([player1.shell_damage, 0])
                    red_bots_group.sprites()[0].check_hp()
                break
            if self.aim == 'player' and len(red_bots_group.sprites()) >= 2 and \
                    pygame.sprite.collide_mask(self, red_bots_group.sprites()[1]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                if min(self.dir, red_bots_group.sprites()[1].dir[2]) + 2 != \
                        max(self.dir, red_bots_group.sprites()[1].dir[2]):
                    red_bots_group.sprites()[1].hp -= random.choice([player1.shell_damage, 0])
                    red_bots_group.sprites()[1].check_hp()
                break
            if self.aim == 'player' and len(red_bots_group.sprites()) >= 3 and \
                    pygame.sprite.collide_mask(self, red_bots_group.sprites()[2]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                if min(self.dir, red_bots_group.sprites()[2].dir[2]) + 2 != \
                        max(self.dir, red_bots_group.sprites()[2].dir[2]):
                    red_bots_group.sprites()[2].hp -= random.choice([player1.shell_damage, 0])
                    red_bots_group.sprites()[2].check_hp()
                break
            if self.aim == 'player' and len(red_bots_group.sprites()) >= 4 and \
                    pygame.sprite.collide_mask(self, red_bots_group.sprites()[3]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                explosion_sound.play()
                if min(self.dir, red_bots_group.sprites()[3].dir[2]) + 2 != \
                        max(self.dir, red_bots_group.sprites()[3].dir[2]):
                    red_bots_group.sprites()[3].hp -= random.choice([player1.shell_damage, 0])
                    red_bots_group.sprites()[3].check_hp()
                break
            if self.aim == 'player' and len(red_bots_group.sprites()) >= 5 and \
                    pygame.sprite.collide_mask(self, red_bots_group.sprites()[4]):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                explosion_sound.play()
                self.kill()
                if min(self.dir, red_bots_group.sprites()[4].dir[2]) + 2 != \
                        max(self.dir, red_bots_group.sprites()[4].dir[2]):
                    red_bots_group.sprites()[4].hp -= random.choice([player1.shell_damage, 0])
                    red_bots_group.sprites()[4].check_hp()
                break
            if self.distance >= 500:
                if self.dir == 1 or self.dir == 3:
                    screen.blit(pixel_boom_image, (self.rect.x - 15, self.rect.y))
                if self.dir == 2 or self.dir == 4:
                    screen.blit(pixel_boom_image, (self.rect.x, self.rect.y - 15))
                explosion_sound.play()
                self.kill()
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
            elif level[y][x] == 'k':
                Tile('sand', x, y)
                Tower(x, y)
            elif level[y][x] == 'q':
                Tile('sand', x, y)
                Tile('wall1', x + 0.5, y + 0.5)
            elif level[y][x] == 'w':
                Tile('sand', x, y)
                Tile('wall2', x + 0.5, y)
            elif level[y][x] == 'e':
                Tile('sand', x, y)
                Tile('wall3', x + 0.5, y)
            elif level[y][x] == 'r':
                Tile('sand', x, y)
                Tile('wall4', x, y)
            elif level[y][x] == 't':
                Tile('wall5', x, y)
            elif level[y][x] == 'y':
                Tile('sand', x, y)
                Tile('wall6', x, y + 0.5)
            elif level[y][x] == 'u':
                Tile('sand', x, y)
                Tile('wall7', x, y + 0.5)
            elif level[y][x] == 'i':
                Tile('sand', x, y)
                Tile('wall8', x, y)
            elif level[y][x] == 'o':
                Tile('sand', x, y)
                Tile('wall9', x, y)
            elif level[y][x] == 'a':
                Tile('sand', x, y)
                Tile('wall4', x, y)
                Tile('wall7', x, y + 0.5)
            elif level[y][x] == 's':
                Tile('sand', x, y)
                Tile('wall6', x, y + 0.5)
                Tile('wall9', x, y)
            elif level[y][x] == 'd':
                Tile('sand', x, y)
                Tile('wall1', x + 0.5, y + 0.5)
                Tile('wall4', x, y)
            elif level[y][x] == 'f':
                Tile('sand', x, y)
                Tile('wall3', x + 0.5, y)
                Tile('wall6', x, y + 0.5)
            elif level[y][x] == 'c':
                Tile('sand', x, y)
                Tile('cactus', x, y)
            elif level[y][x] == 'b':
                Tile('bush', x, y)
            elif level[y][x] == 'g':
                Tile('sand', x, y)
    return new_player, new_player1


# Запуск заставки и описание групп спрайтов
con = sqlite3.connect('match_results.db')
cur = con.cursor()
result = cur.execute('''UPDATE results SET blue_this_game = 0 WHERE id = 1''').fetchall()
result = cur.execute('''UPDATE results SET red_this_game = 0 WHERE id = 1''').fetchall()
con.commit()
while True:
    con.commit()
    pygame.init()
    size = width, height = 1100, 1000
    screen = pygame.display.set_mode(size)
    FPS = 12
    running_2player = False
    running_1player = False
    running_vs_towers = False
    clock = pygame.time.Clock()

    shot_sound = pygame.mixer.Sound('data/tankovyiy-vyistrel.ogg')
    explosion_sound = pygame.mixer.Sound('data/370b925a30aca01.ogg')
    effect_sound = pygame.mixer.Sound('data/effect_sound.mp3')
    effect_sound.set_volume(0.9)
    tank_sound = pygame.mixer.Sound('data/tank_sound.mp3')
    tank_sound.set_volume(0.61)

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
        'corner4': load_image('corner4.jpg', -2),
        'cactus': load_image('cactus.jpg'),
        'bush': load_image('bush.jpg'),
        'sand': load_image('sand.jpg')
    }
    player_image = load_image('player1.png', -1)
    player_image = pygame.transform.scale(player_image, (41, 41))
    player_image = pygame.transform.rotate(player_image, 90)
    bot_r_image = pygame.transform.rotate(load_image('red_bot1.png', -1), 180)
    bot_r_image = pygame.transform.scale(bot_r_image, (41, 41))
    bot_r_image = pygame.transform.rotate(bot_r_image, 270)
    bot_b_image = pygame.transform.rotate(load_image('blue_bot1.png', -1), 180)
    bot_b_image = pygame.transform.scale(bot_b_image, (41, 41))
    bot_b_image = pygame.transform.rotate(bot_b_image, 270)
    shell_image = load_image('shell.png', -1)
    shell_image = pygame.transform.scale(shell_image, (19, 15))
    damaged_player_image = load_image('damaged_tank.jpg', -1)
    damaged_player_image = pygame.transform.scale(damaged_player_image, (41, 41))
    damaged_player_image = pygame.transform.rotate(damaged_player_image, 180)
    pixel_boom_image = pygame.transform.scale(load_image('pixel_boom.png'), (50, 50))
    tile_width = tile_height = 50

    start_screen()

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    box_group = pygame.sprite.Group()
    shell_group = pygame.sprite.Group()
    red_bots_group = pygame.sprite.Group()
    blue_bots_group = pygame.sprite.Group()
    mines_group = pygame.sprite.Group()
    boost_group = pygame.sprite.Group()
    effects_group = pygame.sprite.Group()
    tower_group = pygame.sprite.Group()
    player = None
    player1 = None
    pygame.display.set_caption('Танчики')

    coords_for_mines = [(9, 8), (5, 12), (17, 7), (18, 3),
                        (11, 16), (2, 9), (15, 14), (5, 4), (18, 4)]
    random.shuffle(coords_for_mines)
    num_of_mines = random.randint(0, 7)

    # Игровой цикл для 2 игроков
    if running_2player:
        result = cur.execute(
            '''UPDATE results SET all_games = all_games + 1 WHERE id = 1''').fetchall()
        player1, player = generate_level(load_level('level3.txt'))
        for i in range(num_of_mines):
            Mine(coords_for_mines[i][0], coords_for_mines[i][1])
        damage_boost_coords = random.choice([(10, 10), (11, 10), (12, 9), (12, 10), (12, 8)])
        speed_boost_coords = random.choice([(8, 8), (10, 8), (11, 9), (10, 8), (12, 8)])
        DamageBoost(damage_boost_coords[0], damage_boost_coords[1])
        SpeedBoost(speed_boost_coords[0], speed_boost_coords[1])
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
            player.rect.y -= player.speed
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.y += player.speed
            player.direction = 1
            pygame.mixer.Channel(2).play(tank_sound)
        if pressed_keys[pygame.K_DOWN]:
            player.rect.y += player.speed
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.y -= player.speed
            player.direction = 3
            pygame.mixer.Channel(2).play(tank_sound)
        if pressed_keys[pygame.K_LEFT]:
            player.rect.x -= player.speed
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.x += player.speed
            player.direction = 2
            pygame.mixer.Channel(2).play(tank_sound)
        if pressed_keys[pygame.K_RIGHT]:
            player.rect.x += player.speed
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.x -= player.speed
            player.direction = 4
            pygame.mixer.Channel(2).play(tank_sound)
        if pressed_keys[pygame.K_w]:
            player1.rect.y -= player1.speed
            if pygame.sprite.spritecollideany(player1, box_group):
                player1.rect.y += player1.speed
            player1.direction = 1
            pygame.mixer.Channel(2).play(tank_sound)
        if pressed_keys[pygame.K_s]:
            player1.rect.y += player1.speed
            if pygame.sprite.spritecollideany(player1, box_group):
                player1.rect.y -= player1.speed
            player1.direction = 3
            pygame.mixer.Channel(2).play(tank_sound)
        if pressed_keys[pygame.K_a]:
            player1.rect.x -= player1.speed
            if pygame.sprite.spritecollideany(player1, box_group):
                player1.rect.x += player1.speed
            player1.direction = 2
            pygame.mixer.Channel(2).play(tank_sound)
        if pressed_keys[pygame.K_d]:
            player1.rect.x += player1.speed
            if pygame.sprite.spritecollideany(player1, box_group):
                player1.rect.x -= player1.speed
            player1.direction = 4
            pygame.mixer.Channel(2).play(tank_sound)
        player.image = pygame.transform.rotate(player_image, 90 * player.direction)
        player1.image = pygame.transform.rotate(player_image, 90 * player1.direction)
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        boost_group.draw(screen)
        player_group.draw(screen)
        blue_bots_group.draw(screen)
        red_bots_group.draw(screen)
        effects_group.draw(screen)
        mines_group.draw(screen)
        shell_group.draw(screen)
        clock.tick(FPS)
        boost_group.update()
        effects_group.update()
        red_bots_group.update()
        blue_bots_group.update()
        mines_group.update()
        shell_group.update()
        for el in box_group.sprites():
            if el.__class__.__name__ == 'DamagedTank':
                el.update()
        font = pygame.font.Font(None, 23)
        line_rendered_blue = font.render(f'{player1.hp}', 1, pygame.Color('blue'))
        line_rect_blue = line_rendered_blue.get_rect()
        line_rect_blue.y = player1.rect.y - 25
        if player1.hp == 10:
            line_rect_blue.x = player1.rect.x + 12
        else:
            line_rect_blue.x = player1.rect.x + 15
        screen.blit(line_rendered_blue, line_rect_blue)
        line_rendered_red = font.render(f'{player.hp}', 1, pygame.Color('red'))
        line_rect_red = line_rendered_red.get_rect()
        line_rect_red.y = player.rect.y - 25
        if player.hp == 10:
            line_rect_red.x = player.rect.x + 12
        else:
            line_rect_red.x = player.rect.x + 15
        screen.blit(line_rendered_red, line_rect_red)
        pygame.display.flip()
        check_game_over = True
        if player not in player_group and player1 not in player_group:
            outro('Ничья', 2)
            check_game_over = False
        elif player not in player_group:
            cur.execute('''UPDATE results SET blue_this_game = blue_this_game + 1 WHERE id = 1''')
            cur.execute('''UPDATE results SET blue = blue + 1 WHERE id = 1''')
            con.commit()
            outro('Победил синий игрок', 2)
            check_game_over = False
        elif player1 not in player_group:
            cur.execute('''UPDATE results SET red_this_game = red_this_game + 1 WHERE id = 1''')
            cur.execute('''UPDATE results SET red = red + 1 WHERE id = 1''')
            con.commit()
            outro('Победил красный игрок', 2)
            check_game_over = False
        if not check_game_over:
            check_game_over = True
            running_2player = False

    # Игровой цикл для 1 игрока
    if running_1player:
        player1, player = generate_level(load_level('level3_bots.txt'))
        player1.kill()
        for i in range(num_of_mines):
            Mine(coords_for_mines[i][0], coords_for_mines[i][1])
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
            pygame.mixer.Channel(2).play(tank_sound)
        if pressed_keys[pygame.K_DOWN]:
            player.rect.y += 5
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.y -= 5
            player.direction = 3
            pygame.mixer.Channel(2).play(tank_sound)
        if pressed_keys[pygame.K_LEFT]:
            player.rect.x -= 5
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.x += 5
            player.direction = 2
            pygame.mixer.Channel(2).play(tank_sound)
        if pressed_keys[pygame.K_RIGHT]:
            player.rect.x += 5
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.x -= 5
            player.direction = 4
            pygame.mixer.Channel(2).play(tank_sound)
        player.image = pygame.transform.rotate(player_image, 90 * player.direction)
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        blue_bots_group.draw(screen)
        mines_group.draw(screen)
        shell_group.draw(screen)
        clock.tick(FPS)
        blue_bots_group.update()
        mines_group.update()
        shell_group.update()
        for el in box_group.sprites():
            if el.__class__.__name__ == 'DamagedTank':
                el.update()
        font = pygame.font.Font(None, 23)
        line_rendered_red = font.render(f'{player.hp}', 1, pygame.Color('green'))
        line_rect_red = line_rendered_red.get_rect()
        line_rect_red.y = player.rect.y - 25
        if player.hp == 10:
            line_rect_red.x = player.rect.x + 12
        else:
            line_rect_red.x = player.rect.x + 15
        screen.blit(line_rendered_red, line_rect_red)
        pygame.display.flip()
        check_game_over = True
        if player not in player_group and len(blue_bots_group) == 0:
            outro('Ничья', 1)
            check_game_over = False
        elif player not in player_group:
            outro('Вы проиграли...', 1)
            check_game_over = False
        elif len(blue_bots_group) == 0:
            outro('Вы победили!', 1)
            check_game_over = False
        if not check_game_over:
            check_game_over = True
            running_1player = False

    if running_vs_towers:
        player1, player = generate_level(load_level('level5.txt'))
        player1.shell_damage = 3
        camera = Camera()
        player1.kill()
    while running_vs_towers:
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
            pygame.mixer.Channel(2).play(tank_sound)
        if pressed_keys[pygame.K_DOWN]:
            player.rect.y += 5
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.y -= 5
            player.direction = 3
            pygame.mixer.Channel(2).play(tank_sound)
        if pressed_keys[pygame.K_LEFT]:
            player.rect.x -= 5
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.x += 5
            player.direction = 2
            pygame.mixer.Channel(2).play(tank_sound)
        if pressed_keys[pygame.K_RIGHT]:
            player.rect.x += 5
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.x -= 5
            player.direction = 4
            pygame.mixer.Channel(2).play(tank_sound)
        if len(tower_group.sprites()) == 1:
            player1.shell_damage = 10
        player.image = pygame.transform.rotate(player_image, 90 * player.direction)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        tower_group.draw(screen)
        player_group.draw(screen)
        blue_bots_group.draw(screen)
        shell_group.draw(screen)
        clock.tick(FPS)
        blue_bots_group.update()
        shell_group.update()
        tower_group.update()
        for el in box_group.sprites():
            if el.__class__.__name__ == 'DamagedTank':
                el.update()
        font = pygame.font.Font(None, 23)
        line_rendered_red = font.render(f'{player.hp}', 1, pygame.Color('green'))
        line_rect_red = line_rendered_red.get_rect()
        line_rect_red.y = player.rect.y - 25
        if player.hp == 10:
            line_rect_red.x = player.rect.x + 12
        else:
            line_rect_red.x = player.rect.x + 15
        screen.blit(line_rendered_red, line_rect_red)
        pygame.display.flip()
        check_game_over = True
        if player not in player_group and len(tower_group) == 0:
            outro('Ничья', 1)
            check_game_over = False
        elif player not in player_group:
            outro('Вы проиграли...', 1)
            check_game_over = False
        elif len(tower_group) == 0:
            outro('Вы победили!', 1)
            check_game_over = False
        if not check_game_over:
            check_game_over = True
            running_vs_towers = False

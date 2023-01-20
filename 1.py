import pygame
import os
import sys
import pygame_gui

from pygame_gui.elements import UIButton
# ------------------------------------Бибилиотеки---------------------------------------------------

# --------------------------------Основная часть кода-----------------------------------------------
pygame.init()
size = width, height = 600, 700
screen = pygame.display.set_mode(size)
FPS = 12
running_2player = False
running_1player = False
clock = pygame.time.Clock()


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


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png'),
}
player_image = load_image('tank.png')
player_image = pygame.transform.scale(player_image, (41, 41))
player_image = pygame.transform.rotate(player_image, 270)
shell_image = load_image('shell.png', -1)
shell_image = pygame.transform.scale(shell_image, (19, 15))
tile_width = tile_height = 50


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
    pygame.display.set_caption('Конец игры')
    screen.fill((0, 0, 0))
    rules = ['Конец игры', "", text, '...',
             '...']
    fon = pygame.transform.scale(load_image('fon.jpg'), (600, 350))
    screen.blit(fon, (0, 300))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in rules:
        line_rendered = font.render(line, 1, pygame.Color('white'))
        line_rect = line_rendered.get_rect()
        text_coord += 10
        line_rect.top = text_coord
        line_rect.x = 10
        text_coord += line_rect.height
        screen.blit(line_rendered, line_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


# Загрузка уровня
def load_level(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        map_level = list(map(str.strip, file.readlines()))
        max_width = max(map(len, map_level))
        return list(map(lambda x: x.ljust(max_width, '.'), map_level))


# Класс плитки
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'wall':
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
                break
            if self.aim == 'player1' and pygame.sprite.collide_mask(self, player1):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                player1.rect.y = 5000
                player1.kill()
                break
            if self.aim == 'player' and pygame.sprite.collide_mask(self, player):
                screen.blit(boom_image, (self.rect.x - 23, self.rect.y - 21))
                self.kill()
                player.rect.y = 5000
                player.kill()
                break


# Генерация уровней
def generate_level(level):
    new_player, x, y = None, None, None
    new_player1, x1, y1 = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                if new_player is not None:
                    new_player1 = Player(x, y)
                else:
                    new_player = Player(x, y)
    return new_player, new_player1


# Запуск заставки и описание групп спрайтов
start_screen()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
shell_group = pygame.sprite.Group()
player = None
player1 = None
player1, player = generate_level(load_level('level2.txt'))
pygame.display.set_caption('Танчики')

# Игровой цикл для 2 игроков
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
    clock.tick(FPS)
    shell_group.update()
    pygame.display.flip()
    check_game_over = True
    if player not in player_group and player1 not in player_group:
        outro('Ничья')
        check_game_over = False
    elif player not in player_group:
        outro('Победил первый игрок')
        check_game_over = False
    elif player1 not in player_group:
        outro('Победил второй игрок')
        check_game_over = False
    if not check_game_over:
        terminate()

# Игровой цикл для 1 игрока
while running_1player:
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
    clock.tick(FPS)
    shell_group.update()
    pygame.display.flip()
    check_game_over = True
    if player not in player_group and player1 not in player_group:
        outro('Ничья')
        check_game_over = False
    elif player not in player_group:
        outro('Победил первый игрок')
        check_game_over = False
    elif player1 not in player_group:
        outro('Победил второй игрок')
        check_game_over = False
    if not check_game_over:
        terminate()
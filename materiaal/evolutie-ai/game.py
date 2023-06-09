import math

import neat.nn
import pygame
from pygame import mixer
import os
import random
import csv
from variables import *
import ai

mixer.init()
pygame.init()

class Game():
    def __init__(self, screen):
        # PYGAME SETUP #
        self.screen = screen
        pygame.display.set_caption('Platformer')
        font = pygame.font.SysFont('Futura', 30)
        # set framerate

        # create sprite groups
        self.enemy_group = pygame.sprite.Group()
        self.decoration_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()

        self.world = None
        self.world_data = []
        self.player = None
        self.intro_fade = None
        self.death_fade = None
        self.screen_scroll = 0

        ## OTHER SETUP ##
        # background
        self.pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
        self.pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
        self.mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
        self.sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()
        # store tiles in a list
        self.img_list = []
        for x in range(TILE_TYPES):
            img = pygame.image.load(f'img/Tile/{x}.png')
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            self.img_list.append(img)
        ##

    def draw_bg(self):
        self.screen.fill(BG)
        width = self.sky_img.get_width()
        for x in range(5):
            self.screen.blit(self.sky_img, ((x * width) - bg_scroll * 0.5, 0))
            self.screen.blit(self.mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - self.mountain_img.get_height() - 300))
            self.screen.blit(self.pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - self.pine1_img.get_height() - 150))
            self.screen.blit(self.pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - self.pine2_img.get_height()))

    # function to reset level
    def reset_level(self):
        global bg_scroll
        bg_scroll = 0
        self.enemy_group.empty()
        self.decoration_group.empty()
        self.water_group.empty()
        self.exit_group.empty()

        # create empty tile list
        data = []
        for row in range(ROWS):
            r = [-1] * COLS
            data.append(r)

        return data
    ###

    def create_world(self):
        # create screen fades
        self.intro_fade = ScreenFade(1, BLACK, 15, self)
        self.death_fade = ScreenFade(2, BLACK, 40000, self)

        # create empty tile list
        self.world_data = self.reset_level()
        for row in range(ROWS):
            r = [-1] * COLS
            self.world_data.append(r)
        # load in level data and create world
        with open(LEVEL, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world_data[x][y] = int(tile)

        self.world = World(self)
        self.player = self.world.process_data(self.world_data)

    def play(self):
        FPS = 70
        global level
        global start_game
        global start_intro
        global bg_scroll

        clock = pygame.time.Clock()

        self.create_world()

        run = True
        while run:
            clock.tick(FPS)

            if start_game == False:
                # draw menu
                self.screen.fill(BG)
            else:
                # update background
                self.draw_bg()
                # draw world map
                self.world.draw()

                # draw player
                self.player.update()
                self.player.draw()

                # draw enemies
                for enemy in self.enemy_group:
                    enemy.ai()
                    enemy.update()
                    enemy.draw()

                # update and draw groups
                self.decoration_group.update()
                self.water_group.update()
                self.exit_group.update()
                self.decoration_group.draw(self.screen)
                self.water_group.draw(self.screen)
                self.exit_group.draw(self.screen)

                # show intro
                if start_intro == True:
                    if self.intro_fade.fade():
                        start_intro = False
                        self.intro_fade.fade_counter = 0

                # update player actions
                if self.player.alive:
                    if self.player.in_air:
                        self.player.update_action(2)  # 2: jump
                    elif self.player.moving_left or self.player.moving_right:
                        self.player.update_action(1)  # 1: run
                    else:
                        self.player.update_action(0)  # 0: idle
                    self.screen_scroll, level_complete = self.player.move(self.player.moving_left, self.player.moving_right)
                    bg_scroll -= self.screen_scroll
                    # check if player has completed the level
                    if level_complete:
                        start_intro = True
                        level += 1
                        bg_scroll = 0
                        self.world_data = self.reset_level()
                        if level <= MAX_LEVELS:
                            # load in level data and create world
                            with open(LEVEL, newline='') as csvfile:
                                reader = csv.reader(csvfile, delimiter=',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        self.world_data[x][y] = int(tile)
                            self.world = World(self)
                            self.player = self.world.process_data(self.world_data)
                else:
                    self.screen_scroll = 0
                    if self.death_fade.fade():
                        self.death_fade.fade_counter = 0
                        start_intro = True
                        bg_scroll = 0
                        self.world_data = self.reset_level()
                        # load in level data and create world
                        with open(LEVEL, newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    self.world_data[x][y] = int(tile)
                        self.world = World(self)
                        self.player = self.world.process_data(self.world_data)

            # controls
            for event in pygame.event.get():
                # quit game
                if event.type == pygame.QUIT:
                    run = False
                # keyboard presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.player.moving_left = True
                    if event.key == pygame.K_d:
                        self.player.moving_right = True
                    if event.key == pygame.K_w and self.player.alive:
                        self.player.jump = True
                    if event.key == pygame.K_ESCAPE:
                        run = False

                # keyboard button released
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.player.moving_left = False
                    if event.key == pygame.K_d:
                        self.player.moving_right = False
            pygame.display.update()

    def train_ai(self, genome, config):
        global level
        global start_game
        global start_intro
        global start_intro
        global bg_scroll
        global level_complete

        clock = pygame.time.Clock()

        self.create_world()


        net = neat.nn.FeedForwardNetwork.create(genome, config)

        fitness_counter_of_doom = 0
        run = True
        while run:
            clock.tick(FPS)

            fitness_counter_of_doom = fitness_counter_of_doom + FITNESS_PENALTY * 0.1
            self.player.fitness = self.player.fitness - 0.005

            # update background
            self.draw_bg()
            # draw world map
            self.world.draw()

            # draw player
            self.player.update()
            self.player.draw()

            # draw enemies
            for enemy in self.enemy_group:
                enemy.ai()
                enemy.update()
                enemy.draw()

            # update and draw groups
            self.decoration_group.update()
            self.water_group.update()
            self.exit_group.update()
            self.decoration_group.draw(self.screen)
            self.water_group.draw(self.screen)
            self.exit_group.draw(self.screen)

            # show intro
            if start_intro == True:
                if self.intro_fade.fade():
                    start_intro = False
                    self.intro_fade.fade_counter = 0

            # update player actions
            if self.player.alive:
                if fitness_counter_of_doom > self.player.fitness:
                    self.player.health = 0
                if self.player.fitness <= 0:
                    self.player.health = 0
                if self.player.in_air:
                    self.player.update_action(2)  # 2: jump
                elif self.player.moving_left or self.player.moving_right:
                    self.player.update_action(1)  # 1: run
                else:
                    self.player.update_action(0)  # 0: idle
                self.screen_scroll, level_complete = self.player.move(self.player.moving_left, self.player.moving_right)
                bg_scroll -= self.screen_scroll
                # check if player has completed the level
                if level_complete:
                    self.player.fitness = 50000
            else:
                self.player.fitness = self.player.fitness - 5

            #print(self.player.rect.x)
            #print(self.player.fitness)
            # checks
            if not self.player.alive or level_complete:
                genome.fitness = self.player.fitness
                break

            output = net.activate(ai.get_input(self.player, self.world_data, self))
            decision = output.index(max(output))

            if decision == 0:  # do nothing
                self.player.moving_left = False
                self.player.moving_right = False
            elif decision == 1:  # go left
                self.player.moving_left = True
                self.player.moving_right = False
            elif decision == 2:  # go right
                self.player.moving_left = False
                self.player.moving_right = True
            else:  # jump
                if self.player.alive:
                    self.player.jump = True
                    # jump_fx.play()

            # controls for user
            for event in pygame.event.get():
                # quit game
                if event.type == pygame.QUIT:
                    run = False
                # keyboard presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

            pygame.display.update()


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.sees_player = False
        self.idling = False
        self.idling_counter = 0
        self.moving_left = False
        self.moving_right = False
        self.field_of_vision = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE * 8, TILE_SIZE * 6)
        self.in_lead = False

        # load all images for the players
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.fitness = self.rect.x * 0.1
        self.forward_counter = 0

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.forward_counter > 50:
            self.fitness = self.fitness + 10
            self.forward_counter = 0
        # ddx = self.rect.x
        # if self.rect.x > ddx:
        #     self.fitness = self.fitness + 100 * 0.1
        # elif self.rect.x < ddx:
        #     self.fitness = self.fitness - 100 * 0.1

    def move(self, moving_left, moving_right):
        # reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -14
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # check for collision
        for tile in self.game.world.obstacle_list:
            # check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                # if the ai has hit a wall then make it turn around
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            # check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # check for collision with water
        if pygame.sprite.spritecollide(self, self.game.water_group, False):
            self.health = 0

        # check for collision with enemy
        if pygame.sprite.spritecollide(self, self.game.enemy_group, False) and self.char_type == 'player':
            self.health = 0

        # check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, self.game.exit_group, False):
            level_complete = True

        # check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        # check if going off the edges of the screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        # update rectangle position
        self.forward_counter += dx
        self.rect.x += dx
        self.rect.y += dy
        self.field_of_vision = self.rect.x
        self.field_of_vision = self.rect.y

        # update scroll based on player position
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (
                    self.game.world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
                    or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def ai(self, scroll=-50):
        """
        The movement and behaviour of the ai/enemy soldier
        """
        if self.alive and self.game.player.alive:
            if self.idling == False and random.randint(1, 200) == 1 and self.sees_player == False:
                self.update_action(0)  # 0: idle
                self.idling = True
                self.idling_counter = 50
            # check if the ai in near the player
            if self.vision.colliderect(self.game.player.rect):
                # run towards player
                self.sees_player = True
                if self.direction == 1:
                    ai_moving_right = True
                else:
                    ai_moving_right = False
                ai_moving_left = not ai_moving_right
                self.move(ai_moving_left, ai_moving_right)
                self.update_action(1)  # 1: run
            else:
                self.sees_player = False
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)  # 1: run
                    self.move_counter += 1
                    # update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        self.rect.x += self.game.screen_scroll

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        self.game.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        colour = (0, 255, 255)
        if self.char_type == 'player' and see_field_of_vision == True:
            pygame.draw.rect(self.game.screen, colour,
                             pygame.Rect(self.rect.x - 4 * TILE_SIZE, self.rect.y - 4 * TILE_SIZE, TILE_SIZE * 10,
                                         TILE_SIZE * 8), 2)

class World():
    def __init__(self, game):
        self.game = game
        self.obstacle_list = []
        self.player_x = 0
        self.player_y = 0

    def process_data(self, data):
        self.level_length = len(data[0])
        # iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = self.game.img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE, self.game)
                        self.game.water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE, self.game)
                        self.game.decoration_group.add(decoration)
                    elif tile == 15:  # create player
                        player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, 1.7, 5, self.game)
                        self.player_x = x
                        self.player_y = y
                    elif tile == 16:  # create enemies
                        enemy = Soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.5, 0.1, self.game)
                        self.game.enemy_group.add(enemy)
                    elif tile == 20:  # create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE, self.game)
                        self.game.exit_group.add(exit)
        return player

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += self.game.screen_scroll
            self.game.screen.blit(tile[0], tile[1])

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += self.game.screen_scroll

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += self.game.screen_scroll

# the exit sign
class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
            self.rect.x += self.game.screen_scroll

class ScreenFade():
    def __init__(self, direction, colour, speed, game):
        self.game = game
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:  # whole screen fade
            pygame.draw.rect(self.game.screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(self.game.screen, self.colour,
                             (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(self.game.screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(self.game.screen, self.colour,
                             (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.direction == 2:  # vertical screen fade down
            pygame.draw.rect(self.game.screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True

        return fade_complete
##


if __name__ == '__main__':
    g1 = Game(pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)))
    g2 = Game(pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)))
    g1.play()
    g2.play()

    pygame.quit()
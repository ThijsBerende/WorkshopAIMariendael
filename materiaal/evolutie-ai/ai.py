import neat
from game import *
from variables import *


def get_closest_enemy(player, game):
    distances = []
    enemies = []
    for enemy in game.enemy_group:
        distances.append(math.sqrt((enemy.rect.x - player.rect.x) ** 2 + (enemy.rect.y - player.rect.y) ** 2))
        enemies.append(enemy)

    closest_distance = min(distances)
    closest_enemy = enemies[distances.index(closest_distance)]

    return closest_distance, closest_enemy.rect.x, closest_enemy.rect.y

def get_input(player, world_data, game):
    input = []

    input.append(player.rect.x)
    input.append(player.rect.y)

    enemy_dist, enemy_x, enemy_y = get_closest_enemy(player, game)
    input.append(enemy_dist)
    input.append(enemy_x)
    input.append(enemy_y)

    vis = []
    for row in range(ROWS):
        r = [-1] * COLS
        vis.append(r)
    vis.append(r)
    bot_x = int(player.rect.x / TILE_SIZE)
    bot_y = int(player.rect.y / TILE_SIZE)
    for horizontal in range(-4, 6):  # 3 to the left, 5 to right 4left,5right(-4, 6)
        for vertical in range(-4, 4):  # 4 up, 3 down 3up,2down(-3,3) (-4,-4
            tile_y = bot_y + vertical
            tile_x = bot_x + horizontal
            if 0 <= tile_y < ROWS and 0 <= tile_x < COLS:
                current_tile = world_data[tile_y][tile_x]
                if current_tile >= 0 and current_tile <= 8:
                    vis[tile_y][tile_x] = 50
                    input.append(50)
                elif current_tile == 12:
                    vis[tile_y][tile_x] = 100
                    input.append(100)
                elif current_tile >= 9 and current_tile <= 10:
                    vis[tile_y][tile_x] = 0
                    input.append(0)
                else:
                    vis[tile_y][tile_x] = -50
                    input.append(-50)
            else:
                input.append(-50)

    # print("------------------------")
    # for vi in vis:
    #     print(vi)

    return input


def eval_genomes(genomes, config):
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0
        game = Game(window)
        game.train_ai(genome, config)


def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    p.run(eval_genomes, 100)  # second argument represents the number of generations


if __name__ == '__main__':
    config_path = "./config.txt"
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)


    run_neat(config)
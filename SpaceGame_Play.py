import pygame
from Spaceship import Spaceship
from Bullet import Bullet
from Enemy import EnemyWave
import neat
import os
import time

pygame.init()
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BACKGROUND = back = pygame.image.load("images/back.jpg")

def draw_screen(screen, score, highscore):
    screen.fill((0,0,0))
    screen.blit(BACKGROUND,(0,0))
    font = pygame.font.SysFont("comicsans", 40)
    showscore = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(showscore,(SCREEN_WIDTH - 10 - showscore.get_width(), 10))              
    showscore = font.render(f"High Score: {highscore}", True, (255, 255, 255))
    screen.blit(showscore,(10, 10))

def main(genomes, config):
    # create our screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Check for a highscore file if not set to 0
    try:
        f=open("highscore.txt", "r")
        highscore = int(f.readline())
        f.close()
    except:
        highscore = 0

    

    score = 0
    running = True

    
    clock = pygame.time.Clock()

    nets = []
    ge = []
    spaceships = []
    bullets = []
    enemy_waves = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        spaceships.append(Spaceship())
        bullets.append(Bullet())
        enemy_waves.append(EnemyWave(5, spaceships[_-1]))
        g.fitness = 0
        ge.append(g)
    

    while running:
        draw_screen(screen, score, highscore)
        dt = clock.tick(60)
        speed = 1 / float(dt)

        for spaceship in spaceships:
            spaceship.move(screen)

        pygame.display.update()
        time.sleep(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            spaceship.check_move(event, speed)
            bullet.check_move(event, spaceship.x, spaceship.y)

        result = enemy_wave.check(screen, bullet, spaceship, speed)
        if result >= 0:
            score += result
        else:
            running = False
            if score > int(highscore):
                f=open("highscore.txt", "w")
                f.write(str(score))
                f.close()

        pygame.display.update()
    pygame.quit()

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
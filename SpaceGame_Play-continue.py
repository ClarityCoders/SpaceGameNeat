import pygame
from Spaceship import Spaceship
from Bullet import Bullet
from Enemy import EnemyWave
import neat
import os
import pickle
pygame.font.init()


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BACKGROUND = back = pygame.image.load("images/back.jpg")
generation = 0

def draw_screen(screen, score, highscore, alive, gen):
    font = pygame.font.SysFont("comicsans", 30)
    showscore = font.render(f"Max Score: {score}", True, (255, 255, 255))
    screen.blit(showscore,(SCREEN_WIDTH - 10 - showscore.get_width(), 10))              
    showscore = font.render(f"High Score: {highscore}", True, (255, 255, 255))
    showscore = font.render(f"Alive: {alive}", True, (255, 255, 255))
    screen.blit(showscore,(10, 450))
    showscore = font.render(f"Generation: {gen}", True, (255, 255, 255))
    screen.blit(showscore,(10, 475))

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

    run = True
    clock = pygame.time.Clock()

    global generation 
    generation += 1

    scores = []
    nets = []
    ge = []
    spaceships = []
    bullets = []
    enemy_waves = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        currentShip = Spaceship()
        spaceships.append(currentShip)
        bullets.append(Bullet())
        enemy_waves.append(EnemyWave(5, currentShip))
        scores.append(0)
        g.fitness = 0
        ge.append(g)
    
    max_score = 0
    while run:
        #screen.fill((0,0,0))
        #screen.blit(BACKGROUND,(0,0))   
        dt = clock.tick(60)
        speed = 1 / float(dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        for i, spaceship in enumerate(spaceships):
            output = nets[i].activate((
                spaceship.x, spaceship.y, 
                bullets[i].shoot,
                enemy_waves[i].enemy_list[0].x, enemy_waves[i].enemy_list[0].y,
                enemy_waves[i].enemy_list[1].x, enemy_waves[i].enemy_list[1].y,
                enemy_waves[i].enemy_list[2].x, enemy_waves[i].enemy_list[2].y,
                enemy_waves[i].enemy_list[3].x, enemy_waves[i].enemy_list[3].y,
                enemy_waves[i].enemy_list[4].x, enemy_waves[i].enemy_list[4].y
            ))
            #print(output)

            # Should we shoot?
            if output[4] > .5:
                if not bullets[i].shoot:
                    bullets[i].x = spaceship.x + 32 - (bullets[i].img.get_rect().size[0] / 2 )
                    bullets[i].y = spaceship.y - bullets[i].img.get_rect().size[1]
                    bullets[i].shoot = True

            # Should we move up or down or neither?
            if output[0] > 0 or output[1] > 0:
                # Which is bigger?
                if output[0] > output[1]:
                
                    # move up
                    spaceship.move_y -= spaceship.vel * speed
                
                else:
                    spaceship.move_y += spaceship.vel * speed


            # Should we move left or right or neither?
            if output[2] > 0 or output[3] > 0:
                # Which is bigger?
                if output[2] > output[3]:
                
                    # move left
                    spaceship.move_x -= spaceship.vel * speed
                
                else:
                    spaceship.move_x += spaceship.vel * speed

            #spaceship.check_move(event, speed)
            #bullets[i].check_move(event, spaceship.x, spaceship.y)
            ge[i].fitness += .5
            spaceship.move(screen)
            spaceship.move_x = 0
            spaceship.move_y = 0

            result = enemy_waves[i].check(screen, bullets[i], spaceship, speed)
            if result >= 0:
                scores[i] += result
                ge[i].fitness += result * 5
            else:
                # run = False
                # if score > int(highscore):
                #     f=open("highscore.txt", "w")
                #     f.write(str(score))
                #     f.close()
                ge[i].fitness -= 5
                spaceships.pop(i)
                enemy_waves.pop(i)
                bullets.pop(i)
                nets.pop(i)
                scores.pop(i)
                ge.pop(i)
        #draw_screen(screen, max_score, highscore, len(spaceships), generation)
        #pygame.display.update()
        if len(spaceships) == 0:
            print(f"Max Score {generation}: {max_score}")
            run = False
            break
        elif max(scores) > max_score:
            max_score = max(scores)
    #pygame.quit()

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_path)

    #p = neat.Population(config)
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-99')
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.Checkpointer(10))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 1000)
    print(f"\nBest genome:\n{winner}")
    with open("winner.data", "wb") as data_update:
            pickle.dump(winner, data_update)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
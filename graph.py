import neat
import visualize
import os
import pickle

with open("winner.data", "rb") as load:
        winner = pickle.load(load)

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, "config-feedforward.txt")
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_path)
visualize.draw_net(config, winner, True)
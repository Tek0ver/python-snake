import os, neat, pickle
from game import Game

# see neat-python documentations about the run function
# (https://neat-python.readthedocs.io/en/latest/xor_example.html#example-source)
def run(config_path):

    # load configuration
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    # create the population, which is the top-level object for a NEAT run
    p = neat.Population(config)

    # to load from checkpoint
    # p = neat.Checkpointer.restore_checkpoint('checkpoint-name')

    # add a stdout reporter to show progress in the terminal
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # run for up to 100 generations
    winner = p.run(game.run, 100)
    # save the best AI
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-neat-00.txt")
    game = Game()
    run(config_path)

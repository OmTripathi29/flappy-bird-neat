import os
import neat
from main import Game
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BEST_BIRD_PATH = os.path.join(BASE_DIR, "models", "best_genome.pkl")

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "neat_config.txt")

PIPE_REWARD=1000
MAX_FRAMES=20000

def eval_genomes(genomes, config):
    game=Game(draw=False)
    entries=[]
    for genome_id,genome in genomes:
        genome.fitness=0
        net=neat.nn.FeedForwardNetwork.create(genome, config)
        bird=game.add_birds()
        entries.append((genome, net, bird))
    frames=0
    while frames<MAX_FRAMES:
        actions=[]
        for genome,net,bird in entries:
            if bird.alive:
                output=net.activate(game.get_inputs(bird))
                actions.append(output[0]>0.5)
        score_before=game.score
        anyone_alive=game.step(actions)
        
        pipes_cleared=game.score-score_before
        for genome,net,bird in entries:
            if bird.alive:
                genome.fitness+=1
                genome.fitness+=pipes_cleared*PIPE_REWARD
        if not anyone_alive:
            break
        
        frames+=1

def load_config():
    config=neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                       neat.DefaultSpeciesSet, neat.DefaultStagnation,
                       CONFIG_PATH)
    return config
def run(generations=30):
    config=load_config()
    pop=neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    winner=pop.run(eval_genomes, generations)
    
   
    
  
    os.makedirs(os.path.dirname(BEST_BIRD_PATH), exist_ok=True)
    with open(BEST_BIRD_PATH, "wb") as f:
        pickle.dump(winner, f)
    print("Best genome saved to", BEST_BIRD_PATH )
    return winner

if __name__=="__main__":
    run()
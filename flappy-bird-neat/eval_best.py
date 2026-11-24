import pickle
import neat
from main import Game
from train import load_config, BEST_BIRD_PATH,MAX_FRAMES

config = load_config()
with open(BEST_BIRD_PATH, "rb") as f:
    genome = pickle.load(f)
net = neat.nn.FeedForwardNetwork.create(genome, config)

results = []
for i in range(20):
    game = Game(draw=False)
    bird = game.add_birds()
    frames = 0
    while frames < MAX_FRAMES:
        jump = net.activate(game.get_inputs(bird))[0] > 0.5
        if not game.step([jump]):
            break
        frames += 1
    results.append(game.score)

print("pipes per game:", results)
print("average:", sum(results) / len(results))
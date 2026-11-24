import os
import pickle
import neat
import pygame
from main import Game, SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from train import BEST_BIRD_PATH, load_config

HIGH_SCORE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_score.txt")


def load_high_score():
    try:
        with open(HIGH_SCORE_PATH) as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0


def save_high_score(value):
    with open(HIGH_SCORE_PATH, "w") as f:
        f.write(str(value))


config = load_config()
with open(BEST_BIRD_PATH, "rb") as f:
    genome = pickle.load(f)
net = neat.nn.FeedForwardNetwork.create(genome, config)

game = Game(draw=True)
game.high_score = load_high_score()
bird = game.add_birds()

big_font = pygame.font.SysFont("Arial", 56, bold=True)
mid_font = pygame.font.SysFont("Arial", 32, bold=True)
retry_button = pygame.Rect(SCREEN_WIDTH // 2 - 90, 400, 180, 60)
dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
dim.fill((0, 0, 0, 150))

game_over = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if retry_button.collidepoint(event.pos):
                game.reset()
                bird = game.add_birds()
                game_over = False

    if not game_over:
        jump = net.activate(game.get_inputs(bird))[0] > 0.5
        if not game.step([jump]):
            game_over = True
            save_high_score(game.high_score)
        game.draw()
    else:
        game.render()
        game.screen.blit(dim, (0, 0))

        title = big_font.render("Game Over", True, (255, 255, 255))
        score_text = mid_font.render(f"Score: {game.score}   Best: {game.high_score}", True, (255, 255, 255))
        game.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 250))
        game.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 330))

        pygame.draw.rect(game.screen, (60, 180, 75), retry_button, border_radius=12)
        label = mid_font.render("Retry", True, (255, 255, 255))
        game.screen.blit(label, label.get_rect(center=retry_button.center))

        pygame.display.flip()
        game.clock.tick(FPS)

save_high_score(game.high_score)
pygame.quit()
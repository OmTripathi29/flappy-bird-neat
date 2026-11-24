import pygame
from main import Game

game = Game(draw=True)
bird = game.add_birds()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    jump = game.get_inputs(bird)[3] > 0.05
    if not game.step([jump]):
        game.reset()
        bird = game.add_birds()

    game.draw()

pygame.quit()
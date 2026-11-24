import pygame
import random

pygame.init()
SCREEN_WIDTH  = 600
SCREEN_HEIGHT = 700
FPS           = 90
BIRD_X        = 120
BIRD_RADIUS   = 18
BIRD_COLORS   = (255, 220, 50)
JUMP_VELOCITY = -9
GRAVITY       = 0.5
MAX_FALL_SPEED = 12
GROUND_HEIGHT = 80
GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT
PIPE_WIDTH = 70
PIPE_GAP = 170
PIPE_SPEED = 5
PIPE_COLOR = (60,180, 75)
PIPE_SPACING=400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird AI")
clock = pygame.time.Clock()
font=pygame.font.SysFont("Arial", 48,bold=True)

class Bird:
    def __init__(self):
        self.x=BIRD_X
        self.y=SCREEN_HEIGHT//2
        self.velocity=0
        self.alive=True
    
    def jump(self):
        self.velocity=JUMP_VELOCITY
    
    def update(self):
        self.velocity=min(self.velocity + GRAVITY, MAX_FALL_SPEED)
        self.y+=self.velocity
    
    def get_rect(self):
        return pygame.Rect(self.x-BIRD_RADIUS, self.y-BIRD_RADIUS, BIRD_RADIUS*2, BIRD_RADIUS*2)
    
    def is_out_of_bounfs(self):
        return self.y-BIRD_RADIUS < 0 or self.y+BIRD_RADIUS > GROUND_Y
    
    def draw(self, surface):
        pygame.draw.circle(surface, BIRD_COLORS, (self.x, int(self.y)), BIRD_RADIUS)

def new_pipe(x):
    return {"x":x,
            "gap_top":random.randint(80, GROUND_Y - PIPE_GAP - 80),
            "passed":False}

def reset():
    return Bird(),[new_pipe(SCREEN_WIDTH)],0
        
bird,pipes,score=reset()

running = True

    
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.jump()
    
    bird.update()
    
    for pipe in pipes:
        pipe['x']-=PIPE_SPEED
        if not pipe["passed"] and pipe["x"]+PIPE_WIDTH<BIRD_X:
            score+=1
            pipe["passed"]=True
    
    if pipes[0]["x"]+PIPE_WIDTH<0:
        pipes.pop(0)
    
    if pipes[-1]["x"] < SCREEN_WIDTH - PIPE_SPACING:
        pipes.append(new_pipe(SCREEN_WIDTH))
    
    bird_rect=bird.get_rect()
    dead=False
    if bird.is_out_of_bounfs():
        dead=True
    
    for pipe in pipes:
        bottom_y=pipe["gap_top"]+PIPE_GAP
        top_rect=pygame.Rect(pipe["x"],0,PIPE_WIDTH,pipe["gap_top"])
        bottom_rect=pygame.Rect(pipe["x"],bottom_y,PIPE_WIDTH,GROUND_Y-bottom_y)
        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            dead=True
    
    if dead:
        bird,pipes,score=reset()
    
    screen.fill((112, 197, 255))
    for pipe in pipes:
        bottom_y=pipe["gap_top"]+PIPE_GAP
        pygame.draw.rect(screen,PIPE_COLOR,(pipe["x"],0,PIPE_WIDTH,pipe["gap_top"]))
        pygame.draw.rect(screen,PIPE_COLOR,(pipe["x"],bottom_y,PIPE_WIDTH,GROUND_Y-bottom_y))
    pygame.draw.rect(screen,(222,185,120),(0,GROUND_Y,SCREEN_WIDTH,GROUND_HEIGHT))
    bird.draw(screen)
    score_surface=font.render(str(score),True,(255,255,255))
    screen.blit(score_surface,(SCREEN_WIDTH//2-score_surface.get_width()//2,30))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
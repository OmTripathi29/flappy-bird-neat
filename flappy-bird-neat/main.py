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
PIPE_SPEED = 5
PIPE_COLOR = (60,180, 75)
PIPE_GAP_MIN=130
PIPE_GAP_MAX=180
PIPE_SPACING_MIN=300
PIPE_SPACING_MAX=450

class Game:
    def __init__(self,draw=True):
        self.draw_enabled=draw
        self.high_score=0
        if draw:
            self.small_font=pygame.font.SysFont("Arial", 28,bold=True)
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Flappy Bird AI")
            self.clock = pygame.time.Clock()
            self.font=pygame.font.SysFont("Arial", 48,bold=True)
        self.reset()
    
    def reset(self):
        self.birds=[]
        self.pipes=[new_pipe(SCREEN_WIDTH)]
        self.score=0
    
    def add_birds(self):
        bird=Bird()
        self.birds.append(bird)
        return bird
    
    def alive_birds(self):
        return [b for b in self.birds if b.alive]
    
    def next_pipe(self,bird):
        for pipe in self.pipes:
            if pipe["x"]+PIPE_WIDTH>=bird.x:
                return pipe
        return None
    def get_inputs(self,bird):
        pipe=self.next_pipe(bird)
        if pipe is None:
            return [bird.y/SCREEN_HEIGHT,bird.velocity/MAX_FALL_SPEED,1.0,0.0,0.5]
        gap_centre=pipe["gap_top"]+pipe["gap"]/2
        return[bird.y/SCREEN_HEIGHT,
               bird.velocity/MAX_FALL_SPEED,
               (pipe["x"]-bird.x)/SCREEN_WIDTH,
               (bird.y-gap_centre)/SCREEN_HEIGHT,
               pipe["gap_top"]/SCREEN_HEIGHT]
    
    def step(self,actions=None):
        alive=self.alive_birds()
        for i,bird in enumerate(alive):
            if actions is not None and i<len(actions) and actions[i]:
                bird.jump()
            bird.update()
        for pipe in self.pipes:
            pipe["x"]-=PIPE_SPEED
            if not pipe["passed"] and pipe["x"]+PIPE_WIDTH<BIRD_X:
                pipe["passed"]=True
                self.score+=1
            top,bottom=pipe_rects(pipe)
            for bird in alive:
                rect=bird.get_rect()
                if rect.colliderect(top) or rect.colliderect(bottom):
                    bird.alive=False
        if self.pipes[0]["x"]+PIPE_WIDTH<0:
            self.pipes.pop(0)
        if self.pipes[-1]["x"] < SCREEN_WIDTH - self.pipes[-1]["spacing"]:
            self.pipes.append(new_pipe(SCREEN_WIDTH))
        
        for bird in alive:
            if bird.is_out_of_bounfs():
                bird.alive=False
        if self.score>self.high_score:
            self.high_score=self.score
        return len(self.alive_birds())>0
    def render(self):
        self.screen.fill((112, 197, 255))
        for pipe in self.pipes:
            top,bottom=pipe_rects(pipe)
            pygame.draw.rect(self.screen,PIPE_COLOR,top)
            pygame.draw.rect(self.screen,PIPE_COLOR,bottom)
        pygame.draw.rect(self.screen,(222,185,120),(0,GROUND_Y,SCREEN_WIDTH,GROUND_HEIGHT))
        for bird in self.alive_birds():
            bird.draw(self.screen)
        score_surface=self.font.render(str(self.score),True,(255,255,255))
        self.screen.blit(score_surface,(SCREEN_WIDTH//2-score_surface.get_width()//2,30))
        best_surface=self.small_font.render("Best: "+str(self.high_score),True,(255,255,255))
        self.screen.blit(best_surface,(10,10))
    def draw(self):
        self.render()
        pygame.display.flip()
        self.clock.tick(FPS)

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
    gap= random.randint(PIPE_GAP_MIN, PIPE_GAP_MAX)
    return {"x":x,
            "gap":gap,
            "gap_top":random.randint(80, GROUND_Y - gap - 80),
            "spacing":random.randint(PIPE_SPACING_MIN, PIPE_SPACING_MAX),
            "passed":False}
def pipe_rects(pipe):
    bottom_y=pipe["gap_top"]+pipe["gap"]
    top=pygame.Rect(pipe["x"],0,PIPE_WIDTH,pipe["gap_top"])
    bottom=pygame.Rect(pipe["x"],bottom_y,PIPE_WIDTH,GROUND_Y-bottom_y)
    return top,bottom



if __name__=="__main__":
    game=Game(draw=True)
    bird=game.add_birds()
    running=True
    while running:
        jump=False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jump=True
        still_playing=game.step([jump])
        
        if not still_playing:
            game.reset()
            bird=game.add_birds()
        
        game.draw()
    pygame.quit()


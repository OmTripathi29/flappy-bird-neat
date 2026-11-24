import time
from main import Game
game=Game(draw=False)
bird=game.add_birds()

start=time.perf_counter()
frames=0
while frames<20000:
    inputs=game.get_inputs(bird)
    jump=inputs[3]>0.05
    
    if not game.step([jump]):
        break
    frames+=1
elapsed=time.perf_counter()-start
print("frames survived:",frames,"| score:",game.score,"| seconds:",round(elapsed,3))
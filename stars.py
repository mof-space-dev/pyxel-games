import pyxel
import random

WIDTH, HEIGHT = 160, 120
STAR_COUNT = 100

# 星の座標(ランダム)
stars = [(random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1),random.randint(1, 7)) for _ in range(STAR_COUNT)]

pyxel.init(WIDTH, HEIGHT, title="Stars", fps=30)

def update():
    pass
  
def draw():
    pyxel.cls(0)
    
    for x, y , col in stars:
        pyxel.pset(x, y, col)

pyxel.run(update, draw)
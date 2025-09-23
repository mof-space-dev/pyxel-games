#風船7つが斜めにふわふわ動く
# 30個の星がチカチカ光っている
# タイトル文字は色が変化して光ってるように見える
# 全自動で眺めるだけのデモ画面

import pyxel
import random

pyxel.init(160, 120, title="in---1980 Demo")

# 風船リスト
ballons = [
  {
    "x": random.randint(10, 150),
    "y": random.randint(20, 100), 
    "dx": random.choice([-1, 1]), 
    "dy": random.choice([-1, 1]),
    "color": random.randint(8, 15)
  }
  for _ in range(7)
]

# ランダムな星の位置
stars = [
  {
    "x": random.randint(0, 159),
    "y": random.randint(0, 119),
  }
  for _ in range(30)
]

def update():
    # 風船を動かす
    for b in ballons:
        b["x"] += b["dx"]
        b["y"] += b["dy"]
        # 画面端で跳ね返る
        if b["x"] < 5 or b["x"] > 155:
            b["dx"] *= -1
        if b["y"] < 5 or b["y"] > 105:
            b["dy"] *= -1
            
def draw_ballon(x, y, color):
    pyxel.circ(x, y, 4, color)
    pyxel.line(x, y + 5, x, y + 10, 13)

def draw():
    pyxel.cls(0)
    
    # 星を描く
    for s in stars:
        pyxel.pset(s["x"], s["y"], 7)
    
    # 光るタイトルっぽく
    pyxel.text(60, 100, "in 1980 --- DEMO", pyxel.frame_count % 16)
    
    # 風船を描く
    for b in ballons:
        draw_ballon(b["x"], b["y"], b["color"])

pyxel.run(update, draw)
import pyxel
import random
import math
import time

WIDTH, HEIGHT = 160, 120

# 敵キャラ
enemy = {
    "x": 0, 
    "y": 50, 
    "dx": 2,
    "angle": 0,
    "size": 16, 
    "absorbing": False, 
    "alive": True,
    "frame": 0
 }

# 消失点
vanish_x, vanish_y = WIDTH // 2, HEIGHT // 2

# 点のリスト
num_dots = 100
dots = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT)} for _ in range(num_dots)]

def reset_enemy():
    # 敵キャラを画面端に再配布 再出現
    enemy["x"] = random.randint(0, WIDTH - enemy["size"])
    enemy["y"] = random.randint(20, HEIGHT - 20)
    enemy["dx"] = 2 if random.choice([True, False]) else -2
    enemy["angle"] = 0
    enemy["absorbing"] = False
    enemy["alive"] = True
    enemy["frame"] = 0


def update():
    # -- 敵キャラ --
    if enemy["alive"]:
        enemy["frame"] += 1
        
        if not enemy["absorbing"]:
            # 最初の3秒は左右移動
            enemy["x"] += enemy["dx"]
            if enemy["x"] < 0 or enemy["x"] > WIDTH - enemy["size"]:
                enemy["dx"] *= -1
            if enemy["frame"] > 180:
                # 3秒経過したら吸い込み開始
                enemy["absorbing"] = True
        else:
            # 吸い込み 回転
            dx_e = vanish_x - enemy["x"]
            dy_e = vanish_y - enemy["y"]
            dist = math.hypot(dx_e, dy_e)
            if dist > 1:
                enemy["x"] += dx_e / dist * 2
                enemy["y"] += dy_e / dist * 2
                enemy["angle"] += 10 # 回転量(度数)
            else:
                # 消失点到達で画面外へ戻す
                enemy["alive"] = False
                enemy["frame"] = 0
    else:
        # 敵キャラが消えた後少しフレーム経過したら再登場
        enemy["frame"] += 1
        if enemy["frame"] > 60:
            reset_enemy()
        
    # 点を消失点に吸い込む
    for d in dots:
        # 方向ベクトル
        dx_d = vanish_x - d["x"]
        dy_d = vanish_y - d["y"]
        dist = math.hypot(dx_d, dy_d)
        if dist > 1:
            d["x"] += dx_d / dist * 2 # 速度調整
            d["y"] += dy_d / dist * 2
        else:
            # 消失点に到達したら画面端にランダムで戻す
            d["x"] = random.randint(0, WIDTH)
            d["y"] = random.randint(0, HEIGHT)

        
def draw():
    
     pyxel.cls(0)
     
     # 吸い込まれる線
     for i in range(-WIDTH//2, WIDTH + WIDTH//2, 8):
         pyxel.line(i, HEIGHT, vanish_x, vanish_y, 1)
         pyxel.line(i, -HEIGHT, vanish_x, vanish_y, 1)
         
    # 無数の点(吸い込まれる)
     for d in dots:
         pyxel.pset(int(d["x"]), int(d["y"]), 7)
        
    
     # 適当な敵キャラ(回転表現は簡易的に四角を斜めに)
     if enemy["alive"]:
        size = enemy["size"]
        x, y = enemy["x"], enemy["y"]
        angle = enemy["angle"]
        # 回転を簡易的に表すために頂点をずらす
        offset = (math.sin(math.radians(angle)) * size/2)
        
        pyxel.rect(int(x - offset), int(y - offset), size, size, 15) # 体
        pyxel.pset(int(x - offset + 4), int(y - offset + 4), 0) # 左目
        pyxel.pset(int(x - offset + 11), int(y - offset + 4), 0) # 右目
     
     # タイトルロゴ
     pyxel.text(15, 25, "80's DEMO ", 2)

pyxel.init(WIDTH, HEIGHT, title="onCV")
pyxel.run(update, draw)
    
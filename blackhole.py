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
    "start_dist": 0, 
    "frozen": False,
    "freeze_frame": 0,
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
    enemy["frozen"] = False
    enemy["freeze_frame"] = 0


def update():
    # -- 敵キャラ --
    if enemy["alive"]:
        enemy["frame"] += 1
        if enemy["frozen"]:
            # 一番小さくなった瞬間で停止
            enemy["freeze_frame"] += 1
            if enemy["freeze_frame"] > 60:
                enemy["alive"] = False
                enemy["frame"] = 0
                enemy["frozen"] = False
                enemy["freeze_frame"] = 0
        
        elif not enemy["absorbing"]:
            # 最初の3秒は左右移動
            enemy["x"] += enemy["dx"]
            if enemy["x"] < 0 or enemy["x"] > WIDTH - enemy["size"]:
                enemy["dx"] *= -1
            if enemy["frame"] > 180:
                # 3秒経過したら吸い込み開始
                enemy["absorbing"] = True
                cx = enemy["x"] + enemy["size"] / 2
                cy = enemy["y"] + enemy["size"] / 2
                enemy["start_dist"] = math.hypot(vanish_x - cx, vanish_y - cy)
        else:
            # 吸い込み 回転
            cx = enemy["x"] + enemy["size"] / 2
            cy = enemy["y"] + enemy["size"] / 2
            dx_e = vanish_x - cx
            dy_e = vanish_y - cy
            dist = math.hypot(dx_e, dy_e)
            if dist > 1:
                enemy["x"] += dx_e / dist * 2
                enemy["y"] += dy_e / dist * 2
                spin_speed = 6 + (1 - dist / enemy["start_dist"]) * 24
                enemy["angle"] += spin_speed# 回転量(度数)
            else:
                # 消失点到達で画面外へ戻す
                enemy["frozen"] = True
                enemy["freeze_frame"] = 0
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
            
def draw_rotated_square(cx, cy, size, angle_deg, col):
    half = size / 2
    rad = math.radians(angle_deg)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    
    corners = [(-half, -half), (half, -half), (half, half), (-half, half)]
    pts = []
    for lx, ly in corners:
        rx = lx * cos_a - ly * sin_a
        ry = lx * sin_a + ly * cos_a
        pts.append((cx + rx, cy + ry))
    
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
    pyxel.tri(int(x0), int(y0), int(x1), int(y1), int(x2), int(y2), col)
    pyxel.tri(int(x0), int(y0), int(x2), int(y2), int(x3), int(y3), col)
        
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
        cx = enemy["x"] + enemy["size"] / 2
        cy = enemy["y"] + enemy["size"] / 2
        
        if enemy["absorbing"] and enemy["start_dist"] > 0:
            dist = math.hypot(vanish_x - cx, vanish_y - cy)
            shrink = max(0.0, min(1.0, dist / enemy["start_dist"]))
        else:
            shrink = 1.0
        visual_size = enemy["size"] * shrink
        draw_rotated_square(cx, cy, visual_size, enemy["angle"], 15) # 体
        if visual_size > 4:
            eye_offset = visual_size * 0.18
            pyxel.pset(int(cx - eye_offset), int(cy - eye_offset * 0.3), 0) # 左目
            pyxel.pset(int(cx + eye_offset), int(cy - eye_offset * 0.3), 0) # 右目
     
     # タイトルロゴ
     pyxel.text(15, 25, "BLACK HOLE ", 10)

pyxel.init(WIDTH, HEIGHT, title="BLACK HOLE")
pyxel.load("hole.pyxres")
pyxel.playm(0, loop=True)
pyxel.run(update, draw)
    
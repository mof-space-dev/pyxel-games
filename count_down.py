import pyxel
import random 


width = 160
height = 120

car_y = 110
running = False
goal_y = 15 # この位置まで行ったら止まる

show_start = False # 一瞬の表示用
started = False # もうスタートしたか？
goal_sound_played = False # ゴールBGMフラグ

# A Happy NEW YEAR
show_message = False

# 紙吹雪
confetti = []
confetti_active = False

pyxel.init(width, height, title="COUNT DOWN RUN")

# 音を読み込む
pyxel.load("car_sound.pyxres")

def spawn_confetti():
    global confetti, confetti_active
    confetti = []
    
    for _ in range(80):
        confetti.append({
            "x": random.randint(0, width),
            "y": random.randint(-height, 0),
            "vx": random.uniform(-0.8, -0.3),
            "vy": random.uniform(0.5, 1.5),
            "col": random.choice([8, 9, 10, 11, 12, 14, 15])
        })
        
    confetti_active = True

def update():
    global car_y, running, started, show_start, goal_sound_played, confetti_active, show_message
    # START! 表示後に走る
    
    if pyxel.frame_count >= 60 and pyxel.frame_count < 80:
         show_start = True
    elif  pyxel.frame_count == 80 and not started:
        running = True
        started = True
        show_start = False
        
        # BGM
        pyxel.playm(0, loop=True)
    
    if running:
      if car_y > goal_y:
          if pyxel.frame_count % 2 == 0:
              car_y -= 1
      else:
          running = False
          pyxel.stop()
          
          # ゴールBGM 再生
          if not goal_sound_played:
              pyxel.playm(1)
              goal_sound_played = True
              # 紙吹雪
              spawn_confetti()
              
              show_message = True
              
    if confetti_active:
       for p in confetti:
           p["x"] += p["vx"]
           p["y"] += p["vy"]
        
       confetti[:] = [
            p for p in confetti
            if p["y"] < height and p["x"] > -5
        ]
       
       if not confetti:
           confetti_active = False
      
  
def car(x, y, col):
    pyxel.pset(x + 3, y - 1, col)
    pyxel.pset(x + 4, y - 1, col)
    pyxel.rect(x, y, 8, 8, col)


  
def draw():
    pyxel.cls(0)
    
    pyxel.line(40, 0, 40, height, 11)
    pyxel.line(120, 0, 120, height, 11)
    
    pyxel.text(123, 20, "COUNTDOWN", 7)
    pyxel.text(135, 28, "RUN", 7)
    pyxel.text(125, 100, "(c) MOF", 7)
    
    # 時間制御
    if pyxel.frame_count < 60:
        if (pyxel.frame_count // 10) % 2 == 0:
            pyxel.text(width / 2 - 30, height / 2, "COUNT DOWN RUN", 7)
    else:
      if show_start:
        pyxel.text(width / 2 - 15, height / 2, "START!", 7)
    
    # ゴールフラッグ
    pyxel.tri(width / 2, 5, width / 2 + 4, 7, width / 2 - 2, 10, 8)
    pyxel.line(width / 2 - 1, 5, width / 2 - 3, 15, 7)
    
    car(width / 2 - 5, car_y, 12)
    
    if confetti_active:
        for p in confetti:
            pyxel.rect(p["x"], p["y"], 2, 2, p["col"])
            
    if show_message:
        pyxel.text(width / 2 - 40, height / 2 - 4, "A HAPPY NEW YEAR 2026", 8)
    
pyxel.run(update, draw)
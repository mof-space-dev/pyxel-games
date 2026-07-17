import pyxel

pyxel.init(128,128, title="Pong")
pyxel.load("pong.pyxres")

# パドルデザイン
PADDLE_WIDTH = 4
PADDLE_HEIGHT = 20
PADDLE_MARGIN = 10 # 画面端からの距離

PADDLE_SPEED = 2  # パドルの移動速度の上限

# パドル位置
left_paddle_x = PADDLE_MARGIN
left_paddle_y = 64 - PADDLE_HEIGHT // 2

right_paddle_x = 128 - PADDLE_MARGIN - PADDLE_WIDTH
right_paddle_y = 64 - PADDLE_HEIGHT // 2

# ボール
ball_x = 64
ball_y = 64

ball_dx = -2
ball_dy = 1

# 打ち返した回数
rally_count = 0
# シーン管理
scene = "TITLE"
scene_timer = 0

# スコア
left_paddle_score = 0
right_paddle_score = 0
# winner
winner = ""

def update():
  global scene, scene_timer,ball_x, ball_y, ball_dx, ball_dy, rally_count, left_paddle_x, right_paddle_x, left_paddle_y, right_paddle_y, left_paddle_score, right_paddle_score, winner
  scene_timer += 1
  if scene == "TITLE":
    if scene_timer > 120: #(60fps * 2 2秒後)
      scene = "RALLY"
      scene_timer = 0
      pyxel.play(0, 0)
  elif scene == "RALLY":
    ball_x += ball_dx
    ball_y += ball_dy
    # 左パドルの自動化(ボールが左に向かってるときだけ)
    if ball_dx < 0:
      left_center = left_paddle_y + PADDLE_HEIGHT // 2
      if left_center < ball_y:
        left_paddle_y += PADDLE_SPEED
      elif left_center > ball_y:
        left_paddle_y -= PADDLE_SPEED
    # 右パドルの自動化(ボールが右に向かってる時だけ)
    if ball_dx > 0:
      right_center = right_paddle_y + PADDLE_HEIGHT // 2
      if right_center < ball_y:
        right_paddle_y += PADDLE_SPEED
      elif right_center > ball_y:
        right_paddle_y -= PADDLE_SPEED
    
    
    # 左パドルとの衝突判定
    if (ball_x - 1 < left_paddle_x + PADDLE_WIDTH and
        ball_x + 1 > left_paddle_x and
        ball_y - 1 < left_paddle_y + PADDLE_HEIGHT and
        ball_y + 1 > left_paddle_y):
        ball_dx = -ball_dx
        # 角度調整(左パドル)
        center_y = left_paddle_y + PADDLE_HEIGHT // 2 # パドルの中心
        offset = ball_y - center_y # ズレ
        ball_dy = offset // 3
        if ball_dy == 0:
          ball_dy = 1
        
        left_paddle_score += 10
        rally_count += 1
        pyxel.play(0, 1)
        
    # 右パドルとの衝突判定
    if (ball_x - 1 < right_paddle_x + PADDLE_WIDTH and
        ball_x + 1 > right_paddle_x and
        ball_y - 1  < right_paddle_y + PADDLE_HEIGHT and
        ball_y + 1 > right_paddle_y):
        ball_dx = -ball_dx
        # 角度調整(右パドル)
        center_y = right_paddle_y + PADDLE_HEIGHT // 2
        offset = ball_y - center_y
        ball_dy = offset // 2
        if ball_dy == 0:
          ball_dy = 1
        
        right_paddle_score += 10
        rally_count += 1
        
        if rally_count == 4:
          scene = "BREAK"
          scene_timer = 0
        else:
          pyxel.play(0, 2)
    
  elif scene == "BREAK":
    pyxel.play(0, 3)
    winner = "You Win!"
    if scene_timer > 120:
      scene = "GAMEOVER"
      scene_timer = 0
      left_paddle_score = 0
      right_paddle_score = 0
  elif scene == "GAMEOVER":
    if scene_timer > 120:
      scene = "TITLE"
      scene_timer = 0 # タイトルに戻る
      rally_count = 0
      
      ball_x = 64
      ball_y = 64
      ball_dx = -2
      ball_dy = 1
      
      left_paddle_x = PADDLE_MARGIN
      left_paddle_y = 64 - PADDLE_HEIGHT // 2

      right_paddle_x = 128 - PADDLE_MARGIN - PADDLE_WIDTH
      right_paddle_y = 64 - PADDLE_HEIGHT // 2

def draw():
  pyxel.cls(0)
  
  # BREAK時のパドル色の指定
  if scene == "BREAK":
    pyxel.cls(8)
    pyxel.rect(left_paddle_x, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, 0)
  else:
    pyxel.rect(left_paddle_x, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, 7)
    pyxel.rect(right_paddle_x, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, 7)
  
  # シーンごとの表示
  if scene == "TITLE":
    title ="Pong?"
    tx = (128 - len(title) * 4) // 2
    ty = 128 // 2
    pyxel.text(tx, ty, title, 7)
  
  elif scene == "RALLY":
   pyxel.text(10, 10, str(left_paddle_score), 7)
   pyxel.text(110, 10, str(right_paddle_score), 7)
   pyxel.rect(ball_x - 1, ball_y - 1, 3, 3, 7)
  elif scene == "BREAK":
     # 左パドルはそのまま
    pyxel.rect(left_paddle_x, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, 0)
    center_y = right_paddle_y + PADDLE_HEIGHT // 2
    
    # 座標の定義
    ax, ay = right_paddle_x, right_paddle_y # 上端左
    bx, by = right_paddle_x + 16, right_paddle_y # 上端右
    cx, cy = right_paddle_x + 15, center_y # 中心右(右にずれ)
    dx, dy = right_paddle_x + 18, center_y # 中心左
    ex, ey = right_paddle_x ,right_paddle_y + PADDLE_HEIGHT # 下端左
    fx, fy = right_paddle_x + 16, right_paddle_y + PADDLE_HEIGHT # 下端右
    
    # 上半分
    pyxel.tri(ax, ay, bx, by, cx, cy, 0)
    pyxel.tri(ax, ay, cx, cy, dx, dy, 0)
    
    # 下半分
    pyxel.tri(dx, dy, cx, cy, fx, fy, 0)
    pyxel.tri(dx, dy, fx, fy, ex, ey, 0)
    
    pyxel.text(10, 10, winner, 0)
    pyxel.text((128 - 5 * 4 )// 2, 64, "BREAK", 0)
    
  
  elif scene == "GAMEOVER":
    # 左パドル
    pyxel.rect(left_paddle_x, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, 7)
    # 右パドル
    pyxel.rect(right_paddle_x, right_paddle_y,PADDLE_WIDTH, PADDLE_HEIGHT, 7)
    pyxel.rect(right_paddle_x -1, right_paddle_y + PADDLE_HEIGHT // 2 - 1, PADDLE_WIDTH + 2, 3, 0)
    pyxel.text((128 - 8 * 4 )// 2, 64, "GAMEOVER", 7)
  


pyxel.run(update, draw)
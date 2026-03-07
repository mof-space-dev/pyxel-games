import pyxel
import random
import math

pyxel.init(160, 120, title="Flowers Catch!")
pyxel.load("flowers.pyxres")

# ---- シーン定義 ----

SCENE_TITLE = 0
SCENE_START = 1
SCENE_GAME  = 2
SCENE_FINAL = 3
SCENE_END   = 4


scene = SCENE_TITLE
scene_frame = 0



# 何回目か(RoundCount)
round_count = 0

# タイトル用 花色
side_colors = [
    {"petal": random.choice([8, 11, 12]), "center": random.choice([9, 10])},
    {"petal": random.choice([8, 11, 12]), "center": random.choice([9, 10])},
]

# --- 花(ゲーム用) ---
flower_x = 80
flower_y = 0
flower_speed = 1
flower_center_col = 10



# --- キャラ(ゲーム用) ---
char_x = 80
char_y = 100

# -- プリンセス --
princess_x = 0
princess_y = 0

# -- 蜂 --
bee_x = 160
bee_y = 80
bee_speed = 1
# 衝突フラグ
bee_hit = False

# --- スコア ---
score = 0

final_stopped = False

# --- キャッチタイマー ---
catch_timer = 0

# --- アイテムタイプ ---
item_type = "flower"

# --- 表示用変数 ---
message = ""
message_color = 8

# -- フレーム --
stop_frame = 0

# -- 花(エンディング用)
flowers = []

# BGM
bgm_playing = False
# -- 音(エンディング用)
ending_sound_played = False

# end_start_frame = 0



# 初期化
def init_game():
    global flower_x, flower_y, flower_speed, flower_center_col, item_type,round_count, bee_x, bee_y
    
    flower_x = random.randint(10, 150)
    flower_y = 0
    if round_count == 0:
        item_type = "flower"
    elif round_count == 1:
        item_type = "branch"
    elif round_count == 2:
        item_type = "flower"
    elif round_count == 3:
        item_type = "bee"
        bee_x = pyxel.width
        bee_y = 100
    else:
        item_type = "branch"
        
    flower_speed = 1
    flower_center_col = random.choice([6, 8, 14])
    
# 描画
def draw_title():
    pyxel.cls(6)
    
    start_x = 100
    space = 20
    
    for i in range(3):
        x = start_x + i * space
        
        petal_col = 7
        center_col = 10
        stem_col = 3
        
        if i == 0:
            petal_col = side_colors[0]["petal"]
            center_col = side_colors[0]["center"]
        elif i == 2:
            petal_col = side_colors[1]["petal"]
            center_col = side_colors[1]["center"]
            
        pyxel.circ(x, 40, 4, petal_col)
        pyxel.circ(x, 40, 2, center_col)
        pyxel.line(x, 45, x - 2, 50, stem_col)
    
    # キャラ
    base_x = 70
    char_x = base_x + int(math.sin(scene_frame / 10) * 6)
    pyxel.blt(char_x, 100, 0, 0, 0, 16, 16, 1)
    
    pyxel.text(55, 60, "Flowers Catch", 8)
    

# ゲーム開始の表示
def draw_start():
    pyxel.cls(6)
    
    
    if (scene_frame // 15) % 2 == 0:
        colors = [8, 9, 10, 11, 12, 14]
        color = colors[(scene_frame // 10) % len(colors)]
        pyxel.text(45, 60, "Let's Flowers Catch!", color)
        
# ゲーム中
def draw_game():
    global char_x, message, message_color
    
    pyxel.cls(6)
    
    # cols = [6, 8, 14]
    # col = random.choice(cols)
    
    if item_type == "flower":
        pyxel.circ(flower_x, flower_y, 4, 7)
        pyxel.circ(flower_x, flower_y, 2, flower_center_col)
        pyxel.line(flower_x, flower_y + 5, flower_x -2, flower_y + 10, 3)
    
    if item_type == "branch":
        pyxel.line(flower_x, flower_y, flower_x - 4, flower_y + 10, 4)
        pyxel.line(flower_x - 2, flower_y + 3 , flower_x - 4, flower_y - 2, 4)
        
    if item_type == "bee":
        
         # 羽
        wing_y = bee_y - 3 + (pyxel.frame_count % 2)
        pyxel.rect(bee_x + 2, wing_y, 6, 3, 7)
        # 体
        pyxel.rect(bee_x, bee_y, 10, 5, 10)
        
        # 黒ストライプ
        pyxel.line(bee_x + 3, bee_y, bee_x + 3, bee_y + 4, 0)
        pyxel.line(bee_x + 6, bee_y, bee_x + 3, bee_y + 4, 0)
        
        # お尻
        pyxel.pset(bee_x + 9, bee_y + 2, 0)
        
        # 目
        pyxel.pset(bee_x + 1, bee_y + 1, 0)
        
       
        
    pyxel.blt(char_x, char_y, 2, 0, 0, 16, 16, 1)
    
    if catch_timer > 0:
        pyxel.text(char_x + 2, char_y - 40 +  catch_timer // 3, message, message_color)
    
def init_final():
    global flower_x, flower_y, char_x, final_stopped
    
    char_x = pyxel.width // 2 - 8 # キャラ中央
    flower_x = pyxel.width // 2 - 16 # 大きい花 中央
    flower_y = -32 # 画面上からスタート    
   
    final_stopped = False
    pyxel.play(1, 4)
    
    # pyxel.text(15, 40, "Making a dumb little flower game.", 8)
    # cols = [6, 8, 14]
    # pyxel.circ(80, 60, 4, 7)
    # pyxel.circ(80, 60, 2, random.choice(cols))
    # pyxel.line(80, 65, 80, 70, 3)
    
    # pyxel.pset(79, 67, 3)
    # pyxel.pset(78, 66, 3)
    # pyxel.pset(77, 65, 3)
    
    # pyxel.pset(81, 69, 3)
    # pyxel.pset(82, 68, 3)
    # pyxel.pset(83, 67, 3)
    
def ending():
    global char_x, char_y, princess_x, princess_y, ending_sound_played
    pyxel.cls(6)
    if not ending_sound_played:
        pyxel.play(1, 0)
        ending_sound_played = True
        
    pyxel.blt(char_x, char_y, 0, 0, 0, 16, 16, 1)
    pyxel.blt(princess_x, princess_y, 1, 0, 0, 16, 16, 0)
    
    for f in flowers:
        x = f[0]
        y = f[1]
        petal_col = f[2]
        center_col = f[3]
        
        pyxel.circ(x, y, 4, petal_col)
        pyxel.circ(x, y, 2, center_col)
        pyxel.line(x, y + 5, x - 2, y + 10, 3)
    
    if len(flowers) > 0 and flowers[0][1] > 40:
        pyxel.text(50, 40, "Happy Flowers", 8)
       

# 更新    
def update():
    global scene, scene_frame, flower_x, flower_y, char_x,char_y, score, catch_timer, round_count, message,bee_x, bee_y, message_color, bee_speed, bee_hit, final_stopped, stop_frame, princess_x, princess_y, end_message, bgm_playing, end_start_frame
    
    scene_frame += 1
    
    if scene == SCENE_TITLE:
        if scene_frame > 90:
            scene = SCENE_START
            scene_frame = 0
            pyxel.play(1, 0)
            
    elif scene == SCENE_START:
        if scene_frame > 90:
            scene = SCENE_GAME
            scene_frame = 0
            init_game()
    
    elif scene == SCENE_GAME:
        
        if not bgm_playing:
           
            pyxel.playm(0, loop=True)
            bgm_playing = True
            
        if item_type == "flower" or item_type == "branch":
            
            flower_y += flower_speed
            # 花の中心
            flower_center_x = flower_x + 4
            flower_center_y = flower_y + 4
            
            # キャラの頭の位置
            head_x = char_x + 12
            head_y = char_y + 2
            
            # 頭にだけ当たる判定 (小さめ
            if abs(flower_center_x - head_x) < 6 and abs(flower_center_y - head_y) < 4:
                if item_type == "flower":
                    message = "Catch!"
                    message_color = 8
                    score += 10
                    pyxel.play(1, 1)
                    
                elif item_type == "branch":
                    message = "OUCH!"
                    message_color = 1
                    
                    pyxel.play(1, 2)
                    
                    
                catch_timer = 30
                flower_y = 0
                round_count += 1
                print(round_count)
                init_game()
            
            # 落ちきったとき
            if flower_y > 120:
                flower_y = 0
                
                round_count += 1
                print(round_count)
                init_game()
                flower_center_col = random.choice([6, 8, 14])
                
            
            if head_x < flower_center_x:
                char_x += 1
            if head_x > flower_center_x:
                char_x -= 1
            
            char_x = max(0, min(char_x, pyxel.width - 16))
            
            if catch_timer > 0:
                catch_timer -= 1
            
        if item_type == "bee":
            if not bee_hit:
                bee_x -= bee_speed
            char_x -= 1
            if char_x < 0:
                char_x = 0
            
            # キャラの頭
            head_x = char_x + 12
            head_y = char_y + 2
            
            # 蜂の中心
            bee_center_x = bee_x + 5
            bee_center_y = bee_y + 2
            
            
            # 衝突判定
            if not bee_hit and abs(bee_center_x - head_x) < 8 and abs(bee_center_y - head_y) < 6:  
                
                message = "WOW Bee..."
                message_color = 2
                catch_timer = 90
                bee_hit = True
                bee_speed = 0
                
                pyxel.play(1, 3)
            
            # キャラの小刻み揺れ
            if bee_hit and catch_timer > 0:
                # +-2ピクセルで左右にゆれる
                char_x += (-1)**(catch_timer // 5)
            
            if bee_hit and catch_timer == 0:
                # 揺れ終わったら次へ
                round_count += 1
                bee_hit = False
                
                if round_count == 4:
                    print("FINAL")
                    pyxel.stop()
                    bgm_playing = False
                    scene = SCENE_FINAL
                    init_final()
                else:
                    init_game()
                
        if catch_timer > 0:
                catch_timer -= 1
                
                
    elif scene == SCENE_FINAL:
        head_y = char_y + 2
        
        # 花の下端が頭より上なら落ちる
        if not final_stopped:
            if flower_y + 45 < head_y:
                flower_y += 0.3
            else:
                # 頭の位置で止まる
                flower_y = head_y - 45
                score += 80
                final_stopped = True
                stop_frame = pyxel.frame_count
                
        if final_stopped:
            if pyxel.frame_count - stop_frame > 60:
                scene = SCENE_END
                end_start_frame = pyxel.frame_count
                
                # ここで一回だけ中央にする
                
                # キャラ配置
                char_x = pyxel.width // 2 - 32
                char_y = 100
                
                # プリンセス配置
                princess_x = char_x + 40
                princess_y = 100
                
                
    elif scene == SCENE_END:
        if char_x + 16 <= princess_x:
            char_x += 1
            princess_x -= 1
            # pyxel.play(0, 0)
        
        

            
            
        # たまに新しい花を追加
        if pyxel.frame_count % 15 == 0:
            x = pyxel.rndi(0, pyxel.width - 1)
            petal_col = pyxel.rndi(7, 15)
            center_col = pyxel.rndi(8, 12)
            flowers.append([x, 0, petal_col, center_col])
            
            # 全部の花を落とす   
        for f in flowers:
            f[1] += 1
            
        if pyxel.frame_count - end_start_frame > 190:
            flowers.clear()
            round_count = 0
            score = 0
            scene = SCENE_TITLE
            scene_frame = 0
                
    
        
            
                

# メイン描画振り分け
def draw():
    
    if scene == SCENE_TITLE:
        draw_title()
    elif scene == SCENE_START:
        draw_start()
    elif scene == SCENE_GAME:
        draw_game()
        pyxel.text(pyxel.width - 30, 5, f"{score:03}", 7 )
        
    elif scene == SCENE_FINAL:
        # 止まったら点滅
        if final_stopped:
            if pyxel.frame_count % 10 < 5:
                pyxel.cls(7) # 白
            else:
                pyxel.cls(6)
        else:
            pyxel.cls(6)
            
        pyxel.text(pyxel.width - 30, 5, f"{score:03}", 7 )
        pyxel.text(50, 20, "Flowers for You ", 8)
        
        # Big Flower
        pyxel.circ(flower_x + 16, flower_y + 16, 16, 7)
        pyxel.circ(flower_x + 16, flower_y + 16, 8, 2)
        pyxel.line(flower_x + 16, flower_y + 33, flower_x + 16, flower_y + 46, 3)
    
        pyxel.blt(char_x, char_y, 2, 0, 0, 16, 16, 1)
    
    elif scene == SCENE_END:
        ending()
        
    

pyxel.run(update, draw)
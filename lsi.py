import pyxel

# SCREEN LSI
pyxel.init(128, 160, title="Early 80'S LSI", fps=60)

# SOUND
pyxel.load("my_resource.pyxres")

# 初期位置
missile_y = 135
missile_active = False
score = 0

# フレームカウント用
frame_count = 0

# 自機・ボスの基本位置
ship_x = 56
ship_y = 140

boss_x = 64
boss_y = 40

# ボスのミサイル
boss_missile_x = 0
boss_missile_y = boss_y + 6
boss_missile_active = False
boss_missile_delay = 0
boss_missile_fired = False

# 攻撃カウント
count = 0  # タイトルからスタート

# タイトル表示用
TITLE_DURATION = 120  # 約2秒
CLEAR_DURATION = 120
CLEAR_HOLD = 60

# 音
title_sound_playing = False
bgm_playing = False

def draw_ship(x, y):
    pyxel.rect(x + 4, y - 6, 4, 6, 3)
    pyxel.rect(x, y - 3, 12, 2, 3)
    pyxel.pset(x + 5, y - 7, 3)
    pyxel.pset(x + 6, y - 7, 3)

def draw_boss(x, y):
    pyxel.rect(x - 12, y, 24, 4, 2)
    pyxel.rect(x - 8, y - 4, 16, 4, 2)
    pyxel.rect(x - 16, y + 2, 4, 2, 2)
    pyxel.rect(x + 12, y + 2, 4, 2, 2)
    pyxel.rect(x - 2, y - 2, 4, 4, 8)

def update():
    global missile_y, missile_active, score, frame_count, count
    global boss_missile_active, boss_missile_delay, boss_missile_fired
    global ship_x, boss_x, boss_missile_y,boss_missile_x
    global title_sound_playing, bgm_playing

    frame_count += 1

    # タイトル点滅
    if count == 0:
        if frame_count >= TITLE_DURATION:
            if title_sound_playing:
                pyxel.stop(0)
                title_sound_playing = False
            count = 1
            frame_count = TITLE_DURATION
            return
        if not title_sound_playing:
            pyxel.play(0, 0, loop=True)
            title_sound_playing = True
    
    if 1 <= count <= 3:
        if not bgm_playing:
            pyxel.play(1,2, loop=True)
            bgm_playing = True

    effective_frame = frame_count - TITLE_DURATION

    # 自機攻撃1回目
    if count == 1:
        if effective_frame < 60:
            boss_x = 84
            ship_x = 56
        elif effective_frame < 120:
            boss_x = 44
            ship_x = 52
        elif effective_frame < 160:
            boss_x = 74
            ship_x = 51
        elif effective_frame < 190:
            boss_x = 59
            ship_x = 58
        elif effective_frame < 220:
            boss_x = 64
            ship_x = 56
            if not missile_active:
                missile_active = True
                pyxel.play(0, 1)
                missile_y = ship_y - 6

        if missile_active:
            missile_y -= 1
            if boss_y <= missile_y <= boss_y + 6 and 60 <= boss_x <= 68:
                missile_active = False
                pyxel.play(0, 3)
                score += 10
                count = 2
                frame_count = TITLE_DURATION
                boss_missile_delay = 80
                boss_missile_fired = False

        if missile_y < 0:
            missile_active = False

    # ボス攻撃
    elif count == 2:
        if effective_frame < 60:
            boss_x = 64
            ship_x = 63
        elif effective_frame < 120:
            boss_x = 74
            ship_x = 49
        elif effective_frame < 160:
            boss_x = 14
            ship_x = 58
        elif effective_frame < 190:
            boss_x = 102
            ship_x = 51
        elif effective_frame < 220:
            boss_x = 64
            ship_x = 56

        if not boss_missile_fired:
            if boss_missile_delay > 0:
                boss_missile_delay -= 1
            else:
                boss_missile_active = True
                pyxel.play(0, 4)
                boss_missile_y = boss_y + 6
                boss_missile_x = boss_x
                boss_missile_fired = True

        if boss_missile_active:
            boss_missile_y += 1
            if boss_missile_y > pyxel.height:
                boss_missile_active = False
                count = 3
                frame_count = TITLE_DURATION
                missile_active = False

    
   # 自機攻撃2回目 → CLEAR点滅
    elif count == 3:
        
        if effective_frame < 60:
            boss_x = 102
            ship_x = 63
        elif effective_frame < 120:
            boss_x = 64- 3
            ship_x = 49
            
        if not missile_active:
            missile_active = True
            pyxel.play(0, 1)
            missile_y = ship_y - 6

        if missile_active:
            missile_y -= 1
            # ボスに命中
            if boss_y <= missile_y <= boss_y + 6 and 60 <= boss_x <= 68:
                missile_active = False
                # このタイミングでスコアを10加算する
                score += 10
                if bgm_playing:
                    pyxel.stop(1)
                    bgm_playing = False
                count = 4        # 点滅クリアへ
                frame_count = 0  # CLEAR点滅開始
        if missile_y < 0:
            missile_active = False


    # CLEAR点滅
    elif count == 4:
        if frame_count < CLEAR_DURATION:
            if frame_count % 10 < 5:
                pyxel.play(0, 5)
        else:
            frame_count > CLEAR_DURATION + CLEAR_HOLD
            pyxel.stop()
            # リセット
            count = 0  # タイトルに戻る
            frame_count = 0
            missile_active = False
            score = 0
            boss_missile_active = False
            boss_missile_fired = False

def draw():
    pyxel.cls(0)
    pyxel.text(100, 5, f"{score:03}", 3)
    draw_boss(boss_x, boss_y)
    draw_ship(ship_x, ship_y)

    if missile_active:
        pyxel.rect(62, missile_y, 4, 4, 3)
    if boss_missile_active:
        pyxel.rect(boss_missile_x - 2, boss_missile_y, 8, 8, 8)

    # タイトル点滅
    if count == 0:
        if frame_count % 30 < 15:
            pyxel.text(45, 80, "GAME START", 3)

    # CLEAR点滅
    if count == 4:
        if frame_count < CLEAR_DURATION:
            if frame_count % 10 < 5:
                pyxel.cls(0)
            else:
                pyxel.cls(3)
        else:
            pyxel.text(50, 80, "CLEAR!", 10)

pyxel.run(update, draw)

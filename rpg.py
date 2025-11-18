import pyxel
import math

frame = 0
is_start = False
show_text = False
char_width = 0  # セリフの表示幅

text_y = 90
text_speed = 3  # 文字の速さを速める
text_h = 18  # line1.pngの高さ (2行分)

current_line = 0
mode = "play"

# タイトル表示時間（フレーム数）
TITLE_WAIT = 120  # 少し短めにしてテンポよく

title_counter = 0
line_wait = 30  # セリフが全部流れた後の待機時間を短く
wait_counter = 0

# セリフファイルのリスト
LINES = [
    "line1.png", "line2.png","line3.png","line4.png","line5.png","line6.png",
    "line7.png","line8.png","line9.png","line10.png","line11.png","line12.png",
    "line13.png","line14.png","line15.png","line16.png"
]

pyxel.init(240, 120, title="きせきのほこら")

# サウンド
pyxel.load("my_sound.pyxres")

# タイトル
try:
    pyxel.image(0).load(0, 0, "title.png")
except Exception as e:
    print("LOAD ERROR:", e)

def show_line(line_filename):
    global char_width
    pyxel.cls(0)
    pyxel.image(1).load(0, 0, line_filename)
    char_width = 0

def god(x, y):
    for r in range(12, 16, 2):
        pyxel.circb(x, y, r, 10)
    pyxel.circ(x, y, 5, 2)
    pyxel.pset(x-2, y-1, 0)
    pyxel.pset(x+2, y-1, 0)
    pyxel.rect(x-3, y+5, 6, 15, 2)

def update():
    global frame, is_start, show_text, char_width, current_line, mode
    global title_counter, wait_counter

    frame += 1

    # タイトル画面
    if not is_start:
        title_counter += 1
        if title_counter >= TITLE_WAIT:
            is_start = True
            show_text = True
            current_line = 0
            show_line(LINES[current_line])
        return

    if mode == "play":
        full_width = pyxel.image(1).width
        if show_text and char_width < full_width:
            old_width = char_width
            char_width += text_speed
            if char_width != old_width:
                pyxel.play(0, 0)
        else:
            # 行が終わった後の短め待機
            wait_counter += 1
            if wait_counter >= line_wait:
                wait_counter = 0
                current_line += 1
                if current_line < len(LINES):
                    show_line(LINES[current_line])
                else:
                    mode = "end"

def draw():
    pyxel.cls(0)
    if not is_start:
        pyxel.blt(40, 0, 0, 0, 0, 160, 120)
    else:
        god(120, 40)
        if mode == "play" and show_text:
            draw_w = min(char_width, 240)
            pyxel.blt(0, text_y, 1, 0, 0, draw_w, text_h, 0)
        elif mode == "end":
            pyxel.cls(0)
            pyxel.text(90, 60, "THE END", 7)

pyxel.run(update, draw)


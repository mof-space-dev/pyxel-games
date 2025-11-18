import pyxel
import math

frame = 0
is_start = False
show_text = False
char_width = 0 # セリフの表示幅

text_y = 90
text_speed = 2 # 文字の速さ
text_h = 18 # line1.pngの高さ (2行分)

current_line = 0

mode = "play" # セリフのフラグ



# セリフファイルのリスト
LINES = ["line1.png", "line2.png","line3.png","line4.png","line5.png","line6.png","line7.png","line8.png","line9.png","line10.png","line11.png","line12.png","line13.png","line14.png","line15.png","line16.png"]

pyxel.init(240, 120, title="きせきのほこら")


# sound
pyxel.load("my_sound.pyxres")

# タイトル
try:
    pyxel.image(0).load(0, 0, "title.png")
    print("PNG loaded OK")
except Exception as e:
    print("LOAD ERROR:", e)

# 最初のセリフを読み込む関数
def show_line(line_filename):
    global char_width
    pyxel.cls(0)
    pyxel.image(1).load(0, 0, line_filename)
    char_width = 0


def god(x, y):
    # 光背
    for r in range(12, 16, 2):
        pyxel.circb(x, y, r, 10) # 薄い黄色の輪
        
        # 顔
        pyxel.circ(x, y, 5, 2)
        pyxel.pset(x-2, y-1, 0)
        pyxel.pset(x+2, y-1, 0)
        
        # 体
        pyxel.rect(x-3, y+5, 6, 15, 2)
    
def update():
    global is_start,frame
    global show_text, char_width, current_line, mode
    frame += 1
    
    # タイトル画面 ENTER Line開始
    if not is_start and pyxel.btnp(pyxel.KEY_RETURN):
        is_start = True
        show_text = True
        current_line = 0
        show_line(LINES[current_line])
        return
    
    # Enter次へ
    if mode == "play":
        if is_start and pyxel.btnp(pyxel.KEY_RETURN):
            # 文字がまだ全部出ていない場合は全表示
            full_width = pyxel.image(1).width
            if char_width < full_width:
                char_width = full_width
                return
            # 次のセリフ
            current_line += 1
            if current_line <  len(LINES):
                show_line(LINES[current_line])
            else:
                current_line = len(LINES) - 1 # 最後で止める
                mode = "end"
    # 文字を流す
    full_width = pyxel.image(1).width
    if show_text and char_width < full_width:
        old_width = char_width
        char_width += text_speed
        
        # 音
        if char_width != old_width:
            pyxel.play(0, 0)
  
def draw():
    pyxel.cls(0)
    # とにかく表示
    if not is_start:
       pyxel.blt(40, 0, 0, 0, 0, 160, 120)
       pyxel.text(120, 100, "NEXT ENTERKEY", 7)
    else:
        god(120, 40)
        # セリフ
        if mode == "play":
            if show_text:
                draw_w = min(char_width, 240)
                pyxel.blt(0, text_y, 1, 0, 0, draw_w, text_h, 0)
        elif mode == "end":
            pyxel.cls(0)
            pyxel.text(110, 60, "THE END", 7)
     


pyxel.run(update, draw)

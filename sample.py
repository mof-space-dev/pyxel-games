import pyxel

WIDTH = 256
HEIGHT = 256



# 車の初期位置
car_x, car_y = 110, 140
car_width, car_height = 8, 10
car_color = 6
def draw_course():
    pyxel.cls(1)  # 背景：青
    pyxel.pal(7, 10)  # 黄色い線（任意）

    # 外枠
    pyxel.rectb(8, 8, 240, 240, 10)

    # 内側のコース（ラセン風）
    pyxel.line(8, 32, 224, 32, 10)
    pyxel.line(224, 32, 224, 224, 10)
    pyxel.line(224, 224, 32, 224, 10)
    pyxel.line(32, 224, 32, 64, 10)
    pyxel.line(32, 64, 192, 64, 10)
    pyxel.line(192, 64, 192, 192, 10)
    pyxel.line(192, 192, 64, 192, 10)
    pyxel.line(64, 192, 64, 96, 10)
    pyxel.line(64, 96, 160, 96, 10)
    pyxel.line(160, 96, 160, 160, 10)
    pyxel.line(160, 160, 96, 160, 10)
    pyxel.line(96, 160, 96, 128, 10)
    pyxel.line(96, 128, 128, 128, 10)
    pyxel.line(128, 128, 128, 128, 10)  # ゴール近辺

def update(): pass

def draw():
    draw_course()
    
    # 車
    pyxel.rect(car_x, car_y, car_width, car_height, car_color)

pyxel.init(WIDTH, HEIGHT, title="ROUTE166")
pyxel.run(update, draw)

import pyxel



WIDTH, HEIGHT = 160, 120
CELL_SIZE = 16  # 1マスの大きさ
WALL_THICKNESS = 4  # 壁の太さを細く

# 0 = 通路（黒）、1 = 壁（白）
MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,0,1],
    [1,0,1,1,0,0,0,0,0,1,1,0,1],
    [1,0,1,1,1,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,1,1,0,1],
    [1,1,1,1,1,1,0,1,0,0,0,0,1],
    [1,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,1,1,1,1,1,0,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# 車の初期位置
car_x, car_y = 20, 90
car_speed = 1
auto_mode = False

def draw_maze_smooth():
    """連続する壁を一本の線で描く"""
    rows = len(MAZE)
    cols = len(MAZE[0])

    # 横方向の壁
    for row in range(rows):
        start = None
        for col in range(cols):
            if MAZE[row][col] == 1:
                if start is None:
                    start = col
            else:
                if start is not None:
                    # 連続する壁を横線で描く
                    x1 = start * CELL_SIZE + CELL_SIZE//2
                    y1 = row * CELL_SIZE + CELL_SIZE//2
                    x2 = (col-1) * CELL_SIZE + CELL_SIZE//2
                    y2 = y1
                    pyxel.line(x1, y1, x2, y2, 7)
                    start = None
        if start is not None:
            x1 = start * CELL_SIZE + CELL_SIZE//2
            y1 = row * CELL_SIZE + CELL_SIZE//2
            x2 = (cols-1) * CELL_SIZE + CELL_SIZE//2
            y2 = y1
            pyxel.line(x1, y1, x2, y2, 7)

    # 縦方向の壁
    for col in range(cols):
        start = None
        for row in range(rows):
            if MAZE[row][col] == 1:
                if start is None:
                    start = row
            else:
                if start is not None:
                    x1 = col * CELL_SIZE + CELL_SIZE//2
                    y1 = start * CELL_SIZE + CELL_SIZE//2
                    x2 = x1
                    y2 = (row-1) * CELL_SIZE + CELL_SIZE//2
                    pyxel.line(x1, y1, x2, y2, 7)
                    start = None
        if start is not None:
            x1 = col * CELL_SIZE + CELL_SIZE//2
            y1 = start * CELL_SIZE + CELL_SIZE//2
            x2 = x1
            y2 = (rows-1) * CELL_SIZE + CELL_SIZE//2
            pyxel.line(x1, y1, x2, y2, 7)


def update():
    global auto_mode, car_x, car_y
    if pyxel.btnp(pyxel.KEY_SPACE):
        auto_mode = True

    if auto_mode:
        # 仮の自動走行：右に移動
        car_y -= car_speed
        

def draw():
    pyxel.cls(5)
    draw_maze_smooth()
    pyxel.rect(car_x, car_y, 8, 10, 9)  # 車
    pyxel.tri(135, 100, 140, 105, 135, 105, 8)  # ゴール旗
    pyxel.line(135, 100, 135, 110, 12)  # 棒
    pyxel.text(20, 15, "ROUTE166", pyxel.frame_count % 16)

pyxel.init(WIDTH, HEIGHT, title="ROUTE166")
pyxel.run(update, draw)

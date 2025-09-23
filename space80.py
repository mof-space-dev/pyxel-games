import pyxel, random, math

WIDTH, HEIGHT = 160, 120

class RetroDemo:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="Retro Demo 1980", fps=30)
        self.stars = [(random.randint(0, WIDTH-1),
                       random.randint(0, HEIGHT-1),
                       random.choice([1, 2]))
                      for _ in range(50)]
        self.angle = 0
        pyxel.run(self.update, self.draw)
    
    def update(self):
        # 星の流れ
        new_stars = []
        for x, y, speed in self.stars:
            y += speed
            if y >= HEIGHT:
                y = 0
                x = random.randint(0, WIDTH-1)
            new_stars.append((x, y, speed))
        self.stars = new_stars
        
        # グリッド回転用の角度
        self.angle += 0.05
        
    def draw(self):
        pyxel.cls(0)
        
        # 星空
        for x, y, speed in self.stars:
             pyxel.pset(x, y, 7 if speed == 2 else 6)
        
        # 地面グリッド
        for i in range(1, 12):
            y = HEIGHT - i*10
            for x in range(0,WIDTH, 16):
                offset = int(math.sin(self.angle + x*0.1) * 8)
                pyxel.line(x+offset, y, x+offset, HEIGHT, 3)
            for j in range(6):
                y = HEIGHT - j*10
                pyxel.line(0, y, WIDTH, y, 1)
            
            # タイトルロゴ
            pyxel.text(40, 40, "RETRO WAVE", 8)
            pyxel.text(39, 39, "RETRO WAVE", 10)
            pyxel.text(38, 38, "RETRO WAVE", 7)
            
            # サブテキスト
            pyxel.text(55, 73, "Press Start?", pyxel.frame_count % 16)
            
RetroDemo()
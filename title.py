from PIL import Image, ImageDraw, ImageFont

# Pyxelの制限に合わせて 256×256 以下
WIDTH = 160
HEIGHT = 120

font = ImageFont.truetype("C:/Windows/Fonts/msgothic.ttc", 16)

img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(img)

text = "きせきのほこら"
bbox = draw.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]

x = (WIDTH - tw) // 2
y = (HEIGHT - th) // 2

draw.text((x, y), text, font=font, fill=(255, 255, 255))

img.save("title.png")
print("title.png saved")

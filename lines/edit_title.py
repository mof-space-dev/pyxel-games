from PIL import Image

img = Image.open("title.png")
img = img.resize((150, 60), Image.NEAREST)  # 低解像度向けに NEAREST
img.save("title.png")

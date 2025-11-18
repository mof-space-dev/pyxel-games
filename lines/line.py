from PIL import Image, ImageDraw, ImageFont

from PIL import Image, ImageDraw, ImageFont

def create_text_image(text, filename="line14.png"):
    # 小さめフォントで Pyxel に収まるサイズ
    font = ImageFont.truetype("C:/Windows/Fonts/msgothic.ttc", 8)

    # ダミーで文字サイズ取得
    dummy = Image.new("RGBA", (1,1))
    draw = ImageDraw.Draw(dummy)
    bbox = draw.textbbox((0,0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # 余白込みで PNG 作成
    img_w = text_w + 10
    img_h = text_h + 10
    img = Image.new("RGBA", (img_w, img_h), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.text((5,5), text, font=font, fill=(255,255,255,255))

    img.save(filename)
    print(f"Saved {filename} ({img_w}x{img_h})")

# 例のセリフ
text = "かみさま: そうぷにいけ                              "
create_text_image(text)
print("完了しました。")

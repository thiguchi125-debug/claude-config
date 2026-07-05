#!/usr/bin/env python3
"""白背景ポートレートを切り抜いて透過PNGにする（photo-post エンドカード用）。
四隅・辺から contiguous な白領域だけを floodfill で透過化するため、
スーツ内側の白いシャツ襟は残る（背景と非連結のため塗りつぶされない）。

usage: cutout_portrait.py IN.jpg OUT.png [--thresh 40] [--pad 0]
"""
import sys
from PIL import Image, ImageDraw, ImageFilter

def main():
    inp, outp = sys.argv[1], sys.argv[2]
    thresh = 40
    if "--thresh" in sys.argv:
        thresh = int(sys.argv[sys.argv.index("--thresh") + 1])

    im = Image.open(inp).convert("RGB")
    w, h = im.size
    SENT = (255, 0, 255)  # マゼンタ番兵

    # 背景に触れていそうな種点（四隅＋各辺の中点）から floodfill
    seeds = [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3),
             (w // 2, 2), (2, h // 2), (w - 3, h // 2)]
    for sx, sy in seeds:
        px = im.getpixel((sx, sy))
        # 種点が十分白いときだけ流す（人物が端に触れている辺は流さない）
        if min(px) > 220:
            ImageDraw.floodfill(im, (sx, sy), SENT, thresh=thresh)

    # マゼンタ→alpha0 のマスク生成
    px = im.load()
    mask = Image.new("L", (w, h), 255)
    mpx = mask.load()
    # 保護帯: 下中央（顔下〜スーツ・シャツ・拳）は背景でないので絶対に抜かない。
    # 背景は上部・上部両サイドにしか無いため、この帯を守れば内部の細い明色経路
    # 越しにシャツが誤って抜かれる事故を防げる。
    px0 = int(w * 0.22); px1 = int(w * 0.78)
    py0 = int(h * 0.42)
    for y in range(h):
        for x in range(w):
            if px[x, y] == SENT:
                if px0 <= x <= px1 and y >= py0:
                    continue  # 保護帯は不透明のまま
                mpx[x, y] = 0

    # 1px収縮（白ハロー除去）＋わずかにぼかしてエッジを馴染ませる
    mask = mask.filter(ImageFilter.MinFilter(3))
    mask = mask.filter(ImageFilter.GaussianBlur(0.8))

    src = Image.open(inp).convert("RGB")  # 番兵で汚す前の原画
    out = src.convert("RGBA")
    out.putalpha(mask)

    # 実被写体のバウンディングボックスへトリミング（余白削減）
    bbox = mask.getbbox()
    if bbox:
        pad = 6
        l, t, r, b = bbox
        l = max(0, l - pad); t = max(0, t - pad)
        r = min(w, r + pad); b = min(h, b + pad)
        out = out.crop((l, t, r, b))

    out.save(outp)
    print(f"cutout: {outp} {out.size}")

if __name__ == "__main__":
    main()

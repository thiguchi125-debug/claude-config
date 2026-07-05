#!/usr/bin/env python3
"""白背景ポートレートを GrabCut で切り抜いて透過PNGにする（photo-post エンドカード用）。
閾値方式だと白シャツと白背景が分離できないため、OpenCV GrabCut の
色モデル＋空間的まとまりで前景（人物）を推定する。四隅を確定背景、中央の
胴〜顔を確定前景として種付けし、収束後にエッジを軽く羽化する。

usage: cutout_portrait.py IN.jpg OUT.png [--iter 8]
"""
import sys
import numpy as np
import cv2
from PIL import Image, ImageFilter

def main():
    inp, outp = sys.argv[1], sys.argv[2]
    iters = 8
    if "--iter" in sys.argv:
        iters = int(sys.argv[sys.argv.index("--iter") + 1])

    bgr = cv2.imread(inp)
    h, w = bgr.shape[:2]

    cx = int(w * 0.47)
    mask = np.full((h, w), cv2.GC_BGD, np.uint8)  # 既定=確定背景

    # たぶん前景: 頭〜肩〜胴を覆う広い内側矩形（白背景はGrabCutが色で除外）
    mask[int(h * 0.12):h, int(w * 0.04):int(w * 0.96)] = cv2.GC_PR_FGD

    # 確定前景: 顔核＋胴中央（シャツ・ネクタイ・拳）＋下部の肩幅いっぱい帯
    cv2.ellipse(mask, (cx, int(h * 0.32)),
                (int(w * 0.18), int(h * 0.20)), 0, 0, 360, cv2.GC_FGD, -1)
    cv2.rectangle(mask, (int(w * 0.34), int(h * 0.58)),
                  (int(w * 0.62), h - 1), cv2.GC_FGD, -1)
    cv2.rectangle(mask, (int(w * 0.12), int(h * 0.82)),
                  (int(w * 0.88), h - 1), cv2.GC_FGD, -1)  # 肩・スーツ裾

    # 確定背景: 頭上の白背景（上部10%）＋外周6px
    b = 6
    mask[:int(h * 0.10), :] = cv2.GC_BGD
    mask[:b, :] = cv2.GC_BGD
    mask[-b:, :] = cv2.GC_BGD
    mask[:, :b] = cv2.GC_BGD
    mask[:, -b:] = cv2.GC_BGD

    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    cv2.grabCut(bgr, mask, None, bgdModel, fgdModel, iters, cv2.GC_INIT_WITH_MASK)

    fg = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)

    # 穴埋め（シャツ内側の取りこぼしを塞ぐ）
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE,
                          cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))

    # 最大連結成分だけ残す（孤立ノイズ除去）
    n, labels, stats, _ = cv2.connectedComponentsWithStats(fg, 8)
    if n > 1:
        biggest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        fg = np.where(labels == biggest, 255, 0).astype(np.uint8)

    # 最終工程: 残った白背景を除去（穴埋め後に実施して再付着を防ぐ）。
    # 残す白は「シャツV＝下部中央」の keep ゾーンだけ。襟の開きの奥に覗く背景
    # （首横・肩口の白）は中央にあってもここで落ちる。
    white = bgr.min(axis=2) > 200
    keep = np.zeros((h, w), bool)
    keep[int(0.71 * h):h, int(0.30 * w):int(0.66 * w)] = True
    fg[white & ~keep] = 0

    alpha = Image.fromarray(fg, "L").filter(ImageFilter.GaussianBlur(1.2))

    src = Image.open(inp).convert("RGB")
    out = src.convert("RGBA")
    out.putalpha(alpha)

    bbox = alpha.getbbox()
    if bbox:
        pad = 8
        l, t, r, bo = bbox
        l = max(0, l - pad); t = max(0, t - pad)
        r = min(w, r + pad); bo = min(h, bo + pad)
        out = out.crop((l, t, r, bo))

    out.save(outp)
    print(f"cutout(grabcut): {outp} {out.size}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""ブログサムネ16:9（西野公園プール型・3分割）を1コマンドで作る。
使い方:
  make_thumb.py --place 西野公園プール --line1 小学生は全員 --key 付き添い --ask 線引きの見直しを \
                --site 現場写真.jpg --out ~/outputs/thumbnails/<日付>_<テーマ>/
任意: --site-pos "50% 20%"（現場写真の見せる位置）／--me-x 910（本人写真の左端x）
出力: <out>/thumb_1600x900.html と .png（写真は同フォルダ assets/ にコピー）
文字数から級数を自動で決める（採寸値が上限：1行目84px・核心語126px・要望56px）。"""
import argparse, pathlib, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
COL = 490  # 中央帯で文字が使える幅（x432〜922。右写真の左辺945の手前）

def px(text, cap, width=COL):
    return min(cap, int(width / max(len(text), 1)))

def main():
    a = argparse.ArgumentParser()
    a.add_argument("--place", required=True); a.add_argument("--line1", required=True)
    a.add_argument("--key", required=True); a.add_argument("--ask", required=True)
    a.add_argument("--site", required=True, help="左に置くテーマの現場写真（草川の実写）")
    a.add_argument("--me", default=str(HERE / "assets/me_hero_yukei_full.jpg"))
    a.add_argument("--site-pos", default="50% 30%"); a.add_argument("--site-size", default="cover")
    a.add_argument("--me-w", type=int, default=510); a.add_argument("--me-x", type=int, default=940)
    a.add_argument("--me-y", type=int, default=-8)
    a.add_argument("--out", required=True)
    o = a.parse_args()

    if len(o.key) > 6:
        sys.exit(f"核心語「{o.key}」は{len(o.key)}字。6字以内に削る（黄の1語が主役）")
    out = pathlib.Path(o.out).expanduser(); (out / "assets").mkdir(parents=True, exist_ok=True)
    site = out / "assets" / ("site" + pathlib.Path(o.site).suffix.lower())
    me = out / "assets" / pathlib.Path(o.me).name
    shutil.copy(pathlib.Path(o.site).expanduser(), site); shutil.copy(pathlib.Path(o.me).expanduser(), me)

    rep = {"{{PLACE}}": o.place, "{{LINE1}}": o.line1, "{{KEY}}": o.key, "{{ASK}}": o.ask,
           "{{SITE_PHOTO}}": f"assets/{site.name}", "{{ME_PHOTO}}": f"assets/{me.name}",
           "{{SITE_POS}}": o.site_pos, "{{SITE_SIZE}}": o.site_size,
           "{{ME_X}}": str(o.me_x), "{{ME_Y}}": str(o.me_y), "{{ME_W}}": str(o.me_w),
           "{{L1_PX}}": str(px(o.line1, 84)), "{{KEY_PX}}": str(px(o.key, 126, 504)),
           "{{ASK_PX}}": str(px(o.ask, 56, COL - 44))}
    html = (HERE / "template.html").read_text()
    for k, v in rep.items():
        html = html.replace(k, v)
    h = out / "thumb_1600x900.html"; h.write_text(html)
    png = out / "thumb_1600x900.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1600,900",
                    f"--screenshot={png}", f"file://{h}"], check=True, capture_output=True)
    print(png)

if __name__ == "__main__":
    main()

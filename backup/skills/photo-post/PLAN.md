# photo-post スキル実装計画

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 写真＋ひとことから投稿文・SNS投稿画像（1:1＋9:16）・ショート動画を統合1パスで自動生成する photo-post スキルを実装する。

**Architecture:** SKILL.md（オーケストレーション指示書）＋HTML/CSSカードテンプレート5本（Chrome headlessでPNG化）＋ffmpeg動画生成シェルスクリプト1本。既存の design-studio / short-video-image-designer パターン（EYES-FIRST・ブランドトークン）を踏襲。spark へ連携フック1箇所追記。

**Tech Stack:** bash / ffmpeg（/usr/local/bin/ffmpeg）/ Chrome headless（/Applications/Google Chrome.app/Contents/MacOS/Google Chrome）/ Python3+Pillow 11.3（テスト素材生成・EXIF処理）/ sips（HEIC変換）

## Global Constraints

- 設計正本: `~/.claude/skills/photo-post/DESIGN.md`（草川承認済 2026-07-05）
- ブランドカラー: ライム `#c7ff4a`／濃緑 `#1f5a3a`／最濃緑 `#0f3d27`／生成り `#f3efe4`
- フォント: `"Hiragino Sans","Hiragino Kaku Gothic ProN",sans-serif`
- lime下線は `box-shadow: inset 0 -0.28em 0 #c7ff4a;` 方式（linear-gradientハードストップ禁止）
- 全HTMLに `-webkit-print-color-adjust:exact; print-color-adjust:exact;`
- 絵文字禁止（HTML/出力物とも）・日本語はソース内に直接書く（unicode escape禁止・「亀山」typo厳禁）
- description は400字以内（feedback_agent_description_diet_2026-07-05）
- 配置は `~/.claude/skills/photo-post/` のみ（plugins cache禁止）
- ホームはgitリポジトリではない → コミット工程なし。最終タスクで claude-config バックアップ同期
- 出力サイズ: 画像 1:1=1080×1080 / 9:16=1080×1920、動画 9:16 1080×1920 30fps 10〜20秒

---

### Task 1: 動画生成スクリプト `scripts/make_video.sh`

**Files:**
- Create: `~/.claude/skills/photo-post/scripts/make_video.sh`
- Test: 一時ディレクトリ `/private/tmp/claude-501/-Users-kusakawatakuya/*/scratchpad/pp_test/`（セッションのscratchpad配下。以下 `$SCRATCH/pp_test` と表記）

**Interfaces:**
- Produces: `make_video.sh -o OUT.mp4 -e ENDCARD.png [-t OVERLAY.png] PHOTO1 [PHOTO2 PHOTO3]`
  - PHOTO: JPEG/PNG（任意サイズ・スクリプト内で1080×1920カバークロップ）
  - OVERLAY: 1080×1920 透過PNG（先頭セグメントにフェードイン合成）
  - ENDCARD: 1080×1920 PNG（末尾3.5秒・フェードイン）
  - 写真1枚=9秒/枚、2枚=7秒/枚、3枚以上=5秒/枚 ＋ エンドカード3.5秒

- [ ] **Step 1: テスト素材を生成する（失敗確認用の前提物）**

```bash
SCRATCH="/private/tmp/claude-501/-Users-kusakawatakuya"/*/scratchpad; SCRATCH=$(echo $SCRATCH)
mkdir -p "$SCRATCH/pp_test"
python3 - "$SCRATCH/pp_test" <<'EOF'
import sys, os
from PIL import Image, ImageDraw
d = sys.argv[1]
# テスト写真（横長 2000x1500 グラデ＋目印円）
img = Image.new("RGB", (2000, 1500))
px = img.load()
for y in range(1500):
    for x in range(0, 2000, 4):
        c = (int(40+x/2000*120), int(90+y/1500*100), 60)
        for k in range(4):
            if x+k < 2000: px[x+k, y] = c
dr = ImageDraw.Draw(img)
dr.ellipse([850, 550, 1150, 850], fill=(199, 255, 74))
img.save(os.path.join(d, "photo.jpg"), quality=90)
# 透過オーバーレイ（上1/3に白帯）
ov = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
dr = ImageDraw.Draw(ov)
dr.rectangle([60, 300, 1020, 560], fill=(255, 255, 255, 230))
ov.save(os.path.join(d, "overlay.png"))
# エンドカード（濃緑ベタ＋ライム帯）
ec = Image.new("RGB", (1080, 1920), (15, 61, 39))
dr = ImageDraw.Draw(ec)
dr.rectangle([0, 900, 1080, 1020], fill=(199, 255, 74))
ec.save(os.path.join(d, "endcard.png"))
print("ok")
EOF
```

Expected: `ok`、`$SCRATCH/pp_test/` に photo.jpg / overlay.png / endcard.png

- [ ] **Step 2: スクリプト未実装での失敗を確認**

Run: `bash ~/.claude/skills/photo-post/scripts/make_video.sh -o "$SCRATCH/pp_test/out.mp4" -e "$SCRATCH/pp_test/endcard.png" -t "$SCRATCH/pp_test/overlay.png" "$SCRATCH/pp_test/photo.jpg"`
Expected: FAIL（No such file or directory）

- [ ] **Step 3: スクリプトを実装する**

```bash
mkdir -p ~/.claude/skills/photo-post/scripts
```

`~/.claude/skills/photo-post/scripts/make_video.sh` の内容（Writeで作成後 `chmod +x`）:

```bash
#!/bin/bash
# photo-post 動画生成: 写真1〜3枚 → 9:16 Ken Burns + 見出しオーバーレイ + エンドカード mp4
# usage: make_video.sh -o OUT.mp4 -e ENDCARD.png [-t OVERLAY.png] PHOTO1 [PHOTO2 PHOTO3]
set -euo pipefail

FFMPEG=/usr/local/bin/ffmpeg
OUT="" ; ENDCARD="" ; OVERLAY=""
while getopts "o:e:t:" opt; do
  case $opt in
    o) OUT=$OPTARG ;;
    e) ENDCARD=$OPTARG ;;
    t) OVERLAY=$OPTARG ;;
    *) exit 1 ;;
  esac
done
shift $((OPTIND-1))
PHOTOS=("$@")
if [[ -z $OUT || -z $ENDCARD || ${#PHOTOS[@]} -lt 1 || ${#PHOTOS[@]} -gt 3 ]]; then
  echo "usage: make_video.sh -o out.mp4 -e endcard.png [-t overlay.png] photo1 [photo2 photo3]" >&2
  exit 1
fi

N=${#PHOTOS[@]}
case $N in 1) DUR=9 ;; 2) DUR=7 ;; *) DUR=5 ;; esac
FPS=30
FRAMES=$((DUR * FPS))
FADE_OUT_ST=$(echo "$DUR - 0.5" | bc)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# 各写真セグメント: 2160x3840へカバークロップ→zoompanでスローズーム→1080x1920
BASE="scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='min(zoom+0.0006,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=${FRAMES}:s=1080x1920:fps=${FPS}"

i=0
for P in "${PHOTOS[@]}"; do
  if [[ $i -eq 0 && -n $OVERLAY ]]; then
    "$FFMPEG" -y -loglevel error -i "$P" -loop 1 -t "$DUR" -i "$OVERLAY" \
      -filter_complex "[0:v]${BASE}[bg];[1:v]format=rgba,fade=t=in:st=0.8:d=0.6:alpha=1[ov];[bg][ov]overlay=0:0:shortest=1,fade=t=out:st=${FADE_OUT_ST}:d=0.5,format=yuv420p" \
      -c:v libx264 -preset medium -crf 20 -r "$FPS" "$TMP/seg${i}.mp4"
  else
    "$FFMPEG" -y -loglevel error -i "$P" \
      -filter_complex "[0:v]${BASE},fade=t=in:st=0:d=0.4,fade=t=out:st=${FADE_OUT_ST}:d=0.5,format=yuv420p" \
      -c:v libx264 -preset medium -crf 20 -r "$FPS" "$TMP/seg${i}.mp4"
  fi
  i=$((i + 1))
done

# エンドカード 3.5秒
"$FFMPEG" -y -loglevel error -loop 1 -t 3.5 -i "$ENDCARD" \
  -filter_complex "[0:v]scale=1080:1920,fade=t=in:st=0:d=0.5,format=yuv420p" \
  -c:v libx264 -preset medium -crf 20 -r "$FPS" "$TMP/zzz_end.mp4"

# 連結（同一エンコードなので -c copy）
: > "$TMP/list.txt"
for f in "$TMP"/seg*.mp4 "$TMP"/zzz_end.mp4; do
  echo "file '$f'" >> "$TMP/list.txt"
done
"$FFMPEG" -y -loglevel error -f concat -safe 0 -i "$TMP/list.txt" -c copy "$OUT"

/usr/bin/python3 -c "import subprocess,sys; r=subprocess.run(['/usr/local/bin/ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',sys.argv[1]],capture_output=True,text=True); print(f'done: {sys.argv[1]} ({float(r.stdout):.1f}s)')" "$OUT"
```

作成後: `chmod +x ~/.claude/skills/photo-post/scripts/make_video.sh`

- [ ] **Step 4: 実行して検証**

Run（写真1枚）:
```bash
bash ~/.claude/skills/photo-post/scripts/make_video.sh -o "$SCRATCH/pp_test/out1.mp4" -e "$SCRATCH/pp_test/endcard.png" -t "$SCRATCH/pp_test/overlay.png" "$SCRATCH/pp_test/photo.jpg"
/usr/local/bin/ffprobe -v error -show_entries stream=width,height -show_entries format=duration -of default=nw=1 "$SCRATCH/pp_test/out1.mp4"
```
Expected: `done: ...out1.mp4 (12.5s)` 前後、width=1080 / height=1920、duration≈12.5

Run（写真3枚・同じ写真を3回渡す）:
```bash
bash ~/.claude/skills/photo-post/scripts/make_video.sh -o "$SCRATCH/pp_test/out3.mp4" -e "$SCRATCH/pp_test/endcard.png" "$SCRATCH/pp_test/photo.jpg" "$SCRATCH/pp_test/photo.jpg" "$SCRATCH/pp_test/photo.jpg"
```
Expected: duration≈18.5s（5×3＋3.5）。`open "$SCRATCH/pp_test/out1.mp4"` で目視確認（ズーム動作・オーバーレイのフェードイン・エンドカード）

---

### Task 2: カードテンプレート5本（HTML/CSS）

**Files:**
- Create: `~/.claude/skills/photo-post/templates/card_band.html`（下帯型）
- Create: `~/.claude/skills/photo-post/templates/card_side.html`（サイドバー型）
- Create: `~/.claude/skills/photo-post/templates/card_full.html`（フルブリード座布団型）
- Create: `~/.claude/skills/photo-post/templates/video_overlay.html`（動画用・透過見出し）
- Create: `~/.claude/skills/photo-post/templates/video_endcard.html`（動画用エンドカード）

**Interfaces:**
- Produces: プレースホルダー `{{PHOTO}}`（file://絶対パス）`{{H1A}}` `{{H1B}}`（見出し1行目/2行目・各15字前後）`{{SUB}}`（サブ1行）`{{TAG}}`（#亀山市 等）`{{FOCUS}}`（object-position値・既定 `center 35%`）
- 同一ファイルが `--window-size=1080,1080`（1:1）と `--window-size=1080,1920`（9:16）の両方で崩れない（帯は bottom 固定・px指定・photoはinset:0のcover）

- [ ] **Step 1: card_band.html を作成**

```html
<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">
<style>
:root{--lime:#c7ff4a;--green:#1f5a3a;--deep:#0f3d27;--kinari:#f3efe4;}
*{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
body{width:100vw;height:100vh;overflow:hidden;position:relative;background:#000;
 font-family:"Hiragino Sans","Hiragino Kaku Gothic ProN",sans-serif;}
.photo{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{{FOCUS}};}
.band{position:absolute;left:0;right:0;bottom:0;padding:130px 56px 46px;
 background:linear-gradient(180deg,rgba(15,61,39,0) 0%,rgba(15,61,39,.55) 32%,rgba(15,61,39,.94) 100%);}
.head{display:flex;gap:24px;align-items:stretch;}
.bar{width:14px;background:var(--lime);flex:none;}
h1{color:#fff;font-size:72px;line-height:1.26;font-weight:800;letter-spacing:.01em;}
.sub{margin-top:20px;color:var(--kinari);font-size:33px;font-weight:600;line-height:1.5;}
.meta{margin-top:30px;display:flex;align-items:baseline;gap:20px;
 border-top:2px solid rgba(243,239,228,.35);padding-top:22px;}
.name{color:#fff;font-size:31px;font-weight:700;white-space:nowrap;}
.name small{font-weight:500;font-size:24px;color:var(--kinari);margin-left:12px;}
.tag{margin-left:auto;color:var(--lime);font-size:26px;font-weight:700;letter-spacing:.04em;white-space:nowrap;}
</style></head><body>
<img class="photo" src="{{PHOTO}}">
<div class="band">
 <div class="head"><div class="bar"></div><h1>{{H1A}}<br>{{H1B}}</h1></div>
 <div class="sub">{{SUB}}</div>
 <div class="meta"><div class="name">草川たくや<small>亀山市議会議員</small></div><div class="tag">{{TAG}}</div></div>
</div>
</body></html>
```

- [ ] **Step 2: card_side.html を作成**

```html
<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">
<style>
:root{--lime:#c7ff4a;--green:#1f5a3a;--deep:#0f3d27;--kinari:#f3efe4;}
*{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
body{width:100vw;height:100vh;overflow:hidden;position:relative;background:var(--deep);
 font-family:"Hiragino Sans","Hiragino Kaku Gothic ProN",sans-serif;}
.photo{position:absolute;left:355px;top:0;right:0;bottom:0;width:calc(100vw - 355px);height:100%;
 object-fit:cover;object-position:{{FOCUS}};}
.side{position:absolute;left:0;top:0;bottom:0;width:355px;background:var(--deep);
 padding:64px 38px 48px;display:flex;flex-direction:column;}
.date{color:var(--lime);font-size:24px;font-weight:700;letter-spacing:.08em;margin-bottom:36px;}
h1{color:#fff;font-size:52px;line-height:1.4;font-weight:800;}
h1 span{box-shadow:inset 0 -0.28em 0 rgba(199,255,74,.45);}
.sub{margin-top:28px;color:var(--kinari);font-size:26px;line-height:1.6;font-weight:500;}
.foot{margin-top:auto;}
.bar{width:64px;height:10px;background:var(--lime);margin-bottom:20px;}
.name{color:#fff;font-size:28px;font-weight:700;white-space:nowrap;}
.role{color:var(--kinari);font-size:21px;margin-top:6px;}
.tag{color:var(--lime);font-size:22px;font-weight:700;margin-top:16px;}
</style></head><body>
<div class="side">
 <div class="date">{{TAG}}</div>
 <h1><span>{{H1A}}</span><br><span>{{H1B}}</span></h1>
 <div class="sub">{{SUB}}</div>
 <div class="foot"><div class="bar"></div><div class="name">草川たくや</div>
  <div class="role">亀山市議会議員</div></div>
</div>
<img class="photo" src="{{PHOTO}}">
</body></html>
```

- [ ] **Step 3: card_full.html を作成（座布団チップ型）**

```html
<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">
<style>
:root{--lime:#c7ff4a;--green:#1f5a3a;--deep:#0f3d27;--kinari:#f3efe4;}
*{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
body{width:100vw;height:100vh;overflow:hidden;position:relative;background:#000;
 font-family:"Hiragino Sans","Hiragino Kaku Gothic ProN",sans-serif;}
.photo{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{{FOCUS}};}
.copy{position:absolute;left:56px;top:96px;right:56px;}
h1{font-size:64px;line-height:1.62;font-weight:800;}
h1 span{background:rgba(15,61,39,.90);color:#fff;padding:10px 26px;
 -webkit-box-decoration-break:clone;box-decoration-break:clone;}
h1 .l2 span{background:var(--lime);color:var(--deep);}
.foot{position:absolute;left:56px;right:56px;bottom:44px;display:flex;align-items:center;gap:18px;}
.bar{width:14px;height:52px;background:var(--lime);}
.name{color:#fff;font-size:30px;font-weight:700;text-shadow:0 2px 14px rgba(0,0,0,.6);white-space:nowrap;}
.name small{font-weight:500;font-size:23px;margin-left:12px;}
.tag{margin-left:auto;color:#fff;font-size:24px;font-weight:700;text-shadow:0 2px 14px rgba(0,0,0,.6);white-space:nowrap;}
</style></head><body>
<img class="photo" src="{{PHOTO}}">
<div class="copy"><h1><span>{{H1A}}</span><br class="clear"><span class="l2wrap"></span></h1>
<h1 class="l2" style="margin-top:14px;"><span>{{H1B}}</span></h1>
<div style="margin-top:26px;"><span style="background:rgba(15,61,39,.85);color:#f3efe4;font-size:30px;font-weight:600;padding:8px 20px;">{{SUB}}</span></div></div>
<div class="foot"><div class="bar"></div><div class="name">草川たくや<small>亀山市議会議員</small></div><div class="tag">{{TAG}}</div></div>
</body></html>
```

- [ ] **Step 4: video_overlay.html（透過）と video_endcard.html を作成**

video_overlay.html:
```html
<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{width:100vw;height:100vh;overflow:hidden;position:relative;background:transparent;
 font-family:"Hiragino Sans","Hiragino Kaku Gothic ProN",sans-serif;}
.copy{position:absolute;left:56px;top:300px;right:56px;}
h1{font-size:66px;line-height:1.6;font-weight:800;}
h1 span{background:rgba(15,61,39,.92);color:#fff;padding:10px 26px;
 -webkit-box-decoration-break:clone;box-decoration-break:clone;}
h1.l2{margin-top:14px;}
h1.l2 span{background:#c7ff4a;color:#0f3d27;}
.name{position:absolute;left:56px;bottom:340px;color:#fff;font-size:30px;font-weight:700;
 text-shadow:0 2px 16px rgba(0,0,0,.75);}
.name small{font-weight:500;font-size:23px;margin-left:12px;}
</style></head><body>
<div class="copy"><h1><span>{{H1A}}</span></h1><h1 class="l2"><span>{{H1B}}</span></h1></div>
<div class="name">草川たくや<small>亀山市議会議員</small></div>
</body></html>
```

video_endcard.html:
```html
<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">
<style>
:root{--lime:#c7ff4a;--deep:#0f3d27;--kinari:#f3efe4;}
*{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
body{width:100vw;height:100vh;overflow:hidden;background:var(--deep);display:flex;
 align-items:center;justify-content:center;
 font-family:"Hiragino Sans","Hiragino Kaku Gothic ProN",sans-serif;}
.box{text-align:center;}
.bar{width:120px;height:12px;background:var(--lime);margin:0 auto 48px;}
.slogan{color:#fff;font-size:84px;font-weight:800;letter-spacing:.04em;white-space:nowrap;}
.name{color:var(--lime);font-size:44px;font-weight:800;margin-top:56px;}
.role{color:var(--kinari);font-size:28px;font-weight:500;margin-top:14px;}
.tag{color:var(--kinari);font-size:24px;margin-top:44px;opacity:.85;}
</style></head><body>
<div class="box"><div class="bar"></div>
 <div class="slogan">声を、チカラに。</div>
 <div class="name">草川たくや</div><div class="role">亀山市議会議員</div>
 <div class="tag">{{TAG}}</div></div>
</body></html>
```

- [ ] **Step 5: レンダテスト（EYES-FIRST）**

Task 1 のテスト写真でプレースホルダーを差し替えてレンダし、**PNGを必ずReadで開いて目視検品**する:

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
T=~/.claude/skills/photo-post/templates
for tpl in card_band card_side card_full; do
  sed -e "s|{{PHOTO}}|file://$SCRATCH/pp_test/photo.jpg|" \
      -e "s|{{H1A}}|通学路の危険箇所、|" -e "s|{{H1B}}|現場で確認しました|" \
      -e "s|{{SUB}}|市民の方の声を受けて現地調査|" -e "s|{{TAG}}|#亀山市|" \
      -e "s|{{FOCUS}}|center 35%|" "$T/$tpl.html" > "$SCRATCH/pp_test/$tpl.html"
  "$CHROME" --headless --disable-gpu --hide-scrollbars \
    --screenshot="$SCRATCH/pp_test/${tpl}_sq.png" --window-size=1080,1080 "file://$SCRATCH/pp_test/$tpl.html"
  "$CHROME" --headless --disable-gpu --hide-scrollbars \
    --screenshot="$SCRATCH/pp_test/${tpl}_9x16.png" --window-size=1080,1920 "file://$SCRATCH/pp_test/$tpl.html"
done
sed -e "s|{{H1A}}|通学路の危険箇所、|" -e "s|{{H1B}}|現場で確認しました|" \
    "$T/video_overlay.html" > "$SCRATCH/pp_test/vo.html"
"$CHROME" --headless --disable-gpu --hide-scrollbars --default-background-color=00000000 \
  --screenshot="$SCRATCH/pp_test/vo.png" --window-size=1080,1920 "file://$SCRATCH/pp_test/vo.html"
sed -e "s|{{TAG}}|#亀山市|" "$T/video_endcard.html" > "$SCRATCH/pp_test/ec.html"
"$CHROME" --headless --disable-gpu --hide-scrollbars \
  --screenshot="$SCRATCH/pp_test/ec.png" --window-size=1080,1920 "file://$SCRATCH/pp_test/ec.html"
```

検品基準（各PNGをRead）: 文字切れ・重なりゼロ／1:1と9:16両方で帯・サイドバーが破綻しない／vo.png の背景が透過（市松ではなく黒でもなく透明）／スローガン・名前の欠けなし。崩れがあればテンプレCSSを修正して再レンダ（最大3周）。

- [ ] **Step 6: 透過オーバーレイ＋実レンダ素材で動画を通しで生成**

```bash
bash ~/.claude/skills/photo-post/scripts/make_video.sh \
  -o "$SCRATCH/pp_test/full.mp4" -e "$SCRATCH/pp_test/ec.png" -t "$SCRATCH/pp_test/vo.png" \
  "$SCRATCH/pp_test/photo.jpg"
open "$SCRATCH/pp_test/full.mp4"
```
Expected: 12.5秒前後・見出しチップがフェードインし・末尾に「声を、チカラに。」エンドカード。目視で確認。

---

### Task 3: SKILL.md 本体

**Files:**
- Create: `~/.claude/skills/photo-post/SKILL.md`

**Interfaces:**
- Consumes: Task 1 の `scripts/make_video.sh`、Task 2 の `templates/*.html`（プレースホルダー仕様）
- Produces: スキル本体。frontmatter `name: photo-post`・description 400字以内

- [ ] **Step 1: SKILL.md を作成**

```markdown
---
name: photo-post
description: 草川たくや（亀山市議会議員）の写真1〜3枚＋ひとこと（ひらめき・活動メモ）から、投稿文→SNS投稿画像（1:1＋9:16・実写無加工のデザイン合成）→ショート動画（10〜20秒9:16）まで統合1パスで自動生成するスキル。「この写真で投稿作って」「この写真で投稿画像作って」「写真を投稿用にして」「投稿画像にして」「写真から動画も」「写真をSNS用に加工して」「photo-post」で起動。写真＋ひとことの同時投入も起動候補として提案。確認は2回のみ（①切り口・投稿文・デザイン選択②投稿前最終）。安全ゲート（content-fact-checker→content-risk-reviewer＋写真固有軸）skip禁止。※「記録」を含む→nichijo、「メモ:」「保存して」→smart-intake、セリフ型ショート動画→short-video-create、イラスト挿入画→short-video-image-designer、投稿文のみ→sparkが正。
---

# photo-post — 写真＋ひとこと → 投稿文・画像・動画の統合1パス

設計正本: 同ディレクトリ `DESIGN.md`（2026-07-05草川承認）。以下は実行手順。

## 定数

- CHROME: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- テンプレ: `~/.claude/skills/photo-post/templates/`（card_band=下帯型/card_side=サイドバー型/card_full=座布団型/video_overlay/video_endcard）
- 動画: `~/.claude/skills/photo-post/scripts/make_video.sh -o OUT.mp4 -e ENDCARD.png [-t OVERLAY.png] PHOTO...`
- 出力: `~/outputs/photo-post/<YYYY-MM-DD>_<テーマ>/`（絶対パス・cwd依存禁止）
- ブランド: ライム#c7ff4a／濃緑#1f5a3a／最濃緑#0f3d27／生成り#f3efe4・絵文字禁止・他議員氏名禁止

## Step 1: 受付

- 写真パス（1〜3枚）＋ひとことを受け取る。写真未指定で「いい写真選んで」→ photo-curator に候補3〜5枚出させて草川選択。
- HEIC は `sips -s format jpeg <src> --out <dst>.jpg` で変換。EXIF向きは `python3 -c "from PIL import Image, ImageOps; ImageOps.exif_transpose(Image.open('<src>')).save('<dst>')"` で正規化（位置情報も落ちる）。実写の生成的改変はしない（色調・トリミングのみ可）。
- 作業は出力ディレクトリを先に `mkdir -p` してそこで行う。
- モード判定: (A)写真＋ひとこと=統合1パス（既定・以下全step） (B)「画像だけ」/写真のみ=Step 2の投稿文を作らず画像コピーのみ (C)spark等から投稿文持ち込み=PAIRモード・Step 2は文生成せずコピー抽出のみ (D)「画像だけ」明示時はStep 5をスキップ。

## Step 2: 接地＋文・コピー同時生成

- アーカイブ接地（省略禁止）: `grep -rl "<話題ワード>" ~/.claude/agents/knowledge/kusagawa_archive/{01_council,02_publications,05_resources,06_election}/` ＋草川独自表現も並列。ヒット1〜2件だけ読む。
- 同じ素材から一度に生成する: (a)投稿文=種のサイズに応じてX/Threads等1〜2PF・voice-dna整合・絵文字なし・禁止フレーム回避・架空エピソード禁止 (b)画像用コピー=見出し2行（H1A/H1B・各15字前後）＋サブ1行（SUB）＋タグ（TAG・#亀山市等）。
- 文と画像コピーを別々に作らない（トーン統一＋燃費）。

## Step 3: ✋確認1回目（1画面で）

AskUserQuestion で提示: 切り口＋投稿文案＋デザイン3案（下帯型/サイドバー型/座布団型・各の向き不向き1行）＋動画要否（既定ON）。草川選択後に次へ。

## Step 4: 画像合成（EYES-FIRST）

1. 選択テンプレをコピーし {{PHOTO}}(file://絶対パス)/{{H1A}}/{{H1B}}/{{SUB}}/{{TAG}}/{{FOCUS}}(既定 center 35%・顔位置に合わせ調整) を置換。
2. レンダ: `"$CHROME" --headless --disable-gpu --hide-scrollbars --screenshot=<out>.png --window-size=1080,1080 file://<html>` と `--window-size=1080,1920` の2枚。
3. **PNGを自分でReadして検品**（委譲禁止）: 文字切れ・重なり・顔と帯の衝突・コントラスト。崩れは font-size/FOCUS を調整して再レンダ（最大3周）。可読性フロア: 最小フォント21px相当・SNS UIセーフゾーン（下240px/右150pxに重要要素を置かない・9:16のみ）。

## Step 5: 動画生成（既定で続行・追加入力不要）

1. video_overlay.html に H1A/H1B を差し込み→透過レンダ: `--default-background-color=00000000 --window-size=1080,1920`
2. video_endcard.html に TAG を差し込み→通常レンダ 1080x1920。
3. `make_video.sh -o <出力dir>/video.mp4 -e endcard.png -t overlay.png <写真...>`（1枚9秒/2枚7秒/3枚5秒＋エンドカード3.5秒・無音。BGMはスマホ後乗せ）。

## Step 6: 安全ゲート（skip禁止・まとめて1回）

content-fact-checker（投稿文・コピー内の数値/固有名詞/計画名）→ content-risk-reviewer（8軸＋写真固有軸: 第三者の顔・子どもの顔・車ナンバー・個人宅特定・位置情報・公選法文書図画）。画像・動画のPNGフレームも確認対象に含めることを指示文に明記。HIGH以上はASK_USER・CRITICAL即停止。

## Step 7: ✋確認2回目（最終）→保存

1. 完成セット（投稿文＋画像2枚＋動画）を提示→草川OK後に1回で保存（D2原則）。
2. 保存: `~/outputs/photo-post/<日付>_<テーマ>/` に全ファイル → Drive `📱動画素材/` へ画像・動画をミラー（cp） → 📣SNS投稿管理DB（ds `1bd98deb-`）に1ページ（タイトル先頭📸・投稿文全文＋画像/動画のDriveパス記載・ステータス=未着手）。
3. nichijo日次ログに🔖台帳1行（`🔖 HH:MM 〈テーマ15字〉→photo-post → <mention-page url="...">ページ名</mention-page>`）。
4. 出来が良いレイアウトが生まれたら design_system への「SNSカード」テンプレ昇格を提案（強制しない）。

## やらないこと

- 写真自体のAI生成改変（nano-banana等）。明示依頼時のみ nanobanana-prompt-designer のプロンプトカードをおまけ出力（手貼り用）し、改変画像の投稿はrisk-reviewer必須＋「AI加工」明示を条件とする。
- 7PF一括生成（sns-content-creator）・セリフ型ショート動画（short-video-create）・印刷物（design-studio）。
- BGM付与・本人ナレーション（スマホ編集の領分）。

## 📌 恒久ガードルール

（実運用フィードバックをここに追記する — feedback_rules_reside_in_agents 運用）
```

- [ ] **Step 2: description 文字数検証**

Run: `python3 -c "import re,sys; t=open('/Users/kusakawatakuya/.claude/skills/photo-post/SKILL.md').read(); d=re.search(r'description: (.+)',t).group(1); print(len(d))"`
Expected: 400以下。超過時は NOT句を削って再検証。

- [ ] **Step 3: スキル認識の確認**

新セッションを開かず確認する簡易法として、frontmatterのYAML妥当性を検証:
Run: `python3 -c "import yaml; yaml.safe_load(open('/Users/kusakawatakuya/.claude/skills/photo-post/SKILL.md').read().split('---')[1]); print('yaml ok')"`
Expected: `yaml ok`

---

### Task 4: spark 連携フック（1箇所改修＋領分1行修正）

**Files:**
- Modify: `~/.claude/skills/spark/SKILL.md`（「## ストック分岐」直前に節挿入＋「## やらないこと」1行差し替え）

**Interfaces:**
- Consumes: photo-post の PAIRモード（Step 1 モードC: 投稿文持ち込み・文生成スキップ）

- [ ] **Step 1: 連携節を挿入（Edit・old_string完全一致）**

old_string:
```
## ストック分岐（「貯めて」「ストックして」）
```
new_string:
```
## 写真つきの種（photo-post連携・2026-07-05追加）

種に写真（ファイルパス・添付）が一緒に投入されていたら、Step 5 の保存完了後に「📸 photo-post で投稿画像＋ショート動画も作る？」を選択肢として提示する。YESなら photo-post スキルを PAIRモード（生成済み投稿文を渡す）で起動する——文の再生成はさせず、コピー抽出→画像合成→動画→安全ゲート（画像・動画分のみ）に直行。

## ストック分岐（「貯めて」「ストックして」）
```

- [ ] **Step 2: 「やらないこと」の領分を更新（Edit）**

old_string:
```
- 7PF一括生成・ショート動画・印刷物（それぞれ sns-content-creator フル / short-video-create / print系 の領分）
```
new_string:
```
- 7PF一括生成・セリフ型ショート動画・印刷物（それぞれ sns-content-creator フル / short-video-create / print系 の領分）。ただし**写真つきの種の投稿画像・写真動画化は photo-post に橋渡し**する（上記連携節）
```

- [ ] **Step 3: 整合確認**

Run: `grep -n "photo-post" ~/.claude/skills/spark/SKILL.md`
Expected: 2箇所（連携節・やらないこと）ヒット。

---

### Task 5: E2E ドライラン（統合1パスの通し検証）

**Files:**
- 使用: Task 1〜3 の全成果物。出力先 `~/outputs/photo-post/2026-07-05_e2eテスト/`

- [ ] **Step 1: SKILL.md の手順どおりに通しで実行**

テスト入力: Task 1 のテスト写真＋ひとこと「通学路の危険箇所を現場確認した」を想定し、SKILL.md Step 1→2→4→5 を**書いてある通りに**なぞる（Step 3・6・7 の対人確認と安全ゲートはドライランでは「呼び出し文面を組み立てるところまで」で止める）。card_band を選択したと仮定。

Expected:
- `~/outputs/photo-post/2026-07-05_e2eテスト/` に `card_sq.png`（1080×1080）・`card_9x16.png`（1080×1920）・`video.mp4`（≈12.5s）が揃う
- PNG検品パス（文字切れなし）
- 手順の record どおりに実行して詰まった箇所（パス・コマンド・プレースホルダー名の不一致）があれば SKILL.md を修正

- [ ] **Step 2: テスト生成物の掃除**

```bash
rm -rf ~/outputs/photo-post/2026-07-05_e2eテスト "$SCRATCH/pp_test"
```
Expected: テスト痕跡ゼロ（~/outputs に本番以外を残さない）

---

### Task 6: 登録・メモリ・バックアップ

**Files:**
- Create: `~/.claude/projects/-Users-kusakawatakuya/memory/project_photo_post_skill.md`
- Modify: `~/.claude/projects/-Users-kusakawatakuya/memory/MEMORY.md`（🔄進行中プロジェクトに1行）
- Modify: Notion「スキルトリガー一覧」（`reference_skill_triggers.md` 記載のページ）

- [ ] **Step 1: メモリファイル作成**

`project_photo_post_skill.md`:
```markdown
---
name: project-photo-post-skill
description: photo-postスキル（写真＋ひとこと→投稿文・画像・動画の統合1パス）2026-07-05実装
metadata:
  type: project
---

2026-07-05実装完了。写真1〜3枚＋ひとこと→投稿文（1〜2PF）→SNS投稿画像（1:1＋9:16・実写無加工デザイン合成・テンプレ3種）→ショート動画（ffmpeg Ken Burns＋透過見出し＋エンドカード・10〜20秒9:16）を統合1パス生成。確認2回のみ。[[project_spark_skill]]と連携（写真つきの種→PAIRモード橋渡し）。設計正本=~/.claude/skills/photo-post/DESIGN.md。初回実運用フィードバック待ち。

**Why:** 実運用は「画像＋ひらめき/活動記録を一緒に投稿」が基本形のため、文と画像を同じ接地・同じコピー素材から分岐させ、安全ゲート・保存を各1回に統合（燃費60〜80K）。
**How to apply:** 写真＋ひとこと投入で提案起動。「画像だけ」で動画スキップ。優良レイアウトはdesign_system「SNSカード」昇格提案。
```

MEMORY.md の「## 🔄 進行中プロジェクト」末尾に追記:
```
- [photo-postスキル（写真＋ひとこと→投稿画像・動画）](project_photo_post_skill.md) — 2026-07-05実装。統合1パス（文→画像1:1+9:16→動画）・spark連携PAIRモード・テンプレ3種。初回実運用フィードバック待ち
```

- [ ] **Step 2: Notionスキルトリガー一覧へ1行追加**

`~/.claude/projects/-Users-kusakawatakuya/memory/reference_skill_triggers.md` を読んでページURLを取得 → notion-fetch で現状確認 → 既存行の書式に合わせて photo-post 行（トリガー: この写真で投稿作って／写真を投稿用にして／投稿画像にして／写真から動画も）を追記（update_content は一括置換を避け、追記後 fetch 検証）。

- [ ] **Step 3: claude-config バックアップ同期**

```bash
ls ~/claude-config/scripts/
```
sync系スクリプト（sync-to-git.sh 等）が存在すればそれを実行し、photo-post 一式（SKILL.md/DESIGN.md/PLAN.md/templates/scripts）と spark 改修がGitHubバックアップに乗ったことを出力で確認。スクリプトのガード（plugins cache検知）が発火したら停止して草川に報告。

---

## Self-Review 記録

- **Spec coverage:** DESIGN.md の全節をタスクへ対応付け済み — 統合1パスフロー(Task 3 Step1)・写真入力/HEIC/photo-curator(SKILL.md Step1)・テンプレ2〜3案(Task 2で3種)・動画既定同梱(Task 1＋SKILL.md Step5)・安全ゲート写真軸(SKILL.md Step6)・保存3点セット＋台帳(SKILL.md Step7)・spark連携(Task 4)・トリガー/衝突回避(description)・design_system昇格ループ(SKILL.md Step7-4)・nano-banana明示時のみ(やらないこと節)。
- **Placeholder scan:** TBD/TODO/「適宜」なし。全コード・全編集文字列を実体で記載。
- **Type consistency:** プレースホルダー名 {{PHOTO}}/{{H1A}}/{{H1B}}/{{SUB}}/{{TAG}}/{{FOCUS}} を Task 2 と Task 3(SKILL.md) で一致確認。make_video.sh の引数仕様（-o/-e/-t）も Task 1 と SKILL.md Step 5 で一致。

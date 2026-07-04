# イベントポスター テンプレート

## 用途
地域イベント（夏祭り・地区行事等）の掲示用縦長ポスター1枚もの。**全デザイン制作物の品質基準の正本**（feedback_design_quality_bar_natsumatsuri2026）——参照忠実再現・グリフ単位検品・レイヤー順・EYES-FIRST・完成処理込みの水準はこの作品が基準。

## 正本
- `template.html` = `drafts/2026-08_中庄夏祭りポスター/poster.html` のverbatimコピー
- 画像アセット（背景・タイトル画像・人物イラスト群・雲）は元ディレクトリ `~/.claude/projects/-Users-kusakawatakuya/drafts/2026-08_中庄夏祭りポスター/assets/` に相対参照。単体レンダリングする場合は assets/ ごと複製すること
- 完成見本: 同ディレクトリの `poster_preview.png`

## 紙サイズ・dpi
- ステージ実寸 874×1250px（`@page{size:874px 1250px}`）。A3/A4掲示に流用する場合はステージ寸法と`@page`を変更し全座標をスケール
- 掲示物のため文字は遠目視認優先：日付164px級・白ストローク必須

## レイヤー構成（z-index設計・この順を崩さない）
1. 背景（`.stage` background画像）
2. 帯・ガーランド・地面の波（z-index:2）
3. 人物イラスト・タイトル画像（z-index:3）
4. アーチ副題・日付・会場・時刻（z-index:4）
5. ポップ体キャッチ・料金散らし（z-index:5〜6）

## 主要技法（再利用価値の高い部分）
- 白ストローク視認性: `-webkit-text-stroke: Npx #fff; paint-order: stroke fill;`
- ポップ体1文字色替え: `<b>`分割＋odd/evenで`rotate(±2deg)`＋白/紺の2重text-shadow縁取り
- 中央揃え数字のletter-spacing補正: `text-indent`で末尾字間分を相殺
- アーチ文字: SVG `<textPath>`
- 提灯ガーランド: SVG path＋JSで`getPointAtLength`等配置

## 差し替えポイント
- タイトル（`.title`／title.png）・年号（`.y2026`）・帯文言（bandtext.png）
- 日付・曜日（`.date`）・会場（`.addr`）・時刻（`.time`）
- 料金散らし（`.price` 各ブロック：位置は千鳥配置を維持、整列グリッドにしない）
- 人物イラスト群（`.crowd img`）・配色パレット（`:root`変数）

## PDF/PNG生成
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --window-size=874,1250 --force-device-scale-factor=2 \
  --screenshot=/絶対パス/poster.png /絶対パス/poster.html
# PDF入稿時
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=/絶対パス/poster.pdf /絶対パス/poster.html
open /絶対パス/poster.pdf
```

## 注意
- 配色は案件毎に作り分ける（本作の祭りパレットは正本の一例。ブランド4色固定ではない）
- レンダリング後は必ずPNGを開いてグリフ単位検品（EYES-FIRST）
- 主催表記は正確に（例：中庄夏祭り＝若者有志。「個人主催」誤記系の事故防止）
- 掲示・配布物のため content-fact-checker → content-risk-reviewer 通過必須

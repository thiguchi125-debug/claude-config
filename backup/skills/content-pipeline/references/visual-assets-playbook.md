# 発信ビジュアル制作 プレイブック（サムネ画像・ショート動画）

content-pipeline ステップ4の実装レシピ。2026-07-14 三寺コスモス畑ブログの制作フローを正本化したもの。**サムネ・動画に載る文言は必ず安全ゲート（fact→risk）を通す**（ブログと同一表現なら継承可）。絵文字禁止・他議員名なし・公選法（寄附/おもてなしは団体主体表現）を厳守。

共通ツール: macOS の Chrome headless（`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`）でHTML/CSS→PNG、`ffmpeg`/`ffprobe`（/usr/local/bin）で動画。日本語フォントは「Hiragino Sans」（W3〜W9）。**cwd依存禁止・全部絶対パス**。**EYES-FIRST＝レンダ結果PNGを必ず自分でReadして破綻確認→修正**（サブエージェントに委譲しない）。

---

## A. サムネ画像（アイキャッチ / OGP / SNSカード）

### A-0. 元写真の確認（最初の一手・必須）
「元になる草川の写真はありますか？」と1回聞く（[[feedback_thumbnail_ask_base_photo_first]]）。
- **写真あり**: photo-curator でベスト選定（ZPERSON=18）→写真を主役に据え、文字は写真の余白／スクリム上に。人物が主役だと訴求力が高い。
- **写真なし（草川OK）**: タイポ＋モチーフ主体（下記テンプレ）。

### A-1. サイズと版
- 既定 **1200×630（OGP標準）**。ブログのアイキャッチ・Facebook/Xカード・LINEサムネ兼用。
- Instagram用に縦 **1080×1350** が要る場合は同デザインを縦に再構成。
- 出力は `--force-device-scale-factor=2` で2倍解像度（2400×1260）。

### A-2. デザイン規範（プロ級和文タイポ・[[feedback_thumbnail_pro_typography_default]]）
- フォント: `"Hiragino Sans"`、見出しは `font-weight:900`（W8/W9相当）。
- `font-feature-settings:"palt" 1;`（約物半角詰め）を見出し・帯・数字に必ず付与。
- 見出し `line-height:1.12〜1.16`、`letter-spacing:.01em`。
- 草川カラー: 深緑 `#1f5a3a`／コスモス等ピンク系アクセント `#e0357a`／クリーム地 `#f8f4ea`／補助 lime `#c7ff4a` はブランド動画用。テーマに合わせ主役色を選ぶ（コスモス=ピンク×緑）。
- キーワード1語だけアクセント色で差す（例「**種まき**イベント」の種まきをピンク）。
- 絵文字は使わない。装飾はCSS（ピル/角マーカー/破線ボーダー/花SVG）で。
- 余白と情報階層: 上=募集/無料などのピル、中=主見出し、下=日付大数字＋補足、最下=申込条件。フレーム（内側ボーダー）で締める。

### A-3. 手順
1. HTMLを Write（`~/outputs/thumbnails/<日付>_<テーマ>/thumb.html`）。`<body>` を `width:1200px;height:630px;overflow:hidden` に固定。装飾の花などは inline SVG（`<use href="#…">` で再利用、**円弁のデイジー型が確実に花に見える**。細い楕円弁は鳥/矢印に見えやすいので避ける）。
2. レンダ:
```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --hide-scrollbars --force-device-scale-factor=2 --window-size=1200,630 \
  --screenshot=thumb.png "file://$PWD/thumb.html"
```
3. **PNGを自分でRead**。よくある破綻＝(a)コンテンツが630pxを超えて下段が枠外に消える（`margin-top:auto`＋詰め過ぎが原因→フォント/余白を圧縮）、(b)装飾が意図通りに見えない、(c)可読性不足。修正して再レンダ→再Read、破綻ゼロまで。
4. 完成PNGを `open`。良ければ保存先マップ準拠で保管。

### A-4. 配信面ゲート（必須・skip禁止）

A-3 の「原寸で破綻ゼロ」は**合格条件の半分でしかない**。原寸1200×630で完璧でも、Xカード幅400pxに縮んだ瞬間に本文が7pxになって読めない、という事故が起きる（2026-08-31 育休退園サムネ）。確定前に必ず通す。

```bash
python3 ~/.claude/scripts/feed_preview.py still <画像.png>   # 400px/200px の縮小コンタクトシートを1枚生成
```

→ 生成された1枚を持って **`feed-visual-reviewer` エージェントを起動**し、`PASS` を取ってから確定する。`FIX`／`REBUILD` なら直して再度通す。

**最低限、これだけは覚えておく:**
- **400pxで読めない文字は情報量ゼロの装飾。** 削るか、読めるサイズまで拡大するかの二択。
- **メイン1行は原寸100px以上、副1行は56px以上。** 本文級（20px前後）のテキストがある時点で、それはサムネではなく図版。
- **文字ブロックはサムネ4つまで**（ラベル・見出し・副見出し・署名で既に4）。数字・before/after・詳細は本文と図版に逃がす。
- 伝えている用件を1文で言えなければ作り直し。

---

## B. ショート動画（Instagram Reels / TikTok / YouTube ショート・9:16）

写真スライドショー型（各写真＝背景、テキストは透過PNGカードを overlay、ゆるやかズーム＋ハードカット）。talking-head不要。

### B-1. 写真の正立化とマッピング（必須・Read）
iPhone写真はEXIF回転を持つことがある。**ffmpegはデフォルトでautorotate ON**なので、ffmpeg経由なら正立化される（sipsのorientation照会は`<nil>`でも実際は回っていることがある＝信用しない）。
1. 全写真を作業dirにコピー。
2. 3×2などの**コンタクトシートを1枚生成して自Read**し、ファイル名→内容→縦横を確定（人物/全景/のぼり等の取り違え防止・[[feedback_photo_video_input_run_full_pipeline]]）。
   ```
   ffmpeg -y -i A.jpg -i B.jpg ... -filter_complex \
     "[0:v]scale=600:450:force_original_aspect_ratio=decrease,pad=600:450:(ow-iw)/2:(oh-ih)/2:color=gray[a]; …; [a][b][c]hstack=3[t];[d][e][f]hstack=3[b2];[t][b2]vstack=2[out]" -map "[out]" contact.png
   ```
3. 各写真を 1080×1920 に正立クロップ（縦写真はフル、横写真は中央クロップ・人物は上寄せbias）:
   ```
   ffmpeg -y -i src.jpg -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920:(iw-1080)/2:(ih-1920)*BIAS" -frames:v 1 norm.png
   ```
   BIAS: 0=上 0.5=中央 1=下（草川は顔が切れないよう 0.4前後）。**縦クロップのコンタクトを再度自Read**して框を確認。

### B-2. テキストカード（透過PNG・1080×1920）
1枚のパラメトリックHTML（`card.html?i=N`・JSでカード配列を切替）を作り、6枚前後を生成。
- `html,body{background:transparent}`＋Chrome `--default-background-color=00000000` で**透過PNG**。
- 可読性スクリム: 下から `linear-gradient(180deg, transparent 38%, rgba(0,0,0,.72) 100%)` を全面に敷く。イベント情報カードは半透明パネル（`rgba(20,58,38,.8)`＋白枠）。
- **Reels安全域**: 重要文字は上端UI/下端キャプション帯を避ける。本文ブロックは `bottom:210〜260px` に置く。フォントはヒラギノW9、主見出し ~80px、白＋`text-shadow`、キーワードのみピンク。
- レンダ:
```
for i in 1 2 3 4 5 6; do
 "…/Google Chrome" --headless --disable-gpu --hide-scrollbars \
   --default-background-color=00000000 --force-device-scale-factor=1 \
   --window-size=1080,1920 --screenshot="cards/card$i.png" "file://$PWD/card.html?i=$i"; done
```
- 各カードを写真に overlay した**合成フレームのコンタクトを自Read**して可読性・配置を確認（EYES-FIRST）。zsh配列は**1始まり**（`${P[1]}`）に注意。

### B-3. 構成テンプレ（≈16〜18秒・6カット）
1. フック（ヒーロー写真＋短い引き）→ 2. 復活/背景 → 3. 人物（草川）→ 4. 意味（自分でまいた種が花に）→ 5. **イベント情報カード**（日付大・無料/申込不要/親子歓迎/集合/小雨決行）→ 6. CTA（キャッチ＋Instagram等の導線）。

### B-4. 合成（軽量・タイムアウト回避）
各写真＋カードを合成→2.8秒セグメント（ゆるやかKen Burns）→concat→前後フェード。**重い4Kズームは避ける**（`scale=1350:2400`程度＋`-preset veryfast -crf 23`）。全工程は**スクリプト化してバックグラウンド実行**（フォアグラウンドは2分で切れる）。
```
# セグメント（frameN.png = 写真＋カード合成済）
# ⚠️落とし穴: `-loop 1 -t 2.8` + zoompan `d=70` は掛け算になり 70×70=4900フレーム(196秒)に膨張する。
# 正: 単一フレーム入力（-loop/-t なし）＋ zoompan d=70 → ちょうど70フレーム(2.8秒@25fps)。trimで保険。
ffmpeg -y -i seg/frameN.png -filter_complex \
 "[0:v]scale=1350:2400,zoompan=z='min(zoom+0.0008,1.14)':d=70:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=25,trim=duration=2.8,setsar=1,format=yuv420p[v]" \
 -map "[v]" -c:v libx264 -preset veryfast -crf 23 -r 25 seg/segN.mp4
# 連結（同一コーデック）→ concat demuxer
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy seg/joined.mp4
# 前後フェード
ffmpeg -y -i seg/joined.mp4 -vf "fade=t=in:st=0:d=0.5,fade=t=out:st=<終端-0.5>:d=0.5" \
 -c:v libx264 -preset veryfast -crf 22 -pix_fmt yuv420p -movflags +faststart 完成.mp4
```
- 音声は付けない。納品時に「Instagramアプリ内で音楽を追加してください」と添える。
- `ffprobe` で尺・解像度を検証してから `open`。

### B-5. 保存
`~/outputs/short-video/<日付>_<テーマ>/`（src/ norm/ cards/ seg/ ＋完成mp4）。完成mp4はスマホ編集用に Drive `📱動画素材` ミラーも検討。

---

## C. 落とし穴チェックリスト
- [ ] サムネ着手前に「元写真ある？」を1回聞いたか（[[feedback_thumbnail_ask_base_photo_first]]）
- [ ] 絵文字ゼロ・他議員名ゼロ・公選法（おもてなしは団体主体）を確認したか
- [ ] レンダPNG/合成フレームを**自分でRead**したか（サブエージェント委譲は禁止）
- [ ] 写真の向き・人物/全景の取り違えをコンタクトで確認したか
- [ ] 動画ビルドをバックグラウンド実行したか（フォアグラウンド2分制限）
- [ ] zsh配列は1始まりで参照したか
- [ ] 文言はfact→risk通過（ブログ流用は継承可）したか
- [ ] 出力は絶対パス（~/outputs/…）に保存したか

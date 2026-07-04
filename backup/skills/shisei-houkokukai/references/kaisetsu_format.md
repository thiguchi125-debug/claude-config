# 解説カードPDF 生成フォーマット（kaisetsu_format.md）

> 対象: SKILL.md（shisei-houkokukai）の **Stage4 連動解説**（ノート＋山場フル台本）と **Stage5 前夜チェック**の差分再生成が参照する実装手順書。
> 設計書 `/Users/kusakawatakuya/.claude/skills/shisei-houkokukai/design/2026-07-04-shisei-houkokukai-design.md` §6（Stage4）・§7-1（前夜の差分再生成）を実行可能な手順に落としたもの。
> ベース技法: `[[feedback_event_runsheet_mobile_pdf_format]]`（イベント運営段取り表で確立した「スマホ縦スクロールPDF」手法）を市政報告会の解説カード向けに移植し、本タスクで実地検証して数値を確定した。

## 0. 禁止事項（毎回必須）

- **絵文字を使わない**（`[[feedback_no_emoji_ai_smell]]`）。見出し装飾はCSSのバッジ・カード枠色で行う。
- **他議員の氏名を書かない**（`[[feedback_no_other_council_members_names]]`）。想定質問・引用等で他議員に触れる必要がある場合も汎用表記に留める。
- カードの語りはvoice-dna照合。おうむ返し・AI定型句を排除（設計書§6）。

## 1. カード構造（HTML）

- 1スライド＝1カード。`<section class="card card-note" data-id="s-cover">` のように **slides.html と同じ `data-id` を必ず持たせる**（IDロック。設計書§6）。連番ではなくID紐付けなので、スライドの挿入・差し替えが起きても該当カードだけ再生成すれば済む（§3 差分再生成）。
- カード種別は3つ。class名は固定（後続タスクが参照する契約）:
  - `card-note` — 通常ノート。クリーム地 `#f3efe4`
  - `card-yamaba` — 山場フル台本。lime `#c7ff4a` の帯・枠付きで強調
  - `card-time` — 時間チェックポイント。濃緑 `#0f3d27` 地に白文字
- カード内フィールド（共通）:
  - スライド見出し（`.card-title`）
  - 通し番号表示（`.card-idrow` に `data-id` と併記。「通し番号 5 / 12」のように現在の総枚数中の位置を出す。連番が変わっても data-id は不変）
  - 話す骨子（3行以内・`.card-kossi` の `<li>`）
  - 累積時間目安（`.card-time-badge`。「累積 8:00」等、開始からの累積分）
  - 問いかけ・挙手キュー（`.card-cue`）
  - 用語言い換え（`.card-glossary`。プレイブックD-3の平易言い換え辞書を適用）
- `card-yamaba` のみ追加で **フル台本ブロック**（`.yamaba-script`）を持つ。クイズの回し方（間の取り方・会場の答えの拾い方・外れたときの受け）を読み上げ文そのままで書く。community-rally-speaker の技法（掴み→柱→結びのアジ構造・生活者の言葉）を参照craftとして適用する。
- `card-time` は骨子・問いかけの代わりに `.time-check-value`（経過時間の大きな数字）と `.time-check-note`（押している場合の削り所）を持つ。
- ヘッダー（`header.doc-header`）に地区名・開催日・会場・開始時刻をまとめて出す。全カード共通で1回のみ。

最小スケルトン（実装のベースとして使う。クラス名・data-id属性名は固定契約）:

```html
<div class="wrap" id="doc-root">
  <header class="doc-header">
    <p class="district">〇〇地区 市政報告会</p>
    <p class="meta">開催日: 2026年〇月〇日（〇）<br>会場: 〇〇公民館<br>開始時刻: 19:00</p>
  </header>

  <section class="card card-note" data-id="s-cover">
    <div class="card-idrow"><span>通し番号 1 / 12</span><span>data-id: s-cover</span></div>
    <span class="card-time-badge">累積 0:30</span>
    <h2 class="card-title">開会挨拶・自己紹介</h2>
    <ul class="card-kossi"><li>…</li><li>…</li><li>…</li></ul>
    <div class="card-cue">問いかけ: 「…」</div>
    <div class="card-glossary">用語言い換え: 「一般質問」→「議会で市に質問すること」</div>
  </section>

  <section class="card card-yamaba" data-id="s-quiz-01">
    <div class="card-idrow"><span>通し番号 5 / 12</span><span>data-id: s-quiz-01</span></div>
    <span class="yamaba-label">山場・フル台本</span>
    <span class="card-time-badge">累積 8:00</span>
    <h2 class="card-title">クイズ: 〇〇</h2>
    <ul class="card-kossi"><li>…</li></ul>
    <div class="card-cue">挙手キュー: 「…」（間を作って待つ）</div>
    <div class="yamaba-script">読み上げ文をそのまま書く。……（10秒待つ）……</div>
    <div class="card-glossary">用語言い換え: 「…」</div>
  </section>

  <section class="card card-time" data-id="s-time-01">
    <div class="card-idrow"><span>通し番号 — / 12</span><span>data-id: s-time-01</span></div>
    <p class="time-check-title">時間チェックポイント</p>
    <p class="time-check-value">経過 15:00</p>
    <p class="time-check-note">押している場合は次の柱の具体例を1つ削る。</p>
  </section>
</div>
```

- レイアウトはモバイルファースト1カラム `max-width:390px`・絵文字なし。CSS変数はテンプレ血統デッキと合わせる: `--cream:#f3efe4` `--lime:#c7ff4a` `--green-deep:#0f3d27` `--green:#1f5a3a`。

## 2. PDF化手順（確定・実地検証済み）

`[[feedback_event_runsheet_mobile_pdf_format]]` の確定手法をベースに、本タスクで実際に3カード分のサンプルを生成して数値を検証した。**+200pxは経験則上の「安全な探索の出発点」であって固定の正解値ではない**（本タスクの検証では最終的に+3px程度で足りた）。必ず実測してから決める。

### 手順

1. HTMLは `width=device-width` のレスポンシブで作成し、`open <html絶対パス>` でブラウザ確認する（草川が中身を確認する用途にも使う）。

2. **スクリーンショットで content の概算高さを測る**（印刷用@pageの初期値を決めるため）。ウィンドウを十分縦長（390×4000等）にして headless スクリーンショットを撮り、Pythonで背景色と異なる最終行を検出する:

   ```
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
     --headless --disable-gpu --window-size=390,4000 \
     --screenshot=<出力.png> file://<HTML絶対パス>
   ```

   ```python
   from PIL import Image
   img = Image.open("<出力.png>").convert("RGB")
   w, h = img.size
   bg = (229, 229, 229)  # ページ外枠の背景色（例）。デザインに合わせて変える
   last_content_row = 0
   for y in range(h - 1, -1, -1):
       row = [img.getpixel((x, y)) for x in range(0, w, 10)]
       if any(abs(px[i] - bg[i]) > 6 for px in row for i in range(3)):
           last_content_row = y
           break
   print(last_content_row)  # ここが content の概算下端px
   ```

3. **印刷用コピーを作り、@pageに初期値（概算下端 + 200〜260pxの安全マージン）を入れて Chrome headless で PDF化する**。測定をしやすくするため、このコピーだけ `@media print{html,body{background:#fff}}` にして白背景に固定する:

   ```html
   <style>
   @page{size:390px <H>px;margin:0;}
   @media print{html,body{background:#fff;}}
   </style>
   ```

   ```
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
     --headless --disable-gpu --print-to-pdf=<出力.pdf> --no-pdf-header-footer \
     file://<印刷用HTML絶対パス>
   ```

4. **単ページ検証＝`/Count`が`1`になる高さを下から探索する**:

   ```
   strings <出力.pdf> | grep -m1 "/Count"
   ```

   `<H>` を少しずつ下げながら実行し、`/Count 1` から `/Count 2` に切り替わる境界を見つける（線形探索で十分。10〜20px刻み）。

5. **PIL＋pdftoppmで content の正確な下端pxを取り、切り替わり境界の少し上（+30〜50px程度の安全マージン）を最終の`<H>`にする**（色付き長余白の防止。原則6）:

   ```
   pdftoppm -png -r 96 <出力.pdf> <出力プレフィックス>
   ```

   ```python
   from PIL import Image
   img = Image.open("<出力プレフィックス>-1.png").convert("RGB")
   w, h = img.size
   white = (255, 255, 255)
   last_content_row = 0
   for y in range(h - 1, -1, -1):
       row = [img.getpixel((x, y)) for x in range(0, w, 5)]
       if any(abs(px[i] - white[i]) > 8 for px in row for i in range(3)):
           last_content_row = y
           break
   print(last_content_row)  # ここが content の正確な下端px
   ```

6. **最終の `<H>` を確定したら、白背景の強制指定を外した「本番用HTML」を作り、確定`<H>`で再度 print-to-pdf → `/Count 1` を再確認**してから納品する。body背景色はページ全体を塗るため、ページ高さを中身ぴったりにしておかないと色付きの長い余白ができる（原則6）。

7. `open <確定PDF絶対パス>` でプレビュー→草川承認→`04_kaisetsu/` へ確定保存。

### 実地検証で得た実測値（本タスクのサンプル3カードでの実測。今後の目安）

- スクリーンショット測定（`window-size=390,4000`）での content 下端: **1137px**
- 探索の出発点（1137 + 200 + 60 = 1397 → 1400pxで試行）: `/Count 1`（成功。ただし過剰に高い＝下に大きな余白ができる状態）
- 下からの探索結果: `H=1137px` は `/Count 2`（2ページ化）、`H=1140px` から `/Count 1`（境界は1137〜1140の間）
- 最終確定値: **H=1160px**（境界に対し+23pxの安全マージン）で `/Count 1` を再確認。3カード（card-note 1・card-yamaba 1・card-time 1）＋ヘッダーで幅390px・高さ1160pxの1ページ縦長PDFが生成できた
- 教訓: **+200pxは「まず試す安全な初期値」であり、最終値ではない**。カード数・フル台本の文章量・改行の入り方でcontent高さは毎回変わるため、手順2〜5の実測を毎回必ず行う。決め打ちで固定高さを使い回さない。

## 3. 差分再生成（前夜用・設計書§7-1）

- 対象 `data-id` のカードだけHTMLを書き換える（他のカードは触らない。IDロック設計）。
- カードHTML自体は1ファイルなので、書き換え後に**全体を再度PDF化する**（部分PDF差し替えはしない。手順2〜6を丸ごとやり直す）。
- 書き換えたカードの行数・フル台本の文章量が変わると content 高さも変わるため、**前回の `<H>` を使い回さず、手順2〜5の実測を再実行して `/Count 1` の高さを再探索する**。前夜チェック（Stage5）はこの再生成コストが小さいことを前提にしている（設計書§7-1）。
- 再生成後は必ず `strings <PDF> | grep -m1 "/Count"` → `/Count 1` を再確認してから確定保存する。

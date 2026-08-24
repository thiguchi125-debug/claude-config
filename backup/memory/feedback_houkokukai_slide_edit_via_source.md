---
name: feedback-houkokukai-slide-edit-via-source
description: 市政報告会スライドの追加・削除・差し替えはPDFを切らずソースHTMLを直してrebuild。地区デッキ間の流用手順つき。
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b4262aa4-e6df-42b3-a5c6-8385ef1b59e8
  modified: 2026-08-24T13:44:54.416Z
---

市政報告会デッキ（`~/outputs/houkokukai/<日付>_<地区>/03_slides/`）のスライドを **1枚外す・1枚足す・写真を入れる** ときは、完成PDFを直接加工せず **ソースHTMLを編集して再ビルド** する。

**Why:** デッキは `_body*.html`（本文セクション群）＋ `_head.html`（CSS）→ `build.py` → `slides.html` → Chrome headless → PDF という組み立て。PDFだけページを抜くとソースと版が割れ、次に誰かが再ビルドした瞬間に削除が巻き戻る。ページ番号 `{{P}}` もビルド時に振り直されるため、ソースを直せば通し番号は自動で正しくなる。

**How to apply:**
- 構成ファイルは地区で違う。安知本＝`_body.html` 1本＋`_render.sh`／出屋＝`_body_p1.html`＋`_body_p2.html`＋`rebuild.sh`。まず `ls` して確かめる。CSSは 出屋＝`_head.html`、安知本＝`build.py` 内に直書き、と置き場所も違う。
- 削除は `data-id="..."` の `<section>` ブロック単位で消す。編集前に `cp <file> <file>.bak_$(date +%H%M)`、完成PDFも `_old_<名前>_<旧ページ数>p.pdf` に退避してから差し替える。
- 「写真1枚だけのページ」等の曖昧な指示は、`pdftotext -layout -f N -l N` を全ページ回して**本文の文字数**を出すと一発で特定できる（章扉と写真ページだけ極端に短い）。
- **地区デッキ間の流用**（例：安知本→出屋に4枚移植）は4点セットで運ぶ。①`<section>`ブロック ②`assets/` の画像（md5で既存と重複チェック）③その data-id 専用のCSS上書き（これを忘れると図の比率や `object-fit` が崩れる。複数行にまたがるルールの取りこぼしに注意）④フッターの `市政報告会＠<地区>` を移植先の地区名に置換。data-id は `s-achi-` → `s-dy-` のように接頭辞ごとリネームし、CSSセレクタも同時に置換する。
- レイアウトを変えたら **PNGにして自分で見る**（`pdftoppm -png -r 100 -f N -l N`）。実測したのは、全面テキスト型を `split`（左テキスト58%／右写真42%）へ変えると本文量そのままでは**フッターと出典行が数字ボックスに潰される**こと。本文フォント・stat の padding・出典行の文字数を削って収める。
- 写真に文字が焼き込まれたスクショを渡された場合は、その帯をトリミングして落とし、キャプションはデッキ側の `.cap` で入れ直す（書体・配色が揃う）。`object-position` で被写体が切れない位置に寄せる。

関連: [[feedback-shisei-houkokukai-slides-claude-code]]（制作フローの正本）／[[feedback-report-vs-slides-wording]]（「レポート」の指示語）／[[feedback-open-folder-after-generating-files]]

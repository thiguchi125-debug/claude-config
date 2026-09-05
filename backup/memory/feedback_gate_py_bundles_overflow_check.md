---
name: feedback-gate-py-bundles-overflow-check
description: 挿入画像は check_image_design.py と目視の両方を通っても枠はみ出しが残る。gate.py が同梱する check_overflow.py だけが実測で捕まえる
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e2fb0731-aaa7-4509-be09-72e3bde44b7b
  modified: 2026-08-26T16:42:54.481Z
---

ショート動画の挿入画像は、`check_image_design.py`（級数・行間・帯位置）と `check_subtitle_band.py`（帯の前景率）と**PNGの目視**を全部通しても、**枠からのはみ出しが残ることがある**。実測で捕まえるのは `check_overflow.py` だけで、これは `gate.py` が .html に対して自動で回す。

2026-08-27、育休退園 a3 の出典行が `div.abs`（width 950）を15px超えていた（need=965 / have=950）。PNGでは1080枠の内側（右余白37px）に収まっていたので**目視では崩れて見えず**、design gate も band gate も ✅ を返した。gate.py で初めて 🚨 が出た。

**Why:** `.abs{width:950px}` のような固定幅ボックスは、テキストがはみ出しても `overflow:visible` なら画面内にそのまま描画される。見た目の破綻がないので目視は通る。しかし左右マージン40-60pxの原則は破れていて、印刷・別解像度・トリミングで欠ける。design gate はCSSの数値しか見ず、band gate は帯の中しか見ないので、どちらも構造上これを見つけられない。

**How to apply:**
- 挿入画像・印刷物のHTMLは、**個別のチェッカーを単発で回さず `python3 ~/.claude/scripts/gate.py <html...> --pass` に集約する**。design / overflow / band を全部回したうえで指紋を記録してくれる
- はみ出しが出たら、`.abs` の width を広げるのではなく**文言を短くする**。左右マージンを削ると agents/knowledge/design_system/short_video_templates/README.md §3-5 の「端の見切れなし（左右40-60px）」を破る
- 日本語の実幅は「全角=font-size」の見積もりより広く出る。36pxの1行に26字入るつもりでも実測では入らないことがある。**字数で足りると判断せず、レンダして測る**
- 関連：[[feedback_kameyama_kanji_typo_guard]]

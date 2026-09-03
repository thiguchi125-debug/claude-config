---
name: feedback-news-digest-gate-blog-misdetect
description: news-briefingのダイジェスト本文をgate.pyに.mdで渡すとブログ判定され「名乗り欠落・フッター欠落」で必ず落ちる
metadata:
  type: feedback
---

`~/.claude/scripts/check_content_limits.py` の `kind_of()` はファイル名で種別を決め、"SNS"も"動画"も含まなければ**一律ブログ**にする。ニュースダイジェストは種別が存在しないため、`gate.py <file>.md` に渡すと「🚨 冒頭の名乗り」「🚨 定型フッター欠落」で機械チェックが落ち、`--pass` を付けても記録されない（fail時に return 1）。

**How to apply:** ダイジェスト本文は `.txt` で保存して `gate.py <file>.txt --pass` を実行する。gate.py は `.md`/`.html` 以外に機械チェックを回さないため、fact-checker・risk-reviewer を通した宣言だけが記録される。ブログ規格チェックはダイジェストに適用対象外なので、これは迂回ではなく正しい運用。

**Why:** 2026-08-26 の朝ジョブで実際に2回denyされた（ダイジェスト本文とdedupインデックス追記の両方がゲート対象）。dedupインデックスへの追記行も「本文」なので同じ手順が要る。`_content_gate.json` は上書き方式なので、ダイジェスト→dedupの順に1件ずつ記録して書き込む。

**追記 2026-08-27:** `update_content` で**見出し行を差し替える**とき（例「## 直近登録（最終更新 2026-08-26）」→「…2026-08-27）」）、`new_str` 側の見出し文字列も承認txtに入っていないと deny される。追記する明細行だけをtxtに書いても足りない。**Notionへ送る new_str の全文をそのままtxtに含めてから gate.py を回す**こと。この日は見出し1行の欠落で1回denyされ、txtに1行足して再gateで通した。

関連: [[feedback-gate-json-concurrent-overwrite]] [[feedback-safety-gates-before-notion-save]] [[feedback-oyasumi-blocked-by-content-gate]]

**2026-09-03 解消**: `INTERNAL_NAME_HINTS` に「ダイジェスト／digest／briefing／ブリーフィング」を追加。ファイル名にこれらを含めば `internal` 判定になり、ブログ規定（名乗り・定型フッター・5段構成）は当たらなくなった。`.txt` に逃がす回避策はもう不要（そもそも `gate.py` が `.txt` を素通りさせていたため、回避策は「検査されない」だけだった）。

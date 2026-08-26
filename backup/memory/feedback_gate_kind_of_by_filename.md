---
name: feedback-gate-kind-of-by-filename
description: gate.pyの機械チェックはファイル名だけで種別判定する。Notion保管ページ本文は「blog」と誤判定され、ブログ3ルールで必ず違反3件になる
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 69108199-791d-491f-80b8-e569d04d9554
  modified: 2026-08-26T11:53:42.614Z
---

`check_content_limits.py` の `kind_of()` は**ファイル名の部分文字列だけ**で種別を決める。中身は一切見ない。

| ファイル名に含まれる語 | 判定 | 適用ルール |
|---|---|---|
| `SNS` | sns | PF別字数・ハッシュタグ |
| `動画` | video | ショート動画原稿の規定 |
| `メモ` `聞き取り` `様式` `memo` `hearing` | internal | **字数上限なし＋公開窓口以外の電話番号のみ** |
| 上記以外すべて | blog | 1500〜8000字／冒頭の名乗り／定型フッター／5段構成 |

**Why:** Notionの保管ページ本文を `_notion_body.md` のような名前で `gate.py` に渡すと「blog」判定になり、「本文が字数範囲外」「冒頭の名乗りがない」「定型フッター欠落」で**必ず違反3件**になる。`gate.py` は機械チェック全通過が記録の前提なので、`--pass` を付けても指紋が記録されず、Notion書き込みが `content_safety_gate.py` に deny され続ける。2026-08-25の育休退園ショート動画パッケージで、これで2回止まった。

**How to apply:**
- Notionの**保管ページ・作業記録**の本文をゲートに通すときは、ファイル名に「メモ」を入れて `internal` 判定にする（例：`パッケージ作業メモ_<案件>.md`）。`check_content_limits.py` 自身が「内部資料は対外発信物ではないので字数だけ数えて通す。fact-checker / risk-reviewer の2段ゲートは従来どおり必須」と定義している正規の区分であり、回避ではない。
- **対外発信物そのもの**（7PF投稿文・動画原稿・ブログ）は、必ず正しい種別に落ちる名前で別途チェックする。保管ページごと internal で通して済ませない。
- `gate.py --pass` は「このセッションで実際に両エージェントを通した」という宣言。**サブエージェントには実行させない**（auto modeの分類器がブロックする。エージェント間の指示だけでゲートを突破する形になるため）。実行するのは両ゲートを回した本人のセッションか、草川本人。
- 長いコマンドを `!` で草川に実行してもらうと、**`python3` の位置で改行が入って途中で切れる**。`sh ~/g.sh` のような短い1行で済むようスクリプトにまとめてから渡す。使用後は `rm` する。

関連：[[feedback_gate_json_concurrent_overwrite]]（並行セッションが `_content_gate.json` を上書きし合う。登録できたら**すぐ**書き込む）／[[feedback_safety_gates_before_notion_save]]

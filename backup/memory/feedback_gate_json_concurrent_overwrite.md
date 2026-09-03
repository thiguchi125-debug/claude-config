---
name: feedback-gate-json-concurrent-overwrite
description: gate.pyは_content_gate.jsonを毎回丸ごと書き直すため、並行セッションが互いの承認記録を消し合う。抜け道を作らず記録し直して即書き込む
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0c0b56ce-7018-4a00-816d-14ec55602a5b
  modified: 2026-08-12T13:07:16.068Z
---

`~/.claude/scripts/gate.py` は実行のたびに `~/.claude/hooks/_content_gate.json` を**新しい dict で丸ごと上書き**する（`rec = {...}` → `json.dump`）。マージしない。

**Why**: 2026-08-12、市民相談レコードの保存中に夕便のSNS原稿v3を回す別セッションと**3回衝突**した。gate.py を通した直後にNotionへ書こうとすると、その数十秒の間に相手がgate.pyを走らせて記録が消え、hookが「承認済み原稿に無い文言」でdenyする。エラー文面は「本文が違う」と読めるので、**本文の差分を探して時間を溶かす**のが典型的な罠。

**How to apply**:
- denyされたら、まず本文を疑う前に `python3 -c "import json;d=json.load(open('~/.claude/hooks/_content_gate.json'));print([a['file'] for a in d['approved']], d['generated_at'])"` で**自分のファイル名が載っているか**を見る。載っていなければ衝突。
- 対処は「gate.py を通し直して**同一ターン内で即Notionへ書く**」。間に他の作業を挟まない。
- **他人のファイルを巻き込んで `--pass` しない**。`--pass` は「自分がfact/riskを通した」という宣言であり、他セッションの原稿に付けるのは虚偽になる。
- 自分が上書きした場合は、相手側がgate.py再実行を要することを草川に申し送る。
- 恒久対策はマージ実装への修正だが、**別セッション稼働中に共有ファイルをいじらない**（2026-08-12は「今は触らない」判断）。

関連の罠: gate.py の `.md` はデフォルトでブログ判定になり、名乗り・定型フッターを要求してくる。**内部資料はファイル名に「メモ」「聞き取り」「様式」「memo」「hearing」のいずれかを含める**と `internal` 判定になりブログ規定が外れる（`check_content_limits.py` の `kind_of`）。拡張子を変えて機械チェックごと回避するのは筋が悪い。

hookは**既存ページの1行書き換え（匿名化など）も一律deny**する。差分の意図を判定できないため。小さな匿名化のために抜け道を作らず、草川にNotion上で直接直してもらうか、fact/riskを1往復させる。

[[feedback_safety_gates_before_notion_save]]

**2026-09-03 修理済み**: 真因は `gate.py` の `json.dump(rec, open(GATE,"w"))` ＝**毎回まるごと上書き**していたこと。
並行セッションが --pass するたび、相手の承認記録が消えていた（本日、実際にこちらが別セッション＝妊婦通院関連の記録を消して deny を誘発）。
- `gate.py`：上書き→**マージ**に変更。期限切れだけを落とし、同じファイル名の記録だけを置き換え、他セッションの生きた記録は残す。fcntlロック＋`os.replace` で原子的に書く。レコードに `at` / `ttl_minutes` / `session` を持たせた。
- `content_safety_gate.py`：期限判定を**ファイル単位→レコード単位**に変更（先頭の `generated_at` だけで全部を無効化すると他セッションを巻き込むため）。旧形式のレコードも読める。
- 実測：A→B と続けて --pass しても両方残る（「併存：他に生きている承認記録 N件は消さずに残しました」と表示される）。
以後、denyを見たらまず `_content_gate.json` を疑うのは同じだが、**原因が「消し合い」である可能性は下がった**。指紋不一致（本文を変えた／前後に注記を足した）を先に疑う。


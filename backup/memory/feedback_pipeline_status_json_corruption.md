---
name: feedback-pipeline-status-json-corruption
description: update_status.py は _pipeline_status.json が壊れていると例外終了し夜間ジョブの死活記録が丸ごと落ちる。復旧は raw_decode で有効プレフィックスだけ残す
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 63fc0313-f7c1-4f9b-9bc0-0dfe17de27e6
  modified: 2026-08-14T00:46:26.642Z
---

`~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_pipeline_status.json` は末尾に前回書き込みの断片が残って `JSONDecodeError: Extra data` になることがある（2026-08-14 form-intake夜間バッチで実際に発生。有効JSONは1213字で終わり、その後ろに `-09T03:24:20"\n }\n}` という sns_audit の重複断片が付いていた）。

**Why:** `update_status.py` は先頭で `json.load` するだけでフォールバックが無く、壊れていると **exit 1 で死活記録を書けずに終わる**。夜間ジョブ側は「update_status.py を最後に必ず実行する」前提なので、翌朝の ohayo が🚨誤報を出す（実際の処理は正常に終わっていても）。`os.replace` で原子的に書いてはいるので、原因は並行セッションからの別経路の書き込みと思われる（[[feedback-gate-json-concurrent-overwrite]] と同型の事故）。

**How to apply:** `update_status.py` が JSONDecodeError で落ちたら、本文の処理を疑う前にこのファイルを疑う。復旧は上書きでなく **有効プレフィックスの救出**：`.corrupt_<日付>.bak` を取ってから `json.JSONDecoder().raw_decode(s)` で先頭の正しいオブジェクトだけ取り出し、捨てる末尾を必ず目視してから書き戻す（断片が重複でなく実データなら手で戻す）。書き戻し後に再パース＋キー数を確認してから `update_status.py` を再実行する。

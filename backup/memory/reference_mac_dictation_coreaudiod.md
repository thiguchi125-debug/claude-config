---
name: reference-mac-dictation-coreaudiod
description: Macの音声入力が起動しない時の真因はcoreaudiod（音の司令塔）の不調。音声認識プロセスの再起動では直らない
metadata:
  type: reference
---
2026-09-18 朝（8:00）と昼（11:09）の2回、Macの音声入力が起動しなかった。
- 8:00は corespeechd/assistantd/DictationIM を killall → いったん直ったように見えたが再発。
- 11:09のログで真因が判明：coreaudiod（9/14から4日稼働）の内蔵スピーカーの入出力スレッドが起動できない（Error 1937010544 = 'stop'）→ 音声入力開始時の「ポン」音が鳴らせない → Watchdogタイムアウト → kAFAssistantErrorDomain Code=203 "Corrupt"。
- 対処：`sudo killall coreaudiod`（パスワードが要る＝草川に `! sudo killall coreaudiod` を打ってもらう）。それでも駄目なら再起動。
- 確認コマンド：`/usr/bin/log show --last 30m --predicate 'process == "coreaudiod"' --style compact | grep "failed to start"`
- zshでは `log` がシェル関数と衝突するので必ず `/usr/bin/log`。

---
name: project-stalled-automation-revival-2026-08-20
description: 起動0回のスキルは不要だったのではなく止まっていた。oyasumiとgyakusanをlaunchdで自動化した
metadata: 
  node_type: memory
  type: project
  originSessionId: 7a34af0c-0fd2-4656-9797-2d60b17ff192
  modified: 2026-08-20T12:57:45.884Z
---

2026-08-20、スキル整理のつもりで起動実績を測ったところ、**起動0回のスキルはどれも「不要だから」ではなく別の理由で止まっていた**。草川の「起動していないのには理由があるのでは？」という問いから判明した。

直近1ヶ月の実ユーザー発話 1,185件を抽出して照合した結果:

| スキル | 0回の理由 |
|---|---|
| oyasumi | **手動起動前提**。「おやすみ」発話0件。form-intake・news-briefing は launchd 自動化済みなのに oyasumi だけ手動だった |
| gyakusan | 「月曜のohayoが呼ぶ」設計だが、**ohayoの実行が30日で8回・うち月曜は7/27の1回だけ**。ohayo自体が週2回弱の運用 |
| drive-intake | launchd `com.kusagawa.daily-drive-pipeline` が毎日代行（**正常**。手動は不要） |
| ai-kusakawa | ElevenLabs 未登録で**ブロック中**（草川手番） |
| photo-post | この1ヶ月が印刷物制作期だったため。ただし「googleフォトを読み取って指定イベントの写真からSNS記事を作成できるか」という依頼があり、**Google Photos連携が守備範囲外で応えられていない**（未対応・残作業） |

**入れた自動化**
- `com.kusagawa.oyasumi`（毎晩23:30）— `~/.claude/scripts/oyasumi/oyasumi.sh` ＋ `oyasumi_prompt.md`。form-intake と同じ headless バッチ方式（ネット疎通待ち・2回リトライ・update_status.py で結果記録）
- `com.kusagawa.gyakusan`（毎週月曜6:30）— 単独実行し結果を `~/.claude/scripts/gyakusan/_gyakusan_status.json` に保存。**td.py は読み取りコマンドのみ allowedTools に渡す**ことで、勝手なTodoist登録を構造的に不可能にしてある
- ohayo SKILL.md 末尾を改訂 — 自分でStepを回さず `_gyakusan_status.json` を読んで表示するだけにした。曜日を問わず、7日以内の結果があれば出す

ログの取り方: skill起動は `grep -ohE '"skill":"[a-zA-Z0-9:_-]+"' *.jsonl`、agent起動は `"subagent_type"` を同様に。実ユーザー発話は `"type":"user"` の行から message.content を抜くと1,185件に絞れる（システムプロンプトが全行に載るため素のgrepでは数えられない）。

関連: [[project-token-reduction-2026-08-20]]

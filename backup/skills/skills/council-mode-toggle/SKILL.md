---
name: council-mode-toggle
description: 議会期間中（3/6/9/12月の本会議・委員会開催月）にDrive→ローカル同期Routineを「日次同期」に切り替えるスキル。トリガー: 「議会モードon」「議会モードオン」「議会モード開始」「議会モードoff」「議会モードオフ」「議会モード解除」「議会モード状態」「議会モード確認」など。weekly-drive-sync-kusagawa Routineのcron expressionを書き換えて、議会期は毎日21時JST同期、通常期は週2回（水・日21時JST）同期に切替える。状態は kusagawa_archive/99_raw/_scripts/_council_mode.json に永続化。
---

# 議会モード切替スキル

## 役割
議会期間中（3/6/9/12月）はDrive差分同期の頻度を上げ、議会後の資料を翌日には学習層に反映できるようにする。通常期は週2回で十分。

## トリガー語

### ON切替
- 「議会モードon」「議会モードオン」「議会モード開始」「議会開始」「議会期間入り」

### OFF切替
- 「議会モードoff」「議会モードオフ」「議会モード解除」「議会終了」「議会期間終わり」

### 状態確認
- 「議会モード状態」「議会モード確認」「いま議会モード？」「routine cron状態」

---

## 設計

### モード定義

| モード | cron (UTC) | JST | 頻度 |
|---|---|---|---|
| **通常** | `0 12 * * 0,3` | 毎週水・日 21:00 | 週2 |
| **議会モード** | `0 12 * * *` | 毎日 21:00 | 日次 |

### 状態永続化
`~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_council_mode.json`:

```json
{
  "mode": "normal" or "council",
  "last_changed_at": "ISO datetime",
  "current_cron": "0 12 * * 0,3",
  "history": [
    {"ts": "...", "mode": "council", "trigger": "草川: 議会モードon"}
  ]
}
```

---

## 実行ステップ

### A. ON切替時（通常 → 議会モード）

1. `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_council_mode.json` を読む
2. 既に `mode = council` なら「すでに議会モードです」と返して終了
3. RemoteTrigger update で cron変更:
   ```
   action: update
   trigger_id: trig_016r7yNKRqVubUvCJMTzVZ98
   body: {"cron_expression": "0 12 * * *"}
   ```
4. `_council_mode.json` を更新（mode=council, last_changed_at=now, history追記）
5. 草川に確認:
   ```
   ✅ 議会モード ON
   - cron: 0 12 * * * (毎日21:00 JST)
   - 次回実行: <next_run_at>
   - 議会終了時は「議会モードoff」と言ってください
   ```

### B. OFF切替時（議会モード → 通常）

1. `_council_mode.json` 確認
2. 既に `mode = normal` なら「すでに通常モードです」と返す
3. RemoteTrigger update で cron復元:
   ```
   body: {"cron_expression": "0 12 * * 0,3"}
   ```
4. `_council_mode.json` を更新（mode=normal, last_changed_at=now）
5. 草川に確認:
   ```
   ✅ 議会モード OFF（通常モードに復帰）
   - cron: 0 12 * * 0,3 (毎週水・日21:00 JST)
   - 次回実行: <next_run_at>
   ```

### C. 状態確認時

1. `_council_mode.json` 読む
2. RemoteTrigger get で現状の cron確認
3. 整合性チェック（jsonとRoutineが一致しているか）
4. 草川に表示:
   ```
   📊 議会モード状態
   - 現在: {mode}
   - cron: {current_cron}
   - 最終切替: {last_changed_at}
   - 次回実行: {next_run_at}
   - 切替履歴（直近5件）:
     1. ...
   ```

---

## _council_mode.json 初期化

スキル初回起動時にファイルがなければ作成:

```python
import json
from pathlib import Path
from datetime import datetime, timezone

p = Path("/Users/kusakawatakuya/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_council_mode.json")
if not p.exists():
    state = {
        "mode": "normal",
        "last_changed_at": datetime.now(timezone.utc).isoformat(),
        "current_cron": "0 12 * * 0,3",
        "history": [
            {"ts": datetime.now(timezone.utc).isoformat(), "mode": "normal", "trigger": "initial_setup"}
        ]
    }
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
```

---

## 関連リソース

- Routine: `weekly-drive-sync-kusagawa` (trig_016r7yNKRqVubUvCJMTzVZ98)
- 管理URL: https://claude.ai/code/routines/trig_016r7yNKRqVubUvCJMTzVZ98
- 状態DB: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_council_mode.json`
- 関連スキル: `weekly-drive-sync` / `drive-sync-review` / `ohayo`

## 自動切替（将来オプション・現状は手動）
- 議会日程DB or 議事日程APIから「3月議会開始日〜閉会日」「6月議会...」を取得
- ohayo月初に自動で「明日から議会期に入りますが議会モードonにしますか？」と提案
- 現状は草川の手動コマンドベース（議会日程に応じて随時）

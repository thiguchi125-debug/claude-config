---
name: council-mode-toggle
description: 議会期間中（3/6/9/12月の本会議・委員会開催月）にDrive→ローカル同期の頻度を上げるスキル。トリガー: 「議会モードon」「議会モードオン」「議会モード開始」「議会モードoff」「議会モードオフ」「議会モード解除」「議会モード状態」「議会モード確認」など。2026-05-21〜は **2系統を同時切替**: ①ローカルlaunchd `com.kusagawa.drive-sync.plist`（通常=朝7時+夜22時／議会期=7,13,19,22時の4回） ②クラウドRoutine `weekly-drive-sync-kusagawa`（通常=水・日21時JST／議会期=毎日21時JST）。状態は kusagawa_archive/99_raw/_scripts/_council_mode.json に永続化。
---

# 議会モード切替スキル

## 役割
議会期間中（3/6/9/12月）はDrive差分同期の頻度を上げ、議会後の資料を翌日には学習層に反映できるようにする。通常期は1日2回で十分。

2026-05-21〜 ローカルlaunchd（主軸）＋クラウドRoutine（補完）の2系統同時切替に拡張。

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
| **通常** | クラウド: `0 12 * * 0,3` (水日21時JST) / ローカル: 7,22時 | 週2＋日2回 |
| **議会モード** | クラウド: `0 12 * * *` (毎日21時JST) / ローカル: 7,13,19,22時 | 日次＋日4回 |

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
3. **クラウドRoutine cron変更**:
   ```
   RemoteTrigger update
     trigger_id: trig_016r7yNKRqVubUvCJMTzVZ98
     body: {"cron_expression": "0 12 * * *"}
   ```
4. **ローカルlaunchd 頻度切替（議会期 4回/日）**:
   ```bash
   python3 -c "
   import plistlib
   p='/Users/kusakawatakuya/Library/LaunchAgents/com.kusagawa.drive-sync.plist'
   pl=plistlib.load(open(p,'rb'))
   pl['StartCalendarInterval']=[
     {'Hour':7,'Minute':0},{'Hour':13,'Minute':0},
     {'Hour':19,'Minute':0},{'Hour':22,'Minute':0}
   ]
   plistlib.dump(pl,open(p,'wb'))
   "
   launchctl unload ~/Library/LaunchAgents/com.kusagawa.drive-sync.plist 2>/dev/null
   launchctl load ~/Library/LaunchAgents/com.kusagawa.drive-sync.plist
   ```
5. `_council_mode.json` を更新（mode=council, last_changed_at=now, history追記）
6. 草川に確認:
   ```
   ✅ 議会モード ON
   - クラウドRoutine: 毎日21:00 JST
   - ローカルlaunchd: 7,13,19,22時の4回/日
   - 議会終了時は「議会モードoff」と言ってください
   ```

### B. OFF切替時（議会モード → 通常）

1. `_council_mode.json` 確認
2. 既に `mode = normal` なら「すでに通常モードです」と返す
3. **クラウドRoutine cron復元**:
   ```
   RemoteTrigger update
     trigger_id: trig_016r7yNKRqVubUvCJMTzVZ98
     body: {"cron_expression": "0 12 * * 0,3"}
   ```
4. **ローカルlaunchd 頻度復元（通常期 2回/日）**:
   ```bash
   python3 -c "
   import plistlib
   p='/Users/kusakawatakuya/Library/LaunchAgents/com.kusagawa.drive-sync.plist'
   pl=plistlib.load(open(p,'rb'))
   pl['StartCalendarInterval']=[
     {'Hour':7,'Minute':0},{'Hour':22,'Minute':0}
   ]
   plistlib.dump(pl,open(p,'wb'))
   "
   launchctl unload ~/Library/LaunchAgents/com.kusagawa.drive-sync.plist 2>/dev/null
   launchctl load ~/Library/LaunchAgents/com.kusagawa.drive-sync.plist
   ```
5. `_council_mode.json` を更新（mode=normal, last_changed_at=now）
6. 草川に確認:
   ```
   ✅ 議会モード OFF（通常モードに復帰）
   - クラウドRoutine: 水・日21:00 JST
   - ローカルlaunchd: 7,22時の2回/日
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

---
name: council-mode-toggle
description: 議会期間中（3/6/9/12月の本会議・委員会開催月）であることを宣言する状態フラグ管理スキル。トリガー: 「議会モードon」「議会モードオン」「議会モード開始」「議会モードoff」「議会モードオフ」「議会モード解除」「議会モード状態」「議会モード確認」など。**v3 2026-05-28: Drive Desktop方式へ移行に伴い、launchd plist操作を撤回。Drive→Local同期は常時リアルタイムのため「頻度切替」は不要になった**。本スキルは `_council_mode.json` のflag管理＋クラウドRoutine cronの任意切替に縮小。ohayo/oyasumi/drive-intake等の他スキルがフラグを見て挙動調整する基盤として機能。
---

# 議会モード切替スキル（v3 簡素版）

## v2 → v3 で何が変わったか

| 観点 | v2（2026-05-21〜2026-05-28） | v3（2026-05-28〜） |
|---|---|---|
| ローカルlaunchd plist頻度切替 | 通常2回/日 ↔ 議会期4回/日 | **撤回**（Drive Desktopが常時リアルタイム同期） |
| クラウドRoutine cron切替 | 通常週2 ↔ 議会期毎日 | 任意（Routineが現存しているなら切替、なくてもOK） |
| `_council_mode.json` 状態管理 | 主要機能 | **継続**（他スキルが参照するflag） |

## 役割（v3）

「いま議会期間中ですよ」というフラグを管理する。これを見て他スキルが挙動を変える：
- **drive-intake**: 議会モードON時は `_INBOX_council/` の処理を優先
- **ohayo**: 議会期は朝ブリーフィングに「議会X日目／本日委員会あり」等を表示
- **oyasumi**: 議会期は議事録新着を優先サマリ
- **news-briefing**: 議会期は亀山市政・国政の議会関連ニュースを増量

## トリガー語

### ON切替
「議会モードon」「議会モードオン」「議会モード開始」「議会開始」「議会期間入り」

### OFF切替
「議会モードoff」「議会モードオフ」「議会モード解除」「議会終了」「議会期間終わり」

### 状態確認
「議会モード状態」「議会モード確認」「いま議会モード？」

---

## 状態ファイル

`~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_council_mode.json`:

```json
{
  "mode": "council" | "normal",
  "last_changed_at": "2026-06-01T09:00:00+09:00",
  "current_session": "2026.6",
  "history": [
    {"ts": "...", "mode": "council", "trigger": "草川: 議会モードon"}
  ]
}
```

`current_session` は議会期にON切替時に草川に確認（「6月議会で合ってる？」）。

---

## 実行ステップ

### A. ON切替時

1. `_council_mode.json` を読む
2. 既に `mode == "council"` なら「すでに議会モード中（X月議会期）」と返して終了
3. 草川に当該会期を確認：「2026年X月議会で合ってますか？」（カレンダー上の今月から推定）
4. `_council_mode.json` を更新:
   ```json
   {
     "mode": "council",
     "last_changed_at": "<now>",
     "current_session": "2026.X",
     "history": [..., {"ts": "<now>", "mode": "council", "trigger": "<trigger>"}]
   }
   ```
5. **（任意）クラウドRoutine cron切替**（Routineが存在するなら）:
   ```
   RemoteTrigger update
     trigger_id: trig_016r7yNKRqVubUvCJMTzVZ98  ※存在する場合のみ
     body: {"cron_expression": "0 12 * * *"}    毎日21時JST
   ```
   ※エラーは無視（Routineが廃止されていてもfail-safe）
6. 草川に報告:
   ```
   ✅ 議会モード ON
   会期: 2026.X月議会
   - フラグ: council=true
   - 他スキル（ohayo/oyasumi/drive-intake/news-briefing）が議会期挙動に切替
   - 議会終了時は「議会モードoff」と言ってください
   ```

### B. OFF切替時

1. `_council_mode.json` を読む
2. 既に `mode == "normal"` なら「すでに通常モード」と返す
3. `_council_mode.json` を更新（mode=normal、current_session=null）
4. **（任意）クラウドRoutine cron復元**:
   ```
   RemoteTrigger update
     trigger_id: trig_016r7yNKRqVubUvCJMTzVZ98
     body: {"cron_expression": "0 12 * * 0,3"}   水・日21時JST
   ```
5. 草川に報告:
   ```
   ✅ 議会モード OFF
   - フラグ: council=false
   - 他スキルが通常モード挙動に切替
   ```

### C. 状態確認時

`_council_mode.json` を読んで現在状態を表示:
```
📌 現在: 議会モード（2026.6月議会期）
   開始: 2026-06-01 09:00
   経過: 2日目
   - drive-intake: 議会資料優先処理中
   - ohayo: 議会期表示モード
```

または:
```
📌 現在: 通常モード
   直近の議会モード: 2026.3月議会（〜2026-03-25）
```

---

## v3で撤回した処理（実装しない）

- ❌ `~/Library/LaunchAgents/com.kusagawa.drive-sync.plist` の編集／load／unload
- ❌ `_drive_sync.sh` の頻度変更
- ❌ rclone関連の操作

これらはplistごと `~/Library/LaunchAgents/_deprecated_2026-05-28/` に退避済。
Drive Desktop（OS daemon）が常時リアルタイム同期しているため、頻度概念そのものが不要。

## 関連
- v3アーキ詳細: `~/.claude/projects/-Users-kusakawatakuya/memory/project_drive_structure_v3.md`
- 連動skill: drive-intake / ohayo / oyasumi / news-briefing
- 関連DB: 議会会期ハブDB（年4ページ・/general-question-prep で参照）

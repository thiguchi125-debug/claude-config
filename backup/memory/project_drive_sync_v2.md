---
name: Drive→ローカル同期v2拡張＋議会モード
description: 2026-05-05 v2拡張完了。Drive 3新フォルダ追加(_INBOX/ZZ_政策資料/ZZ_選挙関連)、Routine週2回(水日21時)＋議会モードcron切替、6カテゴリ自動分類、4階層取込先(01/02/05/06)対応
type: project
originSessionId: c51d25d3-bac9-4389-a011-c69108f135b0
---
# Drive→ローカル同期 v2拡張（2026-05-05）

## v1からの変更点

### Drive側
- 新フォルダ3つ追加:
  - `_INBOX_新規投函` (id: 1Cxn0oFSK7QnpWZN0QsQtd2D2OD_F9MMF) — 分類迷ったらここ
  - `ZZ_政策資料` (id: 1x-xtYw5vUEkIlUkduvpKsHp4XBdWqRtt) — 補正予算/要望書/調査
  - `ZZ_選挙関連` (id: 1RCb3IvMM4jvweaVrd_bdislG96WeykPL) — 公約/後援会/戸別訪問

### Routine変更
- cron: `0 12 * * 0` (週1日曜) → `0 12 * * 0,3` (**週2 水・日 21時JST**)
- スキャン対象: 15→**18フォルダ**
- 分類: 4カテゴリ → **6カテゴリ**（議事録/市政報告/印刷物/政策資料/選挙関連/未分類）
- 次回実行: 2026-05-06 21:00 JST (水曜)

### 議会モード
- 新スキル `council-mode-toggle`
- 「議会モードon」→ cron `0 12 * * *` (毎日21時JST)
- 「議会モードoff」→ cron `0 12 * * 0,3` (週2)
- 状態DB: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_council_mode.json`
- 想定運用: 3/6/9/12月の議会期に切替

### ローカル側拡張
- `_classify.py` v2: 6カテゴリ対応（議事録/市政報告/印刷物/選挙関連/政策資料/未分類）
- `drive-sync-review` スキル: 4階層取込先(01_council/02_publications/{reports,leaflets}/05_resources/06_election)対応
- 親フォルダヒント強化（PARENT_HINTS dict）

## 草川向け運用ルール（覚えるだけ）

| 何を | どこに投函 |
|---|---|
| 議会で配布された資料・議事録 | `R0X (年)` 等の年度フォルダ |
| 自分が作った市政報告レポート | `ZZ_市政報告レポート` |
| 行政・他団体からもらった政策資料 | `ZZ_政策資料` ★NEW |
| 選挙公約・後援会・戸別訪問関連 | `ZZ_選挙関連` ★NEW |
| **迷ったら全部** | **`_INBOX_新規投函`** ★NEW |

→ 月曜朝の ohayo が「先週N件投函されました」と教えてくれる
→ `/drive-sync-review` で「全部承認」と返すだけ
→ 自動でローカル kusagawa_archive/ に取込・grep対象化

## 議会モード切替

```
草川: 議会モードon
Claude: cron変更 → 毎日21時JST同期に切替
↓ 議会期はDrive投函翌日に学習層反映

議会終了後
草川: 議会モードoff
Claude: cron復旧 → 週2(水・日)21時JST
```

## モバイル運用
- iPhoneのDriveアプリで `_INBOX_新規投函` をホーム画面ショートカット登録
- LINE/メール添付PDF → 「ファイルに保存」→ Drive → `_INBOX_新規投函`
- 1タップで投函 → 翌週(or議会モード時は翌日)に自動同期

## How to apply
- 議会開催前に「議会モードon」と一言
- 議会閉会後に「議会モードoff」と一言
- 普段は何もしなくても水・日に自動同期＋月曜朝にohayoで通知
- 取り込みたくないファイル（テンプレ・草案・私的）はDriveに置かない or _personalフォルダなど別場所に

## 関連リソース
- Routine: trig_016r7yNKRqVubUvCJMTzVZ98 (https://claude.ai/code/routines/trig_016r7yNKRqVubUvCJMTzVZ98)
- Notion DB: ed2d5e6a-96f9-401f-a204-c3431602de41 (📥Drive取込キュー)
- ハブ: 356cf503-a68f-814c-9997-ef56a3cca376 (📚草川議会質問アーカイブDriveミラー)
- スキル: weekly-drive-sync / drive-sync-review / council-mode-toggle
- 状態DB: _sync_state.json / _council_mode.json (どちらも 99_raw/_scripts/)
- 分類スクリプト: 99_raw/_scripts/_classify.py (v2拡張済)

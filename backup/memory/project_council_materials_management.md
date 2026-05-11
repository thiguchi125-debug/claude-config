---
name: 議会資料管理システム (Phase 1〜4)
description: SideBooks→Drive→ローカル→agentの自動取込パイプライン。2026-05-11設計、Phase 1=Drive整理実行中
type: project
originSessionId: e2db6f87-82e3-41b5-8044-0bc246cee639
---
# 議会資料管理システム

## 概要
亀山市議会SideBooks経由で配信される議案書・委員会資料・行政報告等を、草川操作2ステップでDrive→ローカル→agentまで自動連携させるシステム。

**Why:** SideBooks単独運用＋NotebookLM単独だとClaude Code側のagent群（agenda-analyzer・counter-argument-simulator・policy-archive-miner）から不可視。今後資料が大量化するため、議案カルテ自動生成・答弁シミュレーション・過去発言連動の全てを腐らせない設計が必要。

**How to apply:**
- 議会資料の取扱いに関する質問は本systemの設計に従う
- 新規議会資料は `_INBOX_新規投函/_council_pending/` に投函するルール
- Phase 1 終了後、Phase 2（スクリプト拡張）に進む

## 設計書
- `/Users/kusakawatakuya/.claude/projects/-Users-kusakawatakuya/specs/2026-05-11-council-materials-management-design.md`

## Drive新規フォルダID一覧（2026-05-11作成済）
- `_INBOX_新規投函/_council_pending/`: 1Uk2yabgrJCz56KQP1i2AThGTAMGKKh-l
- `R08(2026)/03_定例会/`: 1dhjjQoF_IUUe6jNUGoqqsOWh_t7niKuk
  - `議案書/`: 1-_1Ew1OmCYPOM7lS7ddWty-tG0QI8blV
  - `委員会資料/`: 1TRW2gfX3jWCqguu_LBP_-buf9jHVAaFS
  - `行政報告/`: 139u0DzNQYI6ZQTfulvGOjeWwDXuGoxHe
  - `議事録/`: 1VBAQkbsLMIjesYGzk6Y6v6PnHEY5_Akt
  - `草川質問/`: 1uruyEpOcrjrssiEELllMOtC1P-K0ywTM
- `R08(2026)/06_定例会/`: 1HUSuEGbsqN5qbZfH-Nrw3zk6CdnipiLj
- `R08(2026)/09_定例会/`: 1f6YgQF8xExh59AHb0VEyRdVc2bNh1zvx
- `R08(2026)/12_定例会/`: 1W55GUdPlrcDKwfB_pV9LD-bveHVYDtjf
- `R08(2026)/委員会・全協（会期外）/`: 14vqekEfrMJGBnV0W9chRZFtUzCVyhZAa

## 草川手動アクション保留中（Phase 1完了に必要）
1. 空フォルダ削除 8件（ZZ_政策資料 + 99_archive_unused配下6件+親）
2. `議事録（年度別）` → `議会記録（年度別）` リネーム
3. 保存先ガイドmd 2件をDriveに手動アップロード
   - ローカル `~/.claude/projects/-Users-kusakawatakuya/specs/_drive_upload/` 配下に用意済

## Phase 進捗
- Phase 1（フォルダ整理）: Drive新規フォルダ作成完了、手動アクション待ち
- Phase 2（スクリプト拡張）: 未着手
- Phase 3（agent連携）: 未着手
- Phase 4（運用開始=R08-06定例会）: 未着手

## NotebookLM並行運用
- Drive=主、NotebookLM=議会期だけ補助
- 議会期前夜に草川がNotebookLMにも別途ドラッグ投函（5〜10分）

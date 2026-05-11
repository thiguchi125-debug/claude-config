---
name: マイドライブ全件取込v1
description: 2026-05-05実施。Driveの「草川たくや 議会質問アーカイブ」以外のマイドライブ全体306ファイルから255件を議員業務関連として取込候補化、108件取込済（残147件は4pm JST resume）
type: project
originSessionId: c51d25d3-bac9-4389-a011-c69108f135b0
---
# マイドライブ全件取込v1（2026-05-05）

## 背景
これまで「草川たくや 議会質問アーカイブ」 (1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg) のみ取込していたが、マイドライブのルートや「過去資料」「001 政策・政治活動」「002 議会」「003 ビジネス」「スキャン」「共有用フォルダ」配下にも議員業務資料が大量に散在していた。

## Discovery結果
- スキャン総数: 306件
- 取込候補（include=true）: 255件
- 除外: 49件（写真/動画/音声/sheet/form/プライベート）

カテゴリ分布:
- 01_council: 70件
- 02_publications/reports: 3件
- 02_publications/leaflets: 2件
- 05_resources: 120件
- 06_election: 1件
- pending（草川判定待ち）: 59件

スキップ:
- パラ陸上、くすのき会、JC、亀山JC、サッカー大会、eスポーツ大会、フォートナイト、コーチング系
- Chrome から保存（webクリップ）×2

## 取込進捗
- バッチ1（63件）: ✅ 完了（成功63/63、大型6件は要約＋フルコピー両方保存）
- バッチ2（64件）: ⏸ partial（71 tool_uses進行 → rate limit）
- バッチ3（64件）: ⏸ partial（59 tool_uses進行 → rate limit）
- バッチ4（64件）: ⏸ partial（28 tool_uses進行 → rate limit）

**実取込件数: 108件**（mydrive_接頭辞）→ **学習層 1117 → 1194件 (+77件本体)**

カテゴリ別追加:
- 01_council/: +27 (166→195)
- 02_publications/leaflets/: +2 (110→112)
- 05_resources/: +47 (577→624)
- 99_raw/_pending_review/: +32 (1→33)

## Resume計画
- subagent rate limit reset: 2026-05-05 16:00 JST
- 残り147件: agentId経由でSendMessageでresume
  - バッチ2 agentId: a6cc13b8429ee9a2d
  - バッチ3 agentId: a086e8886c411d27f
  - バッチ4 agentId: a3cc8b894ba334a84

## 関連ファイル
- 取込候補リスト: `/tmp/mydrive_candidates.json` (131KB, 255件)
- 4分割: `/tmp/mydrive_batch_{1,2,3,4}.json` (各63-64件)
- 取込ファイル接頭辞: `mydrive_<sanitized_title>_<id下5-6桁>.txt`

## マイドライブ整理（草川手動・MCP不可）
チートシートに手順書追加: <https://www.notion.so/356cf503a68f81da9022ccf90e8242fa>
- 過去資料/001/002/003/スキャン/共有用フォルダ → 「草川たくや 議会質問アーカイブ」配下に統合
- パラ陸上/くすのき会/Chrome保存×2 → 99_archive_unused/
- ルート直下の散在ファイル → _INBOX_新規投函/
- 重複ファイル削除

## How to apply
- 残り147件取込後、INDEX.md/CLAUDE.md件数更新
- 草川手動整理後はマイドライブのRoot直下に「議会質問アーカイブ」だけ残る理想形
- 今後の新規ファイルはRoutine（毎週水・日）が自動同期

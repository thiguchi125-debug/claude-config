---
name: 草川議会質問アーカイブ Drive 参照ルート
description: 草川たくやの議事録（年度別）・市政報告レポート・委員会記録・印刷物原稿が一次資料として集約されたGoogle Driveルートフォルダと、ローカル整理済みアーカイブとの対応関係
type: reference
originSessionId: c51d25d3-bac9-4389-a011-c69108f135b0
---
# 草川たくや 議会質問アーカイブ — Drive参照マップ

## 1. Drive ルート（一次資料・raw保管）
- URL: https://drive.google.com/drive/folders/1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg
- folder_id: `1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg`
- 役割: 草川8年分の議事録PDF・委員会記録・市政報告レポート全号・公式OneDrive・音声記録の**一次資料サイロ**
- ユーザー指定: **草川の制作物・考え方・実績を扱う全タスクで常時参照対象**

## 2. 主要サブフォルダ（17件）
| folder | id | 中身 |
|---|---|---|
| 00_INDEX | 1e6688SA8JVeu8dEMHO5Tqw5OgiFcGeZJ | 完了報告書v1（メタ） |
| H30 (2018-12〜2019-2) | 1oQxIunn3nB4vMJQdEzYcFZZgk5N1d2rP | 初当選〜H30年度議事録 |
| R01 (2019) | 1i1Ds5RkCJbt0Y7X2onRuFq6QfXvjq1kp | 議事録PDF |
| R02 (2020) | 1pvIuV4a6id8_G_uNsOS0B2DOjYcD6kB7 | 議事録PDF |
| R03 (2021) | 12ihONYcNTlDRxDqw8SEYsNs_zoLNGs9A | 議事録PDF |
| R04 (2022) | 1_vNgDKDkLiF2qL-ClYFArbzhk-vYLFQI | 議事録PDF |
| R05 (2023) | 1Jn5Y_zwqlNkH8Mo5QwblMBkPBx2i1ojd | R0503/06/09/12 kaigiroku.pdf |
| R06 (2024) | 1KpNNJi5hJPeVm6ICb3iMqYL9yDH22pxH | 議事録PDF |
| R07 (2025) | 1GyCICnLFokDzl6ZK53ztCl3zcgfEV-mW | 議事録PDF |
| R08 (2026) | 1VttHwAVtaTgHT6gj1AEmYk_ZoZ9XTmLx | 3月議事録docx・予算決算委員会txt |
| ZZ_様式テンプレート | 1YBN6IR_3NUI_lmFW2CtAsCG67E4RBnj7 | 議員業務テンプレ |
| ZZ_政策別深掘り資料 | 1RkDuAFY64-VgVDO43IHNo8_eurLtBi5T | テーマ別資料 |
| ZZ_委員会・地域議事録 | 1iIAsrd0LCS9IZ2p2hSEC6VogcPfutrX5 | 委員会・地域別 |
| ZZ_市政報告レポート | 1bhtxwXuGeMi-Y5NNlF6SPE_UQ_65Eqqz | 38〜62号＋地区版（昼生/二本松/南部/東部/けんろう/みずきが丘/菅内 等） |
| ZZ_議会事務局公式OneDrive | 1VX_WYfMELB26UOwcvQ9nzQGfgjxweiLZ | 公式版議事録 |
| ZZ_ブログSNS全アーカイブ | 1mNHzaHx9CxrDAHyMnq3K5EBqMRrTM4au | ブログ・SNS過去全件 |
| 99_音声記録 | 1eDFCCgbbTPe3r4GJ-shBaIvPe70ZbTno | 街頭演説・委員会音源等 |

## 3. ローカル整理済みアーカイブ（高速参照層）
場所: `~/.claude/agents/knowledge/kusagawa_archive/`
- `transcripts/` 議事録テキスト45件 + `_council_search_index.md`（H30〜R7全47エントリ索引）
- `blog_full/` ブログ全文53件（2021-10〜2026-05）
- `canva/` 印刷物107件（市政報告レポート1〜39号 + 応援カード/産後ケア/市政報告会）
- `themes/` テーマ別蒸留11件（子育て教育・防災・福祉・DX・まちづくり経済・環境・観光・議会改革）
- `3pillars/` 政策3本柱草案
- `voice-dna.md` / `policy_compass.md` / `MISSION_REPORT.md` / `manuscripts_inventory.md`

## 4. 参照ハンドリング規約
- **第一手は必ずローカル**: `grep -l "<キーワード>" ~/.claude/agents/knowledge/kusagawa_archive/transcripts/*.txt` および `themes/`・`blog_full/`・`canva/` を検索。テキスト化済なので高速・安価。
- **Drive は補完源**: ローカルに存在しない年度・号数（例: 市政報告レポート40〜62号、R08最新議事録、地区版PDF）が必要な場合のみ Drive MCP `search_files` / `read_file_content` で取得。
- **ローカル不足発見時**: 取得したDrive資料を `~/Documents/市議会・政策/<年>/` 等に保存し、`canva_to_text.sh` または手動で `kusagawa_archive/` 配下にテキスト化追加。
- **エージェント連動**: blog-writer / council-material-creator / sns-content-creator / speech-writer / policy-archive-miner / policy-comparison-benchmarker / agenda-analyzer は原稿生成前にローカル grep を実施。

## 5. How to apply
- ブログ・SNS・議会質問・スピーチ・印刷物・政策提案を生成する**全タスク**で、トピックに関連する草川過去発言を最低1件は確認してから書き始める。
- 「過去にこう言っている」という連続性を担保することで、voice-dna整合性とファクトチェック耐性が同時に上がる。
- 草川自身の実績を語る場面（市政報告会・街頭演説・選挙パンフ）では、年月＋セッション名＋論点を具体名で引用する。

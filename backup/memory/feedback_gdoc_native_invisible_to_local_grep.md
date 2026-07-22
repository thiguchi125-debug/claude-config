---
name: feedback-gdoc-native-invisible-to-local-grep
description: Googleドキュメント/スプレッドシート形式のDriveファイルはローカルミラーに実体が落ちず_indexにも乗らないため「存在しない」と誤断定しやすい
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 62064658-aa7b-493e-9065-0886c82e1334
  modified: 2026-07-22T14:25:35.232Z
---

Drive上のネイティブGoogle形式ファイル（Googleドキュメント/スプレッドシート/スライド）は、Google Drive Desktopのローカルミラーには `.gdoc` / `.gsheet` の**ショートカットしか落ちない**。中身がないので `pdftotext` も効かず、日次パイプラインの `_index/` txtキャッシュにも乗らない。結果、`grep` や `find -iname "*.docx"` 系の探索では**完全に不可視**になる。

**Why:** 2026-07-22、草川から「三重大学応援団のR8コーチング一覧を探して」と言われ、ローカルミラーのfind/grepだけを見て「令和7年度・8年度版は存在しません」と断定した。実際には `20260311更新 R8コーチングスタッフ体制`（Googleドキュメント）がDrive上に存在。草川に「絶対にあるR8」と押し返されて発覚した。ローカル一次探索の原則（CLAUDE.md）は正しいが、**ローカルに無い＝存在しない、ではない**。

**How to apply:**
- ローカルgrep/findで見つからなかったとき、「存在しない」と断定する前に **必ず Drive MCP `search_files` でサーバ側検索**を1回かける（`title contains '...'` / `fullText contains '...'`）。ネイティブGoogle形式はここでしか引っかからない。
- 「無い」と報告してよいのは Drive MCP 検索も空振りしたときだけ。
- 探索は `.gdoc` / `.gsheet` / `.gslides` の**ファイル名だけは**ローカルに見えるので、`find ... -name "*.gdoc"` も併用すると早い。
- 保存場所の誤配置も同時に疑う。上記R8は `日常資料アーカイブ/03_後援会・組織/亀山JC/` に紛れていた（正＝`99_その他/個人/三重大応援団/コーチング/※随時更新データ/`）。
- 関連: [[reference_storage_map]] [[reference_drive_archive_kusagawa]]

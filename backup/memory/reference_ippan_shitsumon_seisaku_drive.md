---
name: reference-ippan-shitsumon-seisaku-drive
description: 一般質問の制作物（通告書・写真・完成品）のDrive保存先。general-question-prep draft/写真保存時に必ずここを使う
metadata: 
  node_type: memory
  type: reference
  originSessionId: 680d5cea-9435-4725-9e51-9c541f5ef017
---

一般質問の**制作物**（草川が作るもの）の保存先＝Drive `草川たくや 議会質問アーカイブ/ZZ_一般質問制作/`（2026-06-02新設）。制作物は既存の`ZZ_`接頭辞慣例（ZZ_市政報告レポート／ZZ_選挙関連）に統一。

**役割分担（混ぜない）:**
- `議会資料アーカイブ/` ＝ 市から受け取る**一次資料**（議案書・現況報告・議事録）。`_index`grep対象
- `ZZ_一般質問制作/` ＝ 草川が作る**制作物**。grep対象外（voice-dna汚染・議事録誤抽出を防ぐ）
- ローカル `~/.claude/projects/-Users-kusakawatakuya/drafts/` ＝ AI下書きのscratch（トークン節約）。**確定版・写真・完成品はDriveへ集約**

**会期別構造:** `ZZ_一般質問制作/R0X (年)/YYYY-MM_◯月議会/` 配下に `01_通告書/` `02_原稿_想定答弁/` `03_提出素材_写真/`（iPhone投函）`04_完成品/`。横断参照用に `_過去通告書ライブラリ/`、`_テンプレート/`、`README_使い方.md`。

**Notionとの連携:** 段取り・進捗・想定答弁＝🏛議会会期ハブDB（[[feedback-council-session-hub-db]]）／実ファイル＝このDriveフォルダ。会期ハブページに保存先パスを追記する運用。

CloudStorage実体: `~/Library/CloudStorage/GoogleDrive-t.higuchi125@gmail.com/マイドライブ/草川たくや 議会質問アーカイブ/ZZ_一般質問制作/`

---
name: project-photo-stock-system
description: Pixel写真→使える写真ストックの月次システム。Googleフォトのアルバム「📷議員活動」1タップ選別＋Claude月一回収（Chrome）→Drive 📷写真ストック整理・台帳化
metadata: 
  node_type: memory
  type: project
  originSessionId: ecc2e32a-ab13-4228-a7cc-45223df3b365
---

# 📷写真ストックシステム（2026-07-08設計・草川承認・初期構築完了）

## 背景
草川のメイン機がGoogle Pixelになり、写真がMac（Photos.app顔DB＝photo-curatorの検索源）に自動で入らなくなった。2026-07-07の市政報告レポート制作で「議場カットが無い・プロフィール写真に皿が写る」等の在庫問題が表面化。
**GoogleフォトとDriveは別物（2019年分離）**・Googleフォト全ライブラリの自動読み出しAPIは2025-03廃止→自動直行ルートなし。容量負担を避けるため全自動同期は不採用（草川判断）、**選別式**で確定。

## 確定した仕組み（正本= Drive `📷写真ストック/README.md`）
1. 草川: Googleフォトで良いカットをアルバム**「📷議員活動」**に追加（2タップ・これだけ）
2. Claude: 月一トリガー**「写真ストック整理して」**で Claude in Chrome→photos.google.comの当該アルバム→前回以降の新着DL（`_state.json`に回収日記録）→`90_原本_月別/`保存→目利きして`10_使える写真/01人物単独〜05季節もの/`へ選抜→`_build_catalog.py`でcatalog.html更新→`_wishlist.md`照合で「今月撮ってほしいカット」を返す→nichijo1行
3. フォールバック: Googleフォト共有→ドライブ→`00_受信箱/`手動投函

## 選抜ルール（README詳細）
第三者の顔特定可はフラグ／家族写真は選抜しない／選挙たすき写真は公選法別扱い／スクショ・書類は原本にも入れない

## 状態
- [x] Drive `📷写真ストック/` フォルダ構成・README・wishlist・catalogスクリプト（2026-07-08）
- [x] 初期在庫5枚（市政報告試作の目利き済み分: スーツ2/里山ぼかし済/米づくり/収穫イベント）
- [ ] **草川の手番: Googleフォトにアルバム「📷議員活動」を作成**（未作成だと回収が空振り）
- [ ] 初回回収の実走（アルバムに数枚入った頃に「写真ストック整理して」）
- ウィッシュリスト最優先: 議場・委員会カット（議会事務局への撮影依頼検討）・皿なしスーツ正面・市民対話構図

関連: [[feedback_system_closing_loops_rot]]（月初リマインドはohayoシグナルに載せ記憶依存を排除）[[project_design_studio]]

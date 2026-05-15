---
name: auto-open-pdf-after-render
description: "印刷物PDFを生成・更新した直後は確認ダイアログ不要で自動 `open` する"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 24051382-f665-4b45-ba81-4ec4e97a25e7
---

印刷物（チラシ・市政報告・応援カード・名刺・ハガキDM・パンフレット等）のPDFを `--print-to-pdf` で**生成または更新した直後**は、ユーザーに確認やコピペコマンドを促さず、即座に `Bash: open <PDF絶対パス>` で macOS プレビュー.app を起動する。

**Why:** 草川は毎回PDFを目視確認したい。コマンドをコピペで案内するのは二度手間で、`open`は完全に reversible（プレビュー.appが開くだけ・ファイル改変なし）なのでリスクなし。2026-05-15 v2チラシ作業時に「自動で表示してくれない？」と直接指示を受けた。

**How to apply:**
- HTMLをEdit/Write後、Chrome headlessでPDF再生成→**直後**に `open "<PDFパス>"` を実行
- プレビューPNG生成（sips）したらPDFも同時にopenする（PNGはチャット表示用、PDFは草川の目視用）
- 既にプレビュー.appで同名PDFが開いている場合、`open`が前面に持ってくる挙動（再リロード）でOK
- 「ファイル準備完了。確認してください」のテキスト案内のみで、コピペ用openコマンドは出さない（同じものを2回見せない）
- 写真・画像（PNG/JPEG）の最終成果物も同様に自動open対象
- ただし**HTMLは自動openしない**（ブラウザは草川の作業用途で別タブが多く、勝手に開かれると邪魔）

**Scope:**
- 印刷物（チラシ／市政報告／応援カード／名刺等）の最終PDF
- 印刷物の途中バージョン（v1/v2/v3）も同様
- design-director / natural-design-reviewer の review対象画像も自動open可

**Do not auto-open:**
- HTML（草川のブラウザ作業を妨げる）
- 中間生成物（/tmp配下のpreview PNG等、チャット表示で済む場合）
- 大量ファイル（5件以上同時open）
- Notion ページ（既に確認可能なため）

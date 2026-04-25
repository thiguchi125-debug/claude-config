---
name: 印刷物デザイン2エージェント新設
description: 2026-04-25新設。print-designer（HTML/CSS→PDF印刷物専任）とphoto-curator（Photos.appベストショット選定）。応援カードv7の作業ノウハウを再利用化
type: project
originSessionId: 117eaaff-c146-4719-8294-a6baba4be080
---
2026-04-25、応援カード作成（v1〜v7）の作業フローをエージェント化。

**1. print-designer**
- 用途: 応援カード／名刺／リーフレット／A4チラシ／A3ポスター／ハガキDM／パンフレット／議会報告書
- パイプライン: HTML/CSS → Chrome headless `--print-to-pdf` → PDF
- 知識: A4/A3/B5規格・余白・塗り足し、日本語タイポグラフィ、緑×金ブランドパレット、写真クロップbest practice
- 制約: **赤色を草川向けに使わない**（ユーザー明示指示）、絵文字も使わない

**2. photo-curator**
- 用途: 草川卓也の最適写真をPhotos.appから抽出
- 草川卓也のZPERSON Z_PK = **18** (約6,242枚顔認識済)
- 既知の罠: EXIF orientationのdrop（sips変換後にRead必須）、iCloud-only file検出、photo bursts偽多様性、ZHEADGEARTYPE=4はヘルメット
- 用途別フィルタレシピ内蔵（応援カード/SNS/街頭演説/会議録）
- ファイル名検索: `ZADDITIONALASSETATTRIBUTES.ZORIGINALFILENAME LIKE 'IMG_xxxx%'`

**Why**: 同種の作業（次の選挙ポスター、議会報告リーフレット、新名刺等）で毎回同じ調査・試行錯誤を繰り返さないため。今回のv1〜v7の修正履歴に詰まったノウハウ（横長/縦長クロップ、緑×金パレット、A4ページ収まり調整、改ページ制御、向き補正）を恒久知識化。

**How to apply**: 
- 草川向けの印刷物作成依頼 → print-designerを起動
- 写真選定依頼（特に「ベスト5枚」「IMG_xxxx使いたい」「印象の良い1枚」）→ photo-curatorを起動
- 両者は連携前提（photo-curator → print-designer の流れ）
- 元になった応援カードPDF最新版: `~/Desktop/草川たくや応援カード_写真候補/草川たくや応援カード_改善版v7.pdf`
- HTMLソース: `/tmp/ouen_card_template.html`

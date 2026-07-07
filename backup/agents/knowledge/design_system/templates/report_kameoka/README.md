# report_kameoka — 市政報告レポートA4両面（かめおか型・**市政報告の正テンプレ**）

> 種: 2026-07-08 市政報告レポート2026夏号v2。**草川本人が広報かめおか見開きをベンチマーク指定**して組んだプロ水準版。
> 前身の西宮型Q&Aカード（report_qa_cards）は「素人以下のAI臭さ」で却下→削除済み。
> **設計の正本 = `design_spec.md`（design-director策定・実装前必読）**。却下理由5点（箱の集合/ベタ帯反復/単一ゴシック/均等グリッド/純白+中央寄せ）＝絶対に繰り返さない。

## 背骨
罫線囲みゼロ・ベタ帯ゼロ。分節は①余白 ②淡ウォッシュ（緑8%/金10%） ③ヘアライン1本 ④明朝見出し、の4手段のみ。
warm paper #fbfaf6／緑#1f5a3a系×金#c89211／明朝（タイトル）×ゴシック（本文）でジャンプ率4倍以上。
意匠は1点ずつ: 手書き風キャッチ=表1点（顔・襟に重ねない）／円形ヌメラル=裏1点／縦組み=編集後記1点。

## ファイル
- `template_omote.html` / `template_ura.html` — 正本（placeholder方式: `__H2__` `__A1__` `__QR_IKEN__` `__QR_LINE__`）
- `build.py` — placeholder→base64埋込finalの再構築スクリプト
- `design_spec.md` — グリッド（216×303mm塗り足し込み・12col・4mmベースライン）・タイポ級数・AI臭チェックリスト14項
- `preview.html` — claude.ai/designカード用縮図

## 制作手順・検証
1. 写真はPILプリクロップ（背景の第三者はGaussianBlur+フェザーマスクでぼかす）
2. レンダ816×1145px→PNG自Read検品→pro参照（`…試作/references_pro/pro1,pro2`）と並べて自己判定
3. QR検証は `--force-device-scale-factor=3以上` の高解像度側で（74dpi相当だと長URLは読めない＝正常）
4. 安全ゲート（fact-checker→risk-reviewer）・natural-design-reviewer 2周は毎回必須

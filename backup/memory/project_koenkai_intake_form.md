---
name: project_koenkai_intake_form
description: 後援会入会フォームシステム（URL1本で募集→名簿CSV→Substack CSV取込→LINE誘導→紹介連鎖）。週次バッチ「後援会取り込み」の正本手順はDrive README
metadata: 
  node_type: memory
  type: project
  originSessionId: 9f3b9230-cabd-4f20-86e7-91633e7895c6
---

# 後援会入会フォームシステム（2026-07-14稼働）

URL1本（メール/LINE/SNS/QR配布）で後援会入会を受付。Googleフォーム（10設問・GAS自動生成）→GAS自動返信メール（LINE誘導＋転送用紹介テンプレ＝紹介連鎖の起点）→名簿マスタCSV→週1でSubstack CSVインポート（2クリック）。

- **運用README（正本・URL一覧と週次手順）**: ミラー `日常資料アーカイブ/06_フォーム・アンケート運用/後援会入会フォーム/README.md`
- **公開URL**: https://docs.google.com/forms/d/e/1FAIpQLSe1ABf6mhOcDMFQGPR9VviZSEpstd87mu6MqOzoCOvzzTFdgQ/viewform
- **名簿マスタ**: ミラー `日常資料アーカイブ/00_名簿・個人情報/後援会名簿マスタ.csv`（13列・grepインデックス対象外区画）
- **トリガー「後援会取り込み」**（毎週月曜・Todoist繰り返しタスクがohayoに出す）: README手順1〜10を実行。積み残しチェック→新着→重複/地区判定→CSV追記→協力申出の提示→Substack用import.csv→Todoist締めタスク→「インポートした」で消込
- **設計書・GAS正本**: `~/publications/2026-07_後援会入会フォーム/`（design.md / plan.md / gas_combined_v3.js）／文言正本: drafts/2026-07-14_後援会フォーム文言_v1.md（v2変更節が最新）
- **Notion後援会員DB(04cc3a1c)には登録しない**（VIP・特別打診用）。一般会員はCSVが正本。
- 安全ゲート通過済（fact-check/risk-review 2回・差分APPROVE）。**告示後(2026-10-18〜)の拡散停止テーブルがREADMEにある**——P3期に入ったら必ず参照。
- ⚠️教訓: GAS認可の「権限を選択」画面でGmail送信チェックが外れたまま許可→自動返信不達が発生。GAS再認可時はスコープ全チェックを確認。

関連: [[project_2026senkyo_visit]] [[feedback_system_closing_loops_rot]]

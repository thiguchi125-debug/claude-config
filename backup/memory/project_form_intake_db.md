---
name: フォーム受付市民意見DB（GAS連携）
description: Google Form→Notion自動連携用の独立DB。📝市民意見リストとは分離し、トリアージ後に手動転記する2段構成
type: project
originSessionId: a0710bec-7974-4709-9b54-efa645d1fe61
---
2026-04-30新設。Google Formからの市民意見をGASスクリプトで自動受信するための専用DB。

**DB情報:**
- 名称: 📋 フォーム受付市民意見
- 親ページ: 市民からの意見まとめ (ec4c8e95-6fe7-4a51-8ecb-393f893a8fde)
- Database ID: 70eeaeab-e7e2-4659-9e0e-7d5f8fef88c6
- Data Source ID: collection://354432ec-6c3a-4a71-b649-ce53c6b74427
- URL: https://app.notion.com/p/70eeaeabe7e246599e0e7d5f8fef88c6

**主要プロパティ:**
- 件名(title) / 受付日時(date) / 氏名 / 連絡先 / 回答者メール(email)
- 地区(select: 亀山市9地区+市外+未記入) / カテゴリ(multi_select: 既存DBと同色9種)
- 緊急度(select: 高中低) / 意見内容 / 対応状況(status)
- 対応メモ / 次アクション / 担当課 / 期限
- 既存リストへ移管(checkbox) / フォーム送信ID(重複防止) / 受付ID(CV-N自動採番)

**Why:** 既存📝市民意見リスト(c2c34bd8-)に直接フォーム自動投入すると、人手追加分とフォーム生データが混ざってトリアージしづらい。受信専用DBで一旦受け止め、重要案件のみ📝市民意見リストへ昇格させる2段構成にした

**How to apply:**
- Google Form新規作成→GASでonFormSubmit→このDBへinsert
- 緊急/重要案件のみ📝市民意見リストへ手動転記し「既存リストへ移管」をON
- citizen-inquiry-responderエージェントは📝市民意見リスト側を参照（既存ワークフロー維持）
- フォームURL/質問項目が確定したら GAS雛形(2026-04-30会話参照) のフィールドマッピングを実物合わせ

---
name: 市民意見受付BOX & ikenスキル
description: 全チャネル受信用の市民意見intake DB（📋市民意見受付BOX）＋ikenスキル。コピペ起動で記録＋返信3案＋次アクション抽出を一気通貫
type: project
originSessionId: a0710bec-7974-4709-9b54-efa645d1fe61
---
2026-04-30新設。Google Form/メール/SNS DM/LINE/電話/窓口/手紙等あらゆるチャネルから届いた市民意見を、ユーザーがコピペ起動で受付する手動ハイブリッド運用。GAS自動連携は不採用（Integration設定の手間で諦め）。

**DB情報:**
- 名称: 📋 市民意見受付BOX（旧「📋フォーム受付市民意見」を改名）
- 親ページ: 市民からの意見まとめ (ec4c8e95-6fe7-4a51-8ecb-393f893a8fde)
- Database ID: 70eeaeab-e7e2-4659-9e0e-7d5f8fef88c6
- Data Source ID: collection://354432ec-6c3a-4a71-b649-ce53c6b74427
- URL: https://app.notion.com/p/70eeaeabe7e246599e0e7d5f8fef88c6

**主要プロパティ:**
- 件名(title) / 受付日時(datetime) / 氏名 / 連絡先 / 回答者メール
- 経路(select: フォーム/メール/SNS DM/LINE/電話/窓口/手紙/口頭/その他) ※2026-04-30追加
- 地区(select: 亀山9地区+市外+未記入) / カテゴリ(multi_select 9種)
- 緊急度(select: 高中低) / 意見内容 / 対応状況(status: 未着手/進行中/完了)
- 対応メモ / 次アクション / 担当課 / 期限
- 既存リストへ移管(checkbox) / フォーム送信ID / 受付ID(CV-N自動採番)

**ikenスキル:**
- 場所: ~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/iken/SKILL.md
- バックアップ: ~/claude-config/backup/skills/skills/iken/SKILL.md
- トリガー: 「意見届いた」「意見コピペ」「市民から意見」「フォーム回答届いた」「DMで意見」「LINE意見」等。**「記録」ワード単体は使わない**（nichijo衝突回避）
- フロー: コピペ受領→経路推定→📋受付BOX保存→返信3案生成（共感型/行動宣言型/コンパクト型）→次アクションをタスクDB登録候補提示→深掘り依頼があればpolicy-researcher呼び出し

**2段運用:**
- 📋受付BOX(354432ec-)= intake、全意見を一旦受け止め
- 📝市民意見リスト(c2c34bd8-)= 草川が責任もって対応する重要案件のみ手動転記
- 転記時は📋側「既存リストへ移管」チェックON

**Why:** GAS+Notion Integration設定が手間で自動化を諦め。代わりにコピペ起動スキルで秘書的に処理する手動ハイブリッド運用に切替。citizen-inquiry-responderエージェント（📝側保存）と棲み分け：受信窓口=ikenスキル、重要案件深掘り=citizen-inquiry-responder

**How to apply:**
- 市民意見が届いたらユーザーがチャットへコピペ
- 「意見届いた」「意見コピペ」等の発言で発火
- 返信3案から選んでユーザーが手動送信
- 重要案件は手動で📝市民意見リストへ昇格

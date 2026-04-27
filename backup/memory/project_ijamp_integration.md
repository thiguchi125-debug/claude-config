---
name: iJAMP連携(news-briefing統合)
description: 時事通信社iJAMPの配信メール5系統をGmail MCP経由でnews-briefingスキルに統合。著作権制約あり
type: project
originSessionId: 965b4e55-9c0d-4183-a66e-e65d5965df6b
---
2026-04-27実装。iJAMP（時事通信社の自治体専門情報サービス、有料法人契約・草川さん利用者ID:5080460002・5/1から本格運用）の朝の情報源として、配信メール5系統をGmail MCP経由でnews-briefingスキルに統合した。

**Why**: 当初Playwrightで自動ログイン取得を計画したが、(1)有料B2Bサービスは利用規約で自動取得禁止が業界標準、(2)違反時はアカウント停止・契約拒否・損害賠償リスク、(3)iJAMP公式が既に5系統のメール配信を提供しており既に草川さんGmailに大量蓄積中、を発見。Gmail経由なら「自分宛メールの自己利用」で規約違反ゼロ。

**How to apply**:
- news-briefingスキル（~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/news-briefing/SKILL.md）の カテゴリ⑦ にiJAMP取り扱いを集約
- 取得: `from:ijamp.jiji.com newer_than:1d` でGmail検索→get_threadで本文取得（FULL_CONTENT）
- 5系統: 官庁速報(kansoku@ 7:42配信)、お昼便(noon-news@ 11:30)、夕方便(evening-news@ 16:30)、部長注目(leaders@ 火金10:00)、速報(flash@ 不定期)
- パース: ◎=メイン記事/★=アンテナ/◇=中央官庁だより/《市政コーナー》=他自治体事例(議会質問の宝庫)/《町村スポット》《デジタルＴＯＤＡＹ》。各記事直下のhttps://www.ijamp.jiji.com/apps/c/kiji/view?mkijiId=...がURL
- **著作権厳守（運用ルール 2026-04-27 補正版）**: メール本文に「無断転載禁止」明記。
  - **原文転載・コピペ・長文引用はNG**（ブログ/SNS含む全媒体）
  - **要約をネタ抽出素材として活用するのはOK**（nichijoコンテンツ抽出モード等）。テーマとして取り上げる場合は草川自身の言葉でリライトし、出典は「時事通信社の報道によると」程度の短い言及にとどめる
  - 議会で言及時は出典明記必須
  - Notion📰DB保存時は概要冒頭に`【iJAMP配信／🔒内部閲覧専用】`を必ず付ける、stdout表示にも「🔒内部閲覧専用：転載禁止」マーカー
- 朝6:00時点で取れるのは前日24時間分（当日官庁速報7:42配信のため）。
- 残課題: Notion📰DBの`情報源`selectに「iJAMP」追加（現状は「その他」+概要冒頭マーカーで運用）

---
name: project-desktop-briefing-deprecation
description: 旧ローカル版デイリーブリーフィング（~/.kameyama-briefing/daily_briefing.py + launchd）を2026-05-12に廃止。news-briefing skill＋ohayoに一本化
metadata: 
  node_type: memory
  type: project
  originSessionId: b6611fd7-7741-4af0-80c5-3aa62944b416
---

# Desktopブリーフィング廃止メモ（2026-05-12）

## 決定事項
旧ローカル自動化（`~/.kameyama-briefing/daily_briefing.py` + launchd `com.kameyama.briefing` 毎朝6:00起動 → `~/Desktop/ブリーフィング/<日付>_ブリーフィング.html`）を**廃止**。

**Why:** 
- 一般質問チェックが `generate_question_ideas()` のテンプレ自動生成で、背景文も `KAMEYAMA_CONTEXT[area]["background"]` を全記事に貼付する設計のため**毎日同一の使い物にならない内容**を量産していた
- 件数制限なし（要チェック13・確認推奨13・関連ニュース174）で意思決定ノイズ
- ohayo skill とは一切連携しておらず**完全に孤立稼働**していた
- 同じ役割は既に `news-briefing` skill（cron→Notion📰DB→ohayoが読込）が担当しており冗長

**How to apply:**
- 朝のニュース把握は `news-briefing` skill + ohayo の Notion📰DB 経路に一本化
- もし「議会一般質問ネタ抽出」を残したい場合は news-briefing skill に薄く追加実装する形で（旧Pythonテンプレ方式は voice-dna 汚染源にもなるので**コピーしない**）
- Desktop に毎朝HTMLが生えなくなったことに気づいても**正常**

## 実行ログ（2026-05-12）
1. `launchctl unload ~/Library/LaunchAgents/com.kameyama.briefing.plist` → 残件0確認
2. `~/Desktop/ブリーフィング/` 全20日分 → `~/Desktop/_archive_briefing_2026-05-12/ブリーフィング/` へ退避
3. `~/Library/LaunchAgents/com.kameyama.briefing.plist` → 同archiveへ `.disabled` リネームで移動

## 残置物（削除していないもの）
- `~/.kameyama-briefing/daily_briefing.py` （Pythonスクリプト本体・~99KB） — launchd 切ったので起動はしないが、参考として保持。将来不要判断したら削除可
- `~/.kameyama-briefing/cache/` キャッシュ・`last_error.log` 等も残置

## 関連メモ
- [[feedback-news-briefing-quality-over-quantity]] — 5〜7件厳守、過去7日重複排除等の品質基準（こちらが正式採用）
- [[feedback-news-briefing-hallucination-guard]] — URL先タイトル類似度+90日以内+本文整合の3点検証
- [[feedback-news-briefing-freshness-check]] — Yahoo検索のキャッシュ罠

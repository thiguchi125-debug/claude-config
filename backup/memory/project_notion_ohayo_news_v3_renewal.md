---
name: project_notion_ohayo_news_v3_renewal
description: 2026-07-03のNotion大改修＋ohayo v3全面書き直し＋news-briefing v3反映＋smart-intakeスキル新設の改修記録。新構成の正本と検証状況
metadata: 
  node_type: memory
  type: project
  originSessionId: 2237a7c2-1e97-4b26-8ecc-ad5b1b3e3b53
---

# Notion大改修＋ohayo/news v3＋smart-intake（2026-07-03）

## 何をしたか

1. **Notion大改修**: 🗄️旧アーカイブページ新設→旧タスクDB/旧PJDB（素の名前で誤登録リスクだった）を📦旧_改名して収容、テンプレ残骸・総称市政報告会ページ等も収容。ダッシュボード📚情報ハブ一覧を現行ハブ（地域選挙ハブ/会議ハブ/ネタDB/投稿管理DB/🗂PF/市民意見リスト/報告会DB）に総張り替え。🌐全体地図をv2（Todoist=実行/Notion=蓄積）に改訂。御幸市政報告会の二重ページ統合。「📥未分類インテーク」ページ新設（ダッシュボード配下）。
2. **smart-intakeスキル新設**（`~/.claude/skills/smart-intake/SKILL.md`）: モードA=投げ込み自動保存（判定ツリー→確認1回→一括保存→**nichijo日次ログに🔖台帳1行**→判定不能は📥未分類インテークへ）／モードB=「〇〇どこ？」横断検索（Notion→Drive _index→drafts/outputs→relocation_log→Todoist）。CLAUDE.mdのスマートインテーク節はこのスキルへの参照に整理済み。
3. **ohayo v3全面書き直し**（1,444行→約150行）: 12層パッチの矛盾（Todoist宣言vs旧Notion手順150行/iJAMP3箇所残存/ニュース書く・書くな・消せの三重矛盾）を物理削除。新設=予定コンテキスト連動（今日の予定×前回宿題・未解決の声）/議会・選挙カウントダウン/ニュース展開フック表示/未分類件数/Routine死活監視。ダッシュボード書込は📅スケジュール・🎯フォーカス・✅タスクの3セクション限定。タスク監査は前日比増分発火（ohayo_state.json）。燃費目標60-80K。
4. **news-briefing v3反映**: 5/26設計のまま未適用だったdedup（30日窓・3層判定・続報は既存ページ追記・国政週1）をSKILL.md本体＋クラウドRoutine `trig_01WXgkt4JqANvhi1YuQLGsEQ`（毎朝6:00 JST）の両方に適用。DBスキーマに`活用`セレクト（演説/SNS/一般質問/ブログ/静観）新設＝展開フック、廃止カテゴリ2つ撤去。oyasumiにStep4.7「新着7日超→確認済へ自動遷移」新設。

## 検証状況

- Routine v3は2026-07-03朝6時の実行から有効（太陽光・水道濁りの再登録が止まるかを翌朝確認）
- ohayo v3・smart-intakeは初回実走で動作確認する（未検証のまま本番に入る場合は初回に注意）

## 関連
[[reference_storage_map]] / [[feedback_news_briefing_v3_duplicate_detection]] / [[feedback_system_closing_loops_rot]] / [[project_notion_overview_map]]

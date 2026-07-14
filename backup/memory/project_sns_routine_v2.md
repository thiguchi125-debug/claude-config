---
name: project-sns-routine-v2
description: SNS発信ルーティンv2（Discord投げ込み→夜間振り分け→朝夕プッシュ）の進行状況と運用
metadata: 
  node_type: memory
  type: project
  originSessionId: 9ee7574d-5bcc-4598-a986-151d530e598a
---

# SNS発信ルーティンv2

## 参照
- 仕様書: `~/.claude/projects/-Users-kusakawatakuya/specs/2026-07-14-sns-routine-v2-design.md`
- 計画書: `~/.claude/projects/-Users-kusakawatakuya/plans/2026-07-14-sns-routine-v2-phase1.md`

## Phase 1（完了・2026-07-14）

**狙い**: 草川がスマホから思いついた瞬間に投げ込めば、迷子ゼロで正規の保存先に振り分けられる。

**入口**: 草川がスマホからDiscord BotへのDMに随時投げ込み。記号あり（「☐やること」「声:意見」「発信:ネタ」）でも記号なし（文脈判定）でもOK。

**処理**: 毎晩3:10 launchd `com.kusagawa.discord-intake` が `~/.claude/scripts/sns-routine/nightly_intake.sh` を実行。
1. `discord_api.py fetch` で新着取得（新着0件なら即終了）
2. 新着ありなら headless `claude -p`（`triage_prompt.md` 準拠）が振り分け判定

**振り分け先**:
- タスク（☐）→ Discordに提案返信 → 草川が「①OK」等で返信 → 翌夜Todoist登録（td.py）
- 声（声:）→ 📝市民意見リスト（`c2c34bd8-`）
- 発信ネタ（発信:）→ 📣SNS投稿管理DBに💡ストック
- 判定不能 → 📥未分類インテーク（`391cf503-a68f-8191-b218-e80fdc7aedeb`）

**処理レシート（Discordリアクション）**:
- ✅ = 保存済み
- ⚠️ = 未分類ボックス行き
- 👀 = queue退避（翌朝flush待ち）

**カーソル規律**: `last_processed_id` は全件処理成功時のみ前進（部分処理での前進禁止）。原本はDiscord履歴に残るため迷子ゼロ。

**フォールバック（queue）**: Notion書込不能・当日nichijoログ未作成等の理由で保存できない場合は `~/.claude/scripts/sns-routine/_notion_queue.jsonl` に退避 → 翌朝ohayoがflush（各行の `dest` に従い保存先へ書込→行削除）。

**状態監視**: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_scripts/_pipeline_status.json` の `discord_intake` キー（ohayo §1直後の節で毎朝確認）。

**トラブル時**:
- ログ確認: `~/.claude/scripts/sns-routine/_intake.log`
- 手動再実行: `~/.claude/scripts/sns-routine/nightly_intake.sh`
- launchd再キック: `launchctl kickstart gui/$(id -u)/com.kusagawa.discord-intake`
- plist・再登録コマンドは `~/.claude/scripts/sns-routine/README.md` に保管（Mac再セットアップ時の復元用）

**検証済み事実**:
- headless `claude -p` からNotion MCPへ到達可（PATH A）
- td.pyはheadless実行で権限拒否されることがあるため、allowedToolsにTodoist MCPを併記済み

## 記号早見

| 記号 | 用途 | 保存先 |
|---|---|---|
| ☐〇〇 | タスク | 提案→返信→翌夜Todoist |
| 声:〇〇 | 市民の声 | 📝市民意見リスト(c2c34bd8-) |
| 発信:〇〇 | 発信ネタ | 📣SNS投稿管理DB（💡ストック） |
| （記号なし） | 文脈判定 | 上記いずれか、または📥未分類インテーク |

## Phase 2（完了・2026-07-14）ニュース収集v2

news-briefingをv4化：4カテゴリ5〜7件（亀山中心）→**7カテゴリ8〜15件・2階層品質モデル**。
- **Tier 1（フル3点セット）**: A亀山2-3件／Bフォーカス曜日ローテ1-2件（従来品質）
- **Tier 2（ライト版=見出し60字/概要50字/議会活用メモ=`亀山→`1行）**: C国政・地方自治HL2-3件（月曜のみ俯瞰解説）／D政策ドメインHL2-3件（フォーカス以外の5ドメイン・日付限定クエリ＋省庁報道発表一覧直行可）／E三重県政・県内他市1-2件／F選挙・世論0-1件
- G iJAMP0-1件（🔒内部専用・**RoutineにGmail接続を追加して復活**＝旧v3.1はGmail未接続で不実行だった）
- クエリ予算=WebSearch10〜11本＋Gmail1回（v1崩壊の再発防止線）・水増し禁止
- 正本2箇所: `~/.claude/skills/news-briefing/SKILL.md`（対話モード）＋クラウドRoutine `trig_01WXgkt4JqANvhi1YuQLGsEQ`（毎朝6:00 JST・model=claude-sonnet-5に更新）
- **ロールバック**: 旧v3.1プロンプト全文＝`~/.claude/scripts/sns-routine/_routine_news_v3_backup.md`
- 📰ニュースDBカテゴリselectに`選挙・世論`＋`その他`追加済み（「その他」はiJAMP用に指定されていたのに実DBに無かった潜在バグ修理）
- 実走テスト済（8件・重複ゼロ・WebSearch要約の偽記事3件をハルシネーション検証ゲートが検出排除）
- `活用=SNS`フラグがPhase 3朝夕プッシュの発信候補選定の参照元になる

## Phase進捗

- **Phase 1（完了 2026-07-14）**: Discord投げ込み→夜間自動振り分け
- **Phase 2（完了 2026-07-14）**: ニュース収集v2 — 国政・6ドメイン・県政・選挙（news-briefing v4）
- **Phase 3（次）**: 朝夕SNSプッシュ（クラウド・Discord Webhook/RESTポーリング・候補パック）
- **Phase 4**: 週次深掘り＋学習ループ

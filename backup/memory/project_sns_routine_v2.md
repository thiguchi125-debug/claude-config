---
name: project-sns-routine-v2
description: SNS発信ルーティンv2（Discord投げ込み→夜間振り分け→朝夕プッシュ）の進行状況と運用
metadata: 
  node_type: memory
  type: project
  originSessionId: 9ee7574d-5bcc-4598-a986-151d530e598a
  modified: 2026-07-24T19:01:59.484Z
---

# SNS発信ルーティンv2→v3

## 参照
- 仕様書v3: `~/.claude/projects/-Users-kusakawatakuya/specs/2026-07-23-sns-routine-v3-design.md`（正）
- 仕様書v2: `~/.claude/projects/-Users-kusakawatakuya/specs/2026-07-14-sns-routine-v2-design.md`
- 計画書: `~/.claude/projects/-Users-kusakawatakuya/plans/2026-07-14-sns-routine-v2-phase1.md`

## 🆕 v3（2026-07-23実装・完成原稿直接納品）

**v2失敗診断**: ①メニュー返信ゼロ→生成ゼロ（7/15以降返信ほぼ0＝投稿ゼロ）②WebFetch403で候補が在庫劣化（7/18-22）③素の活動メモがSNS素材に未活用④振り分け先が見えず「記録が溜まる実感がない」。

**v3の形**: push便が**完成短文原稿（X/Threads/FB＋写真日はInsta）をDM直接納品**。返信は修正時のみ（「Bで」「〇〇直して」「ブログ化」「動画で」「パス」「承知で」「別テーマ:」）。朝6:45／朝返信7:30／**夕19:30**／**夕返信20:15**（夕は当日活動を夜まで拾うため後ろ倒し）。夕便の本命=当日投げ込みの活動メモ・写真（タグ不問）。素材ゼロでも必ず1本（在庫由来は明記）。

**品質**: 新風枠毎便1本必須（直近3日ホット話題×亀山接地・WebSearch2-3本可）／ニュースは一次記事WebFetch本文調査必須／`_theme_history.json` 14日クールダウン（ステータスページにミラー）／iJAMPはGmail `from:ijamp.jiji.com newer_than:1d` 全見出しスキャン→採用時は公開一次情報乗り換え必須（**サイトスクレイピングは2026-04-27決定通り恒久禁止**）。

**見える化**: 📮投げ込み台帳DB（data_source `7a444c29-ef25-4139-9033-c24e9bd78528`）にtriageが全件記録＋毎夜🧾レシートDM（保存先リンク付き）。

**障害耐性**: DM納品をNotion障害と切り離し（queue退避）／claude -p失敗15分リトライ／ネット疎通待ち／`_delivery_state.json`に単純化。allowedToolsに`WebSearch,WebFetch,mcp__claude_ai_Gmail__*`追加。discord_api.pyにattachments＋downloadコマンド追加（Insta写真・必ずRead確認）。

**不変**: 夜間intake3:10の振り分け先／news-briefing6:00／日曜監査／D1 drafts保存／安全ゲート毎便必須。v2ファイルは`_backup_2026-07-23_v3/`。

## v3.1（2026-07-25・遅延並走事故の修理）

実走2日で判明: ①7/23夕便がスリープ凍結→翌朝7/24朝便と並走し同テーマ二重納品 ②7/24夜はバッテリー駆動（9%→3%）でスリープ連発→22:55遅延 ③`_auto_intake.sh`のwrite_statusが全置換で毎晩2:30にsns_*監視キーを消していた ④Notionトークン失効（7/24夜〜）。

対策: sns_leg.shに**120分超遅延の見送りガード＋mkdir排他ロック（macOSにflock無し）＋caffeinate -i**、_auto_intake.shをマージ書込み化。**運用前提=Macは電源接続**（バッテリー時はスリープで便が止まる・遅延分はガードが安全に見送り翌便が繰越）。Notion失効時もDM納品は完走しqueue退避が機能した（設計通り）。

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

## Phase 3（完了・2026-07-14）朝夕SNSプッシュ

**運用の形**: 朝6:45／夕16:30にDiscord DMへ発信候補メニュー2〜3本（🎬動画フラグ付き）→草川が返信→7:30／17:15の返信便が**ブログ（アンカー記事）＋X/Threads/Instagram/Facebookの5点セット**を生成してDM納品＋📣投稿管理DB保存＋drafts保存（D1）。

- **実行基盤＝全部ローカルMac launchd**（当初クラウドRoutine設計だったが、**クラウド実行環境がdiscord.com接続を組織ポリシーで403ブロック**することが実走で判明→ローカル化。Macはsleep=0常時稼働で問題なし。トークンも`~/.claude/channels/discord/.env`のみ＝Notion設定ページからは撤去済み）
- **launchd 6本**: com.kusagawa.sns-morning-push(6:45)／sns-morning-reply(7:30)／sns-evening-push(16:30)／sns-evening-reply(17:15)／sns-audit(日曜3:20)／discord-intake(3:10・Phase1)。実体=`~/.claude/scripts/sns-routine/sns_leg.sh <leg名>`＋`leg_*.md`プロンプト4本
- **返信文法**: 「1で」「2、〇〇だけ直して」「1と3両方」「1を動画で」「パス」「出し直して」（切り口一新の再提案・実走フィードバックで追加）「別テーマ:〇〇」「N 承知で」（HIGHリスク承諾）。返信なし=生成ゼロで繰越
- **候補優先順位**: ①投げ込み（📮候補パック）＞②ニュースSNSフラグ（📰ダイジェスト）＞③💡ストック
- **固定ページ**: 📮候補パック=39dcf503-a68f-8101-beac-c2883ed87e70（夜間Mac第2ステージが全置換・生成ガイド=voice-dnaコア/リスク8軸/禁止表現/PF+ブログ体裁）／📮SNS便ステータス=39dcf503-a68f-811b-bdd3-cce4e418187a（メニュー・処理済みID・動画リクエスト・履歴）／🔧設定=39dcf503-a68f-811c-8238-f94a57bf4513（トークンは撤去済み・ID控えのみ）
- **動画**: 「Nを動画で」→即時台本+撮影メモDM→夜間Mac第3ステージ（_video_queue.txt経由）がshort-video-createフル制作
- **監査**: 日曜3:20にDiscord7日履歴vs リアクション突合（floor=2026-07-14以前は対象外）→`sns_audit`キー→ohayoが日曜朝表示
- **クラウドRoutine 4本は作成済みだが無効化**（trig_01LHVnzjsr5ohwLWRbRXecWw／01BReLaJQcMdC74RcfGj395q／01N7rnm9BUzhh7XfKXEoMKZa／01VBgiUKQVpFbH1kzmExFdpS・claude.ai/code/routinesで削除可・プロンプト保全=_routines_phase3/）
- **E2E実績（2026-07-14）**: メニュー配信→「どれも微妙」→聞き返し→「出し直して」×2→議会実績接地の再提案→「1」選択→体育館空調0%（2024年12月議会）に接地した4PF納品＋📣保存まで本番経路で完走。ブログ標準装備は草川フィードバックで即日追加
- **禁止表現の学び**: voice-dna抽出物に「届かない最後の100m」（距離比喩=禁止）が混入していた→pack_prompt.mdに「voice-dnaコアにも禁止表現を含めない」明文化＋距離比喩を全面禁止に格上げ
- 便を止めたい時: `launchctl bootout gui/$(id -u)/com.kusagawa.sns-<leg名>`（再開はbootstrap）

## Phase進捗

- **Phase 1（完了 2026-07-14）**: Discord投げ込み→夜間自動振り分け
- **Phase 2（完了 2026-07-14）**: ニュース収集v2 — 国政・6ドメイン・県政・選挙（news-briefing v4）
- **Phase 3（完了 2026-07-14）**: 朝夕SNSプッシュ（ローカルlaunchd・ブログ+4PF・出し直し対応・日曜監査）
- **Phase 4（次）**: 週次深掘り（土曜・上位2テーマ→🎯政策・質問ネタDB）＋学習ループ（選択/パス傾向の候補選定への反映）

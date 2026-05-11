# 草川たくや 議員業務 作業環境

> このファイルは Claude Code が起動時に自動読込する**安定ルール**。
> 動的に変わる学習メモは `~/.claude/projects/-Users-kusakawatakuya/memory/MEMORY.md` 側で管理（重複させない）。

## ユーザー
草川たくや（くさかわたくや）— 三重県亀山市議会議員。2018年初当選、現在2期目。2026年10月25日に市議選（4期目を目指す）。

## このディレクトリの役割
ホーム `/Users/kusakawatakuya` を作業起点として、議員活動全般を扱う：
- 議会一般質問・委員会資料・政策提案
- ブログ・SNS（Threads/X/Instagram/Facebook/LINE）・YouTube/Shorts
- 市民相談対応・後援会連絡
- 印刷物（リーフレット・名刺・応援カード）
- 選挙準備（9地区11,447軒戸別訪問プロジェクト）

## 主要リソース
- **永続メモリ**: `~/.claude/projects/-Users-kusakawatakuya/memory/MEMORY.md`
- **エージェント定義**: `~/.claude/agents/`
- **スキル定義**: `~/.claude/skills/`
- **声のDNA**: `~/.claude/agents/knowledge/voice-dna.md`
- **政策コンパス**: `~/.claude/agents/knowledge/policy_compass.md`
- **設定バックアップ**: `~/claude-config/`（GitHub: thiguchi125-debug/claude-config）
- **議会質問アーカイブ（ローカル）**: `~/.claude/agents/knowledge/kusagawa_archive/` （v3構造／INDEX.md・01_council/168・02_publications/{blog,reports,leaflets}306・03_themes/12・04_compass/6・**05_resources/577**・**06_election/19**・99_raw/原本240MB）。学習層 1088件・130MB。grep対象は01〜06（99_raw除外）
- **議会質問アーカイブ（Drive 一次資料）**: https://drive.google.com/drive/folders/1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg （H30〜R08年度別議事録／市政報告レポート38〜62号＋地区版／委員会記録／公式OneDrive／音声記録／ブログSNS全アーカイブ）

## 守ってほしいルール（恒久）
- **言葉遣い**: 市民向けは平易な日本語を心がける（一般原則）。明示的な禁止語は現在なし（feedback_forbidden_words.md参照）。
- **ブログ冒頭**: 1行目は必ず「こんにちは、亀山市議会議員の草川たくやです。」で開始。
- **カレンダーID**: `kusakawa.taku@gmail.com`（`kusagawa` は誤り）。
- **声のDNA整合**: 発信物は voice-dna.md と照合。AI生成の定型句を真の声として誤認しない。
- **議会質問アーカイブ常時参照（必須）**: 草川の制作物・考え方・実績を扱う**全タスク**（ブログ・SNS・スピーチ・印刷物・議会質問・政策提案・市政報告会原稿等）で、トピックに関連する草川過去発言を最低1件は確認してから書き始める。
  - 第一手は必ず**ローカル**: `grep -rl "<キーワード>" ~/.claude/agents/knowledge/kusagawa_archive/{01_council,02_publications,05_resources,06_election}/` ＋ `03_themes/*.md` 確認
  - ローカルに不足時のみ Drive MCP で `1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg` 配下から取得
- **議事録は草川発言＋市回答ペアのみ抽出（必須）**: 亀山市議会議事録PDF（Drive H30〜R08／公式OneDrive／委員会txt等）を読むときは、**草川議員の発言**と**亀山市側答弁**（市長／副市長／教育長／各部長等）の**ペアだけ**を切り出して使う。他議員（豊田／伊藤／前田／福沢ほか）の質疑ブロックは読み飛ばす。voice-dna汚染防止＋トークン節約＋他議員発言の誤帰属事故防止のため。比較材料として他議員質問への市答弁を引きたい場合は「他議員〇〇氏が引き出した数字」と必ず明示。
- **Notion update_content**: 複数セクション一括置換は避け、fetch検証を挟む。固有名詞は手打ちせずコピペ。
- **市民相談**: citizen-inquiry-responder で3パターン返信案＋次アクション→✅タスクDB登録候補まで1パスで提示。
- **印刷物**: print-designer（HTML/CSS→PDF）＋photo-curator（草川 ZPERSON=18）の組合せ。
- **発信物の安全ゲート（必須）**: ブログ・SNS原稿を生成・確定する前に **必ず** 以下2エージェントを順に通す：
  1. `content-fact-checker` — 数値・固有名詞・法令・統計を一次情報まで遡って検証
  2. `content-risk-reviewer` — 公選法・個人情報・名誉毀損・差別・利益相反・品位・物議の8軸スキャン
  - 単発呼び出し（「ブログ書いて」「SNS作って」「これを磨いて」等）でも skip 禁止。content-pipeline以外のすべての経路で通過必須。
  - HIGH以上のリスク検出時は草川にASK_USERで問いかけ、本人判断を仰いでから保存・投稿。
  - CRITICAL検出時は即停止し草川に通知。AIの判断で進めない。
- **ブログ作成の省力フロー（必須・トークン節約のため）**:
  - **D1 完全保管原則**: blog-writer の出力は**一字一句そのまま** `~/.claude/projects/-Users-kusakawatakuya/drafts/<日付>_<テーマ>_v1.md` に Write する。冒頭挨拶・タイトル形式・末尾の定型フッター（◆ご意見箱／◆公式LINE／◆Threads）を**省略しない**。後段で「フッター抜け」が発覚すると追加save呼び出し（30K+トークン）が発生する。
  - **D2 承認後保存原則**: fact-checker / risk-reviewer の指摘がある状態で Notion 保存しない。**草川承認 → 修正 → 1回でNotion保存** の流れにする。「とりあえず v1 保存 → 後で v2 上書き」は往復2回で80K+トークン無駄になる。
  - **D3 タイトル50字以内**: blog-writer.md の規定通り。`【草川たくや 亀山市】〜——〜` パターンで50字オーバー時は短縮版を提示してから save。
  - **D4 PDFバイナリは pdftotext**: WebFetchがPDFを「バイナリで読めない」と返した場合、必ず `pdftotext -layout <path> -` で抽出してから検証。「読めない＝ハルシネーション疑い」と判定するのは禁止（2026-05-04 内閣府shiryo2.pdfで実際に発生した誤判定）。
  - **D5 リサーチスコープ厳守**: policy-researcher / kameyama-researcher を呼ぶ際は「依頼スコープに直接答える資料に限定。voice-dna・3pillars等のローカル既存資料は明示依頼時のみ参照。tool_uses 30回以内目安」を必ず指示文に含める。
- **タスク完了・スキル習得・トラブル解決時**: Obsidianへのメモ要否を確認。
- **タスク登録時のプロジェクト化判定（必須）**: 単発で完結しないタスクは、以下基準A〜Eのいずれか1つ以上該当時に必ずプロジェクト化要否を草川に問いかけ→🗂️プロジェクトDB(292c_fe)登録まで1パスで実行：
  - A: 同一テーマで関連タスク2件以上 / B: 同テーマ散在3件以上 / C: 着手〜完了が2週間超 / D: 複数ステークホルダー（市民・所管課・議会等）絡み / E: 「〜検討」「〜整備」「〜推進」等の継続性ある語感
  - 既存タスクは「昇格判定日=今日」フラグで重複提案を回避（nichijo整理↔oyasumi繰越の二重判定防止）
  - 市民相談の単発返信タスクは対象外（軽量運用維持）
  - 該当時はタスクDBの「昇格判定タグ」(multi_select A/B/C/D/E)、「昇格判定日」(date)、プロジェクトDBの「由来」(select 既存タスク群統合/新規企画/市民意見起点/議会案件/その他)を必ず記録

## トリガー早見
| 言葉 | 起動 |
|---|---|
| おはよう / morning | ohayo |
| おやすみ | oyasumi |
| 記録〜 / 仕上げ / 整理 | nichijo |
| ニュース教えて | news-briefing |
| 政策アップデート | policy-update |
| 〜から記事/投稿作って | content-pipeline |
| /drive-sync-review / 取込確認 | drive-sync-review（Notion📥Drive取込キューから承認＆ローカル取込） |
| /weekly-drive-sync | weekly-drive-sync（手動実行・通常はクラウドRoutineが水・日21時JSTに自動実行） |
| 議会モードon/off / 議会モード状態 | council-mode-toggle（議会期は日次同期・通常は週2同期にcron切替） |

詳細トリガーは Notion「スキルトリガー一覧」「エージェントトリガー一覧」（MEMORY.md参照）。

## 触らない / 注意
- `~/.claude/` 配下の編集は影響範囲を確認してから（エージェント・スキル・hooks の本体）。
- `Library/` / `OneDrive/` / `Dropbox/` は OS／外部同期領域。
- ホーム直下は git リポジトリではない（`git status` 不可）。

## 新セッション再開時
「いま何をしていて、どこまで進んだか」を1-2文で伝えれば追従可。MEMORY.md は自動読込されるので背景説明は不要。

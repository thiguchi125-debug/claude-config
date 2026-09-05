# 草川たくや 議員業務 作業環境

> Claude Code が起動時に自動読込する**安定ルール**。動的な学習メモは `~/.claude/projects/-Users-kusakawatakuya/memory/MEMORY.md` 側（重複させない）。
> **詳細手順は `~/.claude/OPERATIONS.md`**（該当タスクに入る前に該当節をRead）。

## ユーザー
草川たくや（くさかわたくや）— 三重県亀山市議会議員。2018年初当選、現在2期目（亀山市議会 議員名簿で確認済み）。2026年10月25日に市議選（**3期目**を目指す）。

## このディレクトリの役割
ホーム `/Users/kusakawatakuya` を作業起点に議員活動全般（議会質問・SNS/ブログ・市民相談・印刷物・2026選挙準備）を扱う。

## 主要リソース
- **永続メモリ**: `~/.claude/projects/-Users-kusakawatakuya/memory/MEMORY.md`／**運用詳細**: `~/.claude/OPERATIONS.md`
- **エージェント定義**: `~/.claude/agents/`／**スキル定義**: `~/.claude/skills/`
- **声のDNA**: `~/.claude/agents/knowledge/kusagawa_archive/04_compass/voice-dna.md`（コア）／`voice_examples.md`（詳細・必要時のみ）
- **政策コンパス**: 同 `04_compass/policy_compass.md`（コア）／`policy_compass_evidence.md`（詳細・必要時のみ）
- **設定バックアップ**: `~/claude-config/`（GitHub: thiguchi125-debug/claude-config）
- **議会質問アーカイブ（ローカル）**: `~/.claude/agents/knowledge/kusagawa_archive/` 学習層1088件・grep対象は `01_council/02_publications/03_themes/04_compass/05_resources/06_election`（99_raw除外）。構造は INDEX.md と reference_drive_archive_kusagawa.md
- **同（Drive一次資料 v3）**: 高速grepは `_index/` の.txtキャッシュ。投函は `_INBOX_council/`／`_INBOX_daily/`。**詳細＝OPERATIONS.md【F】**

## 守ってほしいルール（恒久）
- **言葉遣い**: 市民向けは平易な日本語（一般原則）。明示的な禁止語は現在なし。
- **ブログ冒頭**: 1行目は必ず「こんにちは、亀山市議会議員の草川たくやです。」で開始。
- **カレンダーID**: `kusakawa.taku@gmail.com`（`kusagawa` は誤り）。
- **声のDNA整合**: 発信物は voice-dna.md と照合。AI生成の定型句を真の声と誤認しない。
- **議会質問アーカイブ常時参照（必須）**: 草川の制作物・考え方・実績を扱う**全タスク**（ブログ・SNS・スピーチ・印刷物・議会質問・政策提案・報告会原稿等）で、関連する草川過去発言を最低1件確認してから書き始める。第一手は必ず**ローカル** `grep -rl "<KW>" ~/.claude/agents/knowledge/kusagawa_archive/{01_council,02_publications,05_resources,06_election}/` ＋ `03_themes/*.md`。不足時のみ Drive MCP（フォルダ `1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg`）。
- **議事録は草川発言＋市回答ペアのみ抽出（必須）**: 亀山市議会議事録を読むときは**草川議員の発言**と**市側答弁**（市長／副市長／教育長／各部長）の**ペアだけ**を切り出す。他議員（豊田／伊藤／前田／福沢ほか）の質疑ブロックは読み飛ばす。voice-dna汚染防止＋トークン節約＋誤帰属事故防止。他議員質問への市答弁を引く場合は「他議員〇〇氏が引き出した数字」と必ず明示。
- **タスク別ガードルールの読込（必須）**: 作業に入る前に `~/.claude/GUARDRAILS.md` の該当節をRead → 発信【1】【2】／印刷物・動画・画像【3】／Notion書込【4】／議会業務【5】／市民対応・報告会【6】／基盤トラブル【7】／個別案件の事実【8】。安全ゲートの一部として実行する。
- **発信物の安全ゲート（必須・skip禁止）**: ブログ・SNS原稿を生成・確定する前に必ず順に通す → ①`content-fact-checker`（数値・固有名詞・法令・統計を一次情報まで） ②`content-risk-reviewer`（公選法・個人情報・名誉毀損・差別・利益相反・品位・物議の8軸）。単発呼び出し（「ブログ書いて」「これを磨いて」等）でも例外なし。**Notion保存も「発信」＝保存前に通す**。HIGH以上は草川にASK_USER、CRITICALは即停止・通知。 **短文SNS（1原稿600字以下）は `content-gate-lite` 1本で可＝同強度・起動1回（2026-09-05）。**
- **タスク・プロジェクトはTodoistに一本化（最上位）**: 登録・参照・更新・完了はすべてTodoist（`td.py`）。Notion ✅タスクDB(292cf503)・🗂プロジェクトDB(292c_fe)は**新規登録に使わない**（参照のみ）。期限付き登録は task-add スキル経由（カレンダー突合必須・hookがdeny）。**詳細＝OPERATIONS.md【B】**
- **情報入力の自動振り分け保存＝スマートインテーク（必須・最上位）**: 保存先指定が無い情報投入（「〇〇地区の件」「〇〇の声があった」「会議メモ:」「〇〇と話した」等）は **smart-intakeスキル**で判定→提案→確認→保存→台帳記録を1パス。正本＝`~/.claude/skills/smart-intake/SKILL.md`。核心3点：①保存前に振り分け先を1回提示→承認後に一括保存（個人情報・CRITICALはcontent-risk-reviewer経由）②どこに保存してもnichijo日次ログに🔖台帳1行を自動追記③判定不能は「📥未分類インテーク」へ（捨てない）。探し物は「〇〇どこ？」。
- **市政報告会の声の自動記録（必須）**: 「記録：〇〇報告会で△△の声」で起動。🎤市政報告会DBの「主な意見・要望」追記＋📝市民意見リスト登録＋Todoist「〇〇地区フォロー」箱。**詳細＝OPERATIONS.md【A】**
- **議会公務会議の資料Notionページ配置（必須）**: 個別の会議体イベントページは期別議会フォルダでなく **📅ミーティングノートDB（`26d7848d-ad1a-4e84-806f-a8dbccb1872b`）配下**。**詳細＝OPERATIONS.md【D】**
- **ブログ作成の省力フロー（必須）**: D1完全保管（フッター省略禁止）／D2承認後1回保存／D3タイトル50字／D4 PDFは`pdftotext -layout`／D5リサーチスコープ厳守。**詳細＝OPERATIONS.md【C】**
- **外部調査は台帳を先にgrep（必須）**: 他自治体・国・県の一次情報をAgentで調べる前に必ず `grep -rl "<KW>" ~/.claude/agents/knowledge/research_ledger/`。ヒットしたら読んで、足りない差分だけ投げる。調査後は最終報告を要約せず `<日付>_<テーマ>.md` で同フォルダへ回収する。正本＝`research_ledger/INDEX.md`（2026-09-03に同じ問いを2回調べて約265M重複させた）。
- **市民相談**: citizen-inquiry-responder で3パターン返信案＋次アクション→**Todoist**登録候補まで1パス（`td.py add`）。
- **印刷物**: 入口は **design-studioスキル**。テンプレ正本=`~/.claude/agents/knowledge/design_system/`。実装層は print-layout-architect／print-designer＋photo-curator（草川 ZPERSON=18）。
- **Notion update_content**: 複数セクション一括置換は避け、fetch検証を挟む。固有名詞は手打ちせずコピペ。

## 📂 保存先マップ（要点・フル版＝OPERATIONS.md【E】／正本＝reference_storage_map.md）
- **資料はすべて Drive マイドライブ直下に置く**（2026-08-26 v5・投函口を一本化）。毎晩2:30に `_root_intake.py` がファイル名→中身（必要ならOCR）→AIの順で判定して正規配置へ。旧 `_INBOX_council/`・`_INBOX_daily/` も副次入口として有効
- **名簿・個人情報** → Drive `日常資料アーカイブ/00_名簿・個人情報/`（grep対象外）
- AI下書き → `~/.claude/projects/-Users-kusakawatakuya/drafts/`／スキル生成物 → `~/outputs/`（絶対パス）
- 署名活動 → `~/publications/`／長期保管 → `~/Archive/`／削除候補 → `~/Archive/_trash_pending_<日付>/`（即rm禁止）
- Desktop/Downloadsは一時作業場（恒久保管禁止）。**Drive直下は野良置き禁止ではなく「投函口」**＝迷ったらそこへ置けばよい（翌朝には正規配置に入っている）。直下に残ってよいのは保護フォルダ4つ（`草川たくや 議会質問アーカイブ`／`📷写真ストック`／`📱動画素材`／`💾Macローカルミラー`）と `.gscript` だけ。

## トリガー早見
| 言葉 | 起動 |
|---|---|
| おはよう / morning | ohayo |
| おやすみ | oyasumi |
| 記録〜 / 仕上げ / 整理 | nichijo |
| ニュース教えて | news-briefing |
| 政策アップデート | policy-radar |
| 〜から記事/投稿作って | content-pipeline |
| ドライブ資料取り込んで / 取り込んで | drive-intake |
| ショート動画作って / TikTokセット | short-video-create |
| 写真ストック整理して / 写真回収して | 📷写真ストック月次整理（正本=Drive `📷写真ストック/README.md`） |
| 節約で〜 / 燃費よく / lean | lean-mode |
| フォーム取り込んで / ご意見箱取り込んで | form-intake |
| 会議メモ: / これ保存して / 〇〇と話した | smart-intake モードA |
| 〇〇どこ？ / あれどこだっけ | smart-intake モードB |
| 発信ネタ: / ひらめき: / ネタにして | spark |
| 〇〇地区の報告会準備 / 報告会の企画・スライド・前夜チェック | shisei-houkokukai |
| 〇〇地区版の市政報告レポート / 地区版レポート | chiku-report |
| チラシ作って / ポスター作って / 印刷物作って | design-studio |
| 逆算チェック / 準備漏れ確認 | gyakusan |
| タスク登録して / Todoistに入れて | task-add |
| 区切り / 区切って / セッション切る / 引き継ぎメモ | kugiri |
| 後援会取り込み | 後援会入会フォーム週次バッチ（正本=Drive `06_フォーム・アンケート運用/後援会入会フォーム/README.md`） |

詳細トリガーは Notion「スキルトリガー一覧」「エージェントトリガー一覧」（MEMORY.md参照）。

## 触らない / 注意
- `~/.claude/` 配下の編集は影響範囲を確認してから（エージェント・スキル・hooks の本体）。
- `Library/` / `OneDrive/` / `Dropbox/` は OS／外部同期領域。
- ホーム直下は git リポジトリではない（`git status` 不可）。

## トークン節約（2026-09-05 実測更新・詳細＝OPERATIONS.md【G】）
コスト＝文脈サイズ×呼び出し回数。8/22〜9/4の実測4.9Gトークンの内訳：**文脈20万超の呼び出しが本体消費の51%**／サブエージェント44%（content-fact-checkerが1本平均50回・5.5M）／夕方SNS便＋ニュース便の自動ジョブが12%。
- **モデルは200K窓の `claude-fable-5-1`（`[1m]` は使わない）**。フックが100K/140K/170Kで鳴る。**140Kを超えたら `/kugiri`**（起動固定費76Kなので100K未満では切らない）。
- **サブエージェントは本数と予算で管理**: 安全ゲートは1原稿1回。派生版（PF別・短尺・修正版）は親が `verified_claims` を渡して新規主張だけ検証。fact-checkerは取得15回上限＋`fact_ledger/verified_facts.tsv` を先に引く。孫Agentはhookがdeny。
- **巨大なツール結果を本体に入れない**（Notion fetchは1回60〜95K）。探索はBash（grep/sed -n）、画像は再Readしない、画像を伴う反復はサブへ隔離。
- **別件は新セッション**。効果測定＝`python3 ~/.claude/scripts/token_report.py 14`。

## 新セッション再開時
**`/kugiri` で区切った直後なら「再開」の一言でよい。** SessionStartフック `handoff_notice.py` が
`~/.claude/handoff/archive/`（24時間以内・最大3件）の本文を案件名付きで冒頭に自動注入するので、草川が説明する必要はない。複数あれば「〇〇を再開」と案件名を添えると確認なしで始まる（LAST.md は2026-09-05廃止）。
それ以外の場合は「いま何をしていて、どこまで進んだか」を1-2文で伝えれば追従可。MEMORY.md は自動読込。

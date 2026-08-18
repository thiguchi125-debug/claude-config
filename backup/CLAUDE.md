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
- **言葉遣い**: 市民向けは平易な日本語（一般原則）。明示的な禁止語は現在なし（feedback_forbidden_words.md）。
- **ブログ冒頭**: 1行目は必ず「こんにちは、亀山市議会議員の草川たくやです。」で開始。
- **カレンダーID**: `kusakawa.taku@gmail.com`（`kusagawa` は誤り）。
- **声のDNA整合**: 発信物は voice-dna.md と照合。AI生成の定型句を真の声と誤認しない。
- **議会質問アーカイブ常時参照（必須）**: 草川の制作物・考え方・実績を扱う**全タスク**（ブログ・SNS・スピーチ・印刷物・議会質問・政策提案・報告会原稿等）で、関連する草川過去発言を最低1件確認してから書き始める。第一手は必ず**ローカル** `grep -rl "<KW>" ~/.claude/agents/knowledge/kusagawa_archive/{01_council,02_publications,05_resources,06_election}/` ＋ `03_themes/*.md`。不足時のみ Drive MCP（フォルダ `1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg`）。
- **議事録は草川発言＋市回答ペアのみ抽出（必須）**: 亀山市議会議事録を読むときは**草川議員の発言**と**市側答弁**（市長／副市長／教育長／各部長）の**ペアだけ**を切り出す。他議員（豊田／伊藤／前田／福沢ほか）の質疑ブロックは読み飛ばす。voice-dna汚染防止＋トークン節約＋誤帰属事故防止。他議員質問への市答弁を引く場合は「他議員〇〇氏が引き出した数字」と必ず明示。
- **タスク別ガードルールの読込（必須）**: 作業に入る前に `~/.claude/GUARDRAILS.md` の該当節をRead → 発信【1】【2】／印刷物・動画・画像【3】／Notion書込【4】／議会業務【5】／市民対応・報告会【6】／基盤トラブル【7】／個別案件の事実【8】。安全ゲートの一部として実行する。
- **発信物の安全ゲート（必須・skip禁止）**: ブログ・SNS原稿を生成・確定する前に必ず順に通す → ①`content-fact-checker`（数値・固有名詞・法令・統計を一次情報まで） ②`content-risk-reviewer`（公選法・個人情報・名誉毀損・差別・利益相反・品位・物議の8軸）。単発呼び出し（「ブログ書いて」「これを磨いて」等）でも例外なし。**Notion保存も「発信」＝保存前に通す**。HIGH以上は草川にASK_USER、CRITICALは即停止・通知。
- **タスク・プロジェクトはTodoistに一本化（最上位）**: 登録・参照・更新・完了はすべてTodoist（`td.py`）。Notion ✅タスクDB(292cf503)・🗂プロジェクトDB(292c_fe)は**新規登録に使わない**（参照のみ）。期限付き登録は task-add スキル経由（カレンダー突合必須・hookがdeny）。**詳細＝OPERATIONS.md【B】**
- **情報入力の自動振り分け保存＝スマートインテーク（必須・最上位）**: 保存先指定が無い情報投入（「〇〇地区の件」「〇〇の声があった」「会議メモ:」「〇〇と話した」等）は **smart-intakeスキル**で判定→提案→確認→保存→台帳記録を1パス。正本＝`~/.claude/skills/smart-intake/SKILL.md`。核心3点：①保存前に振り分け先を1回提示→承認後に一括保存（個人情報・CRITICALはcontent-risk-reviewer経由）②どこに保存してもnichijo日次ログに🔖台帳1行を自動追記③判定不能は「📥未分類インテーク」へ（捨てない）。探し物は「〇〇どこ？」。
- **市政報告会の声の自動記録（必須）**: 「記録：〇〇報告会で△△の声」で起動。🎤市政報告会DBの「主な意見・要望」追記＋📝市民意見リスト登録＋Todoist「〇〇地区フォロー」箱。**詳細＝OPERATIONS.md【A】**
- **議会公務会議の資料Notionページ配置（必須）**: 個別の会議体イベントページは期別議会フォルダでなく **📅ミーティングノートDB（`26d7848d-ad1a-4e84-806f-a8dbccb1872b`）配下**。**詳細＝OPERATIONS.md【D】**
- **ブログ作成の省力フロー（必須）**: D1完全保管（フッター省略禁止）／D2承認後1回保存／D3タイトル50字／D4 PDFは`pdftotext -layout`／D5リサーチスコープ厳守。**詳細＝OPERATIONS.md【C】**
- **市民相談**: citizen-inquiry-responder で3パターン返信案＋次アクション→**Todoist**登録候補まで1パス（`td.py add`）。
- **印刷物**: 入口は **design-studioスキル**。テンプレ正本=`~/.claude/agents/knowledge/design_system/`。実装層は print-layout-architect／print-designer＋photo-curator（草川 ZPERSON=18）。
- **Notion update_content**: 複数セクション一括置換は避け、fetch検証を挟む。固有名詞は手打ちせずコピペ。

## 📂 保存先マップ（要点・フル版＝OPERATIONS.md【E】／正本＝reference_storage_map.md）
- 議会一次資料 → Drive `_INBOX_council/`／日常資料 → Drive `_INBOX_daily/`（夜間2:30に自動振分）
- **名簿・個人情報** → Drive `日常資料アーカイブ/00_名簿・個人情報/`（grep対象外）
- AI下書き → `~/.claude/projects/-Users-kusakawatakuya/drafts/`／スキル生成物 → `~/outputs/`（絶対パス）
- 署名活動 → `~/publications/`／長期保管 → `~/Archive/`／削除候補 → `~/Archive/_trash_pending_<日付>/`（即rm禁止）
- Desktop/Downloadsは一時作業場（恒久保管禁止）。Drive直下への野良置き禁止、迷ったら `_INBOX_daily/`。

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
| 後援会取り込み | 後援会入会フォーム週次バッチ（正本=Drive `06_フォーム・アンケート運用/後援会入会フォーム/README.md`） |

詳細トリガーは Notion「スキルトリガー一覧」「エージェントトリガー一覧」（MEMORY.md参照）。

## 触らない / 注意
- `~/.claude/` 配下の編集は影響範囲を確認してから（エージェント・スキル・hooks の本体）。
- `Library/` / `OneDrive/` / `Dropbox/` は OS／外部同期領域。
- ホーム直下は git リポジトリではない（`git status` 不可）。

## トークン節約（2026-08-19 実測更新）
コストは「文脈サイズ × ツール呼び出し回数」でほぼ決まる。文脈は**減らない**ので、長いセッションほど1回の呼び出しが高くつく（2026年8月実測＝20,139回・4,859Mトークン。**上位10セッションだけで全体の51%**）。
- **セッションを区切る（最大の効き目）**: 250回で区切れば約38%、150回なら約46%の削減。PostToolUseフック `context_budget_notice.py` が200K/350K/500K/700Kで1回ずつ警告するので、警告が出たら成果物を保存して `/clear`。再開は「いま何をしてどこまで進んだか」1-2文でよい。
- **別件は新セッションに分ける**: 用件をまたぐと前の用件の文脈を最後まで払い続ける。
- **画像は溜め込まない**: 1枚約1,500トークンを**セッション終了まで**占有する。8月の画像Read 602件のうち**38%が同一ファイルの2度読み**だった。中身が変わっていない画像の再Readは PreToolUseフック `image_reread_guard.py` が deny する（再レンダ後＝mtimeが動いた読み直しは通る）。
- **画像を伴う反復作業はサブエージェントへ隔離**: デザイン実装ループ（print-layout-architect／natural-design-reviewer）・Chrome自動化は、スクショが親セッションに残らないようAgent側で回す。
- **探索はBash（grep/sed/head）を優先**: Readは全文が文脈に残る。必要な箇所だけ `sed -n` で抜く。

## 新セッション再開時
「いま何をしていて、どこまで進んだか」を1-2文で伝えれば追従可。MEMORY.md は自動読込。

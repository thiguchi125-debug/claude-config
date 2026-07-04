# 草川たくや 議員業務 作業環境

> このファイルは Claude Code が起動時に自動読込する**安定ルール**。
> 動的に変わる学習メモは `~/.claude/projects/-Users-kusakawatakuya/memory/MEMORY.md` 側で管理（重複させない）。

## ユーザー
草川たくや（くさかわたくや）— 三重県亀山市議会議員。2018年初当選、現在2期目。2026年10月25日に市議選（4期目を目指す）。

## このディレクトリの役割
ホーム `/Users/kusakawatakuya` を作業起点に議員活動全般（議会質問・SNS/ブログ・市民相談・印刷物・2026選挙準備）を扱う。

## 主要リソース
- **永続メモリ**: `~/.claude/projects/-Users-kusakawatakuya/memory/MEMORY.md`
- **エージェント定義**: `~/.claude/agents/`
- **スキル定義**: `~/.claude/skills/`
- **声のDNA**: `~/.claude/agents/knowledge/kusagawa_archive/04_compass/voice-dna.md`（コア）／ `voice_examples.md`（実発言サンプル詳細・必要時のみ）
- **政策コンパス**: `~/.claude/agents/knowledge/kusagawa_archive/04_compass/policy_compass.md`（コア）／ `policy_compass_evidence.md`（軸別17セッション裏付け詳細・必要時のみ）
- **設定バックアップ**: `~/claude-config/`（GitHub: thiguchi125-debug/claude-config）
- **議会質問アーカイブ（ローカル）**: `~/.claude/agents/knowledge/kusagawa_archive/` 学習層1088件・grep対象は `01_council/02_publications/03_themes/04_compass/05_resources/06_election`（99_raw除外）。詳細構造は INDEX.md と reference_drive_archive_kusagawa.md
- **議会質問アーカイブ（Drive 一次資料・v3 2026-05-29完成）**: Google Drive Desktop によりMac側に**自動ミラー**＋日次自動振分パイプライン稼働中。3つのアクセス手段：
  - **ローカルsymlink（agent/skillはこれ経由・推奨）**: `~/.claude/agents/knowledge/kusagawa_archive/_drive/`
  - **CloudStorage実体**: `~/Library/CloudStorage/GoogleDrive-t.higuchi125@gmail.com/マイドライブ/草川たくや 議会質問アーカイブ/`
  - **Drive Web UI**: https://drive.google.com/drive/folders/1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg
  - **投函口（一元化）**: `_INBOX_council/`（議会資料用）／`_INBOX_daily/`（日常資料用）。iPhone or Macからどちらかに放り込めば後はパイプラインが処理。
  - **日次パイプライン**: 毎晩2:30に launchd `com.kusagawa.daily-drive-pipeline` が `_auto_intake.sh`（INBOX→キーワード判定→正規配置）→ `_build_index.sh`（pdftotext→_index/）を順次実行。
  - **grep対象（高速）**: `~/.claude/agents/knowledge/kusagawa_archive/_index/` の.txtキャッシュ（PDF直grepより数十倍速い）。
  - 詳細は project_drive_structure_v3.md

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
- **市民相談**: citizen-inquiry-responder で3パターン返信案＋次アクション→**Todoist**登録候補まで1パスで提示（`td.py add`・登録先は Notion✅タスクDB ではなく Todoist）。
- **情報入力の自動振り分け保存＝スマートインテーク（必須・2026-06-14〜・最上位／2026-07-03 smart-intakeスキルに実装統合）**: 草川がトピックに関する情報を入力したとき、**明示的な保存先指定が無くても**（「〇〇地区の件」「〇〇の声があった」「会議メモ:」「〇〇と話した」等）、**smart-intakeスキル**を起動して **判定→提案→確認→保存→台帳記録** を1パスで行う。判定ツリー・保存先ID・確認手順の正本は `~/.claude/skills/smart-intake/SKILL.md`（ここに重複記載しない）。核心3点だけ再掲：①保存前に振り分け先を1回提示→草川承認後に一括保存（個人情報・CRITICALはcontent-risk-reviewer経由）②どこに保存してもnichijo日次ログに🔖台帳1行を自動追記③判定不能は「📥未分類インテーク」ページへ（捨てない・ohayoが毎朝件数表示）。探し物は「〇〇どこ？」でsmart-intake横断検索。
- **市政報告会の声の自動記録（必須・2026-06-14〜）**: 「記録：〇〇報告会で△△の声」「〇〇市政報告会の記録」＋声の内容、で起動。報告会で出た声が行方不明になる事故（[[feedback_shisei_houkokukai_voice_capture]]）を構造的に防ぐ締め工程。手順：
  1. 地区／会場名から🎤市政報告会DB（data_source `df08b5ea-f5ff-4022-afe2-c8073fbe341a`）の該当ページを特定（notion-search／無ければ新規）。
  2. そのページの **「主な意見・要望」プロパティに声を追記**（update_properties・既存内容を保持して `【YYYY-MM-DD開催・当日の声】…` 形式で）＋「議会で取り上げる課題」更新＋進捗ステータス=進行中。← これが従来抜けていた締め工程。
  3. 対応すべき声を **Todoist「〇〇地区 フォロー」箱**（🏛議員活動配下・無ければ `td.py`/API で新設）へ登録。具体アクション明示の声（「まず〇〇に連絡」等）は **期限つき・優先度高**。
  4. 報告会由来タスクには **`要整理`ラベル**を付け、後でまとめてレビューできるようにする。
  5. **重複チェック**：📝一般質問ネタDB／📝市民意見リスト（c2c34bd8-）／既存Todoistに同じ声が既出なら新規作成せず参照（例：小下=「新団地アクセス道路の複合課題」は5/31に既存展開済→重複登録しない）。
- **印刷物**: 入口は **design-studioスキル**（テンプレ選択→実装→レビュー→安全ゲート→PDF→保存→テンプレ昇格を1パス）。テンプレ正本=`~/.claude/agents/knowledge/design_system/`（claude.ai/design「草川たくやデザインシステム」とDesignSync同期）。実装層は print-layout-architect／print-designer＋photo-curator（草川 ZPERSON=18）。
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
- **議会公務会議の資料Notionページ配置（必須）**: 議案分析／委員会説明会／所管事務調査／意見交換会／協議会／一般質問前夜チェック等の **個別の会議体イベントページ** は、期別議会フォルダ（例: `2026.3議会`）配下ではなく **🗂️会議ハブ → 📅ミーティングノートDB（`26d7848d-ad1a-4e84-806f-a8dbccb1872b`）配下** に作成する。会議体マスタ（`46414643-9717-404f-9572-2908c2c0a7f3`）に該当会議体がなければ即新規作成して relation 紐付け。標準プロパティ（会議種別=議会公務／ステータス=開催前／重要度=高／フォローアップ要否=ON／開催日／会議体／場所=亀山市役所／参加者）＋標準テンプレート（A.差分俯瞰／B.部別質問チェックリスト／C.最優先5本／D.発信展開メモ／E.数字回収シート／F.終了後タスク）を適用。詳細手順は `feedback_council_meeting_db_placement.md`。期別議会フォルダ配下に置くのは1議会期サマリ用ページ（一般質問原稿・期別質問構築プラットフォーム等）のみ。
- **タスク・プロジェクトはTodoistに一本化（必須・2026-06-14〜・最上位）**: 草川のタスク／プロジェクトの**登録・参照・更新・完了はすべてTodoist**で行う。Notion ✅タスクDB(292cf503)・🗂️プロジェクトDB(292c_fe)は**新規登録に使わない**（過去データの参照のみ可）。
  - **エンジン**: `python3 ~/.claude/scripts/todoist/td.py <cmd>`（token=`~/.config/todoist/token`・API必ず `/api/v1/`・旧v2/v9は410廃止）。主要cmd＝`morning`(朝の3ブロック+監査)／`add "内容" [--due 2026-07-01|today|tomorrow] [--project 議員活動] [--priority 1-4(4最高)] [--label 結果待ち] [--desc ...]`／`today`／`overdue`／`week`／`audit`／`list [PROJECT]`／`done <id>`／`rm <id>`／`projects`。詳細は td.py 冒頭doc と [[project_todoist_task_migration]]。
  - **構成**: プロジェクト＝Inbox／🏛 議員活動／📋 政策・一般質問／📣 発信／🏡 家族・プライベート。ラベル＝@結果待ち（相手のボール）／@保留（やる方向だが要検討）／@アイデア（いつか）／@読む。状態管理は「進行中/今週中」専用フォルダを作らず**期限＋"今日"ビュー＋ラベル**で表現（軽さの源）。
  - **新規タスク登録手順（2026-06-15確定）**: ①まず「記録で足りるか、タスク化が要るか」を振り分け（方針・状況は記録に残すだけ＝タスクにしない）②タスク化候補のみ保存先＋期限案（推奨=今日+3日）をセットで提示③**草川の回答を得てから**登録。既定値で勝手に確定登録しない（[[feedback_ask_destination_and_deadline_before_register]]が[[feedback_task_deadline_3days]]を上書き）。領域に応じ `--project` 指定。相手待ち＝@結果待ち、要検討＝@保留。
  - **ohayo/oyasumi のタスク処理は td.py**: ohayo朝タスク＝`td.py morning`、監査＝`td.py audit`。繰越は oyasumi では期限据え置き・翌朝 morning で草川承認分のみ `--due today` 付け替え（SKILL.md本体は2026-07-04にtd.py化修理済み・旧override不要）。
  - 市民相談の次アクション・会話中に出たやること・プロジェクト化候補も、**登録先はすべてTodoist**（重いNotion DBは使わない）。
- **タスク登録時のプロジェクト化判定（必須）**: 単発で完結しないタスクは、以下基準A〜Eのいずれか1つ以上該当時に必ずプロジェクト化要否を草川に問いかけ→**Todoistプロジェクト**（🏛議員活動配下のサブプロジェクト等）登録まで1パスで実行（旧🗂️プロジェクトDBは使わない）：
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
| **ドライブ資料取り込んで** / Drive取り込んで / 取り込んで / 資料取り込んで | **drive-intake**（4モード自動順次実行・通常はlaunchdが朝7時/夜22時に無人実行） |
| ショート動画作って / TikTokセット / 動画作って画像も | short-video-create（セリフ→fact-check→risk-review→nano-banana画像プロンプト→📣SNS投稿管理DB保存を1パス） |
| 節約で〜 / 節約モードで / 燃費よく / leanで | lean-mode（品質そのまま・無駄だけ削るトークン節約プレイブック。安全ゲート・主担当agent・アーカイブgrepは削らない） |
| 会議メモ: / これ保存して / メモ: / 〇〇と話した（保存先指定なしの情報投入全般） | **smart-intake モードA**（判定→確認1回→一括保存→🔖台帳） |
| 〇〇どこ？ / あれどこだっけ / 〇〇探して | **smart-intake モードB**（Notion・Drive・drafts・outputs・移動ログ・Todoist横断検索） |
| 発信ネタ: / ひらめき: / これ発信できる？ / ネタにして / この記事から何か作れる？ | **spark**（小さな種→接地→切り口2〜3案→選択分だけ生成→安全ゲート→保存。「貯めて」で📣SNS投稿管理DBに💡ストック） |
| 〇〇地区の報告会準備 / 報告会の企画・案内レポート・スライド・解説・前夜チェック | **shisei-houkokukai**（5ステージ制プロデュース・進捗は_status.json正本・急ぎは短縮経路） |
| チラシ作って / ポスター作って / リーフレット作って / 印刷物作って / デザイン制作 | **design-studio**（design_systemテンプレ候補提示→print-layout-architect実装→natural-design-reviewer→安全ゲート→PDF→保存→テンプレ昇格還元。勝負所のみdesign-director追加） |

詳細トリガーは Notion「スキルトリガー一覧」「エージェントトリガー一覧」（MEMORY.md参照）。

## 📂 保存先マップ（必須・2026-07-02 v4確立・詳細は reference_storage_map.md）
ファイルを保存・生成・受領したら**必ず**下表の正規置き場へ。Desktop/Downloadsは「一時作業場」であり恒久保管禁止（毎晩のパイプライン＋日曜スイープで30日超は`~/Archive/_sweep/`へ自動退避）。

| 用途 | 正規置き場 |
|---|---|
| 議会一次資料（議案書・議事録・委員会） | Drive `_INBOX_council/` に投函（夜間自動振分→議会資料アーカイブ） |
| 日常資料（政策素材・自治会・団体・チラシ） | Drive `_INBOX_daily/` に投函（夜間自動振分→日常資料アーカイブ01〜06） |
| **名簿・連絡先・個人情報を含むファイル** | Drive `日常資料アーカイブ/00_名簿・個人情報/`（grepインデックス対象外・ファイル名に「名簿/個人情報/連絡先」があれば自動隔離） |
| Googleフォーム・回答シート・GAS | Drive `日常資料アーカイブ/06_フォーム・アンケート運用/<案件名>/` |
| 一般質問・議案質疑の制作物 | Drive `ZZ_一般質問制作/`・`ZZ_議案質疑制作/`（R0X/YYYY-MM_◯月議会/01〜04） |
| 市政報告レポート完成品 | Drive `ZZ_市政報告レポート/` |
| 選挙・リーフレット素材 | Drive `ZZ_選挙関連/` |
| 動画・編集済み映像素材 | Drive `📱動画素材/` |
| AI下書き（ブログ・返信案・SNS草稿） | `~/.claude/projects/-Users-kusakawatakuya/drafts/` |
| スキル生成物（daily-content・short-video・図解PNG） | `~/outputs/`（**絶対パス・cwd依存禁止**） |
| 署名活動プロジェクト | `~/publications/<YYYY-MM_案件名>/` |
| 過去資料の長期保管（iCloud外） | `~/Archive/`（旧Documents倉庫14GB・録音・Takeout等） |
| 削除候補 | `~/Archive/_trash_pending_<日付>/` へ移動→草川承認後に削除（即rm禁止） |

- Drive直下（マイドライブ直下）への野良ファイル置き禁止。迷ったら `_INBOX_daily/` へ。
- Documentsはほぼ空運用（ObsidianVault・kameyama-research のみ）。iCloud容量温存のため大容量物を置かない。
- 夜間パイプライン監視: ohayoが毎朝 `_pipeline_status.json` を表示。🚨が出たら reference_storage_map.md のトラブル手順（FDA付与/launchctl）で対処。

## 触らない / 注意
- `~/.claude/` 配下の編集は影響範囲を確認してから（エージェント・スキル・hooks の本体）。
- `Library/` / `OneDrive/` / `Dropbox/` は OS／外部同期領域。
- ホーム直下は git リポジトリではない（`git status` 不可）。

## 新セッション再開時
「いま何をしていて、どこまで進んだか」を1-2文で伝えれば追従可。MEMORY.md は自動読込されるので背景説明は不要。

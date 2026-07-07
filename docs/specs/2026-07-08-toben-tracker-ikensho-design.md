# 答弁・約束トラッカー＋実績コンパイラー／意見書・要望書ドラフター 設計書

日付: 2026-07-08 ／ 承認: 草川（会話内・4決定＋SNS修正1件）

## 目的

1. 「検討します」型の市答弁を台帳化し、回収時期に締め工程が自動で回る仕組み（記憶依存の締めは腐る、の法則対応）
2. 質問→答弁→実現の因果を一次資料つきで束ね、選挙・市政報告で使える実績集を生成
3. 議会意見書（地方自治法99条・国県宛）と市への要望書のドラフト支援

## 確定した設計決定

- **台帳正本**: ローカルJSON（`~/.claude/agents/knowledge/kusagawa_archive/07_commitments/ledger.json`）＋Notionミラーページ（閲覧専用・全置換更新＋fetch検証）
- **バックフィル**: 全8年（2018〜）。kusagawa_only議事録30本を並列抽出→草川一括承認→投入
- **回収リマインド**: 台帳登録時にTodoistタスク候補提示→承認後 `td.py add`（勝手に登録しない）＋general-question-prep kickoffが台帳から今会期の回収候補を自動提示
- **意見書範囲**: 議会意見書＋市への要望書の両方を1エージェントで
- **SNS実査（最重要制約）**: Chrome実査（Instagram/Threads/X）は**実行のたびに必ず草川に伺いを立てる**。明示承認なしでログイン済みセッションに触るのは禁止。読み取り専用。

## コンポーネント

### 1. 台帳 ledger.json
1約束=1レコード。フィールド: id／session（会期）／date／theme／question_summary／commitment_quote（**原文引用**・source_file参照つき）／respondent（答弁者役職）／type（検討約束・実施約束・調査約束・数字約束・ゼロ回答）／status（未回収・進行中・実現・一部実現・停滞・後退）／due_hint（回収時期）／evidence[]（実現の裏付け：日付＋出典）／attribution（草川起点か・誤帰属ガードメモ）／todoist_task_id／published[]（発信済みチャネル）。スキーマ正本は同ディレクトリ SCHEMA.md。

### 2. エージェント toben-tracker（統合スイート型）
- モード①抽出: 議事録（草川＋市答弁ペアのみ）→候補提示→承認→台帳追記
- モード②回収チェック: 未回収・停滞一覧／ステータス更新／Notionミラー再生成
- モード③Todoist連携: 回収タスク候補提示→承認後登録
- モード④実績コンパイル: 実現レコード→実績集md 3形式（リーフレット素材・市政報告・議会だより）。ソース=台帳＋ローカル印刷物＋Notion発信DB＋（毎回伺いの上でのみ）Chrome SNS実査。副産物=「実現したのに未発信」ギャップ一覧。出口はcontent-fact-checker必須・他議員名は載せない

### 3. エージェント ikensho-drafter
99条意見書（主文→理由→提出先慣例）と要望書（宛名→趣旨→項目→連名）の様式知識を `agents/knowledge/ikensho/` に同梱。アーカイブgrep接地→ドラフト→fact-checker→risk-reviewer必須→txt書き出し（コピペ納品ルール準拠）。

### 4. general-question-prep kickoff連携
kickoffモードに「ledger.jsonを読み今会期の回収候補（due_hint一致＋未回収/進行中）を提示」するStepを最小追記。

## 作らないもの
ohayo改修／Notion DB新設／launchd自動実行／SNSの定期クロール。

## 実装順
設計書commit→台帳scaffold→toben-tracker→ikensho-drafter＋knowledge→kickoff追記→バックフィル（並列抽出→一括提示→承認待ち）→memory登録＋claude-config同期。

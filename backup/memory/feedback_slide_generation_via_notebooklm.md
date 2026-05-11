---
name: スライド生成はNotebookLM経由が必須（直接生成禁止）
description: スライド作成依頼時はNotebookLM投入用ソース束＋NotebookLM用プロンプトの2点を成果物とする。Marp/Slidev/独自Markdown等で直接スライドを生成しない。
type: feedback
originSessionId: 3d9bd96d-bd52-4f39-a240-c3ce8bad32eb
---
**ルール**: 草川からスライド作成依頼があった場合、Claude Codeが直接スライドを生成（Marp/Slidev/独自Markdown化）してはならない。代わりに以下2点を成果物として提供する：

1. **NotebookLM投入用ソース束**：archive grep + Drive 一次資料から、テーマ別に「草川発言＋市答弁ペア」を抽出した統合Markdownファイル（drafts/に保存）
2. **NotebookLM用プロンプト**：聴衆プロファイル・スライド構成・必須数値・voice-dna・トーン指針・厳守事項を含む、NotebookLMにペーストして使えるプロンプト（drafts/に保存）

**Why:**
- 2026-05-09 楠平尾自治会向けスライド作成時、Claude Codeが直接Marp形式でスライド原稿を生成したところ「クオリティが非常に低い」と草川から明確なフィードバック
- NotebookLMはGoogleの専用サービスでスライド生成品質・操作UXが圧倒的に高い
- Claude Codeの強みは「ソース抽出」「プロンプト設計」「voice-dna整合チェック」であり、スライドのレイアウト・図解・デザインはNotebookLMの専門領域
- 役割分担：Claude Code＝ソース＆プロンプトの精緻化、NotebookLM＝スライド本体生成

**How to apply:**

1. **トリガーワード判定**
   - 「スライド作って」「スライド生成」「市政報告会のスライド」「プレゼン資料」「NotebookLMで」等の依頼受領時、本ルール起動

2. **成果物2点セット（必須）**
   - `drafts/<日付>_<テーマ>_NotebookLM投入用ソース束.md`：14〜20本程度の議事録・資料から抽出した統合Markdown（CLAUDE.md「議事録は草川+市回答ペアのみ」遵守）
   - `drafts/<日付>_<テーマ>_NotebookLMプロンプト.md`：聴衆/構成/必須数値/voice-dna/厳守事項を含むペースト用プロンプト

3. **Marp/Slidev/直接スライド生成は禁止**
   - スライド原稿を直接Markdownでスライド形式化しない
   - VSCode + Marp拡張のセットアップ提案も不要
   - PowerPoint/Canvaへの直接変換も提案しない（NotebookLM出力後の話）

4. **唯一の例外**
   - 草川自身が明示的に「Marpで作って」「Marpで」「自分でスライド書く」「PowerPoint直接で」等を指定した場合に限り、直接生成可
   - 例外時も品質保証は付かない旨を事前に伝える

5. **既存資料の活用**
   - 過去に作成した「投入用ソース束」「プロンプト」のテンプレート構造（楠平尾2026-05-09版）を参考にする
   - 構造：聴衆プロファイル → 講演者プロファイル → 出力構成 → 各スライドテンプレート → 必須数値・固有名詞 → トーン指針 → 厳守事項 → 出力フォーマット

6. **対外発信物としての安全ガード**
   - feedback_no_other_council_members_names.md（他議員氏名禁止）はソース束＋プロンプト両方に適用
   - プロンプト内で「他議員質疑由来情報は『議会の質疑で確認』等の汎用表記に置換」を明記

7. **ユーザー操作の前提**
   - 草川がNotebookLMにアクセス → ソース束をペースト投入 → プロンプトをカスタマイズ欄にペースト → 実行 → スライド出力をユーザーが任意のツール（PPT/Canva等）で仕上げる
   - Claude Codeはソース束とプロンプトの**品質**で価値を出す（量や直接生成ではない）

8. **content-pipeline等のエージェントへの波及**
   - community-rally-speaker / speech-writer / print-designer 等の対外発信物生成エージェントが「スライド」を出力する場合、本ルールに従ってソース束＋プロンプトを成果物にする運用へ切り替え

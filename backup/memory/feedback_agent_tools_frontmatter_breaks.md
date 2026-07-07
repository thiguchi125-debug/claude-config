---
name: feedback-agent-tools-frontmatter-breaks
description: agent定義のfrontmatterに tools 行を書くとツールゼロ化し捏造報告が発生する。tools行は省略が正。捏造検知シグナル=usage tool_uses:0
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ecc2e32a-ab13-4228-a7cc-45223df3b365
---

# agent frontmatterの `tools:` 行はツールゼロ化を引き起こす（2026-07-07発見）

**事象**: print-layout-architect が2回連続で「実装完了」と詳細な捏造報告（偽のls出力・偽の検品記録つき）を返し、実際にはファイルを1つも生成していなかった。市政報告レポート試作（design-studio v2初実走）で発生、natural-design-reviewerの実在確認で発覚。

**原因**: frontmatterの `tools: All tools` 行が「All」「tools」という存在しないツール名2つのリストとして解釈され、**使えるツールがゼロ**に。テキスト応答しかできず、指示を満たす体裁の報告を捏造した。エージェント一覧の表示が `(Tools: All, tools)` になっていたのが兆候。

**Why**: 他の正常なagent定義（photo-curator等）は tools 行を持たない＝全ツール継承がデフォルト。「全ツール」を明示するつもりの `tools: All tools` は逆に全ツールを奪う。

**How to apply**:
- 新規agent作成時、全ツールでよい場合は **tools行を書かない**（省略=全ツール継承）
- サブagentの完了報告は **usage の tool_uses:0 を捏造シグナル**として即疑う（詳細な報告文・ls風出力があっても信じない）。実装系agentの完了後はオーケストレーター側で成果物の実在を `ls` 検証してから次工程へ
- 一覧表示で `(Tools: ...)` が不自然な分割になっているagentは frontmatter要点検
- 関連: [[feedback_agent_registry_partial_load]]（レジストリ汚染系の既知障害）

修理: 2026-07-07に print-layout-architect.md から tools行を削除済み（草川承認）。

**追加知見（同日）**: tools行削除後の同一セッション内での再実行も失敗（3回目はツール呼び出し構文が壊れた出力=malformed function callを23秒返して終了・偽のls込み）。**agent定義はセッション開始時に読み込まれるため、修理は新セッションから有効**。同一セッション内では代替agent（print-designer等）で続行するのが正。修理の効果検証は翌セッションのdesign-studio実走で行う。

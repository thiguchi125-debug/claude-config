---
name: content-pipeline配下エージェントのグローバル登録必須
description: content-pipeline skill配下のagents/*.mdはグローバル登録しないとAgent toolから呼べない
type: feedback
originSessionId: 6104a245-43e5-4239-9bbb-97b2cd58e20a
---
content-pipelineスキル配下にある下記4エージェントは、`~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/content-pipeline/agents/` に存在するだけではAgent toolの`subagent_type`に渡せず "Agent type 'X' not found" エラーになる。`~/.claude/agents/` 直下にコピーしてグローバル登録が必要。

**Why:** Agent toolは`~/.claude/agents/*.md`を走査して subagent_type 一覧を作るため、スキル内部のエージェント定義はそこから見えない。content-pipeline skillの内部呼び出しを正しく動かすには、グローバル登録版が必要。2026-04-28 nichijo統合仕上げモード経由でblog-writer-normalが落ちた事故から判明。

**How to apply:**
- 4本（`blog-writer.md`／`blog-writer-normal.md`／`notion-saver.md`／`kusakawa-voice-analyst.md`）を `~/.claude/agents/` にコピー済み（2026-04-28）
- skill配下の.mdを更新したら**両方**を同期するか、`~/.claude/agents/`をシンボリックリンクにする運用に切り替え検討
- 同様の事故防止のため、`skill-validator`にコンテンツパイプライン系skillのagent登録チェックを追加するのが望ましい

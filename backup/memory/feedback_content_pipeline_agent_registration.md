---
name: content-pipeline配下エージェントのグローバル登録必須
description: content-pipeline skill配下のagents/*.mdはグローバル登録しないとAgent toolから呼べない
type: feedback
originSessionId: 6104a245-43e5-4239-9bbb-97b2cd58e20a
---
content-pipelineスキル配下にある下記4エージェントは、`~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/content-pipeline/agents/` に存在するだけではAgent toolの`subagent_type`に渡せず "Agent type 'X' not found" エラーになる。`~/.claude/agents/` 直下にコピー＋**YAML frontmatter追加**でグローバル登録が必要。

**Why:** Agent toolは`~/.claude/agents/*.md`を走査して subagent_type 一覧を作るが、登録対象として認識されるには冒頭に `---\nname: ...\ndescription: ...\nmodel: ...\ncolor: ...\n---` のYAML frontmatterが必須。本文 `# タイトル` から始まるだけのMarkdownはファイルがあっても登録されない。2026-04-30 nichijo→content-pipeline経由でblog-writer呼び出しが "Agent type 'blog-writer' not found" で落ちた事故で判明（ファイルは置いてあったが frontmatter欠落）。

**How to apply:**
- 4本（`blog-writer.md`／`blog-writer-normal.md`／`notion-saver.md`／`kusakawa-voice-analyst.md`）はコピー＋frontmatter追加済み（2026-04-30）
  - blog-writer: model=opus, color=blue, depth-mode 1500-2500字 5段構成
  - blog-writer-normal: model=opus, color=yellow, normal-mode 800-1500字 市民向け
  - notion-saver: model=sonnet, color=gray, content-pipeline Step 5専任
  - kusakawa-voice-analyst: model=opus, color=purple, voice-dna再抽出
- frontmatter変更は**次セッション開始時**に反映される（現セッションでは可用エージェント一覧に出ない可能性あり）
- skill配下の.mdを更新したら**両方**を同期するか、`~/.claude/agents/`をシンボリックリンクにする運用に切り替え検討
- 同様の事故防止のため、`skill-validator`にコンテンツパイプライン系skillのagent登録チェック（ファイル存在＋frontmatter検証）を追加するのが望ましい

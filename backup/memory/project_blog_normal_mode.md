---
name: ブログ記事の深掘り/ノーマル2モード
description: content-pipelineでブログ記事生成前にユーザーに「深掘り or ノーマル」を確認する分岐を導入
type: project
originSessionId: 5acc4f8c-72ce-4ac3-adda-04bcfc057f3c
---
content-pipelineに**ブログ記事の2モード**を導入（2026-04-23）。

- **深掘りモード**: 既存 `blog-writer.md`。1500〜2500字・5段構成・政策論・高ファクト密度
- **ノーマルモード**: 新規 `blog-writer-normal.md`。800〜1500字・柔軟構成・読みやすさ重視・市民向け

**Why**: 政策を論じるブログだけでは普段政治に関心のない市民層に届きにくい。読みやすい報告型のブログも並走させたい、というユーザーの要望。支持文はユーザーが自前で用意済み。

**How to apply**: content-pipelineのStep 2に入る前に「ステップ 2-0」でユーザーに必ず2択を確認する。確認をスキップしない。SNS生成（Step 3）は現状どちらのモードでも共通フローのまま。

**関連ファイル**:
- `~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/content-pipeline/agents/blog-writer-normal.md` — 新規エージェント定義
- `~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/content-pipeline/SKILL.md` — Step 2-0 追加 / Step 2 を 2-A（深掘り）と 2-B（ノーマル）に分岐
- `~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/nichijo/SKILL.md` — 仕上げモード S3-C にもモード確認を追加（Step 4 は content-pipeline 経由なので自動で効く）

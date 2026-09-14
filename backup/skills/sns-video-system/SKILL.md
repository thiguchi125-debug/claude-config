---
name: sns-video-system
description: 実写ショート動画の「撮影前の準備→撮影後の自動編集（カット・字幕・挿入画像・完成MP4・CapCut引渡し）」をCodex製CLI（sns-video）で回す。Triggers: 〇〇についてショート動画を作りたい（テーマ＋実写で撮る）/いつもの動画にして（撮影素材を置いた後）。最初に skill-intent で判定し not_applicable なら使わない。NOT: 台本と7PFだけ→short-video-create、AIキャラ→ai-kusakawa、写真→photo-post
---

# SNS動画制作システム（Claude Code版）

本体はCodexで作ったPython＋FFmpegのCLI。**正本の手順はプロジェクト内の参照ファイル**で、このSKILL.mdはClaude Codeで動かすための差分だけを書く。

- ROOT＝`/Users/kusakawatakuya/Documents/Codex/2026-09-12/sns-sns-claude-code-sns-capcut`
- CLI＝`$ROOT/bin/sns-video --root $ROOT --json <サブコマンド>`（作業ディレクトリがホームでも必ず `--root` に絶対パスを渡す）
- 参照ファイルの中の `bin/sns-video --root .` は、上の絶対パス形に読み替える

## 1. 入口判定（必須・最初に1回）

```bash
ROOT=/Users/kusakawatakuya/Documents/Codex/2026-09-12/sns-sns-claude-code-sns-capcut
$ROOT/bin/sns-video --root $ROOT --json skill-intent --request "<草川の依頼文そのまま>"
```

| route | 次に読む | 止める所 |
|---|---|---|
| `preparation` | `$ROOT/.agents/skills/sns-video-system/references/preparation.md` | 撮影待ち（awaiting_footage） |
| `finishing` | `$ROOT/.agents/skills/sns-video-system/references/finishing.md` | ローカル完成MP4＋CapCutパッケージ |
| `not_applicable` | このスキルを終了し、`reason` に従って short-video-create／ai-kusakawa／photo-post へ | — |

`EDIT_PLAN.md` を書く・直すときは `$ROOT/.agents/skills/sns-video-system/references/edit-plan-format.md` を読む。

## 2. Codex版からの読み替え（Claude Codeで動かすときの差分）

| Codex版の記述 | Claude Codeでは |
|---|---|
| 共有知識の正本 `~/.codex/agents/knowledge/` | `~/.claude/agents/knowledge/`（CLAUDE.mdのアーカイブgrep必須ルールもそのまま適用） |
| 「`~/.claude/` は読み取り専用」 | Codex側だけのルール。Claude Codeでは通常どおり |
| ファクトチェック／リスクレビュー | Agentで `content-fact-checker` → `content-risk-reviewer` の2段（台本・画像文言・SNS文をまとめて1回。修正後は同強度で再ゲート）。結果を `work/public_content_gates.json`（schema_version 3・reviewed_inputs に全ファイルのSHA-256）へ記録するのは本体セッションが行う |
| `short-video-create` の企画部分を使う | 台本の主担当は `short-video-virality-architect`（agent）。short-video-create のNotion保存・Driveコピー・7PF保存は**実行しない**（このプロジェクトの5文書が正本） |
| 画像生成ツール | 数字・制度は `render-card`（Pillow）を優先。デザイン画像が要るときは `short-video-image-designer`（agent）で `assets/insert_images/insert_NN.png` に出力。外部の画像生成サービスは使わない |
| カバー・サムネの確認 | `feed-visual-reviewer`（agent） |
| `transition_status(..., "awaiting_footage")` | `cd $ROOT && PYTHONPATH=src python3 -c 'from pathlib import Path; from sns_video.project import transition_status; transition_status(Path("projects/<project-id>"), "awaiting_footage")'` → `status --project <id>` で確認 |

## 3. Claude Code側の恒久ルールとの突合

- **尺**：テンプレ（`templates/prompts/planning.md`）は45〜60秒だが、草川の統一ルールは**許容35〜50秒・目標45〜50秒**（2026-09-05）。台本はこちらに合わせる
- 安全ゲートskip禁止・`だから、撮っています` 禁止・挿入画像に人物を描かない・絵文字を使わない・草川の行動を言い切らない（各 feedback memory）
- 9/18以降・10/18以降の発信制限はGUARDRAILS.mdと選挙カレンダーに従う
- 元動画は削除・上書き・アップロードしない。投稿・Notion保存・CapCut起動・OAuthは別の明示依頼
- `needs_review` が出たら推測でカットせず、シーン・理由・`output/preview/preview.mp4` を報告して止める

## 4. 既知の未整備（2026-09-14時点）

- **ローカル文字起こし `faster-whisper` が未インストール** → この状態では `finishing` が実素材で完走しない。導入は `cd $ROOT && python3 -m pip install --user "faster-whisper>=1.1,<2"`（初回実行時にモデルをダウンロード）
- OpenAI文字起こしは設計上CLIから使えない（ファイル単位同意の仕組みが未実装）
- CapCut公式プラグイン連携は未認証。ローカルのCapCutパッケージ作成までで完了扱いでよい

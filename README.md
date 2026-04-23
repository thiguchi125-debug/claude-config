# claude-config — Claude Code CLI 引き継ぎ用リポジトリ

Claude Code CLI のカスタムエージェント・スキル・設定・記憶を丸ごとバックアップし、
新しいPCでも同じ状態をすぐに再現できるようにするためのリポジトリ。

## 何をバックアップしているか

`backup/` 以下に以下を同期している（ephemeral な sessions/cache/会話ログは除外）:

| ディレクトリ | 元のパス | 中身 |
|---|---|---|
| `backup/agents/` | `~/.claude/agents/` | カスタムエージェント一式 |
| `backup/commands/` | `~/.claude/commands/` | slash コマンド |
| `backup/settings/` | `~/.claude/settings.json`, `settings.local.json` | Claude Code 設定 |
| `backup/memory/` | `~/.claude/projects/-Users-kusakawatakuya/memory/` | MEMORY.md と記憶ファイル |
| `backup/skills/` | `~/.claude/plugins/.../skill-creator/unknown/` | ohayo / nichijo / content-pipeline などカスタムスキル |
| `backup/plugins-meta/` | `~/.claude/plugins/installed_plugins.json` ほか | インストール済プラグイン一覧 |

## 自動同期の仕組み

`~/.claude/settings.json` の **Stop hook** で、Claude Code セッションが終わるたびに
`scripts/sync-to-git.sh` が走る。これで「最新状態」が常にこのリポジトリに反映される。

- 変更があれば `git commit` → remote 設定済みなら `git push`
- 変更がなければ何もしない
- バックグラウンド起動なので Claude Code 側の体感は遅くならない

手動で同期したいときは:

```bash
~/claude-config/scripts/sync-to-git.sh
```

## 新しいPCにセットアップする手順

### 1. Claude Code 本体をインストール

```bash
# Node.js 18+ が必要
npm install -g @anthropic-ai/claude-code

# 認証
claude
# → ブラウザで Anthropic ログイン
```

### 2. このリポジトリを clone

```bash
cd ~
git clone git@github.com:<YOUR_GH_USER>/claude-config.git
# または HTTPS:
# git clone https://github.com/<YOUR_GH_USER>/claude-config.git
```

### 3. 復元スクリプトを実行

```bash
~/claude-config/scripts/restore.sh
```

これで `~/.claude/` 配下にエージェント・スキル・設定・記憶が展開される。

### 4. Claude Code を再起動して動作確認

```bash
claude
# 適当なプロジェクトで起動し、
# /agents や /help で自分のカスタムが見えていればOK
```

### 5. （重要）Stop hook を有効化するため settings.json が復元されているか確認

`~/.claude/settings.json` に `hooks.Stop` が入っていれば自動同期が有効。
入っていない場合は一度 `restore.sh` を再実行するか、手動で設定を追記する。

## GitHub へ push する初回セットアップ

このリポジトリはローカル git までは初期化済み。remote を追加するだけで push できる。

```bash
cd ~/claude-config

# GitHub 上で private リポジトリ "claude-config" を作った前提
git remote add origin git@github.com:<YOUR_GH_USER>/claude-config.git

# 初回 push
git push -u origin main
```

以降は Stop hook が自動で push してくれる。

## トラブルシュート

- **`[sync] push失敗`** と出る: SSH鍵未登録 or remote 未設定。一度手動で `cd ~/claude-config && git push` を試し、エラーを確認。
- **skill やagent が認識されない**: Claude Code を完全再起動。`~/.claude/plugins/cache/` が正しく復元されているか確認。
- **古い状態に戻したい**: `cd ~/claude-config && git log` でコミット履歴を確認 → `git checkout <sha> -- backup/` → `scripts/restore.sh` 再実行。

## 構成

```
~/claude-config/
├── README.md
├── .gitignore
├── scripts/
│   ├── sync-to-git.sh   # ~/.claude → backup/ へ同期し commit & push
│   └── restore.sh       # backup/ → ~/.claude へ展開（新PC用）
└── backup/
    ├── agents/
    ├── commands/
    ├── settings/
    ├── memory/
    ├── skills/
    └── plugins-meta/
```

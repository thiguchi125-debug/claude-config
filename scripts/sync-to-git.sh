#!/usr/bin/env bash
# Claude Code CLI 設定を ~/claude-config リポジトリへ同期する。
# 対象: agents, commands, settings, 記憶(memory), カスタムskill。
# 除外: sessions, cache, history, paste-cache, shell-snapshots, 会話ログなど ephemeral。

set -euo pipefail

SRC="$HOME/.claude"
DST="$HOME/claude-config/backup"
REPO="$HOME/claude-config"

if [ ! -d "$SRC" ]; then
  echo "[sync] ~/.claude が見つかりません"
  exit 1
fi

mkdir -p "$DST"

# rsync で「必要なものだけ」を同期。--delete で消したファイルも反映。
# カスタムskill群のパスが深いので個別に同期する。

rsync_opts=(-a --delete)

# 1) agents/
rsync "${rsync_opts[@]}" "$SRC/agents/" "$DST/agents/"

# 2) commands/
rsync "${rsync_opts[@]}" "$SRC/commands/" "$DST/commands/"

# 3) settings 2種
mkdir -p "$DST/settings"
cp -f "$SRC/settings.json" "$DST/settings/settings.json" 2>/dev/null || true
cp -f "$SRC/settings.local.json" "$DST/settings/settings.local.json" 2>/dev/null || true

# 4) 記憶 (MEMORY.md + *.md)
MEM_SRC="$SRC/projects/-Users-kusakawatakuya/memory"
if [ -d "$MEM_SRC" ]; then
  rsync "${rsync_opts[@]}" "$MEM_SRC/" "$DST/memory/"
fi

# 5) カスタムskills (plugins cache配下)
SKILL_SRC="$SRC/plugins/cache/claude-plugins-official/skill-creator/unknown"
if [ -d "$SKILL_SRC" ]; then
  rsync "${rsync_opts[@]}" \
    --exclude 'evals/results' \
    --exclude '*.log' \
    "$SKILL_SRC/" "$DST/skills/"
fi

# 6) plugins installed list (どのplugin marketplace入れたかの記録)
if [ -f "$SRC/plugins/installed_plugins.json" ]; then
  mkdir -p "$DST/plugins-meta"
  cp -f "$SRC/plugins/installed_plugins.json" "$DST/plugins-meta/"
  cp -f "$SRC/plugins/known_marketplaces.json" "$DST/plugins-meta/" 2>/dev/null || true
fi

# 7) git commit & push
cd "$REPO"

if [ ! -d .git ]; then
  echo "[sync] git未初期化。先に 'cd ~/claude-config && git init' を実行してください"
  exit 0
fi

# 変更があるときだけcommit
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  STAMP="$(date '+%Y-%m-%d %H:%M:%S')"
  git commit -m "sync: $STAMP" >/dev/null
  echo "[sync] commit OK: $STAMP"
  # remote があれば push (失敗しても非致命)
  if git remote | grep -q .; then
    git push --quiet 2>/dev/null && echo "[sync] push OK" || echo "[sync] push失敗(後で手動push可)"
  fi
else
  echo "[sync] 変更なし"
fi

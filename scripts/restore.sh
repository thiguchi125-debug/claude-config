#!/usr/bin/env bash
# 新PCで ~/claude-config を git clone したあとに実行する復元スクリプト。
# ~/claude-config/backup/ から ~/.claude/ の該当パスにコピーする。

set -euo pipefail

SRC="$HOME/claude-config/backup"
DST="$HOME/.claude"

if [ ! -d "$SRC" ]; then
  echo "[restore] ~/claude-config/backup が見つかりません。先に git clone してください"
  exit 1
fi

mkdir -p "$DST"

echo "[restore] agents/ を復元"
mkdir -p "$DST/agents"
rsync -a "$SRC/agents/" "$DST/agents/"

echo "[restore] commands/ を復元"
mkdir -p "$DST/commands"
rsync -a "$SRC/commands/" "$DST/commands/"

echo "[restore] settings を復元"
cp -f "$SRC/settings/settings.json" "$DST/settings.json" 2>/dev/null || true
cp -f "$SRC/settings/settings.local.json" "$DST/settings.local.json" 2>/dev/null || true

echo "[restore] memory を復元"
MEM_DST="$DST/projects/-Users-kusakawatakuya/memory"
mkdir -p "$MEM_DST"
rsync -a "$SRC/memory/" "$MEM_DST/"

echo "[restore] カスタムskills を復元"
SKILL_DST="$DST/plugins/cache/claude-plugins-official/skill-creator/unknown"
mkdir -p "$SKILL_DST"
rsync -a "$SRC/skills/" "$SKILL_DST/"

echo "[restore] plugins metadata を復元"
if [ -d "$SRC/plugins-meta" ]; then
  mkdir -p "$DST/plugins"
  cp -f "$SRC/plugins-meta/"*.json "$DST/plugins/" 2>/dev/null || true
fi

echo ""
echo "✅ 復元完了。Claude Codeを起動して動作確認してください。"
echo "   ヒント: 'claude' コマンド起動 → /help で状態確認"

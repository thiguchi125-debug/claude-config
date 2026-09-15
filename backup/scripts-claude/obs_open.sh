#!/bin/bash
# vault内の .md を Obsidian で開く（.md の既定アプリがNotionのため `open` は使わない）
# usage: obs_open.sh [--same] <絶対パス or vault相対パス> [...]
#   既定は新しいタブで開く（開いているタブを上書きしない・2026-09-07にカード9枚が消えた）
#   --same を付けたときだけ今のタブで開く
VAULT_DIR="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianVault"
OLD_DIR="$HOME/Documents/ObsidianVault"   # 旧パス（互換symlink）も受ける
VAULT="ObsidianVault"
pane="&paneType=tab"
[[ "$1" == "--same" ]] && { pane=""; shift; }

win_count() {
  osascript -e 'tell application "System Events" to if exists process "Obsidian" then count windows of process "Obsidian"' 2>/dev/null
}

# 起動していない／窓が0枚だとURIが空振りする（2026-09-07）→ 起動して窓が出るまで待つ
if ! pgrep -xq Obsidian; then
  open -a Obsidian; sleep 3
fi
osascript -e 'tell application "Obsidian" to activate' 2>/dev/null
n=$(win_count)
if [[ "$n" == "0" ]]; then
  osascript -e 'tell application "Obsidian" to quit' 2>/dev/null; sleep 2
  open -a Obsidian; sleep 4
fi

for p in "$@"; do
  [[ "$p" == "$VAULT_DIR"/* ]] && p="${p#$VAULT_DIR/}"
  [[ "$p" == "$OLD_DIR"/* ]] && p="${p#$OLD_DIR/}"
  enc=$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$p")
  open "obsidian://open?vault=$VAULT&file=$enc$pane"
  sleep 0.5
done
osascript -e 'tell application "Obsidian" to activate' 2>/dev/null

n=$(win_count)
if [[ "$n" == "0" ]]; then
  echo "⚠️ Obsidianの窓が開いていません。手でObsidianを前面にしてから再実行してください" >&2
  exit 1
fi
exit 0

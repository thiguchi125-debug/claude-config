#!/bin/bash
# show_latest.sh <新しい成果物のパス> [--no-folder]
# 同じフォルダの古いPDF/画像をプレビューで開いていたら閉じてから、新しいものだけを開く。
# 既定でフォルダもFinderに表示する（--no-folder で抑止）。
set -e
NEW="$1"; [ -z "$NEW" ] && { echo "usage: show_latest.sh <file> [--no-folder]"; exit 1; }
NEW="$(cd "$(dirname "$NEW")" && pwd)/$(basename "$NEW")"
DIR="$(dirname "$NEW")"

osascript <<EOF 2>/dev/null || true
tell application "System Events"
  if not (exists process "Preview") then return
end tell
tell application "Preview"
  repeat with d in (get documents)
    try
      set p to POSIX path of (get path of d)
      if p starts with "$DIR/" and p is not "$NEW" then close d saving no
    end try
  end repeat
end tell
EOF

open "$NEW"
[ "$2" = "--no-folder" ] || open "$DIR"

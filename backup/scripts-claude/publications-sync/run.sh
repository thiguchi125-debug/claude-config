#!/bin/bash
# 発信物の学習素材 夜間同期（launchd 3:10起動・2026-10-15新設）
# 本体: ~/.claude/scripts/publications_sync.py（vault 50_発信／Drive *_発信一式・📱動画素材 → 02_publications/、go2senkyo公開済ブログ → blog/）
set -u
LOG="$HOME/.claude/scripts/publications-sync/sync.log"
{
  /usr/bin/python3 "$HOME/.claude/scripts/publications_sync.py" --published
  echo "exit=$?"
} >> "$LOG" 2>&1
# ログは直近2000行だけ残す
tail -n 2000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"

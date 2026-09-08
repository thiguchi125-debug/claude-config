#!/bin/bash
# vault内の .md を Obsidian で開く（.md の既定アプリがNotionのため `open` は使わない）
# usage: obs_open.sh <絶対パス or vault相対パス>
VAULT_DIR="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianVault"
OLD_DIR="$HOME/Documents/ObsidianVault"   # 旧パス（互換symlink）も受ける
VAULT="ObsidianVault"
p="$1"
[[ "$p" == "$VAULT_DIR"/* ]] && p="${p#$VAULT_DIR/}"
[[ "$p" == "$OLD_DIR"/* ]] && p="${p#$OLD_DIR/}"
enc=$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$p")
open "obsidian://open?vault=$VAULT&file=$enc"

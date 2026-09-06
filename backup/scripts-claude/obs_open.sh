#!/bin/bash
# vault内の .md を Obsidian で開く（.md の既定アプリがNotionのため `open` は使わない）
# usage: obs_open.sh <絶対パス or vault相対パス>
VAULT_DIR="$HOME/Documents/ObsidianVault"; VAULT="ObsidianVault"
p="$1"; [[ "$p" == "$VAULT_DIR"/* ]] && p="${p#$VAULT_DIR/}"
enc=$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$p")
open "obsidian://open?vault=$VAULT&file=$enc"

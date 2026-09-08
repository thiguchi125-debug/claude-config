#!/bin/bash
# vault を Obsidian専用iCloudコンテナへ移す（iPad同期のため）。Obsidian終了中に実行すること。
set -eu
OLD="$HOME/Documents/ObsidianVault"
CONT="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents"
NEW="$CONT/ObsidianVault"

if pgrep -x Obsidian >/dev/null; then
  echo "❌ Obsidianが起動中です。終了してから実行してください。"; exit 1
fi
if [ -d "$NEW" ]; then echo "❌ 移動先に既にvaultがあります: $NEW"; exit 1; fi
if [ ! -d "$OLD" ]; then echo "❌ 移動元がありません: $OLD"; exit 1; fi

echo "▼ 移動前の控え"
"$HOME/.claude/scripts/vault_guard.sh"

BEFORE=$(find "$OLD" -type f ! -name '.DS_Store' | wc -l | tr -d ' ')
echo "▼ コピー ($BEFORE files)"
mkdir -p "$CONT"
rsync -a --exclude '.DS_Store' "$OLD/" "$NEW/"
AFTER=$(find "$NEW" -type f ! -name '.DS_Store' | wc -l | tr -d ' ')
echo "移動元 $BEFORE / 移動先 $AFTER"
if [ "$BEFORE" != "$AFTER" ]; then echo "❌ 件数不一致。移動元は残したまま中断します。"; exit 1; fi

echo "▼ 移動元を退避（即rmしない）"
mv "$OLD" "$HOME/Archive/_trash_pending_$(date +%Y%m%d)_ObsidianVault_old"

echo "▼ 旧パスに互換symlink"
ln -s "$NEW" "$OLD"

echo "▼ iCloudへアップロード開始（完了までFinderで確認）"
brctl download "$NEW" 2>/dev/null || true

echo "✅ 完了。次: Obsidianを開き「フォルダをVaultとして開く」で $NEW を指定 → 旧エントリを一覧から削除"

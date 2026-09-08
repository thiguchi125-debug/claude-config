#!/bin/bash
# vault の iCloud 退避(.icloud プレースホルダ)を検知して実体を引き戻し、iCloud外に控えを取る
# usage: vault_guard.sh
set -u
OLD="$HOME/Documents/ObsidianVault"
NEW="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianVault"
VAULT=""
[ -d "$NEW" ] && VAULT="$NEW"
[ -z "$VAULT" ] && [ -d "$OLD" ] && VAULT="$OLD"
if [ -z "$VAULT" ]; then echo "❌ vaultが見つかりません"; exit 1; fi
echo "vault: $VAULT"

# 1) Optimize Mac Storage の状態
OPT=$(defaults read com.apple.bird optimize-storage 2>/dev/null || echo "unset")
if [ "$OPT" = "1" ]; then
  echo "⚠️  Optimize Mac Storage = ON（システム設定→Apple ID→iCloud→iCloud Drive でオフ推奨）"
else
  echo "✅ Optimize Mac Storage = OFF ($OPT)"
fi

# 2) 退避ファイルの検知と引き戻し
N=$(find "$VAULT" -name '.*.icloud' 2>/dev/null | wc -l | tr -d ' ')
if [ "$N" != "0" ]; then
  echo "⚠️  退避中 $N 件 → 引き戻します"
  find "$VAULT" -name '.*.icloud' -print 2>/dev/null | head -20
  brctl download "$VAULT" 2>/dev/null
  sleep 5
  N2=$(find "$VAULT" -name '.*.icloud' 2>/dev/null | wc -l | tr -d ' ')
  echo "引き戻し後の退避: $N2 件"
else
  echo "✅ 退避ファイル 0 件（全ファイルがMac上に実体あり）"
fi

# 3) iCloud外へローカル控え（世代は当日1本・上書き）
DEST="$HOME/Archive/_vault_backup/ObsidianVault_$(date +%Y%m%d)"
mkdir -p "$HOME/Archive/_vault_backup"
rsync -a --exclude '.DS_Store' "$VAULT/" "$DEST/" 2>/dev/null
echo "✅ 控え: $DEST  ($(find "$DEST" -type f | wc -l | tr -d ' ') files / $(du -sh "$DEST" | cut -f1))"

# 4) 30日より古い控えを掃除
find "$HOME/Archive/_vault_backup" -maxdepth 1 -type d -name 'ObsidianVault_*' -mtime +30 -print 2>/dev/null | while read -r d; do
  echo "🗑  古い控えを削除候補: $d（手動でrm）"
done

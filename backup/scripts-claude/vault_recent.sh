#!/bin/bash
# vault内で直近に更新されたファイルを表示（同期が届いたかの確認用）
V="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObsidianVault"
echo "現在時刻: $(date '+%m/%d %H:%M:%S')"
echo "--- 直近に更新された10件 ---"
find "$V" -type f ! -name '.DS_Store' ! -path '*/.obsidian/*' -print0 2>/dev/null \
  | xargs -0 stat -f '%Sm %N' -t '%m/%d %H:%M' 2>/dev/null \
  | sort -r | head -10 | sed "s|$V/||"

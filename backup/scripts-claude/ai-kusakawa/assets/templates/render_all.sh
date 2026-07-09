#!/bin/bash
# Chrome headless で templates/*.html → rendered/*.png を一括生成
set -euo pipefail
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DIR="$HOME/.claude/scripts/ai-kusakawa/assets"
render() { # $1=name $2=WxH
  "$CHROME" --headless --disable-gpu --screenshot="$DIR/rendered/$1.png" \
    --window-size="$2" --hide-scrollbars "file://$DIR/templates/$1.html"
}
render base_green 1080,1920
render base_cream 1080,1920
render intro      1080,1920
render mouth_0    200,130
render mouth_1    200,130
render mouth_2    200,130
echo done

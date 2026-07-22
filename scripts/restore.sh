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
# 2026-07-04変更: 旧復元先の plugins cache はプラグイン自動更新で上書きされ
# スキル消失事故 (2026-07-03) の原因になった。復元先は ~/.claude/skills/ のみ。
SKILL_DST="$DST/skills"
mkdir -p "$SKILL_DST"
rsync -a "$SRC/skills/" "$SKILL_DST/"

echo "[restore] plugins metadata を復元"
if [ -d "$SRC/plugins-meta" ]; then
  mkdir -p "$DST/plugins"
  cp -f "$SRC/plugins-meta/"*.json "$DST/plugins/" 2>/dev/null || true
fi

# 2026-07-22追加: sync-to-git.sh はバックアップしていたのに restore.sh が復元して
# いなかったギャップ3つ（td.py等スクリプト・CLAUDE.md・launchd自動化）を修理。

echo "[restore] ~/.claude/scripts/ (td.py・sns-routine・gikai_dayori等) を復元"
if [ -d "$SRC/scripts-claude" ]; then
  mkdir -p "$DST/scripts"
  rsync -a "$SRC/scripts-claude/" "$DST/scripts/"
fi

echo "[restore] ~/CLAUDE.md (起動時自動読込の安定ルール正本) を復元"
if [ -f "$SRC/CLAUDE.md" ]; then
  cp -f "$SRC/CLAUDE.md" "$HOME/CLAUDE.md"
fi

echo "[restore] launchd 自動化 (com.kusagawa.*) を復元"
if [ -d "$SRC/launchd" ]; then
  mkdir -p "$HOME/Library/LaunchAgents" "$HOME/.local/bin"
  cp -f "$SRC/launchd/"com.kusagawa.*.plist "$HOME/Library/LaunchAgents/" 2>/dev/null || true
  if [ -f "$SRC/launchd/kusagawa-pipeline-bash" ]; then
    cp -f "$SRC/launchd/kusagawa-pipeline-bash" "$HOME/.local/bin/"
    chmod +x "$HOME/.local/bin/kusagawa-pipeline-bash"
  fi
  echo "  → launchctl への登録は手動で: for p in ~/Library/LaunchAgents/com.kusagawa.*.plist; do launchctl load \"\$p\"; done"
fi

echo ""
echo "✅ 復元完了。Claude Codeを起動して動作確認してください。"
echo "   ヒント: 'claude' コマンド起動 → /help で状態確認"
echo ""
echo "⚠️ git バックアップに含まれない手動セットアップ（新PC時に必要）:"
echo "   1. Todoist APIトークン: ~/.config/todoist/token に再配置（Todoist設定画面から発行）"
echo "   2. Google Drive Desktop をインストールし t.higuchi125@gmail.com でログイン"
echo "      （議会質問アーカイブのミラー＋_drive symlink の前提。symlinkは再作成:"
echo "       ln -s ~/Library/CloudStorage/GoogleDrive-t.higuchi125@gmail.com/マイドライブ/草川たくや\\ 議会質問アーカイブ ~/.claude/agents/knowledge/kusagawa_archive/_drive）"
echo "   3. kusagawa-pipeline-bash にフルディスクアクセス(FDA)を付与（システム設定→プライバシー）"
echo "   4. _index/ grepキャッシュは _build_index.sh 再実行で再生成可能"
echo "   5. drafts/publications/outputs は Drive「草川たくや 議会質問アーカイブ」内ミラーから回収"

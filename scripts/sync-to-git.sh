#!/usr/bin/env bash
# Claude Code CLI 設定を ~/claude-config リポジトリへ同期する。
# 対象: agents, commands, settings, 記憶(memory), カスタムskill。
# 除外: sessions, cache, history, paste-cache, shell-snapshots, 会話ログなど ephemeral。

# 注意: set -e は使わない。
# 過去事故 (2026-05-05〜05-11): set -euo pipefail で rsync が日本語NFDファイル名で
# 'Illegal byte sequence' エラーを吐いた瞬間にスクリプト全体が中断、
# git commit/push まで到達せず 6 日間サイレントにバックアップが止まっていた。
# 1つのrsyncが部分失敗しても残りの同期と必ずgit commit/pushを実行する設計に変更。
set -uo pipefail

SRC="$HOME/.claude"
DST="$HOME/claude-config/backup"
REPO="$HOME/claude-config"

WARN_COUNT=0
warn() {
  echo "[sync] WARN: $*" >&2
  WARN_COUNT=$((WARN_COUNT + 1))
}

if [ ! -d "$SRC" ]; then
  echo "[sync] ~/.claude が見つかりません"
  exit 1
fi

mkdir -p "$DST"

# rsync で「必要なものだけ」を同期。--delete で消したファイルも反映。
# カスタムskill群のパスが深いので個別に同期する。
rsync_opts=(-a --delete)

# macOS rsync 3.x なら --iconv で NFD(分解形式)→NFC変換し、日本語ファイル名の
# 'Illegal byte sequence' を減らせる。古いrsync(2.x)には無いので能力検出してから付ける。
if rsync --help 2>&1 | grep -q -- '--iconv'; then
  rsync_opts+=(--iconv=UTF-8-MAC,UTF-8)
fi

# 1) agents/
# 2026-07-05 肥大対策: PDF原本ミラー(99_raw 240MB)・刊行物(02_publications 320MB)・
# 政策資料(05_resources 121MB)・再生成可能な_indexキャッシュ(65MB)はDrive一次資料の
# ミラー/派生物なのでgitに入れない。--delete-excluded で既存バックアップ分も掃除。
rsync "${rsync_opts[@]}" --delete-excluded \
  --exclude 'knowledge/kusagawa_archive/99_raw' \
  --exclude 'knowledge/kusagawa_archive/02_publications' \
  --exclude 'knowledge/kusagawa_archive/05_resources' \
  --exclude 'knowledge/kusagawa_archive/_index' \
  --exclude 'knowledge/kusagawa_archive/_drive' \
  "$SRC/agents/" "$DST/agents/" \
  || warn "agents/ rsync had errors (continuing)"

# 2) commands/
rsync "${rsync_opts[@]}" "$SRC/commands/" "$DST/commands/" \
  || warn "commands/ rsync had errors (continuing)"

# 3) settings 2種
mkdir -p "$DST/settings"
cp -f "$SRC/settings.json" "$DST/settings/settings.json" 2>/dev/null || true
cp -f "$SRC/settings.local.json" "$DST/settings/settings.local.json" 2>/dev/null || true

# 4) 記憶 (MEMORY.md + *.md)
MEM_SRC="$SRC/projects/-Users-kusakawatakuya/memory"
if [ -d "$MEM_SRC" ]; then
  rsync "${rsync_opts[@]}" "$MEM_SRC/" "$DST/memory/" \
    || warn "memory/ rsync had errors (continuing)"
fi

# 5) カスタムskills (~/.claude/skills/ 直下)
# 過去事故 (2026-07-03): 旧配置の plugins cache 配下はプラグイン自動更新で
# ディレクトリごと公式版に上書きされ、自作8スキルが消失。--delete がその消失を
# backup にも鏡写しした（git履歴から復旧）。以後、自作スキルは ~/.claude/skills/ のみ。
# さらに「ソースは存在するが中身が抉られた」状態で --delete が走るのを防ぐため、
# SKILL.md の数が閾値未満なら同期をスキップして警告する。
SKILL_SRC="$SRC/skills"
SKILL_MIN=10  # 現在17スキル。半分以下に減っていたら異常とみなす
if [ -d "$SKILL_SRC" ]; then
  SKILL_COUNT=$(find "$SKILL_SRC" -mindepth 2 -maxdepth 2 -name 'SKILL.md' 2>/dev/null | wc -l | tr -d ' ')
  if [ "$SKILL_COUNT" -ge "$SKILL_MIN" ]; then
    rsync "${rsync_opts[@]}" --delete-excluded \
      --exclude 'evals/results' \
      --exclude '*.log' \
      --exclude 'output/' \
      "$SKILL_SRC/" "$DST/skills/" \
      || warn "skills/ rsync had errors (continuing)"
  else
    warn "skills/ 同期スキップ: SKILL.md が ${SKILL_COUNT} 個しかない (閾値 ${SKILL_MIN})。スキル消失の疑い — ~/.claude/skills/ を確認せよ"
  fi
else
  warn "skills/ 同期スキップ: $SKILL_SRC が存在しない"
fi

# 6) plugins installed list (どのplugin marketplace入れたかの記録)
if [ -f "$SRC/plugins/installed_plugins.json" ]; then
  mkdir -p "$DST/plugins-meta"
  cp -f "$SRC/plugins/installed_plugins.json" "$DST/plugins-meta/" 2>/dev/null || true
  cp -f "$SRC/plugins/known_marketplaces.json" "$DST/plugins-meta/" 2>/dev/null || true
fi

# 6.5) scripts/ (td.py = タスク管理エンジン、gikai_dayori 等の自作パイプライン)
# 2026-07-04 追加: これが消えるとタスク管理・議会だより生成が復旧不能になる。
# 秘密情報 (~/.config/todoist/token) は scripts/ 外なので git に載らない。
if [ -d "$SRC/scripts" ]; then
  rsync "${rsync_opts[@]}" \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '*.log' \
    "$SRC/scripts/" "$DST/scripts-claude/" \
    || warn "scripts/ rsync had errors (continuing)"
fi

# 6.6) ホーム直下の CLAUDE.md 現行版 (起動時自動読込される安定ルールの正本)
cp -f "$HOME/CLAUDE.md" "$DST/CLAUDE.md" 2>/dev/null \
  || warn "~/CLAUDE.md のコピーに失敗"

# 6.7) launchd plist (com.kusagawa.* = 日次Driveパイプライン等の自動化定義)
mkdir -p "$DST/launchd"
for plist in "$HOME/Library/LaunchAgents"/com.kusagawa.*.plist; do
  [ -e "$plist" ] || continue
  cp -f "$plist" "$DST/launchd/" 2>/dev/null \
    || warn "launchd plist のコピーに失敗: $plist"
done
# plist が参照するランナー本体も保全
if [ -f "$HOME/.local/bin/kusagawa-pipeline-bash" ]; then
  cp -f "$HOME/.local/bin/kusagawa-pipeline-bash" "$DST/launchd/" 2>/dev/null || true
fi

# 7) git commit & push (rsyncが部分失敗していても必ずここまで到達する)
cd "$REPO"

if [ ! -d .git ]; then
  echo "[sync] git未初期化。先に 'cd ~/claude-config && git init' を実行してください"
  exit 0
fi

if [ -n "$(git status --porcelain)" ]; then
  git add -A
  STAMP="$(date '+%Y-%m-%d %H:%M:%S')"
  MSG="sync: $STAMP"
  if [ "$WARN_COUNT" -gt 0 ]; then
    MSG="$MSG (with $WARN_COUNT rsync warning(s))"
  fi
  git commit -m "$MSG" >/dev/null
  echo "[sync] commit OK: $MSG"
  if git remote | grep -q .; then
    git push --quiet 2>/dev/null && echo "[sync] push OK" || echo "[sync] push失敗(後で手動push可)"
  fi
else
  echo "[sync] 変更なし"
fi

if [ "$WARN_COUNT" -gt 0 ]; then
  echo "[sync] 完了したが $WARN_COUNT 件の警告あり (rsyncエラー)"
  echo "[sync] このメッセージが Stop hook 終了時に見えるはず。継続的に出るなら原因究明を。"
fi

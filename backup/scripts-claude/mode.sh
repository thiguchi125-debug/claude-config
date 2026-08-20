#!/bin/bash
# 起動時文脈の軽量化：時期限定のagent/skillをオン・オフする
# 使い方:  mode.sh council on | mode.sh council off | mode.sh status
#          mode.sh election on|off
# 退避先は ~/.claude/_agents_off / _skills_off（削除しない・いつでも戻せる）
set -u
A=~/.claude/agents;  AOFF=~/.claude/_agents_off
S=~/.claude/skills;  SOFF=~/.claude/_skills_off

COUNCIL_AGENTS="general-question-architect bill-scrutiny-architect bill-scrutiny-scriptwriter agenda-analyzer counter-argument-simulator council-material-creator gikai-dayori-creator toben-tracker ikensho-drafter"
COUNCIL_SKILLS=""
ELECTION_AGENTS="electoral-district-strategist community-rally-speaker daily-street-speech"
ELECTION_SKILLS=""
IDLE_AGENTS=""
IDLE_SKILLS=""

grp_agents(){ case "$1" in council) echo "$COUNCIL_AGENTS";; election) echo "$ELECTION_AGENTS";; idle) echo "$IDLE_AGENTS";; *) echo "";; esac; }
grp_skills(){ case "$1" in council) echo "$COUNCIL_SKILLS";; election) echo "$ELECTION_SKILLS";; idle) echo "$IDLE_SKILLS";; *) echo "";; esac; }

turn(){
  g="$1"; act="$2"; n=0
  for x in $(grp_agents "$g"); do
    if [ "$act" = on ]  && [ -f "$AOFF/$x.md" ]; then mv "$AOFF/$x.md" "$A/$x.md"; n=$((n+1)); fi
    if [ "$act" = off ] && [ -f "$A/$x.md" ];    then mv "$A/$x.md" "$AOFF/$x.md"; n=$((n+1)); fi
  done
  for x in $(grp_skills "$g"); do
    if [ "$act" = on ]  && [ -d "$SOFF/$x" ]; then mv "$SOFF/$x" "$S/$x"; n=$((n+1)); fi
    if [ "$act" = off ] && [ -d "$S/$x" ];    then mv "$S/$x" "$SOFF/$x"; n=$((n+1)); fi
  done
  echo "$g を $act にしました（$n 件移動）"
  [ "$act" = on ] && echo "※ 反映には新しいセッション（/clear または起動し直し）が必要です"
  return 0
}

status(){
  printf "%-10s %-5s %s\n" グループ 状態 内訳
  for g in council election idle; do
    on=0; off=0; items=""
    for x in $(grp_agents "$g"); do
      if [ -f "$A/$x.md" ]; then on=$((on+1)); else off=$((off+1)); fi; items="$items $x"
    done
    for x in $(grp_skills "$g"); do
      if [ -d "$S/$x" ]; then on=$((on+1)); else off=$((off+1)); fi; items="$items $x"
    done
    [ $((on+off)) -eq 0 ] && continue
    if [ $off -eq 0 ]; then st=ON; elif [ $on -eq 0 ]; then st=OFF; else st=混在; fi
    printf "%-10s %-5s on:%d off:%d\n" "$g" "$st" "$on" "$off"
  done
  echo
  echo "退避中: agents $(ls "$AOFF"/*.md 2>/dev/null | wc -l | tr -d ' ')本 / skills $(ls -d "$SOFF"/*/ 2>/dev/null | wc -l | tr -d ' ')本"
}

case "${1:-status}" in
  status) status ;;
  council|election|idle)
    case "${2:-}" in on|off) turn "$1" "$2" ;; *) echo "使い方: mode.sh $1 on|off"; exit 1 ;; esac ;;
  *) echo "使い方: mode.sh {council|election|idle} {on|off} | mode.sh status"; exit 1 ;;
esac

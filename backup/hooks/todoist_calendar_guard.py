#!/usr/bin/env python3
"""Todoist カレンダー突合ゲート（PreToolUse hook）

期限付きのTodoist新規登録を検知し、task-add スキルによるカレンダー突合が
済んでいなければ deny する。設計の正本は
~/.claude/skills/task-add/DESIGN.md。
標準ライブラリのみで動くこと（毎回のツール呼び出しで起動するため）。
"""
import json
import os
import re
import shlex
import sys
import unicodedata
from datetime import datetime, timedelta

VERIFIED_PATH = os.path.expanduser("~/.claude/skills/task-add/_verified.json")

# ゲート対象のMCPツール
# add-tasks    = 新規登録
# update-tasks = 既存タスクへの期限「後付け」。期限なしで登録してから付ける抜け道を塞ぐ
# reschedule-tasks は対象外（朝の繰越＝既に ohayo で承認済みの経路。ここを塞ぐと毎朝の
# 繰越に突合が要り日課が回らなくなる）。CLAUDE.md「繰越は翌朝 morning で承認分のみ」参照。
MCP_ADD_TOOLS = {"mcp__claude_ai_Todoist__add-tasks"}
MCP_UPDATE_TOOLS = {"mcp__claude_ai_Todoist__update-tasks"}

# reschedule-tasks は content を持たず date だけなので、件名照合ができない。
# 「今日・明日へ動かす」＝朝の繰越／即日対応は素通しし、それより先の日付＝計画判断
# （task-audit の 期限なし→今日+3日 など）だけを日付一致でゲートする。
MCP_RESCHEDULE_TOOLS = {"mcp__claude_ai_Todoist__reschedule-tasks"}
CARRYOVER_GRACE_DAYS = 1

# 期限を「外す」指定。付ける方向だけをゲートする
REMOVE_VALUES = {"remove", "none", "null", ""}

_KEEP = re.compile(r"[^0-9A-Za-z぀-ヿ一-鿿]")
_SEGMENT = re.compile(r"&&|\|\||;|\n")


def normalize(s):
    """比較用の正規化。空白・記号・絵文字を落とし、英字は小文字化する。"""
    s = unicodedata.normalize("NFKC", s or "")
    return _KEEP.sub("", s).lower()


def content_matches(a, b):
    """表記ゆれを吸収したタスク名の一致判定。"""
    na, nb = normalize(a), normalize(b)
    if not na or not nb:
        return False
    if na in nb or nb in na:
        return True
    return len(na) >= 10 and len(nb) >= 10 and na[:10] == nb[:10]


def _parse_one_segment(segment):
    if "td.py" not in segment:
        return []
    try:
        tokens = shlex.split(segment)
    except ValueError:
        # クォートが閉じていない等。解析できないものはゲートしない
        return []
    if "add" not in tokens:
        return []
    rest = tokens[tokens.index("add") + 1:]
    content, due = None, None
    i = 0
    while i < len(rest):
        token = rest[i]
        if token == "--due":
            due = rest[i + 1] if i + 1 < len(rest) else None
            i += 2
            continue
        if token.startswith("--"):
            i += 2  # 他のオプションは値ごと読み飛ばす
            continue
        if content is None:
            content = token
        i += 1
    if not due:
        return []
    return [{"content": content or "", "due": due}]


def parse_bash_add(command):
    """Bash コマンド文字列から、ゲート対象の td.py add を抜き出す。"""
    out = []
    for segment in _SEGMENT.split(command or ""):
        out.extend(_parse_one_segment(segment))
    return out


def extract_mcp_tasks(tool_input, need_content):
    """Todoist MCP の入力から、期限を設定しているタスクを抜き出す。

    need_content=True（update-tasks）では、期限だけ触って件名を渡さない呼び出しが
    照合できずに全部 deny されるのを避けるため、件名の無いものは素通しする。
    """
    tasks = tool_input.get("tasks")
    if not isinstance(tasks, list):
        tasks = [tool_input]
    out = []
    for task in tasks:
        if not isinstance(task, dict):
            continue
        due = task.get("deadlineDate") or task.get("dueString")
        if not due or str(due).strip().lower() in REMOVE_VALUES:
            continue
        content = task.get("content") or ""
        if need_content and not content.strip():
            continue
        out.append({"content": content, "due": str(due)})
    return out


def extract_mcp_reschedule(tool_input, today):
    """reschedule-tasks の入力から、繰越の範囲を超える日付移動を抜き出す。"""
    tasks = tool_input.get("tasks")
    if not isinstance(tasks, list):
        tasks = [tool_input]
    out = []
    for task in tasks:
        if not isinstance(task, dict):
            continue
        date = str(task.get("date") or "").strip()
        if not date:
            continue
        try:
            target = datetime.strptime(date[:10], "%Y-%m-%d").date()
        except ValueError:
            # 相対表現など解釈できないものはゲートしない（フェイルオープン）
            continue
        if (target - today).days <= CARRYOVER_GRACE_DAYS:
            continue  # 今日・明日への移動＝繰越。素通し
        out.append({"content": "", "due": date[:10], "match_due_only": True})
    return out


def gated_tasks(tool_name, tool_input, today):
    """このツール呼び出しのうち、突合が必要なタスクを返す。"""
    tool_input = tool_input or {}
    if tool_name == "Bash":
        return parse_bash_add(tool_input.get("command", ""))
    if tool_name in MCP_ADD_TOOLS:
        return extract_mcp_tasks(tool_input, need_content=False)
    if tool_name in MCP_UPDATE_TOOLS:
        return extract_mcp_tasks(tool_input, need_content=True)
    if tool_name in MCP_RESCHEDULE_TOOLS:
        return extract_mcp_reschedule(tool_input, today)
    return []


def load_verified(path):
    """突合記録を読む。存在しない・壊れている場合は None を返す。"""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def is_task_verified(task, data, now):
    """このタスクが有効な突合記録に含まれているか。"""
    if not data:
        return False
    try:
        generated_at = datetime.fromisoformat(str(data.get("generated_at", "")))
    except ValueError:
        return False
    if generated_at.tzinfo is not None:
        generated_at = generated_at.replace(tzinfo=None)
    ttl = data.get("ttl_minutes", 30)
    try:
        ttl = int(ttl)
    except (TypeError, ValueError):
        return False
    if now - generated_at > timedelta(minutes=ttl):
        return False
    for entry in data.get("approved") or []:
        if not isinstance(entry, dict):
            continue
        if str(entry.get("due", "")) != str(task.get("due", "")):
            continue
        if task.get("match_due_only"):
            return True  # reschedule-tasks は件名を持たないので日付一致で判定
        if content_matches(task.get("content", ""), entry.get("content", "")):
            return True
    return False


DENY_MESSAGE = (
    "カレンダー突合が未実施です。task-add スキルを起動し、"
    "期限日の実施可能性を判定した上で草川の承認を得てから登録してください。\n"
    "未突合のタスク: {tasks}\n"
    "（突合が不要な場合は期限を外して登録するか、草川に直接確認してください）"
)


def _deny(unverified):
    listed = "／".join(
        "{}（期限 {}）".format(t.get("content") or "(件名なし)", t.get("due", ""))
        for t in unverified
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": DENY_MESSAGE.format(tasks=listed),
        }
    }, ensure_ascii=False))


def main():
    payload = json.loads(sys.stdin.read())
    now = datetime.now()
    tasks = gated_tasks(
        payload.get("tool_name", ""), payload.get("tool_input"), now.date()
    )
    if not tasks:
        return
    data = load_verified(VERIFIED_PATH)
    unverified = [t for t in tasks if not is_task_verified(t, data, now)]
    if unverified:
        _deny(unverified)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # hook自身のバグで登録が全面停止するのを避ける（フェイルオープン）
        pass
    sys.exit(0)

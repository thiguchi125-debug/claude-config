# task-add 実装計画

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 期限付きTodoist登録の前に Google Calendar と突合して実施可能性を判定し、承認を得てから登録する仕組みを、PreToolUse hook で構造的に強制する。

**Architecture:** 3層。`todoist_calendar_guard.py`（PreToolUse hook）が期限付き登録を検知して突合記録 `_verified.json` と照合し、未突合なら deny する。`task-add` スキルが所要推定→カレンダー取得→セッション判定→提案→承認→記録書込→`td.py add` を行う。登録そのものは既存の `td.py` に委ねる。

**Tech Stack:** Python 3（標準ライブラリのみ・外部依存なし）、Claude Code PreToolUse hook、Google Calendar MCP、既存 `~/.claude/scripts/todoist/td.py`

## Global Constraints

- 設計の正本は `~/.claude/skills/task-add/DESIGN.md`。矛盾したら DESIGN.md が優先
- Python は**標準ライブラリのみ**。`pip install` を要する依存を足さない（hookは毎回のツール呼び出しで走るため起動が軽いこと）
- カレンダーID は `kusakawa.taku@gmail.com`（`kusagawa` は誤り）
- 稼働帯は**全曜日 9:00–21:00**。1セッション = 1時間の連続空き。**1日に同一タスクへ割けるのは最大2セッション**
- 判定閾値: ✅可能 = 確保可能 ≧ 必要×1.5 ／ ⚠️タイト = 必要 ≦ 確保可能 < 必要×1.5 ／ 🚫無理 = 確保可能 < 必要
- hook のパスは `$HOME/.claude/hooks/...` で書く（既存 Stop hook の記法に合わせる。`${CLAUDE_PROJECT_DIR}` は使わない）
- 突合済みのとき hook は**何も出力せず exit 0**。`permissionDecision: "allow"` は返さない（通常の許可フローを飛ばしてしまうため）
- hook スクリプト自体が例外で落ちた場合は exit 0 で通す（hookのバグで登録が全面停止する事態を避ける）
- ホーム直下は git リポジトリではない。`~/.claude/` 配下は Stop hook の `sync-to-git.sh` が `~/claude-config` へ自動commit/pushするため、**タスクごとの手動 git commit は不要**

## File Structure

| ファイル | 責務 |
|---|---|
| `~/.claude/hooks/todoist_calendar_guard.py` | ゲート判定のみ。カレンダーは見ない・登録もしない。`_verified.json` と照合して deny するかを決める |
| `~/.claude/hooks/tests/test_todoist_calendar_guard.py` | 上記のテスト（stdlib unittest） |
| `~/.claude/skills/task-add/SKILL.md` | 突合・判定・提案・承認・登録の手順書 |
| `~/.claude/settings.json` | hook の登録 |
| `~/claude-config/scripts/sync-to-git.sh` | `hooks/` をバックアップ対象に追加 |
| `~/CLAUDE.md` | トリガー追記 |

---

### Task 1: hook のコマンド解析（ゲート対象の検知）

**Files:**
- Create: `~/.claude/hooks/todoist_calendar_guard.py`
- Test: `~/.claude/hooks/tests/test_todoist_calendar_guard.py`

**Interfaces:**
- Produces:
  - `normalize(s: str) -> str`
  - `content_matches(a: str, b: str) -> bool`
  - `parse_bash_add(command: str) -> list[dict]` — 各要素は `{"content": str, "due": str}`
  - `extract_mcp_add(tool_input: dict) -> list[dict]` — 同上
  - `gated_tasks(tool_name: str, tool_input: dict) -> list[dict]` — 同上。空リストならゲート対象外

- [ ] **Step 1: テストディレクトリを作り、失敗するテストを書く**

```bash
mkdir -p ~/.claude/hooks/tests
```

`~/.claude/hooks/tests/test_todoist_calendar_guard.py`:

```python
import importlib.util
import os
import unittest

_HOOK = os.path.expanduser("~/.claude/hooks/todoist_calendar_guard.py")
_spec = importlib.util.spec_from_file_location("guard", _HOOK)
guard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(guard)


class TestParseBashAdd(unittest.TestCase):
    def test_add_with_due_is_gated(self):
        cmd = 'python3 ~/.claude/scripts/todoist/td.py add "原稿を書く" --due 2026-08-10'
        self.assertEqual(
            guard.parse_bash_add(cmd),
            [{"content": "原稿を書く", "due": "2026-08-10"}],
        )

    def test_add_without_due_is_not_gated(self):
        cmd = 'python3 ~/.claude/scripts/todoist/td.py add "原稿を書く"'
        self.assertEqual(guard.parse_bash_add(cmd), [])

    def test_done_is_not_gated(self):
        self.assertEqual(guard.parse_bash_add("td.py done 12345"), [])

    def test_morning_is_not_gated(self):
        self.assertEqual(guard.parse_bash_add("td.py morning"), [])

    def test_unrelated_command_is_not_gated(self):
        self.assertEqual(guard.parse_bash_add("ls -la ~/outputs"), [])

    def test_compound_command_is_parsed(self):
        cmd = 'cd /tmp && td.py add "A" --due 2026-08-10 && td.py add "B" --due 2026-08-11'
        self.assertEqual(
            guard.parse_bash_add(cmd),
            [{"content": "A", "due": "2026-08-10"},
             {"content": "B", "due": "2026-08-11"}],
        )

    def test_other_flags_do_not_swallow_content(self):
        cmd = 'td.py add "資料を読む" --project "🏛 議員活動" --due 2026-08-10 --priority 3'
        self.assertEqual(
            guard.parse_bash_add(cmd),
            [{"content": "資料を読む", "due": "2026-08-10"}],
        )

    def test_unbalanced_quotes_do_not_crash(self):
        self.assertEqual(guard.parse_bash_add('td.py add "壊れた --due 2026-08-10'), [])


class TestExtractMcpAdd(unittest.TestCase):
    def test_due_string_is_gated(self):
        ti = {"tasks": [{"content": "スライド作成", "dueString": "2026-08-12"}]}
        self.assertEqual(
            guard.extract_mcp_add(ti),
            [{"content": "スライド作成", "due": "2026-08-12"}],
        )

    def test_deadline_date_is_gated(self):
        ti = {"tasks": [{"content": "入稿", "deadlineDate": "2026-08-20"}]}
        self.assertEqual(
            guard.extract_mcp_add(ti),
            [{"content": "入稿", "due": "2026-08-20"}],
        )

    def test_no_due_is_not_gated(self):
        self.assertEqual(guard.extract_mcp_add({"tasks": [{"content": "いつか"}]}), [])

    def test_flat_single_task_shape(self):
        ti = {"content": "電話する", "dueString": "2026-08-05"}
        self.assertEqual(
            guard.extract_mcp_add(ti),
            [{"content": "電話する", "due": "2026-08-05"}],
        )


class TestGatedTasks(unittest.TestCase):
    def test_bash_routes_to_parse_bash_add(self):
        ti = {"command": 'td.py add "X" --due 2026-08-10'}
        self.assertEqual(
            guard.gated_tasks("Bash", ti),
            [{"content": "X", "due": "2026-08-10"}],
        )

    def test_add_tasks_tool_is_gated(self):
        ti = {"tasks": [{"content": "X", "dueString": "2026-08-10"}]}
        self.assertEqual(
            guard.gated_tasks("mcp__claude_ai_Todoist__add-tasks", ti),
            [{"content": "X", "due": "2026-08-10"}],
        )

    def test_reschedule_tool_is_not_gated(self):
        ti = {"tasks": [{"id": "1", "dueDate": "2026-08-10"}]}
        self.assertEqual(
            guard.gated_tasks("mcp__claude_ai_Todoist__reschedule-tasks", ti), []
        )

    def test_complete_tool_is_not_gated(self):
        self.assertEqual(
            guard.gated_tasks("mcp__claude_ai_Todoist__complete-tasks", {"tasks": []}), []
        )

    def test_edit_tool_is_not_gated(self):
        self.assertEqual(guard.gated_tasks("Edit", {"file_path": "/tmp/a"}), [])


class TestContentMatches(unittest.TestCase):
    def test_identical(self):
        self.assertTrue(guard.content_matches("川合町報告会のスライド作成",
                                              "川合町報告会のスライド作成"))

    def test_emoji_and_space_are_ignored(self):
        self.assertTrue(guard.content_matches("川合町報告会のスライド作成",
                                              "🏛 川合町報告会のスライド作成 "))

    def test_containment(self):
        self.assertTrue(guard.content_matches("報告会のスライド作成",
                                              "報告会のスライド作成（川合町）"))

    def test_prefix_ten_chars(self):
        self.assertTrue(guard.content_matches("川合町報告会のスライド作成",
                                              "川合町報告会のスライ資料一式をそろえる"))

    def test_different_tasks_do_not_match(self):
        self.assertFalse(guard.content_matches("入稿データを作る", "市民相談の返信"))

    def test_empty_never_matches(self):
        self.assertFalse(guard.content_matches("", "何か"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: テストが失敗することを確認**

Run: `python3 -m unittest discover -s ~/.claude/hooks/tests -v`
Expected: FAIL（`todoist_calendar_guard.py` が存在せず読み込みエラー）

- [ ] **Step 3: hook 本体の解析部を実装**

`~/.claude/hooks/todoist_calendar_guard.py`:

```python
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

# ゲート対象のMCPツール（新規登録のみ。期限変更はゲートしない）
MCP_ADD_TOOLS = {"mcp__claude_ai_Todoist__add-tasks"}

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


def extract_mcp_add(tool_input):
    """Todoist MCP の add-tasks 入力から、期限付きタスクを抜き出す。"""
    tasks = tool_input.get("tasks")
    if not isinstance(tasks, list):
        tasks = [tool_input]
    out = []
    for task in tasks:
        if not isinstance(task, dict):
            continue
        due = task.get("deadlineDate") or task.get("dueString")
        if not due:
            continue
        out.append({"content": task.get("content") or "", "due": str(due)})
    return out


def gated_tasks(tool_name, tool_input):
    """このツール呼び出しのうち、突合が必要なタスクを返す。"""
    tool_input = tool_input or {}
    if tool_name == "Bash":
        return parse_bash_add(tool_input.get("command", ""))
    if tool_name in MCP_ADD_TOOLS:
        return extract_mcp_add(tool_input)
    return []
```

- [ ] **Step 4: テストが通ることを確認**

Run: `python3 -m unittest discover -s ~/.claude/hooks/tests -v`
Expected: PASS（この時点では Task 2 以降のテストはまだ書いていないので全件PASS）

---

### Task 2: 突合記録の照合（TTL・期限・タスク名）

**Files:**
- Modify: `~/.claude/hooks/todoist_calendar_guard.py`
- Test: `~/.claude/hooks/tests/test_todoist_calendar_guard.py`

**Interfaces:**
- Consumes: `content_matches()`（Task 1）
- Produces:
  - `load_verified(path: str) -> dict | None` — 読めない・壊れている場合は `None`
  - `is_task_verified(task: dict, data: dict | None, now: datetime) -> bool`

- [ ] **Step 1: 失敗するテストを追記**

`~/.claude/hooks/tests/test_todoist_calendar_guard.py` の `if __name__` 行の**前**に追記:

```python
import json as _json
import tempfile
from datetime import datetime, timedelta


def _record(content="川合町報告会のスライド作成", due="2026-08-12",
            generated_at="2026-08-03T14:00:00", ttl=30, calendar_ok=True):
    return {
        "generated_at": generated_at,
        "ttl_minutes": ttl,
        "calendar_ok": calendar_ok,
        "approved": [{"content": content, "due": due, "sessions": 4, "verdict": "ok"}],
    }


class TestLoadVerified(unittest.TestCase):
    def test_missing_file_returns_none(self):
        self.assertIsNone(guard.load_verified("/tmp/does-not-exist-98765.json"))

    def test_corrupt_json_returns_none(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write("{壊れている")
            path = f.name
        self.addCleanup(os.unlink, path)
        self.assertIsNone(guard.load_verified(path))

    def test_valid_file_is_loaded(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            _json.dump(_record(), f)
            path = f.name
        self.addCleanup(os.unlink, path)
        self.assertEqual(guard.load_verified(path)["ttl_minutes"], 30)


class TestIsTaskVerified(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 8, 3, 14, 10, 0)
        self.task = {"content": "川合町報告会のスライド作成", "due": "2026-08-12"}

    def test_matching_record_within_ttl(self):
        self.assertTrue(guard.is_task_verified(self.task, _record(), self.now))

    def test_no_record_is_unverified(self):
        self.assertFalse(guard.is_task_verified(self.task, None, self.now))

    def test_expired_ttl_is_unverified(self):
        late = datetime(2026, 8, 3, 14, 31, 0)
        self.assertFalse(guard.is_task_verified(self.task, _record(), late))

    def test_due_mismatch_is_unverified(self):
        task = {"content": "川合町報告会のスライド作成", "due": "2026-08-13"}
        self.assertFalse(guard.is_task_verified(task, _record(), self.now))

    def test_content_mismatch_is_unverified(self):
        task = {"content": "まったく別のタスク", "due": "2026-08-12"}
        self.assertFalse(guard.is_task_verified(task, _record(), self.now))

    def test_content_variation_still_verified(self):
        task = {"content": "🏛 川合町報告会のスライド作成", "due": "2026-08-12"}
        self.assertTrue(guard.is_task_verified(task, _record(), self.now))

    def test_calendar_unavailable_record_still_passes(self):
        data = _record(calendar_ok=False)
        self.assertTrue(guard.is_task_verified(self.task, data, self.now))

    def test_broken_generated_at_is_unverified(self):
        data = _record(generated_at="いつか")
        self.assertFalse(guard.is_task_verified(self.task, data, self.now))

    def test_empty_approved_list_is_unverified(self):
        data = _record()
        data["approved"] = []
        self.assertFalse(guard.is_task_verified(self.task, data, self.now))
```

- [ ] **Step 2: テストが失敗することを確認**

Run: `python3 -m unittest discover -s ~/.claude/hooks/tests -v`
Expected: FAIL with "module 'guard' has no attribute 'load_verified'"

- [ ] **Step 3: 照合部を実装**

`todoist_calendar_guard.py` の `gated_tasks()` の**後**に追記:

```python
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
        if content_matches(task.get("content", ""), entry.get("content", "")):
            return True
    return False
```

- [ ] **Step 4: テストが通ることを確認**

Run: `python3 -m unittest discover -s ~/.claude/hooks/tests -v`
Expected: PASS（全件）

---

### Task 3: main() と deny 出力

**Files:**
- Modify: `~/.claude/hooks/todoist_calendar_guard.py`
- Test: `~/.claude/hooks/tests/test_todoist_calendar_guard.py`

**Interfaces:**
- Consumes: `gated_tasks()`, `load_verified()`, `is_task_verified()`
- Produces: `main() -> None`（stdinのJSONを読み、deny時のみ stdout にJSONを出して exit 0）

- [ ] **Step 1: 失敗するテストを追記**

`if __name__` 行の**前**に追記:

```python
import subprocess


def _run_hook(payload):
    proc = subprocess.run(
        ["python3", _HOOK],
        input=_json.dumps(payload),
        capture_output=True,
        text=True,
    )
    return proc


class TestHookEndToEnd(unittest.TestCase):
    def setUp(self):
        # 実ファイルを退避し、テスト後に戻す
        self.real = guard.VERIFIED_PATH
        self.backup = None
        if os.path.exists(self.real):
            with open(self.real, encoding="utf-8") as f:
                self.backup = f.read()
            os.unlink(self.real)
        self.addCleanup(self._restore)

    def _restore(self):
        if self.backup is not None:
            os.makedirs(os.path.dirname(self.real), exist_ok=True)
            with open(self.real, "w", encoding="utf-8") as f:
                f.write(self.backup)
        elif os.path.exists(self.real):
            os.unlink(self.real)

    def _write_record(self, content, due):
        os.makedirs(os.path.dirname(self.real), exist_ok=True)
        with open(self.real, "w", encoding="utf-8") as f:
            _json.dump({
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "ttl_minutes": 30,
                "calendar_ok": True,
                "approved": [{"content": content, "due": due,
                              "sessions": 1, "verdict": "ok"}],
            }, f, ensure_ascii=False)

    def test_unverified_add_is_denied(self):
        proc = _run_hook({
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": 'td.py add "未突合のタスク" --due 2026-08-10'},
        })
        self.assertEqual(proc.returncode, 0)
        out = _json.loads(proc.stdout)
        self.assertEqual(
            out["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertIn("task-add",
                      out["hookSpecificOutput"]["permissionDecisionReason"])

    def test_verified_add_is_silent(self):
        self._write_record("突合済みのタスク", "2026-08-10")
        proc = _run_hook({
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": 'td.py add "突合済みのタスク" --due 2026-08-10'},
        })
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "")

    def test_no_due_is_silent(self):
        proc = _run_hook({
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": 'td.py add "期限なし"'},
        })
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "")

    def test_unrelated_tool_is_silent(self):
        proc = _run_hook({
            "hook_event_name": "PreToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": "/tmp/a"},
        })
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "")

    def test_garbage_stdin_does_not_block(self):
        proc = subprocess.run(["python3", _HOOK], input="これはJSONではない",
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "")
```

- [ ] **Step 2: テストが失敗することを確認**

Run: `python3 -m unittest discover -s ~/.claude/hooks/tests -v`
Expected: FAIL（hook を実行しても何も出力されず、`test_unverified_add_is_denied` の `json.loads` が空文字で落ちる）

- [ ] **Step 3: main() を実装**

`todoist_calendar_guard.py` の末尾に追記:

```python
DENY_MESSAGE = (
    "カレンダー突合が未実施です。task-add スキルを起動し、"
    "期限日の実施可能性を判定した上で草川の承認を得てから登録してください。\n"
    "未突合のタスク: {tasks}\n"
    "（突合が不要な場合は期限を外して登録するか、草川に直接確認してください）"
)


def _deny(unverified):
    listed = "／".join(
        "{}（期限 {}）".format(t.get("content", ""), t.get("due", ""))
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
    tasks = gated_tasks(payload.get("tool_name", ""), payload.get("tool_input"))
    if not tasks:
        return
    data = load_verified(VERIFIED_PATH)
    now = datetime.now()
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
```

- [ ] **Step 4: テストが通ることを確認**

Run: `python3 -m unittest discover -s ~/.claude/hooks/tests -v`
Expected: PASS（全件）

- [ ] **Step 5: 実行権限を付ける**

```bash
chmod +x ~/.claude/hooks/todoist_calendar_guard.py
```

---

### Task 4: settings.json への登録と実機スモークテスト

**Files:**
- Modify: `~/.claude/settings.json`

**Interfaces:**
- Consumes: `~/.claude/hooks/todoist_calendar_guard.py`（Task 3）

- [ ] **Step 1: 現在の settings.json を退避**

```bash
cp ~/.claude/settings.json ~/.claude/settings.json.bak-taskadd
```

- [ ] **Step 2: PreToolUse を追記**

既存の `Stop` を**必ず残したまま**、`hooks` 直下に `PreToolUse` を足す。編集後の `~/.claude/settings.json` は次の内容になる:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "$HOME/claude-config/scripts/sync-to-git.sh >/dev/null 2>&1 &"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash|mcp__claude_ai_Todoist__add-tasks",
        "hooks": [
          {
            "type": "command",
            "command": "python3 $HOME/.claude/hooks/todoist_calendar_guard.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 3: JSON として妥当か、Stop が残っているかを確認**

```bash
python3 -c "
import json, os
d = json.load(open(os.path.expanduser('~/.claude/settings.json')))
assert 'Stop' in d['hooks'], 'Stop hook が消えている'
assert 'PreToolUse' in d['hooks'], 'PreToolUse が無い'
print('OK', list(d['hooks']))
"
```
Expected: `OK ['Stop', 'PreToolUse']`

- [ ] **Step 4: hook を直接叩いてスモークテスト**

```bash
echo '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"td.py add \"スモークテスト\" --due 2026-12-01"}}' \
  | python3 ~/.claude/hooks/todoist_calendar_guard.py
```
Expected: `permissionDecision: "deny"` を含むJSONが出る

```bash
echo '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"td.py morning"}}' \
  | python3 ~/.claude/hooks/todoist_calendar_guard.py
```
Expected: 出力なし（exit 0）

- [ ] **Step 5: 既存フローが壊れていないことを確認**

```bash
python3 ~/.claude/scripts/todoist/td.py projects | head -5
```
Expected: プロジェクト一覧が出る（ゲート対象外なので hook は黙って通す）

- [ ] **Step 6: 退避ファイルを削除**

```bash
rm ~/.claude/settings.json.bak-taskadd
```

---

### Task 5: バックアップ対象に hooks/ を追加

**Files:**
- Modify: `~/claude-config/scripts/sync-to-git.sh`

`hooks/` は現在バックアップ対象外。settings.json だけが復元されると hook のパスが存在せず、Claude Code が毎回 hook 実行に失敗する状態になる。

- [ ] **Step 1: 現状を確認（hooks が同期されていないことの証拠を取る）**

```bash
ls ~/claude-config/backup/ && ls ~/claude-config/backup/hooks 2>&1
```
Expected: `hooks` ディレクトリが存在しない旨のエラー

- [ ] **Step 2: 同期セクションを追加**

`~/claude-config/scripts/sync-to-git.sh` の「6.6) ホーム直下の CLAUDE.md」節の**直前**に挿入:

```bash
# 6.5.1) hooks/ (PreToolUse等のhook本体)
# 2026-08-03 追加: settings.json は同期されるのに hooks/ が同期されておらず、
# 復元すると settings.json が存在しないスクリプトを指す壊れた状態になっていた。
if [ -d "$SRC/hooks" ]; then
  rsync "${rsync_opts[@]}" \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '*.log' \
    "$SRC/hooks/" "$DST/hooks/" \
    || warn "hooks/ rsync had errors (continuing)"
fi
```

- [ ] **Step 3: 突合記録をバックアップ対象から除外**

`_verified.json` は数分で失効する一時ファイルで、同期すると毎回差分が出て commit が汚れる。「5) カスタムskills」節の rsync に除外を1行足す:

```bash
      --exclude 'evals/results' \
      --exclude '*.log' \
      --exclude 'output/' \
      --exclude '_verified.json' \
```

- [ ] **Step 4: 同期を実行して確認**

```bash
bash ~/claude-config/scripts/sync-to-git.sh
ls ~/claude-config/backup/hooks/
```
Expected: `todoist_calendar_guard.py` と `tests/` が現れる

```bash
ls ~/claude-config/backup/skills/task-add/
```
Expected: `DESIGN.md` `PLAN.md` `SKILL.md` はあるが `_verified.json` は無い

---

### Task 6: SKILL.md の作成

**Files:**
- Create: `~/.claude/skills/task-add/SKILL.md`

**Interfaces:**
- Consumes: `~/.claude/hooks/todoist_calendar_guard.py` が読む `_verified.json` の形（Task 2）

- [ ] **Step 1: SKILL.md を書く**

frontmatter の `description` は、他スキルと同様に**起動トリガー語と NOT 節を含める**こと。本文には以下の節を、DESIGN.md の値をそのまま写して置く。

```markdown
---
name: task-add
description: 草川たくや（亀山市議会議員）のTodoistタスク登録の入口スキル。「タスク登録して」「これタスクにして」「Todoistに入れて」「期限いつにする」「タスクにしといて」等で必ず起動。期限付きで登録する前に Google Calendar（kusakawa.taku@gmail.com）と突合し、想定所要を1時間セッション換算で見積もって「期限日までに実施可能か」を✅可能／⚠️タイト／🚫無理の3値で判定、🚫なら代替期限日を2案提示する。提案→草川の承認→承認分のみ td.py add、が固定の流れで、承認なしに登録しない。突合を飛ばした登録は PreToolUse hook（todoist_calendar_guard.py）が deny する。※イベントからの逆算で不足タスクを洗い出す→gyakusan、既存タスクの棚卸し→task-audit、市民意見そのものの記録→iken が正で本スキルは反応しない。
---

# task-add — カレンダー突合つきタスク登録

（以下の節を置く）

## Step 1: タスクの整理
## Step 2: 想定所要の見積り（既定テーブル＝DESIGN.md 4.5 を転記）
## Step 3: カレンダー取得（list_events を1回・今日〜期限候補+7日）
## Step 4: 空き枠の算出（DESIGN.md 4.3 の手順を転記）
## Step 5: 3値判定（DESIGN.md 4.4 を転記）
## Step 6: 提案（DESIGN.md 5 のフォーマットを転記）
## Step 7: 承認取得
## Step 8: _verified.json 書込
## Step 9: td.py add 実行
## 📌 恒久ガードルール
```

必ず含める具体値:

- カレンダーID `kusakawa.taku@gmail.com`
- 稼働帯 全曜日 9:00–21:00／1セッション=1時間／**1日最大2セッション**／30分未満の隙間は無視／終日予定のある日は0セッション
- 判定閾値 ✅ ≧必要×1.5 ／ ⚠️ 必要以上×1.5未満 ／ 🚫 必要未満
- 最低所要日数 = `ceil(必要セッション ÷ 2)`。残り日数がこれを下回れば空きを見ずに 🚫
- 想定所要テーブル10行（DESIGN.md 4.5 をそのまま）
- 既存タスクは `td.py week` で**件数のみ**併記（所要を差し引かない）
- `td.py projects` で実在プロジェクト名を確認してから `--project` を指定する
- `_verified.json` の書式（`generated_at` は `datetime.now().isoformat(timespec="seconds")` 形式・`ttl_minutes` は 30・`approved` は `{content, due, sessions, verdict}`）
- Google Calendar MCP が応答しない場合は `calendar_ok: false` で記録を書き、提案・登録時に「⚠️ カレンダー未確認で登録」と明示する
- 恒久ガードルール: 承認なしに登録しない／既定値で勝手に期限を確定しない（[[feedback_ask_destination_and_deadline_before_register]]）／想定所要は必ず提示し訂正されたら再計算する

- [ ] **Step 2: `_verified.json` を書く手順が hook と噛み合うか、手で1往復させて確認**

```bash
python3 -c "
import json, os
from datetime import datetime
p = os.path.expanduser('~/.claude/skills/task-add/_verified.json')
json.dump({
  'generated_at': datetime.now().isoformat(timespec='seconds'),
  'ttl_minutes': 30, 'calendar_ok': True,
  'approved': [{'content': '疎通確認タスク', 'due': '2026-12-01',
                'sessions': 1, 'verdict': 'ok'}],
}, open(p, 'w'), ensure_ascii=False)
print('written')
"
echo '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"td.py add \"疎通確認タスク\" --due 2026-12-01"}}' \
  | python3 ~/.claude/hooks/todoist_calendar_guard.py
```
Expected: 出力なし（＝突合済みとして通る）

```bash
echo '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"td.py add \"別のタスク\" --due 2026-12-01"}}' \
  | python3 ~/.claude/hooks/todoist_calendar_guard.py
```
Expected: deny のJSONが出る

- [ ] **Step 3: 疎通確認用の記録を消す**

```bash
rm ~/.claude/skills/task-add/_verified.json
```

---

### Task 7: 既存スキル7本の登録経路を task-add に通す

**Files:**
- Modify: `~/.claude/skills/gyakusan/SKILL.md`
- Modify: `~/.claude/skills/ohayo/SKILL.md`
- Modify: `~/.claude/skills/nichijo/SKILL.md`
- Modify: `~/.claude/skills/iken/SKILL.md`
- Modify: `~/.claude/skills/smart-intake/SKILL.md`
- Modify: `~/.claude/skills/task-audit/SKILL.md`
- Modify: `~/.claude/skills/shisei-houkokukai/SKILL.md`

これら7本は `td.py add ... --due` を直接叩く。hook を入れた時点で**全部ブロックされる**ため、登録経路を task-add に通す。

hook の deny メッセージが「task-add を起動せよ」と教えるので、編集を怠っても最終的には自己修復する（denyされる→task-addを起動する→登録できる）。ただし毎回1往復を無駄にするため、常道の経路を先に正しくしておく。

- [ ] **Step 1: 現状の呼び出し箇所を確認**

```bash
grep -rn "td.py add" ~/.claude/skills/ | grep -v task-add
```
Expected: 7スキルにまたがる箇所が列挙される（この一覧を編集対象とする）

- [ ] **Step 2: 各スキルに同一の1行を追加**

7本すべてに、`td.py add` を説明している箇所の直近に**次の1行をそのまま**入れる（文言を各スキルで変えない。揺れると後で grep できなくなる）:

```markdown
- 🗓 **期限つきで登録する場合は task-add の突合手順を通す**（想定所要を1hセッション換算→カレンダー突合→✅/⚠️/🚫判定→承認）。突合なしの `td.py add --due` は PreToolUse hook が deny する。期限なしの登録はこれまで通り。
```

挿入位置:

| スキル | 挿入位置 |
|---|---|
| `gyakusan/SKILL.md` | 「## Step 5: 提案→承認→登録」の項目3の直後 |
| `ohayo/SKILL.md` | 69行目「🧾 タスク登録候補の承認」節の末尾 |
| `nichijo/SKILL.md` | 85行目「🔴 登録先は全て Todoist」の直後 |
| `iken/SKILL.md` | 15行目「次アクションのタスク化提案の登録先は…」の直後 |
| `smart-intake/SKILL.md` | 28行目の判定ツリー表の直後 |
| `task-audit/SKILL.md` | 74行目「次の一手タスク自動提案」の直後 |
| `shisei-houkokukai/SKILL.md` | 139行目「Todoistへ期限付きタスク登録を提案」の直後 |

- [ ] **Step 3: gyakusan だけ二重取得を避ける追記をする**

gyakusan は Step 1 で既に60日分のカレンダーを取っている。上の1行に続けて、gyakusan にだけ次を足す:

```markdown
  - gyakusan は Step 1 で既にカレンダーを取得済みのため、task-add に**そのイベント一覧を渡して `list_events` を再取得させない**。判定（セッション換算・3値判定・`_verified.json` 書込）だけを task-add の手順で行う。
```

- [ ] **Step 4: 7本すべてに入ったことを確認**

```bash
grep -rln "期限つきで登録する場合は task-add の突合手順を通す" ~/.claude/skills/ | sort
```
Expected: 7ファイルが列挙される（gyakusan / ohayo / nichijo / iken / smart-intake / task-audit / shisei-houkokukai）

---

### Task 8: CLAUDE.md への追記

**Files:**
- Modify: `~/CLAUDE.md`

- [ ] **Step 1: トリガー早見表に1行足す**

「トリガー早見」表の `| 逆算チェック / 準備漏れ確認 ... | **gyakusan** ... |` 行の**次**に挿入:

```markdown
| タスク登録して / これタスクにして / Todoistに入れて / 期限いつにする | **task-add**（想定所要を1hセッション換算→Googleカレンダー突合→✅/⚠️/🚫3値判定→🚫なら代替期限2案→承認分のみ `td.py add`。突合なしの期限付き登録はPreToolUse hookがdenyする） |
```

- [ ] **Step 2: 「新規タスク登録手順」の項を更新**

「**新規タスク登録手順（2026-06-15確定）**」の行を、②の内容を差し替えたこの1行にする:

```markdown
  - **新規タスク登録手順（2026-06-15確定・2026-08-03カレンダー突合を追加）**: ①まず「記録で足りるか、タスク化が要るか」を振り分け（方針・状況は記録に残すだけ＝タスクにしない）②タスク化候補は **task-add スキル**を通し、保存先＋期限案に加えて**カレンダー突合による実施可能性判定（✅/⚠️/🚫＋代替期限案）**をセットで提示③**草川の回答を得てから**登録。既定値で勝手に確定登録しない（[[feedback_ask_destination_and_deadline_before_register]]が[[feedback_task_deadline_3days]]を上書き）。領域に応じ `--project` 指定。相手待ち＝@結果待ち、要検討＝@保留。期限付きの登録は PreToolUse hook が突合済みかを検査する。
```

- [ ] **Step 3: 追記が反映されたか確認**

```bash
grep -c "task-add" ~/CLAUDE.md
```
Expected: `2` 以上

---

### Task 9: 受け入れ条件の通し確認

**Files:** なし（検証のみ）

DESIGN.md 「10. 受け入れ条件」を実際に叩いて確認する。

- [ ] **Step 1: 自動テストを全件流す**

Run: `python3 -m unittest discover -s ~/.claude/hooks/tests -v`
Expected: PASS（全件）

- [ ] **Step 2: 受け入れ条件を1件ずつ確認**

```bash
H=~/.claude/hooks/todoist_calendar_guard.py
mk() { echo "{\"hook_event_name\":\"PreToolUse\",\"tool_name\":\"Bash\",\"tool_input\":{\"command\":\"$1\"}}"; }

echo "--- 1) 突合なしの期限付き登録は deny"
mk 'td.py add \"テスト\" --due 2026-08-10' | python3 $H

echo "--- 3) 期限なしは素通し（出力なしが正）"
mk 'td.py add \"テスト\"' | python3 $H

echo "--- 4) done / list / morning は素通し（出力なしが正）"
mk 'td.py done 123' | python3 $H
mk 'td.py list' | python3 $H
mk 'td.py morning' | python3 $H

echo "--- 8) Stop hook が残っている"
python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/settings.json'))); print('Stop:', 'Stop' in d['hooks'])"

echo "--- 9) 既存7スキルに但し書きが入っている（7と出るのが正）"
grep -rln "期限つきで登録する場合は task-add の突合手順を通す" ~/.claude/skills/ | wc -l

echo "--- 10) hooks がバックアップされ、_verified.json はされていない"
ls ~/claude-config/backup/hooks/todoist_calendar_guard.py
ls ~/claude-config/backup/skills/task-add/_verified.json 2>&1 | tail -1
```
Expected: 1) は deny のJSON／3) 4) は無出力／8) は `Stop: True`／9) は `7`／10) は hook が存在し `_verified.json` は "No such file"

- [ ] **Step 3: 判定ロジックを SKILL.md の手順どおり手で1回流す**

架空の3タスク（「リーフレット入稿・期限3日後」「ブログ執筆・期限1週間後」「◯◯へ電話・期限明日」）で task-add を起動し、次を確認する:

- リーフレット入稿が**最低所要日数4日 > 残り3日**により、空き状況を見るまでもなく 🚫 になること
- 代替期限日が2案提示されること
- 想定所要が提案に明示されること
- 承認していないタスクが登録されないこと
- 8時間空いている日があっても1タスクにつき2セッションしか計上されないこと

- [ ] **Step 4: 実タスクを1件、task-add 経由で登録して端から端まで通す**

草川に「1件テスト登録してよいか」を確認した上で実施し、登録後に `td.py today` または `td.py week` で実在を確認する。確認が取れなければこのステップは飛ばし、飛ばした旨を報告する。

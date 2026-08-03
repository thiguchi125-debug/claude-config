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


if __name__ == "__main__":
    unittest.main()

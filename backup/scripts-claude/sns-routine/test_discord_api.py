#!/usr/bin/env python3
"""discord_api.py のオフラインテスト（HTTP不要のロジックのみ）"""
import json, os, tempfile, unittest

os.environ["SNS_ROUTINE_STATE"] = os.path.join(tempfile.mkdtemp(), "_state.json")
import discord_api  # noqa: E402

USER = discord_api.USER_ID
BOT = "9999"

def msg(mid, author, content="x"):
    return {"id": mid, "author": {"id": author}, "content": content, "timestamp": "t"}

class TestFilterNew(unittest.TestCase):
    def test_excludes_bot_and_sorts_ascending(self):
        msgs = [msg("300", USER), msg("100", USER), msg("200", BOT)]
        out = discord_api.filter_new(msgs, last_id=None)
        self.assertEqual([m["id"] for m in out], ["100", "300"])

    def test_respects_cursor(self):
        msgs = [msg("100", USER), msg("200", USER), msg("300", USER)]
        out = discord_api.filter_new(msgs, last_id="200")
        self.assertEqual([m["id"] for m in out], ["300"])

    def test_empty_when_no_new(self):
        self.assertEqual(discord_api.filter_new([msg("100", USER)], last_id="100"), [])

class TestAdvance(unittest.TestCase):
    def setUp(self):
        if os.path.exists(discord_api.STATE_PATH):
            os.remove(discord_api.STATE_PATH)

    def test_advance_sets_cursor(self):
        discord_api.advance("500")
        self.assertEqual(discord_api.load_state()["last_processed_id"], "500")

    def test_advance_is_monotonic(self):
        discord_api.advance("500")
        discord_api.advance("400")  # 巻き戻し禁止
        self.assertEqual(discord_api.load_state()["last_processed_id"], "500")

if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""discord_api.py のオフラインテスト（HTTP不要のロジックのみ）"""
import json, os, tempfile, unittest

os.environ["SNS_ROUTINE_STATE"] = os.path.join(tempfile.mkdtemp(), "_state.json")
import discord_api  # noqa: E402

USER = discord_api.USER_ID
BOT = "9999"

def msg(mid, author, content="x", reactions=None):
    m = {"id": mid, "author": {"id": author}, "content": content, "timestamp": "t"}
    if reactions:
        m["reactions"] = reactions
    return m

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

class TestFindUnprocessed(unittest.TestCase):
    def test_excludes_reacted_messages(self):
        msgs = [
            msg("100", USER, reactions=[{"emoji": {"name": "✅"}}]),
            msg("200", USER),
        ]
        out = discord_api.find_unprocessed(msgs)
        self.assertEqual([m["id"] for m in out], ["200"])

    def test_excludes_bot_messages(self):
        msgs = [msg("100", USER), msg("200", BOT)]
        out = discord_api.find_unprocessed(msgs)
        self.assertEqual([m["id"] for m in out], ["100"])

    def test_excludes_below_floor_id(self):
        msgs = [msg("100", USER), msg("200", USER), msg("300", USER)]
        out = discord_api.find_unprocessed(msgs, floor_id="200")
        self.assertEqual([m["id"] for m in out], ["300"])

    def test_sorts_ascending_and_mixed(self):
        msgs = [
            msg("500", USER),
            msg("300", USER, reactions=[{"emoji": {"name": "⚠️"}}]),
            msg("400", BOT),
            msg("100", USER),
        ]
        out = discord_api.find_unprocessed(msgs, floor_id="50")
        self.assertEqual([m["id"] for m in out], ["100", "500"])


class TestSnowflake(unittest.TestCase):
    def test_audit_floor_is_2026_07_14_jst(self):
        # 2026-07-13 23:59:59 JST 相当のID・2026-07-14 00:00:00 JST 相当のIDより小さいこと
        floor = int(discord_api.audit_floor_snowflake())
        before = int(discord_api.snowflake_from_ms(
            discord_api.datetime.fromisoformat("2026-07-13T23:59:59+09:00").timestamp() * 1000))
        after = int(discord_api.snowflake_from_ms(
            discord_api.datetime.fromisoformat("2026-07-14T00:00:01+09:00").timestamp() * 1000))
        self.assertLess(before, floor)
        self.assertLess(floor, after)


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

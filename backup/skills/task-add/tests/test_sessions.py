import importlib.util
import json
import os
import tempfile
import unittest

_SCRIPT = os.path.expanduser("~/.claude/skills/task-add/sessions.py")
_spec = importlib.util.spec_from_file_location("sessions", _SCRIPT)
sessions = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sessions)


def _timed(day, start, end, title="予定"):
    return {"summary": title,
            "start": {"dateTime": "{}T{}:00+09:00".format(day, start)},
            "end": {"dateTime": "{}T{}:00+09:00".format(day, end)}}


def _allday(day, title):
    return {"summary": title, "start": {"date": day + "T00:00:00Z"}}


def _write(events):
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                    encoding="utf-8")
    json.dump({"events": events}, f, ensure_ascii=False)
    f.close()
    return f.name


class TestSlotsForDay(unittest.TestCase):
    def test_empty_day_is_capped_at_four_slots(self):
        # 9-21時が丸ごと空いていても、1タスクには最大4コマ（2セッション）
        n, _ = sessions.slots_for_day({"busy": [], "allday": []})
        self.assertEqual(n, 4)

    def test_thirty_minute_gap_counts_as_one_slot(self):
        # 実データ 2026-08-04 と同じ形。1時間単位で切り捨てると0になる罠
        info = {"busy": [(9 * 60, 17 * 60 + 45), (18 * 60 + 15, 21 * 60)],
                "allday": []}
        n, _ = sessions.slots_for_day(info)
        self.assertEqual(n, 1)

    def test_gap_under_thirty_minutes_is_discarded(self):
        info = {"busy": [(9 * 60, 17 * 60), (17 * 60 + 20, 21 * 60)],
                "allday": []}
        n, _ = sessions.slots_for_day(info)
        self.assertEqual(n, 0)

    def test_overlapping_events_are_merged(self):
        # 14-18 と 14-16 が重なる。二重に引かれると空きがマイナス方向にずれる
        info = {"busy": [(14 * 60, 18 * 60), (14 * 60, 16 * 60)], "allday": []}
        n, why = sessions.slots_for_day(info)
        self.assertEqual(n, 4)          # 9-14の5時間 + 18-21の3時間 → 上限4
        self.assertIn("480分", why)

    def test_blocking_allday_zeroes_the_day(self):
        n, why = sessions.slots_for_day({"busy": [], "allday": ["教育民生委員会視察"]})
        self.assertEqual(n, 0)
        self.assertIn("終日拘束", why)

    def test_non_blocking_allday_does_not_zero_the_day(self):
        # 「川合町憩いの場」等の目印を作業不可日にすると全日が0になる
        n, _ = sessions.slots_for_day({"busy": [], "allday": ["川合町憩いの場13:30-"]})
        self.assertEqual(n, 4)

    def test_now_minute_truncates_today(self):
        n, _ = sessions.slots_for_day({"busy": [], "allday": []},
                                      from_minute=20 * 60)
        self.assertEqual(n, 2)          # 20:00-21:00 = 60分 = 2コマ


class TestReferenceEventsIgnored(unittest.TestCase):
    def test_sanko_prefixed_event_is_ignored(self):
        path = _write([_timed("2026-08-03", "09:00", "21:00",
                              "【参考】太岡寺グランドゴルフ")])
        self.addCleanup(os.unlink, path)
        days = sessions.load_days(path)
        self.assertEqual(days, {})

    def test_sanko_allday_is_ignored(self):
        path = _write([_allday("2026-08-03", "【参考】山下グラウンドゴルフ9:00-")])
        self.addCleanup(os.unlink, path)
        self.assertEqual(sessions.load_days(path), {})


class TestLatestStartDay(unittest.TestCase):
    def test_picks_the_last_day_that_still_fits(self):
        import datetime
        rows = [(datetime.date(2026, 8, 3), 4, ""),
                (datetime.date(2026, 8, 4), 1, ""),
                (datetime.date(2026, 8, 5), 4, "")]
        # 必要4コマ → 8/5だけで4コマ足りるので 8/5 が境界日
        self.assertEqual(sessions.latest_start_day(rows, 4),
                         datetime.date(2026, 8, 5))
        # 必要9コマ → 全日必要なので 8/3
        self.assertEqual(sessions.latest_start_day(rows, 9),
                         datetime.date(2026, 8, 3))

    def test_returns_none_when_never_enough(self):
        import datetime
        rows = [(datetime.date(2026, 8, 3), 1, "")]
        self.assertIsNone(sessions.latest_start_day(rows, 5))


class TestVerdict(unittest.TestCase):
    def test_thresholds(self):
        self.assertEqual(sessions.verdict(7, 8), "🚫 無理")
        self.assertEqual(sessions.verdict(8, 8), "⚠️ タイト")
        self.assertEqual(sessions.verdict(11, 8), "⚠️ タイト")
        self.assertEqual(sessions.verdict(12, 8), "✅ 可能")


if __name__ == "__main__":
    unittest.main()

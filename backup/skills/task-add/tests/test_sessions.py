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
        n, _, _ = sessions.slots_for_day({"busy": [], "allday": []})
        self.assertEqual(n, 4)

    def test_thirty_minute_gap_counts_as_one_slot(self):
        # 実データ 2026-08-04 と同じ形。1時間単位で切り捨てると0になる罠
        info = {"busy": [(9 * 60, 17 * 60 + 45), (18 * 60 + 15, 21 * 60)],
                "allday": []}
        n, _, _ = sessions.slots_for_day(info)
        self.assertEqual(n, 1)

    def test_gap_under_thirty_minutes_is_discarded(self):
        info = {"busy": [(9 * 60, 17 * 60), (17 * 60 + 20, 21 * 60)],
                "allday": []}
        n, _, _ = sessions.slots_for_day(info)
        self.assertEqual(n, 0)

    def test_overlapping_events_are_merged(self):
        # 14-18 と 14-16 が重なる。二重に引かれると空きがマイナス方向にずれる
        info = {"busy": [(14 * 60, 18 * 60), (14 * 60, 16 * 60)], "allday": []}
        n, why, _ = sessions.slots_for_day(info)
        self.assertEqual(n, 4)          # 9-14の5時間 + 18-21の3時間 → 上限4
        self.assertIn("480分", why)

    def test_blocking_allday_zeroes_the_day(self):
        n, why, _ = sessions.slots_for_day({"busy": [], "allday": ["教育民生委員会視察"]})
        self.assertEqual(n, 0)
        self.assertIn("終日拘束", why)

    def test_non_blocking_allday_does_not_zero_the_day(self):
        # 「川合町憩いの場」等の目印を作業不可日にすると全日が0になる
        n, _, _ = sessions.slots_for_day({"busy": [], "allday": ["川合町憩いの場13:30-"]})
        self.assertEqual(n, 4)

    def test_now_minute_truncates_today(self):
        n, _, _ = sessions.slots_for_day({"busy": [], "allday": []},
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
        rows = [(datetime.date(2026, 8, 3), 4, "", []),
                (datetime.date(2026, 8, 4), 1, "", []),
                (datetime.date(2026, 8, 5), 4, "", [])]
        # 必要4コマ → 8/5だけで4コマ足りるので 8/5 が境界日
        self.assertEqual(sessions.latest_start_day(rows, 4),
                         datetime.date(2026, 8, 5))
        # 必要9コマ → 全日必要なので 8/3
        self.assertEqual(sessions.latest_start_day(rows, 9),
                         datetime.date(2026, 8, 3))

    def test_returns_none_when_never_enough(self):
        import datetime
        rows = [(datetime.date(2026, 8, 3), 1, "", [])]
        self.assertIsNone(sessions.latest_start_day(rows, 5))


class TestVerdict(unittest.TestCase):
    def test_thresholds(self):
        self.assertEqual(sessions.verdict(7, 8), "🚫 無理")
        self.assertEqual(sessions.verdict(8, 8), "⚠️ タイト")
        self.assertEqual(sessions.verdict(11, 8), "⚠️ タイト")
        self.assertEqual(sessions.verdict(12, 8), "✅ 可能")


class TestPlanBlocks(unittest.TestCase):
    """作業ブロックの割り付け（v3・2026-08-05）。

    コマ数だけ数えて空き時間帯を捨てると「いつやるか」がカレンダーに残らない。
    """

    def _rows(self, specs):
        """[(日, コマ数, 空き区間), ...] から daily_slots 相当の行を作る。"""
        import datetime
        return [(datetime.date(2026, 8, d), n, "", free) for d, n, free in specs]

    def test_one_block_per_free_interval_max_sixty_minutes(self):
        rows = self._rows([(3, 4, [(9 * 60, 21 * 60)])])
        plan, left = sessions.plan_blocks(rows, need=2, max_per_day=4)
        self.assertEqual(len(plan), 1)              # 1区間には1ブロックまで
        self.assertEqual(plan[0][2] - plan[0][1], 60)   # 最大60分
        self.assertEqual(left, 0)

    def test_spreads_across_days_when_slack_is_ample(self):
        # ✅可能のときは max_per_day=2 で呼ぶ → 1日1時間ずつ4日に散る
        rows = self._rows([(d, 4, [(9 * 60, 21 * 60)]) for d in (3, 4, 5, 6)])
        plan, left = sessions.plan_blocks(rows, need=8, max_per_day=2)
        self.assertEqual(left, 0)
        self.assertEqual(len(plan), 4)
        self.assertEqual(len({d for d, _, _ in plan}), 4)

    def test_lunch_is_not_used_for_blocks(self):
        # 11:30-13:30 しか空いていない日。昼を避けると 13:00-13:30 に置かれる
        rows = self._rows([(3, 4, [(11 * 60 + 30, 13 * 60 + 30)])])
        plan, _ = sessions.plan_blocks(rows, need=1, max_per_day=4)
        self.assertEqual(len(plan), 1)
        start, end = plan[0][1], plan[0][2]
        self.assertFalse(start < sessions.LUNCH_END and end > sessions.LUNCH_START)

    def test_blocked_day_gets_nothing(self):
        rows = self._rows([(3, 0, []), (4, 4, [(9 * 60, 21 * 60)])])
        plan, left = sessions.plan_blocks(rows, need=2, max_per_day=4)
        self.assertEqual(left, 0)
        self.assertEqual(plan[0][0].day, 4)

    def test_reports_unplaced_slots_instead_of_silently_dropping(self):
        rows = self._rows([(3, 1, [(9 * 60, 9 * 60 + 30)])])
        plan, left = sessions.plan_blocks(rows, need=8, max_per_day=4)
        self.assertEqual(len(plan), 1)
        self.assertEqual(left, 7)

    def test_thirty_minute_task_gets_thirty_minute_block(self):
        rows = self._rows([(3, 4, [(9 * 60, 21 * 60)])])
        plan, left = sessions.plan_blocks(rows, need=1, max_per_day=2)
        self.assertEqual(plan[0][2] - plan[0][1], 30)
        self.assertEqual(left, 0)


class TestSplitLunch(unittest.TestCase):
    def test_interval_spanning_lunch_is_split(self):
        self.assertEqual(sessions.split_lunch([(9 * 60, 21 * 60)]),
                         [(9 * 60, 12 * 60), (13 * 60, 21 * 60)])

    def test_fragment_under_min_gap_is_dropped(self):
        # 11:50-13:00 → 昼前は10分しか残らないので捨てる
        self.assertEqual(sessions.split_lunch([(11 * 60 + 50, 13 * 60)]), [])


if __name__ == "__main__":
    unittest.main()

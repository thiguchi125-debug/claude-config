import importlib.util
import json
import os
import sys
import tempfile
import unittest

_SKILL_DIR = os.path.expanduser("~/.claude/skills/task-add")
if _SKILL_DIR not in sys.path:            # task_windows を PYTHONPATH 無しで import する
    sys.path.insert(0, _SKILL_DIR)
_SCRIPT = os.path.join(_SKILL_DIR, "sessions.py")
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
        # 昼前の空きが10分しかない日。昼を避けて 13時以降に置かれる
        rows = self._rows([(3, 4, [(11 * 60 + 50, 15 * 60)])])
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
        rows = self._rows([(3, 4, [(9 * 60, 21 * 60)])])
        plan, left = sessions.plan_blocks(rows, need=8, max_per_day=2)
        self.assertEqual(len(plan), 1)
        self.assertEqual(left, 6)

    def test_thirty_minute_gap_between_events_is_not_used_for_placement(self):
        # コマ数としては1コマと数えるが、前後に予定が接しているので実際には置けない
        # （移動・片付けのバッファ。2026-08-06 の見直しで追加）
        rows = self._rows([(3, 1, [(10 * 60, 10 * 60 + 30)])])
        plan, left = sessions.plan_blocks(rows, need=1, max_per_day=4)
        self.assertEqual(plan, [])
        self.assertEqual(left, 1)

    def test_thirty_minute_task_gets_thirty_minute_block(self):
        rows = self._rows([(3, 4, [(9 * 60, 21 * 60)])])
        plan, left = sessions.plan_blocks(rows, need=1, max_per_day=2)
        self.assertEqual(plan[0][2] - plan[0][1], 30)
        self.assertEqual(left, 0)


class TestRealismFilters(unittest.TestCase):
    """現実性フィルタ（2026-08-06 の失敗を受けて追加）。

    空き時間があるという理由だけで、日曜の市役所照会や18時以降の照会を
    置いてしまった。相手がいる時間かどうかを配置側で効かせる。
    """

    def _rows(self, specs):
        import datetime
        return [(datetime.date(2026, 8, d), n, "", free) for d, n, free in specs]

    def test_buffer_is_taken_from_edges_touching_events(self):
        # 10:00-11:00 が空き（前後に予定あり）→ 前後15分ずつ削れて10:15-10:45
        self.assertEqual(sessions.apply_buffer([(10 * 60, 11 * 60)]),
                         [(10 * 60 + 15, 10 * 60 + 45)])

    def test_buffer_not_taken_from_band_edges(self):
        # 稼働帯の端は予定と接していないので削らない
        self.assertEqual(sessions.apply_buffer([(sessions.BAND_START, sessions.BAND_END)]),
                         [(sessions.BAND_START, sessions.BAND_END)])

    def test_buffer_drops_intervals_that_become_too_short(self):
        self.assertEqual(sessions.apply_buffer([(10 * 60, 10 * 60 + 45)]), [])

    def test_clip_windows_restricts_to_office_hours(self):
        self.assertEqual(
            sessions.clip_windows([(9 * 60, 21 * 60)], [(9 * 60, 17 * 60)]),
            [(9 * 60, 17 * 60)])

    def test_clip_windows_empty_means_no_placement(self):
        self.assertEqual(sessions.clip_windows([(9 * 60, 21 * 60)], []), [])

    def test_office_task_gets_nothing_on_sunday(self):
        import task_windows
        # 2026-08-09 は日曜。役所タスクは置けず、翌10日(月)へ流れる
        rows = self._rows([(9, 4, [(9 * 60, 21 * 60)]), (10, 4, [(9 * 60, 21 * 60)])])
        kind, skip = task_windows.classify("学校教育課へ照会")
        self.assertIsNone(skip)
        plan, left = sessions.plan_blocks(rows, 2, 2,
                                          window_fn=task_windows.window_fn(kind))
        self.assertEqual(left, 0)
        self.assertEqual(plan[0][0].day, 10)

    def test_office_task_is_not_placed_after_seventeen(self):
        import task_windows
        # 月曜だが17:30以降しか空いていない → 置けない
        rows = self._rows([(10, 4, [(17 * 60 + 30, 21 * 60)])])
        kind, _ = task_windows.classify("建設部へ照会")
        plan, left = sessions.plan_blocks(rows, 2, 2,
                                          window_fn=task_windows.window_fn(kind))
        self.assertEqual(plan, [])
        self.assertEqual(left, 2)

    def test_desk_task_may_use_the_evening(self):
        import task_windows
        rows = self._rows([(9, 4, [(17 * 60 + 30, 21 * 60)])])
        kind, _ = task_windows.classify("菅内版市政報告レポート作成")
        self.assertEqual(kind.key, "desk")
        plan, _ = sessions.plan_blocks(rows, 2, 2,
                                       window_fn=task_windows.window_fn(kind))
        self.assertTrue(plan)


class TestTaskWindows(unittest.TestCase):
    def test_waiting_label_is_skipped(self):
        import task_windows
        kind, skip = task_windows.classify("段差の件", labels=["結果待ち"])
        self.assertIsNone(kind)
        self.assertIn("結果待ち", skip)

    def test_waiting_in_title_is_skipped(self):
        import task_windows
        for title in ("国1バイパス側道の段差 連絡待ち",
                      "油流出事故対応は川合自治会の協議待ち"):
            kind, skip = task_windows.classify(title)
            self.assertIsNone(kind, msg=title)

    def test_office_beats_contact_when_both_match(self):
        import task_windows
        # 「担当課へ連絡」は連絡でもあるが、窓口が開いている時間の制約が勝つ
        kind, _ = task_windows.classify("担当課へ連絡して状況を確認")
        self.assertEqual(kind.key, "office")

    def test_field_check_is_daylight_all_week(self):
        import task_windows
        kind, _ = task_windows.classify("交差点の草木見通し不良を現地確認")
        self.assertEqual(kind.key, "field")
        self.assertEqual(kind.end, 18 * 60)

    def test_resident_contact_allows_weekend_evening(self):
        import task_windows
        kind, _ = task_windows.classify("宮村さんへ制度案内を回答")
        self.assertEqual(kind.key, "contact")
        self.assertEqual(kind.end, 20 * 60)

    def test_unknown_task_defaults_to_desk(self):
        import task_windows
        kind, skip = task_windows.classify("のど自慢事業")
        self.assertIsNone(skip)
        self.assertEqual(kind.key, "desk")


class TestGreetingReserve(unittest.TestCase):
    """挨拶回り優先枠 15:00-18:30（2026-08-07 草川指示）。"""

    def _rows(self, specs):
        import datetime
        return [(datetime.date(2026, 8, d), n, "", free) for d, n, free in specs]

    def test_split_greeting_removes_the_window(self):
        self.assertEqual(sessions.split_greeting([(9 * 60, 21 * 60)]),
                         [(9 * 60, 15 * 60), (18 * 60 + 30, 21 * 60)])

    def test_no_block_lands_in_greeting_window(self):
        rows = self._rows([(10, 4, [(9 * 60, 21 * 60)])])
        plan, _ = sessions.plan_blocks(rows, need=4, max_per_day=4)
        for _d, s, e in plan:
            self.assertFalse(s < sessions.GREETING_END and e > sessions.GREETING_START)

    def test_day_with_only_greeting_window_free_gets_nothing(self):
        rows = self._rows([(10, 4, [(15 * 60, 18 * 60 + 30)])])
        plan, left = sessions.plan_blocks(rows, need=2, max_per_day=4)
        self.assertEqual(plan, [])
        self.assertEqual(left, 2)

    def test_explicit_override_opens_the_window(self):
        # 草川が「今日はこの時間に作業を入れられる」と言った日だけ開ける
        rows = self._rows([(10, 4, [(15 * 60, 18 * 60 + 30)])])
        plan, left = sessions.plan_blocks(rows, need=2, max_per_day=4,
                                          reserve_greeting=False)
        self.assertTrue(plan)
        self.assertEqual(left, 0)

    def test_evening_after_greeting_window_is_still_usable(self):
        # 18:30以降は空いているので、夜の連絡タスクは置ける
        rows = self._rows([(10, 4, [(18 * 60 + 30, 21 * 60)])])
        plan, left = sessions.plan_blocks(rows, need=2, max_per_day=4)
        self.assertTrue(plan)
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


class TestEarlyMorningDesk(unittest.TestCase):
    """早朝5:00-7:00の机上作業帯（2026-08-07 草川指示）。"""

    def _rows(self, specs, band):
        import datetime
        return [(datetime.date(2026, 8, d), n, "", free) for d, n, free in specs]

    def test_desk_kind_opens_the_early_band(self):
        import task_windows
        kind, _ = task_windows.classify("菅内版市政報告レポート作成")
        self.assertEqual(kind.key, "desk")
        self.assertTrue(kind.early)
        self.assertEqual(kind.band(), (5 * 60, 21 * 60))

    def test_office_kind_does_not_open_the_early_band(self):
        import task_windows
        kind, _ = task_windows.classify("建設部へ照会")
        self.assertFalse(kind.early)
        self.assertEqual(kind.band(), (9 * 60, 21 * 60))

    def test_desk_block_can_land_before_seven(self):
        import task_windows, datetime
        kind, _ = task_windows.classify("レポート作成")
        rows = [(datetime.date(2026, 8, 10), 4, "", [(5 * 60, 7 * 60)])]
        plan, left = sessions.plan_blocks(rows, 2, 2,
                                          window_fn=task_windows.window_fn(kind),
                                          band=kind.band())
        self.assertEqual(left, 0)
        self.assertLess(plan[0][1], 7 * 60)

    def test_office_task_cannot_use_the_early_band(self):
        import task_windows, datetime
        kind, _ = task_windows.classify("学校教育課へ照会")
        rows = [(datetime.date(2026, 8, 10), 4, "", [(5 * 60, 7 * 60)])]
        plan, left = sessions.plan_blocks(rows, 2, 2,
                                          window_fn=task_windows.window_fn(kind),
                                          band=kind.band())
        self.assertEqual(plan, [])
        self.assertEqual(left, 2)

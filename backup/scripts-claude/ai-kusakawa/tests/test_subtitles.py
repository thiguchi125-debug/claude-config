import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path.home() / ".claude/scripts/ai-kusakawa"))
from engine.subtitles import chunk_phrases, build_subs_html
from engine import config


def _mk(text):
    """等間隔0.1秒/文字のダミータイムスタンプを生成"""
    chars = list(text)
    starts = [i * 0.1 for i in range(len(chars))]
    ends = [(i + 1) * 0.1 for i in range(len(chars))]
    return chars, starts, ends


class TestChunk(unittest.TestCase):
    def test_splits_on_punctuation(self):
        ph = chunk_phrases(*_mk("こんにちは。AIくさかわです。"))
        self.assertEqual([p["text"] for p in ph], ["こんにちは。", "AIくさかわです。"])
        self.assertAlmostEqual(ph[0]["start"], 0.0)
        self.assertAlmostEqual(ph[1]["start"], 0.6, places=5)

    def test_splits_long_phrase_at_max_len(self):
        ph = chunk_phrases(*_mk("あ" * 40))  # 句読点なし40文字
        self.assertTrue(all(len(p["text"]) <= 16 for p in ph))
        self.assertEqual(sum(len(p["text"]) for p in ph), 40)

    def test_timestamps_monotonic(self):
        ph = chunk_phrases(*_mk("市政を、動かす。声を、チカラに。"))
        for a, b in zip(ph, ph[1:]):
            self.assertLessEqual(a["end"], b["start"] + 1e-9)


class TestSubsHtml(unittest.TestCase):
    def test_blocks_and_band_height(self):
        ph = chunk_phrases(*_mk("こんにちは。AIくさかわです。"))
        body = build_subs_html(ph)
        self.assertEqual(body.count('class="line"'), 2)
        self.assertIn("こんにちは。", body)
        self.assertIn("AIくさかわです。", body)
        self.assertIn(f"height:{config.SUB_BLOCK_H}px", body)  # 字幕帯220px=y1240-1460
        self.assertIn("background:transparent", body)

    def test_html_escapes_special_chars(self):
        body = build_subs_html([{"text": "A<B&C", "start": 0, "end": 1}])
        self.assertIn("A&lt;B&amp;C", body)


if __name__ == "__main__":
    unittest.main()

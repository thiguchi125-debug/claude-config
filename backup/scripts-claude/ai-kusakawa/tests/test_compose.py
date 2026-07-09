import sys, unittest, tempfile
from pathlib import Path
sys.path.insert(0, str(Path.home() / ".claude/scripts/ai-kusakawa"))
from engine.compose import write_concat, subs_overlay_chain
from engine import config


class TestConcat(unittest.TestCase):
    def test_concat_format(self):
        pngs = {0: Path("/tmp/m0.png"), 1: Path("/tmp/m1.png"), 2: Path("/tmp/m2.png")}
        with tempfile.TemporaryDirectory() as d:
            out = write_concat([(0, 1.5), (2, 0.2), (0, 0.1)], pngs, Path(d) / "c.txt")
            body = out.read_text()
        lines = body.strip().splitlines()
        self.assertEqual(lines[0], "file '/tmp/m0.png'")
        self.assertEqual(lines[1], "duration 1.500000")
        self.assertEqual(lines[2], "file '/tmp/m2.png'")
        # concat demuxer仕様: 最終エントリはduration行の後にfile行を重ねて閉じる
        self.assertEqual(lines[-1], "file '/tmp/m0.png'")


class TestSubsChain(unittest.TestCase):
    def test_chain_structure(self):
        chain = subs_overlay_chain(
            2, [(0.0, 1.0), (1.0, 2.5)], offset=1.5,
            in_label="v2", sheet_label="4:v", out_label="vsub")
        self.assertIn("split=2[sh0][sh1]", chain)
        self.assertIn(f"crop={config.W}:{config.SUB_BLOCK_H}:0:0[s0]", chain)
        self.assertIn(f"crop={config.W}:{config.SUB_BLOCK_H}:0:{config.SUB_BLOCK_H}[s1]", chain)
        self.assertIn(f"overlay=0:{config.SUB_BAND[0]}:enable='between(t,1.500,2.500)'[o0]", chain)
        self.assertIn("between(t,2.500,4.000)'[vsub]", chain)

    def test_zero_phrases_passthrough(self):
        chain = subs_overlay_chain(0, [], offset=1.5, in_label="v2",
                                   sheet_label="4:v", out_label="vsub")
        self.assertEqual(chain, "[v2]null[vsub]")


if __name__ == "__main__":
    unittest.main()

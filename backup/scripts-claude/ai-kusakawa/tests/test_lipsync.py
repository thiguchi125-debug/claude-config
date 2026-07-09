import sys, unittest
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path.home() / ".claude/scripts/ai-kusakawa"))
from engine.lipsync import states_from_samples, to_intervals
from engine import config

SR = 22050


class TestStates(unittest.TestCase):
    def test_silence_is_closed(self):
        s = states_from_samples(np.zeros(SR * 2, dtype=np.float32), SR)
        self.assertEqual(len(s), 2 * config.FPS)
        self.assertTrue(all(x == 0 for x in s))

    def test_loud_speech_opens_mouth(self):
        t = np.linspace(0, 2, SR * 2, dtype=np.float32)
        loud = np.sin(2 * np.pi * 220 * t).astype(np.float32)
        s = states_from_samples(loud, SR)
        self.assertGreater(sum(1 for x in s if x == 2), len(s) * 0.5)

    def test_alternating_produces_multiple_states(self):
        t = np.linspace(0, 1, SR, dtype=np.float32)
        tone = np.sin(2 * np.pi * 220 * t).astype(np.float32)
        sig = np.concatenate([tone, np.zeros(SR, dtype=np.float32),
                              tone * 0.3, np.zeros(SR, dtype=np.float32)])
        s = states_from_samples(sig, SR)
        self.assertEqual(sorted(set(s)), [0, 1, 2])


class TestIntervals(unittest.TestCase):
    def test_merge_and_lead(self):
        iv = to_intervals([0, 0, 2, 2, 2, 1], lead_silence=1.5)
        self.assertEqual(iv[0], (0, 1.5))
        self.assertEqual(iv[1], (0, 2 / config.FPS))
        self.assertEqual(iv[2], (2, 3 / config.FPS))
        self.assertEqual(iv[3], (1, 1 / config.FPS))
        self.assertAlmostEqual(sum(d for _, d in iv), 1.5 + 6 / config.FPS)


if __name__ == "__main__":
    unittest.main()

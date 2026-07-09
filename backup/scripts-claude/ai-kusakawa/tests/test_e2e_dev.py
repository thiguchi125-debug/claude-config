import subprocess, sys, unittest
from pathlib import Path

BASE = Path.home() / ".claude/scripts/ai-kusakawa"
sys.path.insert(0, str(BASE))
from engine import config  # noqa: E402

OUT = Path.home() / "outputs/ai-kusakawa/_e2e_test"


class TestE2EDev(unittest.TestCase):
    def test_generates_valid_mp4(self):
        script = OUT / "script.txt"
        OUT.mkdir(parents=True, exist_ok=True)
        script.write_text("こんにちは、AIくさかわです。今日は亀山市のコミュニティバスの話をします。運賃は小中学生100円、高校生以上200円です。")
        subprocess.run(
            ["python3", str(BASE / "generate.py"), str(script),
             "--dev", "--out-dir", str(OUT)],
            check=True, capture_output=True, text=True)
        mp4 = OUT / "final.mp4"
        self.assertTrue(mp4.exists())
        probe = subprocess.run(
            [config.FFPROBE, "-v", "error", "-show_entries",
             "stream=codec_type,width,height:format=duration",
             "-of", "csv", str(mp4)],
            capture_output=True, text=True, check=True).stdout
        self.assertIn("video,1080,1920", probe)
        self.assertIn("audio", probe)
        dur = float(probe.strip().splitlines()[-1].split(",")[1])
        self.assertGreater(dur, config.INTRO_SEC + 3)   # intro+音声が入っている
        self.assertLess(dur, config.MAX_DURATION)


if __name__ == "__main__":
    unittest.main()

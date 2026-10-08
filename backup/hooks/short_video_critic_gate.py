#!/usr/bin/env python3
"""
ショート動画の台本が「ゲートを通った完成品」になったのに辛口審査が無いまま
ターンを終えようとしたら、Stop を止めて short-video-harsh-critic の起動を促す hook。

なぜ必要か（2026-10-08 3本柱シリーズ第5回）:
  台本v5は fact・risk を通り、作り手の自己採点も66/80で合格だったが、
  草川に「厳しめに分析して」と言われて別の目で見ると26/80だった。
  ゲートは「間違っていないか」しか見ず、「見られるか」を誰も見ていなかった。
  草川「毎回完成品ができたら自動的にチェックできるようにして」。

対象:
  ~/Documents/ObsidianVault/50_発信/ 配下で、直近3時間に更新された
  台本ファイル（台本_v<n>.md／*ショート動画台本*.md）のうち、
  冒頭20行に「通過」（「未通過」は除く）があり、
  同じフォルダに 辛口審査_<ファイル名> が無いもの。
  台本に <!-- NO-CRITIC --> と書けば対象外。

失敗時・2回目の Stop（stop_hook_active）はすべて素通し（作業を止め続けない）。
"""
import sys, os, json, re, time, glob

ROOT = os.path.expanduser("~/Documents/ObsidianVault/50_発信")
WINDOW = 3 * 3600
NAME = re.compile(r"(^台本_v[\d.]+[^/]*\.md$)|(ショート動画台本.*\.md$)")
PASSED = re.compile(r"(?<!未)通過")


def pending():
    now = time.time()
    out = []
    for p in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
        b = os.path.basename(p)
        if b.startswith("辛口審査_") or not NAME.search(b):
            continue
        try:
            if now - os.path.getmtime(p) > WINDOW:
                continue
            with open(p, encoding="utf-8") as f:
                head = "".join(f.readline() for _ in range(20))
        except Exception:
            continue
        # 冒頭に「未通過」があれば台本自身は未通過（他ファイルの「通過済み」への言及に釣られない）
        if "NO-CRITIC" in head or "未通過" in head or not PASSED.search(head):
            continue
        out.append(p)
    # 同じフォルダでは最新版（更新が新しいもの）だけを見る。旧版を審査させない
    latest = {}
    for p in out:
        d = os.path.dirname(p)
        if d not in latest or os.path.getmtime(p) > os.path.getmtime(latest[d]):
            latest[d] = p
    # 最新版を決めてから、審査済みかを見る（先に除くと旧版が繰り上がる）
    return [p for p in latest.values()
            if not os.path.exists(os.path.join(os.path.dirname(p), "辛口審査_" + os.path.basename(p)))]


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("stop_hook_active"):
        return 0
    try:
        files = pending()
    except Exception:
        return 0
    if not files:
        return 0
    lst = "\n".join("- " + f for f in files[:5])
    print(json.dumps({
        "decision": "block",
        "reason": (
            "ゲートを通った動画台本に辛口審査がまだありません。草川に出す前に "
            "short-video-harsh-critic を起動して審査し、同じフォルダに 辛口審査_<台本名> を保存して、"
            "合計点・判定を草川への報告に入れてください（判定が「作り直す」なら差し替え案も）。\n" + lst +
            "\n審査が不要な台本は冒頭に <!-- NO-CRITIC --> を書けば対象外になります。"
        ),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

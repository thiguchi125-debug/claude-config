#!/usr/bin/env python3
"""
発信物フォーマットゲート（機械可読・記憶依存をやめるための実装）

ブログ／SNS7種／ショート動画原稿が、各agent・SKILLの規定に収まっているかを自動判定する。
check_subtitle_band.py（ショート動画の字幕帯ゲート）と同じ思想で、
「ルールをmarkdownに書いておく」から「機械が落とす」へ移す。

正本:
  ブログ  = ~/.claude/agents/blog-writer.md（1500-2500字・5段構成厳守）
  SNS     = ~/.claude/agents/sns-content-creator.md（PF別字数）
  動画    = ~/.claude/skills/short-video-create/SKILL.md（35-45秒・憲法5構成）
            ~/.claude/agents/short-video-virality-architect.md

使い方:
  python3 check_content_limits.py <file.md> [<file.md> ...]
  種別はファイル名から自動判定（SNS7種 / ショート動画原稿 / それ以外=ブログ）

終了コード: 全PASSなら0、1件でもFAILなら1（フック・CIに載せられる）
"""
import sys, re, os

SNS_LIMITS = {  # 表示名の接頭辞 -> (下限, 上限)  ※上限Noneは字数制限なし
    "X":              (None, None),   # X Premium課金済み＝字数上限なし（sns-content-creator.md準拠）
    "Threads":        (300, 500),
    "Instagram":      (600, 1000),
    "Facebook":       (500, 800),
    "LINE":           (200, 500),   # 2026-09-02 草川確認: 上限は500字（feedback_line_500chars_no_hashtag）
}
MAX_TAGS = {"X": 4, "Instagram": 5}   # ハッシュタグ上限
BLOG_TIERS = [("標準", 1500, 2500), ("深掘り", 2500, 4500), ("徹底解説", 4500, 8000)]
NORMAL_TIER = ("ノーマル", 800, 1500)  # blog-writer-normal.md（市民向け活動報告・5段構成の縛りなし）
BLOG_STAGES = ["現場の声", "全国", "制度", "亀山", "締め"]  # 5段構成の手がかり
VIDEO_MIN_SEC, VIDEO_MAX_SEC = 35, 45
VIDEO_CHARS_PER_SEC = 7.0        # 日本語ナレの上限目安
VIDEO_MAX_SENTENCE = 30          # 一文30字超はanti-pattern

def n_chars(t):
    return len(re.sub(r"\s", "", t))

# --- 種別判定 -------------------------------------------------------------
# 2026-09-02 修正: 以前はファイル名の部分文字列だけで種別を決めていた。そのため
# SNS7種セットや動画台本を「SNS」「動画」を含まない名前で渡すと全部 blog 判定になり、
# 「字数範囲外」「冒頭の名乗りがない」「定型フッター欠落」で必ず違反3件が出ていた。
# gate.py は機械チェック全PASSを記録の前提にしているので指紋が残らず、
# Notion書き込みが content_safety_gate.py に deny され続ける事故になっていた。
# → ファイル名のヒントは残したうえで、決まらなければ中身を見て判定する。

SNS_ALIASES = [   # 見出し表記のゆれ -> SNS_LIMITS のキー（長い名前を先に並べる）
    ("公式LINE", "LINE"), ("X（旧Twitter）", "X"), ("X (旧Twitter)", "X"),
    ("Threads", "Threads"), ("Instagram", "Instagram"), ("Facebook", "Facebook"),
    ("LINE", "LINE"), ("X", "X"),
]
PF_HEAD_WORDS = ("Threads", "Instagram", "Facebook", "LINE", "YouTube", "TikTok",
                 "公式LINE", "X（旧Twitter）", "X (旧Twitter)")
INTERNAL_NAME_HINTS = ("メモ", "聞き取り", "様式", "memo", "hearing",
                       "作業記録", "引き継ぎ", "HANDOFF", "handoff",
                       "台帳", "ファクトシート", "factsheet", "_notion_body")

def _norm_head(name):
    """見出しから飾りを剥がす。『## 【Threads】論点＝…』→『Threads 論点＝…』"""
    s = name.strip()
    s = re.sub(r"^[^0-9A-Za-z぀-ヿ一-鿿]+", "", s)  # 先頭の記号・絵文字
    return s.replace("【", "").replace("】", " ").strip()

def sns_key(name):
    """見出し名から SNS_LIMITS のキーを引く。見つからなければ None。"""
    head = _norm_head(name)[:16]
    for alias, key in SNS_ALIASES:
        if head.startswith(alias):
            return key
    return None

def kind_and_reason(path, text=None):
    """(種別, 判定理由) を返す。理由も出すのは、誤判定に目で気づけるようにするため。"""
    b = os.path.basename(path)
    # 1) ファイル名の明示指定を最優先（従来互換）
    if "SNS" in b or "sns" in b:
        return "sns", "ファイル名に SNS"
    if "動画" in b or "video" in b:
        return "video", "ファイル名に 動画/video"
    if any(k in b for k in INTERNAL_NAME_HINTS):
        return "internal", "ファイル名が内部資料"
    # 2) ファイル名で決まらなければ中身を見る
    if text is None:
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            return "blog", "本文を読めずフォールバック"
    heads = re.findall(r"^#{1,4}\s*(.+?)\s*$", text, flags=re.M)
    pf_hits = sum(1 for h in heads
                  if any(_norm_head(h)[:16].startswith(w) for w in PF_HEAD_WORDS))
    if pf_hits >= 3:
        return "sns", f"本文にプラットフォーム見出し{pf_hits}件"
    if re.search(r"カット表|尺の内訳|セリフ連続版", text) or \
       re.search(r"^\|\s*[A-Za-z]?\d+\s*\|\s*\d+:\d\d", text, flags=re.M):
        return "video", "本文にカット表・尺の記述"
    return "blog", "ファイル名・本文とも該当なし（既定＝ブログ）"

def kind_of(path, text=None):
    return kind_and_reason(path, text)[0]

def is_normal_blog(path):
    return "ノーマル" in os.path.basename(path)

def check_sns(text):
    out = []
    for sec in re.split(r"\n## ", text)[1:]:
        name = sec.split("\n")[0].strip()
        raw  = "\n".join(sec.split("\n")[1:])
        body = re.sub(r"^\s*\*\*\d/\d\*\*\s*$", "", raw, flags=re.M)  # スレッド番号除去（字数用）
        n = n_chars(body)
        key = sns_key(name)   # 『## 【Threads】論点＝…』のような飾り付き見出しも拾う
        if key is None:
            continue
        lo, hi = SNS_LIMITS[key]
        # スレッドは投稿単位で数える（**2/4** 等で分割）
        units = re.split(r"^\s*\*\*\d/\d\*\*\s*$", raw, flags=re.M)
        units = [u for u in units if u.strip()] or [body]
        if key in MAX_TAGS:
            worst = max(len(re.findall(r"#\S+", u)) for u in units)
            if worst > MAX_TAGS[key]:
                out.append((False, f"{name}: 1投稿あたりハッシュタグ{worst}個 > 上限{MAX_TAGS[key]}個"))
            else:
                out.append((True, f"{name}: ハッシュタグ最大{worst}個/投稿"))
        if hi and n > hi:
            out.append((False, f"{name}: {n}字 > 上限{hi}字"))
        elif lo and n < lo:
            out.append((False, f"{name}: {n}字 < 下限{lo}字"))
        else:
            out.append((True, f"{name}: {n}字"))
        # ハッシュタグ規定
        has_tag = "#" in body
        if key == "Threads" and has_tag:
            out.append((False, f"{name}: Threadsにハッシュタグ（規定=なし）"))
        if key == "LINE" and has_tag:
            out.append((False, f"{name}: LINEにハッシュタグ（規定=なし）"))
        if key == "X" and not has_tag:
            out.append((False, f"{name}: Xにハッシュタグなし（規定=必須）"))
    if "<BLOG_URL>" in text:
        # 下書き保存の時点では正常。実URLへの差し替えが要るのは「投稿」の直前で、
        # 投稿は各PFで草川が手作業で行うためチェッカーからは強制できない。
        # よってFAILではなく警告として可視化する（見落とし防止）。
        out.append((True, "⚠ プレースホルダ <BLOG_URL> あり — **投稿前に実URLへ差し替えること**"))
    return out

def check_blog(text, normal_mode=False):
    out = []
    body = re.split(r"\n【出典】|\n### 出典|\n## 出典", text)[0]
    body = re.split(r"◆亀山市政や", body)[0]
    n = n_chars(re.sub(r"^#.*$", "", body, flags=re.M))
    exc = re.findall(r"FORMAT-EXCEPTION:\s*(\S+)", text)   # 承認済み逸脱の明示マーカー
    if normal_mode:
        # blog-writer-normal.md：市民向け活動報告。5段構成の縛りはなく、800-1500字。
        _, lo0, hi0 = NORMAL_TIER
        if lo0 <= n <= hi0:
            out.append((True, f"本文 {n}字 → ノーマルモード"))
        else:
            out.append((False, f"本文 {n}字（ノーマルモード規定 {lo0}〜{hi0}字の範囲外）"))
        heads = re.findall(r"^(?:##\s*|■\s*)(.+)$", body, flags=re.M)
        out.append((len(heads) >= 2, f"見出し {len(heads)}本（ノーマルモードは2本以上）"))
    else:
        tier = next((t for t, lo, hi in BLOG_TIERS if lo <= n <= hi), None)
        lo0, hi0 = BLOG_TIERS[0][1], BLOG_TIERS[-1][2]
        if tier:
            out.append((True, f"本文 {n}字 → {tier}モード"))
        elif n > hi0 and "字数" in " ".join(exc):
            # 草川が「字数上限を理由に内容を削るな」と明示承認した回だけ通す。
            # 承認は本文冒頭の <!-- FORMAT-EXCEPTION: 字数 / 承認日 / 理由 --> で記録する。
            out.append((True, f"本文 {n}字 ⚠承認済み例外（規定 上限{hi0}字）"))
        else:
            out.append((False, f"本文 {n}字（{lo0}〜{hi0}字の範囲外）"))
        heads = re.findall(r"^(?:##\s*|■\s*)(.+)$", body, flags=re.M)
        out.append((len(heads) >= 4, f"見出し {len(heads)}本（5段構成の骨格が要る）"))
    first = body.strip().split("\n")
    named = any("草川たくやです" in l for l in first[:4])
    out.append((named, "冒頭の名乗り"))
    if "【ご意見箱】" not in text or "AIインタビュー" not in text:
        out.append((False, "定型フッター欠落（ご意見箱／LINE／Threads／AIインタビュー）"))
    else:
        out.append((True, "定型フッター"))
    return out

def check_video(text):
    out = []
    body = text
    exc = re.findall(r"FORMAT-EXCEPTION:\s*(\S+)", text)   # 承認済み逸脱の明示マーカー
    # --- 憲法5構成 ---
    cold = re.search(r"（0:00[^）]*）[^\n]*\n+([^\n]+)", body)
    if cold and "草川たくやです" in cold.group(1):
        out.append((False, "冒頭が名乗り＝コールドオープン逸脱（憲法・出荷拒否）"))
    else:
        out.append((True, "コールドオープン"))
    out.append((("多いんです" in body or "撮って" in body or "公表しました" in body),
                "「撮っている理由」（憲法・出荷拒否）"))
    out.append((("必ず実現" in body or "あきらめません" in body),
                "結びの決意（憲法・出荷拒否）"))
    out.append((("コメントで教えてください" in body), "コメント誘発CTA"))
    # --- 尺 ---
    ends = [int(m[1]) for m in re.findall(r"0:(\d\d)-0:(\d\d)", body)]
    if ends:
        total = max(ends)
        if VIDEO_MIN_SEC <= total <= VIDEO_MAX_SEC:
            out.append((True, f"尺 {total}秒"))
        elif "尺" in " ".join(exc):
            out.append((True, f"尺 {total}秒 ⚠承認済み例外（規定 {VIDEO_MIN_SEC}〜{VIDEO_MAX_SEC}秒）"))
        else:
            out.append((False, f"尺 {total}秒（規定 {VIDEO_MIN_SEC}〜{VIDEO_MAX_SEC}秒）"))
    # --- カット数 ---
    cuts = len(re.findall(r"^\|\s*\d+\s*\|", body, flags=re.M))
    if cuts:
        need = 15
        out.append((cuts >= need, f"カット数 {cuts}（60秒で{need}以上が基準）"))
    # --- 一文30字超（セリフ節のみ・注記行は除外）---
    m = re.search(r"##\s*セリフ[^\n]*\n(.*?)(?=\n---|\n##\s)", body, flags=re.S)
    serifu = m.group(1) if m else ""
    lines = [l.strip() for l in serifu.split("\n")
             if l.strip() and not l.strip().startswith(("**", ">", "※", "（", "#", "|", "-"))]
    longs = [x.strip() for l in lines for x in re.split(r"(?<=。)", l)
             if x.strip() and n_chars(x) > VIDEO_MAX_SENTENCE]
    out.append((not longs, f"セリフの一文30字超 {len(longs)}件"
                + (f" 例:「{longs[0][:34]}…」" if longs else "")))
    return out

def check_internal(text):
    """内部資料。ブログ規定は当てない。事故が起きやすい点だけ見る。"""
    out = []
    out.append((True, f"本文 {n_chars(text)}字（内部資料＝字数上限なし）"))
    # 内部資料に実名・電話番号が生で入ったまま共有物に化ける事故を防ぐ。
    # 空欄の様式なら当然ゼロ。記入後にこのチェックを再実行すれば引っかかる。
    tel = re.findall(r"0\d{1,4}-\d{1,4}-\d{3,4}", text)
    tel = [t for t in tel if t not in ("0595-96-8822", "0595-82-8180")]  # 市の公開窓口は除外
    out.append((not tel, "市の公開窓口以外の電話番号 "
                + (f"{len(tel)}件（記入済みならDrive 00_名簿・個人情報/へ。Notionには置かない）"
                   if tel else "なし")))
    return out

def main(argv):
    forced = None
    files = []
    for a in argv:
        if a.startswith("--kind="):
            forced = a.split("=", 1)[1].strip()
        else:
            files.append(a)
    if not files:
        print("usage: check_content_limits.py [--kind=blog|sns|video|internal] <file.md> ...")
        return 1
    if forced and forced not in ("blog", "sns", "video", "internal"):
        print(f"unknown --kind={forced}（blog|sns|video|internal のいずれか）"); return 1
    fail = 0
    for f in files:
        text = open(f, encoding="utf-8").read()
        if forced:
            k, why = forced, "--kind で明示指定"
        else:
            k, why = kind_and_reason(f, text)
        print(f"\n== {os.path.basename(f)}  [{k}] ({why}) ==")
        if k == "blog":
            res = check_blog(text, normal_mode=is_normal_blog(f))
        elif k == "internal":
            res = check_internal(text)
        else:
            res = {"sns": check_sns, "video": check_video}[k](text)
        for ok, msg in res:
            print(("  ✅ " if ok else "  🚨 ") + msg)
            if not ok: fail += 1
    print(f"\n-- 違反 {fail}件 --")
    return 1 if fail else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""
発信物のNotion書き込みを、安全ゲート未通過なら deny する PreToolUse hook。

todoist_calendar_guard.py と同じ思想：ルールをmarkdownに書いておくのをやめ、
出口で機械的に止める。

止める対象:
  notion-create-pages / notion-update-page のうち、**本文（content / new_str /
  content_updates）を伴う呼び出し**だけ。プロパティだけの更新は素通しする。
  本文＝市民が読む文章なので、ここが発信の境界。

通す条件:
  ~/.claude/hooks/_content_gate.json に、**その本文と一致する指紋**が
  記録されていること。記録は `python3 ~/.claude/scripts/gate.py <files...>` が作る。
  本文を1文字でも変えたら指紋が変わり、再度ゲートを通すまで書き込めない。

なぜ必要か（2026-08-05〜06 の実例）:
  1. 「Notionに保存するだけ」を発信ではなくファイリングと解釈し、fact/riskを飛ばした。
  2. 画像を「仕様に合わせて作り直すだけ」＝デザイン作業と解釈し、また飛ばした。
     このとき risk-reviewer が必須とした一文（「亀山市も、0%です。」＝被災地への
     指弾を自分事化する装置）をレイアウト都合で削り、指摘前より悪化させた。
  どちらも「本文が変わったのに、本文の変更だと認識しなかった」ことが原因。
  人間の注意力ではなく指紋で検出する。
"""
import sys, os, json, re, hashlib, time, unicodedata

GATE = os.path.expanduser("~/.claude/hooks/_content_gate.json")
GUARDED = {
    "mcp__claude_ai_Notion__notion-create-pages",
    "mcp__claude_ai_Notion__notion-update-page",
}

# ── 内部運用ログの除外（2026-08-11・草川承認）────────────────────────────
# このゲートは「市民が読む文章」を止めるためのもの。ところが本文を書く操作
# すべてにかかっていたため、内部の運用ログまで止めていた。
#
#   夜間triageが📥未分類インテークへ退避しようとして deny され、退避先に
#   書けないまま消し込まれ、育休退園の市民相談が宙に浮いた（相談者は8/7から
#   返信待ち）。同じ理由で🔖台帳とSNS便ステータスが5晩連続で書けず、
#   キューに10件溜まっていた。安全網を書く行為が安全ゲートに阻まれていた。
#
# 除外するのは「対外公開されない」「草川本人しか見ない」置き場だけ。
# ブログ・SNS原稿・レポート・市民意見の本文は一切変わらず従来どおり止まる。
# 追加するときは、そのページが公開経路を持たないことを必ず確認すること。
EXEMPT_PAGES = {
    "391cf503a68f8191b218e80fdc7aedeb",  # 📥未分類インテーク（smart-intakeの締めループ）
    "39dcf503a68f811bbdd3cce4e418187a",  # 📮SNS便ステータス（朝夕便の納品記録）
}

# nichijo日次ログ／デイリーサマリはページIDが毎日変わるので、ID では押さえられない。
# 代わりに「本文が🔖台帳行だけで構成されている」という形で判定する。
#
# ⚠️ 「🔖 が含まれる行」で判定してはいけない。各行の頭に🔖を付ければ
#    ブログ本文がそのまま通ってしまう（2026-08-11のテストで実際に抜けた）。
#    時刻・矢印・行長まで含めた台帳の「形」で判定する。
LEDGER_LINE = re.compile(r"^[-\s#>*・]*🔖\s*\d{1,2}:\d{2}\s+(?P<sum>[^→]{1,30})→\s*(?P<dest>.+)$")
LEDGER_HEAD = re.compile(r"^[-\s#>*・]*🔖\s*(登録)?台帳")
LEDGER_MAX = 120   # 1行の上限。これを超える「台帳行」は散文とみなす
LEDGER_BODY_MAX = 800  # 本文全体の上限。台帳の追記は数行で済む。ブログは必ず超える

# 台帳行の「→」の右側は保存先の名前でなければならない。ここを自由文にすると、
# 散文を「🔖 06:00 〈文〉 → 日次ログ」の形に整形するだけで通ってしまう。
DESTS = ("市民意見", "政策", "質問ネタ", "投げ込み台帳", "Todoist", "日次ログ",
         "未分類", "SNS投稿管理", "市政報告会", "ミーティングノート", "Drive",
         "デイリーサマリ", "議事録", "プロジェクト")
# ─────────────────────────────────────────────────────────────────
DENY = """安全ゲート未通過のため、この本文はNotionへ書き込めません。

本文（市民が読む文章）を書き込む前に、必ず次を済ませてください。
  1. content-fact-checker を通す（数値・固有名詞・制度を一次情報まで遡る）
  2. content-risk-reviewer を通す（公選法・個人情報・名誉毀損・差別・利益相反・品位・物議）
  3. python3 ~/.claude/scripts/gate.py <対象ファイル...> で通過を記録

承認済み原稿に無い文言:\n{heads}

※本文を1文字でも変えたら指紋が変わります。「レイアウト都合で一文削る」も本文の変更です。
　risk-reviewerが必須とした文を落として指摘前より悪化させた実例があります（2026-08-06 a2）。
※プロパティだけの更新は止めません。"""


def norm(t):
    # 全角/半角ゆれ＋markdownの装飾記号を両側で同じように落とす
    t = unicodedata.normalize("NFKC", t or "")
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"[*`>#|]", "", t)
    return re.sub(r"[\s　]+", "", t)


def fp(t):
    return hashlib.sha256(norm(t).encode("utf-8")).hexdigest()[:16]


def bodies(tool_input):
    """本文を伴う部分だけ取り出す。プロパティのみなら空。"""
    out = []
    for p in tool_input.get("pages", []) or []:
        if p.get("content"):
            out.append(p["content"])
    if tool_input.get("new_str"):
        out.append(tool_input["new_str"])
    if tool_input.get("content"):
        out.append(tool_input["content"])
    for u in tool_input.get("content_updates", []) or []:
        if u.get("new_str"):
            out.append(u["new_str"])
    return [b for b in out if norm(b)]


def approved():
    """(指紋集合, 承認済み正規化テキストのリスト) を返す。"""
    try:
        d = json.load(open(GATE))
    except Exception:
        return set(), []
    ttl = d.get("ttl_minutes", 120) * 60
    try:
        born = time.mktime(time.strptime(d["generated_at"][:19], "%Y-%m-%dT%H:%M:%S"))
    except Exception:
        return set(), []
    if time.time() - born > ttl:
        return set(), []
    ap = d.get("approved", [])
    return {e.get("fp") for e in ap if e.get("fp")}, [e.get("text", "") for e in ap]


def exempt_page(tool_input):
    """更新先が内部運用ログのページなら True。create-pages は対象外（新規は必ず検査）。"""
    pid = re.sub(r"[^0-9a-f]", "", str(tool_input.get("page_id") or "").lower())
    return bool(pid) and pid in EXEMPT_PAGES


def ledger_only(b):
    """本文が🔖台帳行だけで出来ているなら True。散文が1行でも混ざれば False。"""
    lines = [l.strip() for l in (b or "").split("\n") if norm(l)]
    if not lines or len(norm(b)) > LEDGER_BODY_MAX:
        return False
    for l in lines:
        if len(norm(l)) > LEDGER_MAX:
            return False
        if LEDGER_HEAD.match(l):
            continue
        m = LEDGER_LINE.match(l)
        if not m or not any(d in m.group("dest") for d in DESTS):
            return False
    return True


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if payload.get("tool_name") not in GUARDED:
        return 0
    tool_input = payload.get("tool_input", {}) or {}
    if exempt_page(tool_input):
        return 0  # 内部運用ログのページ＝素通し
    bs = [b for b in bodies(tool_input) if not ledger_only(b)]
    if not bs:
        return 0  # プロパティのみ／🔖台帳行のみ＝素通し
    fps, texts = approved()

    def segments(b):
        """整形の骨組み（表の罫線・見出し記号・箇条書き）を除き、文単位に割る。"""
        t = re.sub(r"<[^>]+>", "", b or "")
        t = t.replace("|", "\n")                       # 表のセルを分解
        out = []
        for line in t.split("\n"):
            line = re.sub(r"^[\s>#*\-–—\d.、　]+", "", line)
            line = re.sub(r"[*`]", "", line)
            for seg in re.split(r"(?<=[。！？])", line):
                seg = norm(seg)
                if len(seg) >= 12:                     # 短い断片は骨組みとみなす
                    out.append(seg)
        return out

    def unreviewed(b):
        if fp(b) in fps:
            return []
        return [g for g in segments(b) if not any(g in t for t in texts)]

    bad = []
    for b in bs:
        bad += unreviewed(b)
    if not bad:
        return 0
    heads = "\n".join("  ・" + g[:44] + "…" for g in bad[:5])
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": DENY.format(heads=heads),
        }
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

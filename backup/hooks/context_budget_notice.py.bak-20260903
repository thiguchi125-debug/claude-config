#!/usr/bin/env python3
"""PostToolUse: 文脈サイズと巨大ツール結果を実測し、切り時を機械的に知らせる。

トークン消費はほぼ「文脈サイズ × ツール呼び出し回数」で決まる。文脈は減らない
ので、唯一効くのは「区切って /clear する」こと。

2026-09-02 改訂（実測 e02e916f: 24.5時間・227回・100.1M・文脈988Kを受けて）
  1. 300K到達後に沈黙するバグを修正。以降は100Kごとに鳴り続ける。
     旧実装では 300K→988K の区間（約50M＝当該セッションの半分）が無警告だった。
  2. 単発で巨大なツール結果（Notion MCP等）を検出。1度入ると以降の全呼び出しで
     再送され続けるため、入った瞬間に知らせる。
  3. 300K超では「区切れ」ではなく「引き継ぎメモを書いて区切れ」と指示する。
このフックは動作をブロックしない。
"""
import json, os, sys

# 120K/200K/300K のあと、上限まで100Kごとに鳴らし続ける（沈黙させない）
THRESHOLDS = [120_000, 200_000, 300_000] + list(range(400_000, 2_000_001, 100_000))
STATE_DIR = os.path.expanduser("~/.claude/hooks/state")
TAIL_BYTES = 300_000
MAX_SCAN = 6_000_000        # usage が見つかるまで末尾から遡る上限
CHECK_EVERY = 4             # 文脈の再計測はNツール呼び出しに1回（CPU節約）
BIG_RESULT_CHARS = 120_000  # 1回のツール結果がこれを超えたら警告（≒30Kトークン）


def last_context(path):
    """transcript の末尾から遡って最新の usage を探し、文脈サイズを返す。

    1行が数百KBになることがある（画像base64を含む行）ため、固定幅の tail では
    usage 行を跨いで取りこぼす。見つかるまで窓を広げて遡る。
    """
    try:
        size = os.path.getsize(path)
        f = open(path, "rb")
    except OSError:
        return None
    with f:
        window = TAIL_BYTES
        while True:
            start = max(0, size - window)
            f.seek(start)
            if start:
                f.readline()  # 途中で切れた行を捨てる
            lines = f.read().decode("utf-8", "replace").splitlines()
            for line in reversed(lines):
                try:
                    o = json.loads(line)
                except ValueError:
                    continue
                m = o.get("message")
                u = m.get("usage") if isinstance(m, dict) else None
                if not u:
                    continue
                ctx = ((u.get("input_tokens") or 0)
                       + (u.get("cache_creation_input_tokens") or 0)
                       + (u.get("cache_read_input_tokens") or 0))
                if ctx:  # 合計0の空 usage 行は本物の計測値ではないので読み飛ばす
                    return ctx
            if start == 0 or window >= MAX_SCAN:
                return None
            window *= 4


def load_state(sf):
    """{"level": 通知済み閾値, "n": 前回計測からの呼び出し数} を返す。

    旧形式（閾値の整数だけを書いたファイル）も読めるようにしておく。
    """
    try:
        raw = open(sf).read().strip()
    except OSError:
        return {"level": 0, "n": 0}
    try:
        d = json.loads(raw)
    except ValueError:
        d = None
    # 旧形式は閾値の整数だけ（json.loads は int を返すので dict 判定が要る）
    if isinstance(d, dict):
        try:
            return {"level": int(d.get("level", 0)), "n": int(d.get("n", 0))}
        except (TypeError, ValueError):
            return {"level": 0, "n": 0}
    try:
        return {"level": int(raw), "n": 0}
    except ValueError:
        return {"level": 0, "n": 0}


def save_state(sf, level, n):
    os.makedirs(STATE_DIR, exist_ok=True)
    try:
        with open(sf, "w") as f:
            json.dump({"level": level, "n": n}, f)
    except OSError:
        pass


def big_result_msg(inp):
    """1回で文脈に居座る巨大な結果を検出する。"""
    resp = inp.get("tool_response")
    if resp is None:
        return None
    try:
        size = len(resp if isinstance(resp, str)
                   else json.dumps(resp, ensure_ascii=False))
    except (TypeError, ValueError):
        return None
    if size < BIG_RESULT_CHARS:
        return None
    tok = size // 4  # 日本語混在でおおよそ4文字/トークン
    tool = inp.get("tool_name") or "このツール"
    return (f"\U0001f4e6 {tool} の結果が約 {tok//1000}K トークン。"
            "これは以降の全呼び出しで再送され続ける。\n"
            f"   残り100回の呼び出しなら、この1件だけで +{tok*100//1000//1000}M。\n"
            "   同種の大量取得を続けるなら、本体でなくサブエージェント側で受けて"
            "要約だけ返させる。")


def context_msg(ctx, level):
    k = ctx // 1000
    ahead = k * 100 // 1000  # この先100回分のM
    if level >= 300_000:
        return (f"⛔ 文脈 {k}K トークン。"
                f"1ツール呼び出しごとに {k}K を再送している。\n"
                f"   この先100回で +{ahead}M。ここからは"
                "何をしても・何もしなくても同じ値段。\n"
                "   今すぐやること：「区切り」"
                "（/kugiri）を実行して引き継ぎメモを作り、"
                "その場で /clear する。")
    if level >= 200_000:
        return (f"\U0001f534 文脈 {k}K トークン。"
                f"呼び出し1回あたり {k}K を払っている。\n"
                f"   この先100回で +{ahead}M。\n"
                "   区切るなら今：「区切り」（/kugiri）"
                "→ 成果物保存と引き継ぎメモまで自動。")
    return (f"\U0001f7e1 文脈 {k}K トークン。"
            "以降このセッションのコストは"
            "呼び出し回数に比例して増える。\n"
            "   別件を始めるなら新セッションへ。"
            "画像を伴う作業・広い探索は"
            "サブエージェントへ隔離する。")


def main():
    try:
        inp = json.load(sys.stdin)
    except ValueError:
        return

    msgs = []
    big = big_result_msg(inp)
    if big:
        msgs.append(big)

    sid = inp.get("session_id") or "unknown"
    tpath = inp.get("transcript_path")
    if tpath:
        sf = os.path.join(STATE_DIR, f"{sid}.ctx")
        st = load_state(sf)
        n = st["n"] + 1
        # 巨大結果が入った直後は必ず測る（そこが跳ねるポイントなので）
        if n >= CHECK_EVERY or st["level"] == 0 or big:
            ctx = last_context(tpath)
            if ctx:
                crossed = [t for t in THRESHOLDS if ctx >= t]
                level = max(crossed) if crossed else 0
                if level > st["level"]:
                    save_state(sf, level, 0)
                    msgs.append(context_msg(ctx, level))
                else:
                    save_state(sf, st["level"], 0)
            else:
                save_state(sf, st["level"], 0)
        else:
            save_state(sf, st["level"], n)

    if not msgs:
        return
    json.dump({"hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": "[トークン監視] " + "\n".join(msgs),
    }}, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()

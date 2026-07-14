#!/usr/bin/env python3
"""Discord REST薄ラッパー（SNSルーティンv2 Phase1）
Token: ~/.claude/channels/discord/.env の DISCORD_BOT_TOKEN
State: ./_state.json（env SNS_ROUTINE_STATE で上書き可）
Usage:
  discord_api.py fetch                    新着（草川本人のみ・昇順）JSON出力。カーソルは進めない
  discord_api.py react <msg_id> <ok|warn|eye>
  discord_api.py post "<text>"
  discord_api.py advance <msg_id>         全件処理成功後にのみ呼ぶ（単調増加）
"""
import json, os, sys, urllib.parse, urllib.request

BASE = "https://discord.com/api/v10"
DIR = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.environ.get("SNS_ROUTINE_STATE") or os.path.join(DIR, "_state.json")
ENV_PATH = os.path.expanduser("~/.claude/channels/discord/.env")
USER_ID = "1122069094166958121"  # 草川のDiscordユーザーID（access.json allowFrom と一致）
EMOJI = {"ok": "✅", "warn": "⚠️", "eye": "👀"}


def _token():
    for line in open(ENV_PATH):
        if line.startswith("DISCORD_BOT_TOKEN="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("DISCORD_BOT_TOKEN not found in " + ENV_PATH)


def _call(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method)
    req.add_header("Authorization", "Bot " + _token())
    req.add_header("User-Agent", "kusagawa-sns-routine/1.0")
    data = None
    if body is not None:
        req.add_header("Content-Type", "application/json")
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    with urllib.request.urlopen(req, data, timeout=30) as r:
        raw = r.read()
        return json.loads(raw) if raw else None


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH) as f:
            return json.load(f)
    return {}


def save_state(st):
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(st, f, ensure_ascii=False, indent=1)
    os.replace(tmp, STATE_PATH)


def dm_channel_id():
    st = load_state()
    if "dm_channel_id" not in st:
        ch = _call("POST", "/users/@me/channels", {"recipient_id": USER_ID})
        st["dm_channel_id"] = ch["id"]
        save_state(st)
    return st["dm_channel_id"]


def filter_new(messages, last_id, user_id=USER_ID):
    """草川本人のメッセージのみ・カーソルより新しいもの・ID昇順（bot自身の発言は除外）"""
    out = [m for m in messages if m.get("author", {}).get("id") == user_id]
    if last_id:
        out = [m for m in out if int(m["id"]) > int(last_id)]
    return sorted(out, key=lambda m: int(m["id"]))


def fetch():
    st = load_state()
    ch = dm_channel_id()
    q = "?limit=100"
    if st.get("last_processed_id"):
        q += "&after=" + st["last_processed_id"]
    msgs = _call("GET", "/channels/%s/messages%s" % (ch, q)) or []
    new = filter_new(msgs, st.get("last_processed_id"))
    print(json.dumps(
        [{"id": m["id"], "ts": m["timestamp"], "content": m["content"]} for m in new],
        ensure_ascii=False, indent=1))


def react(msg_id, kind):
    ch = dm_channel_id()
    emoji = urllib.parse.quote(EMOJI[kind])
    _call("PUT", "/channels/%s/messages/%s/reactions/%s/@me" % (ch, msg_id, emoji))


def post(text):
    ch = dm_channel_id()
    _call("POST", "/channels/%s/messages" % ch, {"content": text[:1900]})


def advance(msg_id):
    st = load_state()
    cur = st.get("last_processed_id")
    if cur is None or int(msg_id) > int(cur):
        st["last_processed_id"] = str(msg_id)
        save_state(st)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "fetch":
        fetch()
    elif cmd == "react":
        react(sys.argv[2], sys.argv[3])
    elif cmd == "post":
        post(sys.argv[2])
    elif cmd == "advance":
        advance(sys.argv[2])
    else:
        sys.exit(__doc__)

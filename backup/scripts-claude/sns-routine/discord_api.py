#!/usr/bin/env python3
"""Discord REST薄ラッパー（SNSルーティンv2 Phase1+3・ローカル便Phase3拡張）
Token: ~/.claude/channels/discord/.env の DISCORD_BOT_TOKEN
State: ./_state.json（env SNS_ROUTINE_STATE で上書き可）
Usage:
  discord_api.py fetch                    新着（草川本人のみ・昇順）JSON出力。カーソルは進めない
  discord_api.py read <after_msg_id>      after_msg_id以降の全メッセージ（bot含む・is_userフラグで区別）を
                                           昇順JSON出力。読み取り専用・カーソル/リアクションには一切触れない
  discord_api.py react <msg_id> <ok|warn|eye>
  discord_api.py post "<text>"            送信成功時、作成メッセージidをstdoutに1行出力する
  discord_api.py advance <msg_id>         全件処理成功後にのみ呼ぶ（単調増加）
  discord_api.py audit [days]             直近days日分（既定7）の生メッセージをbefore/afterページングで全件取得し、
                                           草川本人メッセージのうちreactionsが1つも付いていないものをJSON出力（日曜監査用）。
                                           AUDIT_FLOOR より古いメッセージ（カーソル初期化前の意図的スキップ分）は対象外。
  discord_api.py download <msg_id> <dir>  msg_idの添付ファイル（写真等）を<dir>へ保存し、保存パスのJSONリストを出力。
                                           読み取り専用（カーソル・リアクション不変更）。v3納品便のInsta写真取得用。
"""
import json, os, socket, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime

BASE = "https://discord.com/api/v10"
DIR = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.environ.get("SNS_ROUTINE_STATE") or os.path.join(DIR, "_state.json")
ENV_PATH = os.path.expanduser("~/.claude/channels/discord/.env")
USER_ID = "1122069094166958121"  # 草川のDiscordユーザーID（access.json allowFrom と一致）
EMOJI = {"ok": "✅", "warn": "⚠️", "eye": "👀"}

DISCORD_EPOCH_MS = 1420070400000  # 2015-01-01T00:00:00.000Z
# 2026-07-14以前は運用開始前のカーソル初期化で意図的にスキップした履歴のため監査対象外
AUDIT_FLOOR_ISO = "2026-07-14T00:00:00+09:00"


def _token():
    for line in open(ENV_PATH):
        if line.startswith("DISCORD_BOT_TOKEN="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("DISCORD_BOT_TOKEN not found in " + ENV_PATH)


# 一時的な障害（起床直後のDNS未起動・回線瞬断・Discord側5xx/429）のリトライ設定。
# 3:10のlaunchd起動はMacが寝ている/起きた直後に当たることがあり、
# getaddrinfo が即failして夜間ジョブが丸ごと落ちる事故が実際に発生した（2026-07-17 03:11）。
_RETRY_MAX = 5              # 初回＋4回の再試行
_RETRY_BACKOFF = [5, 15, 45, 90]  # 秒。合計 約2.5分まで粘る
_SLEEP = time.sleep         # テストから差し替え可能


def _is_transient(err):
    """再試行する価値のある一時障害か（恒久的なトークン誤り等は即座に諦める）"""
    if isinstance(err, urllib.error.HTTPError):
        # 429=レート制限, 5xx=Discord側の一時障害。401/403/404は再試行しても無駄
        return err.code == 429 or 500 <= err.code < 600
    if isinstance(err, urllib.error.URLError):
        return True         # DNS未解決・接続不可・タイムアウト等
    return isinstance(err, (socket.timeout, socket.gaierror, ConnectionError))


def _call(method, path, body=None):
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")

    last_err = None
    for attempt in range(_RETRY_MAX):
        req = urllib.request.Request(BASE + path, method=method)
        req.add_header("Authorization", "Bot " + _token())
        req.add_header("User-Agent", "kusagawa-sns-routine/1.0")
        if body is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, data, timeout=30) as r:
                raw = r.read()
                return json.loads(raw) if raw else None
        except Exception as err:
            if not _is_transient(err) or attempt == _RETRY_MAX - 1:
                raise
            last_err = err
            wait = _RETRY_BACKOFF[min(attempt, len(_RETRY_BACKOFF) - 1)]
            sys.stderr.write(
                "[discord_api] 一時障害のため再試行 %d/%d (%ds待機): %s\n"
                % (attempt + 1, _RETRY_MAX - 1, wait, err))
            _SLEEP(wait)
    raise last_err


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


def snowflake_from_ms(unix_ms):
    """unix epoch ms -> Discord snowflake ID（idの大小比較・afterクエリに使用）"""
    return str((int(unix_ms) - DISCORD_EPOCH_MS) << 22)


def audit_floor_snowflake():
    dt = datetime.fromisoformat(AUDIT_FLOOR_ISO)
    return snowflake_from_ms(int(dt.timestamp() * 1000))


def find_unprocessed(messages, user_id=USER_ID, floor_id=None):
    """草川本人のメッセージのうちreactionsが1つも付いていないものを抽出（bot除外・floor_id以前は除外・id昇順）
    純粋関数（HTTP非依存）。sunday_audit.shの判定ロジック本体。"""
    out = []
    for m in messages:
        if m.get("author", {}).get("id") != user_id:
            continue
        if floor_id is not None and int(m["id"]) <= int(floor_id):
            continue
        if m.get("reactions"):
            continue
        out.append(m)
    return sorted(out, key=lambda m: int(m["id"]))


def _atts(m):
    """メッセージの添付情報を軽量JSON化（写真投げ込みの検出用）"""
    return [{"filename": a.get("filename", ""),
             "content_type": a.get("content_type", ""),
             "url": a.get("url", "")} for a in m.get("attachments", [])]


def fetch():
    st = load_state()
    ch = dm_channel_id()
    q = "?limit=100"
    if st.get("last_processed_id"):
        q += "&after=" + st["last_processed_id"]
    msgs = _call("GET", "/channels/%s/messages%s" % (ch, q)) or []
    new = filter_new(msgs, st.get("last_processed_id"))
    print(json.dumps(
        [{"id": m["id"], "ts": m["timestamp"], "content": m["content"],
          "attachments": _atts(m)} for m in new],
        ensure_ascii=False, indent=1))


def read(after_id):
    """after_id以降の全メッセージ（bot含む）を昇順JSON出力。読み取り専用（カーソル・リアクション不変更）。
    is_user=True のものが草川本人の発言（authorがbot自身のものはis_user=False）。"""
    ch = dm_channel_id()
    q = "?limit=50"
    if after_id:
        q += "&after=" + str(after_id)
    msgs = _call("GET", "/channels/%s/messages%s" % (ch, q)) or []
    out = [{
        "id": m["id"],
        "ts": m["timestamp"],
        "content": m["content"],
        "is_user": m.get("author", {}).get("id") == USER_ID,
        "attachments": _atts(m),
    } for m in msgs]
    out.sort(key=lambda m: int(m["id"]))
    print(json.dumps(out, ensure_ascii=False, indent=1))


def download(msg_id, outdir):
    """msg_idの添付ファイルをoutdirへ保存し、保存パスのJSONリストを出力（読み取り専用）。
    Discord CDNの添付URLは署名付きで期限があるため、当日中の利用を前提とする。"""
    ch = dm_channel_id()
    m = _call("GET", "/channels/%s/messages/%s" % (ch, msg_id))
    os.makedirs(outdir, exist_ok=True)
    saved = []
    for i, a in enumerate(m.get("attachments", [])):
        name = a.get("filename") or ("attachment_%d" % i)
        # パス直下固定（filenameのディレクトリ表記は無害化）
        name = os.path.basename(name)
        dest = os.path.join(outdir, "%s_%s" % (msg_id, name))
        req = urllib.request.Request(a["url"], headers={"User-Agent": "kusagawa-sns-routine/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
            f.write(r.read())
        saved.append(dest)
    print(json.dumps(saved, ensure_ascii=False, indent=1))


def react(msg_id, kind):
    ch = dm_channel_id()
    emoji = urllib.parse.quote(EMOJI[kind])
    _call("PUT", "/channels/%s/messages/%s/reactions/%s/@me" % (ch, msg_id, emoji))


def post(text):
    ch = dm_channel_id()
    resp = _call("POST", "/channels/%s/messages" % ch, {"content": text[:1900]})
    if resp and resp.get("id"):
        print(resp["id"])
    return resp


def audit(days=7):
    """直近days日分の生メッセージ（reactions含む）をbeforeページングで全件取得し、
    草川本人の未リアクションメッセージ（AUDIT_FLOOR以降のみ）をJSON出力。カーソルは一切操作しない（読むだけ）。"""
    ch = dm_channel_id()
    days_floor = snowflake_from_ms(int(time.time() * 1000) - int(days) * 86400 * 1000)
    fixed_floor = audit_floor_snowflake()
    floor_id = str(max(int(days_floor), int(fixed_floor)))

    messages = []
    before = None
    while True:
        q = "?limit=100"
        if before:
            q += "&before=" + before
        batch = _call("GET", "/channels/%s/messages%s" % (ch, q)) or []
        if not batch:
            break
        messages.extend(batch)
        oldest_id = min(int(m["id"]) for m in batch)
        before = str(oldest_id)
        if oldest_id <= int(floor_id) or len(batch) < 100:
            break

    unprocessed = find_unprocessed(messages, USER_ID, floor_id)
    print(json.dumps(
        [{"id": m["id"], "ts": m["timestamp"], "content": m["content"]} for m in unprocessed],
        ensure_ascii=False, indent=1))


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
    elif cmd == "read":
        read(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "react":
        react(sys.argv[2], sys.argv[3])
    elif cmd == "post":
        post(sys.argv[2])
    elif cmd == "advance":
        advance(sys.argv[2])
    elif cmd == "audit":
        audit(int(sys.argv[2]) if len(sys.argv) > 2 else 7)
    elif cmd == "download":
        download(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)

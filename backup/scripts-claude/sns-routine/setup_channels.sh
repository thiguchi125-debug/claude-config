#!/bin/bash
# 用途別チャンネルの仕上げ（2026-08-11）
#
# 草川が Discord サーバー kusakawatakuya に #投げ込み / #納品 / #ログ を作った後、
# これを1回叩けば設定から疎通確認まで終わる。
#
#   bash ~/.claude/scripts/sns-routine/setup_channels.sh
#
# Botに MANAGE_CHANNELS を与えた場合は --create を付けるとチャンネル作成からやる。
#   bash ~/.claude/scripts/sns-routine/setup_channels.sh --create
set -u
cd "$(dirname "$0")"
API="python3 discord_api.py"

if [ "${1:-}" = "--create" ]; then
  echo "▶ チャンネルを作成します"
  python3 - <<'PY'
import discord_api as D, urllib.error
gs = D._call("GET", "/users/@me/guilds") or []
if not gs:
    raise SystemExit("❌ Botがどのサーバーにも入っていません")
gid = gs[0]["id"]
existing = {c["name"]: c["id"] for c in (D._call("GET", "/guilds/%s/channels" % gid) or [])}
for name in ("投げ込み", "納品", "ログ"):
    if name in existing:
        print("  ・既にあります:", name, existing[name]); continue
    try:
        c = D._call("POST", "/guilds/%s/channels" % gid, {"name": name, "type": 0})
        print("  ✅ 作成:", c["name"], c["id"])
    except urllib.error.HTTPError as e:
        print("  ❌", name, "→ HTTP", e.code, e.read().decode()[:160])
        if e.code == 403:
            print("     BotにMANAGE_CHANNELS権限がありません。手でチャンネルを作ってから --create なしで再実行してください。")
        raise SystemExit(1)
PY
  [ $? -ne 0 ] && exit 1
fi

echo "▶ チャンネルを検出して設定します"
$API discover --apply || exit 1

echo
echo "▶ 設定結果"
$API channels

echo
echo "▶ 疎通確認（各チャンネルへ1通ずつ）"
python3 - <<'PY'
import discord_api as D
conf = D.channels()
missing = [k for k, v in conf.items() if not v]
if missing:
    print("  ⚠️ 未設定のまま（DMに落ちます）:", "／".join(missing))
    print("     チャンネル名に「投げ込み」「納品」「ログ」の語が入っているか確認してください。")
msgs = {
  "inbox":    "✅ #投げ込み 開通。ここは草川→システム専用です。市民相談の転送・メモ・写真はここへ。受領レシートと『返事が要る問いかけ』だけを、投げた元メッセージへの返信で返します。",
  "delivery": "✅ #納品 開通。朝夕便のコピペ用原稿（X／Threads／Facebook）はここに届きます。「Bで」「パス」「〇〇直して」の返信もここで受け付けます。",
  "log":      "✅ #ログ 開通。安全ゲート記録・稼働状況・エラーはここへ。読み流して構いません（異常は毎朝のohayoが🚨で出します）。",
}
for kind, text in msgs.items():
    if not conf.get(kind):
        print("  ⊘", kind, "未設定のため送信スキップ"); continue
    D.post(text, kind=kind)
    print("  ✅", kind, "→", conf[kind])
PY

echo
echo "▶ 読み取り対象（#ログは書き専用なので入りません）"
$API channels | python3 -c "import json,sys; print('  ', json.load(sys.stdin)['reading'])"
echo
echo "完了。DM運用へ戻すときは:"
echo "  python3 ~/.claude/scripts/sns-routine/discord_api.py channels --inbox - --delivery - --log -"

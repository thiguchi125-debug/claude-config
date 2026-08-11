#!/usr/bin/env python3
"""
content_safety_gate.py の回帰テスト。

2026-08-11に内部運用ログの除外（EXEMPT_PAGES ／ 🔖台帳行）を入れた。
ゲートを緩めた以上、**本来止まるべきものが今も止まること**を機械で担保する。
このファイルを実行して1件でも ❌ が出たら、除外条件を触った変更を疑う。

  python3 ~/.claude/hooks/tests/test_content_safety_gate.py
"""
import json
import os
import subprocess
import sys

HOOK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "content_safety_gate.py")

UP = "mcp__claude_ai_Notion__notion-update-page"
CR = "mcp__claude_ai_Notion__notion-create-pages"

UNCLASSIFIED = "391cf503-a68f-8191-b218-e80fdc7aedeb"   # 📥未分類インテーク
SNS_STATUS = "39dcf503-a68f-811b-bdd3-cce4e418187a"     # 📮SNS便ステータス
NICHIJO = "3b8cf503-a68f-810c-a53f-e4b19b9165e1"        # 日次ログ（IDは日々変わる）
NORMAL = "3b3cf503a68f811eb795d4f029f8f73e"             # 通常のブログページ

BLOG = ("こんにちは、亀山市議会議員の草川たくやです。避難所になる体育館に冷房がありません。"
        "亀山市の整備率は0%で、2年が過ぎました。国の交付金を使えば6,000万から9,000万円の"
        "工事が補助対象になります。9月議会でこの問題を取り上げたいと考えています。")
SNS = "体育館に冷房がない。亀山市は0%です。9月議会で取り上げたい。"

CASES = [
    # ── 止まらなければならないもの ────────────────────────────
    ("DENY", "未検査のブログ本文", UP, {"page_id": NORMAL, "new_str": BLOG}),
    ("DENY", "未検査の本文で新規ページ", CR, {"pages": [{"content": BLOG}]}),
    ("DENY", "短いSNS原稿", UP, {"page_id": NORMAL, "content": SNS}),
    ("DENY", "content_updates経由の本文", UP,
     {"page_id": NORMAL, "content_updates": [{"old_str": "x", "new_str": BLOG}]}),
    ("DENY", "🔖を1行足してブログを密輸", UP,
     {"page_id": NICHIJO, "content": "🔖 06:20 メモ → 日次ログ\n" + BLOG}),
    ("DENY", "各行に🔖を付けて密輸", UP,
     {"page_id": NICHIJO, "content": "\n".join("🔖 " + l for l in BLOG.split("。") if l)}),
    ("DENY", "各行に🔖＋時刻＋矢印を付けて密輸", UP,
     {"page_id": NICHIJO,
      "content": "\n".join(f"🔖 06:{i:02d} {l} → 日次ログ"
                           for i, l in enumerate(BLOG.split("。")) if l)}),
    ("DENY", "除外ページIDを新規作成の親に指定", CR,
     {"pages": [{"parent": {"page_id": UNCLASSIFIED}, "content": BLOG}]}),

    # ── 通らなければならないもの（すべて実データ由来）──────────
    ("ALLOW", "プロパティのみ更新", UP, {"page_id": NORMAL, "properties": {"件名": "x"}}),
    ("ALLOW", "📥未分類インテークへの退避行", UP,
     {"page_id": UNCLASSIFIED,
      "content": "- [ ] 2026-08-11: 育休退園の件 タスク化候補①②が2晩連続無応答のため退避"}),
    ("ALLOW", "📮SNS便ステータスの納品記録", UP,
     {"page_id": SNS_STATUS,
      "new_str": "- 便名: 朝便（2026-08-11・納品7:04）\n- 送信msg_id: 1536496152034156564"}),
    ("ALLOW", "🔖台帳（8/10実データ・見出し＋2行）", UP,
     {"page_id": NICHIJO,
      "content": "### 🔖 登録台帳（Discord投げ込み夜間振り分け・2026-08-11実行分）\n"
                 "- 🔖 12:14 納涼大会の火の安全 → 📝市民意見リスト＋Todoist提案中\n"
                 "- 🔖 13:08 イベント一覧サイト要望 → 📝市民意見リスト"}),
    ("ALLOW", "🔖台帳（8/1実データ）", UP,
     {"page_id": NICHIJO,
      "content": "🔖 11:30 みずき信号・ビック裏道の連絡先 → Todoist提案＋日次ログ（連絡先は伏せ字でNotion登録）"}),
    ("ALLOW", "🔖台帳（8/6実データ）", UP,
     {"page_id": NICHIJO, "content": "🔖 06:20 道野の水路＝9月議会の質問ネタ → 🎯政策・質問ネタDB（統一）"}),
    ("ALLOW", "🔖台帳（8/7実データ）", UP,
     {"page_id": NICHIJO, "content": "🔖 22:18 育休退園ルール緩和の遡及適用 → 📝市民意見リスト＋🎯政策・質問ネタDB"}),

    # ── 既知の残存リスク（意図的に ALLOW のまま）────────────────
    # 散文を「。」で割り、各断片を28字に切り詰め、時刻と「→ 日次ログ」を付ければ通る。
    # 通すと決めた理由: このゲートが守っているのは「本文が変わったのに本文の変更だと
    # 認識しなかった」という取り違え事故（ヘッダ参照）であって、悪意ある持ち出しではない。
    # 取り違えは絶対にこの形（時刻＋矢印＋保存先語彙＋28字切り詰め）にならないし、
    # 切り詰めた結果は文として壊れているので発信物として機能しない。
    # ここを塞ぐには台帳をNotion本文でなくプロパティかローカルファイルに移すのが筋。
    ("ALLOW", "【既知の穴】28字に切って台帳形式に整形", UP,
     {"page_id": NICHIJO,
      "content": "\n".join(f"🔖 06:{i:02d} {l[:28]} → 日次ログ"
                           for i, l in enumerate(BLOG.split("。")) if l)}),
]


def run(tool, tool_input):
    p = subprocess.run([sys.executable, HOOK],
                       input=json.dumps({"tool_name": tool, "tool_input": tool_input}),
                       capture_output=True, text=True)
    if p.stderr.strip():
        return "ERROR: " + p.stderr.strip()[-200:]
    out = p.stdout.strip()
    if not out:
        return "ALLOW"
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"].upper()


def main():
    ng = 0
    for expected, desc, tool, tool_input in CASES:
        got = run(tool, tool_input)
        ok = got == expected
        ng += not ok
        print(f"{'✅' if ok else '❌'} {desc}: 期待={expected} 実際={got}")
    print()
    if ng:
        print(f"⚠️ {ng}件が期待と違う。除外条件（EXEMPT_PAGES / LEDGER_LINE / DESTS）の変更を疑う。")
        return 1
    print(f"全{len(CASES)}件 期待どおり")
    return 0


if __name__ == "__main__":
    sys.exit(main())

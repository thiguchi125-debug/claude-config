#!/usr/bin/env python3
"""tasks.json の各タスクに SKILL.md の想定所要テーブルを当ててコマ数を付ける。

判定語は SKILL.md「Step 2: 想定所要の見積り」の表をそのまま写したもの。
上から順に最初に当たったものを採用する（重い種別を先に置く）。
"""
import json
import re
import sys

# (必要コマ, ラベル, 判定語の正規表現) — 重い順に並べる
TABLE = [
    (16, "印刷物制作・入稿 8h", r"チラシ|ポスター|リーフレット|入稿|パンフ"),
    (8, "スライド・報告会資料 4h", r"スライド|資料作成|報告会|レポート作成"),
    (8, "一般質問・議案質疑原稿 4h", r"一般質問|質疑|通告"),
    (6, "議案分析・調査 3h", r"分析|調査|リサーチ|検討|企画|作成|設計|まとめ"),
    (2, "訪問・現地確認 1h", r"訪問|現地|視察|下見"),
    (2, "ブログ・SNS 1h", r"ブログ|投稿|発信|SNS|動画"),
    (2, "資料読み込み 1h", r"読む|目を通す|資料確認|チェック"),
    (1, "挨拶原稿 30分", r"挨拶|祝辞|スピーチ"),
    (1, "メール・DM返信 30分", r"返信|メール|返事|送る|送付|提出"),
    (1, "連絡・電話・アポ 15分", r"電話|連絡|アポ|確認|依頼|お礼|申込|予約|手配"),
]
DEFAULT = (2, "表に該当なし→1h と推定")


def estimate(content):
    for slots, label, pattern in TABLE:
        if re.search(pattern, content):
            return slots, label
    return DEFAULT


def main():
    tasks = json.load(open(sys.argv[1], encoding="utf-8"))
    for t in tasks:
        t["slots"], t["basis"] = estimate(t["content"])
    json.dump(tasks, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)

    withdue = [t for t in tasks if t["due"]]
    print("期限あり {}件 / 合計 {}コマ = {}時間".format(
        len(withdue), sum(t["slots"] for t in withdue),
        sum(t["slots"] for t in withdue) / 2))
    for slots in sorted({t["slots"] for t in withdue}, reverse=True):
        group = [t for t in withdue if t["slots"] == slots]
        print("  {}コマ({}分) × {}件".format(slots, slots * 30, len(group)))


if __name__ == "__main__":
    main()

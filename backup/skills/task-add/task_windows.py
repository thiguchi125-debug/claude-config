#!/usr/bin/env python3
"""タスクを「いつなら実際にやれるか」で分類する（現実性フィルタ）。

2026-08-06 の一括実行で、空き時間があるという理由だけで
  ・日曜に市役所への照会を8件
  ・18時以降に役所への照会を7件
  ・「連絡待ち」「協議待ち」＝相手の手番のタスクに作業ブロックを2件
置いてしまった。カレンダー上は埋まっているが、現実には1件も実行できない。

空き時間の有無より先に「相手がいる時間か」「自分の手番か」を見る。
"""
import re

# 曜日集合
WEEKDAY = {0, 1, 2, 3, 4}
ALLDAYS = {0, 1, 2, 3, 4, 5, 6}


class Kind:
    def __init__(self, key, label, days, start, end, why, early=False):
        self.key, self.label = key, label
        self.days, self.start, self.end = days, start * 60, end * 60
        self.why = why
        # 早朝5:00-7:00を使えるか。相手のいない机上作業だけ True（2026-08-07 指示）
        self.early = early

    def windows_for(self, d):
        """その日付で使える時間帯。使えない日は空リスト。"""
        if d.weekday() not in self.days:
            return []
        w = [(self.start, self.end)]
        if self.early:
            w.insert(0, (5 * 60, 7 * 60))
        return w

    def band(self):
        """コマ数を数えるときの稼働帯。早朝が使えるなら5:00から。"""
        return (5 * 60, 21 * 60) if self.early else (9 * 60, 21 * 60)


# 相手の都合で時間帯が決まるものから順に判定する（上が優先）
OFFICE = Kind("office", "役所・関係機関", WEEKDAY, 9, 17,
              "市役所・県・警察・学校は平日日中しか窓口が開いていない")
FIELD = Kind("field", "現地確認", ALLDAYS, 9, 18,
             "明るいうちでないと現地の状況が見えない")
CONTACT = Kind("contact", "住民・関係者への連絡", ALLDAYS, 9, 20,
               "個人宅への電話は夜遅くにかけられない")
DESK = Kind("desk", "机上作業", ALLDAYS, 9, 21,
            "原稿・資料作成は相手がいないので時間帯を選ばない。早朝5:00-7:00も使える",
            early=True)

# 自分の手番でない＝作業ブロックを作らない
WAIT_LABELS = {"結果待ち", "保留"}
WAIT_TEXT = re.compile(r"待ち|待つ|返事待|回答待|連絡待|協議待")

_OFFICE = re.compile(
    r"照会|担当課|課へ|課に|部へ|部に|委員会|教委|市へ|市に確認|県|警察|公安|消防|"
    r"建設部|環境課|学校教育課|教育総務課|上下水道|防災安全課|健康福祉|地域福祉|"
    r"アポ|ヒアリング|要望書|請願|申請|届出")
_FIELD = re.compile(r"現地|下見|視察|見に行|写真記録|点検|草刈|測量|立会")
# 「報告」は市政報告レポート等の制作物にも含まれるので、宛先が読める形だけ拾う
_CONTACT = re.compile(
    r"連絡|電話|返信|返事|回答|お礼|依頼|案内|経過報告|報告する|へ報告|に報告|"
    r"相談者へ|さんへ|さんに|自治会長|会長へ|住民|訪問|届ける")


def classify(content, labels=()):
    """(Kind, skip_reason) を返す。skip_reason があればブロックを作らない。"""
    if set(labels) & WAIT_LABELS:
        return None, "@{} ラベル＝相手の手番".format(
            "／@".join(sorted(set(labels) & WAIT_LABELS)))
    if WAIT_TEXT.search(content):
        return None, "件名が「待ち」＝相手の手番"
    for kind, pattern in ((OFFICE, _OFFICE), (FIELD, _FIELD), (CONTACT, _CONTACT)):
        if pattern.search(content):
            return kind, None
    return DESK, None


def window_fn(kind):
    """plan_blocks に渡す「その日に置ける時間帯」を返す関数。"""
    return lambda d: kind.windows_for(d)

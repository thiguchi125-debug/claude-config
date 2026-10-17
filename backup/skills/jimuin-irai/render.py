#!/usr/bin/env python3
"""事務員（櫻井さん）向け お願いページの生成＋公選法チェック。

使い方:
  python3 render.py            # days/*.json を全部読み、最新日を先頭にHTMLを出力
  python3 render.py --check    # 公選法チェックだけ（HTMLは書かない）

チェックでERRORが1件でもあれば exit 1 でHTMLを書かない。
共通ルール（投稿の進め方・選挙のきまり）はこのファイルの定数で、JSONから消せない。
"""
import datetime as dt
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

DATA_DIR = Path.home() / "outputs/sakurai_irai/days"
OUT = Path.home() / "outputs/sakurai_irai/index.html"

KOJI = dt.date(2026, 10, 18)    # 告示日
TOHYO = dt.date(2026, 10, 25)   # 投票日
WEEK = "月火水木金土日"

# ---- 公選法チェック（日ごとの JSON の文字だけに掛ける。共通ルール文には掛けない） ----
# (正規表現, 理由)。事務員が「選挙運動そのもの」をする書き方を止める。
SHOOT = r"(?!.{0,8}(撮影|収録|撮る|撮って))"  # 「〜を撮影」は止めない
NG = [
    (r"(演説|あいさつ|挨拶)(する|して|を行|をし)" + SHOOT, "事務員は演説・あいさつをしない"),
    (r"(呼びかけ|呼び掛け|声かけ|声掛け)(る|を|して)" + SHOOT, "事務員は有権者への呼びかけをしない"),
    (r"マイク.{0,4}(を持|で).{0,6}(話|呼|訴)", "マイクを持つのは車上運動員・候補者だけ"),
    (r"(チラシ|ビラ|リーフ|ハガキ|はがき|名刺).{0,8}(配|まく|手渡|渡し|ポスティング)", "文書の配布は事務員の作業にしない"),
    (r"投票.{0,6}(お願い|依頼|頼)", "投票依頼は選挙運動"),
    (r"(支持|応援).{0,6}(お願い|依頼|頼)", "支持依頼は選挙運動"),
    (r"電話(で|を|かけ)", "電話作戦は事務員にさせない"),
    (r"(握手|手を?振|手振り)", "握手・手振りは選挙運動"),
    (r"(タスキ|たすき|襷|のぼり|ゼッケン|腕章)", "選挙用の着用物は事務員に付けさせない"),
    (r"(看板|ポスター|スピーカー|拡声).{0,10}(車|付け|設置)", "選挙運動に使える車は遊説車1台だけ"),
    (r"(広告|プロモーション|宣伝費|ブースト)", "候補者のネット有料広告は禁止"),
    (r"投稿文.{0,4}(作成|作っ|作る|書い|書く|考え)", "投稿文は草川が作る。事務員は『整える』まで"),
    (r"(訴え|主張|中身|内容).{0,6}(考え|決め|任せ)", "訴える中身を事務員に任せない"),
    (r"個人演説会.{0,8}(案内|告知|呼びかけ).{0,4}(する|して|を行)", "演説会の口頭案内は遊説車の役。告知画像の作成は可"),
    (r"(拡散|シェア|リポスト|いいね).{0,6}(お願い|依頼|頼)", "有権者への拡散依頼は選挙運動"),
    (r"(メール|ＤＭ|DM|LINE|ライン).{0,8}(送|配信|一斉)", "メールでの選挙運動は候補者・政党だけ。事務員に送らせない"),
    (r"(戸別|一軒(ずつ|一軒)|家々を回)", "戸別訪問は禁止"),
    (r"(自分|個人|櫻井).{0,4}(アカウント|SNS|X|インスタ).{0,10}(投稿|シェア|共有|拡散)", "櫻井さん自身のSNSで発信しない"),
    (r"(AI|ChatGPT|生成).{0,8}(投稿文|文章|キャプション|原稿)", "AIに文章を作らせない（誤字・改行の点検だけ）"),
    (r"(キャプション|文案|テロップ文|台本|構成|企画).{0,6}(考え|作|決め|任せ)", "中身の企画は草川が決める"),
    (r"(自由に|お任せ|おまかせ|判断で|いい感じ|好きなように)", "事務員に裁量を渡さない"),
    (r"(コメント|返信|リプ).{0,4}(返|対応|書)", "コメントへの返信は草川がする"),
    (r"(画像|告知).{0,8}(印刷|プリント|掲示|貼)", "告知画像は草川のアカウントに載せるだけ（印刷・掲示は文書図画の規制）"),
    (r"(SMS|ショートメ)", "SMSは電子メール扱い。事務員に送らせない"),
    (r"(誘導|受付|動員|人集め|サクラ|送迎)", "演説の場では撮影だけ。誘導・受付・動員・送迎はしない"),
    (r"(生配信|ライブ).{0,6}(話|実況|しゃべ)", "生配信で事務員が話さない"),
    (r"(歩合|再生数|成果|ボーナス|上乗せ).{0,8}(報酬|円|手当)", "成果に応じた報酬は払わない（日額のみ）"),
    (r"(情勢|優勢|当選確実|人気投票)", "情勢・人気投票の公表は禁止"),
    (r"(署名|アンケート).{0,6}(集め|取っ|お願い)", "署名・アンケート集めは選挙期間中させない"),
    (r"(飲食|お弁当|弁当|差し入れ).{0,6}(配|出す|渡)", "飲食物の提供は禁止（事務所内の湯茶・弁当の扱いは別途確認）"),
]
POST_WORDS = r"(投稿|告知画像|アップ|公開|配信)"


def texts(day):
    """日ごとの JSON から、チェック対象の文字を (場所, 文) で全部取り出す。"""
    yield "hours", day.get("hours", "")
    yield "todo_title", day.get("todo_title", "")
    yield "todo_sub", day.get("todo_sub", "")
    for b in day.get("blocks", []):
        yield f"blocks/{b.get('title')}", b.get("title", "")
        yield f"blocks/{b.get('title')}/sub", b.get("sub", "")
        yield f"blocks/{b.get('title')}/note", b.get("note", "")
        for t, w in b.get("items", []):
            yield f"blocks/{b.get('title')}/{t}", w
    for t in day.get("todos", []):
        yield "todos", t.get("text", "")
    for e in day.get("extra", []):
        yield "extra", e
    sp = day.get("spots")
    if sp:
        yield "spots", sp.get("label", "")
        for t, w in sp.get("items", []):
            yield f"spots/{t}", w


def check(day):
    errs, warns = [], []
    d = dt.date.fromisoformat(day["date"])
    for where, s in texts(day):
        n = unicodedata.normalize("NFKC", s or "")
        for pat, why in NG:
            if n and re.search(pat, n):
                errs.append(f"{day['date']} {where}: 「{s}」→ {why}")
    alltext = unicodedata.normalize("NFKC", " ".join(s or "" for _, s in texts(day)))
    if d == TOHYO - dt.timedelta(days=1):
        for where, s in texts(day):
            m = re.match(r"\s*(\d{1,2}):", unicodedata.normalize("NFKC", where.split("/")[-1]))
            if m and int(m.group(1)) >= 23:
                warns.append(f"{day['date']} {where}: 24日の投稿は23時までに終える（日付またぎの予約投稿に注意）")
    if d < KOJI and re.search(POST_WORDS, alltext):
        errs.append(f"{day['date']}: 告示前（10/18より前）に選挙運動の投稿・告知はできない（事前運動）")
    if d >= TOHYO and re.search(POST_WORDS, alltext):
        errs.append(f"{day['date']}: 投票日当日以降は新しい投稿・告知をしない")
    if d >= TOHYO - dt.timedelta(days=1) and day.get("spots"):
        errs.append(f"{day['date']}: 翌日（投票日）の演説告知は作らない。spots を消す")
    if day.get("spots"):
        nxt = d + dt.timedelta(days=1)
        if f"{nxt.month}月{nxt.day}日" not in day["spots"].get("label", ""):
            warns.append(f"{day['date']}: 告知の見出しに翌日の日付（{nxt.month}月{nxt.day}日）が無い")
    if not day.get("hours"):
        warns.append(f"{day['date']}: 勤務時間が空")
    return errs, warns


# ---- HTML ----
e = html.escape

CSS = """
/* 1カラム・縦スクロール。時刻を左の太字列に固定して、上から順に読めば1日が追える */
:root{
  --bg:#f5f7f3; --card:#ffffff; --fg:#1d2a22; --muted:#5d6b62; --line:#d9e1da;
  --green:#1f5a3a; --yellow:#f2c230; --yellow-ink:#3a2e00; --warn:#8a2b1a; --warn-bg:#fbeee9;
  --display:"Zen Kaku Gothic New","Hiragino Sans","Noto Sans JP",sans-serif;
  --body:"BIZ UDPGothic","Hiragino Sans","Noto Sans JP",sans-serif;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#121814; --card:#1b231e; --fg:#e8eee9; --muted:#9fb0a5; --line:#2c3a31;
  --green:#7fcf9f; --yellow:#f2c230; --yellow-ink:#2a2100; --warn:#ffb4a2; --warn-bg:#3a201a; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#121814; --card:#1b231e; --fg:#e8eee9; --muted:#9fb0a5; --line:#2c3a31;
  --green:#7fcf9f; --yellow:#f2c230; --yellow-ink:#2a2100; --warn:#ffb4a2; --warn-bg:#3a201a; color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:17px;line-height:1.7;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px 48px}
.wrap{max-width:560px;margin:0 auto;display:flex;flex-direction:column;gap:20px}
header{display:flex;flex-direction:column;gap:4px}
.to{font-size:15px;color:var(--muted)}
h1{font-family:var(--display);font-weight:900;font-size:26px;line-height:1.35;margin:0;text-wrap:balance}
.hours{display:inline-flex;align-self:flex-start;background:var(--yellow);color:var(--yellow-ink);
  font-weight:700;padding:4px 12px;border-radius:999px;font-variant-numeric:tabular-nums;margin-top:6px}
section{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;display:flex;flex-direction:column;gap:12px}
section.rule{border-color:var(--warn);}
h2{font-family:var(--display);font-weight:700;font-size:19px;margin:0;color:var(--green);display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline}
section.rule h2{color:var(--warn)}
h2 .t{font-size:14px;color:var(--muted);font-weight:400;font-variant-numeric:tabular-nums}
ol.tl{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
ol.tl li{display:grid;grid-template-columns:4.2em 1fr;gap:10px;align-items:baseline}
ol.tl .time{font-weight:700;font-variant-numeric:tabular-nums}
ol.tl .what{min-width:0}
.note{font-size:15px;color:var(--muted);border-top:1px dashed var(--line);padding-top:10px;margin:0}
.lead{font-size:15px;margin:0;background:var(--warn-bg);border-radius:8px;padding:10px 12px}
.todo{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
.todo label{display:grid;grid-template-columns:28px 1fr;gap:10px;align-items:start;cursor:pointer}
.todo input{width:24px;height:24px;margin:3px 0 0;accent-color:var(--green)}
.todo input:checked + span{color:var(--muted);text-decoration:line-through}
.first{display:inline-block;background:var(--yellow);color:var(--yellow-ink);font-size:13px;font-weight:700;padding:0 8px;border-radius:4px;margin-right:6px;vertical-align:2px}
.spots{margin:0;padding:12px;background:var(--bg);border-radius:8px;display:flex;flex-direction:column;gap:6px}
.spots .day{font-weight:700}
.spots div{display:grid;grid-template-columns:4.6em 1fr;gap:8px;font-variant-numeric:tabular-nums}
ul.plain{margin:0;padding-left:1.2em;display:flex;flex-direction:column;gap:6px}
details{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px}
details summary{cursor:pointer;font-weight:700;color:var(--muted)}
details[open] summary{margin-bottom:12px}
details .inner{display:flex;flex-direction:column;gap:14px}
footer{font-size:14px;color:var(--muted);text-align:center}
"""

FLOW = """
  <section>
    <h2>投稿の進め方</h2>
    <ol class="tl">
      <li><span class="time">1</span><span class="what">動画を編集し、投稿できる形にそろえる（演説のポイントは、編集のときにできるだけ草川から送ります）</span></li>
      <li><span class="time">2</span><span class="what">投稿文は、動画の内容をふまえて原則として草川が作る</span></li>
      <li><span class="time">3</span><span class="what">草川が確認してから投稿する</span></li>
    </ol>
    <p class="note">草川の手が回らず投稿が遅れそうなときは、草川が送った文を櫻井さんに整えてもらうことがあります。その場合も、投稿は草川が確認してからです。</p>
    <p class="note">整えるのは、誤字・改行・ハッシュタグまで。AIは誤字・改行の点検にだけ使い、AIに文章を作らせないでください。草川が送った文の順番や訴える中身は、足したり変えたりしないでください。</p>
  </section>

  <section>
    <h2>毎日の流れ</h2>
    <ul class="plain">
      <li>各地の演説動画は、編集ができ次第、できるだけ早く投稿の準備をする</li>
      <li>次の日の演説の場所と時間を知らせる画像は、前の日の夜に作る</li>
      <li>細かいお願いは、このページで毎日お知らせします</li>
    </ul>
  </section>

  <section class="rule">
    <h2>気をつけること <span class="t">選挙のきまり</span></h2>
    <p class="lead">櫻井さんは「事務員」としてのお手伝いです。撮影・編集・画像づくり・投稿の作業に専念してください。</p>
    <ul class="plain">
      <li>演説の場所では撮影だけをする。聴衆の誘導・受付・のぼり持ち・人の送迎はしない</li>
      <li>演説、マイクでの呼びかけ、チラシ配り、握手や手振り、電話などで投票をお願いすることはしない</li>
      <li>タスキ・のぼり・候補者名の入った服などは身に着けない</li>
      <li>櫻井さんの車に、看板・ポスター・スピーカーは付けない</li>
      <li>櫻井さん自身のSNSで、シェア・応援の投稿・コメントをしない</li>
      <li>草川のアカウントでも、コメントへの返信はしない（草川がします）</li>
      <li>告知画像は草川のアカウントに載せるだけ。印刷・掲示・個別に送ることはしない。日時と場所は指示どおりにし、言葉を足さない</li>
      <li>お金を払って表示を増やす広告機能は使わない</li>
      <li>メール・SMS・LINEで、知り合いに投票や拡散をお願いしない</li>
      <li>投稿は24日（土）の23時までに終える。25日（投票日）は投稿も修正もしない</li>
      <li>一般の方、特に子どもの顔がはっきり映る場面は、ぼかしを入れるか使わない。子どもが手を振ったり応援したりする場面は使わない</li>
    </ul>
  </section>
"""


def jp_date(d):
    return f"{d.month}月{d.day}日（{WEEK[d.weekday()]}）"


def day_html(day):
    d = dt.date.fromisoformat(day["date"])
    out = []
    for b in day.get("blocks", []):
        items = "".join(
            f'<li><span class="time">{e(t)}</span><span class="what">{e(w)}</span></li>'
            for t, w in b.get("items", []))
        note = f'<p class="note">{e(b["note"])}</p>' if b.get("note") else ""
        sub = f' <span class="t">{e(b["sub"])}</span>' if b.get("sub") else ""
        out.append(f'<section><h2>{e(b["title"])}{sub}</h2><ol class="tl">{items}</ol>{note}</section>')
    todos = day.get("todos", [])
    sp = day.get("spots")
    if todos or sp:
        lis = "".join(
            f'<li><label><input type="checkbox" id="{day["date"]}-{i}"><span>'
            f'{"<span class=first>最優先</span>" if t.get("first") else ""}{e(t["text"])}</span></label></li>'
            for i, t in enumerate(todos))
        spots = ""
        if sp:
            rows = "".join(f"<div><span>{e(t)}</span><span>{e(w)}</span></div>" for t, w in sp["items"])
            spots = f'<div class="spots"><span class="day">{e(sp["label"])}</span>{rows}</div>'
        title = e(day.get("todo_title", "事務所での作業"))
        sub = f' <span class="t">{e(day["todo_sub"])}</span>' if day.get("todo_sub") else ""
        out.append(f'<section><h2>{title}{sub}</h2><ul class="todo">{lis}</ul>{spots}</section>')
    for x in day.get("extra", []):
        out.append(f'<section><p style="margin:0">{e(x)}</p></section>')
    return d, "\n".join(out)


def build(days):
    days = sorted(days, key=lambda x: x["date"], reverse=True)
    d0, body0 = day_html(days[0])
    past = []
    for day in days[1:]:
        d, b = day_html(day)
        past.append(f'<details><summary>{jp_date(d)} のお願い（済）</summary><div class="inner">{b}</div></details>')
    return f"""<title>櫻井さん 動画担当メモ</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;700;900&family=BIZ+UDPGothic:wght@400;700&display=swap">
<style>{CSS}</style>
<div class="wrap">
  <header>
    <div class="to">櫻井 祐輝さんへ（事務員・動画編集）</div>
    <h1>{jp_date(d0)}のお願い</h1>
    <div class="hours">勤務 {e(days[0].get("hours", ""))}</div>
  </header>
{body0}
{FLOW}
{"".join(past)}
  <footer>草川たくや 事務所</footer>
</div>
<script>
document.querySelectorAll('.todo input').forEach(function(cb){{
  try{{ cb.checked = localStorage.getItem('sakurai_'+cb.id)==='1'; }}catch(e){{}}
  cb.addEventListener('change',function(){{
    try{{ localStorage.setItem('sakurai_'+cb.id, cb.checked?'1':'0'); }}catch(e){{}}
  }});
}});
</script>
"""


def main():
    days = [json.loads(p.read_text()) for p in sorted(DATA_DIR.glob("*.json"))]
    if not days:
        sys.exit(f"データがありません: {DATA_DIR}")
    errs, warns = [], []
    for day in days:
        a, b = check(day)
        errs += a
        warns += b
    for w in warns:
        print("WARN ", w)
    for x in errs:
        print("ERROR", x)
    if errs:
        print(f"\n公選法チェック NG {len(errs)}件。HTMLは書いていません。")
        sys.exit(1)
    print("公選法チェック OK")
    if "--check" in sys.argv:
        return
    OUT.write_text(build(days))
    print(f"書き出し: {OUT}")


if __name__ == "__main__":
    main()

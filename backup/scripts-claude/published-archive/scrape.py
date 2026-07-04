#!/usr/bin/env python3
# 草川たくや 公開済アーカイブ スクレイパー
# 用途: ブログ(go2senkyo)/Threads/YouTubeの実テキストを取得し、Notion投入用JSONを出力
#
# 使い方:
#   python3 scrape.py                  # 全ソースを取得しJSON出力
#   python3 scrape.py --source blog    # 個別ソース指定
#   python3 scrape.py --since 30       # 過去N日のみ（差分取得用）
#
# 出力: ~/.claude/scripts/published-archive/output.json

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict, Optional
from xml.etree import ElementTree as ET
from html import unescape

# ──────────────────────────────────────────────────────────
# 定数
# ──────────────────────────────────────────────────────────

BLOG_RSS = "https://www.go2senkyo.com/seijika/168135/posts.rss"
BLOG_BASE = "https://seijiyama.jp"  # go2senkyo URL は相対参照のことがあるので仮ベース
GO2_BASE = "https://www.go2senkyo.com"
YOUTUBE_CHANNEL_ID = "UCy_ttKLUr0q14q77wBKMNVA"
YOUTUBE_RSS = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"
THREADS_HANDLE = "kusagawatakuya"
THREADS_URL = f"https://www.threads.com/@{THREADS_HANDLE}?hl=ja"

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# RSS namespace
NS_ATOM = "http://www.w3.org/2005/Atom"
NS_YT = "http://www.youtube.com/xml/schemas/2015"
NS_MEDIA = "http://search.yahoo.com/mrss/"

# ──────────────────────────────────────────────────────────
# ユーティリティ
# ──────────────────────────────────────────────────────────

def fetch(url: str, timeout: int = 15) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ja"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def strip_html(html: str) -> str:
    """HTMLタグを除去し、空白を整える。"""
    if not html:
        return ""
    # script/styleブロック除去
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.S)
    # figure内の画像URL除去（本文に不要）
    html = re.sub(r"<figure[^>]*>.*?</figure>", "", html, flags=re.S)
    # ブロック要素を改行へ
    html = re.sub(r"</(p|div|h[1-6]|li|br)\s*>", "\n", html, flags=re.I)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    # 残タグ除去
    html = re.sub(r"<[^>]+>", "", html)
    text = unescape(html)
    # 空行整理
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_pubdate_rfc822(s: str) -> str:
    """RFC822形式の日時文字列をISO8601へ変換。"""
    if not s:
        return ""
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()
    except Exception:
        return s


def days_ago(iso_str: str) -> int:
    """ISO日時文字列から「今から何日前か」を返す。失敗時は999。"""
    if not iso_str:
        return 999
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        delta = datetime.now(timezone.utc) - dt
        return delta.days
    except Exception:
        return 999


# ──────────────────────────────────────────────────────────
# ブログ (go2senkyo RSS)
# ──────────────────────────────────────────────────────────

def scrape_blog(since_days: Optional[int] = None) -> List[Dict]:
    xml_text = fetch(BLOG_RSS)
    root = ET.fromstring(xml_text)
    channel = root.find("channel")
    if channel is None:
        return []
    items = []
    for item in channel.findall("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        # go2senkyoは相対パスを返すことがある
        if link.startswith("/"):
            link = GO2_BASE + link
        pubdate = parse_pubdate_rfc822(item.findtext("pubDate") or "")
        desc = item.findtext("description") or ""
        body = strip_html(desc)
        if since_days is not None and days_ago(pubdate) > since_days:
            continue
        items.append({
            "media": "ブログ",
            "title": title,
            "url": link,
            "published": pubdate,
            "body": body,
            "char_count": len(body),
        })
    return items


# ──────────────────────────────────────────────────────────
# YouTube (公式RSS)
# ──────────────────────────────────────────────────────────

def scrape_youtube(since_days: Optional[int] = None) -> List[Dict]:
    xml_text = fetch(YOUTUBE_RSS)
    root = ET.fromstring(xml_text)
    items = []
    for entry in root.findall(f"{{{NS_ATOM}}}entry"):
        title = (entry.findtext(f"{{{NS_ATOM}}}title") or "").strip()
        link_el = entry.find(f"{{{NS_ATOM}}}link")
        link = link_el.get("href") if link_el is not None else ""
        published = (entry.findtext(f"{{{NS_ATOM}}}published") or "").strip()
        media_group = entry.find(f"{{{NS_MEDIA}}}group")
        description = ""
        if media_group is not None:
            description = (media_group.findtext(f"{{{NS_MEDIA}}}description") or "").strip()
        if since_days is not None and days_ago(published) > since_days:
            continue
        items.append({
            "media": "YouTube",
            "title": title,
            "url": link,
            "published": published,
            "body": description,
            "char_count": len(description),
        })
    return items


# ──────────────────────────────────────────────────────────
# Threads (公開HTML・限定的)
# ──────────────────────────────────────────────────────────

def scrape_threads(since_days: Optional[int] = None) -> List[Dict]:
    """Threads公開プロフィールから直近の投稿テキストを抽出。
    ログイン制限のため5〜10件程度。確実性は中程度。"""
    try:
        html = fetch(THREADS_URL)
    except Exception as e:
        return [{"_error": f"threads_fetch_failed: {e}"}]

    items = []
    # 投稿IDパターン: /@kusagawatakuya/post/XXXXX
    post_pattern = re.compile(rf'/@{re.escape(THREADS_HANDLE)}/post/([A-Za-z0-9_-]+)')
    seen_ids = set()
    for m in post_pattern.finditer(html):
        pid = m.group(1)
        if pid in seen_ids:
            continue
        seen_ids.add(pid)

    # 各投稿IDの近傍テキストを収集（簡易抽出・不安定だがフォールバックとして有効）
    # JSON埋め込みから text フィールドを抜く試み
    # Threadsは大きなJSONをHTMLに埋め込んでいる
    for pid in seen_ids:
        text_match = re.search(
            rf'"code":"{re.escape(pid)}"[^}}]*?"text":"((?:[^"\\]|\\.)*?)"',
            html
        )
        text = ""
        if text_match:
            text = text_match.group(1)
            # JSONエスケープ解除
            try:
                text = json.loads(f'"{text}"')
            except Exception:
                text = text.replace("\\n", "\n").replace('\\"', '"')

        # taken_at (UNIX timestamp) を探す
        ts_match = re.search(
            rf'"code":"{re.escape(pid)}"[^}}]*?"taken_at":(\d+)',
            html
        )
        published = ""
        if ts_match:
            ts = int(ts_match.group(1))
            published = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()

        if since_days is not None and published and days_ago(published) > since_days:
            continue

        title = (text[:30] + "…") if len(text) > 30 else text
        if not title:
            title = f"Thread {pid}"
        items.append({
            "media": "Threads",
            "title": title,
            "url": f"https://www.threads.com/@{THREADS_HANDLE}/post/{pid}",
            "published": published,
            "body": text,
            "char_count": len(text),
        })

    return items


# ──────────────────────────────────────────────────────────
# main
# ──────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", choices=["blog", "youtube", "threads", "all"], default="all")
    p.add_argument("--since", type=int, default=None, help="過去N日のみ取得（差分取得用）")
    p.add_argument("--out", default=str(Path.home() / ".claude/scripts/published-archive/output.json"))
    args = p.parse_args()

    results = []
    errors = []

    if args.source in ("blog", "all"):
        try:
            results.extend(scrape_blog(args.since))
        except Exception as e:
            errors.append(f"blog: {e}")
    if args.source in ("youtube", "all"):
        try:
            results.extend(scrape_youtube(args.since))
        except Exception as e:
            errors.append(f"youtube: {e}")
    if args.source in ("threads", "all"):
        try:
            results.extend(scrape_threads(args.since))
        except Exception as e:
            errors.append(f"threads: {e}")

    out = {
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "since_days": args.since,
        "count": len([r for r in results if "_error" not in r]),
        "errors": errors,
        "items": results,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"取得 {out['count']} 件 / errors: {len(errors)}")
    print(f"出力: {args.out}")
    # 内訳
    by_media = {}
    for r in results:
        if "_error" in r:
            continue
        by_media.setdefault(r["media"], 0)
        by_media[r["media"]] += 1
    for k, v in sorted(by_media.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()

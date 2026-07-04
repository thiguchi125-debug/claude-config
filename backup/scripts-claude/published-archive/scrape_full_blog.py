#!/usr/bin/env python3
"""草川たくや 過去ブログ全件取得スクリプト
発見した記事URLリストから本文・タイトル・公開日を抽出し output_full.json に保存
"""

import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from html import unescape

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
PROFILE_BASE = "https://go2senkyo.com/seijika/168135/posts"

# Google検索＋output.jsonから発見したID全件
DISCOVERED_IDS = sorted(set([
    # output.jsonから(2026-04付近〜直近)
    "1350165", "1351939", "1353762", "1356898", "1359316",
    "1360894", "1364471", "1366174", "1367845", "1370223",
    # Google検索で発見
    "311522", "364330", "366643", "461189", "464139", "479983",
    "504462", "528938", "555447",
    "740914", "743821", "750336", "753188", "765810", "798998",
    "876714", "913635", "918240", "946329", "986956", "993728", "998953",
    "1020745", "1036233", "1060241", "1067443", "1069607",
    "1072729", "1076367", "1130752", "1140205",
    "1157198", "1161186", "1178617", "1221097", "1221689",
    "1246471", "1294549", "1301799", "1303694", "1311214",
    "1336338", "1347557",
]))


def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ja"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace"), r.status, r.url


def extract_post(html, post_id):
    """個別記事HTMLからtitle, body, publishedを抽出"""
    # Title
    title_m = re.search(r"<title>([^<]+)</title>", html)
    title = title_m.group(1).strip() if title_m else ""
    # 「【〜】〜 - 草川たくや（〜）｜選挙ドットコム」から本タイトル抜き
    title = re.sub(r"\s*-\s*草川たくや.*?選挙ドットコム\s*$", "", title)

    # Published date (YYYY/M/D or 2026/5/4 形式) — p_seijika_detail_data 内
    date_section = re.search(
        r'<div[^>]+class=[\'"][^\'"]*p_seijika_detail_data[^\'"]*[\'"][^>]*>(.*?)</div>',
        html, re.S
    )
    published = ""
    if date_section:
        date_m = re.search(r"(20\d{2}/\d{1,2}/\d{1,2})", date_section.group(1))
        if date_m:
            try:
                dt = datetime.strptime(date_m.group(1), "%Y/%m/%d")
                published = dt.replace(tzinfo=timezone.utc).isoformat()
            except Exception:
                pass

    # Body — 「こんにちは、亀山市議会議員の草川たくやです」から SNS手前まで
    body = ""
    body_m = re.search(
        r'(<p[^>]*>[^<]*?こんにちは、亀山市議会議員の草川たくやです[^<]*?</p>)(.*?)<div class=[\'"]p_article_detail_contents_sns',
        html, re.S
    )
    if body_m:
        raw = body_m.group(1) + body_m.group(2)
        # script/style除外
        raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", raw, flags=re.S)
        # figure(画像)除外
        raw = re.sub(r"<figure[^>]*>.*?</figure>", "", raw, flags=re.S)
        # ブロック→改行
        raw = re.sub(r"</(p|div|h[1-6]|li|br)\s*>", "\n", raw, flags=re.I)
        raw = re.sub(r"<br\s*/?>", "\n", raw, flags=re.I)
        # 残タグ除去
        raw = re.sub(r"<[^>]+>", "", raw)
        body = unescape(raw)
        body = re.sub(r"\n[ \t]+", "\n", body)
        body = re.sub(r"\n{3,}", "\n\n", body)
        body = body.strip()
    else:
        # フォールバック: p_seijika_detail_contents_inner
        inner_m = re.search(
            r'<div[^>]+class=[\'"][^\'"]*p_seijika_detail_contents_inner[^\'"]*[\'"][^>]*>(.*?)<div class=[\'"]p_article_detail_contents_sns',
            html, re.S
        )
        if inner_m:
            raw = inner_m.group(1)
            raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", raw, flags=re.S)
            raw = re.sub(r"<figure[^>]*>.*?</figure>", "", raw, flags=re.S)
            raw = re.sub(r"</(p|div|h[1-6]|li|br)\s*>", "\n", raw, flags=re.I)
            raw = re.sub(r"<br\s*/?>", "\n", raw, flags=re.I)
            raw = re.sub(r"<[^>]+>", "", raw)
            body = unescape(raw)
            body = re.sub(r"\n[ \t]+", "\n", body)
            body = re.sub(r"\n{3,}", "\n\n", body)
            body = body.strip()

    return {
        "media": "ブログ",
        "title": title,
        "url": f"{PROFILE_BASE}/{post_id}",
        "published": published,
        "body": body,
        "char_count": len(body),
        "post_id": post_id,
    }


def main():
    print(f"Discovering {len(DISCOVERED_IDS)} blog post IDs...")

    items = []
    errors = []

    for i, pid in enumerate(DISCOVERED_IDS, 1):
        url = f"{PROFILE_BASE}/{pid}"
        try:
            html, status, final_url = fetch(url)
            item = extract_post(html, pid)
            if not item["body"]:
                errors.append({"id": pid, "url": url, "reason": "body extraction failed"})
                print(f"  [{i}/{len(DISCOVERED_IDS)}] {pid} ⚠️ body empty (title: {item['title'][:40]})")
            else:
                items.append(item)
                print(f"  [{i}/{len(DISCOVERED_IDS)}] {pid} ✓ {item['char_count']}字 / {item['published'][:10]} / {item['title'][:40]}")
        except Exception as e:
            errors.append({"id": pid, "url": url, "reason": str(e)})
            print(f"  [{i}/{len(DISCOVERED_IDS)}] {pid} ✗ {e}")
        time.sleep(0.5)  # サーバ負荷配慮

    out = {
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "source": "google_search_discovered_urls",
        "discovered_id_count": len(DISCOVERED_IDS),
        "ok_count": len(items),
        "error_count": len(errors),
        "errors": errors,
        "items": items,
    }

    out_path = Path.home() / ".claude/scripts/published-archive/output_full.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print()
    print(f"=== SUMMARY ===")
    print(f"Discovered IDs: {len(DISCOVERED_IDS)}")
    print(f"Successfully extracted: {len(items)}")
    print(f"Errors: {len(errors)}")
    print(f"Output: {out_path}")
    if items:
        total_chars = sum(it["char_count"] for it in items)
        print(f"Total body chars: {total_chars:,}")


if __name__ == "__main__":
    main()

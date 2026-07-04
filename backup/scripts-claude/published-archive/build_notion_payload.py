#!/usr/bin/env python3
# scrape.py の出力 (output.json) を Notion create-pages 用ペイロードへ変換
# 使い方: python3 build_notion_payload.py [--out payload.json]

import argparse
import json
from pathlib import Path

DATA_SOURCE_ID = "0ae2d907-d804-49ab-9860-b4b981d34c56"

# 本文プロパティの最大 (Notion rich_text は1ブロック2000字目安、安全に1900)
BODY_PROP_MAX = 1900

# ページ content (markdown) は短い抜粋＋メタ情報のみ（voice-dnaはローカルJSON参照）
CONTENT_MAX = 400


def build_pages(items):
    pages = []
    for it in items:
        if "_error" in it:
            continue
        title = it.get("title") or "(無題)"
        media = it.get("media") or "その他"
        url = it.get("url") or ""
        published = it.get("published") or ""
        body = it.get("body") or ""
        char_count = it.get("char_count", len(body))

        # 本文プロパティはサマリ用（先頭1500字）
        body_summary = body[:BODY_PROP_MAX]

        # ページ content（markdown）はメタデータ＋短い抜粋＋全文ローカル参照
        excerpt = body[:CONTENT_MAX]
        content_lines = [
            f"## {media} 公開済テキスト",
            "",
            f"- 公開URL: {url}",
            f"- 公開日: {published}",
            f"- 文字数: {char_count}",
            "",
            "### 抜粋（先頭2000字）",
            "",
            excerpt,
        ]
        if len(body) > CONTENT_MAX:
            content_lines.append("")
            content_lines.append("---")
            content_lines.append("*全文は公開URLで確認。voice-dna抽出はローカルJSON（output.json）を使用。*")
        content = "\n".join(content_lines)

        pages.append({
            "icon": {"ブログ": "📝", "Threads": "🧵", "YouTube": "🎥"}.get(media, "📚"),
            "properties": {
                "タイトル": title[:200],  # title 安全上限
                "媒体": media,
                "公開URL": url,
                "date:公開日:start": published,
                "date:公開日:is_datetime": 1,
                "本文": body_summary,
                "文字数": char_count,
                "voice-DNA抽出済": "__NO__",
                "差分あり": "__NO__",
            },
            "content": content,
        })
    return pages


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="in_path", default=str(Path.home() / ".claude/scripts/published-archive/output.json"))
    p.add_argument("--out", default=str(Path.home() / ".claude/scripts/published-archive/payload.json"))
    args = p.parse_args()

    with open(args.in_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items", [])
    pages = build_pages(items)

    out = {
        "parent": {"type": "data_source_id", "data_source_id": DATA_SOURCE_ID},
        "pages": pages,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Notionペイロード生成: {len(pages)} ページ")
    print(f"出力: {args.out}")


if __name__ == "__main__":
    main()

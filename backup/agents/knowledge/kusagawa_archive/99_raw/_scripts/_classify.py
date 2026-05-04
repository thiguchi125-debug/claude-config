#!/usr/bin/env python3
"""ファイル名からカテゴリを自動判定するヘルパー。

スキルから呼ばれて、Drive MCP の search_files 結果（JSON）を受け取り、
カテゴリ別にバケットを返す。

入出力:
  stdin: Drive search_files の files[] JSON
  stdout: { auto_council: [...], auto_reports: [...], pending: [...], skipped: [...] } JSON

使い方（スキル内）:
  echo "$DRIVE_FILES_JSON" | python3 _classify.py
"""
import json
import re
import sys
from pathlib import Path

# ===== カテゴリ判定パターン =====

# 議事録: 確実に学習層に入れたい
COUNCIL_PATTERNS = [
    re.compile(r'kaigiroku', re.IGNORECASE),
    re.compile(r'議事録'),
    re.compile(r'会議録'),
    re.compile(r'委員会'),
    re.compile(r'本会議'),
    re.compile(r'定例会'),
    re.compile(r'^[Rr]\d+\.\d+'),         # R8.3.18 形式
    re.compile(r'^[Rr]\d{4}'),            # R0703 形式
    re.compile(r'^\d{3,4}\.pdf$'),        # 3012.pdf, 313.pdf 形式
    re.compile(r'予算決算'),
    re.compile(r'決算委員会'),
    re.compile(r'総合計画'),
    re.compile(r'通告書'),
    re.compile(r'一般質問'),
    re.compile(r'代表質問'),
    re.compile(r'代表質疑'),
    re.compile(r'議案質疑'),
    re.compile(r'総括質疑'),
    re.compile(r'^令和[\d０-９]+年'),     # 令和8年3月10日.docx
]

# 市政報告: 公開発信物として保管
REPORT_PATTERNS = [
    re.compile(r'市政報告'),
    re.compile(r'市政レポート'),
    re.compile(r'号外'),
    re.compile(r'地区版'),
    re.compile(r'ニュース'),
    re.compile(r'チラシ'),
    re.compile(r'昼生'),
    re.compile(r'二本松'),
    re.compile(r'みずきが丘'),
    re.compile(r'けんろう'),
    re.compile(r'菅内'),
    re.compile(r'御幸'),
    re.compile(r'東部'),
    re.compile(r'南部'),
    re.compile(r'下庄'),
    re.compile(r'田村'),
    re.compile(r'出屋'),
    re.compile(r'川崎'),
    re.compile(r'井田川'),
    re.compile(r'神辺'),
    re.compile(r'城東'),
    re.compile(r'北東'),
]

# 自動スキップ（学習層に入れたくないノイズ）
SKIP_PATTERNS = [
    re.compile(r'テンプレ'),
    re.compile(r'テンプレート'),
    re.compile(r'草案'),
    re.compile(r'下書き'),
    re.compile(r'private', re.IGNORECASE),
    re.compile(r'個人'),
    re.compile(r'非公開'),
    re.compile(r'指示書'),
    re.compile(r'アシスタント'),
    re.compile(r'^\.'),                    # 隠しファイル
    re.compile(r'\.DS_Store$'),
    re.compile(r'~\$'),                    # Office一時ファイル
    re.compile(r'^\d+\.png$', re.IGNORECASE),  # 一般質問資料スライド画像
]

# サポートmime（テキスト化可能なものだけ取込候補）
SUPPORTED_MIMES = {
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # docx
    'application/vnd.google-apps.document',                                      # gdoc
    'text/plain',
    'text/markdown',
}

# 音声・動画・画像は学習対象外（OCR要は別途記録）
EXCLUDE_MIMES = {
    'audio/mpeg', 'audio/wav', 'audio/m4a', 'audio/ogg',
    'video/mp4', 'video/quicktime',
    'image/png', 'image/jpeg', 'image/heic', 'image/gif',
}


def classify(file_meta: dict) -> tuple[str, str]:
    """1ファイルのメタ情報からカテゴリを判定。

    Returns:
        (category, reason) のタプル
        category: auto_council / auto_reports / pending / skipped
    """
    title = file_meta.get('title', '')
    mime = file_meta.get('mimeType', '')

    # 1. 自動スキップ判定（最優先）
    for pat in SKIP_PATTERNS:
        if pat.search(title):
            return 'skipped', f'skip pattern: {pat.pattern}'

    # 2. mime除外（音声/動画/画像）
    if mime in EXCLUDE_MIMES:
        return 'skipped', f'excluded mime: {mime}'

    # 3. mime非対応（zipなど）
    if mime not in SUPPORTED_MIMES and not mime.startswith('application/vnd.google-apps.'):
        return 'pending', f'unsupported mime: {mime} → manual review'

    # 4. 議事録パターン（高信頼自動取込）
    for pat in COUNCIL_PATTERNS:
        if pat.search(title):
            return 'auto_council', f'council pattern: {pat.pattern}'

    # 5. 市政報告パターン（高信頼自動取込）
    for pat in REPORT_PATTERNS:
        if pat.search(title):
            return 'auto_reports', f'report pattern: {pat.pattern}'

    # 6. それ以外は確認待ち
    return 'pending', 'no pattern match'


def main():
    """stdin の Drive files JSON を分類。"""
    data = json.load(sys.stdin)
    files = data.get('files', data) if isinstance(data, dict) else data

    buckets = {
        'auto_council': [],
        'auto_reports': [],
        'pending': [],
        'skipped': [],
    }

    for f in files:
        cat, reason = classify(f)
        f['classification_reason'] = reason
        buckets[cat].append(f)

    summary = {k: len(v) for k, v in buckets.items()}
    print(json.dumps({
        'summary': summary,
        'buckets': buckets,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

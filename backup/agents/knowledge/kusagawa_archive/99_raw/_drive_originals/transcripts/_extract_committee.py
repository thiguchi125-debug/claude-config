#!/usr/bin/env python3
"""委員会音声起こしtxt用の草川パート抽出。

本会議PDFと違い、委員会txtは「○○委員。」「○○課長。」のような短い指名行
（委員長による次発言者の呼びかけ）で発言者が切り替わる。

ロジック:
- 行全体が「(.+)委員。」または「(.+)議員。」または「(.+)さん。」のような
  指名行を検出
- 草川拓也議員/草川委員/草川さん の指名 → ON
- 別議員/委員 の指名 → OFF
- 答弁行: 課長/部長/市長/局長/室長/参事/教育長 等の指名は ON 中のみ出力
- 「草川子供政策課長」は別人なので明示除外
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
TEXT_DIR = ROOT / "_text"
OUT_DIR = ROOT / "_kusagawa_only"
OUT_DIR.mkdir(exist_ok=True)

COMMITTEE_FILES = [
    "R8.3.18決算委員会（総合計画）_20260318162653.txt",
    "R8.3.23予算決算委員会_20260323172950.txt",
]

# 単独行で短い指名行 (例: "草川委員。" "桜井委員。" "産業環境部長。")
SUMMON_RE = re.compile(r'^[ 　]*(.{1,20}?)[。.]\s*$')
# 草川本人 (「子供政策課長草川」「草川子供政策課長」「草川美幸」等は除外)
KUSAGAWA_SELF_RE = re.compile(r'^(?:浅川)?草川(?:拓也|たくや)?(?:議員|委員|さん)$')
# 別議員/委員（草川以外）
OTHER_GIIN_RE = re.compile(r'^(?!.*草川).{1,15}?(?:議員|委員|さん)$')
# 執行部役職
EXEC_KEYWORDS = ('市長', '副市長', '教育長', '部長', '局長', '室長', '参事',
                 '課長', '主幹', '管理者', 'センター長', '館長', '園長')
# 子供政策課長草川（別人ノイズ）
NOISE_RE = re.compile(r'子供政策課長草川|草川子供政策課長|草川美幸')


def is_exec_summon(text: str) -> bool:
    if NOISE_RE.search(text):
        return False
    return any(text.endswith(k) for k in EXEC_KEYWORDS)


def process(in_path: Path):
    lines = in_path.read_text(encoding="utf-8", errors="replace").splitlines()
    out_lines = [
        f"# 草川パート＋執行部答弁抽出（委員会txt用）: {in_path.name}",
        f"# 元ファイル: {in_path.relative_to(ROOT.parent)}",
        "# 抽出ルール: 「草川委員。」「草川拓也議員。」等の指名でON、別議員/委員でOFF。間の執行部答弁を含む。「草川子供政策課長」「草川美幸」は別人として除外。",
        "---",
    ]
    state = "OFF"
    block_buffer: list[str] = []
    sessions = 0

    def flush():
        nonlocal block_buffer, sessions
        if block_buffer and state == "ON":
            out_lines.extend(block_buffer)
            out_lines.append("")
            sessions += 1
        block_buffer.clear()

    for line in lines:
        m = SUMMON_RE.match(line)
        if m:
            text = m.group(1).strip()
            # ノイズ除外
            if NOISE_RE.search(text):
                if state == "ON":
                    block_buffer.append(line)
                continue
            if KUSAGAWA_SELF_RE.match(text):
                if state == "OFF":
                    flush()
                    state = "ON"
                    out_lines.append(f"\n========== セッション {sessions+1} 開始 ==========")
                block_buffer.append(line)
                continue
            if OTHER_GIIN_RE.match(text):
                # 別議員 → OFF
                flush()
                state = "OFF"
                continue
            if is_exec_summon(text):
                if state == "ON":
                    block_buffer.append(line)
                continue
            # その他のマーカー（委員長/院長/副委員長等）→ 状態維持
            if state == "ON":
                block_buffer.append(line)
        else:
            if state == "ON":
                block_buffer.append(line)

    flush()

    if sessions == 0:
        return 0, 0

    out_path = OUT_DIR / in_path.name.replace(".txt", "_kusagawa_only.txt")
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    return len(out_lines), sessions


def main():
    for fn in COMMITTEE_FILES:
        p = TEXT_DIR / fn
        if not p.exists():
            print(f"NOT FOUND: {fn}")
            continue
        n, s = process(p)
        print(f"{fn:<70} 抽出行={n:>6} sessions={s:>3}")


if __name__ == "__main__":
    main()

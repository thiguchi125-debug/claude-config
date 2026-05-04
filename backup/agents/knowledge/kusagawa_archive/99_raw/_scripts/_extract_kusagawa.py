#!/usr/bin/env python3
"""草川パート＋亀山市執行部答弁ペアのみ抽出する。

ロジック:
- 発言者マーカー行: ^[\s　]*[◯○〇][\s　]*(.+?)（(.+?)君[登壇]?[）)]
- 議員マーカー: 役職部分が「N番」 → 議員。名前が「草川」なら草川パートON、それ以外ならOFF
- 執行部マーカー: 役職部分が市長/副市長/教育長/部長/局長/室長/参事 → ON状態時のみ出力
- 議長マーカー: 役職が「議長」「副議長」 → 進行案内として常に出力（短いので可読性のため）
- ON状態中は全行を出力、OFFになったら止める

入出力:
  入力: _text/*.txt
  出力: _kusagawa_only/<basename>.txt
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
TEXT_DIR = ROOT / "_text"
OUT_DIR = ROOT / "_kusagawa_only"
OUT_DIR.mkdir(exist_ok=True)

# 発言者マーカー: ◯/○/〇 + 役職 + （氏名君[登壇]）
SPEAKER_RE = re.compile(
    r'^[\s　]*[◯○〇][\s　]*([^（(]{1,30})[（(]([^（(]{1,40}?)君[登壇]*\s*[）)]'
)
# 議員マーカー: 役職が「N番」または「議員」を含む形（補欠等）
GIIN_RE = re.compile(r'^\d{1,2}番$|議員$')
# 執行部マーカー: 市長/副市長/教育長/部長/局長/室長/参事/教育委員会事務局長等
EXEC_RE = re.compile(
    r'^(市長|副市長|教育長|.*部長|.*局長|.*室長|.*参事|.*課長|.*委員長|.*センター長|.*管理者|.*主幹)$'
)
# 議長マーカー
GICHO_RE = re.compile(r'^(議長|副議長)$')

KUSAGAWA_PAT = re.compile(r'草川')


def process(in_path: Path) -> tuple[int, int]:
    """1ファイル処理。返り値: (草川パート行数, 全行数)"""
    lines = in_path.read_text(encoding="utf-8", errors="replace").splitlines()
    out_lines = []
    state = "OFF"  # ON / OFF
    out_lines.append(f"# 草川パート＋執行部答弁抽出: {in_path.name}")
    out_lines.append(f"# 元ファイル: {in_path.relative_to(ROOT.parent)}")
    out_lines.append("# 抽出ルール: ◯N番（草川卓也君）で開始、別議員（◯N番（他氏君））で終了。間の議長進行・市長/部長等執行部答弁を含む。")
    out_lines.append("---")

    block_buffer: list[str] = []
    sessions = 0

    def flush_if_active():
        nonlocal block_buffer, sessions
        if block_buffer and state == "ON":
            out_lines.extend(block_buffer)
            out_lines.append("")
            sessions += 1
        block_buffer.clear()

    for line in lines:
        m = SPEAKER_RE.match(line)
        if m:
            yakushoku = m.group(1).strip()
            shimei = m.group(2).strip()
            is_giin = bool(GIIN_RE.search(yakushoku))
            is_kusagawa = is_giin and bool(KUSAGAWA_PAT.search(shimei))
            is_exec = bool(EXEC_RE.match(yakushoku))
            is_gicho = bool(GICHO_RE.match(yakushoku))

            if is_kusagawa:
                if state == "OFF":
                    flush_if_active()
                    state = "ON"
                    out_lines.append(f"\n========== セッション {sessions+1} 開始 ==========")
                block_buffer.append(line)
            elif is_giin and not is_kusagawa:
                # 別議員 → 草川セッション終了
                flush_if_active()
                state = "OFF"
                block_buffer.clear()
            elif is_exec or is_gicho:
                if state == "ON":
                    block_buffer.append(line)
                # OFFのときは無視
            else:
                # 不明なマーカーは状態に従う
                if state == "ON":
                    block_buffer.append(line)
        else:
            # 通常の本文行
            if state == "ON":
                block_buffer.append(line)

    # 最終フラッシュ
    flush_if_active()

    if sessions == 0:
        return 0, len(lines)

    out_path = OUT_DIR / in_path.name.replace(".txt", "_kusagawa_only.txt")
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    return len([l for l in out_lines if l.strip()]), sessions


def main():
    files = sorted(TEXT_DIR.glob("*.txt"))
    summary = []
    for f in files:
        n_lines, sessions = process(f)
        summary.append((f.name, n_lines, sessions))

    print(f"処理ファイル数: {len(files)}")
    print(f"{'file':<60} {'抽出行':>8} {'sessions':>8}")
    for name, n, s in summary:
        print(f"{name:<60} {n:>8} {s:>8}")


if __name__ == "__main__":
    main()

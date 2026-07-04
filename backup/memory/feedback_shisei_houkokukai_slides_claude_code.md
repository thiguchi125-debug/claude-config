---
name: feedback-shisei-houkokukai-slides-claude-code
description: 市政報告会スライドは今後もClaude Code（HTML/CSS→PDF）で制作する。NotebookLM経由ではない。
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cfee5869-8d5a-484d-a622-17fa303f5ad2
---

市政報告会（地区別）のプレゼンスライドは、**今後もClaude Code内で HTML/CSS → PDF で直接制作**する。NotebookLM経由にしない（2026-06-13 草川直接指示「小下と同じ流れ、claudecodeで作成、今後もそうして」）。

**Why:** 御幸（2026-05-30）・小下（2026-05-31）・木下（2026-06-13）はいずれもClaude Code内でslides.html→Chrome印刷PDF化して制作し、草川カラー・写真差し込み・数字グリッド・タイムライン等を自在に組めた。地区固有の数字・写真・出典を1枚ずつ作り込む市政報告会スライドはこの方式が最適。NotebookLM必須ルール（[[feedback-slide-generation-via-notebooklm]]）は議会報告等の汎用スライド向けで、市政報告会スライドはこの例外として扱う。

**How to apply:**
- **2026-07-04移管**: 市政報告会スライドの制作フローは shisei-houkokukai スキル（Stage3）が正。
  本メモの規格（16:9・草川カラー・テンプレ血統・2ゲート）はスキルに継承済み。
  トリガーが来たらまず shisei-houkokukai を起動する。出力先も
  ~/outputs/houkokukai/<日付>_<地区>/03_slides/ に変更（過去デッキは slide-deck-prep/output/ に据え置き・参照専用）。
- トリガー「市政報告会のスライド作って」「〇〇（地区）の市政報告会資料」等が来たら、slide-deck-prep（NotebookLMソース束方式）ではなく、**小下/御幸/木下のslides.htmlをテンプレートに複製→地区化**する。
- 出力先: `~/.claude/skills/slide-deck-prep/output/<YYYY-MM-DD>_<地区>市政報告会/`（slides.html / `<地区>市政報告会_<日付>.pdf` / assets/ / _review/）
- テンプレ規格: 16:9（13.333×7.5in）、草川カラー（--lime:#c7ff4a / --green-deep:#0f3d27 / --green:#1f5a3a / --cream:#f3efe4）、topbar lime帯・cover濃緑左+顔写真右+namechip・foot「草川たくや 市政報告会＠<地区>」。CSSは小下slides.htmlからそのまま流用可。
- 素材: 地区固有写真は当該地区の市政報告レポート印刷物フォルダ（02_publications/reports/）＋過去デッキassetsから sips -Z 1500 で最適化コピー。
- 制作後: PDF化→open でプレビュー→ natural-design-reviewer（PNG化して物理破綻チェック）→ content-fact-checker → content-risk-reviewer（必須2ゲート）。
- 開催情報は🎤市政報告会DB（collection://df08b5ea-f5ff-4022-afe2-c8073fbe341a）の該当ページで日程・会場・配布チラシ・開催地区を確認。
- 既存の良い見本: 木下版 `~/.claude/skills/slide-deck-prep/output/2026-06-13_木下市政報告会/`（20枚・30分枠・太陽光条例議案第36号の審議中ライブ表記を含む）。

関連: [[feedback-slide-generation-via-notebooklm]]（汎用スライド向けNotebookLM必須・本ルールはその市政報告会例外）／[[feedback-print-publication-checklist]]（A4配布印刷物の規範）

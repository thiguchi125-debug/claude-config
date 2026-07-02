---
name: project-gikai-dayori-creator
description: 議会だより一般質問ページ制作の専任エージェント＋恒久スクリプト（2026-07-02整備・R7.6月号で実証済みフローを固定化）
metadata: 
  node_type: memory
  type: project
  originSessionId: 5589a5cc-5506-4328-a83e-eefeb6a9bcd2
---

# gikai-dayori-creator エージェント（2026-07-02整備）

定例会ごとの議会だより一般質問ページ制作をフルパイプライン化。R7.6月号（草津線＋半導体）の実制作フローをそのまま固定。

- **エージェント**: `~/.claude/agents/gikai-dayori-creator.md`（トリガー「議会だより作って」等。新規登録は再起動後有効 [[feedback_agent_registry_partial_load]]）
- **スクリプト**: `~/.claude/scripts/gikai_dayori/`
  - `build_docx.py` — 650字原稿JSON→提出用docx（Yu Gothic bold・問=緑#1F5A3A/答=えんじ#B03A2E）。R7.6提出済docxと書式完全一致を検証済
  - `mark_quotes.py` — 会議録原本に引用元を赤（草川）/青（執行部）でfuzzyマーキング。R7.6成果物とbyte一致を検証済。パラメータ（MIN_BLOCK=4/BRIDGE=5/GREEDY_TH=6/MIN_RUN=5/STRONG=5）は実証値
- **ナレッジ**: `~/.claude/agents/knowledge/gikai_dayori/format_spec.md`（編集要領・650字固定・吹き出しとその他はカウント外）＋ `gold_standard_R7.6.md`（最終文言＋圧縮技法メモ）
- **提出物2点セット**: 提出用docx＋引用参照マークdocx。Desktop出力＋Drive `ZZ_一般質問制作/R0X/YYYY-MM_◯月議会/04完成品/` ミラー
- **要点**: docxの問答テキスト＝マークのred/blue_quotesは同一（1ソース2出力）。draftsのv3 mdより提出docxが真の最終版。

**Why:** 会議録→650字圧縮→docx→引用マークの工程は3か月ごとに繰り返すが、書式・fuzzyマッチのパラメータ再発明はトークンと時間の無駄。実証済み資産に固定した。
**How to apply:** 定例会後「議会だより作って」でエージェント起動。スクリプトは書き直さずJSON configだけ作って呼ぶ。

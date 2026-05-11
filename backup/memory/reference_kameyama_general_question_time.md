---
name: reference-kameyama-general-question-time
description: 亀山市議会の一般質問の標準時間は答弁込み45分。質問原稿・想定答弁・再質問カード生成時の時間配分基準
metadata: 
  node_type: memory
  type: reference
  originSessionId: 40803a50-3cd1-4330-8b55-853bf425e37b
---

# 亀山市議会 一般質問の標準時間

**答弁込み45分**（質問だけで45分ではない）

## どこで効くか
- council-material-creator が本番原稿を作るとき → 草川の発言だけで45分を埋めない。市側答弁の所要時間を差し引いて配分する
- counter-argument-simulator が想定答弁を組むとき → 答弁ターンの時間も含めて45分に収まる構成
- 議会会期ハブDB「質問時間」プロパティのデフォルト = 45（単位: 分・答弁込み）
- 2〜3本のテーマ配分：例えば3本なら1本あたり質問＋答弁で約15分、2本なら1本あたり約22分

## 関連
- [[reference-drive-archive-kusagawa]] — 過去の草川一般質問の所要時間サンプル
- 議会一般質問準備プラットフォーム spec: 2026-05-12-ippan-shitsumon-prep-platform-design.md

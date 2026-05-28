---
name: feedback-kirejiha-individual-nowrap
description: 固有名詞の切れ字対策は個別nowrap限定。汎用word-break:keep-all 等の段組CSS変更は禁止 — 2026選挙リーフレット制作で確立
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4c9cf456-6e5b-4e8c-a8dc-174f77501a83
---

# 切れ字対策は「固有名詞だけ個別 nowrap」

**ルール**: テキストの切れ字（単語が改行で分断される）対策は、**該当の固有名詞だけを `<span style="white-space:nowrap">` で囲む**。`.parent { word-break:keep-all; line-break:strict; overflow-wrap:break-word }` 等の汎用CSS変更は禁止。

**Why**: 2026年5月のリーフレット制作中、私（Claude）が「単語切れ防止」のため `.b-pillar-text` 全体に `word-break:keep-all` を適用した結果、ユーザーから「下手な切れ字対策を元に戻して」「固有名詞の切れ字だけないようにして」と明示的に却下された。汎用ルールを適用すると文章全体の改行が不自然になり、本文のリズムが崩れる。

**How to apply**: 
- 切れ字が発生した時、その**特定の単語だけ** nowrap で囲む
- 親要素のCSSは触らない（letter-spacing / word-break / line-break すべて元のまま）
- 行末位置調整のため、本文末尾フレーズ（例:「鈴鹿亀山道路ＩＣ周辺を大きく変える。」）を nowrap で塊化するのもOK

## 個別nowrap対象の代表例（リーフレットv3で適用済）

| 固有名詞 | 理由 |
|---|---|
| 災害ケアマネジメント | 「災害」と「ケアマネジメント」で改行されないように |
| ８０５０ | 数字単語の途中改行防止 |
| 監督 | 「監」と「督」で改行されないように |
| サーバー | 「AIサ」と「ーバー」で改行されないように（ただし「AI」と「サーバー」の間は改行可） |
| 現・東京都知事 | 「現・」で改行されないように |
| 一般社団法人 亀山青年会議所 監事 | 団体名+役職を一塊で |
| 三重パラ陸上競技協会 理事 | 同上 |
| 鈴鹿亀山道路ＩＣ周辺を大きく変える。 | 文末フレーズ全体を行末に押し込む |

## 注意

- 「AIサーバー」のような複合語は、「AI」と「サーバー」の間で改行を許可（AIのみnowrapしない、サーバーをnowrap）
- 行末収め目的の nowrap が長くなりすぎると、box幅オーバーで全体が次行に押し出される副作用あり → 行末調整は本文短縮 or テキストボックス幅拡大の方が安全

Related: [[feedback-leaflet-design-principles]] [[senkyo-leaflet-v3-2026]]

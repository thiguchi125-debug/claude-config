---
name: feedback_thumbnail_pro_typography_default
description: サムネ・SNS画像・図解は最初からプロ級和文タイポで組む（palt/カギ括弧ぶら下げ/実ウェイトW8-9）。素人っぽさを後から直させない
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f2c02e48-8bda-4c7f-8190-678adb61651a
---

草川のサムネイル・SNS投稿画像・図解PNG等を HTML/CSS→Chrome headless で作るとき、**最初のレンダから**プロ級の和文タイポグラフィで組む。「まず作る→後でプロ級にして」の往復はトークン浪費（2026-07-14 給水スポットサムネで往復発生）。

**Why:** 草川は「レイアウトOK。あとはフォントなどデザインをプロ級にして。**最初からそうして**」と明言。テンプレ/AI感の主因は①約物（「」、。×）の間延び ②締まりの緩さ（line-height過大・不要な影）。これらを最初から潰す。

**How to apply（CSSの既定値として最初から入れる）:**
- フォント: `font-family:"Hiragino Sans","Hiragino Kaku Gothic ProN","YuGothic","Yu Gothic",sans-serif;` ＋ `-webkit-font-smoothing:antialiased`。Hiragino SansはW3〜W9の実ウェイトを持つので font-weight 800→W8 Heavy / 900→W9 Black が合成でなく本物の字面に当たる。
- **約物半角（最重要）**: `.canvas` に `font-feature-settings:"palt" 1;` を全体付与。「」、。× の余分な字間が詰まり「ワンワード」化する。これ一発で和文組版を分かってる印象に跳ねる。
- **カギ括弧の左ぶら下げ**: 見出しに `text-indent:-.5em`（1行目の「だけ版面外へ）。1行目の実字（給）と2行目頭（を）のインク左端が一直線に揃う。レンダ後±0.05em目視調整。
- 見出し line-height: 2行大見出しは **1.16〜1.18**（1.28は緩い）。letter-spacing .03em。
- 氏名（表札）: `font-weight:900; letter-spacing:.10em;` で貫禄。役職はW7・サイズ比2:1。
- × セパレータは語より格下げ: `font-weight:400; font-size:.78em; opacity:.6; margin:0 .3em; vertical-align:.06em`（paltで詰まった分をmarginで復元）。
- 影: ソリッド背景の文字は text-shadow **削除**（濁るだけ）。写真の上に載る文字だけ `0 2px 10px rgba(0,0,0,.55)` 程度で締める。
- 写真＋文字の縦型は、文字帯の下地グラデを `.78`前後まで沈めてライム文字の可読性を確保（緑ポロ×緑パネルは色が繋がり一体感が出る）。

勝負所は [[project_design_studio]] の **design-director** に外科的リファイン指示書（before→afterのCSS値粒度）を出させてから実装すると速い。印刷物は design-studio / [[feedback_design_review_gate_no_skip]] の流れ。制作後は必ずPNGを自分でRead検証（EYES-FIRST）。

正規保存先: `~/outputs/thumbnails/`（[[reference_storage_map.md]] 準拠）。

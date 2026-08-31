---
name: feedback-thumbnail-references-are-political
description: サムネ／OGPの参照は政治家・政党の実物を第1優先で集める。「議員の自作紙面は採用不可」は紙のチラシ限定の規則で、サムネには適用しない
metadata:
  type: feedback
---

サムネイル・OGP（16:9）の参照収集では、**政治家・政党の実物サムネを第1優先**で集める。
報道・出版のプロ面（NHK・日経・東洋経済のOGP／雑誌表紙／新書の帯／広報誌表紙）は、
第1優先で8枚に届かないときの**補充**に回す。

参照ライブラリREADMEの「**議員の自作紙面は採用不可**」は**紙のチラシについての規則**であり、
**サムネには適用しない**。採否は「政治家だから」ではなく「サムネとして強いか」で決める。
落とすのは次の4つだけ ——
級数差が小さく文字が全部同じ大きさに見える／顔写真にテロップを乗せただけで造形が無い／
解像度が低くて採寸できない／明らかに素人（中央揃えだけ・既製テンプレそのまま）。

**Why:** 2026-08-31、サムネ制作で参照ライブラリに16:9の判型が1枚も無く、
印刷物の参照（Warren 2020のムードボード、A4縦のインフォグラフィック）を代用して失敗した。
判型も媒体も違うものを模写したのが原因。草川の指示で収集対象を政治広報物へ切り替えた。

**How to apply:** サムネ／OGP／YouTubeサムネの参照依頼が来たら、
発信力で知られる政党・政治家チャンネル（国内外問わず）を最初に当たる。
YouTubeサムネは `https://i.ytimg.com/vi/<videoId>/maxresdefault.jpg` で 1280×720 が確実に取れる。
videoId は YouTube検索結果ページの `ytInitialData` をパースして集めるのが速い。
収集後は必ず**1枚ずつ自分で Read** してから採否とカルテを書く（接触シートでの一次選別は可）。
成果は `~/.claude/agents/knowledge/design_system/references/thumbnail/` へ。
`design_references/` は廃止予定なので書かない。関連 [[feedback-verify-axis-values-against-real-samples]]

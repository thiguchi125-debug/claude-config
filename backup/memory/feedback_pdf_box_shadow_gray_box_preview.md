---
name: pdf-box-shadow-gray-box-preview
description: Chrome→PDFでぼかし影(box-shadow blur)を付けると、macOSプレビューで写真の周りに灰色/黒の四角が出る
metadata:
  type: feedback
---
印刷物HTMLの写真枠に box-shadow（ぼかし付き・半透明）を付けると、Chromeは半透明画像としてPDFに埋め込み、macOSプレビューでは外側が灰色〜黒の四角に見える。Chrome表示・pdftoppm では再現しないので検品をすり抜ける。

**Why:** 2026-10-07 新聞折込版市政報告で草川「写真の周りの黒い四角はなんとかならないか」。原因は顔写真丸抜きの .face の box-shadow。
**How to apply:** 入稿PDFではぼかし影を使わない（ぼかしのない線・白フチで代替）。PDF検品は pdftoppm だけでなく qlmanage/sips（macOS描画）でも画像化して見る。関連 [[design-reference-library-first]]

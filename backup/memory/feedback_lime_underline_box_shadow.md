---
name: feedback-lime-underline-box-shadow
description: タイトル下線のlimeハイライトは linear-gradient ではなく box-shadow inset で実装する — Chrome PDF レンダリング暗化問題への確定対応
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4c9cf456-6e5b-4e8c-a8dc-174f77501a83
---

# タイトル下線の lime ハイライトは box-shadow inset で実装

**ルール**: テキスト下線のlimeマーカーは `linear-gradient(transparent X%, #c7ff4a X%)` でなく、`box-shadow:inset 0 -0.28em 0 #c7ff4a; background:none` で実装する。

**Why**: 2026年5月のリーフレットv3制作で発見した Chrome PDF レンダリングの個体差。`linear-gradient` の hard-stop は PDF 化時に **半透明帯として補間され、黒系テキストのアンチエイリアスと混色して暗化（オリーブ系/グレー寄り）する**。ユーザーから「色が黄緑ではない」「明らかにおかしい」と複数回指摘された結果、natural-design-reviewer agent の客観評価で「描画レイヤー固有の問題」と確定。box-shadow inset に置換することで純度100%の lime に戻った。

**How to apply**:
- タイトルや見出しの「文字下端だけ黄緑」マーカー実装はすべて box-shadow inset
- gradient で半透明limeを使う場合（例: Pillar 01 のように軽い装飾） は問題なし — 黒文字直下のハイライトだけが対象
- 数値: `inset 0 -0.28em 0 #c7ff4a` で文字下端28%が lime に塗られる

## CSS テンプレート

```css
.title-with-lime-underline span {
  background: none;
  box-shadow: inset 0 -0.28em 0 #c7ff4a;
  padding: 0 6px;
  -webkit-box-decoration-break: clone;
  box-decoration-break: clone;
}
```

## 注意

- `box-decoration-break: clone` は複数行の見出しで各行に下線が乗るように必須
- `padding: 0 6px` は下線の左右余白
- Pillar 01 (子育て) の半透明 `rgba(199,255,74,.33)` は gradient のままでもOK（薄い装飾なので暗化が目立たない）
- Pillar 03 (希望、緑深背景) の lime ハイライトも gradient のままでOK（背景が暗いので半透明limeはむしろ自然）
- **問題が起きやすいのは「ベージュ背景 + 黒文字 + 純lime hard-stop」の組合せ**（Pillar 02 のケース）

Related: [[feedback-leaflet-design-principles]] [[senkyo-leaflet-v3-2026]]

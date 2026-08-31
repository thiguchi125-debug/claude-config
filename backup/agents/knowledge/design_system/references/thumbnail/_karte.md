# thumbnail 造形カルテ（ブログOGP・サムネ）

> 規格：**1600×900（16:9）が既定**（2026-08-31改訂・`feed-visual-reviewer` A-3）。
> 安全域＝中央800×800。**下端12%に文字を置かない。外周40px相当に主要要素・署名を置かない。**
> 5軸の測り方は `../_types.md` のデジタル列。型は `../_types.md`。

## 恒久の下限（`feed-visual-reviewer` A-1／`feedback_thumbnail_pro_typography_default` 由来）

- メイン1行 **原寸で最低100px**（1600×900では約133px以上を推奨）、副1行 **最低56px**
- 文字ブロックは **4つまで**（ラベル・見出し・副見出し・署名で既に4）
- `font-feature-settings:"palt" 1` 全体付与。ヒラギノW8/W9の実ウェイト。絵文字なし
- 本文級（20px前後）が入った時点でサムネではなく図版 → 本文の図解へ逃がす

## 参照（未収集）

報道・出版のプロ面を収集して thm01〜 として追加する。
現時点の型 v0（T1〜T4）は `a4_report` / `trifold` / `brand_system` の既存参照から抽出したもので、
**元参照の画像を実装前に必ず Read すること**（下表の「元参照」列のパス）。

| 型 | 元参照（実装前にReadする画像） |
|---|---|
| T1 片側フェード | `../trifold/tri12_coldspark_postcard.png` |
| T2 全面ブリード＋暗幕 | `../a4_report/rep09_sakaide_cover.jpg` |
| T3 タイポを絵にする | `../brand_system/brand01_warren2020.jpg` |
| T4 数字1個主役 | `../a4_report/rep10_kazmia_sr_p14.jpg` |

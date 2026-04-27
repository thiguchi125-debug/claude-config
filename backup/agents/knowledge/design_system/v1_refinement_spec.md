---
name: 亀山建設労働組合 市政報告 v1 → v2 Refinement Spec
description: design-director による v1 のプロ級昇格レビュー。print-designer 向け実装可能な surgical fix list。
type: design-spec
target_file: /Users/kusakawatakuya/Desktop/亀山建設労働組合_市政報告_v1/index.html
created: 2026-04-27
reviewer: design-director
---

# 亀山建設労働組合 市政報告 v1 → v2 Refinement Spec

## 0. レビュー対象とゴール

- **対象**: `/Users/kusakawatakuya/Desktop/亀山建設労働組合_市政報告_v1/index.html` (788行) と同名 PDF
- **ブランド**: ネイビー `#102a52` ／ 安全イエロー `#f4b400` ／ 草川緑 `#1f7a3a` ／ ベージュ `#f7f4ec` (原則維持)
- **配布対象**: 亀山建設労働組合 (組合員 = 中堅〜ベテラン建設業従事者)
- **ゴール**: 議会報告物として「議員が制作したっぽさ」を消し、「広告代理店が制作した政治家広報物」に近づける

---

## 1. 総評

| 項目 | 現状スコア | v2目標 |
|---|---|---|
| Overall | **B-** | A- |
| Contrast | B | A |
| Repetition | B+ | A |
| Alignment | B | A |
| Proximity | B+ | A- |
| Balance | C+ | A- |
| Hierarchy | B | A |
| White Space | C | A- |
| Unity | B | A |

**現状の総括**:
v1 は構造は破綻しておらず、配色・要素配置とも十分「ちゃんとしている」段階。ただし以下4点で「議員手作り感」が抜けない：

1. **垂直リズムの不揃い** — front の greeting 下〜front-footer 間に意図不明な空白、back の pillars 上端が詰まりすぎ
2. **KPI と next-card のヒエラルキー衝突** — どちらもネイビー塗り潰しで「同格」に見え、視線の優先順位がない
3. **タイポグラフィの繊細さ不足** — 約物処理 (palt は効いているが、行頭ぶら下がり・字間調整・和欧混植のベースライン) が粗い
4. **写真処理の野暮ったさ** — Hero photo は object-position が顔の上を切っている。プロフィール写真も crop 設定が不十分

v2 で上記4点を潰せば「政治家本人 + 広告制作会社」レベルに到達可能。

---

## 2. 8原則レビュー

### 2.1 CONTRAST (コントラスト) — 現状 B / 目標 A

**現状**:
- Hero statement (28pt/900) と sub (10.5pt/500) の比 ≒ 2.66:1 — 数値的にはOKだが、navy統一色のため明度差が弱く「同じレイヤー」に見える
- KPI .num (24pt safety yellow) と .lab (8pt white) のサイズ比 = 3:1 — OK
- Pillar h3 (11.5pt/800) と pillar p (8.8pt) の比 ≒ 1.3:1 — **弱すぎる**。本文と見出しが同レイヤー化

**問題**:
- Pillar内のヒエラルキーが弱い → 読者が「タイトルに目を留める」体験ができず、4本柱が文字壁に見える

**修正指示** (CSS、index.html):
```css
/* line 337-345 .pillar h3 */
.pillar h3 {
  font-size: 12.5pt;       /* 11.5pt → 12.5pt */
  font-weight: 800;
  color: var(--kk-navy-900);
  line-height: 1.35;       /* 1.4 → 1.35 (タイトル詰め) */
  margin-bottom: 2.5mm;    /* 2mm → 2.5mm */
  letter-spacing: 0.015em; /* 0.02em → 0.015em */
}

/* line 363-368 .pillar p */
.pillar p {
  font-size: 8.5pt;        /* 8.8pt → 8.5pt (本文を一段絞ってh3との差を作る) */
  line-height: 1.75;       /* 1.7 → 1.75 (呼吸) */
  color: var(--kk-text-600); /* 900 → 600 (本文を少しグレーへ) */
  text-align: justify;
}
```

これで h3/p 比 = 12.5/8.5 = **1.47:1** に拡大、かつ本文がグレー化することで navy h3 が「浮き上がる」。

### 2.2 REPETITION (反復) — 現状 B+ / 目標 A

**現状**:
- 黄ライン (1.2mm border-bottom) は masthead と back-head で反復 → 良い
- section-title の `::before` (1.2mm × 5mm 黄縦線) は3箇所で反復 → 良い
- ただし KPI 上端 0.8mm yellow line と pillar 上端 1mm yellow border が**微妙に違う太さ** = 不統一

**修正指示**:
```css
/* line 175-182 .kpi-card::before */
.kpi-card::before {
  height: 1mm;             /* 0.8mm → 1mm (.pillar の border-top と統一) */
}

/* line 327 .pillar */
.pillar {
  border-top: 1mm solid var(--kk-safety-500); /* 既存維持 */
}
```

新しいルール: **「カードの天面アクセント線は 1mm に統一」** をデザインシステム恒久ルールに昇格。

### 2.3 ALIGNMENT (整列) — 現状 B / 目標 A

**現状**:
- `.page` padding: 8mm、各セクションは独自に padding 6mm → **左端が 14mm でほぼ揃っているが、masthead と back-head は padding 6mm で差異**
- KPI band と pillars が同じ 6mm 横padding = 揃っている → 良い
- ただし .greeting (padding 3mm 6mm 5mm 6mm) と .front-footer (padding 3mm 6mm) の縦リズムが揃っていない

**問題**:
- ベースライングリッドが存在しない → 行間が揃わず、横で並べた時に微妙にズレる

**修正指示**:
- 全ブロックを **横方向 padding 6mm に固定**、`.page` padding を `8mm 0` に変更（縦のみ page padding、横はブロック側で吸収）

```css
/* line 30-37 .page */
.page {
  width: 210mm;
  height: 297mm;
  padding: 0;                /* 8mm → 0 (masthead/back-head が full-bleed になる) */
  position: relative;
  overflow: hidden;
  background: #fff;
}
```

注意: これに伴い masthead と back-head が天面 full-bleed (左右端まで navy) になる → **より雑誌的・プロフェッショナル感が出る**。masthead 内の左右 padding は 8mm に増やす:

```css
/* line 43-51 .masthead */
.masthead {
  padding: 4mm 8mm;          /* 6mm → 8mm */
}
/* line 289-297 .back-head */
.back-head {
  padding: 4mm 8mm;          /* 6mm → 8mm */
}
```

### 2.4 PROXIMITY (近接) — 現状 B+ / 目標 A-

**現状**:
- KPI 4枚と greeting の間 (line 645→648) の余白が中途半端 → KPI が greeting の付随物に見えなくもない
- timeline と next-block の間 (line 716→719) がほぼゼロ → 異なる時制 (過去 vs 未来) の境界が弱い

**修正指示**:
```css
/* line 161-166 .kpi-band */
.kpi-band {
  padding: 6mm 6mm 4mm 6mm;  /* 5mm → 6mm 6mm 4mm 6mm (上を厚く、下を薄く=greetingに近づける) */
}

/* line 371-373 .timeline-block */
.timeline-block {
  padding: 0 6mm 4mm 6mm;    /* 2mm → 4mm (next-block と分離) */
}
```

### 2.5 BALANCE (重心) — 現状 C+ / 目標 A-

**現状**:
- Front: footer (緑帯) が左下に重い → 全体重心が左下偏重
- Back: profile-block が下部全幅で navy-100 背景 → これも重く、上部の pillars が軽く見える
- 全体として「下重い／上軽い」配置 = 安定しているが、**プロは意図的に「上重・下軽」にして視線を上から下に流す**ケースが多い

**修正指示**:
- Hero photo の重さを増す → height 95mm → 100mm に拡大、影を強める

```css
/* line 88-94 .hero .photo */
.hero .photo {
  height: 100mm;             /* 95mm → 100mm */
  border-radius: 1.5mm;
  overflow: hidden;
  box-shadow: 0 1.2mm 3.5mm rgba(16, 42, 82, 0.16); /* 0.12 → 0.16 強化 */
}
```

- Hero copy 側も縦中央でなく上揃えに変更し、重心を上に集中:
```css
/* line 111-116 .hero .copy */
.hero .copy {
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* center → flex-start */
  padding-top: 4mm;            /* 新規 */
  padding-left: 2mm;
}
```

### 2.6 HIERARCHY (階層) — 現状 B / 目標 A

**現状**:
- Front: masthead → hero statement → KPI → greeting → footer (5層)、明確
- Back: back-head → 4 pillars → timeline → 3 next-cards → profile → legal (6層) — ややフラット
- 特に KPI と next-card がどちらもネイビー塗りで**同じヒエラルキー**に見える → next-card は下位情報なのに上位と同格で表現してしまっている

**修正指示** (next-card を navy 塗りから「白 + navy 強アクセント」に格下げ):

```css
/* line 416-422 .next-card */
.next-card {
  background: #fff;           /* navy → 白 */
  color: var(--kk-text-900);  /* 白 → 黒系 */
  padding: 4mm 3.5mm;         /* 3.5mm → 4mm 3.5mm */
  border-radius: 1mm;
  position: relative;
  border: 0.4mm solid var(--kk-rule);
  border-left: 1.2mm solid var(--kk-navy-900); /* 左に navy 線 */
}
.next-card .step {
  font-size: 8.5pt;           /* 9pt → 8.5pt */
  font-weight: 800;
  color: var(--kk-navy-900);  /* yellow → navy (KPI yellow との差別化) */
  letter-spacing: 0.12em;
  font-family: "Inter", sans-serif;
  margin-bottom: 1.5mm;
  display: inline-block;
  background: var(--kk-safety-500);
  padding: 0.4mm 1.5mm;
  border-radius: 0.4mm;
}
.next-card h4 {
  font-size: 10pt;
  font-weight: 800;
  line-height: 1.45;
  margin-bottom: 1.5mm;
  color: var(--kk-navy-900);  /* 新規：白→navy */
}
.next-card p {
  font-size: 8pt;
  line-height: 1.65;          /* 1.55 → 1.65 */
  color: var(--kk-text-600);  /* opacity 0.92 → 明示色 */
  opacity: 1;
}
```

これで KPI (navy 塗り = 実績 = 強) と next-card (白 = 未来 = 軽やか) が明確に分離 → **過去⇆未来の時制が視覚化される**。

### 2.7 WHITE SPACE (余白) — 現状 C / 目標 A-

**現状**:
- Front: greeting と front-footer の間に**約12mm の意図不明な空白** (PDF視認) → 「埋め切れなかった感」
- Back: pillars 上端 padding 3mm = 詰まりすぎ。back-head と 4本柱の間で「呼吸」がない

**修正指示**:
```css
/* line 205-207 .greeting */
.greeting {
  padding: 4mm 6mm 12mm 6mm;  /* 3mm 6mm 5mm 6mm → 下を 12mm 確保 (front-footer と物理的距離キープ) */
}

/* line 318-323 .pillars */
.pillars {
  padding: 5mm 6mm 3mm 6mm;   /* 3mm 6mm 2mm 6mm → 上を 5mm に (back-head と4本柱の呼吸) */
}

/* line 408-410 .next-block */
.next-block {
  padding: 0 6mm 4mm 6mm;     /* 2mm → 4mm */
}

/* line 445-447 .profile-block */
.profile-block {
  padding: 2mm 6mm 14mm 6mm;  /* 0 → 2mm (next-block と切り離し) */
}
```

**白を恐れない原則**: 余白は「埋めるもの」でなく「リズム」。詰めるくらいなら、要素を1つ削る。

### 2.8 UNITY (統一) — 現状 B / 目標 A

**現状**:
- フォントは Hiragino Kaku Gothic Pro 一本 → 良い
- ただし数字は Inter (KPI .num, timeline .when, .step, .pageno) と Hiragino混植 → ベースラインがガタつく可能性
- 角丸: 1mm / 1.5mm / 0.4mm (placeholder) / 0.6mm (qr-box border) と**5種類混在** → ノイズ

**修正指示** (角丸統一):
```css
/* 全 border-radius を以下3種に統一 */
/* small: 1mm  - card, badge, label-chip */
/* medium: 1.5mm - hero photo, greeting body */
/* pill: 999px - 使う場合のみ (現状なし) */

/* line 91 .hero .photo */
.hero .photo { border-radius: 1.5mm; } /* 維持 */
/* line 171 .kpi-card */
.kpi-card { border-radius: 1mm; }      /* 1.5mm → 1mm */
/* line 244 .greeting .body */
.greeting .body { border-radius: 1.5mm; } /* 維持 */
/* line 380 .timeline */
.timeline { border-radius: 1mm; }      /* 維持 */
/* line 420 .next-card */
.next-card { border-radius: 1mm; }     /* 維持 */
/* line 455 .profile */
.profile { border-radius: 1.5mm; }     /* 1mm → 1.5mm (greeting と同格カード) */
/* line 460 .profile .ph */
.profile .ph { border-radius: 1mm; }   /* 維持 */
/* line 561 .contact-inline b */
.contact-inline b { border-radius: 0.6mm; } /* 0.4mm → 0.6mm (chip 系統一) */
```

**Inter 数字統一**: Inter は字幅広めなので、和文との混植時に **font-size を 0.95em に縮小** しベースライン揃え:
```css
/* line 188-190 .kpi-card .num */
.kpi-card .num {
  font-family: "Inter", "Helvetica Neue", sans-serif;
  font-size: 26pt;            /* 24pt → 26pt (Inter は和文比やや小さく見える補正) */
  font-feature-settings: "tnum"; /* 等幅数字 */
}
/* line 391-396 .timeline .item .when */
.timeline .item .when {
  font-feature-settings: "tnum";
  font-size: 8.6pt;           /* 8.4pt → 8.6pt */
}
```

---

## 3. タイポグラフィ詳細

### 3.1 フォントスタック整理

```css
:root {
  --font-base: "Hiragino Kaku Gothic Pro", "Yu Gothic", "Meiryo", sans-serif;
  --font-num: "Inter", "Helvetica Neue", sans-serif;
}
html, body {
  font-family: var(--font-base);
  font-feature-settings: "palt", "kern"; /* palt + kern 両方 */
}
```

### 3.2 級数体系 (v2 確定)

| 用途 | サイズ | weight | line-height | letter-spacing |
|---|---|---|---|---|
| Hero statement | 28pt | 900 | 1.32 | 0.01em |
| Pillar h3 | **12.5pt** | 800 | 1.35 | 0.015em |
| Section label | 13pt | 800 | 1.0 | 0.04em |
| KPI .num (Inter) | **26pt** | 900 | 1.1 | -0.01em |
| Body (greeting) | 10pt | 400 | 1.85 | 0 |
| Pillar p | **8.5pt** | 400 | 1.75 | 0 |
| Timeline item | 8.8pt | 400 | 1.55 | 0 |
| Caption | 7.2pt | 700 | 1.4 | 0.04em |

### 3.3 約物・ぶら下がり・字間

```css
/* 全文に適用 */
* {
  font-feature-settings: "palt", "kern";
}
/* 句読点ぶら下がり (CSS では完全制御不可、HTML側で <wbr> や全角スペース調整) */
.pillar p, .greeting .body p, .timeline .item .what, .next-card p {
  hanging-punctuation: allow-end; /* Safari/Chrome対応 */
  word-break: keep-all;            /* 単語途中改行禁止 */
  overflow-wrap: anywhere;         /* ただし収まらない時は許可 */
}
```

### 3.4 和欧混植の補正

`PILLAR 01` `STEP 01` `KAMEYAMA CITY COUNCIL` などの欧文ラベルは **Inter** を明示指定し、letter-spacing を 0.10em〜0.12em で広めに取る:

```css
.hero .photo .badge,
.pillar h3 .pillar-no,
.next-card .step,
.section-title .en,
.back-head .pageno {
  font-family: var(--font-num);
  letter-spacing: 0.12em;
}
```

### 3.5 「全力応援。」の蛍光ペン処理

現状 `linear-gradient(transparent 62%, var(--kk-safety-500) 62%, var(--kk-safety-500) 92%, transparent 92%)` で良好。ただし**句点「。」が黄色帯から外れる**問題あり:

```css
/* line 142-146 .hero .statement em */
.hero .statement em {
  font-style: normal;
  background: linear-gradient(transparent 60%, var(--kk-safety-500) 60%, var(--kk-safety-500) 94%, transparent 94%);
  padding: 0 1mm 0 0.5mm;       /* 右パディングを増やして句点を含める */
  margin-right: -0.5mm;          /* 視覚調整 */
}
```

HTML側修正案:
```html
<!-- line 619 -->
<h1 class="statement">現場で働く人を、<br/><em>全力応援</em>。</h1>
<!-- ↑ 句点を em の外に出す。蛍光ペンは「全力応援」だけ、句点はベース色 -->
```

---

## 4. カラーハーモニー

### 4.1 現行パレット評価

| 色 | HEX | 用途 | 評価 |
|---|---|---|---|
| Navy 900 | `#102a52` | 主要塗り・テキスト | A: 完成度高 |
| Navy 700 | `#1f3f73` | hover・eyebrow | A |
| Navy 100 | `#eef2f8` | 背景グラデ・profile bg | A |
| Safety 500 | `#f4b400` | アクセント線・KPI数字 | A: 建設労組と整合 |
| Safety 100 | `#fff7d6` | strong背景 | B+: やや弱い |
| Green 700 | `#1f7a3a` | 草川緑・left-border | A |
| Gold 600 | `#c89211` | (未使用) | — |
| Paper | `#f7f4ec` | greeting bg | A |
| Rule | `#d4dbe6` | hairline | A |

### 4.2 微調整提案

- **Safety 100 (`#fff7d6`)** はマーカーとして弱い → `#ffeea8` に強化 (彩度を上げて視認性確保)
- **Green 700** は front-footer で全幅使用しているが、面積が広い割にメッセージは1行のみ → footer の色を **Navy 900** に変更し、「Green は強調点 (greeting border-left, pillar 04 border-top) の専用色」に役割固定

```css
/* :root */
--kk-safety-100: #ffeea8;  /* #fff7d6 → #ffeea8 強化 */

/* line 263-273 .front-footer */
.front-footer {
  background: var(--kk-navy-900);  /* green-700 → navy-900 */
  color: #fff;
  padding: 3.5mm 8mm;              /* 6mm → 8mm */
  border-top: 1mm solid var(--kk-safety-500); /* navy footer に黄ライン */
}
.front-footer .lead strong {
  color: var(--kk-safety-500);     /* 強調を黄色で */
}
```

これで色の役割が明確化:
- **Navy** = 構造・権威 (masthead, footer, KPI, profile bg)
- **Yellow** = 注目・強調 (アクセント線、数字、chip)
- **Green** = 草川アイデンティティ (greeting border, pillar 04, signature)
- **Beige** = 読みやすさ (greeting body, timeline bg)

### 4.3 60-30-10 ルールチェック

- Navy 系: ~55% (masthead, footer, KPI×4, profile bg, pillar h3)
- Yellow: ~8% (lines, chips, KPI num, marker)
- Green: ~3% (limited)
- White/Beige: ~34%

**白を呼吸として 30%+ 残しているため健康**。

---

## 5. グリッド／余白／塗り足し

### 5.1 12カラムグリッド整合性

A4 (210mm) から左右 page padding 0、ブロック横padding 8mm を引くと 194mm 利用可能。
ガター 4mm × 11 = 44mm を引いて 150mm をカラムで分割 → 1カラム = 12.5mm。

| ブロック | カラム配分 |
|---|---|
| Hero | 4カラム (photo) + 8カラム (copy) ※実装は 30:70 fr で近似 |
| KPI | 各 3カラム × 4 |
| Pillars | 各 6カラム × 2 行 |
| Timeline | 各 6カラム × 2 行 |
| Next | 各 4カラム × 3 |
| Profile | 2カラム (ph) + 8カラム (info) + 2カラム (qr) |

### 5.2 8mmベースライン

縦は 4mm 刻み (8mm の半グリッド) でアライン。各セクションの padding 上下を **必ず 4 の倍数 mm** に固定:

```
2mm / 4mm / 6mm / 8mm / 12mm / 16mm
```

### 5.3 塗り足し (bleed)

現状 `@page margin: 0` で全幅使えているが、印刷現場 (商業オフセット) で発注する場合は **3mm 塗り足し** が必要。

**v2 改修案 (オプション)**:
```css
@page {
  size: 216mm 303mm;  /* A4 + bleed 3mm × 2 */
  margin: 0;
}
.page {
  width: 216mm;
  height: 303mm;
  padding: 3mm;  /* 内側に bleed 分の余白 → コンテンツは A4 内 */
  position: relative;
  overflow: hidden;
}
.masthead, .back-head, .front-footer, .legal {
  margin: -3mm -3mm 0 -3mm;  /* 天面 full-bleed */
}
```

ただし **家庭用プリンタ印刷を想定するなら現状維持 (210×297mm)** で OK。納品先確認必須。

### 5.4 トリムマーク

Chrome headless ではトリムマーク自動生成不可。発注時は **PDF を Illustrator で開いて手動追加** するのが現実解。design-director 推奨は v1 PDF ベースで Illustrator マーク追加マニュアル化 (別ドキュメント)。

---

## 6. 写真処理

### 6.1 Hero photo (表紙01スーツサムアップ)

**現状**: `object-position: 50% 25%`、height 95mm
**問題**: 顔の上端 (額) が切れている。サムアップしている手も中途半端

**修正指示**:
```css
/* line 88-100 */
.hero .photo {
  height: 100mm;                /* 95mm → 100mm 縦長強化 */
}
.hero .photo img {
  object-position: 50% 32%;     /* 25% → 32% (顔位置を下げる) */
  filter: contrast(1.05) saturate(1.05); /* 微補正 = 印刷時の眠さ対策 */
}
```

写真自体に顔の余白が足りない場合は photo-curator に再クロップ依頼。

### 6.2 KAMEYAMA CITY COUNCIL バッジ

**現状**: 左端に貼り付き、安全イエロー塗り、navy text
**改善**: 左端から **2mm 内側にずらす** とプロっぽい (ベタ付けは素人感):

```css
/* line 101-110 .hero .photo .badge */
.hero .photo .badge {
  position: absolute;
  left: 2mm; top: 4mm;          /* left 0 → 2mm */
  background: var(--kk-safety-500);
  color: var(--kk-navy-900);
  font-size: 7.8pt;             /* 8pt → 7.8pt */
  font-weight: 800;
  padding: 1.2mm 3mm;
  letter-spacing: 0.12em;       /* 0.06em → 0.12em (英字広め) */
  font-family: var(--font-num);
}
```

### 6.3 プロフィール写真 (裏面)

**現状**: `object-position: 50% 30%`、26×32mm
**改善**: 縦長クロップなので顔位置 35% に下げ、白フチを 0.8mm に強化:

```css
/* line 457-471 */
.profile .ph {
  width: 26mm;
  height: 34mm;                 /* 32mm → 34mm */
  border: 0.8mm solid #fff;     /* 0.5mm → 0.8mm (印刷でハッキリ) */
  box-shadow: 0 0.8mm 2mm rgba(16, 42, 82, 0.22); /* 0.5/1.5/0.18 → 強化 */
}
.profile .ph img {
  object-position: 50% 35%;     /* 30% → 35% */
  filter: contrast(1.04) saturate(1.04);
}
```

### 6.4 写真の解像度確認

base64 埋め込み画像は元解像度に依存。**最低 300dpi 相当 (95mm = 約 1122px)** を確保。photo-curator 出力時に確認。

---

## 7. 視線誘導

### 7.1 表面: Z-pattern 推奨 → 現状 ほぼ Z だが弱点あり

**理想の Z-flow**:
```
[masthead 左→右] (1) navi gate
[hero photo 左] (2) → [hero copy 右上 statement] (3)
[KPI 4枚 横一線] (4) F-pattern 左→右
[greeting] (5) 中央読込
[front-footer] (6) CTA
```

**現状問題**: 
- Hero copy が縦中央配置 → statement が photo の中央高さに位置 = 視線が photo top → copy middle へ斜め降下する **「弧」ではなく「鉛直降下」**になる

**修正**: Hero copy を上揃えに (§2.5 で実施済) → photo top と statement top が水平で揃う Z-pattern が完成。

### 7.2 裏面: F-pattern + 縦リズム

**理想の F-flow**:
```
[back-head 左→右] (1) 章タイトル
[pillars 1-2 左→右] (2) 第一読込
[pillars 3-4 左→右] (3) 第二読込
[timeline 左カラム→右カラム] (4)
[next 1-2-3 左→右] (5) F横ライン
[profile 左 photo → 中央 info → 右 QR] (6) Z終結
[legal] (7)
```

**現状問題**:
- pillars 1-2-3-4 は 2x2 で、視線順序が「左上→右上→左下→右下」と Z 字になるが、**pillar 04 の green-top が「最後に置いた強調」**になっており、F-pattern の自然な流れと衝突 (視線は左下→右下と進むが、右下が強調されることで左下の pillar 03 が霞む)

**修正**:
- pillar 04 (green-top) は維持 (草川アイデンティティとして緑差別化は意義あり)
- 代わりに pillar 03 にも軽い視覚アクセントを追加 (左 padding に navy 縦線):

```css
/* 新規追加 */
.pillar:nth-child(3) {
  border-left: 0.4mm solid var(--kk-rule);  /* 既存 */
  /* 何も変えない、シンプル維持 */
}
/* むしろ pillar 04 の green を「最終ピース＝総合」として位置づけ
   → 04 の h3 冒頭に「総合」マーカー追加を HTML 側で検討 */
```

または HTML 側で pillar 順序を意味的に並び替え:
- 01: 建てる人 (基幹)
- 02: インフラ (現実)
- 03: 防災 (守り)
- 04: 次世代投資 (未来) ← green = 未来色として正当化

→ 現状 OK。**「緑は未来」というナラティブ**を front-footer の lead 文言で補強推奨。

### 7.3 黄金螺旋

A4 縦長フォーマットでは黄金螺旋 (1:1.618) を強引に当てはめると不自然。**Z+F の組み合わせで十分**。

---

## 8. 印刷仕上げスペック

### 8.1 CMYK 変換

| RGB HEX | 推定 CMYK | PANTONE 近似 |
|---|---|---|
| `#102a52` Navy | C100 M85 Y30 K40 | PANTONE 281C |
| `#f4b400` Yellow | C0 M30 Y100 K0 | PANTONE 124C |
| `#1f7a3a` Green | C80 M20 Y100 K20 | PANTONE 357C |
| `#f7f4ec` Beige | C2 M3 Y8 K0 | (4色印刷OK) |

**注意**:
- Chrome headless PDF は **RGB 出力のみ**。商業印刷発注時は印刷会社で CMYK 変換 (RIP)。
- 黄色 `#f4b400` は CMYK 変換時にやや沈む → **PANTONE 124C スポット指定**で発色保証推奨 (高コストだが組合配布なら正当化可能)
- ネイビー `#102a52` も4色印刷だと茶色がかる → PANTONE 281C 指定推奨

### 8.2 解像度

- 写真: **300dpi 最低、推奨 350dpi** (印刷物標準)
- ロゴ・QR: SVG 推奨 (現状 QR はモック → 確定 QR を SVG で差し替え)

### 8.3 PDF/X-1a 要件

家庭用 Chrome headless 出力は PDF/X-1a 非準拠。商業印刷発注時:
1. Chrome → 通常 PDF 出力
2. Adobe Acrobat Pro で「PDF/X-1a:2001 として保存」変換
3. プリフライト実行 (RGB残存・低解像度・フォント未埋込チェック)

代替: Illustrator で再保存して PDF/X-1a 化。

### 8.4 入稿チェックリスト

- [ ] 全画像 300dpi 以上
- [ ] フォント全埋め込み (Hiragino, Inter)
- [ ] CMYK 変換済み (or PANTONE 指定)
- [ ] 塗り足し 3mm (オプションで適用時)
- [ ] トンボ追加 (Illustrator)
- [ ] 黒テキストはリッチブラックでなく **K100 単色** (細字滲み防止)
- [ ] 白抜き文字 (KPI lab 等) は **8pt 以上**確保 (現状OK)

---

## 9. print-designer 向け実装チェックリスト

### Priority A (必須・v2 で必ずやる) — **15項目**

1. **[A]** `.page { padding: 0 }` に変更し、masthead/back-head/footer を full-bleed 化 (§2.3)
2. **[A]** `.masthead`, `.back-head` の横padding を 8mm に増加 (§2.3)
3. **[A]** `.pillar h3` を 12.5pt/800/lh1.35 に強化 (§2.1)
4. **[A]** `.pillar p` を 8.5pt/lh1.75/text-600 に変更 (§2.1)
5. **[A]** `.next-card` を navy塗り → 白+navy左線+yellow chipに格下げ、見出し色 navy へ (§2.6)
6. **[A]** `.front-footer` の background を green → navy に変更 + yellow border-top 1mm (§4.2)
7. **[A]** `--kk-safety-100` を `#ffeea8` に強化 (§4.2)
8. **[A]** `.hero .photo` height 100mm + object-position 32% + filter contrast (§2.5, §6.1)
9. **[A]** `.hero .copy` を justify-content: flex-start + padding-top: 4mm (§2.5)
10. **[A]** `.greeting` padding を `4mm 6mm 12mm 6mm` (front-footer と分離) (§2.7)
11. **[A]** `.pillars` padding 上を 5mm に (back-head と呼吸) (§2.7)
12. **[A]** Hero statement HTML 修正：`<em>全力応援</em>。`(句点を em 外) (§3.5)
13. **[A]** 全角丸を 1mm/1.5mm の2種に統一 (kpi-card, profile, contact-inline b) (§2.8)
14. **[A]** `.kpi-card::before` 高さ 0.8mm → 1mm (pillar と統一) (§2.2)
15. **[A]** `.kpi-card .num` を 26pt + Inter + tnum (§2.8)

### Priority B (推奨・余裕があれば) — **10項目**

16. **[B]** `.pillar` padding を 4mm 4mm に増やし呼吸感 (上下バランス調整)
17. **[B]** `.timeline-block` padding-bottom を 4mm に (next-block と分離) (§2.4)
18. **[B]** `.next-block` padding-bottom を 4mm に (§2.7)
19. **[B]** `.profile-block` padding-top を 2mm に (§2.7)
20. **[B]** `.profile .ph` を 26×34mm + border 0.8mm + shadow 強化 (§6.3)
21. **[B]** `.hero .photo .badge` left 0 → 2mm + Inter + letter-spacing 0.12em (§6.2)
22. **[B]** 全 `.section-title .en` `.kpi-card .num` `.next-card .step` `.timeline .when` に `font-family: var(--font-num); font-feature-settings: "tnum"` 統一 (§3.4)
23. **[B]** `body` に `font-feature-settings: "palt", "kern"` 両方指定 (§3.1)
24. **[B]** 全本文ブロックに `word-break: keep-all; overflow-wrap: anywhere; hanging-punctuation: allow-end` (§3.3)
25. **[B]** Inter ウェブフォント読み込み追加 (Google Fonts CDN または local) — 現状 fallback で Helvetica になっている可能性

### Priority C (オプション・将来検討) — **6項目**

26. **[C]** 塗り足し 3mm 対応 (216×303mm キャンバス + .page padding 3mm + masthead/back-head/footer に negative margin) (§5.3)
27. **[C]** PANTONE 281C/124C/357C スポット指定での再入稿準備 (§8.1)
28. **[C]** 確定 QR を SVG で差し替え (現状モック) (§8.2)
29. **[C]** Illustrator でトンボ追加マニュアル化 (§5.4)
30. **[C]** PDF/X-1a 変換手順書 (§8.3)
31. **[C]** Pillar 04 (green) に「総合」マーカーで「未来=緑」ナラティブを補強 (§7.2)

---

## 10. v2 完成後のレビュー再依頼

v2 完成後、以下フォーマットで design-director に再レビュー依頼:
```
/design-director  
v2 完成。
- HTML: {path}
- PDF: {path}
- 適用済み: Priority A 全項目 / B {n}項目 / C {n}項目
変更箇所のスクリーンショット差分とともに 8原則再採点お願いします。
```

target: **Overall A-** 到達。到達後は他組合 (亀山商工会議所、青年会議所等) 向けテンプレ化検討。

---

## Appendix: 確定済みデザイントークン (v2 reference)

```css
:root {
  /* COLOR */
  --kk-navy-900: #102a52;
  --kk-navy-700: #1f3f73;
  --kk-navy-100: #eef2f8;
  --kk-safety-500: #f4b400;
  --kk-safety-100: #ffeea8;   /* v2 強化 */
  --kk-green-700: #1f7a3a;
  --kk-gold-600: #c89211;
  --kk-text-900: #11151c;
  --kk-text-600: #4a5260;
  --kk-text-400: #8a92a0;
  --kk-paper:    #f7f4ec;
  --kk-rule:     #d4dbe6;

  /* RADIUS */
  --r-sm: 1mm;
  --r-md: 1.5mm;

  /* TYPE */
  --font-base: "Hiragino Kaku Gothic Pro", "Yu Gothic", "Meiryo", sans-serif;
  --font-num:  "Inter", "Helvetica Neue", sans-serif;
}
```

— end of spec —

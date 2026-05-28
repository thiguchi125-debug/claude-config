---
name: feedback-leaflet-design-principles
description: 後援会用リーフレット制作の恒久ルール（デザイン哲学・色・写真・公選法・トーン）— 2026選挙リーフレットv3制作から抽出
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4c9cf456-6e5b-4e8c-a8dc-174f77501a83
---

# 後援会リーフレット 恒久デザイン原則

**Why**: 2026選挙リーフレットv3制作（11セッション以上の往復）で累積した、草川さん固有のデザイン感性・政策トーン・印刷物制作ノウハウ。次回類似制作でゼロから議論し直さない。

**How to apply**: 後援会勧誘＋政策周知用印刷物（リーフレット・市政報告書・後援会向けハガキ等）の制作時に、この原則を最初に参照する。

## 1. デザイン哲学

### 客観確認を怠るな
- ユーザーは「客観的に見て」「目視で分からないか」と頻繁に求める
- 自分の主観でCSS設定を信用せず、**preview PNGを Read で確認 or natural-design-reviewer agent で客観評価**
- 「鮮やかな lime にした」と主張しても、PDF上で暗化していたら無価値

### 元デザインの装飾を尊重
- design-tool で草川が iterations した元の装飾（halftone / stripe / tape / sticker / lime影 etc）は**勝手に削除しない**
- レビューエージェントの推奨を反映しすぎると元の魅力が失われる
- ユーザーが「全くダメ、前のバージョンに戻して」と言ったら、レビュー由来の大量変更を一気にrevertする覚悟が必要

### 段組み・大幅レイアウト変更は指示外で禁止
- プロフィール intro に `columns:2` を勝手に追加して怒られた経緯あり
- ユーザー指示は「●ごと改行」だけだったのに、2段組まで盛り込んで「変な変更」と言われる
- **指示の文言通り、最小限の変更**で対応する

## 2. 色設計（恒久統一）

| 用途 | 色 | 備考 |
|---|---|---|
| 純lime | `#c7ff4a` | たくや/CTA/入会スター/FW pin/Pillar 02下線 — 統一必須 |
| 緑 | `#1f5a3a` | QRコード, 緑帯背景, 中型text-shadow |
| 緑深 | `#0f3d27` | Pillar 03 hero背景, 「や」の文字色 |
| paper (ベージュ) | `#f3efe4` | 紙面背景 |
| ink (黒) | `#111418` | 黒帯, 本文 |

**注意**: lime を `linear-gradient(transparent X%, #c7ff4a X%)` のhard-edgeで使うと PDF レンダリングで暗化（オリーブ系）。**下線は `box-shadow:inset 0 -0.28em 0 #c7ff4a`** で実装する。

## 3. 切れ字対策

固有名詞の切れ字だけ `<span style="white-space:nowrap">` で個別対応。汎用 `word-break:keep-all` は禁止（[[feedback-kirejiha-individual-nowrap]]参照）。

代表的nowrap対象:
- 「災害ケアマネジメント」「８０５０」「監督」「サーバー」
- 「現・東京都知事」「一般社団法人 亀山青年会議所 監事」
- 「三重パラ陸上競技協会 理事」「亀山飲食業組合 顧問」「亀山市eスポーツ協会 事務局長」
- 「鈴鹿亀山道路ＩＣ周辺を大きく変える」（行末収め）

## 4. トーン・表現の好み

### NG表現
- 「規制」を前面（→「適正立地」「適正設置」にフレーム転換）
- 「議会全体／同僚議員」を動かす色（対外発信から外す、執行部宛て限定）
- 「次の議会で追及」型の強い対決動詞
- 「最後の100m」距離比喩
- 「届かなくても届く」「届かないを終わらせる」ポエム的フレーズ
- 内部メモ風表示（filename/ファイルサイズ等の演出）

### OK表現
- 「次は亀山だ」（草川キャッチコピー）
- 「あなたの声を、草川たくや と一緒に。」
- 「ええやん 亀山。」（後援会CTA）
- 「コストコ誘致を諦めない」（継続公約）
- 「亀山に、希望の旗を立てる」

### 政策内容のフレーム転換
- 太陽光: 「規制条例」→「適正立地条例」
- 災害関連死: 「TKB48単独」→「個別避難計画100% + 福祉避難所事前指定 + 災害ケアマネジメント（在宅避難者まで見守り）」のセット
- Pillar 03 産業誘致 → スポーツ拠点（オリンピアン・パラリンピアン）を加える

## 5. 公職選挙法対策（必須）

- **「討議資料」表記**: 紙面右上に白枠透過・白文字 font 8px / opacity .85 で小さく
- これにより政治活動用文書扱い、選挙運動期間外でも合法配布可能
- 「投票してください」「もう一度」等の直接的な投票依頼表現は本文に入れない

## 6. 写真の扱い

### サイズ最適化（印刷300dpi想定）
- 表示mm × 11.81px/mm × 2倍 が必要解像度の目安
- 例: 200×124px枠 (53×33mm) → 1500×900px JPEG 90% で十分
- 元4032×3024px のままだと Chrome PDF が非圧縮埋め込みして80MB級になる
- 必ず `sips -s format jpeg -s formatOptions 90 -Z 1500` で事前最適化
- バックアップは `assets/_orig/` に保管

### プライバシー
- 家族写真の子どもの顔は **PIL ImageDraw + ImageFilter.GaussianBlur(radius=18) を楕円マスクで適用**
- 矩形ぼかしは背景に被って不自然 → 楕円マスクで顔の輪郭にフィット
- 草川本人の顔は通常そのまま使用OK

### キャプション
- `.b-photo .mono`: font-size 10.5px / italic / `white-space:nowrap` / `text-overflow:ellipsis`
- 黒タグ（題名）と書体的に区別するため italic 使用
- イタリック太字でない、軽め

## 7. A4印刷規格

- leaflet 本体: 842×1190px、`@page size:A4; margin:0`、`transform:scale(0.9426)` でA4にフィット
- Chrome headless: `--paper-width=8.27 --paper-height=11.69 --no-pdf-header-footer --virtual-time-budget=20000`
- `.page-label-wrap` は overflow:hidden + page-break-after:always
- `.leaflet { overflow:hidden }` で紙面外コンテンツ切除

## 8. レイアウトの構造化（恒久要素）

### 表面（3本構成）
- 上部: ribbon + 番号ブロック + portrait + sticker + slogan
- 中央: 大きな「草川 たくや」（240/200px）
- 下部: contact strip（CTA + 後援会名 + 連絡先 + QR×2）

### 裏面（VISION + 3本柱 + プロフィール + 活動実績）
- 上部: VISION 「亀山のこれからの4年。」+「2030 VISION・までに」
- 3本柱: Policy 01 (flagship 5つのゼロ + 周産期/学校サブセクション) → Pillar 02 (paper bg) → Pillar 03 (green-deep hero bg)
- プロフィール: 家族写真 + 学歴・職歴 1段フラット
- 活動実績: 5枚サムネ + キャプション

## 9. 改行とテキストボックスの哲学

- 4行収めたい本文は `<br>` で改行位置を強制
- text-box幅は grid template の写真カラム幅で調整（gap も使う）
- 「2列に見える」「右が空欄」のクレームは grid columns と max-width のチューニング問題
- 写真サイズ変更時はテキスト box幅 + 縦余白の両方を再計算

## 10. ファイルとアーカイブ

- 印刷物保存先: `~/.claude/agents/knowledge/kusagawa_archive/02_publications/leaflets/<YYYY-MM>_<案件名>/`
- 元画像バックアップ: 同フォルダ内 `assets/_orig/`
- 最適化済み画像: `assets/` または `assets_opt/`
- PDF出力: 同フォルダ直下、ファイル名は日本語OK

Related: [[senkyo-leaflet-v3-2026]] [[feedback-kirejiha-individual-nowrap]]

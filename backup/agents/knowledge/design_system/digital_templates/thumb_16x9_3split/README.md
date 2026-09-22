# ブログサムネ16:9 ひな形（西野公園プール型・3分割）

目標形＝`../../references/thumbnail/model_kusakawa_nishino_pool_2026-09-14.jpg`（2026-09-22 草川「このサムネが成功例」）。
見本を画像から採寸して起こした。見本と同じ文言で作ると、文字の行位置は数px以内・写真の構図も一致する（2026-09-22 検証）。

## 使い方（1コマンド）
```bash
python3 ~/.claude/agents/knowledge/design_system/digital_templates/thumb_16x9_3split/make_thumb.py \
  --place 西野公園プール --line1 小学生は全員 --key 付き添い --ask 線引きの見直しを \
  --site <テーマの現場写真.jpg> --out ~/outputs/thumbnails/<日付>_<テーマ>/
```
- 出力：`thumb_1600x900.html`／`.png`（写真は出力先 `assets/` にコピー）
- **4つの文言**：`--place` 場所ラベル／`--line1` 白の1行（状況）／`--key` 黄の核心語（6字以内・超えると止まる）／`--ask` 白カードの要望（「〇〇を」型）
- 級数は字数から自動（上限＝見本の採寸値：1行目84px・核心語126px・要望56px）
- 現場写真の寄せ方：既定は cover。看板などに寄るときは `--site-size 1410px --site-pos "-604px -228px"`（見本の値）のように指定
- 本人写真：既定＝`assets/me_hero_yukei_full.jpg`（写真ストック「2026-06-29_白シャツ夕景_ヒーロー向き最良」）を幅510px・x940・y-8。**草川の指定がない限り変えない**

## 注意
- 現場写真が無いテーマは、このひな形を使わずに周産期通院支援の2分割（`~/outputs/thumbnails/2026-09-04_周産期通院支援/eyecatch_1600x900.html`）で作る
- 作った後は PNG を自分で見る → `feed_preview.py still <png>` → feed-visual-reviewer
- `assets/sample_site_nishino_pool.jpg` は動作確認用の見本写真

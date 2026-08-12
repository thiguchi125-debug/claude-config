# A1ポスタースターター

- 入稿サイズ：600×847mm（A1仕上がり594×841mm＋四方3mm塗り足し）
- 文字安全域：仕上がり線から内側24mm以上
- 写真：`.photo`を`<img>`に置換し、`object-fit:cover`と`object-position`を目視調整する
- QR：実寸80mm以上を推奨。差し替え後は`design-render --qr`で読み取り確認する
- 名前・肩書・討議資料表記は案件に応じてcontent-fact-checkerとcontent-risk-reviewerを通す

```bash
~/.agents/bin/design-render \
  --html ~/.agents/knowledge/design_system/templates/poster_a1/template.html \
  --output-dir ./render-a1 \
  --profile a1-bleed3
```

# イベントチラシ A4 テンプレート

## 用途
地域イベント・サークル活動・協会行事の告知チラシ（1枚もの・片面）。SNS画像兼用の縦長比率で制作し、A4印刷にも流用する運用。

## 正本
- `template.html` = `drafts/2026-06_esports_smash/flyer_a2.html` のverbatimコピー（4案比較の最終採用版）
- 選定理由: 公式TUIRTLEロゴ使用（feedback_esports_association_logo 準拠）／ピルバッジ不使用（flyer.html の丸バッジはAI-LP信号のため不採用）／最終PDF・PNGまで完成処理済み
- 画像参照: `logo_t.png`・`form_qr.png` は元ディレクトリ `~/.claude/projects/-Users-kusakawatakuya/drafts/2026-06_esports_smash/` に相対参照。単体レンダリング時は同階層に画像を置くこと

## サイズ・dpi
- ステージ実寸 1080×1350px（4:5。Instagram兼用比率）
- A4印刷時はChrome印刷スケール調整 or `@page` 追記。掲示前提なら文字サイズは現行値以上を維持
- 埋込画像は `sips -Z 1500 -s formatOptions 90` で最適化

## 配色（ダーク系イベント用）
- ベース: #0d0f13〜#1b1f27（ラジアル）／文字: #f4f5f2・#cfd6df
- ライム #c7ff4a は**淡い発光**（gradientテキスト・細罫線・タグ地）で使う。ベタ塗り大面積は不可
- 補助アクセント: シアン #3df0ff／ピンク #ff4d8d（タグ3色・下線）
- 明るい紙もの（自治会向け等）に流用する場合は配色基調を作り替える（特定スタイルの標準化はしない）

## フォント
Noto Sans JP（本文）／Anton（数字・英字ヒーロー）／Space Grotesk（英字ラベル）— Google Fonts @import。オフライン生成時はローカルフォントにフォールバックすることをレンダリングで確認。

## 差し替えポイント
- `.head .org`（キッカー）／`.en`（英字ヒーロー）／`.jp`（和文タイトル・下線位置）／`.lead`
- `.meta`（日付・曜日・時刻・会場・住所）
- `.tags` 3枚（特徴タグ）／`.strip`（料金・対象・定員・持ち物）
- `.foot`（QR画像・申込導線・主催表記）／`.note`（商標・但し書き）
- 主催ロゴ `.logo`（団体公式ロゴの正本を使用。手描き再現・代替イラスト禁止）

## PNG/PDF生成
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --window-size=1080,1350 --force-device-scale-factor=2 \
  --screenshot=/絶対パス/flyer.png /絶対パス/flyer.html
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=/絶対パス/flyer.pdf /絶対パス/flyer.html
open /絶対パス/flyer.pdf
```

## 注意
- 主催表記は正確に（「主催：亀山市eスポーツ協会」等。個人主催と誤認させない）
- 商標を使うイベント（ゲーム大会等）は権利表記を `.note` に必ず入れる
- 配布物のため content-fact-checker → content-risk-reviewer 通過必須／絵文字なし
- バイナリ素材は案件別サブフォルダ `<YYYY-MM>_<案件名>/` に隔離

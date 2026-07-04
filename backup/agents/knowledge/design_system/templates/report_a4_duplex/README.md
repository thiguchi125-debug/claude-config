# 市政報告レポート A4両面（地区版）テンプレート

## 用途
自治会単位で配布する「【〇〇版】市政報告レポート」。A4両面・**家庭用プリンタ印刷前提**（インク節約設計：ベタ塗り総面積3%以下・白背景＋細罫線・強調は太字＋金下線）。

**流用禁止**: 全域版レポート／リーフレット／名刺／選挙公報（別レイアウト）。

## 正本
- `template.html` = `print_templates/district_report/v22_kinoshita_final.html` のverbatimコピー（木下版v22・2026-05-13完全確定。画像はbase64埋込のためファイル単体で完結）
- 目視リファレンスPDF: `~/.claude/agents/knowledge/print_templates/district_report/v22_kinoshita_final.pdf`
- 詳細仕様・実測値・地区別章2マッピング: 同ディレクトリの `README.md`

## 紙サイズ・dpi
- A4 portrait 210×297mm、`@page{size:A4 portrait;margin:0}`、`.page` padding 14mm 12mm
- 写真は300dpi目安（`sips -Z 1500 -s formatOptions 90` で最適化してから埋込）
- 上下余白は実測14mm均一（差2mm以内が合格ライン）

## 配色
インク節約パレット：緑 #1f7a3a（枠線）／深緑 #0e4d27（見出し文字）／金 #c89211（下線・帯・バッジ）。ブランド4色（ライム系）は**この様式では使わない**。

## 差し替えポイント
| 箇所 | セレクタ | 内容 |
|---|---|---|
| 地区バッジ | `.header-sub .district` | 「木下版」→対象地区名 |
| 発行日 | `.header-date` | 発行日 |
| プロフィール写真 | `.profile-photo` | base64（丸型38mm・object-position調整） |
| リード | `.lead` | 地区プロローグ（人口・特性は一次資料照合必須） |
| 章1 | `.chapter-head`＋`.img-frame` | 地区共通テーマ（公共交通等）＋写真70×60mm |
| 章2 | `.ch2-row` | 地区固有テーマ＋写真90×56mm＋2×2数字セル |
| 章3 | `.measure-list` | 市全体テーマ4本柱（基本固定） |
| QR3枠 | `.contact-qrs` | 公式LINE／ご意見箱／公式HP |

## PDF生成
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=/絶対パス/report.pdf /絶対パス/report.html
open /絶対パス/report.pdf
```

## 注意
- **数字は必ず一次資料照合**（content-fact-checker通過必須。「827人減」型の出典不明数字事故の再発防止）
- 配布前に content-risk-reviewer 通過（対外配布物・回収不能）
- 他議員氏名は載せない／絵文字なし
- 完成品はDrive `ZZ_市政報告レポート/` へ

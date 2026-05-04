# Google Drive 取り込みレポート

**実施日**: 2026-05-04
**Drive ルート**: https://drive.google.com/drive/folders/1ZEIt8Cq71oYzJ2sJslxuBNI9GlESHYsg
**ローカル取り込み元**: `~/.claude/agents/knowledge/kusagawa_archive/99_raw/_drive_originals/`

## 取り込み結果サマリ

| 種別 | 投入元 | 変換成功 | 草川パート抽出 | 統合先 |
|---|---|---|---|---|
| 議事録（本会議PDF） | 29件 | 29 | 25件（4件は草川未発言回） | `transcripts/google_drive_kaigiroku/` |
| 議事録（R8 docx） | 1件 | 1 | 1件 | 同上 |
| 議事録（R8 委員会txt） | 2件 | 2（UTF-16→8変換） | 2件（うち1件は薄抽出） | 同上 |
| 市政報告レポート（PDF） | 43件 | 42（OCR要1件） | 全文保存 | `canva/google_drive_reports/` |
| 一般質問資料zip | 1件（画像4枚） | OCR保留 | — | `googledrive/reports/_zip_extracted/` |

**草川パート抽出結果**: 28件・**2.2MB**（元PDF 33MBから1/15に圧縮）
**市政報告レポート全文**: 42件・**360KB**

## 抽出ルール

### 本会議議事録（`_extract_kusagawa.py`）
- マーカー: `○{役職}（{氏名}君[登壇]）` 形式
- 「N番（草川卓也君...）」検出 → 草川パートON
- 別議員「N番（他氏君）」検出 → OFF
- ON状態中の議長進行・市長/副市長/教育長/各部長等の答弁を含めて出力

### 委員会議事録（`_extract_committee.py`）
- 単独行「○○委員。」「○○議員。」「○○課長。」を発言者切替マーカーとして検出
- 「草川拓也議員。」「草川委員。」でON、別議員/委員でOFF
- ノイズ除外: 「子供政策課長草川」（同姓の市職員）、「草川美幸」（人権擁護委員候補）

## 草川未発言回（抽出0件＝正常）
- R0512（2023-12）/ R0603（2024-3）/ R0606（2024-6）/ R0609（2024-9）
- 本会議議事録内に草川の発言なし。会派ローテーション or 質問順番外

## 既知の制約

| 項目 | 状況 | 対応 |
|---|---|---|
| R8.3.18決算委員会 | 草川指名直後の音声起こし誤認識（「長谷川委員」と誤判定）でセッション本体を取り損ね | スクリプト改修要 or 手動追記 |
| 市政レポート51.pdf | テキスト抽出空＝画像PDF | tesseract導入後OCR |
| 草川一般質問資料.zip | PNG 4枚（議場配布資料スライド） | tesseract導入後OCR |
| Google Docs（gdoc） | Drive上に複数（御幸/小下/田村中部/号外多数）あり | ローカル未取込・MCP個別取得が必要 |

## 統合構造

```
~/.claude/agents/knowledge/kusagawa_archive/
├── transcripts/                                    既存45件 + ↓
│   └── google_drive_kaigiroku/                     新規28件（H30〜R08、命名: 年月_セッション_種別_kusagawa.txt）
├── canva/                                           既存107件 + ↓
│   └── google_drive_reports/                       新規42件（市政報告レポート38〜62号 + 地区版）
└── googledrive/                                     原本＋中間テキスト＋抽出スクリプト
    ├── transcripts/
    │   ├── *.pdf / *.docx / *.txt                 原本28+1+2件
    │   ├── _text/                                   pdftotext直出力（中間）
    │   ├── _kusagawa_only/                         草川パート抽出（中間）
    │   ├── _needs_ocr/                              OCR要（現状0件）
    │   ├── _extract_kusagawa.py                    本会議用抽出
    │   └── _extract_committee.py                   委員会用抽出
    └── reports/
        ├── *.pdf                                    原本43件 + zip 1件
        ├── _text/                                   pdftotext直出力
        ├── _needs_ocr/                              OCR要1件
        └── _zip_extracted/                          zip展開（PNG4枚）
```

## 議事録参照ルール（必須）

`feedback_giji_kusagawa_response_only.md` 準拠：
- **草川議員の発言**と**亀山市側答弁**（市長／副市長／教育長／各部長等）の**ペアだけ**を扱う
- 他議員（豊田／伊藤／前田／福沢ほか）の質疑ブロックは読み飛ばす
- 比較材料として他議員質問への市答弁を引きたい場合は明示必須

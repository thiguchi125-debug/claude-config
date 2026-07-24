---
name: project_shisei_report_kawaicho_complete_form
description: 市政報告レポート川合町版が「かめおか文法」チラシデザインの完成形。ネットプリント可・家庭用はインク節約版
metadata: 
  node_type: memory
  type: project
  originSessionId: 4c9fb8c3-5796-4437-9720-ccf29ae20913
  modified: 2026-07-24T06:33:45.268Z
---

2026-07-18 完成。川合町版 市政報告レポート（A4両面）が、[[project_design_studio]] の `report_kameoka` テンプレ（広報かめおか文法）を使った**市政報告チラシデザインの一つの完成形**と草川本人が承認。「ネットプリントで印刷する場合はこのデザインでOK」。

**成果物**: `~/outputs/houkokukai/2026-08-02_川合町/02_report/`（kawai_omote/ura.html→build.py→PDF）。8/2川合町報告会の事前配布・ポスティング一本化・配布期限7/20。

**勝ちパターンの要素（次回の地区版で踏襲）**:
- 表最上部に**草川本人の実筆跡**の手書き挨拶（`handwrite_note.png`＝城東/安知本版と共通。mix-blend-mode:multiply・rotate(-1deg)）。design_specの「手書きは表1点のみ」枠をこれに充てる（ヒーロー上のブラシ体キャッチは置かない）。
- ヒーロー横に**報告会告知ブロック**（金ウォッシュ地・囲み罫なし・日時会場を大きく）。公選法上は「政治活動の集会告知」で問題なし（投票依頼・約束語ゼロが条件）。
- 主役記事は**草川本人の議会質問＋市答弁**を芯に。写真は現場実写（冠水写真・位置関係図）が入ると説得力が段違い。
- 数字レール（大数字＋和文単位）／裏の円形ヌメラル1点（草川が引き出した明言＝12月末めど 等）／縦組み編集後記1点。
- **AIインタビューQR**: フッターに市政全般（`kameyama_shisei_zenpan`）、テーマ別カードに特化版（部活＝`kameyama_bukatsu`）。URL＝`https://depth-interview-kusagawa.vercel.app/interview/<config_id>`。QR検証は必ず**pyzbar**（cv2.QRCodeDetectorはLINEスタイルQRや高密度QRを誤って「読めない」と判定する）。

**恒久の教訓**:
- 却下理由5点（箱囲み/ベタ帯/単一ゴシック/均等グリッド/純白中央寄せ）を踏まない。分節は余白・淡ウォッシュ・ヘアライン・明朝見出しの4手段のみ。
- ページは216×303mm固定＋overflow:hidden。`scrollHeight`は縦あふれ検知に使えない→「最下段コンテンツ下端 vs フッター上端」の衝突量をJSプローブで実測（`_collide_omote.py`）。
- Googleマップを配布物に使うなら**正式クレジット「地図データ ©YYYY Google, ZENRIN」を可視で残す**（「※Googleマップを引用」の言い換えは規約不足）。選挙前の全戸配布ではグレーなので本人判断を仰ぐ。
- 家庭用プリンタで刷る回は**インク節約版**（背景白＋大面積の濃色ベタを削減）を別途用意する。詳細は[[feedback_home_printer_ink_saving_variant]]。
- ドキュメント正本: skill=design-studio／agent=kameoka-grammar-shisei-report／テンプレ=`design_system/templates/report_kameoka/design_spec.md`。
- **裏面プロフィールの正本は安知本版のフル版**（2026-07-24草川指示・和田町版で修正）: 「…衆議院議員 小池百合子（現・東京都知事）秘書を経て2018年初当選。亀山市消防団第３分団員・亀山飲食業組合顧問・亀山市eスポーツ協会事務局長。」まで含める。川合版の短縮プロフィール（秘書名・現役職なし）を次回地区版にコピーしない。手書き挨拶は幅90mm（64mmは小さいと指摘あり）。

---
name: design-quality-bar-natsumatsuri2026
description: 中庄夏祭りポスター2026が全デザイン制作物の品質基準ライン。これ未満のクオリティで納品しない
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f8c7d014-035b-4a70-8c62-7531f783781e
---

草川承認の品質基準（2026-07-02確定）: **「中庄夏祭り2026」ポスターのクオリティが、今後のあらゆるデザイン制作物（チラシ・ポスター・印刷物・スライド・画像）の最低ライン。**

見本の実物: `~/.claude/projects/-Users-kusakawatakuya/drafts/2026-08_中庄夏祭りポスター/`（poster.html＋assets＋完成PDF＋参照素材）

**Why:** 草川が「今後もあらゆるデザインはこれくらいのクオリティ以上を期待したい」と明言。このポスターはプロのテンプレート（Canva参照）と見分けがつかない水準まで詰めた。

**How to apply:**
- **参照画像がある場合はピクセル単位で忠実再現**: 参照をground truthとし、グリッド付き拡大比較・XOR差分可視化で位置・形状を数値検証。ズレや欠けは参照からマスク移植で復元（目分量で描き直さない）
- **文字・数字は1グリフ単位で検品**: AI生成/透かし除去由来の字形崩れ（祭の破片・6が8に化ける等）は拡大して1文字ずつ確認
- **レイヤー順の自然さ**: 装飾線・ガーランド等が文字に被らない（文字は装飾より上）
- **EYES-FIRSTループ必須**: render→実PNGをReadで開いて目視→修正、をズレゼロまで反復（コードを信じない）feedback_print_layout_architect_agent [[skills/chiku-report/references/print_checklist.md]]
- **完成処理まで含めて品質**: わかりやすい日本語ファイル名で納品・旧版/中間生成物は削除・編集可能な一式（HTML+assets）をdrafts/に恒久保存・PDFはopenで即表示 feedback_auto_open_pdf_after_render
- 構図・配色・密度はプロのテンプレート水準を基準に（安っぽいAI風=のっぺり単色・記号的図形・不揃い余白を出荷しない）[[feedback_flyer_avoid_ai_saas_aesthetic]]

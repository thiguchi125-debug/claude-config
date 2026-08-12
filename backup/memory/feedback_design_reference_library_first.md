---
name: feedback-design-reference-library-first
description: 印刷物は templates/ でなく references/ から入る。破綻ゼロは合格ではなく、参照との造形5軸一致度で採点する
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2c42d7c8-a508-4a28-b2ac-74f05c7fb4bb
  modified: 2026-08-12T02:11:54.681Z
---

印刷物制作は `design_system/templates/` からでなく **`design_system/references/`（参照ライブラリ）から入る**。
参照を1本選び、**画像を自分でReadし**、造形カルテの5軸（①級数ジャンプ率 ②色数と役割 ③図形語彙
④写真・図版占有率 ⑤イラスト量）を**数値のまま実装者へ渡す**。完成後は参照画像と出力PNGを並べて採点し、
**5軸中4軸で「可」以上**が合格。参照は案件フォルダに置き去りにせず毎回ライブラリへ回収する。

**Why:** 2026-08 市政報告レポート三つ折りで、参照11枚を集めながら一枚も模写せず、ベタ帯＋水平罫線だけ・
写真は素材8枚中2枚しか使わない紙面を出した。原因は「破綻ゼロ＝合格」で通る構造にあった
（natural-design-reviewer は物理破綻の検出役で、造形の弱さは検出項目に無い）。
またCSSで崩れにくい矩形の帯・等幅カラムへ逃げる癖があり、斜め・円形マスク・重ね・ピルを無意識に避ける。
造形をゼロから発明する能力に期待するのが誤りで、プロの参照から借りる工程に切り替えた。

**How to apply:** 索引＝`design_system/references/_INDEX.md`、採点表と質ゲート＝同 `README.md`、
判型別カルテ＝同 `<判型>/_karte.md`。実装の入口は design-studio Step1／Step3、採点は Step 4-B、
回収は Step 7-0。地区版レポートは chiku-report G5（参照の受け渡し）と G6.5（模写採点）。
参照の質ゲート＝プロ制作物のみ。議員の自作紙面・Wordっぽい紙面・スキャン原稿の寄せ集めは
`_format_only/` へ（様式の確認だけに使う）。空白＝ポスターとA4両面レポートの参照が未収集。
関連 [[project_design_studio]] [[feedback_open_folder_after_generating_files]]

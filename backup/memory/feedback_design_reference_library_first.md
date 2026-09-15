---
name: feedback-design-reference-library-first
description: 印刷物は templates/ でなく references/ から入る。破綻ゼロは合格ではなく、参照との造形5軸一致度で採点する
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2c42d7c8-a508-4a28-b2ac-74f05c7fb4bb
  modified: 2026-09-15T02:01:16.081Z
---

**2026-09-15 草川指示で適用範囲を「ビジュアル制作物すべて」に拡大**：「デザインの改善は今後も全てに応用して反映すること」。
三寺町版レポート（参照＝a4_report/rep10・5軸目標を数値で渡す→G6.5採点）で紙面が急に良くなったのを受けた指示。
対象＝印刷物に限らず、報告会スライド・サムネ・SNS投稿画像・ショート動画の挿入画像・議会資料の図解・AIくさかわ等。
判型に参照が無ければ、作る前に「参照なしで作る」と明示し、design-inspiration-researcher で1本足してから入る。
**反映済み（2026-09-15）**＝shisei-houkokukai Stage3（参照と5軸目標＋品質ループ3模写採点）／short-video-image-designer（参照1本＋5軸目標・制作ループ7）／
photo-post（Step4 4-R＋4-S-5模写採点）。3経路とも16:9スライド・9:16・1:1の参照は未整備→各定義に未整備時の手順を明記。
参照起点＋5軸採点が**定義に入っていない経路（残り）**＝short-video-create／council-material-creator／ai-kusakawa／print-designer。定義への反映が済むまでは、
これらを起動するときに依頼文へ「参照1本＋5軸目標値＋完成後の採点」を本体が書き足す。

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

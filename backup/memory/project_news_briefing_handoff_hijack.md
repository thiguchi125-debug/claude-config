---
name: project_news_briefing_handoff_hijack
description: 朝6:05ニュース便が引き継ぎメモ注入で乗っ取られ収集ゼロ→2026-09-30修理（KUGIRI_NO_HANDOFF）
metadata:
  type: project
---
2026-09-30修理。9/25・26・29・30の朝、launchdの `claude -p`（news_briefing.sh）に SessionStartフック handoff_notice.py が /kugiri の引き継ぎメモを注入し、Claudeが引き継ぎへの返事だけ書いて rc=0 で終了→「ok」扱い・収集ゼロだった。完了通知もlaunchdのロケール未設定で `tr` が日本語を壊し、Discord通知が9/2x以降毎日UnicodeEncodeErrorで落ちていた。

修理: ①handoff_notice.py は `KUGIRI_NO_HANDOFF=1` なら何も出さない ②news_briefing.sh がそれと LANG=ja_JP.UTF-8 をexport ③最終行に「news-briefing v4-local 完了」が無ければ失敗扱いで再試行 ④件数抽出を完了行から取る。バックアップ `*.bak-20260930`。

**Why:** 終了コードだけで成否を見ると「別の話をして終わった」を検出できない。
**How to apply:** 他の claude -p 自動ジョブ（sns_leg / nightly_intake / oyasumi / gyakusan / form_intake）も同じ注入を受けうる。未対応＝各shに `export KUGIRI_NO_HANDOFF=1` を足すかは草川判断。関連 [[project_news_briefing_system]] [[project_kugiri_shuryo_mode]]

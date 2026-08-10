---
name: feedback_check_artifacts_before_scheduling_work
description: 制作物の作業枠を置く前に成果物の実物があるか確認する。_status.jsonの締め漏れで完成済みのレポートに3時間の枠を積んだ
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0a71a97e-35e5-44b7-a5fc-99dec9493ff9
  modified: 2026-08-10T15:11:54.896Z
---

2026-08-10のタスク棚卸しで、北東版 案内レポートの制作に**3時間分の作業枠（8/13×2・8/14×1）を積んでいた**が、
草川から「レポートはすでに完成済み」。実際に見ると前日17:50に v7 が出来ていた。

```
~/outputs/houkokukai/2026-09-12_北東地区/02_report/
  市政報告_北東地区版_2026-09_v7.pdf        10.9MB
  市政報告_北東地区版_2026-09_v7_家庭用.pdf   8.8MB
```

**Why:** `_status.json` の stage2 が `"doing"` のまま、`completed_at` も空だった。
Todoist側のタスクも未完了で残っていた。**成果物は出来ているのに、締めの更新だけが漏れていた。**
その結果、棚卸しは「未完了タスク」として読み、実在しない仕事に枠を割り当てた。
[[feedback_system_closing_loops_rot]]（自動トリガー有=生／記憶依存の締め=腐る）の典型例。

**How to apply**
- 制作物（レポート・チラシ・スライド・原稿）に作業枠を置く前に、**必ず出力先を見る**。
  `~/outputs/houkokukai/<日付>_<地区>/02_report/`、`~/publications/<案件>/`、Drive `ZZ_市政報告レポート/`。
- `_status.json` がある案件は status だけを信じない。ファイルの実物とタイムスタンプを見る。
- 逆に、成果物を作り終えたらその場で `_status.json` と Todoist を閉じる。
  閉じ忘れは「まだやることがある」という誤情報になって後の計画を狂わせる。

**この確認で消えた枠:** 3時間（8/13が5.5h→3.5h、8/14が5.0h→4.0h）。
容量が足りない足りないと配置を組み替えていたが、実際には**やる必要のない仕事を数えていた**。

関連 [[project_task_window_labels]] [[feedback_fixed_weekly_blocks_dont_hold]] [[project_shisei_houkokukai_skill]]

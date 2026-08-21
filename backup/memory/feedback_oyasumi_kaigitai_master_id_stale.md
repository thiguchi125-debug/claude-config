---
name: feedback-oyasumi-kaigitai-master-id-stale
description: oyasumi SKILL.md が持つ会議体マスタDBのdata_source ID 46414643- は存在せず、AIミーティングの会議体マッチングが実行できない
metadata:
  type: feedback
---

oyasumi SKILL.md Step 4.5-4 が指定する 🏛会議体マスタDB の data_source `collection://46414643-0e8f-4ec2-9f5a-1e5e6d3d1b16` は Notion 側で **Data source not found**。そのため確度0.8以上マッチの自動紐付けが一切走らず、転記した会議は全件「会議体 未紐付け」になる。

**Why:** 2026-08-21 の夜間runで実測。skillの表に書かれたIDは頭8桁だけ正しく、残りを推測で補った形跡がある（本文の他DBは完全なUUIDで書かれている）。未紐付けのまま毎晩積み上がると、朝の手動紐付けが溜まる。

**How to apply:** 会議体マッチングを直すときは、まず 🗂️会議ハブ（`a247fd5d56da4acdb9db3ad97cec6a12`）から会議体マスタDBを辿って正しい data_source URL を取り、SKILL.md の Step 4.5-4 と「DB / ページ ID 一覧」の両方を更新する。それまで oyasumi は会議体を空で保存し、サマリに未紐付け件数を出すのが正しい振る舞い。

関連＝[[feedback-oyasumi-blocked-by-content-gate]]

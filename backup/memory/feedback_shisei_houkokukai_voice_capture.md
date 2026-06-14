---
name: feedback_shisei_houkokukai_voice_capture
description: 市政報告会で出た住民の声を自動記録する締め工程（記録トリガー→🎤報告会DB主な意見欄＋Todoist地区フォロー箱）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: db89e985-42f1-43bf-87c3-952f2cc20543
---

# 市政報告会の声の自動記録（2026-06-14実装）

**Why:** 市政報告会（御幸5/30・木下6/13等）で住民から出た声が、開催後どこにも記録されず「行方不明」になる事故が頻発。原因＝🎤市政報告会DB(`df08b5ea-f5ff-4022-afe2-c8073fbe341a`)の「主な意見・要望」欄は**手動記入の締め工程**で、ほぼ全ページ空欄のまま。声が記録される時も iken/nichijo が一般質問ネタDB・市民意見DBに散逸させるだけで報告会単位に戻らず、報告会DBを見ると「空欄＝消えた」ように見える。[[feedback_system_closing_loops_rot]]「自動トリガーのない手動の締め工程は腐る」の典型。2026-06-14に御幸/木下/小下の声を草川の口頭記憶から復元して登録した際に判明。

**How to apply（トリガー＝「記録：〇〇報告会で△△の声」「〇〇市政報告会の記録」＋声）:**
1. 地区／会場名から🎤市政報告会DBの該当ページ特定（notion-search・無ければ新規作成）。
2. **そのページの「主な意見・要望」プロパティに声を追記**（notion-update-page update_properties・既存保持・`【YYYY-MM-DD開催・当日の声】…`形式）＋「議会で取り上げる課題」更新＋進捗ステータス=進行中。
3. 対応すべき声を **Todoist「〇〇地区 フォロー」箱**（🏛議員活動配下・無ければ新設）へ `td.py add`。具体アクション（「まず〇〇に連絡」等）は **--due付き・--priority 3**。
4. 報告会由来タスクには **`要整理`ラベル**付与（後でまとめてレビュー）。
5. **重複チェック**：一般質問ネタDB/市民意見リスト(c2c34bd8-)/既存Todoistに既出なら参照のみ（例：小下「新団地アクセス道路の複合課題」は5/31既存展開済＝重複登録しない）。

**実装場所:** CLAUDE.md「市政報告会の声の自動記録」恒久ルール＋本メモ。nichijo SKILL.md にも追記試行（プラグインキャッシュ上書きリスクありCLAUDE.md側が優先）。

**地区フォロー箱の実例（2026-06-14時点）:** 🏛議員活動配下に 御幸地区 フォロー／木下地区 フォロー を新設。楠平尾は南部地区 市民相談へ統合。小下は井田川地区 市民相談＋🏛単発。

関連: [[feedback_system_closing_loops_rot]] [[project_todoist_task_migration]] [[feedback_council_meeting_db_placement]]

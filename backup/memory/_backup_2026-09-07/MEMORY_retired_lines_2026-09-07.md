# MEMORY.md から退避した索引行（2026-09-07・起動固定費削減 案3）

完了・修理済みのため索引から外した。個別メモリファイル本体は memory/ 直下にそのまま残っている。戻すときはこの行をMEMORY.mdへ貼り戻す。

- [夜間ジョブにAgent/Taskが無く安全ゲートを実起動できない](project_nightly_jobs_missing_agent_tool.md) — 修理済(sns_leg.sh:74にAgent/Task)。9/3〜9/5夕便はゲート実起動で完走
- [Notion大改修＋ohayo/news v3](project_notion_ohayo_news_v3_renewal.md) — 完了
- [議会だより制作エージェント](project_gikai_dayori_creator.md) — 完了
- [Todoist移行](project_todoist_task_migration.md) — 完了。Notion✅/🗂️は参照のみ
- [区切り運用の仕組み化](project_kugiri_session_split.md) — 「区切り」→/clear→「再開」の3語。LAST.md廃止(9/5)・並行区切りは再開時に案件を1問で選ぶ
- [oyasumiのNotion本文denyは解消](feedback_oyasumi_blocked_by_content_gate.md) — 2026-08-26 EXEMPT_PARENTS追加。news側は未修理
- [区切り警告の一発通知は永久沈黙する](feedback_ctx_notice_oneshot_silence.md) — 2026-09-03修理。サブエージェント側で鳴ると本体が黙る
- [gate.pyは並行セッションで承認記録を消し合う](feedback_gate_json_concurrent_overwrite.md) — 2026-09-03マージ化で修理済。deny時はまず指紋不一致を疑う
- [gate.py --passは保存役が名乗らない](feedback_gate_pass_not_by_saver.md) — notion-saverがdeny復旧で自己承認。hookで遮断済み

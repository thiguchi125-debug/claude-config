# Memory Index

> 進行中案件 / 横断ルール / 外部参照ポインタ のみ常駐。**1行120字以内厳守**（詳細は必ずリンク先の個別ファイルへ。ここには書かない）。
> タスク別ガードルール＝`~/.claude/GUARDRAILS.md`／運用詳細手順＝`~/.claude/OPERATIONS.md`。過去ログは `_backup_<日付>/`。

## 🔄 進行中プロジェクト

- [Claude Code活用棚卸し2026-09-06](project_claude_usage_audit_2026-09-06.md) — 9/15に案1・2・5実施（約5〜6Kトークン減）。残＝案6(Todoist MCP切断)は草川判断待ち
- [SNS動画制作システム(Codex製CLI)](project_sns_video_system_codex.md) — 9/14 Claude Code対応・文字起こし導入で完走確認。残＝字幕の固有名詞誤り・未コミット
- [休眠スキル退避](project_dormant_skills.md) — slide-deck-prep/aisatsu-prep/daily-content-generator/drive-intake。「〇〇戻して」でmv
- [私立保育園への支援は他市より少ないか](project_shiritsu_hoikuen_shien_hikaku.md) — 差は金額でなく階層。執行率72.5%・市単独要綱4本。残＝未照会4件を子ども政策課へ
- [9月議会 一般質問2026-09](project_ippan_shitsumon_2026-09.md) — 本番9/10・11。会期フォルダ5種構成へ再編（正本=README.md）。次＝聞き取り/設計カード→議場カード薄い版
- [Obsidian導入・vault運用](project_obsidian_vault_workflow.md) — 2026-09-06。議会文書の正本はvault・注記は`#注記`・開いてるファイルは上書きせず新版。9/15置き場4つに整理
- [ObsidianのiPad同期(iCloud)](project_obsidian_icloud_ipad_sync.md) — 2026-09-09完了・iPad実機確認済。残＝旧実体の削除承認。macOS26でbrctlは死んでいる
- [Todoist総整理2026-09-06](project_task_audit_2026-09-06.md) — 2R完了:子PJ1＋セクション12・台帳KY-070〜074相談者未記録。残＝9/9の11件振り直し・図解は必要な箱だけ
- [市民要望管理台帳(Googleシート)](project_yobo_sheet_citizen_requests.md) — 稼働中。9/7〜Todoistミラー(yobo_mirror.py・期限3日窓)でTodoist「今日」が唯一の入口。残＝報告3件の回答メモ(9/9)
- [トークン燃費改善2026-09-05](project_token_efficiency_overhaul_2026-09-05.md) — [1m]廃止・fact-checker予算＋台帳・自動ジョブmax-turns。9/19に前後比較
- [発信フロー構造改善](project_hasshin_flow_phase1_2026-09-04.md) — A・B・C・E完了(9/6実運用でgate_runs=3達成・フック4点修理)。残＝H③単一入口・④司令塔
- [小中学校体育館エアコン](project_taiikukan_aircon_action.md) — 9月議会で柱1本→選挙後に署名。整備完了年度に誤解あり・要確認
- [ご意見箱フォーム夜間取込](project_form_intake_nightly.md) — 稼働中（9/6 03:32 ok・毎晩3:30）。8月の停止は解消済み
- [Drive直下を投函口にした自動振り分けv5](project_drive_root_intake_v5.md) — 滞留主因はファイル名のみ判定。スキャンPDFはOCR必須・議会語はSTRONG/WEAK分離
- [ファイル管理監査](project_file_audit_2026-07-22.md) — 残＝v4承認・Time Machine・trash_pending承認
- [市政報告レポート川合町版](project_shisei_report_kawaicho_complete_form.md) — チラシ完成形の勝ちパターン
- [content-pipeline発信ビジュアル統合](project_content_pipeline_visual_expansion.md) — 記事URL＋写真→1パス
- [後援会入会フォーム](project_koenkai_intake_form.md) — 告示後(10/18)の拡散停止テーブルあり
- [後援会名簿は2系統](project_koenkai_roster_two_systems.md) — Notion 94件とDrive 60名が氏名ゼロ重複。管理CSVは00_名簿・個人情報/
- [Discord夜間intake停止](project_discord_channel_split.md) — 2026-09-06停止・Todoist Inbox一本化。Botは温存。復活は通知専用のみ
- [SNS発信ルーティン](project_sns_routine_v2.md) — 2026-08-26簡素化。夕19:30の1本のみ・差し替え禁止。Phase4は着手しない
- [発信候補パック夜間ジョブがゲートでdeny](project_hakushin_pack_gate_deny.md) — 未修理
- [Notion保存フックの「=」正規化ずれ](project_content_gate_hook_equals_mismatch.md) — 2026-09-16修理済。norm()はgate.pyとフックの2箇所に別実装＝片方直したら両方
- [newsダイジェスト更新がゲートでdeny](project_news_briefing_digest_gate_deny.md) — 2026-09-06 EXEMPT_PAGESに2ページ追加（草川承認）。9/7朝に--pass回避が消えるか確認
- [AIくさかわ](project_ai_kusakawa.md) — 実装済。**草川手番待ち**＝ElevenLabs登録・キャラ生成
- [gyakusanスキル](project_gyakusan_skill.md) — 初回実運用待ち
- [答弁トラッカー＋実績コンパイラー](project_toben_tracker.md) — SNS実査は毎回伺い必須
- [📷写真ストック](project_photo_stock_system.md) — **草川手番＝アルバム作成が未**
- [デザインスタジオ](project_design_studio.md) — 残＝素材庫20枚生成
- [デザイン力の根本改善](project_design_capability_uplift_2026-08-25.md) — 様式の判断規則化・写真ゲート完了。残＝5軸採寸／ポスター参照
- [かめやま建築コンテスト2026](project_kameyama_building_contest.md) — 草川手番＝会場・スポンサー・協会合意
- [任天堂タイトルの催しの制約](project_nintendo_tournament_license.md) — 団体主催は個別許諾必須
- [eスポーツ協会スポンサーロゴ](project_esports_sponsor_logos.md) — 掲載順は草川指定で固定
- [中庄町夏祭りチラシ](project_nakasho_natsumatsuri_flyer.md) — 公選法HIGH留意
- [市政報告会5ステージ](project_shisei_houkokukai_skill.md) — _status.json正本
- [出屋の奥の太陽光と事業者(DSS)](project_deya_oku_taiyoko_jigyousha.md) — まとめはローカル手元用のみ・9月中に文書回答の約束
- [sparkスキル](project_spark_skill.md)／[photo-postスキル](project_photo_post_skill.md) — 初回FB待ち
- [AI作業環境マップNotion埋込](project_ai_env_map_notion_embed.md) — 「作業環境マップ更新して」で再デプロイ
- [Notion全体整理](project_notion_reorg_2026-07-05.md) — **政策×質問DB＝🎯42716725が唯一の書込先**
- [Notionプロジェクト基盤](project_notion_project_platform.md) — Todoist=実行/Notion=蓄積
- [成果物の実物を見てから作業枠を置く](feedback_check_artifacts_before_scheduling_work.md) — _status.json を信じない
- [Todoist「今日」ビューは4列](feedback_todoist_today_view_three_columns.md) — **削除前にidと件名を突合**
- [実行窓ラベル＋バッチ枠](project_task_window_labels.md) — @役所/@現地/@夜電話/@机上
- [task-add カレンダー突合ゲート](project_task_add_calendar_gate.md) — 期限付き登録は突合必須（hookがdeny）
- [2026年6月議会 一般質問prep](project_ippan_shitsumon_2026-06_resume.md) — 次＝counter-argument-simulator
- [3本柱 v0](../../../agents/knowledge/kusagawa_archive/04_compass/3pillars/v0_handoff.md) — 「3本柱v0見せて」
- [クラウドRoutine棚卸し](project_routine_cleanup_2026-07.md) — 停止4・修理1・現役4
- [亀山JC親子で米づくり体験](project_jc_oyako_komezukuri.md) — 収穫米配布は書かない(199条の3)・農家代表者名は表記割れ・理事長名は市職員と同名
- [熊本地震JC支援物資](project_jc_kumamoto_shien_busshi.md) — **地震は2026-07-28発生**（素の知識に無い）
- [三寺コスモス畑の再生](project_mitsudera_cosmos_saisei.md) — 10/17まつり。代表＝草川
- [kugiri「終了」モード](project_kugiri_shuryo_mode.md) — 未実装。区切り/再開/終了の3語・_done退避・同一案件は最新1本・30日で自動削除
- [トークン削減2026-08-20](project_token_reduction_2026-08-20.md) — 真因①印刷物の画像積み上げ(25枚deny hook)②34hセッション×並行×キャッシュ失効で上限到達
- [止まっていた自動化の復活](project_stalled_automation_revival_2026-08-20.md) — oyasumi毎晩23:30・gyakusan月曜6:30をlaunchd化

## 📦 移設済みルール束（詳細は各agent/SKILL末尾「📌恒久ガードルール」節）

- [運用規約：タスク特化ルールは担当agent/SKILL常駐](feedback_rules_reside_in_agents.md) — 横断ルールだけ個別行
- ohayo/oyasumi 16本／ショート動画7本／印刷物17本／ブログ6本／SNS・AIインタビュー8本／news-briefing 5本／街頭演説4本 → 各agent・SKILL.md末尾

## 📌 常時効く横断ルール（タスク別は GUARDRAILS.md）

- [置き場4つの使い分け](feedback_okiba_4tsu_tsukaiwake.md) — 渡す物→Drive／状況の一覧→Notion／注記する文章→Obsidian／他→ローカル。発信は50_発信/<日付>_<テーマ>/
- [vaultのmdはobs_open.shで開く](feedback_open_md_in_obsidian_not_notion.md) — Obsidianはvault外を表示不可。`open`だとNotionで開く事故あり
- [デザインは参照1本＋5軸採点から入る（全ビジュアル）](feedback_design_reference_library_first.md) — 2026-09-15草川「全てに応用」。スライド・サムネ・動画画像も対象
- [仕組みの不具合は見つけたらその場で直す](feedback_maintenance_weekly_window.md) — 9/15日曜枠廃止。1件だけ直して確認・Todoistに積まない。大改修は提案
- [正本文書が古いことがある](feedback_stale_authoritative_doc_vs_policy_change.md) — 制度変更は最新の事務連絡で上書き確認
- [AskUserQuestionのpreviewは自由記述欄を消す](feedback_askuserquestion_preview_hides_freetext.md) — 判断だけの質問にpreviewを付けない
- [成果物は古い版を閉じて新版だけ開く](feedback_open_folder_after_generating_files.md) — `~/.claude/scripts/show_latest.sh`
- [動画の投稿セットはDrive 📱動画素材/の1フォルダに一本化](feedback_video_package_single_drive_folder.md) — mp4・カバー・SNS7PF・台本・README。Obsidianに重複を置かない
- [渡したDriveファイルをcp上書きしない](feedback_never_overwrite_delivered_drive_file.md) — 草川のクラウド側編集が黙って消える。直すなら別名
- [発信物で絵文字を使わない](feedback_no_emoji_ai_smell.md) — 見出しはCSSライムバー/角マーカー/ピル・スライドも含む
- [架空エピソード禁止](feedback_no_fabricated_stories.md) — 実体験/一次情報/公式データのみ
- [確認事項は1件1問の選択式](feedback_ask_one_by_one_choices.md) — AskUserQuestion・1回最大4問
- [確認は最初に1回束ねる](feedback_ask_bundling_and_upfront_reflection.md) — 入力にある情報は最初から反映
- [「亀山」typo再発防止](feedback_kameyama_kanji_typo_guard.md) — JSONのunicode escape禁止
- [入力の固有名詞は音声入力の誤変換を疑う](feedback_input_proper_noun_dictation_check.md) — 施設名・地名は書く前にmemoryへgrep突合
- [更新日は提供開始日ではない](feedback_koushinbi_is_not_start_date.md) — 案内ページの更新日で開始時期を代用しない（合成エラー）
- [草川 役職・所属委員会マスタ](feedback_kusagawa_role_committee_master.md) — 教育民生委員会の委員
- [まちのミライ亀山は草川が役員](reference_machi_no_mirai_kameyama_yakuin.md) — 氏名冠発信は公選法199条の3。「役員を務める」と明示・物品配布は不可
- **タスク別ルールは `~/.claude/GUARDRAILS.md` 各節**（2026-09-15に本節から65行を移設・5行は既存行に統合。発信【1】ゲート【2】印刷物・動画【3】Notion【4】議会【5】市民対応【6】基盤【7】タスク・日程【9】）

## 🔗 外部参照ポインタ

- [育休退園は変更が2段階](reference_ikukyu_taien_r8_8gatsu_jimurenraku.md) — R8.8.1事務連絡が利用案内Q34を上書き。Q34だけ引くと誤り
- [景観保全作物の種子配付／廃止年度](reference_keikan_hozen_seed_haishi.md) — 要件を誤ると利益相反の説明が崩れる
- [ファイル管理v4 保存先マップ](reference_storage_map.md) — 用途→正規置き場の正本
- [カレンダー終日枠＝Todoist同期](reference_todoist_gcal_sync_allday.md) — 時間の正本は【作業】ブロック側
- [農振除外は5要件でなく6要件](reference_noshin_jogai_6yoken.md) — 号がずれた。受付は例年2月末・8月末
- 亀山の確定事実 — [半導体R8.6.15議場](reference_r8615_handotai_floor_facts.md)／[新庁舎開庁](reference_shincho_kaicho_r18.md)／[次期ごみ処理施設](reference_jiki_gomi_shori_shisetsu.md)／[太岡寺自治会要望書](reference_taikoji_yobosho_taiyoko.md)
- [体育館空調 国の目標と交付金期限](reference_taiikukan_kucho_kokuno_mokuhyo.md) — 目標は令和13年度中（8/27決定・7/31は指示のみ）／交付金の対象期間は令和15年度のまま
- [第3次総合計画の空調記述と指標](reference_dai3ji_sogokeikaku_kucho_shihyo.md) — 特別教室と体育館を同じ一文に書きながら指標は特別教室57%▶100%だけ
- [亀山の陸上競技環境](reference_kameyama_rikujo_kankyo.md) — 公認競技場も400mトラックも無い。西野公園の路面材質だけ未確認
- [かめやまマタニティ・サポート119と産科の確定事実](reference_kameyama_maternity_support_119.md) — 正式表記はひらがな＋中黒。妊婦健診は市内でも可
- [亀山市の道路の所管課](reference_kameyama_doro_shokan_ka.md) — 「道路河川課」は存在しない。既存道路の草刈り・支障木は建設管理課 道路保全グループ
- [通学路交通安全プログラムの対象範囲](reference_tsugakuro_program_scope.md) — 事故りやすい3点あり・着手前に必読
- [防災発信の定番リンク集5本](reference_bosai_link_collection.md) — 気象庁/川の防災/防災みえ/名阪/中電
- [議会質問アーカイブv3構造](reference_drive_archive_kusagawa.md) — 学習層1088件・grep対象6フォルダ
- [ルーティン運行表](reference_routine_unkohyo.md) — 日次ルーティン1枚。「運行表更新して」で再デプロイ
- [claude-configバックアップ](reference_claude_config_backup.md)／[Discordチャンネル起動フラグ](reference_discord_channel_launch_flag.md)
- [スキルトリガー一覧](reference_skill_triggers.md)／[エージェントトリガー一覧](reference_agent_triggers.md) — Notion早見表
- [市民の声3シート＋分類済資産](reference_市民の声情報源.md) — 2021/06〜359件・6ドメイン
- [コミバス運賃](reference_kameyama_combus_fare.md)／[コミバス収支](reference_kameyama_combus_revenue.md)
- [小中高生コミバス無料キャンペーン2026](reference_kameyama_kombus_muryo_campaign_2026.md) — 市実施7/21〜9/30・全7路線。8/26時点900名弱は伝聞・未確認
- [✅タスクDB クイック登録](reference_task_db_quick_create.md) — 参照のみ（新規登録はTodoist）
- [自治会・地区別報告会スライドWF](reference_jichikai_shisei_houkokukai_playbook.md) — 地区別ニュース62本
- 一般質問 — [標準時間](reference_kameyama_general_question_time.md)／[制作物のDrive保存先](reference_ippan_shitsumon_seisaku_drive.md)
- [選挙リーフレットv3](reference_senkyo_leaflet_v3_files.md)／[朝の街頭活動9拠点](reference_morning_street_locations.md)

## 🏛 主要DB／システム参照（呼出時のみ詳細を取りに行く）

- 政策コンパス: project_policy_compass.md — Origin「声を、チカラに。」3軸＝伝える/繋ぐ/希望
- 議会会期ハブDB: feedback_council_session_hub_db.md — /general-question-prep の中心DB
- 自治会×訪問×報告会: project_jichikai_db.md / project_jichikai_seed_48.md / project_shisei_houkokukai_db.md / project_jichikai_all_routes.md
- 後援会×公約: project_koukaikai_db_unification.md / project_koukaikai_kouyaku_db.md
- 選挙: project_2026senkyo_visit.md / project_election_dashboard_integration.md / project_election_hub_unification.md
- Notion全体: project_notion_overview_map.md — 21DB+14ハブ俯瞰
- 市民意見/タスク: project_iken_db_redesign.md / project_task_management_renewal.md / project_task_to_project_promotion.md / project_form_intake_db.md
- 会議/Drive資料: project_meeting_hub_renewal.md / project_meeting_notes_organization_db.md / project_drive_summary_db.md / project_oyasumi_meeting_autoorganize.md
- nichijo/oyasumi/ohayo: project_nichijo_mobile.md / project_nichijo_organize_mode.md / project_oyasumi_system.md / project_calendar_integration_nichijo_oyasumi.md
- ニュース/政策: project_news_briefing_system.md / project_ijamp_integration.md / project_policy_update_system.md / project_policy_expert_agents_11.md
- 発信物安全/品質: project_content_safety_gates.md / project_content_pipeline_quality.md / project_published_archive_system.md / project_blog_normal_mode.md
- AIインタビュー: project_ai_interview_config_db.md / project_ai_interview_config_designer.md / project_ai_interview_sns_poster.md
- 亀山の地震防災4軸データ: project_kameyama_bosai_jishin_local.md（agent-memory/kameyama-researcher/）
- エージェント本体: ~/.claude/agents/ 配下48本

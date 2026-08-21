# Memory Index

> 進行中案件 / 横断ルール / 外部参照ポインタ のみ常駐。**1行120字以内厳守**（詳細は必ずリンク先の個別ファイルへ。ここには書かない）。
> タスク別ガードルール＝`~/.claude/GUARDRAILS.md`／運用詳細手順＝`~/.claude/OPERATIONS.md`。過去ログは `_backup_<日付>/`。

## 🔄 進行中プロジェクト

- [小中学校体育館エアコン](project_taiikukan_aircon_action.md) — 9月議会で柱1本→選挙後に署名。整備完了年度に誤解あり・要確認
- [ご意見箱フォーム夜間取込](project_form_intake_nightly.md) — **停止中**。草川手番＝`/mcp`再認証
- [ファイル管理監査](project_file_audit_2026-07-22.md) — 残＝v4承認・Time Machine・trash_pending承認
- [市政報告レポート川合町版](project_shisei_report_kawaicho_complete_form.md) — チラシ完成形の勝ちパターン
- [content-pipeline発信ビジュアル統合](project_content_pipeline_visual_expansion.md) — 記事URL＋写真→1パス
- [後援会入会フォーム](project_koenkai_intake_form.md) — 告示後(10/18)の拡散停止テーブルあり
- [Discord3チャンネル分離](project_discord_channel_split.md) — 運用中（投げ込み/納品/ログ）
- [SNS発信ルーティンv3](project_sns_routine_v2.md) — 朝6:45/夕19:30にDM納品。次＝Phase4
- [発信候補パック夜間ジョブがゲートでdeny](project_hakushin_pack_gate_deny.md) — 未修理
- [AIくさかわ](project_ai_kusakawa.md) — 実装済。**草川手番待ち**＝ElevenLabs登録・キャラ生成
- [gyakusanスキル](project_gyakusan_skill.md) — 初回実運用待ち
- [答弁トラッカー＋実績コンパイラー](project_toben_tracker.md) — SNS実査は毎回伺い必須
- [📷写真ストック](project_photo_stock_system.md) — **草川手番＝アルバム作成が未**
- [デザインスタジオ](project_design_studio.md) — 残＝素材庫20枚生成
- [かめやま建築コンテスト2026](project_kameyama_building_contest.md) — 草川手番＝会場・スポンサー・協会合意
- [任天堂タイトルの催しの制約](project_nintendo_tournament_license.md) — 団体主催は個別許諾必須
- [eスポーツ協会スポンサーロゴ](project_esports_sponsor_logos.md) — 掲載順は草川指定で固定
- [中庄町夏祭りチラシ](project_nakasho_natsumatsuri_flyer.md) — 公選法HIGH留意
- [市政報告会5ステージ](project_shisei_houkokukai_skill.md) — _status.json正本
- [sparkスキル](project_spark_skill.md)／[photo-postスキル](project_photo_post_skill.md) — 初回FB待ち
- [AI作業環境マップNotion埋込](project_ai_env_map_notion_embed.md) — 「作業環境マップ更新して」で再デプロイ
- [Notion全体整理](project_notion_reorg_2026-07-05.md) — **政策×質問DB＝🎯42716725が唯一の書込先**
- [Notion大改修＋ohayo/news v3](project_notion_ohayo_news_v3_renewal.md) — 完了
- [議会だより制作エージェント](project_gikai_dayori_creator.md) — 完了
- [Notionプロジェクト基盤](project_notion_project_platform.md) — Todoist=実行/Notion=蓄積
- [Todoist移行](project_todoist_task_migration.md) — 完了。Notion✅/🗂️は参照のみ
- [成果物の実物を見てから作業枠を置く](feedback_check_artifacts_before_scheduling_work.md) — _status.json を信じない
- [Todoist「今日」ビューは4列](feedback_todoist_today_view_three_columns.md) — **削除前にidと件名を突合**
- [実行窓ラベル＋バッチ枠](project_task_window_labels.md) — @役所/@現地/@夜電話/@机上
- [task-add カレンダー突合ゲート](project_task_add_calendar_gate.md) — 期限付き登録は突合必須（hookがdeny）
- [2026年6月議会 一般質問prep](project_ippan_shitsumon_2026-06_resume.md) — 次＝counter-argument-simulator
- [3本柱 v0](../../../agents/knowledge/kusagawa_archive/04_compass/3pillars/v0_handoff.md) — 「3本柱v0見せて」
- [クラウドRoutine棚卸し](project_routine_cleanup_2026-07.md) — 停止4・修理1・現役4
- [熊本地震JC支援物資](project_jc_kumamoto_shien_busshi.md) — **地震は2026-07-28発生**（素の知識に無い）
- [三寺コスモス畑の再生](project_mitsudera_cosmos_saisei.md) — 10/17まつり。代表＝草川
- [トークン削減2026-08-20](project_token_reduction_2026-08-20.md) — 真因①印刷物の画像積み上げ(25枚deny hook)②34hセッション×並行×キャッシュ失効で上限到達
- [止まっていた自動化の復活](project_stalled_automation_revival_2026-08-20.md) — oyasumi毎晩23:30・gyakusan月曜6:30をlaunchd化

## 📦 移設済みルール束（詳細は各agent/SKILL末尾「📌恒久ガードルール」節）

- [運用規約：タスク特化ルールは担当agent/SKILL常駐](feedback_rules_reside_in_agents.md) — 横断ルールだけ個別行
- ohayo/oyasumi 16本／ショート動画7本／印刷物17本／ブログ6本／SNS・AIインタビュー8本／news-briefing 5本／街頭演説4本 → 各agent・SKILL.md末尾

## 📌 常時効く横断ルール（タスク別は GUARDRAILS.md）

- [資産価値直結の手続相談は二層分離](feedback_shisan_kachi_tetsuzuki_gaikan_kanri.md) — 農振除外・農地転用。氏名は名簿区画1か所
- [無人oyasumiは安全ゲートでNotion作成できない](feedback_oyasumi_blocked_by_content_gate.md) — 本文はローカル退避／プロパティのみなら通る
- [oyasumiの会議体マスタIDが古い](feedback_oyasumi_kaigitai_master_id_stale.md) — 46414643- は not found・会議体は毎回未紐付け
- [市民意見リストDBに「対応状況」は無い](feedback_iken_db_no_taio_status.md) — 未対応集計は「未完了（要対応）」ビュー
- [gate.pyは並行セッションで承認記録を消し合う](feedback_gate_json_concurrent_overwrite.md) — deny時はまず`_content_gate.json`を疑う
- [update_status.pyは_pipeline_status.json破損で落ちる](feedback_pipeline_status_json_corruption.md) — JSONDecodeErrorはこれ
- [印刷物は参照ライブラリから入る](feedback_design_reference_library_first.md) — `design_system/references/`から参照1本を自分でRead
- [成果物は古い版を閉じて新版だけ開く](feedback_open_folder_after_generating_files.md) — `~/.claude/scripts/show_latest.sh`
- [案件フォルダは番号付き構成＋README](feedback_project_folder_numbered_structure.md) — assetsはリネーム禁止
- [発信前に担当agent/SKILL定義をRead](feedback_read_agent_spec_before_writing.md) — 機械判定＝`check_content_limits.py`
- [Notion保存も「発信」＝保存前に安全ゲート](feedback_safety_gates_before_notion_save.md) — 本文は手打ち禁止・draftからコピペ
- [顔ぼかしは草川本人を除外・二段で潰す](feedback_face_blur_exclude_kusagawa_and_verify.md) — 検出器＋目視
- [発信物で絵文字を使わない](feedback_no_emoji_ai_smell.md) — 見出しはCSSライムバー/角マーカー/ピル
- 禁止表現 — [届かないを終わらせる](feedback_phrase_todokanai_owaraseru.md)／[届かなくても届く](feedback_phrase_todokanakutemo_todoku.md)／[距離比喩](feedback_metric_distance_metaphor_avoid.md)／[抽象・詩的比喩](feedback_no_abstract_poetic_phrases.md)／[つくり話冒頭](feedback_no_halfbaked_story_openings.md)／[空虚な問いかけ](feedback_no_hollow_rhetorical_questions.md)
- [架空エピソード禁止](feedback_no_fabricated_stories.md) — 実体験/一次情報/公式データのみ
- [SNSで草川の行動を言い切らない](feedback_sns_no_action_promise_assertions.md) — 約束は断定しない。事実・数字は可
- [「次の議会で追及」型を軽々に使わない](feedback_no_aggressive_pursuit_phrases.md) — 特定議会×対決動詞禁止
- [Xはハッシュタグ必須・Instagramは5つ](feedback_hashtag_policy_x_instagram.md) — LINEはタグなしが正
- 他議員の誤帰属ガード — [対外発信に名前を載せない](feedback_no_other_council_members_names.md)／[子ども医療費](feedback_kodomo_iryohi_sns_misattribution.md)／[濁り水断水](feedback_fukami_water_distribution_misattribution.md)
- [議会・他議員への提言は対外発信で避ける](feedback_no_council_directed_proposals.md) — 提案宛先は執行部のみ
- [確認事項は1件1問の選択式](feedback_ask_one_by_one_choices.md) — AskUserQuestion・1回最大4問
- [確認は最初に1回束ねる](feedback_ask_bundling_and_upfront_reflection.md) — 入力にある情報は最初から反映
- [コピペ前提原稿はコピペ即可の書式で](feedback_copypaste_draft_delivery.md) — drafts/に1案1txt→`open -e`
- [コンテンツ生成は常時lean full-agent](feedback_content_generation_default_flow.md) — 主担当agent省略禁止
- タスク登録 — [保存先＋期限を提示→回答後に保存](feedback_ask_destination_and_deadline_before_register.md)／[+3日は推奨案](feedback_task_deadline_3days.md)／[Pending系3区分](feedback_task_db_pending_status.md)
- [早朝5:00-7:00は机上作業限定](feedback_early_morning_desk_band.md) — 電話・役所・現地は不可
- [固定曜日・固定時刻の作業枠は成立しない](feedback_fixed_weekly_blocks_dont_hold.md) — 安定は早朝のみ・1日2ブロック
- [15:00-18:30は挨拶回り優先枠](feedback_greeting_rounds_time_reserve.md) — 作業ブロックで埋めない
- [brainstormingのトークン浪費](feedback_brainstorming_token_efficiency.md) — design docは3000字以内
- [「亀山」typo再発防止](feedback_kameyama_kanji_typo_guard.md) — JSONのunicode escape禁止
- [草川 役職・所属委員会マスタ](feedback_kusagawa_role_committee_master.md) — 教育民生委員会の委員

## 🔗 外部参照ポインタ

- [景観保全作物の種子配付／廃止年度](reference_keikan_hozen_seed_haishi.md) — 要件を誤ると利益相反の説明が崩れる
- [ファイル管理v4 保存先マップ](reference_storage_map.md) — 用途→正規置き場の正本
- [カレンダー終日枠＝Todoist同期](reference_todoist_gcal_sync_allday.md) — 時間の正本は【作業】ブロック側
- [農振除外は5要件でなく6要件](reference_noshin_jogai_6yoken.md) — 号がずれた。受付は例年2月末・8月末
- 亀山の確定事実 — [半導体R8.6.15議場](reference_r8615_handotai_floor_facts.md)／[新庁舎開庁](reference_shincho_kaicho_r18.md)／[次期ごみ処理施設](reference_jiki_gomi_shori_shisetsu.md)／[太岡寺自治会要望書](reference_taikoji_yobosho_taiyoko.md)
- [通学路交通安全プログラムの対象範囲](reference_tsugakuro_program_scope.md) — 事故りやすい3点あり・着手前に必読
- [防災発信の定番リンク集5本](reference_bosai_link_collection.md) — 気象庁/川の防災/防災みえ/名阪/中電
- [議会質問アーカイブv3構造](reference_drive_archive_kusagawa.md) — 学習層1088件・grep対象6フォルダ
- [claude-configバックアップ](reference_claude_config_backup.md)／[Discordチャンネル起動フラグ](reference_discord_channel_launch_flag.md)
- [スキルトリガー一覧](reference_skill_triggers.md)／[エージェントトリガー一覧](reference_agent_triggers.md) — Notion早見表
- [市民の声3シート＋分類済資産](reference_市民の声情報源.md) — 2021/06〜359件・6ドメイン
- [コミバス運賃](reference_kameyama_combus_fare.md)／[コミバス収支](reference_kameyama_combus_revenue.md)
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

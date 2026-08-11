# Memory Index

> 進行中案件 / 常時効く横断ルール / 外部参照ポインタ のみ常駐。1行/エントリ厳守（~120字以内）。
> **タスク別ガードルール（印刷物・動画・Notion・議会・市民対応・基盤の罠・個別案件）は `~/.claude/GUARDRAILS.md`** に分離（2026-08-11・トークン削減）。該当タスクに入る前にRead。
> **運用詳細手順は `~/.claude/OPERATIONS.md`**。過去ログは `_backup_<日付>/`。

## 🔄 進行中プロジェクト

- [小中学校体育館エアコン アクション](project_taiikukan_aircon_action.md) — 8月WBGT分散測定→9月議会で柱1本→選挙後に署名。**「リース期間R9-R19だから2033年に間に合わない」は誤り**＝整備はR9完了
- [ご意見箱フォーム夜間自動取込](project_form_intake_nightly.md) — launchd 3:30→📝市民意見リスト＋_citizen_voice。**残=初回キャッチアップ**。Drive read_file_contentはキャッシュ腐りで使用禁止
- [ファイル管理監査2026-07-22](project_file_audit_2026-07-22.md) — Drive直下4フォルダ正規形・💾Macローカルミラー新設。**残=パイプラインv4承認・Time Machine未設定・trash_pending承認**
- [市政報告レポート川合町版＝チラシ完成形](project_shisei_report_kawaicho_complete_form.md) — report_kameokaテンプレの勝ちパターン。QR検証は必ずpyzbar
- [content-pipelineに発信ビジュアル統合](project_content_pipeline_visual_expansion.md) — 記事URL＋写真→ブログ→サムネ＋SNS7種＋Reelを1パス。サムネは着手前に元写真有無を確認
- [後援会入会フォームシステム](project_koenkai_intake_form.md) — URL1本→GAS自動返信→名簿CSV→週次でSubstack CSV。告示後(10/18)拡散停止テーブルあり
- [Discord用途別3チャンネル分離](project_discord_channel_split.md) — 実装済・**草川手番=アプリで`投げ込み/納品/ログ`を作る→`discord_api.py discover --apply`**。未設定でもDMに落ちて壊れない
- [SNS発信ルーティンv3](project_sns_routine_v2.md) — 朝6:45/夕19:30に完成短文をDM直接納品。新風枠毎便必須・iJAMPはGmail経由。次=Phase4週次深掘り
- [AIくさかわ（AI代役ショート動画）](project_ai_kusakawa.md) — 実装完了。**草川手番待ち**=①ElevenLabs登録②nano-bananaキャラ生成。それまで投稿不可
- [gyakusanスキル](project_gyakusan_skill.md) — Calendar＋Notion＋Todoist突合・60日二層逆算・承認分のみ登録。初回実運用待ち
- [答弁トラッカー＋実績コンパイラー](project_toben_tracker.md) — 台帳=07_commitments/ledger.json。**SNS実査は毎回伺い必須**。欠落会期=R05-12・R06-03/06/09
- [📷写真ストックシステム](project_photo_stock_system.md) — Googleフォト「📷議員活動」→月一でChrome回収→Drive整理。**草川手番=アルバム作成が未**
- [デザインスタジオ環境](project_design_studio.md) — v2センス強化済。残=素材庫のnano-banana生成20枚
- [かめやま建築コンテスト2026（マイクラ）](project_kameyama_building_contest.md) — 8/29みらい・小中10名。**Minecraftは主名称にできない／Switch・PSはワールド書出不可**。草川手番=会場確保・スポンサー掲載可否・協会合意
- [任天堂タイトルの催しを協会名義で開く制約](project_nintendo_tournament_license.md) — **団体主催は規模不問で個別許諾申請必須／大会名に「eスポーツ」不可／スポンサー不可／出場料は会計公開義務**。9/19は「かめやまゲーム交流会」へ改称
- [eスポーツ協会スポンサー10社ロゴ](project_esports_sponsor_logos.md) — 掲載順は草川指定で固定・年間スポンサー表記。BUARTSは黄色地のまま。素材は0919案内フォルダが正本
- [中庄町夏祭りチラシ](project_nakasho_natsumatsuri_flyer.md) — 主催「中庄を全力応援する会」（草川と独立前提）。公選法HIGH留意
- [市政報告会5ステージスキル](project_shisei_houkokukai_skill.md) — _status.json正本。**初回実走=安知本地区**
- [sparkスキル](project_spark_skill.md)／[photo-postスキル](project_photo_post_skill.md) — いずれも初回実運用フィードバック待ち
- [AI作業環境マップ Notion埋め込み](project_ai_env_map_notion_embed.md) — 自動更新なし→「作業環境マップ更新して」で再デプロイ
- [Notion全体整理2026-07-05](project_notion_reorg_2026-07-05.md) — 🤖AIハブ新設・**政策×質問DB統一＝🎯42716725が唯一の書込先**（旧6f1895ac凍結）
- [Notion大改修＋ohayo/news v3＋smart-intake](project_notion_ohayo_news_v3_renewal.md) — 2026-07-03実施・指摘3点も同日修理済
- [議会だより制作エージェント](project_gikai_dayori_creator.md) — 整備完了。トリガー「議会だより作って」
- [Notionプロジェクト・プラットフォーム](project_notion_project_platform.md) — Todoist=実行/Notion=蓄積。初期17PJ投入済
- [Todoistへタスク管理移行](project_todoist_task_migration.md) — 完了。td.py使用・Notion✅/🗂️は参照のみ
- [作業枠を置く前に成果物の実物を見る](feedback_check_artifacts_before_scheduling_work.md) — 2026-08-10。北東版レポートは完成済なのに`_status.json`がdoingのままで3時間の枠を積んだ。制作物は必ず`~/outputs/houkokukai/*/02_report/`等を確認
- [Todoist「今日」ビューは4列に分ける](feedback_todoist_today_view_three_columns.md) — 2026-08-10。期限は1種類しかなく手番/催促日/前提待ちが混ざる。td.py実装済。**削除前にidと件名を突き合わせる**（誤削除やらかし有）
- [実行窓ラベル＋バッチ枠](project_task_window_labels.md) — @役所/@現地/@夜電話/@机上。2026-08-10に**期限超過61→0件**。task_windowsはラベルを正規表現より優先
- [task-add カレンダー突合ゲート](project_task_add_calendar_gate.md) — 期限付き登録は突合必須（hookがdeny）。**終日予定は一律ブロックしない・判定は30分コマ**。v3で`--plan`＝作業ブロックをカレンダーに登録（時間の正本はカレンダー側）
- [2026年6月議会 一般質問prep](project_ippan_shitsumon_2026-06_resume.md) — 骨子v7確定。次=counter-argument-simulator
- [3本柱 v0 ハンドオフ](../../../agents/knowledge/kusagawa_archive/04_compass/3pillars/v0_handoff.md) — v0草案保管中。必要時「3本柱v0見せて」
- [クラウドRoutine棚卸し2026-07](project_routine_cleanup_2026-07.md) — 停止4本・修理1本・現役4本

## 📦 移設済みルール束（詳細は各agent/SKILL末尾「📌恒久ガードルール」節）

- [運用規約：タスク特化ルールは担当agent/SKILL常駐](feedback_rules_reside_in_agents.md) — 新feedbackは対象agent/SKILL末尾へ。横断ルールだけ個別行
- ohayo/oyasumi運用16本 → ohayo/oyasumi SKILL.md
- ショート動画7本 → short-video-*（字幕帯y1240-1460に統一済）
- 印刷物17本 → print-designer/print-layout-architect（手書き挨拶は幅90mm前後・縮小禁止等）
- ブログ6本 → blog-writer/normal（深掘りは02_publications/blog実物と型合わせ必須＝絵文字/詩的抽象排除・具体密度）
- SNS/AIインタビュー8本 → sns-content-creator/polisher/ai-interview-sns-poster（[[feedback_sns_blog_link_required]]／[[feedback_line_ai_interview_over_form]]／[[feedback_line_500chars_no_hashtag]]）
- news-briefing 5本 → news-briefing SKILL.md／街頭演説4本 → daily-street-speech

## 📌 常時効く横断ルール（毎ターン効く分だけ・タスク別は GUARDRAILS.md）

- [成果物を作ったら指示されなくてもフォルダを開く](feedback_open_folder_after_generating_files.md) — 画像・PDF・動画素材を作ったら必ず `open <dir>`。貼付とフォルダ表示は両方
- [発信物を書く前に担当agent/SKILLの定義ファイルを必ずRead](feedback_read_agent_spec_before_writing.md) — agent起動不可でも仕様は読める。規定と内容が衝突したら内容を削る前に草川判断（ブログは超過可＝徹底解説モード）。機械判定＝`check_content_limits.py`
- [発信物のNotion保存も「発信」＝保存前に安全ゲート必須](feedback_safety_gates_before_notion_save.md) — 「保存するだけ」は例外にならない。**レビュアーへの依頼でスコープを絞らない（全テキスト＋全画像＋メモを毎回渡す）**。削除を決めた語は`<案件>_banned.txt`→gate.pyが機械スイープ。Notion本文は手打ち禁止＝draftからコピペ。レビューは全修正後の完成パッケージに1回
- [発信物で絵文字を使わない](feedback_no_emoji_ai_smell.md) — 見出し装飾はCSSライムバー/角マーカー/ピル
- 禁止表現集 — [「届かないを終わらせる」](feedback_phrase_todokanai_owaraseru.md)／[「届かなくても届く」](feedback_phrase_todokanakutemo_todoku.md)／[距離比喩](feedback_metric_distance_metaphor_avoid.md)／[抽象・詩的比喩](feedback_no_abstract_poetic_phrases.md)／[つくり話冒頭](feedback_no_halfbaked_story_openings.md)／[空虚な問いかけ風](feedback_no_hollow_rhetorical_questions.md) — 全面禁止・断定と行為語で書く
- [架空エピソード・つくり話禁止](feedback_no_fabricated_stories.md) — 実体験/一次情報/公式データのみ
- [SNS投稿文案で草川の行動を言い切らない](feedback_sns_no_action_promise_assertions.md) — 「取り上げます」等の約束を断定で書かない→「〜したい」。事実・数字の断定は可
- [「次の議会で追及」型表現を軽々に使わない](feedback_no_aggressive_pursuit_phrases.md) — 特定議会×対決動詞禁止
- [Xは必ずハッシュタグ・Instagramは5つ](feedback_hashtag_policy_x_instagram.md) — 標準は`#亀山市 #草川たくや`＋テーマ/地区タグ。**例外＝他地域の災害・事故では地元ブランドタグを使わない**。LINEはタグなしが正
- 他議員の誤帰属ガード — [対外発信に名前を載せない](feedback_no_other_council_members_names.md)（内部資料はOK）／[5/27子ども医療費](feedback_kodomo_iryohi_sns_misattribution.md)（3月議会医療費質疑は福沢議員）／[濁り水断水の給水描写](feedback_fukami_water_distribution_misattribution.md)（深水議員3番。2,700世帯/11月/12月は草川由来OK）
- [議会・他議員への提言は対外発信で避ける](feedback_no_council_directed_proposals.md) — 提案宛先は執行部に限定
- [確認事項は1件1問の選択式で出す](feedback_ask_one_by_one_choices.md) — AskUserQuestionでタップ回答に。**束ねるのはラウンド数・分けるのは設問**。1回最大4問
- [確認は最初に1回束ねる・入力にある情報は最初から反映](feedback_ask_bundling_and_upfront_reflection.md) — 単位不明の数値は勝手に落とさず初回確認に混ぜる／安全ゲート指摘は自分で潰せる分を潰してから出す／締切当日案件は確認1回まで
- [コピペ前提原稿は毎回コピペ即可の書式で出す](feedback_copypaste_draft_delivery.md) — 形式を聞き返さない。既定=drafts/に1案1txt→open -e＋チャットは`>`や・なしのフラット塊
- [コンテンツ生成は常時lean full-agentがデフォルト](feedback_content_generation_default_flow.md) — 主担当agent省略禁止、目標90〜170K
- タスク登録 — [保存先＋期限を提示→本人回答後に保存](feedback_ask_destination_and_deadline_before_register.md)（既定値で勝手に登録しない・[[feedback_task_deadline_3days]]の+3日は推奨案に降格）／[✅タスクDB Pending系3区分](feedback_task_db_pending_status.md)（Pending/Wish List/Waiting）
- [早朝5:00-7:00は机上作業に使える](feedback_early_morning_desk_band.md) — **机上作業限定**（役所・連絡・現地は不可＝電話をかけない）。task_windows.py `Kind.early`／`band()`で容量の数え方から分離
- [固定曜日・固定時刻の作業枠は成立しない](feedback_fixed_weekly_blocks_dont_hold.md) — 2026-08-10実測。安定は**早朝5:00-6:30だけ**（月金6:30の街頭活動で切る）。挨拶枠・昼・バッファを除くと1日2ブロック
- [15:00-18:30は挨拶回り優先枠](feedback_greeting_rounds_time_reserve.md) — 作業ブロックで埋めない（sessions.py `GREETING_START/END`）。実働は平日午前＋13:15-14:45＋18:45以降
- [brainstormingのトークン浪費パターン](feedback_brainstorming_token_efficiency.md) — 同内容md多重生成禁止、design docは3000字以内
- [「亀山」typo再発防止](feedback_kameyama_kanji_typo_guard.md) — JSONのunicode escape禁止・日本語は直接書く
- [草川 役職・所属委員会マスタ](feedback_kusagawa_role_committee_master.md) — 教育民生委員会の委員（確定）

## 🔗 外部参照ポインタ

- [景観保全作物の種子配付／田園環境保全事業の廃止年度](reference_keikan_hozen_seed_haishi.md) — 廃止は**令和7年度**・申請は**農業者要件**（要件を誤ると利益相反の説明が崩れる）・昼生7自治会は「神向谷」表記
- [ファイル管理システムv4 保存先マップ](reference_storage_map.md) — 用途→正規置き場の正本。夜間パイプラインv4・00_名簿区画・週次スイープ
- 亀山の確定事実 — [半導体R8.6.15議場](reference_r8615_handotai_floor_facts.md)（旗は櫻井市長・草川は後押し役）／[新庁舎開庁=令和18年度](reference_shincho_kaicho_r18.md)（「令和12年度」は旧計画＝誤り）／[次期ごみ処理施設](reference_jiki_gomi_shori_shisetsu.md)（R15年度稼働・48t/日・271〜307億・**建設地は未定**）／[太岡寺自治会 太陽光要望書R5.12.12](reference_taikoji_yobosho_taiyoko.md)（村山竹則会長）
- [防災発信の定番リンク集5本](reference_bosai_link_collection.md) — 気象庁(亀山2421000)/川の防災/防災みえ/名阪国道規制/中電停電
- [草川議会質問アーカイブv3構造](reference_drive_archive_kusagawa.md) — 学習層1088件、grep対象は01_council〜06_election
- [claude-configバックアップ](reference_claude_config_backup.md) — GitHub thiguchi125-debug/claude-config、復元はrestore.sh／[Discordチャンネル起動フラグ](reference_discord_channel_launch_flag.md) — 正=`claude --channels plugin:discord@claude-plugins-official`
- [スキルトリガー一覧](reference_skill_triggers.md)／[エージェントトリガー一覧](reference_agent_triggers.md) — Notion早見表
- [市民の声Googleフォーム3シート＋ETL分類済資産](reference_市民の声情報源.md) — 2021/06〜359件、6ドメイン分類済
- [亀山市コミバス運賃](reference_kameyama_combus_fare.md)／[コミバス・のりかめさん収支](reference_kameyama_combus_revenue.md) — 収支率4.8%（R3）
- [✅タスクDB クイック登録](reference_task_db_quick_create.md) — ds=292cf503-a68f-81c6-b9dd-000b3ffdd2ce
- [自治会・地区別市政報告会スライド作成プレイブック](reference_jichikai_shisei_houkokukai_playbook.md) — 地区別ニュース62本・標準WF
- 一般質問 — [標準時間](reference_kameyama_general_question_time.md)（答弁込み45分）／[制作物のDrive保存先](reference_ippan_shitsumon_seisaku_drive.md)（`ZZ_一般質問制作/R0X/YYYY-MM_◯月議会/`）
- [選挙リーフレットv3 ファイル群](reference_senkyo_leaflet_v3_files.md)／[朝の街頭活動場所9拠点](reference_morning_street_locations.md)

## 🏛 主要DB／システム参照（呼出時のみ詳細を取りに行く）

- 政策コンパス: project_policy_compass.md — Origin「声を、チカラに。」3軸=伝える/繋ぐ/希望
- 議会会期ハブDB: feedback_council_session_hub_db.md — 年4ページ・/general-question-prep の中心DB
- 自治会×訪問×市政報告会: project_jichikai_db.md / project_jichikai_seed_48.md / project_shisei_houkokukai_db.md / project_jichikai_all_routes.md
- 後援会×公約: project_koukaikai_db_unification.md / project_koukaikai_kouyaku_db.md
- 選挙: project_2026senkyo_visit.md / project_election_dashboard_integration.md / project_election_hub_unification.md
- Notion全体: project_notion_overview_map.md — 21DB+14ハブ俯瞰、月1見直し
- 市民意見/タスク: project_iken_db_redesign.md / project_task_management_renewal.md / project_task_to_project_promotion.md / project_form_intake_db.md
- 会議/Drive資料: project_meeting_hub_renewal.md / project_meeting_notes_organization_db.md / project_drive_summary_db.md / project_oyasumi_meeting_autoorganize.md
- nichijo/oyasumi/ohayo: project_nichijo_mobile.md / project_nichijo_organize_mode.md / project_oyasumi_system.md / project_calendar_integration_nichijo_oyasumi.md
- ニュース/政策: project_news_briefing_system.md / project_ijamp_integration.md / project_policy_update_system.md / project_policy_expert_agents_11.md
- 発信物安全/品質: project_content_safety_gates.md / project_content_pipeline_quality.md / project_published_archive_system.md / project_blog_normal_mode.md
- AIインタビュー: project_ai_interview_config_db.md / project_ai_interview_config_designer.md / project_ai_interview_sns_poster.md
- 亀山の地震防災4軸データ: project_kameyama_bosai_jishin_local.md（agent-memory/kameyama-researcher/）— 上下水道耐震化計画・個別避難計画・ため池・住宅耐震化の実数
- エージェント本体: ~/.claude/agents/ 配下44本

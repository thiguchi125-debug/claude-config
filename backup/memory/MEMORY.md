# Memory Index

> 進行中案件 / 反復で効くガードルール / 外部参照ポインタ のみ常駐。詳細は各トピックファイル。過去ログは `_backup_<日付>/`。1行/エントリ厳守（~120字以内）。同系統は束ね行。

## 🔄 進行中プロジェクト

- [ご意見箱フォーム夜間自動取込](project_form_intake_nightly.md) — launchd 3:30→📝市民意見リスト＋_citizen_voice。**残=初回キャッチアップ**。Drive read_file_contentはキャッシュ腐りで使用禁止
- [ファイル管理監査2026-07-22](project_file_audit_2026-07-22.md) — Drive直下4フォルダ正規形・💾Macローカルミラー新設。**残=パイプラインv4承認・Time Machine未設定・trash_pending承認**
- [市政報告レポート川合町版＝チラシ完成形](project_shisei_report_kawaicho_complete_form.md) — report_kameokaテンプレの勝ちパターン。QR検証は必ずpyzbar
- [content-pipelineに発信ビジュアル統合](project_content_pipeline_visual_expansion.md) — 記事URL＋写真→ブログ→サムネ＋SNS7種＋Reelを1パス。サムネは着手前に元写真有無を確認
- [後援会入会フォームシステム](project_koenkai_intake_form.md) — URL1本→GAS自動返信→名簿CSV→週次でSubstack CSV。告示後(10/18)拡散停止テーブルあり
- [SNS発信ルーティンv3](project_sns_routine_v2.md) — 朝6:45/夕19:30に完成短文をDM直接納品。新風枠毎便必須・iJAMPはGmail経由。次=Phase4週次深掘り
- [AIくさかわ（AI代役ショート動画）](project_ai_kusakawa.md) — 実装完了。**草川手番待ち**=①ElevenLabs登録②nano-bananaキャラ生成。それまで投稿不可
- [gyakusanスキル](project_gyakusan_skill.md) — Calendar＋Notion＋Todoist突合・60日二層逆算・承認分のみ登録。初回実運用待ち
- [答弁トラッカー＋実績コンパイラー](project_toben_tracker.md) — 台帳=07_commitments/ledger.json。**SNS実査は毎回伺い必須**。欠落会期=R05-12・R06-03/06/09
- [📷写真ストックシステム](project_photo_stock_system.md) — Googleフォト「📷議員活動」→月一でChrome回収→Drive整理。**草川手番=アルバム作成が未**
- [デザインスタジオ環境](project_design_studio.md) — v2センス強化済。残=素材庫のnano-banana生成20枚
- [中庄町夏祭りチラシ](project_nakasho_natsumatsuri_flyer.md) — 主催「中庄を全力応援する会」（草川と独立前提）。公選法HIGH留意
- [市政報告会5ステージスキル](project_shisei_houkokukai_skill.md) — _status.json正本。**初回実走=安知本地区**
- [sparkスキル](project_spark_skill.md)／[photo-postスキル](project_photo_post_skill.md) — いずれも初回実運用フィードバック待ち
- [AI作業環境マップ Notion埋め込み](project_ai_env_map_notion_embed.md) — 自動更新なし→「作業環境マップ更新して」で再デプロイ
- [Notion全体整理2026-07-05](project_notion_reorg_2026-07-05.md) — 🤖AIハブ新設・**政策×質問DB統一＝🎯42716725が唯一の書込先**（旧6f1895ac凍結）
- [Notion大改修＋ohayo/news v3＋smart-intake](project_notion_ohayo_news_v3_renewal.md) — 2026-07-03実施・指摘3点も同日修理済
- [議会だより制作エージェント](project_gikai_dayori_creator.md) — 整備完了。トリガー「議会だより作って」
- [Notionプロジェクト・プラットフォーム](project_notion_project_platform.md) — Todoist=実行/Notion=蓄積。初期17PJ投入済
- [Todoistへタスク管理移行](project_todoist_task_migration.md) — 完了。td.py使用・Notion✅/🗂️は参照のみ
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

## 📌 恒久ガードルール（実運用で効く feedback）

- [発信物を書く前に担当agent/SKILLの定義ファイルを必ずRead](feedback_read_agent_spec_before_writing.md) — 2026-08-05。agent起動不可でも仕様は読める。読まずに書いて憲法5構成を3つ外し、さらに存在しない「X≤140字」を捏造して自分を縛った。規定と内容が衝突したら内容を削る前に草川判断（ブログは超過可＝徹底解説モード新設）。機械判定＝`check_content_limits.py`
- [発信物のNotion保存も「発信」＝保存前に安全ゲート必須](feedback_safety_gates_before_notion_save.md) — 2026-08-05草川指摘。「保存するだけ」「前セッションで通過済」「FINAL付き」は例外にならない。fact→riskを自分で通した時だけ「通過済」と書ける。他地域の災害を導入に使った原稿は[[feedback_disaster_rescue_phase_no_local_pivot]]と地元タグ例外を必ず当てる
- [Xは必ずハッシュタグ・Instagramは5つ](feedback_hashtag_policy_x_instagram.md) — 2026-07-30草川指示。標準は`#亀山市 #草川たくや`＋テーマ/地区タグ。**例外＝他地域の災害・事故の投稿では地元ブランドタグを使わない**（リーチ拡大先が自分の有権者になる）。判断基準「被災地に届けるためか、自分に届かせるためか」。LINEはタグなしが正なので取り違えない
- [他地域の災害・救助フェーズ中は被災地の文章だけ](feedback_disaster_rescue_phase_no_local_pivot.md) — 2026-07-28熊本地震で確立。亀山の備え・政策・実績を同居させず、地元記事は被災地への言及を全削除して独立させる。「まもなく72時間」書き出し／無過失の強調／未確認の情景／「できることは多くありません」型の弁解は禁止
- [ショート動画の挿入画像が永久に作られない穴](feedback_short_video_images_never_created.md) — 2026-07-30 JR亀山駅前で発覚。会話で台本を直し続けた案件はスキル未起動＝Step5が飛ぶ→Mode Rが「未作成＝伝播対象なし」で閉じる。画像枚数はカット表が決める（テロップ全画面・図解・**編集の絶対条件付きテロップは1枚に焼いて分割不能にする**・サムネ）。台本の表記ルールは画像とサムネにも適用。SKILL.md実装済
- [Todoist期限切れの真因はInboxの動詞なし生メモ](feedback_todoist_inbox_verbless_memo_rot.md) — 棚卸しは①死んだ箱②動詞なしメモ③期限切れ実タスクに割る。声の正本はTodoistでなく📝市民意見リスト
- [けんろう版v3の労務費「2026年4月告示」は誤り](feedback_kenro_v3_romuhi_date_error.md) — 正=2025年12月国策定・84.7万円は東京都の例
- [アーバンスポーツ署名はスケボー特化にしない](feedback_urban_sports_not_skateboard_only.md) — 背骨＝「音を出せる×歩いて通える」2条件。**署名①提出先＝市長＋かわまちづくり協議会会長の2者**
- [Chrome MCPのGoogleフォーム編集は拡張競合でブロック](feedback_chrome_mcp_google_forms_write_blocked.md) — navigate/read_page/findは生きてる。手動書込→read_page検証が最速
- [Googleドキュメント形式はローカルgrepに不可視](feedback_gdoc_native_invisible_to_local_grep.md) — ローカル空振り時は**必ずDrive MCP search_files**してから「無い」と言う
- [headlessのMCPはdeferred＝「未接続」ではない](feedback_headless_mcp_deferred_false_absent.md) — allowedToolsに`ToolSearch`必須。「MCP未接続」報告は再認証より先にこれを疑う
- [agent frontmatterのtools行はツールゼロ化→捏造報告](feedback_agent_tools_frontmatter_breaks.md) — tools行は書かない・tool_uses:0は捏造シグナル
- [agent大掃除＋description 400字ルール](feedback_agent_description_diet_2026-07-05.md) — 旧policy-expert 6本→policy-domain-expert／旧実装系4本→policy-strategy-suite
- [サムネ・SNS画像はプロ級和文タイポで組む](feedback_thumbnail_pro_typography_default.md) — palt約物詰め＋カギ括弧ぶら下げ＋Hiragino W8/W9＋見出しlh1.16
- [サムネ制作は元写真を先に求める](feedback_thumbnail_ask_base_photo_first.md) — 第一手＝base写真の有無を1回確認。EYES-FIRST共通
- [家庭用プリンタ回はインク節約版を別途用意](feedback_home_printer_ink_saving_variant.md) — CSS配色だけ差し替え・本文レイアウトは触らない
- [印刷物は確定前に必ずnatural-design-reviewerを通す](feedback_design_review_gate_no_skip.md) — 修正版・構造変更後も通す
- [地域/子どもチラシは明るく柔らかいイラスト路線](feedback_flyer_bright_illustration_style.md) — 淡色＋余白＋水彩花＋キャラ。QRは本物合成→cv2デコード検証
- [自作スキルは ~/.claude/skills/ のみ](feedback_skills_home_not_plugin_cache.md) — plugins cache禁止。sync-to-git.shにガード実装済
- [Notion SQLクエリはプラン限定ブロック](feedback_notion_sql_plan_gate.md) — query-data-sources(SQL)使用禁止・viewはフィルタ欠落の罠
- [Discord夜間triageの途中死は登録済み×カーソル未前進を残す](feedback_discord_triage_partial_write_resume.md) — 再処理夜は📮投げ込み台帳(7a444c29-)をmsg_idで引く
- [システムの法則＝自動トリガー有=生/記憶依存の締め=腐る](feedback_system_closing_loops_rot.md) — 締め工程を定時トリガーに載せる
- [日中メモの捕捉面はDiscord bot DM一本](feedback_daily_capture_discord_dm.md) — 夜間3:10 triageが自動振り分け。Keep EOD貼り付けは廃止
- [市政報告会の声の自動記録](feedback_shisei_houkokukai_voice_capture.md) — 🎤報告会DB「主な意見・要望」欄＋Todoist「〇〇地区フォロー」箱(要整理ラベル)
- [親子で米づくり事業の正しい主催表記](project_oyakode_kometukuri.md) — 亀山JC主催。「個人主催」表記禁止
- [昼生お花見コミバス企画の主催表記](feedback_ohanami_hanyu_shusai_attribution.md) — 主催=昼生地区まちづくり協議会×市地域社会振興会。草川は参加・つなぎ役
- [市民意見DBはc2c34bd8に一本化](feedback_shimin_iken_db_consolidation_c2c34bd8.md) — 旧📋受付BOX`354432ec-`廃止
- [市民意見「経過報告」型返信メールの確定スタイル](feedback_citizen_reply_progress_report_style.md) — txt→open -e／冒頭フルネーム＋様・署名なし・【】見出し
- [市民SNS DM返信の確定スタイル](feedback_citizen_dm_reply_finalize_style.md) — 無知露呈禁止・遅延は冒頭お詫び・DMは署名なし・「本会議で」明示
- [エージェント部分ロードの根本原因](feedback_agent_registry_partial_load.md) — 原因=knowledge配下の入れ子.claude。再発時は`find ~/.claude/agents/knowledge -type d -name .claude`
- [一般質問設計の専任エージェント](feedback_general_question_architect_agent.md) — general-question-architect。時間逆算＋逃げ封じ
- [議案質疑/一般質問の本番原稿化](feedback_bill_scrutiny_scriptwriter_agent.md) — bill-scrutiny-scriptwriter＋honban_genko_craft_v1.md＋GOLD_太陽光条例
- [コンテンツ生成は常時lean full-agentがデフォルト](feedback_content_generation_default_flow.md) — 主担当agent省略禁止、目標90〜170K
- [SNS投稿文案で草川の行動を言い切らない](feedback_sns_no_action_promise_assertions.md) — 「取り上げます」等の約束を断定で書かない→「〜したい」。事実・数字の断定は可
- [「次の議会で追及」型表現を軽々に使わない](feedback_no_aggressive_pursuit_phrases.md) — 特定議会×対決動詞禁止
- [issues返信は記録不要](feedback_issues_response_no_log.md) — 「賛成」「反対」冒頭の意見は保存/タスク化省略、返信3案だけ
- [ブログ定型フッターに◆AIインタビュー常設](feedback_blog_footer_ai_interview_link.md) — Threadsの後にdepth-interview-kusagawaリンク
- [コピペ前提原稿は毎回コピペ即可の書式で出す](feedback_copypaste_draft_delivery.md) — 形式を聞き返さない。既定=drafts/に1案1txt→open -e＋チャットは`>`や・なしのフラット塊
- [Notion内部リンクは mention-page タグ必須](feedback_notion_link_deeplink.md) — markdownリンクはモバイルでブラウザに飛ぶ
- Notion update_content/DSLの罠 — [落とし穴](feedback_notion_update_content_pitfalls.md)／[罠v2](feedback_notion_update_content_pitfalls_v2.md)timeout後も適用済・即リトライ禁止／[DSLステータスフィルタ書込不可](feedback_notion_dsl_status_filter_limitation.md)
- [notion-saver保存後は漢字化け実体確認必須](feedback_notion_saver_kanji_garble_verify.md) — お風呂→お風坂等の実体破損あり。fetch検証→replace_content全置換
- ブログ/SNS DBステータス＆URL — [選択肢3種](feedback_blog_sns_db_status_options.md)／[3DB view_url](feedback_3db_view_url_correction.md)／[SNS DB v2 ds=1bd98deb](feedback_3db_view_url_correction_v2.md)
- [仕上げモードU4後に日次ログ追記必須](feedback_nichijo_finalize_log_append.md)／[会議体マスタの網羅性不足対策](feedback_meeting_master_coverage.md)
- [議会公務の会議資料は📅ミーティングノートDB配下](feedback_council_meeting_db_placement.md) — 期別フォルダでなくMTGノートDB＋会議体マスタ紐付け
- [声のDNA抽出時の注意](feedback_voice_dna_extraction.md) — AI生成の定型句を真の声と誤認しない
- [市民相談→タスク登録連携](feedback_citizen_inquiry_task_registration.md)／[禁止用語リスト（現在は空）](feedback_forbidden_words.md)
- [content-pipeline配下エージェントのグローバル登録必須](feedback_content_pipeline_agent_registration.md) — ~/.claude/agents/ 配置
- [写真＋動画入力はphoto-postフルを最初から回す](feedback_photo_video_input_run_full_pipeline.md) — 写真は必ずRead確認（取り違え防止）
- [Notion会議ページ→カレンダー登録時は元ページ削除まで自走](feedback_notion_meeting_to_calendar.md)
- [議事録は草川発言＋市回答のみ抽出](feedback_giji_kusagawa_response_only.md) — voice-dna汚染防止＋トークン節約
- [5/27子ども医療費は誤帰属あり](feedback_kodomo_iryohi_sns_misattribution.md) — 3月議会医療費質疑は草川でなく福沢議員
- [濁り水断水の給水描写は深水議員(3番)発言](feedback_fukami_water_distribution_misattribution.md) — 2,700世帯/11月/12月は草川由来OK
- [他議員の名前は対外発信物に載せない](feedback_no_other_council_members_names.md) — 内部資料はOK
- スライド制作 — [通常はNotebookLM経由必須](feedback_slide_generation_via_notebooklm.md)／[市政報告会のみClaude Code HTML/CSS→PDF](feedback_shisei_houkokukai_slides_claude_code.md)
- [架空エピソード・つくり話禁止](feedback_no_fabricated_stories.md) — 実体験/一次情報/公式データのみ
- [アーカイブgrepは話題ワード＋草川独自表現を並列で](feedback_archive_grep_keyword_expansion.md) — 「乗って残す」等の草川語彙を引き忘れない
- [返信文でのおうむ返し禁止](feedback_no_parroting_in_replies.md) — 自分の反応→決意→約束で組み立てる
- [確認は最初に1回束ねる・入力にある情報は最初から反映](feedback_ask_bundling_and_upfront_reflection.md) — 2026-07-31草川「台本遅いよ、なんで最初から反映しないの」。単位不明の数値は勝手に落とさず初回確認に混ぜる／安全ゲート指摘は自分で潰せる分を潰してから出す／締切当日案件は確認1回まで
- [タスク登録は保存先＋期限を提示→本人回答後に保存](feedback_ask_destination_and_deadline_before_register.md) — 既定値で勝手に登録しない（[[feedback_task_deadline_3days]]の+3日は推奨案に降格）
- [✅タスクDB Pending／保留系3区分](feedback_task_db_pending_status.md) — Pending/Wish List/Waiting
- [brainstormingのトークン浪費パターン](feedback_brainstorming_token_efficiency.md) — 同内容md多重生成禁止、design docは3000字以内
- [「亀山」typo再発防止](feedback_kameyama_kanji_typo_guard.md) — JSONのunicode escape禁止・日本語は直接書く
- [議会・他議員への提言は対外発信で避ける](feedback_no_council_directed_proposals.md) — 提案宛先は執行部に限定
- [草川 役職・所属委員会マスタ](feedback_kusagawa_role_committee_master.md) — 教育民生委員会の委員（確定）
- 禁止表現集 — [「届かないを終わらせる」](feedback_phrase_todokanai_owaraseru.md)／[「届かなくても届く」](feedback_phrase_todokanakutemo_todoku.md)／[距離比喩](feedback_metric_distance_metaphor_avoid.md)／[抽象・詩的比喩](feedback_no_abstract_poetic_phrases.md)／[つくり話冒頭](feedback_no_halfbaked_story_openings.md)／[空虚な問いかけ風](feedback_no_hollow_rhetorical_questions.md) — 全面禁止・断定と行為語で書く
- [「亀山42% vs 100%」は介護保険・子育てではない](feedback_kameyama_42pct_kaigo_not_childcare.md) — 子育て・保育・教育文脈で使用禁止
- [子育てDX「遅れ」フレームは前面禁止](feedback_kosodate_dx_delay_risky_frame.md) — 「制度はある。問題は運用」に絞る
- [SNS1行目に免責文を置くとフックが死ぬ](feedback_sns_disclaimer_kills_hook.md) — 冒頭は必ずフック・7PF同一原稿禁止
- [LINE公式で第三者団体の署名・動員を呼びかけない](feedback_line_koenkai_no_third_party_mobilization.md) — 後援会→署名の逆流は未担保
- [発信物で絵文字を使わない](feedback_no_emoji_ai_smell.md) — 見出し装飾はCSSライムバー/角マーカー/ピル
- [フォーム回答の属性帰属はoperational contextで判定](feedback_form_response_no_attribution_guess.md) — 過剰な「念のため確認」は信頼損なう
- [ご意見箱の声の引用は属性を付けない](feedback_goikenbako_quote_no_attributes.md) — 年代・地域を添えず本文のみ
- [団体名義SNSの同意を個人政治ブログに移植しない](feedback_consent_scope_org_to_personal_blog.md) — 器が変われば取り直す
- 中学校給食 — [既に実施開始済](feedback_kameyama_chugakko_kyushoku_already_started.md)／[選択制回帰の切り取り注意](feedback_kyushoku_sentakusei_kaiki_misread_guard.md)／[SNS/AI先行調査](feedback_kyushoku_sns_research_first.md)
- [通告書ドラフト→確定版の推敲パターン](feedback_tsukokusho_finalization_pattern.md) — 議案質疑は簡潔・名詞止め／一般質問は答弁者を具体指定
- [一般質問テーマ選定の優先序列](feedback_ippan_shitsumon_theme_priority.md) — 地域と約束＞会派協議中＞市民の声＞当事者性

## 🔗 外部参照ポインタ

- [景観保全作物の種子配付／田園環境保全事業の廃止年度](reference_keikan_hozen_seed_haishi.md) — 廃止は**令和7年度**・申請は**農業者要件**（要件を誤ると利益相反の説明が崩れる）・昼生7自治会は「神向谷」表記

- [ファイル管理システムv4 保存先マップ](reference_storage_map.md) — 用途→正規置き場の正本。夜間パイプラインv4・00_名簿区画・週次スイープ
- [R8.6.15半導体の世界の亀山 議場確定事実](reference_r8615_handotai_floor_facts.md) — 旗は櫻井市長・草川は後押し役
- [防災発信の定番リンク集5本](reference_bosai_link_collection.md) — 気象庁(亀山2421000)/川の防災/防災みえ/名阪国道規制/中電停電
- [草川議会質問アーカイブv3構造](reference_drive_archive_kusagawa.md) — 学習層1088件、grep対象は01_council〜06_election
- [claude-configバックアップ](reference_claude_config_backup.md) — GitHub thiguchi125-debug/claude-config、復元はrestore.sh
- [スキルトリガー一覧](reference_skill_triggers.md)／[エージェントトリガー一覧](reference_agent_triggers.md) — Notion早見表
- [市民の声Googleフォーム3シート＋ETL分類済資産](reference_市民の声情報源.md) — 2021/06〜359件、6ドメイン分類済
- [亀山市コミバス運賃](reference_kameyama_combus_fare.md)／[コミバス・のりかめさん収支](reference_kameyama_combus_revenue.md) — 収支率4.8%（R3）
- [✅タスクDB クイック登録](reference_task_db_quick_create.md) — ds=292cf503-a68f-81c6-b9dd-000b3ffdd2ce
- [自治会・地区別市政報告会スライド作成プレイブック](reference_jichikai_shisei_houkokukai_playbook.md) — 地区別ニュース62本・標準WF
- [亀山市議会 一般質問の標準時間](reference_kameyama_general_question_time.md) — 答弁込み45分
- [太岡寺自治会 太陽光要望書（R5.12.12）](reference_taikoji_yobosho_taiyoko.md) — 村山竹則会長／条例の早期策定要請
- [亀山市新庁舎 開庁=令和18年度（2036）](reference_shincho_kaicho_r18.md) — 「令和12年度」は旧計画＝誤り
- [次期ごみ処理施設](reference_jiki_gomi_shori_shisetsu.md) — 現炉R14年度末終了→次期R15年度稼働・48t/日・271〜307億・**建設地は未定**
- [選挙リーフレットv3 ファイル群](reference_senkyo_leaflet_v3_files.md)／[朝の街頭活動場所9拠点](reference_morning_street_locations.md)
- [一般質問 制作物のDrive保存先](reference_ippan_shitsumon_seisaku_drive.md) — `ZZ_一般質問制作/R0X/YYYY-MM_◯月議会/`
- [Discordチャンネル起動フラグ](reference_discord_channel_launch_flag.md) — 正=`claude --channels plugin:discord@claude-plugins-official`

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

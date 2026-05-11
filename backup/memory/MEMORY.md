# Memory Index

> エージェント/スキル/DB の「新設告知」は本体ファイルに統合済みのため index から外し、個別 .md は memory/ 配下に保持（on-demand 参照可）。
> 直近の進行中案件 / 反復で効くガードルール / 外部参照ポインタ のみここに常駐。
> 完全な過去ログは `_backup_<日付>/MEMORY.md` を参照。

## 🔄 進行中プロジェクト

- [oyasumi v2 (cron化＋自動展開＋仕上げ統合)](project_oyasumi_v2_cron_autoexpansion.md) — 2026-05-08実装完。routine `trig_01TbZU1pJDecnG4QmZKosz72` 毎晩22時JST。Drive/ミーティング→質問ネタ／タスク自動展開、仕上げA/B/C統合、燃費200K→160〜190K
- [マイドライブ全件取込v1](project_mydrive_full_intake.md) — 2026-05-05実施中。255件中108件取込済、残147件はsubagent rate limit reset(4pm JST)後resume
- [oyasumi Step 9 過去ページ漸進棚卸し](project_oyasumi_step9_past_cleanup.md) — 旧情報DB配下を毎晩3件ずつ自動整理、約34日で完了予定
- [Drive→ローカル同期v2拡張＋議会モード](project_drive_sync_v2.md) — Routine週2回(水日21時JST)、_INBOX_新規投函への投入運用、council-mode-toggleで議会期日次切替
- [Notion埋没ページ大掃除2026-05-05](project_notion_buried_pages_2026-05-05.md) — Phase 1本文化(90件)レート制限中断中(3am JST復帰)、Phase 2-3は草川判断待ち
- [3本柱 v0 ハンドオフ](../../../agents/knowledge/kusagawa_archive/04_compass/3pillars/v0_handoff.md) — v0草案完成、次の一手は6ドメインexpert並列起動
- [親子で米づくり事業の正しい主催表記](project_oyakode_kometukuri.md) — 亀山JC主催・草川がJC理事長時代に企画／2026第2回でJC継続事業化、「個人主催」表記禁止
- [議会資料管理システム Phase 1〜4](project_council_materials_management.md) — 2026-05-11設計、Drive新規11フォルダ作成完了、草川手動アクション3件保留、Phase 2スクリプト拡張は次回セッション

## 📌 恒久ガードルール（実運用で効く feedback）

- [コンテンツ生成は常時lean fullーagentがデフォルト](feedback_content_generation_default_flow.md) — 主担当agent省略禁止、lean最適化は毎回適用、目標90〜170K
- [「次の議会で追及」型の表現を軽々に使わない](feedback_no_aggressive_pursuit_phrases.md) — 特定議会×対決動詞の組合せ禁止、継続的取り組みは「継続的フォロー」「対話を重ねる」で表現
- [ブログは市民情報伝達と政策論考を分けて書く](feedback_blog_citizen_first.md) — モードA/B判定後に書き始める
- [街頭演説は選挙文脈を引っ込め政策の中身を厚く](feedback_street_speech_no_election_focus.md) — 投票日・期数・「もう一度」最小化、数字と運用詳細を厚く
- [街頭演説の本論は政策分野を意図的に分散](feedback_street_speech_topic_diversity.md) — 5ドメイン以上から候補リストアップ後に組立
- [issues返信は記録不要](feedback_issues_response_no_log.md) — 「賛成」「反対」冒頭の意見はNotion保存/タスク化省略、返信3案だけ
- [動画原稿の保存先は📣SNS投稿管理DBで統一](feedback_video_script_save_destination.md) — 専用DB作らず投稿管理DBに集約、タイトル先頭🎬
- [AIインタビュー紹介SNSの定型クレジット必須](feedback_ai_interview_disclaimer.md) — 安野貴博・有賀啓介クレジット＋個人情報禁止注意を4PFに必須
- [Notion内部リンクは mention-page タグ必須](feedback_notion_link_deeplink.md) — `<mention-page url="...">タイトル</mention-page>` 形式（普通のmarkdownリンクはモバイルでブラウザに飛ぶ）
- [Notion update_content の落とし穴](feedback_notion_update_content_pitfalls.md) — 複数セクション一括置換でサイレント失敗、fetch検証＆固有名詞コピペ徹底
- [Notion update_content の罠 v2](feedback_notion_update_content_pitfalls_v2.md) — timeout後でも実は適用済が多い、即リトライ禁止、fetchキャッシュが古いケースあり（2026-05-10）
- [Notion view-DSLのステータス型フィルタ書込不可](feedback_notion_dsl_status_filter_limitation.md) — Done/Archive除外フィルタは草川手動追加
- [ブログ／SNS DBのステータス選択肢](feedback_blog_sns_db_status_options.md) — 未着手/進行中/完了のみ、「下書き完成」無いので進行中で代用
- [仕上げモードU4後に日次ログ追記必須](feedback_nichijo_finalize_log_append.md) — 仕上げ生成物が日次ログに自動反映されない仕様の穴
- [ohayo/oyasumi タスクDB実クエリ必須](feedback_ohayo_oyasumi_task_db_query.md) — 旧表流用禁止、view直叩きで本日inbox包含
- [ohayo トークン効率化方針](feedback_ohayo_token_efficiency.md) — 本文置換省略・チャット集約、filter付きview作成で根本対処
- [ohayo トークン効率化 v3](feedback_ohayo_token_efficiency_v3.md) — 本朝120K消費の根因分析、timeout後即リトライ禁止／fetch1回限定／本文置換完全停止／目標70〜90K（2026-05-10）
- [oyasumi トークン効率化方針](feedback_oyasumi_token_efficiency.md) — Drive pageSize10/read1500字/Notion pageSize30、SKILL.md冒頭⚡原則反映済み（2026-05-07）
- [3DB view_url再設定（SNS／一般質問ネタ／市民意見）](feedback_3db_view_url_correction.md) — page URLのみで?v=不在＋廃止DB参照の二重ミス、2026-05-08確定（oyasumi SKILL.md反映済み）
- [📣SNS投稿管理DB v2 確定情報](feedback_3db_view_url_correction_v2.md) — data_source_id=1bd98deb-、ステータスは未着手/進行中/完了（「未投稿」は誤記）、2026-05-10再点検
- [会議体マスタの網羅性不足対策](feedback_meeting_master_coverage.md) — マスタ4件しかなく未紐付発生、単発講演も登録、志事塾追加済、2026-05-10
- [news-briefing 鮮度チェック必須（Yahoo検索キャッシュ罠）](feedback_news_briefing_freshness_check.md) — Yahoo検索は日付修飾効かず・7日で記事削除、必ずWebFetchで本体実在＋配信日確認してからDB登録（2026-05-08事故）
- [ohayo に archive grep 連動を組み込み（v2.2）](feedback_ohayo_archive_grep_integration.md) — news-briefing単独だと過去発言連動が抜ける、cron停止時の耐障害性確保のためohayo側に組込（2026-05-08）
- [1日のルーティンを別ページに独立化](feedback_routine_independent_page.md) — ダッシュボードのチェックボックスリストを「📅 毎日のルーティン（改訂版）」34acf503-に独立化、ohayoは本セクションに一切書込まず燃費数K削減（2026-05-08）
- [ohayo v2.1 街頭演説／ブログSNSテーマ提案](feedback_ohayo_v21_speech_blog_themes.md) — 🎯フォーカス直後に🎤3案＋📝発信テーマ、提案のみ／本文化は下流／チャット限定／追加fetchゼロ
- [ニュースDBクエリの落とし穴](feedback_news_db_query_pitfall.md) — view_url直叩きしないと未検出、data_source_url の database/data_source 取り違え注意
- [ニュースブリーフィングは件数より質](feedback_news_briefing_quality_over_quantity.md) — 5〜7件厳守／過去7日重複排除／国政は俯瞰解説／議会活用メモ3点セット必須（v2 2026-05-06）
- [声のDNA抽出時の注意](feedback_voice_dna_extraction.md) — サンプル不足時にAI生成物の定型句を真の声として誤認しない
- [市民相談→タスク登録連携](feedback_citizen_inquiry_task_registration.md) — 次アクションを✅タスクDBへ親＋サブ階層化で登録候補提示
- [禁止用語リスト（現在は空）](feedback_forbidden_words.md) — 明示的な禁止語なし、市民向けは平易な日本語（一般原則）
- [content-pipeline配下エージェントのグローバル登録必須](feedback_content_pipeline_agent_registration.md) — blog-writer等は ~/.claude/agents/ 配置必須
- [Obsidianメモ確認](feedback_obsidian_memo.md) — タスク完了・スキル習得・トラブル解決時に確認
- [Notion会議ページ→Googleカレンダー登録時は元ページ削除まで自走](feedback_notion_meeting_to_calendar.md) — 「予定入れて」=Calendar登録＋アカウント明示＋元Notion削除依頼まで1パス
- [議事録は草川発言＋市回答のみ抽出](feedback_giji_kusagawa_response_only.md) — voice-dna汚染防止＋トークン節約（CLAUDE.mdに同主旨記載、詳細はファイル）
- [他議員の名前は対外発信物に載せない](feedback_no_other_council_members_names.md) — スライド/SNS/ブログ/印刷物等で他議員氏名禁止、汎用表記に置換、内部資料はOK（2026-05-09 草川直接指示）
- [スライド生成はNotebookLM経由が必須（直接生成禁止）](feedback_slide_generation_via_notebooklm.md) — Marp/Slidev等で直接生成しない、成果物は「ソース束＋プロンプト」の2点セット、NotebookLMがスライド本体を生成（2026-05-09 草川直接指示）
- [街頭演説は1テーマだけ深く掘る・詩的umbrella禁止](feedback_street_speech_one_theme_only.md) — 「1本」=複数話題の傘でなく1テーマ深掘り
- [街頭演説は鮮度基軸×蓄積layer構造](feedback_street_speech_recent_base_archive_layer.md) — 今日のホットニュース基軸＋過去archive層を乗せる
- [架空エピソード・つくり話禁止](feedback_no_fabricated_stories.md) — 「ある中学生が泣いた」型の感情演出は禁止、実体験/一次情報/公式データのみ
- [アーカイブgrepは話題ワード＋草川独自表現を並列で](feedback_archive_grep_keyword_expansion.md) — 「乗って残す」等の草川語彙を引き忘れない
- [返信文でのおうむ返し禁止](feedback_no_parroting_in_replies.md) — 相手が書いた事実（日付・年齢・固有エピソード）の反復はAI臭。自分の反応→決意→約束で組み立てる（2026-05-10）
- [ohayo タスクは「超過＋本日＋今週中」の3ブロック表示が標準](feedback_ohayo_task_3block_display.md) — 本日期限＋超過のみだと中期タスクが朝の視界から消える。3ブロック全件表示・件数絞り込み禁止（2026-05-11）
- [ohayo は期限なしinboxタスクを構造的に拾えない穴](feedback_ohayo_deadline_null_blindspot.md) — eスポーツサークル等の中期戦略タスクが期限未設定で朝視界外。登録時期限必須化＋月次棚卸し必要（2026-05-11）
- [タスクの期限は基本3日以内](feedback_task_deadline_3days.md) — ✅タスクDBへの新規登録時、明示指定がなければ`今日+3日`をデフォルト。遠い期限は朝の視界外＋先送りの温床（2026-05-11 草川直接指示）
- [ohayoのタスク監査シグナル（v2.3）](feedback_ohayo_task_audit_signal.md) — 5指標件数表示＋task-auditスキル誘導。閾値超え時のみ草川手動起動・cron化禁止（2026-05-11）
- [brainstormingセッションのトークン浪費パターン](feedback_brainstorming_token_efficiency.md) — 同内容md多重生成禁止、design docはPhase 1相当3000字以内、探索はサンプリング段階方式（2026-05-11）
- [「亀山」のtypo再発防止（亜山・亵山禁止）](feedback_kameyama_kanji_typo_guard.md) — AskUserQuestion等のJSONでunicode escape送信時に「亀」(U+4E80)を「亜」(U+4E9C)「亵」(U+4EB5)に取り違える事故。日本語は直接書く（2026-05-11）
- [ブログでの自己引用は慎重判断（禁止ではない）](feedback_blog_self_quote_careful.md) — 「私はずっと言ってきた」型は気持ち悪く見えがちだが、自分史記事・実績まとめ等で必要な場面もある。文脈で判断、デフォルトは事実と提案から書く（2026-05-11）
- [ブログ生成パイプラインのトークン効率化（推定400K→150K化）](feedback_blog_pipeline_token_efficiency.md) — リサーチ2並列デフォルト／字数厳守自動圧縮／草川目視前ゲート起動禁止／フレーズ強制継承禁止／1回保存（2026-05-11）
- [ブログ深掘りモードは最先端事例スキャンを書く前に必須](feedback_blog_depth_mode_latest_cases_required.md) — AI/DX等ドメイン専門領域は2025-2026最先端事例5本＋海外1本スキャン後に着手、テンプレ4本柱（段階導入/KPI/人材/県相乗り）は陳腐化サイン（2026-05-11）
- [議会・他議員に対する提言は対外発信物で避ける](feedback_no_council_directed_proposals.md) — 政策提案の宛先は執行部に限定、「議会全体／同僚議員」を動かす色は対外発信から外す、他自治体議会事例は中立紹介としてOK（2026-05-12）
- [ohayo 既発信重複除外チェック（v2.4）](feedback_ohayo_duplication_check.md) — 朝の発信テーマ提案前に投稿管理DB「完了」14日分と突合、既発信は除外or新規角度のみ提案、ショート動画系inbox期限超過は実質完了候補へ分離（2026-05-12）
- [news-briefing ハルシネーション検証ゲート（v2.5）](feedback_news_briefing_hallucination_guard.md) — 2026-05-12朝に部活動地域移行ニュースで古い記事+捏造を検出、登録前3点検証（URL先タイトル類似度/90日以内/本文整合）を必須化、ohayo側でも表示前URL先確認（2026-05-12）

## 🔗 外部参照ポインタ

- [草川議会質問アーカイブv3構造](reference_drive_archive_kusagawa.md) — 学習層1088件、grep対象は01_council〜06_election
- [claude-configバックアップ](reference_claude_config_backup.md) — GitHub thiguchi125-debug/claude-config、新PC復元はrestore.sh
- [スキルトリガー一覧Notion](reference_skill_triggers.md) — 草川用スキル早見表（Notion a0631315配下）
- [エージェントトリガー一覧Notion](reference_agent_triggers.md) — 草川用エージェント18本の発火ワード早見表
- [市民の声Googleフォーム3シート＋ETL分類済資産](reference_市民の声情報源.md) — 2021/06〜継続収集359件、6ドメイン分類済（_citizen_voice/配下）、Step A以降の施策発掘の必読源
- [亀山市コミバス運賃](reference_kameyama_combus_fare.md) — 小中学生以下100円・高校以上200円
- [亀山市コミバス・のりかめさん収支データ](reference_kameyama_combus_revenue.md) — コミバス運賃521万／委託1億／収支率4.8%（R3）、のりかめさん運賃248万／委託881万（R4）。無料化提案の論拠数字
- [✅タスクDB クイック登録](reference_task_db_quick_create.md) — data_source_id=292cf503-a68f-81c6-b9dd-000b3ffdd2ce、最小5プロパティでcreate1発、schema fetch不要
- [自治会・地区別市政報告会スライド作成プレイブック](reference_jichikai_shisei_houkokukai_playbook.md) — 地区別ニュース既存62本確認・一次資料群・03_themes/集約・標準WF・voice-dna辞書（2026-05-09 楠平尾v2セッションから集約）

## 🏛 主要DB／システム参照（呼出時のみ詳細を取りに行く）

- 政策コンパス: project_policy_compass.md — Origin Story「声を、チカラに。」3軸=伝える/繋ぐ/希望
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
- エージェント本体: ~/.claude/agents/ 配下（kameyama-researcher / community-rally-speaker / daily-street-speech / speech-writer / electoral-district-strategist / agenda-analyzer / counter-argument-simulator / video-content-strategist / short-video-virality-architect / sns-content-polisher / policy-archive-miner / policy-validator / design-director / design-inspiration-researcher / print-designer / photo-curator 等）

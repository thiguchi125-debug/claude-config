# Memory Index

> 進行中案件 / 反復で効くガードルール / 外部参照ポインタ のみ常駐。各.mdは memory/ 配下にon-demand保持。過去ログは `_backup_<日付>/MEMORY.md`。1行/エントリ厳守（~200字以内）、詳細は topic ファイルへ。同系統は束ね行（1行に複数リンク）で保持。

## 🔄 進行中プロジェクト

- [Notion大改修＋ohayo/news v3＋smart-intake](project_notion_ohayo_news_v3_renewal.md) — 2026-07-03実施。ohayo=150行v3・news=dedup+活用フック・smart-intake新設（投げ込み保存+「〇〇どこ？」検索・🔖台帳）・🗄️旧アーカイブ収容。翌朝ニュース重複停止とohayo初回実走の確認待ち
- [議会だより制作エージェント](project_gikai_dayori_creator.md) — gikai-dayori-creator整備完了(2026-07-02)。会議録→650字→提出docx＋引用参照マークdocxのフルパイプライン。スクリプト=~/.claude/scripts/gikai_dayori/。トリガー「議会だより作って」（要再起動）
- [Notionプロジェクト・プラットフォーム](project_notion_project_platform.md) — Todoist主要PJ対応の情報蓄積母艦DB（page=37a71464・ds=8975c6a9）。Todoist=実行/Notion=蓄積。初期17PJ投入済
- [Todoistへタスク管理移行](project_todoist_task_migration.md) — 完了。`python3 ~/.claude/scripts/todoist/td.py {morning/add/done/audit/list…}`（token=~/.config/todoist/token・API /api/v1/）。今後タスク/PJ登録は全てTodoist（Notion✅/🗂️は参照のみ）
- [2026年6月議会 一般質問prep](project_ippan_shitsumon_2026-06_resume.md) — 通告書6/2提出済・骨子v7確定。①部活再構成②送迎は利用率型③シャープ=市長への大きな一問（前提是正済[[reference_sharp_kameyama_factory_facts]]）。次=counter-argument-simulatorで全6中項目の戦闘マニュアル
- [3本柱 v0 ハンドオフ](../../../agents/knowledge/kusagawa_archive/04_compass/3pillars/v0_handoff.md) — v0草案完成。【🟡要判断 選挙公約に効くか草川判断待ち】
- [議会資料管理システム Phase 1〜4](project_council_materials_management.md) — Drive11フォルダ作成済・手動3件保留。【🟡要判断 復活/畳む待ち】
- [Drive同期クラウドRoutine 停止検討](project_drive_sync_v2.md) — cron冗長疑い。【🟡要判断 停止可否待ち】議会モード廃止済[[feedback_system_closing_loops_rot]]

## 📌 恒久ガードルール（実運用で効く feedback）

- [デザイン品質基準=中庄夏祭りポスター2026](feedback_design_quality_bar_natsumatsuri2026.md) — 全デザイン制作物はこの水準以上。参照忠実再現・グリフ単位検品・レイヤー順・EYES-FIRST・完成処理込み。見本=drafts/2026-08_中庄夏祭りポスター
- [イベント運営段取り表はスマホ縦スクロールPDF](feedback_event_runsheet_mobile_pdf_format.md) — 幅390px1ページ縦長・カード型・絵文字なし。A4/長尺PNGはNG。実測+200px・/Count=1まで高さ探索。個人情報は見出し＋名に注意書き
- [ohayoダッシュボードのタスク/PJ欄もTodoist由来に](feedback_ohayo_dashboard_task_project_todoist.md) — 朝の✅今日のタスク/🔗進行中PJはtd.pyから。Notion紐付け・mention-page張らない
- [システムの法則＝自動トリガー有=生/記憶依存の締め=腐る](feedback_system_closing_loops_rot.md) — 締め工程を定時トリガーに載せる・機械可読な一次情報から自動導出
- [市政報告会の声の自動記録](feedback_shisei_houkokukai_voice_capture.md) — 「記録：〇〇報告会で△△の声」で🎤報告会DB「主な意見・要望」欄＋Todoist「〇〇地区フォロー」箱(要整理ラベル)
- [親子で米づくり事業の正しい主催表記](project_oyakode_kometukuri.md) — 亀山JC主催・草川がJC理事長時代に企画。「個人主催」表記禁止
- [昼生お花見コミバス企画の主催表記](feedback_ohanami_hanyu_shusai_attribution.md) — 主催=昼生地区まちづくり協議会×市地域社会振興会。草川は参加・つなぎ役、手柄横取り印象回避／市民実名は対外伏せる
- [市民意見DBはc2c34bd8に一本化](feedback_shimin_iken_db_consolidation_c2c34bd8.md) — 正本は📝市民意見リスト`c2c34bd8-`のみ。旧📋受付BOX`354432ec-`廃止。対応状況status廃止
- [市民意見「経過報告」型返信メールの確定スタイル](feedback_citizen_reply_progress_report_style.md) — txt→open -e／冒頭フルネーム＋様・署名なし・「平素より〜」開始・【】見出し・「おっしゃる通り」で受ける
- [市民SNS DM返信の確定スタイル](feedback_citizen_dm_reply_finalize_style.md) — 無知露呈禁止・現場情報は「大事な現場の課題」・遅延は冒頭お詫び・DMは署名なし・「本会議で」明示・「議会で継続して追いかけます」
- [エージェント部分ロードの根本原因と修理記録](feedback_agent_registry_partial_load.md) — 原因=agents/knowledge配下の入れ子.claude/agent-memoryがレジストリ汚染。2026-07-02隔離修理済。再発時は`find ~/.claude/agents/knowledge -type d -name .claude`
- [印刷物レイアウトはprint-layout-architectに任せる](feedback_print_layout_architect_agent.md) — 画像小/中途半端余白/文章を横に系の手戻り防止。地図大きく・text-beside-image2カラム・Chrome実画素確認反復
- [print-layout-architectが0ツールで停止→自分で実測ループ](feedback_print_layout_architect_stalls.md) — 空応答即停止。Chrome実測（scrollHeight−clientHeight=0）。`margin-top:auto`禁。横長地図はaspect-ratio+object-fit cover
- [一般質問設計の専任エージェント](feedback_general_question_architect_agent.md) — general-question-architect。時間逆算＋逃げ封じ（先に認めてから刺す）＋重複/既決チェック。出力＝設計書
- [議案質疑/一般質問の本番原稿化](feedback_bill_scrutiny_scriptwriter_agent.md) — bill-scrutiny-scriptwriter＋honban_genko_craft_v1.md＋GOLD_太陽光条例。設計→原稿化→counter-sim
- [ショート動画は最初からvirality-architectで](feedback_short_video_use_virality_architect_first.md) — 長尺NG・35〜45秒・1動画1メッセージ・冒頭1.5秒フック
- [ショート動画の説明図はHTML/CSS→PNG](feedback_short_video_infographic_html_to_png.md) — AI生成でなくChrome PNG化、ブランド色#c7ff4a/#1f5a3a/#0f3d27/#f3efe4厳守、完成PNGはDrive📱動画素材へ
- ショート動画挿入画像 — [字幕セーフ帯＋安っぽさ7信号](feedback_short_video_subtitle_safe_zone.md) 確定3ゾーン固定=上y0-1240/字幕帯y1240-1460(全画像共通の固定座標・中央寄せ禁止)/下y1460-・文字大きめ・のっぺり/2トーン/棒人間潰す／[専任agent+可読性フロア](feedback_short_video_image_designer_agent.md) short-video-image-designer・記号化/文字消失を潰す・主役72px+・EYES-FIRST／[確定デザイン仕様(往復ゼロ用)](feedback_short_video_insert_image_design_spec.md) 明るい配色基調(暗緑支配NG)・字幕帯y1150-1470固定・行間広く・文字主役級・孤立文字ゼロ・親しみ絵本調(女の子も)・テンプレ=knowledge/short_video_templates/insert_image_v1
- [草川ショート動画原稿のスタイルガイド](feedback_kusagawa_short_video_script_style.md) — 疑問→断定フック／1段落1メッセージ／共感「したこと、ありませんか」／具体3例／独自タグライン強制禁止／テキスト連続版優先
- [コンテンツ生成は常時lean full-agentがデフォルト](feedback_content_generation_default_flow.md) — 主担当agent省略禁止、lean毎回適用、目標90〜170K
- [「次の議会で追及」型表現を軽々に使わない](feedback_no_aggressive_pursuit_phrases.md) — 特定議会×対決動詞禁止、「継続的フォロー」「対話を重ねる」で表現
- [ブログは市民情報伝達と政策論考を分けて書く](feedback_blog_citizen_first.md) — モードA/B判定後に書き始める
- 街頭演説 — [選挙文脈引込め政策厚く](feedback_street_speech_no_election_focus.md)投票日・期数・「もう一度」最小化／[1テーマ深掘り](feedback_street_speech_one_theme_only.md)複数話題の傘でなく／[鮮度基軸×蓄積layer](feedback_street_speech_recent_base_archive_layer.md)今日のホットニュース＋archive層／[本論は分野分散](feedback_street_speech_topic_diversity.md)5ドメイン以上から組立
- [issues返信は記録不要](feedback_issues_response_no_log.md) — 「賛成」「反対」冒頭の意見はNotion保存/タスク化省略、返信3案だけ
- [コピペ前提原稿は納品形式を先に伺う](feedback_copypaste_draft_delivery.md) — コードブロックは左余白が入る。既定はtxt書出し→open -e（TextEdit全選択コピー）。「余白入らない」と断定しない
- [動画原稿の保存先は📣SNS投稿管理DB](feedback_video_script_save_destination.md) — 専用DB作らず集約、タイトル先頭🎬
- [Xは字数制限撤廃→長文可](feedback_x_no_char_limit.md) — X投稿は140字厳守やめ長文OK、内容充実。SNS生成時にX=長文と明示しエージェントの「140字厳守」を上書き
- [Xは1ツイート1メッセージ・リンクはリプライ](feedback_x_post_lean_one_message.md) — 字数制限なくても詳細詰め込み禁止。数字/制度詳細/副論点はブログへ逃がす、URLは本文でなくリプライ欄、演出削ぎ政策主体明示
- [SNSハッシュタグ定番](feedback_sns_hashtag_staples.md) — #草川たくや と #ええやん亀山 を必ず入れる。テーマタグ2〜3個と組み合わせる
- [AIインタビュー紹介SNSの定型クレジット必須](feedback_ai_interview_disclaimer.md) — 安野貴博・有賀啓介クレジット＋個人情報禁止注意を4PFに
- [Notion内部リンクは mention-page タグ必須](feedback_notion_link_deeplink.md) — `<mention-page url="...">タイトル</mention-page>`（markdownリンクはモバイルでブラウザに飛ぶ）
- Notion update_content/DSLの罠 — [落とし穴](feedback_notion_update_content_pitfalls.md)複数セクション一括でサイレント失敗・fetch検証＆固有名詞コピペ／[罠v2](feedback_notion_update_content_pitfalls_v2.md)timeout後も適用済・即リトライ禁止・fetchキャッシュ古い／[DSLステータスフィルタ書込不可](feedback_notion_dsl_status_filter_limitation.md)Done/Archive除外は草川手動
- [notion-saver保存後は漢字化け実体確認必須](feedback_notion_saver_kanji_garble_verify.md) — お風呂→お風坂等の実体破損あり。「表示上の問題」の自己弁明を信じずfetch検証→replace_content全置換
- ブログ/SNS DBステータス＆URL — [選択肢](feedback_blog_sns_db_status_options.md)未着手/進行中/完了のみ・「下書き完成」無く進行中代用／[3DB view_url再設定](feedback_3db_view_url_correction.md)page URLのみ?v=不在・廃止DB参照ミス／[SNS DB v2](feedback_3db_view_url_correction_v2.md)ds=1bd98deb・「未投稿」は誤記
- [仕上げモードU4後に日次ログ追記必須](feedback_nichijo_finalize_log_append.md) — 仕上げ生成物が日次ログに自動反映されない穴
- [ohayo/oyasumi タスクDB実クエリ必須](feedback_ohayo_oyasumi_task_db_query.md) — 旧表流用禁止、view直叩きで本日inbox包含
- ohayo燃費（歴史的経緯・**v3全面書き直しで構造解決済 2026-07-03**） — [効率化](feedback_ohayo_token_efficiency.md)／[v3](feedback_ohayo_token_efficiency_v3.md)timeout後即リトライ禁止は現役／[v2.5](feedback_ohayo_v25_streamline.md)
- [oyasumi トークン効率化方針](feedback_oyasumi_token_efficiency.md) — Drive pageSize10/read1500字/Notion pageSize30
- [会議体マスタの網羅性不足対策](feedback_meeting_master_coverage.md) — マスタ少なく未紐付発生、単発講演も登録
- [議会公務の会議資料は📅ミーティングノートDB配下](feedback_council_meeting_db_placement.md) — 議案分析・委員会説明会・所管事務調査は期別フォルダでなくMTGノートDB＋会議体マスタ紐付け
- news-briefing — [鮮度チェック](feedback_news_briefing_freshness_check.md)WebFetchで本体実在＋配信日確認後DB登録／[DBクエリ落とし穴](feedback_news_db_query_pitfall.md)view_url直叩き・database/data_source取違え／[件数より質](feedback_news_briefing_quality_over_quantity.md)5〜7件・過去7日重複排除・国政俯瞰／[ハルシ検証ゲート](feedback_news_briefing_hallucination_guard.md)登録前3点検証／[v3重複検出(手動編集要)](feedback_news_briefing_v3_duplicate_detection.md)30日窓3層判定
- [ohayo に archive grep 連動](feedback_ohayo_archive_grep_integration.md) — news-briefing単独だと過去発言連動が抜ける、ohayo側に組込
- [1日のルーティンを別ページに独立化](feedback_routine_independent_page.md) — 「📅毎日のルーティン（改訂版）」34acf503-に独立、ohayoは書込まず燃費削減
- [ohayo v2.1 街頭演説／ブログSNSテーマ提案](feedback_ohayo_v21_speech_blog_themes.md) — 🎯直後に🎤3案＋📝発信テーマ、提案のみ・チャット限定
- [ohayo→daily-content-generator連結はB型](feedback_ohayo_daily_content_generator_prompt.md) — トリガー成立時のみ末尾「💫フルパッケージ作る？」1行、自動連結禁止
- [声のDNA抽出時の注意](feedback_voice_dna_extraction.md) — サンプル不足時にAI生成の定型句を真の声と誤認しない
- [市民相談→タスク登録連携](feedback_citizen_inquiry_task_registration.md) — 次アクションを親＋サブ階層化で登録候補提示
- [禁止用語リスト（現在は空）](feedback_forbidden_words.md) — 明示的な禁止語なし、市民向けは平易な日本語
- [content-pipeline配下エージェントのグローバル登録必須](feedback_content_pipeline_agent_registration.md) — blog-writer等は ~/.claude/agents/ 配置
- [Obsidianメモ確認](feedback_obsidian_memo.md) — タスク完了・スキル習得・トラブル解決時に確認
- [Notion会議ページ→カレンダー登録時は元ページ削除まで自走](feedback_notion_meeting_to_calendar.md) — Calendar登録＋アカウント明示＋元Notion削除依頼まで1パス
- [議事録は草川発言＋市回答のみ抽出](feedback_giji_kusagawa_response_only.md) — voice-dna汚染防止＋トークン節約
- [5/27子ども医療費は誤帰属あり](feedback_kodomo_iryohi_sns_misattribution.md) — 3月議会医療費質疑は草川でなく福沢議員。逐語禁止、全国90.5%は「市の調査」で中立可。確定版=drafts/2026-06-03_子ども医療費18歳まで_v3.md
- [濁り水断水の給水描写は深水議員(3番)発言](feedback_fukami_water_distribution_misattribution.md) — 給水車2台等は深水議員。草川は被害アンケート/水質見える化/管路老朽化。2,700世帯/11月/12月は草川由来OK
- [他議員の名前は対外発信物に載せない](feedback_no_other_council_members_names.md) — スライド/SNS/ブログ/印刷物で他議員氏名禁止、汎用表記に。内部資料はOK
- スライド制作 — [通常はNotebookLM経由必須](feedback_slide_generation_via_notebooklm.md)Marp/Slidev直接生成しない・ソース束＋プロンプト2点／[市政報告会スライドは例外=Claude Code(HTML/CSS→PDF)](feedback_shisei_houkokukai_slides_claude_code.md)御幸/小下/木下テンプレ地区化・16:9・草川カラー・2ゲート・見本=木下版
- [架空エピソード・つくり話禁止](feedback_no_fabricated_stories.md) — 感情演出禁止、実体験/一次情報/公式データのみ
- [アーカイブgrepは話題ワード＋草川独自表現を並列で](feedback_archive_grep_keyword_expansion.md) — 「乗って残す」等の草川語彙を引き忘れない
- [返信文でのおうむ返し禁止](feedback_no_parroting_in_replies.md) — 相手が書いた事実の反復はAI臭。自分の反応→決意→約束で組み立てる
- [ohayo タスクは超過＋本日＋今週中の3ブロック表示](feedback_ohayo_task_3block_display.md) — 全件表示・件数絞り込み禁止
- [ohayo は期限なしinboxタスクを拾えない穴](feedback_ohayo_deadline_null_blindspot.md) — 期限未設定で朝視界外。登録時期限必須＋月次棚卸し
- [タスクの期限は基本3日以内](feedback_task_deadline_3days.md) — 明示指定なければ今日+3日デフォルト（提示し回答待ち＝下記で上書き）
- [登録前に保存先と期限を毎回尋ねる](feedback_ask_destination_and_deadline_before_register.md) — 保存先＋期限を本人に尋ね回答を得てから保存。既定値で勝手に登録しない
- [✅タスクDB Pending／保留系3区分](feedback_task_db_pending_status.md) — Pending=実行に検討要／Wish List=追加対応なし／Waiting=相手待ち。status追加はUI手動のみ
- [ohayoのタスク監査シグナル](feedback_ohayo_task_audit_signal.md) — 5指標件数＋task-auditへ誘導。閾値超え時のみ手動起動・cron化禁止
- [brainstormingのトークン浪費パターン](feedback_brainstorming_token_efficiency.md) — 同内容md多重生成禁止、design docは3000字以内、探索はサンプリング段階
- [「亀山」typo再発防止（亜山・亵山禁止）](feedback_kameyama_kanji_typo_guard.md) — JSONのunicode escapeで「亀」(U+4E80)取り違え事故。日本語は直接書く
- ブログ自己引用/振り返り — [自己引用は慎重](feedback_blog_self_quote_careful.md)「私はずっと言ってきた」型は文脈判断・デフォルトは事実と提案／[過去発言一覧導入回避](feedback_blog_past_arguments_recap_avoid.md)新フェーズ提案として直接書出す
- [ブログ生成パイプラインのトークン効率化](feedback_blog_pipeline_token_efficiency.md) — リサーチ2並列／字数厳守自動圧縮／前ゲート起動禁止／1回保存
- [ブログ深掘りは最先端事例スキャンを書く前に必須](feedback_blog_depth_mode_latest_cases_required.md) — AI/DX等は2025-2026事例5本＋海外1本後に着手、テンプレ4本柱は陳腐化サイン
- [議会・他議員への提言は対外発信で避ける](feedback_no_council_directed_proposals.md) — 提案宛先は執行部に限定、他自治体議会事例は中立紹介でOK
- [ohayo 既発信重複除外チェック](feedback_ohayo_duplication_check.md) — 提案前に投稿管理DB「完了」14日分と突合、既発信除外or新規角度のみ
- [草川 役職・所属委員会マスタ](feedback_kusagawa_role_committee_master.md) — 教育民生委員会の委員（確定）。「傍聴」等の立場逸脱表現を排除
- [ohayo 必須セクション実行チェックリスト](feedback_ohayo_section_execution_checklist.md) — 実行漏れ多発、内部TodoListで18セクション管理、全件完了まで出力禁止
- 禁止表現集 — [「届かないを終わらせる」](feedback_phrase_todokanai_owaraseru.md)結び/見出し禁止／[「届かなくても届く」](feedback_phrase_todokanakutemo_todoku.md)代替=申請しなくても届く/先回りする行政／[距離比喩「最後の100m/ラスト1マイル」](feedback_metric_distance_metaphor_avoid.md)行為語で書く／[抽象・詩的比喩](feedback_no_abstract_poetic_phrases.md)情緒メタファー全面禁止／[つくり話・ストーリー冒頭](feedback_no_halfbaked_story_openings.md)事実＋呼びかけから直接／[当たり前を問いかけ風で飾らない](feedback_no_hollow_rhetorical_questions.md)断定で言い切る
- [「亀山42% vs 100%」は介護保険・子育てではない](feedback_kameyama_42pct_kaigo_not_childcare.md) — 子育て・保育・教育文脈で絶対使用禁止
- [子育てDX「遅れ」フレームは前面禁止](feedback_kosodate_dx_delay_risky_frame.md) — 亀山子育てDXは進んでいる側。運用ピンポイント（現金集金3費目/コドモン26機能）に絞る「制度はある。問題は運用」
- [SNSは市民生活のBefore/Afterシーン先行](feedback_sns_citizen_lifescene_first.md) — 事例・数字・固有名詞は冒頭NG、日常シーンで始め数字は中盤以降
- ohayoダッシュボード堆積 — [停止セクション残骸の自動削除](feedback_ohayo_stale_display_removal.md)毎朝Step4で9セクションスイープし空置換／[堆積＋日付誤認](feedback_ohayo_dashboard_accumulation_and_date.md)見出し＋本文を全置換・日付はdate実確認
- 印刷物処理 — [バイナリ素材は案件別サブフォルダ](feedback_publications_binary_storage.md)`<YYYY-MM>_<案件名>/`隔離・中間版は最終後削除／[PDF生成後自動open](feedback_auto_open_pdf_after_render.md)`open <絶対パス>`即実行・HTMLは自動openしない／[画像EXIF正規化](feedback_image_exif_processing.md)`PIL ImageOps.exif_transpose`+EXIF strip／[Drive図面挿入・QR並列・overflow段階圧縮](feedback_print_diagram_qr_layout.md)
- [市政報告レポート印刷物制作チェックリスト](feedback_print_publication_checklist.md) — A4両面のレイアウト/タイポ/写真/章順/安全ゲート/俯瞰レビュー統合。N+1イテレーション予防
- [後援会リーフレットデザイン原則](feedback_leaflet_design_principles.md) — 客観確認・元装飾尊重・段組勝手追加禁止・色統一・「規制→適正立地」・「討議資料」・写真300dpi
- [発信物で絵文字を使わない（AI臭い）](feedback_no_emoji_ai_smell.md) — 絵文字禁止、見出し装飾はCSSライムバー/角マーカー/ピル、制作後にコードポイント検査
- [eスポーツ協会チラシは公式ロゴTUIRTLEを必ず使用](feedback_esports_association_logo.md) — ロゴ正本=assets/esports_logo/logo_transparent.png。ダーク背景は淡ライム発光・別途コントローラー絵は重複NG
- [チラシの固いNGはAI製SaaS LP風のみ](feedback_flyer_avoid_ai_saas_aesthetic.md) — 禁止＝AI臭（紫グラデ/浮き角丸カード/絵文字丸アイコン/ピルバッジ/LP構図）。基調は内容毎に作り分け、特定スタイル標準化しない
- 印刷CSS/入稿 — [切れ字は個別nowrap限定](feedback_kirejiha_individual_nowrap.md)固有名詞だけ`white-space:nowrap`・汎用CSS変更禁止／[lime下線box-shadow inset](feedback_lime_underline_box_shadow.md)gradient hard-stopはPDFで暗化／[画像最適化](feedback_pdf_image_optimization.md)`sips -Z 1500 -s formatOptions 90`で300dpi／[ラクスル裏面ラスタライズ](feedback_rakusuru_back_rasterize.md)`pdftoppm -r 400`+PILで裏面JPEG化→再結合
- [フォーム回答の属性帰属はoperational contextで判定](feedback_form_response_no_attribution_guess.md) — 主語なし自由回答は運営文脈で自然な主体を選び即対応、過剰な「念のため確認」は信頼損なう
- 中学校給食 — [既に実施開始済](feedback_kameyama_chugakko_kyushoku_already_started.md)「過渡期/令和8年度2学期開始」フレーム全面禁止・補食は実施前提でも発生／[選択制回帰の切り取り注意](feedback_kyushoku_sentakusei_kaiki_misread_guard.md)価値として書き制度郷愁にしない・土台肯定＋「後戻りしません」セット・亀山モデル=公平×個別最適の両立・造語連呼3回まで／[SNS/AI先行調査](feedback_kyushoku_sns_research_first.md)声収集してから一体展開
- AIインタビュー由来発信 — [Instagram私的演出禁止](feedback_instagram_no_personal_fiction.md)第一人称体験風＋抽象架空シーン禁止・「届きました」事実＋引用→構造化→比較→提案の4段／[参加呼びかけ必須](feedback_ai_interview_participation_call_required.md)全種類で具体URL https://depth-interview-kusagawa.vercel.app/ ＋テーマ別カスタマイズ
- [ohayoにコンテンツ提案を毎朝常時表示](feedback_ohayo_content_proposal_always_show.md) — 街頭演説3案＋ブログ・SNSテーマは毎朝必出力、トリガー型化禁止、燃費90〜100K
- [通告書ドラフト→確定版の推敲パターン](feedback_tsukokusho_finalization_pattern.md) — 議案質疑は簡潔・名詞止め・評価語削除／一般質問は答弁者を件名ごと具体指定
- [一般質問テーマ選定の優先序列](feedback_ippan_shitsumon_theme_priority.md) — 地域と約束＞会派協議中＞市民の声＞当事者性。議案・報告既出＋3月既出を除外。危険/老朽/矛盾の切実な声を軸

## 🔗 外部参照ポインタ

- [ファイル管理システムv4 保存先マップ](reference_storage_map.md) — 用途→正規置き場の正本。夜間パイプラインv4(FDAランナー必須)・00_名簿・個人情報区画・~/Archive・週次スイープ・_relocation_logロールバック
- [R8.6.15半導体の世界の亀山 議場確定事実](reference_r8615_handotai_floor_facts.md) — 「半導体の世界の亀山」は櫻井市長の旗・草川は後押し役。国支援額は発信で10兆規模補正
- [防災発信の定番リンク集5本](reference_bosai_link_collection.md) — 気象庁(亀山2421000)/川の防災/防災みえ/名阪国道規制/中電停電。台風大雨警報の発信に毎回添える
- [草川議会質問アーカイブv3構造](reference_drive_archive_kusagawa.md) — 学習層1088件、grep対象は01_council〜06_election
- [claude-configバックアップ](reference_claude_config_backup.md) — GitHub thiguchi125-debug/claude-config、復元はrestore.sh
- [スキルトリガー一覧Notion](reference_skill_triggers.md) — 草川用スキル早見表（Notion a0631315配下）
- [エージェントトリガー一覧Notion](reference_agent_triggers.md) — 草川用エージェント18本の発火ワード早見表
- [市民の声Googleフォーム3シート＋ETL分類済資産](reference_市民の声情報源.md) — 2021/06〜359件、6ドメイン分類済（_citizen_voice/配下）、施策発掘の必読源
- [亀山市コミバス運賃](reference_kameyama_combus_fare.md) — 小中学生以下100円・高校以上200円
- [亀山市コミバス・のりかめさん収支データ](reference_kameyama_combus_revenue.md) — コミバス運賃521万/委託1億/収支率4.8%（R3）、のりかめさん運賃248万/委託881万（R4）
- [✅タスクDB クイック登録](reference_task_db_quick_create.md) — data_source_id=292cf503-a68f-81c6-b9dd-000b3ffdd2ce、最小5プロパティでcreate1発
- [自治会・地区別市政報告会スライド作成プレイブック](reference_jichikai_shisei_houkokukai_playbook.md) — 地区別ニュース62本・一次資料・標準WF・voice-dna辞書
- [亀山市議会 一般質問の標準時間](reference_kameyama_general_question_time.md) — 答弁込み45分。時間配分の基準値
- [太岡寺自治会 太陽光要望書（R5.12.12）](reference_taikoji_yobosho_taiyoko.md) — 村山竹則会長／太陽光規制条例の早期策定要請。市内でいち早く市長に直接届けた先見事例
- [亀山市新庁舎 開庁=令和18年度（2036）](reference_shincho_kaicho_r18.md) — JR亀山駅周辺・当初R12計画から6年延伸（市R7.2取りまとめ・R7.6答弁）。発信物は必ずR18年度。「令和12年度」は旧計画＝誤り。失敗教訓は[[feedback_stale_authoritative_doc_vs_policy_change]]
- [次期ごみ処理施設](reference_jiki_gomi_shori_shisetsu.md) — 現施設R12.3稼働終了→次期R15年度稼働目標・80t/日溶融炉・基本構想策定中・能登災害廃棄物R7.9月末受入終了
- [選挙リーフレットv3 ファイル群](reference_senkyo_leaflet_v3_files.md) — 制作物の入口。HTML/PDF/画像/再生成コマンド
- [朝の街頭活動場所9拠点](reference_morning_street_locations.md) — 阿野田公民館/みずきが丘・菅内・亀田・関・和田交差点/田村ミニストップ/商工会議所前/川合9号線前
- [一般質問 制作物のDrive保存先](reference_ippan_shitsumon_seisaku_drive.md) — `ZZ_一般質問制作/R0X/YYYY-MM_◯月議会/`（01通告書/02原稿/03写真/04完成品）

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
- エージェント本体: ~/.claude/agents/ 配下（kameyama-researcher / community-rally-speaker / daily-street-speech / speech-writer / electoral-district-strategist / agenda-analyzer / counter-argument-simulator / short-video-virality-architect / sns-content-polisher / policy-archive-miner / policy-validator / design-director / design-inspiration-researcher / print-designer / photo-curator 等）

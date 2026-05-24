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
- [Desktopブリーフィング廃止](project_desktop_briefing_deprecation.md) — 2026-05-12 旧launchd版（~/.kameyama-briefing/daily_briefing.py）停止、news-briefing skill＋ohayoに一本化、過去20日HTMLは~/Desktop/_archive_briefing_2026-05-12/へ退避
- [short-video-create システム新設](project_short_video_create_system.md) — 2026-05-18新設。skill `short-video-create` + agent `nanobanana-prompt-designer` の2層。セリフ→fact-check→risk-review→画像プロンプト→Notion保存を1パス化、サイズ指定忘れ・公選法漏れ・保存先迷子を構造的に防止
- [task-audit初回実施 2026-05-21](project_task_audit_2026-05-21.md) — standardモード+electoral-district-strategist連動・180K消費・**議席安全圏3,644票**発見・**3本柱5/28必達G7化**・5/31月末ゲート向け新規7件追加／反省: 期限再設定の前に完了確認義務（次回task-auditで恒久ガード化）
- [Drive運用構造v2](project_drive_structure_v2.md) — 2026-05-21設計＋統合。投函口2系統(_INBOX_council/_INBOX_daily)＋月別取込済アーカイブ＋日常資料4カテゴリ。**3スキル→drive-intake 1スキル4モード化**（council-materials-intake deprecated）。rclone v1.74.1導入済・自動move＋[DONE_]prefix付与機能実装済。**草川残作業: ①rclone config OAuth設定 ②Drive UI 旧フォルダリネーム2件＋既存INBOX11件振分**

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
- [議会公務の会議資料は📅ミーティングノートDB配下に置く](feedback_council_meeting_db_placement.md) — 議案分析・委員会説明会・所管事務調査は期別議会フォルダではなくミーティングノートDB＋会議体マスタ紐付けが正解、標準プロパティ＆ページテンプレ整備（2026-05-12）
- [news-briefing 鮮度チェック必須（Yahoo検索キャッシュ罠）](feedback_news_briefing_freshness_check.md) — Yahoo検索は日付修飾効かず・7日で記事削除、必ずWebFetchで本体実在＋配信日確認してからDB登録（2026-05-08事故）
- [ohayo に archive grep 連動を組み込み（v2.2）](feedback_ohayo_archive_grep_integration.md) — news-briefing単独だと過去発言連動が抜ける、cron停止時の耐障害性確保のためohayo側に組込（2026-05-08）
- [1日のルーティンを別ページに独立化](feedback_routine_independent_page.md) — ダッシュボードのチェックボックスリストを「📅 毎日のルーティン（改訂版）」34acf503-に独立化、ohayoは本セクションに一切書込まず燃費数K削減（2026-05-08）
- [ohayo v2.1 街頭演説／ブログSNSテーマ提案](feedback_ohayo_v21_speech_blog_themes.md) — 🎯フォーカス直後に🎤3案＋📝発信テーマ、提案のみ／本文化は下流／チャット限定／追加fetchゼロ
- [ohayo→daily-content-generator連結はB（プロンプト型誘導）](feedback_ohayo_daily_content_generator_prompt.md) — テーマ提案トリガー成立時のみ末尾に「💫 フルパッケージ作る？」1行、自動連結禁止、+0K（v2.5-d 2026-05-21）
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
- [草川 役職・所属委員会マスタ](feedback_kusagawa_role_committee_master.md) — 教育民生委員会の委員（確定）・委員会内容は普段からブログ発信。発信テーマ提案・原稿生成時に必ず参照、「傍聴」等の立場逸脱表現を排除（2026-05-12）
- [ohayo 必須セクション実行チェックリスト](feedback_ohayo_section_execution_checklist.md) — §3-4d市民意見フォーム新規回答処理など実行漏れ多発、起動時に内部TodoListで18セクション管理、全件チェック完了するまで出力禁止（2026-05-12）
- [ohayo v2.5 削除/縮小判断（D1/D2/D5）](feedback_ohayo_v25_streamline.md) — iJAMPチャット停止／§3-6発信テーマ提案トリガー型化／Step4ダッシュボード書込みを「昼間も参照価値あり」3セクション限定、目標85〜95K（2026-05-12）
- [「届かないを終わらせる」フレーズは草川非好み](feedback_phrase_todokanai_owaraseru.md) — 軸1タグライン候補だが単発投下で伝わらない、結び/見出し使用禁止、voice-dna.md/policy_compass.md 次回更新時に候補から外す（2026-05-12）
- [「亀山42% vs 100%」は介護保険分野・子育てではない](feedback_kameyama_42pct_kaigo_not_childcare.md) — 自治体比較数値の誤帰属、子育て・保育・教育文脈で絶対使用禁止、03_themes/子育て・教育.md 内紛れ込みは次回 themes 更新時に介護分野へ移動（2026-05-12）
- [子育てDX「遅れ」フレームは前面禁止](feedback_kosodate_dx_delay_risky_frame.md) — 亀山子育てDXは他分野より進んでいる側で反論材料になる、運用ピンポイント（現金集金3費目／コドモン26機能／集金回数）に絞る、「制度はある。問題は、運用」フレーミング（2026-05-12）
- [草川ショート動画原稿のスタイルガイド](feedback_kusagawa_short_video_script_style.md) — 疑問→断定フック／1段落1メッセージ／広め呼びかけ／共感「したこと、ありませんか」／具体3例＋ダッシュ／継続取組の婉曲表現／議場発言の引用精度／独自タグライン強制禁止／テキスト連続版優先・カット表は補助（2026-05-13 保育園キャッシュレス動画から抽出）
- [距離比喩「最後の100m／ラスト1マイル」は使わない](feedback_metric_distance_metaphor_avoid.md) — 「100mって何の100m？」で読者がつまずく、申請主義の壁は行為語（先回りする/役所側から動く）で書く（2026-05-12）
- [ブログの過去発言一覧振り返り型導入は避ける](feedback_blog_past_arguments_recap_avoid.md) — 「これまで申し上げてきた『A』『B』『C』『D』といった論点」型は読み手の文脈不足で逆に何の話か不明、新フェーズの提案として直接書き出す（2026-05-12）
- [「届かなくても届く」フレーズは意味不明・前面禁止](feedback_phrase_todokanakutemo_todoku.md) — タイトル/見出し/キャプションでの使用禁止、代替は「申請しなくても、届く」「先回りする行政」等の動作明示型（2026-05-13）
- [SNSは市民生活のBefore/Afterシーン先行で書く](feedback_sns_citizen_lifescene_first.md) — 事例・数字・固有名詞は冒頭NG、出産後/75歳到達/引っ越し/障害認定/スマホ苦手等の日常シーンで始め、数字は中盤以降の補強材料（2026-05-13）
- [ohayo停止セクション残骸の自動削除（v2.5-b/c）](feedback_ohayo_stale_display_removal.md) — 書込停止セクションがダッシュボードに古い表示で残る副作用への対策。毎朝Step 4開始時に9セクション分のスイープを実行し空置換削除。タスク詳細は2026-05-13 v2.5-cで削除対象から除外し毎朝3ブロック更新へ復活（2026-05-13 草川直接指示）
- [印刷物バイナリ素材は案件別サブフォルダで隔離](feedback_publications_binary_storage.md) — 02_publications/{reports,leaflets}/ 直下のtxt-grepフラット構造を汚さず、`<YYYY-MM>_<案件名>/` 配下にPDF/HTML/写真素材を格納、中間版は最終確定後に削除（2026-05-14 Desktop整理から確立）
- [印刷物PDFは生成直後に自動open](feedback_auto_open_pdf_after_render.md) — チラシ/市政報告等のPDF更新後はコマンド案内不要、`open <絶対パス>`を即実行してプレビュー.appに表示。HTMLは自動openしない（草川作業用途で邪魔）（2026-05-15 v2作業時に直接指示）
- [市政報告レポート印刷物制作チェックリスト](feedback_print_publication_checklist.md) — A4両面印刷物のレイアウト規範／タイポグラフィ階層／写真サイズ／章順構成／安全ゲート／全体俯瞰レビューを統合。木下版v22規範踏襲、太岡寺版v1→v19の19回イテレーションから集約、N+1イテレーション予防（2026-05-15）
- [画像EXIF処理のテクニック](feedback_image_exif_processing.md) — iPhone写真は`sips -r 90`単独だとブラウザ二重回転事故、`PIL ImageOps.exif_transpose`+EXIF strip で確実に正規化。太岡寺版v9太陽光写真向きおかしい指摘から確立（2026-05-15）
- [印刷物への Drive PDF図面挿入・LINE QR並列・Page overflow段階圧縮](feedback_print_diagram_qr_layout.md) — ①Drive PDF→base64経由→pdftoppm→PIL clip/rotate ②contact-box flex 2カラム化でLINE QR並列（幅26mm） ③overflow解消の優先順位（写真wrap→infobox圧縮→figure max-width→冗長quote削除→padding微減→コメント短縮）。二本松版v6 2026-05-23制作の6イテレーションから集約
- [フォーム回答の属性帰属はoperational contextで判定](feedback_form_response_no_attribution_guess.md) — 「アレルギー・体調・配慮事項」等の主語が書かれない自由回答は運営文脈（誰が食べる／使う／対象か）から自然な主体を選んで即対応、過剰な「念のため確認」は信頼を損なう。お弁当のアレルギー＝食べる主体（お母さま）と即判定（2026-05-19 温泉で産後ケア事故、第1誤=お子さまと断定／第2誤=過剰確認の二重学習）
- [亀山市中学校給食はすでに実施開始済み](feedback_kameyama_chugakko_kyushoku_already_started.md) — 「令和8年度2学期開始予定」「過渡期」フレーミングは古い情報・全面禁止。補食/空腹問題は「給食実施前提でも発生する問題」として論じる（2026-05-19 草川直接訂正）
- [中学校給食はSNS/AIインタビュー先行調査後に書く](feedback_kyushoku_sns_research_first.md) — 即時ブログ発信より AIインタビュー設計→市民の声収集→派生発信が良い。5/13📱補食ブログのSNS化は素材揃ってから一体展開（2026-05-21 草川直接指示）
- [InstagramのAIインタビュー由来投稿で私的演出禁止](feedback_instagram_no_personal_fiction.md) — 「耳から離れない」「あの子は」型の第一人称体験風＋抽象架空シーン描写は全面禁止、AIインタビュー由来は「届きました」事実描写＋引用→構造化→比較→提案の4段で書く（2026-05-23 部活地域移行#37で草川直接指示）

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
- [亀山市議会 一般質問の標準時間](reference_kameyama_general_question_time.md) — 答弁込み45分。原稿・想定答弁・再質問カード時間配分の基準値（2026-05-12）
- [太岡寺自治会 太陽光要望書（R5.12.12）](reference_taikoji_yobosho_taiyoko.md) — 太岡寺自治会から市長への要望書一次情報、村山竹則会長／太陽光規制条例の早期策定要請。亀山市内でいち早く規制条例の必要性を市長に直接届けた先見事例、今後の太岡寺関連／太陽光関連発信の起点情報（2026-05-15）

## 🏛 主要DB／システム参照（呼出時のみ詳細を取りに行く）

- 政策コンパス: project_policy_compass.md — Origin Story「声を、チカラに。」3軸=伝える/繋ぐ/希望
- 議会会期ハブDB: feedback_council_session_hub_db.md — 年4ページ・/general-question-prep の中心DB（2026-05-12新設）
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

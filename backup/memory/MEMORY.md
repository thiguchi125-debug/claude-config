# Memory Index

> 進行中案件 / 反復で効くガードルール / 外部参照ポインタ のみ常駐。各.mdは memory/ 配下にon-demand保持。過去ログは `_backup_<日付>/MEMORY.md`。1行/エントリ厳守（~200字以内）、詳細は topic ファイルへ。同系統は束ね行（1行に複数リンク）で保持。

## 🔄 進行中プロジェクト

- [ファイル管理監査2026-07-22](project_file_audit_2026-07-22.md) — Drive直下4フォルダ正規形・重複日常資料アーカイブ統合・💾Macローカルミラー新設・restore.sh修理済。**残=パイプラインv4承認（PROPOSED_v4.sh）・Time Machine未設定・trash_pending承認**。openrsyncは--iconv非対応

- [市政報告レポート川合町版＝チラシ完成形](project_shisei_report_kawaicho_complete_form.md) — 2026-07-18完成。report_kameokaテンプレの勝ちパターン（実筆跡挨拶／告知ブロック／現場実写／数字レール／円形ヌメラル／AIインタビューQR）。ネットプリント可・家庭用は[[feedback_home_printer_ink_saving_variant]]。QR検証は必ずpyzbar

- [content-pipelineに発信ビジュアル統合](project_content_pipeline_visual_expansion.md) — 2026-07-14拡張。記事URL＋写真→ブログ→安全ゲート→Notion→**サムネ(1200×630)＋SNS7種＋インスタReel(9:16)**を1パス。ブログモードは自動判定→提案。レシピ正本=skills/content-pipeline/references/visual-assets-playbook.md。サムネは着手前に元写真有無を確認

- [後援会入会フォームシステム](project_koenkai_intake_form.md) — 2026-07-14稼働。URL1本→フォーム→GAS自動返信（LINE誘導＋紹介テンプレ）→名簿CSV(00_名簿区画)→週次「後援会取り込み」でSubstack CSV。正本README=Drive 06_フォーム運用配下。告示後(10/18)拡散停止テーブルあり

- [SNS発信ルーティンv2（Discord投げ込み→朝夕プッシュ）](project_sns_routine_v2.md) — Phase1-3完了2026-07-14。①DM投げ込み→毎晩3:10振り分け ②news-briefing v4=7カテゴリ8〜15件 ③朝6:45/夕16:30に候補メニュー→返信で**ブログ+4PF納品**（全ローカルlaunchd・クラウドはdiscord接続不可で撤回・返信文法に「出し直して」あり）。次=Phase4週次深掘り+学習ループ
- [AIくさかわ（AI代役ショート動画）](project_ai_kusakawa.md) — 2026-07-09実装完了（13テストPASS・E2E動画目視済）。skills/ai-kusakawa＋scripts/ai-kusakawa。**草川手番待ち**=①ElevenLabs登録（SETUP_ELEVENLABS.md・聴取サンプル5本）②nano-bananaキャラ生成（prompt_cards.md）。それまでdevプレビューのみ・投稿不可
- [gyakusanスキル（イベント逆算・準備漏れ拾い）](project_gyakusan_skill.md) — 2026-07-09構築。Calendar＋Notion3DB＋Todoist突合・60日二層フィルタ・提案止まり→承認分のみtd.py登録・月曜ohayo自動・却下は_declined.json。**toben-trackerのTodoist自動提案は草川指示で恒久撤去済**。初回実運用フィードバック待ち
- [答弁トラッカー＋実績コンパイラー＋意見書ドラフター](project_toben_tracker.md) — 2026-07-08構築。toben-tracker（台帳=07_commitments/ledger.json・**SNS実査は毎回伺い必須**）＋ikensho-drafter＋general-question-prep kickoff Step4.5連携。欠落会期=R05-12・R06-03/06/09（Driveから追補可）
- [📷写真ストックシステム](project_photo_stock_system.md) — 2026-07-08構築。Googleフォトのアルバム「📷議員活動」に草川が2タップ選別→月一「写真ストック整理して」でClaudeがChrome回収→Drive📷写真ストック整理・台帳・wishlist照合。**草川手番=アルバム作成が未**。全自動同期は容量負担で不採用
- [デザインスタジオ環境（Canva超え）](project_design_studio.md) — 2026-07-05構築→**2026-07-07 v2センス強化**（参照駆動制作をStep1必須化＋foundations/styles/スタイルレシピ5種＋assets/illustrations/素材庫・カード計15枚push済）。残タスク=素材庫のnano-banana生成（prompt_cards.md 20枚を草川がGeminiで生成→投入→「イラスト素材庫を台帳化して」）
- [中庄町夏祭りチラシ（毎年）](project_nakasho_natsumatsuri_flyer.md) — 2026=3年目。主催「中庄を全力応援する会」（草川と独立前提）。公選法HIGH留意（原資負担者・議員名会場表記・酒類許認可・選挙近接時の残置回避）。2026は草川判断で確定配布
- [市政報告会5ステージスキル](project_shisei_houkokukai_skill.md) — 2026-07-04実装。企画→案内→スライド→解説→前夜・新設agent3本・_status.json正本。**初回実走=安知本地区の市政報告会向けに実施予定**（2026-07-05草川指示・spark/design-studio初実走も同案件に合わせ得る）
- [sparkスキル（小さな種→発信）](project_spark_skill.md) — 2026-07-03新設。種→接地→切り口案→生成→安全ゲート→保存。初回実運用フィードバック待ち
- [photo-postスキル（写真＋ひとこと→投稿画像・動画）](project_photo_post_skill.md) — 2026-07-05実装。統合1パス（文→画像1:1+9:16→動画）・実写無加工デザイン合成・spark連携PAIRモード・テンプレ3種。初回実運用フィードバック待ち
- [AI作業環境マップ Notion埋め込み](project_ai_env_map_notion_embed.md) — 2026-07-05設置。🤖AI作業環境ハブ(394cf503-8126)末尾に俯瞰図をHTML embed表示＋ライブリンク。ソース=~/outputs/ai-env-map/。自動更新なし→「作業環境マップ更新して」で再デプロイ＋embed差し替え
- [Notion全体整理2026-07-05](project_notion_reorg_2026-07-05.md) — 🤖AIハブ新設(394cf503-8126)・選挙ハブ=報告会＋チラシ特化・🗄️旧アーカイブv2(394cf503-8150)一元化。**第2弾：政策×質問DB統一＝🎯政策・質問ネタDB(`42716725`・時間軸プロパティ)が唯一の書込先／旧政策候補DB(6f1895ac)凍結**・会議ハブ簡素化・自動追加3本（人名→後援会員DB承認制／報告会声→意見リスト／AI議事録→朝承認）
- [Notion大改修＋ohayo/news v3＋smart-intake](project_notion_ohayo_news_v3_renewal.md) — 2026-07-03実施。ohayo v3・news dedup・smart-intake新設。初回実走の指摘3点も同日修理済（詳細はファイル）
- [議会だより制作エージェント](project_gikai_dayori_creator.md) — 整備完了(2026-07-02)。会議録→650字→提出docx＋引用マークdocx。トリガー「議会だより作って」
- [Notionプロジェクト・プラットフォーム](project_notion_project_platform.md) — Todoist主要PJ対応の情報蓄積母艦DB（page=37a71464・ds=8975c6a9）。Todoist=実行/Notion=蓄積。初期17PJ投入済
- [Todoistへタスク管理移行](project_todoist_task_migration.md) — 完了。td.py使用（詳細はCLAUDE.md正本）。タスク/PJ登録は全てTodoist・Notion✅/🗂️は参照のみ
- [2026年6月議会 一般質問prep](project_ippan_shitsumon_2026-06_resume.md) — 通告書6/2提出済・骨子v7確定（①部活②送迎③シャープ）。次=counter-argument-simulatorで戦闘マニュアル
- [3本柱 v0 ハンドオフ](../../../agents/knowledge/kusagawa_archive/04_compass/3pillars/v0_handoff.md) — v0草案完成・保管中。判断タスクは不要と草川判断（2026-07-05・Todoistから削除済）。公約設計で必要になったら「3本柱v0見せて」
- [クラウドRoutine棚卸し2026-07](project_routine_cleanup_2026-07.md) — 停止4本（drive-sync／選挙週次／旧policy-update週次・月次＝いずれも廃止DB前提or二重生成）・修理1本（oyasumi夜間=Todoist読取専用化）・現役4本。議会資料管理Phase1-4も畳んだ（Drive v3に吸収済[[project_council_materials_management]]）

## 📦 移設済みルール束（2026-07-04・詳細は各agent/SKILL末尾「📌恒久ガードルール」節＋memory各ファイル）

- [運用規約：タスク特化ルールは担当agent/SKILL常駐](feedback_rules_reside_in_agents.md) — 新feedbackは対象agent/SKILL末尾へ追記・索引は束カウントのみ。横断ルールだけ個別行

- ohayo/oyasumi運用16本 → ohayo/oyasumi SKILL.md（feedback_ohayo_*/feedback_oyasumi_*）
- ショート動画7本 → short-video-virality-architect/image-designer/short-video-create（feedback_short_video_*等。字幕帯はy1240-1460に正本統一済2026-07-04）
- 印刷物17本 → print-designer/print-layout-architect（feedback_print_*・leaflet・design_quality_bar・esports_logo・rakusuru・手書き挨拶は幅90mm前後で縮小禁止等）
- ブログ6本 → blog-writer/blog-writer-normal（feedback_blog_*・深掘りは02_publications/blog実物と型合わせ必須=絵文字/詩的抽象排除・具体密度・草川たくやの視点実務節）
- SNS/AIインタビュー7本 → sns-content-creator/polisher/ai-interview-sns-poster（feedback_x_*・feedback_sns_*・feedback_ai_interview_*等。旧X140字記述は2026-07-04掃除済）
- news-briefing 5本 → news-briefing SKILL.md（feedback_news_*）
- 街頭演説4本 → daily-street-speech（feedback_street_speech_*）

## 📌 恒久ガードルール（実運用で効く feedback）

- [アーバンスポーツ署名の発信はスケボー特化にしない](feedback_urban_sports_not_skateboard_only.md) — 主題＝多様なアーバンスポーツ（スケボー/3人制バスケ/BMX/パルクール）による子どもの居場所づくり。背骨＝草川の議場ロジック「音を出せる×歩いて通える」2条件→河川敷・橋の下。フットサル等球技は署名要望文外で書かない。P2(9/18〜)は再投稿要判断
- [Chrome MCPのGoogleフォーム編集は拡張競合で書込ブロックされる](feedback_chrome_mcp_google_forms_write_blocked.md) — docs.google.comで`Cannot access chrome-extension:// URL of different extension`が出たら別拡張の競合。navigate/read_page/findは生きてるので手動書込→read_page検証が最速。必須トグルはAXに出ず目視依頼。数回で見切る
- [Googleドキュメント形式はローカルgrepに不可視＝「無い」と断定するな](feedback_gdoc_native_invisible_to_local_grep.md) — .gdoc/.gsheetはミラーにショートカットのみ・_indexにも乗らない。ローカル空振り時は**必ずDrive MCP search_filesでサーバ側検索**してから「無い」と言う。誤配置も同時に疑う（R8コーチング体制が亀山JCに紛れていた事故2026-07-22）
- [headlessのMCPはdeferred＝「未接続」ではない](feedback_headless_mcp_deferred_false_absent.md) — launchdの`claude -p`はツール登録数が多いとMCPが遅延ロード→ToolSearch知らないジョブが「Notion未接続」と誤判定し成果物ゼロでrc=0完了（SNS便4連続不発の真因・2026-07-17修理）。allowedToolsに`ToolSearch`必須＋プロンプトに明記。「MCP未接続」報告は再認証より先にこれを疑う
- [agent frontmatterのtools行はツールゼロ化→捏造報告](feedback_agent_tools_frontmatter_breaks.md) — `tools: All tools`が存在しないツール名2つと解釈され全ツール喪失→偽ls付き完了報告を捏造。tools行は書かない・tool_uses:0は捏造シグナル・実装agent完了後はls実在検証・修理は新セッションから有効
- [agent大掃除2026-07-05＋description 400字ルール](feedback_agent_description_diet_2026-07-05.md) — 54→44本・description▲73%。旧policy-expert 6本→policy-domain-expert／旧実装系4本→policy-strategy-suiteに読み替え。新規agent/skillのdescriptionは400字以内厳守・復元は_retired_agents/とgit
- [サムネ・SNS画像・図解は最初からプロ級和文タイポで組む](feedback_thumbnail_pro_typography_default.md) — palt約物詰め＋カギ括弧ぶら下げ(text-indent負)＋Hiragino Sans実ウェイトW8/W9＋見出しlh1.16＋不要影削除。「後でプロ級にして」の往復を防ぐ。勝負所はdesign-director
- [サムネ制作は元になる草川の写真を先に求める](feedback_thumbnail_ask_base_photo_first.md) — アイキャッチ/OGP着手の第一手＝base写真の有無を1回確認。ありならphoto-curatorで写真主役、無し選択ならタイポ＋モチーフ（[[feedback_thumbnail_pro_typography_default]]）。EYES-FIRST共通
- [家庭用プリンタで刷る回はインク節約版を別途用意](feedback_home_printer_ink_saving_variant.md) — 背景白＋大面積の濃色ベタ削減（円形ヌメラルはリング化）。CSS配色だけ差し替え本文レイアウトは触らない（再検証不要）。ネット印刷用フル配色版と両保管
- [印刷物デザインは確定前に必ずnatural-design-reviewerを通す](feedback_design_review_gate_no_skip.md) — 2026-07-05コスモスチラシで自分の目視だけで確定し批判agentを飛ばし悪化→草川指摘。修正版・構造変更後も通す。写真上文字が読みにくい時は対症療法せず構造分離
- [地域/子どもチラシは明るく柔らかいイラスト路線が理想](feedback_flyer_bright_illustration_style.md) — Claude Code自作HTMLは暗く硬くなりがち。淡色＋余白＋水彩花＋キャラ。草川が完成デザイン画像を持ち込んだらQR等機能要素だけ直す（本物QR合成→cv2デコード検証）
- [自作スキルは ~/.claude/skills/ のみ（plugins cache禁止）](feedback_skills_home_not_plugin_cache.md) — 2026-07-03プラグイン自動更新でcache同居の8スキル消失→git 41ab43bから復旧。sync-to-git.shにガット検知ガード実装済
- [Notion SQLクエリはプラン限定ブロック](feedback_notion_sql_plan_gate.md) — query-data-sources(SQL)使用禁止・viewはフィルタ欠落の罠。定常一覧は自己管理固定ページ（newsのdedupインデックス/ダイジェスト）パターンで
- [システムの法則＝自動トリガー有=生/記憶依存の締め=腐る](feedback_system_closing_loops_rot.md) — 締め工程を定時トリガーに載せる・機械可読な一次情報から自動導出
- [日中メモの捕捉面はDiscord bot DM一本](feedback_daily_capture_discord_dm.md) — Keep EOD貼り付けは2026-07-23廃止（やれなかった）。スマホからDMに投げるだけ→夜間3:10 triageが自動振り分け（タスク:/声:/発信:/素の行=日次ログ）。fetch/triageに30分後リトライ＋ネット疎通待ち実装済
- [市政報告会の声の自動記録](feedback_shisei_houkokukai_voice_capture.md) — 「記録：〇〇報告会で△△の声」で🎤報告会DB「主な意見・要望」欄＋Todoist「〇〇地区フォロー」箱(要整理ラベル)
- [親子で米づくり事業の正しい主催表記](project_oyakode_kometukuri.md) — 亀山JC主催・草川がJC理事長時代に企画。「個人主催」表記禁止
- [昼生お花見コミバス企画の主催表記](feedback_ohanami_hanyu_shusai_attribution.md) — 主催=昼生地区まちづくり協議会×市地域社会振興会。草川は参加・つなぎ役、手柄横取り印象回避／市民実名は対外伏せる
- [市民意見DBはc2c34bd8に一本化](feedback_shimin_iken_db_consolidation_c2c34bd8.md) — 正本は📝市民意見リスト`c2c34bd8-`のみ。旧📋受付BOX`354432ec-`廃止。対応状況status廃止
- [市民意見「経過報告」型返信メールの確定スタイル](feedback_citizen_reply_progress_report_style.md) — txt→open -e／冒頭フルネーム＋様・署名なし・「平素より〜」開始・【】見出し・「おっしゃる通り」で受ける
- [市民SNS DM返信の確定スタイル](feedback_citizen_dm_reply_finalize_style.md) — 無知露呈禁止・現場情報は「大事な現場の課題」・遅延は冒頭お詫び・DMは署名なし・「本会議で」明示・「議会で継続して追いかけます」
- [エージェント部分ロードの根本原因と修理記録](feedback_agent_registry_partial_load.md) — 原因=agents/knowledge配下の入れ子.claude/agent-memoryがレジストリ汚染。2026-07-02隔離修理済。再発時は`find ~/.claude/agents/knowledge -type d -name .claude`
- [一般質問設計の専任エージェント](feedback_general_question_architect_agent.md) — general-question-architect。時間逆算＋逃げ封じ（先に認めてから刺す）＋重複/既決チェック。出力＝設計書
- [議案質疑/一般質問の本番原稿化](feedback_bill_scrutiny_scriptwriter_agent.md) — bill-scrutiny-scriptwriter＋honban_genko_craft_v1.md＋GOLD_太陽光条例。設計→原稿化→counter-sim
- [コンテンツ生成は常時lean full-agentがデフォルト](feedback_content_generation_default_flow.md) — 主担当agent省略禁止、lean毎回適用、目標90〜170K
- [「次の議会で追及」型表現を軽々に使わない](feedback_no_aggressive_pursuit_phrases.md) — 特定議会×対決動詞禁止、「継続的フォロー」「対話を重ねる」で表現
- [issues返信は記録不要](feedback_issues_response_no_log.md) — 「賛成」「反対」冒頭の意見はNotion保存/タスク化省略、返信3案だけ
- [ブログ定型フッターに◆AIインタビュー常設](feedback_blog_footer_ai_interview_link.md) — Threadsの後にdepth-interview-kusagawa（kameyama_shisei_zenpan）リンク追加。blog-writer/normal実装済
- [コピペ前提原稿は納品形式を先に伺う](feedback_copypaste_draft_delivery.md) — コードブロックは左余白が入る。既定はtxt書出し→open -e（TextEdit全選択コピー）。「余白入らない」と断定しない
- [Notion内部リンクは mention-page タグ必須](feedback_notion_link_deeplink.md) — `<mention-page url="...">タイトル</mention-page>`（markdownリンクはモバイルでブラウザに飛ぶ）
- Notion update_content/DSLの罠 — [落とし穴](feedback_notion_update_content_pitfalls.md)一括置換サイレント失敗・fetch検証必須／[罠v2](feedback_notion_update_content_pitfalls_v2.md)timeout後も適用済・即リトライ禁止／[DSLステータスフィルタ書込不可](feedback_notion_dsl_status_filter_limitation.md)
- [notion-saver保存後は漢字化け実体確認必須](feedback_notion_saver_kanji_garble_verify.md) — お風呂→お風坂等の実体破損あり。「表示上の問題」の自己弁明を信じずfetch検証→replace_content全置換
- ブログ/SNS DBステータス＆URL — [選択肢=未着手/進行中/完了のみ](feedback_blog_sns_db_status_options.md)／[3DB view_url再設定](feedback_3db_view_url_correction.md)／[SNS DB v2 ds=1bd98deb](feedback_3db_view_url_correction_v2.md)
- [仕上げモードU4後に日次ログ追記必須](feedback_nichijo_finalize_log_append.md) — 仕上げ生成物が日次ログに自動反映されない穴
- [会議体マスタの網羅性不足対策](feedback_meeting_master_coverage.md) — マスタ少なく未紐付発生、単発講演も登録
- [議会公務の会議資料は📅ミーティングノートDB配下](feedback_council_meeting_db_placement.md) — 議案分析・委員会説明会・所管事務調査は期別フォルダでなくMTGノートDB＋会議体マスタ紐付け
- [声のDNA抽出時の注意](feedback_voice_dna_extraction.md) — サンプル不足時にAI生成の定型句を真の声と誤認しない
- [市民相談→タスク登録連携](feedback_citizen_inquiry_task_registration.md) — 次アクションを親＋サブ階層化で登録候補提示
- [禁止用語リスト（現在は空）](feedback_forbidden_words.md) — 明示的な禁止語なし、市民向けは平易な日本語
- [content-pipeline配下エージェントのグローバル登録必須](feedback_content_pipeline_agent_registration.md) — blog-writer等は ~/.claude/agents/ 配置
- [写真＋動画入力はphoto-postフルを最初から回す](feedback_photo_video_input_run_full_pipeline.md) — テキスト仕上げで止めるな。「言われたことは全てやれ」＝素材＋スキル完成形まで自走。写真は必ずRead確認（全景/ヘリ取り違え事故防止）
- [Notion会議ページ→カレンダー登録時は元ページ削除まで自走](feedback_notion_meeting_to_calendar.md) — Calendar登録＋アカウント明示＋元Notion削除依頼まで1パス
- [議事録は草川発言＋市回答のみ抽出](feedback_giji_kusagawa_response_only.md) — voice-dna汚染防止＋トークン節約
- [5/27子ども医療費は誤帰属あり](feedback_kodomo_iryohi_sns_misattribution.md) — 3月議会医療費質疑は草川でなく福沢議員。逐語禁止、全国90.5%は「市の調査」で中立可。確定版=drafts/2026-06-03_子ども医療費18歳まで_v3.md
- [濁り水断水の給水描写は深水議員(3番)発言](feedback_fukami_water_distribution_misattribution.md) — 給水車2台等は深水議員。草川は被害アンケート/水質見える化/管路老朽化。2,700世帯/11月/12月は草川由来OK
- [他議員の名前は対外発信物に載せない](feedback_no_other_council_members_names.md) — スライド/SNS/ブログ/印刷物で他議員氏名禁止、汎用表記に。内部資料はOK
- スライド制作 — [通常はNotebookLM経由必須](feedback_slide_generation_via_notebooklm.md)Marp/Slidev直接生成禁止／[市政報告会のみ例外=Claude Code HTML/CSS→PDF](feedback_shisei_houkokukai_slides_claude_code.md)見本=木下版
- [架空エピソード・つくり話禁止](feedback_no_fabricated_stories.md) — 感情演出禁止、実体験/一次情報/公式データのみ
- [アーカイブgrepは話題ワード＋草川独自表現を並列で](feedback_archive_grep_keyword_expansion.md) — 「乗って残す」等の草川語彙を引き忘れない
- [返信文でのおうむ返し禁止](feedback_no_parroting_in_replies.md) — 相手が書いた事実の反復はAI臭。自分の反応→決意→約束で組み立てる
- [タスク登録は記録/タスク振り分け→保存先＋期限（推奨+3日）提示→本人回答後に保存](feedback_ask_destination_and_deadline_before_register.md) — 既定値で勝手に登録しない。[[feedback_task_deadline_3days]]の+3日は「推奨案」に降格済（CLAUDE.mdと統一2026-07-04）
- [✅タスクDB Pending／保留系3区分](feedback_task_db_pending_status.md) — Pending=実行に検討要／Wish List=追加対応なし／Waiting=相手待ち。status追加はUI手動のみ
- [brainstormingのトークン浪費パターン](feedback_brainstorming_token_efficiency.md) — 同内容md多重生成禁止、design docは3000字以内、探索はサンプリング段階
- [「亀山」typo再発防止（亜山・亵山禁止）](feedback_kameyama_kanji_typo_guard.md) — JSONのunicode escapeで「亀」(U+4E80)取り違え事故。日本語は直接書く
- [議会・他議員への提言は対外発信で避ける](feedback_no_council_directed_proposals.md) — 提案宛先は執行部に限定、他自治体議会事例は中立紹介でOK
- [草川 役職・所属委員会マスタ](feedback_kusagawa_role_committee_master.md) — 教育民生委員会の委員（確定）。「傍聴」等の立場逸脱表現を排除
- 禁止表現集 — [「届かないを終わらせる」](feedback_phrase_todokanai_owaraseru.md)／[「届かなくても届く」](feedback_phrase_todokanakutemo_todoku.md)／[距離比喩100m/1マイル](feedback_metric_distance_metaphor_avoid.md)／[抽象・詩的比喩](feedback_no_abstract_poetic_phrases.md)／[つくり話冒頭](feedback_no_halfbaked_story_openings.md)／[空虚な問いかけ風](feedback_no_hollow_rhetorical_questions.md) — いずれも全面禁止・断定と行為語で書く
- [「亀山42% vs 100%」は介護保険・子育てではない](feedback_kameyama_42pct_kaigo_not_childcare.md) — 子育て・保育・教育文脈で絶対使用禁止
- [子育てDX「遅れ」フレームは前面禁止](feedback_kosodate_dx_delay_risky_frame.md) — 亀山子育てDXは進んでいる側。運用ピンポイント（現金集金3費目/コドモン26機能）に絞る「制度はある。問題は運用」
- [発信物で絵文字を使わない（AI臭い）](feedback_no_emoji_ai_smell.md) — 絵文字禁止、見出し装飾はCSSライムバー/角マーカー/ピル、制作後にコードポイント検査
- [フォーム回答の属性帰属はoperational contextで判定](feedback_form_response_no_attribution_guess.md) — 主語なし自由回答は運営文脈で自然な主体を選び即対応、過剰な「念のため確認」は信頼損なう
- [団体名義SNSの同意を個人政治ブログに移植すると射程がズレる](feedback_consent_scope_org_to_personal_blog.md) — 協会名義の掲載同意≠議員個人ブログ掲載同意。器が変われば「政治ブログに実名で載せる」と明示して取り直す（要配慮層は特に）。中和一文＋立場明示
- 中学校給食 — [既に実施開始済（過渡期フレーム禁止）](feedback_kameyama_chugakko_kyushoku_already_started.md)／[選択制回帰の切り取り注意](feedback_kyushoku_sentakusei_kaiki_misread_guard.md)土台肯定＋「後戻りしません」セット／[SNS/AI先行調査](feedback_kyushoku_sns_research_first.md)
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
- [亀山市新庁舎 開庁=令和18年度（2036）](reference_shincho_kaicho_r18.md) — 発信物は必ずR18年度。「令和12年度」は旧計画＝誤り（教訓は[[feedback_stale_authoritative_doc_vs_policy_change]]）
- [次期ごみ処理施設](reference_jiki_gomi_shori_shisetsu.md) — 現施設R12.3稼働終了→次期R15年度稼働目標・80t/日溶融炉・基本構想策定中・能登災害廃棄物R7.9月末受入終了
- [選挙リーフレットv3 ファイル群](reference_senkyo_leaflet_v3_files.md) — 制作物の入口。HTML/PDF/画像/再生成コマンド
- [朝の街頭活動場所9拠点](reference_morning_street_locations.md) — 阿野田公民館/みずきが丘・菅内・亀田・関・和田交差点/田村ミニストップ/商工会議所前/川合9号線前
- [一般質問 制作物のDrive保存先](reference_ippan_shitsumon_seisaku_drive.md) — `ZZ_一般質問制作/R0X/YYYY-MM_◯月議会/`（01通告書/02原稿/03写真/04完成品）
- [Discordチャンネル起動フラグ](reference_discord_channel_launch_flag.md) — 正=`claude --channels plugin:discord@claude-plugins-official`（`:discord`区切りは受信全捨て）。診断はmcp-logs-plugin-discord-discordの「Channel notifications skipped」

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
- エージェント本体: ~/.claude/agents/ 配下54本（発火ワードは[エージェントトリガー一覧Notion](reference_agent_triggers.md)参照）

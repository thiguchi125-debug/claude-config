# agent description 圧縮対照表（2026-07-05・承認待ち）

- 方針: トリガー語は**全部残す**／「Do NOT use → 他agent誘導」も残す／本体.mdと重複するエッセイ部分だけ削る
- 復元: `_description_archive_2026-07-05.md` に原文全文あり＋GitHub `sync: 2026-07-05 17:10:38`
- 表記: 圧縮後は「役割1文。Triggers: … NOT: …」の統一形式

---

## 1. agenda-analyzer（1,104字 → 約280字）
議案・補正予算・条例改正・請願の分析→賛否判断支援。論点抽出・前年/他自治体比較・隠れリスク・賛成/反対両論骨子・スタンス推奨を「議案カルテ」で出力。Triggers: 議案を分析して/採決判断/賛否判断/この議案どう判断する/議案カルテ/補正予算分析/条例改正の論点抽出/請願の採否判断/議案チェック。NOT: 一般質問→council-material-creator、政策生成→policy-synthesizer、過去発言抽出→policy-archive-miner

## 2. ai-interview-config-designer（2,102字 → 約320字）
depth-interview-kusagawa.vercel.app の新規AIインタビュー設定を全項目設計し、📡AIインタビュー設定DB(a2396bf5)へコードブロック登録＋🎯政策・質問ネタDB(42716725)に調査中クロス登録。kameyama-researcher/policy-researcher並列で亀山接地（計画名・統計・条例・担当課必須）。config_idはkameyama_<keyword>形式。Triggers: AIインタビュー設定を作って/新しいインタビューを設計/depth interviewの設定編集/〇〇テーマでAIインタビュー作成/インタビュー設定の素案/config編集内容を考えて/ai-interview-config-designer/〇〇でヒアリング設計。NOT: 結果のSNS化→ai-interview-sns-poster、市民相談返信→citizen-inquiry-responder、一般質問→council-material-creator

## 3. ai-interview-sns-poster（1,719字 → 約300字）
AIインタビュー要約→4PF別（Instagram詩的600-1000字/Facebook論理500-800字/Threads問いかけ300-500字/X言い切り）政策提案SNS投稿。📣SNS投稿管理DBに1ページ統合保存＋📝市民意見リスト1件登録。長文版は定型フッター（安野貴博氏depth interviewベース/有賀啓介氏支援/個人情報禁止/参加URL）必須。Triggers: AIインタビューの要約をSNS化/depth interviewの結果を投稿に/AIインタビュー回答をInstagram・X・Facebook投稿に/市民の声SNS投稿（AIインタビュー）/ai-interview-sns-poster/インタビュー要約からSNS作って。NOT: 7PFセット→sns-content-creator、ブログ→blog-writer、DM返信→citizen-inquiry-responder、街頭→daily-street-speech

## 4. audience-experience-reviewer（847字 → 約290字）
市政報告会制作物の聴衆体験レビュー。①テーマ価値モード(Stage1)=「住民が60分を割く価値/行動変化/一般論落ち」で序列＋ボツ推奨＋磨き方、②聴衆冷読みモード(Stage3/4)=企画シートの当日の顔ぶれからペルソナ2-3生成→分単位飽きカーブ・脱落点・不明用語・クイズ実効性をslide data-id付き外科的TODOで返す。2回目以降は新規指摘のみ。Triggers: 聴衆レビュー/テーマ価値批評/冷読みして/audience-experience-reviewer/報告会の内容レビュー。NOT: 物理破綻→natural-design-reviewer、事実→content-fact-checker、リスク→content-risk-reviewer

## 5. bill-scrutiny-architect（1,508字 → 約300字）
規則・運用を実際に動かす価値ある議案質疑の設計。価値フィルタ／深掘り技法（理念vs実体ギャップ・規則委任の中身・努力義務の実効性・適用除外の穴・他自治体実装比較・現場接続）／論理順序・依存チェック／市民翻訳1行／価値ランク序列化→「議案質疑設計書」を出力。Triggers: 議案質疑を設計/価値ある議案質疑/意味のある質疑を考えて/議案質疑を磨く/質疑構成レビュー/規則運用に効く質疑/市民が腑に落ちる質疑/bill-scrutiny-architect/議案質疑アーキテクト/質疑の深掘り設計/通告の論理整合チェック。NOT: 賛否判断→agenda-analyzer、想定答弁・再質疑→counter-argument-simulator、一般質問原稿→council-material-creator

## 6. bill-scrutiny-scriptwriter（1,468字 → 約320字）
議案質疑設計→演壇でそのまま読める本番原稿化（太陽光条例GOLD型・honban_genko_craft_v1.md準拠）。凡例（本文=読む/🔒=内部メモ）・⏱タイムテーブル＋優先度マーカー・読み上げ散文（先に認めてから刺す）・🔁条件付き返し・🔒想定答弁テーブル＋★先制封じ・🧨根拠弾・📌答弁回収シート＋🔄フォロー。意見表明NG（議長注意回避）。Triggers: 議案質疑の本番原稿作って/議案質疑を原稿化/議案質疑を演壇で読める形にして/議案質疑を答弁込み◯分に組んで/議案質疑の本番台本にして/議案質疑スクリプト/bill-scrutiny-scriptwriter/太陽光みたいな質疑原稿にして/議案質疑の読み上げ原稿。NOT: 質問の設計・価値ランク→bill-scrutiny-architect、賛否→agenda-analyzer、戦闘マニュアル→counter-argument-simulator、一般質問→council-material-creator

## 7. blog-writer（623字 → 約180字）
深掘りモードブログ（1500-2500字・5段構成=現場の声→全国データ→国の制度→亀山市でできること→議会アクション宣言）。voice-dna厳守・事実密度（数値/日付/地名/法令/制度名）必須。content-pipeline Step2-A。NOT: 市民向けノーマル→blog-writer-normal、SNS→sns-content-creator

## 8. blog-writer-normal（667字 → 約160字）
市民向けノーマルブログ（800-1500字・平易な日本語・専門語は括弧注釈・政治に馴染みのない読者向け活動報告）。content-pipeline Step2-B。NOT: 深掘り政策論考→blog-writer、SNS→sns-content-creator

## 9. citizen-inquiry-responder（889字 → 約230字）
市民相談・要望・問い合わせ（SNS/メール/DM）への政治秘書ハブ：📝市民意見リスト自動保存＋返信方向3案＋1画面リサーチ要約＋次アクションのTodoist登録候補提示。重い政策調査は明示依頼時のみpolicy-researcherへ委譲。Triggers: 市民から相談が届いた/この相談どう返そう/返信案を作って/要望メールへの返信/DMで質問が来た/SNSに意見が届いた。NOT: 政策リサーチ→policy-researcher、一般質問→council-material-creator

## 10. citizen-voice-analyst（1,623字 → 約280字）
市民の声コーパス（📋市民意見リスト・Googleフォーム3種360KB+・SNS DM・LINE・街頭・自治会総会・後援会ログ・03_themes/_citizen_voice/）の深層分析：ボリュームゾーン/隠れた痛み/属性・地区別カット/感情推移/政策候補とのギャップ→優先順位付き新政策提案（実際の市民の言葉で接地）。Triggers: 市民の声分析/世論分析/ボリュームゾーン抽出/声にしにくい声を出して/市民意見リスト分析/市民は何を求めている/citizen-voice-analyst/世論ニーズマップ/市民デマンド分析。NOT: 草川自身の過去発言→policy-archive-miner、行政側現状→kameyama-researcher、国政動向→policy-researcher、政策候補生成→policy-synthesizer

## 11. community-rally-speaker（1,239字 → 約270字）
地域集会向け短尺アジテーション演説（3〜10分）：自治会総会・町内会・後援会冒頭・座談会・地区別市政報告会。5ブロック構成（掴み30秒→柱1〜3各2分→結び1分）・地区文脈密着・曖昧な敵（縦割り・無関心）で個人名は挙げない・要点版/フル原稿2モード・kameyama-researcher自動並列。Triggers: 自治会の挨拶/自治会総会の挨拶/地区集会で話す/町内会で挨拶/アジテーションスピーチ/地区別市政報告/〇〇自治会で話す原稿/後援会の冒頭挨拶/アジ演説/地元集会の挨拶。NOT: 所信表明・祝辞・弔辞・基調講演→speech-writer、一般質問→council-material-creator、ブログ/SNS→blog-writer/sns-content-creator

## 12. content-editor（545字 → 約160字）
ブログ/SNS原稿の品質レビュー（5軸=事実密度/亀山ローカル/声の一貫性/PF適合/読者エンゲージ）→合格判定or具体修正指示。blog-writer/sns-content-creator出力後に自動起動。Triggers: レビューして/チェックして/品質チェック/原稿を校正

## 13. content-fact-checker（1,210字 → 約240字）
発信前の外科的ファクトチェック（安全ゲート1段目・全発信必須）：数値・固有名詞・計画名・条例名・法令・統計・日付・予算を一次情報（市公式/会議録/計画書/予算書/法令）まで遡り、根拠URL＋原文引用付きで検証、未検証・誤りをフラグ。Triggers: 事実確認/ファクトチェック/数字あってる？/一次情報確認/fact-check/この数値正しい？/計画名・条例名の正確性確認/content-fact-checker/原稿の裏取り/出典確認/固有名詞チェック。NOT: 総合品質→content-editor、リスク→content-risk-reviewer

## 14. content-risk-reviewer（1,283字 → 約240字）
発信前リスクレビュー（安全ゲート2段目・全発信必須）8軸=個人情報/機密・非公開/公選法（寄附禁止・事前運動・虚偽）/名誉毀損/差別/利益相反/品位/政治的物議→「本当に投稿していい？」形式で提示、APPROVE/ASK_USER/REVISE/REJECT判定。Triggers: 発信リスクチェック/これ問題ない？/物議醸さない？/risk-review/個人情報入ってない？/公選法大丈夫？/content-risk-reviewer/投稿前チェック/リスクレビュー/セーフ？。NOT: 事実→content-fact-checker、品質→content-editor

## 15. council-material-creator（413字 → 約150字・ほぼ現状維持）
一般質問原稿・委員会資料・政策提案資料・データ可視化（グラフ）等の議会資料作成（EBPM視点）。Triggers: 一般質問の原稿/委員会資料/政策提案資料/データを図表に

## 16. counter-argument-simulator（1,340字 → 約270字）
議場想定戦闘マニュアル：想定答弁3パターン（best/standard/evasive）＋各パターンへの再質問カード＋引き出したい数字・約束チェックリスト＋撤退ライン。亀山特有の逃げ答弁テンプレ（検討中/調整中等）・5層反駁階段（受け止め→事実確認→他自治体比較→本質回帰→決断要求）・議場で踏み込むメンタル設計。Triggers: 答弁シミュレーション/想定答弁/反論準備/再質問準備/議場リハーサル/議会前夜/一般質問の前夜チェック/委員会の前夜/答弁逃げ予測/カウンター用意。NOT: 質問原稿の作成→council-material-creator、政策検証→policy-validator、アーカイブ→policy-archive-miner

## 17. daily-street-speech（1,373字 → 約260字）
今日の街頭演説トーキングポイント（20分ループ用アウトライン・フル原稿ではない）：政策コンパス3軸＋📰当日ニュース＋nichijo直近＋📝市民意見＋政策候補＋voice-dnaを自動統合。パターンA重め/B親しみ/C攻めの3パッケージ、コアループ構造（30秒掴み→3軸ローテ→1分結び）＋デリバリーキュー＋公選法NG確認。Triggers: 今日の街頭演説/街頭演説の要旨/駅前で話す/街宣ネタ/今日の街宣/駅頭スピーチ/街頭の話す内容/今日街宣やる/street speech。NOT: 式典・フル原稿→speech-writer、自治会・地区集会挨拶→community-rally-speaker、政策立案→policy-synthesizer

## 18. design-director（1,406字 → 約270字）
デザインのプロ級格上げ（勝負所のみ）：8原則/和文タイポ（ヒラギノ・游・明朝混植・約物半角）/配色理論/8ptグリッド/CMYK・塗り足し・DPI/視線流れ/受賞級リファレンス。上流（デザインシステム・ブリーフ策定）と下流（print-designer出力の外科的リファイン）両対応。Triggers: プロっぽくしたい/もっとデザイン洗練させて/一流のデザインに仕上げて/デザインを格上げして/プロデザイナーレベルに/印刷物の最終チェック/設計指針を作って/デザインシステムを作って/A/Bバリエーション作って/タイポを整えて/グリッドを正して。NOT: HTML/CSS実装→print-designer、web調査→design-inspiration-researcher、写真→photo-curator

## 19. design-inspiration-researcher（1,117字 → 約230字）
印刷物制作前のデザイン参考収集：国内外の政治広報物（議員リーフレット/選挙公報/ポスター/海外campaign mailer）をWebSearch/WebFetch＋画像分析→パターン抽出（配色・グリッド・タイポ・写真処理・コピー階層）→design_references/に蓄積→print-designerが使える仕様書化。Triggers: リーフレットのデザイン参考になるもの集めて/他の議員のチラシどんな感じ？/応援カードの先行事例調べて/デザイントレンド調べて/〇〇党・〇〇議員のデザインを参考に/デザイン性の高い政治家広報物/海外の選挙チラシ参考に。NOT: 制作→print-designer、写真→photo-curator、政策→policy-researcher

## 20. district-hazard-analyst（910字 → 約260字）
指定地区の全ハザードマップ網羅分析：市総合防災マップ/防災みえ/重ねるHM/河川別浸水（鈴鹿川・安楽川等）/土砂警戒・特別警戒/ため池/南海トラフ震度・液状化/内水/避難所を字名・自治会名粒度で調査→クロスチェック（避難所×浸水域矛盾・通学路・要配慮者施設・孤立リスク・市対策の現在地）→地区防災カルテ（提案の種＋スライド用図表指示付き）。数値・区域はfact-checker＋出典必須、不安を煽らない。Triggers: 地区のハザード分析/〇〇地区の防災カルテ/district-hazard-analyst/ハザードマップ調べて分析。NOT: 国・県の防災政策→policy-expert-disaster-safety、市全域→kameyama-researcher、テーマ発掘→district-issue-scout

## 21. district-issue-scout（1,024字 → 約250字）
指定地区レンズで議事録・市資料から重要市政テーマを発掘（供給側・citizen-voice-analystの対）：_index/txtキャッシュ→kusagawa_archive→不足時のみDrive。地区名＋道路・学校・施設・自治会名＋草川語彙並列grep。テーマ別{時系列経緯/ステータス（計画中〜完了・停滞）/地区影響/出典/草川関与}マップ＋簡易ハザードフラグ。議事録は草川＋市答弁ペア原則、他議員数字は汎用化。Triggers: 地区の市政テーマ/〇〇地区の論点発掘/district-issue-scout/地区テーマスカウト。NOT: 市民の声→citizen-voice-analyst、草川発言→policy-archive-miner、市全域→kameyama-researcher、ハザード深掘り→district-hazard-analyst

## 22. electoral-district-strategist（1,286字 → 約250字）
2026-10-25亀山市議選のデータ選挙戦略：投票所/地区別過去結果分析・死守/強化/開拓/撤退セグメント・街宣ルート/ポスティング最適化・限界100票の特定・対立候補地盤モデル・投票率/人口動態シナリオ・後援会動員プラン・月別アクション計画。公選法遵守（公示後の違法勧誘系タスクは扱わない）。Triggers: 選挙地区戦略/票分析/得票分析/重点地区/街宣ルート最適化/ポスティング戦略/投票所別分析/人口動態と票読み/当落シミュレーション/対立候補分析/選挙データ/当選ライン分析。NOT: 演説→speech-writer/community-rally-speaker、印刷物→print-designer、市民返信→citizen-inquiry-responder

## 23. future-scenario-strategist（1,759字 → 約270字）
2030/2040メガトレンド（人口動態・技術・気候・産業構造・地政学・世代価値観）に接地した未来政策設計。シナリオプランニング/Three Horizons/CLA等で8〜15本のインパクト政策候補：各={2030/2040アンカー/今植える理由/亀山ローカライズ/先行都市シグナル/インパクト×実現性×オーナビリティ採点/旗艦vs積み上げ分類/コンパス3軸接続}。Triggers: 未来政策/インパクト政策を考えて/2030年の亀山/2040年シナリオ/メガトレンドから政策/世論を先読みした政策/future-scenario-strategist/希望の旗を立てる政策/草川らしいインパクト施策/差別化政策。NOT: 現状の国政スキャン→policy-researcher、過去発言→policy-archive-miner、亀山現状→kameyama-researcher、市民意見→citizen-voice-analyst、財政検証→policy-fiscal-simulator

## 24. general-question-architect（2,007字 → 約320字）
答弁込み45分（一問一答）に確実に収まる一般質問の設計。価値フィルタ（政策・運用・予算を動かすか/市民共鳴）／時間逆算エンジン（往復所要・自動圧縮・撤退ライン）／逃げ封じ設計=「先に認めてから刺す」で既決返球・報告返球・検討中逃げを先回り／1往復1仕事の非重複フロー＋再質問階段／既決チェック（協定・可決議案・現況報告・過去答弁と照合）／市民翻訳1行／アーカイブ・voice整合→「一般質問設計書」（通告書＆counter-argument-simulatorへのバトン）。Triggers: 一般質問を設計/意味のある一般質問/一般質問を構築/時間内に収まる一般質問/一般質問の骨子を作って/一般質問を磨く/質問構成を整理/逃げられない質問にして/重複を排除して/45分に収めて/報告返球を封じて/general-question-architect/一般質問アーキテクト/質問の流れを整理。NOT: 議案質疑→bill-scrutiny-architect、賛否→agenda-analyzer、想定答弁マニュアル→counter-argument-simulator、最終原稿化→council-material-creator

## 25. gikai-dayori-creator（1,216字 → 約280字）
会議録docx→議会だより一般質問ページのフルパイプライン：①草川質問＋執行部答弁のみ抽出（他議員skip・誤帰属ガード）②650字段階圧縮v1→v3（氏名行/吹き出し/■小見出し＋問答/その他の質問・編集要領準拠）③会議録照合ゲート（語尾整理のみ可・数字固有名詞コピペ）④提出用docx（build_docx.py・問=緑/答=えんじ）⑤引用参照マークdocx（mark_quotes.py・赤=草川/青=執行部）⑥Desktop＋Drive ZZ_一般質問制作/04完成品へ保存。Triggers: 議会だより作って/議会だより原稿/議会だより一般質問ページ/議会だよりの提出物/gikai-dayori-creator/会議録から議会だより/議会だより提出用docx/引用参照マーク作って。NOT: 質問設計→general-question-architect、本番原稿→council-material-creator、ブログSNS化→blog-writer/sns-content-creator、印刷レイアウト→print-designer

## 26. kameyama-researcher（680字 → 約200字）
亀山市ローカル専門リサーチ：市公式計画・予算・施策・議会議事録・統計・担当課・既存施策。policy-researcher（全国・他自治体）のローカル対。content-pipeline Step1.5等から自動並列起動。Triggers: 亀山市の〇〇について調べて/亀山市議会の議事録を検索して/亀山市の総合計画を確認して/亀山市の予算書から抽出/この市民意見の担当課・既存施策を調べて/草川たくやが過去に質問した内容を調べて

## 27. kusakawa-voice-analyst（715字 → 約160字）
voice-dna（声の指紋：常用語・NG表現・文体癖・CTA）の抽出・更新ワンショット：過去発信からvoice-dna.md＋voice_examples.mdを生成。欠損・陳腐化・大量新規発信の取込時のみ。NOT: 日常のコンテンツ生成→各writer

## 28. nanobanana-prompt-designer（1,859字 → 約280字）
ショート動画台本→nano-banana（Gemini 2.5 Flash Image）用英語プロンプトカード2〜5枚：秒数区間パース/サイズヘッダ必須先頭（9:16 1080x1920・1:1・16:9選択）/セット内スタイル一貫/公選法・プライバシーガード（顔・実在ロゴ・学校名NG）/before-after視覚設計/使い方Tipsフッター。SOLO・PAIR（short-video-createから）2モード。Triggers: nano-bananaプロンプト作って/nanobanana画像/ショート動画の画像プロンプト/画像生成プロンプト/差し込み画像のプロンプト/cutaway画像/動画のインサート画/nanobanana-prompt-designer/Geminiで画像作るプロンプト。NOT: 台本→short-video-virality-architect、静止SNS本文→sns-content-creator、写真選定→photo-curator、印刷→print-designer

## 29. natural-design-reviewer（2,041字 → 約300字）
印刷物プレビューの物理破綻チェック（EYES-FIRST）：まず3秒で分かる即物破綻（写真見切れ/連絡先ページ外/大空欄/枠はみ出し/構図破綻）→次に自然さ7軸（余白/サイズ/視線/ブランド/可読性/密度/印刷常識）。鉄則①PNGを必ず自分でReadする（サブagent委譲禁止）②元画像縦横比×CSS枠のクロスチェック③2回目以降は前回未指摘の新規問題のみ。外科的TODOリストを返す（再設計・実装はしない）。Triggers: 不自然なところある？/ツッコミどころ/デザイン違和感/見た目チェック/紙面レビュー/PDFのチェック/natural-design-reviewer/空白でかすぎ？/写真小さい？/バランス見て/印刷物の自然さ確認/ツッコミ入れて/切れてない？/枠から出てない？/写真の構図変じゃない？/前回と違うところ/物理破綻チェック。NOT: プロ格上げ→design-director、実装→print-designer/print-layout-architect、写真→photo-curator、事実→content-fact-checker

## 30. notion-saver（591字 → 約160字）
長文ブログ・SNSセット・メタデータのNotion DB確実保存（長文直接MCP呼び出しのJSONバリデーションエラー回避）。content-pipeline Step5（5-Aブログ/5-B SNS/ネタDB）専用。NOT: 一般Notionクエリ→MCP直接、市民意見登録→citizen-inquiry-responder、日次ログ→nichijoスキル

## 31. photo-curator（967字 → 約230字）
Photos.app顔認識DB（ZPERSON Z_PK=18=草川卓也・6,242顔）から用途別ベスト写真3-5枚ランク付き：品質/笑顔/目開き/帽子/顔サイズでフィルタ、HEIC→JPEG変換・EXIF向き補正・iCloud未DL検出・即使えるパス提示。Triggers: 写真候補を出して/ベストショット5枚/草川の写真探して/IMG_xxxxを使いたい/プロフィール写真選びたい/スーツ姿の写真ある？/この用途に合う写真/photoライブラリから検索。NOT: レタッチ（外部ツール案内）、新規画像生成、他人の写真検索

## 32. policy-archive-miner（1,286字 → 約260字）
草川自身の過去8年の発言・発信の深層アーカイブ抽出：議事録・ブログ・SNS・印刷物・nichijo・スピーチ→テーマ別・時系列進化のナレッジファイル（03_themes/へ出力）。進化追跡（主張の変遷）・ギャップ分析（未言及トピック）・voice-dna一貫性トラッキング。policy-researcher（外部）の歴史アーカイブ対。Triggers: 草川の過去発言を集めて/アーカイブ抽出/〇〇テーマの過去主張を全部出して/議事録から草川の〇〇発言洗い出して/草川の主張の進化を追跡/まだ触れていないトピック教えて/voice-dna一貫性チェック。NOT: 外部リサーチ→policy-researcher、亀山一般→kameyama-researcher、政策立案→policy-synthesizer

## 33. policy-comparison-benchmarker（668字 → 約200字）
類似自治体との系統的ベンチマーク：抽出ロジック（人口5万・産業構造類似・東海圏）・三重県内9市動向・全国類似都市群・政策実装の先行事例×時期×成果のapple-to-apple横並び比較。Triggers: 他自治体比較/類似自治体ベンチマーク/亀山と似た自治体/津伊勢松阪比較/横並び分析/policy-comparison-benchmarker/5万人都市の事例/三重県内自治体比較。NOT: 全国スキャン→policy-researcher、亀山現状→kameyama-researcher、ドメイン深掘り→policy-expert-*

## 34. policy-compass-curator（1,548字 → 約230字）
政策コンパスの蒸留・保守：8年分の発言からorigin story（一生応援部魂）＋3軸（命名/タグライン/why/根拠/具体アクション）＋譲れない原則＋やらないこと境界線をメタ蒸留、Notion🧭＋policy_compass.mdの二重出力同期・定期再蒸留。policy-archive-miner（生抽出）のシンセサイザー対。Triggers: 政策コンパスを作って/政策の軸をまとめて/草川の3軸を蒸留/コンパス更新/origin storyを整理/譲れない原則を明文化/policy-compass/軸となる政策方針。NOT: 生アーカイブ抽出→policy-archive-miner、政策候補生成→policy-synthesizer、EBPM検証→policy-validator

## 35. policy-expert-childcare-education（760字 → 約210字）
子育て・保育・幼児教育・学校教育・不登校・特別支援・いじめ・児童虐待・こども政策のドメイン専門：こども家庭庁/文科省最前線・法改正・亀山の計画/実績/課題・5万人類似自治体先進事例・統計→3本柱/政策候補へ接続。Triggers: 子育て政策深掘り/保育の専門エキスパート/不登校政策/こども家庭庁の最新動向/子育て3本柱の中身/教育政策のドメイン分析/policy-expert-childcare/幼児教育専門。NOT: 統合→policy-synthesizer、亀山現状→kameyama-researcher、議案→agenda-analyzer

## 36. policy-expert-digitaltransformation（694字 → 約210字）
行政DX・デジタル民主主義・自治体生成AI・住民参加・Govtech/Civictechのドメイン専門：デジタル庁/総務省/三重県DX・行かない窓口・子育てDX・施設予約DX・マイナポータル・ガバメントクラウド・合意形成プラットフォーム等。Triggers: 行政DX深掘り/DXエキスパート/行かない窓口専門/生成AI自治体導入/デジタル民主主義/Civictech/policy-expert-dx/ワンストップ・ワンスオンリー。NOT: 統合→policy-synthesizer、亀山現状→kameyama-researcher、議案→agenda-analyzer

## 37. policy-expert-disaster-safety（665字 → 約210字）
防災・減災・通学路安全・国土強靱化・複合災害・避難のドメイン専門：内閣府防災/消防庁/国交省/三重県・地区防災計画・要配慮者個別避難計画・ため池・太陽光適正導入・南海トラフ/線状降水帯・消防団・自主防災・BCP・災害ケースマネジメント等。Triggers: 防災政策深掘り/減災エキスパート/通学路安全専門/要配慮者避難/ため池防災/太陽光発電条例/南海トラフ対策/policy-expert-disaster/国土強靱化亀山版。NOT: 統合→policy-synthesizer、亀山現状→kameyama-researcher、地区ハザード実地分析→district-hazard-analyst、議案→agenda-analyzer

## 38. policy-expert-healthcare-welfare（633字 → 約200字）
医療・福祉・介護・障害・健康政策のドメイン専門：厚労省/こども家庭庁/三重県・地域医療構想・母子保健・産後ケア・介護保険・地域包括ケア・認知症・生活保護・障害福祉・ワクチン助成・救急/在宅医療・地域共生社会等。Triggers: 医療政策深掘り/福祉エキスパート/介護政策/地域医療構想/産後ケアの専門/健康政策ドメイン/policy-expert-healthcare/医療3本柱の中身/障害福祉専門。NOT: 統合→policy-synthesizer、亀山現状→kameyama-researcher、議案→agenda-analyzer

## 39. policy-expert-transport-infrastructure（646字 → 約210字）
公共交通・道路・鉄道・上下水道・橋梁・住宅・空き家・インフラのドメイン専門：国交省/総務省/JR/三重県・関西本線電化・草津線直通化・デマンド交通・上下水道広域化・橋梁長寿命化・道路ストックマネジメント・空家対策・公営住宅等。Triggers: 公共交通深掘り/関西本線電化エキスパート/デマンド交通/上下水道広域化/橋梁老朽化/空き家対策専門/policy-expert-transport/インフラ政策亀山版。NOT: 統合→policy-synthesizer、亀山現状→kameyama-researcher、議案→agenda-analyzer

## 40. policy-expert-urbanplanning-industry（675字 → 約210字）
まちづくり・産業誘致・観光・都市計画・地域経済のドメイン専門：国交省/経産省/観光庁/三重県・立地適正化・コンパクトシティ・産業立地協定・企業誘致・観光DMO・日本遺産・リニア/コストコ/AIサーバー誘致・中心市街地・移住定住等。Triggers: まちづくり政策深掘り/産業誘致エキスパート/観光戦略専門/リニア亀山駅/コストコ誘致/AIサーバー/都市計画/policy-expert-urbanplanning/希望の旗を立てる中身。NOT: 統合→policy-synthesizer、亀山現状→kameyama-researcher、議案→agenda-analyzer

## 41. policy-fiscal-simulator（622字 → 約200字）
政策の財政シミュレーション専門：特財/一般財源/基金/起債の分析・国庫補助金/交付税措置探索・財政指標（経常収支比率等）・亀山財政の実状・ROI/費用対効果試算・類似自治体財政比較。Triggers: 政策の予算試算/財源シミュレーション/いくら必要/財政影響/国庫補助金探索/基金活用/policy-fiscal-simulator/亀山の財政余力/事業費とROI。NOT: 一般検証→policy-validator、政策の中身→policy-expert-*、候補生成→policy-synthesizer

## 42. policy-packaging-strategist（830字 → 約210字）
散在する政策候補を3本柱/公約パッケージ/リーフレット3コラム/HP政策ページに束ねる政治パッケージング（ナラティブアーク・3幕構成・対立軸フレーミング・有権者セグメント・voice-dna整合）：見出しになる柱名＋サブライン＋具体公約3〜5本へ圧縮。Triggers: 3本柱に束ねて/公約パッケージング/リーフレット3コラム/ホームページ政策ページ構成/選挙公約の柱/policy-packaging-strategist/政策の柱を整理/柱のキャッチコピー。NOT: 候補の生成→policy-synthesizer、柱の中身深掘り→policy-expert-*

## 43. policy-researcher（358字 → 現状維持）
（変更なし・既に十分短い）

## 44. policy-roadmap-designer（723字 → 約210字）
政策実装のタイムライン設計専門：議会日程（3月当初/6/9/12月/3月補正）×予算編成サイクル（10〜2月当初・6/12月補正）×4年任期フェーズ×国交付金/県補助金申請サイクル×計画策定承認→段階設計（条例化→予算化→実施→評価→改善）。Triggers: 政策のロードマップ設計/4年計画/議会タイミング/予算サイクル/いつ何をやるか/段階的実装/policy-roadmap-designer/補正予算で何ができる。NOT: 財政面→policy-fiscal-simulator、一般検証→policy-validator、政策中身→policy-expert-*

## 45. policy-stakeholder-mapper（641字 → 約200字）
政策のステークホルダーマッピング専門：関係者洗い出し（市民層・所管課・会派・国/県）・賛成/中立/反対の見立て・折衝シナリオ設計・既得権益接点・庁内/国県縦割りの突破経路・説得材料の事前装填。Triggers: ステークホルダー分析/関係者マッピング/誰を動かす/反対勢力分析/所管課攻略/会派の見方/policy-stakeholder-mapper/折衝シナリオ/誰の賛同が要る。NOT: 財政→policy-fiscal-simulator、政策中身→policy-expert-*、候補生成→policy-synthesizer

## 46. policy-synthesizer（888字 → 約210字）
並列リサーチ出力（kameyama-researcher/policy-researcher/WebSearch/Notion市民意見・ネタDB/会話履歴/NotebookLM）を統合し、政策候補ドラフト（Why/What/How/優先度/次アクション）を生成する統合ハブ。主に/policy-radarから起動。Notionへ直接書かない（承認用ドラフトのみ出力）。NOT: 生リサーチ→各researcher、一般質問原稿→council-material-creator

## 47. policy-validator（1,187字 → 約230字）
政策案のEBPM 8軸検証（🎯政策・質問ネタDB登録や議会・印刷物使用の前段ゲート）：①エビデンス②他自治体実績③費用試算④法的整合（法令・条例・公選法）⑤過去主張連続性⑥voice-dna整合⑦KPI具体性⑧反論準備→各軸A-E採点＋外科的修正指示＋APPROVE/REVISE/REJECT。Triggers: 政策案をEBPM検証して/この政策案レビューして/一般質問の前に裏付け確認/policy-validator/政策チェック/エビデンス十分？/この提案の説得力検証。NOT: 政策生成→policy-synthesizer、アーカイブ抽出→policy-archive-miner、外部リサーチ→policy-researcher

## 48. print-designer（807字 → 約220字）
印刷物のHTML/CSS→PDF実装（Chrome headless）：応援カード/名刺/リーフレット/A4チラシ/A3ポスター/ハガキDM/選挙公報/パンフ/議会報告書。和文組版（級数・行送り・約物半角・縦書き）・規格/余白/塗り足し/トリム・政治広報配色・写真配置・入稿仕様（CMYK/300dpi/PDF-X-1a）。Triggers: 応援カードを作って/名刺を作りたい/リーフレット原稿/A4チラシ/ポスター原稿/ハガキDMを作って/印刷物を作って/選挙公報/パンフレット/広報物デザイン。NOT: 一般質問→council-material-creator、ブログ→blog-writer、SNS→sns-content-creator、演説→speech-writer

## 49. print-layout-architect（1,315字 → 約260字）
印刷物のプロ構図実装＋格上げ（natural-design-reviewerが指摘役なのに対し実装者）：主要ビジュアルを読めるサイズに拡大・文字を画像横の多段組に・中途半端空白撲滅・ページ密度バランス・ページ再配分。自らHTML/CSS実装→Chrome headlessレンダ→PNGを自分でReadして画素批評→修正のEYES-FIRSTループを物理破綻ゼロまで回す。Triggers: レイアウトを作り込んで/デザインを整えて/画像を大きく・読めるように/余白をなくして/文章を画像の横に/プロ水準にして/print-layout-architect/崩壊したレイアウトを直して。NOT: 事実→content-fact-checker、リスク→content-risk-reviewer、本文執筆→blog-writer等、写真選定→photo-curator

## 50. short-video-image-designer（2,275字 → 約300字）
ショート動画挿入画像（9:16 1080×1920 PNG）を完成品まで実装：2大失敗（記号化=SVGプリミティブのピクトグラム化／文字消失=縮小SVG内小文字・低コントラスト）を構造的に殺す。イラスト品質基準（有機ベジェ・2-3トーン陰影・奥行き・小道具・シーン構成）＋可読性フロア（最小フォント・高コントラスト・1フレーム1メッセージ・SNS UIセーフゾーン）をハードゲートに、レンダ→PNG自Read→採点→修正ループ。草川カラー(#c7ff4a/#1f5a3a/#0f3d27/#f3efe4)・絵文字なし・他議員名なし・fact/risk通過。説明図=HTML/CSS、雰囲気=フラットイラスト（nano-bananaは明示依頼時のみ）。完成品はDrive📱動画素材ミラー。Triggers: ショート動画の画像作って/挿入画像をデザインして/動画の差し込み画像を作り直して/記号っぽい絵を直して/文字が見えない画像を直して/short-video-image-designer/インサート画を作画して/動画用の画像を作り込んで。NOT: 台本→short-video-virality-architect、プロンプトカード→nanobanana-prompt-designer、SNS本文→sns-content-creator、印刷→print-designer/print-layout-architect、写真→photo-curator

## 51. short-video-virality-architect（2,097字 → 約290字）
≤60秒ショート動画のバズ設計台本（完視聴率・スワイプ耐性・シェア設計）：15フックパターン・秒単位リテンションカーブ（1.5-2秒刺激変化）・PF別アルゴリズム信号（TikTok完視聴/Shortsスワイプ/Reels DMシェア）・アンチパターン検出（talking head・皆さんこんにちは・テロップ常駐・一文30字超）・voice-dna保持・公選法ガード。SOLO/POLISH 2モード→A（フック最強）/B（感情ストーリー）/C（議論喚起）3バリアント＋秒精度カット表＋フック候補5-8＋8軸自己採点（64/80必達）→fact/risk通過→📣SNS投稿管理DB保存。Triggers: バズる動画/バズらせて（動画）/スキップされない動画/viralショート/retention強化/動画クオリティ上げて/動画磨いて/もっとバズる動画に/フック強化/冒頭3秒/完視聴率/シェアされる動画/ショート動画品質改善/short-video-virality-architect。NOT: 長尺90秒超は対象外、静止SNS→sns-content-creator/sns-content-polisher、政策→policy-synthesizer

## 52. sns-content-creator（501字 → 現状維持）
（変更なし・既に十分短い）

## 53. sns-content-polisher（1,264字 → 約250字）
低品質SNS原稿の昇格リライト：8軸診断（フック強度/声の真正性/具体性/感情共鳴/PFネイティブ感/AI指紋=emダッシュ過多・完璧な三並列・予測可能CTA/行動トリガー/ローカル接地）→パッチでなくPF別に外科的書き直し、before/after診断付き。content-editor（採点差戻し）と違い書き直し済み完成品を直接出す。Triggers: SNS品質改善/もっと刺さる投稿に/AI臭をなくして/SNS投稿が低クオリティ/もっと草川らしく書き直して/SNS文を磨いて/sns-content-polisher/SNS原稿の昇格/投稿文がイマイチ/バズらせて/エンゲージメント高くして。NOT: ゼロから生成→sns-content-creator、ブログ品質→content-editor、AIインタビューSNS化→ai-interview-sns-poster

## 54. speech-writer（1,455字 → 約230字）
格式スピーチ・演説のフル原稿（所信表明/議会冒頭/選挙・後援会演説/年頭所感/祝辞/弔辞/基調講演/大会演説）：古今の名演説カノン×草川voice-dnaを統合、修辞注釈（三連・首句反復・対句・交差・ナラティブアーク・CTA）＋デリバリーキュー（間・テンポ・強調）付き。Triggers: スピーチを書いて/演説原稿/挨拶文/所信表明/祝辞/弔辞/年頭所感/後援会で話す原稿/街頭演説/選挙演説/熱い演説を作って/名演説風に書いて/心を打つスピーチ/講演の原稿/キックオフ演説。NOT: 一般質問→council-material-creator、ブログ/SNS→blog-writer/sns-content-creator、政策リサーチのみ→policy-researcher

---

## 集計
- 現状合計: 約60,400字
- 圧縮後合計: 約13,100字（**▲78%**）
- トークン換算: 約16〜18K → 約9〜10K（**毎ターン ▲7〜9K**）
  ※トリガー語を1語も削らない方針のため、トリガーが占める分は圧縮できない＝これが下限

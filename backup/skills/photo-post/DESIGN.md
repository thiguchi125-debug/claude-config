# photo-post スキル設計書（2026-07-05 草川承認済）

## 目的
手持ち写真1〜数枚＋ひとことテーマから、実写を活かした「新しい時代の政治家」風SNS投稿画像＋ショート動画を1パスで自動生成する。sparkスキル（テキスト投稿文）の視覚面の相棒。

## 確定した設計判断（brainstorming 2026-07-05）
1. **編集方式 = デザイン合成型**。実写は無加工（色調補正・トリミングのみ）。上に見出しタイポ・ライムバー・名前帯・地名タグを草川ブランドで合成。AI生成的改変（nano-banana等）はデフォルトでは使わない — 政治家写真の改変は誤解リスクHIGH＋API未設定で自動化不能のため。
2. **動画も同梱**。ffmpeg（/usr/local/bin/ffmpeg 確認済）でKen Burnsズーム＋テキスト段階表示＋ライム緑エンドカードの10〜20秒 9:16 mp4。無音（BGMはスマホ後乗せ）。複数写真ならスライドショー。
3. **独立スキル＋spark連携**。単体起動トリガーを持ち、sparkは種に写真が添付されていた場合のみ生成後に「photo-postで画像＋動画も作る？」を選択肢提示（spark側改修は1箇所のみ）。
4. **写真入力 = パス投入＋photo-curator探索**。ドラッグ投入パスが基本。未指定で「いい写真選んで」なら photo-curator（ZPERSON=18）が候補3〜5枚。HEIC→JPEG（sips）・EXIF向き補正を自動。
5. **実装方式 = HTML/CSS→Chrome headless**（design-studio / short-video-image-designer と同一パターン）。Pillow直接合成は和文タイポ品質で不採用。

## 既定フロー = 統合1パス（2026-07-05草川指示で確定）
実運用は「写真＋ひらめき/活動メモを一緒に投入→投稿文・画像・動画を順次自動生成」が既定。確認は2箇所のみ。

1. **受付** — 写真パス（複数可）＋ひとことテーマを同時受付。写真未指定→photo-curator。HEIC変換（sips）・EXIF向き補正・軽微色調補正のみ無言で自動。
2. **接地＋文・コピー同時生成** — アーカイブgrep接地（CLAUDE.md必須）→同じ素材から (a)投稿文（種のサイズに応じてX/Threads等1〜2PF・voice-dna整合・絵文字なし・禁止フレーム回避）(b)画像用見出し2行（各15字前後）＋サブ1行＋地名タグ を一度に生成。文と画像を別々に作らない＝トーン統一＋燃費。
3. **✋確認1回目** — 切り口＋投稿文＋デザイン2〜3案を1画面で提示→草川選択。
4. **画像合成** — ブランドトークン（#c7ff4a/#1f5a3a/#0f3d27/#f3efe4）でHTML/CSS実装→Chrome headlessレンダ→PNG自Read採点ループ（short-video-image-designerの可読性フロア基準流用：最小フォント・高コントラスト・SNS UIセーフゾーン）。出力：1:1 1080×1080＋9:16 1080×1920。
5. **動画生成（既定で続行・追加入力不要）** — 選択デザイン＋元写真→ffmpegで10〜20秒 9:16 mp4。ズーム（Ken Burns）→見出し段階表示→エンドカード。エンドカードは**拳ポーズの透過ポートレート（assets/kusagawa_portrait.png）＋スローガン「声をチカラに」（または「ええやん亀山」）＋#ええやん亀山**。句読点付き「声を、チカラに。」は使わない（2026-07-05草川指示）。無音。「画像だけ」指定時はスキップ。
6. **安全ゲート（skip禁止・まとめて1回）** — 文＋画像＋動画を content-fact-checker→content-risk-reviewer（8軸＋写真固有軸：第三者の顔・子どもの顔・車ナンバー・個人宅特定・公選法文書図画）に一括通過。HIGH以上はASK_USER。
7. **✋確認2回目（最終）→保存** — 完成セット提示→OK後に `~/outputs/photo-post/<日付>_<テーマ>/`（絶対パス・cwd依存禁止）＋Drive 📱動画素材ミラー＋📣SNS投稿管理DB(1bd98deb)の**1ページに文・画像・動画を同居**保存。優良テンプレはdesign_system「SNSカード」カテゴリへ昇格提案（design-studio還元ループと同型）。

サブモード：写真だけ渡して「画像にして」→ Step2の投稿文生成を省き画像コピーのみ／既存投稿文あり（spark経由等）→ 文生成をスキップしコピー抽出のみ。

## トリガー（案）
- **主経路**: 写真（パス/ドラッグ）＋ひとこと（ひらめき・活動メモ）が一緒に投入されたら統合1パスを提案起動
- 明示語: 「この写真で投稿作って」「この写真で投稿画像作って」「写真を投稿用にして」「投稿画像にして」「写真から動画も」「写真をSNS用に加工して」「photo-post」
- 衝突回避: 「記録」を含む→nichijo優先（記録後に本スキルを選択肢提示）、「メモ:」「保存して」→smart-intake優先

## NOT（他スキル・agentとの棲み分け）
- ショート動画の挿入イラスト→short-video-image-designer／台本→short-video-virality-architect
- nano-bananaプロンプトカード→nanobanana-prompt-designer（明示依頼時のみphoto-postからおまけ出力可）
- 印刷物→design-studio／写真選定のみ→photo-curator／投稿文のみ→spark・sns-content-creator

## 実装上の制約
- 実装は skill-creator＋superpowers:writing-skills を通す。description 400字以内厳守（feedback_agent_description_diet_2026-07-05）。
- 配置は ~/.claude/skills/photo-post/（plugins cache禁止 = feedback_skills_home_not_plugin_cache）。
- 燃費目標：統合1パス（文＋画像＋動画）60〜80K。動画のffmpeg工程自体はコマンド実行のみでほぼゼロコスト。
- 削らないもの：安全ゲート2本・アーカイブ接地・草川承認（テンプレ選択＋投稿前）。

---
name: project-ai-kusakawa
description: AIくさかわ（イラストキャラ×本人声クローンのAI代役ショート動画システム）の設計確定と実装状況
metadata: 
  node_type: memory
  type: project
  originSessionId: 8988e3f3-d2f0-4456-b2a9-158fd4b47644
---

# AIくさかわ（AI代役ショート動画）

2026-07-09 ブレスト→設計承認済。テキスト入力→「AIくさかわ」が本人の声で話す完成ショート動画（9:16・60秒以内）を全自動生成。撮影できない日の代役チャネル。

**確定方針**: ①AI明記で本人代役（AIあんの型・キャラ名＋AI生成表記必須）②外見=イラストキャラ（実写クローン不採用・誤認ゼロ）③声=ElevenLabs本人クローン④投稿可能な完成動画まで自動⑤方式=案B ローカル合成（ElevenLabs＋口パク3態PNG＋RMS同期＋ffmpeg。HeyGen等SaaS不採用）。

**設計書正本**: `~/.claude/scripts/ai-kusakawa/docs/2026-07-09-ai-kusakawa-design.md`

**パイプライン**: 台本=short-video-virality-architect→fact-checker→risk-reviewer→ElevenLabs音声＋タイムスタンプ→Python/ffmpeg合成（字幕y1240-1460・冒頭1.5秒AI明記カット）→sns-content-creator 7PF→Drive📱動画素材＋📣SNS投稿管理DB（タイトル先頭🤖🎬）。

**AI明記恒久ルール**: 冒頭表示＋常時小ラベル＋キャプション文頭「※この動画はAIが生成しています」。災害・選挙期間・他者言及はHIGH扱い本人判断。実写誤認編集禁止。選挙運動用流用は個別リスクレビュー。

**草川の手番**: ①クリア独り語り録音3〜5分＋ElevenLabsアカウント（Starter $5/月から）②nano-bananaキャラ生成（プロンプトカードはClaude作成・口3態＋表情差分）。

**状況**: 2026-07-09実装完了（全13テストPASS・devモードE2E動画目視済）。スキル=~/.claude/skills/ai-kusakawa/・エンジン=~/.claude/scripts/ai-kusakawa/。**草川手番待ち2つ**: ①声=ElevenLabs登録（手順=docs/SETUP_ELEVENLABS.md・聴取サンプル5本=~/outputs/ai-kusakawa/_voice_candidates/）②キャラ=nano-banana生成（カード=assets/character/prompt_cards.md・参照写真3枚Desktop配置済）。それまで仮キャラ＋devモードでプレビュー可・投稿不可。

**実装メモ**: このMacのffmpeg 8.1.1はass/subtitles/drawtextフィルタ非搭載→字幕は「Chrome headlessで透過PNGシート1回レンダ→ffmpeg crop＋overlay」方式（subtitles.py/compose.py）。口パクはRMS 2しきい値＋3フレーム中央値平滑。実キャラ投入時はconfig.pyのMOUTH_POS/MOUTH_SIZEだけ調整。

関連: [[project-photo-post-skill]] [[feedback_flyer_bright_illustration_style]]

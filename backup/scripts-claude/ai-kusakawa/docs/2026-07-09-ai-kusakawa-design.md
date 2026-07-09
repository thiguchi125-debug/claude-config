# AIくさかわ 設計書（v1・2026-07-09 草川承認済）

> テキストを打ち込むと「AIくさかわ」（本人公認のイラストキャラ×本人声クローン）が
> 話すショート動画を、投稿可能な完成品まで全自動生成する仕組み。
> 撮影できない日でも毎日発信を続けるための代役チャネル。

## 確定した方針（ブレスト結果）

| 論点 | 決定 |
|---|---|
| 見せ方 | **AI明記で本人代役**（「AIあんの」型。キャラ名＋AI生成表記必須） |
| 外見 | **イラストキャラ**（本人モチーフの似顔絵キャラ。誤認リスク構造的ゼロ） |
| 声 | **本人の声クローン**（ElevenLabs・日本語対応） |
| 完成形 | **投稿できる完成動画まで全自動**（本人は確認して投稿するだけ） |
| 実現方式 | **案B：ローカル合成型**（ElevenLabs＋口パクイラスト＋ffmpeg。SaaSアバター不使用） |

案Bの選定理由：①ランニングコスト最小（ElevenLabs $5〜22/月のみ）②外部サービス依存なしで2026選挙まで安定運用③既存short-video-create資産にそのまま接続④イラスト×口パクは一目でAIと分かる誠実さ＋キャラ愛着。

## 1. 全体パイプライン（新スキル `ai-kusakawa`）

```
入力: テーマ1行 or 台本全文
① 台本生成    short-video-virality-architect（既存・35〜45秒・voice-dna準拠）
              ※台本持ち込み時はスキップ
② 安全ゲート  content-fact-checker → content-risk-reviewer（既存・skip禁止）
③ 音声生成    ElevenLabs API（本人声クローン）→ mp3＋文字タイミング
④ 動画合成    Python＋ffmpeg ローカル一発合成
              - キャラ口パク3枚を音声RMSで同期（VTuber方式）
              - 字幕自動同期（y1240-1460帯・既存正本ルール）
              - 挿入図解（short-video-image-designer・任意）
              - 冒頭1.5秒「AIくさかわ｜AI生成動画」明記カット
⑤ 7PF投稿文  sns-content-creator（既存）
⑥ 保存        mp4→Drive📱動画素材／📣SNS投稿管理DB(1bd98deb-)に
              1ページ（タイトル先頭🤖🎬）
```

草川の操作＝「打ち込む→確認→投稿」。各PFのAI生成コンテンツラベルON は本人操作（手順書を同梱）。

## 2. 初期構築（一度だけ）

### 草川の手番（2つ）
1. **声クローン素材**: クリアな独り語り音声3〜5分（スマホ録音可・BGM/雑踏なし）。
   ~/Archive の既存録音の流用可否は実装時にClaude側で先に確認。
   ElevenLabsアカウント作成＋Instant Voice Clone登録。まずStarter（$5/月・約40本分）、
   品質不足ならCreator（$22/月）Professional Cloneに昇格。
2. **キャラ選択**: nano-bananaプロンプトカード（Claude作成）をGeminiで生成→
   2〜3スタイルから選択→同一キャラの口3態（閉/半開/開）＋表情差分を生成→投入。

### Claude側の構築物
- `~/.claude/scripts/ai-kusakawa/` — 合成エンジン（Python＋ffmpeg）
- `~/.claude/skills/ai-kusakawa/SKILL.md` — オーケストレータースキル
- キャラ用 nano-banana プロンプトカード（明るいイラスト路線
  feedback_flyer_bright_illustration_style 準拠・photo-curator選抜写真を参照素材に）
- 背景テンプレ2〜3種（草川カラー #c7ff4a/#1f5a3a/#0f3d27/#f3efe4・HTML/CSS→PNG）
- PF別AIラベルON手順書

## 3. 合成エンジン仕様（`~/.claude/scripts/ai-kusakawa/`)

- ElevenLabs API: text-to-speech with timestamps（eleven_multilingual_v2 or v3・ja）
  → 文字タイミングから字幕srt自動生成→ffmpegで焼き込み
- 口パク: 音声RMS解析（Python・しきい値2段）で口3態PNGを切替→フレーム列生成
- 出力: 9:16 1080×1920 mp4・60秒以内・字幕帯 y1240-1460
- APIキー: `~/.config/elevenlabs/api_key`（token類の既存慣例に合わせ ~/.config 配下）

## 4. AI明記の恒久ルール（memory化する）

- 動画冒頭1.5秒に「AIくさかわ｜AI生成動画」表示＋キャラ横に常時小ラベル
- キャプション文頭に「※この動画はAIが生成しています」固定
- 災害・選挙期間・他者言及を含む台本は risk-reviewer で HIGH 扱い→本人判断必須
- 実写の本人動画と誤認させる編集は禁止
- 公選法: 選挙運動用動画への流用は事前に個別リスクレビュー必須

## 5. コスト・運用

- ElevenLabs $5〜22/月のみ。他は全ローカル・既存資産。
- 品質検証: 初回はテスト動画1本を草川確認→OK後に定常運用。

## 6. スコープ外（YAGNI）

- リアルタイム対話（チャットボット化）— 将来検討
- 実写リップシンク・SaaSアバター（案A）— 不採用
- 自動投稿（投稿は必ず本人操作）

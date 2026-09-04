---
name: ai-kusakawa
description: 草川たくや（亀山市議会議員）の公認AIキャラクター「AIくさかわ」が本人の声クローンで話すショート動画（9:16・35〜50秒・目標45〜50秒・字幕・AI明記付き）を、テキスト入力から投稿可能な完成mp4まで1パスで自動生成するスキル。「AIくさかわ」「AIくさかわで動画」「AI動画作って」「AIくさかわに話させて」「AIくさかわでショート」等で起動。台本生成（short-video-virality-architect）→安全ゲート（content-fact-checker→content-risk-reviewer必須）→ElevenLabs音声→口パク合成（ローカルffmpeg）→7PF投稿文→📣SNS投稿管理DB保存＋Drive📱動画素材ミラーまで実行。※実写ショート動画→short-video-create、写真投稿→photo-post、挿入イラスト単体→short-video-image-designerが正で本スキルは反応しない。
---

# AIくさかわ 動画生成スキル

撮影できない日の代役チャネル。イラストキャラ「AIくさかわ」×本人声クローン×AI明記で、
テキストから投稿可能なショート動画を全自動生成する。

- 合成エンジン正本: `~/.claude/scripts/ai-kusakawa/`（設計書は同 `docs/`）
- 生成物: `~/outputs/ai-kusakawa/<日付>_<slug>/final.mp4`（絶対パス・cwd依存禁止）

## 前提チェック（起動時に毎回）

1. `~/.config/elevenlabs/api_key` と `voice_id` の存在確認。
   - **なければ本番生成不可**。`--dev`（合成音声プレビュー）しか出せない旨を草川に明示し、
     設定手順 `~/.claude/scripts/ai-kusakawa/docs/SETUP_ELEVENLABS.md` を案内する。
     devモード動画は**投稿禁止**（本人の声ではないため）。
2. `~/.claude/scripts/ai-kusakawa/assets/rendered/` に base_green/base_cream/intro/mouth_0-2 の6PNGがあること。
   欠けていれば `assets/templates/render_all.sh` で再レンダ。

## 工程（1パス）

### Step 1: 台本の用意
- **テーマだけ**渡された場合: short-video-virality-architect（SOLOモード・35〜50秒・目標45〜50秒・
  冒頭名乗りは「AIくさかわです」に置換・voice-dna準拠）で台本生成。
- **台本持ち込み**の場合: そのまま使用（60秒超過見込みなら短縮案を先に提示）。
- 冒頭名乗りは実写と区別するため「こんにちは、AIくさかわです。」を標準とする。

### Step 2: 安全ゲート（skip禁止）
1. content-fact-checker — 数値・固有名詞・計画名を一次情報まで検証
2. content-risk-reviewer — 8軸スキャン。**災害・選挙期間・他者言及を含む台本は一律HIGH扱い**
   → ASK_USERで草川判断。CRITICALは即停止。
3. ゲート通過後の台本を草川に提示→**承認を得てから**生成に進む。

### Step 3: 動画生成
```bash
# 台本をtxt保存してから
python3 ~/.claude/scripts/ai-kusakawa/generate.py <台本.txt> [--bg green|cream] [--slug <テーマ>]
# ElevenLabs未設定時のプレビューのみ: --dev を付ける（投稿禁止）
```
- 完成後 `open <final.mp4>` で草川が再生確認できる状態にする。
- 音ズレ・字幕切れ・口パク不同期があれば engine/config.py の該当値を調整して再生成。

### Step 4: 7PF投稿文
- sns-content-creator で7PF生成。**全PFのキャプション文頭に
  「※この動画はAIが生成しています」を固定挿入**（削らない・絵文字なし）。
- 動画ホスト3PF（TikTok/Shorts/Reels）=キャプション、
  クロスポスト4PF（X/Threads/Facebook/LINE）=動画リンク付きティーザー。

### Step 5: 保存
1. final.mp4 を Drive `📱動画素材/` へミラー（スマホから投稿できるように）。
2. 📣SNS投稿管理DB（ds=1bd98deb-）に1ページ保存。タイトル先頭に「🤖🎬」マーカー、
   各PF文をセクション化、動画のDriveパスを記載。
3. 投稿時のPF別AIラベルON手順 `docs/platform_ai_labels.md` を草川に案内。

## キャラ画像の差し替え（実キャラ投入時）

nano-banana生成画像（`assets/character/prompt_cards.md` 参照）が届いたら:
1. 画像を `assets/character/` に配置し、必ずReadで目視確認
2. base用に合成（口領域を空けた1080×1920）→ `assets/rendered/base_*.png` 差し替え
3. 口3態を `MOUTH_SIZE` にクロップ→ `mouth_0/1/2.png` 差し替え
4. `engine/config.py` の `MOUTH_POS`/`MOUTH_SIZE` を実キャラの口位置に合わせて調整
5. E2E再実行（`python3 -m unittest tests.test_e2e_dev`）＋フレーム抽出目視

## 📌 恒久ガードルール

- **AI明記4原則（絶対）**: ①動画冒頭1.5秒の明記カード ②キャラ横の常時小ラベル
  ③キャプション文頭「※この動画はAIが生成しています」 ④実写の本人動画と誤認させる編集禁止。
  いずれもトリミング・削除して投稿しない。
- **選挙運動用への流用は個別リスクレビュー必須**（公選法。content-risk-reviewerでHIGH扱い→本人判断）。
- devモード（合成音声）動画は内部プレビュー専用。対外投稿禁止。
- 安全ゲート（fact-checker→risk-reviewer）はいかなる短縮経路でもskip禁止。
- 発信物に絵文字を使わない（DB管理用タイトルの🤖🎬マーカーのみ例外）。
- 他議員の氏名を台本に載せない（feedback_no_other_council_members_names）。

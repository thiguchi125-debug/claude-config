---
name: photo-post
description: 草川たくや（亀山市議会議員）の写真1〜3枚＋ひとことから、投稿文→SNS投稿画像（1:1＋9:16・実写無加工のデザイン合成）→ショート動画（10〜20秒9:16）まで統合1パスで自動生成するスキル。「この写真で投稿作って」「写真を投稿用にして」「投稿画像にして」「写真から動画も」「photo-post」で起動。写真＋ひとことの同時投入も起動候補として提案。確認は切り口・デザイン選択と投稿前最終の2回のみ。安全ゲート（content-fact-checker→content-risk-reviewer＋写真固有軸）skip禁止。※「記録」を含む→nichijo、「メモ:」「保存して」→smart-intake、セリフ型ショート動画→short-video-create、イラスト挿入画→short-video-image-designer、投稿文のみ→sparkが正。
---

# photo-post — 写真＋ひとこと → 投稿文・画像・動画の統合1パス

設計正本: 同ディレクトリ `DESIGN.md`（2026-07-05草川承認）。以下は実行手順。

## 定数

- CHROME: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- テンプレ: `~/.claude/skills/photo-post/templates/`（card_band=下帯型/card_side=サイドバー型/card_full=座布団型/video_overlay/video_endcard）
- 動画: `~/.claude/skills/photo-post/scripts/make_video.sh -o OUT.mp4 -e ENDCARD.png [-t OVERLAY.png] PHOTO...`（写真1枚9秒/2枚各7秒/3枚各5秒＋エンドカード3.5秒・無音・9:16 1080×1920 30fps）
- 出力: `~/outputs/photo-post/<YYYY-MM-DD>_<テーマ>/`（絶対パス・cwd依存禁止）
- ブランド: ライム#c7ff4a／濃緑#1f5a3a／最濃緑#0f3d27／生成り#f3efe4・絵文字禁止・他議員氏名禁止

## Step 1: 受付

- 写真パス（1〜3枚）＋ひとことを受け取る。写真未指定で「いい写真選んで」→ photo-curator に候補3〜5枚出させて草川選択。
- HEIC は `sips -s format jpeg <src> --out <dst>.jpg` で変換。EXIF向きは `python3 -c "from PIL import Image, ImageOps; ImageOps.exif_transpose(Image.open('<src>')).save('<dst>')"` で正規化（位置情報も落ちる）。実写の生成的改変はしない（色調・トリミングのみ可）。
- 出力ディレクトリを先に `mkdir -p` してそこで作業する。
- モード判定:
  - **A 統合1パス（既定）**: 写真＋ひとこと → 以下全Step
  - **B 画像のみ**: 写真だけ/「画像だけ」→ Step 2の投稿文を作らず画像コピーのみ、Step 5スキップ
  - **C PAIR**: spark等から投稿文持ち込み → Step 2は文生成せずコピー抽出のみ

## Step 2: 接地＋文・コピー同時生成

- アーカイブ接地（省略禁止）: `grep -rl "<話題ワード>" ~/.claude/agents/knowledge/kusagawa_archive/{01_council,02_publications,05_resources,06_election}/` ＋草川独自表現も並列。ヒット1〜2件だけ読む。
- 同じ素材から一度に生成する:
  - (a) 投稿文 = 種のサイズに応じてX/Threads等1〜2PF・voice-dna整合・絵文字なし・禁止フレーム回避・架空エピソード禁止・おうむ返し禁止
  - (b) 画像用コピー = 見出し2行（H1A/H1B・各15字前後）＋サブ1行（SUB）＋タグ（TAG・#亀山市等）
- 文と画像コピーを別々に作らない（トーン統一＋燃費）。

## Step 3: ✋確認1回目（1画面で）

AskUserQuestion で提示: 切り口＋投稿文案＋デザイン3案（下帯型=王道・写真が主役／サイドバー型=情報整理・文字多め向き／座布団型=コピーが主役・写真は背景）＋動画要否（既定ON）。草川選択後に次へ。

## Step 4: 画像合成（EYES-FIRST）

1. 選択テンプレをコピーし `{{PHOTO}}`(file://絶対パス)/`{{H1A}}`/`{{H1B}}`/`{{SUB}}`/`{{TAG}}`/`{{FOCUS}}`(既定 `center 35%`・被写体位置に合わせ調整) を置換（sed可）。
2. レンダ2枚:
   ```
   "$CHROME" --headless --disable-gpu --hide-scrollbars --screenshot=<out>_sq.png --window-size=1080,1080 file://<html>
   "$CHROME" --headless --disable-gpu --hide-scrollbars --screenshot=<out>_9x16.png --window-size=1080,1920 file://<html>
   ```
3. **PNGを自分でReadして検品**（サブagent委譲禁止）: 文字切れ・重なり・被写体と帯の衝突・コントラスト。崩れは font-size/FOCUS を調整して再レンダ（最大3周）。可読性フロア: 最小フォント21px相当・9:16はSNS UIセーフゾーン（下240px/右150pxに重要要素を置かない）。

## Step 5: 動画生成（既定で続行・追加入力不要）

1. video_overlay.html に H1A/H1B を差し込み→透過レンダ: `--default-background-color=00000000 --window-size=1080,1920` → overlay.png
2. video_endcard.html に TAG を差し込み→通常レンダ 1080×1920 → endcard.png
3. `make_video.sh -o <出力dir>/video.mp4 -e endcard.png -t overlay.png <写真...>`
4. 中間フレームを1枚抜いて（`ffmpeg -ss 4 -i video.mp4 -frames:v 1 frame.png`）Readで合成確認。

## Step 6: 安全ゲート（skip禁止・まとめて1回）

content-fact-checker（投稿文・コピー内の数値/固有名詞/計画名）→ content-risk-reviewer（8軸＋**写真固有軸**: 第三者の顔・子どもの顔・車ナンバー・個人宅特定・位置情報・公選法文書図画）。指示文に「画像PNG・動画フレームも確認対象」と明記。HIGH以上はASK_USER・CRITICAL即停止。

## Step 7: ✋確認2回目（最終）→保存

1. 完成セット（投稿文＋画像2枚＋動画）を提示→草川OK後に**1回で**保存（D2原則）。
2. 保存:
   - `~/outputs/photo-post/<日付>_<テーマ>/` に全ファイル
   - Drive `~/Library/CloudStorage/GoogleDrive-t.higuchi125@gmail.com/マイドライブ/📱動画素材/` へ画像・動画を cp ミラー
   - 📣SNS投稿管理DB（ds `1bd98deb-`）に1ページ（タイトル先頭📸・投稿文全文＋画像/動画のDriveパス記載・ステータス=未着手）
3. nichijo日次ログに🔖台帳1行: `🔖 HH:MM 〈テーマ15字〉→photo-post → <mention-page url="...">ページ名</mention-page>`
4. 出来が良いレイアウトが生まれたら design_system への「SNSカード」テンプレ昇格を提案（強制しない）。

## やらないこと

- 写真自体のAI生成改変（nano-banana等）。明示依頼時のみ nanobanana-prompt-designer のプロンプトカードをおまけ出力（手貼り用）し、改変画像の投稿は risk-reviewer 必須＋「AI加工」明示を条件とする。
- 7PF一括生成（sns-content-creator）・セリフ型ショート動画（short-video-create）・印刷物（design-studio）。
- BGM付与・本人ナレーション（スマホ編集の領分）。

## 📌 恒久ガードルール

（実運用フィードバックをここに追記する — feedback_rules_reside_in_agents 運用）

---
name: photo-post
description: "写真1〜3枚＋ひとこと→投稿文→SNS投稿画像（1:1＋9:16・実写無加工合成）→10〜20秒ショート動画まで1パス。確認は切り口選択と投稿前の2回。ゲートskip禁止。Triggers: この写真で投稿作って/写真を投稿用にして/投稿画像にして/写真から動画も。NOT: 「記録」→nichijo、セリフ型動画→short-video-create"
---

# photo-post — 写真＋ひとこと → 投稿文・画像・動画の統合1パス

設計正本: 同ディレクトリ `DESIGN.md`（2026-07-05草川承認）。以下は実行手順。

## 定数

- CHROME: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- テンプレ: `~/.claude/skills/photo-post/templates/`（card_band=下帯型/card_side=サイドバー型/card_full=座布団型/video_overlay/video_endcard）
- 動画: `~/.claude/skills/photo-post/scripts/make_video.sh -o OUT.mp4 -e ENDCARD.png [-t OVERLAY.png] PHOTO...`（**合計10秒以内**＝写真1枚6.5秒/2枚各3.4秒/3枚各2.4秒＋エンドカード2.5秒・無音・9:16 1080×1920 30fps。よほどの品質でなければ10秒超は完視聴が落ちる＝2026-07-05草川指示）
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

## Step 4: 画像合成（固定順序＝参照→採寸→写真→レンダ→機械採点→目視1回→模写採点・2026-09-05／09-15）

### 4-R 参照1本＋5軸目標（着手前・skip禁止）

（2026-09-15 草川指示で追加・正本＝memory feedback_design_reference_library_first）

1. `~/.claude/agents/knowledge/design_system/references/_INDEX.md` から**写真主体のSNS投稿画像の参照を1本だけ**選び、**画像を自分でReadする**（カルテを読むだけで進まない）。1:1と9:16は同じテンプレの2レンダなので参照は共有する。Step3で選ばれたテンプレ（下帯型／サイドバー型／座布団型）に構図が近いものを選ぶ。
2. 5軸目標を**数値で**書き出す（下の0と同じメモに）: ①級数ジャンプ率 **○倍**（H1÷SUB）②色数 **○色**と役割 ③図形語彙 ④写真占有率 **○%** ⑤アイコン・図形アクセント **○点**。
   - **実写無加工の制約が優先**。②③⑤は**デザインレイヤー（帯・座布団・タグ・幾何アクセント）だけで数え、写真の中の色は色数に入れない**。
   - ④は写真を加工せず**テンプレの選択とトリミング（`{{FOCUS}}`・帯幅）で合わせる**。参照の写真占有率に届かないなら帯を細くするか下帯型へ寄せる。写真に図形を重ねて占有率を削る方向には動かさない。
   - ⑤は、参照がイラスト主体なら**その参照は選ばない**（写真主体の参照に取り替える）。参照がアイコン・図形アクセントを使うなら、デザインレイヤーにピル・角マーカー等で入れる。被写体の顔・主題に重ねない。絵文字・人物イラストは使わない。
3. **参照未整備時（2026-09-15時点で該当＝1:1・9:16の判型フォルダが無い）**: Step3の確認画面に「参照未整備」と1行添え、作る前に **design-inspiration-researcher** を起動してプロ制作の写真主体SNS投稿画像（報道機関・自治体・公的機関の公式アカウント等。議員の自作物は不可）を1〜3本収集→ `references/sns_photo/` へ画像＋`_karte.md`（5軸採寸）を回収し `_INDEX.md` に行を足してから入る。`thumbnail/`（16:9）は判型が別なので代用しない（memory feedback_reference_must_match_format）。
   - 収集できない場合のみ、草川に「参照なしで作る」と明示し、下の5の模写採点は「参照未整備のため未実施」と記録する。黙って飛ばさない。

### 4-S 採寸→合成→採点

0. **採寸を先に確定**: `~/.claude/scripts/specs.json` の `image.1:1`／`image.9:16`（読み込み口 `specs.py`）からセーフ域・最小級数を読み、H1の級数・`{{FOCUS}}`（被写体位置・顔は画面高25〜35%）を**着手前に決めて書き出す**。
1. 選択テンプレをコピーし `{{PHOTO}}`(file://絶対パス)/`{{H1A}}`/`{{H1B}}`/`{{SUB}}`/`{{TAG}}`/`{{FOCUS}}`(既定 `center 35%`・被写体位置に合わせ調整) を置換（sed可）。
2. レンダ2枚:
   ```
   "$CHROME" --headless --disable-gpu --hide-scrollbars --screenshot=<out>_sq.png --window-size=1080,1080 file://<html>
   "$CHROME" --headless --disable-gpu --hide-scrollbars --screenshot=<out>_9x16.png --window-size=1080,1920 file://<html>
   ```
3. **機械採点が通るまで目視しない**: `python3 ~/.claude/scripts/check_overflow.py --canvas 1080x1080 <html>`／`--canvas 1080x1920`、`feed_preview.py still <1:1画像>`／`short <9:16画像>` で縮小コンタクトシートを作る。FAILは font-size/FOCUS の数値を直して再レンダ。可読性フロア: 最小フォント21px相当・9:16はSNS UIセーフゾーン（下240px/右150pxに重要要素を置かない）。
4. **目視は最後の1回＝PNGを自分でRead**（サブagent委譲禁止）: 文字切れ・重なり・被写体と帯の衝突・コントラスト。崩れは数値を直して再レンダ→再度3から（最大3周）。
5. **模写採点（skip禁止・2026-09-15追加）**: 4-Rの参照画像と出力PNG（1:1・9:16の2枚）を**両方自分でRead**し、5軸を数値比較（サブagent委譲禁止）。可の基準＝①参照の70%以上 ②参照−1色まで ③参照の語彙の半分以上 ④参照の70%以上 ⑤参照が使うなら必ず使う。**各画像5軸中4軸「可」で合格**、不合格はテンプレ・級数・FOCUSの数値を直して2へ戻る。採点5行×2枚と**素材の使い残し**（渡された写真枚数 vs 画像・動画で使った枚数）1行をチャットに出す。
6. **配信面ゲート（勝負所のみ・投稿画像は原則通す）**: 3のコンタクトシートを持って **`feed-visual-reviewer`** を起動し `PASS` を取る。原寸で読めても実表示幅（400px/グリッド180px）で潰れていれば不合格。写真上の文字が読みにくい指摘は対症療法せずテンプレ変更（座布団型等の構造分離）で解決。natural-design-reviewer は紙の物理破綻用なので投稿画像では呼ばない。

## Step 5: 動画生成（既定で続行・追加入力不要）

1. video_overlay.html に H1A/H1B を差し込み→透過レンダ: `--default-background-color=00000000 --window-size=1080,1920` → overlay.png
2. video_endcard.html に `{{PORTRAIT}}`/`{{SLOGAN}}`/`{{TAG}}` を差し込み→通常レンダ 1080×1920 → endcard.png
   - デザイン = **枠付きフォトカード**（本人写真をライム枠のカードに額装＋幾何アクセント＋スローガン＋名前）。実写のAI改変・白背景の切り抜きはしない（襟と背景が同じ白で破綻しやすい＝2026-07-05検証で確認）。
   - `{{PORTRAIT}}` = `file://~/.claude/skills/photo-post/assets/kusagawa_portrait_src.jpg`（拳ポーズ公式写真・**常用ブランド素材**。白背景のままカードに額装するので無加工でよい）
   - `{{SLOGAN}}` = 既定 `声をチカラに`（または `ええやん亀山`。「声を、チカラに。」の句読点付きは使わない）
   - `{{TAG}}` = `#ええやん亀山` 等
   - （`scripts/cutout_portrait.py` は GrabCut 透過切り抜きの実験実装として残置。現行エンドカードは枠付きカード方式のため通常は使わない。）
3. `make_video.sh -o <出力dir>/video.mp4 -e endcard.png -t overlay.png <写真...>`
4. 末尾付近のフレームを1枚抜いて（`ffmpeg -ss <尺-1> -i video.mp4 -frames:v 1 frame.png`）Readでエンドカード（人物と文字の重なり無し）を確認。

## Step 6: 安全ゲート（skip禁止・まとめて1回）

content-fact-checker（投稿文・コピー内の数値/固有名詞/計画名）→ content-risk-reviewer（8軸＋**写真固有軸**: 第三者の顔・子どもの顔・車ナンバー・個人宅特定・位置情報・公選法文書図画）。指示文に「画像PNG・動画フレームも確認対象」と `ledger: <このテーマの保存先>/_ledger.json` の1行を明記（テーマ内台帳）。画像・動画に焼く文言が投稿文と同一なら別起動せず台帳から継承する。HIGH以上はASK_USER・CRITICAL即停止。

## Step 7: ✋確認2回目（最終）→保存

1. 完成セット（投稿文＋画像2枚＋動画）を提示→草川OK後に**1回で**保存（D2原則）。
2. 保存:
   - `~/outputs/photo-post/<日付>_<テーマ>/` に全ファイル
   - Drive `~/Library/CloudStorage/GoogleDrive-t.higuchi125@gmail.com/マイドライブ/📱動画素材/` へ画像・動画を cp ミラー
   - 📣SNS投稿管理DB（ds `1bd98deb-`）に1ページ（タイトル先頭📸・投稿文全文＋画像/動画のDriveパス記載・ステータス=未着手）
3. nichijo日次ログに🔖台帳1行: `🔖 HH:MM 〈テーマ15字〉→photo-post → <mention-page url="...">ページ名</mention-page>`
4. 出来が良いレイアウトが生まれたら design_system への「SNSカード」テンプレ昇格を提案（強制しない）。

## やらないこと

- 写真自体のAI生成改変（nano-banana等）はしない。AI画像生成ルートは 2026-09-05 に廃止（画像は HTML/CSS→Chrome→PNG のみ）。
- 7PF一括生成（sns-content-creator）・セリフ型ショート動画（short-video-create）・印刷物（design-studio）。
- BGM付与・本人ナレーション（スマホ編集の領分）。

## 📌 恒久ガードルール

（実運用フィードバックをここに追記する — feedback_rules_reside_in_agents 運用）

### 写真＋動画＋ひとことの発信依頼は最初からフル（合成画像＋動画）を回す（2026-07-05）
「SNS投稿：〜」＋写真3枚＋動画の依頼で、テキスト仕上げ＋安全ゲートだけで止めて提示→草川「写真が何も編集されてない、デザイン合成じゃないのか」「言われたことは全てやれ」と強い叱責。写真・動画が素材として渡された時点で期待は本スキルの完成形（実写無加工＋デザインレイヤー合成の1:1＋9:16＋ショート動画）まで。
- 写真（1〜3枚）＋ひとこと/投稿文＋（あれば動画）が来たら**モードAをフルで自走**（投稿文→合成画像→動画→安全ゲート→Drive/Notion保存→nichijo🔖台帳）。テキストだけ返して止めない
- 確認はStep3・Step7の2回まで。判断済みの点を蒸し返さない
- 締め（📱動画素材ミラー・📣投稿管理DB保存・🔖台帳）まで自走して完了扱いにする

### 各写真は必ずRead（画素確認）してから採否・ラベル付けする
ファイル名から中身を推測して「PXL_...517＝ヘリ」と誤認し、実際は体育館全景（顔写り込み＝掲載見送り対象）を動画に混入させかけた（2026-07-05）。肖像権NGと決めた写真の取り違えは事故になる。複数枚はコンタクトシート1枚を生成して自Readし、ファイル名→内容→縦横を確定してから進む（content-pipeline も同手順）

- **投稿画像も参照1本＋5軸目標→模写採点（5軸中4軸で可）を通す**。実写は加工せず、5軸はデザインレイヤーとテンプレ・トリミングで合わせる（2026-09-15・正本＝memory feedback_design_reference_library_first）
- **規格値の正本は `~/.claude/scripts/specs.json`。発信物として保存する前に `~/.claude/scripts/gate.py` を通す**（2026-09-05追記）

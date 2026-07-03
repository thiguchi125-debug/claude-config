---
name: short-video-create
description: 草川たくや（亀山市議会議員）のショート動画を「セリフ生成→ファクトチェック→リスクレビュー→nano-banana画像プロンプト生成→**全7プラットフォーム投稿文生成**→📣SNS投稿管理DB保存」まで1パスで完結させるオーケストレータースキル。「ショート動画作って」「動画作って画像も」「TikTokセット作って」「Reels一式」「セリフから画像までセットで」「ショート動画フルパッケージ」「動画と投稿文一式」「動画＋SNS全部」「short-video-create」等で起動。テーマだけ与えればshort-video-virality-architectでセリフを生成（35〜45秒・冒頭名乗り＋決意型）、既存セリフがあればそれを使い、いずれの場合もcontent-fact-checker→content-risk-reviewer→挿入ビジュアル生成（**説明図＝HTML/CSS→PNGで草川カラー制作／雰囲気イメージのみnano-banana**）→sns-content-creator（7PF同時生成）を直列で通し、最後に📣SNS投稿管理DB(1bd98deb-)へタイトル先頭🎬・各PFをセクション化して1ページに保存する。完成PNGはスマホ編集用にDriveミラー📱動画素材へ配置。動画ホスト3PF（TikTok/Shorts/Reels）はキャプション、クロスポスト4PF（X/Threads/Facebook/LINE）は動画リンク付きティーザーとしてPF別最適化。サイズ指定忘れ・公選法チェック漏れ・Notion保存先迷子・画像プロンプト後追い忘れ・SNS展開後追い忘れを構造的に防ぐ。
---

# short-video-create スキル

## 目的
草川がショート動画を作るたびに発生していた以下の手作業を1パスで吸収する:
1. セリフ生成（short-video-virality-architect 呼び出し）
2. ファクトチェック（content-fact-checker）
3. リスクレビュー（content-risk-reviewer）
4. **nano-banana画像プロンプト生成（nanobanana-prompt-designer）** ← かつて毎回忘れていた
5. **全7プラットフォームSNS投稿文生成（sns-content-creator）** ← 新規追加 2026-05-21
6. 📣SNS投稿管理DB保存（タイトル🎬・プロパティ整備・PF別セクション化）

特に以下のループを構造的に潰す:
- **「セリフは作ったけど画像プロンプトは別セッションで頼む→サイズ指定忘れる→やり直し」**
- **「動画は撮ったけどSNSへの拡散文を別途作るのを忘れて投稿タイミング逃す」** ← 新規対策

7PF全自動化により、動画を撮影UP後すぐに各SNSへコピペで展開可能な状態になる。

## 起動条件

以下のいずれかが含まれる発言で起動:
- 「ショート動画作って」「ショート動画一式」「ショート動画フルパッケージ」
- 「動画作って画像も」「セリフから画像までセットで」
- 「TikTokセット」「Reels一式」「YouTube Shorts一式」
- 「short-video-create」

明示的なトリガーがなくとも、以下の文脈で**草川に1問だけ確認してから起動**:
- 「〇〇でショート動画」と言われた時 → 「画像プロンプトもセットでいく？」
- 「ショート動画磨いて」と言われ画像未整備の時 → 「画像プロンプトも一緒に作る？」

## 委譲先（このスキルが呼ばないもの）

- **静止画のみのSNS展開**（動画なし） → sns-content-creator 単独
- **AIインタビュー結果からのSNS化** → ai-interview-sns-poster
- **長尺YouTube台本（>90秒）** → 対象外（長尺は作らない方針・video-content-strategistは2026-07-02廃止）
- **既存画像ライブラリからの選定** → photo-curator
- **印刷物** → print-designer

ただし、**動画＋SNS展開セット**は本スキルが内部的に sns-content-creator を呼んで一括処理する（草川が別途呼び直す必要はない）。

## 入力（草川から取得）

### 必須
- **テーマ または セリフ全文**（どちらか）
  - テーマだけ → short-video-virality-architectで3バリアント生成
  - セリフ全文 → そのまま使う
- **target_length**: 30秒 / 60秒 / 90秒（既定60秒）

### 任意（未指定はデフォルト値で進む）
- **target_platforms**: TikTok / YouTube Shorts / Instagram Reels（複数可・既定3つ全部）
- **crosspost_platforms**: X / Threads / Facebook / LINE（複数可・既定4つ全部）— 動画リンクをティーザー文と共にクロスポスト
- **num_images**: 2〜5枚（既定3枚）
- **aspect**: 9:16 / 1:1 / 16:9（既定9:16）
- **tonal_arc**: 暖→寒 / アナログ→デジタル / before→after など（未指定時は内容から自動推定）
- **source_url**: 元素材があれば
- **citizen_voice**: 市民の声があれば（最優先素材）
- **video_only**: true なら SNS投稿文生成をスキップ（既定 false = 7PF全生成）

## 処理フロー（8ステップ・完全自動）

### Step 1: 入力解析・分岐判定

```
if 入力 == テーマだけ:
    mode = "from-theme"
    → Step 2 へ（セリフ生成）
elif 入力 == セリフ全文:
    mode = "from-script"
    → Step 3 へ（fact-checkから直行）
elif 入力 == 既存原稿の昇格依頼:
    mode = "polish"
    → short-video-virality-architect Polishモード → Step 3
```

### Step 2: セリフ生成（from-theme時のみ）

**並列起動**:
- `short-video-virality-architect`（Soloモード）

入力に渡すもの:
- topic / target_length / target_platforms / citizen_voice / source_url
- voice-dna・policy_compass 参照は agent 側で実施

出力期待値:
- 3バリアント（A: hook最強 / B: 感情ストーリー / C: 議論誘発）
- 各バリアントのカット表（秒単位）
- 8軸スコア（合格点64/80）

**草川好みのセリフ構成（2026-06-02反映）**: ①最強フック1.5秒 → ②**名乗り＋「最近このご意見がめちゃくちゃ多いんです」**（＝撮っている理由） → ③本論1メッセージ → ④**結びの決意「私は必ず実現させます／あきらめません」** → ⑤コメント誘発。尺は**35〜45秒厳守**（名乗り＋決意込みでも50秒以内）。冒頭の名乗りはコールドオープン回避のため**フックの後ろ**に置く。詳細 [[feedback_short_video_use_virality_architect_first]] [[feedback_kusagawa_short_video_script_style]]。

草川に提示し **どのバリアントで進めるか1問だけ確認**（A/B/C）。承認後にStep 3へ。

### Step 3: ファクトチェック

`content-fact-checker` を起動:
- セリフ内の数値・固有名詞・法令・統計を一次情報まで遡及
- 修正必要箇所があれば草川に提示→承認後に修正

### Step 4: リスクレビュー

`content-risk-reviewer` を起動:
- 8軸（個人情報・機密・公選法・名誉毀損・差別・利益相反・品位・物議）
- HIGH以上検出時は ASK_USER で草川判断仰ぐ
- CRITICAL は即停止・草川通知
- **公選法メモ（2026-06-02）**: 政策実現の決意「必ず実現させます／あきらめません」は**告示前の今は事前運動に当たらず投稿可**（投票依頼・選挙明示・期数言及がなければOK）。ただし**2026年9月頃の告示日以降は同表現での再投稿・固定掲示NG**（選挙運動判定域）。保存ページにこの運用注記を残す。
- **市・執行部は「市の姿勢／市の答弁」止まり**で名指し批判しない。**別議員が引き出した数字・市長答弁を草川が引き出したように繋げない**（質疑応答の誤帰属注意 [[feedback_giji_kusagawa_response_only]]）。

### Step 5: 挿入ビジュアル生成（2ルート分岐・2026-06-02改訂）

挿入画像は用途で2ルートに分ける。**草川に「説明図メイン？／イメージメイン？」を1問確認**（または内容から自動推定）。**多くの政策ショートはルートA（説明図）が主役、ルートBは補助**。

#### ルートA【推奨・データ/説明系】説明図インフォグラフィック（HTML/CSS → PNG）

「全国9割」「23/29市町」「年齢の崖」「Before/After」など**数字・比較・構造を理解させる図**は、AI画像生成を使わず **HTML/CSSで設計して Chrome で PNG化**する（print-designer と同じ作り方）。

- **理由**: nano-banana は日本語・数字を崩す＋写真は雰囲気だけで情報量ゼロになりがち（2026-06-02 子ども医療費動画で「微妙」「情報少なすぎて何の画像か分からない」と本人NG）。説明図HTML→PNGなら**正確な日本語＋数字＋出典**が入り崩れない。
- **草川ブランドカラー必須**: ライム `#c7ff4a`（キーワードのハイライト下線＝`box-shadow:inset 0 -0.26em 0 #c7ff4a`）／ディープグリーン `#1f5a3a`・`#0f3d27`／クリーム背景 `#f3efe4`。リーフレットと統一（[[feedback_leaflet_design_principles]]）。**勝手にアンバー＋ネイビー等にしない**。
- **スタイル**: ニュースフリップ調 ＝ kickerピル（深緑地＋ライム点） → 見出し[キーワードにライム下線] → 中央ビジュアル[人型比率／マス目グリッド／アイコンカード／年齢チャート等] → 出典付きキャプション（一次出典明記）。
- **サイズ**: 1080×1920（9:16）。レンダリング:
  ```
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
    --hide-scrollbars --force-device-scale-factor=1 --window-size=1080,1920 \
    --default-background-color=FFFFFFFF --screenshot=out.png "file://<html絶対パス>"
  ```
  出力後 `sips -g pixelWidth -g pixelHeight out.png` で 1080×1920 を確認し、Read で目視チェック→字割れ・はみ出しを修正。
- **HTMLソースも残す**（数字・文言の微修正→即再レンダリング可能・ガチャ不要）。
- **雛形**: `~/outputs/daily-content/2026-05-27/kodomo-iryouhi-18-musho/infographics/` の既存5枚（人型比率／年齢の崖／3場面アイコンカード／29マスグリッド／強調ピン）を流用・改変するのが最速。

#### ルートB【雰囲気/イメージ系】nano-banana画像プロンプト

卒業式・病院待合など**雰囲気B-rollや抽象イメージ**は `nanobanana-prompt-designer`（PAIRモード）でプロンプト生成:
- 入力: 確定したセリフ全文＋秒単位カット表 / パラメータ: num_images / aspect / tonal_arc
- 出力: N枚の画像プロンプト（冒頭にサイズ指定必須）＋配置マップ＋使い方Tips
- ⚠️ **Gemini API の画像生成は無料枠 0（`limit:0`）**。自動一括レンダリングは**課金必須**（1枚≈6円）。**無料でやるなら手動**＝AI Studio（aistudio.google.com）or Geminiアプリでプロンプトを1枚ずつ生成（スマホならGeminiアプリが楽だが9:16が出にくい→編集でトリミング）。「API無料で全自動」と案内しない。
- プロンプト末尾に `CRITICAL: generate NO text, no kanji, no numbers`（文字は崩れるのでCapCut/Canva後乗せ）。公選法・個人情報ガード内蔵（顔なし・実在ロゴ/学校名なし・他議員なし）。

#### 共通: スマホ編集前提なら完成画像をDriveへ

草川は**動画編集をスマホ（CapCut）でやる**ことが多い。完成PNG（ルートA/B問わず）は Google Driveミラー
`~/Library/CloudStorage/GoogleDrive-t.higuchi125@gmail.com/マイドライブ/📱動画素材/<YYYY-MM>_<テーマ>/`
にコピーする。→ スマホのDriveアプリ→カメラロール→CapCut で取り込める。ファイル名は挿入順（a1,a2,…）で並ぶようにする。

### Step 6: 全7プラットフォームSNS投稿文生成（新規・2026-05-21）

`sns-content-creator` を起動（**video-aware モード**）:

**入力に渡すもの**:
- 確定したセリフ全文（fact-check / risk-review済み）
- 動画メタ情報（テーマ / 長さ / 採用バリアント / voice-dna軸）
- target_platforms（動画ホスト）+ crosspost_platforms（クロスポスト）
- ハッシュタグ素材（テーマ・分野・地名「亀山市」必須）

**video_only=true なら本ステップをスキップ**。

**出力期待値**: 7PF分の投稿文セット。各PF最適化済み：

#### 動画ホスト3PF（動画本体を載せる場所）

| PF | 文字数 | フォーマット | ハッシュタグ |
|---|---|---|---|
| **TikTok** | 150字以内 | 1行フック → 1行核心メッセージ → コール（CTA） | 3〜5個（#亀山市 #市議会 #テーマタグ） |
| **YouTube Shorts** | 説明欄 100〜300字 + ハッシュタグ | フック → 動画の中身予告 → 草川自己紹介1行 → CTA | 5〜8個（SEOキーワード厚め） |
| **Instagram Reels** | 600〜1000字 | 詩的・ストーリー型導入 → 詳細展開 → CTA → ハッシュタグ束 | 10〜15個（広域ハッシュタグ含む） |

#### クロスポスト4PF（動画リンクを貼って拡散）

| PF | 文字数 | フォーマット | 動画リンク扱い |
|---|---|---|---|
| **X (Twitter)** | **140字厳守** | 強フック1文 + 動画リンク + 1〜2ハッシュタグ | リンク必須 |
| **Threads** | 300〜500字 | 問いかけ型導入 → 共感 → 動画への誘導 → CTA | リンク or 「詳しくは動画で」誘導 |
| **Facebook** | 500〜800字 | 論理型・背景説明 → 動画の意義 → CTA | リンク or 動画埋込 |
| **LINE公式** | 300〜500字 | アナウンス型「市議会の最新動画」 → 要点3行 → 動画リンク | リンク必須 |

**各PF共通の必須要素**:
- voice-dna軸（伝える/繋ぐ/希望）に整合
- 「亀山市」「亀山市議会議員」など草川識別ワード1回以上
- voice-dna NG表現リスト回避（「届かないを終わらせる」「最後の100m」等）
- 公選法配慮（投票依頼・寄附該当表現含めず）

**ライト再チェック**:
- セリフから抜き出した範囲は再check不要（既に通過済）
- SNS文で**新規に追加した情報**（ハッシュタグの誤字・統計の付け足し等）のみ content-fact-checker でスポット確認
- 各PF文を content-risk-reviewer に**まとめて1回**通す（個別では非効率）

### Step 7: 統合パッケージ提示

草川に以下を1メッセージで提示:

```markdown
# 🎬 ショート動画フルパッケージ「<テーマ>」

## 📋 メタ
- 長さ: 60秒
- 動画ホスト: TikTok / YouTube Shorts / Instagram Reels
- クロスポスト: X / Threads / Facebook / LINE
- 採用バリアント: B（感情ストーリー）
- 8軸スコア: 72/80 ✅
- fact-checker: ✅ / risk-reviewer: ✅

## 🎤 セリフ・カット表
（秒数 / ナレ / 画 / テロップ）

## 📸 nano-banana画像プロンプト 3枚
（Image 1 / Image 2 / Image 3 各々サイズ指定済み）

## 🎬 配置マップ
| 秒 | ナレ | 画 |

## 💡 nano-banana 使い方Tips
（AI Studio URL / ガチャ対策 / 連続性）

## 📱 SNS投稿文セット（全7PF・コピペ運用）

### 動画ホスト3PF
- **TikTok**（150字以内）: <投稿文 code block>
- **YouTube Shorts**（説明欄）: <投稿文 code block>
- **Instagram Reels**（600〜1000字）: <投稿文 code block>

### クロスポスト4PF（動画リンク `<VIDEO_URL>` 含む）
- **X**（140字厳守）: <投稿文 code block>
- **Threads**（300〜500字）: <投稿文 code block>
- **Facebook**（500〜800字）: <投稿文 code block>
- **LINE公式**（300〜500字）: <投稿文 code block>

文字数チェック: 全PF✅ / NG表現スキャン: ✅ / 公選法: ✅

---
**草川承認後、📣SNS投稿管理DBへ保存します。OK?**
```

### Step 8: Notion 📣SNS投稿管理DB 保存

草川承認後、`notion-saver` agent（または直接MCP）で保存:

**DB**: 📣SNS投稿管理DB
- database_id: `78f40f33-ae71-4f32-9cc3-b00c0a36707c`
- data_source_id: `1bd98deb-624f-402c-aeb3-bdaa4782b389`

**プロパティ**:
- **投稿タイトル**: `🎬【ショート動画＋SNS7PF】<テーマ要約>`
- **ステータス**: `進行中`（DBに「下書き完成」選択肢ないため）
- **プラットフォーム** (multi_select): 動画ホスト3PF＋クロスポスト4PF を全てチェック（YouTube / TikTok / Instagram / X / Threads / Facebook / LINE）
- **分野**: テーマから自動判定（行政/福祉/子育て/教育/防災/産業/交通/環境/都市計画/その他）
- **ネタ元**: 議会/委員会・日次活動・市民相談・行政資料・SNS/新聞 のいずれか
- **アイコン**: 🎬

**page content（セクション順）**:
1. メタ情報（テーマ・長さ・PF・voice-dna軸・採用バリアント）
2. 安全ゲート判定（fact-checker / risk-reviewer 結果）
3. **セリフ・カット表**（採用バージョン）
4. **nano-banana画像プロンプト一式**（Image 1〜N、各々code blockで copy-and-paste 可能形式）
5. nano-banana使い方Tipsフッター
6. 配置マップ
7. タイトル案・サムネ案
8. **📱 SNS投稿文セット（7PF）— 動画UP後のコピペ展開用**
   - 8-A. TikTok 投稿文（code block）
   - 8-B. YouTube Shorts 説明欄（code block）
   - 8-C. Instagram Reels キャプション（code block）
   - 8-D. X 投稿文（140字厳守・code block）
   - 8-E. Threads 投稿文（code block）
   - 8-F. Facebook 投稿文（code block）
   - 8-G. LINE公式 アナウンス（code block）
   - 8-H. ハッシュタグ群（PF別表）
9. 横展開メモ（ブログ深掘り提案）
10. アンチ想定＋返信案
11. 撮影前チェックリスト
12. **公開後タスク** — 動画UP後の作業フロー（YouTube/TikTok/Reelsの順でUP→クロスポスト4PFは動画URL確定後コピペ→Notion ステータスを「完了」に）
13. リサーチソース・元素材URL

## 出力フォーマット（草川画面）

Step 7で示すフルパッケージ＋Step 8でNotion保存後に保存先URLを1行で報告:

```
✅ 保存完了: <NotionページURL>
   →動画ホスト3PFにUP後、ページ内のcode blockを各SNSにコピペでクロスポスト
   →説明図PNGは 📱動画素材/<日付>_<テーマ>/ に配置済（スマホDrive→CapCut取込可）
   →雰囲気イメージは AI Studio/Geminiアプリ で手動生成（API無料枠は0）
```

## ⚡ トークン効率化方針

- リサーチは並列・必要最小限（playbook全読みは agent 任せ）
- fact-checker / risk-reviewer は順次直列（並列にすると修正が二重発生）
- nanobanana-prompt-designer の出力は code block 必須（コピペ運用のため）
- **sns-content-creator はセリフ確定後の単一呼出（PF別個別呼出は禁止・トークン3倍化する）**
- **SNS再チェックは7PF分まとめて1回（個別チェックNG）**
- Notion保存は1回だけ（途中保存禁止、承認後一発・7PF分のセクションを同時に書く）
- 目標トークン: 120〜180K（SNS生成追加後の新基準）

## 🚦 失敗時のフォールバック

| 失敗 | 対応 |
|---|---|
| short-video-virality-architectが64点未満連発 | 草川に「テーマ角度を変えるか、別agentで素材集めるか」確認 |
| fact-checkerでファクト崩壊 | 該当部分削除or修正→risk-reviewerに進む |
| risk-reviewerでCRITICAL | 即停止・草川判断仰ぐ、Notion保存しない |
| nanobanana-prompt-designerで人物顔含む | 自動的に手元・モノ・後ろ姿に書き換え |
| **sns-content-creator がX 140字超過** | 即圧縮（要点だけ残す）→再チェック、3回失敗で草川に「Xは手動短縮」依頼 |
| **sns-content-creator がvoice-dna NG表現混入** | 該当箇所のみ書き直し（全文再生成NG・トークン無駄） |
| **クロスポスト4PFで動画URL未確定** | プレースホルダ `<VIDEO_URL>` で保存・公開後タスクでURL差し替え注記 |
| Notion保存timeout | 1回だけリトライ、それでもダメなら草川に手動保存url案内 |

## 🎯 関連エージェント・スキル

- `short-video-virality-architect` — セリフ生成（Solo / Polish・35〜45秒・名乗り＋決意型）
- **説明図インフォグラフィック** — HTML/CSS→Chrome→PNG（草川カラー・print-designer流）。ルートA・主役
- `nanobanana-prompt-designer` — 雰囲気イメージのプロンプト生成（ルートB・補助・手動レンダ）
- `sns-content-creator` — 7PF SNS投稿文生成（video-aware モード）
- `content-fact-checker` — 一次情報遡及
- `content-risk-reviewer` — 8軸リスクスキャン
- `sns-content-polisher` — 仕上がり品質が低い時のSNS文磨き直し（オンデマンド）
- `notion-saver` — Notion保存代行
- 長尺動画（>90秒）はこのスキル対象外（専任agentは2026-07-02廃止・必要時は都度依頼）

## 🔧 学習・改善

このスキル運用で発見した改善点は `feedback_short_video_create.md` に追記し、本SKILL.mdに反映。
特に以下の指標を月1で確認:
- nano-banana画像プロンプトのサイズ指定忘れ件数（目標: 0件/月）
- Notion保存先迷子件数（目標: 0件/月）
- 草川の途中差し戻し件数（目標: 月3件以下）
- **SNS投稿文の追加修正発生率（目標: 月10%以下 = 7PFのうち平均0.7PF未満修正）**
- **動画UP後のSNS展開完了までの所要時間（目標: 15分以内）**
- **X 140字制限違反件数（目標: 0件/月）**

## 🆕 2026-05-21 更新メモ

SNS投稿文生成（Step 6 新規）を追加し、7ステップ → 8ステップに拡張。
従来は動画完成後に手動で各SNSの投稿文を考えていた → 平均 30〜60分の作業を構造化排除。
動画ホスト3PF（TikTok/Shorts/Reels）はキャプション、クロスポスト4PF（X/Threads/Facebook/LINE）は動画URL付きティーザーとして自動分岐。

## 🆕 2026-06-02 更新メモ（子ども医療費18歳ショート動画の制作から）

**Step 5 を「nano-banana一択」→「2ルート分岐」に刷新**。今回の最大の学び＝**説明図はAI画像生成ではなくHTML/CSS→PNGで作る**。
- 経緯: nano-banana実写B-rollが「微妙」、純アイコン図は「情報少なすぎて何の画像か分からない」と本人NG。原因＝AI画像は日本語/数字を崩し、写真は雰囲気だけ。
- 解決: print-designerと同じHTML→Chrome→PNG で、**正確な日本語＋数字＋出典入りのニュースフリップ図**を制作。崩れ・ガチャなし、微修正は即再レンダ。
- **草川ブランドカラー必須**（ライム#c7ff4a／グリーン#1f5a3a・#0f3d27／クリーム#f3efe4）。初回アンバー+ネイビーで作って「草川カラー踏襲してない」と差し戻し→ブランド色は毎回厳守。
- **Gemini API画像は無料枠0**（limit:0）。「API無料で全自動」は誤案内だった。無料は手動（AI Studio/Geminiアプリ）、自動は課金。
- **セリフ**: 冒頭名乗り＋「この声が多い」＋結びの決意「必ず実現させます」。**35〜45秒厳守**。
- **公選法**: 告示前の決意表明OK／告示後の再投稿NG注記を保存ページに残す。
- **スマホ編集前提** → 完成PNGを Driveミラー `📱動画素材/` へコピーして phone-accessible に。
- 制作資産: `~/outputs/daily-content/2026-05-27/kodomo-iryouhi-18-musho/infographics/`（HTML＋PNG雛形5枚）。詳細 [[feedback_short_video_infographic_html_to_png]]。

# ショート動画 挿入画像（9:16 1080×1920）制作規範

> 正本。数値（サイズ・文字級数・字幕帯座標・深緑面積上限）は `~/.claude/scripts/specs.json` の `image."9:16"` が持つ。本文と食い違ったら JSON が勝つ。
> 2026-09-05 にメモリ3件（infographic_html_to_png／insert_image_design_spec／subtitle_safe_zone）を吸収して新設。実装agent＝short-video-image-designer、呼び出し元＝short-video-create Step5。

## 同dirの道具
- `_starter_9x16.html` … 3ゾーン固定構造の正本スターター（bodyに中央寄せを書けない土台）。新規挿入画像は必ずこれをコピーして作る
- `check_subtitle_band.py` … 字幕帯に前景画素が閾値(1.5%)超あれば🚨FAIL・exit1。複数枚の帯重心yバラつきも警告。**どの制作ルート（agent経由でも手書きでも）でも制作後に `python3 check_subtitle_band.py *.png` を通す**（2026-07-06 図書館100万人4枚で、agentを経由しない手書きルートで違反再発→機械ゲート化）
- テンプレ3種 … `~/.claude/agents/knowledge/short_video_templates/insert_image_v1/`（template_a_scene＝雰囲気シーン／template_b_infocard＝情報カード／template_c_list＝3項目リスト＋各sample png。2026-06-26確定版）
- 全体の機械判定＝`~/.claude/scripts/check_image_design.py`・保存前＝`gate.py`

## 1. 作り方＝HTML/CSS→Chrome→PNG（AI画像生成は使わない）
説明図（内容理解を促すインフォグラフィック）は nano-banana 等のAI画像生成を使わず、HTML/CSS→Chrome headless→PNG で作る（print-designer と同じ）。
- **Why（2026-06-02 子ども医療費18歳動画で確定）**: AI画像は日本語・数字を崩す／写真は雰囲気だけで情報量ゼロ。実写B-rollは「微妙」、純アイコン図は「何の画像か分からない」と本人NG。HTML→PNGなら正確な日本語＋数字＋出典が入り、微修正は即再レンダ
- Gemini API の画像生成は**無料枠0**（「API無料で全自動」は誤案内。無料は AI Studio/Geminiアプリの手動）
- 雰囲気B-roll・抽象イメージは 📷写真ストック/10_使える写真 → 無ければフラットイラスト情景（HTML/CSS）。nano-banana等のAI画像生成ルートは 2026-09-05 廃止（設計書D5）
- レンダ: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=1080,1920 --default-background-color=FFFFFFFF --screenshot=out.png "file://<html>"`。出力後は必ず自分でReadして字割れ・はみ出しを直す。HTMLソースも残す
- スマホ編集前提 → 完成PNGを Drive `📱動画素材/<日付>_<テーマ>/` にコピー（スマホDrive→カメラロール→CapCut）

## 2. 3ゾーン固定レイアウト＋字幕セーフ帯（絶対必須）
動画編集で**中央やや下に白字テロップを焼き込む**前提。**1セット内の全画像で帯の位置を固定座標で完全一致**させる。
- 上ゾーン（帯より上）: kickerピル＋見出し＋メイン図
- **字幕帯（`band_from`〜`band_end`・specs.json）: 読ませ文字・主要素・建物輪郭・カード縁を置かず、穏やかな一様背景のみ**
- 下ゾーン（帯より下）: 区切り線＋結び・出典
- 実装は `position:absolute` の絶対座標固定（`.top height:<band_from>px` ＋ `.bottom top:<band_end>px`）。**`justify-content:center` 等の中央寄せ禁止**（画像ごとに帯位置がズレる元凶＝2026-07-02 京都直通で草川「位置は動かせないので徹底を」）
- 帯幅は約220pxの狭めでよい（旧 y1080〜1500 の420pxは広すぎ）。**帯を「大穴の言い訳」にしない**＝上下ゾーンは意図的に詰め、中途半端な空白を残さない
- 完成後は半透明赤帯オーバーレイのコンタクトシートと `check_subtitle_band.py` で一致確認
- ※座標の履歴: 2026-07-02 京都直通で y1240〜1460 確定（旧 y1150〜1470 は互換）。2026-09-05 夜に草川決定で **specs.json band_from を 1240 に修正**し、check_subtitle_band.py・本README・agent📌節と整合済み（正＝y1240〜1460）

## 3. 確定デザイン仕様（2026-06-26 6往復で確定。最初から全部渡せば往復ゼロ）
1. **配色は明るく・あたたかく（最重要）**: 背景の主役はクリーム/オフホワイト `#f3efe4`〜淡ライトグリーン〜水色の空。深緑 `#0f3d27` `#1f5a3a` は文字・見出し・アクセント・アイコンに限定し暗いベタ面を作らない（面積上限＝specs `darkgreen_max`）。ライム `#c7ff4a` はハイライト（キーワード下線＝`box-shadow:inset 0 -0.26em 0 #c7ff4a`）。子ども・遊び場テーマは特に明るく。暗緑支配は却下された。初回にアンバー＋ネイビーで作って差し戻されたことがある＝ブランド色は毎回厳守（色の正本＝`design_system/templates/leaflet_trifold/README.md`）
2. **スタイル**: ニュースフリップ調＝kickerピル(深緑地＋ライム点)→見出し[キーワードにライム下線]→中央ビジュアル(人型比率／マス目グリッド／アイコンカード／年齢チャート)→出典付きキャプション
3. **行間はハッキリ広く**（数px調整は「分からない」と却下）: 見出し `lh_head_min`／本文 `lh_body_min`（specs）／カード内 見出し↔サブ行 margin 28px+／カード間 30px+
4. **文字は主役級に大きく**: 見出し `h1_want`／主要情報 `big_min`／補助 `support_min`／注記 `note_min`（specs）／番号バッジ特大
5. **孤立文字（折り返しで1文字ぶら下げ）ゼロ**: nowrap＋意味維持の字数調整（「匿名でOK・数分でこたえられる」→「匿名OK・数分で答えられる」）。はみ出しは幅を広げず文言を短くする（左右マージン40〜60pxを削らない）
6. **人物は親しみ絵本調**: 暗いシルエット＝怖いのでNG。明るい肌色＋簡単な笑顔＋髪＋カラフルな服。**女の子も入れる**。実在特定個人の顔は描かない
7. **可読性**: 明るい背景に濃い文字。ライム文字は明るい背景に溶けるので濃色縁取り or 濃色面に乗せる
8. **安っぽさ回避7信号**: ①ベタ塗り→多ストップ繊細グラデ ②質感ゼロ→全画面に微細グレイン(feTurbulence) ③2トーン陰影→3〜4トーン＋接地の暗がり＋一貫光源 ④平面→空気遠近＋多層 ⑤記号的人物（最大の弱点）→有機ベジェ・布のしわ・二次ディテール ⑥無加工の縁→内側シャドウ・ビネット・エッジ微光 ⑦素な構図→意図的非対称・焦点階層。情景型（人物なし）が最も「画」になり、フラット図形の人物カットが最も安く見える
9. 継承ルール: 記号化／文字消失を潰す・EYES-FIRST採点（short-video-image-designer）／AI-SaaS美学回避（foundations/rules.md §1）／絵文字なし／他議員名なし／帯以外は画面を使い切る

## 4. 運用（往復を減らす）
①生成 → ②コーディネーターが各PNGを**自分で**Read（agentの自己採点を鵜呑みにしない）→ ③**3枚を1枚にまとめたコンタクトシートで草川が一度に確認**（1枚ずつ往復しない）。agentのコンテキストは期限切れで再開不可になりがち＝本規範を毎回指示文に入れる（live transcript依存にしない）。

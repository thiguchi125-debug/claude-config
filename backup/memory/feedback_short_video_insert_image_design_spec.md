---
name: feedback-short-video-insert-image-design-spec
description: 草川ショート動画の挿入画像（HTML/CSS→PNG）の確定デザイン仕様。これを最初から適用すれば往復ゼロで合格水準が出る
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 262b3114-2186-4cbf-b168-0bdcbce17614
---

草川のショート動画挿入画像（9:16・1080×1920・short-video-image-designerがHTML/CSS→Chrome PNG化）で、2026-06-26に6回の往復を経て確定した好み。**新規エージェント/スキルは不要**＝既存の short-video-image-designer と short-video-create で足りる。足りなかったのは「最初から渡す確定仕様」。次回以降、画像生成の指示文に本仕様を必ず含める／エージェントに先に読ませる。

**Why:** 好みが後出しで1つずつ出て（暗い→明るく、行間狭い、文字小さい、字幕帯バラバラ、子どもが怖い、孤立文字、「この」不要…）毎回作り直しになった。エージェントの自己採点（7信号クリア）が草川の感覚とズレ、コーディネーターの目視確認も甘く後追い化。仕様を固定すれば1発で出る。

**How to apply（挿入画像の確定仕様・指示文に丸ごと入れる）:**

1. **配色は明るく・あたたかく（最重要）**: 背景の主役は明るいクリーム/オフホワイト(#f3efe4)〜淡ライトグリーン〜水色の空。深緑(#0f3d27/#1f5a3a)は文字・見出し・アクセント・アイコンに限定し暗いベタ面を作らない。ライム(#c7ff4a)はハイライト。子ども/遊び場テーマは特に明るく前向きに。暗緑支配＝NG（印象が悪いと却下された）。
2. **字幕セーフ帯 y=1150〜1470px（中央少し下・約60〜77%）を全画像で固定統一**。帯内は読ませ文字・主要素・建物輪郭・カード縁を置かず穏やかな一様背景のみ。上要素はy1120まで／下要素はy1500から（30pxクリアランス）。完成後、半透明赤帯オーバーレイのコンタクトシートでピクセル一致を必ず確認。
3. **行間はハッキリ広く**（数px調整は「分からない」と却下）: 見出しline-height≈1.4／本文≈1.5/カード内 見出し↔サブ行のmargin 28px+／カード間ギャップ 30px+。詰まり感ゼロを目視で。
4. **文字は主役級に大きく**: 見出し120〜150px／主要情報80〜100px／補助56〜68px／番号バッジ特大。スマホでパッと読める。
5. **孤立文字（折り返しで1文字ぶら下げ）ゼロ**: nowrap＋意味維持の字数調整で解消（例「匿名でOK・数分でこたえられる」→「匿名OK・数分で答えられる」）。
6. **人物は親しみ絵本調**: 暗いシルエット＝怖いのでNG。明るい肌色＋簡単な笑顔＋髪＋カラフルな服。性別が分かる造形で**女の子も入れる**（ツインテール＋ピンクのワンピース等）。実在特定個人の顔は描かない（絵本調の非実在簡略顔はOK）。
7. **可読性**: 明るい背景には濃い文字（深緑）で高コントラスト。ライム文字は明るい背景に溶けるので濃色縁取り or 濃色面に乗せる。白飛び・低コントラスト禁止。
8. 既存ルール継承: 安っぽさ7信号クリア（明るくしてものっぺりにしない＝微グラデ/グレイン/陰影維持）[[feedback-short-video-subtitle-safe-zone]]、HTML/CSS→Chrome PNG・ブランド色 [[feedback-short-video-infographic-html-to-png]]、記号化/文字消失を潰す・EYES-FIRST採点 [[feedback-short-video-image-designer-agent]]、AI-SaaS美学回避 [[feedback-flyer-avoid-ai-saas-aesthetic]]、絵文字なし [[feedback-no-emoji-ai-smell]]、他議員名なし、端の見切れなし（左右マージン40-60px）、帯以外は画面を使い切る（中途半端な余白なし）。

**運用（往復を減らす）:** ①生成→②コーディネーターが各PNGを自分でRead（自己採点を鵜呑みにしない・指摘箇所を狙って目視）→③**3枚を1枚にまとめたコンタクトシートで草川が一度に確認**（1枚ずつ往復しない）。エージェントのコンテキストは期限切れで再開不可になりがち＝本仕様を毎回指示文に入れる前提で（live transcript依存にしない）。

**再利用テンプレート（今日の確定版・ここから始める）:** `~/.claude/agents/knowledge/short_video_templates/insert_image_v1/`（template_a_scene.html＝雰囲気シーン／template_b_infocard.html＝情報カード／template_c_list.html＝3項目リスト＋各sample png）。

**関連:** [[feedback-short-video-image-designer-agent]] [[feedback-short-video-subtitle-safe-zone]] [[feedback-short-video-infographic-html-to-png]] [[feedback-short-video-use-virality-architect-first]]

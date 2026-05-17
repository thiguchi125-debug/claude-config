---
name: short-video-create-system
description: "ショート動画セリフ→nano-banana画像プロンプト→Notion保存を1パス化するシステム。skill `short-video-create` + agent `nanobanana-prompt-designer` の2層構成（2026-05-18新設）"
metadata: 
  node_type: memory
  type: project
  originSessionId: dab5673d-7765-4cd4-8c88-47fdba3fcfa9
---

# short-video-create システム（2026-05-18 新設）

## 構成

| 層 | 名称 | 役割 |
|---|---|---|
| Skill | `short-video-create` | オーケストレーター。セリフ生成→fact-check→risk-review→画像プロンプト→Notion保存を1パス制御 |
| Agent | `nanobanana-prompt-designer` | nano-banana画像プロンプト専門。サイズ指定強制注入・公選法ガード・スタイル統一を内蔵 |

## Why（新設の動機）
2026-05-17に「保育園キャッシュレス」ショート動画で画像プロンプトを作成した際、
**サイズ指定（9:16/1080x1920）を忘れて出力**してしまい、過去（2026-05-06）のテンプレを掘り起こして再出力する事故が発生。

過去履歴を検索した結果、nano-bananaプロンプト生成は今回が2回目で、毎回同じ「サイズ指定忘れ」が起きていた。今後もショート動画制作は継続的に発生するため、構造的に再発防止する必要があった。

## How to apply

### トリガー（草川が言うべき言葉）
- 「ショート動画作って」「ショート動画一式」「ショート動画フルパッケージ」
- 「動画作って画像も」「セリフから画像までセットで」
- 「TikTokセット」「Reels一式」

### 明示トリガーなしでも気を回す場面
- 「〇〇でショート動画」と言われた時 → 「画像プロンプトもセットでいく？」と1問だけ確認
- 「ショート動画磨いて」と言われた時 → 同上

### 関連DB
- 📣SNS投稿管理DB: `78f40f33-ae71-4f32-9cc3-b00c0a36707c` (data_source: `1bd98deb-624f-402c-aeb3-bdaa4782b389`)
- タイトル先頭🎬、ステータス進行中、プラットフォーム multi_select で動画PFをチェック

### nano-banana 標準アスペクト比
- ショート動画インサート: **9:16 vertical (1080x1920)** ← 既定
- Instagram正方形: 1:1 (1080x1080)
- YouTube長尺サムネ: 16:9 (1920x1080)

サイズ指定は**プロンプト第1文に必ず注入**。Agent側で自己チェックで弾く設計。

### 公選法・プライバシー強制ガード
プロンプト末尾に強制注入:
- `No people's faces, no real logos, no real brand names, no identifiable persons, no text overlays.`
- 通貨扱う場合: `CRITICAL: Use only real Japan currency denominations (1, 5, 10, 50, 100, 500 yen).`

### 用途別テンプレ6種（agent内蔵）
- A. 集金袋・現金・小銭（暖色・ノスタルジック）
- B. 朝の生活シーン手元（暖色・生活感）
- C. スマホ・デジタル解決（寒色・モダン）
- D. 防災・備蓄・避難所（やや寒色・緊迫感）
- E. 子育て・保育・公園（暖色・希望、イラスト調）
- F. 交通・コミバス・移動（地域感・夕方）

## 学習指標（月1確認）
- nano-banana画像プロンプトのサイズ指定忘れ件数（目標: 0件/月）
- Notion保存先迷子件数（目標: 0件/月）
- 草川の途中差し戻し件数（目標: 月3件以下）

改善点は `feedback_short_video_create.md` に追記して本projectメモに反映。

## 関連
- [[feedback_video_script_save_destination]] — 📣SNS投稿管理DB統一保存ルール
- [[feedback_kusagawa_short_video_script_style]] — 草川ショート動画原稿スタイルガイド
- [[project_short_video_virality_architect]] — short-video-virality-architect本体の設計メモ

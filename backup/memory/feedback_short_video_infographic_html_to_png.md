---
name: feedback_short_video_infographic_html_to_png
description: ショート動画の説明図はAI画像生成でなくHTML/CSS→PNGで草川カラー制作
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b0bba8ff-ab56-4683-9d90-c90ab7651703
---

ショート動画・SNSの**「内容理解を促進する説明図（インフォグラフィック）」は、nano-banana等のAI画像生成を使わず、HTML/CSS→Chrome→PNG で制作する**（print-designerと同じ作り方）。

**Why（2026-06-02 子ども医療費18歳動画で確定）**:
- AI画像生成は①日本語・数字を崩す ②写真は雰囲気だけで情報量ゼロ。実写B-rollは「微妙」、純アイコン図は「情報少なすぎて何の画像か分からない」と本人NG。
- HTML→PNGなら**正確な日本語＋数字＋出典**が入り、崩れず、微修正は即再レンダリング（ガチャ不要）。
- Gemini API の画像生成は**無料枠0（limit:0）**。「API無料で全自動」は誤案内。無料は手動（AI Studio/Geminiアプリ）、自動レンダは課金。

**How to apply**:
- **草川ブランドカラー必須**: ライム`#c7ff4a`（キーワードのハイライト下線=`box-shadow:inset 0 -0.26em 0 #c7ff4a`）／ディープグリーン`#1f5a3a`・`#0f3d27`／クリーム`#f3efe4`。初回にアンバー+ネイビーで作って差し戻された。ブランド色は毎回厳守（[[feedback_leaflet_design_principles]]）。
- **スタイル**: ニュースフリップ調＝kickerピル(深緑地+ライム点)→見出し[キーワードにライム下線]→中央ビジュアル(人型比率/マス目グリッド/アイコンカード/年齢チャート)→出典付きキャプション。
- **サイズ1080×1920(9:16)**。レンダ: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=1080,1920 --default-background-color=FFFFFFFF --screenshot=out.png "file://<html>"`。出力後 Read で目視→字割れ/はみ出し修正。HTMLソースも残す。
- **雛形5枚**: `~/.claude/projects/-Users-kusakawatakuya/outputs/daily-content/2026-05-27/kodomo-iryouhi-18-musho/infographics/`（人型9+1比率／年齢の崖／3場面アイコンカード／29マスグリッド／強調ピン）。流用が最速。
- **雰囲気B-roll/抽象イメージ**だけ nano-banana（手動・文字焼かない・後乗せ）。
- **スマホ編集前提** → 完成PNGを Driveミラー `📱動画素材/<日付>_<テーマ>/` にコピー（スマホDrive→カメラロール→CapCut）。
- スキル本体反映済: `~/.claude/skills/short-video-create/SKILL.md` Step 5（2ルート分岐）。関連 [[feedback_short_video_use_virality_architect_first]]。

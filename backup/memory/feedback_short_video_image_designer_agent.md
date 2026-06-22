---
name: feedback_short_video_image_designer_agent
description: ショート動画挿入画像の専任エージェント新設＋2つの失敗モード（記号化・文字消失）を潰す可読性フロア規範
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c3eb1f4c-e3fb-4b8e-8d8f-a78daa9056d6
---

ショート動画の挿入画像（9:16・1080×1920）制作で、草川の画像が「単調→記号化→文字消失」と振り子で失敗し続けたため、専任エージェント **short-video-image-designer**（`~/.claude/agents/`・model opus・memory project）を新設（2026-06-19 草川提案）。

**Why:** ゼロから毎回手探りするから品質が安定しない。短尺動画画像の規範をコード化する必要があった。

**潰すべき2つの失敗モード:**
1. **記号化** — 人/物を素のSVG図形（rect+circle+line）で組み、標識ピクトグラム/クリップアートになる。「なんで記号みたいな絵？」
2. **文字消失** — 重要文字を縮小表示されるSVG内に小さく置く／ライム×淡色など低コントラストで置く→スマホで消える。「文字が全く見えない」

**How to apply（恒久規範）:**
- **可読性フロア＝強制ゲート（最優先・ZEROなら即不合格）**: 主役文字72px+（推奨88〜120）/支え文字44px+/最小26px（注釈のみ）。**読ませる文字を縮小SVG内に置かない**＝重要語は必ずHTMLレイヤーの特大テキストで絵の外/上に。コントラストは「クリーム白×濃緑／濃緑×ライム」等の必読ペアのみ（ライム×淡色・同色×同色は禁＝消える）。1画面1メッセージ。安全ゾーン（下250/右120/上100pxはSNS UI被り域、主役を置かない）。
- **作画規範（記号化禁止・方針=イラスト品質追求型を草川選択）**: 人物はベジェ有機シルエット＋2〜3トーン陰影＋接地影＋髪の塊＋動き＋小物（ボール=運動部/楽器・音符=文化部/笛・クリップボード=指導者）。建物は屋根2トーン・桟窓・看板・落ち影。情景はグラデ空＋地面・光源・奥行き3層・質感・遠近。絵は脇役、重要文字を絵に背負わせない。
- **2ルート**: 説明図=HTML/CSS（特大文字＋作画）主力／雰囲気=リッチなフラットイラスト情景、写実明言時のみnano-banana手動。
- **EYES-FIRSTループ**: HTML/CSS→Chrome headless（`--force-device-scale-factor=1 --window-size=1080,1920`）→**書き出しPNGを自分でRead**（サブエージェントに見せない）→6軸ルーブリック採点→修正。
- 絵文字禁止[[feedback_no_emoji_ai_smell]]／他議員名禁止[[feedback_no_other_council_members_names]]／顔出さない（公選法・個人情報）／事実テキストはcontent-fact-checker→content-risk-reviewer。説明図はHTML/CSS→PNG[[feedback_short_video_infographic_html_to_png]]。
- **新規エージェントは要CC再起動**でサブエージェント登録[[feedback_agent_registry_partial_load]]。登録までは general-purpose に本.mdを読ませて成り代わらせる。

実適用：2026-06-16 部活動地域展開動画の挿入画5枚（a1〜b2）。a1で重要文字を縮小SVG内に置き「文字が見えない」事故→重要ラベルを特大HTMLに追い出して解消。完成PNGは `outputs/short-video/<日付>_<テーマ>/infographics/`、原本は`_v1_backup/`。

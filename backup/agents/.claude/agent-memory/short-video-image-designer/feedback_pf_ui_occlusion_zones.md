---
name: pf-ui-occlusion-zones
description: 挿入画は字幕セーフ帯だけでなくPF UI遮蔽4ゾーンも避ける。実質使えるのは y236-1236・左65px・y900以降はwidth820。検証は check_subtitle_band.py と feed_preview.py の2本必須
metadata:
  type: feedback
---

ショート動画の挿入画（9:16 / 1080×1920）は、字幕セーフ帯 y1240-1460 を空けるだけでは不十分。
TikTok / IG Reels / YouTubeショートの再生画面でアプリUIが物理的に上に乗る4ゾーンも避ける。

| ゾーン | 座標(1080×1920) | 覆うもの |
|---|---|---|
| 上部 | y0-221 | ステータスバー・おすすめ／フォロー中ナビ |
| 右アクション列 | x900-1080 × y900-1700 | いいね・コメント・シェア・音源 |
| 下部キャプション | y1520-1840 × x0-940 | ユーザー名・キャプション2行 |
| 最下部 | y1840-1920 | プログレスバー・タブバー |

**使える縦は実質 y221-1240 だけ**（y1460-1520 は60pxしかなく出典等は置けない）。
→ 実装の型：`.stack{position:absolute;left:65px;top:236px;width:950px;height:1000px;
display:flex;flex-direction:column;justify-content:space-between;}` に全要素を入れる。
**y900 以降に掛かる要素は width:820px**（左65+820＝右端885 < 900）。
**出典・注釈は下に置けない。必ず .stack の末尾＝ y1236 で終わらせる。**
（`position:absolute` の絶対座標固定という既存ルールは維持。`.stack` 内の space-between は
先頭を y236・末尾を y1236 に必ず着地させるので、中央寄せ禁止ルールには抵触しない。）

**Why:** 2026-08-31、育休退園セット a1-a4 が check_subtitle_band.py を全部PASSしていたのに、
上部に緑ピルラベル・下部キャプション帯に出典表記が入っていた。**議員の発信で出典が隠れるのは致命的**。
右アクション列には a1 のカードが張り出していた。帯ゲートだけでは全く捕まえられない別種の不具合。

**How to apply:** 挿入画を作る／直すときは検証を必ず2本とも通し、両方PASSで初めて出荷。
```
python3 ~/.claude/agents/knowledge/design_system/short_video_templates/check_subtitle_band.py *.png
python3 ~/.claude/scripts/feed_preview.py short <各PNG>
```
feed_preview.py のコンタクトシートは自分でReadして目視も行う（赤=遮蔽あり／緑=クリア）。
テンプレは `outputs/short-video/2026-08-25_ikukyu-taien/infographics/_base.css` に反映済み。
なお `check_subtitle_band.py *.png` はコンタクトシート等の非9:16 PNGもサイズ不一致でFAILさせるので、
レビュー用画像は `_review/` サブフォルダに逃がす。
関連: [[dense-cut-tradeoffs]]

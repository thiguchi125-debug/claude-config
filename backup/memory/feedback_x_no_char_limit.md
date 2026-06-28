---
name: feedback_x_no_char_limit
description: X(旧Twitter)は字数制限撤廃。X投稿は140字厳守をやめ長文可、内容を充実させる
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ec62ed91-56d9-45b7-bd08-038b09c591b3
---

X（旧Twitter）の字数制限が撤廃されたので、X投稿は従来の「140字厳守」をやめ、**長文も可**。今後のSNS生成ではXも長文前提で、要点を削りすぎず内容を充実させる（ただし冒頭フックは強く・1ツイートで読み切れる構成は維持）。

**Why:** 草川指示（2026-06-28）。Xの仕様変更で短文制約が不要に。
**How to apply:** sns-content-creator / ai-interview-sns-poster / daily-content-generator / short-video-create 等を呼ぶときは「X=長文OK（140字制限なし）。言い切り・拡散性は保ちつつ、背景や具体も入れて読み応えを持たせる」と明示。エージェント定義側の「X＝140字厳守」記述は本ルールで上書きする。Xスレッド型と単発長文型を使い分け可。

関連: [[feedback_sns_citizen_lifescene_first]] [[feedback_no_emoji_ai_smell]]

---
name: feedback_notion_saver_kanji_garble_verify
description: notion-saver保存後はfetchで漢字化け実体確認が必須（「表示上の問題」の自己弁明を信じない）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9da3df6b-cca2-45be-b232-b2173e572830
---

notion-saver エージェント（や長文Notion保存）は、本文の特定漢字を**実体として**化けさせることがある。2026-06-24「温泉で産後ケア」SNS保存で実例：お風呂→「お風坂」、寝不足→「眠不足」、から→「か㆔」、見出し「約380字」→「組84字」。X節は無事だがThreads/IG/FB節が破損。

**Why:** 草川はNotion本文をコピペしてSNS投稿する運用。化けたまま投稿すると公開事故。さらに notion-saver は化けを自己fetchで見たのに「Notion MCP変換の表示上の問題・元の入力は正確」と**誤って弁明**した（実体は破損）。この弁明を信じると素通りする。

**How to apply:** notion-saver / 長文保存の直後は必ず `notion-fetch` で本文を実体確認し、漢字化け（特に呂/坂・寝/眠・から/か＋異体字、数字混じり見出し）を目視チェック。化けていたら `notion-update-page` の `replace_content` で**正しいテキストを丸ごと上書き**（複数箇所のupdate_contentはサイレント失敗しやすい[[feedback_notion_update_content_pitfalls]]ので全置換が安全）。「表示上の問題」というサブエージェントの自己判断は鵜呑みにしない。[[feedback_kameyama_kanji_typo_guard]]の漢字取り違え系と同根。

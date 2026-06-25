---
name: feedback_copypaste_draft_delivery
description: コピペ前提の原稿（LINE案内・メール文・SNS文など）は納品形式を先に伺ってから出す
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 45937869-d531-4ecd-b428-d234bc1135c3
---

LINE案内文など「そのままコピペして使う」原稿を出すとき、チャット内のコードブロック表示は環境によって**各行左に余白（インデント）が入り**、草川が貼るとズレる。「余白が入らない」と口頭で言い切るのは事実と異なる（実際は入る）＝信頼を損なう。

**Why:** コピペ品質が成果物そのもの。余白混入は実害。さらに「入りません」と断言したのに入る、は最も避けるべき不正確報告。

**How to apply:**
- コピペ前提の原稿は、出す前に納品形式を伺う（①txtに書き出してTextEditで開く `open -e`／②プレーン貼り／③ファイル添付 等）。デフォルトは **txt書き出し→`open -e`**（TextEditで全選択コピーすれば余白ゼロ）。
- 行頭マーカー（・）や全角インデント（　）も「左余白」とみなされ得るので、指定なき限り全行フラット。
- 「余白は入りません」等の断定をする前に、自分の出力形式で実際にどう見えるか踏まえる。曖昧なら断定しない。
- 関連: [[feedback_citizen_reply_progress_report_style]]（txt→open -e の納品作法）

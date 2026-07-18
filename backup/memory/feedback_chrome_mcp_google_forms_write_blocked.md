---
name: feedback_chrome_mcp_google_forms_write_blocked
description: Chrome MCPでGoogleフォーム/ドキュメント編集がchrome-extension競合でブロックされる時の対処（読み取りは生きている）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7009245e-9f12-41ed-98e9-2323302f9e2d
  modified: 2026-07-18T03:13:41.995Z
---

Chrome MCPで docs.google.com（Googleフォーム編集画面等）に対して **screenshot / click / type が全て `Error: Cannot access a chrome-extension:// URL of different extension` で失敗**する事象がある（2026-07-18 後援会入会フォームに年齢項目追加時に発生）。

**Why**: 別のChrome拡張が docs.google.com 上で content script / iframe を注入しており、Claude用拡張の書き込み操作と競合する。**空タブでは通るのに docs.google.com を開いた瞬間に復活**するのが特徴＝犯人はGoogleドキュメント/フォーム上で動く拡張（Grammarly・AIライティング・翻訳オーバーレイ・スクショ系等）。全拡張オフ＋全タブ閉じのクリーン再試行でも直らないことがある（環境側制約と割り切る）。

**How to apply**:
- `navigate` と `read_page` / `find` は生きているので、**書き込みは草川に手動でやってもらい→read_page/findで検証**が最速確定ルート。無理に自動書き込みをリトライしない（数回で見切る）。
- 検証は read_page(filter=all) の出力をファイル保存→python/grepで該当質問ブロックを抜き、タイトル・説明文・形式（"短文回答"=記述式）・配置順を確認できる。ただし **checkbox「必須」のON/OFFはAXツリーに出ない**→草川に「赤い * が無ければ必須オフ」と目視1点確認を依頼。
- 自動でやりたい場合の切り分けは「Claude拡張以外を全部オフ→フォームのタブ全閉じ→新規タブで再試行」。それでも駄目なら手動に切替。
- 関連: [[feedback_image_capture_sandbox_limits]]（Chrome MCPのローカル保存制約）

---
name: feedback-image-capture-sandbox-limits
description: Chrome MCPで参照画像をローカル保存する際の環境制約と回避策（design_references/へのファイル保存が難しい理由と現実的な代替）
metadata:
  type: feedback
---

参照画像を design_references/ に「画像ファイルとして」保存するのは、この環境では複数の壁で難しい。無駄打ちを避けるため以下を前提に動く。

**Why（実測した壁・2026-07-10 水鉄砲バトル参照収集で確認）:**
- WebFetch は Pinterest/Behance のギャラリーで本文truncate or 404。直接の画像URLを取れない。
- Chrome MCP `computer` の `save_to_disk:true` はハーネス側に画像を渡す（自分は目視できる）が、Bashからアクセスできるパスにファイルを書かない（find で全域検索しても出ない・MCPログにもパス無し）。
- Google画像の `<img>` サムネイルは gstatic 配信で **CORSタント** → canvas `toDataURL` は SecurityError で使えない。
- `javascript_tool` の出力は安全フィルタが強く、**クエリ文字列を含むURL**も**base64**も `[BLOCKED]` で返る。→ 画像URL文字列やバイト列をJS経由でBashに渡せない。

**How to apply:**
- 画像バイトをローカルに落とすことに固執しない。`computer`のzoom+screenshotで**自分が目視・目利き**して pro判定するのは有効（これは機能する）。
- 成果物は「①テキスト抽出仕様（親が読む主成果）＋②design_references/REFERENCES.md ドッシエ（8軸分析＋再取得元＋転用ポイントを文章で）」で残す。画像ファイル添付は best-effort とし、取れなくても仕様書で print-designer は動ける。
- curlはブラウザCORSの影響を受けないので、**明確な直リンク画像URL（例: 制作者ポートフォリオの静的画像）が判明した場合のみ** Bash curl で落とす価値がある。gstatic/Instagram/Behance は基本落ちない。
- 収集はGoogle画像(`udm=2`)のzoom目視が最も安定。ただしFreepik/イラストAC/Canva等のテンプレ・ストックはプロゲート不合格として除外する。
</content>

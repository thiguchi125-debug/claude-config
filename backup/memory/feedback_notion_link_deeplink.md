---
name: Notion内部リンクの真の落とし穴は表示テキスト
description: Notion API はhrefを自動で app.notion.com/p/ に正規化するので href側は気にしなくて良いが、マークダウンの表示テキスト [ここ](href) に古いURL文字列が露出していると、スマホタップ時にアプリ直起動が阻害される
type: feedback
originSessionId: f734c400-d1a8-4b64-9f3b-5072331e4422
---
Notionページ本文にNotion内部リンクを書くとき、**注意するのは href ではなくマークダウンの「表示テキスト」側**。

**正しい形式**:
```markdown
[ページタイトル](https://app.notion.com/p/<id>)
[わかりやすい説明文](https://app.notion.com/p/<id>)
```

**やってはいけない形式**（スマホでアプリ起動が阻害される）:
```markdown
[https://www.notion.so/xxx](https://app.notion.com/p/<id>)  ← 表示テキストに古いURL露出
[https://www.notion.so/xxx](https://www.notion.so/xxx)  ← 両方古い
```

**Why:**
2026-05-01に2回検証。1回目（直近1週間6ページ）は href 置換を実施したが「まだ飛ばないリンクある」との指摘。2回目（直近3週間9ページ）で実証実験：
- `notion://www.notion.so/...` → 保存時 `https://app.notion.com/p/...` に強制正規化
- `<page url="...">` ブロックタグ → エスケープされて壊れる
- `https://www.notion.so/...` → 保存時 `https://app.notion.com/p/...` に強制正規化
→ **API側はhrefを必ず最新形式に正規化するので href 心配不要**

しかし朝のダッシュボードで約30本、ナビゲーションマップで15本、合計45本が「表示テキストに `https://www.notion.so/xxx` という古いURL文字列を露出させたまま」になっていた。スマホで `[https://www.notion.so/xyz](https://app.notion.com/p/xyz)` をタップすると、表示テキストの方が誘導要因になりブラウザ経由になる挙動だった可能性が高い。表示テキストをページタイトル等の通常文字列に直したら解消。

**How to apply:**
- Notion本文に内部リンクを書くとき、**表示テキストには絶対にURL文字列を入れない**。ページタイトル、説明文、絵文字付きラベル等の通常テキストにする
  - ✗ `[https://www.notion.so/xxx](https://app.notion.com/p/xxx)` 
  - ✓ `[📔 デイリーサマリ](https://app.notion.com/p/xxx)`
- href側は何形式で書いても保存時に `https://app.notion.com/p/<id>` に正規化されるので、`https://www.notion.so/...` のままでも害はない（ただし統一感のため `app.notion.com/p/` 推奨）
- `notion://` deep-linkスキームは Notion本文に書いても保存時に剥がされるため**本文埋め込みでは無意味**。Notion DB に保存しない外部発信物（メール本文／SNSプロフィール／印刷QRコード等）に限り使うと deep-link として機能する
- `<page url="...">` ブロックタグ形式は MCP API でエスケープされて壊れるので使わない
- 既存ページ修正実績：
  - 2026-05-01（1回目）：直近1週間6ページ14リンクを `app.notion.com/p/` 形式に統一（href側）
  - 2026-05-01（2回目）：直近3週間9ページ約45リンクの**表示テキスト**を通常文字列に修正（朝ダッシュボード約30／ナビゲーションマップ15／その他）
- ohayo/oyasumi/nichijo/iken/policy-update/content-pipeline 等、Notionリンクを生成する全スキル・全エージェントに適用される横断ルール
- 新規ページ生成時は最初から「表示テキスト＝通常文字列」で書くこと

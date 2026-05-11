---
name: 📣SNS投稿管理DB の正しい view URL（v2 2026-05-10確定）
description: SNS下書きDBの正しいview URL／data_source_id／ステータス選択肢を確定。2026-05-10 草川指示で再点検
type: feedback
originSessionId: e5b6ab30-0d95-49e8-bed0-fa67fb1aeaab
---
## 📣SNS投稿管理DB（投稿管理DB / SNS＋ブログ統合）

### 確定情報（2026-05-10 fetch 検証済）
- **データベースID（page）**: `78f40f33-ae71-4f32-9cc3-b00c0a36707c`
- **data_source_id**: `1bd98deb-624f-402c-aeb3-bdaa4782b389`
- **data_source_url**: `collection://1bd98deb-624f-402c-aeb3-bdaa4782b389`
- **page_url**: `https://www.notion.so/78f40f33ae714f329cc3b00c0a36707c`

### ステータス選択肢（2026-05-10 確定）
- `未着手` ← **デフォルト**（ohayo SKILL.md の「未投稿」は誤記）
- `進行中`
- `完了`

### 既存ビュー
1. **Default view**（`view://6ac6eddd-53b7-4e54-8ebe-ec2e02227718`）
   - フィルタなし、登録日 DESC
2. **📱下書き仕上げ待ち**（`view://34acf503-a68f-812c-92a0-000cd78dfa77`）
   - フィルタ：投稿タイトルが📱で始まる
3. **未着手SNS下書き**（2026-05-10 新規作成）
   - フィルタ：ステータス=未着手、登録日 DESC

### ohayo Step 3-3 で使うべき URL
```
view_url: https://www.notion.so/78f40f33ae714f329cc3b00c0a36707c
（Default view を呼べばDB全件・ローカルで「ステータス=未着手」フィルタ）
```

または明示的に：
```
data_source_url: collection://1bd98deb-624f-402c-aeb3-bdaa4782b389
filters: { "未着手" でローカルフィルタ }
```

### 旧誤記（廃棄済み）
- ❌ `https://www.notion.so/78f40f33ae714f329cc3b00c0a36707c?v=357cf503a68f8164a1f9000c6c19fbcd`（404）
- ❌ ohayo SKILL.md「ステータス=未投稿」（正しくは「未着手」）

### ohayo SKILL.md の更新箇所（次回更新時に反映）
- 3-3 セクション view_url を上記に修正
- ステータス選択肢「未投稿」→「未着手」に修正

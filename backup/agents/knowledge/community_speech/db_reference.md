# 地区別関係性メモ DB（Notion）

## DB情報

**ハブページ**：🤝 地域挨拶・スピーチ集
- URL: https://www.notion.so/34ecf503a68f810ba7ffde6e6e18b509
- 親：プロジェクト＆タスク › Projects › ★選挙 › 地域別活動計画

**地区別関係性メモ DB**：（次のセクションで作成 ID を記録）

---

## DB スキーマ（設計）

| プロパティ | 型 | 説明 |
|---|---|---|
| 地区名 | title | 二本松／川合町／下庄町／中庄／阿野田町／井田川 等 |
| 自治会長 | rich_text | 現自治会長氏名（前任者は履歴ノートに） |
| 主要連絡先 | rich_text | 役員・キーパーソンの連絡先 |
| 地区の主要課題 | multi_select | 通学路／公共交通／水道／防災／空き家／高齢化／その他 |
| 過去の約束 | rich_text | 草川が公の場で約束した事項（要検証可能性） |
| 直近の場での発言 | rich_text | 直近自治会での挨拶のキーフレーズ |
| 関係性温度 | select | 強支持／支持／中立／要注意 |
| 関連ページ | url | Notion ハブページ内サブページへのリンク |
| 最終更新 | last_edited_time | 自動 |
| メモ | rich_text | 自由記述（地域の本音課題・歴史的経緯） |

---

## 利用フロー（community-rally-speaker から）

```
1. ユーザーから district が指定される
   ↓
2. mcp__claude_ai_Notion__notion-fetch で DB を検索 or 該当エントリを取得
   ↓
3. エントリがあれば：
   - 「過去の約束」を必ず原稿に反映（言行不一致の予防）
   - 「地区の主要課題」を柱選定の参考に
   - 「関係性温度」でアジ強度を調整
   ↓
4. エントリがなければ：
   - 新規エントリ作成を提案（ユーザー確認後）
   - 今回作成する原稿を初期メモとして反映
```

---

## DB ID（運用情報）

```
DATA_SOURCE_ID: 520fe503-116e-4e15-96d5-ed8f2cd8bd4a
DATABASE_URL: https://www.notion.so/38e8b5fdbb03482b817ad3a3b51c43a0
```

## 既存エントリ

- 二本松（強支持）: https://www.notion.so/34ecf503a68f811c9987d3befd9a3a56

## 検索コマンド例

```
mcp__claude_ai_Notion__notion-search
  query: "<地区名>"
  data_source_url: "collection://520fe503-116e-4e15-96d5-ed8f2cd8bd4a"
```

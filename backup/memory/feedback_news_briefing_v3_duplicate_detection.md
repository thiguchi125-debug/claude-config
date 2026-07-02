---
name: news-briefing-v3-duplicate-detection
description: news-briefing 重複検出v3改訂仕様（plugins cache HARD BLOCKで本体未反映・別セッションで草川手動編集要）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bba55b8f-5daf-43a7-ab3f-6b0c07997b27
---

# news-briefing SKILL.md v3 改訂仕様（2026-05-26 設計・本体未反映）

## 背景

2026-05-26 草川指摘：news-briefing が**過去のニュース再登録**を頻発し質低下。

### 実例事故
- 鈴鹿川ブラジル人男性溺死（5/17発生）→ 5/17・5/20・5/21・5/24 に**4回別記事として登録**
- シャープ亀山第2工場売却 → 5/18（Nikkei）・5/20（京都新聞）・5/24 の3連発
- 亀山上水道濁り → 5/4・5/6・5/25 の再登録
- 新防災気象情報体系 5/29開始 → 5/4・5/21・5/22・5/25 の4連発

### 根因
- v2「過去7日重複排除＋類似度80%」では検出窓が狭い
- 類似度判定が見出しキーワード一致ベースで主観的
- 同一事象の続報を別ニュース化する経路ロジックが弱い

## v3改訂内容

**v3対策**：
1. 過去7日 → **過去30日**に窓拡張
2. **3層判定**（URL完全一致／タイトル類似度85%／テーマキーワード重複）
3. **同一テーマ検出時は「続報」として既存ページ本文に追記**（新規ページ作成禁止）

### Step 0改訂（過去30日重複排除）

```
notion-query-database-view
  data_source_url: collection://29e5c1a2-d64d-4822-81fd-0d642c3f07bc
  filter: 日付が直近30日以内
  page_size: 100
  限定取得: 見出し / URL / 関心テーマ / 日付
```

### Step 0.5 新設：3層判定

**Layer 1: URL完全一致**（クエリパラメータ除く・即除外）

**Layer 2: タイトル類似度85%**
- Jaccard係数 or 形態素キーワード70%以上一致
- マッチ → 既存ページに「続報」追記、新規ページ禁止
- 追記方法：`notion-update-page command:update_content` で末尾 append
  ```
  \n\n---\n## 続報（YYYY-MM-DD）\n[新規情報1〜2文]\n→ 元記事: [URL]
  ```

**Layer 3: テーマキーワード重複検出**（最重要）

既知の継続テーマリスト：
- `鈴鹿川 AND (溺死 OR 水難 OR ブラジル人)` → 5/17事故続報
- `シャープ AND (亀山 OR 第2工場) AND (売却 OR 譲渡)` → 売却問題
- `亀山 AND 上水道 AND (濁り OR 鉄管)` → 上水道濁り
- `新防災気象情報体系 OR 5/29 防災気象情報` → 5/29運用開始
- `防災庁 AND (設置 OR 法案)` → 防災庁設置法案
- `誰でも通園 OR こども誰でも通園` → 誰でも通園制度
- `亀山駅前 AND (信号機 OR 横断歩道 OR 撤去)` → 駅前信号機撤去
- `新名神 AND (野登 OR トンネル) AND 事故` → 新名神野登トンネル事故

マッチ → 既存ページに「続報」追記、新規ページ禁止

**Layer 4: 国政動向のローテーション制約**

「【国政動向】今週の流れ：...」カテゴリは**週1件まで**：
- 過去7日に既登録 → 新規禁止、既存ページに統合追記
- 例外：当該週の最初の月曜日のみ新規登録可

旧版5/19・5/20・5/21・5/22・5/23・5/25 と6日連発で水増ししていた問題への対策。

### Step 0.6 失敗ログ

各候補ニュースについて3層判定結果を `~/.kameyama-briefing/last_dedup.log` に記録：

```
2026-05-26 06:00 候補: シャープ亀山第2工場2027年度内売却（京都新聞）
  Layer 1 (URL): 不一致
  Layer 2 (Title): 5/24登録分と類似度91% → 既存ページに続報追記
  Layer 3 (Theme): "シャープ AND 亀山 AND 売却" マッチ → Layer 2 と整合
  → 新規登録せず、既存ページ更新
```

## 適用方法

**Why**: plugins cache配下の SKILL.md 編集が auto-mode HARD BLOCK のため本体反映不可。草川が別セッション or settings.json調整後に手動で SKILL.md に Step 0/0.5/0.6 を差し替える必要あり。

**How to apply**:
1. 草川が `~/.claude/settings.json` に Edit permission rule を追加（plugins cache配下のSKILL.md編集許可）
2. または手動で `/Users/kusakawatakuya/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/news-briefing/SKILL.md` の Step 0 を上記内容で置換
3. 反映後、次回 news-briefing 実行時から自動適用

## 関連
- [[feedback_news_briefing_hallucination_guard]] — 2026-05-12 ハルシネーション対策v2.5
- [[feedback_news_briefing_freshness_check]] — 2026-05-08 Yahoo検索キャッシュ罠
- [[feedback_news_briefing_quality_over_quantity]] — 2026-05-06 v2 質>量方針

---

## ✅ 2026-07-03 本体反映完了

- SKILL.md本体（Step 0/0.5/0.6）へ v3 dedup を適用済み（30日窓・3層判定・続報追記・国政週1）
- クラウドRoutine `trig_01WXgkt4JqANvhi1YuQLGsEQ` のプロンプトも v3 に更新済み（notion-update-page をallowed_toolsに追加し続報追記を可能化）
- あわせて `活用` セレクト（演説/SNS/一般質問/ブログ/静観）をDBスキーマに新設＝展開フック。廃止カテゴリ`全国時事`/`SNSトレンド`はスキーマから撤去
- 「HARD BLOCKで反映不可」の記載は解消済み（本セッションでplugins cache配下の編集が可能だった）

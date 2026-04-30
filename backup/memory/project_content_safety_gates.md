---
name: 発信物安全2エージェント新設
description: 2026-05-01新設。content-fact-checker（一次情報検証）＋content-risk-reviewer（公選法・個人情報・名誉毀損等8軸）。content-pipelineにStep 2.6/2.7/3.6/3.7として組込済み
type: project
originSessionId: 24951467-1863-4b41-b983-d35481e730af
---
# 発信物安全2エージェント新設（2026-05-01）

ブログ・SNS発信物の **誤情報リスク** と **物議リスク** を投稿前に必ず検出する2層ゲート。content-pipelineにブログ後（2.6/2.7）・SNS後（3.6/3.7）両段階で挿入。

**Why:** 議員発信物の誤情報拡散・公選法違反・個人情報漏洩は信頼失墜だけでなく刑事・民事リスク。AI生成ハルシネーションが混入する確率は0でない。誤りなく出すには「数字検証専任」と「リスクスキャン専任」を分離して両方走らせる必要がある。

**How to apply:** content-pipelineは自動でこの順序で動く。手動での個別呼び出しは「ファクトチェック」「リスクチェック」等のトリガーワードで起動。fact-checkerはWebFetchで一次情報まで遡る・research_summaryをそのまま信じない。risk-reviewerはHIGH以上検出時に草川への問いかけを生成・本人判断を仰ぐ（ASK_USER）。

## エージェント1: content-fact-checker

**役割**: 数値・固有名詞・法令・統計の一次情報検証専任

**5カテゴリ検証**:
1. 数値（待機児童数・予算額・補助率・利用件数・比率・日時）
2. 固有名詞（計画名・条例名・地名・施設名・組織名・人名）
3. 法令・制度（法令条文・通知・国制度・条例条文）
4. 議会・行政情報（答弁・議決・委員会・視察先）
5. 他自治体事例

**判定**:
- ✅ VERIFIED: 完全一致
- ⚠️ MINOR_DIFF: 軽微差異
- ❌ INCORRECT: 明確誤り
- ❓ UNVERIFIED: 確認不能
- 🚫 HALLUCINATION: research_summaryにもない混入
- ⏭️ EXEMPT: 検証対象外（個人体験等）

**自動REJECT**: HALLUCINATION 3件以上 / 法令条数誤り 1件以上

## エージェント2: content-risk-reviewer

**役割**: 議員発信物の物議・問題化リスク8軸スキャン

**8軸**:
1. 個人情報（市民相談引用の特定可能性・写真の同意）
2. 機密・非公開情報（議会非公開・人事案件・公表前情報）
3. 公職選挙法（**最重要**：寄附禁止/事前運動/虚偽事項/SNS時代特有）
4. 名誉毀損・侮辱（事実摘示型・公人vs私人）
5. 差別表現（性別・年齢・障害・国籍・宗教）
6. 利益相反（親族企業優遇・特定業種推し）
7. 議員品位（暴言・煽情的表現）
8. 政治的物議（国政党派・歴史認識・賛否分かれるテーマ）

**判定**:
- ✅ APPROVE: 全軸LOW以下
- 🟡 REVISE: MEDIUM 1件以上
- 🔴 ASK_USER: HIGH 1件以上 → **草川に問いかけ・本人判断**
- 🚨 REJECT: CRITICAL 1件以上（公選法違反疑い・明確な個人情報漏洩等）

## content-pipeline統合（2026-05-01改訂）

```
[blog-writer]
  ↓
[content-editor] Step 2.5（5軸品質スコア）
  ↓ pass
[content-fact-checker] Step 2.6（一次情報検証）
  ↓ APPROVE
[content-risk-reviewer] Step 2.7（8軸リスクスキャン）
  ↓ APPROVE
[sns-content-creator] Step 3
  ↓
[content-editor] Step 3.5
  ↓ pass
[content-fact-checker] Step 3.6（SNS固有の主張のみ重点検証）
  ↓ APPROVE
[content-risk-reviewer] Step 3.7（媒体別個別評価）
  ↓ APPROVE
[notion-saver] Step 5（Notion保存）
```

## ASK_USER時の草川向け問いかけ例

```
🔴 個人情報リスク検出:
「井田川地区の3人兄弟のお母様から〜」という表現は地域＋家族構成で個人特定可能。

確認事項:
1. ご相談者本人から発信同意は得ていますか？
2. 同意なしなら「市内の保護者から〜」への匿名化は可能ですか？

判断:
[ A ] 同意済みで継続  [ B ] 匿名化修正  [ C ] 引用削除  [ D ] 投稿見直し
```

## トリガーワード

- **fact-checker**: ファクトチェック / 事実確認 / 数字あってる？ / 一次情報確認 / 出典確認 / 裏取り
- **risk-reviewer**: 発信リスクチェック / これ問題ない？ / 物議醸さない？ / risk-review / 個人情報入ってない？ / 公選法大丈夫？ / セーフ？

## 失敗時の挙動

- 2周してもREVISE → human_review_flagでユーザーに通知
- REJECTは即停止。差し戻し or 削除
- ASK_USERは応答待ち（pipeline blocking）

## 関連ファイル

- `~/.claude/agents/content-fact-checker.md`
- `~/.claude/agents/content-risk-reviewer.md`
- `~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/content-pipeline/SKILL.md`（Step 2.6/2.7/3.6/3.7挿入済）

## トラブル時のチェックポイント

- WebFetch失敗 → 一次情報の代替URL（議会会議録・例規類集の各URL）を試す
- ASK_USERで応答が遅い → タイムアウト不要・草川判断は議員業務として妥当な遅延
- 過検出（MEDIUM多発） → リスクrubricの閾値を見直し、過敏すぎる項目はLOWに調整
- 過小検出（公選法見落とし） → リスク事例DBを充実化

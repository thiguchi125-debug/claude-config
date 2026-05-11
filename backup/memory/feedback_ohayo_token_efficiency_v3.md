---
name: ohayo トークン効率化方針 v3（2026-05-10更新）
description: 本朝120K消費の主因分析と削減策。timeout後の即リトライ禁止／fetch回数1回限定／更新失敗時はチャット出力に集約
type: feedback
originSessionId: e5b6ab30-0d95-49e8-bed0-fa67fb1aeaab
---
## 2026-05-10 本朝消費 約120K の内訳分析

| 工程 | 概算 | 主因 |
|---|---|---|
| 並列データ収集（Calendar/Gmail/Notion search/サマリfetch/dashboard fetch） | 35K | やむを得ず |
| ニュースDB / タスクDB / プロジェクトDB query | 35K | view から全件取得（has_more=true で50件超） |
| ダッシュボード再fetch（古いキャッシュ判明） | 10K | timeout後の verify が裏目 |
| ダッシュボード再試行 update_content（×3回・全失敗 or 反映確認できず） | 25K | old_str マッチ失敗の連鎖 |
| その他（archive grep / SNS DB調査 / 7DB各種） | 15K | |

## 削減策（次回ohayo以降に厳守）

### A. timeout 後の即リトライ禁止（最重要）
- `update_page` timeout = サーバ側で多くの場合は適用済み
- 即fetchすると古いキャッシュが返る → 「未反映」と誤判定 → 再送信 → 再fetch... の連鎖が25K喰う
- **timeout発生したら verify を完全スキップして次のステップへ進む**
- 草川にチャットで「timeout発生・反映状態は次回ohayoで再確認」と1行報告

### B. fetch は1セッション1回限定
- 同じページを2回 fetch すると、2回目はキャッシュの可能性
- ダッシュボード fetch 1回で得た本文を、Step 4 の old_str 抽出と verify 両方に使い回す
- verify が失敗しても再fetchしない（次回ohayoに送る）

### C. ニュース/タスク/プロジェクトDB は「filtered view」を絶対使う
- 現在の `292cf503...?v=292cf503...` view はフィルタなし → 50件以上取得
- ohayoが叩く専用 view を作る：
  - **本日タスク view**: ステータス∉Done/Archive、期限<=今日
  - **本日ニュース view**: 日付=今日（既にあるが filter 日付の自動更新が問題）
  - **進行中プロジェクト view**: ステータス=進行中
- これだけで35K→15Kに削減可能

### D. ダッシュボード本文置換は完全停止（2026-05-06草川合意の徹底）
- 見出しの日付置換だけ実施
- 本文（スケジュール詳細・フォーカス詳細・タスク表）はチャット出力に完全集約
- old_str マッチ失敗のリスクをゼロにする

### E. 1セッション内のリトライ回数 上限2回
- update_content timeout → 待機 → 再fetch して反映確認 → だめなら諦める
- 3回目以降はやらない（連鎖でトークン喰い）

## 目標値
- 標準ohayo: 70〜90K（本朝120K → 30〜40%削減）
- 軽量ohayo（fetch問題なし時）: 60K前後

## ohayo SKILL.md 次回更新で反映する箇所
1. ⚡トークン効率化原則 §A〜§E を上記に置換
2. Step 4 の verify を「**timeout時はskip**」明記
3. notion-create-view 経由でフィルタ付きviewを ohayo 初回起動時に作成（草川承認後）

## 教訓（短く）
- timeout = 失敗 ではない
- 即リトライ = 燃費の敵
- fetch回数の最小化が最大効率化

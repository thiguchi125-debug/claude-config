# 定型ルーティンのleanルール（ohayo / oyasumi / nichijo）

ルーティンはNotion・Calendar・Gmail・Drive・Todoistを横断して何度も外部を叩くため、燃費悪化の主戦場。目標: ohayo標準 70〜90K（コンテンツ提案込みで90〜100K）。

## A. timeout後の即リトライ禁止（最重要・-25K級）

- `update_page` / `update_content` のtimeout＝サーバ側では多くの場合**適用済み**
- 即fetchすると古いキャッシュが返る→「未反映」と誤判定→再送信→再fetch…の連鎖が25K喰う
- **timeoutが出たらverifyを完全スキップして次のステップへ**。草川にチャットで「timeout発生・反映状態は次回に再確認」と1行報告するだけでよい

## B. fetchは1セッション1ページ1回

- 同じページの2回目fetchはキャッシュの可能性が高く、情報価値がない
- 1回のfetchで得た本文を、old_str抽出とverifyの両方に使い回す
- verify失敗しても再fetchしない（次回ルーティンに送る）

## C. DBクエリは必ずfiltered view

- フィルタなしviewは50件超（has_more=true）を引きずり込み、35K→15K圧縮の機会を捨てる
- 本日タスク／本日ニュース／進行中PJ など目的別のfiltered viewを叩く
- タスク・PJは**Notionではなくtd.py**（`td.py morning` / `td.py audit`）——CLAUDE.mdのohayo/oyasumi override準拠。Notion✅タスクDBを叩かない

## D. ダッシュボード本文置換は最小限

- 見出しの日付置換など確実に当たる最小置換のみ。大きな本文はチャット出力に集約
- old_strマッチ失敗の連鎖リスクをゼロに保つ
- 堆積スイープ等の定型置換は「見出し＋本文の全置換」1発で（部分置換の試行錯誤をしない）

## E. リトライ上限2回

- update失敗→待機→反映確認→ダメなら諦めて次回へ。3回目はやらない

## F. 読込サイズの上限

- Drive: pageSize 10 / 1ファイルread 1,500字目安
- Notion検索: pageSize 30目安
- ニュースは5〜7件に厳選（件数より質）

## G. 書込セクションの限定

- ルーティンがNotionに書き込むセクションは必要最小限（ohayo v2.5では3セクション限定の実績）
- 「書かなくても済むものはチャット出力」が原則

## 各ルーティンのSKILL.md・feedbackメモとの関係

各ルーティンの詳細仕様は各SKILL.mdとmemoryのfeedbackファイル（feedback_ohayo_token_efficiency_v3 等）が正。本ファイルは横断原則のみ。矛盾があれば新しい方＝memoryのfeedbackを優先し、本ファイルの更新を提案する。

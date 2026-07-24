# ご意見箱フォーム 夜間自動取込システム（form-intake）設計書

- 日付: 2026-07-25
- 承認: 草川（設計3問承認済み：範囲=登録＋朝通知／方式=夜間launchd／ETL追記=自動）

## 目的

Googleフォーム「ご意見箱」（回答スプレッドシート3枚）に届く市民意見の手動コピペ運用（ikenスキル）の
「投函の一手間」を自動化する。夜間に新着を検出→📝市民意見リストへ自動登録＋ドメイン分類ファイル追記→
翌朝ohayoで「新着◯件＋要約」を表示。返信案生成・タスク化は従来どおり草川の指示があったときだけ（ikenの後半フロー）。

## 対象データ源（3シート・fileId固定）

| # | シート | fileId | 初期state（2026-05-06 ETL時点の行数） |
|---|---|---|---|
| S1 | 【2025アンケート】市政へのご意見（回答） | 1F-zNtaJPyD8XRM_UYcajsSGnuONG9afEX5VfBBsth5k | 40 |
| S2 | 市政へのご意見（アンケートなし）（回答） | 1sJzr4TGsO963wyIsFbSeBM18e5Oy8xhHVbTmRshmDXo | 195 |
| S3 | 市政へのご意見（アンケートあり）（回答） | 1Lqj24se04T-q6VkF3RayAk0ZHy9Ym9OD8541EHjn8ec | 124 |

新着検出は「シートのデータ行数 > state記録の処理済み行数」の差分方式（行は追記のみされる前提）。
行ID `S<n>-<行番号>` を既存ETL資産と同じ形式で使い、重複・追跡の鍵とする。

## 実装時の重要変更（2026-07-25・実装中に発覚）

- **ohayo §9 が2026-05-11から既に毎朝同じ3シートをポーリングしてNotion登録していた**
  （state=`iken_poller_state.json`・タイムスタンプ方式・テスト/スパムフィルタ・列マップ完備・最終処理2026-07-05）。
  本システムは「新設」ではなく **§9の夜間前倒し**として実装：
  - stateは新設せず `iken_poller_state.json` を共用（`last_processed_timestamp`=Notion登録済み／新設`etl_last_row`=ETL追記済み行数の2トラック）
  - ohayo §9は「_form_status.json の結果表示＋死活監視」に書き換え（シート直接ポーリング廃止・二重登録防止）
- **`read_file_content` は古いキャッシュを返す実事故あり → `download_file_content`＋base64デコード必須**（stateのnoteに記録されていた知見をSKILLの恒久ガードに昇格）。

## コンポーネント

1. `~/.claude/skills/form-intake/SKILL.md` — 取込手順の正本。手動トリガー「フォーム取り込んで」でも起動。
2. `~/.claude/scripts/form-intake/form_intake.sh` — launchdランナー。ネット疎通待ち→`claude -p`（失敗時30分後1回リトライ）→失敗時のみ`update_status.py form_intake error`。
3. `~/.claude/scripts/form-intake/intake_prompt.md` — headless用プロンプト（SKILL.mdを読んで実行せよ、の薄いラッパー＋headless注意事項）。
4. `~/.claude/scripts/form-intake/_state.json` — シート別処理済み行数。**Notion登録が成功した分だけ進める**（失敗分は翌夜再処理）。
5. `~/.claude/scripts/form-intake/_form_status.json` — ohayo表示用（実行日・新着件数・各件1行要約・NotionURL・エラー）。
6. `~/Library/LaunchAgents/com.kusagawa.form-intake.plist` — 毎晩3:30（drive-pipeline 2:30／discord-intake 3:10の後）。ProgramArguments は kusagawa-pipeline-bash 経由（FDA）。
7. パイプライン死活は既存 `_pipeline_status.json` に `form_intake` キーでマージ（`~/.claude/scripts/sns-routine/update_status.py` を流用）。

## 取込処理（SKILL.md正本の要約）

1. ToolSearchでDrive/Notion MCPツールをロード（headlessのdeferred誤判定対策・必須）。
2. `_state.json` を読み、3シートをDrive MCPで読んで新着行を抽出。0件なら status ok「新着0件」で終了（Notionは触らない）。
3. 新着1件ごとに：
   - ikenスキルStep1と同じ解析（氏名/連絡先/経路=フォーム→「その他」/地区/分類タグ/緊急度）
   - **重複ガード**: 📝市民意見リストの直近14日を検索し、同一内容（冒頭一致等）が既登録ならスキップ（日中に手動ikenで登録済みのケース）
   - 📝市民意見リスト（c2c34bd8-）へ登録（ikenスキルStep3のプロパティ仕様に完全準拠）
   - 6ドメイン分類→`03_themes/_citizen_voice/<domain>.md` の個別意見一覧末尾に既存形式で追記（**メール・電話・LINE IDは削除、氏名は氏のみ/匿名化**）＋`_index.md`件数更新
4. `_form_status.json` 書き出し＋`_state.json`更新＋`update_status.py form_intake ok "新着N件登録"`。
5. 自治会紐付け（iken Step3.5）・返信案・タスク化は夜間はやらない（朝以降、草川指示で）。

## ohayo連携

- `_pipeline_status.json` の `form_intake` キー死活チェック（error→🚨／updated 26h超→🚨 launchctl案内）を既存discord_intake節と同型で追加。
- 新着があった朝は「📮ご意見箱 新着◯件」セクションに `_form_status.json` の1行要約＋NotionURLを表示し、「返信案作って」でikenの後半フローへ接続。

## エラー方針

- Drive/Notion MCP不通・claude失敗 → statusにerror → 翌朝ohayoが🚨＋「フォーム取り込んで」手動実行を案内。stateは進まないので取りこぼしなし。
- シート行数が減っていた（=想定外の削除）→ その夜は取込せずerror報告（誤差分検出防止）。

## 初回キャッチアップ

stateはETL時点（2026-04まで処理済み）で初期化するため、初回実行は2026-05〜07の未取込分をまとめて処理する。
初回はlaunchd任せにせず「フォーム取り込んで」で対話実行し、草川が結果を目視確認する。

## やらないこと（YAGNI）

- GAS・Google Sheets API直叩き（認証整備が重い。Drive MCPで足りる）
- リアルタイム通知（日次で十分）
- 夜間の返信案自動生成（承認ルールと相性が悪い・トークン浪費）

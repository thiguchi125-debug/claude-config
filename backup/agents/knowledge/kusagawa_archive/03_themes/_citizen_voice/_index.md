# 市民の声 ETL Index

**ETL日時**: 2026-05-06
**増分取込**: 2026-08-07（S2-213・病児保育の利用促進）／2026-07-29（S2-212・体育館の冷房設置要望）／2026-07-27（S2-211・図書館の水飲み場要望）／2026-07-25（S1-41〜48/S2-196〜210/S3-125〜148・テスト3件除外）
**ETL実施者**: Claude Code subagent (general-purpose)
**ミッション**: Step A v2 施策発掘の素材整理

## 出典シート

| # | タイトル | fileId | 期間 | 件数 |
|---|---|---|---|---|
| 1 | 【2025アンケート】市政へのご意見（回答） | 1F-zNtaJPyD8XRM_UYcajsSGnuONG9afEX5VfBBsth5k | 2025/7〜2026/7 | 48件 |
| 2 | 市政へのご意見（アンケートなし）（回答） | 1sJzr4TGsO963wyIsFbSeBM18e5Oy8xhHVbTmRshmDXo | 2022〜継続 | 213件（うちテスト2件は取込対象外） |
| 3 | 市政へのご意見（アンケートあり）（回答） | 1Lqj24se04T-q6VkF3RayAk0ZHy9Ym9OD8541EHjn8ec | 2021〜継続 | 148件（うちテスト1件は取込対象外） |
| **計** | | | **2021/06〜2026/08** | **406件（=359＋増分47・テスト3件除外）** |

## ドメイン別件数

| ドメイン | 件数 | ファイル |
|---|---|---|
| childcare_education（子育て・教育） | 169 | childcare_education.md |
| urbanplanning_industry（都市計画・産業誘致） | 53 | urbanplanning_industry.md |
| transport_infrastructure（交通・インフラ） | 66 | transport_infrastructure.md |
| disaster_safety（防災・安全・水道） | 38 | disaster_safety.md |
| dx_administrative（行政DX・市役所運営・市政情報発信） | 62 | dx_administrative.md |
| healthcare_welfare（医療・福祉） | 17 | healthcare_welfare.md |
| _other（その他） | 1 | _other.md |
| **合計** | **406** | |

## 個人情報配慮

- メールアドレス・電話番号・LINE IDは全件マスク／削除済み
- 氏名は「氏のみ」（surname-only）に短縮、または匿名化
- フルネーム検出時は「匿名」に置換
- 年代・地区（小学校区）はそのまま保持

## 増分取込運用（今後）

新規回答が3シートに追加された場合：

1. `mcp__claude_ai_Google_Drive__read_file_content` で増分行を抽出
2. 6ドメインのいずれかに分類（`/tmp/citizen_voice_etl/parser.py` の DOMAIN_KEYWORDS / STRONG_SIGNALS / classify() を再利用）
3. 該当ドメインファイルに追記（時系列順を維持）
4. _index.md の件数・日付を更新

実装案：oyasumi（夜間バッチ）で週次自動更新、または iken / nichijo / policy-update スキルから手動更新。

## 分類スキーム概要

- **dx_administrative** — 行政DX・市役所運営・市政情報発信・行政手続オンライン化・市役所と「あいあい」分散・パブコメ・市民対話・選挙透明化・プレミアム商品券販売
- **childcare_education** — 保育・幼稚園・学校教育・給食・学童・不登校・特別支援・子ども医療費・不妊治療・出産支援・ヤングケアラー・教職員働き方・GIGAスクール
- **healthcare_welfare** — 医療体制・産科・産後ケア・介護・地域包括ケア・認知症・障害福祉・高齢者支援・予防接種・がん検診・健康づくり・国保・ひきこもり
- **disaster_safety** — 防災・避難計画・水道濁り問題・水道管老朽化・災害広報・通学路安全・交通安全・自主防災・太陽光適正条例・ため池・獣害
- **transport_infrastructure** — 関西本線電化・コミュニティバス・デマンド交通・高齢者免許返納・道路歩道・自転車レーン・空き家・市営住宅・上下水道（事故以外の維持管理）
- **urbanplanning_industry** — コストコ誘致・リニア亀山駅・IKEA等大型商業・商店街・駅前活性化・ふるさと納税・関宿/坂本棚田観光・創業支援・産業団地・歴史博物館・移住定住・市内雇用
- **_other** — 上記6つに収まらない

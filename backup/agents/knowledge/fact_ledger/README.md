# 検証済み事実台帳（fact_ledger）

content-fact-checker が一次情報で確認した主張を1行ずつ蓄積する。目的＝同じ数字を毎回Webから取り直さない（2026-09-05新設。それまで1本平均50回・5.5Mトークン）。

- 形式: `verified_facts.tsv`（タブ区切り）`日付 / 判定(VERIFIED|INCORRECT) / 主張 / 正しい値 / 出典URL / テーマ`
- 引き方: `grep -i "<KW>" verified_facts.tsv`。180日以内（変動する数字は90日）なら再取得しない
- 書き方: `printf '%s\t%s\t%s\t%s\t%s\t%s\n' ... >> verified_facts.tsv`
- 個人情報・非公開資料由来の値は書かない。INCORRECTも残す（同じ誤りの再発検知）
- 兄弟＝`research_ledger/`（調査レポート単位）。こちらは主張1行単位

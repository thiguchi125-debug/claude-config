# 亀山市選挙データセット

草川たくや議員（亀山市議会議員）の2026年10月25日選挙準備のため、`electoral-district-strategist` エージェントが恒久参照する基礎データ。

## 最終更新日
2026-04-26（kameyama-researcher による初回収集）

## ファイル一覧

| ファイル | 内容 | 取得元 |
|---------|------|--------|
| `kameyama_election_2022.md` | 2022年市議選結果（候補者21名・投票区別投票者数29カ所） | 亀山市公式・広報亀山PDF・選挙ドットコム |
| `kameyama_election_2018.md` | 2018年市議選結果（候補者23名） | 亀山市公式 |
| `voting_districts.md` | 投票区マスタ（29投票区） | 亀山市公式「投票所一覧」 |
| `population_demographics.md` | 町別人口（令和8年4月1日現在）・年齢別人口・地区別 | 亀山市公式統計（PDF直抽出） |
| `competitor_landscape.md` | 現職17議員（1欠員）・会派構成・所属政党 | 亀山市議会名簿PDF・Wikipedia・選挙ドットコム |
| `data_gaps.md` | 取得できなかった情報のリスト（手動補完すべき項目） | — |

## データソース一覧

### 一次情報（亀山市公式）
- 2022年市議選結果: https://www.city.kameyama.mie.jp/docs/2022102000014/
- 2018年市議選結果: https://www.city.kameyama.mie.jp/docs/2018102800013/
- 投票所一覧: https://www.city.kameyama.mie.jp/docs/2021121300020/
- 人口統計トップ: https://www.city.kameyama.mie.jp/shisei/2014112308662/
- 町別人口PDF: https://www.city.kameyama.mie.jp/shisei/2014112308662/file_contents/town_0804.pdf
- 年齢別人口PDF: https://www.city.kameyama.mie.jp/shisei/2014112308662/file_contents/age_0804.pdf
- 議員名簿PDF: https://www.city.kameyama.mie.jp/gikai/giin/2015111300046/file_contents/giinmeibo071114.pdf
- 広報亀山2022.11.16号（選挙特集）: https://www.city.kameyama.mie.jp/docs/2022110900030/file_contents/koho_221116-6-7.pdf
- 選挙管理委員会事務局: https://www.city.kameyama.mie.jp/categories/groups/senkan/

### 補助情報
- 選挙ドットコム（2022年候補者プロファイル）: https://go2senkyo.com/local/senkyo/20432
- Wikipedia「亀山市議会」: https://ja.wikipedia.org/wiki/%E4%BA%80%E5%B1%B1%E5%B8%82%E8%AD%B0%E4%BC%9A
- 政治山「三重県亀山市」: https://seijiyama.jp/lgov/24/242101/
- 選挙ドットコム（2026年予定）: https://go2senkyo.com/local/senkyo/26143

## 重要な注意事項

1. **投票区別×候補者別マトリクス（最重要データ）は亀山市公式サイトでは未公開**。市選挙管理委員会への直接問い合わせが必要（TEL: 0595-84-5017、senkan@city.kameyama.mie.jp）。詳細は `data_gaps.md` 参照。
2. 投票区別の**投票者数・投票率**は2022年分のみ取得済（広報亀山PDFから抽出）。2018年分は未公開。
3. 人口データは**令和8年4月1日現在**の最新値（市町村合併後の22地区分類で集計）。
4. 議員名簿は2026年4月時点。議席番号17が**欠員**（前任者引退または辞職）。

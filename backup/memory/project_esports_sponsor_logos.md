---
name: project_esports_sponsor_logos
description: 亀山市eスポーツ協会の制作物のロゴ規約＝協会公式ロゴTUIRTLE必須（置き場・透過版・発光処理）＋スポンサー10社の掲載順（草川指定・固定）と加工ルール
metadata: 
  node_type: memory
  type: project
  originSessionId: 46213ebf-544f-4b50-8754-187bf9d796e7
  modified: 2026-08-10T05:10:12.419Z
---

亀山市eスポーツ協会の制作物にスポンサー10社を載せるときの**掲載順は固定**（2026-08-10 草川指定）。
協会の**年間スポンサー**表記であってイベント単発の協賛ではないため、回が変わっても同じ帯をそのまま流用する。

見出し＝`OFFICIAL SPONSORS` ＋「亀山市eスポーツ協会 オフィシャルスポンサー（順不同）」

**5列×2段の並び（この順を崩さない）**

| | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| 上段 | エイド | くるま屋ごとう | i-Living ひのきの家 | BUARTS | 中野久生事務所 |
| 下段 | 日本ハウスHD | いのうえサポート合同会社 | 河村設備 | ときわ自動車 | 有限会社太田コンクリート |

**素材の正本**: `~/publications/2026-09_esports_circle_0919/02_制作データ/sponsors/`
（`*.png`＝カラー整形済／`gray/`＝インク節約版用／`_raw/`＝受領原本）。Driveミラーは
`日常資料アーカイブ/04_印刷物素材/2026-09_eスポーツサークル0919案内/`。

**加工ルール（再現時に必ず守る）**
- 中野久生事務所・ときわ自動車・日本ハウスHDは受領画像に**外枠の矩形**がある→除去して文字だけにする
- **BUARTSは黄色地のまま使う**（草川指示）。ただしインク節約版だけは黄色が灰ベタになるので白地ロゴ版（`gray/06_buarts.png`）
- くるま屋ごとうは2枚の板の間の空白を詰めてから配置（そのままだと板が極端に小さくなる）
- 縦横比がバラバラなので**1点ずつCSSで上限を変えて光学的な大きさを揃える**（heavy=黒ベタ社名は幅を抑える／tall=河村設備／sq=i-Livingは高さを上げる／wood=くるま屋／plate=黄色地BUARTS）。**並び替えるときはクラスもロゴに付いて動かす**

**未確認（草川手番）**: 10社の掲載可否・社名表記の協会側同意／太田コンクリートの高解像度版（受領画像は376×53pxでA4 300dpiちょうど原寸）

## 協会公式ロゴ「TUIRTLE」は必ず使う（旧 feedback_esports_association_logo を統合 2026-09-05）

協会の制作物（チラシ・告知・SNS画像・スライド等）には**今後も必ず公式ロゴ「TUIRTLE」を使用**（2026-06-23 草川直接指示）。
- 正本: 原本（白背景）`~/.claude/projects/-Users-kusakawatakuya/assets/esports_logo/logo_original.png`／透過版（推奨）`同/logo_transparent.png`（321×228）
- 仕様: 緑＆グレーのカメ＋甲羅がゲームパッド、ワードマーク「TUIRTLE」（turtleの捩り・意図的表記）、下帯「KAMEYAMA CITY ESPORTS ASOCIATION」（**"ASOCIATION" は原本の表記のまま尊重・勝手に直さない**）
- Why: 協会のブランド統一。手描きの汎用ゲームパッド等で代用すると協会らしさが出ずブランドが分散する。任天堂ロゴの代わりにもなり権利面も安全（[[project_nintendo_tournament_license]]）
- ダーク背景には透過版をそのまま置き、暗背景でフチが沈むので `filter: drop-shadow(...) drop-shadow(0 0 30px rgba(199,255,74,.18))` 等で淡く発光させる。白背景は原本でも透過版でも可
- ロゴ内に既にゲームパッド要素があるため、別途コントローラーのイラストを足すと重複→ロゴをマスコットの主役に据える
- 透過処理の再現: 四隅からの白フラッドフィル（near-white>236を連結成分で抜く）→内部のシルバー文字は保持→getbboxでトリム（PIL）
- 初出制作物: `drafts/2026-06_esports_smash/flyer_a2.html`（スマブラ交流＆大会チラシ・ダークのアーケードeスポーツ調）。テンプレ化済み＝`design_system/templates/flyer_a4/`

関連: [[feedback_esports_mail_meigi_separation]] [[project_design_studio]]

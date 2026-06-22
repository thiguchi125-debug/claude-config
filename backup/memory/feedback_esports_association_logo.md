---
name: feedback_esports_association_logo
description: 亀山市eスポーツ協会のチラシ等制作物には必ず公式ロゴ（TUIRTLE）を使用する。ロゴ画像の保存場所と透過処理メモ
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4408ae7c-f1b4-47f3-80be-cc86a051d060
---

亀山市eスポーツ協会の制作物（チラシ・告知・SNS画像・スライド等）には、**今後も必ず公式ロゴ「TUIRTLE」を使用**する（2026-06-23 草川直接指示）。

**ロゴ保存場所（消えない正本）**:
- 原本（白背景）: `~/.claude/projects/-Users-kusakawatakuya/assets/esports_logo/logo_original.png`
- 透過版（背景抜き済・推奨）: `~/.claude/projects/-Users-kusakawatakuya/assets/esports_logo/logo_transparent.png`（321×228）

**ロゴ仕様**: 緑＆グレーのカメ＋甲羅がゲームパッド、ワードマーク「TUIRTLE」（turtleの捩り・意図的表記）、下帯「KAMEYAMA CITY ESPORTS ASOCIATION」（※"ASOCIATION"はロゴ原本の表記のまま尊重・勝手に直さない）。

**Why**: 協会のブランド統一。手描きの汎用ゲームパッド等で代用すると協会らしさが出ず、ブランドが分散する。任天堂ロゴの代わりにもなり権利面も安全。

**How to apply**:
- ダーク背景には透過版をそのまま配置。暗背景でフチが沈むので `filter: drop-shadow(...) drop-shadow(0 0 30px rgba(199,255,74,.18))` 等で淡く発光させて浮かせる。
- 白背景制作物には原本でも透過版でも可。
- ロゴ内に既にゲームパッド要素があるため、別途コントローラーのイラストを足すと重複する→ロゴをマスコットの主役に据える。
- 透過処理の再現: 四隅からの白フラッドフィル（near-white>236を連結成分で抜く）→内部のシルバー文字は保持→getbboxでトリム（PIL、scriptは2026-06 esportsチラシ制作ログ参照）。

初出制作物: `drafts/2026-06_esports_smash/flyer_a2.html`（スマブラ交流＆大会チラシ・ダークのアーケードeスポーツ調）。

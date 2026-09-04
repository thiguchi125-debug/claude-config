---
name: feedback_short_video_use_virality_architect_first
description: ショート動画原稿は最初からshort-video-virality-architectで作る。素朴生成の長尺はNG
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b0bba8ff-ab56-4683-9d90-c90ab7651703
---

ショート動画（TikTok/Shorts/Reels）の原稿は、**最初から `short-video-virality-architect` を使う**。daily-content-generator や素朴な生成で出すと、情報を詰め込みすぎて90秒超・冗長・分かりにくくなり、草川本人からNGが出る（2026-05-27 子ども医療費動画で実際に発生：「急いで読んでも90秒以上、想定が甘い、分かりにくい」と指摘）。

**草川のショート動画基準**：
- 尺は **35〜45秒厳守**（読み上げ実測。日本語ナレーション ≒ 6字/秒 → 40秒で約240字が上限目安）
- **1動画＝1メッセージ**。年表・試算額・制度の細部・数値羅列は完視聴率を削るノイズとしてカット
- 冒頭1.5秒で最強の数字/対比フック。「皆さんこんにちは」型・自己紹介・前置き禁止
- 1.5〜2秒ごとに画/テロップ切替、ループ設計、末尾コメント誘発の問い1つ
- 3バリアント（A数字ショック/B共感/C議論喚起）、各40秒前後

**Why**: ショート動画は完視聴率が命。長い＝即離脱＝アルゴリズム不利。専門エージェントは8軸自己診断（64/80でship）と retention curve 設計を持つ。

**How to apply**: 「ショート動画作って」「動画の原稿」系の依頼、および short-video-create / daily-content-generator のショート動画工程では、セリフ生成の主担当を必ず short-video-virality-architect にする。素朴生成→後で短縮は二度手間（2026-05-27は v1長尺→ファクト精査多数→本人NG→作り直しで往復が膨らんだ）。関連: [[feedback_kusagawa_short_video_script_style]] [[project_short_video_create_system]]

**2026-09-02 再発（周産期通院支援）**: SNS7種一括生成で `sns-content-creator` が7枠目のTikTok台本を自前生成し、58秒・数値羅列7種の原稿を納品。
真因は「ルールを忘れた」ではなく **経路にルールが無かった**こと — 本ルールは short-video-virality-architect.md 末尾（＝呼ばれなかったagent）にしか無く、
実際に走った sns-content-creator.md §7 は逆に「30〜60秒／46〜60秒で行動宣言」と書いていた。仕様に忠実に従うと必ず違反する状態だった。
対策（2026-09-03 実施）: ①sns-content-creator.md §7 を委譲指示に書き換え・30〜60秒表記を35〜45秒へ是正・チェックリストに尺と数値羅列を追加
②content-pipeline SKILL.md の生成メディアを6種に変更し、7枠目は architect へ委譲する節を追加 ③MEMORY.md索引に個別行を露出。

**2026-09-03 再々発（かめやま健康弁当）**: 60秒・実食枠なしでも52秒・数値12個・年表付きの台本が「確定版」として drafts/ と引き継ぎメモに載った。
真因は今回も「ルールを忘れた」ではなく **経路にルールが無かった／機械が黙って通した**の2つ。
- **①仕様が自己矛盾していた**: `short-video-virality-architect.md` は本体が全編「60秒・15カット以上」「### 60秒カット表」「target_length既定60秒」で書かれ、
  35〜45秒は**末尾の📌ガードルール1行だけ**だった。仕様に忠実に従うほど違反する。`short-video-create/SKILL.md` も「既定60秒」「長さ60秒」、
  さらに読み上げ速度が **8.4字/秒**（architectとmemoryは6字/秒）で、同じ字数を短く見積もる＝過積載の設計になっていた。
- **②機械判定が表記ゆれで黙ってスキップしていた**: `check_content_limits.py` の尺判定は `0:(\d\d)-0:(\d\d)` 固定で、
  `0:00.0–0:02.7`（小数秒・全角ダッシュ）を1件も拾えず、カット数も `| C1 |` 形式を拾えなかった。
  **違反6件のはずが「違反2件」と表示**され、しかも検出できなかったことを表示しない silent skip だった。
- **③🚨が出ていたのに出荷された**: 憲法「撮っている理由」欠落は当時から検出されていたが、原稿は保存され引き継がれた。チェッカーの出力が出口を止めていなかった。

**対策（2026-09-03 実施・すべてテスト済み）**:
1. `short-video-virality-architect.md`：本体の60秒表記を全て35〜45秒・18カット以上・1カット3.0秒以内に是正。冒頭に「草川案件は例外なく35〜45秒。この一行が本文中のどの秒数記述より優先」を追加。
   憲法直後に**出力前ハードゲート**（check_content_limits.py で違反0件でなければ出さない／秒表記は `0:00.0-0:02.7` 形式／45秒に入らないならカットを詰めず**セリフを削る**）を追加。
2. `short-video-create/SKILL.md`：既定を35〜45秒に。読み上げ速度を **8.4字/秒→6字/秒** に統一。
3. `check_content_limits.py`：尺判定を表記ゆれ耐性に（小数秒・全角ダッシュ・分表記）。**判定不能そのものを違反として出す**（silent skip廃止）。
   **3.0秒超カット**・**尺に対するカット密度**・**セリフ中の数値6個以下（1動画1メッセージの機械近似）**を新設。
4. `hooks/short_video_limits_gate.py` 新設＋settings.json登録：**Write/Editで動画台本を規定違反のまま保存しようとすると deny**（Bash保存はPostToolUseで警告）。
   草川承認済みの逸脱のみ `<!-- FORMAT-EXCEPTION: 尺=NN秒 / 草川承認 YYYY-MM-DD / 理由 -->` で通る（自己承認は不可）。

**教訓（横断）**: 同じ事故が3回とも「人が忘れた」ではなく **仕様の矛盾＋機械の見逃し**で起きている。
ルール違反を見つけたら、まず**その経路の仕様ファイルが何と書いてあるか**と**機械判定がその項目を本当に見ているか**を確認する。markdownに注意書きを足すのは対策ではない。


**2026-09-05 尺規定の見直し（草川決定）**: 35〜45秒の根拠を洗ったところ、実データでなく2026-05-27の1件のNG＋一般論だった。
草川決定＝**許容35〜50秒／目標45〜50秒**（6字/秒→上限約300字）。同日、`check_content_limits.py`（VIDEO_MAX_SEC=50）・`short_video_limits_gate.py`・
`short-video-virality-architect.md`・`sns-content-creator.md`・skills（short-video-create／ai-kusakawa／content-pipeline／daily-content-generator）・
sns-routine legs を同時に書き換え、食い違い（60秒以内／45〜60秒／50秒以内）を解消。**1動画1メッセージ・1カット3.0秒以内・数値6個以下は据え置き**（質を守るのはこの3つ）。

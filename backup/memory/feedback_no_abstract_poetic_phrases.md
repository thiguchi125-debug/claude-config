---
name: feedback_no_abstract_poetic_phrases
description: 響かない抽象・詩的比喩（「家計の音が変わる」等）は使わない。意味は具体的な事実・行為・金額で書く
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 97a453c2-2c4b-4bb3-93b0-d293fc581677
---

発信物（SNS・ブログ・動画セリフ・スピーチ・印刷物すべて）で、**意味がぼやける抽象的・詩的な比喩表現は使わない**。読み手が「何のこと？」とつまずく時点で失敗。

**禁止例（実際に草川NG）:**
- 「家計の音が変わる」← 2026-06-02 子ども医療費18歳動画のSNS化で全7PFに混入。意味＝「中学まで無料だった病院代が高校で自己負担に戻り出費が増える」だが、詩的にぼかして伝わらなくなった
- 「次の旗」「希望の旗」「旗を立てる/掲げる」← 2026-06-11 6月議会一般質問シャープ後産業のビジョン質問で multiuse。草川「この文脈で無理に『旗』を使うのは一般的でないし意味不明で響かない」と直接NG。→「次の産業の柱」「次に何で食べていくか」「次の主力産業」等の具体語へ全置換。**議会質問・スピーチ・原稿でも同様。general-question-architect等のエージェントは"旗""希望の旗"フレームを好むので生成後に必ず潰す**
- 同種: 「〇〇の音が変わる」「心に灯がともる」「未来への種をまく」等の情緒系メタファー全般

**Why:** 抽象詩語はAI臭が強く、具体の力（金額・行為・固有名詞・年齢の崖）を消す。草川の声は「数字と運用詳細を厚く・生活シーン先行」が芯。比喩で雰囲気を出すと逆に何の話か分からなくなり響かない。

**How to apply:**
- 比喩を書きそうになったら「これを具体的な事実・行為・お金の動きに直すと？」と自問して書き換える
- 例: 「家計の音が変わる」→「子どもの病院代が、また家計の負担に戻ってくる」「これまで無料だった病院代を、また払うようになる」
- 生活シーン先行はOK（[[feedback_sns_citizen_lifescene_first]]）。ただしシーンも"具体的な行為・場面"で描き、抽象比喩で締めない
- sns-content-creator / blog-writer / short-video-virality-architect の出力に詩的メタファーが出たら、確定前に具体へ置換

関連: [[feedback_phrase_todokanakutemo_todoku]] [[feedback_phrase_todokanai_owaraseru]] [[feedback_metric_distance_metaphor_avoid]] [[feedback_sns_citizen_lifescene_first]] [[feedback_no_fabricated_stories]]

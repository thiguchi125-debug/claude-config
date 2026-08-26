---
name: feedback-askuserquestion-preview-hides-freetext
description: AskUserQuestionでoptionにpreviewを付けると左右分割UIになり「Type something」の自由記述欄が出なくなる
metadata:
  type: feedback
---

AskUserQuestion の option に `preview` を付けると UI が左右分割レイアウトに切り替わり、**「Type something」の自由記述欄が表示されなくなる**。草川が意見を書くには質問全体をキャンセルするしかなくなる。

**Why:** 2026-08-26、文案を大きく見せようとして毎回 preview を付けた結果、草川が「意見を入力するには毎回全部キャンセルしなければならない」と何度も指摘することになった。原因の特定に時間をかけてしまった。

**How to apply:**
- **判断だけを聞く質問には preview を付けない**（label と description で足りる）。これで Type something が出る
- **文案を読み比べる必要があるときは、本文をチャットのメッセージ側に書き、選択肢は preview なしの短いラベルにする**。両方成立する
- 番号を並べた平文で選択肢を出すのも草川の好みではない。**選択肢は AskUserQuestion ツールで出す**
- 関連: [[feedback-ask-one-by-one-choices]]

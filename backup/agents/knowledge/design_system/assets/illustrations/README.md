# イラスト素材庫（自前生成・政治利用セーフ）

> 「淡色＋水彩＋キャラ」路線（[[feedback_flyer_bright_illustration_style]]）をHTML/CSS印刷物で実現するための
> 装飾イラスト置き場。**いらすとや等のフリー素材は政治利用禁止規約があるため使わない**。全て自前生成。

## 運用フロー

1. `prompt_cards.md` のカードを草川がGemini（nano-banana）にコピペして生成
2. 生成PNGをこのフォルダに投入（ファイル名はカードID: `flower_sakura_01.png` 等）
3. Claudeに「イラスト素材庫を台帳化して」→ `catalog.html`（一覧プレビュー）を再生成
4. design-studio Step2 で photo-curator と並ぶ素材源として参照

## 白背景素材の使い方（透過が不完全でも困らない）

nano-banana は真の透過PNGが安定しないため、**白背景で生成**して以下で馴染ませる:

- 淡色背景のチラシ: `mix-blend-mode: multiply;` で白が消えて水彩だけ乗る（最も確実・推奨）
- どうしても透過が必要な場合: Claudeに依頼→PIL で白抜き処理（水彩のにじみは劣化するので multiply 優先）

## 命名規約

`<カテゴリ>_<モチーフ>_<連番>.png` — カテゴリ = flower / season / people / frame / washi

## 権利メモ

自前生成（Gemini出力）のみ。実在人物・実在ロゴ・キャラクターIP風の生成は禁止（prompt_cards.md のガード文言を削らない）。

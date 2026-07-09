# AIくさかわ キャラ生成 nano-bananaプロンプトカード

> 使い方: Gemini（nano-banana）に**参照写真を添付**してから各カードの英語プロンプトを貼る。
> まずカード1〜3で3スタイルを1枚ずつ生成→草川が好みのスタイルを選択→
> カード4で口差分2枚を生成→計3枚（口閉じ・半開き・開き）を `assets/character/` に保存→
> Claudeに「AIくさかわのキャラ画像を投入して」と指示（クロップ・座標調整・E2EはClaude側で実施）。

## 参照写真（photo-curator選抜済・Geminiに添付する）

```
/Users/kusakawatakuya/Desktop/AIくさかわ参照_写真候補/参照1_2025-01-19_スーツ正面.jpg
/Users/kusakawatakuya/Desktop/AIくさかわ参照_写真候補/参照2_2025-04-16_スーツ緑タイ正面.jpg
/Users/kusakawatakuya/Desktop/AIくさかわ参照_写真候補/参照3_2026-06-29_白シャツ夕景.jpg
```
- 参照1: スーツ正面・柔らかい笑顔（顔の素性把握用）
- 参照2: スーツ緑ネクタイ真正面（輪郭・髪型・服装の基準）
- 参照3: 白シャツやや斜め（立体把握の補強）
- 原本はDrive `📷写真ストック/10_使える写真/01_人物単独`。Desktopの3枚は30日スイープで消えるため、
  生成はお早めに。消えていたら「AIくさかわの参照写真をもう一度出して」でOK。

## 共通要件（全カード末尾に自動で含めてある）

- 明るく親しみやすいイラスト（feedback_flyer_bright_illustration_style準拠・暗く硬い絵は不可）
- 40代日本人男性・参照写真の顔立ちに寄せる・スーツ＋緑系ネクタイ
- 正面向き・胸から上・背景は単色 #1f5a3a・口は閉じ
- 9:16向け（1080×1920で顔が上半分中央に来る構図）・文字入れなし

---

## カード1: スタイルA（水彩タッチの温かい似顔絵）

```
Create a warm watercolor-style illustrated portrait character based on the attached
reference photos. Subject: a friendly Japanese man in his 40s, faithful to the face
in the reference photos (face shape, hairstyle, eyebrows). He wears a navy suit with
a green tie. Front facing, waist-up, mouth closed, gentle smile, eyes open.
Soft watercolor texture, warm bright tones, light brush strokes, approachable and
kind mood. Plain solid background color #1f5a3a. Vertical 9:16 composition (1080x1920),
face centered in the upper half. No text, no logos.
```

## カード2: スタイルB（フラットで現代的な広報イラスト）

```
Create a modern flat-design illustrated portrait character based on the attached
reference photos. Subject: a friendly Japanese man in his 40s, faithful to the face
in the reference photos (face shape, hairstyle, eyebrows). He wears a navy suit with
a green tie. Front facing, waist-up, mouth closed, confident warm smile, eyes open.
Clean flat vector style with 2-3 tone cel shading, organic smooth curves (not
geometric primitives), bright and optimistic civic-communication mood.
Plain solid background color #1f5a3a. Vertical 9:16 composition (1080x1920),
face centered in the upper half. No text, no logos.
```

## カード3: スタイルC（親しみ系マスコット調）

```
Create a cute approachable mascot-style illustrated character based on the attached
reference photos. Subject: a friendly Japanese man in his 40s, clearly recognizable
from the reference photos but gently stylized with a slightly larger head and
simplified friendly features. He wears a navy suit with a green tie. Front facing,
waist-up, mouth closed, cheerful smile, eyes open. Soft rounded shapes, bright
pastel-leaning palette, hand-drawn warmth, the mood of a beloved local-community
mascot. Plain solid background color #1f5a3a. Vertical 9:16 composition (1080x1920),
face centered in the upper half. No text, no logos.
```

---

## カード4: 口差分2枚（選択スタイルの画像を添付して実行・1枚ずつ）

口半開き:
```
Edit the attached illustration. Keep everything absolutely identical — same character,
same pose, same colors, same background, same framing — and change ONLY the mouth:
the mouth is now half-open, as if mid-speech, showing a natural relaxed talking
expression. Do not move the head, eyes, or body.
```

口開き:
```
Edit the attached illustration. Keep everything absolutely identical — same character,
same pose, same colors, same background, same framing — and change ONLY the mouth:
the mouth is now wide open, as if pronouncing a clear vowel while speaking
energetically. Slight visible inner mouth is fine. Do not move the head, eyes, or body.
```

---

## 出力契約（Claude側の投入処理が前提にする形）

- 3枚とも**同一構図・同一サイズ**（口以外のピクセルが動いていないほど品質が上がる）
- 推奨ファイル名: `chara_closed.png` / `chara_half.png` / `chara_open.png`
- 置き場所: `~/.claude/scripts/ai-kusakawa/assets/character/`
- 投入指示ワード: 「**AIくさかわのキャラ画像を投入して**」
  → Claudeが目視確認→口領域クロップ→base再構成→config座標調整→E2E→フレーム目視まで実施

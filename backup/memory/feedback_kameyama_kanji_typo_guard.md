---
name: 「亀山」のtypo再発防止（亜山・亵山禁止）
description: AskUserQuestion等のJSON引数で日本語をunicode escape送信する際、「亀」(U+4E80)を「亜」(U+4E9C)「亵」(U+4EB5)に取り違える事故を防ぐルール
type: feedback
originSessionId: 496bb067-3041-43af-8073-485bc32bb7e8
---
AskUserQuestion等のtool引数に日本語を含めるときに「亀山」を「亜山」「亵山」と誤記する事故が立て続けに発生（2026-05-11セッション）。

**Why:**
- 「亀」のunicodeは U+4E80
- 「亜」は U+4E9C、「亵」は U+4EB5 — 視覚的に近いコードポイント
- escape形式で書くと脳内チェックが効かず、似た文字を混ぜてしまう
- 草川は亀山市議会議員。市名の誤記は信頼を損なう最も基本的なミス

**How to apply:**
- AskUserQuestion / Write / Edit 等のJSON引数で日本語を含める時は、unicode escape形式ではなく日本語のまま直接書く（特に「亀山」「亀山市」を含む文字列）
- やむを得ずescapeを使う場合は、「亀」= `亀` であることを毎回目視確認
- typoを発見した時は即訂正し、本ファイル更新で記録を更新
- 関連する変換ミス候補：「亜山」「亵山」「龜山」（旧字体は人名地名で稀に使うが市名は新字体「亀山」が正）

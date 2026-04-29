---
name: nichijo＋oyasumiにCalendar連携
description: 2026-04-29実装。当日Calendar（kusakawa.taku@gmail.com）から議員業務分（KEEP）を自動抽出し日次ログ「📅本日のスケジュール」セクションに反映。nichijoはStep1.5新設・oyasumiはStep2分岐2-A/2-B
type: project
originSessionId: 5c4d4819-c63f-43f1-b3e9-ef800355d065
---
# nichijo＋oyasumiへのCalendar連携運用（2026-04-29実装）

## 何が変わったか
nichijoとoyasumiが当日Google Calendar（`kusakawa.taku@gmail.com`）を読み、議員業務として記録に値する予定（KEEP）を活動ログに自動反映するようになった。

**Why:** 朝に「今日のネタ抽出」した際、Calendarに登録された街頭演説／挨拶まわり／地域行事等の予定が活動ログに反映されておらず、コンテンツ抽出（C1）の情報源として見えなかった。Calendar記述を加えると⑤現場報告SNSが具体化し、⑥「等身大型ブログ」のような新規テーマ候補が見えてくる。

**How to apply:**
- nichijo記録モード起動時：Step 1.5 で当日Calendar取得→KEEP分を `### 📅 本日のスケジュール（Google Calendar抽出・議員業務分のみ）` セクションに自動反映
- oyasumi起動時：日次ログが既存ならStep 2-Bで同セクションが無ければ追記、既存なら何もしない
- KEEP（記録に残す）：議会公務／視察／委員会／市民相談／街頭演説／挨拶まわり／地域イベント／後援会・支持者交流／講演登壇／公開行事
- SKIP（除外）：家族関連／個人習い事／【参考】プレフィクス／private明示
- 判断迷ったらKEEP寄り

## ファイル変更箇所

### nichijoスキル（`~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/nichijo/SKILL.md`）
- Step 1.5新設（KEEP/SKIP判定基準・Calendar取得パラメータ・抽出フォーマット）
- Step 2-Bテンプレートに `### 📅 本日のスケジュール` 追記処理追加
- Step 2-Cテンプレートに `### 📅 本日のスケジュール` セクション追加
- コンテンツ抽出モードC1表に📅Google Calendar行追加
- C2判断ルールに「Calendar当日分の取り扱い」追記（事前予定はSNS予告系、ブログ深掘りには回さない）
- 統合仕上げモードU1並列スキャンにCalendar追加

### oyasumiスキル（`~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/oyasumi/SKILL.md`）
- Step 2を2-A（ページ無し→新規生成）と2-B（ページ有り→Calendarセクション補完）に分割
- KEEP/SKIP判定基準をnichijo Step 1.5と同期

## カレンダーID（再掲）
- `kusakawa.taku@gmail.com`（kusagawaは誤り。2026-04-26取りこぼし事故済み）

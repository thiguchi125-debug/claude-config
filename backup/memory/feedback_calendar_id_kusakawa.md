---
name: カレンダーIDは kusakawa.taku（kusagawa ではない）
description: 草川たくやの2つ目のGoogleカレンダーIDの正しい綴りと、過去のtypo事故を防ぐための運用ルール
type: feedback
originSessionId: 6d722022-d55b-4d60-b1f2-5c2dbe39b743
---
草川たくやのGoogleカレンダーIDは `kusakawa.taku@gmail.com`。`kusagawa.taku@gmail.com`（g付き）は存在せず、API呼び出しは `java.lang.Throwable` で失敗する。

**Why:** ユーザーの姓「草川」は「くさかわ（kusakawa）」と読む。漢字「草」を音読みで「kusa-ga-wa」と推測すると `kusagawa` という誤った綴りになる。実際のユーザーホームディレクトリも `kusakawatakuya` で、これが唯一正しい綴り。`ohayo` スキルのSKILL.md (line 18) も `kusakawa.taku@gmail.com` で正しく記載されている。2026-04-26朝のブリーフィングで実際にこのtypoが発生し、二本松自治会総会・藤まつり・街頭演説など6件の予定を取りこぼした事故あり。

**How to apply:** Google Calendar の `list_events` / `get_event` などで草川の個人アカウントを呼び出す際は必ず `kusakawa.taku@gmail.com`（k-u-s-a-k-a-w-a）を使う。スキル定義からコピペし、自分で打ち直さない。エラーが返ったら最初に綴りを疑い、必要に応じて `list_calendars` で利用可能IDを確認する。

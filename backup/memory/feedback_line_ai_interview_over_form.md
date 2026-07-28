---
name: feedback_line_ai_interview_over_form
description: 公式LINEに貼る意見受付導線はご意見箱フォームではなくAIインタビュー
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f6cee28f-1650-4ec3-9b0c-500dc2924d8e
  modified: 2026-07-28T00:16:28.973Z
---

**公式LINEの意見受付導線は「ご意見箱」ではなく「AIインタビュー」を貼る**（2026-07-28 草川指示）。
URL＝`https://depth-interview-kusagawa.vercel.app/interview/kameyama_shisei_zenpan`

**Why:** 公式LINEの登録者はすでに草川と接点のある層。フォームに書き込むより、AIが対話形式で掘り下げるほうが深い意見が集まる。ご意見箱は「まだ接点のない人が匿名で投げる入口」として使い分ける。

**How to apply:**
- 誘い文句は**市政全般**の書き方にする。config_id が `kameyama_shisei_zenpan`（市政全般）なので、個別テーマ専用のように書かない。型＝「市政へのご意見は、AIが対話形式で深掘りするインタビューからもお寄せいただけます。伺った内容は私のもとに届き、市政に活かしていきます。」
- LINE本文の並び＝本文 → ブログURL（[[feedback_sns_blog_link_required]]）→ AIインタビューURL → 「皆さんの声、これからもお聞かせください。」で終止。
- **ブログの定型フッター4本（ご意見箱／公式LINE／Threads／AIインタビュー）は従来どおり変更しない。** このルールは公式LINE本文だけに効く。
- 個別テーマ専用のAIインタビュー設定を新規に作った場合は、そのテーマのLINE配信ではそちらのURLに差し替える（設定作成は ai-interview-config-designer）。

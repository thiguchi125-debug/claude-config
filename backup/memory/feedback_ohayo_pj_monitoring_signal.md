---
name: ohayo-pj-monitoring-signal
description: ohayo シグナルに「動いてないPJ N件」を追加。閾値超え時に task-audit pj-focus モードへ誘導する仕組み。2026-05-21 草川指示。
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4309475f-1a19-41c7-a218-f3c8eab58267
---

# ohayo シグナル拡張：動いてないPJ 監視

**Why**: 2026-05-21 草川指示「PJ進捗監視を ohayo シグナルに「動いてないPJ N件」を追加」

**How to apply**: ohayo SKILL.md の v2.3 「§3-X-3 タスク監査シグナル」セクションに **PJ監視シグナル** を追加。

## 追加するシグナル

```
🔷 PJ監視シグナル（v2.6追加）
  ├ 動いてないPJ（30日超活動なし）: N件 [⚠️ or ✅]
  └ 「次の一手」不足PJ（進行中なのにDone以外0件）: M件 [⚠️ or ✅]
```

## 閾値

- **動いてないPJ ⚠️ 5件超**：注意水準
- **動いてないPJ 🚨 10件超**：危険水準・即起動推奨
- **次の一手不足PJ ⚠️ 3件超**：注意水準

## 誘導文の条件分岐

- ⚠️ が **1つでもある**場合：「task-audit pj-focus モード」で起動可能と1行誘導
- ⚠️ が **3つ以上**場合：強調表示「🚨 PJ整理急務」

## 判定ロジック（軽量）

ohayo Step 3-5 で「進行中プロジェクト」取得時に：

1. 各PJの最終更新日（updated_at）を取得
2. 直近30日に更新があるか判定
3. 進行中ステータスのPJに対して、関連タスクが全てDone/Archiveでないか判定（タスク先頭1件の状態確認）

トークン追加：+3-5K（軽量・PJ DB 1回叩くのみ）

## task-audit 連動

- ohayo の警告誘導文：「PJ N件動いてません→ pj-focus モードで「PJ整理」を起動」
- task-audit SKILL.md の pj-focus モードと連動（[[feedback_task_audit_pj_monitoring]] 参照）

## 関連メモリ

- [[feedback_ohayo_task_audit_signal]] — ohayo v2.3 タスク監査シグナル（同じ場所に追加）
- [[feedback_task_audit_pj_monitoring]] — task-audit pj-focus モード設計
- [[project_task_audit_2026-05-21]] — 初回実施記録・本シグナル設計の起点

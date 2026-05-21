---
name: council-materials-intake
description: DEPRECATED 2026-05-21 — このスキルは drive-intake に統合されました。「議会資料取り込んで」「議案書取り込んで」「議会資料インテーク」「council-materials-intake」等の旧トリガーは全て drive-intake が継承しています。本フォルダは後方互換のため残置されていますが、実装は drive-intake/SKILL.md を参照してください。
---

# council-materials-intake (DEPRECATED)

⚠️ **このスキルは 2026-05-21 に [drive-intake](../drive-intake/SKILL.md) に統合されました。**

## 移行先

すべてのトリガー語・実行ステップ・Drive構造定義は drive-intake スキルが継承しています。

```
旧 council-materials-intake  →  drive-intake モードA（即時取込・議会資料）
旧 drive-sync-review         →  drive-intake モードC（レビュー承認型）/ D（手動差分スキャン）
旧 weekly-drive-sync         →  drive-intake モードD（2026-05-21に drive-sync-review 経由で統合済み）
```

## なぜ統合したか
3スキルとも実態は同じ `_drive_sync.sh` を呼ぶだけで、違いは「起動経路（草川直接投函 vs Notion DB承認 vs クラウドRoutine）」だけだったため、1スキル4モードに集約。草川は「取込」起点さえ覚えれば全モードに辿り着ける。

## このフォルダを残している理由
- 旧トリガー語「council-materials-intake」での参照が他ドキュメントに残るため
- スキル検索時に「あれ、消えた？」と迷わないため

将来的に本フォルダは削除予定。新しい運用は [drive-intake/SKILL.md](../drive-intake/SKILL.md) を参照。

## 関連MEMORY
- `project_drive_structure_v2.md` — Drive構造v2の設計
- `project_council_materials_management.md` — 旧議会資料管理システム設計

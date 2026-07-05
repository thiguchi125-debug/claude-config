---
name: project_ai_env_map_notion_embed
description: AI作業環境マップ（俯瞰インフォグラフィック）のNotionハブ埋め込みと更新手順
metadata: 
  node_type: memory
  type: project
  originSessionId: 13668352-49b9-4fa7-afd9-ab3c99ec7eb0
---

2026-07-05設置。スキル20+/エージェント54本/安全ゲート2/保存先3を1枚に整理した俯瞰インフォグラフィック「草川たくや Claude Code 作業環境マップ」を **🤖AI作業環境ハブ**（page `394cf503a68f81269d49d2015f39d7b4`・朝のダッシュボード配下）末尾に埋め込み表示。

- **表示方式**: PNG静止画ではなく **HTMLファイルをNotionにアップロード→`<embed src="file-upload://...">` でサンドボックス描画**（NotionはローカルPNGバイナリを直接受けられないため。HTML埋め込みの方が文字くっきり・差し替え可で上位互換）。
- **ライブリンク併記**: アーティファクト `https://claude.ai/code/artifact/75373ef6-a0e9-4580-8854-fed7e3a94749?via=auto_preview`（開くたび現行）。
- **ソース正本**: `~/outputs/ai-env-map/kusagawa_env_map.html`（＋PNG同梱）。編集→headless Chrome再レンダで画像も作れる。
- **自動更新はしない**（手作り俯瞰図＝ライブデータ源なし）。トリガー「**作業環境マップ更新して**」で：①ソースHTMLの数字/一覧を現行構成に更新 ②Artifactツールで同じアーティファクトURLへ再デプロイ ③`notion-create-attachment`でHTML再アップ→ハブページのembed差し替え（旧embedブロック置換）。
- スキル/エージェントを新設・廃止したら [[project_notion_reorg_2026-07-05]] のトリガー一覧2枚更新と合わせてこの地図も更新する。

---
name: feedback-agent-description-diet
description: 2026-07-05 agent大掃除の記録と、新規agent/skillのdescription 400字以内ルール（トークン固定費の再発防止）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 583575e3-84cb-478d-97d7-b9522e678718
---

**2026-07-05 agentレジストリ大掃除（草川承認済み）**：54本→44本、description総量 60,355字→16,234字（▲73%）＝毎ターン固定費 約7〜9Kトークン削減。

- **圧縮**: 52本のdescriptionを「役割1文＋Triggers全保持＋NOT境界」形式に統一。トリガー語は1語も削っていない。
- **統合1**: policy-expert 6本（子育て/DX/防災/医療/交通/まちづくり）→ `policy-domain-expert` 1本。知識は `~/.claude/agents/knowledge/policy_domains/` に全文保存、起動時に該当ドメインをRead。
- **統合2**: 実装系4本（財政試算/ロードマップ/ステークホルダー/公約パッケージング）→ `policy-strategy-suite` 1本。知識は `~/.claude/agents/knowledge/policy_strategy/`。**公約設計（7〜9月）時にpolicy-radar等へ自動配線予定**。
- **退役2本**: future-scenario-strategist（3本柱v0完了）／policy-compass-curator（コンパス完成済）→ `~/.claude/_retired_agents/`（原本12ファイル保管）。
- **残した0回agent**: 議会系（agenda-analyzer/bill-scrutiny×2/gikai-dayori/council-material=会期物）、スキル配線済み11本、design-inspiration-researcher（7/2作成の新品）、print-designer（スキル3本参照のため見送り）。

**Why:** agent新設が続くとdescriptionが毎ターンの固定コンテキストに積み上がる。6月〜7月の新設ラッシュで約6万字＝約20Kトークン/ターンに達していた。

**How to apply:**
1. **新規agent/skillのdescriptionは400字以内**（役割1文＋トリガー語＋NOT境界のみ。能力の詳細説明は本体に書く）。
2. 復元手段: `~/.claude/agents/_description_archive_2026-07-05.md`（原文全文）／GitHub claude-config `sync: 2026-07-05 17:10:38`（圧縮前）・`17:41:37`（完了後）／退役原本は `~/.claude/_retired_agents/`。
3. 旧policy-expert-*・旧実装系4本への参照を見たら、[[project-todoist-task-migration]]同様「統合先（policy-domain-expert / policy-strategy-suite）に読み替える」。

## 第2次ダイエット（2026-08-25）＋ YAMLの罠

400字ルールは決めただけで守られておらず、agent 14本・skill 16本が超過（超過合計3,870字）。重い上位10本を圧縮し **28,086字 → 25,183字（-2,903字/セッション）**。

**圧縮の原則**: descriptionの仕事は「いつ起動するか／しないか」のルーティングだけ。実装手順・保存先のNotion ID・ファイルパス・agent直列の内訳は**本文にあるのでdescriptionから落とす**。逆に Triggers と NOT は起動精度そのものなので削らない。

**⚠️ YAMLの罠（今回踏んだ）**: skillのdescriptionは無引用のプレーンスカラーで書かれている。そこへ `Triggers: ` のような**コロン＋スペース**を入れると YAML として不正になり `yaml.safe_load` が落ちる（ハーネスは寛容に読めてしまうので気づかない）。**descriptionを書き換えたら必ず `"` で囲む**。今回この不正は drive-intake / daily-content-generator に**以前から潜在していた**（自分の編集前から壊れていた）ので、編集後は全73本を `yaml.safe_load` で通して確認すること。

**残り**: policy-domain-expert(458字)・policy-strategy-suite(509字)は統合agentでトリガー網羅が要るため400字超のまま許容。未着手の超過は agent 12本・skill 14本（合計約1,000字）。

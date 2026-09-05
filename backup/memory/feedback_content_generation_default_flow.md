---
name: コンテンツ生成は常時lean fullーagentがデフォルト
description: ブログ・SNS・動画キャプション等の発信物生成依頼は、毎回主担当agent + lean最適化で起動する。トークン節約のためのagent省略は禁止。ユーザー明示指示なしに「直書き」「最小修正」へフォールバックしない。
type: feedback
originSessionId: f9ce7d72-d2c5-4789-9818-7a14186adaf8
---
# コンテンツ生成のデフォルトフロー

ブログ・SNS投稿・ショート動画キャプション・スピーチ・印刷物コピー等、草川名義の発信物を生成するすべての依頼で、主担当agent + lean最適化を**毎回**適用する。

**Why**:
- 2026-05-06、特別教室エアコン展開セット生成時に「トークン節約」を理由にagentをスキップして直書き → 一人称混在・フッター抜け（プレースホルダ放置）が発生 → やり直しで結局244K消費（最初から正しくやれば170K以下で済んだ）
- voice-dna整合・PF別声分け・5段構成・定型フッター完備は主担当agent経由でしか担保できない
- 「フル修正」「最小修正」という対立軸は誤り。lean fullがデフォルト、最小修正は緊急時のみ

**How to apply**:

## デフォルトフロー（毎回これ）

### Phase 0: main thread事前準備（1回のみ・約12〜15K）
- voice-dna.md コア抽出（一人称・定型フッター・3軸キーフレーズ）
- 元素材／source（Notion等）読込・主要ファクト箇条書き化
- **【必須・追加】議会質問アーカイブgrep**（CLAUDE.md「議会質問アーカイブ常時参照（必須）」準拠）：
  - `grep -rl "<トピックキーワード>" ~/.claude/agents/knowledge/kusagawa_archive/{01_council,02_publications,05_resources,06_election}/`
  - ヒットしたファイルから草川過去発言の関連箇所をmain側で**最低3件**抽出（年月・議会名・要求内容・市答弁の概略）
  - 「過去にこう質問してきた → 今回の決定はその答えとしてどう位置づくか」のナラティブ素材を作成
  - これがあると voice-dna軸2「繋ぐ思いを、形にする」が活き、草川の継続的政策追求の credibility が出る
- 各agent向け統一仕様確定（タイトル50字・5段構成・PF文字数・出力ファイルパス）
- これらを各agent promptに**直接埋込**（agentが自前で再fetchしない）

**Why Phase 0アーカイブgrepが特別に重要**:
- 2026-05-06、特別教室エアコンブログ初回生成時、私がblog-writerに「policy-researcher呼ばない・tool_uses 20回以内」と制約したため、blog-writerがアーカイブgrepステップをスキップ。結果、草川が令和6年12月議会・令和7年3月代表質問で「R11完了」を求めていた事実、そして今回の市決定（R9夏稼働）が**草川の要求より2年前倒し**である事実が、ブログから完全に欠落。
- 後追いでアーカイブgrepしたら、上記の決定的ナラティブが見つかった。Phase 0で先に grepしていればblog-writerが最初から織込めた。
- アーカイブgrepはmain側で5K以下で完了する。これをスキップするのは「節約」ではなく「品質を捨てる」だけ。

### Phase 1: 生成（並列・約75K）
- `blog-writer` または `blog-writer-normal`（埋込コンテキスト＋既知ファクト渡し）→ 約35K
- `sns-content-creator`（同上）→ 約40K
- 短尺動画は `short-video-virality-architect`（必要時）

### Phase 2: 安全ゲート（直列・約25〜55K）
- `content-fact-checker`：upstream済（元素材で実施済）なら派生新規数値のみ検証 → 0〜30K
- `content-risk-reviewer`：事前判明懸念点リスト渡し（8軸全スキャンではなく重点軸） → 約25K

### Phase 3: Notion保存（約30K）
- main側でDB ID・properties JSON・本文blocks完成形を組立
- `notion-saver` に丸ごと渡す（探索作業させない）→ create-pages + mention設定のみで完了

**目標値**:
- fact-check含む：130〜170K
- fact-check skip可能（upstream済）：90〜130K

## 5つの節約レバー（毎回適用）

| レバー | 効果 | 適用方法 |
|---|---|---|
| A. context事前埋込 | -30〜50K | voice-dna/source/方針をmain側で1回読みprompt直書き |
| B. fact-check upstream-only | -40〜60K | 元素材でfact-check済なら派生物はskip、新数値混入時のみリトライ |
| C. notion-saver完成形渡し | -30〜40K | DB ID/schema/properties/blocksをmain側で組立 |
| D. risk-reviewer重点軸指定 | -15〜20K | 事前判明懸念点リストを prompt に明記 |
| E. agent統一仕様事前指定 | -10〜15K | 文字数・構成・出力フォーマットをmain側で確定 |

## 禁止事項

- ❌ 「トークン節約のためagent省略して直書き」（独断）
- ❌ 「最小修正で済ませる」をデフォルト提案にする
- ❌ 「フル修正」「軽量版」と対立軸でユーザーに選択させる（lean fullが常時デフォルト）
- ❌ agent促されてからlean最適化を提案する（最初から適用）

## 例外（ユーザー明示指示時のみ）

- 「軽くやって」「ざっくりでいい」「直書きで」→ 主担当agent省略可
- 「ファクトチェック不要」→ fact-checker skip
- 「リスクレビュー不要」→ risk-reviewer skip（ただしHIGH懸念があれば草川に確認）
- 上記いずれの場合も、何をskipしたかを実行前に明言する

## 関連

- CLAUDE.md「発信物の安全ゲート（必須）」 — fact-check + risk-review は明文必須
- agents/blog-writer.md 📌節「モードA/B判定」（旧 feedback_blog_citizen_first）
- D1〜D5原則（CLAUDE.md「ブログ作成の省力フロー」） — 完全保管・承認後保存・タイトル50字・PDF扱い・スコープ厳守

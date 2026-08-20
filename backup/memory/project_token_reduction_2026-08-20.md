---
name: project-token-reduction-2026-08-20
description: 2026-08-20のトークン削減作業。真因は印刷物デザインループの画像積み上げで、スキルの多さではなかった
metadata: 
  node_type: memory
  type: project
  originSessionId: 7a34af0c-0fd2-4656-9797-2d60b17ff192
  modified: 2026-08-20T12:57:25.006Z
---

2026-08-20 に「トークン消費が激しすぎる」を実測から詰めた作業。直近14日 4,455Mトークン / 17,735呼び出し / 149セッション。

**真因はスキル・エージェントの多さではなく、印刷物デザインループを親セッションで回していたこと。**
重いセッション上位4本のうち3本が印刷物制作で、ed309187(8/10)=画像147枚/446.8M、619d05d7(8/16)=110枚/229.8M、47f93789(8/07)=98枚/518.6M。画像1枚≒1,500トークンがセッション終了まで居座り、147枚≒220Kが757回の呼び出し全部に再送されていた。CLAUDE.mdに「画像を伴う反復作業はサブエージェントへ隔離」と書いてあるが機械的に強制されておらず守られていなかった。`image_reread_guard.py` は mtime+size 同一のときだけ deny する仕様なので、再レンダのたびに mtime が動くデザインループには効かない。

**入れた対策**
- `~/.claude/hooks/image_budget_guard.py`（新規・settings.json の PreToolUse:Read に登録）— セッション累計の画像Readを数え 10枚警告 / 18枚警告 / 25枚 deny。詰まったら `rm ~/.claude/hooks/state/<sid>.imgcount` で解除できる旨をメッセージに明記してある
- `context_budget_notice.py` の閾値を 200/350/500/700K → **120/200/300K** に前倒し。文面に「この先100回で+NM」と保存→/clear の手順を入れた
- `~/.claude/scripts/mode.sh` 新設 — council(議会9本) / election(選挙・演説3本) を `~/.claude/_agents_off/` へ出し入れする。**作っただけで、まだ off にしていない**（9月議会が近く戻し忘れリスクが削減効果6%を上回るため）
- `~/.claude/agents/.claude/agent-memory/` の誤配置6本を `~/.claude/agent-memory/` へ移設（agent定義として起動時に載っていた）
- daily-content-generator の description 1,177→579字（トリガー語・NOT節は全保持）

**起動時固定費の内訳**（中央値74.5K・全呼び出しに毎回乗る＝全体の約30%）: agents 46本 16,563字 / skills 25本 12,121字 / MEMORY.md 9,083字 / CLAUDE.md 6,023字。**description圧縮は2026-07-05に実施済み**（原文79,557字→16,563字）で余地は小さい。対照表は `~/.claude/agents/_description_compress_proposal_2026-07-05.md`、原文は同 `_description_archive_2026-07-05.md`。

バックアップは全て `~/Archive/_trash_pending_2026-08-20_agent_memory_fix/`。

効果測定は `python3 ~/.claude/scripts/token_report.py 14`（第2引数に `MM-DD` で対策前後の比較）。

関連: [[feedback-startup-context-is-30-percent-of-cost]] [[project-stalled-automation-revival-2026-08-20]]

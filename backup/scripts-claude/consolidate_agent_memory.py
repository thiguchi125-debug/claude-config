#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""入れ子 .claude/agent-memory を正本 ~/.claude/agent-memory へ統合して入れ子を消す。

真因: サブエージェントが cwd をホーム以外にして走ると、その cwd に
      .claude/agent-memory/<agent>/ が作られ、同じagentの記憶が分裂する。
      分裂した .md は agent として誤登録され、起動時の文脈も食う。
      2026-08-20 に手作業で直したが 5日で再発したため常設化した。
使い方: python3 consolidate_agent_memory.py [--dry-run]
"""
import os, sys, shutil, hashlib

HOME = os.path.expanduser('~')
ROOT = os.path.join(HOME, '.claude')
CANON = os.path.join(ROOT, 'agent-memory')
DRY = '--dry-run' in sys.argv

def sha(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def find_nested():
    out = []
    for root, dirs, _ in os.walk(ROOT):
        if os.path.basename(root) == '.claude' and root != ROOT:
            out.append(root)
            dirs[:] = []
    return out

def main():
    nested = find_nested()
    if not nested:
        print('nested .claude: none'); return 0
    merged = dup = conflict = idx = 0
    for nd in nested:
        am = os.path.join(nd, 'agent-memory')
        if os.path.isdir(am):
            for agent in sorted(os.listdir(am)):
                sdir = os.path.join(am, agent)
                if not os.path.isdir(sdir):
                    continue
                ddir = os.path.join(CANON, agent)
                if not DRY:
                    os.makedirs(ddir, exist_ok=True)
                for f in sorted(os.listdir(sdir)):
                    if not f.endswith('.md'):
                        continue
                    s, d = os.path.join(sdir, f), os.path.join(ddir, f)
                    if f == 'MEMORY.md':
                        # 索引は行単位ユニオンで追記（既存行は保持）
                        cur = open(d, encoding='utf-8').read() if os.path.exists(d) else '# Memory Index\n'
                        have = {l.strip() for l in cur.splitlines() if l.strip()}
                        add = [l.rstrip('\n') for l in open(s, encoding='utf-8')
                               if l.strip().startswith('- ') and l.strip() not in have]
                        if add and not DRY:
                            open(d, 'w', encoding='utf-8').write(
                                cur.rstrip('\n') + '\n' + '\n'.join(add) + '\n')
                        idx += len(add)
                    elif not os.path.exists(d):
                        if not DRY:
                            shutil.copy2(s, d)
                        merged += 1
                    elif sha(s) == sha(d):
                        dup += 1
                    else:
                        alt = d[:-3] + '__nested.md'
                        if not os.path.exists(alt):
                            if not DRY:
                                shutil.copy2(s, alt)
                            conflict += 1
                        else:
                            dup += 1
        if not DRY:
            shutil.rmtree(nd)
    tag = '[dry-run] ' if DRY else ''
    print('%s入れ子.claude %d箇所を統合: 新規%d / 重複%d / 差異%d / 索引追記%d行'
          % (tag, len(nested), merged, dup, conflict, idx))
    return 0

if __name__ == '__main__':
    sys.exit(main())

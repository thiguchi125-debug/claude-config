# -*- coding: utf-8 -*-
import os
"""議場カード v8 を「読む束/返す束/封じ手・出典束」へ機械分割する。
本文は1文字も書き換えない。行を仕分けるだけ。"""
import io,glob,os,re,sys
D=os.path.abspath(sys.argv[1]) if len(sys.argv)>1 else os.getcwd()
os.chdir(D)
A,B,C=[],[],[]   # 読む / 返す / 封じ手・出典
files=sorted(glob.glob('カード[1-6]*_v8.md'))
for f in files:
    lines=io.open(f,encoding='utf-8').read().split('\n')
    title=lines[0]
    for L in (A,B,C): L.append('\n---\n\n'+title+'\n')
    sec=''
    for i,L in enumerate(lines[1:]):
        s=L.strip()
        if s.startswith('# '): continue
        if s.startswith('## '):
            sec=s
            if '引き出す数字' in s: B.append(''); B.append(L); continue
            if '言わないこと' in s: C.append(''); C.append(L); continue
            for X in (A,B,C): X.append(''); X.append(L)
            continue
        if '引き出す数字' in sec: B.append(L); continue
        if '言わないこと' in sec: C.append(L); continue
        if not s: continue
        body=s[2:].lstrip() if s.startswith('> ') else s
        if s.startswith('> ') and not body.startswith(('🔒','#注記')):
            A.append(L); A.append(''); continue
        if '🔒' in s:
            C.append(L)
            m=re.match(r'\*\*(★[^*]{0,40}?)\*\*', s)
            if m: A.append('🔸〔条件付き：%s〕── 読まない。使うときだけC束を見る' % m.group(1)); A.append('')
            continue
        if s.startswith(('✅','⚠️','📎','|','　URL','📌')):
            C.append(L); continue
        if s.startswith('**想定答弁→返し**') or s.startswith('- 「') or s.startswith('**返し（1行）**') or s.startswith('**引き出す約束**'):
            B.append(L); continue
        if s.startswith('**答弁者**') or s.startswith('**★') or s.startswith('**本問**') or s.startswith('- **'):
            A.append(L); A.append(''); continue
        if s.startswith('**読み上げ') or s.startswith('**通告'):
            C.append(L); continue
        C.append(L)
def prune(X):
    out=[]
    for i,L in enumerate(X):
        if L.startswith('## '):
            j=i+1; empty=True
            while j<len(X) and not X[j].startswith(('## ','# ','---')):
                if X[j].strip(): empty=False; break
                j+=1
            if empty: continue
        out.append(L)
    return out
A=prune(A)
HDR=('# {}　── 令和8年9月定例会 一般質問（草川たくや）\n\n'
     '**{}**\n\n取扱い：議場メモ・手元限定（内部文書）\n')
io.open('_本番束/A_読む束_v8.md','w',encoding='utf-8').write(
  HDR.format('A｜読む束','登壇中はこの束だけを見る。ここに書いてある「> 」の行を、書いてあるとおりに読む。')+ '\n'.join(A))
io.open('_本番束/B_返す束_v8.md','w',encoding='utf-8').write(
  HDR.format('B｜返す束','着席して答弁を聞きながら開く。左が想定答弁、右が返し。★返しは全体で2回まで（1回0.9分）。')+ '\n'.join(B))
io.open('_本番束/C_封じ手・出典束_v8.md','w',encoding='utf-8').write(
  HDR.format('C｜封じ手・出典束','机の端に伏せておく控え。🔒＝言い方と条件付き原稿／✅⚠️＝出典と未確認／言わないこと。')+ '\n'.join(C))
for n in ('A_読む束','B_返す束','C_封じ手・出典束'):
    p=f'_本番束/{n}_v8.md'; print(n, len(io.open(p,encoding='utf-8').read()), '字')

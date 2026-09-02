#!/usr/bin/env python3
"""pool.py — POOL.json manager for feature-lane-runner v2.1
Usage:
  python pool.py summary [POOL.json]
  python pool.py ready   [POOL.json]
  python pool.py plan W1 [--names "หนังสือรับรอง,ESS Portal"] [--lanes 3] [--pool POOL.json] [--out briefs/W1/CHECKLIST.md]
  python pool.py check W1 [--pool POOL.json] [--checklist briefs/W1/CHECKLIST.md]
  python pool.py set "<feature name>" <status> [--run W1] [--reason "..."]   # status: todo|picked|running|done|blocked|skipped
"""
import sys, json, re, os, argparse, collections, datetime
DONE=('done','ba-done')
def load(p):
    b=json.load(open(p,encoding='utf-8')); return b
def save(p,b): json.dump(b,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
def find(b,name):
    n=name.strip().lower()
    for f in b['features']:
        if f['name'].lower()==n or (f.get('name_th') or '').lower()==n or f.get('id','').lower()==n: return f
    for f in b['features']:
        if n in f['name'].lower() or n in (f.get('name_th') or '').lower(): return f
    return None
def dep_names(f):
    d=f.get('depends_on') or ''
    return [x.strip() for x in re.split(r'[·,/]|\bรอ:',d) if x.strip() and len(x.strip())>2]
def dep_ok(b,f):
    missing=[]
    for dn in dep_names(f):
        t=find(b,dn)
        if t and t['status'] not in DONE: missing.append(t['name'])
    return missing
def decl(f): return [k for k,v in f['declarations'].items() if v]
def summary(b):
    c=collections.Counter(); w=collections.defaultdict(collections.Counter)
    for f in b['features']:
        c[f['status']]+=1; w[f['wave']][f['status']]+=1
    print(f"POOL {b.get('total',len(b['features']))} features · "+' · '.join(f"{k}={v}" for k,v in c.items()))
    for k in sorted(w): print(f"  {k:5} "+' · '.join(f"{s}={n}" for s,n in w[k].items()))
def ready(b):
    rows=[f for f in b['features'] if f['status'] in ('todo','picked') and not dep_ok(b,f)]
    for f in rows: print(f"{f['wave']:4} {f['module']:18} {f['name']:34} {f['archetype_guess']:14} {' '.join(decl(f))}")
    print(f"\n{len(rows)} ready")
def plan(b,wave,names,lanes,out):
    feats=[f for f in b['features'] if f['wave']==wave and f['status']!='done'] if not names else [find(b,n) for n in names]
    feats=[f for f in feats if f]
    lines=[f"# WAVE {wave} — CHECKLIST  (gen {datetime.date.today()} · pool {b.get('generated','')} · แก้ ✔ / scope note ได้ตามใจ)",
           "run_mode: full","parallel: %d"%lanes,"stop_on: never","",
           "| ✔ | Feature | Module | Archetype | Declarations | Wave | Lane | Dep (สถานะ) | Scope note / OQ ตอบล่วงหน้า |",
           "|---|---|---|---|---|---|---|---|---|"]
    L='ABC'
    for i,f in enumerate(feats):
        miss=dep_ok(b,f); tick='[ ]' if miss else '[x]'
        depstr=('⛔ รอ: '+', '.join(miss)) if miss else ('✅ '+(f.get('depends_on') or '—')[:40])
        lines.append(f"| {tick} | {f['name']} | {f['module']} | {f['archetype_guess']} | {' · '.join(decl(f)) or '—'} | {f['wave']} | {L[i%lanes]} | {depstr} | |")
    lines+=["","> ✔ = ทำรอบนี้ · dep ⛔ ถูกยกเลิกติ๊กให้แล้ว · Lane A/B/C = session ขนาน · scope note = ที่เดียวที่ใส่เจตนา/ตอบ OQ (ยิ่งเขียน block ยิ่งน้อย)"]
    os.makedirs(os.path.dirname(out) or '.',exist_ok=True); open(out,'w',encoding='utf-8').write('\n'.join(lines))
    for f in feats: f['status']='picked'; f['run_id']=wave
    print(f"wrote {out} ({len(feats)} features)")
def parse_checklist(path):
    rows=[]
    for line in open(path,encoding='utf-8'):
        m=re.match(r'\|\s*\[(x|X| )\]\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|',line)
        if m: rows.append(dict(on=m.group(1).lower()=='x',name=m.group(2),module=m.group(3),arch=m.group(4),decl=m.group(5),wave=m.group(6),lane=m.group(7),dep=m.group(8),note=m.group(9)))
    return rows
def check(b,wave,path):
    rows=parse_checklist(path); ok=True; seen={}
    print(f"CHECK {path}: {sum(r['on'] for r in rows)} ✔ / {len(rows)} rows")
    for r in rows:
        if not r['on']: continue
        f=find(b,r['name']); tag='PASS'; why=[]
        if not f: tag='FAIL'; why.append('ไม่มีใน POOL')
        else:
            if f['status']=='done': tag='FAIL'; why.append('done แล้ว')
            miss=dep_ok(b,f)
            if miss: tag='FAIL'; why.append('dep ยังไม่เสร็จ: '+', '.join(miss))
            if f['name'] in seen: tag='FAIL'; why.append('ซ้ำ lane '+seen[f['name']])
            seen[f['name']]=r['lane']
            if not r['note'].strip() and ('doa' in r['decl'] or 'csq' in r['decl']): why.append('WARN: ไม่มี scope note ทั้งที่มี doa/csq — OQ จะกลายเป็น [ASSUMED]')
        if tag=='FAIL': ok=False
        print(f"  {tag:4} {r['name']:34} {' · '.join(why)}")
    print('RESULT:', 'PASS — รันได้' if ok else 'FAIL — แก้ checklist ก่อน')
    return ok
if __name__=='__main__':
    a=sys.argv[1:]
    if not a: print(__doc__); sys.exit(2)
    cmd=a[0]; ap=argparse.ArgumentParser(); ap.add_argument('rest',nargs='*'); ap.add_argument('--pool',default='POOL.json'); ap.add_argument('--names'); ap.add_argument('--lanes',type=int,default=3); ap.add_argument('--out'); ap.add_argument('--checklist'); ap.add_argument('--run'); ap.add_argument('--reason',default='')
    ns=ap.parse_args(a[1:]); b=load(ns.pool)
    if cmd=='summary': summary(b)
    elif cmd=='ready': ready(b)
    elif cmd=='plan':
        w=ns.rest[0]; plan(b,w,[x.strip() for x in ns.names.split(',')] if ns.names else None,ns.lanes,ns.out or f'briefs/{w}/CHECKLIST.md'); save(ns.pool,b)
    elif cmd=='check':
        w=ns.rest[0]; sys.exit(0 if check(b,w,ns.checklist or f'briefs/{w}/CHECKLIST.md') else 1)
    elif cmd=='set':
        f=find(b,ns.rest[0]); assert f, 'not found'; f['status']=ns.rest[1]; f['run_id']=ns.run or f.get('run_id'); f['blocked_reason']=ns.reason; save(ns.pool,b); print('set',f['name'],f['status'])

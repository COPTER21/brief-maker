#!/usr/bin/env python3
"""decl_rule.py — decide which declarations to run for a feature (S1.8) → _DECL.json
Usage: python decl_rule.py <brief_dir> [--pool POOL.json] [--name "feature name"]   # brief_dir = briefs/W1/F-xxx
Reads 0_SOURCE/LANE_BRIEF.md (chips) + 0_SOURCE/PREBRIEF.md §12 (AUTHORITATIVE) · keyword hints from prebrief_checklist.py are advisory only (never set need)
Output: _lane/DECL.json
"""
import sys, json, re, os, subprocess, glob
d=sys.argv[1]; pool=None; name=None
if '--pool' in sys.argv: pool=sys.argv[sys.argv.index('--pool')+1]
if '--name' in sys.argv: name=sys.argv[sys.argv.index('--name')+1]
PIPES=['doa','ntf','csq','doccfg','pdfdoc']
SKILL={'doa':'doa-declaration','ntf':'ntf-declaration','csq':'csq-declaration','doccfg':'doccfg-declaration','pdfdoc':'thai-doc-pdf-generator'}
OUT={'doa':'5_DECLARATIONS/DOA_BRIEF.md','ntf':'5_DECLARATIONS/NTF_BRIEF.md','csq':'5_DECLARATIONS/CSQ_BRIEF.md','doccfg':'5_DECLARATIONS/DOCCFG_BRIEF.md','pdfdoc':'5_DECLARATIONS/PDFDOC/'}   # relative to output dir
chip={p:False for p in PIPES}
def first(*c):
    for x in c:
        if os.path.exists(x): return x
bf=first(os.path.join(d,'LANE_BRIEF.md'),os.path.join(d,'0_SOURCE','LANE_BRIEF.md'),os.path.join(d,'00_LANE_BRIEF.md'))
brief=open(bf,encoding='utf-8').read() if bf else ''
for p in PIPES:
    m=re.search(r'\|\s*'+{'doa':'DOA','ntf':'NTF','csq':'CSQ','doccfg':'DOCCFG','pdfdoc':'PDF DOC'}[p]+r'\s*\|\s*(✓|—|-)',brief)
    if m: chip[p]= m.group(1)=='✓'
if pool and name:
    b=json.load(open(pool,encoding='utf-8'))
    for f in b['features']:
        if f['name']==name: chip.update({k:bool(v) for k,v in f['declarations'].items() if k in chip})
# detect from prebrief via shared script
det={p:None for p in PIPES}; arch=''
pb=first(os.path.join(d,'PREBRIEF.md'),os.path.join(d,'0_SOURCE','PREBRIEF.md'),os.path.join(d,'01_PREBRIEF.md')) or ''; fc=glob.glob(os.path.join(d,'FUNCTION_CHECKLIST*.md'))+glob.glob(os.path.join(d,'0_SOURCE','FUNCTION_CHECKLIST*.md'))+glob.glob(os.path.join(d,'01_FUNCTION_CHECKLIST*.md'))
hint={p:None for p in PIPES}
if pb and os.path.exists(pb):
    t=open(pb,encoding='utf-8').read()
    m=re.search(r'archetype_confirmed:\s*([\w-]+)',t); arch=m.group(1) if m else ''
    # §12 table
    for p,lab in {'doa':'DOA','ntf':'NTF','csq':'CSQ','doccfg':'DOCCFG','pdfdoc':'PDF DOC'}.items():
        m=re.search(r'\|\s*'+lab+r'\s*\|[^|]*\|[^|]*\|\s*(need|no|DIVERGENCE)',t,re.I)
        if m: det[p]= m.group(1).lower()!='no'
    script=glob.glob('/mnt/skills/user/qc-coverage-checker/scripts/prebrief_checklist.py')
    if fc and script and any(v is None for v in det.values()):
        try:
            out=json.loads(subprocess.check_output([sys.executable,script[0],fc[0],pb],text=True))
            for p in ['doa','ntf','csq','doccfg']:
                hint[p]=out['declarations'].get(p,False)   # advisory only
        except Exception as e: print('warn: prebrief_checklist failed',e,file=sys.stderr)
    if det['pdfdoc'] is None and arch.startswith('Q'): det['pdfdoc']=True   # Q archetype ⇒ pdf doc
st=os.path.join(d,'_lane','LANE_STATE.json'); outdir=json.load(open(st,encoding='utf-8')).get('out_dir','') if os.path.exists(st) else ''
res={'archetype':arch,'out_dir':outdir,'pipes':{}}; div=[]
for p in PIPES:
    if det[p] is not None: need=bool(det[p]); src='prebrief§12'
    else: need=bool(chip[p]); src='chip'
    if det[p] is not None and det[p]!=chip[p]: div.append(f"{p}: chip={'✓' if chip[p] else '—'} PREBRIEF§12={'✓' if det[p] else '—'} → รันตาม §12")
    if hint.get(p) and not need: div.append(f"{p}: keyword hint พบสัญญาณใน PREBRIEF แต่ §12/chip = ไม่ต้อง → ตรวจดู (hint only)")
    res['pipes'][p]={'need':need,'chip':chip[p],'detect':det[p],'hint':hint.get(p),'source':src,'skill':SKILL[p],'output':OUT[p]}
res['divergence']=div
os.makedirs(os.path.join(d,'_lane'),exist_ok=True); json.dump(res,open(os.path.join(d,'_lane','DECL.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(json.dumps(res,ensure_ascii=False,indent=1))

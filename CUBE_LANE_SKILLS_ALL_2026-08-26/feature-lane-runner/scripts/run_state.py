#!/usr/bin/env python3
"""run_state.py — lane/wave state (resumable)
Usage:
  python run_state.py init <brief_dir> <feature_name> <wave> --out <output_dir> [--lane A]   # brief_dir = briefs/W1/F-xxx · output_dir = output/YYYY-MM-DD/F-xxx_ชื่อ
  python run_state.py set  <feature_dir> <stage> <status> [--note "..."] [--retry]     # status: pass|warn|block|skip|running
  python run_state.py next <feature_dir>                                              # print next stage to run
  python run_state.py wave <brief_wave_dir>                                            # aggregate briefs/W1/*/_lane/LANE_STATE.json → briefs/W1/_RUN_STATE.json
"""
import sys, json, os, glob, datetime
STAGES=['S0','S0.5','S1','S1.5','S1.8','S2','S3a','S3b','S3c','S4','S5','S6','S6.5','S7','S8','S9']
CAP={'S1':2,'S3a':3,'S3b':3,'S3c':2,'S4':2,'S5':2,'S6.5':2}; CAP_TOTAL=10
def p(d):
    os.makedirs(os.path.join(d,'_lane'),exist_ok=True); return os.path.join(d,'_lane','LANE_STATE.json')
def now(): return datetime.datetime.now().isoformat(timespec='seconds')
cmd=sys.argv[1]; args=sys.argv[2:]
if cmd=='init':
    d,name,wave=args[:3]; lane=args[args.index('--lane')+1] if '--lane' in args else ''
    out=args[args.index('--out')+1] if '--out' in args else ''
    os.makedirs(d,exist_ok=True)
    if out:
        for sub in ['1_HTML','2_BRD','3_FRD','4_TC','5_DECLARATIONS']: os.makedirs(os.path.join(out,sub),exist_ok=True)
    s={'feature':name,'wave':wave,'lane':lane,'brief_dir':os.path.abspath(d),'out_dir':os.path.abspath(out) if out else '','status':'running','created':now(),'stages':{k:{'status':'pending','retries':0} for k in STAGES},'total_retries':0,'assumed':[],'divergence':[],'log':[]}
    json.dump(s,open(p(d),'w',encoding='utf-8'),ensure_ascii=False,indent=1); print('init',name)
elif cmd=='set':
    d,st,status=args[:3]; s=json.load(open(p(d),encoding='utf-8')); note=args[args.index('--note')+1] if '--note' in args else ''
    e=s['stages'][st]; 
    if '--retry' in args: e['retries']+=1; s['total_retries']+=1
    e['status']=status; e['at']=now(); 
    if note: e['note']=note
    s['log'].append({'at':now(),'stage':st,'status':status,'note':note})
    if status=='block' and (e['retries']>=CAP.get(st,1) or s['total_retries']>=CAP_TOTAL): s['status']='blocked'; s['blocked_at']=st
    elif status=='skip': s['status']='skipped'
    elif st=='S9' and status in('pass','warn'): s['status']='done'
    json.dump(s,open(p(d),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    with open(os.path.join(d,'_lane','LANE_LOG.md'),'a',encoding='utf-8') as f: f.write(f"- {now()} · {st} · {status} · retries={e['retries']} · {note}\n")
    print(st,status,'→',s['status'])
elif cmd=='next':
    s=json.load(open(p(args[0]),encoding='utf-8'))
    if s['status'] in('blocked','done','skipped'): print(s['status']); sys.exit(0)
    for k in STAGES:
        if s['stages'][k]['status'] not in('pass','warn'): print(k); break
elif cmd=='wave':
    wd=args[0]; wave=os.path.basename(wd.rstrip('/')); feats=[]
    for f in glob.glob(os.path.join(wd,'*','_lane','LANE_STATE.json'))+glob.glob('features/*/_lane/LANE_STATE.json'):
        s=json.load(open(f,encoding='utf-8'))
        if s.get('wave')==wave: feats.append({'feature':s['feature'],'lane':s.get('lane'),'status':s['status'],'blocked_at':s.get('blocked_at'),'total_retries':s['total_retries'],'dir':os.path.abspath(os.path.dirname(os.path.dirname(f))),'out_dir':s.get('out_dir','')})
    seen=set(); feats=[x for x in feats if not (x['dir'] in seen or seen.add(x['dir']))]
    r={'wave':wave,'updated':now(),'features':feats,'counts':{k:sum(1 for x in feats if x['status']==k) for k in('done','running','blocked','skipped')}}
    os.makedirs(wd,exist_ok=True); json.dump(r,open(os.path.join(wd,'_RUN_STATE.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1); print(json.dumps(r['counts']))

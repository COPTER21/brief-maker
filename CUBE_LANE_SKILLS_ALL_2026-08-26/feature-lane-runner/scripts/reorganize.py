#!/usr/bin/env python3
"""reorganize.py — convert older lane output (v2.1.0 flat · v2.1.1 0_SOURCE/1_HTML…) → v2.3 (briefs/<W>/<F> + output/<date>/<F>_<ชื่อ>)
Usage: python reorganize.py <old_feature_dir> --wave W1 --date 2026-08-26 [--name "ชื่อไทย"] [--root .] [--dry]
"""
import sys, os, shutil, glob, re, json, argparse
ap=argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('--wave',required=True); ap.add_argument('--date',required=True); ap.add_argument('--name',default=''); ap.add_argument('--root',default='.'); ap.add_argument('--dry',action='store_true')
a=ap.parse_args(); src=a.src.rstrip('/'); fcode=os.path.basename(src).split('_')[0]; name=a.name or ('_'.join(os.path.basename(src).split('_')[1:]) or fcode)
B=os.path.join(a.root,'briefs',a.wave,fcode); O=os.path.join(a.root,'output',a.date,f"{fcode}_{name}"); L=os.path.join(B,'_lane'); Q=os.path.join(L,'QC')
def mv(s,d):
    if not os.path.exists(s): return
    print(('DRY ' if a.dry else '')+f"{os.path.relpath(s)} → {os.path.relpath(d)}")
    if a.dry: return
    os.makedirs(os.path.dirname(d),exist_ok=True)
    if os.path.isdir(s) and os.path.isdir(d):
        for x in os.listdir(s): shutil.move(os.path.join(s,x),os.path.join(d,x))
        os.rmdir(s)
    else: shutil.move(s,d)
J=lambda *p: os.path.join(src,*p)
# --- brief side ---
for old,new in [('0_SOURCE/LANE_BRIEF.md','LANE_BRIEF.md'),('00_LANE_BRIEF.md','LANE_BRIEF.md'),('0_SOURCE/_VALIDATION.md','_VALIDATION.md'),('_VALIDATION.md','_VALIDATION.md'),
 ('0_SOURCE/STANDARD_BASELINE.md','STANDARD_BASELINE.md'),('0_SOURCE/PREBRIEF.md','PREBRIEF.md'),('01_PREBRIEF.md','PREBRIEF.md'),
 ('0_SOURCE/FUNCTION_CHECKLIST.md','FUNCTION_CHECKLIST.md'),('01_FUNCTION_CHECKLIST.md','FUNCTION_CHECKLIST.md'),('0_SOURCE/FUNCTION_CHECKLIST.html','FUNCTION_CHECKLIST.html'),('01_FUNCTION_CHECKLIST.html','FUNCTION_CHECKLIST.html'),
 ('0_SOURCE/STANDARD_GAP.md','STANDARD_GAP.md'),('02_STANDARD_GAP.md','STANDARD_GAP.md')]:
    mv(J(old),os.path.join(B,new))
for old,new in [('_lane','.'),('_LANE_STATE.json','LANE_STATE.json'),('_LANE_LOG.md','LANE_LOG.md'),('_DECL.json','DECL.json'),('_MANIFEST.json','MANIFEST.json'),('_OP_MANIFEST.json','OP_MANIFEST.json'),('REGISTRY_PATCH.md','REGISTRY_PATCH.md'),('_NOTIFY.md','_NOTIFY.md'),('_BLOCKED.md','BLOCKED.md')]:
    mv(J(old),L if new=='.' else os.path.join(L,new))
# QC → _lane/QC
for g in [J('1_HTML','QC'),J('11_GATES')]:
    if os.path.isdir(g):
        for x in os.listdir(g):
            n={'_AUDIT_SH.txt':'audit.txt','_UX_CHECK_REPORT.md':'UX_CHECK_REPORT.md','_COVERAGE_R1.md':'COVERAGE_R1.md','_COVERAGE_R2.md':'COVERAGE_R2.md','_shots':'shots','_RENDER.json':'RENDER.json'}.get(x,x.lstrip('_'))
            mv(os.path.join(g,x),os.path.join(Q,n))
        if not a.dry and os.path.isdir(g) and not os.listdir(g): os.rmdir(g)
for c in [J('4_TC','COVERAGE_R2.md'),J('_COVERAGE_R2.md')]: mv(c,os.path.join(Q,'COVERAGE_R2.md'))
for w in [J('4_TC','_work'),J('22_TC','_work')]: mv(w,os.path.join(L,'TC_work'))
# --- output side ---
for h in glob.glob(J('1_HTML','*.html'))+glob.glob(J('10_HTML','*.html'))+glob.glob(J('10_*.html')):
    mv(h,os.path.join(O,'1_HTML',re.sub(r'^10_','',os.path.basename(h))))
for b in glob.glob(J('2_BRD','*'))+glob.glob(J('20_BRD','*'))+glob.glob(J('20_BRD*.*')): mv(b,os.path.join(O,'2_BRD',re.sub(r'^20_','',os.path.basename(b))))
for f in glob.glob(J('3_FRD','*'))+glob.glob(J('21_FRD_Pack','*'))+glob.glob(J('23_UI_BRIEF','*'))+glob.glob(J('22_UI_BRIEF*.md')): mv(f,os.path.join(O,'3_FRD',re.sub(r'^22_','',os.path.basename(f))))
work={'cases.json','shot-spec.json','shots_b64.json','shots_b64.report.json','_qa_shots'}
for t in glob.glob(J('4_TC','*'))+glob.glob(J('22_TC','*'))+glob.glob(J('3[012]_*')):
    n=re.sub(r'^3[012]_','',os.path.basename(t))
    if n=='COVERAGE_R2.md': continue
    mv(t,os.path.join(L,'TC_work',n) if n in work else os.path.join(O,'4_TC',n))
# declarations → 5_DECLARATIONS (need only) · NOT-NEEDED merged
nn=[]
for src_d in [J('0_SOURCE','declarations'),src]:
    for f in glob.glob(os.path.join(src_d,'*_BRIEF.md'))+glob.glob(os.path.join(src_d,'03_*_BRIEF.md')):
        pipe=re.sub(r'^03_|_BRIEF\.md$','',os.path.basename(f)); t=open(f,encoding='utf-8',errors='ignore').read()
        if re.search(r'NOT[-_ ]NEEDED',t[:400]): nn.append(f'## {pipe}\n'+t.strip()+'\n'); print(f'{os.path.basename(f)} → NOT_NEEDED.md');  a.dry or os.remove(f)
        else: mv(f,os.path.join(O,'5_DECLARATIONS',f'{pipe}_BRIEF.md'))
    mv(os.path.join(src_d,'PDFDOC'),os.path.join(O,'5_DECLARATIONS','PDFDOC')); mv(os.path.join(src_d,'03_PDFDOC'),os.path.join(O,'5_DECLARATIONS','PDFDOC'))
    mv(os.path.join(src_d,'NOT_NEEDED.md'),os.path.join(O,'5_DECLARATIONS','NOT_NEEDED.md'))
if nn and not a.dry:
    os.makedirs(os.path.join(O,'5_DECLARATIONS'),exist_ok=True)
    with open(os.path.join(O,'5_DECLARATIONS','NOT_NEEDED.md'),'a',encoding='utf-8') as f: f.write('# Declarations NOT NEEDED\n\n'+'\n'.join(nn))
ps=os.path.join(O,'5_DECLARATIONS','PDFDOC','print-spec.md')
if os.path.exists(ps) and not a.dry: shutil.copy(ps,os.path.join(O,'3_FRD','PRINT_SPEC.md'))
for z in glob.glob(J('*_DevPack.zip')): print('remove',z); a.dry or os.remove(z)
# update state out_dir
st=os.path.join(L,'LANE_STATE.json')
if os.path.exists(st) and not a.dry:
    s=json.load(open(st,encoding='utf-8')); s['brief_dir']=os.path.abspath(B); s['out_dir']=os.path.abspath(O); json.dump(s,open(st,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
# cleanup empty
if not a.dry:
    for root,dirs,files in os.walk(src,topdown=False):
        for dd in dirs:
            p=os.path.join(root,dd)
            if not os.listdir(p): os.rmdir(p)
    if os.path.isdir(src) and not os.listdir(src): os.rmdir(src)
    elif os.path.isdir(src): print('เหลือใน', src, os.listdir(src))
print('brief →',B); print('output →',O)

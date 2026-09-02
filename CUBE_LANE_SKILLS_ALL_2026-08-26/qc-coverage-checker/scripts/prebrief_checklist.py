#!/usr/bin/env python3
"""prebrief_checklist.py — extract coverage contract from feature-prebrief outputs
Usage: python prebrief_checklist.py <FUNCTION_CHECKLIST_F-xx.md> [PREBRIEF_F-xx.md] [--html file.html]
Output JSON: FN rows (id/text/trace/category), S-XX scenarios, BR-XX rules, not-supported list,
declaration signals (doa/ntf/csq/doccfg) detected from text, and — if --html given — naive evidence hits per FN.
Contract only; final evidence judgement is Claude's job.
"""
import sys, re, json
args=[a for a in sys.argv[1:] if not a.startswith('--')]
html=None
if '--html' in sys.argv: html=sys.argv[sys.argv.index('--html')+1]
if not args: print(__doc__); sys.exit(2)
fc=open(args[0],encoding='utf-8').read()
pb=open(args[1],encoding='utf-8').read() if len(args)>1 and not args[1].endswith('.html') else ''
out={'source':args[0],'fn':[],'scenarios':[],'rules':[],'not_supported':[],'declarations':{}}
cat=''
for line in fc.splitlines():
    m=re.match(r'##\s+หมวด\s*\d+\s*·\s*(.+)',line)
    if m: cat=m.group(1).strip(); continue
    m=re.match(r'\|\s*(FN-\d+)\s*\|\s*(.+?)\s*\|\s*(.*?)\s*\|',line)
    if m: out['fn'].append({'id':m.group(1),'text':m.group(2),'trace':m.group(3),'category':cat,
        'tags':re.findall(r'\[(STD|AI-DRAFT|มติ)\]',m.group(2))})
_m=list(re.finditer(r'(?m)^## สิ่งที่ไม่รองรับ',fc)); ns=_m[-1].start() if _m else -1
if ns>0:
    seg=fc[ns:]; end=re.search(r'\n(##|```)',seg[1:]); seg=seg[:end.start()+1] if end else seg
    out['not_supported']=[l[2:].strip() for l in seg.splitlines() if l.startswith('- ')]
src=fc+'\n'+pb
out['scenarios']=sorted(set(re.findall(r'\bS-\d{2}\b',src)))
out['rules']=sorted(set(re.findall(r'\bBR-\d{2}\b',src)))
low=src.lower()
out['declarations']={
 'doa': bool(re.search(r'อนุมัติ|approv|ส่งอนุมัติ|เซ็น|sign-?off|doa',low)),
 'ntf': bool(re.search(r'แจ้งเตือน|notify|notification|มอบหมาย|ส่งให้ลูกค้า|ครบกำหนด|low stock',low)),
 'csq': bool(re.search(r'ต้นทุน|มูลค่า|cost|บัญชี|gl|posting|เงินสด|งบ|budget|pdpa|ข้อมูลอ่อนไหว|masking|consequence|7c',low)),
 'doccfg': bool(re.search(r'เลขที่เอกสาร|running|เลขรัน|[A-Z]{2,4}-\d{4}-\d{4}|snapshot|สำเนา',src)),
}
# quick sanity: S-XX without FN
fn_traces=' '.join(f['trace'] for f in out['fn'])
out['scenarios_without_fn']=[s for s in out['scenarios'] if s not in fn_traces]
out['fn_without_trace']=[f['id'] for f in out['fn'] if not f['trace'] or f['trace']=='—']
if html:
    h=open(html,encoding='utf-8').read()
    hits=[]
    for f in out['fn']:
        words=[w for w in re.findall(r'[ก-๙A-Za-z0-9]{3,}',f['text']) if w not in ('ได้','แล้ว','ต้อง','การ','ทุก','ไม่')]
        found=[w for w in words if w in h]
        hits.append({'id':f['id'],'keyword_hit_ratio':round(len(found)/max(1,len(words)),2),'hits':found[:6]})
    out['html_keyword_hits']=hits
print(json.dumps(out,ensure_ascii=False,indent=1))

#!/usr/bin/env python3
"""
build_checklist_html.py — แปลง FUNCTION_CHECKLIST_[F-code].md → FUNCTION_CHECKLIST_[F-code].html
(HTML ติ๊กได้ · 3 ด่าน WF/DEV/QA · save ในเครื่อง · ส่งผลเป็น PDF/JSON/สรุปแชท)

Usage:
  python3 build_checklist_html.py FUNCTION_CHECKLIST_F-GRN.md                 # → ข้าง ๆ md
  python3 build_checklist_html.py FUNCTION_CHECKLIST_F-GRN.md -o out/x.html
  python3 build_checklist_html.py payload.json                              # ป้อน payload ตรงก็ได้
  python3 build_checklist_html.py FUNCTION_CHECKLIST_F-GRN.md --dump-json     # พิมพ์ payload ที่ parse ได้ (debug)

กติกา (ตรงกับ FUNCTION_CHECKLIST_TEMPLATE.md):
  - หัวเรื่อง       : บรรทัดแรกที่ขึ้นด้วย "# "  → meta.title (ตัด "Function Checklist ·" ออกให้)
  - meta line       : บรรทัด "> จาก PREBRIEF_[F-code] v[x] ..." → meta.source + feature_id
  - หมวด            : "## หมวด N · ชื่อ" (หรือ "## N. ชื่อ" / "## ชื่อ") → group
  - แถว FN          : | FN-XX | ข้อความ | trace | ☐ | ☐ | ☐ |  → item (คอลัมน์ 4-6 ไม่ใช้ — ด่านมาจาก header ตาราง)
  - ด่าน (lanes)    : อ่านจากหัวตาราง | FN | ต้องทำอะไรได้ | trace | WF | DEV | QA | (default WF/DEV/QA ถ้าไม่พบ)
  - ไม่รองรับ       : section "## สิ่งที่ไม่รองรับ" bullet "- ข้อความ — [มติ/OQ]" → unsupported (แยก why หลัง " — ")
  - 1 MD FN = 1 HTML FN · ห้ามตัด/รวม/เรียงใหม่ (Pipeline Mode เดียวกับ qa-friendly R12)
"""
import sys, re, json, os, argparse, hashlib

HERE=os.path.dirname(os.path.abspath(__file__))
TEMPLATE=os.path.join(HERE,'..','references','FUNCTION_CHECKLIST_HTML_TEMPLATE.html')
LANE_LABEL={'WF':'BA/UX รีวิว wireframe','DEV':'ผู้พัฒนา','QA':'ผู้ทดสอบ','UAT':'ผู้ใช้ทดสอบ','BA':'BA'}
DEFAULT_LANES=['WF','DEV','QA']

def split_row(line):
    line=line.strip()
    if line.startswith('|'): line=line[1:]
    if line.endswith('|'): line=line[:-1]
    return [c.strip() for c in line.split('|')]

def is_sep(cells):
    return all(re.fullmatch(r':?-{2,}:?',c) for c in cells if c) and any(cells)

def parse_trace(s):
    s=s.strip()
    if not s or s in ('—','-','–'): return []
    parts=re.split(r'\s*[·,;/]\s*',s)
    return [p for p in (x.strip() for x in parts) if p]

def parse_md(text):
    meta={'title':'','source':'','feature_id':''}
    lanes=None; groups=[]; items=[]; ns=[]
    cur=None; in_ns=False; seen_ids=set()
    lines=text.splitlines()
    for raw in lines:
        line=raw.rstrip()
        s=line.strip()
        if s.startswith('```'): continue
        m=re.match(r'^#\s+(.*)',s)
        if m and not meta['title']:
            t=m.group(1).strip()
            t=re.sub(r'^Function\s+Checklist\s*[·:\-—]\s*','',t,flags=re.I)
            meta['title']=t; continue
        if s.startswith('>') and not meta['source']:
            q=s.lstrip('> ').strip()
            mm=re.search(r'(PREBRIEF_[A-Za-z0-9\-]+(?:\s*v[\d.]+)?)',q)
            if mm:
                meta['source']=mm.group(1).strip()
                fid=re.search(r'PREBRIEF_([A-Za-z0-9\-]+)',q)
                if fid: meta['feature_id']=fid.group(1)
            continue
        m=re.match(r'^##\s+(.*)',s)
        if m:
            h=m.group(1).strip()
            if re.search(r'ไม่รองรับ|not\s+supported|out\s+of\s+scope',h,re.I):
                in_ns=True; cur=None; continue
            in_ns=False
            name=re.sub(r'^หมวด\s*\d+\s*[·:.\-—]\s*','',h)
            name=re.sub(r'^\d+[.)]\s*','',name).strip() or h
            gid='g%d'%(len(groups)+1)
            groups.append({'id':gid,'name':name}); cur=gid; continue
        if in_ns:
            m=re.match(r'^[-*•]\s+(.*)',s)
            if m:
                body=m.group(1).strip()
                why=''
                mm=re.split(r'\s+[—–]\s+',body,maxsplit=1)
                if len(mm)==2: body,why=mm[0].strip(),mm[1].strip()
                ns.append({'text':body,'why':why})
            continue
        if s.startswith('|'):
            cells=split_row(s)
            if is_sep(cells): continue
            first=cells[0] if cells else ''
            if re.fullmatch(r'FN',first,re.I) or (first.upper()=='FN'):
                # header row → lanes from cols after trace
                if lanes is None and len(cells)>3:
                    cand=[c for c in cells[3:] if c and not re.search(r'หมายเหตุ|note',c,re.I)]
                    if cand: lanes=[re.sub(r'\s+.*$','',c).upper() for c in cand]
                continue
            m=re.match(r'^(FN-\d+[A-Za-z]?)$',first)
            if m and len(cells)>=2:
                fid=m.group(1)
                if fid in seen_ids:
                    print(f'[WARN] duplicate FN id {fid} — คงไว้ทั้งคู่ตาม MD แต่ควรแก้ต้นทาง',file=sys.stderr)
                seen_ids.add(fid)
                if cur is None:
                    groups.append({'id':'g%d'%(len(groups)+1),'name':'ทั่วไป'}); cur=groups[-1]['id']
                text=cells[1]
                tag=''
                mt=re.search(r'\[(STD|AI-DRAFT|มติ|แผน)\]',text)
                if mt: tag=mt.group(1)
                trace=parse_trace(cells[2]) if len(cells)>2 else []
                it={'id':fid,'grp':cur,'text':text,'trace':trace}
                if tag: it['tag']=tag
                items.append(it)
    if not lanes: lanes=DEFAULT_LANES
    lane_objs=[{'id':l.lower(),'name':l,'label':LANE_LABEL.get(l,'')} for l in lanes]
    fid=meta['feature_id'] or 'F-XXX'
    payload={'meta':{'feature_id':fid,'title':meta['title'] or f'Function Checklist · {fid}',
                     'crumb':'Function Checklist','code':f"{fid} · จาก {meta['source'] or 'PREBRIEF'}",
                     'source':meta['source'],'footer':f'{fid} · Function Checklist · 2BSimple · ผลบันทึกในเครื่องนี้อัตโนมัติ'},
             'lanes':lane_objs,'groups':groups,'items':items,'unsupported':ns}
    return payload

def validate(p):
    errs=[]
    if not p['items']: errs.append('ไม่พบแถว FN-XX เลย — เช็คว่าตารางขึ้นต้นด้วย | FN-01 |')
    ids=[i['id'] for i in p['items']]
    if len(ids)!=len(set(ids)): errs.append('FN id ซ้ำ: '+', '.join(sorted({x for x in ids if ids.count(x)>1})))
    no_trace=[i['id'] for i in p['items'] if not i['trace']]
    if no_trace: print('[WARN] FN ไม่มี trace: '+', '.join(no_trace)+' (กติกา: ทุก FN ต้อง trace กลับ S-XX/BR-XX/กติกากลาง)',file=sys.stderr)
    if not p['unsupported']: print('[WARN] ไม่พบหมวด "สิ่งที่ไม่รองรับ" — template บังคับมี (เขียน "ไม่มี" ก็ยังต้องมี section)',file=sys.stderr)
    return errs

def build(payload,out):
    tpl=open(TEMPLATE,encoding='utf-8').read()
    m=re.search(r'/\*__PAYLOAD__\*/.*?/\*__END_PAYLOAD__\*/',tpl,re.S)
    if not m: raise SystemExit('template ไม่มี /*__PAYLOAD__*/ marker')
    js=json.dumps(payload,ensure_ascii=False).replace('</script','<\\/script')
    html=tpl[:m.start()]+'/*__PAYLOAD__*/'+js+'/*__END_PAYLOAD__*/'+tpl[m.end():]
    html=html.replace('<title>Function Checklist</title>','<title>'+payload['meta']['title'].replace('<','&lt;')+'</title>',1)
    os.makedirs(os.path.dirname(os.path.abspath(out)),exist_ok=True)
    open(out,'w',encoding='utf-8').write(html)
    return html

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('-o','--out'); ap.add_argument('--dump-json',action='store_true')
    a=ap.parse_args()
    src=a.src
    if src.lower().endswith('.json'):
        payload=json.load(open(src,encoding='utf-8'))
    else:
        payload=parse_md(open(src,encoding='utf-8').read())
    if a.dump_json:
        print(json.dumps(payload,ensure_ascii=False,indent=2)); return
    errs=validate(payload)
    for e in errs: print('[BLOCK] '+e,file=sys.stderr)
    if errs: sys.exit(2)
    out=a.out or re.sub(r'\.(md|json)$','',src)+'.html'
    html=build(payload,out)
    g=len(payload['groups']); n=len(payload['items']); l='/'.join(x['name'] for x in payload['lanes'])
    print(f'OK  {out}\n    FN {n} ข้อ · {g} หมวด · ด่าน {l} · ไม่รองรับ {len(payload["unsupported"])} · md5 {hashlib.md5(html.encode()).hexdigest()}')

if __name__=='__main__': main()

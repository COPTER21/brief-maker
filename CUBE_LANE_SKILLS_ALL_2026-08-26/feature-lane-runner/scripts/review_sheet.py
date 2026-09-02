#!/usr/bin/env python3
"""review_sheet.py — build waves/<W>/REVIEW_SHEET.html (+ REGISTRY_PATCH.md, DIVERGENCE.md, _BLOCKED.md summary)
Usage: python review_sheet.py <wave> [--briefs briefs]   # reads briefs/<wave>/*/_lane/LANE_STATE.json · writes briefs/<wave>/REVIEW_SHEET.html etc.
Reads features/*/_LANE_STATE.json (wave match), _DECL.json, 11_GATES/_shots/*.png (embedded as <img src=file path>), REGISTRY_PATCH.md, _BLOCKED.md
"""
import sys, json, os, glob, html, datetime, re
wave=sys.argv[1]; BD=sys.argv[sys.argv.index('--briefs')+1] if '--briefs' in sys.argv else 'briefs'
out_dir=os.path.join(BD,wave); os.makedirs(out_dir,exist_ok=True); FD=out_dir
feats=[]
for st in sorted(glob.glob(os.path.join(FD,'*','_lane','LANE_STATE.json'))):
    s=json.load(open(st,encoding='utf-8'))
    if s.get('wave')!=wave: continue
    d=os.path.dirname(os.path.dirname(st)); L=os.path.join(d,'_lane')
    decl=json.load(open(os.path.join(L,'DECL.json'),encoding='utf-8')) if os.path.exists(os.path.join(L,'DECL.json')) else {}
    shots=sorted(glob.glob(os.path.join(L,'QC','shots','*.png')))[:4]; od=s.get('out_dir','')
    rp=os.path.join(L,'REGISTRY_PATCH.md'); bl=os.path.join(L,'BLOCKED.md')
    assumed=[]; 
    for f in glob.glob(os.path.join(d,'*.md'))+(glob.glob(os.path.join(od,'2_BRD','*.md'))+glob.glob(os.path.join(od,'3_FRD','*.md')) if od else []):
        for line in open(f,encoding='utf-8',errors='ignore'):
            if '[ASSUMED]' in line: assumed.append(line.strip()[:160])
    feats.append(dict(name=s['feature'],lane=s.get('lane',''),status=s['status'],blocked_at=s.get('blocked_at'),retries=s['total_retries'],
        stages=s['stages'],decl=decl.get('pipes',{}),div=decl.get('divergence',[]),shots=[os.path.relpath(x,out_dir) for x in shots],
        assumed=sorted(set(assumed))[:12],out=os.path.relpath(od,out_dir) if od else '',registry=open(rp,encoding='utf-8').read() if os.path.exists(rp) else '',blocked=open(bl,encoding='utf-8').read() if os.path.exists(bl) else '',dir=os.path.relpath(d,out_dir)))
c={k:sum(1 for f in feats if f['status']==k) for k in('done','blocked','skipped','running')}
def pill(s): return {'done':'<span class="pill ok">เสร็จ</span>','blocked':'<span class="pill bad">ติด</span>','skipped':'<span class="pill mute">ข้าม (dep)</span>'}.get(s,'<span class="pill warn">กำลังรัน</span>')
def stg(f):
    return ''.join(f'<span class="st {v["status"]}" title="{k} · {v["status"]} · retries {v["retries"]}">{k}</span>' for k,v in f['stages'].items())
def declrow(f):
    return ' '.join(f'<span class="tag {"on" if v.get("need") else ""}">{k}</span>' for k,v in f['decl'].items())
H=f'''<!DOCTYPE html><html lang="th"><head><meta charset="utf-8"><title>REVIEW_SHEET {wave}</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>:root{{--ivory:#FAF8F5;--ink:#111;--red:#FF3B30;--orange:#FF9A1F;--green:#1F9D55;--mute:#73757B;--soft:#9A9CA2;--line:#DEDAD4;--line2:#EFEBE6}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:'Satoshi','Noto Sans Thai',sans-serif;background:var(--ivory);color:var(--ink);font-size:13px;line-height:1.5}}
.mast{{height:56px;display:flex;align-items:center;gap:14px;padding:0 22px;background:#fff;border-bottom:1px solid var(--line)}}.brand{{font-weight:700;font-size:15px}}.brand em{{font-style:normal;color:var(--red)}}.sep{{width:1px;height:22px;background:var(--line)}}.t{{font-size:17px;font-weight:700}}.meta{{margin-left:auto;color:var(--soft);font-size:12px}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding:18px 22px 0}}.stat{{background:#fff;border:1px solid var(--line2);border-radius:10px;padding:12px 16px}}.stat .l{{font-size:12px;color:var(--mute)}}.stat .v{{font-size:22px;font-weight:700;margin-top:4px}}.v.g{{color:var(--green)}}.v.r{{color:var(--red)}}.v.o{{color:var(--orange)}}
.grid{{padding:18px 22px;display:grid;grid-template-columns:repeat(auto-fill,minmax(460px,1fr));gap:16px}}.card{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 16px}}.card.blocked{{border-color:rgba(255,59,48,.5)}}
.head{{display:flex;align-items:center;gap:8px;margin-bottom:8px}}.head b{{font-size:14px}}.lane{{font-size:11px;color:var(--soft);margin-left:auto}}
.pill{{font-size:11px;font-weight:600;padding:2px 8px;border-radius:999px}}.ok{{background:#E7F6EF;color:var(--green)}}.bad{{background:#FFEDEC;color:var(--red)}}.warn{{background:rgba(255,154,31,.12);color:#B8650A}}.mute{{background:var(--line2);color:var(--mute)}}
.st{{display:inline-block;font-size:10px;padding:1px 6px;border-radius:4px;margin:2px 2px 0 0;background:var(--line2);color:var(--mute)}}.st.pass{{background:#E7F6EF;color:var(--green)}}.st.warn{{background:rgba(255,154,31,.12);color:#B8650A}}.st.block{{background:#FFEDEC;color:var(--red)}}.st.skip{{opacity:.5}}
.tag{{font-size:10px;padding:1px 7px;border-radius:999px;border:1px solid var(--line);color:var(--soft)}}.tag.on{{background:var(--ink);color:#fff;border-color:var(--ink)}}
.shots{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin:10px 0}}.shots img{{width:100%;border:1px solid var(--line2);border-radius:6px;background:#fff}}
.sec{{font-size:11.5px;font-weight:600;color:var(--mute);margin-top:10px}}ul{{padding-left:18px;font-size:12px;color:var(--mute)}}li.d{{color:#B8650A}}
pre{{font-size:11px;background:var(--ivory);border:1px solid var(--line2);border-radius:8px;padding:8px;white-space:pre-wrap;margin-top:6px}}
textarea{{width:100%;margin-top:8px;border:1px dashed var(--line);border-radius:6px;padding:6px;font:inherit;font-size:12px;min-height:44px}}
</style></head><body>
<div class="mast"><div class="brand">CUBE <em>4.0</em></div><span class="sep"></span><div class="t">Review Sheet — {wave}</div><div class="meta">{datetime.date.today()} · {len(feats)} features</div></div>
<div class="stats"><div class="stat"><div class="l">ทั้งหมด</div><div class="v">{len(feats)}</div></div><div class="stat"><div class="l">เสร็จ (DevPack)</div><div class="v g">{c['done']}</div></div><div class="stat"><div class="l">ติด (BLOCKED)</div><div class="v r">{c['blocked']}</div></div><div class="stat"><div class="l">ข้าม / กำลังรัน</div><div class="v o">{c['skipped']+c['running']}</div></div></div>
<div class="grid">'''
for f in feats:
    H+=f'''<div class="card {f['status']}"><div class="head"><b>{html.escape(f['name'])}</b>{pill(f['status'])}<span class="lane">lane {f['lane']} · retries {f['retries']}{(' · ติดที่ '+f['blocked_at']) if f['blocked_at'] else ''}</span></div>
<div>{stg(f)}</div><div style="margin-top:6px">{declrow(f)}</div>
{('<div class="shots">'+''.join(f'<a href="{html.escape(s)}"><img src="{html.escape(s)}" loading="lazy"></a>' for s in f['shots'])+'</div>') if f['shots'] else '<div class="sec">ไม่มี screenshot (S3b ยังไม่ผ่าน)</div>'}
{('<div class="sec">DIVERGENCE (chip ≠ detect — Strike เคาะ)</div><ul>'+''.join(f'<li class="d">{html.escape(x)}</li>' for x in f['div'])+'</ul>') if f['div'] else ''}
{('<div class="sec">[ASSUMED] — default ที่เลนตัดสินแทน</div><ul>'+''.join(f'<li>{html.escape(x)}</li>' for x in f['assumed'])+'</ul>') if f['assumed'] else ''}
{('<div class="sec">_BLOCKED</div><pre>'+html.escape(f['blocked'][:1200])+'</pre>') if f['blocked'] else ''}
<div class="sec">note ส่งกลับแก้ → copy ลง knowledge/TASTE_LOG.md</div><textarea placeholder="เช่น: ตำแหน่ง pill ซ้อนใน list · ชื่อ step 2 ควรเป็น … "></textarea>
<div class="sec"><a href="{html.escape(f['dir'])}">brief</a>{(' · <a href="'+html.escape(f['out'])+'">dev pack (output)</a>') if f['out'] else ''}</div></div>'''
H+='</div></body></html>'
open(os.path.join(out_dir,'REVIEW_SHEET.html'),'w',encoding='utf-8').write(H)
open(os.path.join(out_dir,'REGISTRY_PATCH.md'),'w',encoding='utf-8').write(f"# REGISTRY_PATCH — {wave} ({datetime.date.today()})\n\n"+'\n\n'.join(f['registry'] for f in feats if f['registry']))
open(os.path.join(out_dir,'DIVERGENCE.md'),'w',encoding='utf-8').write(f"# DIVERGENCE — {wave}\n\n"+'\n'.join(f"- **{f['name']}**: {x}" for f in feats for x in f['div']))
open(os.path.join(out_dir,'BLOCKED.md'),'w',encoding='utf-8').write(f"# BLOCKED — {wave}\n\n"+'\n\n'.join(f"## {f['name']} (ติดที่ {f['blocked_at']})\n{f['blocked']}" for f in feats if f['status']=='blocked'))
print('wrote',out_dir,json.dumps(c))

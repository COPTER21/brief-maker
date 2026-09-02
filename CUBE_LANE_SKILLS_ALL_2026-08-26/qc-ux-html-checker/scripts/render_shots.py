#!/usr/bin/env python3
"""Render Gate — จับ screenshot ทุก route ของ single-file SPA (hash routing)
ใช้: python render_shots.py <file.html> <outdir>
ต้องมี: pip install playwright && playwright install chromium
"""
import sys, re, os, asyncio, pathlib

async def main(html_path, outdir):
    from playwright.async_api import async_playwright
    html_path = pathlib.Path(html_path).resolve()
    os.makedirs(outdir, exist_ok=True)
    src = html_path.read_text(encoding='utf-8', errors='ignore')
    routes = sorted(set(re.findall(r'#/[A-Za-z0-9_/:-]+', src)))
    routes = [r for r in routes if ':' not in r] or ['#/']
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width':1440,'height':900})
        shots = []; geo = []; errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        for r in routes:
            await pg.goto(f"file://{html_path}{r}")
            await pg.wait_for_timeout(600)
            name = r.strip('#/').replace('/','_') or 'home'
            f = f"{outdir}/route_{name}.png"
            await pg.screenshot(path=f, full_page=True)
            shots.append(f)
            # v3 GEOMETRY GATE (#40/#103 list rows · filter bar stack · #105 demo controls in header · #96 fill)
            try:
                g = await pg.evaluate(r"""() => {
                  const q=s=>document.querySelector(s), qa=s=>[...document.querySelectorAll(s)];
                  const vis=e=>e && e.getBoundingClientRect().height>0;
                  const rows=qa('table tbody tr').filter(vis).slice(0,20).map(tr=>tr.getBoundingClientRect().height);
                  const fb=qa('.filter-row,.filters,.filter-bar,.toolbar,[class*="filter"]').filter(vis).map(e=>e.getBoundingClientRect().height);
                  const ph=q('.ph-right,.ph-actions,.page-head-actions,.ph .actions');
                  const demoInHeader=ph? [...ph.querySelectorAll('*')].some(e=>/persona|demo|seg|role-switch/i.test(e.className||'')||/\(ปิดบัง\)|\(เปิดเผย\)|persona|demo/i.test(e.textContent||'')):false;
                  const personCells=qa('table tbody tr td:first-child, table tbody tr td:nth-child(2)').filter(vis).slice(0,10);
                  const stacked=personCells.filter(td=>{const av=td.querySelector('[class*="avatar"],[class*="av"]'); if(!av) return false; const a=av.getBoundingClientRect(); const txt=[...td.querySelectorAll('span,div,b,strong')].find(x=>x!==av && !av.contains(x) && x.textContent.trim().length>1); if(!txt) return false; const t=txt.getBoundingClientRect(); return t.top>=a.bottom-2;}).length;
                  const body=document.body.getBoundingClientRect();
                  return {rows, maxRow:Math.max(0,...rows), filterHeights:fb, demoInHeader, stackedPersonCells:stacked, bodyScrollX: document.documentElement.scrollWidth>window.innerWidth};
                }""")
                g['route']=r; geo.append(g)
                flags=[]
                if g['maxRow']>64: flags.append(f"ROW_TOO_TALL {g['maxRow']:.0f}px (>64 · #40/#103)")
                if any(h>60 for h in g['filterHeights']): flags.append(f"FILTER_STACKED {max(g['filterHeights']):.0f}px (>60 · filter-row ต้องแถวเดียว)")
                if g['demoInHeader']: flags.append("DEMO_CONTROL_IN_HEADER (#105 persona/demo → demo strip)")
                if g['stackedPersonCells']: flags.append(f"AVATAR_STACKED {g['stackedPersonCells']} cells (#40 ใช้ .tbl-person inline)")
                if g['bodyScrollX']: flags.append("BODY_HSCROLL (#97)")
                for fl in flags: print(f"GEOMETRY_BLOCK {r}: {fl}")
            except Exception as e: print('geometry skip:', e)
            # เปิด drawer/modal ตัวแรกที่เจอ (best-effort)
            for sel in ['[data-open-drawer]','.btn-primary','tbody tr']:
                try:
                    el = await pg.query_selector(sel)
                    if el:
                        await el.click(); await pg.wait_for_timeout(500)
                        f2 = f"{outdir}/route_{name}__overlay_{sel.strip('[].')}.png"
                        await pg.screenshot(path=f2, full_page=True); shots.append(f2)
                        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(300)
                        break
                except Exception: pass
            # v2: คลิกทุก tab + ตรวจ overlay ค้าง (#73.1/#68.1)
            try:
                tabs = await pg.query_selector_all('[class*="drawer-tab"],[class*="tab-btn"]')
                for ti,t in enumerate(tabs[:8]):
                    await t.click(); await pg.wait_for_timeout(300)
                    await pg.screenshot(path=f"{outdir}/route_{name}__tab{ti}.png"); shots.append('tab')
                stuck = await pg.eval_on_selector_all('[data-overlay].open, .drawer.open','els=>els.length')
                await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200)
                stuck2 = await pg.eval_on_selector_all('[data-overlay].open, .drawer.open','els=>els.length')
                if stuck2 >= stuck and stuck > 0: print(f"STUCK_OVERLAY at {r}: {stuck2}")
            except Exception as e: print('interact skip:', e)
        await b.close()
    import json
    json.dump({'routes':geo,'pageerrors':errs}, open(f"{outdir}/RENDER.json",'w',encoding='utf-8'), ensure_ascii=False, indent=1)
    if errs: print(f"PAGEERROR {len(errs)}: {errs[0][:160]}")
    print(f"SHOTS: {len(shots)} files → {outdir}")
    for s in shots: print(" -", s)

if __name__ == '__main__':
    if len(sys.argv) < 3: print(__doc__); sys.exit(1)
    asyncio.run(main(sys.argv[1], sys.argv[2]))

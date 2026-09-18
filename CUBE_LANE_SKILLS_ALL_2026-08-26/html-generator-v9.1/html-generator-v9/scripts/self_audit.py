#!/usr/bin/env python3
"""Self-Audit v2 (Rule #60 รอบ 1) — นับ violation ของ Layout Integrity #50-#62 + Component Contracts #63-#68
ใช้: python self_audit.py <file.html>   → exit 0 เมื่อทุกตัวนับ = 0
"""
import re, sys, collections

SPACING = {'0','1','2','3','4','6','8','10','12','16','18','20','24','32','40','28','36','56'}  # 28 gutter · 36 control · 56 topbar (structural)
FONTS   = {'11','12','12.5','13','14','16','20','26'}
HEX_WL  = {'#111111','#FF3B30','#E62E24','#FF9A1F','#FFB763','#FAF8F5','#54565C','#73757B',
           '#9A9CA2','#DEDAD4','#E9E5E0','#F1EEEA','#FFF','#FFFFFF','#1F9D55','#E8870F',
           '#E6F0FF','#1A5FCC','#E4F4EB','#157A41','#FFF1DD','#B8690B','#FFE9E7'}

def main(path):
    s = open(path, encoding='utf-8', errors='ignore').read()
    css = s[s.find('<style'):s.find('</style>')]
    markup = s[s.find('</style>'):]
    R = {}

    vals = re.findall(r'(?:padding|margin|gap)[^:;{]*:\s*([^;}]+)', css)
    px = [p for v in vals for p in re.findall(r'(\d+(?:\.\d+)?)px', v)]
    R['spacing_off'] = [p for p in px if p not in SPACING]

    fs = re.findall(r'font-size:\s*([\d.]+)px', css)
    R['font_off'] = sorted({f for f in fs if f not in FONTS})
    R['font_count'] = len(set(fs))

    blocks = re.findall(r'([^{}]+)\{([^}]+)\}', css)
    R['flex_noalign'] = [sel.strip()[:40] for sel, b in blocks
                         if 'display:flex' in b.replace(' ','') and 'align-items' not in b
                         and b.count(';') > 1 and 'flex-direction:column' not in b.replace(' ','')]
    R['grid_nogap'] = [sel.strip()[:40] for sel, b in blocks
                       if 'display:grid' in b.replace(' ','') and 'gap' not in b]
    R['inline_layout'] = re.findall(r'style="[^"]*(?:margin|padding|width|height)[^"]*"', markup)
    z = re.findall(r'z-index:\s*([^;}]+)', css)
    R['z_adhoc'] = [v.strip() for v in z if 'var(--z-' not in v and not (v.strip().isdigit() and int(v.strip())<10)]
    hexes = re.findall(r'#[0-9A-Fa-f]{3,6}\b', css)
    R['hex_off'] = sorted({h.upper() for h in hexes if h.upper() not in HEX_WL and len(h) in (4,7)})
    R['preflight'] = [] if '<!-- PREFLIGHT' in s else ['missing stamp']

    # ---- Component Contracts #63-#68 ----
    js = markup
    has_menu = bool(re.search(r'class="[^"]*(?:dropdown|ac-menu|select-menu|autocomplete|menu-list)', s)) or 'data-overlay' in s
    if has_menu:
        R['menu_no_maxheight'] = [] if re.search(r'(?:dropdown|ac-menu|select-menu|menu-list|data-overlay)[^}]*max-height', css) or 'maxHeight' in js else ['เมนูไม่มี max-height+scroll (#65)']
        R['menu_no_flip'] = [] if ('getBoundingClientRect' in js and ('drop-up' in s or 'spaceBelow' in js or 'positionMenu' in js)) else ['ไม่มี flip-up logic (#66)']
        R['no_global_outside_close'] = [] if re.search(r"document\.addEventListener\(\s*['\"]click", js) else ['ไม่มี global outside-click handler (#68)']
    else:
        R['menu_no_maxheight'] = R['menu_no_flip'] = R['no_global_outside_close'] = []
    R['stopprop_blanket'] = re.findall(r'stopPropagation\(\)', js)[3:]  # เกิน 3 จุด = เหมาแน่ (#68)

    # #67 hint เปลือยยาว
    hints = re.findall(r'class="[^"]*(?:hint|help|form-hint)[^"]*"[^>]*>([^<]{61,})<', markup)
    R['naked_hints'] = [h[:40] for h in hints]
    # #67/#74 v3: banner/note อธิบายยาว (>120) = ต้องเข้า ⓘ · ยกเว้นมีคำเตือน/error
    banners = re.findall(r'class="[^"]*(?:note|banner|info-box|callout|explain)[^"]*"[^>]*>(.{121,}?)</', markup, re.S)
    R['long_banners'] = [re.sub(r'<[^>]+>','',b)[:40] for b in banners
                         if not re.search(r'คำเตือน|ห้าม|ระวัง|error|ผิดพลาด|ลบ', b)]
    # #62.1: overlay ไม่ประกาศ z-index
    ov=[]
    for sel,b in blocks:
        if re.search(r'\.(drawer|modal|backdrop|toast)(?![-\w])', sel) and 'position:fixed' in b.replace(' ','') and 'z-index' not in b:
            ov.append(sel.strip()[:40])
    R['overlay_no_z'] = ov
    # #82: dead refs — onclick เรียก fn ที่ไม่มีจริง / getElementById หา id ที่ไม่มี
    js_all=' '.join(re.findall(r'<script\b[^>]*>(.*?)</script>', s, re.S))
    defined=set(re.findall(r'function\s+([A-Za-z_$][\w$]*)', js_all))|set(re.findall(r'(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:\(|function|async)', js_all))
    called=set(re.findall(r'on(?:click|change|input|submit|keydown)="\s*([A-Za-z_$][\w$]*)\s*\(', markup))
    R['undefined_handlers']=sorted(called-defined)[:8]
    ids=set(re.findall(r'id="([^"]+)"', s))
    wanted=set(re.findall(r"getElementById\(['\"]([^'\"]+)", js_all))
    R['missing_ids']=sorted(wanted-ids)[:8]
    # #81: ศัพท์ภายในรั่วขึ้นจอ
    vis=re.sub(r'<script.*?</script>','',markup,flags=re.S)
    R['jargon_leak'] = re.findall(r'(E-\d{3}|GR-[A-Z]+-\d+|XR-\d+|bucket model|self-slice)', vis)[:8]
    # #62.2: เมนูลอยไม่มีพื้นทึบ/ชั้น
    mn=[]
    for sel,b in blocks:
        if re.search(r'(?:menu|dropdown|ac-list|suggest)', sel) and 'position:absolute' in b.replace(' ',''):
            if 'background' not in b or 'z-index' not in b: mn.append(sel.strip()[:40])
    R['menu_no_bg_z'] = mn
    # #78: select เต็มแถว (ไม่มี width จำกัดใน attr/style) ในโซน toolbar/filter
    lone=[]
    for m in re.finditer(r'<select[^>]*>', markup):
        tag=m.group(0)
        if 'width' not in tag:
            ctx=markup[max(0,m.start()-300):m.start()]
            if re.search(r'(?:toolbar|filter|search)', ctx): lone.append(tag[:40])
    R['fullwidth_select'] = lone
    # #78.5: นับซ้ำ — มีทั้ง stat card และ chip ที่มีตัวเลข
    has_stat = bool(re.search(r'class="[^"]*(?:stat|kpi)', markup))
    chip_counts = re.findall(r'class="[^"]*chip[^"]*"[^>]*>[^<]*\d+', markup)
    R['duplicate_counts'] = ['stat+chips ซ้ำ'] if (has_stat and len(chip_counts)>=3) else []
    # #80: img placeholder/รูปแตก
    R['img_placeholders'] = re.findall(r'data-lucide="image(?:-off)?"', markup)
    # #74: tab เถื่อน — มี class *tab* ที่ไม่ใช่ของ kit
    tabs = set(re.findall(r'class="([^"]*tab[^"]*)"', markup))
    KIT_TABS = {'drawer-tabs','drawer-tab','tab-content','tab-pane'}
    R['custom_tabs'] = sorted({t for t in tabs
                               if not any(k in t.split() for k in KIT_TABS)
                               and 'table' not in t})[:6]

    # #63 density: td padding แนวตั้ง >10 / tbody font >13
    tdp = re.findall(r'(?:td|tbody[^{]*)\{[^}]*padding:\s*(\d+)px', css)
    R['td_pad_fat'] = [p for p in tdp if int(p) > 10]
    tbf = re.findall(r'(?:tbody|td)[^{]*\{[^}]*font-size:\s*([\d.]+)px', css)
    R['tbody_font_fat'] = [f for f in tbf if float(f) > 13]

    fail = False
    print(f"== self_audit: {path} ==")
    for k, v in R.items():
        if k == 'font_count':
            bad = v > 8
            print(f"{'❌' if bad else '✅'} font_count = {v} (limit 8)")
            fail |= bad; continue
        n = len(v)
        bad = n > 0
        print(f"{'❌' if bad else '✅'} {k} = {n}" + (f"  → {v[:6]}" if bad else ""))
        fail |= bad
    print("RESULT:", "FAIL — แก้แล้วรันซ้ำจนศูนย์" if fail else "PASS — ประทับ PREFLIGHT ได้")
    sys.exit(1 if fail else 0)

if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)
    main(sys.argv[1])

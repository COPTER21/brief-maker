#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
html_to_md.py — แปลงเอกสาร QA-friendly HTML (ผลของ qa-friendly-html-generator) ให้เป็น
Markdown test set แบบละเอียด ที่ AI อ่านแล้ว "ทดสอบเอง (self-test)" ได้.

อ่านได้จาก: PAYLOAD ที่ฝังอยู่ใน HTML (meta, groups, data, cases[, shots]).
Output: ไฟล์ .md เดียว ประกอบด้วย
  - Meta + Coverage matrix
  - Data Sets (ฟิลด์/ค่า ของทุกชุด)
  - Test Cases รายเคส: ตาราง Step | Action | Input | Expected | Screenshot | Result
    (+ คอลัมน์ Setup/Locator ถ้าแนบ --spec)
  - AI Self-Test Protocol + ผลลัพธ์เทมเพลต (ให้ AI กรอก)
  - Appendix: บล็อก JSON ของทั้ง suite (ไม่รวม base64) ให้ AI parse ตรง ๆ

ไม่อ่าน base64 รูปเข้า context: รูปถูกอ้างเป็น regionKey เท่านั้น (หรือ export เป็นไฟล์ด้วย --with-images).

Usage:
  python html_to_md.py --html testcase-F-91.html --out testset-F-91.md
      [--spec shot-spec.json]     # เพิ่มคอลัมน์ Setup(JS) + Locator ให้ AI รัน Playwright ได้
      [--with-images]             # export รูปไป <out>_shots/ แล้วอ้างอิงใน MD (สำหรับ vision AI)
      [--app-url URL]             # ระบุ URL/path ของแอปจริงที่จะให้ AI เปิดทดสอบ
"""
import argparse, base64, json, pathlib, re, sys

PRI = {"high": "สำคัญมาก (High)", "med": "ปานกลาง (Medium)", "low": "ทั่วไป (Low)"}

def extract_payload(html):
    i = html.find('const PAYLOAD=')
    if i < 0:
        sys.exit("ERROR: ไม่พบ PAYLOAD ใน HTML (ไฟล์นี้อาจไม่ได้สร้างจาก qa-friendly-html-generator)")
    j = html.find('{', i)
    depth = 0; instr = False; esc = False; q = ''
    k = j
    while k < len(html):
        c = html[k]
        if instr:
            if esc: esc = False
            elif c == '\\': esc = True
            elif c == q: instr = False
        else:
            if c in '"\'': instr = True; q = c
            elif c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    return json.loads(html[j:k+1])
        k += 1
    sys.exit("ERROR: PAYLOAD JSON ไม่สมดุล")

def esc_md(s):
    return str(s).replace('|', '\\|').replace('\n', ' ').strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--html', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--spec', default=None)
    ap.add_argument('--with-images', action='store_true')
    ap.add_argument('--app-url', default=None)
    args = ap.parse_args()

    html = pathlib.Path(args.html).read_text(encoding='utf-8')
    P = extract_payload(html)
    meta = P.get('meta', {}); groups = P['groups']; data = P.get('data', {})
    cases = P['cases']; shots = P.get('shots', {})

    spec_map = {}
    if args.spec:
        spec = json.load(open(args.spec, encoding='utf-8'))
        for sh in spec.get('shots', []):
            spec_map[sh['key']] = sh

    # optional image export (no base64 in MD; references files instead)
    img_dir = None
    if args.with_images and shots:
        img_dir = pathlib.Path(args.out).with_suffix('')  # e.g. testset-F-91
        img_dir = pathlib.Path(str(img_dir) + '_shots')
        img_dir.mkdir(exist_ok=True)
        for k, v in shots.items():
            b = v.split(',', 1)[1] if ',' in v else v
            (img_dir / f"{k}.jpg").write_bytes(base64.b64decode(b))

    feat = meta.get('feature_id', 'FEATURE')
    title = meta.get('title', 'Test Suite')
    total = len(cases)

    L = []
    L.append(f"# Test Suite — {title}")
    L.append("")
    L.append(f"> เอกสารชุดทดสอบสำหรับ **AI self-test**. AI อ่านทีละเคส ทำตาม Action จริง สังเกตผล "
             f"เทียบกับ Expected แล้วบันทึก PASS/FAIL ตาม **AI Self-Test Protocol** ท้ายไฟล์.")
    L.append("")
    L.append("| รายการ | ค่า |")
    L.append("|---|---|")
    L.append(f"| Feature ID | `{feat}` |")
    L.append(f"| ชื่อชุดทดสอบ | {esc_md(title)} |")
    if meta.get('code'): L.append(f"| เวอร์ชัน | {esc_md(meta['code'])} |")
    L.append(f"| จำนวนเคสทั้งหมด | {total} |")
    L.append(f"| จำนวนหมวด | {len(groups)} |")
    if args.app_url: L.append(f"| URL/แอปที่ทดสอบ | {esc_md(args.app_url)} |")
    has_auto = bool(spec_map)
    L.append(f"| โหมดที่รองรับ | {'Automated (Playwright) + Vision/Manual' if has_auto else 'Vision/Manual'} |")
    L.append("")

    # coverage matrix
    L.append("## Coverage Matrix")
    L.append("")
    L.append("| # | หมวด (Group) | เคส | High | Med | Low |")
    L.append("|---|---|---|---|---|---|")
    for idx, g in enumerate(groups, 1):
        cs = [c for c in cases if c['grp'] == g['id']]
        h = sum(1 for c in cs if c.get('pri') == 'high')
        m = sum(1 for c in cs if c.get('pri') == 'med')
        lo = sum(1 for c in cs if c.get('pri') == 'low')
        L.append(f"| {idx:02d} | {esc_md(g['name'])} | {len(cs)} | {h} | {m} | {lo} |")
    L.append("")

    # data sets
    if data:
        L.append("## Data Sets (ตัวอย่างข้อมูลที่ใช้กรอก)")
        L.append("")
        for key in data:
            rows = data[key].get('rows', [])
            L.append(f"**ชุด {key}**")
            L.append("")
            L.append("| ฟิลด์ | data sample |")
            L.append("|---|---|")
            for r in rows:
                L.append(f"| {esc_md(r[0])} | {esc_md(r[1] if len(r) > 1 else '')} |")
            L.append("")

    # test cases
    L.append("## Test Cases")
    L.append("")
    gname = {g['id']: g['name'] for g in groups}
    for c in cases:
        L.append(f"### {c['id']} — {esc_md(c['title'])}")
        L.append("")
        L.append(f"- **หมวด:** {esc_md(gname.get(c['grp'], c['grp']))}")
        L.append(f"- **ความสำคัญ:** {PRI.get(c.get('pri'), c.get('pri',''))}")
        L.append(f"- **ทดสอบเพื่อ:** {esc_md(c.get('why',''))}")
        L.append(f"- **ผู้ทดสอบ (role):** {esc_md(c.get('who',''))}")
        L.append(f"- **เตรียมก่อนเริ่ม (Preconditions):** {esc_md(c.get('pre',''))}")
        if c.get('data') and c['data'] in data:
            L.append(f"- **ชุดข้อมูล:** {c['data']} (ดูหัวข้อ Data Sets)")
        L.append(f"- **ถือว่าผ่านเมื่อ (Pass criteria):** {esc_md(c.get('pass',''))}")
        L.append("")
        if has_auto:
            L.append("| # | Action (ทำอะไร) | Input | Expected (ผลที่ควรเห็น) | Setup/Locator | Screenshot | Result |")
            L.append("|---|---|---|---|---|---|---|")
        else:
            L.append("| # | Action (ทำอะไร) | Input | Expected (ผลที่ควรเห็น) | Screenshot | Result |")
            L.append("|---|---|---|---|---|---|")
        for i, s in enumerate(c['steps'], 1):
            do = esc_md(s[0]); inp = esc_md(s[1]) if len(s) > 1 else ''
            exp = esc_md(s[2]) if len(s) > 2 else ''
            rk = s[3] if len(s) > 3 else ''
            shot = ''
            if rk:
                if img_dir is not None:
                    rel = f"{img_dir.name}/{rk}.jpg"
                    shot = f"![{rk}]({rel})"
                else:
                    shot = f"`{rk}`"
            else:
                shot = '—'
            if has_auto:
                loc = ''
                if rk and rk in spec_map:
                    sm = spec_map[rk]
                    setup = '; '.join(sm.get('setup', [])) or '—'
                    tgt = sm.get('target', {})
                    locator = tgt.get('selector', '')
                    if tgt.get('has_text'): locator += f" (text: {tgt['has_text']})"
                    loc = f"setup: `{esc_md(setup)}`<br>el: `{esc_md(locator)}`"
                else:
                    loc = '—'
                L.append(f"| {i} | {do} | {inp} | {exp} | {loc} | {shot} | ☐ |")
            else:
                L.append(f"| {i} | {do} | {inp} | {exp} | {shot} | ☐ |")
        L.append("")

    # AI self-test protocol
    L.append("## AI Self-Test Protocol")
    L.append("")
    L.append("ทำตามนี้ทุกเคส:")
    L.append("")
    L.append("1. อ่าน **Preconditions** แล้วจัดสถานะระบบให้พร้อม")
    if has_auto:
        L.append("2. ถ้าทดสอบแบบ automated: ใช้ **Setup/Locator** ในตาราง — รัน `setup` (JS) เพื่อไปยังหน้าจอ "
                 "แล้วใช้ `el` (selector/ข้อความ) เป็นจุดอ้างอิงในการคลิก/ตรวจ")
        L.append("3. ถ้าทดสอบแบบ vision/manual: เปิดแอปจริง ทำตาม **Action** ทีละขั้น (อ้างอิงภาพจาก Screenshot ได้)")
    else:
        L.append("2. เปิดแอปจริง ทำตาม **Action** ทีละขั้น (อ้างอิงภาพจาก Screenshot column ได้ถ้ามี)")
    L.append(f"{'4' if has_auto else '3'}. หลังแต่ละขั้น เทียบสิ่งที่เกิดกับ **Expected** → ถ้าตรง = PASS, ไม่ตรง = FAIL (พร้อมเหตุผลสั้น ๆ)")
    L.append(f"{'5' if has_auto else '4'}. เคสจะ **ผ่าน** เมื่อทุกขั้น PASS และตรงกับ *ถือว่าผ่านเมื่อ*; ถ้ามีขั้นใด FAIL = เคสไม่ผ่าน")
    L.append(f"{'6' if has_auto else '5'}. ห้ามเปลี่ยน/ลบข้อมูลจริงเกินที่เคสกำหนด; ถ้าเคยทดสอบสร้างของ ให้ล้างหลังเสร็จถ้าทำได้")
    L.append("")
    L.append("### รูปแบบผลลัพธ์ที่ AI ต้องส่งกลับ")
    L.append("")
    L.append("กรอกตารางสรุปนี้ + ราย step ที่ FAIL:")
    L.append("")
    L.append("```json")
    L.append(json.dumps({
        "feature_id": feat,
        "run_by": "AI",
        "summary": {"total": total, "pass": 0, "fail": 0, "blocked": 0, "pass_rate": "0%"},
        "results": [
            {"id": c['id'], "verdict": "pass|fail|blocked",
             "failed_steps": [], "note": ""} for c in cases
        ]
    }, ensure_ascii=False, indent=2))
    L.append("```")
    L.append("")

    # machine-readable appendix (no base64)
    L.append("## Appendix — Structured Suite (JSON)")
    L.append("")
    L.append("> สำหรับให้ AI parse ตรง ๆ (ไม่รวมรูป base64).")
    L.append("")
    L.append("```json")
    slim = {
        "meta": meta,
        "groups": groups,
        "data": data,
        "cases": [
            {k: v for k, v in c.items()} for c in cases
        ]
    }
    L.append(json.dumps(slim, ensure_ascii=False, indent=1))
    L.append("```")
    L.append("")

    out = pathlib.Path(args.out)
    out.write_text("\n".join(L), encoding='utf-8')
    kb = out.stat().st_size // 1024
    print(f"WROTE {out}  ({kb} KB)  | cases {total} | groups {len(groups)}"
          f" | mode {'automated+vision' if has_auto else 'vision'}"
          f"{' | images exported' if img_dir else ''}")

if __name__ == '__main__':
    main()

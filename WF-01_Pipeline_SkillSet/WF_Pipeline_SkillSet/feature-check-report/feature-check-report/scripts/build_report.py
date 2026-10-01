#!/usr/bin/env python3
"""build_report.py — แปลง report.json → รายงานผลตรวจฟีเจอร์ (HTML ไฟล์เดียว)

ใช้:  python3 build_report.py report.json [--out DIR]

- คำนวณผลตัดสิน / สิ่งที่ต้องทำต่อ / จำนวน / เลขรายงาน / ชื่อไฟล์ ให้อัตโนมัติ
- UI/UX เติม checklist มาตรฐานให้เอง ผู้ตรวจบอกเฉพาะข้อที่มีปัญหา
- รูปหลักฐาน (path ไฟล์ภาพ) ถูกฝังในไฟล์ → ส่งต่อไฟล์เดียวจบ
"""
import json, os, base64, html, datetime, argparse, mimetypes

HERE = os.path.dirname(os.path.abspath(__file__))

UI_STD = [
    ("U-01", "สี / ฟอนต์ ตรง CI"),
    ("U-02", "ระยะห่าง / การจัดแนว ฟอร์มและตาราง"),
    ("U-03", "ตาราง 1 ช่อง = 1 บรรทัด ไม่ซ้อนข้อมูล"),
    ("U-04", "ปุ่ม / ไอคอน ขนาดและสไตล์สม่ำเสมอ"),
    ("U-05", "ข้อความไทยถูกต้อง ไม่พิมพ์ผิด ไม่ตกบรรทัดแปลก"),
    ("U-06", "Dropdown / popup ไม่จม ไม่ล้นจอ"),
]
UX_STD = [
    ("X-01", "ทำงานหลักจบได้เองโดยไม่ต้องเดา"),
    ("X-02", "กดแล้วระบบบอกผลทุกครั้ง (แจ้งเตือน / สถานะเปลี่ยน)"),
    ("X-03", "ข้อความ error บอกว่าผิดที่ไหน แก้ยังไง"),
    ("X-04", "ถามยืนยันก่อนลบ / ยกเลิก / สิ่งที่ย้อนไม่ได้"),
    ("X-05", "หน้าว่าง / กำลังโหลด / โหลดไม่สำเร็จ มีทางไปต่อ"),
    ("X-06", "ความเร็วตอบสนองรับได้"),
]
ST = {"pass": ("ผ่าน", "pass"), "note": ("มีข้อสังเกต", "warn"),
      "fail": ("ไม่ผ่าน", "fail"), "na": ("ไม่ได้ตรวจ", "na")}
SEV = {"critical": ("Critical", "sev-c", 0), "high": ("High", "sev-h", 1),
       "medium": ("Medium", "sev-m", 2), "low": ("Low", "sev-l", 3)}
TH_M = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]


def e(s):
    return html.escape(str(s if s is not None else ""))


def thdate(d):
    try:
        d = datetime.date.fromisoformat(d)
    except Exception:
        return e(d) if d else "____/____/____"
    return f"{d.day} {TH_M[d.month - 1]} {d.year + 543}"


def norm_status(s):
    s = str(s or "").lower()
    return s if s in ST else "na"


def chip(status):
    t, c = ST[norm_status(status)]
    return f'<span class="chip {c}">{t}</span>'


def evid(x, base):
    """หลักฐาน: ไฟล์ภาพที่มีอยู่จริง → ฝังรูป (คลิกขยาย) / อย่างอื่น → แสดงชื่อไฟล์"""
    if not x:
        return "—"
    out = []
    for it in (x if isinstance(x, list) else [x]):
        p = it if os.path.isabs(it) else os.path.join(base, it)
        mt = mimetypes.guess_type(p)[0] or ""
        if os.path.isfile(p) and mt.startswith("image/"):
            b64 = base64.b64encode(open(p, "rb").read()).decode()
            out.append(f'<img class="shot" src="data:{mt};base64,{b64}" alt="{e(os.path.basename(p))}" title="คลิกเพื่อขยาย">')
        else:
            out.append(f'<span class="file">{e(os.path.basename(str(it)))}</span>')
    return " ".join(out)


def merge_std(std, checked, overrides, prefix):
    """checked=True → ข้อที่ไม่ได้พูดถึง = ผ่าน · False → = ไม่ได้ตรวจ"""
    by = {o["id"]: o for o in overrides if o.get("id")}
    rows = []
    for k, label in std:
        o = by.pop(k, {})
        rows.append({"id": k, "item": o.get("item", label),
                     "status": norm_status(o.get("status", "pass" if checked else "na")),
                     "note": o.get("note", ""), "evidence": o.get("evidence")})
    n = len(std)
    for o in overrides:
        if o.get("id") and o["id"] not in by:
            continue  # merged into a standard row already
        n += 1
        rows.append({"id": o.get("id") or f"{prefix}-{n:02d}", "item": o.get("item", ""),
                     "status": norm_status(o.get("status", "note")),
                     "note": o.get("note", ""), "evidence": o.get("evidence")})
    return rows


def count(rows):
    c = {k: 0 for k in ST}
    for r in rows:
        c[norm_status(r["status"])] += 1
    return c


def verdict(logic, bugs):
    open_b = [b for b in bugs if b.get("status", "open") != "fixed"]
    crit = [b for b in open_b if b["sev"] == "critical"]
    high = [b for b in open_b if b["sev"] == "high"]
    lc = count(logic)
    checked = lc["pass"] + lc["note"] + lc["fail"]
    fails = [r for r in logic if r["status"] == "fail"]
    if checked == 0:
        return ("ยังสรุปไม่ได้", "na", "ยังไม่มีข้อ Logic ที่ตรวจแล้ว",
                "ระบุสิ่งที่ตรวจในข้อ 1 แล้วออกรายงานใหม่")
    if crit or lc["fail"] >= 3:
        why = (f"พบ Bug ระดับ Critical {len(crit)} รายการ" if crit
               else f"Logic ไม่ผ่าน {lc['fail']} จาก {checked} ข้อ")
        return ("ไม่ผ่าน", "fail", why, "ส่งกลับ Dev แก้ทั้งหมด แล้วตรวจใหม่ทั้งรอบ")
    if high or fails:
        parts = []
        if high:
            parts.append(f"Bug ระดับ High {len(high)} รายการ")
        if fails:
            parts.append(f"Logic ไม่ผ่าน {len(fails)} ข้อ")
        must = [b["id"] for b in high] + [r["bug"] or r["id"] for r in fails]
        must = list(dict.fromkeys(must))
        return ("ผ่านแบบมีเงื่อนไข", "warn", "พบ " + " และ ".join(parts),
                "แก้ " + ", ".join(must) + " แล้วตรวจซ้ำเฉพาะจุด ก่อนขึ้น Production")
    rest = len(open_b)
    return ("ผ่าน", "pass", "Logic ถูกต้องครบ ไม่พบ Bug ระดับ High ขึ้นไป",
            "ขึ้น Production ได้" + (f" · Bug Medium / Low {rest} รายการ ตามแก้รอบถัดไป" if rest else ""))


def build(d, base):
    css = open(os.path.join(HERE, "..", "assets", "report.css"), encoding="utf-8").read()
    f = d.get("feature", {})
    code = f.get("code") or "F-XXX"
    rnd = int(d.get("round") or 1)
    date = d.get("date") or datetime.date.today().isoformat()

    logic = []
    for i, r in enumerate(d.get("logic", []), 1):
        st = norm_status(r.get("status", "pass"))
        logic.append({"id": r.get("id") or f"L-{i:02d}", "item": r.get("item", ""),
                      "expected": r.get("expected", ""),
                      "actual": r.get("actual") or ("ตรงตามคาด" if st == "pass" else ""),
                      "status": st, "bug": r.get("bug", ""), "ref": r.get("ref", "")})
    ui = merge_std(UI_STD, d.get("ui_checked", True), d.get("ui", []), "U")
    ux = merge_std(UX_STD, d.get("ux_checked", True), d.get("ux", []), "X")
    bugs = []
    for i, b in enumerate(d.get("bugs", []), 1):
        s = str(b.get("severity", "medium")).lower()
        bugs.append({**b, "id": b.get("id") or f"BUG-{i:02d}", "sev": s if s in SEV else "medium"})
    bugs.sort(key=lambda b: SEV[b["sev"]][2])

    v_txt, v_cls, v_why, v_next = verdict(logic, bugs)
    if d.get("summary_note"):
        v_why = d["summary_note"]
    lc, uc, xc = count(logic), count(ui), count(ux)

    def score(c):
        chk = c["pass"] + c["note"] + c["fail"]
        if chk == 0:
            return '<div class="n na-t">—</div><div class="s">ไม่ได้ตรวจ</div>'
        sub = [f"{ST[k][0]} {c[k]}" for k in ("note", "fail", "na") if c[k]]
        return (f'<div class="n">{c["pass"]}<span>/{chk}</span></div>'
                f'<div class="s">{" · ".join(sub) or "ผ่านทุกข้อ"}</div>')

    sev_c = {}
    for b in bugs:
        sev_c[b["sev"]] = sev_c.get(b["sev"], 0) + 1
    sev_chips = "".join(f'<span class="chip {SEV[k][1]}">{SEV[k][0]} {sev_c[k]}</span>'
                        for k in SEV if k in sev_c) or '<span class="s">ไม่พบ Bug</span>'
    docno = f"FR-{date[:4]}-{code}-R{rnd}"

    envb = " · ".join(x for x in [d.get("env"), d.get("build")] if x)
    meta = [("Module", e(f.get("module"))), ("Environment / Build", e(envb)),
            ("ผู้ตรวจ", e(d.get("tester"))), ("วันที่ตรวจ", thdate(date)),
            ("เอกสารอ้างอิง", e(d.get("refs"))), ("Dev ผู้รับผิดชอบ", e(d.get("dev")))]
    meta_html = "".join(f'<div><small>{k}</small><span>{v or "—"}</span></div>' for k, v in meta)

    sc = d.get("scope", {})
    checked = "".join(f"<li>{e(x)}</li>" for x in sc.get("checked", [])) or "<li>ตามรายการในข้อ 1–3</li>"
    notc = []
    for x in sc.get("not_checked", []):
        if isinstance(x, dict):
            notc.append(f"<li>{e(x.get('item'))}{' — ' + e(x['reason']) if x.get('reason') else ''}</li>")
        else:
            notc.append(f"<li>{e(x)}</li>")
    notc_html = "".join(notc) or "<li>ไม่มี — ตรวจครบตามขอบเขต</li>"

    if logic:
        rows = []
        for r in logic:
            ref = f'<a href="#{e(r["bug"])}">{e(r["bug"])}</a>' if r["bug"] else (e(r["ref"]) or "—")
            rows.append(f'<tr class="r-{r["status"]}"><td class="id">{e(r["id"])}</td><td>{e(r["item"])}</td>'
                        f'<td>{e(r["expected"]) or "—"}</td><td>{e(r["actual"]) or "—"}</td>'
                        f'<td>{chip(r["status"])}</td><td class="ev">{ref}</td></tr>')
        logic_html = "".join(rows)
    else:
        logic_html = '<tr><td colspan="6" class="empty">ยังไม่มีรายการ</td></tr>'

    def check_rows(rows):
        return "".join(f'<tr class="r-{r["status"]}"><td class="id">{e(r["id"])}</td><td>{e(r["item"])}</td>'
                       f'<td>{chip(r["status"])}</td><td>{e(r["note"]) or "—"}</td>'
                       f'<td class="ev">{evid(r["evidence"], base)}</td></tr>' for r in rows)

    if bugs:
        cards = []
        for b in bugs:
            steps = b.get("steps") or []
            if isinstance(steps, list) and steps:
                steps_html = "<ol>" + "".join(f"<li>{e(s)}</li>" for s in steps) + "</ol>"
            else:
                steps_html = e(steps) if steps else "—"
            st = ('<span class="chip pass">แก้แล้ว</span>' if b.get("status") == "fixed"
                  else '<span class="chip na">รอแก้</span>')
            ev = f'<div class="ev">{evid(b["evidence"], base)}</div>' if b.get("evidence") else ""
            cards.append(
                f'<div class="bug" id="{e(b["id"])}"><div class="bug-h"><b>{e(b["id"])}</b>'
                f'<span class="t">{e(b.get("title", ""))}</span>'
                f'<span class="chip {SEV[b["sev"]][1]}">{SEV[b["sev"]][0]}</span>{st}</div>'
                f'<div class="bug-b"><div><small>ขั้นตอนทำซ้ำ</small>{steps_html}</div>'
                f'<div><small>ผลที่ควรเป็น</small>{e(b.get("expected") or "—")}</div>'
                f'<div><small>ผลที่เกิดจริง</small>{e(b.get("actual") or "—")}{ev}</div></div></div>')
        bug_html = "".join(cards)
    else:
        bug_html = '<p class="none">ไม่พบ Bug ในรอบนี้</p>'

    sug = d.get("suggestions", [])
    sug_html = ""
    if sug:
        srows = "".join(
            f'<tr><td class="id">S-{i:02d}</td><td>{e(s.get("item") if isinstance(s, dict) else s)}</td>'
            f'<td>{e((s.get("reason") if isinstance(s, dict) else "") or "—")}</td></tr>'
            for i, s in enumerate(sug, 1))
        sug_html = ('<h2><span class="no">5</span>ข้อเสนอแนะ (ไม่ใช่ Bug)</h2>'
                    '<p class="lead">ทำงานถูกตาม spec แล้ว แต่ควรปรับให้ดีขึ้น — ส่งต่อเป็น Enhancement ถ้าทีมเห็นด้วย</p>'
                    f'<div class="tbl-wrap"><table><thead><tr><th>#</th><th>ข้อเสนอ</th><th>เหตุผล</th></tr></thead>'
                    f'<tbody>{srows}</tbody></table></div>')
    sign_no = 6 if sug else 5
    title = f'{code} {f.get("name", "")}'.strip()

    page = f'''<!DOCTYPE html>
<html lang="th"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>รายงานผลตรวจ — {e(title)}</title>
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;500;600;700&display=swap">
<style>{css}</style></head>
<body><div class="page"><div class="sheet">
<div class="toolbar"><button type="button" onclick="window.print()">พิมพ์ / บันทึก PDF</button></div>
<header class="head"><div><h1>รายงานผลตรวจฟีเจอร์</h1><div class="feat">{e(title)}</div></div>
<div class="docno">เลขที่รายงาน<b>{docno}</b>รอบตรวจที่ {rnd}</div></header>
<div class="meta">{meta_html}</div>

<section class="verdict v-{v_cls}">
<div class="v-main"><small>ผลการตรวจ</small><div class="v">{v_txt}</div><p>{e(v_why)}</p>
<div class="next"><small>สิ่งที่ต้องทำต่อ</small>{e(v_next)}</div></div>
<div class="v-grid">
<div class="v-cell"><small>1 · Logic</small>{score(lc)}</div>
<div class="v-cell"><small>2 · UI ความเรียบร้อย</small>{score(uc)}</div>
<div class="v-cell"><small>3 · UX ใช้งานง่าย</small>{score(xc)}</div>
<div class="v-cell"><small>4 · Bug ที่พบ</small><div class="n">{len(bugs)}</div><div class="bars">{sev_chips}</div></div>
</div></section>

<h2><span class="no">0</span>ขอบเขตการตรวจ</h2>
<p class="lead">ส่วนที่ไม่ได้ตรวจ อยู่นอกความรับผิดชอบของรายงานฉบับนี้</p>
<div class="scope"><div class="box"><h3>ตรวจแล้ว</h3><ul>{checked}</ul></div>
<div class="box"><h3>ไม่ได้ตรวจ</h3><ul>{notc_html}</ul></div></div>

<h2><span class="no">1</span>Logic — ทำงานถูกตามกฎธุรกิจ</h2>
<p class="lead">เทียบผลจริงกับ FRD / Test Case — ข้อที่ไม่ผ่านต้องผูกกับ Bug ในข้อ 4</p>
<div class="tbl-wrap"><table><thead><tr><th>#</th><th>กฎ / Scenario</th><th>ผลที่คาดหวัง</th><th>ผลจริง</th><th>ผล</th><th>อ้างอิง</th></tr></thead>
<tbody>{logic_html}</tbody></table></div>

<h2><span class="no">2</span>UI — ความเรียบร้อยของหน้าจอ</h2>
<p class="lead">Checklist มาตรฐาน · "ผ่าน" = ผู้ตรวจดูแล้วไม่พบปัญหา</p>
<div class="tbl-wrap"><table><thead><tr><th>#</th><th>หัวข้อตรวจ</th><th>ผล</th><th>หมายเหตุ</th><th>หลักฐาน</th></tr></thead>
<tbody>{check_rows(ui)}</tbody></table></div>

<h2><span class="no">3</span>UX — ใช้งานลื่นไหล</h2>
<p class="lead">มองจากผู้ใช้จริง · "ผ่าน" = ผู้ตรวจลองใช้แล้วไม่ติดขัด</p>
<div class="tbl-wrap"><table><thead><tr><th>#</th><th>หัวข้อตรวจ</th><th>ผล</th><th>หมายเหตุ</th><th>หลักฐาน</th></tr></thead>
<tbody>{check_rows(ux)}</tbody></table></div>

<h2><span class="no">4</span>Bug ที่พบ</h2>
<p class="lead">เรียงจากรุนแรงมากไปน้อย · ทำซ้ำได้ตามขั้นตอน</p>
{bug_html}
{sug_html}

<h2><span class="no">{sign_no}</span>การรับรองผลตรวจ</h2>
<div class="attest">ข้าพเจ้าได้ตรวจฟีเจอร์นี้ตามขอบเขตในข้อ 0 บน environment และ build ที่ระบุ ผลทั้งหมดมาจากการทดสอบจริง ข้อที่ระบุว่า "ผ่าน" คือได้ตรวจแล้วไม่พบปัญหา ส่วนที่ "ไม่ได้ตรวจ" อยู่นอกความรับผิดชอบของรายงานฉบับนี้</div>
<div class="signs">
<div class="sign"><small>ผู้ตรวจ</small><div class="line"></div><div class="who">{e(d.get("tester"))}&nbsp;</div><div class="d">{thdate(date)}</div></div>
<div class="sign"><small>ผู้ทบทวนรายงาน</small><div class="line"></div><div class="who">{e(d.get("reviewer"))}&nbsp;</div><div class="d">____/____/____</div></div>
<div class="sign"><small>Dev รับทราบ</small><div class="line"></div><div class="who">{e(d.get("dev"))}&nbsp;</div><div class="d">____/____/____</div></div>
</div>

<div class="rules"><b>เกณฑ์ตัดสินผล</b> (คำนวณอัตโนมัติ)
<ul><li><b>ไม่ผ่าน</b> — มี Bug Critical ค้าง หรือ Logic ไม่ผ่านตั้งแต่ 3 ข้อ</li>
<li><b>ผ่านแบบมีเงื่อนไข</b> — มี Bug High ค้าง หรือ Logic ไม่ผ่าน 1–2 ข้อ → แก้แล้วตรวจซ้ำเฉพาะจุด</li>
<li><b>ผ่าน</b> — Logic ผ่านทุกข้อ ไม่มี Bug High ขึ้นไป (Medium / Low ตามแก้รอบถัดไป)</li></ul>
<b>ระดับ Bug</b> · Critical ใช้งานไม่ได้ / ข้อมูลเสีย / ข้ามสิทธิ์หรือสายอนุมัติ · High ผลลัพธ์ผิด (เงิน สต๊อก สถานะ) · Medium ผิด spec แต่มีทางเลี่ยง · Low หน้าตา / ข้อความ</div>
</div></div>
<div class="lb" id="lb"><img alt=""></div>
<script>
(function(){{
  var lb=document.getElementById('lb');
  document.querySelectorAll('.shot').forEach(function(i){{
    i.addEventListener('click',function(){{lb.querySelector('img').src=i.src;lb.classList.add('on');}});
  }});
  lb.addEventListener('click',function(){{lb.classList.remove('on');}});
  document.addEventListener('keydown',function(ev){{if(ev.key==='Escape')lb.classList.remove('on');}});
}})();
</script>
</body></html>'''
    return page, {"docno": docno, "code": code, "round": rnd, "date": date,
                  "verdict": v_txt, "why": v_why, "next": v_next, "bugs": len(bugs)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    d = json.load(open(a.json, encoding="utf-8"))
    page, info = build(d, os.path.dirname(os.path.abspath(a.json)))
    os.makedirs(a.out, exist_ok=True)
    fn = os.path.join(a.out, f"FR_{info['code']}_R{info['round']}_{info['date'].replace('-', '')}.html")
    open(fn, "w", encoding="utf-8").write(page)
    info["file"] = fn
    print(json.dumps(info, ensure_ascii=False))

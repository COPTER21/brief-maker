---
name: qa-friendly-html-generator
description: >-
  สร้าง "เอกสารแบบทดสอบฉบับผู้ใช้" (QA-friendly Test Case HTML) จาก feature pack
  (BRD + FRD + HTML prototype) — HTML ไฟล์เดียว self-contained ที่ผู้ทดสอบไม่รู้ระบบ
  ก็ทำตามได้: step ภาษาคนละเอียดทีละขั้น ไม่มีศัพท์เทคนิค, ภาพหน้าจอจริงไฮไลต์จุดทดสอบ
  (กด 👁 ดูเต็มจอ), ปุ่ม "data sample" ดู+คัดลอกค่าที่ต้องกรอก, ติ๊กผลรายขั้น + "ผ่านทั้งเคส",
  บันทึกผลค้างในเครื่อง, พิมพ์/ดาวน์โหลด PDF รายงานผลได้จริง. ★ v2 Pipeline Mode:
  รับ testcases-*.md จาก ai-testcase-md-generator เป็นต้นฉบับเคส แปลง 1:1 (คง TC id,
  ห้าม drop เคส/ยุบ step) — เคสครบเท่าฝั่ง AI, cross-check ผลกันได้. ใช้แทน frd-qa-generator เมื่อผู้ทดสอบเป็น end-user/ลูกค้า.
  ใช้เมื่อ user พูดถึง "เอกสารทดสอบ friendly", "test case อ่านง่าย", "แบบทดสอบให้ลูกค้า/ผู้ใช้",
  "qa friendly html", "qa-friendly-html-generator", "สร้าง UAT doc", "แปลง testcases md เป็นแบบทดสอบคน". Input: testcases-*.md (แนะนำ —
  รองรับ v1.1: XT cross-module, LOCK, Manifest) หรือ BRD + FRD (+ HTML). Output: HTML ไฟล์เดียว
  เปิดได้ทันที. ทำงานที่ SOW3.5 ของ WF-01 คู่กับ ai-testcase-md-generator.
---

# qa-friendly-html-generator — v2.2 (Warm Light)

**ตำแหน่งใน workflow:** WF-01 · SOP3 · SOW3.5 (คู่กับ `ai-testcase-md-generator` — ฝั่ง AI ทำ MD, ฝั่งนี้ทำ UAT HTML สำหรับคน — TC id เดียวกัน cross-check ผลได้)
**DoD:** เคส/step ใน HTML = ใน MD ครบตาม R15 (รวมเคส XT/LOCK — sys:true ถ้าคนทำไม่ได้)

แปลง feature pack ให้เป็น **เอกสารแบบทดสอบที่คนทั่วไปทำตามได้** — ไฟล์ HTML เดียว
เปิดในเบราว์เซอร์ได้เลย (ฟอนต์ + library PDF ฝังในตัว, ใช้ offline ได้).

> อ่าน `references/iron-rules.md` ให้ครบก่อนเริ่มเสมอ — เป็นกฎที่ห้ามฝ่าฝืน
> (โดยเฉพาะ R1 ห้ามมีโค้ด/ศัพท์, R6 ห้ามอ่าน base64 กลับเข้า context)

## Input
- **BRD** + **FRD** (06_TESTS / 05_RULES ใช้ดึงเคส; UI/LOGIC ใช้เขียน "ผลที่ควรเห็น")
- **HTML prototype** ของฟีเจอร์ (ถ้ามี) — ใช้ถ่ายภาพหน้าจอจริง + ไฮไลต์
  - ถ้าไม่มี prototype: ยังสร้างเอกสารได้ แต่ทุก step ตั้ง `regionKey = ""` (ไม่มีปุ่ม 👁)

## Output
ไฟล์เดียว `testcase-<feature>.html` — มี:
- sidebar charcoal — CI Warm Light ตาม html-generator-v6 (`assets/template.html` sync token จาก
  `html-generator-v6/knowledge/ci-tokens.md` — ถ้า v6 อัพเดต CI ต้อง sync template ตาม, ห้ามแก้สีเอง),
  ความคืบหน้ารวม, nav แต่ละหมวด (= คนละหน้า)
- ตารางขั้นตอน: ขั้น · ทำอะไร · ข้อมูลที่ใช้ (ปุ่ม **data sample**) · ผลที่ควรเห็น · 👁 ดูจอ · ผล
- ติ๊กผล ✓ ✗ — รายขั้น + ปุ่มลัด "✓ ผ่านทั้งเคส" + บันทึกผลค้าง (localStorage)
- ปุ่ม "พิมพ์ผลทดสอบ" → หน้า preview เอกสาร A4 (กรอกผู้ตรวจ/วันที่) → ดาวน์โหลด PDF จริง / พิมพ์

---

## กระบวนการ 7 ขั้น

### 0) เลือกโหมด (สำคัญ — ตัดสินก่อนเริ่ม)
- **Pipeline Mode (แนะนำ/default):** ถ้ามีไฟล์ `testcases-<feature>.md` จาก skill
  `ai-testcase-md-generator` (หรือ user ชี้ให้ใช้) → **ใช้ไฟล์นั้นเป็นต้นฉบับเคสทั้งหมด**
  ห้ามคิดเคสใหม่เอง. งานของ skill นี้ = "แปล + render" ตาม `references/md-to-cases-mapping.md`.
- **Standalone Mode (fallback):** ไม่มี MD → **ห้ามคิดเคสสด ๆ จาก pack ตรง ๆ** (จะได้เคสน้อย
  ไม่ครบ). ให้ทำกระบวนการของ `ai-testcase-md-generator` ก่อน (อ่าน pack → **Coverage Ledger
  ไล่ทุก FR/rule/EC/error/permission → derivation playbook → Coverage Audit**) จนได้ชุดเคส
  ครบในหัว/ไฟล์ .md ชั่วคราว แล้วจึงเข้าขั้น 2 แบบเดียวกับ Pipeline Mode.
  ถ้า skill ai-testcase-md-generator ติดตั้งอยู่ ให้เปิดอ่าน references ของมันประกอบ.

### 1) อ่าน input
- Pipeline: อ่าน `testcases-*.md` ทั้งไฟล์ (Meta, Coverage Ledger, Data Sets, ทุกเคสทุก step,
  Coverage Audit) + เปิด HTML prototype (ใช้ถ่ายภาพ)
- Standalone: อ่าน BRD + FRD (06_TESTS, 05_RULES, UI/LOGIC) + HTML → ทำ Ledger ตามขั้น 0

### 2) เขียน `cases.json`  (งานแปล 1:1 — ไม่ใช่งานคิดใหม่)
ตาม `references/cases-schema.md` + `references/iron-rules.md` + **`references/md-to-cases-mapping.md`**:
- **1 MD case = 1 cases.json case — คง TC id เดิม** (R12) · **1 MD step = 1 step** ห้ามยุบ (R13)
- แปลภาษา agent → ภาษาคน: verb tag → ประโยคจับมือทำ, route → "เปิดหน้า…" (R1/R2 เดิม)
- `Setup:` ของ MD → `pre` · Data Sets → `data{}` · `ผ่านเมื่อ` → `pass` · priority → `pri`
- เคสที่คนทำไม่ได้ (simulate/ระบบหลังบ้าน/ข้าม tenant) → ใส่เป็นเคส `sys: true` แบบจาง
  พร้อมเหตุผล — **ห้ามลบทิ้งเงียบ ๆ** (R14)
- ปิดท้ายด้วย **นับตรวจ** (R15): จำนวนเคส/step ใน cases.json = ใน MD (หรือมีรายการตัด+เหตุผล)

### 3) เขียน `shot-spec.json`  (ถ้ามี prototype)
ตาม `references/shot-spec-schema.md`: อ่าน HTML เพื่อรู้ว่า JS ตัวไหนเปิดหน้าจอไหน,
selector/ข้อความของ element ที่ทดสอบ, container ที่เป็น "หน้าจอ".
ตั้ง `key` ให้ตรงกับ `regionKey` ที่ใช้ใน cases.json.
**Pipeline Mode ได้เปรียบ:** MD ระบุ `Start` route + anchor ข้อความจริงทุก step อยู่แล้ว —
derive regionKey จาก route/ป้ายใน MD ได้ตรง ๆ ไม่ต้องเดา.

### 4) ถ่ายภาพ (engine)
```bash
export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers     # ถ้าจำเป็นใน env นี้
python scripts/capture.py --pack <packDir> --spec shot-spec.json --out shots_b64.json
```
สคริปต์ render หน้าจริง → ไฮไลต์ spotlight → optimize (แนวนอน 1300 / แนวตั้ง 940, JPEG q86).
**อย่าอ่าน `shots_b64.json` กลับเข้า context** (R6).

### 5) build (engine — dedup + inject)
```bash
python scripts/build.py --cases cases.json --shots shots_b64.json --out testcase-<feature>.html
```
build จะ dedup (ยุบ byte ซ้ำ + ตัดภาพไม่ถูกใช้) แล้วฝัง fonts + html2pdf + payload เป็นไฟล์เดียว.
ออปชั่น: `--no-embed-pdf` (ใช้ CDN, ไฟล์เบา) · `--no-embed-fonts` (ใช้ Google Fonts, ต้องมีเน็ต).

### 6) ตรวจเร็ว
เปิดไฟล์ render ดู: nav สลับหน้า, 👁 เปิดภาพไฮไลต์, ปุ่ม data sample, ติ๊กผล, preview/PDF.
(ตรวจด้วยการ "เปิดไฟล์/screenshot" — **ห้าม cat ไฟล์ผลลัพธ์** เพราะมี base64 ใหญ่มาก)

### 7) ส่งมอบ
`present_files` ไฟล์ HTML เดียว. ไม่ต้องโพสต์เนื้อ base64 ใด ๆ.

---

## ไฟล์ในสกิล
```
scripts/
  capture.py     # ENGINE: render + spotlight highlight + optimize  -> shots_b64.json
  build.py       # ENGINE: merge cases+shots, dedup, inject fonts/pdf/payload -> 1 HTML
  make_fonts.py  # (ออปชั่น) subset TTF -> assets/fonts_b64.json ใหม่
assets/
  template.html      # template หลัก (placeholder __PAYLOAD__/__PDFLIB__/__FONT_NOTO__/__FONT_INTER__)
  html2pdf.min.js    # library ทำ PDF (ฝังตอน build)
  fonts_b64.json     # Noto Sans Thai + Inter (woff2 subset, base64) — ฝังตอน build
  fonts/             # noto.woff2, inter.woff2 (ต้นฉบับ subset)
  lucide.umd.js      # ใช้ตอน capture เพื่อ render ไอคอน Lucide ของ prototype
references/
  cases-schema.md  shot-spec-schema.md  iron-rules.md
  md-to-cases-mapping.md   # ★ ตารางแปลง testcases-*.md → cases.json (Pipeline Mode)
examples/F-91/
  cases.json  shot-spec.json  shots_b64.json  README.md   # ตัวอย่างครบ + build ได้ทันที
```

## หมายเหตุ environment
- ต้องมี `playwright` (chromium) + `Pillow` สำหรับ capture; `fonttools`+`brotli` เฉพาะถ้าจะ rerun make_fonts
- ขนาดไฟล์ผลลัพธ์ ≈ ผลรวมภาพ + (html2pdf ~0.9MB ถ้าฝัง) + (fonts ~0.24MB ถ้าฝัง).
  ถ้าต้องการไฟล์เบา ใช้ `--no-embed-pdf`/`--no-embed-fonts` (แลกกับต้องมีเน็ตตอนเปิด)

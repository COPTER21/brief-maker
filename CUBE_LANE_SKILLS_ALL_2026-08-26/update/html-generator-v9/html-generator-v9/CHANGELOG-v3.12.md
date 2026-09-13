# html-generator-v3 — v3.12 (2026-07-01)

## เพิ่ม Iron Rules #38–#43 (37 → 43) + self-audit tooling

### Rules ใหม่
- **#38 Thai Vertical Rhythm** — element fix-height + ข้อความไทย ต้องไม่ลอยสูง (font metric ของ Noto Sans Thai เผื่อสระล่าง). nudge: `.btn 2px`, `.pill 4/3`, `.table td 13/11`. **ต้อง render จริงด้วยฟอนต์ไทยเทียบเส้นกึ่งกลางก่อน claim** (text-box-trim ยังรองรับแค่ Chrome 133+ จึงใช้ padding nudge).
- **#39 Empty State (always)** — list/section ที่ว่างได้ ต้องมี `emptyStateHTML()` (icon+title+desc+action) แยกเคส "ยังไม่มีข้อมูล" vs "filter ไม่เจอ".
- **#40 List Cell Atomicity** — 1 ข้อมูล = 1 คอลัมน์, ห้ามซ้อน sub-line ใต้ค่าหลัก (เกิน 8 คอลัมน์ → ตัดลง view drawer).
- **#41 List Row = view** — กดแถวเปิด view เสมอ, ไม่มีไอคอนดวงตา, action cell `stopPropagation()`. (Pattern E: กดแถว=expand inline ก็ไม่มี eye)
- **#42 Long-list UX** — `.table-scroll.is-sticky` (sticky header + **bg ทึบที่ th** กัน row ทะลุ — ทดสอบด้วย scroll จริง) + `.cell-truncate` (Thai-safe).
- **#43 Validation + Format** — `validateField()` (on-blur) + `.field-error` จองพื้นที่ (ไม่กระตุก) + `fmtNumber/fmtMoney/fmtDate/fmtDateTime` (th-TH) + `.num` tabular + `col-num` ชิดขวา.

### Tooling ใหม่
- `scripts/audit.sh <file.html>` — grep banned patterns (line-height:1 บนปุ่ม, eye, .content max-width, bare createIcons, console.log, localStorage, …). Exit 1 ถ้า FAIL.
- `scripts/render-check.py <file.html>` — screenshot ด้วย playwright เพื่อ verify visual (Thai rhythm / empty / sticky / ปุ่มเบี้ยว).

### แก้ของเดิม
- **Rule #36** — เปลี่ยนกลไกจัดกึ่งกลางปุ่มจาก line-height เป็น `padding-top:2px` (line-height:1 ตัดสระไทย). เพิ่ม `.btn-truncate .lbl` (truncate ที่ span ไม่ตัดสระ).
- **Pattern A** — รื้อตาม #40/#41: ชื่อ/บริษัท/อีเมล แยกคอลัมน์ (เลิกซ้อน uc-email), เอา eye ออก, row `.is-clickable`, sticky, empty state, fmtDate.
- **Pattern E** — เอาปุ่ม eye "ดูรายละเอียดเต็ม → drawer" ออก (ขัด premise "detail inline, no drawer").

### Verify
ทุก visual rule ผ่านการ render จริงด้วยฟอนต์ Noto Sans Thai (playwright) — ปุ่ม/pill/เซลล์เข้ากึ่งกลาง, sticky scroll ไม่ซ้อน, empty/validation ทำงาน.

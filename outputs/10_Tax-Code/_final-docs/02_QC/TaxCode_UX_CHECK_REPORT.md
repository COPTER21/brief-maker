# UX Check Report — Tax Code

- วันที่: 2026-08-05 · **Iteration: 2 (R2 — re-run gate หลังแก้ CI/density/column)**
- Generator spec: `html-generator-v7` · authoritative iron rules #1–#94 (Sync Read จาก `WF-01_Pipeline_SkillSet/WF_Pipeline_SkillSet/html-generator-v7/knowledge/`)
- ไฟล์ที่ตรวจ: `01_HTML/TaxCode.html` (2,840 บรรทัด, 130 KB)
- Route: `#/accounting/setup/tax-codes`
- Render env: `.venv` playwright 1.61 + chromium-headless-shell 1228 (ติดตั้งจริงในรอบนี้)

## Verdict: 🟢 PASS (0 warnings)

| BLOCK | WARN | INFO | NOT-CHECKED |
|---:|---:|---:|---:|
| 0 | 0 | 2 | 0 |

การแก้ CI/density/column ล่าสุดผ่าน gate — ไม่มีงาน UX ค้างก่อน coverage gate

---

## Mechanical / Geometry Evidence (นับสดรอบนี้ ไม่เชื่อ stamp)

- **`static_scan.py`:** hex ทุกตัวที่ใช้ **อยู่ใน ci-tokens whitelist v7** — รวม `#FF3B30`(4) `#FF9A1F`(4) `#111111`(5) และ blue `#1A5FCC`/`#E6F0FF` (= สี Info/Active ตาม CUBE design system ci-tokens.md บรรทัด 54 → **ไม่ใช่ violation**) · font stack = Satoshi/Noto Sans Thai (2 stack, ตรง) · px watchlist: drawer 920/680 ✓, modal 440 ✓, sidebar 232 ✓, shell 52 ✓, **legacy 540 = 0** · hash routing ✓, Esc handler ✓, backdrop ✓, scrollbar 5px ✓, ไม่มี localStorage
- **`self_audit.py` (independent recount):** **PASS — ทั้ง 26 counters = 0, font_count=8** · โดยเฉพาะ `hex_off=0`, `td_pad_fat=0`, `tbody_font_fat=0`, `custom_tabs=0`, `inline_layout=0`, `naked_hints=0`, `jargon_leak=0`, `duplicate_counts=0`
- **Stamp vs recount:** PREFLIGHT stamp ในไฟล์ (26 counters=0, font=8) **ตรงกับการนับสด 100%** — stamp เชื่อถือได้
- **Emoji:** static_scan เจอ ⚠/✅ 4 จุด — ทั้งหมดอยู่ใน **CSS/JS comment** (L387/392/600/1746) ไม่ใช่ UI → ไม่นับ

## Render Evidence (Pass R — ผ่าน, ภาพจริง)

ภาพใน `02_QC/ux-shots-R2/` (12 ไฟล์) — review ฉากหลัก:

| ภาพ | ตรวจ | ผล |
|---|---|---|
| `route_accounting_setup_tax-codes.png` | VAT list — CI color + density | ✅ sidebar Charcoal, accent/active/primary แดง `#FF3B30`, tab underline แดง, 8 คอลัมน์, แถวกระชับ **ไม่บวม** (แก้ BA "ใหญ่แปลก" แล้ว), pill สถานะ blue(ใช้งาน)/gray(ปิดใช้งาน) |
| `...__overlay_btn-primary.png` | create drawer 680 | ✅ ฟอร์ม grid 2 คอลัมน์ ไม่ซ้อนบรรทัด, GL ภาษีขาย+ซื้อ แยก field (direction=ทั้งคู่), footer ยกเลิก/บันทึกร่าง/ยืนยันสร้าง, focus ring แดง, ไม่มี hint รก, ไม่มี h-scroll |
| `...__tab1.png` | (คาดหวัง WHT) | render script คลิก tab ไม่ติด (ยังโชว์ VAT) — **ข้อจำกัด script ไม่ใช่บั๊ก HTML**; R1 ยืนยัน WHT tab = 5 แถวผ่าน browser แล้ว |

BA complaint (สี CI เพี้ยน / ขนาดใหญ่แปลก) → **ยืนยันด้วยตาว่าแก้แล้วจริง**: ไม่เหลือ `color-mix` drift, สี = token ตรง, density กระชับ

## R1 → R2 Diff

- **แก้แล้ว/ยังคงอยู่ ✓:** UX-01 (dropdown flip-up), UX-02 (selection column ถูกเอาออก — R2 ยืนยัน 8 คอลัมน์ ไม่มี checkbox), UX-03 (semantic filter pickable/attention — KPI 9/7/2/8 ตรง)
- **remaining:** 0
- **โผล่ใหม่:** 0 BLOCK / 0 WARN
- **การเปลี่ยนแปลงระหว่าง R1→R2 (CI/density/column) ที่ verify เพิ่ม:** color-mix ออกหมด, `--row-h:44px --fs-table:12.5px` padding 8×12, tab 36px, ตาราง 9→8 คอลัมน์ (ย้าย "การใช้งาน" ไป View Drawer + KPI) — ทั้งหมดผ่าน mechanical + visual

## ℹ️ INFO (ไม่บล็อก)

1. `.dot.is-active` (L714) ใช้ box-shadow `rgba(37,99,235,…)` = `#2563EB` ซึ่งเป็น blue คนละเฉดกับ token `#1A5FCC` — เป็น shadow tint ของ dot เล็ก ๆ (ไม่ใช่ fill) self_audit ไม่จับเพราะเป็น rgba · consistency INFO เฉย ๆ แก้/ไม่แก้ก็ได้
2. Render script switch-tab / บาง interaction ข้าม (`Element not attached to DOM`) — เป็น timing ของ script ตัว SPA ทำงานปกติ (R1 ยืนยัน). ถ้าต้องการภาพ WHT list / view drawer / picker เพิ่ม ให้ capture เจาะจงอีกรอบได้

## NOT-CHECKED
- ไม่มี (mechanical + geometry + render ครบ)

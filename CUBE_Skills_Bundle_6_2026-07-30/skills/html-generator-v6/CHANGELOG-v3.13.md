# html-generator-v3 — v3.13 "Design Consistency Edition" (2026-07-06)

## เป้าหมาย: output ทุกไฟล์ต้องดูเป็นระบบเดียวกัน 100% — ยุบ source of truth ที่ชนกัน + ล็อกทุกอย่างที่เคยเป็น "ช่วง/แล้วแต่รอบ"

### แก้ Drift ที่ตรวจพบ
- **Drawer width unified** — ci-tokens / iron-rules #11-14 / skeleton เคยบอก 540px ขณะที่ DRAWER STANDARD v2 บอก 920/680 → ตอนนี้ 920px + `.drawer.standard` 680px ค่าเดียวทั้ง skill; audit.sh FAIL ถ้าเจอ 540px
- **component-catalog** — ตัด `sb-section/sb-section-title` (BANNED ตาม Rule #27) ออกจากรายชื่อ canonical
- **Microcopy ขัดกันใน Rule 31** — ปุ่ม primary create = `ยืนยันสร้าง` ค่าเดียว (เดิม 31.2 ใช้ "บันทึกและสร้าง")
- **README** — จำนวน rules 26 → 48

### Fixed Tokens (เลิกใช้ช่วง)
- Type scale: `--fs-h1 22 / --fs-h2 17 / --fs-h3 15 / --fs-body 14 / --fs-sub 13 / --fs-meta 12 / --fs-cap 11 / --fs-kpi 28`
- Spacing: `--sp-xs 4 / sm 8 / md 12 / lg 20 / xl 28` · Radius: `--r-xs 4 / sm 6 / md 8 / lg 12 / full 999`
- Icon size ต่อ context เป็นตารางตายตัว (chevron w-3 → empty state w-10)
- ทั้งหมดลง `:root` ใน skeleton แล้ว — feature CSS ห้ามพิมพ์ px ลอย

### Rules ใหม่ #44-#48
- **#44 Loading/Submitting** — disabled + loader-2 spin + "กำลังบันทึก…" + กัน double-submit + toast หลังปิด
- **#45 Disabled/Read-only + Form Section Grouping** — ฟอร์ม >6 fields แบ่งกลุ่ม, ลำดับกลุ่มมาตรฐาน
- **#46 Placement Contract ⭐** — ปุ่มสร้าง=`.ph-actions` ขวาสุดเท่านั้น · drawer primary ล่างขวาชิดขวา (sticky footer) · badge หลังชื่อห่าง 8px, pill เดียวระดับ header · list row action = pencil→trash-2 ลำดับตายตัว · edit drawer ไม่มีปุ่มลบ · ลบผ่าน confirm modal เสมอ · toast ขวาล่าง · search ซ้ายสุด filter bar
- **#47 Stepper Standard** — `.stepper/.step-dot/.step-label/.step-connector` component กลางใน skeleton, 2-5 steps, step สุดท้าย "ตรวจสอบและยืนยัน"
- **#48 Landing Standard** — 3 variants เท่านั้น (M1 Hero+Tiles / M2 Workspace Grid / M3 KPI Home), ห้าม carousel/banner

### ของใหม่
- `knowledge/microcopy.md` — คำมาตรฐานปุ่ม/toast/confirm/empty state + **Status Pill Vocabulary กลาง** (สถานะเดียว=label เดียว=สีเดียวทุกไฟล์) + format มาตรฐาน + คำต้องห้าม
- `patterns/J_dashboard-kpi-chart.md` — Dashboard J1/J2/J3 + SVG chart vanilla (สีซีรีส์ primary→teal→warning)
- `patterns/K_report-print.md` — Informative report + print CSS (@media print ซ่อน shell + หัวกระดาษ)
- `patterns/L_collection-views.md` — Card grid / Kanban / Timeline
- `patterns/M_landing-home.md` — Landing 3 variants
- Stepper CSS ลง skeleton

### Tooling
- `audit.sh` เพิ่ม: FAIL 540px, FAIL sb-section, FAIL carousel, WARN hardcoded font-size, WARN helper ซ้ำ, WARN submit ไม่มี loader, WARN stepper ไม่ใช้ component กลาง

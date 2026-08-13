# HTML Generation Log · Sales Territory

วันที่สร้าง: 2026-08-13  
Skill: `html-generator-v8`  
Mode: Standalone/Pipeline partial (PREBRIEF + Function Checklist + HTML prototype)  
Output: `sales-territory.html`

## Source priority

1. `f-territory.html` — source of truth ด้าน UI และ behavior
2. `PREBRIEF_F-SALES-TERRITORY.md` — business rules, scenarios, data และ edges
3. `FUNCTION_CHECKLIST_F-SALES-TERRITORY.md` — function coverage
4. `Central Plan v2` — ทิศทางการเชื่อมข้าม feature เท่านั้น
5. คำยืนยัน PM/BA — Sales Team/Salesperson, Customer Master, Sales Order, Sales Target และ Visit Operation ยังไม่มี ให้เตรียม future hooks/mock โดยไม่สร้าง hard dependency

## Page and pattern inventory

| ส่วน | Pattern | สถานะ |
|---|---|---|
| ทะเบียนเขตและตัวกรอง | A · List view | ครบ |
| สร้าง/แก้ไข Route | B · Create/Edit drawer | ครบ |
| ดู Route แบบ view-first | C · View drawer | ครบ |
| ยืนยันเก็บเข้าคลัง | D · Confirmation modal | ครบ |
| ภาระงานเซลส์ | Dashboard/table view | ครบ |
| แผนที่ประเทศไทย offline | Interactive SVG dashboard | ครบ |
| Sidebar ERP | N · Module/Feature shell | ปรับตาม v8 |

## Coverage map

| Coverage | สิ่งที่ตรวจ | Evidence ใน HTML | ผล |
|---|---|---|---|
| FN-01–04 | สร้าง/แก้ Route, รหัสล็อก, format/unique validation | `openCreate`, `openEdit`, `save`, `fld-code` | ครบ |
| FN-05–07 | soft archive, เตือนจำนวนลูกค้า, restore | `openArchive`, `confirmArchive`, `restoreRoute` | ครบ |
| FN-08–11 | จังหวัด optional, ภาค, Salesperson combobox, inactive contract | `COMBOS`, `comboField`, form validation | ครบด้วย mock; inactive behavior เป็น AI-DEFAULT |
| FN-12–16 | workload รวมหลายเขต, universe ว่าง, snapshot copy, coverage, utilization | `workloadBody`, `routeStats` | ครบด้วยข้อมูล mock/read-only |
| FN-17–18 | append-only audit, view-first, future handoff, Esc chain | `pushAudit`, row click, drawer actions, keydown | ครบใน prototype |
| FN-19–24 | offline map, hover, pin, filter region, unmapped list, mouseleave | `mapBody`, `mapPanel`, `mapHover`, `mapSelect` | ครบ |
| FN-90 | ค้นหาและกรองสถานะ | `filtered`, `setQ`, `setStatus` | ครบ |

## Future integration hooks

Feature ต่อไปนี้ยังไม่มีตามคำยืนยัน PM/BA จึงไม่มี API call หรือ hard dependency ใน HTML:

- Sales Team / Salesperson — ใช้ `SALESPERSONS` mock และ candidate shape `id/name/team/role/cap`; endpoint ยังไม่ยืนยัน
- Customer Master — ใช้ `CUST` mock เพื่อแสดงจำนวนลูกค้าและ coverage; ปุ่มปลายทางแจ้งว่ายังไม่พร้อม
- Sales Order — ใช้ `orders90` mock แบบ read-only
- Sales Target — เตรียมมิติ Route/Salesperson ในข้อมูล แต่ไม่มีปุ่มหรือ flow ใหม่เพราะ source ไม่ระบุ UI
- Visit Operation — ปุ่ม future handoff ใน view drawer แจ้งว่ายังไม่พร้อม

## [AI-DEFAULT] / gaps awaiting PM/BA

- สิทธิ์หัวหน้าขายและการจำกัดข้อมูลของพนักงานขาย (OQ-02)
- พฤติกรรมเมื่อ Salesperson ถูกปิดใช้งาน (OQ-03)
- เกณฑ์ coverage สี 25% (OQ-04)
- capacity ต่อบทบาท (OQ-06)
- Route type 10 แบบ (OQ-07)
- UI ประวัติรอ Audit Trail กลาง (OQ-08)
- การยอมให้พื้นที่ซ้อนกัน (OQ-09)
- choropleth/route line และ GPS ลูกค้าอยู่นอก scope (OQ-10/OQ-11)
- ที่อยู่ geo dataset ตอน implement จริง (OQ-12)
- จังหวัดเดียวมีเขตต่างภาคใช้สีของเขตแรก (OQ-13)

## Conflict and drift decisions

- PREBRIEF §1 มีข้อความเก่าว่า “ไม่มีแผนที่ในรอบนี้” แต่ OB-11, §2A, Function Checklist และ HTML source ระบุแผนที่เป็นแท็บที่ 3 จึงยึดหลักฐานล่าสุดและ HTML source: มีแผนที่
- Comment เก่าใน HTML ที่ระบุว่าตัดแผนที่ถูกแก้ให้ตรง behavior จริง
- Comment เก่าที่กล่าวถึงหลายคน/ทั้งทีมถูกลบ เพราะมติคือ 1 เขตต่อพนักงานขาย 1 คน
- ไม่มี PDF generation ใน feature นี้ จึงไม่เรียก `thai-doc-pdf-generator`

## v8 compliance changes

- เพิ่ม Module/Feature sidebar structure และ `data-module`/`data-feature`
- เพิ่ม `body min-width:768px`, scrollbar styling, z-index registry และ list full-height behavior
- ปรับ drawer header/footer action placement, status pill และ view footer
- เพิ่ม submitting state สำหรับ create/edit/archive
- คง master combobox แบบ portal พร้อม keyboard/Esc/outside-click
- ปรับ tabs เป็น kit classes, table density, spacing/type scale, no inline layout และ preflight stamp
- future handoff เปลี่ยนจากข้อความเสมือนเปิด feature เป็นข้อความแจ้งว่ายังไม่พร้อม

## Verification

| Check | Result |
|---|---|
| `self_audit.py` | PASS — ทุก counter = 0; font sizes 8 |
| `audit.sh` | PASS hard gate — FAIL=0, WARN=1 (script เตือน hardcoded font-size แม้ค่าทั้งหมดอยู่ใน allowed type scale) |
| Render 1440×900 | PASS visual inspection — shell, KPI, tabs, filter, table และ Thai labels ปกติ |
| Render 1024×768 | PASS visual inspection — content/table อยู่ใน viewport และ scroll ภายใน; ไม่มี body overflow ที่เห็น |
| HTML parse/runtime | PASS โดย render-check; หน้าเปิด route `#/sales-territory` สำเร็จ |

ภาพตรวจถูกแยกออกจาก deliverable และเก็บที่ `../../test-artifacts/05_Sales_Territory/render-1440.png` และ `../../test-artifacts/05_Sales_Territory/render-1024.png`.

## PM/BA feedback — Central Area Route mock (2026-08-13)

- Source/Central Plan search found no existing Area Route whose `region` is `ภาคกลาง`; existing `R-NP-03`/`R-SP-02` are explicitly west labels and Bangkok KAM rows use `ส่วนกลาง / ออนไลน์`, so none were relabeled.
- Reused exact available anchors from source: province `กรุงเทพมหานคร` in the embedded central-province dataset and salesperson `เอก ทวีสุข` from `ทีมขาย GT ภาคกลาง-ตะวันตก`.
- Added minimal `[AI-DEFAULT]` mock: `R-BK-01` · `กรุงเทพฯ ชั้นใน สาย 1` · Area Route (GT) · `ภาคกลาง` · `กรุงเทพมหานคร` · `เอก ทวีสุข` · universe 30; read-only Customer/Sales Order mock = F4 1, F2 2, F1 1, orders90 325,000.
- **PM/BA confirmation needed:** confirm Route code/name, universe/customer frequencies/orders90 and whether `ภาคกลาง` should remain a distinct selectable region alongside `ส่วนกลาง / ออนไลน์`. These values are prototype mock only and not a production master-data decision.

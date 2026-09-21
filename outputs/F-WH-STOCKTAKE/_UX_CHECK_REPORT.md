# UX Check Report — F-WH-STOCKTAKE

- วันที่: 2026-09-20 · Iteration: 3 (Manual Test layout re-gate)
- Generator spec: `html-generator-v9` (Sync Read จาก skill ใน workspace)
- Passes run: Node syntax · `audit.sh` · `static_scan.py` · `self_audit.py` · Render Gate · viewport 1024 · E2E runtime 20 cases
- ไฟล์ที่ตรวจ: `F-WH-STOCKTAKE.html` (single-file SPA)

## Verdict: 🟢 PASS with 1 warning

| BLOCK | WARN | INFO | NOT-CHECKED |
|---:|---:|---:|---:|
| 0 | 1 | 2 | 0 |

`audit.sh`: FAIL 0 · WARN 1 · `self_audit.py`: PASS ทุกตัวนับ · E2E 20/20 · browser console error 0

## Manual Test layout re-gate

- UI-01: footer แท็บ “ใบนับ” ใช้ `.table-actions` แบบ flex และเว้นปุ่ม “สแกน”/“ส่งผลนับ” 8px; regression probe วัดได้ผ่าน
- UI-02: “ส่งต่อใบปรับยอด” ในแท็บ “ประวัติ” เปลี่ยนจาก `.card` ซ้อน `.card` เป็น flat section `.history-handoff` คั่นด้วยเส้นและช่องไฟ
- พิสูจน์ก่อนแก้: UI-01 วัด gap ได้ 0px และ UI-02 พบ `.card section-pad` ซ้อนกัน 1 จุด; หลังแก้ทั้งสองเคส PASS
- SEC-01: ใบนับแสดงช่องกรอก/ปุ่มส่งเฉพาะ persona ที่ได้รับมอบหมาย และ `submitCount()` guard ตัวตนซ้ำอีกชั้น; คนอื่นเรียกตรงก็เปลี่ยนสถานะไม่ได้

## PM/BA feedback re-gate

- FIX-01–03: function guards ผ่าน B1/B2/B3; freeze/handoff/approval bypass ไม่ได้
- FIX-04: ตารางแสดงมูลค่าส่วนต่าง; 25,000 บาท resolve 2 ขั้นและอนุมัติ P3 → P4 ทีละขั้น
- FIX-05: handoff เก็บ payload รายบรรทัด + F082 ack และแสดงในประวัติ
- FIX-06: `STOCKTAKE_LOCKS` แสดง “พื้นที่ถูกล็อก” และปลดเฉพาะ rejected/closed
- FIX-07: มี F089 scan surface และ CSQ anchors สอง event
- FIX-08: persona switch เป็น `.demo-only`; inject hide แล้ว action/layout หลักยังอยู่

## 🟡 WARN

### UX-01 · CI token hygiene · CSS line 2

- **พบ:** ยังมี `font-size` แบบ px ตรงใน BASE CSS เช่น `.brand`, `.ph h1`, `.stat strong` และ label ขนาดเล็ก แม้ค่าที่ใช้สอดคล้องกันทั้งหน้า
- **ผลกระทบ:** ไม่กระทบการใช้งานหรือ geometry แต่ควรรวมเป็น typography variables เมื่อ BASE-KIT กลางประกาศ scale ชุดถัดไป
- **แก้ภายหลัง:** เปลี่ยนเป็น token กลางโดยไม่เปลี่ยนขนาดที่ render; ไม่ควรสร้าง token feature-local เพิ่มเองในรอบนี้

## ℹ️ INFO

- `#/rounds` ใช้โครง `.page-fill > .toolbar > .search-box + select 200/180px > .table-wrap > .table-foot`; ภาพ `route_rounds.png` และ `viewport-1024.png` ไม่พบการล้นหรือแนวเบี้ยว
- `#/create` ใช้ drawer 920px, backdrop, footer actions, searchable location combobox และ Esc/backdrop close; ภาพ `route_create.png` กับ `route_create__overlay_btn-primary.png` ผ่าน visual review

## Checks ที่ผ่าน

- Lane rules #104–#106: tab row อยู่ใต้ page header, persona switch มี `data-demo="persona-switch"` + badge DEMO, toolbar เป็น block มาตรฐาน
- State/interaction: empty, validation error, disabled/loading submit, toast, confirmation modal, Esc chain และ backdrop close มีครบ
- Layout: inline layout 0, spacing/font/hex drift 0, z-index ใช้ registry, table density compact, numeric cells ชิดขวา
- Security/role UX: counter ไม่เห็นยอดตั้งต้น/ผลต่าง; supervisor เปิดดูได้
- Document archetype: N/A — feature นี้เป็น operational master flow ไม่ใช่ Pattern Q และไม่มี printable document
- Render evidence: `_shots/route_rounds.png`, `_shots/route_create.png`, `_shots/route_rounds__tab0.png`, `_shots/viewport-1024-feedback.png`, `_e2e/shots/stocktake-boundary.png`, `_e2e/shots/ui-count-actions.png`, `_e2e/shots/ui-history-handoff.png`

## Loop Diff

| สถานะ | รายการ |
|---|---|
| ✓ แก้แล้ว | PM/BA FIX-01 ถึง FIX-08 |
| ✓ แก้แล้ว | Manual Test UI-01 ปุ่มชิด และ UI-02 card ซ้อน |
| ✓ แก้แล้ว | SEC-01 คนอื่นส่งผลนับแทนผู้ได้รับมอบหมายไม่ได้ |
| ⏳ ค้างแบบไม่ block | FIX-09 typography token warning |
| 🆕 ใหม่ | ไม่มี |

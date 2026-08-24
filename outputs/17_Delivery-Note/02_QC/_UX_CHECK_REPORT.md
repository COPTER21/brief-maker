# UX CHECK REPORT — F-WH-DN Delivery Note

**รอบตรวจ:** Fresh gate หลัง Step 1 · 20 สิงหาคม 2569  
**ไฟล์ตรวจ:** `outputs\17_Delivery-Note\f-wh-delivery-note.html`  
**Verdict:** **PASS WITH WARNINGS** — ไม่มี defect ระดับ BLOCK และไม่มี undefined handler

## 1. ผลตรวจที่ยืนยันแล้ว

| Check | ผล | Evidence |
|---|---|---|
| เปิดหน้า list ที่ 1440×1000 | PASS | `02_QC/step1-render.png` |
| Render route + row overlay ที่ 1440×900 | PASS | `02_QC/ux-shots/route_list.png`, `route_list__overlay_tbody tr.png` |
| Iron Rules audit | PASS | `FAIL=0`, `WARN=3` |
| Handler integrity | PASS | `undefined_handlers=0` |
| Stock Transfer เป็นงานอ้างอิงจริง | PASS | HTML บรรทัด 922, 988, 1006; แถว `PACK-2026-0460 / TR-2026-0012` ในภาพ |
| รวมหลาย SO เฉพาะลูกค้าและที่ส่งเดียวกัน | PASS | HTML บรรทัด 1031–1033 และ guard ใน `openCreateConfirm()` |
| Manual แยกจาก reference | PASS | HTML บรรทัด 1291, 1326–1360 |
| Manual เปลี่ยนได้ทุกสถานะพร้อมเหตุผล | PASS | HTML บรรทัด 1316, 1357–1367 |
| A4 printable | PASS | `06_PRINT/DN_sample.pdf`, ภาพ `02_QC/dn-a4-preview.png` |

## 2. Warnings ที่รับไว้โดยตั้งใจ

| ID | Finding | การตัดสินใจ |
|---|---|---|
| UX-W01 | Row action ใช้ไอคอน eye ซ้ำกับการกดทั้งแถว | Inherited จาก seed; ไม่กระทบ task completion และ PM/BA กำชับให้คง UI เดิม |
| UX-W02 | Print-preview CSS เดิมมี hardcoded font sizes/colors และ inline layout จำนวนมาก | Inherited BASE-KIT/seed debt; การแก้ทั้งหมดเป็น redesign ไม่ใช่ surgical change |
| UX-W03 | Stepper เดิมไม่ได้ใช้ `.step-dot` กลาง | Inherited จาก seed; ไม่มี geometry break ในภาพจริง |
| UX-W04 | `self_audit.py` รายงาน token/inline-style/custom-tab debt เดิม | ไม่ถือเป็น feature defect รอบนี้ เพราะ baseline ก่อนแก้ก็ FAIL กลุ่มเดียวกัน; audit หลักผ่าน `FAIL=0` |

## 3. การตรวจด้วยตา

- Layout ไม่ล้นแนวนอนที่ desktop 1440px; sidebar, header, filter, table และ footer อยู่ใน viewport
- ปุ่ม `สร้างแบบ Manual` แยกจากปุ่มอ้างอิง `ออกใบส่งของ` ชัดเจน
- Stock Transfer แสดง `WH-01 → WH-02`, เลข TR และปลายทาง โดยไม่ปลอมเป็นลูกค้า
- Modal แถวงานอ้างอิงมี backdrop, close action และปุ่มหลักครบ
- A4 มีหัวเอกสาร รายการ สรุป และลายเซ็น 4 ฝ่ายครบในหน้าเดียว

## 4. Fresh-check commands

```powershell
.tools\bash.cmd .agents/skills/html-generator-v8/scripts/audit.sh outputs/17_Delivery-Note/f-wh-delivery-note.html
.tools\python.cmd .agents\skills\html-generator-v8\scripts\self_audit.py outputs\17_Delivery-Note\f-wh-delivery-note.html
.tools\python.cmd .agents\skills\qc-ux-html-checker\scripts\static_scan.py outputs\17_Delivery-Note\f-wh-delivery-note.html
.tools\python.cmd .agents\skills\qc-ux-html-checker\scripts\render_shots.py outputs\17_Delivery-Note\f-wh-delivery-note.html outputs\17_Delivery-Note\02_QC\ux-shots
```

ไม่มีรายการแก้ค้างที่เป็น defect ของ Delivery Note รอบนี้; warnings ทั้งหมดเป็นข้อสังเกตต่อ seed/BASE-KIT ที่ต้องแยกจัดการ ไม่แก้ปนใน feature นี้

## 5. Fresh recheck หลัง manual-test feedback

- แก้ไอคอนปุ่ม Manual ให้ render เป็น SVG จริง และเพิ่ม shared check จับ Lucide placeholder ที่ว่าง
- เพิ่มคำอธิบายว่าช่องลูกค้า reference มาจาก SO และต้องแก้ที่เอกสารต้นทาง
- Refresh จาก route รายละเอียดกลับ `#/list` และปิด drawer
- Manual `failed` สร้าง attempt ครั้งที่ 1; ไม่แสดงครั้งที่ 0
- Iron Rules audit: `FAIL=0` · E2E: `16/16` · console errors: `0`

## 6. PM/BA refinement — transport assignment

- Confirm-create และ draft drawer ใช้ search dropdown สำหรับผู้รับผิดชอบ ผู้ขนส่ง รถ และคนขับ
- ผู้รับผิดชอบค้นได้จาก `PEOPLE` ซึ่งเป็นพนักงานบริษัทเท่านั้น ไม่มีตัวเลือกกรอกเอง
- รถมีตัวเลือก `กรอกเลขรถเอง`; คนขนส่งมีตัวเลือกกรอกชื่อ นามสกุล และเบอร์โทร พร้อม validation
- ค่าที่กรอกเองแสดงต่อใน DN, dispatch summary และเอกสารพิมพ์
- Fresh gate หลังแก้: `WF 34/34` · E2E `17/17` · console errors `0` · Iron Rules `FAIL=0`

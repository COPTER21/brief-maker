# 00_OVERVIEW — F-TMP-002 บันทึกภายใน (Internal Memo)

## Document Control
| หัวข้อ | ค่า |
|---|---|
| Feature ID | F-TMP-002 *(รหัสชั่วคราว — ต้องจองรหัสจริงใน FEATURE_REGISTRY)* |
| ชื่อ | บันทึกภายใน (Internal Memo) |
| Module / Area | HR · เอกสารภายใน |
| แบบพิมพ์ต้นทาง | FM-HRM-54 · Rev.00 : 01/07/2569 |
| Pack Variant | **FULL** (fallback จาก BRD: pages=4, states=5, approval=Yes) |
| Input | `PREBRIEF_REQ-TMP-002_v2.md` · `FORM_SPEC.json` · `DECISIONS.lock.json` · `BRD_F-TMP-002.md` · prototype `feature.html` |
| Scope Lock | `DECISIONS.lock` (REQ-TMP-002) — มติทุกข้อ **AI-DEFAULT** รอลูกค้ายืนยัน |
| Prototype | `feature.html` (html-generator-v9.3 · archetype `Q-form`) |
| Version | v1.0 · 2026-10-07 |

## Scope
สร้าง · แก้ร่าง · ส่งอนุมัติ · พิจารณา · ยกเลิก · พิมพ์ บันทึกภายในตามแบบ FM-HRM-54 แบบช่องตรงกระดาษ 1:1
**ไม่อยู่ใน scope:** เปลี่ยนค่าในระบบเมื่ออนุมัติ · ส่งต่อระบบอื่น · ทำซ้ำ · ประกาศ (ดู 07_LOCKED_DECISIONS)

## Roles
| Role | ความหมาย |
|---|---|
| ผู้จัดทำ | พนักงานที่สร้างบันทึก (owner ของ record) |
| ผู้พิจารณา | ผู้ที่ถูก resolve เข้า `approval_chain` ตามขั้นที่ตั้งใน DOA กลาง (ค่าเริ่ม `role-compliance` = ฝ่ายกฎหมาย) |
| ผู้ดูแลทะเบียนเอกสาร | admin role ของหน่วยงานเจ้าของเอกสาร — เห็นทุกใบ · ยกเลิกได้ |

## Dependencies
- HR · Employee (อ่านอย่างเดียว — ยังไม่มีรหัส feature ใน FEATURE_REGISTRY)
- F-DOCCFG (doc_type `MEM` · เลขรัน · print_config) — `DOCCFG_BRIEF_F-TMP-002.md`
- DOA กลาง F-DLG-001 — `DOA_BRIEF_F-TMP-002.md` (`wire_status: pending`)
- ENG-NOTIFY — `NTF_BRIEF_F-TMP-002.md`
- F185 Master Document — `MDOC_BRIEF_MEM.md`

## คำถามค้าง (ต้องให้คนตอบก่อน UAT)
1. มติ 15 ข้อเป็น AI-DEFAULT ทั้งหมด — รอลูกค้ายืนยันในใบลงนาม
2. `role-legal` ไม่มีใน `doa-roles-contract.md` → ใช้ `role-compliance` แทนชั่วคราว
3. `class_code` / `function_code` ใน MDOC เลือกเองเพราะไม่มี Taxonomy Master ในชุดงานนี้
4. กระดาษไม่มี ☐ อนุมัติ/ไม่อนุมัติ — คำตัดสินบนแบบพิมพ์เป็นสิ่งที่ระบบเพิ่ม (DEC-07)

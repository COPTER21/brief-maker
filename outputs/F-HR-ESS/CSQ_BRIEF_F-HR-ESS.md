# CSQ_BRIEF — F-HR-ESS · พนักงานทำเอง (F059 · ESS Portal)

> ที่มา: BA Phase A (`Pack Brief Feature/F-HR-ESS/5_DECLARATIONS/CSQ_BRIEF.md`) — csq ไม่มี runnable skill จึงคัดมาไว้ในแพ็ก output ตามมติผู้ใช้ (ntf + csq per PREBRIEF §12)

## Declared Events
| event_id | trigger | ท่อ | เงื่อนไข | payload |
|---|---|---|---|---|
| ess.self_access | พนักงานเปิดดูข้อมูลตัวเอง (สลิป/ลา/OT/เบิก… S-10·BR-06) | **SecC** | การเข้าถึงข้อมูลส่วนบุคคลของตัวเอง (self-access log) | ref:employee_id · surface(payslip/leave/…) · action(view) |

## ไม่ประกาศ: OC(OP) · DC-เอกสาร+doa_*(ไม่มี DOA) · AC/FC(ไม่ลงบัญชี/เงินสด · portal อ่านอย่างเดียว) · SC(สงวน)

## หมายเหตุ: ESS ไม่ประกาศ event ของ feature ต้นทางซ้ำ (payslip/leave/expense event ประกาศแล้วในแต่ละ feature) — ประกาศเฉพาะ self-access ของ portal

## ⚠️ OQ-ESS-01 (รอเคาะก่อน dev wire SecC) — ต้องเคาะโดย PM/BA + Architect + ENG-CSQ owner
event_id ในใบประกาศนี้ = `ess.self_access` (1 event รวม) แต่ HTML/FRD วาง anchor ไว้ **2 จุดแยก**:
- `ess.access_denied` — modal 403 (เข้าถึงข้อมูลคนอื่น → ปฏิเสธ) · ess.html L2657
- `ess.restricted_view` — เปิดดูข้อมูล RESTRICTED (สลิป/เลขบัตร/บัญชี) · ess.html L2534

→ ต้องเคาะว่าท่อ SecC รับ **1 event รวม** (`ess.self_access`) หรือ **2 event แยก** (access_denied + restricted_view) ก่อน dev ตั้งค่าจริง · รายละเอียดใน `FRD_F-HR-ESS_Pack/05_RULES.md §5.7` · **ห้ามประกาศท่อ OC/DC ซ้ำ**

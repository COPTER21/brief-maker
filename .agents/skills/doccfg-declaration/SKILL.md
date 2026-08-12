---
name: doccfg-declaration
description: >
  Companion skill ฉีด context เรื่อง Document Configuration (F-DOCCFG — Document Type Master กลาง:
  เลขรัน + snapshot policy) ตอนทำ FRD/HTML ของ feature ที่ออกเอกสาร (QT/SO/PICK/PACK/DLV/INV/RV/
  CN/DN/JE/PR/PO/GRN) แล้วออก DOCCFG_BRIEF_[F-xxx].md = ใบประกาศ doc_type ที่ระบบใช้ auto-register
  ลง Document Configuration ตอน deploy — feature ประกาศเท่านั้น ห้าม hardcode เลขรัน/รูปแบบเลข/logic
  เก็บสำเนา: เลขทุกใบจาก ENG-DOC-NUM.next() สำเนาทุกใบจาก ENG-DOC-STORE.store() ซึ่งอ่าน config
  จาก F-DOCCFG เท่านั้น ใช้เมื่อ user พูดถึง "doccfg-declaration", "ทำ DOCCFG brief", "ประกาศ doc type",
  "register เอกสาร", "เลขรันของ feature", "running number", "ผูก document configuration",
  "ตั้งเลขเอกสาร", "declare doc type", "เตรียม doc config entry" — และใช้อัตโนมัติทุกครั้งที่รัน
  frd-generator กับ feature ที่ออกเอกสารธุรกรรม แม้ไม่เรียกชื่อ skill ★ companion (Sync Read F-DOCCFG)
  — ตระกูล declaration: doa / ntf / doccfg
---

# doccfg-declaration — ใบประกาศ Document Type → Document Configuration

## เมื่อไหร่ต้องรัน
1. Feature สร้าง**เลขเอกสาร**ใหม่ (มี running number ของตัวเอง) — บังคับ
2. Feature **generate เอกสาร/PDF** ที่อาจต้องเก็บสำเนา (ส่งลูกค้า / e-Tax / อนุมัติแบบมีลายเซ็น)
3. Feature enhancement ที่เพิ่มเอกสารประเภทใหม่ให้ feature เดิม

## Input
- FRD Pack ของ feature (03_LOGIC: state ไหนออกเลข/ออกใบ · 05_RULES) หรือ PREBRIEF (โหมด early-draft)
- **Registry ปัจจุบันจาก F-DOCCFG** (`f-doccfg.html` → TYPES + FMT_PRESETS) — Sync Read ห้าม copy ค้าง
- มติกลาง: preset 7 แบบ · scope 2 (global/branch) · no-gap · snapshot 2 events (sent_external / approved_final)

## ขั้นตอน
1. อ่าน FRD → list เอกสารที่ feature ออก (บาง feature ออกหลายประเภท เช่น Sales ออก QT+SO)
2. **เช็คชนกับ registry เดิม** — code ซ้ำ = ใช้ entry เดิม (ห้ามประกาศใหม่) · ความหมายซ้อน (เช่นจะสร้าง "ใบส่งของ 2") = BLOCK ให้ทีมเคาะก่อน
3. ต่อ doc_type ใหม่: กำหนด code (A-Z 2-5 ตัว unique), ชื่อไทย, module เจ้าของ, **default ตอน register**: preset เลขรัน + reset + scope + no-gap + snapshot flags (admin แก้ทีหลังได้ทุกค่า — default คือจุดเริ่มที่สมเหตุผลที่สุด)
4. ระบุ **trigger point การออกเลข**: state transition ไหนเรียก `ENG-DOC-NUM.next()` (มาตรฐาน: ตอน confirm/issue — ไม่ออกเลขตอน draft ถ้าเป็น no-gap) — อ้าง FRD §
5. ระบุ **trigger point snapshot**: event ไหนเรียก `ENG-DOC-STORE.store()` (map กับ 2 flags)
6. ออก `DOCCFG_BRIEF_[F-xxx].md` — ระบบใช้ auto-register ตอน deploy (XT-3 ของ F-DOCCFG)

## Output: DOCCFG_BRIEF_[F-xxx].md (โครง)
```md
# DOCCFG_BRIEF — F-SO-001 Sales Order
> Auto-register ลง Document Configuration ตอน deploy · admin ปรับค่าได้ทุกช่องหลัง register
> เลขทุกใบจาก ENG-DOC-NUM เท่านั้น · สำเนาทุกใบจาก ENG-DOC-STORE เท่านั้น — ห้าม hardcode

## doc_type ที่ประกาศ
| Code | ชื่อ | Module | Preset default | Reset | Scope | No-gap | Snap: ส่งออก | Snap: อนุมัติ+เซ็น |
|---|---|---|---|---|---|---|---|---|
| SO | คำสั่งขาย | SAL | {PREFIX}-{YYYY}-{run:4} | รายปี | global | ✗ | ✓ | ✗ |

## จุดออกเลข (ENG-DOC-NUM)
| เมื่อไหร่ | อ้าง FRD | หมายเหตุ |
|---|---|---|
| S: draft→confirmed | 03_LOGIC §2.1 | ไม่ออกเลขตอน draft (กันเปลืองเลข + รองรับ no-gap ในอนาคต) |

## จุดเก็บสำเนา (ENG-DOC-STORE)
| Event | เมื่อไหร่ | อ้าง FRD |
|---|---|---|
| sent_external | กด "ส่ง SO ให้ลูกค้า" (email) | 03_LOGIC §3.4 |

## Dev wiring note
- `so.number = ENG-DOC-NUM.next('SO', company_ctx)` ที่ transition ข้างบน — ห้าม format เอง ห้าม +1 เอง
- render PDF แล้วเรียก `ENG-DOC-STORE.store(pdf,'SO',so_id,'sent_external')` — engine เช็ค flag เองว่าเก็บหรือไม่
- ห้ามอ่าน/เขียนตาราง config ตรง — ผ่าน engine API เท่านั้น
```

## กติกาตายตัว (Iron)
1. **ห้าม hardcode**: รูปแบบเลข, การ +1 เลขรัน, เงื่อนไขเก็บสำเนา — ทั้งหมดอยู่ที่ F-DOCCFG ผ่าน engine
2. **Code unique ทั้งระบบ** — ชนกับ registry เดิม = ใช้ตัวเดิมหรือ BLOCK ให้เคาะ (ห้ามตั้งชื่อเลี่ยง)
3. **เลขเอกสาร immutable** — ออกแล้วห้ามเปลี่ยน/renumber ไม่ว่า config เปลี่ยนยังไง
4. **ไม่ออกเลขตอน draft** สำหรับเอกสารที่อาจเป็น no-gap (INV/RV/CN/DN/JE) — ออกตอน confirm/issue เท่านั้น
5. ทุก doc_type ต้องมีอย่างน้อย 1 จุดออกเลข · snapshot จะมีหรือไม่มีก็ได้ (ใบภายในล้วนไม่ต้อง)
6. ห้ามประกาศค่า "บังคับแก้ไม่ได้" — ทุก default ที่ให้ admin ต้องแก้ได้ที่จอ F-DOCCFG (มติ 2026-08-11)

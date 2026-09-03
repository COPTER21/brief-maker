# NOT_NEEDED — ท่อประกาศที่ **ไม่ต้องรัน** สำหรับ F-HR-CONFIG · HR Configuration

> S1.8 · 2026-08-28 · ตัดสินจาก `PREBRIEF.md` §12 (**authoritative**) ยืนยันด้วย `decl_rule.py` → `_lane/DECL.json`
> chip ใน `LANE_BRIEF.md` = `csq` ตัวเดียว · ตาราง CONTEXT_PACK/HR.md = `✓ SecC` เท่านั้น → **ตรงกันทั้ง 3 แหล่ง · DIVERGENCE: —**
> ท่อที่ต้องรัน: **CSQ เท่านั้น** → `CSQ_BRIEF.md` (SecC)

| ท่อ | skill ที่ไม่ได้รัน | สถานะ | เหตุผล (อ้าง PREBRIEF) | ถ้าเคาะกลับให้ทำอะไร |
|---|---|---|---|---|
| **DOA** ⚖ | `doa-declaration` | **NOT-NEEDED** | feature นี้ **ไม่มี action ส่งอนุมัติ/อนุมัติ/ไม่อนุมัติ เลย** — §5 state machine ไม่มี transition อนุมัติ · §6 ไม่มีปุ่มส่งอนุมัติ · **S-23 ประกาศชัดว่าไม่รองรับ** · scope note ของ CHECKLIST ระบุ "ไม่มี approval" (OB-07) · ไม่มีวงเงิน · การคุมการเปลี่ยนนโยบายใช้ `effective_date` + audit append-only แทน · มาตรฐาน D365/SAP มี workflow → **ยกเป็น [OQ-STD-01] ไม่ตัดเงียบ** | เพิ่ม `doa-declaration` (สาย HR Manager · ไม่มีวงเงิน) และผูก `GET /doa/resolve` ที่ transition **Draft → Scheduled จุดเดียว** — ห้าม hardcode chain · DOA engine จะยิง DC ระดับเอกสารให้เอง (ห้ามเพิ่ม `dc` ใน CSQ_BRIEF) |
| **NTF** 🔔 | `ntf-declaration` | **NOT-NEEDED** | ไม่มี transition ที่ต้องแจ้งคนนอก HR Admin **จาก feature นี้** — ผลกระทบถึงพนักงานเกิดที่ feature ปลายทาง (Leave · OT/Shift · Shift & Roster · Payroll ประกาศ event ของตัวเองอยู่แล้วตามตาราง CONTEXT_PACK) · ประกาศที่นี่ = **แจ้งซ้ำ** · §12 = no · **S-29 ไม่รองรับ** · [OQ-STD-05] | ออก `NTF_BRIEF` event `hrconfig.published` / `hrconfig.effective` (in-app + email ตาม ENG-NOTIFY default) — **ไม่ประกาศซ้ำ `doa_*`** |
| **DOCCFG** | `doccfg-declaration` | **NOT-NEEDED** | feature นี้ **ไม่ออกเอกสาร** — ไม่มีเลขที่เอกสาร/เลขรัน/สำเนา (PREBRIEF §7 ระบุ "เลขรัน/doc number: N/A — config ไม่ใช่เอกสาร") · ไม่มี doc_type ให้ประกาศ · §12 = no | ถ้าอนาคตออก "ประกาศนโยบาย HR" เป็นเอกสารทางการ → ออก `DOCCFG_BRIEF` doc_type `HRPOL-YYYY-NNNN` |
| **PDF DOC** 📄 | `thai-doc-pdf-generator` | **NOT-NEEDED** | ไม่มีเอกสาร/แบบฟอร์มที่คนถือ/ยื่น/พิมพ์ส่ง · ไม่มีช่องลายเซ็น · ไม่มี tab PDF Preview (§3, §6 · archetype = master/config ไม่ใช่ Pattern Q) · §12 = no | ถ้าอนาคตต้องพิมพ์ "ประกาศวันหยุดประจำปี" แจกพนักงาน → รัน `thai-doc-pdf-generator` (template.html + sample.pdf + print-spec.md แนบ FRD) |

## ท่อ 7C ที่ **ห้ามประกาศ** (ระบบ reject 422) — บันทึกไว้กันพลาดรอบหน้า
- **OC** — มาจาก Operation Process (`sow.*`) อัตโนมัติ · feature นี้ไม่สร้างงาน OP
- **DC ระดับเอกสาร** — มาจาก DOA engine · feature นี้ไม่มี approval อยู่แล้ว
- **SC** — สงวนไว้ (`trigger=false` เสมอ · OQ-C3 ยังไม่เคาะ)
- เหตุผลของ **EC / AC / FC** ที่ไม่ประกาศ อยู่ใน `CSQ_BRIEF.md` §3 (สรุป: ที่นี่เก็บ "อัตรา" ไม่ใช่ธุรกรรม — ประกาศ EC = นับซ้ำกับ OT/Leave/Payroll)

## สรุปสำหรับ REVIEW_SHEET
`need = csq (SecC)` · `not-needed = doa · ntf · doccfg · pdfdoc` · `divergence = —` · OQ ที่ผูกกับการตัดสินนี้: **OQ-STD-01 (approval)** · **OQ-STD-05 (แจ้งเตือน)**

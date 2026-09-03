# NOT_NEEDED — ท่อประกาศที่ **ไม่ต้องรัน** สำหรับ F-HR-SALSTRUCT · Salary Structure (โครงเงินเดือน)

> S1.8 · 2026-08-28 · ตัดสินจาก `PREBRIEF.md` §12 (**authoritative**) ยืนยันด้วย `decl_rule.py` → `_lane/DECL.json`
> chip ใน `LANE_BRIEF.md` = `csq` ตัวเดียว · POOL.json `declarations` = `csq:true` เท่านั้น · ตาราง `CONTEXT_PACK/HR.md` = `✓ EC/SecC` · `FEATURE_LIST_ALL.md` = `csq` → **ตรงกันทั้ง 4 แหล่ง · DIVERGENCE: —**
> ท่อที่ต้องรัน: **CSQ เท่านั้น** → `CSQ_BRIEF.md` (**EC + SecC** · 10 events)

| ท่อ | skill ที่ไม่ได้รัน | สถานะ | เหตุผล (อ้าง PREBRIEF) | ถ้าเคาะกลับให้ทำอะไร |
|---|---|---|---|---|
| **DOA** ⚖ | `doa-declaration` | **NOT-NEEDED** | feature นี้ **ไม่มี action ส่งอนุมัติ/อนุมัติ/ไม่อนุมัติ เลย** — §5.1/§5.2/§5.3 ไม่มี transition อนุมัติ · §6 ไม่มีปุ่มส่งอนุมัติ (แถวสุดท้ายระบุ ❌ ชัด) · **BR-21** · **S-36 ประกาศไม่รองรับ** · **FN-47 บังคับพิสูจน์ว่าไม่มีปุ่มในทุกหน้า** · ไม่มีวงเงิน · **scope note ตัดชัด**: "ไม่มี approval ในตัว — การปรับเงินเดือนอยู่ Employee Movement" · การเปลี่ยนอัตราคุมด้วย `effective_date` + `change_reason_code` + audit append-only แทน · มาตรฐาน D365/SAP มี workflow → **ยกเป็น [OQ-STD-01] ไม่ตัดเงียบ** | เพิ่ม `doa-declaration` **ที่ Employee Movement (W3) ไม่ใช่ที่นี่** · ถ้าเคาะว่าต้องมีที่นี่จริง → ผูก `GET /doa/resolve` ที่ transition **รอมีผล → ปัจจุบัน** จุดเดียว · ห้าม hardcode chain · DOA engine จะยิง DC ระดับเอกสารให้เอง (**ห้ามเพิ่ม `dc` ใน CSQ_BRIEF**) |
| **NTF** 🔔 | `ntf-declaration` | **NOT-NEEDED** | ไม่มี transition ที่ต้องแจ้งคนนอกทีม HR **จาก feature นี้** — การแจ้ง "เงินเดือนใหม่" ผูกกับ **คำสั่ง** ซึ่งเป็นของ **Employee Movement** (ประกาศ `✓` NTF อยู่แล้วในตาราง CONTEXT_PACK) · payslip เป็นของ **Payroll** · ประกาศที่นี่ = **แจ้งซ้ำ** · §12 = `no` · **[OQ-STD-08]** | ออก `NTF_BRIEF` event `salcomp.assigned` / `salstruct.effective` (in-app + email ตาม ENG-NOTIFY default) — **ไม่ประกาศซ้ำ `doa_*`** และต้องเช็คก่อนว่าไม่ชนกับ event ของ Employee Movement |
| **DOCCFG** | `doccfg-declaration` | **NOT-NEEDED** | feature นี้ **ไม่ออกเอกสาร** — PREBRIEF §7 ระบุ "เลขรัน/doc number: **N/A**" · ไม่มี doc_type ให้ประกาศ · เลขที่คำสั่งปรับเงินเดือน `MV-YYYY-NNNN` เป็นของ **Employee Movement** · หนังสือรับรองเงินเดือน `CERT-YYYY-NNNN` เป็นของ **หนังสือรับรอง (W3)** · §12 = `no` | ถ้าอนาคตออก "ประกาศโครงเงินเดือนประจำปี" เป็นเอกสารทางการ → ออก `DOCCFG_BRIEF` doc_type `SAL-YYYY-NNNN` |
| **PDF DOC** 📄 | `thai-doc-pdf-generator` | **NOT-NEEDED** | ไม่มีเอกสาร/แบบฟอร์มที่คนถือ/ยื่น/พิมพ์ส่ง · ไม่มีช่องลายเซ็น · ไม่มี tab PDF Preview (§6 ระบุ ❌ พิมพ์เอกสาร/PDF) · **archetype = master/config ไม่ใช่ Pattern Q** (STANDARD_BASELINE §3) · §12 = `no` | ถ้าอนาคตต้องพิมพ์ "ตารางโครงเงินเดือน" แจกผู้บริหาร → รัน `thai-doc-pdf-generator` (template.html + sample.pdf + print-spec.md แนบ FRD) · **แต่หนังสือรับรองเงินเดือนยังเป็นของ feature หนังสือรับรอง เสมอ** |

## ท่อ 7C ที่ **ห้ามประกาศ** (ระบบ reject 422) — บันทึกไว้กันพลาดรอบหน้า
- **OC** — มาจาก Operation Process (`sow.*`) อัตโนมัติ · feature นี้ไม่สร้างงาน OP
- **DC ระดับเอกสาร** — มาจาก DOA engine · feature นี้ไม่มี approval อยู่แล้ว
- **SC** — สงวนไว้ (`trigger=false` เสมอ · OQ-C3 ยังไม่เคาะ)
- เหตุผลของ **AC / FC / DC (terminal decision)** และของ **EC ที่ระดับโครง** ที่ไม่ประกาศ อยู่ใน `CSQ_BRIEF.md` §3 (สรุป: บัญชีเกิดที่ Payroll · งบเกิดที่ Manpower Planning · EC ยิงที่ระดับพนักงานเท่านั้นเพื่อกันนับซ้ำ)

## สรุปสำหรับ REVIEW_SHEET
`need = csq (EC + SecC · 10 events)` · `not-needed = doa · ntf · doccfg · pdfdoc` · `divergence = —`
OQ ที่ผูกกับการตัดสินนี้: **OQ-STD-01 (approval → Employee Movement)** · **OQ-STD-08 (แจ้งเตือน → ปลายทาง)** · **OQ-CSQ-01 (E10 view-restricted)** · **OQ-CSQ-02 (payload RESTRICTED)** · **OQ-CSQ-04 (EC ระดับโครง → Manpower Planning)**

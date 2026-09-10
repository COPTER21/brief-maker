# PROPOSALS_outbound — F-HR-EXPENSE (เบิกค่าใช้จ่าย · F101)

> ประเด็นที่ **feature นี้ตัดสินเองไม่ได้** — ต้องส่งกลับเจ้าของ feature/มติปลายทาง หรือ BA/SEC/Finance/Strike เคาะก่อน dev wire
> ปิดงาน 2026-09-10 · ผ่าน 12 step + BA review (10 FIX) + manual test (8 รอบ) + PM/BA OQ 3 ข้อ (เพิ่ม 3 จุดเชื่อม) + re-gate เขียวทุกด่าน (qc-ux PASS · coverage R1+R2 PASS · e2e 48/48)

---

## A. ข้อเสนอส่งออกไป feature/เจ้าของอื่น (outbound)

| # | ถึง | เรื่อง | สถานะปัจจุบันในงานนี้ | ต้องการ |
|---|---|---|---|---|
| **OB-PETTY-01** | Petty Cash (F091 · Finance · ยังไม่ dev) | F101 เพิ่ม **ช่องทางจ่าย "เงินสดย่อย"** เป็น hook display-only (ไม่ได้สร้างระบบ imprest) | จอทำ display-only (`payDownstream` → "เงินสดย่อย · hook F091 · Finance") · ไม่ execute จ่าย (BR-09) | wire ปลายทางจริงตอน F091 พร้อม |
| **OB-ADV-01** | Advance เงินทดรอง (F103 · Finance · ยังไม่ dev) | F101 เพิ่ม **"เคลียร์เงินทดรอง หักลบอัตโนมัติ"** soft-ref (ยอดจ่ายสุทธิ = ยอดรวม − ทดรองค้าง) display-only · F101 ไม่ออก/ไม่ปรับยอดทดรอง | `F103_ADVANCE_MOCK` mock ต่อผู้เบิก · ENG-EXP-02 advance-offset · ไม่แตะ ledger F103 | wire ค่าทดรองค้างจริง + ส่งค่าหักลบกลับ F103 ตอน F103 พร้อม |
| **OB-DOA-01** | เจ้าของ DOA master / พี่เบิร์ด / SEC | **`references/doa-contract.md` หายจาก skill install** → verify role-id ปลายทางไม่ได้ (G1 ตรวจไม่ได้) · HTML mock ใช้ชื่อตำแหน่งไทยล้วน (หัวหน้าสายงาน/ผจก.แผนก/ผอ.) **ไม่มี role-id เลย** | role-id ทั้งหมด `[DEFAULT—รอยืนยัน]` · HTML ใช้ `resolveDoa()` runtime ไม่ hardcode (G7 ผ่าน) · DOA entry เสนอ `DOA-EXP-CLAIM-001` | ยืนยัน (1) จำนวน FREE range + cut-points จริง (2) role-id จริงทุกขั้น (3) **🔴 CL-0013 สายผู้บริหาร แขวน 31 ส.ค.** — เพิ่มช่วงวงเงินสูง + slot ผู้บริหารไหม (4) DOA entry key |
| **OB-NTF-01** | F-NOTIFY | ทะเบียน event กลางไม่มีกลุ่ม HR/ค่าใช้จ่าย · 5 event `exp.submitted/approved/rejected/paid/overcap` ยังไม่ลงทะเบียน | ประกาศใน `NTF_BRIEF_F-HR-EXPENSE.md` เป็น feature-proposed · ไม่ hardcode · doa_*/FC-EC/pay-hook ไม่ re-declare | เพิ่มกลุ่ม "ค่าใช้จ่าย (HR)" + ยืนยัน exact event_id · **reconcile naming**: BA brief = 4 event snake_case (รวม `expense_result`) vs FRD/HTML = 5 event dotted (แยก approved/rejected) — เลือก canonical |
| **OB-BUD-01** | Budget Control (F117 · W7 ยังไม่ dev) + Welfare (F102) | จอมี hook display-only **ตรวจงบ F117 + สิทธิ์สวัสดิการคงเหลือ F102** (FIX-07 · Feature List F101 "c" รองรับ) | display-only mock (`F117_BUDGET_MOCK` / `F102_WELFARE_REMAIN`) · badge ที่มา | ยืนยันคง hook ไว้ (แนะนำคง — Central-Plan-backed edge) + wire ค่าจริงตอน dev |
| **OB-GL-01** | Accounting / Finance | จ่ายจริง + post GL = hook (BR-09) · A-EXP-02 contract | display-only "อ่านจากปลายทาง" · Expense ไม่จ่าย/ไม่ลงบัญชีเอง | contract จริง → FRD Phase B |
| **OB-EC-01** | Finance / Accounting | **reverse-EC / release-FC เมื่อยกเลิก/แก้ใบเบิกหลังอนุมัติ+FC/EC แล้ว** (กระทบเงิน) | **ไม่มี path ในดีไซน์ปัจจุบัน** — ยกเลิก = เฉพาะร่าง · reopen = เฉพาะตีกลับ (FIX-04/05) → ยังไม่มีการยกเลิกหลังอนุมัติ | BA/Finance เคาะว่าต้องมี path นี้ไหม · ถ้ามี ต้องออกแบบ compensating reverse-EC/release-FC (EC-05/XT-04/LD-06) |

---

## B. OQ ภายใน — BA/SEC/Strike เคาะ (ไม่บล็อก prototype · บล็อกการตั้งค่า/dev บางส่วน)

| OQ | ประเด็น | ค่าปัจจุบัน (default) | ผู้เคาะ |
|---|---|---|---|
| **OQ-EXP-04** | หมวดค่าใช้จ่าย group ยังไม่มีใน HR Config (#107) | mock + โครงอ้าง `resolve()` (A-EXP-04) | Strike/HR Config |
| **OQ-RBAC** | mapping role→login จริง (demo = demo-strip เลือก role) | 3 role: ผู้เบิก/ธุรการ(self) · ผู้อนุมัติ DOA · **เจ้าหน้าที่ HR/Finance(all·ไม่อนุมัติ)** | SEC/BA |
| **OQ-DOCCFG-พ.ศ.** | เลขเอกสารใช้ **พ.ศ.** (HTML=2569) แต่ registry default = ค.ศ. · reset cadence + **counter global vs per-branch** (BA brief = branch · HTML = global) | ประกาศ `EXP-<พ.ศ.>-NNNN` pad4 global monotonic ออกตอนอนุมัติจบ | BA/DOCCFG owner |
| **OQ-DOCCFG-module** | registry ไม่มี module `HR` · doc_type `EXP` ใหม่ (ไม่ชน) | เสนอเพิ่ม module HR หรือ register EXP ใต้ module อื่น | DOCCFG owner |
| **OQ-CSQ (W3)** | FRD/HTML อ้าง `CSQ_BRIEF_F101` (7C FC/EC) แต่ **ไม่ได้เลือก csq + ไม่มี skill csq-declaration** ใน workflow | 7C ระบุครบใน FRD (FN-19 · FC/EC ไม่มี AC) · CSQ มีเป็น **input brief BA** ที่ `5_DECLARATIONS/CSQ_BRIEF.md` | BA ยืนยันว่า 7C config ใช้ input brief นั้นพอ (ไม่ต้องมี declaration output แยก) |
| **OQ-UX** | ศัพท์ระบบบนจอ (`hook`/`display-only`/`F091`/`F103`/`7C`) — ตัดออกสำหรับ end-user ไหม | คงไว้ (prototype scaffolding · `jargon_leak=0`) | BA |
| **OQ-ERR** | 3 error code (`ERR_NOT_AUTHENTICATED` 401 · `ERR_INSUFFICIENT_ROLE` · `ERR_NOT_FOUND` 404) = backend guard ไม่มีทางเข้าที่ UI | ตรวจไม่ได้ที่ prototype · dev enforce | dev/backend |

---

## C. Design System Pending (BASE-KIT — ส่งเจ้าของ design system)
บันทึกใน `outputs/_SHARED/DESIGN_SYSTEM_PENDING.md`:
- **DSP-01** modal-in-drawer z-index (เกิดซ้ำทุก W5 HR · แก้สำเนา) · **DSP-02** combobox focus/trapFocus · **DSP-03** combobox ไม่ portal (dropdown ดัน modal scroll + flip-up ที่ viewport เตี้ย) — F101 workaround ครบ + uikit checks เพิ่มรอบนี้ (C3.8: U08–U16 · assert_slot_dropdown_no_spill ฯลฯ)
- ข้อเสนอ upstream: ให้ `.ss-list` portal ผ่าน `portalMenu()`/overlay-root (position:fixed) ทน scroll container ทุกที่
- **D-06** (UI Brief): overlay ไม่มี `lockScroll`/`is-overlay-open` — ข้อเสนอ ไม่ใช่ defect

---

## D. บันทึกที่ทำแล้ว (ไม่ต้องเคาะ — เพื่อ trace)
- **PM/BA OQ 2026-09-10 เคาะครบ 3** → เพิ่ม 3 จุดเชื่อม (FN-18 petty/PV + advance-clearing F103 · FN-19 7C=FC/EC no-AC · FN-20 scope self/all + role เจ้าหน้าที่) เป็น **display-only/soft-ref** ("แค่จุดเชื่อม" ไม่สร้างระบบ F091/F103 ซ้ำ) · ผนวกเข้า BRD/FRD/UI-Brief/TC/UAT ครบ
- **⚠️ GOVERNANCE:** FN-18/19/20 = **เพิ่มใน BRD/FRD แล้ว** แต่ **PREBRIEF §10 + FUNCTION_CHECKLIST.html ยังเป็น 22 FN** — BA ควรอัปเดต 2 ไฟล์บรีฟต้นทางให้ตรง (FN ปัจจุบัน = 25)
- **แก้ตาม BA review 10 FIX ครบ** (FIX-01 approve guard · 02 chain step-by-step · 03 masking+SoD · 04/05 reopen/cancel guard · 06 monotonic docnum · 07 F117/F102 hook · 08 NTF anchor · 09 icon · 10 CSQ microcopy)
- **manual test 8 รอบ เจอ bug จริง แก้ครบ** — ตัววัดหลุด → เพิ่ม uikit helper (append-only) กันหลุด feature อื่น (C3.8)
- **declaration รอบนี้ = doa + doccfg + ntf** (user เลือก · csq/pdfdoc ไม่เลือก — pdfdoc = step 2 ทำแล้ว · csq = ไม่มี skill · handled ผ่าน BA input brief)

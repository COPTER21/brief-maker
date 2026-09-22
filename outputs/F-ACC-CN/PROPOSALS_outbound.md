# PROPOSALS_outbound — F-ACC-CN · ใบลดหนี้ลูกค้า (Credit Note · F096)

> **WF-01 Step 12 · ปิดงาน** · 2026-09-22
> ข้อเสนอ/คำถามที่ต้องส่งกลับ **PM/BA** และ **เจ้าของ design system/skill** ก่อน dev เอาไปตั้งค่าจริง
> ทุกข้อ **ไม่บล็อก** ตัว prototype/เอกสาร (gate เขียวครบ) — แต่บางข้อ dev ต้องได้คำตอบ **ก่อนตั้งค่า engine จริง**

---

## A · Open Questions ให้ BA/PM เคาะ (ธุรกิจ — AI ห้ามเดา)

| OQ | เรื่อง | ทำไมต้องเคาะ | ตอนนี้ทำอะไรไว้ | ใครต้องใช้คำตอบ |
|---|---|---|---|---|
| **OQ-CN-01** | รายการเหตุผลตามกฎหมาย (legal reason master) + จุดยืน "ส่วนลดทางการค้าล้วน" | ประกาศอธิบดีฯ (VAT ฉ.82) กำหนดเหตุที่ออกใบลดหนี้ภาษีได้ — ส่วนลดการค้าล้วนอาจไม่เข้าข่าย | ปิด "ลดหนี้ไม่อ้างใบ" ไว้ · DISC ผูก legal_basis "ลดราคาเพราะสินค้าผิดข้อกำหนด/ชำรุด" + คำเตือน | dev (ตั้ง reason master + validation), บัญชี |
| **OQ-CN-02** | เส้นทางแก้ใบที่ออกเลขแล้ว = ใบเพิ่มหนี้ (DN) หรือ ใบลดหนี้ใหม่อ้างใบนี้ | ห้ามยกเลิกใบภาษีที่ออกเลขแล้ว — ต้องมีเอกสารทดแทน | ปุ่ม "ออกเอกสารแก้ไข" (display-only) อธิบาย 2 ทาง · ไม่ถอนยอด · mark `voided_by='(รอเอกสารทดแทน)'` | dev (flow แก้เอกสาร), บัญชี |
| **OQ-CN-03** | CSQ FC profile — refund/คืนเงินเมื่อชำระครบ ไปทาง RV/PV ตัวไหน | CN ลดยอดค้างเท่านั้น ไม่คืนเงินสด — ต้องรู้ปลายทาง | CSQ ประกาศแค่ AC+EC · ไม่ประกาศ FC-doc (กัน register 422) · comment รอเคาะ | dev (CSQ config), บัญชี |
| **OQ-CN-04** | จุดตัดวงเงิน DOA (50k / 300k) + เดือนภาษี (ม.82/10) ยืนยัน | ตัวเลข tier + เดือนที่ลง ภ.พ.30 มีผลกับ engine จริง | ใช้ 3-tier 50k/300k (จาก PREBRIEF) · netVat ลงเดือน cnDate | dev (DOA + VAT report config) |
| **OQ-AR-06** | **role-ids จริง** — `role-mgr-acc` ยังไม่มีใน role master | DOA chain ต้องผูก role-id จริง เดาผิด = สายอนุมัติผิดตอนใช้งาน | ใช้ [ASSUMED] role-ids ใน DOA_BRIEF · mark ชัด | dev (DOA declaration setup) **← สำคัญสุด** |

> **หมายเหตุ legal reference:** legal_basis ผูก **ม.86/10** (ออกใบลดหนี้อ้างใบกำกับเดิม) · **ม.82/10** = เดือนภาษีที่ netVat ลง ภ.พ.30 — แยกกันชัด ไม่ปน (ยืนยันใน coverage R2 §3)

---

## B · Cross-feature contract [ASSUMED] — รอ BA ยืนยัน

| รายการ | สมมติที่ใช้ | ต้องยืนยันกับ |
|---|---|---|
| **F094 AR Invoice** | ลดยอด `ar_open_item` (cn_applied += grand → outstanding ลด) · picker เฉพาะ issued/sent outstanding>0 | เจ้าของ F094 |
| **F090 Sales Return** | RET อ้าง SR ของใบเดียวกัน · qty ≤ ที่รับคืน (หน้าจอ SR จริงเป็น W4-LITE mock) | เจ้าของ F090 |
| **F093 Journal Entry** | JE จำลอง (Dr 4110/4120 netBefore · Dr 2150 netVat · Cr 1130 grand) — รอเชื่อมจริง | เจ้าของ F093 |
| **F105 VAT Report** | output_vat_line negative = netVat เดือน cnDate | เจ้าของ F105 |

---

## C · AI-DEFAULT (ตัดสินไว้ตาม standard — เปลี่ยนได้ถ้า BA ไม่เห็นด้วย)

| ID | เรื่อง | ค่าที่ใช้ |
|---|---|---|
| OQ-EB-01 | การปัดเศษ ebVat (VAT ส่วนลดท้ายบิล) | ปัด 2 ตำแหน่ง ตาม `ebVat=ebAmt×(vat/after)` |
| OQ-CC-01 | concurrent approval lock | 409 conflict + busyGate (กันกดซ้ำ) |
| OQ-FU-01 | ชนิด/ขนาดไฟล์แนบ | input file จริง multiple · ไม่จำกัด type ใน prototype (dev กำหนดตอนต่อ storage) |

---

## D · ส่งกลับเจ้าของ design system / skill (registered ที่ PENDING_REGISTRY)

| ID | เรื่อง | สถานะ |
|---|---|---|
| **DSP-08** | **v9.1 SKELETON z regression** — shared `.backdrop` ได้ global `--z-backdrop`(50) แต่ modal `.card` ไม่มี z → backdrop ทับ card → คลิก card = ปิด modal (flow อนุมัติกดไม่ได้) | ลงทะเบียนแล้วที่ `outputs/_SHARED/DESIGN_SYSTEM_PENDING.md` · แก้สำเนา `.modal-overlay > *:not(.backdrop){position:relative;z-index:var(--z-modal)}` · uikit `assert_modal_card_topmost` (prove-by-revert) · **ทุก feature ที่ gen ด้วย v9.1 จะโดนซ้ำจนกว่าจะแก้ skeleton ต้นทาง** |

---

## E · Governance note (บันทึกมติ)

- **FN-19 (ส่วนลดท้ายบิล)** เพิ่มเข้า PREBRIEF (BR-11 cap / BR-12 VAT ม.86/10) + FUNCTION_CHECKLIST → **22 FN** · marked `[มติ BA 2026-09-22]` — BA ควรยืนยัน format ในบรีฟอย่างเป็นทางการ
- **OQ-b RESOLVED (BA "หลัง"):** DOA tier คิดจากยอด NET **หลัง**หักส่วนลดท้ายบิล = พฤติกรรมปัจจุบัน (`resolveDoa` อ่าน `totals().grand`) · บันทึกเป็น **LD-05** ใน 07_LOCKED
- **UI Brief Drift D-2:** modal ยังไม่ล็อก body scroll — dev ยืนยันตอน implement

---

## F · Declarations รอบนี้

**ใช้ 4 ตัว:** `doa-declaration` + `ntf-declaration` + `csq-declaration` + `doccfg-declaration`
(+ `pdfdoc` = step 2 เอกสารพิมพ์ A4) · briefs ที่ `outputs/F-ACC-CN/5_DECLARATIONS/`
— ทั้งหมด **ผู้ใช้เลือกเอง** (C3.10) · chip=detect ทุกท่อ · ไม่มี DIVERGENCE (coverage R2 §4)

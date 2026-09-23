# PROPOSALS_outbound — F-ACC-DN · ใบลดหนี้ผู้ขาย (Debit Note · F097)

> **WF-01 Step 12 · ปิดงาน** · 2026-09-23
> ข้อเสนอ/คำถามที่ต้องส่งกลับ **PM/BA** และ **เจ้าของ design system/skill** ก่อน dev เอาไปตั้งค่าจริง
> ทุกข้อ **ไม่บล็อก** ตัว prototype/เอกสาร (gate เขียวครบ — audit FAIL=0 · e2e 36/36 FN 24/24 · qc-ux PASS · coverage R1+R2 PASS) — แต่บางข้อ dev ต้องได้คำตอบ **ก่อนตั้งค่า engine จริง**
> feature นี้เป็น **AP/ฝั่งซื้อ mirror ของ F-ACC-CN (Credit Note)**

---

## A · Open Questions ให้ BA/PM เคาะ (ธุรกิจ — AI ห้ามเดา)

| OQ | เรื่อง | ทำไมต้องเคาะ | ตอนนี้ทำอะไรไว้ | ใครต้องใช้คำตอบ |
|---|---|---|---|---|
| **OQ-AP-06** | **role-ids จริง** — `role-mgr-pur` (ผจก.จัดซื้อ) + `role-mgr-acc` ยังไม่ยืนยันใน role master | DOA chain ต้องผูก role-id จริง เดาผิด = สายอนุมัติผิดตอนใช้งาน | ใช้ [ASSUMED] role-ids ใน DOA_BRIEF · mark ชัด | dev (DOA declaration setup) **← สำคัญสุด** |
| **OQ-DN-05** | **legal basis ภาษีซื้อฝั่งผู้ซื้อ (ม.82/10)** — ผู้ซื้อลดภาษีซื้อในเดือนที่ **ได้รับใบลดหนี้จากผู้ขาย** | เอกสารภาษีคือใบลดหนี้ของผู้ขาย ไม่ใช่ DN ที่เราออก — เดือนที่ลง ภ.พ.30 มีผลจริง | UI 2-state: ไม่มี vendorCn → "รอเอกสาร" · มี → เดือนภาษี = vendorCnDate · comment ม.82/10 | dev (VAT report config), บัญชี/ภาษี |
| **OQ-DN-02** | จุดตัดวงเงิน DOA (50k / 300k) + บทบาทต่อ tier | ตัวเลข tier + role มีผลกับ engine จริง | ใช้ 3-tier 50k/300k (จาก PREBRIEF) [DEFAULT] | dev (DOA config) |
| **OQ-DN-04** | เส้นทางแก้/ยกเลิกใบที่ออกเลขแล้ว ("ออกเอกสารแก้ไข") | ห้ามยกเลิกใบภาษีที่ออกเลขแล้ว — ต้องมีเอกสารทดแทน | **ไม่ได้ build ใน prototype v1** (ต่างจาก CN ที่มี display-only) · FRD tag เป็น forward · toast "ใบที่อนุมัติแล้วยกเลิกไม่ได้ (OQ-DN-04)" | dev (flow แก้เอกสาร), บัญชี |
| **OQ-DN-03 / OQ-DN-06** | เครดิตคงเหลือกับผู้ขาย → settlement/หักบิลถัดไป/refund ไปทางไหน (CSQ FC?) | DN เกินหนี้ค้าง = vendor credit (ไม่ใช่เงินสด) — ต้องรู้ปลายทางการใช้ยอด | แสดง vendor credit (card+modal display-only) · CSQ ไม่ประกาศ FC (กัน register 422) · flow ใช้ยอด = นอก scope | dev (CSQ config), บัญชี |
| **OQ-DN-07** | CSQ profile-id `CSQ-ACC-DN` + event id (`ap_dn.approved` vs แยก `ap_dn.vat_applied` ตอน late-fill vendorCn) | ยิงผลบัญชีตอน late-fill vendorCn ต้องไม่สร้างผลซ้ำ | ใช้ idempotency_key เดิม + patch field vendor_cn_date · [ASSUMED] | dev (7C Engine registry) |
| **OQ-DN-01** | "ลดหนี้ไม่อ้างใบตั้งหนี้" (ลดลอย) | นโยบาย/กฎหมายเอกสารภาษี | ปิดไว้ (tile disabled) [ASSUMED] | BA, บัญชี |

> **legal reference แยกให้ชัด:** **ม.86/10** = การออกใบลดหนี้อ้างใบกำกับเดิม + คำนวณ VAT ส่วนลดท้ายบิลตามสัดส่วน · **ม.82/10** = เดือนภาษีที่ **ผู้ซื้อ** ลดภาษีซื้อใน ภ.พ.30 (= เดือนที่ได้รับใบลดหนี้ผู้ขาย) — ทั้งคู่ยัง [ASSUMED — mirror CN] รอ BA/ภาษียืนยัน

---

## B · Cross-feature contract [ASSUMED] — รอ BA ยืนยัน

| รายการ | สมมติที่ใช้ | ต้องยืนยันกับ |
|---|---|---|
| **F-ACC-APINV (AP Invoice)** | ลดยอด `ap_open_item` (`dn_applied += applyToAp` → outstanding ลด) · picker ใบที่ **dnRoom>0** (รวมใบจ่ายครบ) | เจ้าของ F-ACC-APINV |
| **RTV (รับคืนสินค้าจากผู้ขาย)** | RET อ้าง RTV ของใบเดียวกัน · qty ≤ ที่คืน (หน้าจอ RTV จริง = W3-LITE mock) | เจ้าของ RTV feature |
| **F093 Journal Entry** | JE จำลอง (Dr 2110/2120 เจ้าหนี้ = grand · Cr 5xxx/1140 = netBefore · Cr **1170 ภาษีซื้อ** = netVat) — รอเชื่อมจริง | เจ้าของ F093 |
| **VAT Report (ภ.พ.30)** | `input_vat_line` **ค่าลบ** = netVat เดือน **vendorCnDate** (ไม่ใช่ dnDate) | เจ้าของ VAT report |

---

## C · AI-DEFAULT (ตัดสินไว้ตาม standard — เปลี่ยนได้ถ้า BA ไม่เห็นด้วย)

| ID | เรื่อง | ค่าที่ใช้ |
|---|---|---|
| OQ-EB-01 | การปัดเศษ ebVat (VAT ส่วนลดท้ายบิล ม.86/10) | ปัด 2 ตำแหน่ง ตาม `ebVat=ebAmt×(vat/after)` |
| OQ-CC-01 | concurrent approval lock | 409 conflict + busyGate (กันกดซ้ำ) |
| OQ-FU-01 | ชนิด/ขนาดไฟล์แนบ | input file จริง multiple · ไม่จำกัด type ใน prototype (dev กำหนดตอนต่อ storage) |

---

## D · ส่งกลับเจ้าของ design system / skill (registered ที่ PENDING_REGISTRY)

| ID | เรื่อง | สถานะ |
|---|---|---|
| **DSP-08** | **v9.1 SKELETON z regression** — shared `.backdrop` ได้ global `--z-backdrop`(50) แต่ modal `.card` ไม่มี z → backdrop ทับ card → คลิก card = ปิด modal | ลงทะเบียนแล้วที่ `outputs/_SHARED/DESIGN_SYSTEM_PENDING.md` (โดย CN) · DN ก็ gen ด้วย v9.1 = โดนคลาสเดียวกัน · แก้ในสำเนา + uikit `assert_modal_card_topmost` · **ทุก feature v9.1 โดนซ้ำจนกว่าจะแก้ skeleton ต้นทาง** |

---

## E · Governance note (บันทึกมติ)

- **FN-19/20/21 + BR-11..14** เพิ่มเข้า PREBRIEF + FUNCTION_CHECKLIST → **24 FN** · marked `[มติ 2026-09-23]` / `[มติ BA FIX 2026-09-23]` — BA ควรยืนยัน format ในบรีฟอย่างเป็นทางการ
  - FN-19 ส่วนลดท้ายบิล (cap + VAT ม.86/10) · FN-20 เครดิตคงเหลือกับผู้ขาย · FN-21 ภาษีซื้อกลับตาม vendorCn (ม.82/10)
- **⭐ FN-04 / S-13 / S-11 REVERSAL (BA FIX-01):** ใบตั้งหนี้ที่ **จ่ายครบแล้ว ยังออก DN ได้** (คืนของหลังจ่าย → ส่วนเกิน = เครดิตคงเหลือกับผู้ขาย) — เพดาน DN = **`dnRoom` (grand−ลดแล้ว−รออนุมัติ) ไม่หัก paid** · `approveGuard` ขั้นสุดท้ายเช็ค `grand ≤ dnRoom` (ไม่ใช่ ≤ outstanding) · S-11 re-check re-framed = "ใบลดหนี้อื่นอนุมัติเพิ่มกินเพดาน" (การจ่ายเงินไม่บล็อก) · FN-04 ใหม่ = ใบที่ **ลดหนี้เต็มมูลค่าแล้ว** (dnRoom=0) ไม่โผล่
- **UI Brief Drift D-3 (revise-doc "ออกเอกสารแก้ไข") + D-4 (resend):** FRD subagent mirror มาจาก CN แต่ **HTML prototype v1 ไม่มี** → แก้ FRD ทุก layer ให้ tag เป็น **forward ภายใต้ OQ-DN-04** + footer ตรง AS-BUILT (approved=[ส่งให้ผู้ขาย] · sent=ไม่มีปุ่ม · ปุ่ม vendorCn อยู่ในแท็บ ref) — dev อย่า build จนกว่า BA เคาะ OQ-DN-04
- **Coverage R2 WARN#2:** 06_TESTS §6.2 Test Inventory เป็น subset ~30 core TC ขณะที่ testcases.md = 102 เคส — reconcile count ให้ตรงก่อน gen QA HTML/AI testset รอบถัดไป (มี note รับทราบในไฟล์แล้ว · ไม่กระทบความครบ FN 24/24)
- **JE account drift (minor):** FRD 01_UI เขียน "Cr 1150 ภาษีซื้อ" แต่ HTML JE ใช้ **1170 ภาษีซื้อ** — ยึด HTML (1170) เป็น truth · dev ยืนยันผังบัญชีจริงตอนเชื่อม F093

---

## F · Declarations รอบนี้

**ใช้ 4 ตัว:** `doa-declaration` + `ntf-declaration` + `csq-declaration` + `doccfg-declaration`
(+ `pdfdoc` = step 2 เอกสารพิมพ์ A4) · briefs ที่ `outputs/F-ACC-DN/5_DECLARATIONS/`
— ทั้งหมด **ผู้ใช้เลือกเอง** ที่ kickoff (C3.10) · chip=detect ทุกท่อ · ไม่มี DIVERGENCE (coverage R2)
- **DN nuance vs CN:** DOA approveGuard ใช้ `dnRoom` ไม่ใช่ outstanding · CSQ/NTF ภาษีซื้อกลับผูก `vendor_cn_date` (ม.82/10) ไม่ใช่ dn_date · code DN-YYYY-NNNN · events dn.issued/dn.sent/dn.cancelled

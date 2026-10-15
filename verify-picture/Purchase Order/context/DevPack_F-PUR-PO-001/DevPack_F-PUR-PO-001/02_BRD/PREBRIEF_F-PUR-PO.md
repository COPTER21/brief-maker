# PREBRIEF · Purchase Order — PO ใบสั่งซื้อ

> Module: Purchase · Wave: W3P (ลำดับ 1) · fid F078 · fcode `F-PUR-PO` · arch **Q-document**
> จาก Central Plan CUBE-LANE-W3-LITE + CONTEXT_PACK/W3-LITE.md + CHECKLIST W3P + BASELINE_F-PUR-PO.md · 2026-09-10
> เอกสารนี้คือ **source of truth เชิง business** ของ feature — ข้อที่ AI คิดเองติด `[AI-DRAFT]` รอเคาะผ่าน wireframe review
> ปี **ค.ศ. ล้วน** ทุกจุดในเอกสารและใน UI

---

## 0. Obligations — พันธะจากต้นทาง (ทุกแถวต้องถูกอ้างกลับ)

| # | พันธะ | จาก | ถูกตอบที่ § |
|---|---|---|---|
| OB-1 | เส้นเข้า: PR (F072 · W2) → PO — เปิด PO จาก PR ได้ · **mock `[ASSUMED contract]` ห้าม implement จริง** | CONTEXT_PACK §2.6 · graph external_deps | §2 S-01 · §3.1 · §9 · §12 |
| OB-2 | เปิด PO **ตรงไม่ผ่าน PR** ต้องได้ด้วย | CHECKLIST W3P · CONTEXT_PACK §2.6 | §2 S-02 · §6 |
| OB-3 | เส้นเข้า: Compare Vendors (F073 · W2) → ผลผู้ชนะ **soft-ref `[ASSUMED contract]`** | CONTEXT_PACK §2.6 | §2 S-03 · §3.1 · §9 |
| OB-4 | เส้นออก: PO → GRN (F079) ดึง PO line ไปรับของ · ยอดรับสะสมย้อนกลับมาที่ PO line | BUILD_ORDER edges · CHECKLIST | §3.2 · §5 · §9 · S-10/S-11 |
| OB-5 | forward-wire: ตรวจงบ → Budget Control (F117 · W7) = **mock + `TODO: budget-control hook`** | CONTEXT_PACK §2.6 | §2 S-06 · §3.4 · §9 · §12 |
| OB-6 | **สั่งซื้อ = commitment** (ผูกพันผู้ขาย · เกิดภาระผูกพันงบตอน approved) | CHECKLIST W3P | §1 · §4 BR-13 · §5 · §9 |
| OB-7 | DOA วงเงิน — **slot picker คนจริง** (avatar+ตำแหน่ง+ชื่อ) ห้าม role ID · ห้าม hardcode สายอนุมัติ | GOLDEN_RULES §3 · DOA-UI-LOCK 2026-08-17 | §2 S-04/S-05 · §5 · §6 · §7 |
| OB-8 | doccfg เลขรัน `PO-YYYY-NNNN` — ประกาศผ่าน doccfg-declaration **ห้าม hardcode** | CONTEXT_PACK §2.3 | §7 · §12 (DOCCFG_BRIEF) |
| OB-9 | pdfdoc — print spec ตาม thai-doc-pdf-generator แนบ BRD | CONTEXT_PACK §2.3 | §7 · §12 (print-spec-po.md) |
| OB-10 | สถานะ `draft → approved → sent → partially received → closed/cancelled` | CHECKLIST W3P | §5 |
| OB-11 | **แก้หลัง approve = re-approve (Transition Guard)** | CHECKLIST W3P | §2 S-08 · §4 BR-10 · §5 |
| OB-12 | Soft-reference LD-4C-02: Vendor · Item · UOM · Warehouse/Location · Cost Center = picker เท่านั้น ไม่ FK validate · nullable | GOLDEN_RULES §4 · TASTE_LOG | §3.1 · §3.2 · §7 |
| OB-13 | `OQ-PO-01 [ASSUMED]` รับเกิน PO ได้ไม่เกิน tolerance % (config ต่อ tenant · **default 0%**) — owner Strike | CONTEXT_PACK §3 | §3.4 · §4 BR-08 · §10 |
| OB-14 | Q-document เต็ม archetype: list + wizard 5 steps + view tabs (รายละเอียด › PDF › ลายเซ็น › ประวัติ) + เอกสารแนบใน landing + **B2 v2 line editor** | CONTEXT_PACK §2.1 | §6 · §3.2 |
| OB-15 | Declarations = `doa, ntf, csq, doccfg, pdfdoc` (chip ตรง FEATURE_LIST) | CONTEXT_PACK §2.2 | §12 |
| OB-16 | audit append-only · ไม่มี hard delete · ทุก threshold/เลขแจ้งเตือนอยู่ NC rules ไม่อยู่ feature code | GOLDEN_RULES §4 · CONTEXT_PACK §2.8 | §7 · §4 BR-16 |
| OB-17 | CI CUBE Warm Light + Satoshi/Noto Sans Thai + Lucide · **ปี ค.ศ. ล้วน** · sidebar ตาม module map ห้าม invent เมนู | GOLDEN_RULES §1 · TASTE_LOG | §6 · §7 |
| OB-18 | Gap จาก BASELINE ที่ต้องเติม: G-02 re-approve+สถานะย้อน · G-03 tolerance config · G-04 manual short-close | BASELINE_F-PUR-PO §6 | S-08 · §3.4 · S-12 |

**orphan check: 0** — ทุก OB มีจุดอ้างกลับแล้ว

---

## 1. สรุป + ผู้ใช้ + สิทธิ์

**ทำอะไร** [แผน]
PO ใบสั่งซื้อคือเอกสารที่องค์กร "ผูกพัน" กับผู้ขายว่าจะซื้อสินค้า/บริการตามรายการ ราคา และกำหนดส่งที่ระบุ — ต่างจาก PR ที่เป็นแค่ "ขอ" ภายใน. PO ที่ผ่านอนุมัติแล้วถือเป็น **commitment**: กันงบไว้ (ผ่าน Budget Control ในอนาคต) และกลายเป็นเอกสารต้นทางที่ GRN ใช้รับของ และ AP ใช้ทำ 3-way match ต่อไป. รอบนี้ PO เปิดได้ทั้งจาก PR (mock) และเปิดตรง, ผ่านสายอนุมัติ DOA ตามวงเงินโดยเลือก **คนจริง** ต่อ slot, ส่งให้ผู้ขายเป็น PDF, แล้วติดตามยอดรับของสะสมจนปิดใบ.

**ผู้ใช้ + สิทธิ์** [AI-DRAFT]

| Role | เห็นอะไร | ทำอะไรได้ |
|---|---|---|
| จัดซื้อ (Buyer) | PO ทุกใบในหน่วยงานตัวเอง | สร้าง/แก้ร่าง · ส่งอนุมัติ · ส่งให้ผู้ขาย · ยกเลิก (ตามสถานะ) · ปิดใบก่อนกำหนด (short-close) |
| หัวหน้าจัดซื้อ | PO ทุกใบทั้งแผนก | ทุกอย่างของ Buyer + เป็น slot อนุมัติได้ |
| ผู้อนุมัติตาม DOA | PO ที่ตัวเองถูกเลือกเป็น slot | อนุมัติ / ส่งกลับแก้ / ปฏิเสธ + ระบุเหตุผล |
| คลัง | PO ที่ approved/sent ขึ้นไป (อ่านอย่างเดียว) | ใช้เป็นต้นทางเปิด GRN (feature ถัดไป) |
| บัญชี/การเงิน | PO ทุกใบ (อ่านอย่างเดียว) | ดูภาระผูกพัน · ดาวน์โหลด PDF |
| ผู้ดูแลระบบ | ทุกใบ | ดูประวัติ audit ทั้งหมด (อ่านอย่างเดียว — append-only) |

> สิทธิ์ระดับ field/ปุ่มเป็น `[AI-DRAFT]` — รอเคาะตอน wireframe review

---

## 2. Scenarios — ทุกกรณีที่เกิดได้ (derive จาก D1–D6)

> **บันทึกการ derive:**
> D1 (ปริมาณ) → S-10, S-11, S-12, S-16 · D2 (state machine) → S-04, S-05, S-07, S-08, S-09, S-13, S-14 ·
> D3 (จุดตรวจ/อนุมัติ) → S-04, S-05, S-06 · D4 (เอกสารอ้างอิงเส้นเข้า) → S-01, S-02, S-03, S-15 ·
> D5 (ผลปลายทาง) → ผลใน S-07, S-10, S-11, S-12 (+ §9) · D6 [STD] → S-06, S-12, S-16, S-17, S-18, S-19

| S | ประเภท | ชื่อ | เกิดอะไร | **ข้อมูลที่ scenario นี้ต้องมี** | ผลปลายทาง |
|---|---|---|---|---|---|
| **S-01** | Happy | เปิด PO จาก PR ที่อนุมัติแล้ว | เลือก PR (mock) → ดึง line มาตั้งต้น → เลือกผู้ขาย → ใส่ราคา → ส่งอนุมัติ | เลข PR อ้างอิง · line จาก PR (สินค้า/จำนวน/หน่วย) · ผู้ขาย · ราคาต่อหน่วย · วันที่ต้องการรับ | PO draft ผูกกลับ PR (mock) · PR ฝั่ง W2 แสดง "ออก PO แล้ว" (mock badge) |
| **S-02** | Happy | เปิด PO ตรงไม่ผ่าน PR | สร้างใบเปล่า → เลือกผู้ขาย → เพิ่ม line เอง | ผู้ขาย · line ครบทุก field · เหตุผลที่ไม่ผ่าน PR (หมายเหตุ) | PO draft ไม่มี ref PR — ต้องทำได้เท่ากับ S-01 ทุกประการ |
| **S-03** | Alt | เปิด PO จากผลเทียบราคา (Compare Vendors) | รับผู้ชนะ + ราคาที่ชนะมาเป็นค่าตั้งต้น (soft-ref) | เลขใบเทียบราคา · ผู้ขายผู้ชนะ · ราคาที่ชนะต่อรายการ | PO draft มี badge "จากผลเทียบราคา #xxx" `[ASSUMED contract]` |
| **S-04** | Happy | ส่งอนุมัติ → อนุมัติผ่านครบ slot | เลือก **คนจริง** ต่อ slot ตามวงเงิน → ผู้อนุมัติกดอนุมัติครบ | slot ตามวงเงิน · คนจริงต่อ slot (avatar+ตำแหน่ง+ชื่อ) · วัน-เวลาอนุมัติ · ความเห็น | `draft → approved` · เกิด commitment · ntf แจ้งผู้ขอ+จัดซื้อ |
| **S-05** | Exception | ผู้อนุมัติ **ส่งกลับแก้ / ปฏิเสธ** | ส่งกลับ = กลับเป็น draft แก้ได้ · ปฏิเสธ = จบใบ | เหตุผล (บังคับ) · ผู้ตัดสิน · เวลา | ส่งกลับ → `draft` · ปฏิเสธ → `cancelled` (เหตุผล = ถูกปฏิเสธ) · ntf กลับผู้ยื่น |
| **S-06** | Exception | ตรวจงบไม่ผ่าน (mock) | ตอนส่งอนุมัติ hook ตรวจงบตอบ "เกินงบ" | หมวดงบ/cost center · ยอดที่ใช้ไป vs วงเงิน (mock) | **mock + `TODO: budget-control hook`** — แสดงเตือนใน wizard step ตรวจสอบ · ไม่บล็อกจริงในรอบนี้ `[AI-DRAFT]` |
| **S-07** | Happy | ส่ง PO ให้ผู้ขาย | `approved → sent` พร้อมออก PDF | ช่องทางส่ง (mock: อีเมล/พิมพ์) · วัน-เวลาที่ส่ง · ผู้ส่ง | สถานะ `sent` · ntf event `po.sent` · PDF ตาม print spec · หลังจากนี้ GRN เปิดได้ |
| **S-08** | Exception | **แก้ PO หลัง approve → re-approve** | กดแก้ที่ใบ approved/sent → Transition Guard เตือน → ยืนยัน → ใบกลับไปรออนุมัติใหม่ | เหตุผลการแก้ (บังคับ) · สิ่งที่แก้ (audit diff) · slot อนุมัติชุดใหม่ตามวงเงินใหม่ | สถานะกลับ `draft` (รอ re-approve) · audit เก็บทั้งค่าก่อน/หลัง (append-only) · ntf แจ้งผู้อนุมัติเดิม `[AI-DRAFT]` |
| **S-09** | Alt | บันทึกร่างค้างไว้ | ยังไม่ส่งอนุมัติ | — | ไม่เกิด commitment · ไม่มีผลปลายทาง · แก้/ลบร่างได้ (soft archive) |
| **S-10** | Happy | รับของครบตาม PO (ผลจาก GRN) | GRN ยิงยอดรับกลับมาครบทุก line | ยอดรับสะสมต่อ line (จาก GRN) | line ทุกบรรทัด `คงเหลือ = 0` → PO `closed` อัตโนมัติ |
| **S-11** | Alt | รับของบางส่วน | GRN รับไม่ครบ | ยอดรับสะสม < สั่ง | สถานะ `partially received` · คงเหลือรับต่อ line ถูกต้อง · เปิด GRN รอบถัดไปได้ |
| **S-12** | Alt/Exception | **ปิดใบก่อนรับครบ (short-close)** [STD] | ผู้ขายส่งไม่ครบและไม่ส่งแล้ว → จัดซื้อสั่งปิด | เหตุผลปิด (บังคับ) · ผู้สั่งปิด · ยอดที่ยกเลิกค้างรับ | `partially received → closed` · ยอดค้างรับถูกยกเลิก · GRN เปิดต่อไม่ได้ · ปลด commitment ส่วนที่เหลือ (mock งบ) |
| **S-13** | Exception | ยกเลิก PO ก่อนรับของ | ยกเลิกได้จาก draft / approved / sent | เหตุผลยกเลิก (บังคับ) · ผู้ยกเลิก | `cancelled` · ปลด commitment (mock) · ntf ผู้ขาย ถ้าเคย sent |
| **S-14** | ไม่รองรับ | ยกเลิก PO หลังรับของบางส่วน | — | — | **ไม่รองรับ** — ต้องใช้ short-close (S-12) แทน · เหตุผล: ของเข้าคลังแล้ว movement append-only ห้ามลบ [มติ CONTEXT_PACK §2.8] |
| **S-15** | Exception | PR ต้นทางถูกยกเลิก/แก้ ระหว่างที่ PO ยังร่าง | ตรวจตอนส่งอนุมัติ | สถานะ PR ล่าสุด (mock) | เตือน + ชี้กลับ PR · ไม่บล็อกอัตโนมัติในรอบนี้ (PR เป็น mock) `[ASSUMED contract]` |
| **S-16** | Exception | รับเกินจำนวนสั่ง | GRN พยายามรับ > คงเหลือ | tolerance % ต่อ tenant (config) | **`OQ-PO-01 [ASSUMED]` default 0%** → เกิน = บล็อกที่ GRN · PO เก็บค่า tolerance ต่อ line ให้ GRN อ่าน · owner Strike |
| **S-17** | Exception | ผู้ขายถูกระงับ/ปิดใช้งาน [STD] | เลือกผู้ขายที่ inactive | สถานะผู้ขาย (จาก master soft-ref) | เตือน "ผู้ขายถูกระงับ" แต่ **ไม่ FK validate** ตาม LD-4C-02 — เลือกได้ ผู้ใช้รับผิดชอบ `[AI-DRAFT]` |
| **S-18** | Exception | PO ซ้ำ (ผู้ขาย+รายการ+ช่วงเวลาใกล้กัน) [STD] | ระบบเตือนตอนบันทึก | เลข PO ที่คล้าย · วันที่ | เตือนอย่างเดียว ไม่บล็อก · เกณฑ์ความซ้ำอยู่ NC rules ไม่อยู่ feature code |
| **S-19** | ไม่รองรับ | Blanket PO / สัญญาซื้อระยะยาว + call-off [STD] | — | — | **ไม่รองรับใน W3** — backlog (BASELINE N-01) |
| **S-20** | ไม่รองรับ | Landed cost · Multi-currency FX revaluation · Drop-ship · Subcontracting · Auto-PO จาก reorder | — | — | **ไม่รองรับใน W3** — backlog (BASELINE N-03/N-04/N-05/N-06/N-07) |

---

## 3. Data — full data dict

### 3.1 Header

| Field | ชนิด | บังคับ | Default | ที่มา | Validation | ที่มาข้อ |
|---|---|---|---|---|---|---|
| เลขที่ PO | ข้อความ (auto) | ✅ | ว่าง จนกว่าจะบันทึก | **doccfg `PO-YYYY-NNNN`** (ห้าม hardcode) | อ่านอย่างเดียว · ไม่ซ้ำ | [แผน] OB-8 |
| สถานะ | enum | ✅ | `draft` | ระบบ | ตาม §5 เท่านั้น | [แผน] OB-10 |
| วันที่เอกสาร | วันที่ (ค.ศ.) | ✅ | วันนี้ | ผู้ใช้ | ไม่เกินวันนี้ + N วัน (NC rules) | [AI-DRAFT] |
| ผู้ขาย | combobox soft-ref | ✅ | — | Vendor Master (LD-4C-02) | **ไม่ FK validate** · เตือนถ้า inactive (S-17) | [แผน] OB-12 |
| ผู้ติดต่อผู้ขาย | ข้อความ | ⬜ | ดึงจากผู้ขาย | Vendor Master (soft) | — | [AI-DRAFT] |
| อ้างอิง PR | combobox soft-ref | ⬜ (**nullable**) | — | PR F072 **mock `[ASSUMED contract]`** | ไม่บังคับ — เปิดตรงได้ (OB-2) | [แผน] OB-1/OB-2 |
| อ้างอิงใบเทียบราคา | combobox soft-ref | ⬜ | — | Compare Vendors F073 **soft-ref** | ไม่บังคับ | [แผน] OB-3 |
| สกุลเงิน | enum soft | ✅ | THB | ระบบ/ผู้ขาย | รอบนี้ใช้ THB เป็นหลัก · FX logic ไม่อยู่ scope (S-20) | [AI-DRAFT] |
| เงื่อนไขการชำระเงิน | combobox soft | ✅ | จาก Vendor Master | master (soft) | — | [AI-DRAFT] |
| วันที่ต้องการรับของ (ใบ) | วันที่ (ค.ศ.) | ✅ | — | ผู้ใช้ | ≥ วันที่เอกสาร | [AI-DRAFT][STD] |
| คลัง/สถานที่ส่งของ | combobox soft-ref | ✅ | คลังหลักของผู้ใช้ | Warehouse/Location (LD-4C-02) | ไม่ FK validate | [แผน] OB-12 |
| ที่อยู่จัดส่ง (ข้อความ) | ข้อความยาว | ⬜ | ดึงจากคลัง | master (soft) | — | [AI-DRAFT] |
| Cost Center | combobox soft-ref | ⬜ | จากหน่วยงานผู้ใช้ | Cost Center (LD-4C-02) | nullable | [แผน] OB-12 |
| ผู้จัดซื้อผู้รับผิดชอบ | ผู้ใช้ (picker คนจริง) | ✅ | ผู้สร้าง | ทะเบียนพนักงาน | — | [AI-DRAFT] |
| หมายเหตุ / เงื่อนไขพิเศษ | ข้อความยาว | ⬜ | — | ผู้ใช้ | — | [AI-DRAFT] |
| ส่วนลดท้ายบิล | จำนวน/เปอร์เซ็นต์ | ⬜ | 0 | ผู้ใช้ | ≥ 0 · ไม่เกินยอดรวม | [AI-DRAFT] |
| ยอดรวมก่อนภาษี | จำนวน (computed) | — | — | คำนวณจาก lines | อ่านอย่างเดียว | §3.3 |
| ฐานภาษี / ภาษีมูลค่าเพิ่ม | จำนวน (computed) | — | — | คำนวณจาก lines | อ่านอย่างเดียว | §3.3 |
| ยอดสุทธิ | จำนวน (computed) | — | — | คำนวณ | อ่านอย่างเดียว · ใช้ตัดสินชั้น DOA | §3.3 · OB-7 |
| สาย DOA (slot list) | รายการ slot | ✅ ตอนส่งอนุมัติ | ตามวงเงิน (จาก DOA engine) | **DOA declaration** | ทุก slot ต้องมี **คนจริง** (avatar+ตำแหน่ง+ชื่อ) ห้าม role ID · ห้าม hardcode สาย | [แผน] OB-7 |
| ผลตรวจงบ (mock) | ป้ายสถานะ | — | ยังไม่ตรวจ | **mock — `TODO: budget-control hook`** | อ่านอย่างเดียว · ไม่บล็อกรอบนี้ | [แผน] OB-5 |
| เอกสารแนบ | ไฟล์แนบหลายไฟล์ | ⬜ | — | ผู้ใช้ | แสดงใน landing ตาม Pattern Q | [แผน] OB-14 |
| เหตุผลยกเลิก / เหตุผลปิดใบ | ข้อความ | ✅ เมื่อ cancel/short-close | — | ผู้ใช้ | บังคับกรอก (S-12, S-13) | [AI-DRAFT] |
| เหตุผลการแก้หลังอนุมัติ | ข้อความ | ✅ เมื่อ re-approve | — | ผู้ใช้ | บังคับกรอก (S-08) | [แผน] OB-11 |

### 3.2 Lines (grid B2 v2 — compact · VAT segmented · ส่วนลด · totals)

| Field | ชนิด | บังคับ | Default | ที่มา | Validation |
|---|---|---|---|---|---|
| ลำดับ | เลข | ✅ | auto | ระบบ | เรียง/ย้ายได้ |
| ประเภทบรรทัด | enum (สินค้า / บริการ) | ✅ | สินค้า | ผู้ใช้ | บริการ = ไม่มีผลคลัง (GRN จัดการต่างกัน) `[AI-DRAFT][STD]` |
| สินค้า/บริการ | combobox soft-ref | ✅ | — | Item Master (LD-4C-02) | ไม่ FK validate · พิมพ์เองได้ถ้าไม่มีใน master |
| คำอธิบาย | ข้อความ | ⬜ | ดึงจาก item | master (soft) | แก้ทับได้ |
| จำนวนสั่ง | จำนวน | ✅ | 1 | ผู้ใช้ | > 0 · ไม่รับ 0/ติดลบ (BR-05) |
| หน่วย (UOM) | combobox soft-ref | ✅ | จาก item | UOM Master (LD-4C-02) | ไม่ FK validate |
| ราคาต่อหน่วย | จำนวน | ✅ | จากผลเทียบราคา/ราคาซื้อล่าสุด (hint) | ผู้ใช้ / S-03 | ≥ 0 |
| ส่วนลดบรรทัด | จำนวน หรือ % | ⬜ | 0 | ผู้ใช้ | ไม่เกินยอดบรรทัด |
| ยอดก่อนภาษี (บรรทัด) | จำนวน (computed) | — | — | คำนวณ | อ่านอย่างเดียว |
| ภาษี (VAT) | **segmented: 7% / 0% / ยกเว้น** | ✅ | 7% | ผู้ใช้ | ต่อบรรทัด |
| วันที่ต้องการรับ (บรรทัด) | วันที่ (ค.ศ.) | ⬜ | ตามหัวเอกสาร | ผู้ใช้ | ≥ วันที่เอกสาร |
| Cost Center (บรรทัด) | combobox soft-ref | ⬜ | ตามหัวเอกสาร | LD-4C-02 | nullable |
| **รับแล้วสะสม** | จำนวน (อ่านอย่างเดียว) | — | 0 | **จาก GRN (F079)** | อ่านอย่างเดียว · append-only |
| **คงเหลือรับ** | จำนวน (computed) | — | = จำนวนสั่ง | คำนวณ | อ่านอย่างเดียว (§3.3) |
| tolerance รับเกิน % | เปอร์เซ็นต์ | ⬜ | **จาก config tenant · default 0%** | **config — `OQ-PO-01 [ASSUMED]`** | ห้าม hardcode ใน feature · GRN อ่านค่านี้ไปบังคับ |
| สถานะบรรทัด | enum (open / partial / closed / short-closed) | — | open | derive | อ่านอย่างเดียว |
| หมายเหตุบรรทัด | ข้อความ | ⬜ | — | ผู้ใช้ | — |

### 3.3 Computed / แสดงอย่างเดียว

| ค่า | สูตร |
|---|---|
| ยอดก่อนภาษี (บรรทัด) | `จำนวนสั่ง × ราคาต่อหน่วย − ส่วนลดบรรทัด` |
| ยอดรวมก่อนภาษี (ใบ) | `Σ ยอดก่อนภาษีทุกบรรทัด − ส่วนลดท้ายบิล` |
| ฐานภาษี | `Σ ยอดบรรทัดที่ VAT = 7%` (ปันส่วนลดท้ายบิลตามสัดส่วน) |
| ภาษีมูลค่าเพิ่ม | `ฐานภาษี × 7%` |
| ยอดสุทธิ | `ยอดรวมก่อนภาษี + ภาษีมูลค่าเพิ่ม` — **ใช้ตัดสินชั้น DOA** |
| คงเหลือรับ (บรรทัด) | `จำนวนสั่ง − รับแล้วสะสม` (ไม่ต่ำกว่า 0) |
| สถานะบรรทัด | คงเหลือ = จำนวนสั่ง → `open` · 0 < รับสะสม < สั่ง → `partial` · คงเหลือ = 0 → `closed` · ปิดโดย S-12 → `short-closed` |
| สถานะใบ (ส่วนรับของ) | ทุกบรรทัด `open` → คงสถานะเดิม · มีบรรทัดใด `partial/closed` แต่ไม่ครบ → `partially received` · ทุกบรรทัด `closed/short-closed` → `closed` |
| ภาระผูกพัน (commitment) คงค้าง | `Σ (คงเหลือรับ × ราคาต่อหน่วยสุทธิ)` — แสดงอย่างเดียว · **mock** ส่งต่อ Budget Control |

### 3.4 Config ที่ feature นี้อ่าน (ห้าม hardcode ใน feature)

| Config | เจ้าของ | ค่า default | หมายเหตุ |
|---|---|---|---|
| รูปแบบเลขรัน `PO-YYYY-NNNN` | **F-DOCCFG** (doccfg-declaration) | ปีเป็น **ค.ศ.** | OB-8 |
| tolerance รับเกิน % ต่อ tenant | **config ต่อ tenant** | **0%** | `OQ-PO-01 [ASSUMED]` owner Strike · OB-13/G-03 |
| สาย DOA ตามวงเงิน | **F-DLG-001 DOA engine** | ตั้งที่หน้า DOA กลาง | feature ประกาศเท่านั้น (OB-7) |
| ช่องทาง/เงื่อนไขแจ้งเตือน | **ENG-NOTIFY** | ตั้งที่ Notification Center | feature ประกาศ event เท่านั้น |
| เกณฑ์เตือน PO ซ้ำ · วันที่เอกสารย้อนหลังได้กี่วัน | **NC rules** | — | OB-16 — ห้ามอยู่ feature code |
| วงเงิน/หมวดงบ | **Budget Control (F117 · W7)** | — | **mock + `TODO: budget-control hook`** |

---

## 4. Business Rules

| BR | กติกา | พฤติกรรมเมื่อชน | scenario ที่เกี่ยว | ที่มา |
|---|---|---|---|---|
| BR-01 | PO ต้องมีอย่างน้อย 1 บรรทัด จึงส่งอนุมัติได้ | บล็อก + ชี้ไป step รายการ | S-01,S-02 | [AI-DRAFT] |
| BR-02 | ผู้ขาย + วันที่เอกสาร + วันที่ต้องการรับ + คลังปลายทาง = บังคับก่อนส่งอนุมัติ | บล็อก + ชี้ field แรกที่ขาด | S-01,S-02 | [AI-DRAFT] |
| BR-03 | เปิด PO **ไม่ต้องมี PR ก็ได้** — ห้ามบังคับ ref PR | — | S-02 | [แผน] OB-2 |
| BR-04 | ราคาต่อหน่วย ≥ 0 · ส่วนลดบรรทัดไม่เกินยอดบรรทัด | บล็อกที่ช่องนั้น + ข้อความบอกเหตุ | S-01,S-02 | [AI-DRAFT] |
| BR-05 | จำนวนสั่ง > 0 (ห้าม 0 / ติดลบ) | บล็อกที่ช่อง | ทุก scenario สร้าง | [AI-DRAFT] |
| BR-06 | ชั้นอนุมัติ DOA ตัดสินจาก **ยอดสุทธิของใบ** | เปลี่ยนยอด = ชุด slot เปลี่ยน | S-04,S-08 | [แผน] OB-7 |
| BR-07 | ทุก slot อนุมัติต้องระบุ **คนจริง** (avatar+ตำแหน่ง+ชื่อ) — **ห้าม role ID** ห้ามปล่อยว่าง | ส่งอนุมัติไม่ได้จนกว่าเลือกครบทุก slot | S-04 | [แผน] OB-7 · DOA-UI-LOCK 2026-08-17 |
| BR-08 | รับเกินจำนวนสั่งได้ไม่เกิน **tolerance % (config ต่อ tenant · default 0%)** | เกิน = บล็อกที่ GRN · PO เก็บค่า tolerance ให้ GRN อ่าน | S-16 | **`OQ-PO-01 [ASSUMED]`** owner Strike |
| BR-09 | PO ที่ยัง `draft` ไม่เกิด commitment · commitment เกิดตอน `approved` | — | S-04,S-09 | [แผน] OB-6 |
| BR-10 | **แก้ PO ที่ approved/sent = Transition Guard** → ต้องยืนยัน + ระบุเหตุผล → ใบกลับไปรออนุมัติใหม่ (re-approve) | แก้เงียบ ๆ ไม่ได้ | S-08 | [แผน] OB-11 |
| BR-11 | ยกเลิกได้เฉพาะสถานะ `draft` / `approved` / `sent` และต้องระบุเหตุผล | หลังรับของบางส่วนแล้ว = ปุ่มยกเลิกปิด ให้ใช้ short-close แทน | S-13,S-14 | [AI-DRAFT] |
| BR-12 | **Short-close** ได้เฉพาะ `partially received` และต้องระบุเหตุผล — ยอดค้างรับถูกยกเลิก เปิด GRN ต่อไม่ได้ | — | S-12 | [AI-DRAFT][STD] · G-04 |
| BR-13 | ยอดรับสะสมต่อบรรทัดมาจาก **GRN เท่านั้น** — แก้มือไม่ได้ · append-only | field อ่านอย่างเดียว | S-10,S-11 | [แผน] OB-4/OB-16 |
| BR-14 | GRN เปิดได้เฉพาะ PO สถานะ `sent` หรือ `partially received` เท่านั้น | สถานะอื่นไม่โผล่ในตัวเลือกของ GRN | S-07,S-11 | [AI-DRAFT] |
| BR-15 | ตรวจงบก่อนอนุมัติ = **mock** — แสดงผล ไม่บล็อกจริงในรอบนี้ | ป้ายเตือนใน step ตรวจสอบ + `TODO: budget-control hook` | S-06 | [แผน] OB-5 |
| BR-16 | ทุกการสร้าง/แก้/อนุมัติ/ส่ง/ยกเลิก/ปิดใบ ลง audit **append-only** — ไม่มี hard delete | ร่างที่ทิ้ง = soft archive | ทุก scenario | [แผน] OB-16 |
| BR-17 | Master ทุกตัว (ผู้ขาย/สินค้า/หน่วย/คลัง/cost center) = **picker soft-ref ไม่ FK validate · nullable** | เลือกค่าที่ไม่มีใน master ได้ · เตือนอย่างเดียว | S-17 · ทุก scenario | [แผน] OB-12 · LD-4C-02 |
| BR-18 | เตือน PO ซ้ำ (ผู้ขาย+รายการ+ช่วงเวลาใกล้กัน) — **เตือนอย่างเดียว ไม่บล็อก** · เกณฑ์อยู่ NC rules | — | S-18 | [AI-DRAFT][STD] |
| BR-19 | ปี **ค.ศ. ล้วน** ทุกจุดที่แสดงวันที่ (หน้าจอ + PDF) | ห้ามปน พ.ศ. | ทุก scenario | [แผน] OB-17 |
| BR-20 | เลขที่ PO ออกจาก doccfg เท่านั้น (`PO-YYYY-NNNN`) — ห้าม feature ตั้งเลขเอง | — | ทุก scenario | [แผน] OB-8 |

---

## 5. State Machine

```
draft ──ส่งอนุมัติ+DOA ครบ──▶ approved ──ส่งให้ผู้ขาย──▶ sent ──GRN รับบางส่วน──▶ partially received
  ▲                              │                        │                            │
  │ ส่งกลับแก้ (S-05)             │                        │ รับครบ (S-10)              │ รับครบ / short-close (S-12)
  │ แก้หลัง approve (S-08)        ▼                        ▼                            ▼
  └───────────────────────── cancelled ◀──ยกเลิก (S-13)── closed ◀────────────────────┘
```

| จาก | ไป | ใครกด | เงื่อนไข | scenario |
|---|---|---|---|---|
| — | `draft` | จัดซื้อ | สร้างใบใหม่ (จาก PR / ตรง / จากผลเทียบราคา) | S-01,S-02,S-03,S-09 |
| `draft` | `approved` | ผู้อนุมัติทุก slot | ผ่าน BR-01/02/07 · DOA ครบทุกชั้น | S-04 |
| `draft` | `draft` (ส่งกลับ) | ผู้อนุมัติ | ระบุเหตุผล | S-05 |
| `draft` | `cancelled` | จัดซื้อ / ผู้อนุมัติ (ปฏิเสธ) | ระบุเหตุผล | S-05,S-13 |
| `approved` | `sent` | จัดซื้อ | ออก PDF + บันทึกการส่ง | S-07 |
| `approved` | `draft` | จัดซื้อ | **แก้หลังอนุมัติ → Transition Guard → re-approve** (ระบุเหตุผล) | S-08 |
| `approved` | `cancelled` | จัดซื้อ | ระบุเหตุผล · ยังไม่รับของ | S-13 |
| `sent` | `draft` | จัดซื้อ | แก้หลังส่ง → Transition Guard → re-approve + แจ้งผู้ขาย | S-08 |
| `sent` | `partially received` | ระบบ (จาก GRN) | GRN post ยอดบางส่วน | S-11 |
| `sent` | `closed` | ระบบ (จาก GRN) | GRN post ครบทุกบรรทัด | S-10 |
| `sent` | `cancelled` | จัดซื้อ | ระบุเหตุผล · **ยังไม่มี GRN ใด ๆ** | S-13 |
| `partially received` | `closed` | ระบบ (จาก GRN) | รับครบทุกบรรทัด | S-10 |
| `partially received` | `closed` (short-close) | จัดซื้อ | ระบุเหตุผลปิด · ยกเลิกยอดค้างรับ | S-12 |
| `partially received` | `cancelled` | — | **ไม่รองรับ** — ใช้ short-close แทน | S-14 |
| `closed` / `cancelled` | — | — | สถานะปลายทาง · อ่านอย่างเดียว · แก้ไม่ได้ | — |

> **DOA**: ทุก transition `draft → approved` ผ่าน DOA engine (slot picker คนจริง) — feature ประกาศเท่านั้น ห้าม hardcode สาย (OB-7)

---

## 6. Actions ต่อหน้า (Pattern Q archetype)

### 6.1 Landing / List (Pattern Q list + เอกสารแนบใน landing)

| action | enable เมื่อ | ทำอะไร | toast/ผล |
|---|---|---|---|
| สร้าง PO ใหม่ | เสมอ | เปิด wizard 5 steps — เลือกจุดตั้งต้น (จาก PR / จากผลเทียบราคา / เปิดตรง) | เข้า step 1 |
| ค้นหา / filter (สถานะ · ผู้ขาย · ช่วงวันที่ · ผู้จัดซื้อ) | เสมอ | กรอง list | มี empty state ชัดเจน |
| เปิดดูใบ | เลือกแถว | เปิด view drawer 4 tabs | — |
| ดาวน์โหลด PDF | สถานะ ≥ approved | ออกไฟล์ตาม print spec | toast "สร้างไฟล์แล้ว" |
| แนบเอกสาร | เสมอ | เพิ่มไฟล์แนบเข้าใบ (แสดงในโซนเอกสารแนบของ landing) | toast |

### 6.2 Wizard 5 steps (สร้าง/แก้)

| Step | ชื่อ | ทำอะไร | ผ่านไป step ถัดไปเมื่อ |
|---|---|---|---|
| 1 | จุดตั้งต้น + ผู้ขาย | เลือกโหมด (จาก PR mock / จากผลเทียบราคา soft-ref / เปิดตรง) + เลือกผู้ขาย + เงื่อนไขชำระ | มีผู้ขาย (BR-02) |
| 2 | รายการสินค้า (**B2 v2 line editor**) | เพิ่ม/แก้/ลบบรรทัด · จำนวน · ราคา · ส่วนลด · **VAT segmented** · วันที่รับต่อบรรทัด · totals สดด้านล่าง | ≥ 1 บรรทัด + ผ่าน BR-04/BR-05 (BR-01) |
| 3 | การจัดส่ง + งบประมาณ | คลัง/ที่อยู่ส่งของ · วันที่ต้องการรับ · cost center · **ผลตรวจงบ (mock + `TODO: budget-control hook`)** | ครบ field บังคับ |
| 4 | ผู้อนุมัติ (**DOA slot picker คนจริง**) | ระบบเสนอชั้นตามยอดสุทธิ → ผู้ใช้เลือก **คนจริง** ต่อ slot (avatar + ตำแหน่ง + ชื่อ) | ทุก slot มีคนจริง (BR-07) |
| 5 | ตรวจทาน + ส่ง | สรุปทั้งใบ + preview PDF + ปุ่ม "บันทึกร่าง" / "ส่งอนุมัติ" | — |

| action ใน wizard | enable เมื่อ | ทำอะไร | toast/ผล |
|---|---|---|---|
| บันทึกร่าง | ทุก step | เก็บเป็น `draft` (soft archive ถ้าทิ้ง) | toast "บันทึกร่างแล้ว" · S-09 |
| ส่งอนุมัติ | step 5 · ผ่าน BR-01/02/04/05/07 | เข้า DOA · สถานะรออนุมัติ | toast + ntf ผู้อนุมัติ slot แรก · S-04 |
| ออกจาก wizard | ทุก step | Esc chain → ถามยืนยันถ้ามีการแก้ | — |

### 6.3 View drawer — 4 tabs (Pattern Q)

| Tab | เนื้อหา | action |
|---|---|---|
| **รายละเอียด** | header + lines + totals + **ยอดรับสะสม/คงเหลือต่อบรรทัด** + ป้ายผลตรวจงบ (mock) | แก้ (Transition Guard ถ้า ≥ approved) · ส่งให้ผู้ขาย · ยกเลิก · ปิดใบก่อนกำหนด |
| **PDF** | preview A4 ตาม print spec (ปี ค.ศ.) | ดาวน์โหลด · พิมพ์ |
| **ลายเซ็น** | สาย DOA — slot + **คนจริง** (avatar+ตำแหน่ง+ชื่อ) + สถานะ/เวลา/ความเห็นต่อ slot | อนุมัติ · ส่งกลับแก้ · ปฏิเสธ (เฉพาะผู้ที่เป็น slot นั้น) |
| **ประวัติ** | audit append-only ทุก event (สร้าง/แก้ diff/อนุมัติ/ส่ง/รับของจาก GRN/ยกเลิก/ปิดใบ) | อ่านอย่างเดียว — ไม่มีลบ |

| action สำคัญ | enable เมื่อ | ทำอะไร | toast/ผล |
|---|---|---|---|
| อนุมัติ / ส่งกลับแก้ / ปฏิเสธ | ผู้ใช้เป็น slot ที่ถึงคิว | เดินสาย DOA | S-04, S-05 |
| ส่งให้ผู้ขาย | `approved` | `→ sent` + ออก PDF + ntf `po.sent` | S-07 |
| แก้หลังอนุมัติ | `approved` / `sent` | **Transition Guard**: ยืนยัน + เหตุผล → กลับ `draft` รอ re-approve | S-08 |
| ยกเลิก | `draft`/`approved`/`sent` · ไม่มี GRN | confirm แบบ destructive + เหตุผลบังคับ | S-13 |
| ปิดใบก่อนกำหนด (short-close) | `partially received` | confirm + เหตุผลบังคับ → `closed` ยกเลิกยอดค้าง | S-12 |

---

## 7. Data behaviour

- **เลขรัน**: `PO-YYYY-NNNN` ออกจาก **F-DOCCFG** ผ่าน doccfg-declaration — ห้าม feature ตั้งเลขเอง · ปี = **ค.ศ.** (OB-8, BR-20)
- **Soft-reference (LD-4C-02)**: Vendor · Item/Product · UOM · Warehouse/Location · Cost Center = combobox picker · **ไม่ FK validate · nullable** — ค่าที่หายจาก master ยังแสดงเป็นข้อความเดิม ไม่พัง
- **Soft archive**: ร่างที่ทิ้ง / ใบที่ยกเลิก = ซ่อนจาก list ปกติ แต่ยังค้นเจอผ่าน filter "รวมที่ยกเลิก" — **ไม่มี hard delete**
- **Audit append-only**: ทุก event ต่อท้ายอย่างเดียว · การแก้เก็บทั้งค่าก่อน/หลัง (diff) · แถว audit แก้/ลบไม่ได้ (OB-16, BR-16)
- **Commitment**: เกิดตอน `approved` · ปลดตอน `cancelled` / `short-close` (ส่วนค้าง) / `closed` — รอบนี้ **แสดงเป็นตัวเลข mock** ส่งต่อ Budget Control ในอนาคต
- **ยอดรับสะสม**: เขียนโดย **GRN เท่านั้น** — PO อ่านอย่างเดียว (BR-13) · movement ฝั่งคลัง append-only ไม่มีลบ
- **เอกสารแนบ**: ผูก Document Center · แสดงในโซนเอกสารแนบของ landing ตาม Pattern Q
- **แจ้งเตือน**: ประกาศ event ผ่าน **ntf-declaration** เท่านั้น — ห้าม hardcode ช่องทาง/เงื่อนไข · `doa_pending`/`doa_result` มาจาก DOA engine อัตโนมัติ (ห้ามประกาศซ้ำ)
- **Threshold/เกณฑ์เตือนทุกตัว** (PO ซ้ำ · วันที่ย้อนหลัง · tolerance) → อยู่ **NC rules / config** ไม่อยู่ feature code (OB-16)
- **วันที่**: แสดง **ค.ศ. ล้วน** ทั้งหน้าจอและ PDF (BR-19)

---

## 8. Mock Data Spec — ชุดข้อมูลที่ prove ทุก scenario ได้

> ห้าม lorem — ชื่อผู้ขาย/สินค้า/ตัวเลข ต้องหน้าตาเหมือนธุรกิจจริง · KPI/ยอดใน landing ต้องคำนวณจากชุดนี้แล้วสมเหตุผล

| ชุด | รายการ | prove scenario |
|---|---|---|
| `PO-2026-0001` · draft · จาก `PR-2026-0142` (mock) · บ.สหชัยวัสดุภัณฑ์ · 3 บรรทัด (ท่อ PVC 4" · ข้อต่อ · กาว) | เปิดจาก PR แล้วยังไม่ส่ง | S-01, S-09 |
| `PO-2026-0002` · draft · เปิดตรงไม่มี PR · หจก.ไทยเทคซัพพลาย · 2 บรรทัด (ตลับหมึก · กระดาษ A4) | เปิดตรงต้องทำได้เท่ากับเปิดจาก PR | S-02 |
| `PO-2026-0003` · draft · จากใบเทียบราคา `CMP-2026-0031` (soft-ref) · บ.เอเชียพาวเวอร์ · ผู้ชนะ + ราคาที่ชนะ | รับผลผู้ชนะจาก Compare Vendors | S-03 |
| `PO-2026-0004` · รออนุมัติ · ยอดสุทธิ 148,000 · slot 2 ชั้น (หัวหน้าจัดซื้อ: คุณวรพล ศรีสุข · ผู้อำนวยการ: คุณณัฐกานต์ พูนทรัพย์) | DOA slot picker คนจริง 2 ชั้น | S-04 |
| `PO-2026-0005` · ถูกส่งกลับแก้ · เหตุผล "ราคาสูงกว่าที่เทียบไว้ ขอเจรจาใหม่" | ส่งกลับแก้ + เหตุผลบังคับ | S-05 |
| `PO-2026-0006` · รออนุมัติ · ยอด 890,000 · ป้ายผลตรวจงบ = "เกินวงเงินคงเหลือ (mock)" | ตรวจงบไม่ผ่าน (mock + TODO) | S-06 |
| `PO-2026-0007` · sent · ส่งอีเมลแล้ว 2026-09-03 | ส่งให้ผู้ขาย + PDF | S-07 |
| `PO-2026-0008` · approved แล้วถูกแก้ราคา → กลับมารออนุมัติใหม่ · เหตุผล "ผู้ขายปรับราคาขึ้น 3%" | แก้หลัง approve → re-approve (Transition Guard) | S-08 |
| `PO-2026-0009` · partially received · 3 บรรทัด: บรรทัด 1 รับครบ 100/100 · บรรทัด 2 รับ 40/120 · บรรทัด 3 ยังไม่รับ 0/50 | รับบางส่วน + ยอดค้างรับถูกต้อง | S-11 |
| `PO-2026-0010` · closed · รับครบทุกบรรทัด | รับครบ → ปิดอัตโนมัติ | S-10 |
| `PO-2026-0011` · partially received → short-closed · เหตุผล "ผู้ขายแจ้งของขาดตลาด ยกเลิกส่วนที่เหลือ" | short-close | S-12 |
| `PO-2026-0012` · cancelled จากสถานะ sent · เหตุผล "เปลี่ยนสเปคงาน" | ยกเลิกก่อนรับของ | S-13 |
| `PO-2026-0013` · sent · บรรทัดตั้ง tolerance 0% (default) และมี 1 บรรทัดตั้ง 5% | ให้ GRN ทดสอบรับเกิน | S-16 |
| ผู้ขาย `บ.เก่าแก่การค้า` สถานะ **ถูกระงับ** ในชุด master mock | เตือนแต่ไม่บล็อก (soft-ref) | S-17 |
| `PO-2026-0014` · ผู้ขายเดียวกัน + รายการเดียวกันกับ `PO-2026-0002` ห่างกัน 2 วัน | เตือน PO ซ้ำ | S-18 |

**KPI ที่ landing ต้องคำนวณได้จากชุดนี้**: จำนวนใบรออนุมัติ · จำนวนใบค้างรับ · มูลค่าภาระผูกพันคงค้าง · ใบที่เกินกำหนดรับ

---

## 9. Edges + Hotspot + ผลปลายทาง

| ทิศ | คู่ | จุดใน UI | เกิดอะไรที่ปลายทาง (wireframe ต้อง demo แม้ mock) |
|---|---|---|---|
| เข้า | **PR (F072 · W2)** `[ASSUMED contract]` | wizard step 1 โหมด "จากใบขอซื้อ" | ดึง line จาก PR mock · PR แสดง badge "ออก PO แล้ว" (mock) — **ห้าม implement PR จริง** |
| เข้า | **Compare Vendors (F073 · W2)** soft-ref | wizard step 1 โหมด "จากผลเทียบราคา" | ตั้งต้นผู้ขายผู้ชนะ + ราคาที่ชนะ · badge อ้างเลขใบเทียบราคา `[ASSUMED contract]` |
| เข้า | Vendor / Item / UOM / Location / Cost Center (DONE) | combobox ทุกจุด | soft-ref picker · ไม่ FK validate (LD-4C-02) |
| เข้า | **DOA engine (F-DLG-001)** | wizard step 4 + tab ลายเซ็น | slot ตามวงเงิน · เลือก **คนจริง** · event `doa_pending`/`doa_result` มาจาก engine เอง |
| ออก | **GRN (F079 · W3P ตัวถัดไป)** | tab รายละเอียด — คอลัมน์ รับแล้ว/คงเหลือ | GRN ดึง PO line ของ PO สถานะ `sent`/`partially received` → post แล้วยิงยอดรับสะสมกลับ → PO เปลี่ยนเป็น `partially received` / `closed` |
| ออก | **Budget Control (F117 · W7)** | wizard step 3 ป้ายผลตรวจงบ + tab รายละเอียด | **mock + `TODO: budget-control hook`** — แสดงผลอย่างเดียว ไม่บล็อกจริง ห้ามคำนวณงบเอง |
| ออก | **ENG-NOTIFY** | ทุก transition | ประกาศ event ผ่าน ntf-declaration — ห้าม hardcode ช่องทาง |
| ออก | **7C Consequence (ENG-CSQ)** | ตอน approved / sent / closed / cancelled | ประกาศ event ผ่าน csq-declaration — ห้าม hardcode ท่อ |
| ออก | **F-DOCCFG** | ตอนบันทึกใบแรก | ขอเลข `PO-YYYY-NNNN` จาก ENG-DOC-NUM |
| ออก | ผู้ขาย (ภายนอก) | tab PDF · ปุ่มส่งให้ผู้ขาย | PDF A4 ตาม print spec (thai-doc-pdf-generator) · ปี ค.ศ. |
| **ไม่มีเส้น** | JE / GL posting | — | PO **ไม่ post บัญชี** — commitment ≠ actual (JE เกิดที่ GRN/Invoice · W5) |

---

## 10. OQ + [AI-DRAFT] register → pin

| # | ประเด็น | สถานะ | เจ้าภาพ | pin ที่ |
|---|---|---|---|---|
| **OQ-PO-01** | รับเกิน PO ได้ไม่เกิน tolerance % — config ต่อ tenant · **default 0%** | **`[ASSUMED]` ใช้ default แล้ว** | **Strike** | §3.2 tolerance · §3.4 · BR-08 · S-16 |
| OQ-PO-02 `[AI-DRAFT]` | แก้หลัง approve — ควรเก็บเป็น **version (v1/v2)** แบบ SAP/D365 หรือ audit diff พอ? รอบนี้เลือก **audit diff + re-approve** | ตัดสินชั่วคราว | Strike | S-08 · BR-10 · BASELINE G-02 |
| OQ-PO-03 `[AI-DRAFT]` | ตรวจงบไม่ผ่าน — ควร **บล็อกการอนุมัติ** หรือ **เตือนแล้วให้ผ่านได้**? รอบนี้ = เตือนอย่างเดียว (Budget Control ยังไม่มีจริง) | รอ W7 | Strike + เจ้าของ F117 | S-06 · BR-15 |
| OQ-PO-04 `[AI-DRAFT]` | ใครมีสิทธิ์ **short-close**? รอบนี้ = จัดซื้อผู้รับผิดชอบ + หัวหน้าจัดซื้อ · ควรต้องผ่าน DOA ด้วยไหม | รอเคาะ | Strike | S-12 · BR-12 |
| OQ-PO-05 `[AI-DRAFT]` | PR ต้นทางถูกยกเลิกระหว่าง PO ยังร่าง — **บล็อก** หรือ **เตือน**? รอบนี้ = เตือน (PR เป็น mock) | รอ W2 ปิด | Strike + เจ้าของ F072 | S-15 |
| OQ-PO-06 `[AI-DRAFT]` | บรรทัดประเภท **บริการ** — GRN ต้องรับไหม หรือปิดบรรทัดด้วยการยืนยันงานเสร็จ | รอ W3P GRN | Strike | §3.2 ประเภทบรรทัด |
| OQ-PO-07 `[AI-DRAFT]` | เกณฑ์เตือน **PO ซ้ำ** (ช่วงกี่วัน · เทียบระดับใบหรือระดับบรรทัด) — ต้องไปอยู่ NC rules | รอเคาะ | Strike | BR-18 · S-18 |

---

## 11. Coverage Matrix (ledger — gate อยู่ที่นี่)

| S | BR ที่ใช้ | transition | หน้าจอ/ปุ่ม | FN ใน checklist |
|---|---|---|---|---|
| S-01 | BR-01,02,03,04,05,17,20 | — → draft | wizard step 1 โหมด "จากใบขอซื้อ" + step 2 | FN-01, FN-03, FN-04 |
| S-02 | BR-01,02,03,04,05,17 | — → draft | wizard step 1 โหมด "เปิดตรง" | FN-02, FN-04 |
| S-03 | BR-04,17 | — → draft | wizard step 1 โหมด "จากผลเทียบราคา" | FN-05 |
| S-04 | BR-06,07,09 | draft → approved | wizard step 4 slot picker + tab ลายเซ็น ปุ่มอนุมัติ | FN-10, FN-11, FN-12 |
| S-05 | BR-07 | draft → draft / draft → cancelled | tab ลายเซ็น ปุ่มส่งกลับแก้ / ปฏิเสธ | FN-13 |
| S-06 | BR-15 | (ไม่เปลี่ยนสถานะ) | wizard step 3 ป้ายผลตรวจงบ (mock) | FN-14 |
| S-07 | BR-19 | approved → sent | tab รายละเอียด ปุ่มส่งให้ผู้ขาย + tab PDF | FN-15, FN-16 |
| S-08 | BR-06,10,16 | approved/sent → draft | ปุ่มแก้ + Transition Guard dialog | FN-17, FN-18 |
| S-09 | BR-16 | — → draft | ปุ่มบันทึกร่างในทุก step | FN-19 |
| S-10 | BR-13,14 | sent/partially received → closed | tab รายละเอียด คอลัมน์ รับแล้ว/คงเหลือ + badge สถานะ | FN-20, FN-22 |
| S-11 | BR-13,14 | sent → partially received | tab รายละเอียด คอลัมน์ รับแล้ว/คงเหลือ | FN-21, FN-22 |
| S-12 | BR-12,16 | partially received → closed | ปุ่มปิดใบก่อนกำหนด + dialog เหตุผล | FN-23 |
| S-13 | BR-11,16 | draft/approved/sent → cancelled | ปุ่มยกเลิก + confirm destructive | FN-24 |
| S-14 | BR-11 | (ถูกปฏิเสธ) | ปุ่มยกเลิกถูกปิดเมื่อ partially received | FN-25 |
| S-15 | BR-03 | (ไม่เปลี่ยนสถานะ) | แถบเตือนใน step 1 / step 5 | FN-06 |
| S-16 | BR-08 | (ไม่เปลี่ยนสถานะ) | คอลัมน์ tolerance % ใน line editor | FN-07 |
| S-17 | BR-17 | (ไม่เปลี่ยนสถานะ) | combobox ผู้ขาย + badge เตือน | FN-08 |
| S-18 | BR-18 | (ไม่เปลี่ยนสถานะ) | เตือนตอนบันทึก/ส่งอนุมัติ | FN-09 |
| S-19 | — | — | (ไม่รองรับ — อยู่หมวด "สิ่งที่ไม่รองรับ") | — |
| S-20 | — | — | (ไม่รองรับ — อยู่หมวด "สิ่งที่ไม่รองรับ") | — |
| ทุก S | BR-16,19 | ทุก transition | tab ประวัติ (append-only) · วันที่ ค.ศ. ทุกจุด | FN-93, FN-94 |

**เงื่อนไขผ่าน**
- ✅ ทุก BR-01..BR-20 ปรากฏ ≥ 1 แถว
- ✅ ทุก transition ใน §5 ปรากฏ ≥ 1 แถว (รวม transition ที่ถูกปฏิเสธ S-14)
- ✅ ทุก S ที่รองรับมีหน้าจอ/ปุ่ม + FN (S-19/S-20 = ไม่รองรับ อยู่ใน section "สิ่งที่ไม่รองรับ" ของ checklist)
- ✅ ทุก OB-1..OB-18 ถูกอ้างกลับใน §0 แล้ว (0 orphan)

---

## 12. Declarations ที่ feature นี้ต้องออก (chip = `doa, ntf, csq, doccfg, pdfdoc`)

| Declaration | ประกาศอะไร | ไฟล์ |
|---|---|---|
| **doa** | มีวงเงิน ✅ — matrix ชั้นอนุมัติตามยอดสุทธิ · slot picker **คนจริง** | `5_DECLARATIONS/DOA_BRIEF_F-PUR-PO.md` |
| **ntf** | event ธุรกิจของ PO (ส่งให้ผู้ขาย · รับของบางส่วน · ปิดใบ · ยกเลิก · ใกล้ถึงกำหนดรับ) — **ไม่ประกาศซ้ำ** `doa_pending`/`doa_result` | `5_DECLARATIONS/NTF_BRIEF_F-PUR-PO.md` |
| **csq** | 7C event ที่ PO ทำให้เกิด (commitment/งบ · ต้นทุน) — **ไม่ประกาศซ้ำ** OC (มาจาก Operation Process) และ DC ระดับเอกสาร (มาจาก DOA engine) · SC = false เสมอ | `5_DECLARATIONS/CSQ_BRIEF_F-PUR-PO.md` |
| **doccfg** | doc_type `PO` · เลขรัน **`PO-YYYY-NNNN`** (ปี ค.ศ.) · snapshot policy | `5_DECLARATIONS/DOCCFG_BRIEF_F-PUR-PO.md` |
| **pdfdoc** | print spec A4 ใบสั่งซื้อ (thai-doc-pdf-generator) | `5_DECLARATIONS/print-spec-po.md` |

**chip verify**: FEATURE_LIST_ALL แถว F078 = `doa,ntf,csq,doccfg,pdfdoc` / arch `Q-document` — **detect = chip → ไม่มี DIVERGENCE**

---

## 13. S1.5 Gap Check — PREBRIEF ครอบ BASELINE / CHECKLIST / OQ ครบหรือยัง

### 13.1 BASELINE must-have (M-01..M-15) → จุดที่ถูกครอบใน PREBRIEF

| M | ครอบที่ | ผล |
|---|---|---|
| M-01 header/line structure | §3.1 · §3.2 | ✅ |
| M-02 lifecycle 5 สถานะ | §5 · OB-10 | ✅ |
| M-03 สายอนุมัติตามวงเงิน | §6.2 step 4 · BR-06/07 · S-04 | ✅ |
| M-04 สร้างจาก PR + traceability | S-01 · FN-01/FN-03 (mock `[ASSUMED contract]`) | ✅ |
| M-05 สร้าง PO ตรง | S-02 · BR-03 · FN-02 | ✅ |
| M-06 change order + re-approval | S-08 · BR-10 · FN-17/FN-18 | ✅ |
| M-07 รับสะสมต่อ line / open qty | §3.2 · §3.3 · S-10/S-11 · FN-20..22 | ✅ |
| M-08 over-delivery tolerance | §3.2 tolerance · BR-08 · S-16 · FN-07 | ✅ `[ASSUMED OQ-PO-01]` |
| M-09 ส่ง PO + สถานะ sent | S-07 · FN-15/FN-16 | ✅ |
| M-10 เลขรันตั้งค่าได้ | §3.4 doccfg · BR-20 · FN-31 | ✅ |
| M-11 ยกเลิก + guard | S-13/S-14 · BR-11 · FN-24/FN-25 | ✅ |
| M-12 audit append-only | §7 · BR-16 · FN-93 | ✅ |
| M-13 budget commitment check | S-06 · BR-15 · FN-14 | ⚠️ **mock + `TODO: budget-control hook`** (ตั้งใจ — forward-wire W7) |
| M-14 3-way match readiness | §9 เส้นออก GRN · BR-14 | ✅ |
| M-15 เอกสารแนบ | §3.1 · §7 · FN-32 | ✅ |

**สรุป: must-have 15/15 ถูกครอบ** (M-13 เป็น mock โดยเจตนาตามกติกา forward-wire — ไม่นับเป็นช่องว่าง)

### 13.2 BASELINE gap G-01..G-07 → ถูกเติมแล้วที่ไหน

| G | เรื่อง | เติมที่ |
|---|---|---|
| G-01 | commitment เข้างบตอน approve แต่ยังไม่มี Budget Control | BR-09 (commitment เกิดตอน approved) + BR-15 (mock) + §3.3 "ภาระผูกพันคงค้าง" |
| G-02 | change order versioning | S-08 + BR-10 + **OQ-PO-02** (เลือก audit diff + re-approve · versioning = backlog) |
| G-03 | tolerance config | §3.2 field tolerance + §3.4 config + BR-08 + **OQ-PO-01 `[ASSUMED]` default 0%** |
| G-04 | manual short-close | **S-12** + BR-12 + FN-23/FN-34 + **OQ-PO-04** (ใครมีสิทธิ์) |
| G-05 | ส่ง email แล้วอัพเดตสถานะ | S-07 + §7 (ประกาศ event ผ่าน ntf ห้าม hardcode ช่องทาง) |
| G-06 | approval matrix อ้าง role — CUBE ล็อกคนจริง | BR-07 + FN-11 (ระบุชัดว่าต่างจาก standard โดยตั้งใจ) |
| G-07 | line type บริการ | §3.2 ประเภทบรรทัด + **OQ-PO-06** |

### 13.3 CHECKLIST W3P (แถว F-PUR-PO) → ครบทุกข้อ

| ข้อใน CHECKLIST | ครอบที่ |
|---|---|
| Q-document เต็ม (Pattern Q + B2 v2) | §6 (list + wizard 5 steps + view tabs 4 + เอกสารแนบใน landing) · §3.2 (B2 v2 grid + VAT segmented + ส่วนลด + totals) |
| สั่งซื้อ = commitment | OB-6 · BR-09 · §3.3 |
| เปิดจาก PR (mock) หรือเปิดตรง | S-01 / S-02 · BR-03 · FN-01/FN-02 |
| รับผลผู้ชนะจาก Compare Vendors (soft-ref) | S-03 · §9 · FN-05 |
| DOA วงเงิน slot picker คนจริง | BR-06/BR-07 · §6.2 step 4 · FN-10..12 |
| doccfg `PO-YYYY-NNNN` + pdfdoc print spec | §3.4 · §12 · FN-31/FN-16 |
| forward-wire ตรวจงบ → Budget Control mock+TODO | S-06 · BR-15 · §9 · FN-14 |
| สถานะ draft→approved→sent→partially received→closed/cancelled | §5 ครบทุก transition |
| แก้หลัง approve = re-approve (Transition Guard) | S-08 · BR-10 · FN-17/FN-18 |

**ครบ 9/9 ข้อ**

### 13.4 OQ / `[ASSUMED]` register — ครบและมี owner

| รายการ | มาร์กแล้ว | owner |
|---|---|---|
| `OQ-PO-01` tolerance รับเกิน default 0% | ✅ `[ASSUMED]` (§3.2, §3.4, BR-08, S-16, FN-07) | **Strike** |
| PR contract | ✅ `[ASSUMED contract]` (OB-1, S-01, §9, FN-01) | Strike + เจ้าของ F072 |
| Compare Vendors contract | ✅ `[ASSUMED contract]` (OB-3, S-03, §9, FN-05) | Strike + เจ้าของ F073 |
| Budget Control | ✅ `TODO: budget-control hook` (OB-5, S-06, BR-15, §9) | เจ้าของ F117 (W7) |
| OQ-PO-02..07 `[AI-DRAFT]` | ✅ §10 ครบ 6 ข้อ พร้อม pin | Strike |

**รวม `[ASSUMED]` = 3 ตัว (OQ-PO-01, PR contract, Compare Vendors contract) · `TODO:` forward-wire = 1 ตัว (Budget Control W7) · `[AI-DRAFT]` register = 6 ข้อ**

### 13.5 ผลรวม S1.5
ไม่พบช่องว่างที่ต้องเพิ่ม scenario ใหม่ — gap ทั้ง 3 ตัวจาก BASELINE §6 (G-02/G-03/G-04) ถูกเติมเข้า PREBRIEF ตั้งแต่ S1 แล้ว (S-08 · tolerance config · S-12) · **S1.5 = pass**

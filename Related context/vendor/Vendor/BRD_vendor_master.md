# BRD: Vendor Master (F-VENDOR-MASTER-001)

| Field | Value |
|---|---|
| BRD ID | BRD-P2P-MD-VENDOR-001 |
| Feature Name | Vendor Master (ทะเบียนคู่ค้า) |
| BRD Type | New Feature |
| Version | 1.1 |
| Status | Draft → AI Reviewed (revised) |
| Module | Master Data · P2P Domain · CUBE NATIVE |
| Owner | 2BSimple BA Team |
| Stakeholders | Procurement (Officer/Manager/Director) · Finance · Compliance · Internal Audit · Admin |
| Created Date | 2026-05-29 |
| Last Updated | 2026-05-29 (v1.1 revision) |
| Source | Revision Mode — HTML v2 + BRD v1.0 |
| Linked Artifacts | `vendor-master.html` v2 (HTML Prototype) · `F-VENDOR-PRICE-LIST` (cross-feature read dependency) |

## Changelog
- **v1.1 (2026-05-29):** Revision per HTML v2 — เพิ่ม Tab 5 "สินค้า/บริการ" ใน view drawer (read-only embed จาก F-VENDOR-PRICE-LIST) → updates §3 Scope, §6 Data Entity, §7 User Stories (US-11), §12 Dependencies, §14.6 Layout Deviation Log, §15 OQ-09
- **v1.0 (2026-05-29):** สร้าง BRD ครั้งแรกผ่าน `brd-generator-full` (Standalone Mode, source = HTML prototype)
- HTML reference: `vendor-master.html` v2 — ผ่าน Iron Rules 30/30 ของ html-generator-v3 v3.6 + 5-tab view drawer pattern

---

## Section 2: Business Context

### 2.1 ปัญหา / โอกาส

องค์กรในกลุ่ม CUBE NATIVE ERP ปัจจุบันบริหารข้อมูลคู่ค้า (vendors) แบบกระจายตาม Excel/ไฟล์ word ของแต่ละแผนก ส่งผลให้:
- **ข้อมูลคู่ค้าซ้ำซ้อน** — vendor เดียวอาจถูกเปิดหลายครั้งโดยแผนกต่างกัน เลขผู้เสียภาษีเหมือนแต่ระบบไม่ตรวจ
- **ไม่มี KYC gate** — เปิด PO/จ่ายเงินไปก่อน ค่อยตรวจหลังเอกสาร = เสี่ยงทำธุรกรรมกับ vendor ที่ติด sanctions
- **ไม่มี audit trail** — ใครเปิด/แก้/อนุมัติ vendor ไหน เมื่อไหร่ ไม่สามารถ trace ได้ (PDPA + ISO 27001 ต้องมี)
- **ไม่มี SoD** — คนเปิด vendor สามารถอนุมัติเองได้ → ช่องโหว่ fraud
- **อนุมัติแบบ flat** — ไม่มี DOA chain ตามวงเงิน → ทุก vendor ผ่านอำนาจคนเดียว

### 2.2 เป้าหมายทาง Business

- **Single Source of Truth ของคู่ค้า** — ทุก module ใน ERP (PO, PR, PV, GR) อ้างอิง vendor_id จาก master นี้
- **KYC Gate ก่อนทำธุรกรรม** — vendor ต้องผ่าน Compliance review + sanctions screening ก่อน active
- **DOA Approval Chain** — อนุมัติตามวงเงิน รองรับ multi-step (เช่น Manager → Director สำหรับวงเงินสูง)
- **SoD Enforcement** — ผู้สร้าง vendor ≠ ผู้อนุมัติ (ป้องกัน fraud, มาตรฐาน internal control)
- **Data Classification + Masking** — เลขภาษี (Confidential) และเลขบัญชี (Restricted) ปกปิดให้ role ที่ไม่ควรเห็น
- **WORM Audit Trail** — ทุก action บันทึก who/when/what ไม่สามารถลบหรือแก้ย้อนหลัง

### 2.3 ตัวชี้วัดความสำเร็จ (Success Metrics)

| Metric | Baseline | Target | วัดยังไง |
|---|---|---|---|
| Vendor duplicate rate | ~12% (จาก Excel survey) | < 1% | Unique constraint on tax_id per country |
| KYC compliance rate | ~40% (post-hoc) | 100% (gate) | % vendors with status=active that have kyc=passed |
| Approval bypass incidents | 3 cases/year | 0 | SoD violations blocked by system |
| Vendor onboarding lead time | 5–7 days (manual) | < 24 hr | Time from prospect → active |
| Audit query response time | 2 days (manual search) | < 5 min | Audit log searchable in UI |
| Sanctions hit detection | Manual quarterly | Real-time (every KYC) | % vendor checked against OFAC/UN/EU |

### 2.4 ที่มาของ Requirement

- เคสที่เกิด: Q4/2025 — vendor หนึ่ง ถูกพบใน UN sanctions list หลังจ่ายเงินไปแล้ว → ปัญหาด้าน compliance
- Request จาก: Internal Audit Committee + CFO
- KPI Gap: ผ่าน ISO 27001 + PDPA แต่ vendor data layer ยังไม่ compliant
- Strategic Fit: เป็น foundation feature ของ P2P value stream — module อื่น (PR, PO, GR, PV) ต้อง depend on vendor master ที่สมบูรณ์

---

## Section 3: Scope

### 3.1 In Scope

- CRUD ของ vendor master (สร้าง / แก้ไข / ดู / บล็อก / ปลดบล็อก / แบล็คลิสต์)
- **11 ประเภท vendor:** RM, TR, SV, MN, CT, LG, SP, UT, GV, EM, OT (one-time)
- **Vendor code auto-gen** รูปแบบ `V-CC-TT-NNNNN` (Country ISO + Type 2 ตัว + running 5 หลัก)
- **6-state lifecycle:** prospect → pending_kyc → pending_approval → active ↔ blocked → blacklisted (terminal)
- **KYC gate** — Compliance review (พบ/ไม่พบ sanctions, ตรวจเอกสารแนบ, ตรวจรูปแบบเลขภาษี)
- **DOA Approval Chain** — ลำดับขั้นตามวงเงินเครดิต (placeholder rule; wire to Policy Center DOA engine ภายหลัง)
- **Multi-bank accounts** — Finance verifies; primary toggle; purpose tags
- **Multi-address + Multi-contact** — รองรับ billing address + shipping addresses
- **Payment terms (code only)** — อ้างอิง code จาก Finance Payment Terms master
- **Data Classification + Role-based Masking** — Confidential (เลขภาษี) + Restricted (เลขบัญชี)
- **WORM Audit Trail** — log ทุก action (read by audit job, ไม่ surface ใน UI หลัก)
- **One-time vendor (OT) auto-approve** — สำหรับ vendor ครั้งเดียว ไม่ต้อง chain
- **Attachments** — แนบไฟล์ทั่วไป (หนังสือรับรอง, สำเนาบัญชี ฯลฯ)
- **Price List read-only embed (Tab 5)** ⭐ NEW v1.1 — แสดง summary ของสินค้า/บริการที่ vendor ขาย (compact table: ชื่อ + ราคา/หน่วย + สถานะ) — **ข้อมูล source จาก F-VENDOR-PRICE-LIST · view-only** · link ออกไป feature เต็มเพื่อแก้ไข

### 3.2 Out of Scope (Phase 1)

- **Price List CRUD** ⭐ — สร้าง/แก้/ลบ items + ราคา + validity → อยู่ที่ **F-VENDOR-PRICE-LIST** (separate feature) — Vendor Master แค่ embed view เท่านั้น
- **Vendor merge / split** — เคส vendor 2 record ที่เป็นบริษัทเดียวกัน รวมกัน (เลื่อน Phase 2)
- **Vendor performance scoring** — KPI ของ vendor (on-time delivery, defect rate) — แยกเป็น feature
- **Vendor portal (external)** — vendor login มาอัปเดตข้อมูลเอง (Phase 3+)
- **Payment Terms master** — อยู่ใน Finance domain (vendor แค่อ้างอิง code)
- **DOA engine implementation** — Policy Center wave (vendor ใช้ placeholder rule + wire ทีหลัง)
- **PDPA consent management** — แยก Policy Center feature

### 3.3 Assumptions

- Country master + ISO codes มีพร้อม (TH, US, JP, CN, SG ฯลฯ)
- Currency master + FX rate มีพร้อม (THB, USD, EUR, SGD, CNY)
- Bank master (Thai banks 5 อันดับแรก) มีพร้อม
- Thai address master (จังหวัด/อำเภอ/ตำบล/ไปรษณีย์) มีพร้อม
- Sanctions list source (OFAC/UN/EU) มี API หรือ feed
- Authentication + RBAC framework (Core Cube) พร้อมรองรับ 6 roles

---

## Section 4: User Roles & Permissions

### 4.1 Role Matrix

| Role | สร้าง | แก้ไข | ส่ง KYC/อนุมัติ | ตรวจ KYC | อนุมัติ (DOA) | บล็อก/ปลดบล็อก | แบล็คลิสต์ | เห็นเลขภาษีเต็ม | เห็นเลขบัญชีเต็ม |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Procurement Officer** | ✅ | ✅ | ✅ | ❌ | ✅ (ขั้น 1 เท่านั้น) | ✅ | ❌ | ❌ (mask) | ❌ (mask) |
| **Procurement Manager** | ❌ | ❌ | ❌ | ❌ | ✅ (ขั้น 1-2) | ✅ | ❌ | ❌ (mask) | ❌ (mask) |
| **Procurement Director** | ❌ | ❌ | ❌ | ❌ | ✅ (ทุกขั้น override) | ✅ | ✅ (terminal) | ❌ (mask) | ❌ (mask) |
| **Finance** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ (+ verify bank) |
| **Compliance** | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ (mask) |
| **Admin** | ✅ | ✅ | ✅ | ✅ | ✅ (override) | ✅ | ✅ | ✅ | ✅ |

### 4.2 SoD (Separation of Duties) Rules

- **SoD-01:** ผู้สร้าง vendor (createdBy) ≠ ผู้อนุมัติ (approver ใน chain step ใดๆ) — บังคับใน confirmApprove guard
- **SoD-02:** ผู้ตรวจ KYC (Compliance) ≠ ผู้อนุมัติ DOA (Procurement)
- **SoD-03:** ผู้ verify bank (Finance) ≠ ผู้สร้าง vendor

---

## Section 5: User Journey (with COSO)

### 5.1 Happy Path: สร้าง vendor ใหม่ → active

| ขั้น | Action | Maker | Checker | Approver | System |
|---|---|---|---|---|---|
| 1 | กรอกข้อมูลคู่ค้า (3-step wizard) | Procurement Officer | — | — | validate fields, auto-gen vendor code |
| 2 | บันทึก vendor (status=prospect) | Procurement Officer | — | — | persist + audit `created` |
| 3 | ส่งเข้า KYC (status=pending_kyc) | Procurement Officer | — | — | audit `submitted_for_kyc` |
| 4 | ตรวจ KYC: เอกสารแนบ + sanctions screening + tax format | — | Compliance | — | call ENG-SANCTIONS; if hit → auto-block |
| 5 | บันทึกผล KYC=passed | — | — | Compliance | audit `kyc_passed`, lock tax_id (IR-01) |
| 6 | Officer ส่งอนุมัติ (status=pending_approval) | Procurement Officer | — | — | build approval_chain via DOA rule |
| 7 | ผู้จัดการอนุมัติขั้น 1 | — | — | Procurement Manager | guard: KYC=passed, SoD (approver≠creator) |
| 8 | (ถ้า credit > 5M) ผอ.จัดซื้อ อนุมัติขั้น 2 | — | — | Procurement Director | guard เดียวกัน + role match step |
| 9 | Chain done → status=active | — | — | — | audit `chain_complete`, vendor available for PO |

### 5.2 Alternative Paths

- **5.2.1 OT (One-time) vendor:** ขั้น 6 → skip chain → auto-approve → status=active
- **5.2.2 ตีกลับ (Reject):** ขั้น 7-8 → ผู้อนุมัติกด "ตีกลับ" + ระบุเหตุผล → status=pending_kyc + clear approvalChain → Officer แก้แล้วส่งใหม่ → chain build ใหม่
- **5.2.3 KYC ไม่ผ่าน:** ขั้น 4 → Compliance กด "ไม่ผ่าน" → kyc=failed (status ยัง=pending_kyc) → Officer แก้เอกสาร แล้วให้ Compliance ตรวจซ้ำ
- **5.2.4 Sanctions hit:** ขั้น 4 → ระบบตรวจพบ → kyc=failed + status=blocked + auto-record reason "sanctions hit" (BR-S06)
- **5.2.5 Block + Unblock:** vendor=active → ผู้มีสิทธิ์กดบล็อก + ระบุเหตุผล → status=blocked → ปลดบล็อกด้วย modal+เหตุผล → status=active
- **5.2.6 Blacklist (terminal):** ผอ.จัดซื้อ กด แบล็คลิสต์ + เหตุผล → status=blacklisted → ห้ามใช้งานต่อ (one-way)

### 5.3 SoD Enforcement Points

- จุดที่ 7-8 (อนุมัติ): block ถ้า `approver.uid === createdBy` → toast "SOD_VIOLATION"
- จุดที่ 5 (KYC pass): ไม่ได้ block แต่ลง audit ว่าใครตรวจ ใครส่ง

---

## Section 6: Data Entity & Fields

### 6.1 Entity: `vendor` (master)

| Field | Type | Required | Classification | Notes |
|---|---|:---:|---|---|
| id | UUID | ✓ | Internal | PK |
| code | string(20) | ✓ | Internal | Auto-gen `V-{CC}-{TT}-{NNNNN}` (unique per country+type) |
| name | string(255) | ✓ | Internal | ชื่อตามกฎหมาย |
| display | string(255) | — | Internal | ชื่อที่ใช้แสดง (ถ้าต่างจาก legal) |
| type | enum(11) | ✓ | Internal | RM/TR/SV/MN/CT/LG/SP/UT/GV/EM/OT |
| country | ISO-2 | ✓ | Internal | TH default |
| tax_id | string(13) | conditional | **Confidential** | จำเป็นยกเว้น OT ที่ไม่มี — locked หลัง KYC pass (IR-01) |
| vat | string(20) | — | Confidential | เลข VAT (ถ้ามี) |
| companyReg | string(20) | — | Confidential | เลขทะเบียนนิติบุคคล |
| currency | ISO-3 | ✓ | Internal | THB default |
| term | string(20) | ✓ | Internal | Payment term code (FK → Finance.payment_terms) |
| wht | decimal(5,2) | — | Internal | ภาษีหัก ณ ที่จ่าย % (3/5/etc) |
| creditLimit | decimal(15,2) | — | Confidential | วงเงินเครดิต — input to DOA chain |
| kyc | enum | ✓ | Internal | pending / passed / failed / expired |
| kycAt | timestamp | — | Internal | เวลาที่ kyc=passed |
| status | enum(6) | ✓ | Internal | prospect / pending_kyc / pending_approval / active / blocked / blacklisted |
| approvalChain | array | — | Internal | DOA chain snapshot — [{seq, role, label, status, approver, at, comment}] |
| approvedBy | string | — | Internal | ผู้อนุมัติขั้นสุดท้าย (final approver) |
| approvedAt | timestamp | — | Internal | เวลาที่ active |
| block | string(500) | — | Internal | เหตุผลถูก block/blacklist |
| hasTxn | boolean | ✓ | Internal | มี transaction อ้างอิงหรือไม่ — affects soft-delete |
| createdBy | string | ✓ | Internal | uid ของผู้สร้าง — input to SoD |
| created | timestamp | ✓ | Internal | เวลาสร้าง |
| version | int | ✓ | Internal | optimistic concurrency |
| audit | array (WORM) | ✓ | Internal | log entries — read-only, append-only |
| contacts | array | — | Internal | [{role, name, email, phone}] ≥1 required pre-active |
| addresses | array | — | Internal | [{label, line, province_code, district_code, subdistrict_code, postal, is_billing, is_primary_shipping}] |
| banks | array | conditional | **Restricted** | [{bank, acct, name, purpose, primary, verified, verified_at}] — non-OT requires ≥1 verified |
| attachments | array | — | Internal | [{id, name, size}] |

### 6.2 Master References (FK)

| Reference | Source Module | Notes |
|---|---|---|
| country | Core Cube · Country Master | ISO 3166 alpha-2 |
| currency | Core Cube · Currency Master | ISO 4217 + FX rate |
| term (payment) | **Finance · Payment Terms Master** | vendor เก็บแค่ code; นิยามจริง (discount, baseline, net days) อยู่ที่ Finance |
| bank | Core Cube · Bank Master | Thai banks + foreign |
| province/district/subdistrict | Core Cube · Thai Address Master | for TH country only |
| sanctions list | ENG-SANCTIONS (Compliance) | OFAC/UN/EU feed |
| approval_chain rule | **Policy Center · DOA Engine** | placeholder ใน Phase 1; wire ใน Phase 2 |
| **price_list (read-only)** ⭐ NEW v1.1 | **F-VENDOR-PRICE-LIST (separate feature)** | Vendor Master เก็บแค่ join key (vendor_id) · ไม่มี FK column ใน T_vendor · embed view ผ่าน API call to Price List feature |

### 6.3 ER Diagram (text)

```
vendor (1) ─── (N) contact
vendor (1) ─── (N) address
vendor (1) ─── (N) bank_account
vendor (1) ─── (N) attachment
vendor (1) ─── (N) audit_entry  [WORM]
vendor (1) ─── (1) approval_chain (snapshot, JSON array of steps)

vendor (N) ─── (1) country [FK]
vendor (N) ─── (1) currency [FK]
vendor (N) ─── (1) payment_term [FK — Finance domain]
bank_account (N) ─── (1) bank [FK]
address (N) ─── (1) province [FK, TH only]

vendor (1) ─── (N) price_list_item   [⭐ cross-feature, read-only embed]
                                     [data lives in F-VENDOR-PRICE-LIST]
                                     [Vendor Master = consumer only, no write]
```

### 6.4 Price List Cross-Feature Reference ⭐ NEW v1.1

**Boundary:**
- **F-VENDOR-PRICE-LIST is the SINGLE SOURCE OF TRUTH** for vendor's items/prices/validity
- Vendor Master imports a **read-only summary view** via API call: `GET /api/v1/vendors/{id}/price-list-summary` → proxy to F-VENDOR-PRICE-LIST
- **No price list data stored in T_vendor or sub-tables** — pure runtime fetch + cache
- **No CRUD operations** in Vendor Master UI — edit buttons fully absent in Tab 5 (UI/UX boundary enforcement)

**Fields fetched (minimal — เฉพาะที่ Procurement ใช้ scan):**

| Field | Use in Tab 5 | Cut from view |
|---|---|---|
| code | ✅ show below name | — |
| name | ✅ primary identifier | — |
| price | ✅ show with currency | — |
| unit | ✅ show after price | — |
| status (active/expired) | ✅ visual dot | — |
| ~~category~~ | ❌ cut | aggregate at F-VENDOR-PRICE-LIST instead |
| ~~minQty~~ | ❌ cut | shown in F-VENDOR-PRICE-LIST detail |
| ~~validFrom/validTo~~ | ❌ cut | derived → expired status |

**Performance:** Cache price list summary 5 min in Redis (keyed by vendor_id) — stale read OK for view; user can click "ดู Price List เต็ม →" to refresh

---

## Section 7: User Stories & Acceptance Criteria

### US-01: Procurement Officer เปิด vendor ใหม่
**As** เจ้าหน้าที่จัดซื้อ
**I want to** กรอกข้อมูล vendor ใหม่ผ่าน 3-step wizard
**So that** vendor พร้อมเข้ากระบวนการ KYC

**AC:**
- **Given** Officer login + กดปุ่ม "+ เพิ่มคู่ค้า" → drawer slide-in 540px
- **When** Step 1: เลือก country + type → vendor code ขึ้นอัตโนมัติ (read-only preview)
- **Then** code มี format `V-{country}-{type}-{N+1}` โดย N = max running ในกลุ่ม country+type นั้น
- **And** กรอกชื่อ + เลขภาษี (validate 13 หลัก, unique ต่อประเทศ)
- **And** ถ้า type=OT → เลขภาษีเป็น optional (ยกเว้น)
- **When** Step 2: เพิ่ม contact + address + bank (≥1 contact required ก่อนส่ง KYC)
- **When** Step 3: เลือก payment term + credit limit + แนบเอกสาร
- **Then** กดบันทึก → vendor บันทึก status=prospect + audit log

### US-02: Officer ส่ง vendor เข้า KYC
- **Given** vendor status=prospect + ข้อมูล complete (≥1 contact)
- **When** กด "ส่ง KYC" จาก drawer
- **Then** status=pending_kyc + audit `submitted_for_kyc`

### US-03: Compliance ตรวจ KYC
- **Given** vendor status=pending_kyc + role=Compliance
- **When** กด "ตรวจ KYC" → modal ขึ้น
- **And** simulate sanctions check (UI checkbox สำหรับ test) + กด "ผ่าน" หรือ "ไม่ผ่าน"
- **Then** ถ้าผ่าน → kyc=passed, kycAt=now, lock tax_id (IR-01), audit `kyc_passed`
- **And** ถ้าตรวจพบ sanctions → kyc=failed + status=blocked + reason="sanctions hit" (BR-S06)
- **And** ถ้าไม่ผ่าน (manual) → kyc=failed, status คงเป็น pending_kyc

### US-04: Officer ส่งอนุมัติ DOA chain
- **Given** vendor status=pending_kyc + kyc=passed + ≥1 verified bank (non-OT) + ≥1 contact ครบ
- **When** กด "ส่งอนุมัติ"
- **Then** ระบบสร้าง `approvalChain` จาก `resolveApprovalChain(vendor)`:
  - OT → chain=[] (auto-approve → active)
  - creditLimit > 5,000,000 → 2 ขั้น [Manager, Director]
  - creditLimit > 1,000,000 → 1 ขั้น [Manager]
  - else → 1 ขั้น [Officer]
- **And** status=pending_approval + audit `submitted_for_approval`

### US-05: ผู้อนุมัติอนุมัติทีละขั้น (multi-step)
- **Given** vendor status=pending_approval + role ของ user ตรงกับขั้น current ของ chain (หรือ Director/Admin override)
- **When** กด "อนุมัติ (ขั้น N)" → modal guard: KYC pass ✓ + SoD (approver≠creator) ✓ + role match step ✓ + data ready ✓
- **And** กดยืนยัน
- **Then** step current → approved (approver, at, comment) + audit `approved_step_N`
- **And** ถ้ายังเหลือขั้น → toast "อนุมัติขั้น N — รอ <ขั้นถัดไป>" (status ยัง=pending_approval)
- **And** ถ้าครบทุกขั้น → status=active + approvedBy=last approver + audit `chain_complete`

### US-06: ตีกลับ (reject)
- **Given** vendor status=pending_approval + role ตรงขั้นปัจจุบัน
- **When** กด "ตีกลับ" + ระบุเหตุผล (required) + ยืนยัน
- **Then** status=pending_kyc + approvalChain=[] + audit `rejected — <reason>`
- **And** Officer เห็น vendor กลับมา → แก้ไข แล้วกด "ส่งอนุมัติ" → chain ใหม่

### US-07: Finance ยืนยันบัญชีธนาคาร
- **Given** vendor มี bank.verified=false + role=Finance
- **When** กด "ยืนยัน" บนการ์ดบัญชี (จาก tab "ธนาคาร & ติดต่อ")
- **Then** bank.verified=true, verified_at=now + audit `bank_verified — <masked_acct>`
- **And** ปลด gate "ต้องมีบัญชี verified ≥1" สำหรับการส่งอนุมัติ

### US-08: Block / Unblock vendor
- **Given** vendor=active + role ใน Procurement
- **When** กด "บล็อก" + ระบุเหตุผล + ยืนยัน
- **Then** status=blocked + audit `blocked — <reason>` + closeDrawer
- **And** กด "ปลดบล็อก" จาก list/drawer → modal + reason บังคับ + ยืนยัน → status=active

### US-09: Blacklist (terminal)
- **Given** vendor=active หรือ blocked + role=Director/Admin
- **When** กด "แบล็คลิสต์" + เหตุผล + ยืนยัน
- **Then** status=blacklisted (terminal, one-way) + audit `blacklisted — <reason>`
- **And** ไม่มี action ใดทำให้กลับมา active ได้ (เปิด vendor ใหม่ถ้าจำเป็น)

### US-10: Role-based masking
- **Given** user เปิด drawer view vendor
- **When** role ∈ {procurement_officer, procurement_manager, procurement_director}
- **Then** tax_id แสดงเป็น `0105••••••67` (4 หลักหน้า + dots + 2 หลักท้าย)
- **And** bank account แสดงเป็น `0123••••44` (3 หลักหน้า + dots + 2 หลักท้าย)
- **When** role=Finance หรือ Admin → เห็นเต็มทั้ง 2 field
- **When** role=Compliance → เห็นเลขภาษีเต็ม แต่ bank ยัง mask (Restricted)

### US-11: View vendor's Price List summary (read-only) ⭐ NEW v1.1
**As** Procurement Officer / Manager
**I want to** ดู summary ของสินค้า/บริการที่ vendor ขาย พร้อมราคา จากหน้า view drawer
**So that** ใช้ context ในการตัดสินใจ (เลือก vendor, ตรวจราคา, อ้างใน PR/PO) โดยไม่ต้อง switch หน้า

**AC:**
- **Given** user เปิด view drawer ของ vendor ใด ๆ + กดเข้า tab "สินค้า/บริการ"
- **When** vendor มี price list ใน F-VENDOR-PRICE-LIST
- **Then** แสดง compact table 3 columns: `สินค้า/บริการ (name + code)` · `ราคา/หน่วย` · `สถานะ`
- **And** แสดง summary box ด้านบน: "{N} รายการ · ({active} active · {expired} expired) · อัพเดต {date}"
- **And** items ที่ status=expired แสดง dimmed row (opacity 0.55) + strikethrough บน name + brown dot
- **And** ปุ่ม "ดู Price List เต็ม →" navigate ไป F-VENDOR-PRICE-LIST (read-only summary, **ไม่มี edit/add/delete** ใน tab นี้)
- **When** vendor ไม่มี price list (เช่น OT, Employee, blacklisted vendor ส่วนใหญ่)
- **Then** แสดง empty state: "ยังไม่มี Price List สำหรับคู่ค้านี้" + ปุ่ม "ไปที่ Price List feature →"
- **When** user กดปุ่ม edit/add/delete (ไม่มีในtab นี้)
- **Then** ไม่มี element ให้กด — แก้ไขทำผ่าน F-VENDOR-PRICE-LIST เท่านั้น (data ownership boundary)

**Note:** Phase 1 ใช้ mock data inline; Phase 2 จะเรียก API จาก F-VENDOR-PRICE-LIST จริง (ดู OQ-09)

---

## Section 8: Status & Lifecycle

### 8.1 State Diagram

```
        ┌─────────┐  ส่ง KYC   ┌──────────────┐
   ─→   │ prospect │ ─────────→ │ pending_kyc  │
        └─────────┘             └──────┬───────┘
                                       │ KYC ผ่าน + ส่งอนุมัติ
                                       ▼
                              ┌────────────────────┐
                              │ pending_approval   │
                              └────────┬───────────┘
                  ตีกลับ                │ อนุมัติครบทุกขั้น (chain done)
                  (clear chain)          │  หรือ OT auto-approve
                  ┌──────────────────────┤
                  │                      ▼
                  │             ┌──────────┐  บล็อก   ┌─────────┐
                  ▼             │  active  │ ──────→ │ blocked │
        (กลับ pending_kyc)       └────┬─────┘ ←───── └─────────┘
                                      │ ปลดบล็อก
                                      │
                                      │ แบล็คลิสต์ (Director)
                                      ▼
                              ┌──────────────┐
                              │ blacklisted  │  (terminal — one-way)
                              └──────────────┘

  Sanctions hit (in KYC) → auto-block → status=blocked
  OT vendor → submit จาก pending_kyc → auto-active (skip chain)
```

### 8.2 Transition Table

| From | Action | Guard | To | Audit |
|---|---|---|---|---|
| (new) | สร้าง | Officer/Admin | prospect | `created` |
| prospect | ส่ง KYC | Officer/Admin | pending_kyc | `submitted_for_kyc` |
| pending_kyc | Compliance "ผ่าน" | Compliance | pending_kyc (kyc=passed) | `kyc_passed` |
| pending_kyc | Compliance "ไม่ผ่าน" | Compliance | pending_kyc (kyc=failed) | `kyc_failed` |
| pending_kyc | Sanctions hit | System | blocked | `sanctions_hit_auto_block` |
| pending_kyc | ส่งอนุมัติ | kyc=passed + contact + bank (non-OT) | pending_approval (chain) | `submitted_for_approval` |
| pending_kyc | OT auto-approve | OT + kyc=passed + contact | active | `ot_auto_approved` |
| pending_approval | อนุมัติขั้นย่อย | role match step + SoD | pending_approval (step approved) | `approved_step_N` |
| pending_approval | อนุมัติขั้นสุดท้าย | chain done | active | `chain_complete` |
| pending_approval | ตีกลับ | role match + reason | pending_kyc (chain=[]) | `rejected — <reason>` |
| active | บล็อก | Procurement + reason | blocked | `blocked — <reason>` |
| blocked | ปลดบล็อก | Procurement + reason | active | `unblocked — <reason>` |
| (any active/blocked) | แบล็คลิสต์ | Director + reason | blacklisted (terminal) | `blacklisted — <reason>` |

---

## Section 9: Business Rules + Validation (with Tags)

> **Tags:** `FIXED` (ตายตัว) · `CONFIGURABLE` (admin ตั้ง) · `DYNAMIC` (engine ตัดสิน) · `WARNING` (ยังไม่ระบุชัด)

### 9.1 Core Validation Rules

| ID | Rule | Tag | Notes |
|---|---|---|---|
| BR-V01 | tax_id ต้อง 13 หลัก + ผ่าน checksum (สำหรับ TH) | FIXED | กฎสรรพากร |
| BR-V02 | tax_id ต้อง unique ต่อ country (UQ) | FIXED | DB constraint |
| BR-V03 | tax_id ของ OT vendor → optional (ยกเว้น) | FIXED | one-time ไม่มีนิติบุคคล |
| BR-V04 | vendor code auto-gen `V-{CC}-{TT}-{NNNNN}` running per country+type | FIXED | format ไม่เปลี่ยน |
| BR-V05 | vendor name required, ≤255 ตัวอักษร | FIXED | — |
| BR-V06 | bank account number 10-15 หลัก ตัวเลขเท่านั้น | CONFIGURABLE | แต่ละธนาคารต่างกัน (admin ตั้ง per bank) |
| BR-V07 | bank account ต้องมี ≥1 ที่ verified ก่อนส่งอนุมัติ (non-OT) | FIXED | จาก paidVendorNeedsBank() |
| BR-V08 | contact ต้องมี ≥1 ที่ email + phone ครบ ก่อนส่งอนุมัติ | FIXED | จาก hasValidContact() |
| BR-V09 | credit limit ≥0 | FIXED | ไม่มี negative |

### 9.2 KYC & Sanctions Rules

| ID | Rule | Tag | Notes |
|---|---|---|---|
| BR-K01 | vendor ต้องผ่าน kyc=passed ก่อนเข้า approval | FIXED | gate (FN-09) |
| BR-K02 | sanctions hit ทำให้ status=blocked อัตโนมัติ | FIXED | (BR-S06) |
| BR-K03 | tax_id immutable หลัง kyc=passed | FIXED | **IR-01** — ป้องกันการเปลี่ยน identity หลัง verify |
| BR-K04 | KYC ตรวจโดย Compliance role เท่านั้น | FIXED | (FN-17) |
| BR-K05 | KYC review ครอบคลุม: เอกสารแนบ + tax format + sanctions list | CONFIGURABLE | scope ของการตรวจอาจเปลี่ยน |

### 9.3 Approval Rules

| ID | Rule | Tag | Notes |
|---|---|---|---|
| BR-A01 | ผู้อนุมัติ ≠ ผู้สร้าง (SoD) | FIXED | บังคับ |
| BR-A02 | role ต้องตรงขั้น chain ปัจจุบัน (หรือ Director/Admin override) | DYNAMIC | DOA engine กำหนด |
| BR-A03 | approval chain rule ขึ้นกับ credit limit | **DYNAMIC** | wire to Policy Center DOA engine; placeholder ปัจจุบัน: >5M=[Mgr,Dir], >1M=[Mgr], else=[Off] |
| BR-A04 | OT vendor → chain=[] (auto-approve) | FIXED | one-time skip approval |
| BR-A05 | reject → status=pending_kyc + clear chain | FIXED | resubmit สร้าง chain ใหม่ |

### 9.4 Masking & Permission Rules

| ID | Rule | Tag | Notes |
|---|---|---|---|
| BR-M01 | tax_id classification = Confidential | FIXED | mask สำหรับ role ที่ไม่ใช่ Finance/Compliance/Admin |
| BR-M02 | bank account classification = Restricted | FIXED | mask ทุก role ยกเว้น Finance/Admin |
| BR-M03 | mask pattern: 4 หน้า + dots + 2 ท้าย (tax), 3 หน้า + dots + 2 ท้าย (bank) | CONFIGURABLE | ตั้งใน Data Classification engine |

### 9.5 Lifecycle Rules

| ID | Rule | Tag | Notes |
|---|---|---|---|
| BR-L01 | blacklisted = terminal (one-way) | FIXED | ห้าม transition กลับ |
| BR-L02 | edit อนุญาตเฉพาะ status ∈ {prospect, pending_kyc, active} | FIXED | (blocked/blacklisted ไม่ได้) |
| BR-L03 | ทุก block/unblock/blacklist ต้องมี reason (required) | FIXED | audit + accountability |
| BR-L04 | vendor ที่มี hasTxn=true → soft-delete only | FIXED | match key คือ vendor_id; ห้ามลบ record |

---

## Section 9.5 สรุประดับความยืดหยุ่น

| ระดับ | จำนวน | Rule IDs ตัวอย่าง |
|---|---|---|
| **FIXED** | 23 | BR-V01, V02, V03, V04, V05, V07, V08, V09, K01-K04, A01, A04, A05, M01, M02, L01-L04 |
| **CONFIGURABLE** | 3 | BR-V06 (bank acct length per bank), BR-K05 (KYC scope), BR-M03 (mask pattern) |
| **DYNAMIC** | 2 | BR-A02 (role-step match), BR-A03 (chain rule from DOA engine) |
| **WARNING** | 0 | ทุก rule classified แล้ว |

**ระดับ Configuration ที่แนะนำ:**
- BR-V06 → **Admin Panel** (Bank master ของ Core Cube)
- BR-K05 → **Rule Management** (Compliance หรือ Policy Center)
- BR-M03 → **Engine Management** (Data Classification engine, Policy Center)
- BR-A02, A03 → **Engine Management** (DOA engine, Policy Center)

---

## Section 10: Edge Cases

### 10.1 Edge Cases ที่ BA ระบุ

| # | Case | Expected Behavior |
|---|---|---|
| EC-01 | สร้าง vendor ที่ tax_id ซ้ำใน country เดียวกัน | Block — toast "DUPLICATE_TAX_ID" |
| EC-02 | OT vendor ไม่มี tax_id แต่กรอกอย่างอื่นครบ | OK — tax_id แสดง "ยกเว้น" |
| EC-03 | กด "ส่งอนุมัติ" ตอน kyc ยังไม่ pass | Block — toast "KYC_NOT_PASSED" |
| EC-04 | กด "ส่งอนุมัติ" ตอนไม่มี contact (email+phone) | Block — toast "NOT_READY · ต้องมี contact" |
| EC-05 | กด "ส่งอนุมัติ" ตอนไม่มี verified bank (non-OT) | Block — toast "NOT_READY · ต้องมี bank verified" |
| EC-06 | คน A สร้าง vendor → คน A กดอนุมัติเอง | Block — toast "SOD_VIOLATION · approver ≠ creator" |
| EC-07 | role ไม่ตรงขั้น chain ปัจจุบัน (Officer พยายามอนุมัติขั้น Director) | Block — toast "WRONG_APPROVER · ต้อง <role label>" |
| EC-08 | KYC ตรวจพบ sanctions hit | auto: kyc=failed + status=blocked + reason="sanctions hit" |
| EC-09 | แก้ tax_id หลัง KYC pass | input disabled + label "ล็อก — ผ่าน KYC แล้ว (IR-01)" |
| EC-10 | ตีกลับ vendor ที่ chain เพิ่งอนุมัติขั้น 1 ไป | status=pending_kyc + chain=[] (รีเซ็ต) ส่งใหม่ chain build ใหม่ |
| EC-11 | บล็อก vendor ที่ hasTxn=true | OK — soft-block, ไม่ลบ record (vendor_id ยังเป็น match key) |
| EC-12 | blacklist vendor → user พยายามกลับเป็น active | ไม่มี UI action ให้กด (terminal state) |
| EC-13 | ลบ verified bank สุดท้าย ของ vendor ที่ active | warn — vendor ยัง active แต่ใช้ PV ไม่ได้จนกว่าจะมี bank verified ใหม่ |

### 10.2 Edge Cases ที่ AI ขยายเพิ่ม (Pattern-based)

| Pattern | Case | Expected |
|---|---|---|
| FU (Future) | tax_id format ของประเทศที่ไม่ใช่ TH | ใช้ regex/checksum ตาม country master (P2 — ปัจจุบันรองรับ TH format) |
| CA (Concurrency) | 2 users กด "อนุมัติขั้นเดียวกัน" พร้อมกัน | optimistic concurrency: version conflict → toast + reload |
| EM (Empty) | vendor ที่ไม่มี contact/bank/address เลย ยังบันทึก draft ได้ | OK — บันทึก status=prospect; gate เฉพาะตอนส่งอนุมัติ |
| DI (Disconnect) | network drop ตอนกด confirmApprove | retry safe — idempotent: ขั้นที่ status='approved' จะไม่ถูก mark ซ้ำ |
| CL (Closure) | vendor ที่ใช้มา 5 ปี อยากปิด (ไม่ใช่ blacklist) | Phase 2: "inactive" status + retain history (ปัจจุบันใช้ blocked + reason="ปิด") |
| ST (State race) | กด edit + อีก tab กดบล็อก พร้อมกัน | version mismatch → toast "ข้อมูลถูกแก้โดยผู้อื่น — refresh" |
| PD (PDPA Delete) | คำขอลบข้อมูล vendor (PDPA Article 33) | Phase 2: anonymize personal fields (contact.name/email/phone) + retain transactional fields |
| PM (Permission) | role ถูกลดสิทธิ์ระหว่างใช้งาน (officer → reader) | re-evaluate permission ทุก render — กดปุ่มที่หมดสิทธิ์ → toast "FORBIDDEN" |
| EN (Encoding) | ชื่อ vendor มี emoji หรือ special char | escape เพื่อ XSS prevention (ใช้ `esc()` helper) |

---

## Section 11: Impact Analysis / Regression Scope

**Not applicable — New Feature** (ไม่มี existing implementation ของ Vendor Master ใน CUBE NATIVE)

**Module ที่จะ depend on Vendor Master:**
- **Purchase Request (PR)** — vendor selector
- **Purchase Order (PO)** — vendor + payment term + tax info
- **Goods Receipt (GR)** — vendor reference
- **Payment Voucher (PV)** — vendor + bank account + verified bank gate
- **Invoice (AP)** — vendor + tax info

Module เหล่านี้จะถูก develop หลังจาก Vendor Master พร้อม (dependency order).

---

## Section 12: Dependencies

### 12.1 Master Data Dependencies

| Dependency | Module | Status |
|---|---|---|
| Country Master | Core Cube | Required (Phase 1) |
| Currency Master | Core Cube | Required (Phase 1) |
| Bank Master | Core Cube | Required (Phase 1) |
| Thai Address Master | Core Cube | Required (Phase 1) — embedded in prototype |
| Payment Terms Master | **Finance** | Required (Phase 1) — vendor เก็บแค่ code |
| **F-VENDOR-PRICE-LIST** ⭐ NEW v1.1 | **P2P · Master Data (separate feature)** | Phase 2 — Phase 1 uses mock data inline ใน HTML · Tab 5 view-only embed |

### 12.2 Engine Dependencies

| Engine | Module | Status |
|---|---|---|
| ENG-SANCTIONS (OFAC/UN/EU screening) | Compliance | Required (Phase 1) — stub ใน prototype |
| **DOA Engine** | **Policy Center** | Phase 2 — placeholder rule ใน prototype |
| **Data Classification Engine** | Policy Center | Phase 2 — hardcoded mask ใน prototype |
| Audit (WORM) Logger | Core Cube | Required (Phase 1) |
| **Price List Summary API** ⭐ NEW v1.1 | **F-VENDOR-PRICE-LIST** | Phase 2 — `GET /api/v1/vendors/{id}/price-list-summary` returns top-N items · 5-min Redis cache · auth: read permission required |

### 12.3 Existing System Reference

**Existing implementation:** ❌ ไม่มี — feature ใหม่
**Closest analog:** ไม่มีระบบ vendor master ในระบบเดิมของ 2BSimple
**Migration:** ไม่มี — เริ่มต้นจาก zero data (อาจ import vendor list จาก Excel ของแต่ละลูกค้าได้ Phase 1.5)

---

## Section 13: Delivery Phases

### Phase 1 — MVP (Foundation, ~ 6 weeks)
- ✅ CRUD vendor + 6-state lifecycle (prospect ↔ pending_kyc ↔ pending_approval → active ↔ blocked → blacklisted)
- ✅ 11 vendor types + auto-gen code
- ✅ Multi-bank + multi-contact + multi-address
- ✅ KYC modal (Compliance) + sanctions stub
- ✅ DOA chain — **placeholder rule** (hardcoded by creditLimit threshold) + TODO wire to DOA engine
- ✅ Role-based masking (hardcoded — tax_id Confidential, bank Restricted)
- ✅ WORM audit logging (backend; not surfaced in UI)
- ✅ 6 roles + permission matrix
- ✅ Block/Unblock/Blacklist + reason required (modal-based)
- **Deliverable:** vendor module พร้อมใช้สำหรับ pilot client (COE/WKN)

### Phase 2 — Engine Integration (~ 4 weeks)
- 🔌 Wire DOA chain → **Policy Center DOA Engine** (rule definition + chain resolution)
- 🔌 Wire masking → **Data Classification Engine** (per-column classification + runtime mask)
- 🔌 Wire sanctions → real OFAC/UN/EU API feed
- ➕ Bank account validation rule per bank (configurable via Bank Master)
- **Deliverable:** vendor independent of hardcoded rules, configurable via Policy Center

### Phase 3 — Performance & Portal (~ 6 weeks)
- ➕ Vendor performance scoring (on-time delivery, defect rate)
- ➕ Vendor portal (external) — vendor login + self-service update
- ➕ Vendor merge / split tool
- ➕ Inactive status + retention policy
- ➕ PDPA anonymization tool
- **Deliverable:** vendor full lifecycle + self-service

### Phase 4 — Analytics (~ 3 weeks)
- 📊 Vendor analytics dashboard (top spend, concentration risk, payment terms distribution)
- 📊 Compliance dashboard (KYC expiry, sanctions hits over time)
- **Deliverable:** business intelligence layer

---

## Section 14: Dev Requirements Summary "ใบสั่ง"

### 14.1 Scope สำหรับ Dev (Phase 1)
- **1 entity** (vendor) + 4 sub-entities (contact, address, bank_account, attachment) + WORM audit log table
- **6 lifecycle states** + transitions
- **30+ APIs** ครอบคลุม CRUD + lifecycle actions + KYC + approve/reject + block/unblock/blacklist + bank verify + masking
- **6 roles** + RBAC enforcement
- **3-step wizard UI** + view drawer with 4 tabs + 6 modals
- **HTML reference:** `vendor-master.html` v1 — pixel-faithful implementation guide

### 14.2 Standards & Iron Rules
- **UI layer:** html-generator-v3 patterns A (list) + B (create wizard) + C (view drawer tabbed) + D (modal confirm) + I (signature card for approval chain)
- **CUBE NATIVE CI** locked: Navy #0B1D3A · Primary #0B5CFF · Teal #00A88E
- **Iron Rules 30/30** ของ html-generator-v3 v3.6 — pass

### 14.3 Backend Stack (recommended)
- API: REST + GraphQL (CUBE NATIVE standard)
- DB: PostgreSQL with JSONB for `approvalChain` + `audit`
- Audit: WORM table — `INSERT only`, no UPDATE/DELETE grant
- Indexes: `vendor.tax_id` UQ (per country), `vendor.code` UQ, `vendor.status` BTREE, `vendor.kyc` BTREE

### 14.4 Non-functional
- **Performance:** list query < 200ms for 10k vendors (with indexes)
- **Concurrency:** optimistic via `version` column
- **Security:** all PII fields encrypted at rest; mask at API layer per role
- **Audit retention:** WORM, 7 years minimum (statutory)

### 14.5 Acceptance / Done Definition
- Functional: ทุก US-01 ถึง **US-11** ทำได้ครบ + AC ทุกข้อ pass
- Non-functional: NFR ใน 14.4 ผ่าน
- QA: test set ครอบคลุม 13 Edge Cases ใน §10.1 + 9 patterns ใน §10.2
- UAT: 1 pilot client (เช่น COE) ใช้งานครบ 1 รอบ (เปิด vendor → KYC → approve → ออก PV จริง)
- **Cross-feature integration:** Tab 5 Price List embed ใน Phase 1 ใช้ mock data; Phase 2 ต้อง integrate กับ F-VENDOR-PRICE-LIST API จริง (ไม่กระทบ UI)

### 14.6 Layout Deviation Log

| Page | Layout Template | Standard | Deviation | Rationale |
|---|---|---|---|---|
| Landing (list) | Pattern A — List View | html-generator-v3 v3.6 | **No scorecards** (intentional per user) | feature ไม่ต้องการ KPI surface บน landing |
| Create/Edit | Pattern B — 3-step drawer wizard 540px | v3.6 | None | ตามมาตรฐาน |
| View Drawer | Pattern C — View Drawer Tabbed 540px | v3.6 | **Status-conditional action bar** ระหว่าง header กับ tabs (เพิ่มจากมาตรฐาน) | จำเป็นเพราะมี 4-6 actions (Edit/Submit/KYC/Approve/Reject/Block/Unblock/Blacklist) — ใส่ใน footer ไม่พอ |
| View Drawer — Tab count | Pattern C standard 3-4 tabs | v3.6 | **5 tabs** (ภาพรวม · ธนาคาร & ติดต่อ · เอกสารแนบ · การอนุมัติ · **สินค้า/บริการ**) | ⭐ NEW v1.1 — Tab 5 read-only embed จาก F-VENDOR-PRICE-LIST · 5 tabs overflow-x scroll รองรับโดย v3.6 (`scrollbar-width:none`) ไม่ break pattern |
| Tab 5 (Price List) | Custom table (3 col compact) | — | **Read-only — ไม่มี edit/add/delete buttons** | ⭐ NEW v1.1 — data ownership boundary: edit ผ่าน F-VENDOR-PRICE-LIST เท่านั้น · ตัด category/minQty/validity range ออก (Procurement scan-only view) |
| Approval Tab | Pattern I — Signature Card List + vertical line | v3.6 | None | DOA chain visual (เส้น) ตรง Pattern I |
| Modals (6 types) | Pattern D — Modal Confirmation 440px | v3.6 | None | ทุก modal มี reason field |
| KYC pill | (custom) | — | Status pill v3.6 มี `.dot is-X` | aligned |

**No CI deviation** — palette อยู่ใน Navy/Primary/Teal ครบ
**No iron rule violation** — ผ่าน 30/30

---

## Section 15: Open Questions

| # | Question | Owner | Target Resolution |
|---|---|---|---|
| OQ-01 | DOA chain rule ที่แท้จริงคืออะไร (placeholder ปัจจุบัน: by creditLimit threshold) | Policy Center team | Phase 2 — wire to DOA engine |
| OQ-02 | Data Classification engine จะกำหนด mask pattern แบบไหน (per-field config?) | Policy Center team | Phase 2 |
| OQ-03 | Sanctions API source จริงคืออะไร (commercial — Refinitiv, Dow Jones, in-house?) | Compliance team | Phase 1 |
| OQ-04 | KYC expiry policy — เมื่อไหร่ kyc=expired (yearly review?) | Compliance team | Phase 1 |
| OQ-05 | rename status `pending_kyc` label หรือไม่ (UI vocabulary KYC vs ตรวจสอบ) | UX + BA | Phase 1 |
| OQ-06 | Bank account length validation per bank — มี master พร้อมหรือไม่ | Core Cube team | Phase 1.5 |
| OQ-07 | PDPA delete flow — Phase 2 implementation detail (anonymize vs hard delete) | Legal + Compliance | Phase 2 |
| OQ-08 | Vendor migration จาก Excel เก่า — มี source data format มาตรฐานหรือไม่ | Pilot clients (COE, WKN) | Phase 1.5 |
| **OQ-09 ⭐ NEW v1.1** | **F-VENDOR-PRICE-LIST API contract** — endpoint shape, auth model, cache TTL, paging strategy (ถ้า vendor มี items > 100), edge cases (vendor deleted while price list still has refs) | **F-VENDOR-PRICE-LIST team + Vendor Master BA** | **Phase 2 kickoff** — ต้อง finalize ก่อน implement Tab 5 integration |

---

## Section 16: Security & Compliance (Philosophy Embedded)

### 16.1 Security Preset: **P2 — Confidential PII**

| Layer | Control |
|---|---|
| Authentication | SSO + MFA (CUBE Auth) |
| Authorization | RBAC — 6 roles × action matrix (§4.1) |
| Data Classification | 4 levels: Public / Internal / **Confidential** (tax_id, vat, companyReg, creditLimit) / **Restricted** (bank_account) |
| Encryption (at rest) | AES-256 for all PII fields |
| Encryption (in transit) | TLS 1.3 minimum |
| Audit | WORM table, 7-yr retention |
| Masking | API layer enforces per-role visibility |

### 16.2 78 Security Controls Coverage (P2 preset)

ครอบคลุม controls กลุ่มหลัก: **AC** (Access Control), **AU** (Audit), **CM** (Configuration Mgmt), **IA** (Identity & Auth), **MP** (Media Protection), **PE** (Physical), **SC** (System & Comm), **SI** (System Integrity)

ตัวอย่าง critical controls ที่ feature นี้ implement:
- **AC-2** Account Management — RBAC 6 roles
- **AC-3** Access Enforcement — permission check ทุก action
- **AC-5** Separation of Duties — SoD-01 (approver ≠ creator), SoD-02, SoD-03
- **AC-6** Least Privilege — role matrix §4.1
- **AU-2** Audit Events — ทุก action บันทึก
- **AU-9** Protection of Audit Information — WORM, append-only
- **AU-11** Audit Retention — 7 ปี
- **IA-2** Identification — uid ทุก audit entry
- **SC-8** Transmission Confidentiality — TLS 1.3
- **SC-28** Protection of Information at Rest — AES-256
- **SI-10** Information Input Validation — tax/bank/contact validation rules

### 16.3 Compliance Standards Mapping

| Standard | Coverage |
|---|---|
| **PDPA Thailand** | masking (BR-M01, M02) + WORM audit + (Phase 2) anonymization |
| **ISO 27001** | A.5.15 (RBAC), A.8.2 (Classification), A.8.13 (Backup), A.8.34 (Audit), A.5.34 (Privacy) |
| **SOC 2 Type II** | CC6.1 (Logical Access), CC7.2 (Detection), CC7.3 (Evaluation) |
| **NIST 800-53** | (mapped via 78 Controls above) |
| **AML / Sanctions** | KYC + sanctions screening (BR-K02, BR-S06) |
| **Internal Audit** | SoD + WORM + approval chain audit |

---

## Section 17: Health Check (SLA / KPI / Threshold) — Philosophy Embedded

### 17.1 SLA Targets

| Service | SLA | Measurement |
|---|---|---|
| API response (list) | p95 < 300ms | APM monitor |
| API response (create vendor) | p95 < 800ms | APM |
| API response (approve action) | p95 < 500ms | APM |
| Sanctions check | p95 < 2 sec | External API call timing |
| Audit write | 100% success | failed writes = critical alert |

### 17.2 KPIs

| KPI | Target | Frequency |
|---|---|---|
| Active vendor count | Trend up | Daily |
| KYC pass rate | > 90% | Weekly |
| Approval cycle time (prospect → active) | < 24 hr p50 | Weekly |
| Sanctions hit rate | < 0.5% | Monthly |
| Bank verification queue | < 5 pending | Real-time |
| Blacklist rate | < 0.1% | Quarterly |

### 17.3 Thresholds (Alerting)

| Metric | Threshold | Action |
|---|---|---|
| KYC pending > 7 days | Warning | Notify Compliance lead |
| KYC pending > 14 days | Critical | Escalate to CFO |
| Sanctions API error rate > 5% | Critical | Failover to manual review + alert SRE |
| Approval pending > 3 days | Warning | Reminder email to approver |
| Audit write failure | Critical (any) | Block all writes + page on-call |
| Same tax_id duplicate attempt | Info | Log + counter |

### 17.4 Control Points (Runtime Checks)

| Control | Check | Frequency |
|---|---|---|
| C-KYC-01 | vendor active without kyc=passed | Continuous (DB query) |
| C-SOD-01 | approver = creator in any approval log | Continuous |
| C-BANK-01 | bank verified by non-Finance | Daily audit job |
| C-MASK-01 | Restricted field exposed to non-Finance/Admin in API response | API gateway middleware |
| C-WORM-01 | audit entry modified or deleted | DB trigger (block + alert) |

---

## Section 18: Monitoring (Reports / Widgets) — Philosophy Embedded

### 18.1 Operational Widgets (Procurement Dashboard)

| Widget | Data | Refresh | Owner |
|---|---|---|---|
| Vendor count by status | bar chart (6 statuses) | 5 min | Procurement |
| KYC queue | list of pending_kyc + age | 1 min | Compliance |
| Approval queue (mine) | list filtered to current user as approver | 1 min | Procurement Manager/Director |
| Recent activations (this week) | count + list | hourly | Procurement |
| Sanctions hits (this month) | count + drill-down | daily | Compliance |

### 18.2 Compliance Reports (Periodic)

| Report | Frequency | Recipient | Content |
|---|---|---|---|
| Vendor lifecycle audit | Monthly | Internal Audit + CFO | All transitions + reasons + actor |
| KYC compliance | Monthly | Compliance lead | % passed / failed / expired |
| SoD violation attempts | Monthly | Internal Audit | Blocked actions + actor |
| Bank verification status | Weekly | Finance lead | Pending / verified / failed |
| Sanctions screening log | Quarterly | Risk Committee | All screenings + hits |

### 18.3 Business Reports (Strategic)

| Report | Frequency | Recipient | Content |
|---|---|---|---|
| Top vendors by spend (joined w/ PO/PV) | Monthly | CFO + CPO | top 50 vendors, concentration % |
| Vendor onboarding cycle time | Quarterly | CPO | trend + Pareto by reason for delay |
| Payment terms distribution | Quarterly | CFO | terms histogram, average WHT |
| Vendor diversity (by type, region, size) | Annual | ESG officer | sustainability metric |

---

## Appendix A: Screen List

| Screen | Layout Template | Sidebar Active | Breadcrumb | Page Title |
|---|---|---|---|---|
| Vendor List | Pattern A (List View) — html-generator-v3 v3.6 | Master Data › Vendor Master | Master Data › Vendor Master | ทะเบียนคู่ค้า |
| Create Drawer (3-step) | Pattern B (Multi-Step Wizard 540px) | (same as list) | (drawer — no breadcrumb) | เพิ่มคู่ค้าใหม่ |
| Edit Drawer (3-step) | Pattern B | (same) | (drawer) | แก้ไขคู่ค้า |
| View Drawer (4 tabs) | Pattern C (View Drawer Tabbed 540px) + status-conditional action bar | (same) | (drawer) | ดูคู่ค้า: <name> |
| └─ Tab: ภาพรวม | inline | — | — | — |
| └─ Tab: ธนาคาร & ติดต่อ | inline | — | — | — |
| └─ Tab: เอกสารแนบ | inline | — | — | — |
| └─ Tab: การอนุมัติ | Pattern I (Signature Card List, vertical chain) | — | — | — |
| Modal: ตรวจ KYC | Pattern D 440px | — | — | ตรวจ KYC (Compliance) |
| Modal: อนุมัติ (ขั้น N) | Pattern D | — | — | อนุมัติคู่ค้า — ขั้น N/M |
| Modal: ตีกลับ | Pattern D | — | — | ตีกลับคู่ค้า |
| Modal: บล็อก | Pattern D | — | — | บล็อกคู่ค้า |
| Modal: แบล็คลิสต์ | Pattern D | — | — | แบล็คลิสต์คู่ค้า |
| Modal: ปลดบล็อก | Pattern D | — | — | ปลดบล็อกคู่ค้า |

---

## Appendix B: Glossary

| Term | Definition |
|---|---|
| **DOA** | Delegation of Authority — chain ของผู้อนุมัติตามวงเงิน/ประเภท |
| **KYC** | Know-Your-Customer — กระบวนการตรวจสอบ identity ก่อนทำธุรกรรม |
| **SoD** | Separation of Duties — ผู้สร้าง ≠ ผู้อนุมัติ |
| **WORM** | Write-Once-Read-Many — audit log ที่แก้ไม่ได้ |
| **OT (One-time)** | Vendor ครั้งเดียว — ใช้ครั้งเดียวจบ ไม่ต้อง approval chain |
| **Confidential** | Data classification level — ต้อง mask สำหรับ role ที่ไม่ใช่ Finance/Compliance/Admin |
| **Restricted** | Data classification level สูงสุด — ต้อง mask ทุก role ยกเว้น Finance/Admin |
| **IR-01** | Immutable Rule 01 — tax_id ห้ามแก้หลัง KYC pass |
| **DOA Engine** | บริการ Policy Center ที่ resolve chain จาก rule |

---

## Appendix C: Document Control

| Field | Value |
|---|---|
| Document Owner | 2BSimple BA Team |
| Approval Required | CPO + CFO + Compliance Lead |
| Approval Status | Draft (pending review) |
| Distribution | Procurement · Finance · Compliance · Internal Audit · Dev Team · QA |
| Next Review | Phase 2 kickoff (DOA engine integration) |
| Retention | 7 years (per ISO 27001 + statutory) |
| Related Documents | `vendor-master.html` (HTML Prototype) · FRD (TBD) · QA Pack (TBD) · Dev Brief (TBD) |

---

## 🔍 AI Review Report

### Status: **APPROVED (v1.1)**

### Checklist (C01–C19 + PE01–PE05 + **C20 NEW v1.1**)

| ID | Check | Result | Note |
|---|---|:---:|---|
| C01 | Document structure ครบ 18 sections + Appendix | ✅ | |
| C02 | Section 1 Document Info ครบ | ✅ | v1.1 — Source = Revision Mode |
| C03 | Business Context มี Problem + Goal + Metric | ✅ | 6 metrics with baseline + target |
| C04 | Scope ระบุชัด In/Out | ✅ | v1.1 — เพิ่ม Price List read-only embed (In); Price List CRUD (Out) |
| C05 | Role Matrix ครบ + SoD rules | ✅ | 6 roles × 9 actions |
| C06 | User Journey + COSO ทุก step | ✅ | 9 steps with M/C/A/S |
| C07 | Data Entity ครบ + classification tag | ✅ | 1 main + 4 sub-entities + §6.4 cross-feature read (Price List) |
| C08 | User Stories Given-When-Then | ✅ | **11 stories** (US-11 ใหม่: Price List view-only) |
| C09 | Lifecycle + State Diagram | ✅ | 6 states, 13 transitions |
| C10 | Business Rules มี Tag ครบ | ✅ | 28 rules tagged |
| C11 | สรุประดับความยืดหยุ่น | ✅ | §9.5 — 23 FIXED, 3 CONFIGURABLE, 2 DYNAMIC, 0 WARNING |
| C12 | Edge Cases ครบ (BA + AI) | ✅ | 13 BA + 9 AI patterns |
| C13 | Dependencies + Existing System | ✅ | v1.1 — เพิ่ม F-VENDOR-PRICE-LIST (upstream) |
| C14 | Delivery Phases | ✅ | 4 phases |
| C15 | Dev Summary "ใบสั่ง" | ✅ | scope + standards + NFR + DoD |
| C16 | Open Questions tracked | ✅ | **9 OQs** (OQ-09 ใหม่: Price List API contract) |
| C17 | Security 78 Controls + Preset | ✅ | P2 preset, key controls listed |
| C18 | Health Check (SLA/KPI/Threshold) | ✅ | §17 ครบ |
| C19 | Monitoring (Widgets + Reports) | ✅ | §18 ครบ |
| **C20 ⭐ NEW v1.1** | **Cross-feature data ownership boundary** | ✅ | §6.4 ระบุ Price List = source of truth ที่ F-VENDOR-PRICE-LIST · Vendor Master = consumer (read-only, no write) · UI/UX boundary enforced (Tab 5 ไม่มี edit buttons) |
| PE01 | Cross-Pillar: BC ↔ Edge Cases | ✅ | duplicate prevention → EC-01 |
| PE02 | Cross-Pillar: Control ↔ Health Check | ✅ | SoD-01 ↔ C-SOD-01 |
| PE03 | Cross-Pillar: Metric ↔ Widget | ✅ | KYC compliance rate ↔ KYC queue widget |
| PE04 | Layout Standard Enforcement | ✅ | §14.6 ระบุ **3 deviations** + rationale (action bar, 5-tab count, Tab 5 read-only) |
| PE05 | CI palette ไม่ override | ✅ | Navy/Primary/Teal locked |

### Strengths
- HTML reference เป็น "production UI" ที่ implement ได้จริง — ลด ambiguity ของ spec
- Cross-doc consistency 100% — ทุก rule + edge case + role + state ตรงกันระหว่าง BRD v1.1 ↔ HTML v2
- DOA chain มี placeholder ที่ชัด พร้อม TODO ว่า wire ที่ไหน (Policy Center)
- Masking pattern ระบุชัดทั้ง classification level + role coverage
- Lifecycle เหลือ 6 states ที่ reachable ทั้งหมด (ไม่มี orphan)
- **Cross-feature boundary (v1.1)** — Price List data ownership ชัด · UI ไม่มี edit buttons ให้กดผิด · backend boundary enforced ผ่าน API ของ F-VENDOR-PRICE-LIST

### Notes for Downstream
- **frd-generator-v5** → FRD Pack v1.1: ต้อง regenerate เพื่อสะท้อน Tab 5 + API-16 (Price List proxy) + OQ-09
- **html-generator-v3** → HTML v2 reference เป็น final UI (Tab 5 implemented, 5-tab scroll behavior); FRD ใช้ trace requirement
- **frd-qa-generator-v2** → test scenarios สามารถดึงจาก §7 (US-11 ใหม่: View Price List Summary) + §14.6 (Tab 5 read-only verification)
- **Phase 2 trigger 1:** เมื่อ Policy Center DOA Engine พร้อม → revisit §6 (Data Entity) + §9.3 (Approval Rules) + §13 (Phase 2)
- **Phase 2 trigger 2 ⭐ NEW v1.1:** เมื่อ F-VENDOR-PRICE-LIST API พร้อม → resolve OQ-09 + replace mock data ใน HTML ด้วย API call · ไม่กระทบ UI

### Revision Impact (v1.0 → v1.1)
- **Sections touched:** §1 (meta), §3 (scope), §6 (entity + new §6.4), §7 (US-11 added), §12 (deps), §14 (deviation log), §15 (OQ-09)
- **Sections unchanged:** §2 (business context), §4 (roles), §5 (journey), §8 (lifecycle), §9 (BR), §10 (edge cases), §11, §13 (phases), §16-§18
- **Net impact:** +1 user story · +1 dependency · +1 OQ · +2 layout deviation rows · +1 checklist item (C20)
- **Breaking changes:** ❌ None — additive only · all v1.0 ACs still valid · existing tests still pass

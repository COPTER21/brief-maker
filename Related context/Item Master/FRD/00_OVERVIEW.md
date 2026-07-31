# 00_OVERVIEW — F-PRODUCT-MASTER-001 Product Master (ทะเบียนสินค้า)

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Open Questions
> **⭐ Generation Mode: REVERSE — HTML `product-master.html` (v6, ผ่าน gate ครบ) = Source of Truth · ไม่มี BRD upstream (pack v3.5 เดิม = stale เพราะ scope เปลี่ยน)**

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-PRODUCT-MASTER-001 (scope-local prefix ในเอกสาร = `F-PDM` — ดู 07 CD-01) |
| **Feature Name** | Product Master — ทะเบียนสินค้า |
| **Module** | Master Data (P2P · Core Cube — Operation area) |
| **Variant** | FULL (9 files + INDEX) |
| **Status** | DRAFT (รอ review) |
| **FRD Version** | 2.0 (2026-07-27) — แทน pack v3.5 ทั้งชุด |
| **Generator** | frd-generator-v6 (v6.1 · Reverse Mode) |
| **Source Brief** | — (ไม่มี — Reverse Mode) |
| **Source BRD** | — (v3.5 BRD = superseded/stale — ห้ามใช้อ้าง) |
| **Source HTML** | `product-master.html` v6 (md5 `af945e0378a46d3d6207da785c541470`) — gates: node PASS · audit v6 FAIL=0 · Playwright 46/46 · JS error 0 |
| **Author** | BA (2BSimple) |
| **Reviewers** | Strike (scope) · พี่เบิร์ด (BE) · Chin (UI) |

**Variant decision log:** fallback rule — pages = 5 กลุ่ม (list + wizard 4 ขั้น + view 5 แท็บ + 3 status-modal + bulk 3 ขั้น) · **states = 5 (≥ 4 → FULL)** · approval = NO (ถอดออก) · money rule = YES (pricing Confidential + cost gate)

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.x | (v3.5 pack) | BA | Base + DOA 3-tier + 4-Code — **superseded** |
| 2.0 | 2026-07-27 | BA | Reverse จาก HTML v6: +ENH-MINMAX · +state transitions ครบ · +bulk import 3 ขั้น · −ENH-4CODE · **−approval/DOA ทั้งชั้น** (คง placeholder fields) |

---

## §0.3 Scope

### In Scope
- ทะเบียนสินค้า 8 ประเภท (FG/RM/PM/CN/SV/TR/EX/NS) + behavior flags (stocked/sellable/purchasable) default จากประเภท ปรับมือได้
- รหัสสินค้า auto-generate `{TYPE}-{running}` (ฐาน 1001) — immutable หลังสร้าง (IR-01)
- Multi-UOM: หน่วยฐาน (เล็กสุด) + หน่วยแปลง factor ≥ 1, ห้ามข้ามหมวด (นับจำนวน/น้ำหนัก/ปริมาตร), flags ซื้อ/ขาย/เริ่มต้น/เก็บสต็อก — **lock ทั้งชุดเมื่อ `has_txn`** (IR-02)
- ราคา/ต้นทุน Confidential — role-gated (แสดง `•••` เมื่อไม่มีสิทธิ์)
- Posting Group (สินค้า + ภาษี) — resolve GL จริงที่ Finance Posting Setup
- Min/Max stock alert (ENH-MINMAX): VR-MM, contract `PRODUCT_STOCK_THRESHOLD v1` → Inventory Monitoring
- State machine 5 สถานะ **ไม่มีขั้นอนุมัติ**: draft → active (เปิดใช้งานตรง ผ่าน validateActivation) → obsolete → discontinued → archived + obsolete → active (reactivate)
- แก้ไข = amend ตรง (version+1 + audit) ทุกสถานะที่แก้ได้ (draft/active/obsolete)
- Soft delete เท่านั้น (archive) · versioning + audit timeline
- รูปภาพสินค้า (หลายรูป + ตั้งปก) + เอกสารแนบ
- Bulk import CSV 3 ขั้น: เลือกไฟล์ → preview + validate ต่อแถว → นำเข้าเฉพาะแถวผ่านเป็นร่าง + รายงาน IMPORT_ERROR รายแถว (ไม่ล้มทั้งไฟล์)
- List: ค้นหา (code/รหัสเก่า/ชื่อ/GTIN/คำอธิบาย/หมวด/กลุ่ม) + filter (ประเภท/หมวด/สถานะ) + sort + pagination windowing + empty state 2 เคส

### Out of Scope
- **ชั้นอนุมัติ / DOA ทั้งหมด** (pending status, approve/reject, tier, SoD, re-approval) — ถอดออกตามคำสั่ง 2026-07-27; field placeholder คงไว้ (ดู §0.8 OQ-01)
- **ENH-4CODE (Item/SKU composer)** — ตัดออกทั้งชุดตามคำสั่ง
- Lot/Serial/Expiry/FIFO tracking — field มีใน data model (legacy) แต่**ไม่มี UI** ใน v6 นี้ (ดู OQ-04)
- การนับสต็อกจริง / stock bucket per UOM — รอ Inventory 4.0 (`is_stock_uom` flag พร้อมแล้ว)
- Notification จริง — กระดิ่งเป็น placeholder ชี้ Notification Center (F-NT)
- ไฟล์อัปโหลดจริง (รูป/เอกสาร = mock placeholder — dev ต่อ multipart + object storage)

---

## §0.4 Roles & Responsibilities (COSO)

> ไม่มีชั้นอนุมัติใน scope นี้ — Maker เปิดใช้งานเองเมื่อข้อมูลครบ (validateActivation = system Checker)

| Role | Person/Team | Responsibilities |
|---|---|---|
| **Maker** | `master_data_clerk`, `product_manager` | สร้าง/แก้/เปิดใช้งาน/เปลี่ยนสถานะ/นำเข้า |
| **Checker (system)** | validateActivation + VR-MM + VR-03/04 | gate ก่อน active — NOT_READY block |
| **Approver** | — (N/A — DOA placeholder รอ Policy Center) | — |
| **Owner** | `product_manager` | ดูแล master + ตอบ OQ |

---

## §0.5 Dependencies

### Upstream
| Dependency | Type | Source |
|---|---|---|
| UOM Master (F-UOM-MASTER-001) | Data (FK `uom_code` + category) | API-06 GET /uoms?status=active |
| Category / Group master | Data (picker — soft reference LD-4C-02 legacy policy) | master data |
| Finance Posting Setup | Config (Posting Group → GL resolve) | Accounting module |

### Downstream
| Consumer | What it uses |
|---|---|
| Inventory Monitoring | contract `PRODUCT_STOCK_THRESHOLD v1` (ดู 02_API §2.X) — engine candidate `ENG-STOCK-ALERT` |
| BOM (F-BOM-001) | FK `product_code` + `standard_cost` + base uom + type + active gate |
| Inventory 4.0 | `is_stock_uom` per conversion (Multi-UOM stockkeeping) |
| Sales / Purchase docs | product picker (active only) + list_price / purchase_price |
| Policy Center (อนาคต) | DOA engine เสียบ `approver_role/approved_by/approved_at` (placeholder) |

### External — ไม่มี

---

## §0.6 Stack & Architecture

| Layer | Technology |
|---|---|
| Frontend | React + Vite (prototype = vanilla JS single-file SPA, hash routing) |
| API | Go backend |
| Database | PostgreSQL + RLS (multi-tenant) |
| Engine layer | CUBIC Registry (candidate: ENG-STOCK-ALERT — downstream owner) |
| Auth | JWT + role-based |

---

## §0.7 Multi-Tenant & Security Context

- [x] Multi-tenant feature: **YES** (RLS)
- [ ] PII data involved: **NO** (ไม่มี personal data — `created_by` = user id reference)
- [x] Financial data: **YES** (cost/price)
- [x] Audit log required: **YES** (ทุก mutation + version)

**Security Bible domains applied:** D2 (Auth), D5 (Financial), D9 (Audit), D15 (Admin actions/status transitions), D17 (Multi-tenant) — ดู 05_RULES §5.7 · D7 (PII) = not triggered

### §0.7.1 Data Classification Summary
- [x] **Has Confidential fields** — `standard_cost, avg_cost, last_cost, purchase_price, list_price` (role-gated `•••` บนจอจริง)
- [x] Internal (default) — ที่เหลือทั้งหมด
- [ ] Restricted — ไม่มี
- [ ] Public-facing — ไม่มี

**Linkage:** Confidential fields → Policy Center Data Classification (mask rule per role `canSeePricing`)

---

## §0.8 Open Questions

| ID | Question | Blocking? | Owner |
|---|---|---|---|
| OQ-01 | DOA/approval กลับเข้า UI phase ไหน — placeholder `approver_role/approved_by/approved_at` พร้อมเสียบ Policy Center engine | NO | Strike |
| OQ-02 | Bulk import: ไฟล์จริง + parser + ENG-COSTING default cost — spec คอลัมน์เต็ม (ตอนนี้ mock 10 คอลัมน์หลัก) | NO | พี่เบิร์ด |
| OQ-03 | `PRODUCT_STOCK_THRESHOLD v1` → register `ENG-STOCK-ALERT` ที่ CUBIC (owner = Inventory Monitoring) | NO | Architect |
| OQ-04 | Lot/Serial/Expiry/FIFO fields อยู่ใน data model แต่ไม่มี UI — เปิด UI phase ไหน หรือถอด field | NO | Strike |
| OQ-05 | `regulated` flag ค้างใน seed (เดิมใช้ DOA tier 3) — ถอดหรือเก็บรอ compliance phase | NO | Strike |
| OQ-06 | wizard 4 ขั้นไม่มีขั้น "ตรวจสอบและยืนยัน" (Rule #47 ระบุขั้นสุดท้าย = review) — จอจริงเป็น 4 ขั้นจบที่รูปภาพ & เอกสาร → คงตามจอ (R14) หรือเพิ่มขั้น 5 | NO | Chin |
| OQ-07 | `[AI-DEFAULT]` rules จาก Phase 2.5 (optimistic lock / idempotency / code-running race — ดู 05_RULES) รอ BA confirm | NO | BA/พี่เบิร์ด |

---

## §0.9 Glossary

| Term | Definition |
|---|---|
| TYPEMETA | ตารางประเภทสินค้า 8 ตัว + default behavior flags |
| has_txn | สินค้ามี transaction แล้ว → lock UOM/สูตรแปลง (IR-02) |
| amend | แก้ไข record ตรง ๆ → version+1 + audit (ไม่มี re-approval) |
| VR-MM | validation rule Min/Max stock (max ≥ min ≥ 0, stocked only) |
| Posting Group | กลุ่มบัญชี — ตัวกลาง resolve GL ที่ Finance Posting Setup |
| Soft reference | master picker ไม่มี FK enforcement — format soft + uniqueness blocking |

---

## §0.10 Pack Navigation

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW.md | All | Meta + scope |
| 01_UI.md | FE dev | Layout Decision Log + Pages + Journey |
| 02_API.md | BE dev (HTTP) | API contracts + Cross-Module Contract |
| 03_LOGIC.md | BE dev (logic) | Functions + Engines + Trace |
| 04_DB.md | DBA / BE | Tables + Classification |
| 05_RULES.md | BE + QA | Rules + State machine + Edge + Errors |
| 06_TESTS.md | QA | AC + DoD + Cross-module |
| 07_LOCKED_DECISIONS.md | All | Scope Lock N/A + LD + CD |
| INDEX.md | All | Quick nav + trace |

---

## §0.12 Coverage Manifest ⭐ (Reverse Mode — source = HTML observed requirement)

> ไม่มี BRD → คอลัมน์แรกอ้าง **หลักฐานบนจอจริง** (route/selector/ข้อความ) แทน §BRD

| Src | Requirement (ย่อ) | อยู่ที่ใน Pack |
|---|---|---|
| H-01 | List 8 คอลัมน์ + filter + sort + paginate + empty 2 เคส | 01_UI P-01 · 02_API-01 · 03 FN-01 · 06 AC-01/02 |
| H-02 | สร้างสินค้า wizard 4 ขั้น + gen code + draft | 01_UI P-02 · 02_API-03 · 03 FN-02/09/10 · 06 AC-03 |
| H-03 | บันทึกและเปิดใช้งาน (validateActivation → active) | 02_API-03/05 · 03 FN-04/06 · 05 BR-PDM-05 · 06 AC-04/05 |
| H-04 | แก้ไข = amend version+1 (draft/active/obsolete เท่านั้น) | 02_API-04 · 03 FN-03 · 05 BR-PDM-07 · 06 AC-06/07 |
| H-05 | Multi-UOM + VR-03/04 + IR-02 lock | 01_UI P-02 step2 · 03 FN-08 · 05 BR-PDM-03/04 · 06 AC-08/09 |
| H-06 | Min/Max VR-MM + view section + contract | 05 BR-PDM-06 · 02 §2.X · 06 AC-10 + XT-01 |
| H-07 | Pricing Confidential role-gate ••• | 04_DB §4.2/§4.6 · 05 §5.7 D-CLASS · 06 AC-11 |
| H-08 | State transitions: obsolete/discontinue/reactivate/archive + guards INVALID_STATE | 02_API-06 · 03 FN-05 · 05 §5.2 · 06 AC-12..15 |
| H-09 | Soft delete (archive) + has_txn warning | 02_API-06 · 05 BR-PDM-08 · 06 AC-15 |
| H-10 | Bulk import 3 ขั้น + per-row validate + partial import | 01_UI P-06 · 02_API-07 · 03 FN-11/12 · 05 EC-05 · 06 AC-16/17 |
| H-11 | Audit timeline + version | 04 T_product_audit · 06 AC-18 |
| H-12 | Routing hash + Esc chain + modal-over-view กลับ context คง tab | 01_UI §1.2/§1.6 · 06 AC-19 |
| H-13 | DOA placeholder fields (null) | 04 §4.2 · 07 LD-02 |
| H-14 | Empty/microcopy ตามจอ verbatim | 06 §6.10 |

**สรุป:** HTML observed 14/14 ✅ · ไม่มีที่ลง → ไม่มี (OQ track ส่วนอนาคตแล้ว)

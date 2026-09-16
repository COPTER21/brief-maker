# 00_OVERVIEW — F082 F-WH-STKADJ ใบปรับยอดสต๊อก (Stock Adjustment)

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Coverage Manifest + Open Questions

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-WH-STKADJ (fid **F082**) |
| **Feature Name** | ใบปรับยอดสต๊อก (Stock Adjustment) |
| **Module** | Warehouse · Wave W3Q · arch **Q-document** (Pattern Q + B2 v2) |
| **Variant** | **FULL** (9 files + INDEX) |
| **Status** | DRAFT (FRD) |
| **FRD Version** | 1.0 (2026-09-16) |
| **Generator** | frd-generator-v6 (HTML-first mode) |
| **Source BRD** | BRD-WH-082 v2.0 · **APPROVED** (2026-09-16, 28✅/0❌) |
| **Source HTML** | `outputs/F-WH-STKADJ/F-WH-STKADJ.html` (ผ่าน ux + coverage R1 gate · 55/55 FN) |
| **Source contracts** | PREBRIEF_F-WH-STKADJ v1 · FUNCTION_CHECKLIST (55 FN) · BASELINE · HANDOFF · 5_DECLARATIONS (DOA/NTF/CSQ/DOCCFG/print-spec) |
| **Author** | BA (WF-01 lane) |

**Variant decision (fallback from BRD):** pages=3 top-level (list/wizard/view) + 8 modals · **states = 6** (≥4) · **approval AND money** (DOA ตามมูลค่า) · engines ≥2 owned + external. → **FULL** (pack-variants.md Q2/Q3/Q4 = YES).

---

## §0.2 Revision History
| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-09-16 | BA | Initial FRD (HTML-first) — reflects BA re-gate FIX-02/03/04 · FN 55 · view 4 tabs · reversal via DOA · cancel ร่าง/รออนุมัติ only · count-doc trace |

---

## §0.3 Scope

### In Scope
- ออกใบปรับยอด (+/−) ราย (bin, สินค้า) · ผลต่าง + มูลค่า · เหตุผลบังคับทุกบรรทัด
- สายอนุมัติ DOA ตามมูลค่า (ค่าสัมบูรณ์) · slot picker คนจริง
- ผ่านรายการ (post) → movement append-only · กลับรายการ (reversal ผ่าน DOA)
- ยกเลิก (ร่าง/รออนุมัติ) · PDF A4 + ลายเซ็น · trace ใบนับต้นเรื่อง (display-only)
- location model จาก Putaway §3.0 (read-only) · soft-reference masters

### Out of Scope (ตัดออกชัดเจน — negative FN + backlog)
- **นับสต๊อก / cycle count / ใบนับ** — backlog owner Strike (FN-35 · BR-24)
- **เปลี่ยน/ย้าย location (bin↔bin, คลัง↔คลัง)** — = Stock Transfer F083 (FN-36 · BR-05)
- **เขียน in-transit** — จองให้ Stock Transfer (FN-32 · BR-13)
- **post JE จริง / valuation จริง (FIFO/MA)** — W5 (mock · BR-19 · gap G-01)
- **ตั้งค่าเลขรัน / threshold / สายอนุมัติในหน้านี้** — F-DOCCFG / NC rules / F-DLG-001 (FN-47/48)
- **คอลัมน์ VAT/ส่วนลด** (FN-49) · Lot/Serial · CSV import · revaluation

### Out of Scope (Phase 2.5 conservative defaults → OQ)
- Draft expiry policy (OQ-09) · idempotency/optimistic-lock/permission-recheck ค่า default (OQ-08)

---

## §0.4 Roles & Responsibilities (COSO)
| Role | Team | Responsibilities |
|---|---|---|
| **Maker** | เจ้าหน้าที่คลัง | สร้าง/แก้ร่าง · กรอกรายการ+เหตุผล · แนบหลักฐาน · ส่งอนุมัติ · ยกเลิกร่างตัวเอง |
| **Checker** | หัวหน้าคลัง | ทุกอย่างของ Maker + **ผ่านรายการ** + ริเริ่มกลับรายการ (อนุมัติชั้นแรกด้วย) |
| **Approver** | ตาม DOA slot (ผจก.คลัง / ผจก.บัญชี / ผอ.สายงาน) | อนุมัติ/ตีกลับ เฉพาะ slot ตัวเอง · **SoD: ไม่อนุมัติใบตัวเอง** |
| **Owner (RO)** | บัญชี · ผู้ตรวจสอบภายใน | อ่าน/พิมพ์ · audit · movement append-only |
> รายละเอียด workflow → 01_UI §1.3–1.4 · สิทธิ์จริง = Policy Center (ไม่ hardcode · Security Preset P2)

---

## §0.5 Dependencies

### Upstream (feature นี้พึ่ง)
| Dependency | Type | Source |
|---|---|---|
| Location model (warehouse/zone/bin + location_type) | Data (read-only soft-ref) | **F081 Putaway §3.0** (LOCK-07) |
| ยอดคงเหลือราย bin (Σ movement) | Data | Putaway §3.4 ledger (shared) |
| Item / UOM / Cost Center Master | Data (soft-ref) | Masters (LD-4C-02) |
| ใบนับ F084/F086 (ref_count_doc) | Data (display-only) | Count Doc features |
| สาย DOA + วงเงิน | Engine (resolve) | **F-DLG-001** (DOA-WH-ADJ-01) |
| เลขรัน + สำเนาเอกสาร | Engine | **F-DOCCFG** (ENG-DOC-NUM/STORE) |
| ต้นทุน/valuation | Data (mock) | **W5** (Inventory Valuation) |

### Downstream (พึ่ง feature นี้)
| Consumer | ใช้อะไร |
|---|---|
| F083 Stock Transfer | reuse F082-ENG-01/02 + movement schema + reversal pattern + DOA slot picker (OB-16) |
| GL/JE (W5) | มูลค่า movement + บัญชีปลายทาง (รอ post จริง) |
| ENG-NOTIFY / 7C CSQ | 6 NTF events / 5 CSQ events |
| รายงาน inventory accuracy | ความถี่/มูลค่าการปรับ (KPI §17.3) |

### External Engines (ประกาศ ไม่ implement)
F-DLG-001 (DOA) · F-DOCCFG · F-NOTIFY · F-CSQ-01 — ผ่าน declaration briefs (5_DECLARATIONS)

---

## §0.6 Stack & Architecture
| Layer | Tech |
|---|---|
| Frontend | React/Tailwind · hash routing (SPA) · Warm Light CI · Satoshi + Noto Sans Thai + Lucide |
| API | Node/Strapi · REST /api/v1 |
| DB | PostgreSQL (RLS multi-tenant) |
| Engine | CUBIC Registry (ENG-01/02 candidate) |
| Auth | JWT + role-based + SoD |

---

## §0.7 Multi-Tenant & Security Context
- [x] Multi-tenant: YES (RLS + row scope ตามคลัง)
- [x] PII: YES (ชื่อ/ตำแหน่งผู้ปฏิบัติงานใน audit/ลายเซ็น — PDPA scope · BRD §16.2)
- [x] Financial: YES (มูลค่าปรับ · JE mock)
- [x] Audit log required: YES (append-only · BR-25)

**Security Bible domains:** D2, D5, D7/PDPA, D9, D15, D17 — ดู 05_RULES §5.7 · **Security Preset = P2 (Approval/Workflow · 14 controls)**

### §0.7.1 Data Classification Summary
- [ ] Restricted fields: **ไม่มี** (ไม่มีเงินเดือน/ACL รายบุคคล)
- [x] Confidential: มูลค่า/ต้นทุน (financial) + ชื่อ/ตำแหน่งผู้อนุมัติ-ผู้จัดทำ (PII)
- [x] Internal (default): ทุก field อื่น
- **Highest level = Confidential** · Linkage: Policy Center → Data Classification + PDPA consent (ดู 04_DB §4.6)

---

## §0.8 Open Questions

| ID | Question | Blocking? | Owner |
|---|---|---|---|
| OQ-01 | จุดตัดวงเงิน DOA 20,000/200,000/1,000,000 + จำนวนชั้น (`[DEFAULT — รอยืนยัน]`) | NO (default ใช้ได้) | Strike + F-DLG-001 |
| OQ-02 | เกณฑ์ "มูลค่าสูง" (adj_high_value) + อายุใบค้าง — อยู่ NC rules ยังไม่เคาะเลข (R26) | NO | Strike + NC rules |
| OQ-03 | ต้นทุน/valuation จริง (FIFO/MA) — รอบนี้ mock Item Master (R27 · gap G-01) | NO | W5 + บัญชี |
| OQ-04 | no-gap เลขรัน = ✗ (`[DEFAULT]`) — ถ้าบัญชีต้อง no-gap ต้องเลื่อนออกเลขไปตอน post (OQ-ADJ-07) | NO | Strike + F-DOCCFG |
| OQ-05 | วันที่มีผลย้อนหลัง = งวดที่ยังเปิด (กติกางวดจริง = W5 · OQ-ADJ-05) | NO | Strike / W5 |
| OQ-06 | จำกัดสิทธิ์ใช้เหตุผลบางตัวตามตำแหน่ง — รอบนี้ไม่จำกัดใน UI → Security Preset (OQ-ADJ-06) | NO | Strike |
| OQ-07 | W5 เจ้าของท่อ AC กันนับซ้ำ — StockAdj ไม่ประกาศ AC (CSQ-Q2) | NO | F-CSQ-01 + GL |
| OQ-08 `[AI-DEFAULT]` | Phase 2.5 conservative defaults: optimistic lock (version) · idempotency key 24hr · re-check role at mutation — รอ BA ยืนยันค่า | NO | BA + BE |
| OQ-09 `[AI-DEFAULT]` | Draft expiry policy — รอบนี้ persist ไม่หมดอายุอัตโนมัติ (PR-6) | NO | BA |
| OQ-10 | Restricted Resources registry: ยืนยันว่า feature นี้ **ไม่มี** field ระดับ Restricted (มูลค่า=Confidential) — ไม่ต้อง wire | NO | Policy Center |

> ไม่มี OQ blocking. ทุก OQ มี interim answer + owner (BRD §15 Q1–Q15 · PREBRIEF §10). **ไม่พบ LOCK/HTML-vs-PREBRIEF conflict ที่ต้องเคาะ** — BRD สกัดจาก HTML เดียวกัน (drift = none).

---

## §0.9 Glossary
| Term | Meaning |
|---|---|
| ค่าสัมบูรณ์ (abs) | `Σ|มูลค่าต่อบรรทัด|` — **ฐาน DOA** (BR-09) ไม่ใช่ยอดสุทธิ |
| movement (append-only) | รายการเคลื่อนไหวสต๊อก · ห้ามลบ/แก้ · reversal = แถวใหม่ทิศตรงข้าม |
| กลับรายการ (reversal) | ใบใหม่แก้ใบที่ post แล้ว ผ่านสาย DOA (FIX-03) · ผูกคู่ 2 ทาง |
| soft-ref | picker ไม่ FK validate nullable + เก็บ snapshot ข้อความ (LD-4C-02) |
| location_type | staging/storage/quarantine/damage/in-transit (in-transit ห้ามแตะ) |
| ref_count_doc | ใบนับต้นเรื่อง F084/F086 · display-only (FIX-04) |

## §0.10 Pack Navigation
00 OVERVIEW · 01 UI · 02 API · 03 LOGIC · 04 DB · 05 RULES · 06 TESTS · 07 LOCKED_DECISIONS · INDEX

---

## §0.11 Scope Lock (imported จาก BRD §3.4)
> FULL variant → รายละเอียดเต็มที่ **07_LOCKED §7.0** (LOCK-01..LOCK-10, immutable). Scope Lock Ref: **N/A — standalone** (เข้า lane ผ่าน CUBE-LANE-W3-LITE ไม่ใช่ chain ใบเซ็น · drift = none).

---

## §0.12 Coverage Manifest ⭐ (กัน requirement หล่น)

### FN Ledger — ทุก 55 FN → ที่อยู่ใน pack

| FN | ย่อ | อยู่ที่ใน Pack |
|---|---|---|
| FN-01 | ปรับกักกัน → bin QA-* | 01 P-02 · 02 API-13 · 03 FN-05 · 05 BR-12 · 06 AC-21 |
| FN-02 | ตัดจำหน่าย → bin DM-* | 01 P-02 · 02 API-13 · 03 FN-05 · 05 BR-12 · 06 AC-21 |
| FN-03 | bin ล็อก/โซนปิด disabled | 02 API-13 · 03 FN-05 · 05 BR-14 · 06 AC-21 |
| FN-04 | เลือก bin+สินค้า ยอดระบบ+ผลต่าง+ | 01 P-02 s2 · 02 API-15 · 03 FN-04 · 06 AC-03 |
| FN-05 | ผลต่าง − ชิปแดง | 01 P-02 s2 · 03 FN-03/ENG-01 · 06 AC-03 |
| FN-06 | มูลค่า = ผลต่าง×ต้นทุน | 03 ENG-01 · 05 §5.4 · 06 AC-03 |
| FN-07 | สลับโหมดกรอก | 01 P-02 s2 · 03 FN-03 · 06 AC-04 |
| FN-08 | totals Σ abs vs สุทธิ | 01 P-02 s2 · 03 ENG-01 · 05 BR-09 · 06 AC-05 |
| FN-09 | เปลี่ยนคลัง → confirm ล้างบรรทัด | 01 P-02 s1 · 03 FN-03 · 05 BR-04 · 06 AC-25 |
| FN-10 | คู่ (bin,สินค้า) ซ้ำ | 03 FN-03/FN-06 · 04 UNIQUE · 05 BR-01 · 06 AC-08 |
| FN-11 | ผลต่าง=0 บล็อก | 03 FN-06 · 05 BR-02/VR-08 · 06 AC-06 |
| FN-12 | ปรับลดติดลบ บล็อก | 03 FN-06 · 05 BR-03/VR-09 · 06 AC-07 |
| FN-13 | ป้ายต้นทุน mock (FWD-WIRE) | 01 P-02 s2 · 03 FN-04 · 05 §5.9 · gap G-01 |
| FN-14 | ขั้นผู้อนุมัติ Σ abs + ชั้น | 01 P-02 s4 · 02 API-16 · 05 BR-09 · 06 AC-11 |
| FN-15 | มูลค่าต่ำ 1 ชั้น | 02 API-16 · 05 §5.9 · 06 AC-11 |
| FN-16 | มูลค่าสูง หลายชั้น | 02 API-16 · 06 AC-11 |
| FN-17 | ทุก slot คนจริง (บล็อกถ้าว่าง) | 01 P-02 s4/P-04 · 03 FN-06 · 05 BR-10/VR-12 · 06 AC-12 |
| FN-18 | บรรทัดไม่มีเหตุผล ส่งไม่ได้ | 01 P-02 s3 · 03 FN-06 · 05 BR-06 · 06 AC-09 |
| FN-19 | บันทึกร่าง ไม่มีเลขจริง | 01 P-02 s5 · 02 API-03 · 03 FN-02 · 05 BR-21 · 06 AC-02 |
| FN-20 | ส่งอนุมัติ → ออกเลข ADJ-YYYY-NNNN | 02 API-05 · 03 FN-08 · 05 BR-21 · 06 AC-13 |
| FN-21 | อนุมัติ → slot ถัดไป/ครบ | 02 API-06 · 03 FN-09 · 05 §5.2 · 06 AC-14 |
| FN-22 | ตีกลับ + เหตุผล → ร่าง | 02 API-07 · 03 FN-10 · 05 BR-11 · 06 AC-15 |
| FN-23 | ผ่านรายการเฉพาะ approved | 02 API-09 · 03 FN-13 · 05 BR-08/VR-13 · 06 AC-16 |
| FN-24 | ยกเลิกเฉพาะ ร่าง/รออนุมัติ ★ | 02 API-08 · 03 FN-11 · 05 BR-27/VR-16 · 06 AC-17 |
| FN-25 | post แล้วไม่มียกเลิก มีแต่กลับรายการ | 02 API-10 · 03 FN-14 · 05 BR-17 · 06 AC-18 |
| FN-26 | list กรองครบทุกสถานะ | 01 P-01 · 02 API-01 · 03 FN-01 · 06 AC-01 |
| FN-27 | ยอดเปลี่ยน → เตือน 2 ยอดก่อน post ★ | 01 P-06 · 03 FN-12 · 05 BR-15/EC-04 · 06 AC-19 |
| FN-28 | tab ลายเซ็นการ์ดผู้อนุมัติจริง | 01 P-03 · 03 FN-17 · 06 AC-14/22 |
| FN-29 | tab ประวัติ movement + คู่ reversal | 01 P-03 · 02 API-11 · 03 FN-16 · 05 BR-16/18 · 06 AC-20 |
| FN-30 | ป้ายรอลงบัญชี + JE marker (ไม่มีปุ่มจริง) | 01 P-03 · 03 FN-13 · 05 BR-19 · 06 AC-20 |
| FN-31 | สินค้า archive ยังแสดงข้อความเดิม | 04 snapshot cols · 05 BR-22/EC-07 · 06 AC-23 |
| FN-32 | in-transit ไม่เจอใน picker (neg) | 02 API-13 · 03 FN-05 · 05 BR-13 · 06 NEG-01 |
| FN-33 | แนบไฟล์ → เอกสารแนบ landing | 01 P-01/P-02 · 02 API-12/20 · 03 FN-15/18 · 06 AC-26 |
| FN-34 | tab PDF A4 ครบ + พิมพ์ | 01 P-03 · 02 API-19 · 03 FN-17 · 06 AC-22 |
| FN-35 | ไม่มีนับสต๊อก (neg) | 05 BR-24 · 06 NEG-02 · §0.3 out |
| FN-36 | ไม่มี bin ปลายทาง/ย้าย (neg) | 05 BR-05 · 06 NEG-03 · §0.3 out |
| FN-37 | dropdown เหตุผลกรองตามทิศ | 01 P-02 s3 · 03 FN-03 · 05 BR-07 · 06 AC-09 |
| FN-38 | ปี ค.ศ. ทุกจุด | 01 §1.7 · 03 FN-17 · 05 §5.8 · 06 AC-22 |
| FN-39 | audit append-only ทุก event | 04 T_audit_log · 05 BR-25 · 06 AC-20 |
| FN-40 | เหตุผล "อื่น ๆ" บังคับคำอธิบาย | 03 FN-06 · 05 BR-06/VR-11 · 06 AC-09 |
| FN-41 | เหตุผลรวมของใบ เติมบรรทัดว่าง | 01 P-02 s1 · 03 FN-07 · 06 AC-10 |
| FN-42 | ไม่ใช้ role ID แทนคน (neg-ish) | 01 P-04 · 03 FN-06 · 05 BR-10 · 06 AC-12 |
| FN-43 | ใบผสมสุทธิ≈0 ยังต้องอนุมัติตาม abs | 03 ENG-01 · 05 BR-09 · 06 AC-05 |
| FN-44 | กลับรายการซ้ำไม่ได้ | 02 API-10 · 03 FN-14 · 05 BR-18 · 06 AC-18 |
| FN-45 | ไม่มีปุ่มลบ/แก้ movement (neg) | 02 (no endpoint) · 04 append-only grant · 05 BR-16 · 06 NEG-08 |
| FN-46 | quarantine ปรับได้ ย้ายออกไม่ได้ | 02 API-13 · 03 FN-05 · 05 BR-12 · 06 NEG-04 |
| FN-47 | ไม่มีช่องเลขเอง/ตั้งเลขรัน (neg) | 05 BR-20 · 06 NEG-05 · §0.3 out |
| FN-48 | ไม่มีช่อง threshold/% (neg) | 05 BR-20/§5.9 · 06 NEG-06 · §0.3 out |
| FN-49 | ไม่มีคอลัมน์ VAT (neg) | 01 §1.0 · 06 NEG-07 · §0.3 out |
| FN-50 | sidebar module map | 01 §1.2 · 06 NEG-09 |
| FN-51 | damage บังคับแนบหลักฐาน | 02 API-05 · 03 FN-06 · 05 BR-23/VR-13 · 06 AC-26 |
| FN-52 | count-doc trace ★ | 01 P-02 s1/P-03 · 02 API-18 · 03 FN-06 · 05 BR-26/VR-05 · 06 AC-24 |
| FN-90 | ค้นหา/filter + empty state | 01 P-01 · 02 API-01 · 03 FN-01 · 06 AC-01 |
| FN-91 | ยกเลิก/กลับรายการผ่าน confirm · ไม่มี hard delete | 01 P-07 · 02 §2.3 · 05 BR-16/17 |
| FN-92 | field validate + กัน double-submit | 02 §2.3 idempotency · 03 FN-06 · 05 EC-02 |

**FN สรุป: 55/55 ✅ ทุก FN มีที่ลง** (หมวด7 negative FN-32/35/36/45/46/47/48/49 = พิสูจน์ "ไม่มี" ที่ 06 §6.7)

### Story / Scenario (PREBRIEF §2 S-01..S-26)
S-01..S-26 ทุก scenario → mapped ผ่าน AC/TC/NEG ใน 06_TESTS (S-07 happy AC-13/14/16 · S-10 reversal AC-18 · S-15 drift AC-19 · S-20 NEG-01 · S-24 NEG-02 · S-25 NEG-03 · S-26 AC-24). **26/26 ✅**

### Business Rules (BRD §9 R01–R28 / PREBRIEF BR-01..BR-27)
ทุก R/BR → 05_RULES §5.1 (BR-01..BR-27 ยึด PREBRIEF ids; map R01–R28 ใน §5.1 header) + test. **27/27 ✅** · VR01–VR17 → 05_RULES §5.4. **17/17 ✅**

### Edge (PREBRIEF §10 OQ / Phase 2.5)
EC-01..EC-07 → 05_RULES §5.5 + 06 TC. **7/7 ✅**

### Downstream / Value Stream (BRD §12.1)
8 downstream → 02_API §2.X + 06_TESTS §6.9 (XT-01..XT-11). **ครบ ✅**

**สรุป Coverage:** Stories 26/26 ✅ · FN 55/55 ✅ · Rules 27/27 + VR 17/17 ✅ · Edges 7/7 ✅ · Downstream 8/8 ✅ · **ไม่มีแถวที่ "อยู่ที่" ว่าง** — OQ ทั้งหมดมี owner (non-blocking).

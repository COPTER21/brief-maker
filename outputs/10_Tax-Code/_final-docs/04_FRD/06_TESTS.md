# 06_TESTS — F-TAX Tax Code (รหัสภาษี)

> **Audience:** QA engineer
> **Purpose:** Acceptance Criteria + DoD + Cross-Module cases
> **Coverage source:** 02_API + 03_LOGIC + 05_RULES + BRD §7 stories
> **Expected text:** ยึด**ข้อความจริงบนจอ (verbatim)** จาก TaxCode.html ก่อน แล้ว fallback microcopy กลาง v7 (ดู §6.10) — ห้ามแต่งคำเอง.

---

## §6.1 Acceptance Criteria (AC) — map ต่อ BRD §7 stories

### AC-01: List แยก VAT/WHT + KPI (S-01)
**Given** login มี `tax_code.view`, current company set
**When** เปิด `#/accounting/setup/tax-codes`
**Then** เห็นตาราง 8 คอลัมน์ + KPI stats (`รหัสทั้งหมด`, `ใช้งาน`, `ร่าง / ปิดใช้งาน`) + tabs `ภาษีมูลค่าเพิ่ม (VAT)` / `ภาษีหัก ณ ที่จ่าย (WHT)`
**And** กด tab WHT → แสดงเฉพาะ family=WHT ของบริษัทปัจจุบัน

### AC-02: Create + activate — happy (S-02)
**Given** กด `สร้างรหัสภาษี`, กรอกครบ + GL role ถูก, Approver
**When** กด `ยืนยันสร้าง` (mode=activate)
**Then** status=active + toast `สร้างรหัสภาษีสำเร็จ` + audit `สร้างและเปิดใช้งานรหัสภาษี`

### AC-02b: Duplicate code (S-02 AC2 / E06)
**Given** code ซ้ำใน company (case-insensitive)
**When** submit
**Then** block inline `รหัสนี้มีอยู่แล้วในบริษัทปัจจุบัน` (VR02) + 422 BR_TAX_CODE_DUPLICATE

### AC-03: Create + activate — SoD block (S-02 / E16)
**Given** user เป็น Maker (ไม่มี `tax_code.activate`)
**When** พยายาม activate (submitForm)
**Then** toast `คุณไม่มีสิทธิ์สร้างหรือเปิดใช้รหัสภาษี` (VR12) + server 403; อนุญาตเฉพาะ saveDraft

### AC-04: Save draft ไม่ผูก GL (S-03)
**Given** กรอก code+ชื่อ ยังไม่เลือก GL
**When** กด `บันทึกร่าง`
**Then** status=draft สำเร็จ + toast `บันทึกร่างแล้ว`
**And** พยายาม activate โดยยังไม่มี GL → block `ต้องเลือกบัญชี GL กลุ่ม...ก่อนเปิดใช้งาน` (VR07-09)

### AC-05: GL role filter (S-04)
**Given** VAT direction=sale
**When** เปิด combobox GL ภาษีขาย (F-TAX-API-11 tax_role=VAT_SALE)
**Then** เห็นเฉพาะ GL role=VAT_SALE ของ company ปัจจุบันที่ active+posting
### AC-05b: WHT GL = WHT_PAYABLE เท่านั้น (S-04 AC2 / LOCK-12 / FLAG-1)
**Given** family=WHT
**When** เปิด combobox GL
**Then** เห็นเฉพาะ GL role=WHT_PAYABLE (ไม่ใช่ทุก GL) — ยืนยัน FLAG-1 RESOLVED (ENG-03/VR09)

### AC-06: WHT income required (S-05)
**Given** family=WHT ไม่เลือกประเภทเงินได้
**When** activate
**Then** block `WHT ต้องระบุประเภทเงินได้` (VR06)
**And** เลือกประเภทเงินได้ + บันทึก → `income_category_code` set อัตโนมัติ (FN-12)

### AC-07: Rate lock used>0 (S-06 / E02)
**Given** รหัส used>0
**When** เปิดแก้ไข
**Then** ช่องอัตรา/ตระกูล/ทิศทาง/รหัส อ่านอย่างเดียว + ป้าย "อ่านอย่างเดียว" + ปุ่ม `สร้างรหัสแทน`
**And** พยายาม PUT แก้ rate → 422 BR_TAX_RATE_LOCKED

### AC-08: Replacement + lineage (S-07)
**Given** สร้างรหัสแทนจากรหัสเดิม (code+"-N", อัตรา+วันมีผลใหม่)
**When** ยืนยัน (F-TAX-API-08)
**Then** ใหม่ตั้ง `replaces_tax_code_id`, เดิมตั้ง `replaced_by_tax_code_id` + เดิม eff_end = วันก่อน eff_start ใหม่
**And** view drawer แสดง `ใช้แทนรหัส` / `ถูกแทนด้วย`

### AC-09: Deactivate (S-08 AC1)
**Given** รหัส active
**When** ยืนยันปิดใช้งาน (modal `ปิดใช้งานรหัสภาษี?`)
**Then** status=inactive + eff_end=today + audit + toast `ปิดใช้งานรหัสภาษีแล้ว`; เอกสารเดิมยังอ้างอิงได้

### AC-10: Archive draft — no hard delete (S-08 AC2 / R05)
**Given** รหัส draft
**When** เก็บร่างถาวร
**Then** status=archived + modal alert `ระบบไม่มีการลบถาวรสำหรับรหัสภาษี` + toast `เก็บร่างถาวรแล้ว`

### AC-11: Picker ตามวันที่เอกสาร + snapshot (S-09)
**Given** เลือก context + วันที่เอกสาร ใน picker (F-TAX-API-09)
**When** ระบบกรอง (ENG-02)
**Then** แสดงเฉพาะ active ที่ eff_start ≤ docDate ≤ eff_end + ทิศทางตรง context
**And** เลือก+capture → immutable snapshot (ENG-01); WHT ในซื้อ → `WHT ในเอกสารซื้อเป็นเพียงคำแนะนำ โปรดยืนยันตอนจ่าย` (block final)

### AC-12: Audit gated view_audit (S-10)
**Given** มี `tax_code.view_audit`, เปิด view drawer
**Then** เห็น section `ประวัติการเปลี่ยนแปลง (Audit)` เรียงล่าสุดก่อน
**And** ไม่มี view_audit → ไม่แสดง section (UI) + API-10 direct → 403 (E17)

---

## §6.2 Test Case Inventory

| TC ID | Name | Type | Maps to | Priority |
|---|---|---|---|---|
| TC-01 | List + tabs + KPI | UI/API | AC-01 | P0 |
| TC-02 | Create+activate happy | API | AC-02 | P0 |
| TC-02b | Duplicate code | API neg | AC-02b/EC-06 | P1 |
| TC-03 | SoD activate block | API neg | AC-03/EC-16 | P0 |
| TC-04 | Save draft no GL | API | AC-04/EC-04 | P0 |
| TC-05 | GL VAT_SALE filter | API | AC-05 | P1 |
| TC-05b | GL WHT_PAYABLE only | API | AC-05b/LOCK-12 | P0 |
| TC-06 | WHT income required | API neg | AC-06 | P1 |
| TC-07 | Rate lock used>0 | API neg | AC-07/EC-02 | P0 |
| TC-08 | Replacement lineage | API | AC-08/EC-12 | P0 |
| TC-09 | Deactivate | API | AC-09/EC-01 | P1 |
| TC-10 | Archive draft (no delete) | API | AC-10/EC-03 | P1 |
| TC-11 | Picker + snapshot | API | AC-11 | P0 |
| TC-12 | Audit gate | API | AC-12/EC-17 | P1 |
| TC-CC-01 | Concurrent create (uniq DB) | API stress | EC-14 | P1 |
| TC-CC-02 | Concurrent edit/deactivate (409) | API stress | EC-15/OQ-9 | P2 |
| TC-ID-01 | Idempotency-Key dup | API | OQ-8 | P1 |
| TC-XC-01 | Cross-company block | API sec | EC-18 | P0 |

---

## §6.3 Test Data Setup

- 2 companies (COMP-001 current, COMP-002 other — cross-company test E18)
- GL accounts (จาก HTML L2091-2100): VAT_SALE ×3, VAT_PURCHASE ×2, WHT_PAYABLE ×3, OTHER/inactive ×1, other-company ×1
- Income_Type 8 rows (L2108-2115)
- Preset ไทย 7 รหัส + demo: VAT10-OLD (inactive, used>0), draft (WHT รอผูก GL)
- Roles: `qa_accountant` (Maker), `qa_manager` (Approver), `qa_viewer` (view only, no view_audit)

---

## §6.4 Definition of Done (DoD)

### Code
- [ ] ทุก AC implemented + unit tests
- [ ] Integration (API+DB+Engine ENG-01/02/03)
- [ ] **Server-side enforcement** (BRD §14.3): uniqueness DB index, GL role+company filter, immutable used-rate, effective overlap, snapshot immutability, append-only audit, company scope, activate=Approver
- [ ] Code review + no critical security findings

### Documentation
- [ ] API docs (auto จาก 02_API)
- [ ] CUBIC Registry: ENG-01/02/03 registered
- [ ] 07_LOCKED reflects final (OQ-8/9/10 resolved หรือ carried)

### QA
- [ ] P0 + P1 pass; no P0/P1 bug open
- [ ] Security checklist (D2/D5/D9/D15/D17) verified
- [ ] Consumer picker query < 1s (BRD §17.1)

---

## §6.5 WebSocket Events
> **ไม่มี** — feature เป็น admin/config surface, ไม่มี realtime push (ตรง 01_UI §1.5).

---

## §6.6 Performance Benchmarks

| Endpoint | P95 latency | Note |
|---|---|---|
| GET /tax-codes (list) | < 500ms | master ขนาดเล็ก (~9-1000 รหัส/company) |
| GET /tax-codes/pickable | < 1000ms | stress point (BRD §17.1/§17.5) — index pickable |
| POST /tax-codes (create+activate) | < 1000ms | + validate + audit |

---

## §6.7 Test Environment Notes
- Staging company `COMP-001`; cross-company `COMP-002`
- ENG-01/02/03 deterministic (pure) — golden test vectors
- Seed script: preset 7 รหัส + income types + GL (04_DB §4.4)

---

## §6.8 Trace: AC → Logic Coverage

| AC | API | Functions | Engines |
|---|---|---|---|
| AC-01 | API-01 | FN-01 | — |
| AC-02 | API-03/05 | FN-02, FN-04, FN-05, FN-14, FN-12, FN-13 | ENG-03 |
| AC-04 | API-03 | FN-02, FN-04 | — |
| AC-05/05b | API-11 | FN-11 | ENG-03 |
| AC-06 | API-05 | FN-04, FN-12 | — |
| AC-07 | API-04 | FN-03 | — |
| AC-08 | API-08 | FN-08, FN-04, FN-05 | — |
| AC-09 | API-06 | FN-06, FN-13 | — |
| AC-10 | API-07 | FN-07, FN-13 | — |
| AC-11 | API-09 | FN-09 | ENG-02, ENG-01 |
| AC-12 | API-10 | FN-13 | — |

> **Coverage check:** ทุก Function (FN-01..15) + Engine (ENG-01/02/03) ถูก trace ≥1 AC/XT. FN-15 (seed) → verified by seed/migration test (§6.4 DoD).

---

## §6.9 Cross-Module Test Cases ⭐ (จาก BRD §12.1 — External Contract, 5 downstream)

| ID | Scenario | Downstream | Expected |
|---|---|---|---|
| **XT-01** | ปิดใช้งานรหัส VAT ขายที่ active แล้ว | SO/AR Invoice | เอกสารเดิมใช้ snapshot ต่อได้; เอกสารใหม่ (docDate หลัง eff_end) เลือกไม่ได้ (ENG-02/E01) |
| **XT-02** | pick VAT ซื้อ + WHT ใน PO/AP | PO/AP Invoice | VAT ซื้อ pickable; WHT return `advisory=true` (ยังไม่ final) |
| **XT-03** | ยืนยัน WHT ตอนจ่าย | Payment Voucher | WHT final ที่ payment context (LOCK-06); report อ่านจาก payment result ไม่ใช่ AP suggestion |
| **XT-04** | snapshot immutable หลัง master เปลี่ยน | VAT Return (ภ.พ.30) | `vat_report_category` จาก snapshot คงที่แม้ master เปลี่ยน (R08); multi-rate per line รองรับ (E19) |
| **XT-05** | WHT report resolve income category | ภ.ง.ด.3/53 | อ่าน income_category + WHT final จาก payment result (LOCK-05/06) |

> ทุก downstream = External Contract / ยังไม่ implement → test เป็น **contract test** (mock consumer) ต่อ F-TAX-API-09 + snapshot payload (ENG-01).

---

## §6.10 Microcopy-Aware Expected Text (verbatim จาก HTML)

| บริบท | Expected text (verbatim) | HTML |
|---|---|---|
| ปุ่มสร้าง | `สร้างรหัสภาษี` | L2321 |
| ปุ่ม create submit | `ยืนยันสร้าง` | L2504 |
| ปุ่ม edit submit | `บันทึกการแก้ไข` | L2504 |
| ปุ่ม draft | `บันทึกร่าง` | L2540 |
| toast create | `สร้างรหัสภาษีสำเร็จ` | L2680 |
| toast draft | `บันทึกร่างแล้ว` | L2669 |
| toast edit | `บันทึกการแก้ไขแล้ว` | L2680 |
| toast deactivate | `ปิดใช้งานรหัสภาษีแล้ว` | L2765 |
| toast archive | `เก็บร่างถาวรแล้ว` | L2765 |
| validate dup | `รหัสนี้มีอยู่แล้วในบริษัทปัจจุบัน` | L2597 |
| validate GL WHT | `ต้องเลือกบัญชี GL กลุ่มภาษีหัก ณ ที่จ่ายค้างจ่ายก่อนเปิดใช้งาน` | L2609 |
| validate WHT income | `WHT ต้องระบุประเภทเงินได้` | L2604 |
| validate eff | `วันสิ้นสุดต้องไม่ก่อนวันเริ่ม` | L2613 |
| no-perm toast | `คุณไม่มีสิทธิ์สร้างหรือเปิดใช้รหัสภาษี` | L2673 |
| confirm deactivate | `ปิดใช้งานรหัสภาษี?` | L2783 |
| no hard delete alert | `ระบบไม่มีการลบถาวรสำหรับรหัสภาษี` | L2776 |
| audit section | `ประวัติการเปลี่ยนแปลง (Audit)` | L2742 |
| WHT advisory | `WHT ในเอกสารซื้อเป็นเพียงคำแนะนำ โปรดยืนยันตอนจ่าย` | L2822 |
| tabs | `ภาษีมูลค่าเพิ่ม (VAT)` / `ภาษีหัก ณ ที่จ่าย (WHT)` | L2333 |

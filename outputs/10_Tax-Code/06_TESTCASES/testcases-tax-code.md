# AI Test Cases — F-TAX Tax Code (รหัสภาษี)

เอกสารนี้เขียนให้ **AI agent (browser-use / vision)** อ่านแล้วลงมือทดสอบบนหน้าจอจริงของ prototype `TaxCode.html` แล้วรายงานผลกลับ. ทุก action ผูกกับ **ข้อความ/ป้ายที่เห็นบนจอ** (verbatim จาก HTML) + route จริง; ทุก Expected ตรวจได้ด้วยตา. Anchor priority: **HTML ต้นทาง (verbatim) > 01_UI > microcopy กลาง v7**.

> **Microcopy source log:** `html-generator-v6` ไม่ได้ติดตั้ง → ใช้เวอร์ชันสูงสุด = **html-generator-v7** (`WF-01_Pipeline_SkillSet/WF_Pipeline_SkillSet/html-generator-v7/knowledge/microcopy.md` v3.13). ข้อความมาตรฐาน (toast/empty/pill/submitting) ไม่ติดธง ⚠.
>
> **Drift log (HTML ชนะ + note):**
> - **KPI stat กลาง:** 01_UI/06 §AC-01 เขียนการ์ด KPI = `ใช้งาน` แต่ **HTML L2327 = `พร้อมใช้วันนี้`** (pickable). → ยึด HTML. เคสใช้ `พร้อมใช้วันนี้`.
> - **archiveDraft modal title:** 06_TESTS §6.10 อ้าง `ระบบไม่มีการลบถาวรสำหรับรหัสภาษี` เป็น title; **HTML L2775 title = `เก็บร่างถาวร?`** และข้อความ no-hard-delete = **alert ใน modal-body L2776**. → ยึด HTML.
> - **Picker WHT-in-purchase:** HTML แสดงเป็น **pill `แนะนำ · ยืนยันตอนจ่าย` (L2800)** ไม่มีปุ่มเลือก (ไม่ใช่ toast). toast VR13 (L2822) เป็น defensive path.
>
> **หมายเหตุ single-user sandbox:** prototype demo user ถือครบ **6 สิทธิ์** (`CURRENT_PERMISSIONS` HTML L2067-2070) และอยู่ใน `COMP-001` (L2066) เท่านั้น. เคส permission-deny / SoD / cross-company / concurrency / idempotency **กดมือไม่ได้บน prototype** → tag `(ต้อง simulate)` + Setup ระบุวิธี inject (แก้ Set / seed / mock consumer).

---

## Meta

| Field | Value |
|---|---|
| Feature ID | F-TAX |
| Feature Name | Tax Code — รหัสภาษี (VAT ขาย/ซื้อ + Withholding Tax Master Data) |
| Variant / FRD Version | FULL · FRD 1.0 (2026-08-05) |
| App entry (prototype) | เปิดไฟล์ `outputs/10_Tax-Code/01_HTML/TaxCode.html` ใน browser |
| Route (จริง, refresh-safe) | `#/accounting/setup/tax-codes` (HTML L2086; prod `/accounting/setup/tax-codes` — LOCK-11) |
| Surfaces | P-01 list · P-02 form drawer (680px) · P-03 view drawer · P-04 picker modal (440px) · P-05 confirm modal |
| ที่มา | FRD Pack `04_FRD/FRD_F-TAX_Pack/` (00/01/05/06/07) · BRD `03_BRD/BRD_F-TAX_TaxCode.md` · HTML `01_HTML/TaxCode.html` (source of truth) · Context `00_CONTEXT/AI_DEFAULTS.md`+`DECISION_LOG.md` |
| จำนวนเคส | **76 เคส** ใน 10 groups |
| หมวด (คร่าว) | happy 21 · negative 18 · edge/boundary 10 · error 8 · permission 5 · XT (cross-module) 5 · LOCK verify 12 (บางส่วน reuse เคส) · concurrency/idempotency 3 |

---

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| A — List / KPI / tabs / filter / sort / states (P-01) | TC-L01..L17 (17) | สูง |
| B — Create + activate + field validation (P-02) | TC-C01..C18 (18) | สูง |
| C — Save draft (P-02) | TC-D01..D04 (4) | สูง |
| D — GL master combobox filter (Rule #94 / FLAG-1) | TC-G01..G04 (4) | สูง |
| E — Rate lock used>0 + Replacement lineage (P-02) | TC-R01..R04 (4) | สูง |
| F — Deactivate / Archive (P-05) | TC-DE01..DE04 (4) | กลาง |
| G — View drawer + Audit gate (P-03) | TC-V01..V03 (3) | กลาง |
| H — Picker + snapshot (P-04) | TC-PK01..PK06 (6) | สูง |
| I — Permissions / SoD | TC-P01..P05 (5) | สูง |
| J — XT cross-module / LOCK / concurrency / idempotency | TC-X01/X03/X05, TC-XC01, TC-CC01, TC-CC02, TC-ID01, TC-EC08, TC-EC13, TC-LK02, TC-LK11 (11) | สูง |

---

## Coverage Ledger

### FR / Acceptance (06_TESTS §6.1)
| item | cases |
|---|---|
| AC-01 List + tabs + KPI | TC-L01, TC-L02, TC-L03, TC-L04, TC-L05, TC-L16 |
| AC-02 Create + activate happy | TC-C01, TC-C02 |
| AC-02b Duplicate code | TC-C03 |
| AC-03 SoD activate block | TC-P01 |
| AC-04 Save draft ไม่ผูก GL | TC-D01, TC-D03 |
| AC-05 GL role VAT_SALE filter | TC-G01, TC-G02 |
| AC-05b GL WHT_PAYABLE เท่านั้น (FLAG-1/LOCK-12) | TC-G03 |
| AC-06 WHT income required | TC-C15 |
| AC-07 Rate lock used>0 | TC-R01 |
| AC-08 Replacement + lineage | TC-R02, TC-R03 |
| AC-09 Deactivate | TC-DE01 |
| AC-10 Archive draft (no hard delete) | TC-DE02, TC-DE04 |
| AC-11 Picker ตามวันที่ + snapshot | TC-PK01, TC-PK02, TC-PK03 |
| AC-12 Audit gated view_audit | TC-V02, TC-V03 |

### Business Rules (05_RULES §5.1)
| rule | cases |
|---|---|
| BR-TAX-01 uniqueness case-insensitive (R01/LOCK-01) | TC-C03, TC-CC01 |
| BR-TAX-02 immutable used-rate → replacement (R02/LOCK-09) | TC-R01, TC-R02 |
| BR-TAX-03 WHT income required (R03) | TC-C15 |
| BR-TAX-04 GL required before active (R04) | TC-C11, TC-C12, TC-C14, TC-D03 |
| BR-TAX-05 no hard delete (R05/LOCK-08) | TC-DE01, TC-DE02, TC-DE04 |
| BR-TAX-06 GL = company/active/posting only (R06/LOCK-03) | TC-G04, TC-EC08 |
| BR-TAX-07 GL role WHT=WHT_PAYABLE (R07/LOCK-12) | TC-G03 |
| BR-TAX-08 picker docDate + immutable snapshot (R08/LOCK-07) | TC-PK03, TC-PK06 |
| BR-TAX-09 pickable window (R09) | TC-PK01, TC-PK02 |
| BR-TAX-10 VAT enum + zero/exempt rate=0 + vat_report_category (R10/LOCK-04) | TC-C16, TC-C17 |
| BR-TAX-11 WHT report resolve at payment (R11/LOCK-05) | TC-V01, TC-X05 |
| BR-TAX-12 AP advisory / Payment final (R12/LOCK-06) | TC-PK04, TC-PK05, TC-X03 |
| BR-TAX-15 current-company context (R15/LOCK-02) | TC-LK02, TC-XC01 |
| BR-TAX-16 preset seed 7 (R16) | TC-L01 (VAT presets), TC-L02 (WHT presets) |
| BR-TAX-17 WHT recommended rate = hint (R17) | TC-C02 (OQ-7 note) |
| VR05 rate 0–100 (R13) | TC-C07, TC-C08 |
| VR11 effEnd ≥ effStart (R14) | TC-C10 |

### Field Validation (05_RULES §5.4)
| VR | cases |
|---|---|
| VR01 code required | TC-C04 |
| VR02 code duplicate | TC-C03 |
| VR03 name required | TC-C05 |
| VR04 rate required (activate) | TC-C06 |
| VR05 rate 0–100 | TC-C07, TC-C08 |
| VR06 WHT income required | TC-C15 |
| VR07 gl_sale role VAT_SALE | TC-C11, TC-C13 |
| VR08 gl_purchase role VAT_PURCHASE | TC-C12, TC-C13 |
| VR09 gl_wht role WHT_PAYABLE | TC-C14, TC-G03 |
| VR10 eff_start required | TC-C09 |
| VR11 eff_end ≥ eff_start | TC-C10 |
| VR12 permission (toast) | TC-P01, TC-D02 |
| VR13 WHT purchase advisory block final | TC-PK04 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 deactivate→picker/snapshot | TC-X01, TC-DE01 |
| EC-02 edit rate used>0 | TC-R01 |
| EC-03 delete used → block soft-archive only | TC-DE04 |
| EC-04 draft no GL | TC-D01, TC-D03 |
| EC-05 WHT-in-purchase advisory | TC-PK04, TC-X03 |
| EC-06 duplicate code | TC-C03 |
| EC-07 foreign tax → ไม่รองรับ | — ข้าม (out of scope; ไม่มี selector บนจอ — verify โดยไม่มีช่องประเทศ/สกุลเงินให้เลือกในฟอร์ม) → TC-C01 step VERIFY |
| EC-08 GL deactivated in CoA later → OQ-6 | TC-EC08 (ต้อง simulate; behavior undecided) |
| EC-09 GL taxRole moved | — ข้าม (verify ที่ next activate = OQ-6 scope; หลังบ้าน ไม่มีผลบนจอ prototype) |
| EC-10 income type removed → snapshot code | — ข้าม (historical/หลังบ้าน; snapshot code ไม่มีหน้าจอ prototype) |
| EC-11 future effStart → active แต่ยัง pickable ไม่ได้ | TC-PK02 |
| EC-12 replacement overlap effEnd | TC-R02 |
| EC-13 reactivate inactive set effEnd `[AI-DEFAULT]` | TC-EC13 |
| EC-14 concurrent create (uniq DB) | TC-CC01 (ต้อง simulate) |
| EC-15 concurrent edit/deactivate 409 `[AI-DEFAULT]` | TC-CC02 (ต้อง simulate) |
| EC-16 Maker submit guard | TC-P01 |
| EC-17 view_audit direct 403 | TC-V03 |
| EC-18 cross-company access | TC-XC01 (ต้อง simulate) |
| EC-19 multi-rate per doc | TC-X04→ merged in TC-PK06 / XT-04 contract |

### Error Catalog (05_RULES §5.6)
| error | cases |
|---|---|
| ERR_VALIDATION_FAILED | TC-C04, TC-C05, TC-C06, TC-C07, TC-C09, TC-C10 |
| ERR_INSUFFICIENT_ROLE (403) | TC-P01, TC-V03, TC-XC01 |
| ERR_NOT_FOUND (404 cross-company) | TC-XC01 |
| ERR_DUPLICATE_IDEMPOTENCY_KEY (409) `[AI-DEFAULT]` | TC-ID01 |
| ERR_STALE_DATA (409) `[AI-DEFAULT]` | TC-CC02 |
| BR_TAX_CODE_DUPLICATE (422) | TC-C03, TC-CC01 |
| BR_TAX_RATE_LOCKED (422) | TC-R01 |
| BR_TAX_GL_REQUIRED (422) | TC-C11, TC-C12, TC-C14, TC-G03 |
| BR_TAX_WHT_INCOME_REQUIRED (422) | TC-C15 |
| BR_TAX_EFF_START_REQUIRED (422) | TC-C09 |
| BR_TAX_EFF_RANGE (422) | TC-C10 |
| ENG_ERR_INVALID_INPUT (500) | — ข้าม (engine schema mismatch = internal; ไม่มี trigger บน UI) |

### Permission Matrix (05_RULES §5.3 — role × action)
| cell | cases |
|---|---|
| Maker create = allow | TC-C01, TC-D01 |
| Maker update = allow | TC-R04 |
| Maker activate = **deny** (SoD) | TC-P01 |
| Maker deactivate = **deny** | TC-P03 |
| Approver activate = allow | TC-P04, TC-C01 |
| Approver deactivate = allow | TC-DE01 |
| Viewer (no create) → ปุ่มสร้างหาย | TC-P02 |
| view_audit = allow → เห็น section | TC-V02 |
| view_audit = deny → section หาย + API 403 | TC-V03 |
| saveDraft allowed for Maker | TC-P05 |

### Cross-Module (XT — 06_TESTS §6.9)
| XT | Downstream | Case |
|---|---|---|
| XT-01 deactivate VAT ขาย → เอกสารเดิม snapshot ต่อ / ใหม่เลือกไม่ได้ | SO/AR Invoice | TC-X01 (contract/simulate) |
| XT-02 pick VAT ซื้อ + WHT ใน PO/AP (advisory) | PO/AP Invoice | TC-PK04 |
| XT-03 ยืนยัน WHT ตอนจ่าย | Payment Voucher | TC-X03 (contract/simulate) |
| XT-04 snapshot immutable หลัง master เปลี่ยน + multi-rate per line | VAT Return (ภ.พ.30) | TC-PK06 (contract/simulate) |
| XT-05 WHT report resolve income category | ภ.ง.ด.3/53 | TC-X05 (contract/simulate) |

### Scope Lock (07_LOCKED §7.0 — ทุกข้อต้องมีเคส verify)
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LOCK-01 | รหัส unique case-insensitive ต่อบริษัท | TC-C03 |
| LOCK-02 | current-company context (เปลี่ยนบริษัทในฟอร์มไม่ได้) | TC-LK02 |
| LOCK-03 | GL รับเฉพาะ company/active/posting | TC-G04 |
| LOCK-04 | VAT STANDARD/ZERO/EXEMPT + zero/exempt rate=0 | TC-C16, TC-C17 |
| LOCK-05 | WHT report resolve ที่ payment/reporting | TC-V01, TC-X05 |
| LOCK-06 | AP advisory / Payment = จุดยืนยันหัก | TC-PK05, TC-X03 |
| LOCK-07 | picker วันที่เอกสาร + immutable snapshot | TC-PK03 |
| LOCK-08 | ไม่มี hard delete | TC-DE04 |
| LOCK-09 | อัตราของรหัส used>0 แก้ไม่ได้ → replacement | TC-R01, TC-R02 |
| LOCK-10 | permissions ชุด tax_code.* 6 สิทธิ์ | TC-P01..P05 (matrix) |
| LOCK-11 | route `/accounting/setup/tax-codes` | TC-LK11 |
| LOCK-12 | WHT GL picker = WHT_PAYABLE เท่านั้น (FLAG-1) | TC-G03 |

### Cross-cutting / States / Events
| item | cases |
|---|---|
| Loading skeleton | — ข้าม (prototype render ทันที; ไม่มี async list load ที่จับ skeleton ได้) |
| Empty state (no data) `ยังไม่มีรหัสภาษี` | TC-L17 (ต้อง simulate seed ว่าง) |
| Filtered-empty `ไม่พบรายการที่ค้นหา` + `ล้างตัวกรอง` | TC-L07 |
| Status pills variant | TC-L16 |
| Submitting state `กำลังบันทึก…` | TC-C18 |
| audit append-only event `สร้างและเปิดใช้งานรหัสภาษี` | TC-C01, TC-V02 |
| RLS cross-tenant | TC-XC01 |
| draft no auto-expiry `[AI-DEFAULT]` (OQ-10) | TC-D04 |

---

## Data Sets

| ชุด | ฟิลด์ | ค่า (กรอกได้จริง) |
|---|---|---|
| **A** (VAT create happy) | ตระกูล / รหัส / ชื่อ / อัตรา / ทิศทาง / ประเภท VAT / GL ภาษีขาย / GL ภาษีซื้อ / วันมีผลเริ่ม | `ภาษีมูลค่าเพิ่ม (VAT)` / `VAT7-TEST` / `ภาษีมูลค่าเพิ่ม 7% (ทดสอบ)` / `7` / `ขาย (ภาษีขาย)`→เปลี่ยนเป็นทั้งคู่ตามฟอร์ม / `standard` / `2131-01 · ภาษีขาย (Output VAT)` / `1151-01 · ภาษีซื้อ (Input VAT)` / `2026-01-01` |
| **B** (WHT create happy) | ตระกูล / รหัส / ชื่อ / อัตรา / ทิศทาง / ประเภทเงินได้ / GL WHT / วันมีผลเริ่ม | `ภาษีหัก ณ ที่จ่าย (WHT)` / `WHT3-TEST` / `หัก ณ ที่จ่าย 3% (ทดสอบ)` / `3` / `จ่าย` / `ค่าบริการ / รับจ้างทำของ` / `2132-01 · ภาษีหัก ณ ที่จ่ายค้างจ่าย` / `2026-01-01` |
| **C** (duplicate) | รหัส | `VAT7` (มีอยู่แล้ว = preset TX-01) · และ `vat7` (case-insensitive) |
| **D** (bad rate) | อัตรา | `150` (เกิน 100) · `-5` (ต่ำกว่า 0) |
| **E** (bad eff range) | วันมีผลเริ่ม / วันมีผลสิ้นสุด | `2026-12-31` / `2026-01-01` |
| **F** (VAT zero-rated) | ตระกูล / ประเภท VAT / อัตรา | `ภาษีมูลค่าเพิ่ม (VAT)` / `zero` / (ระบบบังคับ 0) |
| **G** (replacement) | รหัสเดิม / รหัสใหม่ / อัตรา / วันมีผลเริ่มใหม่ | `VAT7` (used=128) → `VAT7-2` / `7` / `2027-01-01` |

### ค่าตั้งต้นใน seed (prototype records — HTML L2119-2161)
- `VAT7` (TX-01) VAT 7% both **active used=128** · `VAT0` (TX-02) 0% zero sale active used=24 · `VAT-EX` (TX-03) exempt sale active used=8
- `VAT10-OLD` (TX-04) 10% both **inactive** used=340 (eff 1997-08-16 → 1999-03-31)
- `WHT1/2/3/5` (TX-05..08) active used>0 (WHT3=214) · `WHT3-PRO` (TX-09) **draft used=0 ไม่มี GL**
- GL: VAT_SALE = `2131-01/2131-03/2131-09` · VAT_PURCHASE = `1151-01/1151-02` · WHT_PAYABLE = `2132-01`(+2) · `9999-99 · บัญชีปิดใช้งาน` (inactive, ไม่ควรโผล่) · `2131-X · บัญชีของบริษัทอื่น` (COMP-002, ไม่ควรโผล่)

### ไฟล์ทดสอบ (Files)
- `—` (feature นี้ไม่มี CSV import / upload)

---

## Test Cases

### Group A — List / KPI / tabs / filter / sort / states (P-01)

#### TC-L01 — โหลดรายการ VAT + 8 คอลัมน์ + KPI (happy)
- group: List · ความสำคัญ: สูง · trace: AC-01 / FR-01 / BR-TAX-16 / event preset seed
- actor: Accountant (view) · Setup: role=demo(ครบสิทธิ์) · seed=preset 7 รหัส (default) · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ชุดข้อมูล: — · ผ่านเมื่อ: เห็นตาราง 8 คอลัมน์ + KPI 3 การ์ด + 2 tabs, tab VAT active default

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` | — | หน้ารายการโหลด; หัวข้อ **รหัสภาษี** + count `N รหัส`; sub `Master รหัสภาษีที่ทุกเอกสารการเงินอ้างอิง — VAT (ขาย/ซื้อ) และ ภาษีหัก ณ ที่จ่าย (WHT)` | ☐ |
| 2 | VERIFY แถบ KPI stats ด้านบน | — | 3 การ์ด: **รหัสทั้งหมด** (VAT n · WHT n), **พร้อมใช้วันนี้**, **ร่าง / ปิดใช้งาน** | ☐ |
| 3 | VERIFY แถว tabs | — | 2 tab: **ภาษีมูลค่าเพิ่ม (VAT)** (active) · **ภาษีหัก ณ ที่จ่าย (WHT)**; แต่ละ tab มี pill นับจำนวน | ☐ |
| 4 | VERIFY หัวตาราง | — | 8 คอลัมน์: **รหัส · ชื่อ · อัตรา · ทิศทาง · วันมีผลเริ่ม · วันมีผลสิ้นสุด · สถานะ · (actions)** | ☐ |
| 5 | VERIFY แถวข้อมูล VAT | — | เห็น `VAT7` / `ภาษีมูลค่าเพิ่ม 7%` / อัตรา 7 · pill **ใช้งาน** (สีฟ้า) | ☐ |
| 6 | VERIFY table footer | — | ข้อความ `แสดง N จาก M รหัสในกลุ่ม VAT` + `บริษัท 2BSimple จำกัด · THB · ประเทศไทย` | ☐ |

#### TC-L02 — สลับไป tab WHT (family filter)
- group: List · ความสำคัญ: สูง · trace: AC-01 / BR-TAX-16
- actor: Accountant · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: ตารางแสดงเฉพาะ family=WHT + คอลัมน์ที่ 4 เปลี่ยนเป็น "ประเภทเงินได้"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` | — | tab VAT active | ☐ |
| 2 | CLICK tab **ภาษีหัก ณ ที่จ่าย (WHT)** | — | tab WHT active; ตารางแสดงเฉพาะรหัส WHT (`WHT1/2/3/5`, `WHT3-PRO`) | ☐ |
| 3 | VERIFY หัวคอลัมน์ที่ 4 | — | เปลี่ยนจาก **ทิศทาง** เป็น **ประเภทเงินได้** | ☐ |
| 4 | VERIFY แถว `WHT3` | — | ประเภทเงินได้ = `ค่าบริการ / รับจ้างทำของ` | ☐ |

#### TC-L03 — KPI คลิก "พร้อมใช้วันนี้" กรอง pickable
- group: List · ความสำคัญ: กลาง · trace: AC-01 / BR-TAX-09
- actor: Accountant · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: ตารางเหลือเฉพาะรหัส active ที่วันนี้อยู่ในช่วงวันมีผล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → VERIFY+บันทึกจำนวนแถวเริ่มต้น | — | จดจำนวนแถวปัจจุบันไว้อ้าง step 3 | ☐ |
| 2 | CLICK การ์ด KPI **พร้อมใช้วันนี้** | — | การ์ดถูกไฮไลต์ (active state) | ☐ |
| 3 | VERIFY ตาราง | — | แสดงเฉพาะแถว pill **ใช้งาน** ที่อยู่ในช่วงวันมีผล; `VAT10-OLD` (inactive) หายไป | ☐ |

#### TC-L04 — KPI คลิก "ร่าง / ปิดใช้งาน"
- group: List · ความสำคัญ: กลาง · trace: AC-01
- actor: Accountant · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: ตารางแสดงเฉพาะ draft/inactive/archived

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` | — | list โหลด | ☐ |
| 2 | CLICK การ์ด KPI **ร่าง / ปิดใช้งาน** | — | dropdown สถานะเลื่อนเป็น `ร่าง / ปิดใช้งาน / เก็บถาวร` | ☐ |
| 3 | CLICK tab **ภาษีหัก ณ ที่จ่าย (WHT)** → VERIFY | — | เห็น `WHT3-PRO` pill **ร่าง** (สีเทา) | ☐ |

#### TC-L05 — KPI "รหัสทั้งหมด" รีเซ็ต filter
- group: List · ความสำคัญ: ต่ำ · trace: AC-01
- actor: Accountant · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: กลับมาแสดงทุกสถานะของ tab ปัจจุบัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` | — | list | ☐ |
| 2 | CLICK KPI **ร่าง / ปิดใช้งาน** | — | filter ถูก apply | ☐ |
| 3 | CLICK KPI **รหัสทั้งหมด** | — | ตารางกลับมาแสดงทุกสถานะของ tab; การ์ด **รหัสทั้งหมด** ไฮไลต์ | ☐ |

#### TC-L06 — ค้นหาเจอ (search hit)
- group: List · ความสำคัญ: กลาง · trace: AC-01 (list search)
- actor: Accountant · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: พิมพ์ `VAT7` แล้วเหลือแถวที่ตรง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` | — | list | ☐ |
| 2 | TYPE `VAT7` → ช่องค้นหา (placeholder **ค้นหารหัส / ชื่อ / ประเภทเงินได้**) | `VAT7` | ตารางเหลือแถวที่รหัส/ชื่อมี VAT7 | ☐ |

#### TC-L07 — ค้นหาไม่เจอ (filtered-empty state)
- group: List · ความสำคัญ: กลาง · trace: AC-01 / empty state (Rule #39)
- actor: Accountant · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: เห็น empty state + ปุ่ม ล้างตัวกรอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` | — | list | ☐ |
| 2 | TYPE `ZZZ-ไม่มีจริง` → ช่องค้นหา | `ZZZ-ไม่มีจริง` | ตารางว่าง; แสดง empty **ไม่พบรายการที่ค้นหา** + desc `ลองปรับคำค้นหรือล้างตัวกรอง` + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 3 | CLICK ปุ่ม **ล้างตัวกรอง** | — | ค่าค้นหาหาย; ตารางกลับมาเต็ม | ☐ |

#### TC-L08 — ค้นหาด้วยประเภทเงินได้ภาษาไทย (WHT)
- group: List · ความสำคัญ: ต่ำ · trace: AC-01 (search Thai)
- actor: Accountant · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: ค้นด้วยชื่อประเภทเงินได้แล้วเจอแถว WHT

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK tab **ภาษีหัก ณ ที่จ่าย (WHT)** | — | tab WHT | ☐ |
| 2 | TYPE `ค่าขนส่ง` → ช่องค้นหา | `ค่าขนส่ง` | เหลือแถว `WHT1` (ประเภทเงินได้ ค่าขนส่ง) | ☐ |

#### TC-L09 — filter สถานะ dropdown ทุกค่า
- group: List · ความสำคัญ: กลาง · trace: AC-01 (filter enum)
- actor: Accountant · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: แต่ละค่าใน dropdown สถานะกรองถูกต้อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` | — | list | ☐ |
| 2 | SELECT `ใช้งาน` → dropdown สถานะ | `ใช้งาน` | เหลือเฉพาะ pill **ใช้งาน** | ☐ |
| 3 | SELECT `ปิดใช้งาน` → dropdown สถานะ | `ปิดใช้งาน` | เหลือเฉพาะ pill **ปิดใช้งาน** (เช่น `VAT10-OLD`) | ☐ |
| 4 | SELECT `เก็บถาวร` → dropdown สถานะ | `เก็บถาวร` | เหลือเฉพาะ pill **เก็บถาวร** (หรือ empty ถ้าไม่มี) | ☐ |
| 5 | SELECT `ร่าง / ปิดใช้งาน / เก็บถาวร` | (attention) | แสดง draft+inactive+archived รวม | ☐ |

#### TC-L10 — ล้างตัวกรอง (reset)
- group: List · ความสำคัญ: ต่ำ · trace: AC-01
- actor: Accountant · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: ปุ่มล้างตัวกรองคืนค่าเริ่มต้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → SELECT `ปิดใช้งาน` | — | ตารางถูกกรอง; ปุ่ม **ล้างตัวกรอง** ปรากฏ | ☐ |
| 2 | CLICK ปุ่ม **ล้างตัวกรอง** | — | สถานะกลับ default; ปุ่มล้างตัวกรองหาย | ☐ |

#### TC-L11 — sort คอลัมน์ รหัส (2 ทิศ)
- group: List · ความสำคัญ: ต่ำ · trace: AC-01 (sort)
- actor: Accountant · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: คลิกหัวคอลัมน์สลับ asc/desc

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → VERIFY+จดรหัสแถวบนสุด | — | จดค่าไว้อ้าง step ถัดไป | ☐ |
| 2 | CLICK หัวคอลัมน์ **รหัส** | — | แถวเรียงตามรหัส (asc); ลูกศร sort ปรากฏ | ☐ |
| 3 | CLICK หัวคอลัมน์ **รหัส** อีกครั้ง | — | ทิศเรียงกลับด้าน (desc); แถวบนสุดต่างจาก step 2 | ☐ |

#### TC-L12 — sort คอลัมน์ อัตรา
- group: List · ความสำคัญ: ต่ำ · trace: AC-01 (sort numeric)
- actor: Accountant · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: เรียงตามค่าอัตราถูกต้อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` | — | list | ☐ |
| 2 | CLICK หัวคอลัมน์ **อัตรา** | — | เรียงจากอัตราน้อย→มาก (0,0,7,...) | ☐ |

#### TC-L13 — sort คอลัมน์ วันมีผลเริ่ม
- group: List · ความสำคัญ: ต่ำ · trace: AC-01 (sort date)
- actor: Accountant · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: เรียงตามวันที่ถูกต้อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` | — | list | ☐ |
| 2 | CLICK หัวคอลัมน์ **วันมีผลเริ่ม** | — | แถวเรียงตามวันมีผลเริ่ม (asc); `VAT10-OLD` (1997) ขึ้นบน | ☐ |

#### TC-L14 — คลิกแถว → เปิด view drawer
- group: List · ความสำคัญ: กลาง · trace: AC-01 → P-03
- actor: Accountant · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: view drawer เปิดพร้อมข้อมูลรหัสที่คลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` | — | list | ☐ |
| 2 | CLICK แถว `VAT7` | — | view drawer เลื่อนเข้า; หัวข้อ/รหัส = VAT7; pill **ใช้งาน** | ☐ |

#### TC-L15 — used badge (ใช้แล้ว vs ยังไม่ถูกใช้)
- group: List · ความสำคัญ: ต่ำ · trace: AC-01 / used glossary
- actor: Accountant · Setup: role=demo · seed=preset (VAT7 used=128, WHT3-PRO used=0) · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: badge used ตรงกับ seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK แถว `VAT7` | — | view drawer แสดง badge **ใช้แล้ว 128 เอกสาร** | ☐ |
| 2 | PRESS Esc → CLICK tab WHT → CLICK แถว `WHT3-PRO` | — | view drawer แสดง **ยังไม่ถูกใช้** | ☐ |

#### TC-L16 — status pill variant ถูกต้อง
- group: List · ความสำคัญ: ต่ำ · trace: AC-01 / status pill vocabulary
- actor: Accountant · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: pill สี/label ตรง mapping กลาง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` | — | list | ☐ |
| 2 | VERIFY pill ของ `VAT7` | — | **ใช้งาน** สีฟ้า (pill-info) | ☐ |
| 3 | SELECT `ปิดใช้งาน` → VERIFY `VAT10-OLD` | — | **ปิดใช้งาน** สีเทา (pill-muted) | ☐ |
| 4 | CLICK tab WHT → VERIFY `WHT3-PRO` | — | **ร่าง** สีเทา (pill-muted) | ☐ |

#### TC-L17 — empty state ไม่มีข้อมูลเลย (ต้อง simulate)
- group: List · ความสำคัญ: ต่ำ · trace: empty state (Rule #39)
- actor: Accountant · **(ต้อง simulate)** · Setup: role=demo · seed=**ล้าง `state.records = []`** (แก้ HTML L2119 ให้ว่าง หรือ console `state.records=[]; render()`) · files=—
- Start: OPEN `#/accounting/setup/tax-codes` (หลัง inject)
- ผ่านเมื่อ: เห็น empty state ไม่มีข้อมูล + CTA สร้าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` (records ว่าง) | — | เห็น empty **ยังไม่มีรหัสภาษี** + ปุ่ม CTA **สร้างรหัสภาษี** (primary) | ☐ |

---

### Group B — Create + activate + field validation (P-02)

#### TC-C01 — สร้าง VAT + เปิดใช้งาน ครบฟิลด์ (happy)
- group: Create · ความสำคัญ: สูง · trace: AC-02 / BR-TAX-04,10 / VR01,03,04,07,08,10 / event `สร้างและเปิดใช้งานรหัสภาษี`
- actor: Approver (activate) · Setup: role=demo(มี activate) · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes` แล้ว CLICK ปุ่ม **สร้างรหัสภาษี**
- ชุดข้อมูล: A · ผ่านเมื่อ: บันทึก active + toast **สร้างรหัสภาษีสำเร็จ** + drawer ปิด + เห็นแถวใหม่ในตาราง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK ปุ่ม **สร้างรหัสภาษี** | — | form drawer เปิด; eyebrow **รหัสภาษีใหม่**; title **สร้างรหัสภาษี** | ☐ |
| 2 | SELECT `ภาษีมูลค่าเพิ่ม (VAT)` → ช่อง **ตระกูล** | A | ฟอร์มแสดงฟิลด์สาย VAT (ประเภท VAT + ทิศทาง + GL ภาษีขาย/ซื้อ) | ☐ |
| 3 | TYPE `VAT7-TEST` → ช่อง **รหัส** | A | ช่องแสดงค่าที่กรอก | ☐ |
| 4 | TYPE `ภาษีมูลค่าเพิ่ม 7% (ทดสอบ)` → ช่อง **ชื่อ** | A | ช่องแสดงค่าที่กรอก | ☐ |
| 5 | TYPE `7` → ช่อง **อัตรา** | A | ช่องแสดง 7 | ☐ |
| 6 | VERIFY ไม่มีช่องเลือกประเทศ/สกุลเงิน (EC-07 foreign tax ไม่รองรับ) | — | ฟอร์มไม่มี selector ประเทศ/สกุลเงิน (THB/ไทยเท่านั้น) | ☐ |
| 7 | SELECT GL `2131-01 · ภาษีขาย (Output VAT)` → **บัญชี GL — ภาษีขาย** (master combobox ค้นหา) | A | ช่องแสดงบัญชีที่เลือก | ☐ |
| 8 | SELECT GL `1151-01 · ภาษีซื้อ (Input VAT)` → **บัญชี GL — ภาษีซื้อ** | A | ช่องแสดงบัญชีที่เลือก | ☐ |
| 9 | TYPE `2026-01-01` → ช่อง **วันมีผลเริ่ม** | A | ช่องแสดงวันที่ | ☐ |
| 10 | CLICK ปุ่ม **ยืนยันสร้าง** | — | drawer ปิด + toast **สร้างรหัสภาษีสำเร็จ** | ☐ |
| 11 | VERIFY ตาราง | — | เห็นแถว `VAT7-TEST` pill **ใช้งาน** | ☐ |
| 12 | CLICK แถว `VAT7-TEST` → VERIFY section audit | — | timeline มีรายการ **สร้างและเปิดใช้งานรหัสภาษี** | ☐ |

#### TC-C02 — สร้าง WHT + เปิดใช้งาน (happy, income + GL WHT)
- group: Create · ความสำคัญ: สูง · trace: AC-02/AC-06 / BR-TAX-03,07 / VR06,09 / R17 (OQ-7)
- actor: Approver · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ชุดข้อมูล: B · ผ่านเมื่อ: active + toast **สร้างรหัสภาษีสำเร็จ**
- note: R17 อัตราแนะนำต่อประเภทเงินได้เป็น "คำแนะนำ" ไม่บังคับ — **OQ-7** (ยังไม่ยืนยันแหล่งเก็บ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** | — | form drawer | ☐ |
| 2 | SELECT `ภาษีหัก ณ ที่จ่าย (WHT)` → **ตระกูล** | B | ฟอร์มเปลี่ยนเป็นสาย WHT: มีช่อง **ประเภทเงินได้** + **บัญชี GL — ภาษีหัก ณ ที่จ่ายค้างจ่าย**; ไม่มี GL ภาษีขาย/ซื้อ | ☐ |
| 3 | TYPE `WHT3-TEST` → **รหัส** · TYPE `หัก ณ ที่จ่าย 3% (ทดสอบ)` → **ชื่อ** · TYPE `3` → **อัตรา** | B | ช่องแสดงค่า | ☐ |
| 4 | SELECT `ค่าบริการ / รับจ้างทำของ` → **ประเภทเงินได้** (search combobox) | B | ช่องแสดงประเภทที่เลือก (sub `ภงด.3/53 · แนะนำ 3%`) | ☐ |
| 5 | SELECT GL `2132-01 · ภาษีหัก ณ ที่จ่ายค้างจ่าย` → **บัญชี GL — ภาษีหัก ณ ที่จ่ายค้างจ่าย** | B | ช่องแสดงบัญชี | ☐ |
| 6 | TYPE `2026-01-01` → **วันมีผลเริ่ม** | B | ช่องแสดงวันที่ | ☐ |
| 7 | CLICK ปุ่ม **ยืนยันสร้าง** | — | drawer ปิด + toast **สร้างรหัสภาษีสำเร็จ**; แถว `WHT3-TEST` pill **ใช้งาน** ใน tab WHT | ☐ |

#### TC-C03 — รหัสซ้ำในบริษัท (negative, case-insensitive) [LOCK-01]
- group: Create · ความสำคัญ: สูง · trace: AC-02b / EC-06 / BR-TAX-01 / VR02 / BR_TAX_CODE_DUPLICATE / LOCK-01
- actor: Approver · Setup: role=demo · seed=preset (มี `VAT7`) · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ชุดข้อมูล: C · ผ่านเมื่อ: block inline ที่ช่องรหัส

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** | — | form drawer | ☐ |
| 2 | TYPE `VAT7` → **รหัส** · TYPE `ชื่อทดสอบ` → **ชื่อ** · TYPE `7` → **อัตรา** | C | ช่องแสดงค่า | ☐ |
| 3 | CLICK ปุ่ม **ยืนยันสร้าง** | — | inline error ใต้ช่องรหัส: **รหัสนี้มีอยู่แล้วในบริษัทปัจจุบัน** (VR02 / 422 BR_TAX_CODE_DUPLICATE); ไม่บันทึก | ☐ |
| 4 | TYPE (ลบแล้วพิมพ์) `vat7` → **รหัส** → CLICK **ยืนยันสร้าง** | `vat7` | ยัง block ด้วยข้อความเดิม (case-insensitive) | ☐ |

#### TC-C04 — เว้นรหัสว่าง (negative, VR01 required)
- group: Create · ความสำคัญ: สูง · trace: VR01 / ERR_VALIDATION_FAILED
- actor: Approver · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: error required ที่ช่องรหัส

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** | — | form drawer | ☐ |
| 2 | TYPE `ชื่อทดสอบ` → **ชื่อ** (เว้นรหัสว่าง) → CLICK **ยืนยันสร้าง** | — | inline error ใต้ช่องรหัส: **กรุณากรอกรหัส** | ☐ |

#### TC-C05 — เว้นชื่อว่าง (negative, VR03 required)
- group: Create · ความสำคัญ: กลาง · trace: VR03 / ERR_VALIDATION_FAILED
- actor: Approver · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: error required ที่ช่องชื่อ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** | — | form drawer | ☐ |
| 2 | TYPE `TEST-C05` → **รหัส** (เว้นชื่อว่าง) → CLICK **ยืนยันสร้าง** | — | inline error ใต้ช่องชื่อ: **กรุณากรอกชื่อ** | ☐ |

#### TC-C06 — เว้นอัตราตอน activate VAT standard (negative, VR04)
- group: Create · ความสำคัญ: กลาง · trace: VR04 / ERR_VALIDATION_FAILED
- actor: Approver · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: error กรุณากรอกอัตรา (VAT standard บังคับ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** | — | form drawer (default VAT standard) | ☐ |
| 2 | TYPE `TEST-C06` → **รหัส** · TYPE `ชื่อ` → **ชื่อ** (เว้นอัตราว่าง) → CLICK **ยืนยันสร้าง** | — | inline error ใต้ช่องอัตรา: **กรุณากรอกอัตรา** | ☐ |

#### TC-C07 — อัตรานอกช่วง (boundary, VR05 >100 / <0)
- group: Create · ความสำคัญ: กลาง · trace: VR05 / R13 / ERR_VALIDATION_FAILED
- actor: Approver · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ชุดข้อมูล: D · ผ่านเมื่อ: error อัตราต้องอยู่ระหว่าง 0 ถึง 100

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** | — | form drawer | ☐ |
| 2 | TYPE `TEST-C07` → **รหัส** · `ชื่อ` → **ชื่อ** · TYPE `150` → **อัตรา** → CLICK **ยืนยันสร้าง** | D | inline error ใต้ช่องอัตรา: **อัตราต้องอยู่ระหว่าง 0 ถึง 100** | ☐ |
| 3 | TYPE `-5` → **อัตรา** → CLICK **ยืนยันสร้าง** | D | ยัง block ด้วยข้อความเดิม (ต่ำกว่า 0) | ☐ |

#### TC-C08 — อัตรา boundary ค่าถูก (0 และ 100 ผ่าน)
- group: Create · ความสำคัญ: ต่ำ · trace: VR05 boundary ฝั่งผ่าน
- actor: Approver · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: อัตรา 0 (zero VAT) และ 100 ผ่าน validation

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** | — | form drawer | ☐ |
| 2 | TYPE `TEST-C08` → **รหัส** · `ชื่อ` → **ชื่อ** · TYPE `100` → **อัตรา** · SELECT GL ภาษีขาย+ซื้อ · TYPE `2026-01-01` → **วันมีผลเริ่ม** → CLICK **ยืนยันสร้าง** | — | ไม่มี error ที่ช่องอัตรา; บันทึกผ่าน (toast **สร้างรหัสภาษีสำเร็จ**) | ☐ |

#### TC-C09 — เว้นวันมีผลเริ่มตอน activate (negative, VR10)
- group: Create · ความสำคัญ: กลาง · trace: VR10 / BR_TAX_EFF_START_REQUIRED
- actor: Approver · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: error กรุณาระบุวันมีผลเริ่ม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** | — | form drawer | ☐ |
| 2 | กรอก รหัส/ชื่อ/อัตรา 7 + GL ครบ (เว้นวันมีผลเริ่ม) → CLICK **ยืนยันสร้าง** | A (ยกเว้น effStart) | inline error ใต้วันมีผลเริ่ม: **กรุณาระบุวันมีผลเริ่ม** | ☐ |

#### TC-C10 — วันสิ้นสุดก่อนวันเริ่ม (negative, VR11)
- group: Create · ความสำคัญ: กลาง · trace: VR11 / R14 / BR_TAX_EFF_RANGE
- actor: Approver · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ชุดข้อมูล: E · ผ่านเมื่อ: error วันสิ้นสุดต้องไม่ก่อนวันเริ่ม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** | — | form drawer | ☐ |
| 2 | กรอก รหัส/ชื่อ/อัตรา + TYPE `2026-12-31` → **วันมีผลเริ่ม** + TYPE `2026-01-01` → **วันมีผลสิ้นสุด** → CLICK **ยืนยันสร้าง** | E | inline error ใต้วันมีผลสิ้นสุด: **วันสิ้นสุดต้องไม่ก่อนวันเริ่ม** | ☐ |

#### TC-C11 — VAT ขาย ไม่ผูก GL ภาษีขาย (negative, VR07)
- group: Create · ความสำคัญ: สูง · trace: VR07 / BR-TAX-04 / BR_TAX_GL_REQUIRED
- actor: Approver · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: error ต้องเลือกบัญชี GL กลุ่มภาษีขาย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** | — | form drawer VAT | ☐ |
| 2 | SELECT `ขาย (ภาษีขาย)` → **ทิศทาง** · กรอก รหัส/ชื่อ/อัตรา 7 (เว้น GL ภาษีขาย) → CLICK **ยืนยันสร้าง** | — | inline error ใต้ GL ภาษีขาย: **ต้องเลือกบัญชี GL กลุ่มภาษีขายก่อนเปิดใช้งาน** | ☐ |

#### TC-C12 — VAT ซื้อ ไม่ผูก GL ภาษีซื้อ (negative, VR08)
- group: Create · ความสำคัญ: กลาง · trace: VR08 / BR-TAX-04 / BR_TAX_GL_REQUIRED
- actor: Approver · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: error ต้องเลือกบัญชี GL กลุ่มภาษีซื้อ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** | — | form drawer VAT | ☐ |
| 2 | SELECT `ซื้อ (ภาษีซื้อ)` → **ทิศทาง** · กรอก รหัส/ชื่อ/อัตรา (เว้น GL ภาษีซื้อ) → CLICK **ยืนยันสร้าง** | — | inline error ใต้ GL ภาษีซื้อ: **ต้องเลือกบัญชี GL กลุ่มภาษีซื้อก่อนเปิดใช้งาน** | ☐ |

#### TC-C13 — VAT ทั้งคู่ ไม่ผูก GL ทั้งสอง (negative, VR07+VR08)
- group: Create · ความสำคัญ: กลาง · trace: VR07,VR08 / BR-TAX-04
- actor: Approver · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: error ทั้ง GL ภาษีขายและภาษีซื้อ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** | — | form drawer VAT default ทิศทาง ทั้งคู่ | ☐ |
| 2 | กรอก รหัส/ชื่อ/อัตรา 7 (เว้น GL ทั้งสอง) → CLICK **ยืนยันสร้าง** | — | เห็น error **ต้องเลือกบัญชี GL กลุ่มภาษีขายก่อนเปิดใช้งาน** และ **...ภาษีซื้อ...** ทั้งคู่ | ☐ |

#### TC-C14 — WHT ไม่ผูก GL WHT (negative, VR09) [LOCK-12 boundary]
- group: Create · ความสำคัญ: สูง · trace: VR09 / BR-TAX-07 / BR_TAX_GL_REQUIRED
- actor: Approver · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: error GL WHT ค้างจ่าย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** → SELECT `ภาษีหัก ณ ที่จ่าย (WHT)` → **ตระกูล** | — | ฟอร์มสาย WHT | ☐ |
| 2 | กรอก รหัส/ชื่อ/อัตรา 3 + SELECT ประเภทเงินได้ (เว้น GL WHT) → CLICK **ยืนยันสร้าง** | — | inline error ใต้ GL WHT: **ต้องเลือกบัญชี GL กลุ่มภาษีหัก ณ ที่จ่ายค้างจ่ายก่อนเปิดใช้งาน** | ☐ |

#### TC-C15 — WHT ไม่เลือกประเภทเงินได้ (negative, VR06)
- group: Create · ความสำคัญ: สูง · trace: AC-06 / VR06 / BR-TAX-03 / BR_TAX_WHT_INCOME_REQUIRED
- actor: Approver · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: error WHT ต้องระบุประเภทเงินได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** → SELECT `ภาษีหัก ณ ที่จ่าย (WHT)` → **ตระกูล** | — | ฟอร์มสาย WHT | ☐ |
| 2 | กรอก รหัส/ชื่อ/อัตรา 3 + SELECT GL WHT (เว้นประเภทเงินได้) → CLICK **ยืนยันสร้าง** | — | inline error ใต้ประเภทเงินได้: **WHT ต้องระบุประเภทเงินได้** | ☐ |

#### TC-C16 — VAT zero-rated → อัตราถูกบังคับ 0 [LOCK-04]
- group: Create · ความสำคัญ: กลาง · trace: BR-TAX-10 / LOCK-04 / R10
- actor: Approver · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ชุดข้อมูล: F · ผ่านเมื่อ: เลือกประเภท zero → อัตรา = 0 (บังคับ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** | — | form drawer VAT | ☐ |
| 2 | SELECT ประเภท VAT `zero` (อัตราศูนย์) → **ประเภท VAT** | F | ช่องอัตราถูกตั้ง/บังคับเป็น **0** (ไม่ต้องกรอกเอง) | ☐ |
| 3 | กรอก รหัส/ชื่อ + SELECT GL ภาษีขาย + วันมีผลเริ่ม → CLICK **ยืนยันสร้าง** | — | บันทึก active สำเร็จ + toast **สร้างรหัสภาษีสำเร็จ**; อัตราแสดง 0 ในตาราง | ☐ |

#### TC-C17 — VAT exempt → อัตรา 0 [LOCK-04]
- group: Create · ความสำคัญ: ต่ำ · trace: BR-TAX-10 / LOCK-04
- actor: Approver · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: exempt → อัตรา 0

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** | — | form drawer VAT | ☐ |
| 2 | SELECT ประเภท VAT `exempt` (ยกเว้น) → **ประเภท VAT** | — | อัตราถูกบังคับ 0 | ☐ |

#### TC-C18 — submitting state "กำลังบันทึก…" (UX)
- group: Create · ความสำคัญ: ต่ำ · trace: submitting state (Rule #44)
- actor: Approver · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: ระหว่างบันทึกเห็นปุ่ม disabled ข้อความ กำลังบันทึก…

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** | — | form drawer | ☐ |
| 2 | กรอกครบ (ชุด A) → CLICK **ยืนยันสร้าง** → WAIT สังเกตปุ่มทันที | A | ปุ่มเปลี่ยนเป็น **กำลังบันทึก…** (disabled + สปินเนอร์) ชั่วครู่ก่อน toast | ☐ |

---

### Group C — Save draft (P-02)

#### TC-D01 — บันทึกร่างไม่ผูก GL (happy) [Maker]
- group: Draft · ความสำคัญ: สูง · trace: AC-04 / EC-04 / BR-TAX-05
- actor: Maker (create) · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ชุดข้อมูล: B (ไม่ผูก GL) · ผ่านเมื่อ: draft สำเร็จ + toast บันทึกร่างแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** → SELECT `ภาษีหัก ณ ที่จ่าย (WHT)` | — | ฟอร์มสาย WHT | ☐ |
| 2 | TYPE `WHT-DRAFT` → **รหัส** · `ร่างทดสอบ` → **ชื่อ** (ไม่เลือก GL / income) | — | ช่องแสดงค่า | ☐ |
| 3 | CLICK ปุ่ม **บันทึกร่าง** | — | drawer ปิด + toast **บันทึกร่างแล้ว** (info) | ☐ |
| 4 | CLICK tab WHT → VERIFY แถว `WHT-DRAFT` | — | pill **ร่าง** (สีเทา) | ☐ |

#### TC-D02 — บันทึกร่างขาดรหัส/ชื่อ (negative)
- group: Draft · ความสำคัญ: กลาง · trace: VR01/VR03 (draft ต้องมี code+name) / warning toast
- actor: Maker · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: toast เตือนกรอกรหัสและชื่อก่อน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** | — | form drawer | ☐ |
| 2 | CLICK ปุ่ม **บันทึกร่าง** (เว้นรหัส/ชื่อ) | — | toast (warning) **กรุณากรอกรหัสและชื่อก่อนบันทึกร่าง**; ไม่บันทึก | ☐ |

#### TC-D03 — draft แล้ว activate ยังไม่มี GL ถูกบล็อก (AC-04)
- group: Draft · ความสำคัญ: สูง · trace: AC-04 / EC-04 / BR-TAX-04 / VR09
- actor: Approver · Setup: role=demo · seed=draft `WHT3-PRO` (TX-09, ไม่มี GL) · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → tab WHT → เปิดแก้ไข `WHT3-PRO`
- ผ่านเมื่อ: กด activate → block เพราะยังไม่มี GL

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK tab WHT → CLICK แถว `WHT3-PRO` → CLICK **แก้ไข** | — | form drawer edit, eyebrow **แก้ไขรหัสภาษี** | ☐ |
| 2 | CLICK ปุ่ม **บันทึกการแก้ไข** (ยังไม่เลือก GL) | — | inline error GL WHT: **ต้องเลือกบัญชี GL กลุ่มภาษีหัก ณ ที่จ่ายค้างจ่ายก่อนเปิดใช้งาน**; ไม่ activate | ☐ |
| 3 | SELECT GL `2132-01 · ภาษีหัก ณ ที่จ่ายค้างจ่าย` + วันมีผลเริ่ม → CLICK **บันทึกการแก้ไข** | — | บันทึก active + toast **บันทึกการแก้ไขแล้ว** | ☐ |

#### TC-D04 — draft คงอยู่ ไม่มี auto-expiry `[AI-DEFAULT]`
- group: Draft · ความสำคัญ: ต่ำ · trace: OQ-10 / PR-6 (LD-05) · **`[AI-DEFAULT]`**
- actor: Maker · Setup: role=demo · seed=draft `WHT3-PRO` · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- note: **`[AI-DEFAULT]`** draft persist indefinitely, ไม่มี cleanup job — **OQ-10** (ยังไม่ยืนยัน). ทดสอบเชิงสังเกต: draft ยังอยู่หลัง reload
- ผ่านเมื่อ: reload แล้ว draft ยังอยู่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK tab WHT → VERIFY `WHT3-PRO` | — | เห็นแถว draft | ☐ |
| 2 | OPEN `#/accounting/setup/tax-codes` (reload หน้าใหม่) → CLICK tab WHT → VERIFY `WHT3-PRO` | — | draft ยังอยู่ (ไม่หาย/ไม่ expire) | ☐ |

---

### Group D — GL master combobox filter (Rule #94 / FLAG-1)

#### TC-G01 — GL ภาษีขาย แสดงเฉพาะ role VAT_SALE
- group: GL · ความสำคัญ: สูง · trace: AC-05 / BR-TAX-06,07 / ENG-03
- actor: Maker · Setup: role=demo · seed=GL preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: dropdown GL ภาษีขายมีเฉพาะบัญชี VAT_SALE

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** → SELECT `ขาย (ภาษีขาย)` → **ทิศทาง** | — | ฟอร์ม VAT ขาย | ☐ |
| 2 | CLICK ช่อง **บัญชี GL — ภาษีขาย** (เปิด combobox) | — | รายการมีเฉพาะบัญชี VAT_SALE: `2131-01 · ภาษีขาย (Output VAT)`, `2131-03 · ภาษีขายอัตราศูนย์`, `2131-09 · ภาษีขาย–ยกเว้น` | ☐ |
| 3 | VERIFY ไม่มี `1151-01` (ภาษีซื้อ) / `2132-01` (WHT) ในรายการ | — | ไม่พบบัญชีต่าง role | ☐ |

#### TC-G02 — GL ภาษีซื้อ แสดงเฉพาะ role VAT_PURCHASE
- group: GL · ความสำคัญ: สูง · trace: AC-05 / BR-TAX-06,07
- actor: Maker · Setup: role=demo · seed=GL preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: dropdown GL ภาษีซื้อมีเฉพาะ VAT_PURCHASE

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** → SELECT `ซื้อ (ภาษีซื้อ)` → **ทิศทาง** | — | ฟอร์ม VAT ซื้อ | ☐ |
| 2 | CLICK ช่อง **บัญชี GL — ภาษีซื้อ** | — | มีเฉพาะ `1151-01 · ภาษีซื้อ (Input VAT)`, `1151-02 · ภาษีซื้อรอเรียกคืน`; ไม่มี VAT_SALE/WHT | ☐ |

#### TC-G03 — GL WHT แสดงเฉพาะ WHT_PAYABLE เท่านั้น ⭐ (FLAG-1 / LOCK-12 / AC-05b)
- group: GL · ความสำคัญ: สูง · trace: AC-05b / BR-TAX-07 / VR09 / LOCK-12 / FLAG-1
- actor: Maker · Setup: role=demo · seed=GL preset (WHT_PAYABLE ≥1 + VAT_SALE/VAT_PURCHASE/OTHER อยู่ด้วย) · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** → SELECT WHT
- ผ่านเมื่อ: GL WHT combobox มี **เฉพาะ** บัญชี role WHT_PAYABLE (ไม่ใช่ทุก GL)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** → SELECT `ภาษีหัก ณ ที่จ่าย (WHT)` → **ตระกูล** | — | ฟอร์มสาย WHT; มีช่อง **บัญชี GL — ภาษีหัก ณ ที่จ่ายค้างจ่าย** | ☐ |
| 2 | CLICK ช่อง **บัญชี GL — ภาษีหัก ณ ที่จ่ายค้างจ่าย** (เปิด combobox) | — | รายการมี **เฉพาะ** บัญชี WHT_PAYABLE เช่น `2132-01 · ภาษีหัก ณ ที่จ่ายค้างจ่าย` | ☐ |
| 3 | VERIFY ไม่มีบัญชี VAT/OTHER | — | ไม่พบ `2131-01` (VAT_SALE), `1151-01` (VAT_PURCHASE), `9999-99` (OTHER) ในรายการ — ยืนยัน FLAG-1 RESOLVED (WHT_PAYABLE เท่านั้น) | ☐ |

#### TC-G04 — GL ตัดบัญชี inactive / posting=false / บริษัทอื่น [LOCK-03]
- group: GL · ความสำคัญ: สูง · trace: BR-TAX-06 / LOCK-03 / ENG-03
- actor: Maker · Setup: role=demo · seed=GL (มี `9999-99` inactive + `2131-X` COMP-002) · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: combobox GL ไม่มีบัญชี inactive/no-posting/บริษัทอื่น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** → SELECT `ขาย (ภาษีขาย)` → **ทิศทาง** | — | ฟอร์ม VAT ขาย | ☐ |
| 2 | CLICK ช่อง **บัญชี GL — ภาษีขาย** → TYPE `9999` ค้นหา | `9999` | ไม่พบ `9999-99 · บัญชีปิดใช้งาน` (inactive + posting=false ถูกกรองออก) | ☐ |
| 3 | TYPE `2131-X` ค้นหา | `2131-X` | ไม่พบ `2131-X · บัญชีของบริษัทอื่น` (COMP-002 ถูกกรองออก) | ☐ |

---

### Group E — Rate lock used>0 + Replacement lineage (P-02)

#### TC-R01 — เปิดแก้ไขรหัส used>0 → ฟิลด์อ่านอย่างเดียว (AC-07) [LOCK-09]
- group: Replacement · ความสำคัญ: สูง · trace: AC-07 / EC-02 / BR-TAX-02 / BR_TAX_RATE_LOCKED / LOCK-09
- actor: Maker · Setup: role=demo · seed=`VAT7` (used=128) · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK แถว `VAT7` → CLICK **แก้ไข**
- ผ่านเมื่อ: อัตรา/ตระกูล/ทิศทาง/รหัส read-only + ป้าย อ่านอย่างเดียว + ปุ่ม สร้างรหัสแทน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK แถว `VAT7` | — | view drawer; badge **ใช้แล้ว 128 เอกสาร** | ☐ |
| 2 | CLICK ปุ่ม **แก้ไข** | — | form drawer edit `แก้ไข VAT7` | ☐ |
| 3 | VERIFY ช่อง อัตรา/รหัส/ตระกูล/ทิศทาง | — | เป็น read-only + ป้าย **อ่านอย่างเดียว** (ไอคอน lock) | ☐ |
| 4 | VERIFY ปุ่ม replacement | — | เห็นปุ่ม **สร้างรหัสแทน** | ☐ |

#### TC-R02 — Replacement flow สร้างรหัสแทน + lineage (AC-08) [LOCK-09]
- group: Replacement · ความสำคัญ: สูง · trace: AC-08 / EC-12 / BR-TAX-02 / FN-08
- actor: Approver · Setup: role=demo · seed=`VAT7` (used=128) · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK แถว `VAT7` → CLICK **แก้ไข** → CLICK **สร้างรหัสแทน**
- ชุดข้อมูล: G · ผ่านเมื่อ: สร้างรหัสใหม่ที่ตั้งค่าอัตรา+วันมีผลใหม่ และ lineage เชื่อมกัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK แถว `VAT7` → CLICK **แก้ไข** → VERIFY+จดรหัสเดิม | — | จด `VAT7` used=128 ไว้อ้าง step ท้าย | ☐ |
| 2 | CLICK ปุ่ม **สร้างรหัสแทน** | — | ฟอร์มเปลี่ยนเป็น eyebrow **สร้างรหัสแทน**; alert `กำลังสร้างรหัสแทนของ VAT7 — กำหนดอัตราและวันมีผลใหม่`; รหัส prefill `VAT7-2` (code+"-N") | ☐ |
| 3 | TYPE `2027-01-01` → **วันมีผลเริ่ม** (อัตราใหม่ตามชุด G) → CLICK **ยืนยันสร้าง** | G | drawer ปิด + toast **สร้างรหัสภาษีสำเร็จ**; แถว `VAT7-2` ปรากฏ pill **ใช้งาน** | ☐ |
| 4 | CLICK แถว `VAT7-2` → VERIFY lineage | — | เห็น field **ใช้แทนรหัส** = `VAT7` | ☐ |
| 5 | PRESS Esc → CLICK แถว `VAT7` → VERIFY | — | field **ถูกแทนด้วย** = `VAT7-2`; วันมีผลสิ้นสุดเดิม = วันก่อน 2027-01-01 (= 2026-12-31) | ☐ |

#### TC-R03 — view drawer แสดง lineage ทั้งสองทาง
- group: Replacement · ความสำคัญ: กลาง · trace: AC-08 (view lineage)
- actor: Accountant · Setup: role=demo · seed=มีคู่ replacement (รันหลัง TC-R02) · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: view drawer ของทั้งรหัสเดิมและใหม่แสดง lineage

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK แถว `VAT7-2` → VERIFY | — | **ใช้แทนรหัส VAT7** | ☐ |
| 2 | PRESS Esc → CLICK แถว `VAT7` → VERIFY | — | **ถูกแทนด้วย VAT7-2** | ☐ |

#### TC-R04 — แก้ไข draft (used=0) ฟิลด์แก้ได้ (Maker update allow)
- group: Replacement · ความสำคัญ: กลาง · trace: Maker update = allow / EC-04
- actor: Maker · Setup: role=demo · seed=draft `WHT3-PRO` (used=0) · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → tab WHT → CLICK แถว `WHT3-PRO` → CLICK **แก้ไข**
- ผ่านเมื่อ: อัตรา/รหัสแก้ได้ (ไม่ล็อกเพราะ used=0)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK tab WHT → CLICK แถว `WHT3-PRO` → CLICK **แก้ไข** | — | form drawer edit | ☐ |
| 2 | VERIFY ช่อง อัตรา/รหัส | — | แก้ไขได้ (ไม่มีป้าย อ่านอย่างเดียว); ไม่มีปุ่ม สร้างรหัสแทน | ☐ |
| 3 | TYPE `5` → **อัตรา** → CLICK **บันทึกร่าง** | — | toast **บันทึกร่างแล้ว**; ค่าอัตราอัปเดต | ☐ |

---

### Group F — Deactivate / Archive (P-05)

#### TC-DE01 — ปิดใช้งานรหัส active (AC-09) [LOCK-08]
- group: Deactivate · ความสำคัญ: สูง · trace: AC-09 / EC-01 / BR-TAX-05 / toast deactivate
- actor: Approver · Setup: role=demo(มี deactivate) · seed=`VAT7` active · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: ยืนยัน modal → status inactive + toast

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK ไอคอน **ปิดใช้งาน** (power) ท้ายแถว `VAT7` | — | confirm modal เปิด; title **ปิดใช้งานรหัสภาษี?**; body มี `"VAT7" จะไม่แสดงในตัวเลือกของเอกสารใหม่...`; alert **สามารถเปิดใช้งานใหม่ได้ภายหลังจากหน้าแก้ไข** | ☐ |
| 2 | CLICK ปุ่ม **ปิดใช้งาน** (danger) | — | modal ปิด + toast **ปิดใช้งานรหัสภาษีแล้ว** (success) | ☐ |
| 3 | SELECT `ปิดใช้งาน` → dropdown สถานะ → VERIFY `VAT7` | — | pill **ปิดใช้งาน** (สีเทา) | ☐ |

#### TC-DE02 — เก็บร่างถาวร (AC-10, no hard delete)
- group: Archive · ความสำคัญ: กลาง · trace: AC-10 / EC-03 / BR-TAX-05 / R05
- actor: Approver · Setup: role=demo · seed=draft `WHT3-PRO` · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → tab WHT
- ผ่านเมื่อ: modal alert no-hard-delete + toast เก็บร่างถาวรแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK tab WHT → CLICK ไอคอน **เก็บร่างถาวร** (archive) ท้ายแถว `WHT3-PRO` | — | confirm modal; title **เก็บร่างถาวร?**; alert ใน body **ระบบไม่มีการลบถาวรสำหรับรหัสภาษี** | ☐ |
| 2 | CLICK ปุ่ม **เก็บร่างถาวร** (danger) | — | modal ปิด + toast **เก็บร่างถาวรแล้ว** (success) | ☐ |
| 3 | SELECT `เก็บถาวร` → dropdown สถานะ → VERIFY | — | `WHT3-PRO` pill **เก็บถาวร** (สีเทา); ยังอยู่ในระบบ (ไม่ถูกลบ) | ☐ |

#### TC-DE03 — ยกเลิก modal ปิดใช้งาน (dirty-safe)
- group: Deactivate · ความสำคัญ: ต่ำ · trace: AC-09 (cancel path)
- actor: Approver · Setup: role=demo · seed=`WHT1` active · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → tab WHT
- ผ่านเมื่อ: กดยกเลิก → สถานะไม่เปลี่ยน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK tab WHT → CLICK ไอคอน **ปิดใช้งาน** ท้ายแถว `WHT1` | — | confirm modal เปิด | ☐ |
| 2 | CLICK ปุ่ม **ยกเลิก** | — | modal ปิด; `WHT1` ยัง pill **ใช้งาน** (ไม่เปลี่ยน) | ☐ |
| 3 | CLICK ไอคอน **ปิดใช้งาน** → PRESS Esc | — | modal ปิดด้วย Esc; สถานะไม่เปลี่ยน | ☐ |

#### TC-DE04 — ไม่มี hard delete บนจอ (verify LOCK-08)
- group: Archive · ความสำคัญ: กลาง · trace: BR-TAX-05 / LOCK-08 / EC-03
- actor: Accountant · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: ไม่มีปุ่ม/action "ลบ" ที่ไหนเลย (มีแค่ ปิดใช้งาน/เก็บร่างถาวร)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → VERIFY action ท้ายแถว active | — | มีเฉพาะไอคอน **ปิดใช้งาน**; ไม่มีไอคอน/ปุ่ม **ลบ** (trash) | ☐ |
| 2 | CLICK แถว `VAT7` → VERIFY ปุ่มใน view drawer | — | มี **แก้ไข** / **ปิดใช้งาน** / **ปิด**; ไม่มีปุ่ม **ลบ** | ☐ |
| 3 | CLICK tab WHT → VERIFY action ท้ายแถว draft `WHT3-PRO` | — | มีเฉพาะ **เก็บร่างถาวร**; ไม่มี **ลบ** | ☐ |

---

### Group G — View drawer + Audit gate (P-03)

#### TC-V01 — view drawer แสดงรายละเอียดครบ [LOCK-05 WHT mapping]
- group: View · ความสำคัญ: กลาง · trace: AC-12 / BR-TAX-11 / LOCK-05
- actor: Accountant · Setup: role=demo · seed=`WHT3` (WHT active) + `VAT7` · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: view drawer แสดง field summary; WHT แสดงกติกาแบบรายงาน resolve ที่ payee/payment

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK แถว `VAT7` | — | view drawer: ตระกูล **ภาษีมูลค่าเพิ่ม (VAT)** · บริษัท `บริษัท 2BSimple จำกัด` · GL ภาษีขาย/ซื้อ · วันมีผล | ☐ |
| 2 | PRESS Esc → CLICK tab WHT → CLICK แถว `WHT3` → VERIFY | — | ตระกูล **ภาษีหัก ณ ที่จ่าย (WHT)** · ประเภทเงินได้ `ค่าบริการ / รับจ้างทำของ` · กติกาแบบรายงาน **เลือกจากผู้รับเงินและบริบทการจ่าย** (LOCK-05) | ☐ |

#### TC-V02 — audit section แสดงเมื่อมี view_audit (AC-12)
- group: View · ความสำคัญ: กลาง · trace: AC-12 / §5.3 view_audit / event audit
- actor: Accountant (มี view_audit) · Setup: role=demo(มี view_audit) · seed=`VAT7` (มี audit) · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: เห็น section ประวัติการเปลี่ยนแปลง (Audit) เรียงล่าสุดก่อน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK แถว `VAT7` | — | view drawer | ☐ |
| 2 | VERIFY section audit | — | เห็นหัวข้อ **ประวัติการเปลี่ยนแปลง (Audit)** + timeline (เช่น `สร้างและเปิดใช้งานรหัสภาษี` โดย `ระบบ (Preset)`) | ☐ |

#### TC-V03 — audit section ซ่อนเมื่อไม่มี view_audit (EC-17) (ต้อง simulate)
- group: View · ความสำคัญ: กลาง · trace: AC-12 / EC-17 / ERR_INSUFFICIENT_ROLE (403) · **(ต้อง simulate)**
- actor: Viewer (ไม่มี view_audit) · Setup: role=viewer · seed=`VAT7` · **inject:** แก้ `CURRENT_PERMISSIONS` (HTML L2067-2070) ลบ `'tax_code.view_audit'` แล้ว reload · files=—
- Start: OPEN `#/accounting/setup/tax-codes` (หลัง inject)
- ผ่านเมื่อ: view drawer ไม่มี section audit (API-10 direct → 403)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` (permission ไม่มี view_audit) → CLICK แถว `VAT7` | — | view drawer เปิด | ☐ |
| 2 | VERIFY section audit | — | **ไม่มี** หัวข้อ ประวัติการเปลี่ยนแปลง (Audit) (section ถูกซ่อน) | ☐ |
| 3 | (contract) เรียก F-TAX-API-10 GET audit ตรง | — | ตอบ 403 ERR_INSUFFICIENT_ROLE + log access (D9) | ☐ |

---

### Group H — Picker + snapshot (P-04)

#### TC-PK01 — picker บริบทขาย แสดง VAT ขาย pickable (AC-11)
- group: Picker · ความสำคัญ: สูง · trace: AC-11 / BR-TAX-09 / ENG-02
- actor: Consumer/Accountant · Setup: role=demo · seed=preset (VAT7 active both) · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK ปุ่ม **ดูรายการที่เลือกได้ในเอกสารใหม่**
- ผ่านเมื่อ: modal picker แสดง VAT ที่ pickable ในบริบทขาย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK ปุ่ม **ดูรายการที่เลือกได้ในเอกสารใหม่** | — | modal เปิด; title **ตัวเลือกตามวันที่เอกสาร**; field **นำไปใช้กับ** default `เอกสารขาย (SO / AR Invoice)` | ☐ |
| 2 | VERIFY กลุ่ม VAT | — | หัวข้อ **VAT ที่ใช้ได้** + รายการ VAT ขาย/ทั้งคู่ (เช่น `VAT7`, `VAT0`) แต่ละแถวมีปุ่ม **เลือกและบันทึกค่า** | ☐ |
| 3 | VERIFY ไม่มี VAT10-OLD | — | `VAT10-OLD` (inactive) ไม่โผล่ในรายการ pickable | ☐ |

#### TC-PK02 — เปลี่ยนวันที่เอกสารเป็นอดีต/อนาคต (EC-11 future effStart)
- group: Picker · ความสำคัญ: กลาง · trace: AC-11 / EC-11 / BR-TAX-09 / ENG-02
- actor: Consumer · Setup: role=demo · seed=preset (VAT10-OLD eff 1997-1999; VAT7 eff 2017→) · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → เปิด picker
- ผ่านเมื่อ: เปลี่ยนวันที่แล้วรายการ pickable เปลี่ยนตามช่วงวันมีผล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **ดูรายการที่เลือกได้ในเอกสารใหม่** → VERIFY+จดรายการ VAT วันนี้ | — | จดรายการ pickable ปัจจุบันไว้อ้าง | ☐ |
| 2 | TYPE `1998-06-01` → ช่อง **วันที่เอกสาร** | 1998-06-01 | รายการเปลี่ยน; `VAT10-OLD` แม้ inactive ก็ยังไม่ pickable (status ต้อง active) → ไม่โผล่ | ☐ |
| 3 | TYPE `2015-01-01` → ช่อง **วันที่เอกสาร** (ก่อน VAT7 effStart 2017) | 2015-01-01 | `VAT7` หายจากรายการ (docDate < effStart, EC-11 window) | ☐ |

#### TC-PK03 — capture snapshot (immutable) [LOCK-07]
- group: Picker · ความสำคัญ: สูง · trace: AC-11 / BR-TAX-08 / LOCK-07 / ENG-01
- actor: Consumer · Setup: role=demo · seed=`VAT7` active · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → เปิด picker
- ผ่านเมื่อ: เลือก VAT → snapshot card ปรากฏ + toast

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **ดูรายการที่เลือกได้ในเอกสารใหม่** | — | picker (บริบท ขาย) | ☐ |
| 2 | CLICK ปุ่ม **เลือกและบันทึกค่า** ที่แถว `VAT7` | — | toast **เลือกและบันทึก snapshot ในเอกสารแล้ว** (success); card **Snapshot ที่บันทึกในเอกสาร** ปรากฏ = `VAT7 · ... · อัตรา 7% · วันที่เอกสาร ...` | ☐ |
| 3 | VERIFY snapshot code | — | card แสดง `taxCodeId · family · vatKind` (immutable payload — ENG-01) | ☐ |

#### TC-PK04 — บริบทซื้อ: WHT = advisory (block final) (XT-02 / VR13)
- group: Picker · ความสำคัญ: สูง · trace: AC-11 / XT-02 / EC-05 / VR13 / BR-TAX-12
- actor: Consumer · Setup: role=demo · seed=preset (VAT ซื้อ + WHT active) · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → เปิด picker → บริบทซื้อ
- ผ่านเมื่อ: VAT ซื้อเลือกได้; WHT แสดงเป็นคำแนะนำ ไม่มีปุ่มเลือก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **ดูรายการที่เลือกได้ในเอกสารใหม่** | — | picker | ☐ |
| 2 | SELECT `เอกสารซื้อ (PO / AP Invoice)` → **นำไปใช้กับ** | — | แสดงกลุ่ม **VAT ที่ใช้ได้** (VAT ซื้อ/ทั้งคู่) + กลุ่ม **WHT ที่แนะนำ** | ☐ |
| 3 | VERIFY แถว WHT ในกลุ่มที่แนะนำ | — | แต่ละแถว WHT แสดง pill **แนะนำ · ยืนยันตอนจ่าย** (ไม่มีปุ่ม เลือกและบันทึกค่า) — block final snapshot (VR13/LOCK-06) | ☐ |
| 4 | CLICK ปุ่ม **เลือกและบันทึกค่า** ที่แถว VAT ซื้อ | — | snapshot VAT ซื้อถูก capture (toast success) | ☐ |

#### TC-PK05 — บริบทใบสำคัญจ่าย: WHT ยืนยันตอนจ่าย [LOCK-06]
- group: Picker · ความสำคัญ: สูง · trace: XT-03 / BR-TAX-12 / LOCK-06
- actor: Consumer · Setup: role=demo · seed=preset (WHT active) · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → เปิด picker → บริบท ใบสำคัญจ่าย
- ผ่านเมื่อ: WHT เลือก+บันทึกได้ในบริบท payment

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **ดูรายการที่เลือกได้ในเอกสารใหม่** → SELECT `ใบสำคัญจ่าย (ยืนยัน WHT)` → **นำไปใช้กับ** | — | แสดงกลุ่ม **WHT ที่ยืนยันตอนจ่าย** (ไม่มีกลุ่ม VAT) | ☐ |
| 2 | CLICK ปุ่ม **เลือกและบันทึกค่า** ที่แถว WHT | — | toast **เลือกและบันทึก snapshot ในเอกสารแล้ว**; snapshot card WHT ปรากฏ (จุดยืนยันหักที่ payment) | ☐ |

#### TC-PK06 — snapshot คงที่หลัง master เปลี่ยน (XT-04) (ต้อง simulate)
- group: Picker · ความสำคัญ: สูง · trace: XT-04 / EC-19 / BR-TAX-08 / R08 · **(ต้อง simulate — mock consumer)**
- actor: Consumer · Setup: role=demo · seed=snapshot ที่ capture ไว้แล้ว (จาก TC-PK03) + mock consumer doc · files=—
- Start: (contract test) mock consumer ถือ snapshot
- note: downstream VAT Return (ภ.พ.30) = External Contract ยังไม่ implement → **contract test** ต่อ snapshot payload; multi-rate per line (E19) รองรับใน snapshot
- ผ่านเมื่อ: snapshot ไม่เปลี่ยนแม้แก้ master

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (mock) VERIFY+จดค่า snapshot ที่ capture (code/rate/vat_report_category) | — | จดค่าไว้อ้าง step ท้าย | ☐ |
| 2 | (simulate) แก้ master rate/vat_report_category ของรหัสเดิม | — | master เปลี่ยน | ☐ |
| 3 | VERIFY snapshot ใน consumer doc อีกครั้ง | — | ค่า snapshot = ค่าที่จดใน step 1 (ไม่เปลี่ยนตาม master — immutable, R08) | ☐ |

---

### Group I — Permissions / SoD

#### TC-P01 — Maker กด activate ถูกบล็อก (SoD) (AC-03/EC-16) (ต้อง simulate)
- group: Permission · ความสำคัญ: สูง · trace: AC-03 / EC-16 / VR12 / ERR_INSUFFICIENT_ROLE (403) / LOCK-10 · **(ต้อง simulate)**
- actor: Maker (ไม่มี activate) · Setup: role=maker · **inject:** แก้ `CURRENT_PERMISSIONS` (L2067-2070) ลบ `'tax_code.activate'` แล้ว reload · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` (หลัง inject) → CLICK **สร้างรหัสภาษี**
- note: OQ-3 — ยังไม่ยืนยัน second-person approval จริง vs single-role admin; ใช้ SoD Maker≠Approver ไปก่อน
- ผ่านเมื่อ: กด ยืนยันสร้าง → toast ไม่มีสิทธิ์; อนุญาตเฉพาะ บันทึกร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` (ไม่มี activate) → CLICK **สร้างรหัสภาษี** | — | form drawer | ☐ |
| 2 | กรอกครบ (ชุด A) → CLICK ปุ่ม **ยืนยันสร้าง** | A | toast (warning) **คุณไม่มีสิทธิ์สร้างหรือเปิดใช้รหัสภาษี** (VR12); ไม่ activate (server 403) | ☐ |
| 3 | CLICK ปุ่ม **บันทึกร่าง** | — | บันทึกได้ + toast **บันทึกร่างแล้ว** (Maker ทำ draft ได้) | ☐ |

#### TC-P02 — Viewer ไม่มีสิทธิ์ create → ปุ่มสร้างหาย (ต้อง simulate)
- group: Permission · ความสำคัญ: กลาง · trace: LOCK-10 / permission matrix (create deny) · **(ต้อง simulate)**
- actor: Viewer · Setup: role=viewer · **inject:** ลบ `'tax_code.create'` จาก `CURRENT_PERMISSIONS` แล้ว reload · files=—
- Start: OPEN `#/accounting/setup/tax-codes` (หลัง inject)
- ผ่านเมื่อ: ไม่เห็นปุ่ม สร้างรหัสภาษี

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` (ไม่มี create) → VERIFY header actions | — | **ไม่เห็น** ปุ่ม **สร้างรหัสภาษี** (primary); ยังเห็นปุ่ม **ดูรายการที่เลือกได้ในเอกสารใหม่** | ☐ |

#### TC-P03 — ไม่มี deactivate → ไม่เห็นปุ่มปิดใช้งาน (ต้อง simulate)
- group: Permission · ความสำคัญ: กลาง · trace: LOCK-10 / permission matrix (deactivate deny) · **(ต้อง simulate)**
- actor: Maker · Setup: role=maker · **inject:** ลบ `'tax_code.deactivate'` จาก `CURRENT_PERMISSIONS` แล้ว reload · seed=`VAT7` active · files=—
- Start: OPEN `#/accounting/setup/tax-codes` (หลัง inject)
- ผ่านเมื่อ: ท้ายแถว active ไม่มีไอคอนปิดใช้งาน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` (ไม่มี deactivate) → VERIFY action ท้ายแถว `VAT7` | — | **ไม่เห็น** ไอคอน **ปิดใช้งาน** (power) | ☐ |
| 2 | CLICK แถว `VAT7` → VERIFY ปุ่มใน view drawer | — | ไม่มีปุ่ม **ปิดใช้งาน** (มีแค่ แก้ไข / ปิด) | ☐ |

#### TC-P04 — Approver activate ได้ (allow)
- group: Permission · ความสำคัญ: สูง · trace: LOCK-10 / permission matrix (Approver activate allow)
- actor: Approver · Setup: role=demo(ครบสิทธิ์ = default) · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: activate สำเร็จ (คู่ allow ของ TC-P01)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** → กรอกครบ (ชุด A) → CLICK **ยืนยันสร้าง** | A | บันทึก active + toast **สร้างรหัสภาษีสำเร็จ** (ไม่มี toast ไม่มีสิทธิ์) | ☐ |

#### TC-P05 — Maker บันทึกร่างได้ (allow)
- group: Permission · ความสำคัญ: กลาง · trace: permission matrix (Maker create/saveDraft allow)
- actor: Maker · Setup: role=demo · seed=— · files=—
- Start: OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี**
- ผ่านเมื่อ: บันทึกร่างสำเร็จ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **สร้างรหัสภาษี** → TYPE รหัส+ชื่อ → CLICK **บันทึกร่าง** | — | toast **บันทึกร่างแล้ว**; แถว draft ปรากฏ | ☐ |

---

### Group J — XT cross-module / LOCK / concurrency / idempotency

#### TC-X01 — deactivate VAT ขาย → เอกสารเดิม snapshot ต่อ / ใหม่เลือกไม่ได้ (XT-01) (ต้อง simulate)
- group: XT · ความสำคัญ: สูง · trace: XT-01 / EC-01 / ENG-01/02 · **(ต้อง simulate — mock SO/AR consumer)**
- actor: Approver + Consumer · Setup: role=demo · seed=`VAT7` active + mock เอกสารขายเก่าที่ถือ snapshot VAT7 · files=—
- note: downstream SO/AR Invoice = External Contract ยังไม่ implement → contract test
- ผ่านเมื่อ: หลัง deactivate เอกสารเดิมยังใช้ snapshot; docDate หลัง eff_end เลือกไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK **ดูรายการที่เลือกได้ในเอกสารใหม่** → VERIFY+จด `VAT7` pickable วันนี้ | — | จดว่า VAT7 อยู่ในรายการ | ☐ |
| 2 | ปิด picker → CLICK ไอคอน **ปิดใช้งาน** ท้ายแถว `VAT7` → CLICK **ปิดใช้งาน** | — | toast **ปิดใช้งานรหัสภาษีแล้ว**; eff_end = วันนี้ | ☐ |
| 3 | เปิด picker → VERIFY (docDate = พรุ่งนี้) | (พรุ่งนี้) | `VAT7` **ไม่โผล่** ในรายการ pickable (ENG-02) | ☐ |
| 4 | (mock consumer) VERIFY เอกสารขายเก่าที่ถือ snapshot | — | ยังแสดง VAT7 · อัตรา 7% (snapshot immutable — ใช้อ้างอิงได้ต่อ, EC-01) | ☐ |

#### TC-X03 — ยืนยัน WHT ตอนจ่าย (XT-03) (ต้อง simulate)
- group: XT · ความสำคัญ: สูง · trace: XT-03 / BR-TAX-12 / LOCK-06 · **(ต้อง simulate — mock Payment Voucher)**
- actor: Consumer · Setup: role=demo · seed=mock AP invoice ที่มี WHT advisory + Payment Voucher context · files=—
- note: Payment Voucher = External Contract; report อ่านจาก payment result ไม่ใช่ AP suggestion
- ผ่านเมื่อ: WHT final resolve ที่ payment context

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → เปิด picker → SELECT `เอกสารซื้อ (PO / AP Invoice)` → VERIFY WHT | — | WHT = pill **แนะนำ · ยืนยันตอนจ่าย** (advisory, ยังไม่ final) | ☐ |
| 2 | SELECT `ใบสำคัญจ่าย (ยืนยัน WHT)` → CLICK **เลือกและบันทึกค่า** ที่แถว WHT | — | snapshot WHT ถูก capture ที่ payment context (จุดยืนยันหัก) | ☐ |
| 3 | (mock report) VERIFY WHT report source | — | report อ่านค่าจาก payment result (ไม่ใช่ AP advisory) — LOCK-06 | ☐ |

#### TC-X05 — WHT report resolve income category (XT-05) (ต้อง simulate)
- group: XT · ความสำคัญ: กลาง · trace: XT-05 / BR-TAX-11 / LOCK-05 · **(ต้อง simulate — mock ภ.ง.ด.3/53)**
- actor: Consumer · Setup: role=demo · seed=WHT snapshot ที่มี income_category + payment result · files=—
- note: ภ.ง.ด.3/53 = External Contract; income category + WHT final อ่านจาก payment result
- ผ่านเมื่อ: report contract map income_category ถูกต้อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → CLICK tab WHT → CLICK แถว `WHT3` → VERIFY | — | ประเภทเงินได้ `ค่าบริการ / รับจ้างทำของ` · กติกาแบบรายงาน **เลือกจากผู้รับเงินและบริบทการจ่าย** | ☐ |
| 2 | (mock report) VERIFY payload contract | — | report ภ.ง.ด.3/53 ได้ income_category + WHT final จาก payment result (RESOLVE_BY_PAYEE_AND_PAYMENT_CONTEXT) | ☐ |

#### TC-XC01 — เข้าถึงรหัสข้ามบริษัทถูกบล็อก (EC-18) (ต้อง simulate)
- group: XT/Security · ความสำคัญ: สูง · trace: EC-18 / BR-TAX-15 / LOCK-02 / D17 / ERR_NOT_FOUND(404) หรือ 403 · **(ต้อง simulate — mock cross-company)**
- actor: user COMP-001 · Setup: role=demo · seed=รหัสของ COMP-002 (id ต่างบริษัท) · **inject:** เรียก detail ด้วย id ของบริษัทอื่น · files=—
- ผ่านเมื่อ: server block (RLS) — ไม่เห็นข้อมูลบริษัทอื่น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → VERIFY footer | — | บริษัท = `บริษัท 2BSimple จำกัด` (COMP-001) เท่านั้น; รายการทั้งหมดของ COMP-001 | ☐ |
| 2 | (contract) เรียก F-TAX-API-02 GET /tax-codes/:id ด้วย id ของ COMP-002 | — | ตอบ **404 ERR_NOT_FOUND** (หรือ 403) — RLS ตัด cross-company (E18/D17) | ☐ |

#### TC-CC01 — สร้างรหัสเดียวกันพร้อมกัน → คนที่ 2 ได้ duplicate (EC-14) (ต้อง simulate)
- group: Concurrency · ความสำคัญ: กลาง · trace: EC-14 / BR-TAX-01 / BR_TAX_CODE_DUPLICATE (422)/ UQ DB · **(ต้อง simulate — 2 requests race)**
- actor: 2 Makers · Setup: role=demo · seed=— · **inject:** ยิง POST /tax-codes code เดียวกัน 2 ครั้งพร้อมกัน · files=—
- ผ่านเมื่อ: DB UQ ทำให้ตัวที่ 2 fail

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (contract) POST /tax-codes {code:`RACE1`} ×2 พร้อมกัน | — | request แรก 201 created; request ที่ 2 = **422 BR_TAX_CODE_DUPLICATE** (UQ `(company_id, lower(code))` ระดับ DB — ไม่พึ่ง client) | ☐ |

#### TC-CC02 — แก้/ปิดใช้งานรหัสเดียวกันพร้อมกัน → 409 (EC-15) `[AI-DEFAULT]` (ต้อง simulate)
- group: Concurrency · ความสำคัญ: กลาง · trace: EC-15 / OQ-9 / ERR_STALE_DATA (409) / LD-01 · **`[AI-DEFAULT]`** · **(ต้อง simulate)**
- actor: 2 Approvers · Setup: role=demo · seed=`VAT7` version=v1 · **inject:** 2 PUT ด้วย If-Match/version เดียวกัน · files=—
- note: **`[AI-DEFAULT]`** optimistic lock (`If-Match`/`version`) → 409 — **OQ-9** (ยังไม่ยืนยัน contract)
- ผ่านเมื่อ: ตัวที่ 2 ได้ 409 stale

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (contract) VERIFY+จด version ปัจจุบันของ `VAT7` | — | จด version=v1 | ☐ |
| 2 | (contract) PUT #1 (If-Match: v1) สำเร็จ → PUT #2 (If-Match: v1) | — | PUT #1 = 200 (version→v2); PUT #2 = **409 ERR_STALE_DATA** (version mismatch) | ☐ |

#### TC-ID01 — Idempotency-Key ซ้ำ body ต่าง → 409 (OQ-8) `[AI-DEFAULT]` (ต้อง simulate)
- group: Idempotency · ความสำคัญ: กลาง · trace: OQ-8 / PR-7 / ERR_DUPLICATE_IDEMPOTENCY_KEY (409) / LD-03 · **`[AI-DEFAULT]`** · **(ต้อง simulate)**
- actor: Maker · Setup: role=demo · seed=— · **inject:** POST 2 ครั้ง Idempotency-Key เดียวกัน body ต่าง · files=—
- note: **`[AI-DEFAULT]`** Idempotency-Key required ทุก mutation, TTL 24h — **OQ-8** (ยังไม่ยืนยันนโยบาย/TTL)
- ผ่านเมื่อ: key ซ้ำ + body ต่าง → 409

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (contract) POST /tax-codes (Idempotency-Key: K1, body A) | — | 201 created | ☐ |
| 2 | (contract) POST /tax-codes (Idempotency-Key: K1, body B ต่างจาก A) | — | **409 ERR_DUPLICATE_IDEMPOTENCY_KEY** | ☐ |

#### TC-EC08 — GL ที่ผูกไว้ถูก deactivate ใน CoA ภายหลัง (OQ-6 BLOCKING) (ต้อง simulate)
- group: Edge · ความสำคัญ: สูง · trace: EC-08 / OQ-6 / BR-TAX-06 · **(ต้อง simulate)** · **behavior ยังไม่ตัดสิน**
- actor: Accountant · Setup: role=demo · seed=รหัส active ที่ผูก GL `2131-01` + inject GL นั้นเป็น inactive ใน CoA · files=—
- note: **OQ-6 (BLOCKING)** — ยังไม่ตัดสินว่า block posting / warn / re-bind. ENG-03 ตรวจ ณ activate เท่านั้น; ห้าม assume cascade. เคสนี้บันทึกพฤติกรรมที่สังเกตได้เพื่อรอ decision
- ผ่านเมื่อ: บันทึกพฤติกรรมจริง (ยังไม่มี expected ตายตัวจนกว่า OQ-6 resolve)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) ตั้ง GL `2131-01` เป็น inactive/posting=false ใน CoA | — | GL ถูก deactivate | ☐ |
| 2 | OPEN `#/accounting/setup/tax-codes` → CLICK แถวที่ผูก GL นั้น → CLICK **แก้ไข** → CLICK **บันทึกการแก้ไข** | — | ระบบตรวจ GL role ณ activate → คาด block ด้วย **ต้องเลือกบัญชี GL...ก่อนเปิดใช้งาน** (GL ไม่ผ่าน filter อีกต่อไป). **บันทึกผลจริงไว้ — OQ-6 ยังไม่ตัดสิน (BLOCKING)** | ☐ |

#### TC-EC13 — reactivate inactive → ต้อง set effEnd ใหม่ `[AI-DEFAULT]` (ต้อง simulate)
- group: Edge · ความสำคัญ: กลาง · trace: EC-13 / state inactive→active · **`[AI-DEFAULT]`** · **(ต้อง simulate — effEnd อดีต)**
- actor: Approver · Setup: role=demo · seed=`VAT10-OLD` (inactive, eff_end 1999-03-31 อดีต) · files=—
- note: **`[AI-DEFAULT]`** บังคับ set eff_end ≥ today ก่อน reactivate (conservative default)
- ผ่านเมื่อ: เปิดใช้งานใหม่ผ่านหน้าแก้ไขต้องกำหนดวันมีผลใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → SELECT `ปิดใช้งาน` → CLICK แถว `VAT10-OLD` → CLICK **แก้ไข** | — | form drawer edit; eff_end เดิม = 1999-03-31 (อดีต) | ☐ |
| 2 | CLICK **บันทึกการแก้ไข** (ยังไม่แก้ eff_end / effEnd อดีต) | — | คาดถูก block/เตือนให้ตั้งวันมีผลใหม่ (`[AI-DEFAULT]` set eff_end ≥ today); บันทึกผลจริง | ☐ |
| 3 | TYPE `2027-12-31` → **วันมีผลสิ้นสุด** + วันมีผลเริ่มปัจจุบัน → CLICK **บันทึกการแก้ไข** | — | reactivate สำเร็จ (status active) + toast **บันทึกการแก้ไขแล้ว** | ☐ |

#### TC-LK02 — company context chip read-only (LOCK-02)
- group: LOCK · ความสำคัญ: กลาง · trace: LOCK-02 / BR-TAX-15 / R15
- actor: Accountant · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: chip บริษัทปัจจุบันแสดงแบบ read-only เปลี่ยนในฟอร์มไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` → VERIFY แถบ context บริษัท | — | chip **บริษัทปัจจุบัน · 2BSimple จำกัด** (read-only) | ☐ |
| 2 | CLICK **สร้างรหัสภาษี** → VERIFY ในฟอร์ม | — | ฟอร์มไม่มีช่องเลือก/เปลี่ยนบริษัท (current-company context, LOCK-02) | ☐ |

#### TC-LK11 — route จริง refresh-safe (LOCK-11)
- group: LOCK · ความสำคัญ: กลาง · trace: LOCK-11 / route
- actor: Accountant · Setup: role=demo · seed=preset · files=—
- Start: OPEN `#/accounting/setup/tax-codes`
- ผ่านเมื่อ: route hash ตรง + refresh แล้วยังอยู่หน้าเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/accounting/setup/tax-codes` | — | URL hash = `#/accounting/setup/tax-codes`; sidebar item **รหัสภาษี** active; breadcrumb `ตั้งค่าบัญชี > รหัสภาษี` | ☐ |
| 2 | OPEN `#/accounting/setup/tax-codes` (reload) | — | ยังอยู่หน้ารายการรหัสภาษี (refresh-safe) | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิดไฟล์ `outputs/10_Tax-Code/01_HTML/TaxCode.html` ใน browser (prototype vanilla SPA).
2. ทุกเคสเริ่มที่ `Start` route ของตัวเอง (`OPEN #/accounting/setup/tax-codes`) — refresh ก่อนเริ่มเคสใหม่เพื่อล้างสถานะค้าง (records ถูก re-seed ทุก reload).
3. ทำ step ตามลำดับ; ทุก Action ขึ้นต้นด้วย verb tag (OPEN/CLICK/TYPE/SELECT/TOGGLE/UPLOAD/PRESS/WAIT/VERIFY). ผูกกับ **ข้อความบนจอ** ในเครื่องหมาย ** **.
4. ติ๊ก Result `☐`→`☑` ต่อ step; เคสผ่าน = ทุก step ผ่าน.
5. เคส `(ต้อง simulate)` = runner ต้อง inject ตาม `Setup:` (แก้ `CURRENT_PERMISSIONS` L2067-2070 / `CURRENT_COMPANY` L2066 / mock consumer / contract API) — ถ้าทำไม่ได้ mark `blocked`.
6. Expected แบบ delta (จด+เทียบ) ต้องทำ step VERIFY บันทึกค่าตั้งต้นก่อนเสมอ.
7. กรอกผลกลับตาม schema ด้านล่าง.

---

## Coverage Audit

| หมวด | covered / total |
|---|---|
| Acceptance Criteria (AC-01..12, รวม 02b/05b) | 14 / 14 |
| Business Rules (BR-TAX-01..17) | 17 / 17 |
| Field Validation (VR01..13) | 13 / 13 |
| Edge Cases (EC-01..19) | 15 / 19 (ข้าม 4 พร้อมเหตุผล) |
| Error codes | 11 / 12 (ข้าม ENG_ERR_INVALID_INPUT — internal) |
| Permission cells (สำคัญ) | 10 / 10 |
| Cross-Module (XT-01..05) | 5 / 5 |
| Scope Lock (LOCK-01..12) | 12 / 12 |
| States / Cross-cutting | empty(sim)/filtered-empty/pills/submitting/audit/RLS/draft-no-expiry ครบ; loading skeleton ข้าม |

- Cross-Module (XT): **5 / 5** (ทั้งหมด contract/simulate — downstream = External Contract)
- Scope Lock (LOCK): **12 / 12** (ทุกข้อมีเคส verify)
- **Manifest cross-check (FRD §0.12): ✅ 46/46** — Stories 10/10 (S-01..10 map ครบผ่าน AC cases), Rules 17/17 (R01..17), Edges 19/19 (E01..19 — covered หรือ ข้ามพร้อมเหตุผล). ทุกแถว manifest มีคู่ใน Ledger.
- **[AI-DEFAULT] cases:** 5 เคส — TC-D04 (OQ-10), TC-CC02 (OQ-9), TC-ID01 (OQ-8), TC-EC13 (EC-13 default), และ note OQ ใน TC-C02 (OQ-7), TC-P01 (OQ-3), TC-EC08 (OQ-6 BLOCKING).
- **⚠ ยืนยัน anchor:** 0 (ทุก anchor verbatim จาก HTML/01_UI/microcopy v7).

### ข้าม (พร้อมเหตุผล)
- **EC-07 foreign tax** — Out of Scope (ไทย/THB เท่านั้น); ไม่มี selector บนจอ → verify เชิงลบใน TC-C01 step 6 (ไม่มีช่องประเทศ).
- **EC-09 GL taxRole moved** — หลังบ้าน/verify ที่ next activate = OQ-6 scope; ไม่มีผลสังเกตได้บน prototype.
- **EC-10 income type removed** — historical snapshot code (derive แล้ว); ไม่มีหน้าจอ prototype.
- **ENG_ERR_INVALID_INPUT (500)** — engine schema mismatch = internal; ไม่มี trigger บน UI.
- **Loading skeleton** — prototype render records ทันที (ไม่มี async list fetch ที่จับ skeleton ได้).
- **OQ-6 (EC-08 TC-EC08)** — เขียนเป็นเคส แต่ behavior **ยังไม่ตัดสิน (BLOCKING)**: block posting / warn / re-bind ต้องรอ decision (Accounting + CoA owner ก่อน dev validation).
- **นอกขอบเขตใบเซ็น (Exclusions — ห้ามสร้างเคส):** Default Tax Code รายชนิดเอกสาร, Incoming WHT, RD e-filing, PDF generation, multi-jurisdiction, หน้ารายงาน ภ.พ.30/ภ.ง.ด.3/53 (downstream External Contract — เฉพาะ contract test ผ่าน XT).

---

## Result Report (schema)

```json
{
  "feature_id": "F-TAX",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 76, "pass": 0, "fail": 0, "blocked": 0 }
}
```
> `evidence` = สิ่งที่ agent **เห็นจริง** ตอน fail/blocked (ข้อความ error จริง / route ที่ค้าง / สิ่งที่แสดงแทน Expected). เคส `(ต้อง simulate)` ที่ inject ไม่ได้ → `status: blocked` + `note` ระบุว่าติด inject อะไร.

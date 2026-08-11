# AI Test Cases — F-TAX ทะเบียนรหัสภาษี (Tax Code Master)

เอกสารนี้เป็นชุด Test Case สำหรับ **AI agent (browser-use / vision)** อ่านแล้วลงมือทดสอบบนหน้าจอจริงของ prototype `f-taxcode.html` (SPA route เดียว `#/tax-codes`, overlay = drawer/modal). ทุก action ขึ้นต้น verb tag; ทุก Expected เช็คได้ด้วยตาจากข้อความ/ป้ายที่ปรากฏ. **ข้อความบนจอทั้งหมดเป็น verbatim จาก HTML ต้นทาง** (source of truth) — ห้าม paraphrase.

> **หมายเหตุ prototype (สำคัญต่อ runner):**
> 1. overlay ทุกตัว (create/edit/view/import/delete) เปิดด้วยฟังก์ชัน JS ไม่ใช่ hash route → **ไม่ refresh-safe**. ทุกเคสเริ่มที่ `#/tax-codes` แล้วคลิกเปิด overlay เอง.
> 2. การนำเข้า CSV เป็น mock: `bulkPick()` **ไม่อ่านเนื้อไฟล์จริง** — ใช้ `BULK_SAMPLE` (5 แถวคงที่) เสมอไม่ว่าเลือกไฟล์อะไร. เคสที่ต้อง trigger error code นอกเหนือจาก 2 ตัวใน sample ต้อง **patch `BULK_SAMPLE`** จึง mark `(ต้อง simulate)`.
> 3. `used_count` เป็น mock (OQ-TAX-04) — guard/skip พึ่งตัวเลข seed.
> 4. ไม่มี backend → เคส server-guard (IR-TAX-01 bypass) และ cross-module ต้อง simulate ตามที่ระบุใน `Setup:`.

---

## Meta

| Field | Value |
|---|---|
| Feature ID | F-TAX |
| Feature Name | ทะเบียนรหัสภาษี (Tax Code Master) |
| Pack version | FRD v1.0 (2026-08-10, STANDARD) + BRD APPROVED + HTML as-built (html-generator-v8) |
| App entry / Route | `#/tax-codes` (single hash route; overlay drawer/modal ไม่มี route แยก) |
| ที่มา (source) | FRD_F-TAX_Pack (00/01/02/03/04/05/06) · BRD_F-TAX_Tax-Code.md · UI_BRIEF_F-TAX · **`f-taxcode.html` (SoT, verbatim anchor)** |
| Microcopy source | HTML ต้นทาง (verbatim จอชนะ) → 01_UI → html-generator-v8/microcopy.md |
| Role (prototype) | `tax_admin` (mock user เดียวเปิดหมด — RBAC จริง deferred OQ-TAX-06 `[AI-DEFAULT]`) |
| จำนวนเคส | 72 (TC-L01..14 · TC-C01..10 · TC-E01..06 · TC-V01..06 · TC-B01..06 · TC-D01..04 · TC-I01..14 · TC-X01 · TC-K01..05 · TC-XT01..04 · TC-P01 · TC-CC01) |
| หมวด | happy 20 · negative 12 · edge 10 · error 18 · permission 3 · absence/lock 9 |

---

## Coverage

| Group | เคส | จำนวน | ความสำคัญ |
|---|---|---|---|
| G1 List / filter / sort / pager (P-01) | TC-L01..L14 | 14 | สูง |
| G2 สร้างรหัสภาษี (P-02) | TC-C01..C10 | 10 | สูง |
| G3 แก้ไข + IR-TAX-01 guard (P-03) | TC-E01..E06 | 6 | **สูงสุด (TC-E04 = P0)** |
| G4 ดูรายละเอียด + เปลี่ยนสถานะ (P-04) | TC-V01..V06 | 6 | กลาง |
| G5 Bulk เปลี่ยนสถานะ | TC-B01..B06 | 6 | กลาง |
| G6 Bulk delete (P-06) | TC-D01..D04 | 4 | สูง |
| G7 นำเข้า CSV 3-step + 6 error codes (P-05) | TC-I01..I14 | 14 | สูง |
| G8 ส่งออก CSV | TC-X01 | 1 | กลาง |
| G9 LOCK absence | TC-K01..K05 | 5 | กลาง |
| G10 Cross-Module (XT) | TC-XT01..XT04 | 4 | กลาง |
| G11 Permission / Concurrency | TC-P01, TC-CC01 | 2 | กลาง |

---

## Coverage Ledger

### FR / Acceptance (06_TESTS §6.1–§6.2)
| item | cases |
|---|---|
| AC-01 สร้าง happy + auto-code (TC-01) | TC-C01, TC-C04 |
| AC-02 auto-code ตามประเภทไม่ชน (TC-01) | TC-C01, TC-C02 |
| AC-03 exempt → rate ล็อก 0 (TC-02) | TC-C03 |
| AC-04 แก้ used=0 ทุก field (TC-03) | TC-E01 |
| AC-05 แก้ used>0 ล็อก 3 field (TC-04) | TC-E02, TC-E05 |
| AC-06 IR-TAX-01 server guard (TC-05, **P0**) | **TC-E04** |
| AC-07 เปลี่ยนสถานะอิสระ (TC-06) | TC-V04, TC-V05, TC-V06 |
| AC-08 bulk เปลี่ยนสถานะ (TC-06) | TC-B02, TC-B03, TC-B04 |
| AC-09 bulk delete confirm (TC-07) | TC-D01, TC-D03 |
| AC-10 bulk delete ผสม used>0/=0 (TC-07) | TC-D02 |
| AC-11 รหัสซ้ำ case-insensitive (TC-08) | TC-C07, TC-E06 |
| AC-12 อัตราผิด (TC-09) | TC-C06 |
| AC-13 import จอแรก (TC-10) | TC-I01, TC-I02 |
| AC-14 import preview + status ว่าง=ร่าง (TC-10) | TC-I04, TC-I05 |
| AC-15 import ทศนิยม ผ่าน (TC-10) | TC-I06 |
| AC-16 import 6 error codes (TC-11) | TC-I07..I12, TC-I13 |
| AC-17 export CSV BOM 7 cols (TC-12) | TC-X01 |
| AC-18 view tabs usage/history (TC-13) | TC-V01, TC-V02, TC-V03 |
| AC-19 LOCK absence (TC-14) | TC-K01..K05 |

### Business Rules (05_RULES §5.1)
| rule | cases |
|---|---|
| BR-01 รหัสห้ามซ้ำ case-insensitive | TC-C07, TC-E06, TC-I07, TC-CC01 |
| BR-02 อัตรา 0–100 ทศนิยม `[AI-DEFAULT ← EC-A5 precision 2]` | TC-C06, TC-I06, TC-I08 |
| BR-03 exempt → rate 0 `[LOCK-EXEMPT-0]` | TC-C03, TC-I11 |
| BR-04 IR-TAX-01 lock-on-use `[LOCK-IR-TAX-01]` | TC-E02, TC-E04, TC-E05, TC-XT03 |
| BR-05 used>0 ลบไม่ได้ (bulk skip) `[LOCK-BULK-DEL]` | TC-D02, TC-K01 |
| BR-06 สถานะเปลี่ยนอิสระ `[LOCK-STATUS-FREE]` | TC-V04, TC-V05, TC-V06, TC-B02..B04 |
| BR-07 ปลายทางเลือกเฉพาะ active `[LOCK-SOFT-REF]` | TC-XT01 |
| BR-08 import รายแถว/status ว่าง=ร่าง | TC-I04, TC-I05, TC-I13 |
| BR-09 ไม่เก็บ GL `[LOCK-NO-GL]` | TC-K02, TC-XT04 |
| BR-10 audit who/when | TC-V03 |

### Field Validation (05_RULES §5.4)
| VR | cases |
|---|---|
| VR-01 name_th ว่าง | TC-C05 |
| VR-02 code ซ้ำ case-insensitive | TC-C07, TC-E06 |
| VR-03 rate ว่าง/NaN/<0/>100 | TC-C06 |
| VR-04 exempt trigger rate 0 + tag | TC-C03 |
| VR-05 double-submit loader | TC-C08 |
| VR-06..11 import 6 กรณี | TC-I05..I12 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 รหัสซ้ำต่างตัวพิมพ์ | TC-C07 |
| EC-02 rate=120 (import) | TC-I08 |
| EC-03 exempt+rate≠0 (import) | TC-I11 |
| EC-04 rate ทศนิยม 0.75 | TC-I06 |
| EC-05 import status ว่าง=draft | TC-I05 |
| EC-06 bulk ลบผสม used>0/=0 | TC-D02 |
| EC-07 ฝืน submit used>0 (guard) | TC-E04 |
| EC-08 นำเข้าไฟล์ที่ไม่ได้เลือก | TC-I02 |
| EC-A3 concurrent create same code | TC-CC01 (ต้อง simulate — DB unique 409) |
| EC-A5 rate ทศนิยมยาว precision 2 | TC-I06 (note precision `[AI-DEFAULT]`) |
| EC-A7 ลบตัวปลายทางอ้างจริงแต่ used mock=0 | — ข้าม (OQ-TAX-04 backend sync; ตรวจบน UI prototype ไม่ได้) |

### Import Error Catalog (05_RULES §5.6 — 6 codes verbatim)
| code | cases |
|---|---|
| REQUIRED "ข้อมูลบังคับไม่ครบ (REQUIRED)" | TC-I09 (ต้อง simulate) |
| BAD_TYPE "ประเภทไม่ถูกต้อง (BAD_TYPE)" | TC-I10 (ต้อง simulate) |
| RATE_INVALID "อัตราไม่ถูกต้อง 0–100 (RATE_INVALID)" | TC-I08 |
| EXEMPT_RATE "ยกเว้นภาษีต้องอัตรา 0 (EXEMPT_RATE)" | TC-I11 (ต้อง simulate) |
| BAD_STATUS "สถานะไม่ถูกต้อง (BAD_STATUS — ใช้ ใช้งาน/ไม่ใช้งาน/ร่าง)" | TC-I12 (ต้อง simulate) |
| CODE_DUPLICATE "รหัสซ้ำ (CODE_DUPLICATE)" | TC-I07 |

### API Error Catalog (05_RULES §5.6 — production)
| code | cases / สถานะ |
|---|---|
| ERR_CODE_DUPLICATE 409 | TC-C07 (form msg), TC-CC01 (concurrent) |
| ERR_VALIDATION_FAILED 400 | TC-C05, TC-C06 |
| BR_EXEMPT_RATE 422 | TC-C03 (UI ล็อก) / TC-I11 (import) |
| ERR_INVALID_STATUS 400 | TC-I12 (import BAD_STATUS) |
| ERR_NOT_AUTHENTICATED 401 / ERR_INSUFFICIENT_ROLE 403 | — ข้าม (deferred OQ-TAX-06, mock เปิดหมด — TC-P01 note) |
| ERR_STALE_DATA 409 / ERR_DUPLICATE_IDEMPOTENCY_KEY 409 | — ข้าม (optimistic lock/idempotency `[AI-DEFAULT]` backend-only, ไม่มีผลบน UI prototype) |
| ERR_NOT_FOUND 404 | — ข้าม (backend-only) |

### Permission Matrix (05_RULES §5.3)
| cell | cases |
|---|---|
| tax_admin ทำได้ทุก action (create/edit/status/import/export/bulk-del) | TC-P01 (+ ครอบทุก G ที่ทำ action สำเร็จ) |
| consumer เห็นเฉพาะ active ผ่าน lookup (read-only, ไม่มีปุ่มจัดการ) | TC-XT01 |
| role-gate จริงต่อ action `[AI-DEFAULT ← OQ-TAX-06]` | — ข้าม (deferred, mock เปิดหมด — TC-P01 note) |

### State Machine (05_RULES §5.2 — free 3-value)
| transition | cases |
|---|---|
| current disabled ในเมนู + mark "ปัจจุบัน" | TC-V04 |
| active→inactive (single) | TC-V05 |
| draft→inactive / inactive→active (ทุกทิศ ไม่มี gate) | TC-V06 |
| bulk → active/draft/inactive | TC-B02, TC-B03, TC-B04 |
| default create=active · import ว่าง=draft | TC-C09, TC-I05 |

### Scope Lock (00 §0.11 — LOCK ทุกข้อต้องมีเคส verify)
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LOCK-IR-TAX-01 | used>0 ล็อกรหัส/อัตรา/ประเภท (UI+server) | TC-E02, **TC-E04** |
| LOCK-EXEMPT-0 | exempt → rate 0 เสมอ | TC-C03, TC-I11 |
| LOCK-TYPE-3 | ประเภท fix 3 ค่า | TC-C03 (select มี 3 ตัวเลือกเท่านั้น), TC-K (form) |
| LOCK-NO-GL | ไม่มี field/endpoint GL | TC-K02, TC-XT04 |
| LOCK-DOA-NULL | ไม่มีสายอนุมัติ (approver=null) | TC-K03 |
| LOCK-NO-NOTIF | ไม่ emit event (กระดิ่ง placeholder) | TC-K05 |
| LOCK-STATUS-FREE | 3 ค่าเปลี่ยนอิสระ ไม่มี gate | TC-V06, TC-B02..B04 |
| LOCK-SOFT-REF | ปลายทางเก็บแค่ code · เลือกเฉพาะ active | TC-XT01, TC-XT02 |
| LOCK-BULK-DEL | ไม่มีลบเดี่ยว · bulk + used>0 ข้าม | TC-K01, TC-D02 |

### Cross-Module (06_TESTS §6.9 XT)
| XT | Downstream | Case |
|---|---|---|
| XT-01 lookup คืนเฉพาะ active | Item Master / เอกสาร | TC-XT01 (ต้อง simulate downstream) |
| XT-02 inactive ภายหลัง เอกสารเดิมคงค่า | เอกสารเดิม | TC-XT02 (ต้อง simulate) |
| XT-03 แก้ rate ตัว used>0 ถูก guard บล็อก | เอกสารซื้อ-ขาย | TC-XT03 (อ้าง TC-E04) |
| XT-04 GL Posting อ่าน code, ไม่ถือ GL | GL | TC-XT04 (ต้อง simulate) |

### Cross-cutting / States / Events
| item | cases |
|---|---|
| Empty (no data) | TC-L13 |
| Empty (filtered) | TC-L03 |
| Loading loader "กำลังบันทึก…" | TC-C08 |
| Stat cards ×4 + quick filter | TC-L01, TC-L06, TC-L07 |
| Esc chain (menu>modal>drawer) | TC-C10, TC-D04, TC-V04 |
| Export BOM + escape | TC-X01 |
| Audit trail (created/updated by+at) | TC-V03 |
| WebSocket events | — ข้าม (LOCK-NO-NOTIF, ไม่มี event — TC-K05 ยืนยัน absence) |

---

## Data Sets

### ชุดสร้าง/แก้ไข (form)
| ชุด | code | rate | name_th | name_en | category (ค่าที่เลือก) | status |
|---|---|---|---|---|---|---|
| **A** (VAT happy, เว้นรหัส) | (เว้นว่าง) | 7 | ภาษีมูลค่าเพิ่ม 7% ทดสอบ | VAT 7% Test | ภาษีมูลค่าเพิ่ม (VAT) | ใช้งาน (default) |
| **B** (WHT happy, เว้นรหัส) | (เว้นว่าง) | 3 | หัก ณ ที่จ่าย 3% ทดสอบ | WHT 3% Test | หัก ณ ที่จ่าย (WHT) | ร่าง |
| **C** (exempt) | (เว้นว่าง) | (ล็อก 0) | ยกเว้นภาษีทดสอบ | Exempt Test | ยกเว้นภาษี | ใช้งาน |
| **D** (ระบุ code เอง) | VATTEST | 5 | ภาษีทดสอบระบุรหัส | Coded Test | ภาษีมูลค่าเพิ่ม (VAT) | ใช้งาน |
| **E-dup** (รหัสซ้ำ) | vat7 | 7 | ทดสอบรหัสซ้ำ | dup | ภาษีมูลค่าเพิ่ม (VAT) | ใช้งาน |
| **E-name0** (ชื่อไทยว่าง) | (เว้นว่าง) | 7 | (เว้นว่าง) | x | ภาษีมูลค่าเพิ่ม (VAT) | ใช้งาน |
| **E-rate-neg** | (เว้นว่าง) | -1 | ทดสอบอัตราลบ | x | ภาษีมูลค่าเพิ่ม (VAT) | ใช้งาน |
| **E-rate-hi** | (เว้นว่าง) | 120 | ทดสอบอัตราเกิน | x | ภาษีมูลค่าเพิ่ม (VAT) | ใช้งาน |
| **E-rate-empty** | (เว้นว่าง) | (เว้นว่าง) | ทดสอบอัตราว่าง | x | ภาษีมูลค่าเพิ่ม (VAT) | ใช้งาน |

### Seed records (มาจาก HTML mock §8 — 10 แถว)
| id | code | name_th | rate | category | status | used |
|---|---|---|---|---|---|---|
| T-001 | VAT7 | ภาษีมูลค่าเพิ่ม 7% | 7 | vat | active | **214** (ล็อก IR-TAX-01) |
| T-002 | VAT0 | ภาษีมูลค่าเพิ่ม 0% | 0 | vat | active | 36 |
| T-003 | NONVAT | ยกเว้นภาษีมูลค่าเพิ่ม | 0 | exempt | active | 18 (ล็อก) |
| T-004 | WHT1 | หัก ณ ที่จ่าย 1% (ขนส่ง) | 1 | wht | active | 22 |
| T-005 | WHT2 | หัก ณ ที่จ่าย 2% (โฆษณา) | 2 | wht | active | 5 |
| T-006 | WHT3 | หัก ณ ที่จ่าย 3% (บริการ) | 3 | wht | active | 87 |
| T-007 | WHT5 | หัก ณ ที่จ่าย 5% (เช่า) | 5 | wht | active | 12 |
| T-008 | WHT10 | หัก ณ ที่จ่าย 10% (เงินปันผล) | 10 | wht | active | 2 |
| T-009 | WHT15 | หัก ณ ที่จ่าย 15% (ดอกเบี้ย) | 15 | wht | **inactive** | **0** |
| T-010 | VAT10 | ภาษีมูลค่าเพิ่ม 10% (เตรียมอัตราใหม่) | 10 | vat | **draft** | **0** |

> รวม 10 แถว, pageSize=8 → 2 หน้า. status: active=8, inactive=1, draft=1.

### ไฟล์ทดสอบ (Files) — สำหรับ import
| ชื่อไฟล์ | เนื้อหา (mock BULK_SAMPLE 5 แถว — คงที่ ไม่อ่านเนื้อจริง) | ใช้ในเคส |
|---|---|---|
| `taxcode_import_sample.csv` | WHT075(0.75,ใช้งาน→ผ่าน) · VAT9(9,status ว่าง→ผ่าน=ร่าง) · TAXOLD(5,ไม่ใช้งาน→ผ่าน) · VAT7(7,ซ้ำ→CODE_DUPLICATE) · WHT99(120→RATE_INVALID). **ok=3 · err=2** | TC-I02..I08, TC-I13 |
| `taxcode_import_required.csv` | (ต้อง patch `BULK_SAMPLE`) ≥1 แถวเว้น code หรือ rate ว่าง → **REQUIRED** | TC-I09 |
| `taxcode_import_badtype.csv` | (patch) ≥1 แถว category ไม่อยู่ใน 3 ชื่อไทย (เช่น "อื่นๆ") → **BAD_TYPE** | TC-I10 |
| `taxcode_import_exempt.csv` | (patch) ≥1 แถว category "ยกเว้นภาษี" + rate≠0 → **EXEMPT_RATE** | TC-I11 |
| `taxcode_import_badstatus.csv` | (patch) ≥1 แถว status ไม่ใช่ ใช้งาน/ไม่ใช้งาน/ร่าง (เช่น "pending") → **BAD_STATUS** | TC-I12 |
| `taxcode_import_allerr.csv` | (patch) ทุกแถว err → ok=0 (ปุ่มนำเข้า disabled) | TC-I14 |
| `taxcode_import_template.csv` | ไฟล์ที่ปุ่ม "ดาวน์โหลด template ตัวอย่าง" สร้าง (header `code,name_th,name_en,type,rate,status`) | TC-I03 |

---

## Test Cases

## G1 — List / Filter / Sort / Pager (P-01)

### TC-L01 — เปิดหน้ารายการ + แถบ Stats + ตาราง (happy)
- group: List · ความสำคัญ: สูง · trace: AC (P-01) / stat cards / BR-10 columns
- actor (role): tax_admin
- Setup: role=tax_admin · seed=10 records default · files=—
- Start: OPEN `#/tax-codes`
- ชุดข้อมูล: seed 10 แถว
- ผ่านเมื่อ: เห็นหัวข้อ "ทะเบียนรหัสภาษี" + count "10 รายการ" + stat 4 ใบ + ตาราง 8 แถวแรก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` | — | หัวข้อ **ทะเบียนรหัสภาษี** + ป้าย **10 รายการ** ข้างหัวข้อ | ☐ |
| 2 | VERIFY ปุ่มมุมขวาบน | — | เห็นปุ่ม **ส่งออก CSV** · **นำเข้า CSV** · **สร้างรหัสภาษี** | ☐ |
| 3 | VERIFY แถบ Stats (4 การ์ด) | — | **รหัสภาษีทั้งหมด**=10 · **ใช้งานอยู่**=8 · **ไม่ใช้งาน**=1 · **ร่าง**=1 | ☐ |
| 4 | VERIFY หัวตาราง | — | คอลัมน์: (checkbox) · **รหัส** · **ชื่อรหัสภาษี** · **อัตรา** · **ประเภท** · **ใช้ในสินค้า/เอกสาร** · **สถานะ** · **จัดการ** | ☐ |
| 5 | VERIFY แถว VAT7 | — | รหัส **VAT7** · อัตรา **7%** · type-pill **ภาษีมูลค่าเพิ่ม (VAT)** · used **214 รายการ** · pill **ใช้งาน** · ปุ่มจัดการมีเฉพาะไอคอนดินสอ (แก้ไข) | ☐ |
| 6 | VERIFY ท้ายตาราง | — | ข้อความ **แสดง 1–8 จาก 10 รายการ** + pager มี 2 หน้า | ☐ |

### TC-L02 — ค้นหาเจอ (happy)
- group: List · ความสำคัญ: กลาง · trace: filter search
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`
- ผ่านเมื่อ: พิมพ์ "WHT" กรองเหลือเฉพาะแถว WHT

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` | — | ตารางแสดง 8 แถวแรก | ☐ |
| 2 | TYPE "WHT" → ช่อง **ค้นหารหัส ชื่อ หรืออัตรา…** | WHT | ตารางเหลือเฉพาะแถวรหัสขึ้นต้น WHT (WHT1/2/3/5/10/15) | ☐ |
| 3 | VERIFY count ท้ายตาราง | — | **แสดง 1–6 จาก 6 รายการ** | ☐ |
| 4 | TYPE "7%" → ช่องค้นหา (แทนคำเดิม) | 7% | เห็นแถวที่ rate มี 7% (เช่น VAT7) — ค้นหาครอบ r@te ด้วย | ☐ |

### TC-L03 — ค้นหาไม่เจอ → filtered empty (edge)
- group: List · ความสำคัญ: กลาง · trace: State empty(filtered) EC
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`
- ผ่านเมื่อ: แสดง empty state ตัวกรอง + ปุ่ม ล้างตัวกรอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` | — | ตารางมีข้อมูล | ☐ |
| 2 | TYPE "ZZZNONE" → ช่องค้นหา | ZZZNONE | ตารางหาย แสดง empty title **ไม่พบรหัสภาษีที่ตรงกับตัวกรอง** | ☐ |
| 3 | VERIFY desc + ปุ่ม | — | desc **ลองปรับคำค้นหรือล้างตัวกรองเพื่อดูรายการทั้งหมด** + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 4 | CLICK ปุ่ม **ล้างตัวกรอง** | — | ตารางกลับมาแสดง 10 รายการ | ☐ |

### TC-L04 — กรองตามประเภท ครบทุกค่า (happy)
- group: List · ความสำคัญ: กลาง · trace: filter category (3 enum + all)
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`
- ผ่านเมื่อ: เลือกแต่ละประเภทแล้วตารางกรองถูก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` | — | ตาราง 10 แถว | ☐ |
| 2 | SELECT **ภาษีมูลค่าเพิ่ม (VAT)** → dropdown กรองตามหมวด | vat | เหลือ VAT7/VAT0/VAT10 (3 แถว) | ☐ |
| 3 | SELECT **หัก ณ ที่จ่าย (WHT)** → dropdown หมวด | wht | เหลือ 6 แถว WHT | ☐ |
| 4 | SELECT **ยกเว้นภาษี** → dropdown หมวด | exempt | เหลือ NONVAT (1 แถว) | ☐ |
| 5 | SELECT **ทุกประเภท** → dropdown หมวด | all | กลับมา 10 แถว | ☐ |

### TC-L05 — กรองตามสถานะ ครบทุกค่า (happy)
- group: List · ความสำคัญ: กลาง · trace: filter status (draft/active/inactive/all)
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` | — | ตาราง 10 แถว | ☐ |
| 2 | SELECT **ใช้งาน** → dropdown กรองตามสถานะ | active | เหลือ 8 แถว (ทุก pill = ใช้งาน) | ☐ |
| 3 | SELECT **ไม่ใช้งาน** → dropdown สถานะ | inactive | เหลือ 1 แถว (WHT15, pill ไม่ใช้งาน) | ☐ |
| 4 | SELECT **ร่าง** → dropdown สถานะ | draft | เหลือ 1 แถว (VAT10, pill ร่าง) | ☐ |
| 5 | SELECT **ทุกสถานะ** → dropdown สถานะ | all | กลับมา 10 แถว | ☐ |

### TC-L06 — Stat card quick-filter toggle (happy)
- group: List · ความสำคัญ: กลาง · trace: quickFilter
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`
- ผ่านเมื่อ: คลิกการ์ด "ใช้งานอยู่" กรอง active, คลิกซ้ำยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` | — | ตาราง 10 แถว | ☐ |
| 2 | CLICK การ์ด **ใช้งานอยู่** | — | ตารางกรองเหลือ 8 แถว active · การ์ดขึ้น state ถูกเลือก (is-on) | ☐ |
| 3 | CLICK การ์ด **ใช้งานอยู่** ซ้ำ | — | ยกเลิกกรอง กลับมา 10 แถว | ☐ |

### TC-L07 — Stat "รหัสภาษีทั้งหมด" = reset (happy)
- group: List · ความสำคัญ: ต่ำ · trace: quickFilter('all')
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` → SELECT **ร่าง** (dropdown สถานะ) | draft | เหลือ 1 แถว | ☐ |
| 2 | CLICK การ์ด **รหัสภาษีทั้งหมด** | — | ล้าง status+category filter กลับมา 10 แถว | ☐ |

### TC-L08 — Sort อัตรา เชิงตัวเลข (edge: numeric sort)
- group: List · ความสำคัญ: กลาง · trace: sortBy rate (numeric)
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`
- ผ่านเมื่อ: เรียง rate จากน้อยไปมากถูกต้องเชิงตัวเลข (0,1,2,... ไม่ใช่ string)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` | — | ตารางเรียงตามรหัส (default) | ☐ |
| 2 | CLICK หัวคอลัมน์ **อัตรา** | — | ไอคอนหัวเปลี่ยนเป็นลูกศรขึ้น · แถวเรียง rate น้อย→มาก: 0,0,0,1,2,3,5,7 (หน้าแรก) — 15 ต้องอยู่ท้ายสุด ไม่ใช่ก่อน 2 | ☐ |
| 3 | CLICK หัวคอลัมน์ **อัตรา** ซ้ำ | — | ลูกศรลง · เรียงมาก→น้อย: 15,10,10,7,... | ☐ |

### TC-L09 — Sort used เชิงตัวเลข (edge)
- group: List · ความสำคัญ: ต่ำ · trace: sortBy used (numeric)
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` | — | ตาราง 10 แถว | ☐ |
| 2 | CLICK หัวคอลัมน์ **ใช้ในสินค้า/เอกสาร** | — | เรียง used น้อย→มาก: 0,0,2,5,... (214 ท้ายสุดหน้า 2) — เชิงตัวเลข | ☐ |

### TC-L10 — Sort คอลัมน์ตัวอักษร (happy)
- group: List · ความสำคัญ: ต่ำ · trace: sortBy code/name (string)
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` → CLICK หัว **รหัส** | — | เรียง code A→Z (NONVAT,VAT0,VAT10,VAT7,WHT1,...) | ☐ |
| 2 | CLICK หัว **ชื่อรหัสภาษี** | — | เรียงตาม name_th | ☐ |

### TC-L11 — Pagination 2 หน้า (happy)
- group: List · ความสำคัญ: กลาง · trace: pager pageSize=8
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`
- ผ่านเมื่อ: ไปหน้า 2 เห็น 2 แถวที่เหลือ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` | — | **แสดง 1–8 จาก 10 รายการ** · pager มีปุ่ม 1, 2 | ☐ |
| 2 | CLICK ปุ่มหน้า **2** ใน pager | — | ตารางแสดง 2 แถวที่เหลือ · **แสดง 9–10 จาก 10 รายการ** · ปุ่ม 2 เป็น active | ☐ |
| 3 | CLICK ปุ่มลูกศรซ้าย (ก่อนหน้า) | — | กลับหน้า 1 · แสดง 1–8 | ☐ |

### TC-L12 — ล้างตัวกรอง (happy)
- group: List · ความสำคัญ: ต่ำ · trace: resetFilters
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` → TYPE "VAT" + SELECT หมวด **ยกเว้นภาษี** | VAT / exempt | ตารางกรอง (อาจว่าง) | ☐ |
| 2 | CLICK ปุ่ม **ล้างตัวกรอง** (ใน filter bar) | — | ช่องค้นหาว่าง · dropdown กลับ ทุกประเภท/ทุกสถานะ · ตาราง 10 แถว | ☐ |

### TC-L13 — Empty (no data) state (edge)
- group: List · ความสำคัญ: กลาง · trace: State empty(no data)
- Setup: role=tax_admin · **seed=ลบ records ทั้งหมด (state.records=[])** · files=— · **(ต้อง simulate — ล้าง seed)**
- Start: OPEN `#/tax-codes`
- ผ่านเมื่อ: แสดง empty state พร้อมปุ่มสร้าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` (records ว่าง) | — | empty title **ยังไม่มีรหัสภาษีในระบบ** | ☐ |
| 2 | VERIFY desc + ปุ่ม | — | desc **เริ่มต้นด้วยการสร้างรหัสภาษีแรกเข้าสู่ทะเบียน** + ปุ่ม **สร้างรหัสภาษี** | ☐ |
| 3 | VERIFY stat cards | — | ทุกการ์ดแสดงค่า 0 | ☐ |

### TC-L14 — คลิกแถวเปิด view drawer (happy)
- group: List · ความสำคัญ: กลาง · trace: openView
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` | — | ตาราง 10 แถว | ☐ |
| 2 | CLICK แถว **WHT3** (บริเวณที่ไม่ใช่ checkbox/ปุ่ม) | — | drawer รายละเอียดเปิด · eyebrow **รหัสภาษี · WHT3** · title **หัก ณ ที่จ่าย 3% (บริการ)** | ☐ |
| 3 | PRESS Esc | — | drawer ปิด กลับหน้า list | ☐ |

## G2 — สร้างรหัสภาษี (P-02)

### TC-C01 — สร้าง VAT ครบ + auto-code VAT01 (happy)
- group: สร้าง · ความสำคัญ: สูง · trace: AC-01/02 / BR-01 / VR-05 / event taxcode.created
- actor (role): tax_admin
- Setup: role=tax_admin · seed=10 (ไม่มี VAT01) · files=—
- Start: OPEN `#/tax-codes` → CLICK ปุ่ม **สร้างรหัสภาษี**
- ชุดข้อมูล: A
- ผ่านเมื่อ: บันทึกได้ + toast สร้างสำเร็จ + แถวใหม่บนสุด code=VAT01 used=0 status ใช้งาน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างรหัสภาษี** | — | drawer เปิด · eyebrow **รหัสภาษีใหม่** · title **สร้างรหัสภาษี** · section **ข้อมูลรหัสภาษี** | ☐ |
| 2 | VERIFY dropdown **ประเภทภาษี** | — | default = **ภาษีมูลค่าเพิ่ม (VAT)** · dropdown มี **เฉพาะ 3 ตัวเลือก** (VAT/WHT/ยกเว้นภาษี) [LOCK-TYPE-3] | ☐ |
| 3 | VERIFY dropdown **สถานะ** | — | default = **ใช้งาน** | ☐ |
| 4 | TYPE ช่อง **ชื่อ (ไทย)** | A: ภาษีมูลค่าเพิ่ม 7% ทดสอบ | ช่องแสดงค่าที่พิมพ์ | ☐ |
| 5 | TYPE ช่อง **อัตรา (%)** | A: 7 | ช่องแสดง 7 | ☐ |
| 6 | TYPE ช่อง **ชื่อ (อังกฤษ)** | A: VAT 7% Test | ช่องแสดงค่า (optional) | ☐ |
| 7 | (เว้นช่อง **รหัสภาษี** ว่าง) | — | ปล่อยว่างเพื่อให้ auto-code | ☐ |
| 8 | CLICK ปุ่ม **ยืนยันสร้าง** | — | ปุ่มขึ้น loader **กำลังบันทึก…** ชั่วคราว | ☐ |
| 9 | WAIT จน toast ปรากฏ (≤3s) | — | toast success **สร้างรหัสภาษี "ภาษีมูลค่าเพิ่ม 7% ทดสอบ" สำเร็จ** · drawer ปิด | ☐ |
| 10 | VERIFY แถวบนสุดของตาราง | — | code **VAT01** · used **0 รายการ** · pill **ใช้งาน** · count หัวข้อ = **11 รายการ** | ☐ |

### TC-C02 — auto-code WHT ไม่ชนของเดิม (happy)
- group: สร้าง · ความสำคัญ: กลาง · trace: AC-02 / autoCode
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes` → CLICK **สร้างรหัสภาษี**
- ชุดข้อมูล: B
- ผ่านเมื่อ: code เป็น WHT + 2 หลัก ที่ยังไม่มี (WHT01)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างรหัสภาษี** | — | drawer เปิด | ☐ |
| 2 | SELECT **หัก ณ ที่จ่าย (WHT)** → ประเภทภาษี | wht | dropdown เปลี่ยนเป็น WHT | ☐ |
| 3 | TYPE ช่อง **ชื่อ (ไทย)** | B: หัก ณ ที่จ่าย 3% ทดสอบ | แสดงค่า | ☐ |
| 4 | TYPE ช่อง **อัตรา (%)** | B: 3 | แสดง 3 | ☐ |
| 5 | SELECT **ร่าง** → สถานะ | draft | dropdown = ร่าง | ☐ |
| 6 | CLICK **ยืนยันสร้าง** → WAIT toast | — | toast **สร้างรหัสภาษี "หัก ณ ที่จ่าย 3% ทดสอบ" สำเร็จ** | ☐ |
| 7 | VERIFY แถวบนสุด | — | code **WHT01** (ไม่ชน WHT1/WHT10/WHT15) · pill **ร่าง** | ☐ |

### TC-C03 — สร้างยกเว้นภาษี → rate ล็อก 0 + tag (happy · LOCK-EXEMPT-0)
- group: สร้าง · ความสำคัญ: สูง · trace: AC-03 / BR-03 / VR-04 / LOCK-EXEMPT-0
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes` → CLICK **สร้างรหัสภาษี**
- ชุดข้อมูล: C
- ผ่านเมื่อ: เลือก exempt → ช่องอัตรา = 0 disabled + tag; สลับกลับ VAT ปลดล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างรหัสภาษี** | — | drawer เปิด · ช่องอัตราแก้ได้ปกติ | ☐ |
| 2 | SELECT **ยกเว้นภาษี** → ประเภทภาษี | exempt | ช่อง **อัตรา (%)** กลายเป็น **0** + disabled (กรอกไม่ได้) · ขึ้น tag **ยกเว้นภาษี = อัตรา 0** ข้าง label อัตรา | ☐ |
| 3 | TYPE ช่อง **ชื่อ (ไทย)** | C: ยกเว้นภาษีทดสอบ | แสดงค่า | ☐ |
| 4 | SELECT **ภาษีมูลค่าเพิ่ม (VAT)** → ประเภทภาษี (สลับกลับ) | vat | ช่องอัตราปลดล็อก (แก้ได้) · tag **ยกเว้นภาษี = อัตรา 0** หายไป | ☐ |
| 5 | SELECT **ยกเว้นภาษี** อีกครั้ง → บันทึก | exempt | อัตรากลับเป็น 0 disabled + tag | ☐ |
| 6 | CLICK **ยืนยันสร้าง** → WAIT toast | — | toast **สร้างรหัสภาษี "ยกเว้นภาษีทดสอบ" สำเร็จ** · แถวใหม่ rate **0%** · type-pill **ยกเว้นภาษี** · code auto **TAX01** | ☐ |

### TC-C04 — สร้างระบุรหัสเอง (happy)
- group: สร้าง · ความสำคัญ: กลาง · trace: AC-01
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes` → CLICK **สร้างรหัสภาษี**
- ชุดข้อมูล: D

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างรหัสภาษี** | — | drawer เปิด | ☐ |
| 2 | TYPE ช่อง **รหัสภาษี** | D: VATTEST | แสดง VATTEST | ☐ |
| 3 | TYPE **ชื่อ (ไทย)** + **อัตรา (%)** | D: ภาษีทดสอบระบุรหัส / 5 | แสดงค่า | ☐ |
| 4 | CLICK **ยืนยันสร้าง** → WAIT toast | — | toast สร้างสำเร็จ · แถวใหม่ code **VATTEST** (ใช้รหัสที่กรอก ไม่ auto) | ☐ |

### TC-C05 — ชื่อไทยว่าง → error (negative)
- group: สร้าง · ความสำคัญ: สูง · trace: AC-12/VR-01 / ERR_VALIDATION_FAILED
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes` → CLICK **สร้างรหัสภาษี**
- ชุดข้อมูล: E-name0

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างรหัสภาษี** | — | drawer เปิด | ☐ |
| 2 | TYPE ช่อง **อัตรา (%)** (เว้นชื่อไทย) | 7 | ช่องชื่อไทยยังว่าง | ☐ |
| 3 | CLICK **ยืนยันสร้าง** | — | ไม่บันทึก · drawer ยังเปิด · ช่องชื่อไทยขึ้น error **กรุณากรอกชื่อภาษาไทย** (has-err) | ☐ |
| 4 | VERIFY ไม่มี toast สำเร็จ | — | ไม่มี toast "สร้างรหัสภาษี ... สำเร็จ" | ☐ |

### TC-C06 — อัตราผิด: ว่าง / -1 / 120 → error (negative · boundary)
- group: สร้าง · ความสำคัญ: สูง · trace: AC-12 / BR-02 / VR-03 · `[AI-DEFAULT ← EC-A5 precision 2]`
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes` → CLICK **สร้างรหัสภาษี**
- ชุดข้อมูล: E-rate-empty / E-rate-neg / E-rate-hi

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างรหัสภาษี** → TYPE ชื่อไทย | ทดสอบอัตราว่าง | ช่องชื่อมีค่า | ☐ |
| 2 | CLICK **ยืนยันสร้าง** (เว้นอัตรา) | E-rate-empty | ช่องอัตราขึ้น error **กรุณากรอกอัตรา 0–100** · ไม่บันทึก | ☐ |
| 3 | TYPE ช่อง **อัตรา (%)** | E-rate-neg: -1 | — | ☐ |
| 4 | CLICK **ยืนยันสร้าง** | — | error **กรุณากรอกอัตรา 0–100** · ไม่บันทึก | ☐ |
| 5 | TYPE ช่อง **อัตรา (%)** | E-rate-hi: 120 | — | ☐ |
| 6 | CLICK **ยืนยันสร้าง** | — | error **กรุณากรอกอัตรา 0–100** · ไม่บันทึก | ☐ |
| 7 | TYPE ช่อง **อัตรา (%)** = 0 (boundary ล่าง) → CLICK **ยืนยันสร้าง** | 0 | บันทึกได้ (0 อยู่ในช่วง) — toast สร้างสำเร็จ | ☐ |

### TC-C07 — รหัสซ้ำ case-insensitive → error (negative · EC-01)
- group: สร้าง · ความสำคัญ: สูง · trace: AC-11 / BR-01 / EC-01 / ERR_CODE_DUPLICATE
- Setup: role=tax_admin · seed=10 (มี VAT7) · files=—
- Start: OPEN `#/tax-codes` → CLICK **สร้างรหัสภาษี**
- ชุดข้อมูล: E-dup (code=vat7 ตัวพิมพ์เล็ก)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างรหัสภาษี** | — | drawer เปิด | ☐ |
| 2 | TYPE ช่อง **รหัสภาษี** | vat7 (พิมพ์เล็ก) | แสดง vat7 | ☐ |
| 3 | TYPE **ชื่อ (ไทย)** + **อัตรา (%)** | ทดสอบรหัสซ้ำ / 7 | แสดงค่า | ☐ |
| 4 | CLICK **ยืนยันสร้าง** | — | ช่องรหัสขึ้น error **รหัส vat7 ถูกใช้แล้ว** (has-err) · ไม่บันทึก (case-insensitive ชน VAT7) | ☐ |

### TC-C08 — กันกดซ้ำ double-submit (edge · VR-05)
- group: สร้าง · ความสำคัญ: กลาง · trace: VR-05 loader
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes` → CLICK **สร้างรหัสภาษี**
- ชุดข้อมูล: A

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างรหัสภาษี** → TYPE ชื่อไทย + อัตรา | A | ค่าครบ | ☐ |
| 2 | CLICK ปุ่ม **ยืนยันสร้าง** | — | ปุ่มเปลี่ยนเป็น loader **กำลังบันทึก…** และ disable (กดซ้ำไม่ได้) | ☐ |
| 3 | CLICK ปุ่มซ้ำระหว่าง loader | — | ไม่เกิด record ซ้ำ · WAIT toast → มีแค่ 1 แถวใหม่ (count เพิ่ม 1 เท่านั้น) | ☐ |

### TC-C09 — สถานะเริ่มต้น + เลือกได้ 3 ค่า (happy · state default)
- group: สร้าง · ความสำคัญ: ต่ำ · trace: BR-06 default create=active
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes` → CLICK **สร้างรหัสภาษี**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างรหัสภาษี** → VERIFY dropdown **สถานะ** | — | default = **ใช้งาน** · ตัวเลือกมี ร่าง/ใช้งาน/ไม่ใช้งาน (3 ค่า) | ☐ |
| 2 | SELECT **ร่าง** → TYPE ชื่อ+อัตรา → **ยืนยันสร้าง** | draft | แถวใหม่ pill **ร่าง** | ☐ |

### TC-C10 — ปิด drawer 3 ทาง (edge · Esc chain)
- group: สร้าง · ความสำคัญ: ต่ำ · trace: Esc chain / dismiss (ไม่มี dirty-confirm ใน prototype)
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes` → CLICK **สร้างรหัสภาษี**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างรหัสภาษี** → CLICK ปุ่ม **ยกเลิก** (footer) | — | drawer ปิดทันที (ไม่มี dialog ยืนยัน — prototype ไม่มี dirty-check) | ☐ |
| 2 | CLICK **สร้างรหัสภาษี** → CLICK ไอคอน **x** มุมขวาบน drawer | — | drawer ปิด | ☐ |
| 3 | CLICK **สร้างรหัสภาษี** → PRESS Esc | — | drawer ปิด | ☐ |
| 4 | CLICK **สร้างรหัสภาษี** → CLICK พื้นที่มืดนอก drawer (backdrop) | — | drawer ปิด | ☐ |

## G3 — แก้ไข + IR-TAX-01 Guard (P-03)

### TC-E01 — แก้ตัว used=0 แก้ได้ทุก field (happy)
- group: แก้ไข · ความสำคัญ: สูง · trace: AC-04 / FN-03 (used=0) / S-03
- actor (role): tax_admin
- Setup: role=tax_admin · seed=VAT10 (T-010, draft, used=0) · files=—
- Start: OPEN `#/tax-codes` → หาแถว **VAT10** → CLICK ปุ่มดินสอ (แก้ไข) ท้ายแถว
- ผ่านเมื่อ: code/rate/category แก้ได้ (ไม่ disabled) + บันทึกแล้ว toast แก้ไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอนดินสอ (แก้ไข) ท้ายแถว **VAT10** | — | drawer เปิด · eyebrow **แก้ไขรหัสภาษี** · title = **ภาษีมูลค่าเพิ่ม 10% (เตรียมอัตราใหม่)** | ☐ |
| 2 | VERIFY ช่อง รหัส/อัตรา/ประเภท | — | **ทั้ง 3 ช่องแก้ได้** (ไม่ disabled) · ไม่มี lock-tag "ล็อก — ถูกใช้งานแล้ว" | ☐ |
| 3 | TYPE ช่อง **อัตรา (%)** แก้เป็น 12 | 12 | แสดง 12 | ☐ |
| 4 | TYPE ช่อง **ชื่อ (ไทย)** แก้ | ภาษีมูลค่าเพิ่ม 12% แก้แล้ว | แสดงค่าใหม่ | ☐ |
| 5 | CLICK ปุ่ม **บันทึกการแก้ไข** → WAIT toast | — | toast **บันทึกการแก้ไข "ภาษีมูลค่าเพิ่ม 12% แก้แล้ว" แล้ว** · drawer ปิด | ☐ |
| 6 | VERIFY แถว VAT10 ในตาราง | — | อัตราแสดง **12%** · ชื่อใหม่ | ☐ |

### TC-E02 — แก้ตัว used>0 UI ล็อก 3 field (happy · LOCK-IR-TAX-01)
- group: แก้ไข · ความสำคัญ: สูง · trace: AC-05 / BR-04 / LOCK-IR-TAX-01
- Setup: role=tax_admin · seed=VAT7 (T-001, used=214) · files=—
- Start: OPEN `#/tax-codes` → CLICK ปุ่มดินสอ (แก้ไข) ท้ายแถว **VAT7**
- ผ่านเมื่อ: code/rate/category disabled + lock-tag; name/status ยังแก้ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอนดินสอ (แก้ไข) ท้ายแถว **VAT7** | — | drawer เปิด · title **ภาษีมูลค่าเพิ่ม 7%** | ☐ |
| 2 | VERIFY ช่อง **รหัสภาษี** | — | disabled (กรอกไม่ได้) · มี tag **ล็อก — ถูกใช้งานแล้ว** ข้าง label | ☐ |
| 3 | VERIFY ช่อง **อัตรา (%)** | — | disabled · มี tag **ล็อก — ถูกใช้งานแล้ว** | ☐ |
| 4 | VERIFY dropdown **ประเภทภาษี** | — | disabled · มี tag **ล็อก — ถูกใช้งานแล้ว** | ☐ |
| 5 | VERIFY ช่อง **ชื่อ (ไทย)** / **สถานะ** | — | แก้ได้ปกติ (ไม่ disabled) | ☐ |

### TC-E03 — แก้ตัว used>0 เปลี่ยนชื่อ/สถานะได้ (happy)
- group: แก้ไข · ความสำคัญ: สูง · trace: AC-05 / BR-04
- Setup: role=tax_admin · seed=VAT7 (used=214) · files=—
- Start: OPEN `#/tax-codes` → CLICK แก้ไขแถว **VAT7**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แก้ไขแถว **VAT7** | — | drawer เปิด (fields ล็อกตาม TC-E02) | ☐ |
| 2 | TYPE ช่อง **ชื่อ (ไทย)** แก้ | ภาษีมูลค่าเพิ่ม 7% (แก้ชื่อ) | แสดงค่าใหม่ | ☐ |
| 3 | SELECT **ไม่ใช้งาน** → สถานะ | inactive | dropdown = ไม่ใช้งาน | ☐ |
| 4 | CLICK **บันทึกการแก้ไข** → WAIT toast | — | toast **บันทึกการแก้ไข "ภาษีมูลค่าเพิ่ม 7% (แก้ชื่อ)" แล้ว** | ☐ |
| 5 | VERIFY แถว VAT7 | — | ชื่อใหม่ · pill **ไม่ใช้งาน** · **อัตรายังเป็น 7% · code ยัง VAT7** (ไม่เปลี่ยน) | ☐ |

### TC-E04 — ★ IR-TAX-01 server guard (bypass UI) — **P0** (negative · error · EC-07 · ต้อง simulate)
- group: แก้ไข · ความสำคัญ: **สูงสุด (P0)** · trace: AC-06 / TC-05 / BR-04 / EC-07 / KPI-02 (0 persist violation)
- actor (role): tax_admin
- Setup: role=tax_admin · seed=VAT7 (used=214, rate=7, category=vat) · files=— · **(ต้อง simulate — ฝั่ง client bypass UI: re-enable ช่องที่ disabled แล้วแก้ค่า/ยิง PUT พร้อม code/rate/category ใหม่)**
- Start: OPEN `#/tax-codes` → CLICK แก้ไขแถว **VAT7**
- ผ่านเมื่อ: แม้ payload ฝืนส่ง code/rate/category ใหม่ → หลังบันทึกค่า **3 field เดิมไม่เปลี่ยน** (server/logic guard คงค่าเดิม)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แก้ไขแถว **VAT7** → VERIFY+จดค่าเดิม | — | บันทึกค่าตั้งต้น: **code=VAT7 · อัตรา=7 · ประเภท=ภาษีมูลค่าเพิ่ม (VAT)** (อ้างใน step 4) | ☐ |
| 2 | (simulate) เปิด devtools/JS ปลด `disabled` ของ ช่องรหัส/อัตรา/ประเภท | — | 3 ช่องกรอกได้ (bypass UI lock) | ☐ |
| 3 | TYPE รหัส="VATHACK" · อัตรา="99" · SELECT ประเภท="หัก ณ ที่จ่าย (WHT)" → CLICK **บันทึกการแก้ไข** → WAIT toast | — | toast **บันทึกการแก้ไข "…" แล้ว** (ชื่อ/สถานะ persist) | ☐ |
| 4 | OPEN `#/tax-codes` → CLICK แก้ไขแถว **VAT7** อีกครั้ง → VERIFY 3 field | — | **code ยัง=VAT7 · อัตรา ยัง=7 · ประเภท ยัง=ภาษีมูลค่าเพิ่ม (VAT)** — ตรงกับค่าที่จดใน step 1 (guard คงค่าเดิม 3 field ต่อให้ payload ฝืน) · **0 persist violation** | ☐ |
| 5 | VERIFY แถว VAT7 ในตาราง | — | ไม่มีแถว/ค่า VATHACK · rate ยัง 7% · type-pill ยัง ภาษีมูลค่าเพิ่ม (VAT) | ☐ |

> หมายเหตุ (production): F-TAX-API-04 (PUT) ต้อง persist เฉพาะ name_th/name_en/status เมื่อ used>0 — ตอบ record ที่ 3 field เดิมไม่เปลี่ยน (ไม่ใช่แค่ UI disable). เป็น P0 DoD.

### TC-E05 — แก้ตัว exempt ที่ used>0 (edge · LOCK ผสม exempt)
- group: แก้ไข · ความสำคัญ: กลาง · trace: BR-03 + BR-04 (NONVAT used=18, exempt)
- Setup: role=tax_admin · seed=NONVAT (T-003, exempt, used=18) · files=—
- Start: OPEN `#/tax-codes` → CLICK แก้ไขแถว **NONVAT**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แก้ไขแถว **NONVAT** | — | drawer เปิด · code/rate/category **disabled + lock-tag** (used>0 ชนะ) | ☐ |
| 2 | VERIFY ช่องอัตรา | — | ค่า **0** และ disabled (ทั้งจาก exempt และ lock-on-use) | ☐ |
| 3 | TYPE ช่อง **ชื่อ (อังกฤษ)** แก้ → **บันทึกการแก้ไข** | VAT Exempt (edited) | toast แก้ไขสำเร็จ · rate ยัง 0 · ประเภท ยัง ยกเว้นภาษี | ☐ |

### TC-E06 — แก้ code ชนตัวอื่น case-insensitive (negative)
- group: แก้ไข · ความสำคัญ: กลาง · trace: AC-11 / BR-01 / VR-02 (บน edit used=0)
- Setup: role=tax_admin · seed=VAT10 (T-010, used=0) + VAT0 (T-002) · files=—
- Start: OPEN `#/tax-codes` → CLICK แก้ไขแถว **VAT10**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แก้ไขแถว **VAT10** | — | drawer เปิด · ช่องรหัสแก้ได้ (used=0) | ☐ |
| 2 | TYPE ช่อง **รหัสภาษี** เปลี่ยนเป็น | vat0 (พิมพ์เล็ก) | แสดง vat0 | ☐ |
| 3 | CLICK **บันทึกการแก้ไข** | — | ช่องรหัสขึ้น error **รหัส vat0 ถูกใช้แล้ว** · ไม่บันทึก (ชน VAT0) | ☐ |

## G4 — ดูรายละเอียด + เปลี่ยนสถานะ (P-04)

### TC-V01 — เปิด view drawer 3 tab (happy)
- group: View · ความสำคัญ: กลาง · trace: AC-18 / P-04 tabs
- Setup: role=tax_admin · seed=WHT3 (used=87) · files=—
- Start: OPEN `#/tax-codes` → CLICK แถว **WHT3**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **WHT3** | — | drawer เปิด · eyebrow **รหัสภาษี · WHT3** · title **หัก ณ ที่จ่าย 3% (บริการ)** · subtitle pill **ใช้งาน** + **หัก ณ ที่จ่าย (WHT)** | ☐ |
| 2 | VERIFY แถบ tab | — | 3 tab: **ภาพรวม** (active) · **การใช้งาน** (มี badge **87**) · **ประวัติ** | ☐ |
| 3 | VERIFY tab ภาพรวม (def-grid) | — | แสดง รหัส/อัตรา/ชื่อไทย/ชื่ออังกฤษ/ประเภท/สถานะ | ☐ |
| 4 | VERIFY footer | — | meta **แก้ไขล่าสุด {date}** + ปุ่ม **ปิด** | ☐ |

### TC-V02 — tab การใช้งาน badge + count, ไม่มีแถวลบ (happy · FN-23)
- group: View · ความสำคัญ: กลาง · trace: AC-18 / FN-23 (no delete row)
- Setup: role=tax_admin · seed=WHT3 (used=87) · files=—
- Start: OPEN `#/tax-codes` → CLICK แถว **WHT3**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **WHT3** → CLICK tab **การใช้งาน** | — | badge tab = **87** · แสดง **การอ้างอิงจากสินค้า** · **จำนวนที่ถูกอ้างอิง** = **87 รายการ** | ☐ |
| 2 | VERIFY ไม่มีปุ่มลบ | — | **ไม่มี** ปุ่ม/แถว "ลบออกจากทะเบียน" ใน tab นี้ | ☐ |

### TC-V03 — tab ประวัติ timeline audit (happy · BR-10)
- group: View · ความสำคัญ: ต่ำ · trace: AC-18 / BR-10 / FN-93
- Setup: role=tax_admin · seed=WHT3 · files=—
- Start: OPEN `#/tax-codes` → CLICK แถว **WHT3**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **WHT3** → CLICK tab **ประวัติ** | — | timeline 2 รายการ: **แก้ไขล่าสุด** {ผู้แก้ · วันที่} และ **สร้างรายการ** {ผู้สร้าง · วันที่} | ☐ |

### TC-V04 — status menu ค่าปัจจุบัน dimmed + "ปัจจุบัน" (edge · state)
- group: View/Status · ความสำคัญ: สูง · trace: AC-07 / BR-06 / §5.2 current disabled
- Setup: role=tax_admin · seed=WHT3 (active) · files=—
- Start: OPEN `#/tax-codes` → CLICK แถว **WHT3**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **WHT3** → CLICK ปุ่ม **เปลี่ยนสถานะ** (header) | — | เมนู `.status-menu` เปิด · หัวเมนู **เปลี่ยนสถานะเป็น** · 3 ตัวเลือก ร่าง/ใช้งาน/ไม่ใช้งาน | ☐ |
| 2 | VERIFY ตัวเลือก **ใช้งาน** (ค่าปัจจุบัน) | — | disabled/กดไม่ได้ + mark **ปัจจุบัน** (มีเครื่องหมาย check) | ☐ |
| 3 | VERIFY ตัวเลือก ร่าง/ไม่ใช้งาน | — | กดได้ทั้งคู่ (ไม่มี gate/อนุมัติ) | ☐ |
| 4 | PRESS Esc | — | เมนูปิด (Esc chain: ปิด menu ก่อน — drawer ยังเปิด) | ☐ |

### TC-V05 — เปลี่ยนสถานะเดี่ยว active→inactive (happy · BR-06)
- group: View/Status · ความสำคัญ: สูง · trace: AC-07 / BR-06 / setStatus
- Setup: role=tax_admin · seed=WHT3 (active) · files=—
- Start: OPEN `#/tax-codes` → CLICK แถว **WHT3**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **WHT3** → CLICK **เปลี่ยนสถานะ** | — | เมนูเปิด | ☐ |
| 2 | CLICK ตัวเลือก **ไม่ใช้งาน** | — | WAIT toast **เปลี่ยนสถานะ "หัก ณ ที่จ่าย 3% (บริการ)" เป็น ไม่ใช้งาน แล้ว** · ไม่มีขั้นอนุมัติ | ☐ |
| 3 | VERIFY drawer/list | — | subtitle pill ใน drawer = **ไม่ใช้งาน** · แถวใน list pill **ไม่ใช้งาน** | ☐ |

### TC-V06 — free transition ทุกทิศ (draft→inactive) (edge · LOCK-STATUS-FREE)
- group: View/Status · ความสำคัญ: กลาง · trace: BR-06 / §5.2 free transitions / LOCK-STATUS-FREE
- Setup: role=tax_admin · seed=VAT10 (draft, used=0) · files=—
- Start: OPEN `#/tax-codes` → CLICK แถว **VAT10**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **VAT10** (draft) → CLICK **เปลี่ยนสถานะ** | — | เมนูเปิด · ค่าปัจจุบัน **ร่าง** = disabled+ปัจจุบัน | ☐ |
| 2 | CLICK ตัวเลือก **ไม่ใช้งาน** (ข้าม active โดยตรง) | — | toast **เปลี่ยนสถานะ "…" เป็น ไม่ใช้งาน แล้ว** — เปลี่ยนได้ทันทีทุกทิศ ไม่ต้องผ่าน active | ☐ |
| 3 | CLICK **เปลี่ยนสถานะ** → CLICK **ใช้งาน** | — | toast เปลี่ยนเป็น ใช้งาน — inactive→active ตรงได้เช่นกัน | ☐ |

## G5 — Bulk เปลี่ยนสถานะ

### TC-B01 — เลือกแถว → bulk bar ปรากฏ (happy)
- group: Bulk · ความสำคัญ: กลาง · trace: toggleSel / bulk bar
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` | — | ไม่มี bulk bar | ☐ |
| 2 | CLICK checkbox ต้นแถว **WHT1** | — | bulk bar ปรากฏ · ข้อความ **เลือก 1 รายการ** · ปุ่ม ตั้งเป็น ใช้งาน/ร่าง/ไม่ใช้งาน · ลบ · ยกเลิกการเลือก | ☐ |
| 3 | CLICK checkbox **WHT2** | — | **เลือก 2 รายการ** | ☐ |

### TC-B02 — bulk ตั้งเป็น ใช้งาน (happy · AC-08)
- group: Bulk · ความสำคัญ: สูง · trace: AC-08 / BR-06 / bulkSetStatus
- Setup: role=tax_admin · seed=VAT10(draft)+WHT15(inactive) · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` → CLICK checkbox **VAT10** + **WHT15** | — | **เลือก 2 รายการ** | ☐ |
| 2 | CLICK ปุ่ม **ตั้งเป็น ใช้งาน** (bulk bar) | — | WAIT toast **เปลี่ยนสถานะ 2 รายการ เป็น ใช้งาน แล้ว** | ☐ |
| 3 | VERIFY 2 แถว | — | ทั้ง VAT10 และ WHT15 pill = **ใช้งาน** · selection ถูกล้าง (bulk bar หาย) | ☐ |

### TC-B03 — bulk ตั้งเป็น ร่าง (happy)
- group: Bulk · ความสำคัญ: กลาง · trace: AC-08 / BR-06
- Setup: role=tax_admin · seed=WHT1+WHT2 (active) · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox **WHT1** + **WHT2** → CLICK **ตั้งเป็น ร่าง** | — | toast **เปลี่ยนสถานะ 2 รายการ เป็น ร่าง แล้ว** · 2 แถว pill **ร่าง** | ☐ |

### TC-B04 — bulk ตั้งเป็น ไม่ใช้งาน (happy)
- group: Bulk · ความสำคัญ: กลาง · trace: AC-08 / BR-06
- Setup: role=tax_admin · seed=WHT1+WHT2 (active) · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox **WHT1** + **WHT2** → CLICK **ตั้งเป็น ไม่ใช้งาน** | — | toast **เปลี่ยนสถานะ 2 รายการ เป็น ไม่ใช้งาน แล้ว** · 2 แถว pill **ไม่ใช้งาน** | ☐ |

### TC-B05 — select-all หน้านี้ (edge)
- group: Bulk · ความสำคัญ: ต่ำ · trace: toggleSelPage
- Setup: role=tax_admin · seed=10 (หน้าแรก 8 แถว) · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` → CLICK checkbox หัวตาราง (select all) | — | ทุกแถวในหน้า (8) ถูกติ๊ก · bulk bar **เลือก 8 รายการ** | ☐ |
| 2 | CLICK checkbox หัวตารางซ้ำ | — | ยกเลิกทั้งหมด · bulk bar หาย | ☐ |

### TC-B06 — ยกเลิกการเลือก (happy)
- group: Bulk · ความสำคัญ: ต่ำ · trace: clearBulkSel
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox **WHT1** → CLICK ปุ่ม **ยกเลิกการเลือก** | — | selection ล้าง · bulk bar หาย | ☐ |

## G6 — Bulk Delete (P-06)

### TC-D01 — bulk delete used=0 ทั้งหมด (happy · AC-09)
- group: Delete · ความสำคัญ: สูง · trace: AC-09 / BR-05 / FN-07 / LOCK-BULK-DEL
- actor (role): tax_admin
- Setup: role=tax_admin · seed=VAT10(used=0)+WHT15(used=0) · files=—
- Start: OPEN `#/tax-codes`
- ผ่านเมื่อ: modal confirm → ลบ 2 แถว → toast success

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` → CLICK checkbox **VAT10** + **WHT15** → VERIFY+จดจำนวนแถวรวม | — | จดค่า: count = **10 รายการ** (อ้างใน step 4) · **เลือก 2 รายการ** | ☐ |
| 2 | CLICK ปุ่ม **ลบ** (bulk bar) | — | modal เปิด · title **ลบรหัสภาษี 2 รายการ?** · desc **การกระทำนี้ย้อนกลับไม่ได้** (ไม่มี used>0) | ☐ |
| 3 | CLICK ปุ่ม **ลบ 2 รายการ** (danger) | — | WAIT toast **ลบแล้ว 2 รายการ** (success) · modal ปิด | ☐ |
| 4 | VERIFY count หัวข้อ | — | **8 รายการ** (ลดจาก 10 = 2 ที่ลบ) · ไม่เห็น VAT10/WHT15 | ☐ |

### TC-D02 — bulk delete ผสม used>0/used=0 → ข้าม used>0 (edge · error · AC-10 · EC-06)
- group: Delete · ความสำคัญ: สูง · trace: AC-10 / EC-06 / BR-05
- Setup: role=tax_admin · seed=VAT7(used=214)+VAT10(used=0) · files=—
- Start: OPEN `#/tax-codes`
- ผ่านเมื่อ: VAT10 ถูกลบ · VAT7 ถูกข้าม · toast warning

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` → CLICK checkbox **VAT7** + **VAT10** | — | **เลือก 2 รายการ** | ☐ |
| 2 | CLICK ปุ่ม **ลบ** | — | modal · title **ลบรหัสภาษี 2 รายการ?** · desc **มี 1 รายการถูกอ้างอิงในสินค้า/เอกสาร — จะถูกข้าม ไม่ลบ** · ปุ่ม **ลบ 1 รายการ** (2-1) | ☐ |
| 3 | CLICK **ลบ 1 รายการ** | — | WAIT toast (warning) **ลบแล้ว 1 รายการ · ข้าม 1 (ถูกใช้ในสินค้า/เอกสาร)** | ☐ |
| 4 | VERIFY ตาราง | — | **VAT10 หายไป** · **VAT7 ยังอยู่** (used>0 ข้าม) | ☐ |

### TC-D03 — confirm modal แสดงยอด used>0 ถูกต้อง (edge)
- group: Delete · ความสำคัญ: กลาง · trace: AC-09 desc/button count
- Setup: role=tax_admin · seed=VAT7(214)+VAT0(36)+VAT10(0) · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox **VAT7** + **VAT0** + **VAT10** → CLICK **ลบ** | — | title **ลบรหัสภาษี 3 รายการ?** · desc **มี 2 รายการถูกอ้างอิง…จะถูกข้าม ไม่ลบ** · ปุ่ม **ลบ 1 รายการ** (3-2) | ☐ |

### TC-D04 — ยกเลิกการลบ (happy · Esc chain)
- group: Delete · ความสำคัญ: ต่ำ · trace: dismiss modal
- Setup: role=tax_admin · seed=VAT10(0) · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox **VAT10** → CLICK **ลบ** | — | modal เปิด | ☐ |
| 2 | CLICK ปุ่ม **ยกเลิก** (ghost) | — | modal ปิด · ไม่มีอะไรถูกลบ · VAT10 ยังอยู่ | ☐ |
| 3 | CLICK **ลบ** → PRESS Esc | — | modal ปิด (Esc chain: modal) · ไม่ลบ | ☐ |

## G7 — นำเข้า CSV 3-step + 6 Error Codes (P-05)

### TC-I01 — จอแรก import: ไม่มีข้อความคอลัมน์ + ยังไม่ preview (happy · AC-13 · EC-08)
- group: Import · ความสำคัญ: สูง · trace: AC-13 / EC-08 / FN-16
- actor (role): tax_admin
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes` → CLICK ปุ่ม **นำเข้า CSV**
- ผ่านเมื่อ: modal จอแรกมีแค่ upload-box + ปุ่ม template, ไม่มีตาราง preview

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **นำเข้า CSV** | — | modal เปิด · title **นำเข้ารหัสภาษีจากไฟล์** · desc **CSV / Excel — ระบุสถานะได้ในไฟล์** | ☐ |
| 2 | VERIFY เนื้อ modal จอแรก | — | มี upload-box **เลือกไฟล์ CSV / Excel** + สถานะ **ยังไม่ได้เลือกไฟล์** · **ไม่มีข้อความอธิบายคอลัมน์ใด ๆ** | ☐ |
| 3 | VERIFY footer | — | ปุ่ม **ดาวน์โหลด template ตัวอย่าง** + ปุ่ม **ปิด** | ☐ |
| 4 | VERIFY ไม่มี preview | — | ยังไม่มีตารางรายแถว/สรุป "ตรวจแล้ว…" (preview เกิดเฉพาะเมื่อเลือกไฟล์จริง) | ☐ |

### TC-I02 — ต้องเลือกไฟล์ก่อนจึง preview (edge · EC-08)
- group: Import · ความสำคัญ: สูง · trace: AC-13 / EC-08 / bulkFileChosen
- Setup: role=tax_admin · seed=10 · files=`taxcode_import_sample.csv`
- Start: OPEN `#/tax-codes` → CLICK **นำเข้า CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **นำเข้า CSV** | — | จอแรก (pick) ไม่มี preview | ☐ |
| 2 | CLICK upload-box **เลือกไฟล์ CSV / Excel** → UPLOAD | taxcode_import_sample.csv | file picker เปิด แล้วเลือกไฟล์ | ☐ |
| 3 | WAIT จอเปลี่ยน | — | modal ไป step preview (มีสรุป "ตรวจแล้ว…") — preview เกิดหลังเลือกไฟล์เท่านั้น | ☐ |

### TC-I03 — ดาวน์โหลด template ตัวอย่าง (happy)
- group: Import · ความสำคัญ: ต่ำ · trace: FN-16 downloadTemplate
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes` → CLICK **นำเข้า CSV**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **นำเข้า CSV** → CLICK ปุ่ม **ดาวน์โหลด template ตัวอย่าง** | — | ไฟล์ `taxcode_import_template.csv` ถูกดาวน์โหลด · WAIT toast **ดาวน์โหลด template ตัวอย่างแล้ว** | ☐ |

### TC-I04 — preview สรุปตรวจแถว (happy · AC-14)
- group: Import · ความสำคัญ: สูง · trace: AC-14 / BR-08
- Setup: role=tax_admin · seed=10 (มี VAT7) · files=`taxcode_import_sample.csv` (5 แถว, 3 ok/2 err)
- Start: OPEN `#/tax-codes` → CLICK **นำเข้า CSV** → UPLOAD sample

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **นำเข้า CSV** → UPLOAD `taxcode_import_sample.csv` | — | ไป step preview | ☐ |
| 2 | VERIFY แถบสรุป | — | **ตรวจแล้ว 5 แถว — นำเข้าได้ 3 · ติดปัญหา 2 (แถวผิดจะถูกข้าม)** | ☐ |
| 3 | VERIFY หัวตาราง preview | — | คอลัมน์ รหัส/ชื่อรหัสภาษี/ประเภท/อัตรา/สถานะ/**ผลตรวจ** | ☐ |
| 4 | VERIFY ปุ่ม footer | — | **ยกเลิก** + **นำเข้า 3 แถว** (enabled) | ☐ |

### TC-I05 — import status ว่าง = ร่าง (edge · EC-05)
- group: Import · ความสำคัญ: กลาง · trace: AC-14 / EC-05 / BR-08
- Setup: role=tax_admin · seed=10 · files=`taxcode_import_sample.csv`
- Start: OPEN `#/tax-codes` → CLICK **นำเข้า CSV** → UPLOAD sample

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD sample → VERIFY แถว **VAT9** (status ในไฟล์ว่าง) | — | คอลัมน์สถานะ preview = pill **ร่าง** · ผลตรวจ = **พร้อมนำเข้า** | ☐ |

### TC-I06 — import อัตราทศนิยม 0.75 ผ่าน (edge · EC-04 · `[AI-DEFAULT]` precision 2)
- group: Import · ความสำคัญ: กลาง · trace: AC-15 / EC-04 / BR-02 `[AI-DEFAULT ← EC-A5 numeric(5,2)]`
- Setup: role=tax_admin · seed=10 · files=`taxcode_import_sample.csv`
- Start: OPEN `#/tax-codes` → CLICK **นำเข้า CSV** → UPLOAD sample

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD sample → VERIFY แถว **WHT075** (rate 0.75, ใช้งาน) | — | ผลตรวจ = **พร้อมนำเข้า** · อัตรา preview = **0.75%** | ☐ |
| 2 | CLICK **นำเข้า 3 แถว** → OPEN `#/tax-codes` VERIFY WHT075 | — | record ใหม่ WHT075 · อัตรา **0.75%** · pill **ใช้งาน** (ทศนิยม 2 ตำแหน่งถูกเก็บ — `[AI-DEFAULT]` precision 2) | ☐ |

### TC-I07 — import error CODE_DUPLICATE (error · AC-16 · EC-01)
- group: Import · ความสำคัญ: สูง · trace: AC-16 / BR-01 / CODE_DUPLICATE
- Setup: role=tax_admin · seed=10 (มี VAT7) · files=`taxcode_import_sample.csv`
- Start: OPEN `#/tax-codes` → CLICK **นำเข้า CSV** → UPLOAD sample

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD sample → VERIFY แถว **VAT7** (ซ้ำกับ seed) | — | ผลตรวจ = pill error **รหัสซ้ำ (CODE_DUPLICATE)** | ☐ |

### TC-I08 — import error RATE_INVALID (error · AC-16 · EC-02)
- group: Import · ความสำคัญ: สูง · trace: AC-16 / BR-02 / RATE_INVALID
- Setup: role=tax_admin · seed=10 · files=`taxcode_import_sample.csv`
- Start: OPEN `#/tax-codes` → CLICK **นำเข้า CSV** → UPLOAD sample

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD sample → VERIFY แถว **WHT99** (rate 120) | — | ผลตรวจ = pill error **อัตราไม่ถูกต้อง 0–100 (RATE_INVALID)** | ☐ |

### TC-I09 — import error REQUIRED (error · ต้อง simulate)
- group: Import · ความสำคัญ: กลาง · trace: AC-16 / §5.6 REQUIRED
- Setup: role=tax_admin · seed=10 · files=`taxcode_import_required.csv` · **(ต้อง simulate — patch `BULK_SAMPLE` ให้มี ≥1 แถวเว้น code หรือ rate ว่าง)**
- Start: OPEN `#/tax-codes` → CLICK **นำเข้า CSV** → UPLOAD required file

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `taxcode_import_required.csv` → VERIFY แถวที่ข้อมูลไม่ครบ | — | ผลตรวจ = pill error **ข้อมูลบังคับไม่ครบ (REQUIRED)** | ☐ |

### TC-I10 — import error BAD_TYPE (error · ต้อง simulate)
- group: Import · ความสำคัญ: กลาง · trace: AC-16 / §5.6 BAD_TYPE
- Setup: role=tax_admin · seed=10 · files=`taxcode_import_badtype.csv` · **(ต้อง simulate — patch แถว category นอก 3 ชื่อไทย)**
- Start: OPEN `#/tax-codes` → CLICK **นำเข้า CSV** → UPLOAD badtype file

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `taxcode_import_badtype.csv` → VERIFY แถว category ผิด | — | ผลตรวจ = pill error **ประเภทไม่ถูกต้อง (BAD_TYPE)** | ☐ |

### TC-I11 — import error EXEMPT_RATE (error · EC-03 · ต้อง simulate · LOCK-EXEMPT-0)
- group: Import · ความสำคัญ: กลาง · trace: AC-16 / EC-03 / BR-03 / EXEMPT_RATE
- Setup: role=tax_admin · seed=10 · files=`taxcode_import_exempt.csv` · **(ต้อง simulate — patch แถว "ยกเว้นภาษี" + rate≠0)**
- Start: OPEN `#/tax-codes` → CLICK **นำเข้า CSV** → UPLOAD exempt file

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `taxcode_import_exempt.csv` → VERIFY แถว exempt+rate≠0 | — | ผลตรวจ = pill error **ยกเว้นภาษีต้องอัตรา 0 (EXEMPT_RATE)** | ☐ |

### TC-I12 — import error BAD_STATUS (error · ต้อง simulate)
- group: Import · ความสำคัญ: กลาง · trace: AC-16 / §5.6 BAD_STATUS / ERR_INVALID_STATUS
- Setup: role=tax_admin · seed=10 · files=`taxcode_import_badstatus.csv` · **(ต้อง simulate — patch แถว status นอก ใช้งาน/ไม่ใช้งาน/ร่าง)**
- Start: OPEN `#/tax-codes` → CLICK **นำเข้า CSV** → UPLOAD badstatus file

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `taxcode_import_badstatus.csv` → VERIFY แถว status ผิด | — | ผลตรวจ = pill error **สถานะไม่ถูกต้อง (BAD_STATUS — ใช้ ใช้งาน/ไม่ใช้งาน/ร่าง)** | ☐ |

### TC-I13 — import commit → done + toast + list อัปเดต (happy · AC-16)
- group: Import · ความสำคัญ: สูง · trace: AC-16 / BR-08 / FN-19 / row isolation
- Setup: role=tax_admin · seed=10 (มี VAT7) · files=`taxcode_import_sample.csv`
- Start: OPEN `#/tax-codes` → CLICK **นำเข้า CSV** → UPLOAD sample
- ผ่านเมื่อ: commit → done step + toast import + list เพิ่ม 3 แถว (แถวผิดข้าม ไม่ล้มไฟล์)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD sample → VERIFY+จด count | — | จดค่า count = **10 รายการ** (อ้าง step 4) · สรุป **ตรวจแล้ว 5 แถว — นำเข้าได้ 3 · ติดปัญหา 2** | ☐ |
| 2 | CLICK ปุ่ม **นำเข้า 3 แถว** | — | ไป step done · แถบ **นำเข้าเสร็จ 3 รายการ (สถานะตามไฟล์) · ข้าม 2 แถว (IMPORT_ERROR)** + ตารางแถวข้าม (รหัส/ชื่อ/สาเหตุ) แสดง VAT7, WHT99 | ☐ |
| 3 | WAIT toast | — | toast (warning) **นำเข้าแล้ว 3 รายการ · ข้าม 2 แถว (IMPORT_ERROR)** | ☐ |
| 4 | CLICK ปุ่ม **ปิด** → VERIFY count | — | count = **13 รายการ** (10+3) · เห็น WHT075/VAT9/TAXOLD ในตาราง · VAT7 ไม่ซ้ำ (แถวผิดไม่ล้มไฟล์) | ☐ |

### TC-I14 — ปุ่มนำเข้า disabled เมื่อ ok=0 (edge · ต้อง simulate)
- group: Import · ความสำคัญ: ต่ำ · trace: preview footer disabled
- Setup: role=tax_admin · seed=10 · files=`taxcode_import_allerr.csv` · **(ต้อง simulate — patch ทุกแถว err)**
- Start: OPEN `#/tax-codes` → CLICK **นำเข้า CSV** → UPLOAD allerr file

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `taxcode_import_allerr.csv` | — | สรุป **นำเข้าได้ 0 · ติดปัญหา N** · ปุ่ม **นำเข้า 0 แถว** เป็น disabled (กดไม่ได้) | ☐ |

## G8 — ส่งออก CSV

### TC-X01 — export CSV ตาม filter, 7 คอลัมน์, BOM (happy · AC-17)
- group: Export · ความสำคัญ: กลาง · trace: AC-17 / FN-20 / C-07 (BOM+escape)
- actor (role): tax_admin
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`
- ผ่านเมื่อ: ดาวน์โหลดไฟล์ตาม filter ปัจจุบัน + toast จำนวน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` → SELECT หมวด **หัก ณ ที่จ่าย (WHT)** | wht | ตารางเหลือ 6 แถว WHT | ☐ |
| 2 | CLICK ปุ่ม **ส่งออก CSV** | — | ไฟล์ `taxcode_export_YYYY-MM-DD.csv` ถูกดาวน์โหลด · WAIT toast **ส่งออก 6 รายการเป็น CSV แล้ว** (นับเฉพาะที่ filter) | ☐ |
| 3 | VERIFY เนื้อไฟล์ (ถ้าเปิดได้) | — | header 7 คอลัมน์ `code,name_th,name_en,type,rate,status,used_in` · มี BOM (เปิด Excel ไทยไม่เพี้ยน) | ☐ |
| 4 | CLICK **ล้างตัวกรอง** → CLICK **ส่งออก CSV** | — | toast **ส่งออก 10 รายการเป็น CSV แล้ว** (export ตาม filter ที่ล้างแล้ว = ทั้งหมด) | ☐ |

## G9 — LOCK Absence (ยืนยันสิ่งที่ต้อง "ไม่มี") (AC-19)

### TC-K01 — ไม่มีปุ่มลบเดี่ยว (absence · LOCK-BULK-DEL)
- group: LOCK · ความสำคัญ: กลาง · trace: AC-19 / BR-05 / LOCK-BULK-DEL
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` → VERIFY คอลัมน์ **จัดการ** ของทุกแถว | — | มีเฉพาะไอคอนดินสอ (**แก้ไข**) · **ไม่มี** ไอคอนถังขยะ/ปุ่มลบรายแถว (ลบได้เฉพาะผ่าน bulk) | ☐ |

### TC-K02 — ไม่มี field เลขบัญชี GL ในฟอร์ม (absence · LOCK-NO-GL)
- group: LOCK · ความสำคัญ: กลาง · trace: AC-19 / BR-09 / LOCK-NO-GL
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes` → CLICK **สร้างรหัสภาษี**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างรหัสภาษี** → VERIFY ฟิลด์ในฟอร์ม | — | มีเฉพาะ รหัสภาษี/อัตรา (%)/ชื่อ (ไทย)/ชื่อ (อังกฤษ)/ประเภทภาษี/สถานะ · **ไม่มีช่องเลขบัญชี GL** | ☐ |

### TC-K03 — ไม่มีปุ่มส่งอนุมัติ / สายอนุมัติ (absence · LOCK-DOA-NULL) `[AI-DEFAULT COSO Approver=N/A]`
- group: LOCK · ความสำคัญ: กลาง · trace: AC-19 / LOCK-DOA-NULL
- Setup: role=tax_admin · seed=WHT3 · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างรหัสภาษี** → VERIFY footer | — | ปุ่มมีเฉพาะ **ยกเลิก** + **ยืนยันสร้าง** · **ไม่มี** ปุ่ม "ส่งอนุมัติ"/สายอนุมัติ | ☐ |
| 2 | CLICK แถว **WHT3** (view) → VERIFY header actions | — | มีเฉพาะ แก้ไข/เปลี่ยนสถานะ/ปิด · ไม่มี approver/ลายเซ็น/พิมพ์ | ☐ |

### TC-K04 — ไม่มี icon/avatar หน้ารหัสใน list (absence)
- group: LOCK · ความสำคัญ: ต่ำ · trace: AC-19 (cell-code ไม่มี icon)
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY คอลัมน์ **รหัส** ทุกแถว | — | แสดงข้อความรหัสอย่างเดียว · **ไม่มี** icon/avatar นำหน้ารหัส | ☐ |

### TC-K05 — กระดิ่งเป็น placeholder ไม่ emit event (absence · LOCK-NO-NOTIF)
- group: LOCK · ความสำคัญ: ต่ำ · trace: AC-19 / LOCK-NO-NOTIF / §6.5 no WebSocket
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างรหัสภาษี** → สร้าง record (ชุด A) → WAIT toast สำเร็จ | A | มี toast success | ☐ |
| 2 | CLICK ไอคอนกระดิ่ง (มุมขวาบน) | — | เมนูแจ้งเตือนเป็นข้อความ placeholder คงที่ · **ไม่มี** รายการแจ้งเตือนใหม่จากการสร้างเมื่อครู่ (feature ไม่ emit event) | ☐ |

## G10 — Cross-Module (XT — 06_TESTS §6.9)

### TC-XT01 — lookup ปลายทางเห็นเฉพาะ active (integration · XT-01 · BR-07 · LOCK-SOFT-REF)
- group: XT · ความสำคัญ: กลาง · trace: XT-01 / BR-07 / F-TAX-API-10
- actor (role): consumer (Item Master/เอกสาร) — read-only
- Setup: role=consumer · seed=รหัส active หลายตัว + WHT15(inactive) + VAT10(draft) · files=— · **(ต้อง simulate — prototype ไม่มีหน้า Item Master; ตรวจจาก contract lookup ว่าคืนเฉพาะ status=active)**
- Start: (downstream) เปิด combobox กลุ่มภาษีในหน้า Item Master/เอกสาร
- ผ่านเมื่อ: combobox แสดงเฉพาะรหัส active; draft/inactive ไม่โผล่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN หน้า Item Master (simulate) → CLICK combobox กลุ่มภาษี | — | รายการเลือกได้ = เฉพาะ status **ใช้งาน** (VAT7/VAT0/WHT1..) | ☐ |
| 2 | VERIFY WHT15 (inactive) + VAT10 (draft) | — | **ไม่โผล่** ใน combobox (F-TAX-API-10 force active) | ☐ |

### TC-XT02 — เปลี่ยนรหัสเป็น inactive ภายหลัง เอกสารเดิมคงค่า (integration · XT-02 · EC-A4/A6)
- group: XT · ความสำคัญ: กลาง · trace: XT-02 / BR-07 / LOCK-SOFT-REF (soft ref, no cascade)
- Setup: role=tax_admin+consumer · seed=WHT3(active,used>0) + เอกสารเดิม 1 ใบอ้าง WHT3 rate 3% · files=— · **(ต้อง simulate — ตรวจเอกสารเดิมฝั่ง downstream)**
- Start: OPEN `#/tax-codes` → เปลี่ยน WHT3 เป็น inactive

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) OPEN เอกสารเดิมที่อ้าง WHT3 → VERIFY+จดค่า | — | จดค่า: เอกสารแสดง code **WHT3** rate **3%** (อ้าง step 4) | ☐ |
| 2 | OPEN `#/tax-codes` → CLICK WHT3 → **เปลี่ยนสถานะ** → **ไม่ใช้งาน** | — | toast เปลี่ยนสถานะเป็น ไม่ใช้งาน | ☐ |
| 3 | (simulate) OPEN combobox เลือกรหัสในเอกสาร**ใหม่** | — | WHT3 **เลือกใหม่ไม่ได้** (inactive ซ่อน) | ☐ |
| 4 | (simulate) OPEN เอกสาร**เดิม** อีกครั้ง → VERIFY | — | ยังแสดง code **WHT3** rate **3%** เท่าค่าที่จดใน step 1 (soft ref ไม่ cascade — เอกสารเดิมคงค่า) | ☐ |

### TC-XT03 — guard คุ้มครองบิลเก่า (integration · XT-03 · BR-04)
- group: XT · ความสำคัญ: กลาง · trace: XT-03 / BR-04 (อ้าง TC-E04)
- Setup: role=tax_admin · seed=VAT7(used=214) + บิลเก่าอ้าง VAT7 rate 7% · files=— · **(ต้อง simulate — ผ่าน TC-E04 + ตรวจบิลฝั่ง downstream)**
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ทำ TC-E04 (พยายามแก้ rate ของ VAT7 used>0) | — | ถูก IR-TAX-01 guard บล็อก · rate ยัง 7% | ☐ |
| 2 | (simulate) OPEN บิลเก่าที่อ้าง VAT7 → VERIFY การคำนวณ VAT | — | บิลเก่าคำนวณ VAT ที่ 7% ถูกต้องตลอด (accounting integrity) | ☐ |

### TC-XT04 — GL Posting อ่าน code แต่ทะเบียนไม่ถือเลข GL (integration · XT-04 · LOCK-NO-GL)
- group: XT · ความสำคัญ: ต่ำ · trace: XT-04 / BR-09 / LOCK-NO-GL
- Setup: role=tax_admin · seed=VAT7 · files=— · **(ต้อง simulate — ฝั่ง GL Posting Setup)**
- Start: OPEN `#/tax-codes`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/tax-codes` → CLICK VAT7 (view) → VERIFY | — | ทะเบียนแสดง code VAT7 · **ไม่มี** field เลขบัญชี GL (mapping อยู่ที่ GL Posting Setup) | ☐ |
| 2 | (simulate) OPEN GL Posting Setup → VERIFY อ่าน code | — | GL อ่าน `code` VAT7 ได้เพื่อ map เข้าบัญชี (soft ref) | ☐ |

## G11 — Permission / Concurrency

### TC-P01 — mock user ทำได้ทุก action (permission · deferred RBAC) `[AI-DEFAULT ← OQ-TAX-06]`
- group: Permission · ความสำคัญ: กลาง · trace: §5.3 tax_admin allow-all · OQ-TAX-06 `[AI-DEFAULT]`
- actor (role): tax_admin (mock เปิดหมด)
- Setup: role=tax_admin · seed=10 · files=—
- Start: OPEN `#/tax-codes`
- ผ่านเมื่อ: ทุกปุ่ม action ปรากฏและใช้ได้ (RBAC จริง deferred — note)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม action บนหน้า list | — | เห็นและกดได้: **สร้างรหัสภาษี** · **นำเข้า CSV** · **ส่งออก CSV** · แก้ไข (รายแถว) · bulk (สถานะ/ลบ) | ☐ |
| 2 | VERIFY view drawer | — | มีปุ่ม แก้ไข + เปลี่ยนสถานะ ใช้ได้ | ☐ |

> หมายเหตุ: prototype = mock user เดียวเปิดหมด. role-gate จริงต่อ action (ใครสร้าง/แก้/นำเข้า) **deferred → OQ-TAX-06** `[AI-DEFAULT]`. เคส deny ต่อ role ทำไม่ได้บน prototype (ไม่มี RBAC) — ทดสอบตอน production ที่มี JWT/role.

### TC-CC01 — สร้างรหัสเดียวกันพร้อมกัน (concurrency · EC-A3 · ต้อง simulate) `[AI-DEFAULT]`
- group: Concurrency · ความสำคัญ: กลาง · trace: EC-A3 / BR-01 / ERR_CODE_DUPLICATE 409 `[AI-DEFAULT ← OQ-TAX-CONCURRENCY]`
- Setup: role=tax_admin ×2 session · seed=10 · files=— · **(ต้อง simulate — ยิง POST /tax-codes code เดียวกัน 2 ครั้งพร้อมกัน; prototype ไม่มี backend)**
- Start: (production API) POST /tax-codes ×2 code="VATCC"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) ยิง POST 2 request พร้อมกัน code="VATCC" | — | request แรกสำเร็จ 201 · request ที่สอง **409 ERR_CODE_DUPLICATE** (DB unique `(tenant_id, lower(code))` กัน race) — `[AI-DEFAULT]` | ☐ |
| 2 | OPEN `#/tax-codes` → VERIFY | — | มี VATCC เพียง **1** แถว (ไม่ซ้ำ) | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. โหลด `f-taxcode.html` ในเบราว์เซอร์ → ทุกเคสเริ่มด้วย `OPEN #/tax-codes` (refresh หน้าเพื่อรีเซ็ต state ก่อนเคสใหม่ — overlay ไม่ refresh-safe).
2. ทำ step ตามลำดับ; แต่ละ step อ่าน **Action** (verb tag + target ที่เห็น), ป้อน **Input** ตาม Data Sets, แล้วตรวจ **Expected** จากสิ่งที่ปรากฏบนจอ. ติ๊ก `Result` เป็น pass/fail.
3. **เคส `(ต้อง simulate)`**: runner ต้องเตรียมตาม `Setup:` (patch `BULK_SAMPLE`, ปลด `disabled` ผ่าน devtools, หรือ backend/downstream จริง). ถ้าทำไม่ได้ → mark **blocked** พร้อม note เหตุผล.
4. ข้อความบนจอเทียบ **verbatim** กับ Expected (รวมเครื่องหมาย " " โค้งใน 4 toast ที่มีชื่อ record, en-dash `–` ใน"0–100", และ `·` คั่น). ถ้าต่าง = fail + บันทึกข้อความจริงที่เห็นใน `evidence`.
5. จบทุกเคส → กรอก Result Report (schema) ส่งกลับ.

---

## Coverage Audit

| หมวด | covered / total |
|---|---|
| Acceptance Criteria (AC-01..19) | 19 / 19 |
| Business Rules (BR-01..10) | 10 / 10 |
| Field Validation (VR-01..05, VR-06..11 import) | 11 / 11 |
| Edge Cases confirmed (EC-01..08) | 8 / 8 |
| Import error codes (6) | 6 / 6 |
| API error catalog (มีผลบน UI) | 4 / 9 (5 backend-only ข้าม) |
| Permission cells (mock scope) | 2 / 2 (deny-by-role deferred) |
| State transitions (free 3-value) | ครบ (single + bulk + default) |
| Scope Lock (LOCK) | 9 / 9 |
| Cross-Module (XT-01..04) | 4 / 4 |
| Cross-cutting / states / events | ครบ (empty×2, loading, esc chain, BOM, audit, no-notif) |

- Cross-Module (XT): **4 / 4**
- Scope Lock (LOCK): **9 / 9**
- **Manifest cross-check (FRD §0.12): ✅ Stories 10/10 · Rules 10/10 · Edges confirmed 8/8**

### ข้าม (พร้อมเหตุผล)
- **API errors** ERR_NOT_AUTHENTICATED(401)/ERR_INSUFFICIENT_ROLE(403)/ERR_NOT_FOUND(404)/ERR_STALE_DATA(409)/ERR_DUPLICATE_IDEMPOTENCY_KEY(409) — backend-only, ไม่มีผลสังเกตบน UI prototype (401/403 = deferred OQ-TAX-06; stale/idempotency = `[AI-DEFAULT]` optimistic-lock/Idempotency-Key ระดับ API). ทดสอบตอน production API.
- **EC-A7** (ลบตัวปลายทางอ้างจริงแต่ used mock=0) — พึ่ง real `used` sync จาก backend (**OQ-TAX-04** blocking) ตรวจบน prototype ไม่ได้.
- **EC-A1/A2** (CSV encoding/header/พันแถว) — parser จริง (OQ-TAX-IMPORT-PARSE); mock ข้ามขั้น parse.
- **role deny cells** (consumer/อื่นทำ write ไม่ได้) — RBAC จริง deferred **OQ-TAX-06** `[AI-DEFAULT]`, mock เปิดหมด.
- **Out of Scope (นอกขอบเขต/LOCK Exclusions)** — ไม่สร้างเคส: effective date/validity (OQ-TAX-02), เพิ่ม/แก้ประเภทภาษี (LOCK-TYPE-3), ผูกเลข GL ในหน้านี้ (LOCK-NO-GL), ลบรายตัว (LOCK-BULK-DEL), ส่งอนุมัติ (LOCK-DOA-NULL), NOTIF emit (LOCK-NO-NOTIF). LOCK เหล่านี้ verify แบบ **absence** ที่ G9/G10 แทน.

### [AI-DEFAULT] ที่ propagate เข้าเคส (ผล fail อาจแปลว่า "default ผิด" ไม่ใช่ "โค้ดผิด")
- **BR-02 rate precision numeric(5,2)** `[AI-DEFAULT ← EC-A5]` → TC-C06, TC-I06 (ทศนิยม 0.75 เก็บ 2 ตำแหน่ง)
- **EC-A3 concurrent unique → 409** `[AI-DEFAULT ← OQ-TAX-CONCURRENCY]` → TC-CC01
- **RBAC deferred, mock เปิดหมด** `[AI-DEFAULT ← OQ-TAX-06]` → TC-P01
- **COSO Approver = N/A** `[AI-DEFAULT ← BRD §5]` → TC-K03

---

## Result Report (schema)

```json
{
  "feature_id": "F-TAX",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 72, "pass": 0, "fail": 0, "blocked": 0 }
}
```

> `evidence` = ข้อความ/สิ่งที่ agent **เห็นจริง** ตอน fail/blocked (เช่น toast จริงที่ต่างจาก verbatim, error code ที่แสดง, route ที่ค้าง). `note` = หมายเหตุเสริม (เช่น "blocked: patch BULK_SAMPLE ไม่ได้").
> เคส `(ต้อง simulate)` ที่รันไม่ได้บน prototype ล้วน → mark **blocked** ไม่ใช่ fail: TC-E04, TC-L13, TC-I09..I12, TC-I14, TC-XT01..XT04, TC-CC01.





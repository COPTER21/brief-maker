# AI Test Cases — F-CUSTOMER Core CRM Customer

ชุดทดสอบสำหรับ AI agent (browser-use / vision) อ่านแล้วลงมือทดสอบบนหน้าจอจริง แล้วรายงานผลกลับตาม
สคีมาท้ายไฟล์. ทุกเคส independent — เริ่มจาก `Start` route ของตัวเอง. anchor ทั้งหมด ground จาก 01_UI
(ยังไม่มีไฟล์ HTML ต้นทางในรอบนี้ — จุดที่ต้องยืนยันกับ UI จริงติดธง `⚠ ยืนยัน anchor`).

## Meta
| คีย์ | ค่า |
|---|---|
| Feature ID | F-CUSTOMER |
| ชื่อฟีเจอร์ | Core CRM Customer (CRM-CUSTOMER-001) |
| เวอร์ชัน | FRD 1.0 |
| App entry | `core.cube.com/CRM/Customer` |
| Routes | `#/list` · `#/view/:id` · `#/create` · `#/edit/:id` · modal overlays P-05/P-06/P-07 |
| ที่มา | FRD F-CUSTOMER (06_TESTS, 05_RULES, 01_UI, 00_OVERVIEW) · BRD v1.0 |
| จำนวน | 85 เคส · 13 กลุ่ม |

## Coverage
| กลุ่ม (group) | เคส | ความสำคัญเด่น |
|---|---|---|
| L · รายการ/ค้นหา/กรอง (P-01) | TC-L01..L08 | สูง-กลาง |
| C · สร้าง + identity validation (P-03) | TC-C01..C11 | สูง |
| A · ที่อยู่ + cascade (P-03/04) | TC-A01..A09 | สูง |
| B · บัญชีธนาคาร (P-04) | TC-B01..B06 | สูง-กลาง |
| P · สิทธิ์รายฟิลด์/action | TC-P01..P08 | สูง |
| V · View Drawer + Activity (P-02) | TC-V01..V05 | กลาง |
| CNV · Convert จาก Prospect (P-06→03) | TC-CNV01..07 | สูง (critical) |
| IMP · นำเข้า CSV (P-07) | TC-IMP01..09 | สูง |
| BLK · Bulk + Archive (P-05) | TC-BLK01..07 + TC-ARC01 | สูง-กลาง |
| EXP · Export | TC-EXP01..03 | กลาง |
| STA · State transition | TC-STA01..02 | กลาง |
| UX · interaction/dirty | TC-UX01..05 | กลาง |
| X · cross-cutting security | TC-X01..04 | สูง |

## Coverage Ledger

### FR (06_TESTS)
| item | cases |
|---|---|
| FR-01 Create Company | TC-C01, TC-C03, TC-C04, TC-V01 |
| FR-02 Create Individual | TC-C02, TC-C05, TC-V04 |
| FR-03 Multiple Addresses | TC-A01..A07 |
| FR-04 Convert (atomic) ⭐ | TC-CNV01..07 |
| FR-05 Bulk Import CSV | TC-IMP01..09 |
| FR-06 Finance Edit Bank | TC-B01..B06, TC-P01 |
| FR-07 Bulk Archive | TC-BLK01..07, TC-ARC01 |
| FR-08 Export Filtered | TC-EXP01..03 |
| FR-09 View Activity Log | TC-V02, TC-V03 |
| FR-10 Dirty Check | TC-UX01, TC-UX02 |

### Business Rules (05_RULES)
| rule | cases |
|---|---|
| R-IDN-01 company→legal_name+tax_id req | TC-C01, TC-C03 |
| R-IDN-02 individual req fields | TC-C02, TC-C05 |
| R-IDN-03 tax_id 13 digits | TC-C04 |
| R-IDN-04 national_id 13 digits | TC-C05 |
| R-IDN-05 customer_code format (atomic) | TC-C10, TC-X02 |
| R-IDN-06 customer_code immutable | TC-P08 |
| R-IDN-07 display_name auto-compute | TC-C09 |
| R-IDN-08 tax_id dup warn+override | TC-C11 |
| R-ADR-01 company ≥1 address | TC-A07 |
| R-ADR-02 individual no address ok | TC-A07 |
| R-ADR-03 address required fields | TC-A01 |
| R-ADR-04 postal auto-fill+override | TC-A01, TC-A08 |
| R-ADR-05/06 cascade district∈prov, sub∈dist | TC-A02 |
| R-ADR-07 change province clears children | TC-A03 |
| R-ADR-08 exactly 1 billing | TC-A05 |
| R-ADR-09 exactly 1 primary shipping | TC-A04 |
| R-ADR-10 delete primary→auto-promote | TC-A06 |
| R-ADR-11 address format export | TC-EXP03, TC-V01 |
| R-BNK-01 bank optional | TC-A07 (individual no bank) |
| R-BNK-02 ≥1 bank→exactly 1 primary | TC-B01 |
| R-BNK-03 account 10-15 digits auto-strip | TC-B02, TC-B03 |
| R-BNK-04 bank_code∈master | TC-B04 |
| R-BNK-05 account encrypted at rest | TC-X04 (skip-UI) |
| R-BNK-06 masked display | TC-B05 |
| R-BNK-07 delete primary bank→auto-promote | TC-B06 |
| R-CNV-01 converted hidden in browse | TC-CNV04 |
| R-CNV-02 convert atomic rollback | TC-CNV02 |
| R-CNV-03 lead_source locked=prospect_convert | TC-CNV01, TC-CNV05 |
| R-CNV-04 callback contract locked | TC-CNV02/03 (สังเกตผลปลายทาง) |
| R-CNV-05 onCancel only on cancel | TC-CNV03 |
| R-CNV-06 spam-click guard 220ms | TC-CNV02 (สังเกต) |
| R-PRM-01 sales_rep scope own/team | TC-P07 |
| R-PRM-02 RLS multi-tenant | TC-X01 |
| R-PRM-03 archived visible only by filter | TC-L04 |
| R-PRM-04 export = visible filter only | TC-EXP01 |
| R-IMP-01 UTF-8 (BOM ok) | TC-IMP02 |
| R-IMP-02 required headers | TC-IMP03 |
| R-IMP-03/04 per-row required+id format | TC-IMP06 |
| R-IMP-05/06 best-effort addr/bank parse | TC-IMP02 (สังเกต preview) |
| R-IMP-07 placeholder row skip | TC-IMP02 |
| R-IMP-08 template ≥1 sample/type | TC-IMP01 |
| R-IMP-09 export filename pattern | TC-EXP01 |
| R-IMP-10 ≤5,000 rows | TC-IMP05 |
| R-UX-01/02 drawer vs modal sizes | TC-C01, TC-CNV01 (สังเกต) |
| R-UX-03 3 close methods | TC-UX03 |
| R-UX-04 dirty check | TC-UX01 |
| R-UX-05 Ctrl+S save | TC-UX04 |
| R-UX-06/07 scroll/focus preserve | TC-UX (สังเกต) — ข้ามเชิงลึก |
| R-UX-08 ≤8 columns | TC-L01 |
| R-UX-09 smart pagination ellipsis | TC-L07 |
| R-UX-10 empty state ทุก list | TC-L03, TC-L08, TC-V03 |
| R-STA-01 archived→vip forbidden | TC-STA02 |
| R-STA-02 convert→active always | TC-CNV02 |
| R-STA-03 suspended→active needs note | TC-STA01 |

### Edge Cases
| EC | cases / สถานะ |
|---|---|
| EC-01 identity switch after save | TC-P08 |
| EC-02 dup tax_id across tenants | TC-X01 (allowed by RLS) |
| EC-03 convert while module down | TC-CNV06 |
| EC-04 bulk archive w/ active invoice | — ข้าม (Phase 1 ไม่ตรวจ; Finance ยังไม่มี) |
| EC-05 dup tax_id within CSV | TC-IMP07 |
| EC-06 cascade master deprecated | — ข้าม (ต้อง seed master deprecated; backend) |
| EC-07 converted w/ deleted prospect | — ข้าม (Phase 2 hard-delete) |
| EC-08 dirty + network timeout | TC-UX05? → จริง ๆ ข้าม (ต้อง simulate timeout) |
| EC-09 long address line | TC-A09 |
| EC-10 concurrent edit | — ข้าม (Phase 2 optimistic lock) |
| EC-11 master not loaded (skeleton) | TC-A01 (สังเกต loading) — ข้ามเชิงลึก |
| EC-12 encryption key lost | TC-V05 (กรณีไม่มีสิทธิ์/decrypt fail) — partial |
| EC-13 postal override conflict | TC-A08 |
| EC-14 bulk selection across pages | TC-BLK03 |
| EC-15 large CSV export | — ข้าม (Phase 1 sync; ต้อง seed 10k) |

### Error Codes (catalog)
| error | cases |
|---|---|
| VALIDATION_FAILED | TC-B02 |
| MISSING_REQUIRED_FIELD | TC-C03 |
| INVALID_TAX_ID_FORMAT | TC-C04 |
| INVALID_NATIONAL_ID_FORMAT | TC-C05 |
| INVALID_EMAIL_FORMAT | TC-C06 |
| INVALID_FIELD_FOR_ROLE | TC-P02 |
| IMMUTABLE_FIELD | TC-P08 |
| INVALID_FK_CODE | TC-B04 |
| CASCADE_VIOLATION | TC-A02 |
| MULTIPLE_PRIMARY_VIOLATION | TC-A04/A05 (UI กันไว้) |
| FILE_TOO_LARGE | TC-IMP04 |
| INVALID_FILE_TYPE | TC-IMP09 |
| MISSING_REQUIRED_HEADERS | TC-IMP03 |
| ROW_LIMIT_EXCEEDED | TC-IMP05 |
| NO_DATA_TO_EXPORT | TC-EXP02 |
| INVALID_QUERY_PARAM | — ข้าม (filter UI จำกัดค่าให้อยู่แล้ว) |
| DUPLICATE_TAX_ID | TC-C11 |
| DUPLICATE_EMAIL | TC-C11 (แนวเดียวกัน — warn) |
| ALREADY_ARCHIVED | TC-BLK05 |
| IDEMPOTENCY_KEY_REUSED | — ข้าม (header-level, backend) |
| CONCURRENT_UPDATE | — ข้าม (Phase 2) |
| PROSPECT_ALREADY_CONVERTED | TC-CNV04 |
| STATE_TRANSITION_FORBIDDEN | TC-STA02 |
| NOTE_REQUIRED_FOR_TRANSITION | TC-STA01 |
| CUSTOMER_TYPE_LOCKED | TC-P08 |
| COUNTER_OVERFLOW | — ข้าม (extreme: 10000/วัน) |
| UNAUTHORIZED/SESSION_EXPIRED | — ข้าม (auth layer ทั่วระบบ) |
| FORBIDDEN | TC-P05 |
| INSUFFICIENT_PERMISSION | TC-V05 |
| TENANT_MISMATCH | TC-X01 (defense in depth) |
| CUSTOMER_NOT_FOUND | TC-X01 |
| ADDRESS/BANK/PROSPECT_NOT_FOUND | — ข้าม (deep-link ลบแล้ว; ขอบเขตน้อย) |
| 5xx (INTERNAL/CODE_GEN/IMPORT/DECRYPT/EVENT/MASTER/SERVICE) | — ข้าม (ต้อง fault-inject; backend) |
| RATE_LIMIT_EXCEEDED | — ข้าม (load) |

### Permission Matrix (role × action/field) — §5.5/§6.2.6
| cell | cases |
|---|---|
| finance edit credit_limit = allow | TC-P01 |
| finance edit legal_name = deny | TC-P02 |
| cs edit contact_email = allow | TC-P03 |
| cs add bank = deny | TC-P04 |
| sales_rep bulk-archive = deny | TC-P05 |
| auditor read activity = allow; create = deny | TC-P06 |
| sales_rep scope own = enforce | TC-P07 |
| immutable fields = deny all | TC-P08 |

### Cross-cutting / Events / States
| item | cases |
|---|---|
| RLS cross-tenant 404 | TC-X01 |
| customer_code per-tenant counter | TC-X02 |
| encryption at rest (SQL) | TC-X04 — ข้าม (ไม่ใช่ UI) |
| event customer.created/updated/archived/converted/bulk_* | สังเกตผ่าน toast/ผลปลายทางใน TC-C01, TC-CNV02, TC-BLK04, TC-IMP02 |
| empty/filtered-empty/error/loading states | TC-L03, TC-L08, TC-V03 (+ loading ข้ามเชิงลึก) |

## Data Sets

### A — บริษัทถูกต้อง (company valid)
| ฟิลด์ | ค่า |
|---|---|
| ประเภท | นิติบุคคล |
| ชื่อนิติบุคคล (legal_name) | บริษัท ดับเบิ้ลบี ซิมเปิล จำกัด |
| เลขผู้เสียภาษี (tax_id) | 0105540012345 |
| customer_group | Enterprise |
| ผู้ติดต่อหลัก | คุณสไตรค์ |
| อีเมล | strike@2bsimple.co.th |
| payment_term | NET-30 |
| sales_rep | (auto จาก user) |

### B — บุคคลธรรมดาถูกต้อง (individual valid)
| ฟิลด์ | ค่า |
|---|---|
| ประเภท | บุคคลธรรมดา |
| ชื่อ (first_name) | สมหญิง |
| นามสกุล (last_name) | ใจดี |
| national_id | 1100400112345 |
| วันเกิด (date_of_birth) | 1990-05-12 |
| customer_group | Retail |
| ผู้ติดต่อหลัก | สมหญิง ใจดี |
| อีเมล | somying@example.com |
| payment_term | CASH |

### C — บริษัท ข้อมูลผิด (negative)
| ฟิลด์ | ค่า |
|---|---|
| ประเภท | นิติบุคคล |
| ชื่อนิติบุคคล | (เว้นว่าง) |
| tax_id | 12345 (ผิด: ไม่ครบ 13 หลัก) |
| อีเมล | strike[at]2bsimple |

### D — ที่อยู่ถูกต้อง ต่างจังหวัด
| ฟิลด์ | ค่า |
|---|---|
| label | สำนักงานใหญ่ |
| address_line | 99 หมู่ 5 ถ.แสงชูโต |
| จังหวัด | กาญจนบุรี |
| อำเภอ | ท่ามะกา |
| ตำบล | วังขนาย |
| postal | (auto = 71120) |

### E — ที่อยู่ cascade ผิด
| ฟิลด์ | ค่า |
|---|---|
| จังหวัด | กรุงเทพมหานคร |
| อำเภอ/เขต | เลือกเขตของจังหวัดอื่นที่ไม่ใช่ กทม. (mismatch) |

### F — บัญชีธนาคารถูกต้อง
| ฟิลด์ | ค่า |
|---|---|
| ธนาคาร | กสิกรไทย |
| account_number | 1234567890 (10 หลัก) |
| account_name | บริษัท ดับเบิ้ลบี ซิมเปิล จำกัด |
| สาขา | ท่ามะกา |

### G — เลขบัญชีผิด boundary
| ฟิลด์ | ค่า |
|---|---|
| สั้นไป | 12345 (5 หลัก) |
| ยาวไป | 12345678901234567890 (20 หลัก) |
| มี format | 123-4-56789-0 (ต้อง auto-strip → 10 หลัก) |

### ไฟล์ทดสอบ (Files) — runner เตรียมตามชื่อ (อ้าง 06_TESTS §6.6.4)
| ไฟล์ | เนื้อหา | ใช้ในเคส |
|---|---|---|
| `valid_100.csv` | 100 แถวถูกต้อง (company+individual ผสม) | TC-IMP02 |
| `with_errors.csv` | 50 แถว: 40 valid + 10 error หลายชนิด | TC-IMP06 |
| `all_errors.csv` | ทุกแถว error (valid=0) | TC-IMP08 |
| `too_large.csv` | 5,001 แถว (เกิน limit) | TC-IMP05 |
| `oversize_6mb.csv` | ไฟล์ > 5 MB | TC-IMP04 |
| `bad_format.csv` | ขาด header จำเป็น | TC-IMP03 |
| `dup_in_file.csv` | มี 2 แถว tax_id ซ้ำกัน | TC-IMP07 |
| `not_a_csv.xlsx` | ไฟล์ไม่ใช่ CSV | TC-IMP09 |

---

## วิธีอ่านเคส — Action verbs (agent map 1:1)
ทุก Action ขึ้นต้นด้วย verb: **OPEN** ไป route · **CLICK** คลิกสิ่งที่เห็น · **TYPE** พิมพ์ลงช่อง ·
**SELECT** เลือก dropdown · **TOGGLE** สลับ toggle/checkbox · **UPLOAD** เลือกไฟล์ · **PRESS** คีย์ลัด ·
**VERIFY** step สังเกตล้วน. `Setup:` บอกสิ่งที่ runner ต้องเตรียมก่อนรัน (role + seed + files).
step ที่ติด `⚠ ยืนยัน anchor` = ข้อความมาจาก 01_UI ยังไม่ยืนยันกับ HTML จริง.

---

## Test Cases

### กลุ่ม L — รายการ / ค้นหา / กรอง (P-01)

#### TC-L01 — ดูรายการลูกค้า + Stats Strip + ตาราง 8 คอลัมน์ (happy)
- group: L · ความสำคัญ: สูง · trace: FR-list / R-UX-08
- actor: Sales Mgr
- Setup: role=sales_mgr · seed=ลูกค้าหลายราย (active/vip/suspended) · files=—
- Start: OPEN `#/list` · ชุดข้อมูล: — · ผ่านเมื่อ: เห็นตาราง + stats ครบ ไม่มีข้อมูลเปลี่ยน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/list` | — | breadcrumb **Home > CRM > Customer**; หัวข้อ **Customer** + จำนวนรายการ | ☐ |
| 2 | VERIFY Stats Strip ด้านบน | — | เห็น 4 การ์ด: **Total / Active / VIP / Converted this month** | ☐ |
| 3 | VERIFY หัวตาราง | — | ≤ 8 คอลัมน์: checkbox, **รหัส, ลูกค้า, ประเภท, Source, Credit, สถานะ, Actions** | ☐ |
| 4 | VERIFY ปุ่มมุมขวาบน | — | เห็นปุ่ม **Template · Import · Export · Convert · เพิ่ม Customer** | ☐ |

#### TC-L02 — ค้นหาเจอ
- group: L · ความสำคัญ: กลาง · trace: FR-list
- Setup: role=sales_mgr · seed=มีลูกค้าที่ชื่อตรงคำค้น · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: ตารางกรองเหลือเฉพาะที่ตรงคำค้น
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/list` | — | เห็นช่องค้นหา (placeholder ค้นหา) | ☐ |
| 2 | TYPE → ช่องค้นหา | ส่วนหนึ่งของชื่อลูกค้าที่มี | ตารางเหลือเฉพาะแถวที่ชื่อ/อีเมลตรงคำค้น | ☐ |

#### TC-L03 — ค้นหาไม่เจอ → filtered-empty state
- group: L · ความสำคัญ: กลาง · trace: R-UX-10
- Setup: role=sales_mgr · seed=— · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: ตารางว่าง + empty state
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/list` | — | เห็นช่องค้นหา | ☐ |
| 2 | TYPE → ช่องค้นหา | `zzzqqq123` | ตารางว่าง + ข้อความ **ไม่พบ Customer** + แนะนำล้าง filter | ☐ |

#### TC-L04 — กรองสถานะทุกค่า (archived เห็นเฉพาะตอนเลือก)
- group: L · ความสำคัญ: สูง · trace: R-PRM-03
- Setup: role=sales_mgr · seed=ลูกค้าครบทุกสถานะรวม archived ≥1 · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: แต่ละค่า filter กรองถูก; archived ซ่อนใน default
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/list` | — | ตารางไม่มีแถวสถานะ **archived** | ☐ |
| 2 | SELECT "active" → filter สถานะ | active | ทุกแถว pill = active | ☐ |
| 3 | SELECT "vip" → filter สถานะ | vip | ทุกแถว pill = vip | ☐ |
| 4 | SELECT "suspended" → filter สถานะ | suspended | ทุกแถว pill = suspended (ส้ม) | ☐ |
| 5 | SELECT "archived" → filter สถานะ | archived | แถว archived ปรากฏ (ที่ default ซ่อน) | ☐ |

#### TC-L05 — กรองประเภท/แหล่งที่มา + Reset
- group: L · ความสำคัญ: กลาง · trace: FR-list
- Setup: role=sales_mgr · seed=ลูกค้าหลายประเภท + มี source=prospect_convert · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: filter ประเภท+source ทำงาน + Reset คืนค่า
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "นิติบุคคล" → filter ประเภท | company | เหลือเฉพาะแถว pill นิติบุคคล | ☐ |
| 2 | SELECT "prospect_convert" → filter Source | prospect_convert | เหลือเฉพาะแถว badge convert | ☐ |
| 3 | CLICK ปุ่ม **Reset** | — | filter กลับค่าเริ่มต้น + ตารางแสดงครบ | ☐ |

#### TC-L06 — Sort คอลัมน์ + สลับทิศ
- group: L · ความสำคัญ: กลาง · trace: FR-list
- Setup: role=sales_mgr · seed=ลูกค้า ≥3 ราย · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: คลิกหัวคอลัมน์แล้วลำดับเปลี่ยนตามทิศ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK หัวคอลัมน์ **ลูกค้า** | — | แถวเรียงตามชื่อ (asc) + ไอคอนทิศปรากฏ | ☐ |
| 2 | CLICK หัวคอลัมน์ **ลูกค้า** (ซ้ำ) | — | ทิศสลับเป็น desc + ลำดับกลับด้าน | ☐ |

#### TC-L07 — Pagination + ellipsis
- group: L · ความสำคัญ: กลาง · trace: R-UX-09
- Setup: role=sales_mgr · seed=ลูกค้ามากกว่า 7 หน้า · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: เปลี่ยนหน้าได้ + ellipsis แสดง + filter รีหน้า
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/list` | — | แถบหน้ารูปแบบ `1 … 5 6 7 … N` (ellipsis) | ☐ |
| 2 | CLICK เลขหน้าถัดไป | — | ตารางแสดงชุดข้อมูลหน้าใหม่ + เลขหน้า active เปลี่ยน | ☐ |
| 3 | SELECT "active" → filter สถานะ | active | เด้งกลับหน้า 1 | ☐ |

#### TC-L08 — Empty state (ไม่มีข้อมูลเลย)
- group: L · ความสำคัญ: กลาง · trace: R-UX-10
- Setup: role=sales_mgr · seed=tenant ที่ยังไม่มีลูกค้า · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: เห็น empty state + ชวนสร้าง
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/list` | — | empty state ไอคอน + ข้อความ **ไม่พบ Customer** + ปุ่ม/คำแนะนำให้สร้าง | ☐ |

### กลุ่ม C — สร้าง + Identity Validation (P-03)

#### TC-C01 — สร้างลูกค้านิติบุคคลครบฟิลด์ (happy)
- group: C · ความสำคัญ: สูง · trace: FR-01 / R-IDN-01,03,05,07 / R-UX-02 / event customer.created
- actor: Sales Rep
- Setup: role=sales_rep · seed=— · files=—
- Start: OPEN `#/list` แล้ว CLICK **เพิ่ม Customer** (หรือ OPEN `#/create`) · ชุดข้อมูล: A
- ผ่านเมื่อ: บันทึกได้ + toast code `CUST-YYYYMMDD-XXXX` + กลับ list เห็นแถวใหม่บนสุด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **เพิ่ม Customer** | — | drawer 540px เปิดจากขวา หัวข้อ **เพิ่ม Customer ใหม่**; ประเภท default **นิติบุคคล** | ☐ |
| 2 | VERIFY ด้านบน drawer | — | ช่อง **Customer Code** read-only (auto-generated) | ☐ |
| 3 | TYPE → ช่อง **ชื่อนิติบุคคล** | A | ช่องแสดงค่า | ☐ |
| 4 | TYPE → ช่อง **เลขผู้เสียภาษี** | A: 0105540012345 | ช่องแสดง 13 หลัก | ☐ |
| 5 | SELECT "Enterprise" → **customer_group** | A | dropdown แสดงค่าที่เลือก | ☐ |
| 6 | TYPE → **ผู้ติดต่อหลัก** + **อีเมล** | A | ช่องแสดงค่า | ☐ |
| 7 | SELECT "NET-30" → **payment_term** | A | แสดงค่า | ☐ |
| 8 | CLICK ปุ่ม **บันทึก** | — | drawer ปิด + toast **สร้าง Customer สำเร็จ — CUST-…** + route `#/list` | ☐ |
| 9 | VERIFY แถวบนสุด | — | ชื่อบริษัทที่สร้าง + pill ประเภท **นิติบุคคล** | ☐ |

#### TC-C02 — สร้างลูกค้าบุคคลธรรมดา (happy, national_id masked)
- group: C · ความสำคัญ: สูง · trace: FR-02 / R-IDN-02,04 / mask
- Setup: role=sales_rep · seed=— · files=—
- Start: OPEN `#/create` · ชุดข้อมูล: B · ผ่านเมื่อ: บันทึกได้ + list เห็น pill **บุคคล**
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/create` | — | drawer เปิด | ☐ |
| 2 | CLICK ตัวเลือก **บุคคลธรรมดา** | — | ฟอร์ม Identity เปลี่ยนเป็น first/last/national_id/วันเกิด | ☐ |
| 3 | TYPE → **ชื่อ** + **นามสกุล** | B | display_name auto = "สมหญิง ใจดี" | ☐ |
| 4 | TYPE → **national_id** | B: 1100400112345 | ช่องรับค่า | ☐ |
| 5 | SELECT วันเกิด | B: 1990-05-12 | แสดงวันที่ | ☐ |
| 6 | TYPE → **อีเมล** + **ผู้ติดต่อหลัก** | B | ช่องแสดงค่า | ☐ |
| 7 | CLICK ปุ่ม **บันทึก** | — | toast สำเร็จ + list มีแถวใหม่ pill **บุคคล** | ☐ |

#### TC-C03 — บริษัทเว้น legal_name/tax_id (negative, required)
- group: C · ความสำคัญ: สูง · trace: R-IDN-01 / MISSING_REQUIRED_FIELD
- Setup: role=sales_rep · seed=— · files=—
- Start: OPEN `#/create` · ชุดข้อมูล: C · ผ่านเมื่อ: บันทึกไม่ผ่าน + เตือนช่องจำเป็น
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/create` (ประเภท นิติบุคคล) | — | ช่อง ชื่อนิติบุคคล + เลขผู้เสียภาษี ว่าง | ☐ |
| 2 | TYPE → **อีเมล** เท่านั้น | C | กรอกอีเมล | ☐ |
| 3 | CLICK ปุ่ม **บันทึก** | — | ไม่ผ่าน (drawer ยังเปิด) + เตือน required ใต้ช่องที่จำเป็น | ☐ |

#### TC-C04 — tax_id ผิดรูปแบบ (negative)
- group: C · ความสำคัญ: สูง · trace: R-IDN-03 / INVALID_TAX_ID_FORMAT
- Setup: role=sales_rep · seed=— · files=—
- Start: OPEN `#/create` · ชุดข้อมูล: C · ผ่านเมื่อ: เตือน format ที่ช่องเลขภาษี
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → legal_name + อีเมลถูก | A | ช่องแสดงค่า | ☐ |
| 2 | TYPE → **tax_id** | C: 12345 | ช่องรับค่า | ☐ |
| 3 | CLICK ปุ่ม **บันทึก** | — | ไม่ผ่าน + ใต้ **เลขผู้เสียภาษี** แจ้งต้อง 13 หลัก | ☐ |

#### TC-C05 — national_id ผิดรูปแบบ (negative)
- group: C · ความสำคัญ: สูง · trace: R-IDN-04 / INVALID_NATIONAL_ID_FORMAT
- Setup: role=sales_rep · seed=— · files=—
- Start: OPEN `#/create` (บุคคลธรรมดา) · ผ่านเมื่อ: เตือน format national_id
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ตัวเลือก **บุคคลธรรมดา** | — | ฟอร์มเปลี่ยน | ☐ |
| 2 | TYPE → first/last/อีเมลถูก | B | ช่องแสดงค่า | ☐ |
| 3 | TYPE → **national_id** | `99` | ช่องรับค่า | ☐ |
| 4 | CLICK ปุ่ม **บันทึก** | — | ไม่ผ่าน + เตือนต้อง 13 หลัก | ☐ |

#### TC-C06 — อีเมลผิดรูปแบบ (negative)
- group: C · ความสำคัญ: สูง · trace: INVALID_EMAIL_FORMAT
- Setup: role=sales_rep · seed=— · files=—
- Start: OPEN `#/create` · ชุดข้อมูล: C · ผ่านเมื่อ: เตือน format อีเมล
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ฟิลด์จำเป็นถูก | A | ช่องแสดงค่า | ☐ |
| 2 | TYPE → **อีเมล** | C: strike[at]2bsimple | ช่องรับค่า | ☐ |
| 3 | CLICK ปุ่ม **บันทึก** | — | ไม่ผ่าน + ใต้ **อีเมล** แจ้งรูปแบบไม่ถูกต้อง | ☐ |

#### TC-C07 — ฟิลด์จำเป็นร่วมว่าง (negative)
- group: C · ความสำคัญ: กลาง · trace: R-IDN / MISSING_REQUIRED_FIELD
- Setup: role=sales_rep · seed=— · files=—
- Start: OPEN `#/create` · ผ่านเมื่อ: เตือนทุกช่องจำเป็นที่เว้น
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ชื่อ+tax_id+อีเมลถูก เว้น customer_group/payment_term/ผู้ติดต่อหลัก | A (บางส่วน) | ช่องที่เว้นว่าง | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | — | ไม่ผ่าน + เตือน required ที่ 3 ช่อง | ☐ |

#### TC-C08 — วันเกิด boundary (อนาคต / เกิน 120 ปี)
- group: C · ความสำคัญ: กลาง · trace: R-IDN-02 (dob ≤ today, ≥ today-120y)
- Setup: role=sales_rep · seed=— · files=—
- Start: OPEN `#/create` (บุคคลธรรมดา) · ผ่านเมื่อ: ปฏิเสธวันเกินขอบ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT วันเกิด = วันพรุ่งนี้ | (อนาคต) | เตือน/เลือกไม่ได้ หรือบันทึกไม่ผ่าน | ☐ |
| 2 | SELECT วันเกิด = `1800-01-01` | เกิน 120 ปี | เตือน/ปฏิเสธ | ☐ |

#### TC-C09 — display_name auto-compute (R-IDN-07)
- group: C · ความสำคัญ: กลาง · trace: R-IDN-07
- Setup: role=sales_rep · seed=— · files=—
- Start: OPEN `#/create` · ผ่านเมื่อ: เว้น display_name แล้วระบบเติม
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → legal_name (เว้น display_name) | A | ช่องแสดงค่า | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | — | รายการแสดง display_name = legal_name | ☐ |

#### TC-C10 — Customer Code รูปแบบ + อ่านอย่างเดียว (R-IDN-05/06)
- group: C · ความสำคัญ: สูง · trace: R-IDN-05,06
- Setup: role=sales_rep · seed=— · files=—
- Start: OPEN `#/create` · ผ่านเมื่อ: code อยู่รูป `CUST-YYYYMMDD-XXXX` และแก้ไม่ได้
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง Customer Code | — | แสดงรูป `CUST-YYYYMMDD-XXXX` (read-only + ปุ่มคัดลอก) | ☐ |
| 2 | CLICK ช่อง code แล้วลองพิมพ์ | — | แก้ไม่ได้ (ช่องล็อก) | ☐ |

#### TC-C11 — tax_id ซ้ำ → เตือนแต่ override ได้ (warning)
- group: C · ความสำคัญ: กลาง · trace: R-IDN-08 / DUPLICATE_TAX_ID
- Setup: role=sales_rep · seed=ลูกค้าที่ใช้ tax_id 0105540012345 อยู่แล้ว · files=—
- Start: OPEN `#/create` · ชุดข้อมูล: A · ผ่านเมื่อ: เตือนซ้ำ + ยืนยันแล้วบันทึกได้
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ฟิลด์ถูก + **tax_id** ที่มีอยู่แล้ว | A: 0105540012345 | ช่องแสดงค่า | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | — | คำเตือน **มีเลขผู้เสียภาษีนี้อยู่แล้ว** (เตือน ไม่บล็อก) | ☐ |
| 3 | CLICK ยืนยัน override | — | บันทึกสำเร็จ + toast | ☐ |

### กลุ่ม A — ที่อยู่ + Cascade (P-03/P-04)

#### TC-A01 — เพิ่มที่อยู่ cascade ถูก + postal auto-fill (happy)
- group: A · ความสำคัญ: สูง · trace: FR-03 / R-ADR-03,04,05,06
- Setup: role=sales_rep · seed=master ที่อยู่ subset (กาญจนบุรี) โหลดได้ · files=—
- Start: OPEN `#/create` · ชุดข้อมูล: D · ผ่านเมื่อ: เลือกครบลำดับ + postal เติมเอง
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **เพิ่มที่อยู่** | — | การ์ดที่อยู่ใหม่ + dropdown จังหวัด/อำเภอ/ตำบล + postal | ☐ |
| 2 | TYPE → **address_line** | D | ช่องแสดงค่า | ☐ |
| 3 | SELECT "กาญจนบุรี" → **จังหวัด** | D | dropdown อำเภอ enable เฉพาะอำเภอกาญจนบุรี | ☐ |
| 4 | SELECT "ท่ามะกา" → **อำเภอ** | D | dropdown ตำบล enable เฉพาะตำบลท่ามะกา | ☐ |
| 5 | SELECT "วังขนาย" → **ตำบล** | D | ช่อง **postal** เติมอัตโนมัติ (71120) | ☐ |

#### TC-A02 — cascade ไม่ตรง → CASCADE_VIOLATION (negative)
- group: A · ความสำคัญ: สูง · trace: R-ADR-05,06 / CASCADE_VIOLATION
- Setup: role=sales_rep · seed=master โหลดได้ · files=— · หมายเหตุ: ถ้า UI บังคับ cascade จน mismatch เลือกไม่ได้ ให้ทดสอบผ่าน import/payload (mark BLOCKED ถ้าทำบน UI ล้วนไม่ได้)
- Start: OPEN `#/create` · ชุดข้อมูล: E · ผ่านเมื่อ: ระบบกันอำเภอที่ไม่อยู่ในจังหวัด
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "กรุงเทพมหานคร" → **จังหวัด** | E | อำเภอ/เขตของ กทม. ปรากฏ | ☐ |
| 2 | VERIFY ว่าเลือกอำเภอนอกจังหวัดได้หรือไม่ | — | dropdown ให้เลือกได้เฉพาะของ กทม. (UI กัน mismatch) ⚠ ยืนยัน anchor | ☐ |
| 3 | CLICK ปุ่ม **บันทึก** (เฉพาะถ้าส่ง mismatch ได้) | E | ไม่ผ่าน + ข้อความ **อำเภอไม่อยู่ในจังหวัดที่เลือก** (CASCADE_VIOLATION) | ☐ |

#### TC-A03 — เปลี่ยนจังหวัด → child เคลียร์ (R-ADR-07)
- group: A · ความสำคัญ: กลาง · trace: R-ADR-07
- Setup: role=sales_rep · seed=master โหลดได้ · files=—
- Start: OPEN `#/create` · ผ่านเมื่อ: เปลี่ยน parent แล้ว child ว่าง
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT จังหวัด→อำเภอ→ตำบล จน postal เติม | D | ทุกช่องมีค่า | ☐ |
| 2 | SELECT "กรุงเทพมหานคร" → **จังหวัด** (เปลี่ยน) | — | อำเภอ + ตำบล + postal ถูกล้างเป็นว่าง | ☐ |

#### TC-A04 — สองที่อยู่: toggle primary shipping แย่งกัน (R-ADR-09)
- group: A · ความสำคัญ: สูง · trace: R-ADR-09 / MULTIPLE_PRIMARY_VIOLATION (UI กัน)
- Setup: role=sales_rep · seed=— · files=—
- Start: OPEN `#/create` · ผ่านเมื่อ: เปิด primary ใบ 2 → ใบ 1 หลุด
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มที่อยู่** ×2 (ใบ 1 จัดส่งหลัก=เปิด) | D ×2 | ใบ 1 มี badge **จัดส่งหลัก** | ☐ |
| 2 | TOGGLE "ตั้งเป็นจัดส่งหลัก" (การ์ดที่ 2) | — | ใบ 2 ได้ badge จัดส่งหลัก และใบ 1 หลุด badge | ☐ |

#### TC-A05 — billing มีได้ใบเดียว (R-ADR-08)
- group: A · ความสำคัญ: กลาง · trace: R-ADR-08
- Setup: role=sales_rep · seed=— · files=—
- Start: OPEN `#/create` · ผ่านเมื่อ: เปิด billing ใบ 2 → ใบ 1 หลุด
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มที่อยู่** ×2 (ใบ 1 billing=เปิด) | D ×2 | ใบ 1 badge **ที่อยู่เรียกเก็บเงิน** | ☐ |
| 2 | TOGGLE "ที่อยู่เรียกเก็บเงิน" (การ์ดที่ 2) | — | ใบ 2 ได้ badge billing, ใบ 1 หลุด | ☐ |

#### TC-A06 — ลบ primary address → auto-promote (R-ADR-10)
- group: A · ความสำคัญ: กลาง · trace: R-ADR-10
- Setup: role=sales_mgr · seed=ลูกค้า 1 รายมี ≥2 ที่อยู่ (ใบ 1 = จัดส่งหลัก) · files=—
- Start: OPEN `#/edit/:id` · ผ่านเมื่อ: ลบใบ primary แล้วใบถัดไปขึ้น primary
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/edit/:id` | — | เห็น 2 การ์ดที่อยู่ | ☐ |
| 2 | CLICK ไอคอนถังขยะ (การ์ดที่ 1) | — | เหลือ 1 ใบ และใบที่เหลือถูกตั้ง **จัดส่งหลัก** อัตโนมัติ | ☐ |

#### TC-A07 — company ต้องมี ≥1 ที่อยู่ / individual ไม่บังคับ (R-ADR-01/02, R-BNK-01)
- group: A · ความสำคัญ: สูง · trace: R-ADR-01,02 / R-BNK-01
- Setup: role=sales_rep · seed=— · files=—
- Start: OPEN `#/create` · ผ่านเมื่อ: company เว้นที่อยู่ → error; individual เว้น → ผ่าน
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → identity นิติบุคคลครบ (ไม่เพิ่มที่อยู่) แล้ว CLICK **บันทึก** | A | ไม่ผ่าน + เตือนต้องมีที่อยู่อย่างน้อย 1 | ☐ |
| 2 | CLICK **บุคคลธรรมดา** + TYPE identity ครบ (ไม่เพิ่มที่อยู่/บัญชี) แล้ว CLICK **บันทึก** | B | บันทึกสำเร็จ (ไม่บังคับที่อยู่/ธนาคาร) | ☐ |

#### TC-A08 — postal override (edge: EC-13)
- group: A · ความสำคัญ: ต่ำ · trace: R-ADR-04 / EC-13
- Setup: role=sales_rep · seed=master โหลดได้ · files=—
- Start: OPEN `#/create` · ผ่านเมื่อ: แก้ postal ที่ auto-fill แล้วระบบยอมรับ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ตำบลจน postal เติม `71120` | D | postal = 71120 | ☐ |
| 2 | TYPE → **postal** ทับเป็น `71121` | 71121 | ช่อง postal เก็บค่าที่พิมพ์ทับ (Phase 1 ยอมรับ) | ☐ |

#### TC-A09 — address_line ยาวมาก (edge: EC-09)
- group: A · ความสำคัญ: ต่ำ · trace: EC-09
- Setup: role=sales_rep · seed=— · files=—
- Start: OPEN `#/create` · ผ่านเมื่อ: รับข้อความยาว + textarea wrap
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → **address_line** ยาว 500+ ตัวอักษร | (ข้อความยาว) | ช่องรับได้ + ตัดบรรทัด (ไม่ error) | ☐ |

### กลุ่ม B — บัญชีธนาคาร (P-04 Financial)

#### TC-B01 — เพิ่มบัญชีแรก auto primary (happy)
- group: B · ความสำคัญ: สูง · trace: FR-06 / R-BNK-02
- Setup: role=finance · seed=ลูกค้า 1 ราย (เปิด edit ได้) · files=—
- Start: OPEN `#/edit/:id` · ชุดข้อมูล: F · ผ่านเมื่อ: บัญชีแรกได้ primary อัตโนมัติ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/edit/:id` → ส่วน **บัญชีธนาคาร** → CLICK **เพิ่มบัญชี** | — | การ์ดบัญชีใหม่ + dropdown 14 ธนาคาร (preview สี) | ☐ |
| 2 | SELECT "กสิกรไทย" → ธนาคาร; TYPE → เลขบัญชี + ชื่อบัญชี | F | ช่องแสดงค่า | ☐ |
| 3 | VERIFY การ์ดบัญชี | — | มี badge **บัญชีหลัก (primary)** อัตโนมัติ (บัญชีแรก) | ☐ |

#### TC-B02 — เลขบัญชีสั้น/ยาวเกิน (boundary, negative)
- group: B · ความสำคัญ: สูง · trace: R-BNK-03 / VALIDATION_FAILED
- Setup: role=finance · seed=ลูกค้า 1 ราย · files=—
- Start: OPEN `#/edit/:id` · ชุดข้อมูล: G · ผ่านเมื่อ: ปฏิเสธความยาวนอก 10-15
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มบัญชี**; TYPE → เลขบัญชี `12345` แล้ว CLICK **บันทึก** | G สั้นไป | เตือน/ไม่ผ่าน (สั้นเกิน) | ☐ |
| 2 | TYPE → เลขบัญชี 20 หลัก แล้ว CLICK **บันทึก** | G ยาวไป | เตือน/ไม่ผ่าน (ยาวเกิน) | ☐ |

#### TC-B03 — เลขบัญชีมี format → auto-strip (R-BNK-03)
- group: B · ความสำคัญ: กลาง · trace: R-BNK-03
- Setup: role=finance · seed=ลูกค้า 1 ราย · files=—
- Start: OPEN `#/edit/:id` · ชุดข้อมูล: G · ผ่านเมื่อ: ใส่ `123-4-56789-0` แล้วผ่าน (เหลือ 10 หลัก)
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มบัญชี**; TYPE → เลขบัญชี `123-4-56789-0`; SELECT ธนาคาร; TYPE ชื่อบัญชี; CLICK **บันทึก** | G มี format | ผ่าน (ระบบตัดขีดเหลือ 10 หลัก) | ☐ |

#### TC-B04 — bank_code จำกัดเฉพาะ master (R-BNK-04)
- group: B · ความสำคัญ: กลาง · trace: R-BNK-04 / INVALID_FK_CODE
- Setup: role=finance · seed=ลูกค้า 1 ราย · files=—
- Start: OPEN `#/edit/:id` · ผ่านเมื่อ: dropdown มีเฉพาะ 14 ธนาคาร
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มบัญชี** → VERIFY dropdown ธนาคาร | — | มีเฉพาะ 14 ธนาคารใน master (เลือกนอกรายการไม่ได้) ⚠ ยืนยัน anchor | ☐ |

#### TC-B05 — แสดงเลขบัญชี masked (R-BNK-06)
- group: B · ความสำคัญ: กลาง · trace: R-BNK-06 / mask
- Setup: role=sales_mgr · seed=ลูกค้า 1 รายมีบัญชี 10 หลัก · files=—
- Start: OPEN `#/view/:id` → tab Financial · ผ่านเมื่อ: เลข 10 หลักแสดง `XXX-X-XXXXX-X`
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/view/:id` → CLICK tab **Financial** | — | เลขบัญชีแสดง `XXX-X-XXXXX-X` (โชว์หลักท้าย) | ☐ |

#### TC-B06 — ลบบัญชี primary → auto-promote (R-BNK-07)
- group: B · ความสำคัญ: กลาง · trace: R-BNK-07
- Setup: role=finance · seed=ลูกค้า 1 รายมี ≥2 บัญชี (ใบ 1 = primary) · files=—
- Start: OPEN `#/edit/:id` · ผ่านเมื่อ: ลบ primary แล้วบัญชีถัดไปขึ้น primary
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/edit/:id` | — | เห็น 2 การ์ดบัญชี | ☐ |
| 2 | CLICK ไอคอนลบ (บัญชีใบ 1) | — | เหลือ 1 ใบ ถูกตั้ง **บัญชีหลัก** อัตโนมัติ | ☐ |

### กลุ่ม P — สิทธิ์รายฟิลด์/Action (§5.5 / §6.2.6)

#### TC-P01 — finance แก้ credit_limit ได้ (allow)
- group: P · ความสำคัญ: สูง · trace: matrix finance×Financial=allow
- Setup: role=finance · seed=ลูกค้า 1 ราย · files=—
- Start: OPEN `#/edit/:id` · ผ่านเมื่อ: แก้ financial ได้ + บันทึกผ่าน
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/edit/:id` (login finance) | — | ส่วน **Financial + Bank** แก้ได้; Identity/Contact เป็น read-only/เทา | ☐ |
| 2 | TYPE → **credit_limit** แล้ว CLICK **บันทึก** | 500000 | บันทึกสำเร็จ + toast | ☐ |

#### TC-P02 — finance แก้ legal_name ถูกปฏิเสธ (permission)
- group: P · ความสำคัญ: สูง · trace: INVALID_FIELD_FOR_ROLE
- Setup: role=finance · seed=ลูกค้านิติบุคคล 1 ราย · files=—
- Start: OPEN `#/edit/:id` · ผ่านเมื่อ: ช่อง legal_name แก้ไม่ได้
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/edit/:id` (finance) → VERIFY ช่อง **ชื่อนิติบุคคล** | — | ช่อง read-only/เทา (แก้ไม่ได้) | ☐ |

#### TC-P03 — cs แก้ contact_email ได้ (allow)
- group: P · ความสำคัญ: กลาง · trace: matrix cs×Contact=allow
- Setup: role=cs · seed=ลูกค้า 1 ราย · files=—
- Start: OPEN `#/edit/:id` · ผ่านเมื่อ: แก้อีเมลได้ บันทึกผ่าน
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/edit/:id` (cs) → TYPE → **อีเมล** → CLICK **บันทึก** | new@example.com | สำเร็จ; ส่วน Financial/Bank ไม่ให้แก้ | ☐ |

#### TC-P04 — cs เพิ่มบัญชีธนาคารถูกปฏิเสธ (permission)
- group: P · ความสำคัญ: กลาง · trace: cs×Bank=deny / FORBIDDEN
- Setup: role=cs · seed=ลูกค้า 1 ราย · files=—
- Start: OPEN `#/edit/:id` · ผ่านเมื่อ: ไม่มีปุ่มเพิ่มบัญชี/ถูกปฏิเสธ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/edit/:id` (cs) → VERIFY ส่วนบัญชีธนาคาร | — | ส่วนบัญชี/ปุ่มเพิ่มบัญชีไม่ปรากฏ (หรือ disabled) ⚠ ยืนยัน anchor | ☐ |

#### TC-P05 — sales_rep กด bulk-archive ถูกปฏิเสธ (permission)
- group: P · ความสำคัญ: สูง · trace: §6.2.6 sales_rep×bulk-archive=403 / FORBIDDEN
- Setup: role=sales_rep · seed=ลูกค้าของ sales_rep ≥2 ราย · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: ไม่มีปุ่ม Archive selected/ถูกปฏิเสธ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/list` (sales_rep) → TOGGLE checkbox 1 แถว → VERIFY Bulk Bar | — | ปุ่ม **Archive selected** ไม่ปรากฏ/disabled ⚠ ยืนยัน anchor | ☐ |

#### TC-P06 — auditor อ่าน activity ได้ แต่สร้างไม่ได้ (permission)
- group: P · ความสำคัญ: กลาง · trace: auditor read=allow / create=deny
- Setup: role=auditor · seed=ลูกค้า 1 รายมีประวัติ · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: เห็น activity ได้; ไม่มีปุ่มเพิ่ม
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/view/:id` → CLICK tab **Activity** | — | เห็น timeline ได้ | ☐ |
| 2 | VERIFY ปุ่ม **เพิ่ม Customer** | — | ไม่ปรากฏ/ปิดการใช้งาน | ☐ |

#### TC-P07 — sales_rep เห็นเฉพาะของตัวเอง (scope)
- group: P · ความสำคัญ: กลาง · trace: R-PRM-01
- Setup: role=sales_rep · seed=ลูกค้าของ sales_rep นี้ + ของคนอื่น (ต้องไม่เห็น) · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: รายการมีเฉพาะลูกค้าของ sales_rep นี้
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/list` (sales_rep) → VERIFY ทุกแถว | — | ทุกแถว sales_rep = ผู้ใช้ปัจจุบัน (ไม่เห็นของคนอื่น) | ☐ |

#### TC-P08 — ฟิลด์ immutable แก้ไม่ได้ + ล็อกประเภทหลัง save (EC-01)
- group: P · ความสำคัญ: สูง · trace: R-IDN-06 / IMMUTABLE_FIELD / CUSTOMER_TYPE_LOCKED / EC-01
- Setup: role=sales_mgr · seed=ลูกค้าที่บันทึกแล้ว 1 ราย · files=—
- Start: OPEN `#/edit/:id` · ผ่านเมื่อ: code + ประเภท แก้ไม่ได้
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/edit/:id` → VERIFY ช่อง Customer Code | — | read-only | ☐ |
| 2 | VERIFY ตัวเลือกประเภท (segmented) | — | ล็อก read-only (สลับ นิติบุคคล↔บุคคล ไม่ได้) | ☐ |

### กลุ่ม V — View Drawer + Activity (P-02)

#### TC-V01 — view drawer 4 แท็บแสดงข้อมูลครบ
- group: V · ความสำคัญ: กลาง · trace: FR read / R-ADR-11
- Setup: role=sales_mgr · seed=ลูกค้า 1 รายมีที่อยู่ต่างจังหวัด + บัญชี · files=—
- Start: OPEN `#/view/:id` · ผ่านเมื่อ: เห็น 4 tab + ข้อมูลตรง
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/list` → CLICK แถวลูกค้า | — | drawer view เปิด หัวมี avatar + display_name + customer_code + pill สถานะ | ☐ |
| 2 | VERIFY tab bar | — | 4 แท็บ **Profile / Addresses / Financial / Activity** | ☐ |
| 3 | CLICK tab **Addresses** | — | ที่อยู่ format `ต.… อ.… จังหวัด postal` + badge billing/จัดส่งหลัก | ☐ |
| 4 | CLICK tab **Financial** | — | payment_term/credit_limit + การ์ดบัญชี (เลข masked) | ☐ |

#### TC-V02 — activity timeline แสดง event
- group: V · ความสำคัญ: กลาง · trace: FR-09
- Setup: role=sales_mgr · seed=ลูกค้า 1 รายมีประวัติ (create/update) · files=—
- Start: OPEN `#/view/:id` · ผ่านเมื่อ: timeline แสดง event + actor + เวลา
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/view/:id` → CLICK tab **Activity** | — | timeline แสดงเหตุการณ์ แต่ละอันมีไอคอน + หัวข้อ + ผู้ทำ + เวลา | ☐ |

#### TC-V03 — activity empty state
- group: V · ความสำคัญ: ต่ำ · trace: R-UX-10
- Setup: role=sales_mgr · seed=ลูกค้าที่เพิ่งสร้างล้วน (ไม่มีประวัติเพิ่ม) · files=—
- Start: OPEN `#/view/:id` · ผ่านเมื่อ: เห็น empty state
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/view/:id` → CLICK tab **Activity** | — | empty state (ไม่มีกิจกรรม) | ☐ |

#### TC-V04 — national_id masked ใน Profile (mask)
- group: V · ความสำคัญ: กลาง · trace: §0.7 mask
- Setup: role=sales_mgr · seed=ลูกค้าบุคคลธรรมดา 1 ราย · files=—
- Start: OPEN `#/view/:id` · ผ่านเมื่อ: เลขบัตรแสดงแบบ mask
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/view/:id` (บุคคลธรรมดา) → VERIFY Profile | — | national_id แสดง masked (เช่น `1-XXXX-XXXXX-78-9`) ไม่ใช่เลขเต็ม | ☐ |

#### TC-V05 — เปิดดู PII เต็ม: ไม่มีสิทธิ์ vs มีสิทธิ์ (permission, EC-12)
- group: V · ความสำคัญ: กลาง · trace: §6.2.3 / INSUFFICIENT_PERMISSION / EC-12
- Setup: role=cs (ไม่มี view_sensitive_pii) แล้วทดสอบซ้ำด้วย role ที่มีสิทธิ์ · seed=ลูกค้าบุคคลธรรมดา 1 ราย · files=—
- Start: OPEN `#/view/:id` · ผ่านเมื่อ: ไม่มีสิทธิ์ → เปิดไม่ได้; มีสิทธิ์ → เห็น + บันทึก audit
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มเปิดเผยเลขบัตรเต็ม (role ไม่มีสิทธิ์) | — | ถูกปฏิเสธ/ไม่มีปุ่มเปิดเผย (INSUFFICIENT_PERMISSION) ⚠ ยืนยัน anchor | ☐ |
| 2 | CLICK ปุ่มเปิดเผยเลขบัตรเต็ม (role มีสิทธิ์) | — | เห็นค่าเต็ม + ระบบบันทึกการเข้าดู (โผล่ใน Activity ภายหลัง) | ☐ |

### กลุ่ม CNV — Convert จาก Prospect (P-06 → P-03) ⭐

#### TC-CNV01 — เปิด browse → เลือก prospect → prefill เข้า drawer (happy)
- group: CNV · ความสำคัญ: สูง · trace: FR-04 / R-CNV-03 / R-UX-01
- Setup: role=sales_rep · seed=prospect active ในโมดูล Prospect (มี company_name + engagement_score) เช่น "Slick" usr_007 · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: prefill มา + badge From Prospect + lead_source ล็อก
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **Convert** | — | modal **Browse Prospects** กว้าง 720px เปิด มีช่องค้นหา | ☐ |
| 2 | TYPE → ช่องค้นหา | "Slick" | รายการกรอง real-time ตามชื่อ/อีเมล/บริษัท | ☐ |
| 3 | CLICK แถว prospect "Slick" | — | modal ปิด → drawer **เพิ่ม Customer ใหม่** เปิดพร้อม prefill (ชื่อ/อีเมล/บริษัท) | ☐ |
| 4 | VERIFY ด้านบน drawer | — | badge **From Prospect: usr_007 (engagement_score: 78)** | ☐ |
| 5 | VERIFY ช่อง lead_source | — | ล็อกค่า **prospect_convert** (แก้ไม่ได้) | ☐ |

#### TC-CNV02 — บันทึก convert สำเร็จ → prospect = converted (atomic happy)
- group: CNV · ความสำคัญ: สูง · trace: FR-04 / R-CNV-02 / R-STA-02 / events
- Setup: role=sales_rep · seed=ต่อจาก TC-CNV01 (drawer convert เปิดอยู่) · files=—
- Start: (ต่อจาก TC-CNV01) · ผ่านเมื่อ: toast convert + prospect ฝั่ง Prospect = Converted
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **Save Customer & Convert** (เติมที่อยู่/บัญชีก่อนถ้าต้อง) | F/D | toast **สร้าง Customer สำเร็จ — CUST-… (Prospect convert)** + drawer ปิด + กลับ list | ☐ |
| 2 | VERIFY สถานะลูกค้าใหม่ | — | สถานะ = **active** (ไม่ใช่ vip) | ☐ |
| 3 | OPEN โมดูล Prospect → VERIFY prospect เดิม | — | prospect แสดงสถานะ **Converted** | ☐ |

#### TC-CNV03 — ยกเลิก drawer → onCancel, prospect ยัง active (R-CNV-05)
- group: CNV · ความสำคัญ: สูง · trace: R-CNV-05
- Setup: role=sales_rep · seed=prospect active 1 ราย · files=—
- Start: (เปิด convert drawer ตาม TC-CNV01) · ผ่านเมื่อ: ปิดโดยไม่บันทึก → prospect ไม่เปลี่ยน
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **Cancel** (หรือ PRESS Esc) ที่ drawer convert | — | drawer ปิด + (ฝั่ง Prospect) toast **ยกเลิกการ convert** | ☐ |
| 2 | OPEN โมดูล Prospect → VERIFY prospect เดิม | — | ยังเป็นสถานะ **active** | ☐ |

#### TC-CNV04 — prospect ที่ convert แล้วไม่โผล่ใน browse (R-CNV-01)
- group: CNV · ความสำคัญ: กลาง · trace: R-CNV-01 / PROSPECT_ALREADY_CONVERTED
- Setup: role=sales_rep · seed=prospect ที่ status=converted แล้ว 1 ราย · files=—
- Start: OPEN `#/list` → CLICK **Convert** · ผ่านเมื่อ: ไม่เห็น prospect ที่ converted
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **Convert** → TYPE ชื่อ prospect ที่ convert ไปแล้ว | (ชื่อ converted) | ไม่ปรากฏในรายการ | ☐ |

#### TC-CNV05 — ประเภทล็อกนิติบุคคลเมื่อ prefill มี company_name (FR-04)
- group: CNV · ความสำคัญ: กลาง · trace: FR-04
- Setup: role=sales_rep · seed=prospect ที่มี company_name · files=—
- Start: (convert prospect ที่มีบริษัท) · ผ่านเมื่อ: ตัวเลือกประเภทล็อก นิติบุคคล
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **Convert** → CLICK prospect ที่มีบริษัท → VERIFY ตัวเลือกประเภท | — | ล็อกที่ **นิติบุคคล** (สลับไม่ได้) | ☐ |

#### TC-CNV06 — โมดูล Customer ไม่พร้อม → fallback toast (edge: EC-03) (ต้อง simulate)
- group: CNV · ความสำคัญ: ต่ำ · trace: EC-03
- Setup: role=sales_rep · seed=prospect active · files=— · simulate: ทำให้ `window.openCustomerCreateModal` ไม่ถูกโหลด (เช่น block สคริปต์ Customer) — ถ้า simulate ไม่ได้ → BLOCKED
- Start: (ฝั่ง Prospect) กด convert · ผ่านเมื่อ: เห็น fallback toast
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK convert ขณะ Customer module ไม่พร้อม (ฝั่ง Prospect) | — | toast **ระบบ Customer ไม่พร้อม กรุณาลองอีกครั้ง** | ☐ |

#### TC-CNV07 — badge engagement_score แสดงถูก (FR-04)
- group: CNV · ความสำคัญ: ต่ำ · trace: FR-04
- Setup: role=sales_rep · seed=prospect engagement_score=78 · files=—
- Start: (convert prospect) · ผ่านเมื่อ: badge โชว์คะแนน
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **Convert** → CLICK prospect (score 78) → VERIFY badge | — | badge แสดง **engagement_score: 78** | ☐ |

### กลุ่ม IMP — นำเข้า CSV (P-07)

#### TC-IMP01 — ดาวน์โหลด Template (R-IMP-08)
- group: IMP · ความสำคัญ: กลาง · trace: FR-05 / R-IMP-08
- Setup: role=sales_mgr · seed=— · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: กด Template แล้วได้ CSV มี sample 2 ประเภท
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **Template** | — | ดาวน์โหลด CSV (header 32 คอลัมน์ + sample company + individual) | ☐ |

#### TC-IMP02 — นำเข้าไฟล์ valid → preview → commit (happy)
- group: IMP · ความสำคัญ: สูง · trace: FR-05 / R-IMP-01,03,05,06,07
- Setup: role=sales_mgr · seed=— · files=`valid_100.csv`
- Start: OPEN `#/list` · ผ่านเมื่อ: preview ถูก แล้ว commit → toast จำนวน
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **Import** → UPLOAD `valid_100.csv` | valid_100.csv | modal **Import Preview** เปิด | ☐ |
| 2 | VERIFY stats banner | — | **X valid / Y errors / total N** + ตาราง preview | ☐ |
| 3 | CLICK ปุ่ม **Import X customers** | — | modal ปิด + toast **Import สำเร็จ — N customers ใหม่** | ☐ |
| 4 | VERIFY list | — | แถวใหม่บนสุด (code auto-gen ต่อแถว) | ☐ |

#### TC-IMP03 — header ไม่ครบ → reject (negative)
- group: IMP · ความสำคัญ: สูง · trace: R-IMP-02 / MISSING_REQUIRED_HEADERS
- Setup: role=sales_mgr · seed=— · files=`bad_format.csv`
- Start: OPEN `#/list` · ผ่านเมื่อ: ไฟล์ขาด header จำเป็นถูกปฏิเสธ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **Import** → UPLOAD `bad_format.csv` | bad_format.csv | แจ้ง **header ไม่ครบ** + ไม่ให้ import | ☐ |

#### TC-IMP04 — ไฟล์ใหญ่เกิน 5 MB (boundary)
- group: IMP · ความสำคัญ: กลาง · trace: FILE_TOO_LARGE
- Setup: role=sales_mgr · seed=— · files=`oversize_6mb.csv`
- Start: OPEN `#/list` · ผ่านเมื่อ: ไฟล์ > 5MB ถูกปฏิเสธ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **Import** → UPLOAD `oversize_6mb.csv` | oversize_6mb.csv | แจ้งไฟล์ใหญ่เกินกำหนด | ☐ |

#### TC-IMP05 — แถวเกิน 5,000 (boundary)
- group: IMP · ความสำคัญ: กลาง · trace: R-IMP-10 / ROW_LIMIT_EXCEEDED
- Setup: role=sales_mgr · seed=— · files=`too_large.csv`
- Start: OPEN `#/list` · ผ่านเมื่อ: ไฟล์ > 5,000 แถวถูกปฏิเสธ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **Import** → UPLOAD `too_large.csv` | too_large.csv | แจ้งเกินจำนวนแถวสูงสุด (5,000) | ☐ |

#### TC-IMP06 — แถวผิด validation แสดงใน error list (negative)
- group: IMP · ความสำคัญ: สูง · trace: R-IMP-03,04
- Setup: role=sales_mgr · seed=— · files=`with_errors.csv`
- Start: OPEN `#/list` · ผ่านเมื่อ: preview แยก valid/error + บอกบรรทัด+เหตุผล
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **Import** → UPLOAD `with_errors.csv` | with_errors.csv | preview แสดง 40 valid, 10 errors + รายการ error (บรรทัด + เหตุผล) | ☐ |
| 2 | VERIFY ปุ่ม import | — | ปุ่มแสดง **Import 40 customers** | ☐ |

#### TC-IMP07 — tax_id ซ้ำในไฟล์ → warning (edge: EC-05)
- group: IMP · ความสำคัญ: ต่ำ · trace: EC-05
- Setup: role=sales_mgr · seed=— · files=`dup_in_file.csv`
- Start: OPEN `#/list` · ผ่านเมื่อ: preview เตือนแถวซ้ำในไฟล์
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **Import** → UPLOAD `dup_in_file.csv` | dup_in_file.csv | preview ติดธง **ซ้ำในไฟล์** (warning) | ☐ |

#### TC-IMP08 — ปุ่ม import disabled เมื่อ valid=0
- group: IMP · ความสำคัญ: กลาง · trace: FR-05 (UI)
- Setup: role=sales_mgr · seed=— · files=`all_errors.csv`
- Start: OPEN `#/list` · ผ่านเมื่อ: ทุกแถว error → ปุ่ม import กดไม่ได้
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **Import** → UPLOAD `all_errors.csv` | all_errors.csv | ปุ่ม **Import 0 customers** disabled | ☐ |

#### TC-IMP09 — ไฟล์ไม่ใช่ CSV (negative)
- group: IMP · ความสำคัญ: ต่ำ · trace: INVALID_FILE_TYPE
- Setup: role=sales_mgr · seed=— · files=`not_a_csv.xlsx`
- Start: OPEN `#/list` · ผ่านเมื่อ: เลือกไฟล์ที่ไม่ใช่ CSV ถูกปฏิเสธ
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **Import** → UPLOAD `not_a_csv.xlsx` | not_a_csv.xlsx | แจ้งชนิดไฟล์ไม่ถูกต้อง ⚠ ยืนยัน anchor | ☐ |

### กลุ่ม BLK — Bulk + Archive (P-05)

#### TC-BLK01 — เลือกแถว → Bulk Bar ปรากฏ
- group: BLK · ความสำคัญ: กลาง · trace: FR-07
- Setup: role=sales_mgr · seed=ลูกค้า ≥2 ราย · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: ติ๊กแล้ว bulk bar โผล่
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TOGGLE checkbox 2 แถว | — | แถบ navy **Bulk Bar** ปรากฏ **2 รายการ ถูกเลือก** + 3 ปุ่ม | ☐ |

#### TC-BLK02 — master checkbox + indeterminate
- group: BLK · ความสำคัญ: กลาง · trace: FR-07 / indeterminate
- Setup: role=sales_mgr · seed=ลูกค้า ≥3 รายในหน้า · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: master เลือกทั้งหน้า + indeterminate ตอนเลือกบางส่วน
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TOGGLE master checkbox (หัวตาราง) | — | ทุกแถวในหน้าถูกเลือก + bulk bar นับรวม | ☐ |
| 2 | TOGGLE checkbox 1 แถว (เอาออก) | — | master checkbox เป็น indeterminate (ครึ่ง) | ☐ |

#### TC-BLK03 — selection ค้างข้ามหน้า (edge: EC-14)
- group: BLK · ความสำคัญ: กลาง · trace: EC-14
- Setup: role=sales_mgr · seed=ลูกค้าหลายหน้า · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: เลือกหน้า 1 + หน้า 2 แล้วนับสะสม
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TOGGLE 3 แถว (หน้า 1) | — | bulk bar = 3 | ☐ |
| 2 | CLICK เลขหน้า 2 → TOGGLE 2 แถว | — | bulk bar = **5 รายการ ถูกเลือก** (สะสมข้ามหน้า) | ☐ |

#### TC-BLK04 — bulk archive → ยืนยัน → ซ่อนจาก list (happy)
- group: BLK · ความสำคัญ: สูง · trace: FR-07 / event customer.bulk_archived
- Setup: role=sales_mgr · seed=ลูกค้า status=suspended ≥3 ราย · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: archive แล้ว toast + แถวหาย (default filter)
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "suspended" → filter สถานะ → TOGGLE master checkbox | — | bulk bar นับจำนวน | ☐ |
| 2 | CLICK ปุ่ม **Archive selected** | — | modal ยืนยัน (440px) แสดงจำนวน | ☐ |
| 3 | CLICK ปุ่ม **Archive** | — | toast **Archive สำเร็จ — N customers** + selection ล้าง + แถวหายจาก list | ☐ |
| 4 | SELECT "archived" → filter สถานะ | archived | แถวที่เพิ่ง archive ปรากฏ | ☐ |

#### TC-BLK05 — archive ของที่ archived แล้ว → skipped (edge)
- group: BLK · ความสำคัญ: ต่ำ · trace: ALREADY_ARCHIVED
- Setup: role=sales_mgr · seed=ชุดที่มีทั้ง active + archived · files=—
- Start: OPEN `#/list` (filter=all) · ผ่านเมื่อ: id ที่ archived แล้วถูก skip
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TOGGLE เลือกชุดที่มีทั้ง active + archived → CLICK **Archive selected** → CLICK **Archive** | — | ผลแจ้งว่า record ที่ archived อยู่แล้วถูกข้าม (skipped) ⚠ ยืนยัน anchor | ☐ |

#### TC-BLK06 — bulk export selected
- group: BLK · ความสำคัญ: กลาง · trace: FR-08
- Setup: role=sales_mgr · seed=ลูกค้า ≥3 ราย · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: เลือกแล้วกด Export selected → CSV ของที่เลือก
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TOGGLE 3 แถว → CLICK ปุ่ม **Export selected** | — | ดาวน์โหลด CSV ชื่อ `customer-selected-YYYY-MM-DD.csv` | ☐ |

#### TC-BLK07 — clear selection
- group: BLK · ความสำคัญ: ต่ำ · trace: FR-07
- Setup: role=sales_mgr · seed=ลูกค้า ≥2 ราย · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: กด Clear → selection หาย bulk bar ปิด
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TOGGLE หลายแถว → CLICK ปุ่ม **Clear** | — | selection ถูกล้าง + bulk bar หาย | ☐ |

#### TC-ARC01 — archive รายตัวจากไอคอนในแถว
- group: BLK · ความสำคัญ: กลาง · trace: FR-07 (single)
- Setup: role=sales_mgr · seed=ลูกค้า active ≥1 ราย · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: กด archive ในแถว → ยืนยัน → แถวหาย
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอน **Archive** (ท้ายแถว) | — | modal ยืนยันเปิด | ☐ |
| 2 | CLICK ปุ่ม **Archive** | — | toast + แถวหายจาก list (default filter) | ☐ |

### กลุ่ม EXP — Export

#### TC-EXP01 — export ตาม filter ปัจจุบัน (R-PRM-04, R-IMP-09)
- group: EXP · ความสำคัญ: กลาง · trace: FR-08 / R-PRM-04 / R-IMP-09
- Setup: role=sales_mgr · seed=ลูกค้า vip ≥1 ราย · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: ใช้ filter แล้ว Export → CSV ชื่อ pattern ถูก
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "vip" → filter สถานะ → CLICK ปุ่ม **Export** | — | ดาวน์โหลด CSV ชื่อ `customer-export-YYYY-MM-DD.csv` (เฉพาะ vip ที่เห็น) | ☐ |

#### TC-EXP02 — export เมื่อไม่มีข้อมูล (negative)
- group: EXP · ความสำคัญ: ต่ำ · trace: NO_DATA_TO_EXPORT
- Setup: role=sales_mgr · seed=— · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: filter ที่ผลว่าง → export แจ้งไม่มีข้อมูล
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE คำค้นที่ไม่มีผล → CLICK ปุ่ม **Export** | `zzzqqq123` | แจ้งไม่มีข้อมูลให้ export (ไม่ดาวน์โหลดไฟล์ว่าง) ⚠ ยืนยัน anchor | ☐ |

#### TC-EXP03 — sensitive ไม่ถูกถอดรหัสใน export (mask)
- group: EXP · ความสำคัญ: กลาง · trace: FR-08 (CSV) / R-ADR-11
- Setup: role=sales_mgr · seed=ลูกค้ามีบัญชีธนาคาร · files=—
- Start: OPEN `#/list` · ผ่านเมื่อ: เปิดไฟล์ที่ export แล้ว เลขบัญชี = masked
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **Export** → เปิดไฟล์ CSV → VERIFY คอลัมน์บัญชี | — | account_number masked/last4 (ไม่ใช่เลขเต็ม) + ที่อยู่ format ถูก | ☐ |

### กลุ่ม STA — State Transition

#### TC-STA01 — suspended → active ต้องมี note (R-STA-03)
- group: STA · ความสำคัญ: กลาง · trace: R-STA-03 / NOTE_REQUIRED_FOR_TRANSITION
- Setup: role=sales_mgr · seed=ลูกค้า status=suspended 1 ราย · files=—
- Start: OPEN `#/edit/:id` · ผ่านเมื่อ: เปลี่ยนเป็น active โดยไม่ใส่ note ถูกบล็อก
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "active" → สถานะ (ไม่กรอก note) → CLICK **บันทึก** | — | ถูกบล็อก + แจ้งต้องมีหมายเหตุ | ☐ |
| 2 | TYPE → note → CLICK **บันทึก** | "ชำระครบแล้ว" | สำเร็จ + สถานะเป็น active | ☐ |

#### TC-STA02 — archived → vip ต้องห้าม (R-STA-01)
- group: STA · ความสำคัญ: กลาง · trace: R-STA-01 / STATE_TRANSITION_FORBIDDEN
- Setup: role=admin · seed=ลูกค้า status=archived 1 ราย · files=—
- Start: OPEN `#/edit/:id` (ลูกค้า archived) · ผ่านเมื่อ: ข้ามไป vip ตรง ๆ ไม่ได้
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "vip" → สถานะ (จาก archived) → CLICK **บันทึก** | — | ถูกปฏิเสธ + แจ้งต้อง restore เป็น active ก่อน ⚠ ยืนยัน anchor | ☐ |

### กลุ่ม UX — Interaction / Dirty

#### TC-UX01 — dirty check ก่อนปิด (FR-10, R-UX-04)
- group: UX · ความสำคัญ: กลาง · trace: FR-10 / R-UX-04
- Setup: role=sales_mgr · seed=ลูกค้า 1 ราย · files=—
- Start: OPEN `#/edit/:id` · ผ่านเมื่อ: แก้แล้วปิด → ถาม confirm
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/edit/:id` → TYPE แก้ฟิลด์ใดฟิลด์หนึ่ง → CLICK ปุ่ม **X** | — | dialog **ข้อมูลที่กรอกจะหายไป — ยืนยันปิด?** | ☐ |
| 2 | CLICK **Cancel** | — | drawer ยังเปิด | ☐ |
| 3 | CLICK ปุ่ม **X** → CLICK **OK** | — | drawer ปิด + ทิ้งการแก้ | ☐ |

#### TC-UX02 — ไม่ dirty → ปิดทันที (FR-10)
- group: UX · ความสำคัญ: ต่ำ · trace: FR-10
- Setup: role=sales_mgr · seed=ลูกค้า 1 ราย · files=—
- Start: OPEN `#/edit/:id` · ผ่านเมื่อ: ไม่แก้แล้วปิด → ปิดเลยไม่ถาม
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/edit/:id` → CLICK ปุ่ม **X** (ไม่แก้อะไร) | — | drawer ปิดทันที ไม่มี dialog | ☐ |

#### TC-UX03 — 3 ทางปิด ESC/Backdrop/X (R-UX-03)
- group: UX · ความสำคัญ: ต่ำ · trace: R-UX-03
- Setup: role=sales_mgr · seed=ลูกค้า 1 ราย · files=—
- Start: OPEN `#/view/:id` · ผ่านเมื่อ: ปิดได้ทั้ง ESC, backdrop, X
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/view/:id` → PRESS Esc | — | drawer ปิด → route `#/list` | ☐ |
| 2 | OPEN `#/view/:id` → CLICK พื้นหลัง (backdrop) | — | drawer ปิด | ☐ |
| 3 | OPEN `#/view/:id` → CLICK ปุ่ม **X** | — | drawer ปิด | ☐ |

#### TC-UX04 — Ctrl/Cmd+S บันทึก (R-UX-05)
- group: UX · ความสำคัญ: ต่ำ · trace: R-UX-05
- Setup: role=sales_rep · seed=— · files=—
- Start: OPEN `#/create` · ผ่านเมื่อ: กรอกครบแล้วกด Ctrl+S → บันทึก
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/create` → TYPE/SELECT ฟอร์มครบ | A | ฟอร์มครบ | ☐ |
| 2 | PRESS Ctrl+S | — | บันทึก (เหมือนกด Save) + toast | ☐ |

#### TC-UX05 — ESC ใน modal-over-drawer ปิดเฉพาะ modal (§6.7.4)
- group: UX · ความสำคัญ: ต่ำ · trace: keyboard nav
- Setup: role=sales_rep · seed=prospect active (เพื่อเปิด browse ซ้อน) · files=—
- Start: OPEN `#/create` แล้วเปิด modal ซ้อน · ผ่านเมื่อ: ESC ปิด modal เหลือ drawer
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS Esc (ขณะมี modal ซ้อนบน drawer) | — | modal ปิด แต่ drawer ยังเปิดอยู่ | ☐ |

### กลุ่ม X — Cross-cutting Security

#### TC-X01 — RLS: tenant อื่นมองไม่เห็น (R-PRM-02)
- group: X · ความสำคัญ: สูง · trace: R-PRM-02 / §6.2.1 / CUSTOMER_NOT_FOUND / TENANT_MISMATCH / EC-02
- Setup: role=any (tenant A) · seed=ลูกค้า id หนึ่งที่อยู่ tenant B · files=—
- Start: OPEN `#/view/:id` (id ของ tenant B) · ผ่านเมื่อ: เข้าไม่ถึง (404/ไม่แสดง)
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/view/:id` ของ tenant B (ขณะ login tenant A) | (id ของ B) | ไม่พบข้อมูล/หน้าว่าง (RLS ซ่อน) — ไม่เห็นข้ามtenant | ☐ |

#### TC-X02 — customer_code per-tenant counter (§6.2.2)
- group: X · ความสำคัญ: กลาง · trace: R-IDN-05 / §6.2.2
- Setup: role=sales_rep · seed=— · files=—
- Start: OPEN `#/create` · ผ่านเมื่อ: สร้าง 2 รายวันเดียวกัน → counter +1
| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/create` → TYPE/SELECT ครบ → CLICK **บันทึก** (รายแรกของวัน) | A | code ลงท้าย `-0001` (วันนี้) | ☐ |
| 2 | OPEN `#/create` → TYPE/SELECT ครบ → CLICK **บันทึก** (รายที่สอง) | A (ต่าง tax_id) | code ลงท้าย `-0002` | ☐ |

#### TC-X03 — Idempotency replay (backend)
- group: X · trace: §6.2.2 · **สถานะ: ข้าม** — header-level backend ไม่เห็นบน UI

#### TC-X04 — Encryption at rest (SQL)
- group: X · trace: R-BNK-05 / §6.2.3 · **สถานะ: ข้าม** — ตรวจที่ DB ไม่ใช่ UI

---

## วิธีที่ agent รัน (Run protocol)
1. อ่าน `Setup:` ของเคส → เตรียม role (login), seed data, และไฟล์ตามชื่อ ก่อนเริ่ม
2. ทำตาม `Start` (OPEN route) ก่อนเริ่ม step 1 เสมอ (refresh-safe)
3. ทำ Action ทีละ step ตาม verb: **OPEN/CLICK/TYPE/SELECT/TOGGLE/UPLOAD/PRESS/VERIFY** โดยหา target จาก **ข้อความ/ป้ายที่เห็นบนจอ**; กรอก Input ตามชุดข้อมูล
4. ตรวจ Expected จากสิ่งที่ปรากฏ — ตรง = ผ่าน step
5. เคส **PASS** เมื่อทุก step ผ่าน + ตรง "ผ่านเมื่อ"; ไม่ตรง = **FAIL** (บันทึก step + สิ่งที่เห็น);
   เปิด route ไม่ได้ / simulate ไม่ได้ / ไม่มีไฟล์ที่ Setup ต้องการ = **BLOCKED**
6. step ที่ติด `⚠ ยืนยัน anchor` = anchor จาก 01_UI ให้จับข้อความบนจอจริงที่ใกล้สุด

## Coverage Audit
| หมวด | covered / total |
|---|---|
| FR (06_TESTS) | 10 / 10 |
| Business rules (05_RULES) | 47 / 48 (R-UX-06/07 รวมเป็นสังเกต) |
| Edge cases | 8 / 15 (ที่เหลือ backend/Phase 2) |
| Error codes | 24 / ~40 (ที่เหลือ auth/5xx/backend) |
| Permission cells (สำคัญ) | 8 / 8 |
| Cross-cutting / events / states | RLS✔ code✔ mask✔ empty✔ ; encryption(SQL)=ข้าม |

### ข้าม (พร้อมเหตุผล)
- **EC-04** bulk archive w/ active invoice — Phase 1 ไม่ตรวจ (Finance ยังไม่มี)
- **EC-06** cascade master deprecated — ต้อง seed master is_active=false (DBA)
- **EC-07** converted + deleted prospect — Phase 2 hard delete
- **EC-08** dirty + network timeout — ต้อง fault-inject network
- **EC-10 / CONCURRENT_UPDATE** — Phase 2 optimistic locking
- **EC-11** master not loaded (skeleton) — โหลดเร็วเกินสังเกต
- **EC-15** large CSV export — ต้อง seed 10k (rare)
- **R-UX-06/07** scroll/focus preservation — interaction ลึก รวมเป็นสังเกต
- **IDEMPOTENCY_KEY_REUSED / 5xx / RATE_LIMIT / AUTH(401/403 session)** — backend/fault-inject/load
- **TC-X03 / TC-X04** — ตรวจหลังบ้าน/DB ไม่ใช่หน้าจอ

## Result Report (schema)
```json
{
  "feature_id": "F-CUSTOMER",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 85, "pass": 0, "fail": 0, "blocked": 0 }
}
```
> เติม `results[]` ให้ครบทุก TC id (TC-L01..TC-X04) แล้วอัปเดต `summary`.

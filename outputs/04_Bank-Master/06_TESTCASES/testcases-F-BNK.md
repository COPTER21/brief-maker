# AI Test Cases — F-BNK บัญชีธนาคาร (Bank Master)

ไฟล์นี้เขียนให้ **AI agent (browser-use / vision)** อ่านแล้วลงมือทดสอบบนหน้าจอจริง + รายงานผลกลับ machine-readable.
ทุก action ขึ้นต้นด้วย **verb tag** (OPEN/CLICK/TYPE/SELECT/TOGGLE/UPLOAD/PRESS/WAIT/VERIFY) + target ที่เห็นบนจอ.
ทุก Expected เช็คได้ด้วยตา (ข้อความปรากฏ/หาย · pill เปลี่ยนสี · จำนวนแถว · ปุ่ม disabled · toast).

> **Anchor source priority:** HTML SoT `01_HTML/f-bank.html` (verbatim) > `01_UI` > microcopy กลาง html-generator-v8.
> **หน้าจอ = single-view SPA + overlay** (hash route เดียว `#/bank-master`; navigation ภายใน = overlay function). "route (production)"
> = เส้นทางที่เสนอ 1:1 กับ overlay. agent ที่รันบน prototype: เปิดไฟล์ HTML = เข้าหน้า List (P-01) เสมอ · reload = กลับ List, mock state in-memory (แก้แล้วไม่ persist ข้าม reload — เคสที่พึ่งลำดับต้อง refresh-safe).
> **Toast:** top-center · error/warning ค้างนานกว่า success · หายเอง.
>
> **⚠ Drift Log (HTML ชนะ + note):**
> 1. **Import KBANK-01 row:** FRD 06_TESTS §6.10/AT-16 ระบุแถว `KBANK-01` = `ACCT_DUPLICATE` แต่ **HTML จริงคืน `รหัสซ้ำ (CODE_DUPLICATE)`** — เพราะ sample row มี `account_no=012-9-99999-9` (digits `0129999999`) ซึ่ง **ไม่ตรง** กับทะเบียน `KBANK-01` (`012-3-45678-9`) → ผ่านด่าน ACCT_DUPLICATE แล้วไปติด CODE_DUPLICATE (รหัสซ้ำทะเบียน). Expected ในไฟล์นี้ยึด **HTML actual = CODE_DUPLICATE**. ผลรวม "นำเข้าได้ 3 · ติดปัญหา 3" ไม่เปลี่ยน. (flag ให้ product ปรับ FRD หรือปรับ sample row)
> 2. **ไม่มีปุ่ม demo ในจอ import:** ฟังก์ชัน `bulkPickDemo()` มีใน JS แต่ **ไม่ผูกกับปุ่มใด** — จอ pick มีเฉพาะ upload-box (real file picker `accept=.csv`). ดังนั้นเคส import ทุกเคสต้อง **UPLOAD ไฟล์จริง** (runner เตรียมไฟล์ตามชื่อใน §ไฟล์ทดสอบ).

---

## Meta

| Field | Value |
|---|---|
| Feature ID | F-BNK (F-BANK-MASTER-001 · node F-0.21) |
| Feature Name | Bank Master — บัญชีธนาคาร |
| Module | การเงิน (Accounting) — sidebar item "บัญชีธนาคาร" (is-active) |
| FRD Version | 1.0 (2026-08-11, FULL pack, HTML-first) |
| App entry (observed) | โหลด `f-bank.html` → หน้า List (P-01) · breadcrumb "Finance › บัญชีธนาคาร" |
| Routes (production 1:1) | List `#/finance/bank-master` · Create `…/new` · Edit `…/:id/edit` · View `…/:id` · Import modal · Bulk-delete modal |
| แหล่งอ้างอิง | FRD `06_TESTS` (AT-01..21, XT-01..05) · `05_RULES` (BR-01..10, EC-01..11) · `01_UI` (P-01..06) · `07_LOCKED §7.0` (LOCK) · FUNCTION_CHECKLIST (FN-01..25, FN-40, FN-90) · HTML SoT · UI Brief |
| Seed data | 8 บัญชี (B-001..B-008) — ดูตาราง Seed · active 6 / draft 1 / inactive 1 · used 0..620 |
| จำนวนเคส | 96 เคส (ดู Coverage) |
| Note (regen) | รอบแรก — TC-id เสถียรสำหรับ regen ถัดไป (R16) |

**Seed อ้างอิง (จาก HTML `state.records`) — ใช้เป็น precondition:**

| id | code | ธนาคาร · สาขา | เลขที่บัญชี | ประเภท | ฝั่ง | ★ | กลุ่ม GL | promptpay | สถานะ | used |
|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | **KBANK-01** | กสิกรไทย · สำนักงานใหญ่ (พหลโยธิน) | 012-3-45678-9 | ออมทรัพย์ | รับ+จ่าย | **★รับ** | KBANK | 0105561234567 (13) | ใช้งาน | **620** |
| B-002 | **SCB-01** | ไทยพาณิชย์ · รัชโยธิน | 987-6-54321-0 | กระแสรายวัน | จ่าย | **★จ่าย** | **SCB (draft)** | — | ใช้งาน | **340** |
| B-003 | BBL-01 | กรุงเทพ · สีลม | 111-2-33344-5 | กระแสรายวัน | รับ+จ่าย | — | — (ไม่ผูก) | — | ใช้งาน | 88 |
| B-004 | **KTB-01** | กรุงไทย · งามวงศ์วาน | 555-6-77788-9 | ออมทรัพย์ | รับ | — | — (ไม่ผูก) | — | ใช้งาน | **0** (ลบได้) |
| B-005 | KBANK-02 | กสิกรไทย · เซ็นทรัลลาดพร้าว | 044-1-98765-2 | ออมทรัพย์ | รับ | — | KBANK | — | ใช้งาน | 12 |
| B-006 | BAY-01 | กรุงศรีอยุธยา · ออนไลน์ | 777-1-11223-4 | ออมทรัพย์ | รับ | — | — (ไม่ผูก) | 0812345678 (10) | ใช้งาน | 45 |
| B-007 | TTB-01 | ทีเอ็มบีธนชาต · พระราม 9 (เตรียมเปิดใช้) | 333-4-55667-8 | กระแสรายวัน | จ่าย | — | — (ไม่ผูก) | — | **ร่าง** | 0 |
| B-008 | GSB-01 | ออมสิน · สะพานใหม่ (ปิดบัญชีแล้ว) | 020-1-40506-7 | ออมทรัพย์ | รับ+จ่าย | — | — (ไม่ผูก) | — | **ไม่ใช้งาน** | 15 |

> Stat cards เริ่มต้น: **บัญชีทั้งหมด 8** (meta = 7 ธนาคาร) · **ใช้งานอยู่ 6** · **ไม่ใช้งาน 1** · **ร่าง 1**.
> ph-count หัวหน้า = "**8 บัญชี**". pageSize = 8 (8 แถวพอดี 1 หน้า; เพิ่ม record → หน้า 2).
> **BANKS (9):** กสิกรไทย(KBANK) · ไทยพาณิชย์(SCB) · กรุงเทพ(BBL) · กรุงไทย(KTB) · ทีเอ็มบีธนชาต(TTB) · กรุงศรีอยุธยา(BAY) · ออมสิน(GSB) · ยูโอบี(UOB) · อื่น ๆ(OTHER). **ACCT_TYPES (3):** ออมทรัพย์ · กระแสรายวัน · ฝากประจำ. **GL groups (F-PG kind=bank):** KBANK=active · SCB=draft.

---

## Coverage

| Group | รหัส | เคส | ความสำคัญ |
|---|---|---|---|
| A. List / Search / Filter / Sort / Pager (P-01) | TC-L01..L12 | 12 | สูง |
| B. Create happy + GL + auto-code + defaults | TC-C01..C08 | 8 | สูง |
| C. Create validation / negative | TC-V01..V10 | 10 | สูง |
| D. ★ Default per side + DEFAULT_GUARD + radio | TC-DF01..DF06 | 6 | สูง |
| E. Edit + IR-BNK-01 lock + save guard | TC-E01..E06 | 6 | สูง |
| F. GL picker active-only + keep-bound draft | TC-GL01..GL04 | 4 | สูง |
| G. Status change (single + bulk) + ★ drop | TC-S01..S06 | 6 | สูง |
| H. Bulk delete + guard used>0 | TC-D01..D05 | 5 | สูง |
| I. CSV Import (merge-only, 3 จังหวะ) | TC-IM01..IM08 | 8 | สูง |
| J. Export CSV | TC-X01..X02 | 2 | กลาง |
| K. View drawer (P-04) | TC-VW01..VW05 | 5 | กลาง |
| L. v8 / regression (#96/#29/#44/#97/Esc/empty) | TC-EC01..EC06 | 6 | กลาง |
| M. Scope-Lock / FN-40 "must-NOT-exist" | TC-SL01..SL10 | 10 | สูง |
| N. Permission (Viewer/Consumer 403) | TC-PM01..PM02 | 2 | กลาง |
| O. Cross-Module (XT — simulate) | TC-XT01..XT04 | 4 | กลาง |
| P. Concurrency / Idempotency (simulate) | TC-CC01..CC02 | 2 | ต่ำ |
| **รวม** | | **96** | |

---

## Coverage Ledger

### FR / Acceptance (06_TESTS §6.1)
| item | cases |
|---|---|
| AT-01 create happy | TC-C01 |
| AT-02 code auto + duplicate | TC-C02, TC-V05 |
| AT-03 search/filter/sort/pager | TC-L01..L12 |
| AT-04 account_no 10–12 หลัก | TC-V01, TC-V02 |
| AT-05 account_no unique dash-strip | TC-V03 |
| AT-05b promptpay ว่าง/10/13 | TC-V07, TC-V08, TC-C06 |
| AT-06 use side ≥1 | TC-V06 |
| AT-07 ★ default guard + radio | TC-DF01..DF05 |
| AT-08 IR-BNK-01 lock (UI) | TC-E02, TC-E03 |
| AT-09 IR-BNK-01 save guard (DOM ฝืน) | TC-E04 (ต้อง simulate) |
| AT-10 edit used=0 all editable | TC-E01 |
| AT-11 GL picker active-only | TC-GL01 |
| AT-12 GL keep-bound draft + rebind | TC-GL02, TC-GL03 |
| AT-13 status change single | TC-S01, TC-S02 |
| AT-14 ★ drop เมื่อออก active | TC-S05, TC-DF06 |
| AT-15 bulk delete guard | TC-D01..D05 |
| AT-16 import preview validate (IN_FILE_DUPLICATE) | TC-IM02, TC-IM03, TC-IM04 |
| AT-17 import commit merge-only + defaults | TC-IM05, TC-IM06 |
| AT-17b non-csv reject | TC-IM07 |
| AT-18 export roundtrip + BOM | TC-X01, TC-X02 |
| AT-19 no currency/SWIFT/used (absence) | TC-SL02, TC-SL03, TC-SL04 |
| AT-20 Viewer/Consumer 403 | TC-PM01, TC-PM02 (ต้อง simulate) |
| AT-21 empty + close chain + 0 console err | TC-L03, TC-EC05, TC-EC06 |

### Business Rules (05_RULES §5.1)
| rule | cases |
|---|---|
| BR-01 account_no 10–12 · unique dash-strip | TC-V01, TC-V02, TC-V03, TC-IM03 |
| BR-02 IR-BNK-01 used>0 lock + ลบไม่ได้ | TC-E02, TC-E03, TC-E04, TC-D01, TC-D02 |
| BR-03 ฝั่ง ≥1 · ★ 1/ฝั่ง radio · DEFAULT_GUARD · หลุด active→★ หลุด | TC-V06, TC-DF01..DF06, TC-S05 |
| BR-04 GL resolve ผ่านกลุ่ม · binding OPTIONAL (view เตือน) | TC-C05, TC-GL01, TC-GL04, TC-VW04 |
| BR-05 Receipt/PV active + ฝั่งตรง · ★ pre-select · snapshot | TC-XT01, TC-XT02 (ต้อง simulate) |
| BR-06 promptpay ว่าง/10/13 | TC-V07, TC-V08, TC-C06 |
| BR-07 import merge-only · ค่าไทย · default ออมทรัพย์/ทั้งสอง/ร่าง | TC-IM01, TC-IM05, TC-IM06, TC-IM08 |
| BR-08 code unique + UPPERCASE (auto {bank}-{seq}) | TC-C02, TC-V05 |
| BR-09 THB คงที่ · ไม่มี multi-currency/SWIFT/IBAN | TC-C01, TC-SL02, TC-SL03 |
| BR-10 BANKS 9 + ACCT_TYPES 3 reference | TC-C01, TC-C03, TC-IM04 |

### Function Checklist (FN-01..25, FN-40, FN-90)
| FN | cases |
|---|---|
| FN-01 form 3 sections (ไม่มี hint) | TC-C01, TC-SL10 |
| FN-02 auto code | TC-C02 |
| FN-03 9 banks + 3 types | TC-C01, TC-C03 |
| FN-04 GL group active-only optional | TC-C05, TC-GL01, TC-VW04 |
| FN-05 THB disabled | TC-C01, TC-SL02 |
| FN-06 DOA null + used=0 | TC-C01, TC-SL05 |
| FN-07 ใช้ฝั่ง vs ★ radio 1/side | TC-DF01, TC-DF02, TC-DF03 |
| FN-08 DEFAULT_GUARD | TC-DF04, TC-DF05 |
| FN-09 leave active → ★ drop · list/view ★รับ/★จ่าย | TC-S05, TC-DF06, TC-L05, TC-VW05 |
| FN-10 used>0 UI lock + lock-tag | TC-E02, TC-E03 |
| FN-11 used>0 logic guard save | TC-E04 (ต้อง simulate) |
| FN-12 validate acct/dup/code/name/side | TC-V01..V06 |
| FN-13 promptpay blank/10/13 | TC-V07, TC-V08 |
| FN-14 view status menu 3 ค่า current disabled | TC-S01, TC-S02 |
| FN-15 bulk bar 3 status + cancel + select-all-thead + row highlight | TC-S03, TC-S04, TC-L11 |
| FN-16 stat+filter+search+sort+pager together | TC-L01..L12 |
| FN-17 bulk delete confirm skip + no-deletable disabled | TC-D01..D05 |
| FN-18 import 3 จังหวะ upload+template only | TC-IM01, TC-SL08 |
| FN-19 preview per-row reasons + IN_FILE_DUPLICATE | TC-IM02, TC-IM03, TC-IM04 |
| FN-20 import merge-only + Thai defaults + no pg/promptpay + DOA null | TC-IM05, TC-IM06, TC-IM08 |
| FN-21 done summary imported/skipped + skipped table | TC-IM05, TC-IM06 |
| FN-22 export per filter + roundtrip + BOM + filename | TC-X01, TC-X02 |
| FN-23 view title mask + 4 chips | TC-VW01, TC-VW02 |
| FN-24 view 3 sections + GL warning + tabs | TC-VW03, TC-VW04 |
| FN-25 #96/#29/#97/Esc chain | TC-EC01..EC06 |
| FN-40 must-not-exist | TC-SL01..SL10 |
| FN-90 ลบผ่าน confirm เสมอ (ไม่มีลบเดี่ยว) | TC-SL01, TC-D01 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 IR lock + save guard | TC-E02, TC-E03, TC-E04 |
| EC-02 นิยาม `used` (OQ-BNK-07 OPEN) | — ข้าม (blocking OQ ยังไม่ปิด · `used` ไม่โชว์บนจอ → สังเกตไม่ได้) |
| EC-03 เปลี่ยน type/ฝั่ง ของ used>0 | TC-E05 |
| EC-04 GL group ผูกไว้ถูกเปลี่ยน draft | TC-GL02, TC-GL03 |
| EC-05 ปลายทางอ้าง inactive mid-doc | TC-XT02 (ต้อง simulate) |
| EC-06 posting_group source drift (OQ-BNK-06 OPEN) | TC-XT03 (ต้อง simulate — GL contract) |
| EC-07 กลุ่ม account_1 = NULL | TC-XT04 (ต้อง simulate — downstream GL) |
| EC-08 concurrent ★ (409) | TC-CC01 (ต้อง simulate) |
| EC-09 double-submit create | TC-CC02 |
| EC-10 ไฟล์นำเข้า ≠ .csv | TC-IM07 |
| EC-11 PII/masking account_no (OQ-BNK-08 OPEN) | TC-VW01 (header mask สังเกตได้) · ระดับ table/def-grid — ข้าม (OQ Security) |

### Error Codes (05_RULES §5.6)
| error | cases |
|---|---|
| ERR_REQUIRED (ชื่อบัญชีว่าง) | TC-V04 |
| ERR_BAD_BANK (import) | TC-IM04 |
| ERR_ACCT_INVALID | TC-V01, TC-V02, TC-IM04 |
| ERR_ACCT_DUPLICATE | TC-V03 |
| ERR_CODE_DUPLICATE | TC-V05, TC-IM03 |
| ERR_PROMPTPAY_INVALID | TC-V07, TC-V08 |
| ERR_USE_IN_EMPTY | TC-V06 |
| ERR_DEFAULT_GUARD | TC-DF04, TC-DF05 |
| ERR_BAD_TYPE / ERR_BAD_USE / ERR_BAD_STATUS (import) | TC-IM02 (คลุม), — บางส่วน (ดูหมายเหตุ) |
| ERR_IN_FILE_DUPLICATE | TC-IM02, TC-IM03 |
| ERR_INSUFFICIENT_ROLE (403) | TC-PM01, TC-PM02 (ต้อง simulate) |
| ERR_STALE_DATA (409) | TC-CC01 (ต้อง simulate) |
| ERR_DUPLICATE_IDEMPOTENCY_KEY | TC-CC02 (ต้อง simulate) |
| ERR_NOT_FOUND / ERR_NOT_AUTHENTICATED / ERR_VALIDATION_FAILED | — ข้าม (API-only, ไม่มี trigger บน UI prototype) |

### Permission Matrix (05_RULES §5.3)
| cell | cases |
|---|---|
| Finance Master Admin = ทุก action | ครอบทั้งไฟล์ (default user = Finance Admin) |
| Finance Viewer = view/ค้นหา/sort (mutation deny) | TC-PM01 (ต้อง simulate role) |
| Consumer = picker active + ฝั่งตรง (mutation deny) | TC-PM02, TC-XT01 (ต้อง simulate) |

### Cross-Module (XT — 06_TESTS §6.9)
| XT | Downstream | Case |
|---|---|---|
| XT-01 Receipt/PV picker active+ฝั่งตรง+★ pre-select+snapshot | Receipt/PV | TC-XT01 (ต้อง simulate) |
| XT-02 master→inactive ไม่โผล่ picker · เอกสารเก่า snapshot ยังใช้ | picker | TC-XT02 (ต้อง simulate) |
| XT-03 consume F-PG API-01 (?kind=bank&status=active) 3 drifts | F-PG | TC-XT03 (ต้อง simulate; master-side observable บางส่วน = TC-GL01) |
| XT-04 กลุ่มผูกแล้ว account_1=NULL → post ไม่ได้ | GL engine | TC-XT04 (ต้อง simulate) |
| XT-05 ~~เส้นออก Payment Method~~ | ~~PM (F-0.20)~~ | TC-SL01 (negative — ยืนยันไม่มี) |

### Scope Lock (07_LOCKED §7.0) — LOCK ทุกข้อต้องมีเคส verify
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| OQ-BNK-01 = NO | ไม่มีเส้นออก Payment Method (ไม่มี endpoint/UI) | TC-SL01 |
| OQ-BNK-02 = OPTIONAL | บันทึกได้ไม่ผูกกลุ่ม (view เตือน) · picker active-only + keep-bound draft | TC-C05, TC-GL01, TC-GL02, TC-VW04 |
| OQ-BNK-03 = IR-BNK-01 | used>0 ล็อกธนาคาร+เลขบัญชี · ลบไม่ได้ · used ไม่โชว์ | TC-E02, TC-E04, TC-D01, TC-SL04 |
| OQ-BNK-04 = CONFIRMED | Receipt/PV active+ฝั่งตรง+★+snapshot | TC-XT01, TC-XT02 |
| GL Contract | soft-ref code · ?kind=bank · active-only คืน KBANK · no COA ตรง | TC-GL01, TC-XT03 |
| Pattern VD-PDM | 3 สถานะอิสระ ไม่มีอนุมัติ · ไม่มีลบเดี่ยว · import merge-only · ตัด hint · ไม่โชว์ used | TC-SL06, TC-SL08, TC-SL09, TC-SL10, TC-SL04 |
| Governance | DOA null · NOTIF ไม่ emit · THB-only · Esc chain | TC-SL02, TC-SL05, TC-SL07, TC-EC06 |

### [AI-DEFAULT] propagation (00 §0.8)
| AD | ข้อ | Case |
|---|---|---|
| AD-BNK-01 | `used` = count Receipt/PV posted (ไม่นับ draft) — OQ-BNK-07 | TC-XT01 [AI-DEFAULT] (ต้อง simulate) · EC-02 ข้าม |
| AD-BNK-02 | optimistic-lock + idempotency | TC-CC01, TC-CC02 [AI-DEFAULT] (ต้อง simulate) |

### UI states / interaction
| item | cases |
|---|---|
| loaded list | TC-L01 |
| filtered-empty ("ไม่พบบัญชีธนาคารที่ตรงกับตัวกรอง" + "ล้างตัวกรอง") | TC-L03 |
| scroll preservation (Iron Rule #29) | TC-EC02 |
| sticky thead full-height (#96) | TC-EC01 |
| responsive 768–1180 sidebar off-canvas (#97) | TC-EC04 |
| double-submit guard (#44 / EC-09) | TC-EC03, TC-CC02 |
| Esc chain menu>modal>drawer | TC-EC05, TC-EC06 |
| status menu paint above drawer body (E2E R2 #3) | TC-S01 |
| toast top-center | ทุกเคส create/status/import/export |

---

## Data Sets

> ทุกค่ากรอกได้จริง. `code` เก็บ UPPERCASE. ธนาคาร/ประเภท/สถานะ เลือกจาก dropdown ด้วย label ที่เห็นบนจอ.
> เลขที่บัญชี "ใส่ขีดได้" (dash-strip 10–12 หลัก). ★ = checkbox "บัญชีรับหลัก"/"บัญชีจ่ายหลัก".

### ชุดถูก (happy)
| Set | code | ธนาคาร | เลขที่บัญชี | ชื่อบัญชี | ประเภท | promptpay | กลุ่ม GL | ฝั่ง | ★ | สถานะ |
|---|---|---|---|---|---|---|---|---|---|---|
| CR-1 | (เว้น→auto) | กสิกรไทย | 100-2-30040-5 | บริษัท คิวบ์ เนทีฟ จำกัด | ออมทรัพย์ | — | — ยังไม่ผูกกลุ่ม — | รับ | — | ใช้งาน |
| CR-CODE | MYBANK-99 | กรุงเทพ | 222-3-44455-6 | บัญชีทดสอบรหัสมือ | กระแสรายวัน | — | KBANK — ธนาคารกสิกรไทย | รับ+จ่าย | — | ใช้งาน |
| CR-FIXED | (เว้น→auto) | กรุงไทย | 333-1-22233-4 | บัญชีฝากประจำทดสอบ | ฝากประจำ | — | — | จ่าย | — | ใช้งาน |
| CR-GLBIND | (เว้น→auto) | กสิกรไทย | 401-2-30045-1 | บัญชีผูกกลุ่ม GL | ออมทรัพย์ | — | KBANK — ธนาคารกสิกรไทย | รับ | — | ใช้งาน |
| CR-NOGL | (เว้น→auto) | ยูโอบี | 501-2-30046-2 | บัญชีไม่ผูกกลุ่ม | ออมทรัพย์ | — | — ยังไม่ผูกกลุ่ม — | รับ | — | ใช้งาน |
| CR-PP10 | (เว้น→auto) | กรุงศรีอยุธยา | 601-2-30047-3 | บัญชีพร้อมเพย์เบอร์ | ออมทรัพย์ | 0899999999 (10) | — | รับ | — | ใช้งาน |
| CR-PP13 | (เว้น→auto) | ออมสิน | 701-2-30048-4 | บัญชีพร้อมเพย์เลขภาษี | ออมทรัพย์ | 0105561234999 (13) | — | รับ | — | ใช้งาน |
| CR-STAR | (เว้น→auto) | กรุงเทพ | 801-2-30049-5 | บัญชีตั้งดาวรับ | ออมทรัพย์ | — | — | รับ | **★รับ** | ใช้งาน |

### ชุดผิด (negative)
| Set | อธิบาย | ค่า |
|---|---|---|
| NEG-ACCT-SHORT | เลขบัญชี < 10 หลัก | code เว้น, ธนาคาร=กสิกรไทย, เลข=`123`, ชื่อ=ทดสอบ, ฝั่ง=รับ |
| NEG-ACCT-ALPHA | เลขบัญชีมีตัวอักษร (dash-strip < 10) | ธนาคาร=กสิกรไทย, เลข=`ABC-XYZ`, ชื่อ=ทดสอบ, ฝั่ง=รับ |
| NEG-ACCT-DUP | เลขบัญชีซ้ำทะเบียน (ตัดขีด) | ธนาคาร=กสิกรไทย, เลข=`0123456789` (= KBANK-01 012-3-45678-9), ชื่อ=ทดสอบ, ฝั่ง=รับ |
| NEG-NAME-EMPTY | ชื่อบัญชีว่าง | ธนาคาร=กสิกรไทย, เลข=`908-1-20030-4`, เว้นชื่อ, ฝั่ง=รับ |
| NEG-CODE-DUP | code ซ้ำของจริง | code=`KBANK-01`, ธนาคาร=กสิกรไทย, เลข=`908-1-20031-5`, ชื่อ=ทดสอบ, ฝั่ง=รับ |
| NEG-NO-SIDE | ไม่เลือกฝั่งเลย | ธนาคาร=กสิกรไทย, เลข=`908-1-20032-6`, ชื่อ=ทดสอบ, ปิดทั้ง 2 ฝั่ง |
| NEG-PP5 | promptpay 5 หลัก | ธนาคาร=กสิกรไทย, เลข=`908-1-20033-7`, ชื่อ=ทดสอบ, promptpay=`12345`, ฝั่ง=รับ |
| NEG-PP11 | promptpay 11 หลัก | ธนาคาร=กสิกรไทย, เลข=`908-1-20034-8`, ชื่อ=ทดสอบ, promptpay=`01234567890`, ฝั่ง=รับ |
| NEG-STAR-GUARD | ★รับ บนฝั่งที่ไม่เปิด | ธนาคาร=กสิกรไทย, เลข=`908-1-20035-9`, ชื่อ=ทดสอบ, ฝั่ง=**จ่าย** (ปิดรับ), ติ๊ก **★รับ** |
| NEG-STAR-DRAFT | ★ บนสถานะ ≠ ใช้งาน | ธนาคาร=กสิกรไทย, เลข=`908-1-20036-0`, ชื่อ=ทดสอบ, ฝั่ง=รับ, ติ๊ก ★รับ, สถานะ=**ร่าง** |

### ไฟล์ทดสอบ (Files)
> จอ Import มีเฉพาะ real file picker (`accept=.csv`) — ไม่มีปุ่ม demo. runner ต้องเตรียมไฟล์ต่อไปนี้ก่อนรัน (หัวคอลัมน์: `code,bank,branch,account_no,account_name,account_type,use_in,status`).

- **`bank_import_sample.csv`** (6 แถว = BULK_SAMPLE — 3 valid + 3 problem):
  ```
  code,bank,branch,account_no,account_name,account_type,use_in,status
  UOB-01,ยูโอบี,อโศก,201-1-22334-5,บริษัท คิวบ์ เนทีฟ จำกัด,ออมทรัพย์,รับ,ใช้งาน
  KTB-02,กรุงไทย,ปิ่นเกล้า,556-7-88990-1,บริษัท คิวบ์ เนทีฟ จำกัด,,,
  SCB-02,ไทยพาณิชย์,ท่าพระ (ปิดแล้ว),900-2-11122-3,บริษัท คิวบ์ เนทีฟ จำกัด,กระแสรายวัน,ทั้งสอง,ไม่ใช้งาน
  KBANK-01,กสิกรไทย,ซ้ำทะเบียน,012-9-99999-9,ซ้ำ,ออมทรัพย์,,ใช้งาน
  BAD-01,ธนาคารดวงดาว,-,123,ผิดหลายจุด,ออมทรัพย์,,ใช้งาน
  UOB-01,ยูโอบี,ซ้ำในไฟล์,201-1-22334-5,แถวซ้ำแถวแรก,ออมทรัพย์,,ใช้งาน
  ```
  ผลตรวจที่คาด (per row): แถว1 UOB-01=✓ · แถว2 KTB-02=✓ · แถว3 SCB-02=✓ · แถว4 KBANK-01=✗ `รหัสซ้ำ (CODE_DUPLICATE)` *(ดู Drift Log — FRD เขียน ACCT_DUPLICATE)* · แถว5 BAD-01=✗ `ธนาคารไม่รู้จัก (BAD_BANK)` · แถว6 UOB-01=✗ `รหัสซ้ำในไฟล์ (IN_FILE_DUPLICATE)`.
- **`bank_import_valid3.csv`** (3 แถวแรกจากด้านบน UOB-01/KTB-02/SCB-02 เท่านั้น — commit clean):
  ```
  code,bank,branch,account_no,account_name,account_type,use_in,status
  UOB-01,ยูโอบี,อโศก,201-1-22334-5,บริษัท คิวบ์ เนทีฟ จำกัด,ออมทรัพย์,รับ,ใช้งาน
  KTB-02,กรุงไทย,ปิ่นเกล้า,556-7-88990-1,บริษัท คิวบ์ เนทีฟ จำกัด,,,
  SCB-02,ไทยพาณิชย์,ท่าพระ (ปิดแล้ว),900-2-11122-3,บริษัท คิวบ์ เนทีฟ จำกัด,กระแสรายวัน,ทั้งสอง,ไม่ใช้งาน
  ```
- **`bad_type_use_status.csv`** (แถวเดียว ทดสอบ BAD_TYPE/BAD_USE/BAD_STATUS): `KX-90,กสิกรไทย,ทดสอบ,908-7-70001-2,บัญชีทดสอบ,เผือก,ซ้าย,รออนุมัติ` — คาด ✗ `ประเภทบัญชีไม่ถูกต้อง (BAD_TYPE)` (ด่านแรกที่ผิด).
- **`bank_accounts.xlsx`** (ไฟล์ ≠ .csv — ทดสอบ reject).

---

## Test Cases

### GROUP A — List / Search / Filter / Sort / Pager (P-01)

#### TC-L01 — เปิดหน้า List เห็นโครงครบ (happy / loaded)
- group: List · ความสำคัญ: สูง · trace: AT-03 / FN-16 / US-08
- actor (role): Finance Admin
- Setup: role=finance_admin · seed=8 บัญชีตาราง Seed · files=—
- Start: OPEN `#/finance/bank-master` (โหลด `f-bank.html`)
- ผ่านเมื่อ: เห็นหัวข้อ + stat 4 ใบ + ตาราง 8 แถว + footer นับถูก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/finance/bank-master` | — | หน้า List โหลด · breadcrumb "Finance › บัญชีธนาคาร" · sidebar "บัญชีธนาคาร" active | ☐ |
| 2 | VERIFY หัวข้อหน้า | — | เห็น "บัญชีธนาคาร" + ph-count "**8 บัญชี**" | ☐ |
| 3 | VERIFY แถบ Stats (4 ใบ) | — | "บัญชีทั้งหมด **8**" (meta "7 ธนาคาร") · "ใช้งานอยู่ **6**" · "ไม่ใช้งาน **1**" · "ร่าง **1**" | ☐ |
| 4 | VERIFY หัวตาราง | — | คอลัมน์: (checkbox) · รหัส · ธนาคาร / ชื่อบัญชี · เลขที่บัญชี · ประเภทบัญชี · กลุ่มบัญชี GL · ใช้ฝั่ง · สถานะ · จัดการ · มี 8 แถว | ☐ |
| 5 | VERIFY แถว KBANK-01 | — | รหัส "KBANK-01" มี badge "**★รับ**" · เลข "012-3-45678-9" · กลุ่ม GL "KBANK" · ใช้ฝั่ง "รับ + จ่าย" · pill "ใช้งาน" (เขียว) | ☐ |
| 6 | VERIFY แถว SCB-01 | — | รหัส "SCB-01" มี badge "**★จ่าย**" · ใช้ฝั่ง "ฝั่งจ่าย (PV)" | ☐ |
| 7 | VERIFY footer + toolbar | — | footer "แสดง **1–8 จาก 8 รายการ**" · toolbar มีปุ่ม "ส่งออก CSV" · "นำเข้า CSV" · "เพิ่มบัญชีธนาคาร" (แดง) | ☐ |

#### TC-L02 — ค้นหาด้วยรหัส (search พบ)
- group: List · ความสำคัญ: สูง · trace: AT-03 / FN-16
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "KBANK" → ช่องค้นหา "ค้นหารหัส ธนาคาร สาขา หรือเลขบัญชี…" | KBANK | ตารางเหลือ 2 แถว (KBANK-01, KBANK-02) · footer "แสดง 1–2 จาก 2 รายการ" | ☐ |
| 2 | VERIFY โฟกัส/scroll | — | โฟกัสยังอยู่ในช่องค้นหา · ตารางไม่เด้ง scroll (Iron Rule #29) | ☐ |

#### TC-L03 — ค้นหาไม่พบ (filtered-empty)
- group: List · ความสำคัญ: กลาง · trace: AT-21 / empty state
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ZZZNONE" → ช่องค้นหา | ZZZNONE | ตารางแสดง empty "**ไม่พบบัญชีธนาคารที่ตรงกับตัวกรอง**" + ปุ่ม "ล้างตัวกรอง" · footer "แสดง 0 จาก 0 รายการ" | ☐ |
| 2 | CLICK ปุ่ม "ล้างตัวกรอง" | — | ตารางกลับมา 8 แถว · ช่องค้นหาว่าง | ☐ |

#### TC-L04 — ค้นหาด้วยเลขบัญชี / สาขา
- group: List · ความสำคัญ: กลาง · trace: AT-03 / FN-16
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "987-6" → ช่องค้นหา | 987-6 | เหลือ 1 แถว (SCB-01, เลข 987-6-54321-0) | ☐ |
| 2 | Clear แล้ว TYPE "สีลม" → ช่องค้นหา | สีลม | เหลือ 1 แถว (BBL-01, สาขา สีลม) | ☐ |
| 3 | Clear แล้ว TYPE "กสิกร" → ช่องค้นหา | กสิกร | เหลือ 2 แถว (KBANK-01, KBANK-02 — ค้นชื่อธนาคาร) | ☐ |

#### TC-L05 — กรองด้วย Bank filter = กสิกรไทย
- group: List · ความสำคัญ: สูง · trace: AT-03 / FN-16 / FN-09
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "กสิกรไทย" → dropdown กรองธนาคาร | กสิกรไทย | ตารางเหลือ 2 แถว (KBANK-01, KBANK-02) · footer "แสดง 1–2 จาก 2 รายการ" | ☐ |
| 2 | VERIFY badge ★ | — | แถว KBANK-01 มี "★รับ" · KBANK-02 ไม่มี ★ | ☐ |
| 3 | SELECT "ทุกธนาคาร" → dropdown | ทุกธนาคาร | ตารางกลับมา 8 แถว | ☐ |

#### TC-L06 — กรองด้วย Status filter = ร่าง
- group: List · ความสำคัญ: สูง · trace: AT-03 / FN-16
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "ร่าง" → dropdown กรองสถานะ | ร่าง | เหลือ 1 แถว (TTB-01, pill "ร่าง") · footer "แสดง 1 จาก 1 รายการ" | ☐ |
| 2 | SELECT "ไม่ใช้งาน" → dropdown สถานะ | ไม่ใช้งาน | เหลือ 1 แถว (GSB-01, pill "ไม่ใช้งาน") | ☐ |

#### TC-L07 — Stat card filter = ใช้งานอยู่ (toggle)
- group: List · ความสำคัญ: สูง · trace: AT-03 / FN-16
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK การ์ด "ใช้งานอยู่" | — | การ์ดขึ้น active (กรอบเน้น) · ตารางเหลือ **6** แถว (ทุก active) · footer "แสดง 1–6 จาก 6 รายการ" | ☐ |
| 2 | CLICK การ์ด "ใช้งานอยู่" ซ้ำ | — | ยกเลิก filter · ตารางกลับมา 8 แถว | ☐ |
| 3 | CLICK การ์ด "บัญชีทั้งหมด" | — | reset ทุก filter · ตาราง 8 แถว | ☐ |

#### TC-L08 — Sort คอลัมน์ รหัส (asc/desc)
- group: List · ความสำคัญ: กลาง · trace: AT-03 / FN-16
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ลำดับเริ่มต้น | — | เรียงตาม รหัส asc (default): แถวแรก = BAY-01 (ตัวอักษรน้อยสุด) | ☐ |
| 2 | CLICK หัวคอลัมน์ "รหัส" | — | สลับเป็น desc · แถวแรก = TTB-01 (หรือรหัสมากสุดตามพจนานุกรม) | ☐ |
| 3 | CLICK หัวคอลัมน์ "เลขที่บัญชี" | — | เรียงตามเลขบัญชี asc · ตารางไม่เด้ง scroll (#29) | ☐ |
| 4 | CLICK หัวคอลัมน์ "สถานะ" | — | เรียงตามสถานะ · ลำดับเปลี่ยน (จัดกลุ่มตามสถานะ) | ☐ |

#### TC-L09 — Pager ทำงานเมื่อเกิน 8 แถว
- group: List · ความสำคัญ: กลาง · trace: AT-03 / FN-16
- Setup: role=finance_admin · seed=8 · files=— · เพิ่ม 1 record ให้เป็น 9 (ทำใน step 1)
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "เพิ่มบัญชีธนาคาร" → กรอก CR-1 → CLICK "ยืนยันสร้าง" | CR-1 | สร้างสำเร็จ · ph-count "9 บัญชี" · pager โผล่ 2 ปุ่มหน้า (1,2) · footer "แสดง 1–8 จาก 9 รายการ" | ☐ |
| 2 | CLICK ปุ่มหน้า "2" ใน pager | — | ไปหน้า 2 · เห็น 1 แถว · footer "แสดง 9–9 จาก 9 รายการ" | ☐ |
| 3 | TYPE "KBANK" → ช่องค้นหา | KBANK | filter reset ไปหน้า 1 · เหลือ 2 แถว | ☐ |

#### TC-L10 — filter ผสม (stat + bank + search)
- group: List · ความสำคัญ: กลาง · trace: AT-03 / FN-16
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK การ์ด "ใช้งานอยู่" | — | 6 แถว | ☐ |
| 2 | SELECT "กสิกรไทย" → dropdown ธนาคาร | กสิกรไทย | เหลือ 2 แถว (KBANK-01, KBANK-02 — active + กสิกร) | ☐ |
| 3 | TYPE "02" → ช่องค้นหา | 02 | เหลือ 1 แถว (KBANK-02) · footer "แสดง 1 จาก 1 รายการ" | ☐ |

#### TC-L11 — Select-all จาก thead + row highlight + bulk bar
- group: List · ความสำคัญ: สูง · trace: FN-15 / bulk selection
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox หัวตาราง (select all) | — | ทุกแถวถูกติ๊ก + พื้นแถวไฮไลต์ · โผล่ bulk bar "เลือก **8** รายการ" | ☐ |
| 2 | VERIFY ปุ่มใน bulk bar | — | มี "ตั้งเป็น ใช้งาน" · "ตั้งเป็น ร่าง" · "ตั้งเป็น ไม่ใช้งาน" · "ลบ" (แดง) · "ยกเลิกการเลือก" | ☐ |
| 3 | CLICK "ยกเลิกการเลือก" | — | ล้างการเลือก · bulk bar หาย · แถวไม่ไฮไลต์ | ☐ |

#### TC-L12 — คลิกแถว เปิด View drawer
- group: List · ความสำคัญ: สูง · trace: AT-03 / FN-23 / P-04
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "KBANK-01" (นอก checkbox/ปุ่มแก้ไข) | — | view drawer เลื่อนเข้าจากขวา · eyebrow "บัญชีธนาคาร · KBANK-01" · title = "กสิกรไทย xxx-x-xx78-9" (mask) | ☐ |
| 2 | CLICK ปุ่ม "ปิด" (หรือ PRESS Esc) | — | drawer ปิด กลับหน้า List | ☐ |

---

### GROUP B — Create Happy + GL + auto-code + defaults

> ฟอร์ม create (P-02) drawer 680px · 3 sections: **ข้อมูลบัญชี** → **บัญชีแยกประเภท (GL)** → **การใช้งาน** · footer ปุ่ม "ยืนยันสร้าง".
> ค่า default ตอนเปิด create: ประเภท = ออมทรัพย์ · สกุลเงิน = "THB — บาทไทย" (disabled) · ฝั่งรับเงิน = **ติ๊กไว้** · สถานะ = ใช้งาน.

#### TC-C01 — สร้างบัญชีครบ field + auto code (happy · AT-01)
- group: Create · ความสำคัญ: สูง · trace: AT-01 / BR-08,09,10 / FN-01,03,05,06 / S-01 / US-01
- actor (role): Finance Admin
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK ปุ่ม "เพิ่มบัญชีธนาคาร"
- ชุดข้อมูล: CR-1
- ผ่านเมื่อ: drawer ปิด + toast success + ph-count เป็น 9 + แถวใหม่ (code auto `KBANK-03`) ปรากฏ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "เพิ่มบัญชีธนาคาร" | — | drawer เปิด หัวข้อ "**เพิ่มบัญชีธนาคาร**" · เห็น 3 section title: "ข้อมูลบัญชี" / "บัญชีแยกประเภท (GL)" / "การใช้งาน" · footer ปุ่ม "ยืนยันสร้าง" | ☐ |
| 2 | VERIFY default ในฟอร์ม | — | ช่อง "รหัส" ว่าง (placeholder "เช่น KBANK-01 (เว้นว่าง = สร้างอัตโนมัติ)") · "ประเภทบัญชี" = ออมทรัพย์ · "สกุลเงิน" = "THB — บาทไทย" **disabled** · checkbox "ฝั่งรับเงิน (Receipt)" ติ๊กไว้ · สถานะ = ใช้งาน | ☐ |
| 3 | SELECT "กสิกรไทย" → ช่อง "ธนาคาร" | CR-1 | ช่องแสดง "กสิกรไทย" | ☐ |
| 4 | TYPE "100-2-30040-5" → ช่อง "เลขที่บัญชี" | CR-1 | ช่องแสดงค่าที่กรอก | ☐ |
| 5 | TYPE "บริษัท คิวบ์ เนทีฟ จำกัด" → ช่อง "ชื่อบัญชี" | CR-1 | ช่องแสดงค่าที่กรอก | ☐ |
| 6 | VERIFY การใช้งาน | — | checkbox "ฝั่งรับเงิน (Receipt)" ติ๊กอยู่ (ตรง CR-1) | ☐ |
| 7 | CLICK ปุ่ม "ยืนยันสร้าง" | — | drawer ปิด · WAIT toast (top-center) "**เพิ่มบัญชีธนาคาร "KBANK-03" แล้ว**" (เขียว) *(auto code = KBANK-03)* | ☐ |
| 8 | VERIFY List | — | ph-count "**9 บัญชี**" · มีแถว "KBANK-03" ประเภท "ออมทรัพย์" สถานะ "ใช้งาน" กลุ่ม GL "—" | ☐ |

#### TC-C02 — auto code `{bank}-{seq}` ไม่ชนกัน (AT-02 · FN-02)
- group: Create · ความสำคัญ: สูง · trace: AT-02 / BR-08 / FN-02 / S-01
- Setup: role=finance_admin · seed=8 (มี KBANK-01, KBANK-02) · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"
- ผ่านเมื่อ: เว้น code → ระบบ gen `KBANK-03` (seq ถัดไปไม่ชน)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "กสิกรไทย" → ธนาคาร · เว้นช่อง "รหัส" ว่าง | — | รหัสยังว่าง | ☐ |
| 2 | TYPE "100-2-30041-6" → เลขที่บัญชี · TYPE "บัญชีออโต้โค้ด" → ชื่อบัญชี | — | ช่องแสดงค่า | ☐ |
| 3 | CLICK "ยืนยันสร้าง" | — | toast "เพิ่มบัญชีธนาคาร "**KBANK-03**" แล้ว" (ไม่ใช่ KBANK-01/02 ที่มีแล้ว) · แถวใหม่ code "KBANK-03" | ☐ |

#### TC-C03 — เลือกครบ 9 ธนาคาร + 3 ประเภท (FN-03 / BR-10)
- group: Create · ความสำคัญ: กลาง · trace: FN-03 / BR-10 / S-01
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK dropdown "ธนาคาร" | — | เห็น **9 ตัวเลือก**: กสิกรไทย · ไทยพาณิชย์ · กรุงเทพ · กรุงไทย · ทีเอ็มบีธนชาต · กรุงศรีอยุธยา · ออมสิน · ยูโอบี · อื่น ๆ | ☐ |
| 2 | CLICK dropdown "ประเภทบัญชี" | — | เห็น **3 ตัวเลือก**: ออมทรัพย์ · กระแสรายวัน · ฝากประจำ | ☐ |
| 3 | SELECT "ฝากประจำ" → ประเภทบัญชี · SELECT "กรุงไทย" → ธนาคาร · TYPE "333-1-22233-4" → เลขบัญชี · TYPE "บัญชีฝากประจำทดสอบ" → ชื่อ · TOGGLE "ฝั่งจ่ายเงิน (Payment Voucher)" ON · TOGGLE "ฝั่งรับเงิน (Receipt)" OFF | CR-FIXED | ค่าครบ | ☐ |
| 4 | CLICK "ยืนยันสร้าง" | — | toast success · แถวใหม่ประเภท "ฝากประจำ" ใช้ฝั่ง "ฝั่งจ่าย (PV)" | ☐ |

#### TC-C04 — กรอก code เอง (UPPERCASE) + ผูกกลุ่ม GL
- group: Create · ความสำคัญ: กลาง · trace: AT-01 / BR-08 / BR-04
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"
- ชุดข้อมูล: CR-CODE

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "MYBANK-99" → ช่อง "รหัส" | CR-CODE | ช่องแสดง "MYBANK-99" | ☐ |
| 2 | SELECT "กรุงเทพ" → ธนาคาร · TYPE "222-3-44455-6" → เลขบัญชี · TYPE "บัญชีทดสอบรหัสมือ" → ชื่อ | CR-CODE | ค่าครบ | ☐ |
| 3 | SELECT "KBANK — ธนาคารกสิกรไทย" → ช่อง "กลุ่มบัญชี GL (Bank Posting Group)" | CR-CODE | ช่องแสดง "KBANK — ธนาคารกสิกรไทย" | ☐ |
| 4 | TOGGLE "ฝั่งจ่ายเงิน (Payment Voucher)" ON | CR-CODE | ทั้ง 2 ฝั่งติ๊ก | ☐ |
| 5 | CLICK "ยืนยันสร้าง" | — | toast "เพิ่มบัญชีธนาคาร "MYBANK-99" แล้ว" · แถวใหม่ code "MYBANK-99" กลุ่ม GL "KBANK" | ☐ |

#### TC-C05 — บันทึกได้โดยไม่ผูกกลุ่ม GL (binding OPTIONAL · BR-04)
- group: Create · ความสำคัญ: สูง · trace: BR-04 / FN-04 / OQ-BNK-02 (LOCK) / S-02
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"
- ชุดข้อมูล: CR-NOGL
- ผ่านเมื่อ: ไม่เลือกกลุ่ม GL ก็บันทึกได้ (ไม่มี error) · view แจ้งเตือนภายหลัง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง "กลุ่มบัญชี GL" | — | ค่าเริ่มต้น = "— ยังไม่ผูกกลุ่ม —" | ☐ |
| 2 | SELECT "ยูโอบี" → ธนาคาร · TYPE "501-2-30046-2" → เลขบัญชี · TYPE "บัญชีไม่ผูกกลุ่ม" → ชื่อ (คงกลุ่ม GL = ยังไม่ผูก) | CR-NOGL | ค่าครบ | ☐ |
| 3 | CLICK "ยืนยันสร้าง" | — | **ไม่มี** error เรื่องกลุ่ม GL · toast success · แถวใหม่ กลุ่ม GL แสดง "—" | ☐ |
| 4 | CLICK แถวใหม่ (เปิด view) | — | section "บัญชีแยกประเภท (GL)" แสดงคำเตือน "**ยังไม่ผูก — GL post ไม่ได้จนกว่าจะผูกกลุ่ม**" | ☐ |

#### TC-C06 — promptpay 10/13 หลัก ผ่าน (AT-05b · BR-06)
- group: Create · ความสำคัญ: กลาง · trace: AT-05b / BR-06 / FN-13
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"
- ชุดข้อมูล: CR-PP10, CR-PP13

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "กรุงศรีอยุธยา" → ธนาคาร · TYPE "601-2-30047-3" → เลขบัญชี · TYPE "บัญชีพร้อมเพย์เบอร์" → ชื่อ · TYPE "0899999999" → ช่อง "พร้อมเพย์ผูกบัญชี" | CR-PP10 | ช่อง promptpay แสดง 10 หลัก | ☐ |
| 2 | CLICK "ยืนยันสร้าง" | — | toast success (10 หลัก = ผ่าน) | ☐ |
| 3 | CLICK "เพิ่มบัญชีธนาคาร" → SELECT "ออมสิน" → ธนาคาร · TYPE "701-2-30048-4" → เลขบัญชี · TYPE "บัญชีพร้อมเพย์เลขภาษี" → ชื่อ · TYPE "0105561234999" → พร้อมเพย์ | CR-PP13 | ช่อง promptpay แสดง 13 หลัก | ☐ |
| 4 | CLICK "ยืนยันสร้าง" | — | toast success (13 หลัก = ผ่าน) | ☐ |

#### TC-C07 — สร้างพร้อมตั้ง ★รับ (active + ฝั่งเปิด)
- group: Create · ความสำคัญ: กลาง · trace: AT-07 / BR-03 / FN-07
- Setup: role=finance_admin · seed=8 (★รับ ปัจจุบัน = KBANK-01) · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"
- ชุดข้อมูล: CR-STAR
- ผ่านเมื่อ: ตั้ง ★รับ ได้ · KBANK-01 เดิมหลุด ★รับ (radio ทั้งระบบ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จด baseline | — | (เปิด view KBANK-01 ก่อน หรือดู list) จดว่า **KBANK-01 มี ★รับ** อยู่ก่อน (อ้างใน step 4) | ☐ |
| 2 | SELECT "กรุงเทพ" → ธนาคาร · TYPE "801-2-30049-5" → เลขบัญชี · TYPE "บัญชีตั้งดาวรับ" → ชื่อ (ฝั่งรับติ๊กอยู่ · สถานะ = ใช้งาน) | CR-STAR | ค่าครบ | ☐ |
| 3 | TOGGLE checkbox "บัญชีรับหลัก" (★รับ) ON | CR-STAR | checkbox ติ๊ก | ☐ |
| 4 | CLICK "ยืนยันสร้าง" | — | toast success · แถวใหม่มี badge "★รับ" · **KBANK-01 ไม่มี "★รับ" แล้ว** (เทียบกับ baseline step 1 — radio ทั้งระบบ ตัวเก่าหลุด) | ☐ |

#### TC-C08 — ปิด create ด้วย ยกเลิก / Esc / X (ไม่บันทึก)
- group: Create · ความสำคัญ: กลาง · trace: FN-25 / dirty-close
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ทดสอบยกเลิก" → ช่อง "ชื่อบัญชี" | — | ช่องแสดงค่า | ☐ |
| 2 | CLICK ปุ่ม "ยกเลิก" (footer) | — | drawer ปิด · ไม่มี toast · ph-count ยัง "8 บัญชี" (ไม่บันทึก) | ☐ |
| 3 | CLICK "เพิ่มบัญชีธนาคาร" → PRESS Esc | — | drawer ปิด · ยังคง 8 บัญชี | ☐ |

---

### GROUP C — Create Validation / Negative

> ทุกเคสกลุ่มนี้: drawer **ไม่ปิด** · ช่องที่ผิดขึ้นกรอบแดง (has-err) + inline error · (★ ผิด) มี toast error top-center. count ไม่เพิ่ม.

#### TC-V01 — เลขบัญชีสั้นเกิน (< 10 หลัก) → block (AT-04 · ERR_ACCT_INVALID)
- group: Validation · ความสำคัญ: สูง · trace: AT-04 / BR-01 / FN-12 / ERR_ACCT_INVALID
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"
- ชุดข้อมูล: NEG-ACCT-SHORT

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "กสิกรไทย" → ธนาคาร · TYPE "123" → เลขที่บัญชี · TYPE "ทดสอบ" → ชื่อบัญชี | NEG-ACCT-SHORT | ค่าในช่อง | ☐ |
| 2 | CLICK "ยืนยันสร้าง" | — | drawer ไม่ปิด · ช่อง "เลขที่บัญชี" กรอบแดง + inline "**เลขบัญชี 10–12 หลัก (ใส่ขีดได้)**" · ph-count ยัง 8 | ☐ |

#### TC-V02 — เลขบัญชีมีตัวอักษร (dash-strip < 10) → block (AT-04)
- group: Validation · ความสำคัญ: กลาง · trace: AT-04 / BR-01 / FN-12 / ERR_ACCT_INVALID
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"
- ชุดข้อมูล: NEG-ACCT-ALPHA

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "กสิกรไทย" → ธนาคาร · TYPE "ABC-XYZ" → เลขบัญชี · TYPE "ทดสอบ" → ชื่อ | NEG-ACCT-ALPHA | ค่าในช่อง | ☐ |
| 2 | CLICK "ยืนยันสร้าง" | — | block · ช่องเลขบัญชี has-err "เลขบัญชี 10–12 หลัก (ใส่ขีดได้)" (digits=0) | ☐ |

#### TC-V03 — เลขบัญชีซ้ำทะเบียน (ตัดขีด) → block (AT-05 · ERR_ACCT_DUPLICATE)
- group: Validation · ความสำคัญ: สูง · trace: AT-05 / BR-01 / FN-12 / ERR_ACCT_DUPLICATE
- Setup: role=finance_admin · seed=8 (KBANK-01 = 012-3-45678-9) · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"
- ชุดข้อมูล: NEG-ACCT-DUP
- ผ่านเมื่อ: เลขที่ตัดขีดตรงกับที่มี → block ด้วย ACCT_DUPLICATE (พิสูจน์ dash-strip)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "กสิกรไทย" → ธนาคาร · TYPE "0123456789" → เลขบัญชี (ไม่ใส่ขีด แต่ digits = KBANK-01) · TYPE "ทดสอบ" → ชื่อ | NEG-ACCT-DUP | ค่าในช่อง | ☐ |
| 2 | CLICK "ยืนยันสร้าง" | — | block · ช่องเลขบัญชี has-err "**เลขบัญชีนี้มีในทะเบียนแล้ว (ACCT_DUPLICATE)**" (เทียบตัดขีดกับ 012-3-45678-9) | ☐ |

#### TC-V04 — ชื่อบัญชีว่าง → block (ERR_REQUIRED)
- group: Validation · ความสำคัญ: สูง · trace: FN-12 / ERR_REQUIRED
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"
- ชุดข้อมูล: NEG-NAME-EMPTY

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "กสิกรไทย" → ธนาคาร · TYPE "908-1-20030-4" → เลขบัญชี · เว้นช่อง "ชื่อบัญชี" ว่าง | NEG-NAME-EMPTY | ชื่อว่าง | ☐ |
| 2 | CLICK "ยืนยันสร้าง" | — | block · ช่อง "ชื่อบัญชี" has-err "**กรุณากรอกชื่อบัญชี**" | ☐ |

#### TC-V05 — code ซ้ำของจริง → block (AT-02 · ERR_CODE_DUPLICATE)
- group: Validation · ความสำคัญ: สูง · trace: AT-02 / BR-08 / FN-12 / ERR_CODE_DUPLICATE
- Setup: role=finance_admin · seed=8 (มี KBANK-01) · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"
- ชุดข้อมูล: NEG-CODE-DUP

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "KBANK-01" → ช่อง "รหัส" · SELECT "กสิกรไทย" → ธนาคาร · TYPE "908-1-20031-5" → เลขบัญชี · TYPE "ทดสอบ" → ชื่อ | NEG-CODE-DUP | ค่าในช่อง | ☐ |
| 2 | CLICK "ยืนยันสร้าง" | — | block · ช่อง "รหัส" has-err "**รหัส KBANK-01 ถูกใช้แล้ว**" (case-insensitive) | ☐ |

#### TC-V06 — ไม่เลือกฝั่งเลย → block (AT-06 · ERR_USE_IN_EMPTY)
- group: Validation · ความสำคัญ: สูง · trace: AT-06 / BR-03 / FN-12 / ERR_USE_IN_EMPTY
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"
- ชุดข้อมูล: NEG-NO-SIDE

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "กสิกรไทย" → ธนาคาร · TYPE "908-1-20032-6" → เลขบัญชี · TYPE "ทดสอบ" → ชื่อ | NEG-NO-SIDE | ค่าในช่อง | ☐ |
| 2 | TOGGLE "ฝั่งรับเงิน (Receipt)" OFF (ปิดฝั่งรับที่ติ๊กมาให้) | — | ทั้ง 2 ฝั่งไม่ติ๊ก | ☐ |
| 3 | CLICK "ยืนยันสร้าง" | — | block · ช่อง "ใช้กับฝั่ง" has-err "**ต้องเลือกอย่างน้อย 1 ฝั่ง**" | ☐ |

#### TC-V07 — promptpay 5 หลัก → block (AT-05b · ERR_PROMPTPAY_INVALID)
- group: Validation · ความสำคัญ: กลาง · trace: AT-05b / BR-06 / FN-13 / ERR_PROMPTPAY_INVALID
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"
- ชุดข้อมูล: NEG-PP5

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "กสิกรไทย" → ธนาคาร · TYPE "908-1-20033-7" → เลขบัญชี · TYPE "ทดสอบ" → ชื่อ · TYPE "12345" → พร้อมเพย์ | NEG-PP5 | ค่าในช่อง | ☐ |
| 2 | CLICK "ยืนยันสร้าง" | — | block · ช่อง "พร้อมเพย์ผูกบัญชี" has-err "**ต้องเป็นเบอร์ 10 หลัก หรือเลขภาษี 13 หลัก**" | ☐ |

#### TC-V08 — promptpay 11 หลัก → block (boundary)
- group: Validation · ความสำคัญ: กลาง · trace: AT-05b / BR-06 / FN-13 / ERR_PROMPTPAY_INVALID
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"
- ชุดข้อมูล: NEG-PP11

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "กสิกรไทย" → ธนาคาร · TYPE "908-1-20034-8" → เลขบัญชี · TYPE "ทดสอบ" → ชื่อ · TYPE "01234567890" → พร้อมเพย์ (11 หลัก) | NEG-PP11 | ค่าในช่อง | ☐ |
| 2 | CLICK "ยืนยันสร้าง" | — | block · ช่องพร้อมเพย์ has-err "ต้องเป็นเบอร์ 10 หลัก หรือเลขภาษี 13 หลัก" (11 ≠ 10/13) | ☐ |

#### TC-V09 — แก้ error แล้วบันทึกผ่าน (recovery)
- group: Validation · ความสำคัญ: กลาง · trace: FN-12 / recovery
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "กสิกรไทย" → ธนาคาร · TYPE "12" → เลขบัญชี · TYPE "ทดสอบแก้ไข" → ชื่อ · CLICK "ยืนยันสร้าง" | — | block · เลขบัญชี has-err | ☐ |
| 2 | Clear "เลขที่บัญชี" → TYPE "909-1-20040-1" | — | ช่องแสดงเลขใหม่ (10+ หลัก) | ☐ |
| 3 | CLICK "ยืนยันสร้าง" | — | drawer ปิด · toast success (error หายหลังแก้) | ☐ |

#### TC-V10 — เลขบัญชี 13 หลัก (เกิน max 12) → block (boundary บน)
- group: Validation · ความสำคัญ: กลาง · trace: AT-04 / BR-01 / boundary
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "กสิกรไทย" → ธนาคาร · TYPE "1234567890123" → เลขบัญชี (13 digits) · TYPE "ทดสอบเกิน" → ชื่อ | — | ค่าในช่อง | ☐ |
| 2 | CLICK "ยืนยันสร้าง" | — | block · เลขบัญชี has-err "เลขบัญชี 10–12 หลัก (ใส่ขีดได้)" (13 > 12) | ☐ |

---

### GROUP D — ★ Default per side + DEFAULT_GUARD + radio

> "ใช้กับฝั่ง" = สิทธิ์ใช้ (≥1) · "บัญชีรับหลัก / บัญชีจ่ายหลัก" (★) = default 1 ตัว/ฝั่งทั้งระบบ (radio).

#### TC-DF01 — ★รับ radio ทั้งระบบ (ตั้งใหม่ ตัวเก่าหลุด · AT-07 · FN-07)
- group: Default · ความสำคัญ: สูง · trace: AT-07 / BR-03 / FN-07
- Setup: role=finance_admin · seed=8 (★รับ = KBANK-01) · files=—
- Start: OPEN `#/finance/bank-master`
- ผ่านเมื่อ: ตั้ง ★รับ ให้ตัวอื่น → KBANK-01 หลุด ★รับ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จด baseline | — | list: **KBANK-01 มี ★รับ** · KBANK-02 ไม่มี ★ (จดไว้อ้าง step 4) | ☐ |
| 2 | CLICK ปุ่มแก้ไข (ไอคอนดินสอ) แถว KBANK-02 | — | edit drawer เปิด (KBANK-02 used=12 · ธนาคาร/เลขบัญชี disabled + lock-tag — ★ แก้ได้) | ☐ |
| 3 | TOGGLE checkbox "บัญชีรับหลัก" (★รับ) ON → CLICK "บันทึกการแก้ไข" | — | toast "บันทึกการแก้ไข "KBANK-02" แล้ว" | ☐ |
| 4 | VERIFY list | — | แถว **KBANK-02 มี "★รับ"** · **KBANK-01 ไม่มี "★รับ" แล้ว** (radio ทั้งระบบ — เทียบ baseline step 1) | ☐ |

#### TC-DF02 — ★จ่าย แยกอิสระจาก ★รับ (คนละฝั่ง)
- group: Default · ความสำคัญ: กลาง · trace: AT-07 / BR-03 / FN-07
- Setup: role=finance_admin · seed=8 (★จ่าย = SCB-01) · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จด baseline | — | SCB-01 มี "★จ่าย" (จดไว้) | ☐ |
| 2 | CLICK ปุ่มแก้ไข แถว BBL-01 (used=88, active, รับ+จ่าย) | — | edit drawer เปิด | ☐ |
| 3 | TOGGLE "บัญชีจ่ายหลัก" (★จ่าย) ON → CLICK "บันทึกการแก้ไข" | — | toast success | ☐ |
| 4 | VERIFY list | — | BBL-01 มี "★จ่าย" · **SCB-01 ไม่มี "★จ่าย" แล้ว** · ★รับ ของฝั่งรับไม่ถูกกระทบ (คนละ radio) | ☐ |

#### TC-DF03 — 1 บัญชีเป็น ★ ได้ทั้ง 2 ฝั่ง (รับ+จ่าย)
- group: Default · ความสำคัญ: กลาง · trace: AT-07 / BR-03 / FN-07
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มแก้ไข แถว BBL-01 (รับ+จ่าย, active) | — | edit drawer เปิด · ทั้ง 2 ฝั่งเปิดอยู่ | ☐ |
| 2 | TOGGLE "บัญชีรับหลัก" ON · TOGGLE "บัญชีจ่ายหลัก" ON → CLICK "บันทึกการแก้ไข" | — | toast success | ☐ |
| 3 | VERIFY list | — | แถว BBL-01 มีทั้ง "★รับ" และ "★จ่าย" | ☐ |

#### TC-DF04 — ★รับ บนฝั่งที่ไม่เปิด → DEFAULT_GUARD block (AT-07 · ERR_DEFAULT_GUARD)
- group: Default · ความสำคัญ: สูง · trace: AT-07 / BR-03 / FN-08 / ERR_DEFAULT_GUARD
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"
- ชุดข้อมูล: NEG-STAR-GUARD
- ผ่านเมื่อ: ★รับ แต่ปิดฝั่งรับ → block + toast error

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "กสิกรไทย" → ธนาคาร · TYPE "908-1-20035-9" → เลขบัญชี · TYPE "ทดสอบ" → ชื่อ | NEG-STAR-GUARD | ค่าในช่อง | ☐ |
| 2 | TOGGLE "ฝั่งรับเงิน (Receipt)" OFF · TOGGLE "ฝั่งจ่ายเงิน (Payment Voucher)" ON | — | ฝั่งรับปิด ฝั่งจ่ายเปิด | ☐ |
| 3 | TOGGLE "บัญชีรับหลัก" (★รับ) ON | — | checkbox ★รับ ติ๊ก (แต่ฝั่งรับปิด) | ☐ |
| 4 | CLICK "ยืนยันสร้าง" | — | block · WAIT toast error (top-center) "**บัญชีหลักต้องอยู่ฝั่งที่เปิดใช้ และสถานะ "ใช้งาน" เท่านั้น**" · drawer ไม่ปิด | ☐ |

#### TC-DF05 — ★ บนสถานะ ≠ ใช้งาน → DEFAULT_GUARD block
- group: Default · ความสำคัญ: สูง · trace: AT-07 / BR-03 / FN-08 / ERR_DEFAULT_GUARD
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"
- ชุดข้อมูล: NEG-STAR-DRAFT

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "กสิกรไทย" → ธนาคาร · TYPE "908-1-20036-0" → เลขบัญชี · TYPE "ทดสอบ" → ชื่อ (ฝั่งรับเปิดอยู่) | NEG-STAR-DRAFT | ค่าในช่อง | ☐ |
| 2 | TOGGLE "บัญชีรับหลัก" (★รับ) ON · SELECT "ร่าง" → ช่อง "สถานะ" | — | ★รับ ติ๊ก · สถานะ = ร่าง | ☐ |
| 3 | CLICK "ยืนยันสร้าง" | — | block · toast error "บัญชีหลักต้องอยู่ฝั่งที่เปิดใช้ และสถานะ "ใช้งาน" เท่านั้น" | ☐ |

#### TC-DF06 — เปลี่ยนสถานะออก active → ★ ทั้ง 2 ฝั่งหลุด (AT-14 · FN-09)
- group: Default · ความสำคัญ: สูง · trace: AT-14 / BR-03 / FN-09
- Setup: role=finance_admin · seed=8 (KBANK-01 active + ★รับ) · files=—
- Start: OPEN `#/finance/bank-master`
- ผ่านเมื่อ: KBANK-01 → ไม่ใช้งาน แล้ว ★รับ หลุด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จด baseline | — | KBANK-01 = active + มี "★รับ" (จดไว้) | ☐ |
| 2 | CLICK แถว "KBANK-01" (เปิด view) → CLICK "เปลี่ยนสถานะ" | — | เมนูเปิด "เปลี่ยนสถานะเป็น" 3 ค่า (ค่า "ใช้งาน" disabled ป้าย "ปัจจุบัน") | ☐ |
| 3 | CLICK "ไม่ใช้งาน" ในเมนู | — | WAIT toast "เปลี่ยนสถานะ "KBANK-01" เป็น ไม่ใช้งาน แล้ว" | ☐ |
| 4 | VERIFY list แถว KBANK-01 | — | pill "ไม่ใช้งาน" · **ไม่มี badge "★รับ" แล้ว** (★ หลุดเมื่อออก active — เทียบ baseline step 1) | ☐ |

---

### GROUP E — Edit + IR-BNK-01 lock + save guard

#### TC-E01 — แก้บัญชี used=0 แก้ได้ทุก field (AT-10)
- group: Edit · ความสำคัญ: สูง · trace: AT-10 / S-04
- Setup: role=finance_admin · seed=8 (KTB-01 used=0) · files=—
- Start: OPEN `#/finance/bank-master`
- ผ่านเมื่อ: ธนาคาร+เลขบัญชี **ไม่ล็อก** · save ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มแก้ไข แถว "KTB-01" | — | edit drawer เปิด หัวข้อ "KTB-01" · footer ปุ่ม "**บันทึกการแก้ไข**" · ช่อง "ธนาคาร" + "เลขที่บัญชี" **ไม่ disabled** (ไม่มี lock-tag) | ☐ |
| 2 | TYPE " (ปรับสาขา)" ต่อท้าย → ช่อง "สาขา" · Clear "เลขที่บัญชี" → TYPE "555-6-77788-0" | — | ช่องแก้ได้ (used=0) | ☐ |
| 3 | CLICK "บันทึกการแก้ไข" | — | drawer ปิด · toast "**บันทึกการแก้ไข "KTB-01" แล้ว**" | ☐ |

#### TC-E02 — แก้บัญชี used>0 → ธนาคาร+เลขบัญชี disabled + lock-tag (AT-08 · FN-10)
- group: Edit · ความสำคัญ: สูง · trace: AT-08 / BR-02 / FN-10 / IR-BNK-01 (LOCK) / EC-01
- Setup: role=finance_admin · seed=8 (KBANK-01 used=620) · files=—
- Start: OPEN `#/finance/bank-master`
- ผ่านเมื่อ: 2 field ล็อก + lock-tag · field อื่นแก้ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มแก้ไข แถว "KBANK-01" | — | edit drawer เปิด · ช่อง "ธนาคาร" **disabled** · ช่อง "เลขที่บัญชี" **disabled** · ทั้ง 2 label มี lock-tag "**ล็อก — มีเอกสารผ่านแล้ว**" | ☐ |
| 2 | VERIFY field อื่น | — | ช่อง "ชื่อบัญชี" / "สาขา" / "ประเภทบัญชี" / "พร้อมเพย์" / "กลุ่มบัญชี GL" / checkbox ฝั่ง / ★ / สถานะ = **แก้ได้** (ไม่ disabled) | ☐ |
| 3 | VERIFY absence | — | **ไม่มี** การแสดงจำนวน `used` ที่ใดในฟอร์ม (S-10⑤) | ☐ |

#### TC-E03 — แก้ field อื่นของ used>0 → บันทึกได้ (ธนาคาร/เลขบัญชีคงเดิม)
- group: Edit · ความสำคัญ: สูง · trace: AT-08 / BR-02 / FN-10,11 / EC-03
- Setup: role=finance_admin · seed=8 (KBANK-01 used=620) · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มแก้ไข แถว "KBANK-01" | — | edit drawer เปิด (ธนาคาร/เลขบัญชี ล็อก) | ☐ |
| 2 | Clear "ชื่อบัญชี" → TYPE "บริษัท คิวบ์ เนทีฟ จำกัด (แก้ไข)" · SELECT "กระแสรายวัน" → ประเภทบัญชี | — | field อื่นรับค่า | ☐ |
| 3 | CLICK "บันทึกการแก้ไข" | — | toast "บันทึกการแก้ไข "KBANK-01" แล้ว" | ☐ |
| 4 | CLICK แถว KBANK-01 (view) | — | ชื่อ = "...(แก้ไข)" · ประเภท = กระแสรายวัน · **ธนาคาร ยัง "กสิกรไทย" · เลขบัญชี ยัง 012-3-45678-9** (ไม่เปลี่ยน) | ☐ |

#### TC-E04 — save guard: ฝืน DOM เปลี่ยนธนาคาร/เลขบัญชี → ไม่ persist (AT-09 · FN-11) `(ต้อง simulate)`
- group: Edit · ความสำคัญ: สูง · trace: AT-09 / BR-02 / FN-11 / EC-01 · **[AI-DEFAULT ไม่เกี่ยว — LOCK]**
- Setup: role=finance_admin · seed=8 (KBANK-01 used=620) · files=— · **inject:** ลบ attribute `disabled` ของ `#in-bank`/`#in-acct-no` ผ่าน devtools/JS แล้วเปลี่ยนค่า (จำลอง client ฝืน) — ถ้าทำไม่ได้ = BLOCKED
- Start: OPEN `#/finance/bank-master`
- ผ่านเมื่อ: แม้ฝืนเปลี่ยน DOM ค่าที่ save คงเป็น bank=KBANK / เลขเดิม (logic guard)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มแก้ไข แถว "KBANK-01" | — | edit drawer · ธนาคาร/เลขบัญชี disabled | ☐ |
| 2 | (simulate) ลบ `disabled` ของ `#in-bank` แล้ว SELECT "กรุงเทพ" · ลบ `disabled` ของ `#in-acct-no` แล้ว TYPE "999-9-99999-9" | — | DOM เปลี่ยนค่าชั่วคราว (ฝืน) | ☐ |
| 3 | CLICK "บันทึกการแก้ไข" | — | toast success | ☐ |
| 4 | CLICK แถว KBANK-01 (view) | — | **ธนาคาร ยัง "กสิกรไทย" · เลขบัญชี ยัง 012-3-45678-9** (logic guard `if(!locked){...}` ไม่ assign — ค่าที่ฝืนไม่ persist) | ☐ |

#### TC-E05 — เปลี่ยนประเภท/ฝั่ง/★ ของ used>0 ได้ (EC-03)
- group: Edit · ความสำคัญ: กลาง · trace: EC-03 / BR-02
- Setup: role=finance_admin · seed=8 (SCB-01 used=340, ★จ่าย) · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มแก้ไข แถว "SCB-01" | — | edit drawer · ธนาคาร/เลขบัญชี ล็อก · ฝั่ง/★/ประเภท แก้ได้ | ☐ |
| 2 | TOGGLE "ฝั่งรับเงิน (Receipt)" ON (เปิดเพิ่มฝั่งรับ) → CLICK "บันทึกการแก้ไข" | — | toast success | ☐ |
| 3 | VERIFY list แถว SCB-01 | — | ใช้ฝั่ง = "รับ + จ่าย" (เปลี่ยนได้แม้ used>0) · ★จ่าย คงอยู่ | ☐ |

#### TC-E06 — แก้ไขจาก View drawer (ปุ่ม "แก้ไข")
- group: Edit · ความสำคัญ: กลาง · trace: AT-10 / P-04
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "BBL-01" (เปิด view) → CLICK ปุ่ม "แก้ไข" | — | สลับเป็น edit drawer หัวข้อ "BBL-01" | ☐ |
| 2 | Clear "สาขา" → TYPE "สีลม (ปรับปรุง)" → CLICK "บันทึกการแก้ไข" | — | toast success · list สาขาอัปเดต | ☐ |

---

### GROUP F — GL picker active-only + keep-bound draft

#### TC-GL01 — picker กลุ่ม GL แสดงเฉพาะ active (SCB draft ไม่โผล่ · AT-11 · FN-04)
- group: GL · ความสำคัญ: สูง · trace: AT-11 / BR-04 / FN-04 / GL Contract (LOCK) / S-02
- Setup: role=finance_admin · seed=8 · GL groups: KBANK=active, SCB=draft · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"
- ผ่านเมื่อ: create ใหม่ → dropdown มีแค่ "— ยังไม่ผูกกลุ่ม —" + "KBANK" (ไม่มี SCB)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK dropdown "กลุ่มบัญชี GL (Bank Posting Group)" | — | เห็น **2 ตัวเลือกเท่านั้น**: "— ยังไม่ผูกกลุ่ม —" และ "KBANK — ธนาคารกสิกรไทย" · **ไม่มี** "SCB" (draft ถูกกรอง) | ☐ |

#### TC-GL02 — edit บัญชีผูก SCB(draft) → keep-bound แสดง "(ร่าง)" (AT-12 · EC-04)
- group: GL · ความสำคัญ: สูง · trace: AT-12 / BR-04 / FN-04 / EC-04 / OQ-BNK-02 (LOCK)
- Setup: role=finance_admin · seed=8 (SCB-01 ผูก SCB=draft) · files=—
- Start: OPEN `#/finance/bank-master`
- ผ่านเมื่อ: option "SCB … (ร่าง)" ปรากฏ + selected (กัน binding หลุด)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มแก้ไข แถว "SCB-01" | — | edit drawer เปิด | ☐ |
| 2 | VERIFY ช่อง "กลุ่มบัญชี GL" | — | ค่าที่เลือกอยู่ = "**SCB — ธนาคารไทยพาณิชย์ (ร่าง)**" (คงกลุ่มเดิมแม้ draft) | ☐ |
| 3 | CLICK dropdown "กลุ่มบัญชี GL" | — | เห็น option: "— ยังไม่ผูกกลุ่ม —" · "KBANK — ธนาคารกสิกรไทย" · "**SCB — ธนาคารไทยพาณิชย์ (ร่าง)**" (union current-bound แม้ draft) | ☐ |

#### TC-GL03 — rebind SCB(draft) → KBANK แล้ว save (แทนที่สะอาด)
- group: GL · ความสำคัญ: กลาง · trace: AT-12 / BR-04 / FN-04
- Setup: role=finance_admin · seed=8 (SCB-01 ผูก SCB=draft) · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มแก้ไข แถว "SCB-01" → SELECT "KBANK — ธนาคารกสิกรไทย" → ช่อง "กลุ่มบัญชี GL" | — | ช่องแสดง "KBANK — ธนาคารกสิกรไทย" | ☐ |
| 2 | CLICK "บันทึกการแก้ไข" | — | toast success | ☐ |
| 3 | VERIFY list แถว SCB-01 | — | คอลัมน์ "กลุ่มบัญชี GL" = "KBANK" (แทนที่ SCB draft สะอาด ไม่มี orphan) | ☐ |

#### TC-GL04 — ปลดกลุ่ม GL กลับเป็นไม่ผูก → view เตือน
- group: GL · ความสำคัญ: กลาง · trace: BR-04 / FN-24
- Setup: role=finance_admin · seed=8 (KBANK-02 ผูก KBANK) · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มแก้ไข แถว "KBANK-02" → SELECT "— ยังไม่ผูกกลุ่ม —" → กลุ่ม GL → CLICK "บันทึกการแก้ไข" | — | toast success · list กลุ่ม GL = "—" | ☐ |
| 2 | CLICK แถว KBANK-02 (view) | — | section "บัญชีแยกประเภท (GL)" เตือน "ยังไม่ผูก — GL post ไม่ได้จนกว่าจะผูกกลุ่ม" | ☐ |

---

### GROUP G — Status change (single + bulk) + ★ drop

#### TC-S01 — เปลี่ยนสถานะเดี่ยว จาก view menu (AT-13 · FN-14)
- group: Status · ความสำคัญ: สูง · trace: AT-13 / FN-14 / S-06 / US-05
- Setup: role=finance_admin · seed=8 (BBL-01 active) · files=—
- Start: OPEN `#/finance/bank-master`
- ผ่านเมื่อ: เมนู 3 ค่า ค่าปัจจุบัน disabled · เปลี่ยนได้ทุกทิศ · menu paint เหนือ drawer body

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "BBL-01" (view) → CLICK ปุ่ม "เปลี่ยนสถานะ" | — | เมนูเปิด (paint เหนือเนื้อ drawer) หัว "เปลี่ยนสถานะเป็น" · 3 รายการ: ใช้งาน (**disabled + ป้าย "ปัจจุบัน"**) · ไม่ใช้งาน · ร่าง | ☐ |
| 2 | CLICK "ร่าง" ในเมนู | — | WAIT toast "**เปลี่ยนสถานะ "BBL-01" เป็น ร่าง แล้ว**" | ☐ |
| 3 | VERIFY list แถว BBL-01 | — | pill สถานะ = "ร่าง" | ☐ |

#### TC-S02 — เปลี่ยนสถานะ ร่าง → ใช้งาน (ทุกทิศ)
- group: Status · ความสำคัญ: กลาง · trace: AT-13 / FN-14 / §5.2
- Setup: role=finance_admin · seed=8 (TTB-01 draft) · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "TTB-01" (view) → CLICK "เปลี่ยนสถานะ" | — | เมนู 3 ค่า · ค่า "ร่าง" disabled (ปัจจุบัน) | ☐ |
| 2 | CLICK "ใช้งาน" | — | toast "เปลี่ยนสถานะ "TTB-01" เป็น ใช้งาน แล้ว" · pill = "ใช้งาน" | ☐ |

#### TC-S03 — bulk set status หลายรายการ (FN-15)
- group: Status · ความสำคัญ: สูง · trace: AT-11(bulk) / FN-15 / S-06
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox แถว "KTB-01" + checkbox แถว "BAY-01" | — | 2 แถวไฮไลต์ · bulk bar "เลือก **2** รายการ" | ☐ |
| 2 | CLICK "ตั้งเป็น ไม่ใช้งาน" ใน bulk bar | — | WAIT toast "**เปลี่ยนสถานะ 2 รายการ เป็น ไม่ใช้งาน แล้ว**" · การเลือกล้าง | ☐ |
| 3 | VERIFY list | — | KTB-01 + BAY-01 pill = "ไม่ใช้งาน" · stat "ไม่ใช้งาน" เพิ่มเป็น 3 | ☐ |

#### TC-S04 — bulk set status = ร่าง + ยกเลิกการเลือก
- group: Status · ความสำคัญ: กลาง · trace: FN-15
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox หัวตาราง (select all) → CLICK "ตั้งเป็น ร่าง" | — | toast "เปลี่ยนสถานะ 8 รายการ เป็น ร่าง แล้ว" · stat "ร่าง" = 8 | ☐ |
| 2 | CLICK checkbox หัวตาราง (select all) → CLICK "ยกเลิกการเลือก" | — | bulk bar หาย · การเลือกล้าง | ☐ |

#### TC-S05 — bulk → ไม่ใช้งาน ทำ ★ หลุด (AT-14 · FN-09)
- group: Status · ความสำคัญ: สูง · trace: AT-14 / BR-03 / FN-09
- Setup: role=finance_admin · seed=8 (KBANK-01 ★รับ, SCB-01 ★จ่าย) · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จด baseline | — | KBANK-01 มี ★รับ · SCB-01 มี ★จ่าย (จดไว้) | ☐ |
| 2 | CLICK checkbox แถว "KBANK-01" + "SCB-01" → CLICK "ตั้งเป็น ไม่ใช้งาน" | — | toast "เปลี่ยนสถานะ 2 รายการ เป็น ไม่ใช้งาน แล้ว" | ☐ |
| 3 | VERIFY list | — | KBANK-01 = ไม่ใช้งาน + **ไม่มี ★รับ** · SCB-01 = ไม่ใช้งาน + **ไม่มี ★จ่าย** (★ หลุดเมื่อออก active) | ☐ |

#### TC-S06 — เปลี่ยนสถานะ ค่าปัจจุบันเลือกไม่ได้ (guard)
- group: Status · ความสำคัญ: กลาง · trace: FN-14
- Setup: role=finance_admin · seed=8 (GSB-01 inactive) · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "GSB-01" (view) → CLICK "เปลี่ยนสถานะ" | — | เมนู 3 ค่า · "ไม่ใช้งาน" disabled + ป้าย "ปัจจุบัน" (opacity จาง) · คลิกไม่ได้ | ☐ |
| 2 | CLICK "ใช้งาน" | — | toast "เปลี่ยนสถานะ "GSB-01" เป็น ใช้งาน แล้ว" | ☐ |

---

### GROUP H — Bulk delete + guard used>0

> ไม่มีปุ่มลบรายตัวในแถว (FN-90/VD-PDM) — ลบได้เฉพาะ bulk + confirm modal.

#### TC-D01 — bulk ลบ ตัว used=0 สำเร็จ (AT-15)
- group: Delete · ความสำคัญ: สูง · trace: AT-15 / BR-02 / FN-17,90 / S-07
- Setup: role=finance_admin · seed=8 (KTB-01 used=0) · files=—
- Start: OPEN `#/finance/bank-master`
- ผ่านเมื่อ: KTB-01 ถูกลบ · records 8→7

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox แถว "KTB-01" → CLICK "ลบ" (bulk bar) | — | modal เปิด "**ลบบัญชีธนาคาร 1 รายการ?**" · desc "การกระทำนี้ย้อนกลับไม่ได้" · ปุ่ม "**ลบ 1 รายการ**" (แดง, กดได้) | ☐ |
| 2 | CLICK "ลบ 1 รายการ" | — | modal ปิด · WAIT toast "**ลบแล้ว 1 รายการ**" · ph-count "7 บัญชี" · แถว KTB-01 หาย | ☐ |

#### TC-D02 — bulk ลบ ตัว used>0 ถูกข้าม (AT-15 · guard)
- group: Delete · ความสำคัญ: สูง · trace: AT-15 / BR-02 / FN-17
- Setup: role=finance_admin · seed=8 (KBANK-01 used=620) · files=—
- Start: OPEN `#/finance/bank-master`
- ผ่านเมื่อ: modal บอกยอดข้าม · ปุ่มลบ disabled (0 ตัวลบได้)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox แถว "KBANK-01" (used>0) → CLICK "ลบ" | — | modal "ลบบัญชีธนาคาร 1 รายการ?" · desc "**มี 1 รายการมีเอกสารรับ/จ่ายผ่านแล้ว — จะถูกข้าม ไม่ลบ (ใช้เปลี่ยนสถานะแทน)**" · ปุ่ม "ลบ **0** รายการ" **disabled** | ☐ |
| 2 | CLICK "ยกเลิก" (หรือ PRESS Esc) | — | modal ปิด · records ไม่เปลี่ยน (ยัง 8) | ☐ |

#### TC-D03 — bulk ลบ ผสม (used=0 + used>0) → ลบบางส่วน + รายงานข้าม
- group: Delete · ความสำคัญ: สูง · trace: AT-15 / BR-02 / FN-17
- Setup: role=finance_admin · seed=8 (KTB-01 used=0 + TTB-01 used=0 + KBANK-01 used>0) · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox "KTB-01" + "TTB-01" + "KBANK-01" → CLICK "ลบ" | — | modal "ลบบัญชีธนาคาร 3 รายการ?" · desc "มี 1 รายการมีเอกสารรับ/จ่ายผ่านแล้ว — จะถูกข้าม…" · ปุ่ม "**ลบ 2 รายการ**" (กดได้) | ☐ |
| 2 | CLICK "ลบ 2 รายการ" | — | WAIT toast (warning) "**ลบแล้ว 2 รายการ · ข้าม 1 (มีเอกสารผ่านแล้ว)**" · KTB-01+TTB-01 หาย · KBANK-01 ยังอยู่ · records 8→6 | ☐ |

#### TC-D04 — เลือกทั้งหน้า แล้วลบ (ตัว used>0 ทั้งหมดข้าม)
- group: Delete · ความสำคัญ: กลาง · trace: AT-15 / FN-15,17
- Setup: role=finance_admin · seed=8 (used=0: KTB-01, TTB-01) · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox หัวตาราง (select all 8) → CLICK "ลบ" | — | modal "ลบบัญชีธนาคาร 8 รายการ?" · desc "มี 6 รายการมีเอกสารรับ/จ่ายผ่านแล้ว — จะถูกข้าม…" · ปุ่ม "ลบ **2** รายการ" | ☐ |
| 2 | CLICK "ลบ 2 รายการ" | — | toast warning "ลบแล้ว 2 รายการ · ข้าม 6 (มีเอกสารผ่านแล้ว)" · เหลือ 6 แถว (ที่ used>0) | ☐ |

#### TC-D05 — ปิด modal ลบ ด้วย X / backdrop (ไม่ลบ)
- group: Delete · ความสำคัญ: กลาง · trace: FN-25 / Esc chain
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox "KTB-01" → CLICK "ลบ" → PRESS Esc | — | modal ปิด · records ไม่เปลี่ยน · การเลือกยังอยู่ (bulk bar ยังโชว์) | ☐ |

---

### GROUP I — CSV Import (merge-only, 3 จังหวะ)

> จอ import = modal .is-wide · 3 จังหวะ pick → preview → done · **มีเฉพาะ real file picker (accept=.csv)** + ปุ่ม "ดาวน์โหลด template ตัวอย่าง". runner ต้องเตรียมไฟล์ (§ไฟล์ทดสอบ).

#### TC-IM01 — เปิด import modal + ดาวน์โหลด template (FN-18)
- group: Import · ความสำคัญ: กลาง · trace: AT-16 / FN-18 / BR-07
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`
- ผ่านเมื่อ: modal 3 จังหวะ · จังหวะ pick มี upload-box + template เท่านั้น (ไม่มีตัวเลือกโหมด Replace)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม "นำเข้า CSV" | — | modal เปิด title "**นำเข้าบัญชีธนาคารจากไฟล์**" · desc "ไฟล์ CSV — ระบุสถานะได้ในไฟล์ · เพิ่มรายการใหม่เท่านั้น" · upload-box "เลือกไฟล์ CSV" · footer ปุ่ม "ดาวน์โหลด template ตัวอย่าง" | ☐ |
| 2 | VERIFY absence | — | **ไม่มี** ตัวเลือก "Replace / Merge" หรือ radio โหมดใด ๆ (merge/append-only) | ☐ |
| 3 | CLICK "ดาวน์โหลด template ตัวอย่าง" | — | WAIT toast "**ดาวน์โหลด template ตัวอย่างแล้ว**" · ไฟล์ `bank_import_template.csv` ดาวน์โหลด | ☐ |

#### TC-IM02 — preview 6 แถว: ✓/✗ ต่อแถว + สรุปนับ (AT-16 · FN-19)
- group: Import · ความสำคัญ: สูง · trace: AT-16 / FN-19 / BR-01,07,10
- Setup: role=finance_admin · seed=8 · files=**`bank_import_sample.csv`** (6 แถว)
- Start: OPEN `#/finance/bank-master` → CLICK "นำเข้า CSV"
- ผ่านเมื่อ: preview "นำเข้าได้ 3 · ติดปัญหา 3" + ผลตรวจต่อแถวถูก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK upload-box "เลือกไฟล์ CSV" → UPLOAD `bank_import_sample.csv` | bank_import_sample.csv | จังหวะ preview · สรุป "**ตรวจแล้ว 6 แถว — นำเข้าได้ 3 · ติดปัญหา 3 (แถวผิดจะถูกข้าม)**" | ☐ |
| 2 | VERIFY แถว valid | — | UOB-01 (แถว1) · KTB-02 · SCB-02 = "**✓ พร้อมนำเข้า**" (pill เขียว) | ☐ |
| 3 | VERIFY แถว KBANK-01 | — | "✗ **รหัสซ้ำ (CODE_DUPLICATE)**" *(HTML actual — ดู Drift Log; FRD เขียน ACCT_DUPLICATE)* | ☐ |
| 4 | VERIFY แถว BAD-01 | — | "✗ **ธนาคารไม่รู้จัก (BAD_BANK)**" | ☐ |
| 5 | VERIFY แถว UOB-01 (แถวที่ 6) | — | "✗ **รหัสซ้ำในไฟล์ (IN_FILE_DUPLICATE)**" | ☐ |
| 6 | VERIFY ปุ่ม commit | — | ปุ่ม "**นำเข้า 3 แถว**" (กดได้) | ☐ |

#### TC-IM03 — ตรวจ IN_FILE_DUPLICATE เด่นชัด (FN-19)
- group: Import · ความสำคัญ: สูง · trace: AT-16 / FN-19 / BR-01
- Setup: role=finance_admin · seed=8 · files=`bank_import_sample.csv`
- Start: OPEN `#/finance/bank-master` → CLICK "นำเข้า CSV"
- ผ่านเมื่อ: UOB-01 แถวแรก ผ่าน · UOB-01 แถวสอง = IN_FILE_DUPLICATE (ซ้ำกันเองในไฟล์)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `bank_import_sample.csv` | bank_import_sample.csv | preview 6 แถว | ☐ |
| 2 | VERIFY UOB-01 คู่แรก vs คู่สอง | — | แถวแรก UOB-01 = "✓ พร้อมนำเข้า" · แถวสอง UOB-01 (เลข/รหัสเดียวกัน) = "✗ รหัสซ้ำในไฟล์ (IN_FILE_DUPLICATE)" — ตรวจนอกเหนือ ACCT_DUPLICATE ทะเบียน | ☐ |

#### TC-IM04 — per-row error อื่น (BAD_BANK/ACCT_INVALID/BAD_TYPE) (FN-19 · BR-10)
- group: Import · ความสำคัญ: กลาง · trace: AT-16 / FN-19 / BR-10 / ERR_BAD_BANK/ERR_BAD_TYPE
- Setup: role=finance_admin · seed=8 · files=`bank_import_sample.csv` + `bad_type_use_status.csv`
- Start: OPEN `#/finance/bank-master` → CLICK "นำเข้า CSV"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `bank_import_sample.csv` → VERIFY แถว BAD-01 | bank_import_sample.csv | BAD-01 (ธนาคาร "ธนาคารดวงดาว" + เลข "123") = "✗ ธนาคารไม่รู้จัก (BAD_BANK)" (ด่านธนาคารก่อนเลขบัญชี) | ☐ |
| 2 | CLICK "ยกเลิก" → CLICK "นำเข้า CSV" → UPLOAD `bad_type_use_status.csv` | bad_type_use_status.csv | แถว KX-90 (ประเภท "เผือก") = "✗ **ประเภทบัญชีไม่ถูกต้อง (BAD_TYPE)**" · สรุป "นำเข้าได้ 0 · ติดปัญหา 1" · ปุ่มนำเข้า disabled | ☐ |

#### TC-IM05 — commit merge-only 3 แถว + defaults + summary (AT-17 · FN-20,21)
- group: Import · ความสำคัญ: สูง · trace: AT-17 / FN-20,21 / BR-07
- Setup: role=finance_admin · seed=8 · files=`bank_import_sample.csv`
- Start: OPEN `#/finance/bank-master` → CLICK "นำเข้า CSV"
- ผ่านเมื่อ: เพิ่ม 3 record · toast warning มีข้าม 3 · done summary + ตารางข้าม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `bank_import_sample.csv` → CLICK "นำเข้า 3 แถว" | bank_import_sample.csv | จังหวะ done · สรุป "**นำเข้าเสร็จ 3 รายการ (สถานะตามไฟล์) · ข้าม 3 แถว (IMPORT_ERROR)**" · ตารางแถวข้าม 3 (KBANK-01/BAD-01/UOB-01) พร้อมสาเหตุ | ☐ |
| 2 | WAIT toast | — | toast (warning) "**นำเข้าแล้ว 3 รายการ · ข้าม 3 แถว (IMPORT_ERROR)**" | ☐ |
| 3 | CLICK "ปิด" → VERIFY List | — | ph-count "**11 บัญชี**" (8+3) · มีแถว UOB-01, KTB-02, SCB-02 | ☐ |
| 4 | CLICK แถว "KTB-02" (view) — ตรวจ default ของแถวที่เว้นค่า | — | ประเภท = **ออมทรัพย์** · ใช้ฝั่ง = **รับ + จ่าย** (ทั้งสอง) · สถานะ = **ร่าง** · กลุ่ม GL = "—" (ไฟล์ไม่มี posting_group) · ไม่มี promptpay | ☐ |

#### TC-IM06 — commit ไฟล์ valid ล้วน → toast success (ไม่มีข้าม)
- group: Import · ความสำคัญ: กลาง · trace: AT-17 / FN-20,21 / BR-07
- Setup: role=finance_admin · seed=8 · files=`bank_import_valid3.csv`
- Start: OPEN `#/finance/bank-master` → CLICK "นำเข้า CSV"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `bank_import_valid3.csv` | bank_import_valid3.csv | preview "ตรวจแล้ว 3 แถว — นำเข้าได้ 3 · ติดปัญหา 0" · ทุกแถว "✓ พร้อมนำเข้า" | ☐ |
| 2 | CLICK "นำเข้า 3 แถว" | — | done "นำเข้าเสร็จ 3 รายการ (สถานะตามไฟล์)" (ไม่มีตารางข้าม) · WAIT toast (success) "**นำเข้าแล้ว 3 รายการ**" | ☐ |
| 3 | CLICK "ปิด" → VERIFY List | — | ph-count "11 บัญชี" | ☐ |

#### TC-IM07 — เลือกไฟล์ ≠ .csv → reject (AT-17b · EC-10)
- group: Import · ความสำคัญ: กลาง · trace: AT-17b / EC-10
- Setup: role=finance_admin · seed=8 · files=`bank_accounts.xlsx`
- Start: OPEN `#/finance/bank-master` → CLICK "นำเข้า CSV"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK upload-box → UPLOAD `bank_accounts.xlsx` (ผ่าน file picker; ถ้า picker กรอง .csv ให้เลือก "ไฟล์ทั้งหมด") | bank_accounts.xlsx | WAIT toast (warning) "**โหมดสาธิตรองรับเฉพาะ .csv — .xlsx ให้ save as CSV ก่อน (dev: parser จริงตอน integrate)**" · ไม่เข้าจังหวะ preview | ☐ |

#### TC-IM08 — merge-only ไม่แตะ record เดิม (append)
- group: Import · ความสำคัญ: กลาง · trace: AT-17 / BR-07 / FN-20
- Setup: role=finance_admin · seed=8 · files=`bank_import_valid3.csv`
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จด baseline | — | จดค่า KBANK-01 (used=620, ★รับ, active) ก่อน import | ☐ |
| 2 | CLICK "นำเข้า CSV" → UPLOAD `bank_import_valid3.csv` → CLICK "นำเข้า 3 แถว" → CLICK "ปิด" | bank_import_valid3.csv | ph-count "11 บัญชี" | ☐ |
| 3 | VERIFY KBANK-01 | — | KBANK-01 ยังคงเดิมทุกค่า (used/★รับ/active ไม่ถูกแตะ — เพิ่มอย่างเดียว) | ☐ |

---

### GROUP J — Export CSV

#### TC-X01 — ส่งออกทั้งหมด (BOM + filename + toast · AT-18 · FN-22)
- group: Export · ความสำคัญ: กลาง · trace: AT-18 / FN-22 / US-08
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`
- ผ่านเมื่อ: ดาวน์โหลด `bank_export_YYYY-MM-DD.csv` + toast

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม "ส่งออก CSV" | — | ไฟล์ดาวน์โหลดชื่อ "**bank_export_2026-08-11.csv**" (วันที่ปัจจุบัน) · WAIT toast (success) "**ส่งออก 8 รายการเป็น CSV แล้ว**" | ☐ |
| 2 | VERIFY ไฟล์ (ถ้าเปิดได้) | — | หัวคอลัมน์ `code,bank,branch,account_no,account_name,account_type,use_in,status` (roundtrip กับ template) · มี BOM · ค่า ธนาคาร/ประเภท/ฝั่ง/สถานะ เป็นไทย | ☐ |

#### TC-X02 — ส่งออกตาม filter ปัจจุบัน (subset)
- group: Export · ความสำคัญ: กลาง · trace: AT-18 / FN-22
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "กสิกรไทย" → dropdown ธนาคาร | — | เหลือ 2 แถว (KBANK-01, KBANK-02) | ☐ |
| 2 | CLICK "ส่งออก CSV" | — | toast "**ส่งออก 2 รายการเป็น CSV แล้ว**" (ตาม filter, ไม่ใช่ 8) | ☐ |

---

### GROUP K — View drawer (P-04)

#### TC-VW01 — view header mask เลขบัญชี + 4 summary chips (FN-23 · EC-11)
- group: View · ความสำคัญ: กลาง · trace: FN-23 / EC-11 (mask) / §6
- Setup: role=finance_admin · seed=8 (KBANK-01) · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "KBANK-01" | — | view drawer · title = "**กสิกรไทย xxx-x-xx78-9**" (เลขบัญชี masked) · eyebrow "บัญชีธนาคาร · KBANK-01" | ☐ |
| 2 | VERIFY summary chips | — | 4 chip: **ธนาคาร** / **เลขที่บัญชี** / **ใช้กับฝั่ง** (รับ + จ่าย) / **กลุ่มบัญชี GL** (KBANK) | ☐ |

#### TC-VW02 — view chip กลุ่ม GL = "ยังไม่ผูก" เมื่อไม่ผูก
- group: View · ความสำคัญ: กลาง · trace: FN-23,24 / BR-04
- Setup: role=finance_admin · seed=8 (BBL-01 ไม่ผูกกลุ่ม) · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "BBL-01" | — | chip "กลุ่มบัญชี GL" = "**ยังไม่ผูก**" | ☐ |

#### TC-VW03 — view tabs ภาพรวม / ประวัติ (FN-24)
- group: View · ความสำคัญ: กลาง · trace: FN-24
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "KBANK-01" | — | tab "ภาพรวม" active · 3 section: "ข้อมูลบัญชี" / "บัญชีแยกประเภท (GL)" / "การใช้งานในเอกสาร" | ☐ |
| 2 | VERIFY section การใช้งาน | — | "ฝั่งรับเงิน (Receipt)" = "เปิดใช้ · ★ บัญชีรับหลัก" · "ฝั่งจ่ายเงิน (PV)" = "เปิดใช้" | ☐ |
| 3 | CLICK tab "ประวัติ" | — | timeline: แก้ไขล่าสุด / สร้างรายการ (actor + วันที่) | ☐ |

#### TC-VW04 — view GL warning เมื่อไม่ผูกกลุ่ม (FN-24 · BR-04)
- group: View · ความสำคัญ: สูง · trace: FN-24 / BR-04 / OQ-BNK-02 (LOCK)
- Setup: role=finance_admin · seed=8 (KTB-01 ไม่ผูกกลุ่ม) · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "KTB-01" → VERIFY section "บัญชีแยกประเภท (GL)" | — | คำเตือน "**ยังไม่ผูก — GL post ไม่ได้จนกว่าจะผูกกลุ่ม**" | ☐ |
| 2 | CLICK แถว "KBANK-01" (ผูก KBANK) → VERIFY section GL | — | ไม่มีคำเตือน · แสดง resolve "ตามกลุ่ม KBANK ใน GL Posting Group" | ☐ |

#### TC-VW05 — view แสดง ★รับ/★จ่าย badge (FN-09)
- group: View · ความสำคัญ: กลาง · trace: FN-09 / §6
- Setup: role=finance_admin · seed=8 (SCB-01 ★จ่าย) · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "SCB-01" → VERIFY section การใช้งาน | — | "ฝั่งจ่ายเงิน (PV)" = "เปิดใช้ · **★ บัญชีจ่ายหลัก**" · "ฝั่งรับเงิน (Receipt)" = "—" | ☐ |

---

### GROUP L — v8 / regression (#96 / #29 / #44 / #97 / Esc / empty)

#### TC-EC01 — #96 sticky thead full-height
- group: Regression · ความสำคัญ: กลาง · trace: FN-25 / Iron Rule #96
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตาราง | — | ตารางอยู่ใน `.table-scroll` ติดขอบล่าง content · หัวตาราง (thead) sticky | ☐ |
| 2 | (ถ้ามีแถวเกินจอ) Scroll ในตาราง | — | thead ค้างด้านบนขณะ scroll | ☐ |

#### TC-EC02 — #29 scroll/focus preserve ตอน re-render
- group: Regression · ความสำคัญ: กลาง · trace: FN-25 / Iron Rule #29
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่องค้นหา → TYPE "0" ทีละตัว | 0 | ตารางกรอง live · **โฟกัสยังอยู่ในช่องค้นหา** · ตารางไม่เด้ง scroll ขึ้นบน | ☐ |
| 2 | SELECT "ใช้งาน" → dropdown สถานะ | — | กรองแล้ว scroll ตำแหน่งเดิมคงอยู่ (ไม่กระโดด) | ☐ |

#### TC-EC03 — #44 double-submit guard (create)
- group: Regression · ความสำคัญ: กลาง · trace: EC-09 / AD-BNK-02 [AI-DEFAULT] / #44
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | กรอก CR-1 (ธนาคาร/เลขบัญชี/ชื่อ) → CLICK "ยืนยันสร้าง" **2 ครั้งเร็ว ๆ** | CR-1 | ปุ่ม "ยืนยันสร้าง" กลาย disabled/pointer-events:none หลังคลิกแรก · สร้าง record **1 รายการเท่านั้น** (ไม่ซ้ำ) · ph-count เพิ่ม 1 (เป็น 9 ไม่ใช่ 10) | ☐ |

#### TC-EC04 — #97 responsive 768–1180 (sidebar off-canvas)
- group: Regression · ความสำคัญ: กลาง · trace: FN-25 / Iron Rule #97
- Setup: role=finance_admin · seed=8 · files=— · viewport ปรับได้
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ปรับ viewport กว้าง ~1000px (ช่วง 768–1180) | — | sidebar ยุบเป็น off-canvas · โผล่ปุ่ม hamburger (`.nav-toggle`) | ☐ |
| 2 | CLICK ปุ่ม hamburger | — | sidebar เลื่อนเข้า · เห็นเมนู Finance › บัญชีธนาคาร | ☐ |

#### TC-EC05 — Esc chain: menu > modal > drawer
- group: Regression · ความสำคัญ: กลาง · trace: FN-25 / AT-21 / Esc chain
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว "BBL-01" (view) → CLICK "เปลี่ยนสถานะ" (เมนูเปิด) → PRESS Esc | — | เมนูปิดก่อน · drawer ยังเปิด | ☐ |
| 2 | PRESS Esc อีกครั้ง | — | view drawer ปิด · กลับ List | ☐ |

#### TC-EC06 — ปิด drawer/modal 3 ทาง (Esc/backdrop/X) + reload สะอาด (AT-21)
- group: Regression · ความสำคัญ: กลาง · trace: AT-21 / FN-25 / 0 console error
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "เพิ่มบัญชีธนาคาร" → CLICK ปุ่ม X (มุมขวาบน drawer) | — | drawer ปิด | ☐ |
| 2 | CLICK "นำเข้า CSV" → CLICK นอก modal (backdrop) หรือ X | — | modal ปิด | ☐ |
| 3 | Reload หน้า (กลาง state) | — | กลับหน้า List สะอาด · **0 console error** (ตรวจ devtools console) | ☐ |

---

### GROUP M — Scope-Lock / FN-40 "must-NOT-exist"

> ทุกเคสยืนยัน "ไม่มี" ของที่ตัดออก (LOCK/มติ). ผ่านเมื่อเห็นว่า element/option/ปุ่มนั้น **ไม่ปรากฏ**.

#### TC-SL01 — ไม่มีเส้นออก Payment Method + ไม่มีปุ่มลบรายตัว (OQ-BNK-01=NO · FN-90 · XT-05)
- group: Scope-Lock · ความสำคัญ: สูง · trace: OQ-BNK-01 (LOCK) / XT-05 / FN-90 / VD-PDM
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถวตาราง คอลัมน์ "จัดการ" | — | มีเฉพาะปุ่ม **แก้ไข (ดินสอ)** · **ไม่มี** ปุ่มลบรายตัว/ไอคอนถังขยะในแถว | ☐ |
| 2 | VERIFY view drawer (KBANK-01) | — | มีปุ่ม "แก้ไข" · "เปลี่ยนสถานะ" · "ปิด" — **ไม่มี** ปุ่ม/ลิงก์ "ส่งไป Payment Method" หรือ interface ไป PM ใด ๆ | ☐ |

#### TC-SL02 — สกุลเงิน THB disabled (ไม่มีสกุลอื่น · BR-09 · FN-05 · FN-40)
- group: Scope-Lock · ความสำคัญ: สูง · trace: AT-19 / BR-09 / FN-05,40
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง "สกุลเงิน" (section GL) | — | ค่า = "**THB — บาทไทย**" · **disabled** (แก้ไม่ได้) · ไม่ใช่ dropdown ที่มีสกุลอื่น | ☐ |

#### TC-SL03 — ไม่มี SWIFT/IBAN/ยอดคงเหลือ/opening balance (FN-40)
- group: Scope-Lock · ความสำคัญ: สูง · trace: AT-19 / BR-09 / FN-40 / S-10①②③
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ทุก section ของฟอร์ม | — | **ไม่มี** ช่อง SWIFT / IBAN / ยอดคงเหลือ / opening balance ที่ใดในฟอร์ม | ☐ |
| 2 | CLICK แถว KBANK-01 (view) → VERIFY | — | view ไม่มีข้อมูลยอดคงเหลือ/opening balance ที่ใด | ☐ |

#### TC-SL04 — ไม่โชว์จำนวน `used` บนจอ (มติ r2 · FN-40)
- group: Scope-Lock · ความสำคัญ: สูง · trace: AT-19 / BR-02 / FN-40 / S-10⑤
- Setup: role=finance_admin · seed=8 (KBANK-01 used=620) · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตาราง List | — | **ไม่มี** คอลัมน์/ตัวเลขแสดง `used` (620 ไม่โผล่ที่ใด) | ☐ |
| 2 | CLICK แถว KBANK-01 (view) + CLICK ปุ่มแก้ไข | — | ทั้ง view + edit form **ไม่แสดงจำนวน used** (guard อยู่ใน logic เท่านั้น) | ☐ |

#### TC-SL05 — ไม่มีผู้อนุมัติ/วงเงิน/สายอนุมัติ (DOA null · FN-06 · FN-40)
- group: Scope-Lock · ความสำคัญ: กลาง · trace: OB-6 / FN-06,40 / Governance (LOCK)
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ฟอร์ม + view | — | **ไม่มี** ช่อง/ปุ่ม ผู้มีอำนาจเซ็น / วงเงิน / สายอนุมัติ / approval chain · commit ทันทีไม่มีขั้นอนุมัติ | ☐ |

#### TC-SL06 — สถานะมีแค่ 3 ค่า ไม่มี archive/reactivate (§5.2 · FN-40)
- group: Scope-Lock · ความสำคัญ: กลาง · trace: §5.2 / VD-PDM
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY dropdown กรองสถานะ | — | มีแค่ "ทุกสถานะ / ร่าง / ใช้งาน / ไม่ใช้งาน" — **ไม่มี** archived/reactivate | ☐ |
| 2 | CLICK view KBANK-01 → "เปลี่ยนสถานะ" | — | เมนูมี **3 ค่าเท่านั้น** (ใช้งาน/ไม่ใช้งาน/ร่าง) | ☐ |

#### TC-SL07 — ไม่มี NOTIF/แจ้งเตือน event ของ feature (Governance)
- group: Scope-Lock · ความสำคัญ: ต่ำ · trace: §1.5 / Governance (LOCK)
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | สร้าง/เปลี่ยนสถานะบัญชี 1 รายการ → VERIFY | — | feedback = toast เท่านั้น · **ไม่มี** notification จริงของ feature (shell bell = static mock, ไม่ผูก event Bank Master) | ☐ |

#### TC-SL08 — import ไม่มีโหมด Replace (merge-only · FN-18 · FN-40)
- group: Scope-Lock · ความสำคัญ: กลาง · trace: BR-07 / FN-18,40 / S-10⑥
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "นำเข้า CSV"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY จังหวะ pick | — | มีแค่ upload-box + "ดาวน์โหลด template" · **ไม่มี** toggle/radio "Replace / Merge / Overwrite" | ☐ |

#### TC-SL09 — template import ไม่มีคอลัมน์ posting_group/promptpay (FN-20 · FN-40)
- group: Scope-Lock · ความสำคัญ: กลาง · trace: BR-07 / FN-20,40 / S-10⑨
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "นำเข้า CSV"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK "ดาวน์โหลด template ตัวอย่าง" → เปิดไฟล์ `bank_import_template.csv` | — | หัวคอลัมน์ = `code,bank,branch,account_no,account_name,account_type,use_in,status` — **ไม่มี** `posting_group` และ `promptpay` (ผูกทีหลังในจอ) | ☐ |

#### TC-SL10 — ฟอร์มไม่มีข้อความช่วยใต้ช่อง (hint/field-help) (มติเลน · FN-01 · FN-40)
- group: Scope-Lock · ความสำคัญ: กลาง · trace: FN-01,40 / VD-PDM (ตัด hint)
- Setup: role=finance_admin · seed=8 · files=—
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ทุกช่องในฟอร์ม | — | มีเฉพาะ label + input (+ inline error เมื่อผิด) · **ไม่มี** ข้อความ hint/คำอธิบายถาวรใต้ช่อง (placeholder ในช่องไม่นับ) | ☐ |

---

### GROUP N — Permission (Viewer / Consumer 403) `(ต้อง simulate role)`

#### TC-PM01 — Finance Viewer ดูได้ mutation ถูกปฏิเสธ (AT-20)
- group: Permission · ความสำคัญ: กลาง · trace: AT-20 / §5.3 / ERR_INSUFFICIENT_ROLE · **(ต้อง simulate)**
- Setup: role=**finance_viewer** · seed=8 · files=— · **inject:** login เป็น Viewer (prototype อาจไม่มี role switch → simulate โดยเรียก API mutation ตรง หรือ mark BLOCKED)
- Start: OPEN `#/finance/bank-master`
- ผ่านเมื่อ: view/ค้นหา ได้ · create/edit/bulk/import/export mutation = ปุ่มซ่อน หรือ API 403

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY List (role viewer) | — | เห็นตาราง + ค้นหา/กรอง/sort ได้ · ปุ่ม "เพิ่มบัญชีธนาคาร"/"นำเข้า"/bulk ถูกซ่อน (enforce server-side) | ☐ |
| 2 | (simulate) เรียก POST /bank-accounts ตรงด้วย token viewer | — | ตอบ **403 ERR_INSUFFICIENT_ROLE** | ☐ |

#### TC-PM02 — Consumer เลือกได้เฉพาะ active + ฝั่งตรง (mutation deny) (AT-20)
- group: Permission · ความสำคัญ: กลาง · trace: AT-20 / §5.3 / BR-05 · **(ต้อง simulate)**
- Setup: role=**consumer** · seed=8 · files=— · **inject:** เรียก picker endpoint (Receipt/PV ยังไม่ทำ → simulate GET /active)
- Start: (downstream / API)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) GET /bank-accounts/active?side=receive (role consumer) | — | คืนเฉพาะ active + use_receive · ★รับ pre-select | ☐ |
| 2 | (simulate) เรียก PUT /bank-accounts/:id (role consumer) | — | 403 ERR_INSUFFICIENT_ROLE (consumer แก้ master ไม่ได้) | ☐ |

---

### GROUP O — Cross-Module (XT — simulate)

#### TC-XT01 — Receipt/PV picker active + ฝั่งตรง + ★ pre-select + snapshot (XT-01) `(ต้อง simulate)`
- group: Cross-Module · ความสำคัญ: กลาง · trace: XT-01 / BR-05 / OQ-BNK-04 (LOCK) / AD-BNK-01 [AI-DEFAULT]
- Setup: role=consumer · seed=8 (KBANK-01 ★รับ active) · files=— · **inject:** ปลายทาง Receipt ยังไม่ทำ → simulate GET /active?side=receive + สร้างเอกสาร mock
- Start: (downstream — simulate)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) เปิด picker บัญชีฝั่งรับใน Receipt | — | คืนเฉพาะ active + use_receive=true · **KBANK-01 (★รับ) pre-select** · GSB-01 (inactive) ไม่โผล่ | ☐ |
| 2 | (simulate) เลือกบัญชี → บันทึกเอกสาร → VERIFY snapshot | — | เอกสารเก็บ code + ค่า ณ เวลาบันทึก (snapshot) | ☐ |
| 3 | (simulate) แก้ master (ชื่อบัญชี) แล้วดูเอกสารเก่า | — | เอกสารเก่า snapshot **ไม่เปลี่ยน** (soft-ref) | ☐ |

#### TC-XT02 — master → inactive ไม่โผล่ picker · เอกสารเก่า snapshot ยังใช้ (XT-02 · EC-05) `(ต้อง simulate)`
- group: Cross-Module · ความสำคัญ: กลาง · trace: XT-02 / EC-05 / BR-05
- Setup: role=finance_admin+consumer · seed=8 · files=— · **inject:** simulate picker หลังปิดบัญชี
- Start: OPEN `#/finance/bank-master`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปลี่ยน KBANK-02 → ไม่ใช้งาน (view menu) | — | toast success | ☐ |
| 2 | (simulate) เปิด picker ฝั่งรับใน Receipt ใหม่ | — | KBANK-02 **ไม่โผล่** (inactive ถูกซ่อน) · เอกสารเก่าที่อ้าง KBANK-02 (snapshot) ยังใช้ได้ | ☐ |

#### TC-XT03 — consume F-PG API-01 (?kind=bank&status=active) 3 drifts (XT-03 · EC-06) `(ต้อง simulate)`
- group: Cross-Module · ความสำคัญ: กลาง · trace: XT-03 / EC-06 / GL Contract (LOCK) / OQ-BNK-06 (OPEN)
- Setup: role=finance_admin · seed=8 · files=— · **inject:** production ต่อ F-PG API-01 จริง (HTML mock = local list)
- Start: OPEN `#/finance/bank-master` → CLICK "เพิ่มบัญชีธนาคาร"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate/verify contract) picker กลุ่ม GL เรียก `GET /api/v1/gl/posting-groups?kind=bank&status=active` | — | ใช้ `?kind=bank` (ไม่ใช่ `?type=`) · generic API-01 (ไม่มี endpoint เฉพาะ) · active-only คืน **KBANK เท่านั้น** (SCB=draft filtered) · เก็บเฉพาะ code (no FK) | ☐ |
| 2 | (master-side observable) เทียบกับ TC-GL01 | — | จอ prototype ตรงกับ contract: ตัวเลือก picker = KBANK เท่านั้น (+ current-bound draft ตอน edit) | ☐ |

#### TC-XT04 — กลุ่มผูกแล้ว account_1 = NULL → GL post ไม่ได้ (XT-04 · EC-07) `(ต้อง simulate)`
- group: Cross-Module · ความสำคัญ: ต่ำ · trace: XT-04 / EC-07 / BR-04
- Setup: role=finance_admin · seed=8 · files=— · **inject:** F-PG กลุ่มผูกไว้ account_1=NULL — enforce ที่ external GL engine
- Start: (downstream GL — simulate)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) บัญชีผูกกลุ่มที่ account_1=NULL → post Receipt | — | GL post **ไม่ได้** แม้ผูกกลุ่ม (enforce ฝั่ง GL engine) · view เตือนล่วงหน้าถ้าไม่ผูก (BR-04) | ☐ |

---

### GROUP P — Concurrency / Idempotency (simulate)

#### TC-CC01 — concurrent ★ ฝั่งเดียวกัน → 409 (EC-08) `(ต้อง simulate)`
- group: Concurrency · ความสำคัญ: ต่ำ · trace: EC-08 / AD-BNK-02 [AI-DEFAULT] / ERR_STALE_DATA
- Setup: role=finance_admin ×2 · seed=8 · files=— · **inject:** 2 session ตั้ง ★รับ ตัวต่างกันพร้อมกัน (optimistic lock If-Match) — HTML mock ไม่มี race → simulate ที่ API
- Start: (API — simulate)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) session A + B โหลด version เดียวกัน → A ตั้ง ★รับ commit ก่อน | — | A สำเร็จ (version++) | ☐ |
| 2 | (simulate) B ตั้ง ★รับ commit ทีหลัง (version เก่า) | — | B ได้ **409 ERR_STALE_DATA** (first-commit-wins) | ☐ |

#### TC-CC02 — double-submit idempotency (EC-09) `(ต้อง simulate)`
- group: Concurrency · ความสำคัญ: ต่ำ · trace: EC-09 / AD-BNK-02 [AI-DEFAULT] / ERR_DUPLICATE_IDEMPOTENCY_KEY
- Setup: role=finance_admin · seed=8 · files=— · **inject:** ส่ง POST /bank-accounts ซ้ำด้วย Idempotency-Key เดียวกัน (production networked)
- Start: (API — simulate) · **หมายเหตุ:** ฝั่ง UI = TC-EC03 (guard disable ปุ่ม) ครอบแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) POST create ครั้งที่ 1 (Idempotency-Key=K1) | — | 201 created | ☐ |
| 2 | (simulate) POST create ครั้งที่ 2 (Idempotency-Key=K1 เดิม) | — | ไม่สร้างซ้ำ · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY (หรือคืน record เดิม) | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิดไฟล์ `01_HTML/f-bank.html` = เข้าหน้า List (P-01). แต่ละเคสเริ่มที่ `Start` ของตัวเอง (refresh-safe — reload = state กลับ seed 8 บัญชี).
2. ทำ step ตามลำดับ; ทุก Action ขึ้นต้น verb tag — map ตรงกับสิ่งที่เห็นบนจอ. ถ้า target หาไม่เจอ → mark step นั้น fail + จด evidence (สิ่งที่เห็นแทน).
3. เคส **(ต้อง simulate)** = ต้องมี runner/role/inject; ถ้าทำไม่ได้บน prototype → mark `blocked` + เหตุผล.
4. เคส import ต้องมีไฟล์ตาม `### ไฟล์ทดสอบ` เตรียมล่วงหน้า (agent อัปโหลดไฟล์เองไม่ได้ — runner วางไฟล์).
5. เคสที่ทำ mutation (create/delete/status/import) ทำให้ state เปลี่ยนภายใน session — เคสถัดไปที่พึ่ง seed เดิมควร **reload** ก่อน (state in-memory).
6. กรอกผลแต่ละ step ที่คอลัมน์ Result (☐→✅/❌) + สรุปกลับใน Result Report schema.

---

## Coverage Audit

| หมวด | covered / total |
|---|---|
| FR / Acceptance (AT-01..21) | 21 / 21 |
| Business Rules (BR-01..10) | 10 / 10 |
| Function Checklist (FN-01..25, FN-40, FN-90) | 27 / 27 |
| Edge cases (EC-01..11) | 9 / 11 (ข้าม EC-02, EC-11-table = OQ) |
| Error codes | 12 / 15 (ข้าม 3 API-only) |
| Permission cells (สำคัญ) | 3 / 3 |
| Cross-cutting / UI states / interaction | ครบ (#96/#29/#44/#97/Esc/empty/toast) |

- Cross-Module (XT): **4 / 4** (XT-01..04; XT-05 = negative TC-SL01) — ทั้งหมด simulate
- Scope Lock (LOCK): **7 / 7** (OQ-BNK-01..04 + GL Contract + VD-PDM + Governance) — ทุกข้อมีเคส verify
- FN-40 must-not-exist: **ครบ** (PM path / THB / SWIFT-IBAN-balance / used บนจอ / DOA / Replace / posting_group·promptpay ในไฟล์ / ลบเดี่ยว / ★ หลายตัว / hint) → TC-SL01..SL10
- **[AI-DEFAULT]:** AD-BNK-01 (used=posted) → TC-XT01 · AD-BNK-02 (optimistic-lock/idempotency) → TC-CC01/CC02
- **Manifest cross-check (FRD §0.12): ✅** Stories 8/8 · Rules 10/10 · Edges (13 confirmed + probe-mapped) — ทุกแถว manifest มีคู่ใน Ledger

### ข้าม (พร้อมเหตุผล)
- **EC-02** (นิยาม `used`) — OPEN (OQ-BNK-07 blocking); `used` ไม่โชว์บนจอ → สังเกตผลบน UI ไม่ได้ (verify เมื่อ spec ปิด)
- **EC-11 (table/def-grid masking level)** — OQ-BNK-08 (Security review); เฉพาะ header mask สังเกตได้ (คลุมใน TC-VW01)
- **ERR_NOT_FOUND / ERR_NOT_AUTHENTICATED / ERR_VALIDATION_FAILED** — API-only, ไม่มี trigger บน UI prototype
- **ERR_BAD_USE / ERR_BAD_STATUS** — คลุมบางส่วน (TC-IM04 คลุม BAD_TYPE เป็นตัวแทน per-row import error chain; BAD_USE/BAD_STATUS ตรวจได้เพิ่มด้วยไฟล์ที่ผิดเฉพาะฟิลด์นั้น — ระบุใน Data Sets `bad_type_use_status.csv` แต่ด่านหยุดที่ BAD_TYPE ก่อน)
- **เส้นออก Payment Method (นอกขอบเขตใบเซ็น OQ-BNK-01=NO)** — ห้ามสร้างเคส positive; verify negative แล้วที่ TC-SL01

---

## Result Report (schema)

```json
{
  "feature_id": "F-BNK",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 96, "pass": 0, "fail": 0, "blocked": 0 }
}
```
> `evidence` = สิ่งที่ agent **เห็นจริง** ตอน fail/blocked (ข้อความ toast จริง · route ค้าง · pill/สถานะที่ปรากฏแทน Expected). `note` = หมายเหตุเสริม (เช่น "simulate ไม่ได้บน prototype").
> **เคส (ต้อง simulate):** TC-E04, TC-PM01, TC-PM02, TC-XT01..XT04, TC-CC01, TC-CC02 — ถ้า runner ไม่รองรับ role switch / API inject → `blocked` ไม่ใช่ `fail`.

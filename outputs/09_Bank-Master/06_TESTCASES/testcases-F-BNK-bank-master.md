# AI Test Cases — F-BNK Bank Master (ธนาคาร / บัญชีบริษัท)

Test cases สำหรับ **AI agent (browser-use / vision)** อ่านแล้วลงมือทดสอบบนหน้าจอจริงของ prototype `BankMaster.html` แล้วรายงานผลกลับ. ทุก action ขึ้นต้นด้วย verb tag; ทุก Expected ตรวจได้ด้วยตา (ข้อความ/route/pill/ปุ่มที่ปรากฏ). **HTML = source of truth** — microcopy ทั้งหมดคัดลอกverbatim จาก `01_HTML/BankMaster.html` + FRD `06_TESTS §6.10`.

> **✅ EC-14 / OQ-BNK-05 — RESOLVED 2026-08-06 (warn + clear):** เมื่อปิดใช้งาน/เก็บถาวรบัญชีที่เป็น default → confirm modal แสดง warning ว่าค่าเริ่มต้นจะถูกยกเลิก **และ** `defaultPay`/`defaultReceive` **ถูกเคลียร์** (`confirmDeactivate` / `confirmArchive`: `a.defaultPay=false; a.defaultReceive=false`). FRD ปรับให้ตรงกับ HTML แล้ว — ไม่มี divergence. ดูเคส **TC-E03 / TC-E06**.

---

## Meta

| ฟิลด์ | ค่า |
|---|---|
| Feature ID | F-BNK |
| Feature Name | Bank Master — ธนาคาร / บัญชีบริษัท |
| FRD Version | 1.0 (2026-08-06, FULL pack) |
| App entry / Route | single-file SPA · route เดียว **`#/bank-master`** (hash) · 2 แท็บ in-memory `บัญชีบริษัท` / `ธนาคาร` (ไม่ผูก hash → refresh คืนสู่แท็บ `บัญชีบริษัท` เสมอ) |
| Source of truth (HTML) | `01_HTML/BankMaster.html` (2970 บรรทัด, in-memory, no storage) |
| Traced from | FRD Pack `04_FRD/FRD_F-BNK_Pack/` (00_OVERVIEW §0.12 Manifest · 05_RULES · 06_TESTS §6.1–6.10) · BRD · UI Brief `05_UI_BRIEF/` |
| Test user (prototype) | `currentUser = { name:'ศศิธร บุญมี', canRevealFull:true }` (L1998) — role Finance Admin. deny/other-role เคสต้อง **simulate** (แก้ค่านี้ / mock RBAC) |
| Persistence | **in-memory เท่านั้น** — refresh = reset ทุกอย่างกลับ seed. ทุกเคส refresh-safe (เริ่มที่ `#/bank-master`) |
| จำนวนเคส | **76** (happy 20 · negative 22 · edge 13 · error 6 · permission 15) — นับละเอียดใน Coverage Audit |

**Seed สำคัญ (in-memory จริงในไฟล์ — อ้างใน Setup):**
- Companies: **C1** `บริษัท ทูบี ซิมเปิล จำกัด` (taxId `0105558001234`) · **C2** `บริษัท คิวบ์ เทค โซลูชันส์ จำกัด` (taxId `0105561009876`).
- Accounts (5): **BA-001** C1·KBANK·`0012345678`·active·**จ่ายเริ่มต้น**·usedInDoc · **BA-002** C1·SCB·`4051234567`·active·**รับเริ่มต้น**·usedInDoc · **BA-003** C1·BBL·`1470098765`·active·ไม่ใช้·ไม่มี default · **BA-004** C1·KTB·`9800112233`·**inactive**·usedInDoc·GL `1010-06` (payroll) · **BA-005** C2·TTB·`2337788990011`·active·จ่าย+รับเริ่มต้น·ไม่ใช้.
- Banks: **22 preset ธปท. ทั้งหมด** (`is_custom=false`) — foreign 5 (ICBCT/MHCB/CITI/SMBC/SCBT). **ไม่มี custom bank ใน seed** → เคส banks-CRUD ต้องสร้าง custom ก่อน.
- CoA (6): `1010-01..06`; payroll = `1010-06 เงินฝากธนาคาร - บัญชีเงินเดือน`.
- masked format = `••••••NNNN` (bullets = จำนวนหลักที่ซ่อน + 4 หลักท้าย). เช่น `0012345678` → `••••••5678`.

---

## Coverage

| Group | เคส | จำนวน | ความสำคัญ |
|---|---|---|---|
| A — สร้างบัญชี + validation (FN-01/FN-03) | TC-A01..A10 | 10 | สูง |
| B — สลับบริษัท / list / filter | TC-B01..B07 | 7 | กลาง |
| C — default จ่าย/รับ unique (FN-02/FN-06) | TC-C01..C06 | 6 | สูง |
| D — mask / reveal / audit (P0 security) | TC-D01..D07 | 7 | **สูงสุด (P0)** |
| E — lifecycle deactivate/activate/archive (FN-07) | TC-E01..E07 | 7 | สูง |
| F — Banks tab CRUD (preset/custom/W1) | TC-F01..F14 | 14 | สูง |
| G — Cross-module pickers (XT-01..04) | TC-G01..G05 | 5 | กลาง |
| H — Audit (FN-12) | TC-H01..H03 | 3 | กลาง |
| I — Edit / view drawer / UX | TC-I01..I05 | 5 | กลาง |
| J — backend gate / concurrency / role (P0) | TC-J01..J05 | 5 | **สูง (P0 security)** |
| K — Scope Lock verify | TC-K01..K07 | 7 | สูง |

---

## Coverage Ledger

### FR / User Stories (00 §0.12 · 06_TESTS §6.1)
| item | cases |
|---|---|
| US-01 / AC-01 สร้างบัญชี (happy) | TC-A01, TC-A10, TC-I01 |
| US-02 / AC-03 สลับบริษัท scope | TC-B01, TC-B06 |
| US-03 / AC-04 default จ่าย/รับ 1/บริษัท | TC-C01, TC-C02, TC-C03, TC-C05 |
| US-04 / AC-08 masked (ผู้ไม่มีสิทธิ์) | TC-D01, TC-D04 |
| US-05 / AC-07 reveal + audit (ผู้มีสิทธิ์) | TC-D02, TC-D03, TC-D05, TC-D07 |
| US-06 / AC-05 ปิด/เปิดใช้งาน (reversible) | TC-E01, TC-E02 |
| US-07 / AC-06 archive used (no hard delete) | TC-E04, TC-E05 |
| US-08 / AC-10 สร้าง custom bank + SWIFT | TC-F02, TC-F03 |
| US-09 / AC-12/13 ลบ custom (used=0 only) | TC-F09, TC-F10 |

### Business Rules (05_RULES §5.1)
| rule | cases |
|---|---|
| BR-BNK-01 accNo unique/company (FIXED) | TC-A04, TC-A05 |
| BR-BNK-02 default 1/company + active-required (FIXED) | TC-C01, TC-C02, TC-C03, TC-C04, TC-C05 |
| BR-BNK-03 accNo numeric 10–15 `[AI-DEFAULT]` | TC-A02, TC-A03 |
| BR-BNK-04 SWIFT 8/11 alnum (FIXED) | TC-F03, TC-F04, TC-F05 |
| BR-BNK-05 inactive→hidden from picker; docs unchanged (FIXED) | TC-E07, TC-G01, TC-G03 |
| BR-BNK-06 used→no hard delete→archive (FIXED) | TC-E04, TC-E05 |
| BR-BNK-07 every action→append-only audit (FIXED) | TC-H01, TC-H02, TC-H03, TC-F13 |
| BR-BNK-08 ⭐ custom delete used=0 only; preset never (W1) | TC-F09, TC-F10, TC-F11, TC-K07 |
| BR-BNK-09 ⭐ mask last-4 + reveal `canRevealFull` + audit | TC-D01, TC-D02, TC-D04, TC-D05, TC-D06 |
| BR-BNK-10 currency THB only readonly `[AI-DEFAULT]` | TC-A09, TC-K04 |
| BR-BNK-11 GL required (FIXED) | TC-A06 |
| BR-BNK-12 preset ธปท. read-only (FIXED) | TC-F01, TC-F11 |

### Field Validation (05_RULES §5.4)
| field/rule | cases |
|---|---|
| bank_code required → `กรุณาเลือกธนาคาร` | TC-A07 |
| acc_no required → `กรุณากรอกเลขที่บัญชี` | TC-A02 (empty variant) |
| acc_no format `^[0-9]{10,15}$` | TC-A02, TC-A03 |
| acc_no unique/company | TC-A04, TC-A05 |
| acc_name required → `กรุณากรอกชื่อบัญชี` | TC-A08 |
| gl_code required → `กรุณาเลือกบัญชี GL` | TC-A06 |
| currency server-forced THB readonly | TC-A09 |
| swift format 8/11 | TC-F04 |
| swift required | TC-F07 |
| swift unique | TC-F05 |
| name_th / abbr required (bank) | TC-F07 |
| code(BOT) `^[0-9]{3}$` if present | TC-F06 |

### Edge Cases (05_RULES §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 ☑ accNo dup in company | TC-A04 |
| EC-02 ☑ accNo not 10–15 / letters | TC-A02, TC-A03 |
| EC-03 ☑ set 2nd default → auto-move | TC-C01, TC-C02 |
| EC-04 ☑ inactive gone from picker | TC-E07, TC-G01 |
| EC-05 ☑ reveal w/o permission | TC-D04 |
| EC-06 ☑ delete used → archive | TC-E04 |
| EC-07 ☑ SWIFT not 8/11 | TC-F04 |
| EC-08 ☑ delete custom used>0 blocked | TC-F10 |
| EC-09 ☑ archived terminal | TC-E05 |
| EC-10 ☐→`[AI-DEFAULT]` bank archived/deleted after account | TC-F10 note (custom used>0 ลบไม่ได้ → snapshot ยังอยู่); ดู note ใน TC-G03 |
| EC-11 ☐→`[AI-DEFAULT]` GL disabled in CoA | — ข้าม (posting owned by downstream consumer; ไม่มีผลสังเกตบน UI ของ master นี้) |
| EC-12 ☐→`[AI-DEFAULT]` concurrent default | TC-C06 (ต้อง simulate) |
| EC-13 ☐→OQ-04 direct URL w/o edit permission | TC-J01 (ต้อง simulate) |
| EC-14 ✅ default deactivated/archived → warn + clear | TC-E03, TC-E06 (RESOLVED: warn+clear) |
| EC-15 ☐→OQ-03 export/print mask always | TC-D06 (ต้อง simulate — ไม่มี print surface) |
| EC-16 probe idempotent create | TC-J02 (ต้อง simulate) |
| EC-17 probe stale edit 409 | TC-J03 (ต้อง simulate) |

### Error Catalog (05_RULES §5.6)
| error | cases |
|---|---|
| BR_ACCNO_DUPLICATE (422) | TC-A04 |
| BR_ACCNO_FORMAT (422) | TC-A02, TC-A03 |
| BR_GL_REQUIRED (422) | TC-A06 |
| BR_SWIFT_FORMAT (422) | TC-F04 |
| BR_SWIFT_DUPLICATE (422) | TC-F05 |
| BR_BOTCODE_FORMAT (422) | TC-F06 |
| BR_BANK_IN_USE (422) | TC-F10 |
| BR_INVALID_TRANSITION (422) | TC-E05 (reactivate archived — UI no path) |
| BR_DEFAULT_REQUIRES_ACTIVE (422) | TC-C04 |
| ERR_REVEAL_FORBIDDEN (403) | TC-D04 |
| ERR_REVEAL_RATE_LIMITED (429) | TC-J05 (ต้อง simulate) |
| ERR_PRESET_READONLY (403) | TC-F11 |
| ERR_INSUFFICIENT_ROLE / ERR_PERMISSION_REVOKED (403) | TC-J01, TC-J04 |
| ERR_STALE_DATA (409) | TC-J03 |
| ERR_DUPLICATE_IDEMPOTENCY_KEY / idempotent | TC-J02 |
| ERR_VALIDATION_FAILED → `กรุณากรอกข้อมูลให้ครบถ้วน` | TC-A02, TC-A06, TC-F04 |

### Permission Matrix (05_RULES §5.3 — role × action)
| cell | cases |
|---|---|
| finance_admin view (masked) = allow | TC-D01, TC-B01 |
| finance_admin reveal (canRevealFull) = allow | TC-D02 |
| finance_admin create/edit = allow | TC-A01, TC-I01 |
| finance_admin deactivate/archive = allow | TC-E01, TC-E04 |
| finance_admin set default = allow | TC-C01 |
| finance_admin manage custom bank = allow | TC-F02, TC-F08, TC-F09 |
| finance_user view masked only = allow-view | TC-J04 (ต้อง simulate) |
| finance_user reveal / create / edit / archive = **deny** | TC-J04 (ต้อง simulate) |
| any role reveal without canRevealFull = **deny** | TC-D04 |
| backend re-check at mutation (not button-hide) = enforce | TC-J01 |

### Cross-Module (XT — 06_TESTS §6.9)
| XT | Downstream | Case |
|---|---|---|
| XT-01 PV picks pay-from (active only, snapshot) | Payment Voucher | TC-G01 |
| XT-02 RV auto-selects default-receive | Receipt Voucher | TC-G02 (ต้อง simulate real RV) |
| XT-03 Recon reference then archive (soft-ref) | Bank Reconciliation | TC-G03 |
| XT-04 ⭐ Payroll picks GL 1010-06 account | Payroll | TC-G04 |

### Scope Lock (07 §7.0 — ทุกข้อต้องมีเคส verify)
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LOCK-01 Master · NO tier / no Lite-Full | TC-K01 |
| LOCK-02 2 levels only (bank list + company account) | TC-K02 |
| LOCK-03 downstream PV/RV/Recon/Payroll · inbound CoA GL | TC-K03 (+ TC-G01..G04) |
| LOCK-04 OUT: bank API/statement · multi-currency THB only | TC-K04 |
| LOCK-05 HTML = source of truth screen (1 route) | TC-K05 |
| LOCK-06 no scope beyond declared coverage | TC-K06 (scope-creep sweep) |
| LOCK-07 W1 custom hard-delete only used=0 | TC-K07 (+ TC-F09/F10) |

### States / Cross-cutting
| item | cases |
|---|---|
| status pill active/inactive/archived | TC-B04, TC-E01, TC-E04 |
| empty (list unfiltered) | TC-B07 (ต้อง simulate — seed ไม่มีบริษัทว่าง) |
| filtered-empty (search ไม่เจอ) | TC-B03 |
| banks filtered-empty | TC-F12 |
| audit newest-first / append-only | TC-H02, TC-H03 |
| Esc chain (combobox→drawer) | TC-I05 |
| doc-picker soft-ref note (PV-2025-014) | TC-G05 |

### ข้าม (นอกขอบเขต / ไม่มีผลบน UI) — คงไว้ใน Ledger
- **EC-11 (GL disabled in CoA)** — posting/warn เป็นของ downstream consumer, ไม่มีผลสังเกตได้บนหน้า master นี้ → ข้าม (เหตุผล: ไม่มี observable UI).
- **OOS-1..6 / LOCK-04 exclusions** (bank API, statement import, multi-currency active, PromptPay, per-account purpose tag, per-bank format table) → **ห้ามสร้างเคสทดสอบฟีเจอร์** (นอกขอบเขตใบเซ็น); verify การ**ไม่มี**อยู่ที่ TC-K04 เท่านั้น.

---

## Data Sets

### ชุด A — สร้างบัญชีถูกต้อง (happy, company C1)
| ฟิลด์ (label บนจอ) | ค่า |
|---|---|
| ธนาคาร * (combobox #94) | `ธนาคารกรุงศรีอยุธยา` (พิมพ์ `กรุงศรี` หรือ `BAY` หรือ `025`) |
| เลขที่บัญชี * | `0123456789` (10 หลัก) |
| ชื่อบัญชี * | `บจก. ทูบี ซิมเปิล` |
| ประเภทบัญชี * | `ออมทรัพย์` |
| สาขา | `สยามพารากอน` |
| สกุลเงิน | `THB — บาทไทย` (readonly — ไม่ต้องกรอก) |
| บัญชี GL * (combobox #94) | `เงินฝากธนาคาร - ออมทรัพย์` (พิมพ์ `1010-03`) |

### ชุด B — accNo ผิด format (negative)
| กรณี | ค่า | error ที่คาด |
|---|---|---|
| B1 สั้นไป | `123` | `เลขบัญชีต้องเป็นตัวเลข 10-15 หลัก` |
| B2 มีตัวอักษร | `12A4567890` | `เลขบัญชีต้องเป็นตัวเลข 10-15 หลัก` |
| B3 เว้นว่าง | (ไม่กรอก) | `กรุณากรอกเลขที่บัญชี` |
| B4 ยาวเกิน | `1234567890123456` (16 หลัก) | `เลขบัญชีต้องเป็นตัวเลข 10-15 หลัก` |

### ชุด C — accNo ซ้ำ (negative / edge)
| กรณี | company | ค่า | ผลที่คาด |
|---|---|---|---|
| C1 ซ้ำในบริษัทเดียวกัน | C1 | `0012345678` (= BA-001) | block `เลขบัญชีนี้มีอยู่แล้วในบริษัทนี้` |
| C2 เลขเดียวกันคนละบริษัท | C2 | `0012345678` | อนุญาต (สร้างได้) |

### ชุด D — สร้าง custom bank (happy)
| ฟิลด์ | D1 (SWIFT 8) | D2 (SWIFT 11) |
|---|---|---|
| ชื่อธนาคาร * | `ธนาคาร HSBC` | `ธนาคาร Deutsche` |
| ชื่อย่อ * | `HSBC` | `DEUT` |
| รหัส ธปท. (ถ้ามี) | (เว้นว่าง) | (เว้นว่าง) |
| รหัส SWIFT / BIC * | `HSBCTHBK` | `DEUTDEFF500` |
| ประเภท | `ต่างประเทศ` | `ต่างประเทศ` |

### ชุด E — custom bank SWIFT/code ผิด (negative)
| กรณี | ค่า | error |
|---|---|---|
| E1 SWIFT สั้น | SWIFT `HSBC` (4) | `SWIFT ต้องมี 8 หรือ 11 หลัก` |
| E2 SWIFT ซ้ำ | SWIFT `BKKBTHBK` (= BBL preset) | `รหัส SWIFT นี้มีอยู่แล้ว` |
| E3 BOT code ผิด | รหัส ธปท. `99` | `รหัส ธปท. ต้องเป็นตัวเลข 3 หลัก` |
| E4 ชื่อ/ย่อ ว่าง | เว้นชื่อธนาคาร + ชื่อย่อ | `กรุณากรอกชื่อธนาคาร` / `กรุณากรอกชื่อย่อ` |

### ไฟล์ทดสอบ (Files)
- `—` (ฟีเจอร์นี้ไม่มี CSV import / upload / print surface. export/print masking ทดสอบที่ API layer — ดู TC-D06 simulate.)

---

## Test Cases

### Group A — สร้างบัญชี + validation

#### TC-A01 — สร้างบัญชีธนาคารครบฟิลด์ (happy)
- group: สร้างบัญชี · ความสำคัญ: สูง · trace: FR US-01 / AC-01 / BR-BNK-03,11 / event `created`
- actor (role): Finance Admin
- Setup: role=finance_admin (currentUser default) · seed=company C1 มี 4 บัญชี · files=—
- Start: OPEN `#/bank-master` (แท็บ `บัญชีบริษัท`, company = C1)
- ชุดข้อมูล: A
- ผ่านเมื่อ: drawer ปิด + toast `สร้างบัญชีธนาคารสำเร็จ` + แถวใหม่โผล่ในตาราง + เลขบัญชีแสดง masked `••••••6789`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` | — | หัวข้อหน้า `ธนาคาร / บัญชีบริษัท`; แท็บ `บัญชีบริษัท` active; ตารางแสดง 4 แถว (BA-001..004) | ☐ |
| 2 | CLICK ปุ่ม `สร้างบัญชี` (มุมขวาบน, ไอคอน +) | — | drawer เปิดจากขวา (680px); eyebrow `สร้างบัญชีธนาคาร`; title `บัญชีธนาคารใหม่` | ☐ |
| 3 | CLICK ช่อง `ธนาคาร *` (combobox) แล้ว TYPE `กรุงศรี` | A | popover แสดงตัวเลือก `ธนาคารกรุงศรีอยุธยา` (คำค้นถูก highlight) | ☐ |
| 4 | CLICK ตัวเลือก `ธนาคารกรุงศรีอยุธยา` | — | ช่อง `ธนาคาร` แสดง `ธนาคารกรุงศรีอยุธยา`; popover ปิด | ☐ |
| 5 | TYPE → ช่อง `เลขที่บัญชี *` | A: `0123456789` | ช่องแสดง `0123456789` (placeholder เดิม `ตัวเลข 10-15 หลัก`) | ☐ |
| 6 | TYPE → ช่อง `ชื่อบัญชี *` | A: `บจก. ทูบี ซิมเปิล` | ช่องแสดงค่าที่กรอก | ☐ |
| 7 | SELECT `ออมทรัพย์` → `ประเภทบัญชี *` | A | dropdown แสดง `ออมทรัพย์` | ☐ |
| 8 | TYPE → ช่อง `สาขา` | A: `สยามพารากอน` | ช่องแสดงค่าที่กรอก | ☐ |
| 9 | VERIFY ช่อง `สกุลเงิน` | — | ค่า `THB — บาทไทย` readonly (แก้ไม่ได้); มี info-tip | ☐ |
| 10 | CLICK ช่อง `บัญชี GL (ผังบัญชี) *` แล้ว TYPE `1010-03` | A | popover แสดง `เงินฝากธนาคาร - ออมทรัพย์` | ☐ |
| 11 | CLICK ตัวเลือก `เงินฝากธนาคาร - ออมทรัพย์` | — | ช่อง GL แสดงค่าที่เลือก | ☐ |
| 12 | CLICK ปุ่ม `ยืนยันสร้าง` | — | ปุ่มเปลี่ยนเป็น `กำลังบันทึก…` (spinner) ชั่วครู่ | ☐ |
| 13 | WAIT จน drawer ปิด (≤2s) | — | drawer ปิด + toast `สร้างบัญชีธนาคารสำเร็จ` (สีเขียว success) | ☐ |
| 14 | VERIFY ตารางบัญชี | — | มีแถวใหม่ `ธนาคารกรุงศรีอยุธยา` / ชื่อบัญชี / เลขบัญชี `••••••6789` / ประเภท `ออมทรัพย์` / GL `1010-03` / สถานะ pill `ใช้งาน`; footer `แสดง 5 จาก 5 รายการ` | ☐ |

#### TC-A02 — เลขบัญชีสั้น/ว่าง (negative, BR-BNK-03)
- group: สร้างบัญชี · ความสำคัญ: สูง · `[AI-DEFAULT]` (BR-BNK-03 range configurable) · trace: AC-02 / EC-02 / BR_ACCNO_FORMAT
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 · files=—
- Start: OPEN `#/bank-master` → CLICK `สร้างบัญชี`
- ชุดข้อมูล: B1, B3
- ผ่านเมื่อ: block บันทึก + inline error + toast `กรุณากรอกข้อมูลให้ครบถ้วน`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → CLICK `สร้างบัญชี` | — | drawer สร้างบัญชีเปิด | ☐ |
| 2 | CLICK `ธนาคาร *` → เลือก `ธนาคารกรุงเทพ` | — | ช่องธนาคารมีค่า | ☐ |
| 3 | TYPE → `เลขที่บัญชี *` | B1: `123` | ช่องแสดง `123` | ☐ |
| 4 | TYPE → `ชื่อบัญชี *` + เลือก GL ใด ๆ | `บจก. ทดสอบ` + `1010-02` | ฟิลด์อื่นครบ | ☐ |
| 5 | CLICK `ยืนยันสร้าง` | — | **ไม่บันทึก**; inline ใต้ `เลขที่บัญชี` = `เลขบัญชีต้องเป็นตัวเลข 10-15 หลัก`; toast `กรุณากรอกข้อมูลให้ครบถ้วน` (warning); drawer ยังเปิด | ☐ |
| 6 | CLICK ช่อง `เลขที่บัญชี` → ลบให้ว่าง → CLICK `ยืนยันสร้าง` | B3 | inline เปลี่ยนเป็น `กรุณากรอกเลขที่บัญชี` | ☐ |

#### TC-A03 — เลขบัญชีมีตัวอักษร / ยาวเกิน (negative, boundary, BR-BNK-03)
- group: สร้างบัญชี · ความสำคัญ: กลาง · `[AI-DEFAULT]` · trace: AC-02 / EC-02 / BR_ACCNO_FORMAT
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 · files=—
- Start: OPEN `#/bank-master` → CLICK `สร้างบัญชี`
- ชุดข้อมูล: B2, B4
- ผ่านเมื่อ: ทั้ง 2 ค่าถูก block ด้วย `เลขบัญชีต้องเป็นตัวเลข 10-15 หลัก`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → CLICK `สร้างบัญชี` → เลือกธนาคาร + ชื่อบัญชี + GL | — | ฟิลด์อื่นครบ | ☐ |
| 2 | TYPE → `เลขที่บัญชี *` | B2: `12A4567890` | ช่องอาจ strip เป็นตัวเลขเท่านั้น (`124567890`) ตาม help `กรอกเฉพาะตัวเลข…` | ☐ |
| 3 | CLICK `ยืนยันสร้าง` | — | block; inline `เลขบัญชีต้องเป็นตัวเลข 10-15 หลัก` (ค่าไม่ครบ 10 หลัก) | ☐ |
| 4 | CLEAR ช่อง → TYPE | B4: `1234567890123456` (16 หลัก) | ช่องแสดง 16 หลัก | ☐ |
| 5 | CLICK `ยืนยันสร้าง` | — | block; inline `เลขบัญชีต้องเป็นตัวเลข 10-15 หลัก` | ☐ |

#### TC-A04 — เลขบัญชีซ้ำในบริษัทเดียวกัน (negative, EC-01/BR-BNK-01)
- group: สร้างบัญชี · ความสำคัญ: สูง · trace: AC-02b / EC-01 / BR_ACCNO_DUPLICATE
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 มี BA-001 accNo `0012345678` · files=—
- Start: OPEN `#/bank-master` (company C1) → CLICK `สร้างบัญชี`
- ชุดข้อมูล: C1
- ผ่านเมื่อ: block + inline `เลขบัญชีนี้มีอยู่แล้วในบริษัทนี้`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → CLICK `สร้างบัญชี` | — | drawer เปิด | ☐ |
| 2 | เลือก `ธนาคารกสิกรไทย` + TYPE `เลขที่บัญชี` | C1: `0012345678` | ช่องแสดงเลขซ้ำกับ BA-001 | ☐ |
| 3 | TYPE ชื่อบัญชี + เลือก GL | `บจก. ทดสอบ` + `1010-02` | ครบฟิลด์ | ☐ |
| 4 | CLICK `ยืนยันสร้าง` | — | **block**; inline ใต้เลขบัญชี = `เลขบัญชีนี้มีอยู่แล้วในบริษัทนี้`; toast `กรุณากรอกข้อมูลให้ครบถ้วน`; ไม่มีแถวใหม่ | ☐ |

#### TC-A05 — เลขบัญชีเดียวกันคนละบริษัท = อนุญาต (edge, BR-BNK-01)
- group: สร้างบัญชี · ความสำคัญ: กลาง · trace: AC-02b (scope company)
- actor: Finance Admin
- Setup: role=finance_admin · seed=BA-001 (C1) มี `0012345678`; C2 ไม่มีเลขนี้ · files=—
- Start: OPEN `#/bank-master` → สลับ company เป็น C2
- ชุดข้อมูล: C2
- ผ่านเมื่อ: สร้างได้ (เลขซ้ำข้ามบริษัทไม่ block) + toast สำเร็จ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → SELECT `บริษัท คิวบ์ เทค โซลูชันส์ จำกัด` → co-bar `บริษัท` | — | ตารางแสดงเฉพาะบัญชีของ C2 (BA-005, 1 แถว) | ☐ |
| 2 | CLICK `สร้างบัญชี` → เลือกธนาคาร + ชื่อบัญชี + GL | — | ฟิลด์ครบ | ☐ |
| 3 | TYPE `เลขที่บัญชี` | C2: `0012345678` | ช่องแสดงเลขที่ตรงกับ BA-001 ของ C1 | ☐ |
| 4 | CLICK `ยืนยันสร้าง` → WAIT | — | **สร้างสำเร็จ** (ไม่ block); toast `สร้างบัญชีธนาคารสำเร็จ`; C2 มี 2 แถว | ☐ |

#### TC-A06 — GL required (negative, BR-BNK-11)
- group: สร้างบัญชี · ความสำคัญ: กลาง · trace: AC-02c / BR_GL_REQUIRED
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 · files=—
- Start: OPEN `#/bank-master` → CLICK `สร้างบัญชี`
- ชุดข้อมูล: A (ยกเว้น GL)
- ผ่านเมื่อ: block + inline `กรุณาเลือกบัญชี GL`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → CLICK `สร้างบัญชี` | — | drawer เปิด | ☐ |
| 2 | กรอก ธนาคาร + เลขที่บัญชี `0123456789` + ชื่อบัญชี — **ไม่เลือก GL** | A (no GL) | ทุกช่องยกเว้น GL มีค่า | ☐ |
| 3 | CLICK `ยืนยันสร้าง` | — | block; inline ใต้ `บัญชี GL (ผังบัญชี)` = `กรุณาเลือกบัญชี GL`; toast `กรุณากรอกข้อมูลให้ครบถ้วน` | ☐ |

#### TC-A07 — ธนาคาร required (negative)
- group: สร้างบัญชี · ความสำคัญ: กลาง · trace: BR_BANK_REQUIRED / `กรุณาเลือกธนาคาร`
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 · files=—
- Start: OPEN `#/bank-master` → CLICK `สร้างบัญชี`
- ชุดข้อมูล: A (ยกเว้นธนาคาร)
- ผ่านเมื่อ: block + inline `กรุณาเลือกธนาคาร`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → CLICK `สร้างบัญชี` | — | drawer เปิด, ช่องธนาคารว่าง | ☐ |
| 2 | กรอก เลขที่บัญชี `0123456789` + ชื่อบัญชี + GL — **ไม่เลือกธนาคาร** | A (no bank) | ฟิลด์อื่นครบ | ☐ |
| 3 | CLICK `ยืนยันสร้าง` | — | block; inline ใต้ `ธนาคาร` = `กรุณาเลือกธนาคาร`; toast `กรุณากรอกข้อมูลให้ครบถ้วน` | ☐ |

#### TC-A08 — ชื่อบัญชี required (negative)
- group: สร้างบัญชี · ความสำคัญ: ต่ำ · trace: field acc_name required / `กรุณากรอกชื่อบัญชี`
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 · files=—
- Start: OPEN `#/bank-master` → CLICK `สร้างบัญชี`
- ชุดข้อมูล: A (ลบชื่อบัญชีให้ว่าง)
- ผ่านเมื่อ: block + inline `กรุณากรอกชื่อบัญชี`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → CLICK `สร้างบัญชี` | — | drawer เปิด (ชื่อบัญชี pre-fill ด้วยชื่อบริษัท) | ☐ |
| 2 | เลือกธนาคาร + เลขที่บัญชี `0123456789` + GL; CLEAR ช่อง `ชื่อบัญชี` ให้ว่าง | A (empty name) | ช่องชื่อบัญชีว่าง | ☐ |
| 3 | CLICK `ยืนยันสร้าง` | — | block; inline ใต้ `ชื่อบัญชี` = `กรุณากรอกชื่อบัญชี` | ☐ |

#### TC-A09 — สกุลเงิน THB readonly (edge, BR-BNK-10)
- group: สร้างบัญชี · ความสำคัญ: ต่ำ · `[AI-DEFAULT]` (multi-currency roadmap) · trace: AC-15 / BR-BNK-10
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 · files=—
- Start: OPEN `#/bank-master` → CLICK `สร้างบัญชี`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ช่องสกุลเงินแสดง `THB — บาทไทย`, แก้ไม่ได้, info-tip ระบุ THB เท่านั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → CLICK `สร้างบัญชี` | — | drawer เปิด | ☐ |
| 2 | VERIFY ช่อง `สกุลเงิน` | — | ค่า `THB — บาทไทย`; readonly (คลิก/พิมพ์ไม่เปลี่ยน) | ☐ |
| 3 | CLICK/HOVER ไอคอน info ข้างช่องสกุลเงิน | — | tooltip `เฟสนี้รองรับ THB เท่านั้น — สกุลเงินอื่นจะเปิดใช้พร้อม multi-currency (OQ-2)` | ☐ |

#### TC-A10 — สร้างบัญชีพร้อมตั้ง default จ่าย → ย้าย default เดิม (happy/edge, EC-03)
- group: สร้างบัญชี · ความสำคัญ: สูง · trace: AC-01+AC-04 / BR-BNK-02 / EC-03
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 BA-001 เป็น `จ่ายเริ่มต้น` อยู่ · files=—
- Start: OPEN `#/bank-master` (C1)
- ชุดข้อมูล: A + toggle `บัญชีจ่ายเริ่มต้น` ON
- ผ่านเมื่อ: บัญชีใหม่เป็น default จ่าย + BA-001 หลุด default จ่าย (มีได้ 1/บริษัท)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → VERIFY co-bar | — | `บัญชีจ่ายเริ่มต้น` = `KBANK ••••••5678` (BA-001); จดค่าไว้อ้าง step ท้าย | ☐ |
| 2 | CLICK `สร้างบัญชี` → กรอกครบตามชุด A | A | ฟิลด์ครบ | ☐ |
| 3 | TOGGLE `บัญชีจ่ายเริ่มต้น` (ในส่วน `ค่าเริ่มต้นการชำระเงิน`) เป็น ON | — | toggle เป็นสีแดง (on); desc `ตั้งค่าได้เพียง 1 บัญชีต่อบริษัท — เลือกใหม่จะย้ายค่าเริ่มต้นมาบัญชีนี้` | ☐ |
| 4 | CLICK `ยืนยันสร้าง` → WAIT | — | toast `สร้างบัญชีธนาคารสำเร็จ` | ☐ |
| 5 | VERIFY co-bar + แถว | — | `บัญชีจ่ายเริ่มต้น` = ธนาคารใหม่ (BAY) — **ไม่ใช่ KBANK แล้ว**; แถวใหม่มีธง `จ่าย`; แถว BA-001 (KBANK) คอลัมน์ `ค่าเริ่มต้น` = `—` (ถูกย้ายออก) | ☐ |

---

### Group B — สลับบริษัท / list / filter

#### TC-B01 — สลับบริษัทเห็นเฉพาะบัญชีบริษัทนั้น (happy, US-02/AC-03)
- group: list · ความสำคัญ: สูง · trace: AC-03 / FN-04
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 4 บัญชี, C2 1 บัญชี · files=—
- Start: OPEN `#/bank-master`
- ผ่านเมื่อ: C1 แสดง 4 แถว, C2 แสดง 1 แถว, ตัวเลข footer + stat เปลี่ยนตามบริษัท

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` | — | company = C1; footer `แสดง 4 จาก 4 รายการ`; stat `บัญชีทั้งหมด` = `4` | ☐ |
| 2 | VERIFY co-bar | — | `เลขผู้เสียภาษี 0105558001234` | ☐ |
| 3 | SELECT `บริษัท คิวบ์ เทค โซลูชันส์ จำกัด` → co-bar `บริษัท` | — | ตารางแสดง 1 แถว (TTB `••••••0011`); footer `แสดง 1 จาก 1 รายการ` + ชื่อ `บริษัท คิวบ์ เทค โซลูชันส์ จำกัด`; stat `บัญชีทั้งหมด` = `1` | ☐ |
| 4 | VERIFY co-bar (C2) | — | `เลขผู้เสียภาษี 0105561009876` | ☐ |
| 5 | SELECT กลับเป็น `บริษัท ทูบี ซิมเปิล จำกัด` | — | ตารางกลับมา 4 แถว | ☐ |

#### TC-B02 — ค้นหาเจอ (happy)
- group: list · ความสำคัญ: กลาง · trace: filter search
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 · files=—
- Start: OPEN `#/bank-master`
- ผ่านเมื่อ: พิมพ์คำค้นแล้วตารางกรองเหลือเฉพาะแถวที่ match

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` | — | 4 แถว | ☐ |
| 2 | TYPE → ช่องค้นหา (placeholder `ค้นหาธนาคาร / ชื่อบัญชี / เลขบัญชี`) | `กสิกร` | ตารางเหลือ 1 แถว (`ธนาคารกสิกรไทย` / BA-001) | ☐ |
| 3 | CLEAR ช่องค้นหา → TYPE เลขบัญชี | `4051` | ตารางเหลือแถว BA-002 (SCB) | ☐ |

#### TC-B03 — ค้นหาไม่เจอ → filtered empty (edge, state)
- group: list · ความสำคัญ: กลาง · trace: empty-filtered state
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 · files=—
- Start: OPEN `#/bank-master`
- ผ่านเมื่อ: empty state `ไม่พบรายการที่ค้นหา` + ปุ่ม `ล้างตัวกรอง`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → TYPE ช่องค้นหา | `zzzไม่มีจริง` | ตารางหาย; แสดง empty: title `ไม่พบรายการที่ค้นหา` · desc `ลองปรับคำค้นหรือล้างตัวกรอง` · ปุ่ม `ล้างตัวกรอง` | ☐ |
| 2 | CLICK ปุ่ม `ล้างตัวกรอง` (ใน empty state) | — | ช่องค้นหาว่าง; ตารางกลับมา 4 แถว | ☐ |

#### TC-B04 — filter สถานะทุกค่า (edge, states)
- group: list · ความสำคัญ: กลาง · trace: status filter enum (all/active/inactive/archived)
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 มี active 3 (BA-001/002/003) + inactive 1 (BA-004); ยังไม่มี archived · files=—
- Start: OPEN `#/bank-master`
- ผ่านเมื่อ: แต่ละค่ากรองถูกต้อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → SELECT `ใช้งาน` → dropdown สถานะ | — | เหลือ 3 แถว (pill `ใช้งาน` ทั้งหมด) | ☐ |
| 2 | SELECT `ปิดใช้งาน` | — | เหลือ 1 แถว (BA-004 KTB, pill `ปิดใช้งาน`) | ☐ |
| 3 | SELECT `เก็บถาวร` | — | 0 แถว → empty `ไม่พบรายการที่ค้นหา` (ยังไม่มี archived ใน seed) | ☐ |
| 4 | SELECT `ทุกสถานะ` | — | กลับมา 4 แถว | ☐ |

#### TC-B05 — ล้างตัวกรอง reset ทั้ง search + status (happy)
- group: list · ความสำคัญ: ต่ำ · trace: resetFilters
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 · files=—
- Start: OPEN `#/bank-master`
- ผ่านเมื่อ: ปุ่ม `ล้างตัวกรอง` ล้างทั้ง search + status กลับ default

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → TYPE ค้นหา `SCB` + SELECT สถานะ `ใช้งาน` | — | ตารางกรองแล้ว | ☐ |
| 2 | CLICK ปุ่ม `ล้างตัวกรอง` (ใน filter bar, ไอคอน rotate) | — | ช่องค้นหาว่าง + dropdown กลับ `ทุกสถานะ`; ตาราง 4 แถว | ☐ |

#### TC-B06 — co-bar + stat cards แสดง default ถูกต้อง (verify)
- group: list · ความสำคัญ: กลาง · trace: AC-03 / co-meta / stats
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 BA-001 จ่าย, BA-002 รับ · files=—
- Start: OPEN `#/bank-master`
- ผ่านเมื่อ: co-bar + stat แสดง abbr + masked ของ default จ่าย/รับ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → VERIFY co-bar | — | `บัญชีจ่ายเริ่มต้น KBANK ••••••5678` · `บัญชีรับเริ่มต้น SCB ••••••4567` | ☐ |
| 2 | VERIFY stat cards (4 ใบ) | — | `บัญชีทั้งหมด 4` (ในบริษัทนี้) · `ใช้งานอยู่ 3` (พร้อมใช้ในเอกสาร) · `บัญชีจ่ายเริ่มต้น KBANK` (meta `กระแสรายวัน · ••••••5678`) · `บัญชีรับเริ่มต้น SCB` | ☐ |

#### TC-B07 — empty state (บริษัทไม่มีบัญชี) (edge, ต้อง simulate)
- group: list · ความสำคัญ: ต่ำ · trace: empty-unfiltered state `ยังไม่มีบัญชีธนาคาร`
- actor: Finance Admin
- Setup: role=finance_admin · **seed=ต้องมีบริษัทที่มี 0 บัญชี** — seed ปัจจุบันทั้ง C1/C2 มีบัญชี → **(ต้อง simulate)**: เพิ่ม company ที่ไม่มีบัญชี หรือ archive/ลบบัญชีทั้งหมดของบริษัทใดบริษัทหนึ่งออกก่อน · files=—
- Start: OPEN `#/bank-master` แล้วสลับไปบริษัทที่ 0 บัญชี
- ผ่านเมื่อ: empty state `ยังไม่มีบัญชีธนาคาร` + ปุ่ม `สร้างบัญชี`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) เตรียมบริษัทที่ไม่มีบัญชี → SELECT บริษัทนั้น | — | ตารางหาย; empty: title `ยังไม่มีบัญชีธนาคาร` · desc `เริ่มต้นด้วยการสร้างบัญชีธนาคารแรกของบริษัทนี้` · ปุ่ม `สร้างบัญชี` | ☐ |
| 2 | CLICK ปุ่ม `สร้างบัญชี` (ใน empty) | — | drawer สร้างบัญชีเปิด | ☐ |

---

### Group C — default จ่าย/รับ unique per company

#### TC-C01 — ตั้ง default จ่ายใหม่ → ย้ายจากบัญชีเดิม (happy, EC-03/BR-BNK-02)
- group: default · ความสำคัญ: สูง · trace: AC-04 / BR-BNK-02 / EC-03 / event `set-default`
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 BA-001 = จ่ายเริ่มต้น, BA-003 = ไม่มี default (active) · files=—
- Start: OPEN `#/bank-master` (C1) → CLICK แถว BA-003 (BBL) เปิด view drawer
- ผ่านเมื่อ: BA-003 กลายเป็น default จ่าย + BA-001 หลุด (มีได้ 1/บริษัท)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → VERIFY co-bar | — | `บัญชีจ่ายเริ่มต้น KBANK ••••••5678` (BA-001); จดไว้ | ☐ |
| 2 | CLICK แถว `ธนาคารกรุงเทพ` (BA-003) | — | view drawer เปิด; eyebrow `บัญชีธนาคาร · BA-003` | ☐ |
| 3 | CLICK แท็บ `ค่าเริ่มต้น` ใน drawer | — | เห็น toggle `บัญชีจ่ายเริ่มต้น` (off) + `บัญชีรับเริ่มต้น` (off) | ☐ |
| 4 | TOGGLE `บัญชีจ่ายเริ่มต้น` เป็น ON | — | toast `ตั้งเป็นบัญชีจ่ายเริ่มต้นแล้ว` (info); toggle เป็น on | ☐ |
| 5 | CLICK `ปิด` → VERIFY co-bar + ตาราง | — | `บัญชีจ่ายเริ่มต้น` = `BBL ••••••8765` (BA-003); แถว BA-001 (KBANK) คอลัมน์ `ค่าเริ่มต้น` = `—`; แถว BA-003 มีธง `จ่าย` | ☐ |

#### TC-C02 — ตั้ง default รับ unique (happy, EC-03)
- group: default · ความสำคัญ: กลาง · trace: AC-04 / BR-BNK-02
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 BA-002 = รับเริ่มต้น, BA-003 active · files=—
- Start: OPEN `#/bank-master` (C1) → เปิด view BA-003
- ผ่านเมื่อ: BA-003 เป็น default รับ + BA-002 หลุด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → CLICK แถว BA-003 → แท็บ `ค่าเริ่มต้น` | — | drawer default tab เปิด | ☐ |
| 2 | TOGGLE `บัญชีรับเริ่มต้น` ON | — | toast `ตั้งเป็นบัญชีรับเริ่มต้นแล้ว` | ☐ |
| 3 | CLICK `ปิด` → VERIFY co-bar | — | `บัญชีรับเริ่มต้น` = `BBL ••••••8765`; แถว BA-002 (SCB) `ค่าเริ่มต้น` = `—` | ☐ |

#### TC-C03 — default จ่าย + รับ อยู่คนละบัญชีได้พร้อมกัน (edge)
- group: default · ความสำคัญ: กลาง · trace: AC-04 (coexist)
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 BA-001 จ่าย, BA-002 รับ · files=—
- Start: OPEN `#/bank-master` (C1)
- ผ่านเมื่อ: จ่าย (BA-001) และ รับ (BA-002) อยู่คนละแถว แสดงพร้อมกันได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → VERIFY แถว BA-001 | — | คอลัมน์ `ค่าเริ่มต้น` มีธง `จ่าย` (สีส้ม) | ☐ |
| 2 | VERIFY แถว BA-002 | — | คอลัมน์ `ค่าเริ่มต้น` มีธง `รับ` (สีเขียว) | ☐ |
| 3 | VERIFY co-bar | — | จ่าย = KBANK, รับ = SCB (คนละบัญชี) พร้อมกัน | ☐ |

#### TC-C04 — ตั้ง default บนบัญชีที่ไม่ active → block (negative, BR_DEFAULT_REQUIRES_ACTIVE)
- group: default · ความสำคัญ: สูง · trace: BR-BNK-02 / BR_DEFAULT_REQUIRES_ACTIVE
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 BA-004 = inactive · files=—
- Start: OPEN `#/bank-master` (C1) → เปิด view BA-004
- ผ่านเมื่อ: toggle ถูก block + toast `บัญชีต้องอยู่สถานะใช้งานก่อนตั้งเป็นค่าเริ่มต้น`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → SELECT สถานะ `ปิดใช้งาน` → CLICK แถว BA-004 (KTB) | — | view drawer เปิด; สถานะ pill `ปิดใช้งาน` | ☐ |
| 2 | CLICK แท็บ `ค่าเริ่มต้น` | — | เห็น warn note `บัญชีที่ไม่ได้อยู่สถานะใช้งาน ไม่สามารถตั้งเป็นค่าเริ่มต้นได้` | ☐ |
| 3 | TOGGLE `บัญชีจ่ายเริ่มต้น` | — | **ไม่เปลี่ยน**; toast `บัญชีต้องอยู่สถานะใช้งานก่อนตั้งเป็นค่าเริ่มต้น` (warning); toggle ยัง off | ☐ |

#### TC-C05 — ยกเลิก default (toggle off) (happy)
- group: default · ความสำคัญ: ต่ำ · trace: toggleDefault off / `ยกเลิกค่าเริ่มต้นแล้ว`
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 BA-001 = จ่ายเริ่มต้น · files=—
- Start: OPEN `#/bank-master` (C1) → เปิด view BA-001
- ผ่านเมื่อ: toggle off → toast `ยกเลิกค่าเริ่มต้นแล้ว` + co-bar จ่าย = `ยังไม่ตั้ง`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → CLICK แถว BA-001 → แท็บ `ค่าเริ่มต้น` | — | toggle `บัญชีจ่ายเริ่มต้น` = on | ☐ |
| 2 | TOGGLE `บัญชีจ่ายเริ่มต้น` เป็น off | — | toast `ยกเลิกค่าเริ่มต้นแล้ว` (info); toggle off | ☐ |
| 3 | CLICK `ปิด` → VERIFY co-bar | — | `บัญชีจ่ายเริ่มต้น` = `ยังไม่ตั้ง`; stat `บัญชีจ่ายเริ่มต้น` = `—` (`ยังไม่ได้ตั้งค่า`) | ☐ |

#### TC-C06 — concurrent default set → last-write-wins ≤1 (edge, ต้อง simulate)
- group: default · ความสำคัญ: ต่ำ · `[AI-DEFAULT]` (PR-1/PR-9) · trace: AC-04b / EC-12
- actor: Finance Admin ×2 (สอง session)
- Setup: role=finance_admin · **(ต้อง simulate)** — prototype in-memory session เดียว, จำลอง 2 ผู้ใช้ตั้ง default พร้อมกันไม่ได้บน UI; ต้องทดสอบที่ backend/API (partial-unique index). seed=C1 BA-001/BA-003 active · files=—
- Start: (simulate API) POST set-default BA-001 และ BA-003 พร้อมกัน
- ผ่านเมื่อ: เหลือ default จ่ายเพียง 1 บัญชี (last-write-wins) + audit ทั้งสอง write

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) VERIFY หลัง concurrent set | — | มี `defaultPay=true` เพียง 1 บัญชีในบริษัท (partial-unique enforced); ทั้งสอง set มี audit `set-default` | ☐ |

---

### Group D — mask / reveal / audit (P0 security spine)

#### TC-D01 — เลขบัญชี masked ทุกที่โดย default (P0, BR-BNK-09)
- group: security · ความสำคัญ: **สูงสุด (P0)** · trace: AC-01/AC-08 / BR-BNK-09 / R10
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 · files=—
- Start: OPEN `#/bank-master`
- ผ่านเมื่อ: ทุกจุดแสดง masked `••••••NNNN` (ไม่มีเลขเต็มโผล่โดยไม่กด reveal)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → VERIFY คอลัมน์ `เลขบัญชี` ทุกแถว | — | แถว BA-001 = `••••••5678` + ปุ่ม `ดูเต็ม`; ไม่มีแถวใดโชว์เลขเต็ม | ☐ |
| 2 | VERIFY co-bar + stat | — | default จ่าย/รับ แสดง masked (เช่น `••••••5678`) | ☐ |
| 3 | CLICK แถว BA-001 (view drawer) → แท็บ `รายละเอียด` | — | บรรทัด `เลขที่บัญชี` = masked `••••••5678` + ปุ่ม `ดูเต็ม` | ☐ |

#### TC-D02 — reveal เลขเต็ม (มีสิทธิ์) + เขียน audit (P0, AC-07)
- group: security · ความสำคัญ: **สูงสุด (P0)** · trace: AC-07 / US-05 / BR-BNK-09 / event `revealed`
- actor: Finance Admin (canRevealFull=true)
- Setup: role=finance_admin · currentUser.canRevealFull=true (default) · seed=BA-001 · files=—
- Start: OPEN `#/bank-master`
- ผ่านเมื่อ: กด `ดูเต็ม` → เลขเต็ม `0012345678` + toast `บันทึกการเข้าถึงเลขบัญชีเต็มแล้ว` + audit `revealed`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → VERIFY แถว BA-001 | — | `••••••5678` + ปุ่ม `ดูเต็ม` (title `ต้องมีสิทธิ์ · ระบบจะบันทึกการเข้าถึง`) | ☐ |
| 2 | CLICK ปุ่ม `ดูเต็ม` (ท้าย cell เลขบัญชี แถว BA-001) | — | cell เปลี่ยนเป็นเลขเต็ม `0012345678`; ปุ่มเปลี่ยนเป็น `ซ่อน`; toast `บันทึกการเข้าถึงเลขบัญชีเต็มแล้ว` (info) | ☐ |
| 3 | CLICK แถว BA-001 → แท็บ `ประวัติ` ใน view drawer | — | รายการบนสุด = `เปิดดูเลขบัญชีเต็ม KBANK` (ไอคอน scan-line, พื้นแดงจาง) + ผู้ใช้ `ศศิธร บุญมี` + เวลา | ☐ |

#### TC-D03 — ซ่อนเลขกลับ masked (happy, AC-07)
- group: security · ความสำคัญ: กลาง · trace: AC-07 (hide re-mask)
- actor: Finance Admin
- Setup: role=finance_admin · seed=BA-001 · files=—
- Start: OPEN `#/bank-master` → reveal BA-001 ก่อน
- ผ่านเมื่อ: กด `ซ่อน` → กลับเป็น masked, **ไม่เขียน audit เพิ่ม**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → CLICK `ดูเต็ม` แถว BA-001 | — | เลขเต็ม `0012345678` + ปุ่ม `ซ่อน` | ☐ |
| 2 | CLICK ปุ่ม `ซ่อน` | — | cell กลับเป็น `••••••5678` + ปุ่ม `ดูเต็ม` | ☐ |
| 3 | CLICK แถว → แท็บ `ประวัติ` | — | มี `revealed` แค่ 1 รายการ (การกด `ซ่อน` ไม่เพิ่ม audit) | ☐ |

#### TC-D04 — reveal ไม่มีสิทธิ์ → ถูกปฏิเสธ เลขยัง masked (P0 negative, EC-05/AC-08) ⭐
- group: security · ความสำคัญ: **สูงสุด (P0)** · trace: AC-08 / EC-05 / ERR_REVEAL_FORBIDDEN / BR-BNK-09
- actor: user ที่ `canRevealFull=false`
- Setup: **(ต้อง simulate)** — prototype ship `canRevealFull=true` (L1998). ต้องแก้ `currentUser.canRevealFull=false` (หรือ login user `qa_finance_admin_noreveal`) ก่อนรัน · seed=BA-001 · files=—
- Start: OPEN `#/bank-master` (หลังตั้ง canRevealFull=false)
- ผ่านเมื่อ: กด `ดูเต็ม` → toast `คุณไม่มีสิทธิ์ดูเลขบัญชีเต็ม` + เลข **ยัง masked** + **ไม่มี** audit `revealed`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) ตั้ง `currentUser.canRevealFull=false` → OPEN `#/bank-master` | — | แถว BA-001 = `••••••5678` + ปุ่ม `ดูเต็ม` | ☐ |
| 2 | CLICK ปุ่ม `ดูเต็ม` แถว BA-001 | — | toast `คุณไม่มีสิทธิ์ดูเลขบัญชีเต็ม` (warning); cell **ยังเป็น `••••••5678`** (ไม่เปลี่ยนเป็นเลขเต็ม); ปุ่มยังเป็น `ดูเต็ม` | ☐ |
| 3 | CLICK แถว → แท็บ `ประวัติ` | — | **ไม่มี** รายการ `เปิดดูเลขบัญชีเต็ม` เพิ่ม (reveal ที่ถูกปฏิเสธไม่ลง audit) | ☐ |

#### TC-D05 — reveal เขียน audit ตรวจสอบได้ (P0, AC-07/AC-14)
- group: security · ความสำคัญ: สูง (P0) · trace: AC-07/AC-14 / BR-BNK-07,09 / non-repudiation
- actor: Finance Admin (canRevealFull=true)
- Setup: role=finance_admin · seed=BA-002 · files=—
- Start: OPEN `#/bank-master`
- ผ่านเมื่อ: หลัง reveal มี audit entry `revealed` พร้อม actor + timestamp

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → CLICK แถว BA-002 → แท็บ `ประวัติ` | — | จดจำนวนรายการ audit ปัจจุบัน (เช่น n) ไว้อ้าง | ☐ |
| 2 | CLICK `ปิด` → CLICK ปุ่ม `ดูเต็ม` แถว BA-002 ในตาราง | — | เลขเต็ม `4051234567`; toast `บันทึกการเข้าถึงเลขบัญชีเต็มแล้ว` | ☐ |
| 3 | CLICK แถว BA-002 → แท็บ `ประวัติ (n+1)` | — | มีรายการใหม่บนสุด `เปิดดูเลขบัญชีเต็ม SCB` + `ศศิธร บุญมี` + timestamp; จำนวนเพิ่มจาก n เป็น n+1 | ☐ |

#### TC-D06 — export/print masking (P0 negative, EC-15/AC-09, ต้อง simulate)
- group: security · ความสำคัญ: สูง (P0) · `[AI-DEFAULT]` (OQ-03) · trace: AC-09 / EC-15 / BR-BNK-09
- actor: user without permission
- Setup: **(ต้อง simulate)** — prototype ไม่มี surface export/print (06_TESTS §6.7). ทดสอบที่ API/export layer: เรียก export บัญชีด้วย user ที่ `canRevealFull=false` · files=—
- Start: (simulate export API)
- ผ่านเมื่อ: เลขบัญชีใน export ถูก mask last-4; full reveal ต้องมีสิทธิ์ + เขียน audit

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) เรียก export/print รายการบัญชีด้วย user ไม่มีสิทธิ์ | — | เลขบัญชีในผลลัพธ์ = masked last-4 เท่านั้น; ไม่มีเลขเต็มรั่ว | ☐ |
| 2 | (simulate) export ด้วย user มีสิทธิ์ (canRevealFull) | — | หากคืนเลขเต็ม → ต้องมี audit entry (export/reveal) บันทึก | ☐ |

#### TC-D07 — reveal ใน view drawer detail tab (P0, AC-07)
- group: security · ความสำคัญ: กลาง · trace: AC-07 (reveal จาก view drawer)
- actor: Finance Admin
- Setup: role=finance_admin · seed=BA-001 · files=—
- Start: OPEN `#/bank-master` → เปิด view BA-001
- ผ่านเมื่อ: กด `ดูเต็ม` ใน detail tab → เลขเต็ม + toast + audit

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → CLICK แถว BA-001 → แท็บ `รายละเอียด` | — | บรรทัด `เลขที่บัญชี` = `••••••5678` + `ดูเต็ม` | ☐ |
| 2 | CLICK `ดูเต็ม` (ในบรรทัดเลขที่บัญชี) | — | เลขเต็ม `0012345678` + ปุ่ม `ซ่อน`; toast `บันทึกการเข้าถึงเลขบัญชีเต็มแล้ว` | ☐ |

---

### Group E — lifecycle: deactivate / activate / archive

#### TC-E01 — ปิดใช้งานบัญชี active (happy, AC-05)
- group: lifecycle · ความสำคัญ: สูง · trace: AC-05 / US-06 / state active→inactive / event `deactivated`
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 BA-003 (active, ไม่มี default) · files=—
- Start: OPEN `#/bank-master` (C1) → เปิด view BA-003
- ผ่านเมื่อ: modal ยืนยัน → สถานะ `ปิดใช้งาน` + toast `ปิดใช้งานบัญชีแล้ว`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → CLICK แถว BA-003 (BBL) | — | view drawer; header มีปุ่ม `แก้ไข` · `ปิดใช้งาน` · `เก็บถาวร` | ☐ |
| 2 | CLICK ปุ่ม `ปิดใช้งาน` | — | modal เปิด (บนสุด z), title `ปิดใช้งานบัญชีนี้?`; body กล่าวถึงจะไม่ปรากฏในเอกสารใหม่ | ☐ |
| 3 | CLICK ปุ่ม `ปิดใช้งาน` (สีแดงใน modal) | — | modal ปิด; toast `ปิดใช้งานบัญชีแล้ว` (success) | ☐ |
| 4 | VERIFY แถว BA-003 (filter สถานะ `ปิดใช้งาน`) | — | BA-003 มี pill `ปิดใช้งาน` | ☐ |

#### TC-E02 — เปิดใช้งานบัญชี inactive (happy, AC-05 reversible)
- group: lifecycle · ความสำคัญ: สูง · trace: AC-05 / state inactive→active / event `activated`
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 BA-004 (inactive) · files=—
- Start: OPEN `#/bank-master` (C1) → filter `ปิดใช้งาน` → เปิด view BA-004
- ผ่านเมื่อ: กด `เปิดใช้งาน` → สถานะ `ใช้งาน` + toast `เปิดใช้งานบัญชีแล้ว`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → SELECT สถานะ `ปิดใช้งาน` → CLICK แถว BA-004 (KTB) | — | view drawer; header มีปุ่ม `เปิดใช้งาน` (แทน `ปิดใช้งาน`) | ☐ |
| 2 | CLICK ปุ่ม `เปิดใช้งาน` | — | toast `เปิดใช้งานบัญชีแล้ว` (success); สถานะ pill เปลี่ยนเป็น `ใช้งาน` | ☐ |

#### TC-E03 — ปิดใช้งานบัญชีที่เป็น default → **warn + flag ถูกเคลียร์** (edge, EC-14)
- group: lifecycle · ความสำคัญ: สูง · trace: AC-05c / EC-14 / OQ-BNK-05 (RESOLVED 2026-08-06: warn+clear)
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 BA-001 = จ่ายเริ่มต้น (active) · files=—
- Start: OPEN `#/bank-master` (C1) → เปิด view BA-001
- ผ่านเมื่อ: confirm modal แสดง default-loss warning ก่อนยืนยัน → หลังปิดใช้งาน BA-001 → **default จ่ายถูกเคลียร์** (co-bar `ยังไม่ตั้ง`)

> **✅ RESOLVED (EC-14 / OQ-BNK-05): warn + clear.** confirm modal แสดง warn note ว่าค่าเริ่มต้นจะถูกยกเลิก และ `confirmDeactivate` เคลียร์ `defaultPay/defaultReceive`. FRD ปรับให้ตรงกับ HTML แล้ว.

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → VERIFY co-bar | — | `บัญชีจ่ายเริ่มต้น KBANK ••••••5678` (BA-001); แถว BA-001 มีธง `จ่าย`; จดไว้ | ☐ |
| 2 | CLICK แถว BA-001 → CLICK `ปิดใช้งาน` → VERIFY เนื้อ modal ก่อนยืนยัน | — | modal แสดง warn note (สีส้ม) `บัญชีนี้เป็นบัญชีจ่ายเริ่มต้นของบริษัท — เมื่อปิดใช้งาน ค่าเริ่มต้นนี้จะถูกยกเลิก บริษัทจะไม่มีค่าเริ่มต้นดังกล่าว กรุณาตั้งบัญชีอื่นแทนภายหลัง` | ☐ |
| 3 | CLICK ยืนยัน `ปิดใช้งาน` ใน modal | — | toast `ปิดใช้งานบัญชีแล้ว` | ☐ |
| 4 | VERIFY co-bar + แถว BA-001 | — | `บัญชีจ่ายเริ่มต้น` = `ยังไม่ตั้ง`; แถว BA-001 คอลัมน์ `ค่าเริ่มต้น` = `—` (flag ถูกเคลียร์); สถานะ `ปิดใช้งาน` | ☐ |

#### TC-E04 — เก็บถาวรบัญชีที่ถูกใช้ในเอกสาร (happy, AC-06/EC-06)
- group: lifecycle · ความสำคัญ: สูง · trace: AC-06 / US-07 / EC-06 / BR-BNK-06 / event `archived`
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 BA-002 (active, usedInDoc=true) · files=—
- Start: OPEN `#/bank-master` (C1) → เปิด view BA-002 หรือกดไอคอน archive ที่แถว
- ผ่านเมื่อ: modal แสดง used-in-doc note → สถานะ `เก็บถาวร` + toast `เก็บถาวรบัญชีแล้ว` (ไม่มี hard delete)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → ที่แถว BA-002 (SCB) CLICK ไอคอน archive (ท้ายแถว, สีแดง) | — | modal เปิด; title `เก็บถาวรบัญชีนี้?`; sub `ธนาคารไทยพาณิชย์ · ••••••4567` | ☐ |
| 2 | VERIFY เนื้อ modal | — | body `ต้องการเก็บถาวรบัญชี "บจก. ทูบี ซิมเปิล" ใช่หรือไม่ …`; note (lock) `บัญชีนี้ถูกใช้ในเอกสารและรายการกระทบยอดธนาคารแล้ว จึงลบถาวรไม่ได้ — ระบบจะเก็บถาวร (soft archive) เท่านั้น …` | ☐ |
| 3 | CLICK ปุ่ม `เก็บถาวร` (สีแดง) | — | modal ปิด; toast `เก็บถาวรบัญชีแล้ว` (success) | ☐ |
| 4 | SELECT สถานะ `เก็บถาวร` → VERIFY | — | BA-002 มี pill `เก็บถาวร` | ☐ |

#### TC-E05 — บัญชี archived เป็น terminal (negative/edge, AC-06b/EC-09)
- group: lifecycle · ความสำคัญ: กลาง · trace: AC-06b / EC-09 / BR_INVALID_TRANSITION
- actor: Finance Admin
- Setup: role=finance_admin · seed=มีบัญชี archived (ทำ TC-E04 ก่อน หรือ archive BA-003) · files=—
- Start: OPEN `#/bank-master` (C1) → filter `เก็บถาวร` → เปิด view บัญชี archived
- ผ่านเมื่อ: ไม่มีปุ่ม `เก็บถาวร`/`เปิดใช้งาน` (ไม่มี path กลับ); ไอคอน archive ที่แถวหายไป

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → (archive BA-003 ก่อนถ้ายังไม่มี archived) → SELECT สถานะ `เก็บถาวร` | — | แถวบัญชี archived; **ไอคอน archive ท้ายแถวหายไป** (เหลือแค่ `แก้ไข`) | ☐ |
| 2 | CLICK แถว archived → VERIFY header ปุ่ม | — | **ไม่มี** ปุ่ม `เก็บถาวร` และไม่มี `เปิดใช้งาน` (terminal — ไม่มีทางกลับ); สถานะ pill `เก็บถาวร` | ☐ |

#### TC-E06 — เก็บถาวรบัญชีที่เป็น default → **warn + flag ถูกเคลียร์** (edge)
- group: lifecycle · ความสำคัญ: กลาง · trace: EC-14 / confirmArchive (RESOLVED 2026-08-06: warn+clear)
- actor: Finance Admin
- Setup: role=finance_admin · seed=C2 BA-005 = จ่าย+รับเริ่มต้น (active) · files=—
- Start: OPEN `#/bank-master` → สลับ C2 → เปิด view BA-005
- ผ่านเมื่อ: confirm modal แสดง default-loss warning ก่อนยืนยัน → หลัง archive BA-005 → default จ่าย+รับ ของ C2 ถูกเคลียร์ (`ยังไม่ตั้ง`)

> **✅ RESOLVED: warn + clear.** เช่นเดียวกับ TC-E03 — confirm modal แสดง warn note และ `confirmArchive` เคลียร์ `defaultPay/defaultReceive`. FRD ตรงกับ HTML แล้ว.

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → SELECT `บริษัท คิวบ์ เทค โซลูชันส์ จำกัด` → VERIFY co-bar | — | จ่าย = `TTB ••••••0011`, รับ = `TTB ••••••0011` (BA-005 เป็นทั้งคู่); จดไว้ | ☐ |
| 2 | CLICK แถว BA-005 → CLICK `เก็บถาวร` → VERIFY เนื้อ modal ก่อนยืนยัน | — | modal แสดง warn note (สีส้ม) `บัญชีนี้เป็นบัญชีจ่ายและรับเริ่มต้นของบริษัท — เมื่อเก็บถาวร ค่าเริ่มต้นนี้จะถูกยกเลิก บริษัทจะไม่มีค่าเริ่มต้นดังกล่าว กรุณาตั้งบัญชีอื่นแทนภายหลัง` | ☐ |
| 3 | CLICK ยืนยัน `เก็บถาวร` ใน modal | — | toast `เก็บถาวรบัญชีแล้ว` | ☐ |
| 4 | VERIFY co-bar (C2) | — | `บัญชีจ่ายเริ่มต้น` = `ยังไม่ตั้ง` และ `บัญชีรับเริ่มต้น` = `ยังไม่ตั้ง` (flag ถูกเคลียร์) | ☐ |

#### TC-E07 — บัญชี inactive หายจาก doc picker แต่เอกสารเดิมยังอ้างอิงได้ (edge, EC-04/BR-BNK-05)
- group: lifecycle · ความสำคัญ: สูง · trace: AC-05b / EC-04 / BR-BNK-05 (soft-ref)
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 BA-004 = inactive + usedInDoc (อ้างใน PV-2025-014) · files=—
- Start: OPEN `#/bank-master` (C1) → CLICK `จำลองเลือกในเอกสาร`
- ผ่านเมื่อ: picker แสดงเฉพาะ active (ไม่มี BA-004) + note อ้างเอกสารเดิม PV-2025-014

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → CLICK ปุ่ม `จำลองเลือกในเอกสาร` | — | modal `จำลอง: เลือกบัญชีในเอกสาร`; sub `แสดงเฉพาะบัญชี "ใช้งาน" ของ บริษัท ทูบี ซิมเปิล จำกัด` | ☐ |
| 2 | VERIFY รายการใน picker | — | มีเฉพาะบัญชี active (BA-001/002/003); **ไม่มี** BA-004 (KTB inactive) | ☐ |
| 3 | VERIFY note ท้าย picker | — | note (info) อ้าง `PV-2025-014` อ้างอิงบัญชี KTB ที่ปัจจุบันปิดใช้งาน — เอกสารเดิมยังแสดงตามปกติ | ☐ |

---

### Group F — Banks tab CRUD (preset / custom / W1)

#### TC-F01 — ดูรายการธนาคาร preset ทั้งหมด read-only (happy, BR-BNK-12)
- group: banks · ความสำคัญ: สูง · trace: AC-13 / BR-BNK-12 / R-12 / LOCK
- actor: Finance Admin
- Setup: role=finance_admin · seed=22 preset banks (ไม่มี custom) · files=—
- Start: OPEN `#/bank-master` → CLICK แท็บ `ธนาคาร`
- ผ่านเมื่อ: ทุกแถว preset คอลัมน์ `จัดการ` = `มาตรฐาน` (ไม่มีปุ่มแก้ไข/ลบ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → CLICK แท็บ `ธนาคาร` (ไอคอน landmark) | — | ตารางธนาคาร; หัวคอลัมน์ `รหัส ธปท. · ธนาคาร · ชื่อย่อ · SWIFT / BIC · ประเภท · บัญชีที่ใช้ · จัดการ`; footer `22 จาก 22 ธนาคาร` | ☐ |
| 2 | VERIFY คอลัมน์ `จัดการ` ของแถว preset (เช่น BBL) | — | ข้อความ `มาตรฐาน` (ไม่มีปุ่มแก้ไข/ลบ) | ☐ |
| 3 | VERIFY คอลัมน์ `ประเภท` | — | pill `ในประเทศ` (local) / `ต่างประเทศ` (foreign เช่น ICBCT/CITI); คอลัมน์ `บัญชีที่ใช้` = `{n} บัญชี` หรือ `—` | ☐ |

#### TC-F02 — สร้างธนาคาร custom ต่างประเทศ SWIFT 8 หลัก (happy, AC-10)
- group: banks · ความสำคัญ: สูง · trace: AC-10 / US-08 / BR-BNK-04 / event `bank-added`
- actor: Finance Admin
- Setup: role=finance_admin · seed=banks · files=—
- Start: OPEN `#/bank-master` → แท็บ `ธนาคาร` → CLICK `สร้างธนาคาร`
- ชุดข้อมูล: D1
- ผ่านเมื่อ: สร้างได้ + toast `สร้างธนาคารสำเร็จ` + แถวใหม่ในตาราง + audit `bank-added`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → แท็บ `ธนาคาร` → CLICK ปุ่ม `สร้างธนาคาร` | — | drawer เปิด; eyebrow `สร้างธนาคาร`; title `ธนาคารใหม่ (นอก preset)` | ☐ |
| 2 | TYPE → `ชื่อธนาคาร *` | D1: `ธนาคาร HSBC` | ช่องแสดงค่า | ☐ |
| 3 | TYPE → `ชื่อย่อ *` | D1: `HSBC` | ช่องแสดง `HSBC` (auto-uppercase) | ☐ |
| 4 | TYPE → `รหัส SWIFT / BIC *` | D1: `HSBCTHBK` | ช่องแสดง `HSBCTHBK` | ☐ |
| 5 | SELECT `ประเภท` = `ต่างประเทศ` | D1 | dropdown แสดง `ต่างประเทศ` | ☐ |
| 6 | CLICK `ยืนยันสร้าง` → WAIT | — | drawer ปิด; toast `สร้างธนาคารสำเร็จ` (success); แท็บสลับมาที่ `ธนาคาร` | ☐ |
| 7 | VERIFY ตาราง + audit section | — | มีแถว `ธนาคาร HSBC` / `HSBC` / `HSBCTHBK` / pill `ต่างประเทศ` / บัญชีที่ใช้ `—`; footer `23 จาก 23`; ส่วน `ประวัติการเปลี่ยนแปลงรายชื่อธนาคาร` มีรายการ `สร้างธนาคาร HSBC (SWIFT HSBCTHBK)` | ☐ |

#### TC-F03 — สร้างธนาคาร custom SWIFT 11 หลัก (happy, BR-BNK-04)
- group: banks · ความสำคัญ: กลาง · trace: AC-10 / BR-BNK-04 (11-char valid)
- actor: Finance Admin
- Setup: role=finance_admin · seed=banks · files=—
- Start: OPEN `#/bank-master` → แท็บ `ธนาคาร` → `สร้างธนาคาร`
- ชุดข้อมูล: D2
- ผ่านเมื่อ: SWIFT 11 หลัก valid → สร้างสำเร็จ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → แท็บ `ธนาคาร` → `สร้างธนาคาร` | — | drawer เปิด | ☐ |
| 2 | กรอก ชื่อธนาคาร + ชื่อย่อ + SWIFT + ประเภท | D2: SWIFT `DEUTDEFF500` (11) | ฟิลด์ครบ | ☐ |
| 3 | CLICK `ยืนยันสร้าง` → WAIT | — | toast `สร้างธนาคารสำเร็จ`; แถว `ธนาคาร Deutsche` โผล่ | ☐ |

#### TC-F04 — SWIFT format ผิด (negative, EC-07/BR-BNK-04)
- group: banks · ความสำคัญ: สูง · trace: AC-11 / EC-07 / BR_SWIFT_FORMAT
- actor: Finance Admin
- Setup: role=finance_admin · seed=banks · files=—
- Start: OPEN `#/bank-master` → แท็บ `ธนาคาร` → `สร้างธนาคาร`
- ชุดข้อมูล: E1
- ผ่านเมื่อ: block + inline `SWIFT ต้องมี 8 หรือ 11 หลัก`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → แท็บ `ธนาคาร` → `สร้างธนาคาร` | — | drawer เปิด | ☐ |
| 2 | กรอก ชื่อธนาคาร + ชื่อย่อ; TYPE SWIFT | E1: `HSBC` (4 ตัว) | ช่อง SWIFT แสดง `HSBC` | ☐ |
| 3 | CLICK `ยืนยันสร้าง` | — | block; inline ใต้ SWIFT = `SWIFT ต้องมี 8 หรือ 11 หลัก`; toast `กรุณากรอกข้อมูลให้ครบถ้วน` | ☐ |

#### TC-F05 — SWIFT ซ้ำ (negative, BR_SWIFT_DUPLICATE)
- group: banks · ความสำคัญ: กลาง · trace: AC-11 / BR_SWIFT_DUPLICATE
- actor: Finance Admin
- Setup: role=finance_admin · seed=BBL preset SWIFT `BKKBTHBK` · files=—
- Start: OPEN `#/bank-master` → แท็บ `ธนาคาร` → `สร้างธนาคาร`
- ชุดข้อมูล: E2
- ผ่านเมื่อ: block + inline `รหัส SWIFT นี้มีอยู่แล้ว`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → แท็บ `ธนาคาร` → `สร้างธนาคาร` | — | drawer เปิด | ☐ |
| 2 | กรอก ชื่อธนาคาร + ชื่อย่อ; TYPE SWIFT | E2: `BKKBTHBK` (ซ้ำกับ BBL) | ช่อง SWIFT แสดงค่า | ☐ |
| 3 | CLICK `ยืนยันสร้าง` | — | block; inline `รหัส SWIFT นี้มีอยู่แล้ว` | ☐ |

#### TC-F06 — รหัส ธปท. ผิด format (negative, BR_BOTCODE_FORMAT)
- group: banks · ความสำคัญ: ต่ำ · trace: field code(BOT) `^[0-9]{3}$` / BR_BOTCODE_FORMAT
- actor: Finance Admin
- Setup: role=finance_admin · seed=banks · files=—
- Start: OPEN `#/bank-master` → แท็บ `ธนาคาร` → `สร้างธนาคาร`
- ชุดข้อมูล: E3
- ผ่านเมื่อ: block + inline `รหัส ธปท. ต้องเป็นตัวเลข 3 หลัก`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → แท็บ `ธนาคาร` → `สร้างธนาคาร` | — | drawer เปิด | ☐ |
| 2 | กรอก ชื่อธนาคาร + ชื่อย่อ + SWIFT valid `HSBCTHBK`; TYPE `รหัส ธปท. (ถ้ามี)` | E3: `99` | ช่องรหัสแสดง `99` | ☐ |
| 3 | CLICK `ยืนยันสร้าง` | — | block; inline ใต้รหัส ธปท. = `รหัส ธปท. ต้องเป็นตัวเลข 3 หลัก` | ☐ |

#### TC-F07 — ชื่อธนาคาร / ชื่อย่อ / SWIFT required (negative)
- group: banks · ความสำคัญ: กลาง · trace: field required (name_th/abbr/swift)
- actor: Finance Admin
- Setup: role=finance_admin · seed=banks · files=—
- Start: OPEN `#/bank-master` → แท็บ `ธนาคาร` → `สร้างธนาคาร`
- ชุดข้อมูล: E4
- ผ่านเมื่อ: submit ว่าง → inline errors ทั้ง 3 ช่อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → แท็บ `ธนาคาร` → `สร้างธนาคาร` | — | drawer เปิด, ช่องว่างทั้งหมด | ☐ |
| 2 | CLICK `ยืนยันสร้าง` (โดยไม่กรอก) | — | inline `กรุณากรอกชื่อธนาคาร` + `กรุณากรอกชื่อย่อ` + `กรุณากรอกรหัส SWIFT`; toast `กรุณากรอกข้อมูลให้ครบถ้วน` | ☐ |

#### TC-F08 — แก้ไขธนาคาร custom (happy, banks-tab CRUD edit)
- group: banks · ความสำคัญ: กลาง · trace: banks CRUD edit / event `bank-edited`
- actor: Finance Admin
- Setup: role=finance_admin · **seed=ต้องมี custom bank** — สร้างก่อนด้วย TC-F02 (HSBC) · files=—
- Start: OPEN `#/bank-master` → แท็บ `ธนาคาร` → หาแถว custom (HSBC)
- ผ่านเมื่อ: แก้ชื่อ/ประเภทได้ + toast `บันทึกการแก้ไขแล้ว`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prereq) สร้าง custom bank HSBC (TC-F02) → แท็บ `ธนาคาร` | — | แถว `ธนาคาร HSBC` มีปุ่ม `แก้ไขธนาคาร` (pencil) ท้ายแถว | ☐ |
| 2 | CLICK ปุ่ม `แก้ไขธนาคาร` (pencil) ที่แถว HSBC | — | drawer เปิด; eyebrow `แก้ไขธนาคาร`; ช่องรหัส ธปท. readonly | ☐ |
| 3 | CLEAR `ชื่อธนาคาร` → TYPE `ธนาคาร HSBC (สาขาไทย)` → CLICK `บันทึกการแก้ไข` → WAIT | — | toast `บันทึกการแก้ไขแล้ว` (success); ตารางแสดงชื่อใหม่ | ☐ |

#### TC-F09 — ลบธนาคาร custom used=0 (happy, AC-13/W1)
- group: banks · ความสำคัญ: สูง · trace: AC-13 / BR-BNK-08 / LOCK-07 / event `bank-removed`
- actor: Finance Admin
- Setup: role=finance_admin · **seed=custom bank ที่ไม่มีบัญชีอ้างอิง (used=0)** — สร้าง HSBC (TC-F02) โดยไม่ผูกบัญชี · files=—
- Start: OPEN `#/bank-master` → แท็บ `ธนาคาร` → แถว HSBC
- ผ่านเมื่อ: ลบได้ + toast `ลบธนาคารแล้ว` + audit `bank-removed`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prereq) มี custom HSBC used=0 → แท็บ `ธนาคาร` | — | แถว HSBC: คอลัมน์ `บัญชีที่ใช้` = `—`; ปุ่มลบ (trash) **กดได้** (สีแดง), title `ลบธนาคารที่สร้างเอง` | ☐ |
| 2 | CLICK ปุ่มลบ (trash) ที่แถว HSBC | — | toast `ลบธนาคารแล้ว` (success); แถว HSBC หายจากตาราง | ☐ |
| 3 | VERIFY ส่วน `ประวัติการเปลี่ยนแปลงรายชื่อธนาคาร` | — | มีรายการ `ลบธนาคาร HSBC (SWIFT HSBCTHBK)` | ☐ |

#### TC-F10 — ลบธนาคาร custom used>0 ถูก block (negative, AC-12/EC-08/W1) ⭐
- group: banks · ความสำคัญ: **สูง (P0/W1)** · trace: AC-12 / EC-08 / BR-BNK-08 / BR_BANK_IN_USE
- actor: Finance Admin
- Setup: role=finance_admin · **seed=custom bank ที่มีบัญชีอ้างอิง (used>0)** — (1) สร้าง custom bank (เช่น HSBC, TC-F02); (2) สร้างบัญชีในแท็บ `บัญชีบริษัท` โดยเลือกธนาคาร HSBC → ทำให้ used=1 · files=—
- Start: OPEN `#/bank-master` → แท็บ `ธนาคาร` → แถว HSBC
- ผ่านเมื่อ: ปุ่มลบ **disabled** + tooltip; ไม่มีทางลบได้จาก UI

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prereq) สร้าง custom HSBC + สร้าง 1 บัญชีที่ใช้ HSBC → แท็บ `ธนาคาร` | — | แถว HSBC: คอลัมน์ `บัญชีที่ใช้` = `1 บัญชี` | ☐ |
| 2 | VERIFY ปุ่มลบ (trash) ที่แถว HSBC | — | ปุ่มลบ **disabled** (จาง, กดไม่ได้); hover → tooltip `มี 1 บัญชีอ้างอิงธนาคารนี้ — ลบไม่ได้` | ☐ |
| 3 | CLICK แถว HSBC (เปิด bank view) → VERIFY ปุ่ม `ลบ` | — | ปุ่มลบใน view drawer ก็ disabled พร้อม tooltip เดียวกัน (W1 guard) | ☐ |
| 4 | (simulate) บังคับเรียก API-13 ลบ HSBC (used>0) | — | ถูกปฏิเสธ 422 BR_BANK_IN_USE; toast `ลบไม่ได้ — มี 1 บัญชีอ้างอิงธนาคารนี้อยู่ (ย้าย/ปิดบัญชีก่อน)` | ☐ |

> [note EC-10] custom bank ที่ used>0 ลบไม่ได้อยู่แล้ว → บัญชีที่ snapshot bankCode ไว้จึงไม่มีทางถูกทำลาย (soft-ref ปลอดภัย).

#### TC-F11 — preset ธปท. แก้ไข/ลบไม่ได้ (negative/permission, AC-13/BR-BNK-12) ⭐
- group: banks · ความสำคัญ: สูง · trace: AC-13 / R-12 / ERR_PRESET_READONLY
- actor: Finance Admin
- Setup: role=finance_admin · seed=preset BBL · files=—
- Start: OPEN `#/bank-master` → แท็บ `ธนาคาร`
- ผ่านเมื่อ: preset ไม่มีปุ่มแก้ไข/ลบ (cell `มาตรฐาน`); การบังคับแก้ (simulate) → toast `ธนาคารมาตรฐาน ธปท. แก้ไขไม่ได้`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → แท็บ `ธนาคาร` → VERIFY แถว `ธนาคารกรุงเทพ` (preset) | — | คอลัมน์ `จัดการ` = `มาตรฐาน` (ไม่มีปุ่มแก้ไข/ลบ) | ☐ |
| 2 | CLICK แถว preset (เปิด bank view) → VERIFY | — | ไม่มีปุ่ม `แก้ไข`/`ลบ`; note `รายการมาตรฐาน ธปท. — เป็นข้อมูลอ้างอิงกลาง แก้ไข/ลบไม่ได้` | ☐ |
| 3 | (simulate) เรียก `openBankEdit('002')` / API-12 บน preset | — | toast `ธนาคารมาตรฐาน ธปท. แก้ไขไม่ได้` (warning); API → 403 ERR_PRESET_READONLY (ไม่แก้ได้) | ☐ |

#### TC-F12 — ค้นหาธนาคารไม่เจอ → empty (edge)
- group: banks · ความสำคัญ: ต่ำ · trace: banks filtered-empty
- actor: Finance Admin
- Setup: role=finance_admin · seed=banks · files=—
- Start: OPEN `#/bank-master` → แท็บ `ธนาคาร`
- ผ่านเมื่อ: search ไม่เจอ → `ไม่พบธนาคารที่ค้นหา`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → แท็บ `ธนาคาร` → TYPE ช่องค้นหา (`ค้นหาธนาคาร / SWIFT / รหัส`) | `zzzไม่มี` | empty: title `ไม่พบธนาคารที่ค้นหา` · desc `ลองปรับคำค้น` (ไม่มีปุ่ม action) | ☐ |
| 2 | CLEAR ช่องค้นหา → TYPE | `กสิกร` | ตารางเหลือ `ธนาคารกสิกรไทย` | ☐ |

#### TC-F13 — bank audit section แสดง bank-added/removed (edge, AC-14)
- group: banks · ความสำคัญ: กลาง · trace: AC-14 / BR-BNK-07 (bank stream)
- actor: Finance Admin
- Setup: role=finance_admin · seed=banks · files=—
- Start: OPEN `#/bank-master` → แท็บ `ธนาคาร`
- ผ่านเมื่อ: ก่อนสร้าง = empty `ยังไม่มีการสร้างหรือลบธนาคารที่สร้างเอง`; หลังสร้าง/ลบ = มีรายการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → แท็บ `ธนาคาร` → VERIFY ส่วน `ประวัติการเปลี่ยนแปลงรายชื่อธนาคาร` | — | empty `ยังไม่มีการสร้างหรือลบธนาคารที่สร้างเอง` (ก่อนมี custom) | ☐ |
| 2 | สร้าง custom bank (TC-F02) → VERIFY ส่วน audit อีกครั้ง | — | มีรายการบนสุด `สร้างธนาคาร HSBC (SWIFT HSBCTHBK)` + user + timestamp (newest-first) | ☐ |

#### TC-F14 — bank view drawer preset (verify, P-06)
- group: banks · ความสำคัญ: ต่ำ · trace: P-06 bank view
- actor: Finance Admin
- Setup: role=finance_admin · seed=preset · files=—
- Start: OPEN `#/bank-master` → แท็บ `ธนาคาร` → CLICK แถว preset
- ผ่านเมื่อ: view drawer แสดง grid ข้อมูล + note preset read-only

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → แท็บ `ธนาคาร` → CLICK แถว `ธนาคารกสิกรไทย` | — | bank view drawer; eyebrow `ธนาคาร · รหัส 004`; grid: `ชื่อธนาคาร ธนาคารกสิกรไทย` · `ชื่อย่อ KBANK` · `SWIFT / BIC KASITHBK` · `ประเภท ในประเทศ` · `แหล่งข้อมูล มาตรฐาน ธปท.` | ☐ |
| 2 | VERIFY note + footer | — | note `รายการมาตรฐาน ธปท. — เป็นข้อมูลอ้างอิงกลาง แก้ไข/ลบไม่ได้`; ปุ่ม `ปิด` | ☐ |

---

### Group G — Cross-module pickers (XT)

#### TC-G01 — PV picker แสดงเฉพาะบัญชี active (XT-01)
- group: cross-module · ความสำคัญ: กลาง · trace: XT-01 / BR-BNK-05 / AC-05b (Payment Voucher)
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 active 3 (BA-001/002/003) + inactive 1 (BA-004) · files=—
- Start: OPEN `#/bank-master` (C1) → CLICK `จำลองเลือกในเอกสาร`
- ผ่านเมื่อ: picker แสดงเฉพาะ active + เลือกได้ (snapshot จำลอง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → CLICK `จำลองเลือกในเอกสาร` | — | modal `จำลอง: เลือกบัญชีในเอกสาร`; แสดงเฉพาะบัญชี active (3 รายการ, มีป้าย `· ค่าเริ่มต้นจ่าย`/`· ค่าเริ่มต้นรับ`) | ☐ |
| 2 | CLICK ปุ่ม `เลือก` ที่บัญชีแรก | — | modal ปิด; toast `เลือกบัญชี {abbr} {mask} แล้ว (จำลอง)` (เช่น `เลือกบัญชี KBANK ••••••5678 แล้ว (จำลอง)`) | ☐ |
| 3 | [note snapshot] | — | เอกสารจริง (PV) จะ snapshot ค่า ณ ตอนเลือก — แก้บัญชีภายหลังไม่กระทบเอกสารที่ออกแล้ว (soft-ref; ทดสอบเต็มที่ real PV, XT-01) | ☐ |

#### TC-G02 — RV auto-select default-receive (XT-02, ต้อง simulate)
- group: cross-module · ความสำคัญ: กลาง · trace: XT-02 (Receipt Voucher)
- actor: Finance Admin
- Setup: **(ต้อง simulate)** — prototype ไม่มีหน้า Receipt Voucher จริง; picker จำลองไม่ pre-select. ทดสอบที่ real RV / API-16 (`is_default_receive`) · seed=C1 BA-002 = รับเริ่มต้น · files=—
- Start: (simulate) RV เปิด account picker
- ผ่านเมื่อ: pickable รวม flag `is_default_receive` และ RV pre-select บัญชีรับเริ่มต้น (BA-002)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) เรียก API-16 สำหรับ RV | — | รายการบัญชี active มี field `is_default_receive`; BA-002 = true | ☐ |
| 2 | (simulate) RV เปิดฟอร์มใหม่ | — | ช่องบัญชีรับ pre-select = BA-002 (บัญชีรับเริ่มต้น) | ☐ |

#### TC-G03 — Bank Recon อ้างอิงบัญชีแล้ว archive (soft-ref, XT-03)
- group: cross-module · ความสำคัญ: กลาง · trace: XT-03 / BR-BNK-05 (Bank Reconciliation)
- actor: Finance Admin
- Setup: **(ต้อง simulate downstream)** — prototype ไม่มีหน้า Bank Recon; ทดสอบ soft-ref: บัญชีที่ archive แล้วต้องหายจาก picker ของ recon ใหม่ แต่ประวัติ recon เดิมยังอ้างอิงได้ · seed=บัญชี used ใน recon · files=—
- Start: (simulate) archive บัญชีที่มีใน recon history
- ผ่านเมื่อ: recon history เดิมคงอยู่ (no cascade); บัญชี archived หายจาก picker recon ใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (บน prototype) archive BA-002 (มี usedInDoc) | — | toast `เก็บถาวรบัญชีแล้ว`; บัญชีหายจาก doc picker (`จำลองเลือกในเอกสาร`) | ☐ |
| 2 | (simulate) VERIFY recon history เดิม | — | รายการ recon เดิมที่อ้าง BA-002 ยังแสดง/อ้างอิงได้ (no cascade); picker recon ใหม่ไม่มี BA-002 | ☐ |

#### TC-G04 — Payroll เลือกบัญชีจ่ายผูก GL 1010-06 (XT-04) ⭐
- group: cross-module · ความสำคัญ: สูง · trace: XT-04 / LOCK-03 (Payroll · GL 1010-06)
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 BA-004 ผูก GL `1010-06` แต่ **inactive** · files=—
- Start: OPEN `#/bank-master` (C1) → CLICK `จำลองเลือกในเอกสาร`
- ผ่านเมื่อ: picker แสดงเฉพาะ active → BA-004 (payroll GL, inactive) **ไม่โผล่**; ต้องเปิดใช้งานก่อน payroll run ถึงจะเลือกได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → CLICK `จำลองเลือกในเอกสาร` → VERIFY | — | BA-004 (KTB, GL 1010-06 payroll) **ไม่อยู่ใน picker** (เพราะ inactive) | ☐ |
| 2 | ปิด modal → filter `ปิดใช้งาน` → เปิด BA-004 → CLICK `เปิดใช้งาน` | — | toast `เปิดใช้งานบัญชีแล้ว`; BA-004 = active | ☐ |
| 3 | CLICK `จำลองเลือกในเอกสาร` อีกครั้ง → VERIFY | — | BA-004 (KTB, ผูก payroll GL 1010-06) โผล่ใน picker แล้ว (active) | ☐ |
| 4 | [note XT-04] | — | payroll run จะ snapshot บัญชี ณ ตอนเลือก; ถ้าบัญชี inactive ระหว่าง run ถัดไป → รอบถัดไปเลือกไม่ได้ แต่ run ก่อนยังคงเดิม (ทดสอบเต็มที่ real Payroll) | ☐ |

#### TC-G05 — doc-picker note soft-ref เอกสารเดิม (edge)
- group: cross-module · ความสำคัญ: ต่ำ · trace: doc picker existing note (soft-ref)
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 มี BA-004 inactive + usedInDoc · files=—
- Start: OPEN `#/bank-master` (C1) → CLICK `จำลองเลือกในเอกสาร`
- ผ่านเมื่อ: note info อ้าง `PV-2025-014` + บัญชีที่ปิดใช้งานยังแสดงในเอกสารเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → CLICK `จำลองเลือกในเอกสาร` → VERIFY note | — | note (info, ไอคอน file-clock) อ้าง `PV-2025-014` อ้างอิงบัญชี KTB (`••••••2233`) ที่ปัจจุบันปิดใช้งาน — เอกสารเดิมยังแสดงตามปกติ แต่ไม่อยู่ในรายการให้เลือก | ☐ |

---

### Group H — Audit (FN-12)

#### TC-H01 — ทุก action เขียน audit หนึ่งรายการ (AC-14/BR-BNK-07)
- group: audit · ความสำคัญ: กลาง · trace: AC-14 / BR-BNK-07
- actor: Finance Admin
- Setup: role=finance_admin · seed=BA-003 (active, ไม่ใช้ในเอกสาร) · files=—
- Start: OPEN `#/bank-master` (C1) → เปิด view BA-003
- ผ่านเมื่อ: แต่ละ action (reveal/set-default/deactivate) เพิ่ม audit 1 รายการใน history tab

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → CLICK แถว BA-003 → แท็บ `ประวัติ` | — | จดจำนวน audit เริ่มต้น (เช่น n) | ☐ |
| 2 | CLICK `ปิด` → CLICK `ดูเต็ม` BA-003 → เปิด view → แท็บ `ประวัติ` | — | +1 รายการ `เปิดดูเลขบัญชีเต็ม BBL` | ☐ |
| 3 | แท็บ `ค่าเริ่มต้น` → TOGGLE `บัญชีจ่ายเริ่มต้น` ON → แท็บ `ประวัติ` | — | +1 รายการ `ตั้งเป็นบัญชีจ่ายเริ่มต้น` | ☐ |
| 4 | CLICK `ปิดใช้งาน` → ยืนยัน → เปิด view → แท็บ `ประวัติ` | — | +1 รายการ `ปิดใช้งานบัญชี BBL`; รวมเพิ่มจาก n ≥ 3 รายการ | ☐ |

#### TC-H02 — audit เรียง newest-first (edge)
- group: audit · ความสำคัญ: ต่ำ · trace: AC-14 (ordering)
- actor: Finance Admin
- Setup: role=finance_admin · seed=BA-001 (มี audit created + set-default) · files=—
- Start: OPEN `#/bank-master` (C1) → เปิด view BA-001 → แท็บ `ประวัติ`
- ผ่านเมื่อ: รายการล่าสุดอยู่บนสุด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → CLICK BA-001 → แท็บ `ประวัติ ({n})` | — | รายการเรียงจากใหม่→เก่า (created ของ BA-001 อยู่ล่างสุด) | ☐ |
| 2 | CLICK `ปิด` → `ดูเต็ม` BA-001 → เปิด view → แท็บ `ประวัติ` | — | รายการ `เปิดดูเลขบัญชีเต็ม KBANK` อยู่ **บนสุด** | ☐ |

#### TC-H03 — audit append-only (แก้/ลบไม่ได้) (verify)
- group: audit · ความสำคัญ: ต่ำ · trace: BR-BNK-07 (immutable)
- actor: Finance Admin
- Setup: role=finance_admin · seed=BA-001 · files=—
- Start: OPEN `#/bank-master` (C1) → เปิด view BA-001 → แท็บ `ประวัติ`
- ผ่านเมื่อ: history tab เป็น read-only — ไม่มีปุ่มแก้ไข/ลบรายการ audit

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → CLICK BA-001 → แท็บ `ประวัติ` | — | รายการ audit แสดงเป็น list; **ไม่มี** ปุ่มแก้ไข/ลบ ต่อรายการ (append-only) | ☐ |

---

### Group I — Edit / view drawer / UX

#### TC-I01 — แก้ไขบัญชี + บันทึก (happy)
- group: edit · ความสำคัญ: สูง · trace: AC-01 (edit) / event `edited`
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 BA-003 · files=—
- Start: OPEN `#/bank-master` (C1) → ที่แถว BA-003 CLICK ไอคอน `แก้ไข`
- ผ่านเมื่อ: แก้ field ได้ + toast `บันทึกการแก้ไขแล้ว`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → ที่แถว BA-003 (BBL) CLICK ไอคอน `แก้ไข` (pencil ท้ายแถว) | — | drawer เปิด; eyebrow `แก้ไขบัญชีธนาคาร`; ฟิลด์ pre-fill ค่าเดิม | ☐ |
| 2 | CLEAR ช่อง `สาขา` → TYPE `สีลม (ใหม่)` | — | ช่องแสดงค่าใหม่ | ☐ |
| 3 | CLICK `บันทึกการแก้ไข` → WAIT | — | drawer ปิด; toast `บันทึกการแก้ไขแล้ว` (success) | ☐ |
| 4 | CLICK แถว BA-003 → แท็บ `รายละเอียด` | — | `สาขา` = `สีลม (ใหม่)`; แท็บ `ประวัติ` มีรายการ `แก้ไขข้อมูลบัญชี BBL` | ☐ |

#### TC-I02 — view drawer detail tab ทุกฟิลด์ (verify, P-04)
- group: view · ความสำคัญ: กลาง · trace: P-04 detail grid
- actor: Finance Admin
- Setup: role=finance_admin · seed=BA-001 · files=—
- Start: OPEN `#/bank-master` (C1) → CLICK แถว BA-001
- ผ่านเมื่อ: grid แสดงทุก label + `การใช้งานในเอกสาร`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → CLICK แถว BA-001 → แท็บ `รายละเอียด` | — | grid labels: `ธนาคาร ธนาคารกสิกรไทย` · `เลขที่บัญชี ••••••5678` (+ดูเต็ม) · `ชื่อบัญชี` · `ประเภทบัญชี กระแสรายวัน` · `สาขา สยามพารากอน` · `สกุลเงิน THB` · `บัญชี GL 1010-02` · `บริษัท` · `การใช้งานในเอกสาร มีการอ้างอิงแล้ว` | ☐ |

#### TC-I03 — view drawer 3 แท็บสลับได้ (verify)
- group: view · ความสำคัญ: ต่ำ · trace: P-04 tabs
- actor: Finance Admin
- Setup: role=finance_admin · seed=BA-001 · files=—
- Start: OPEN `#/bank-master` (C1) → CLICK แถว BA-001
- ผ่านเมื่อ: สลับ `รายละเอียด`/`ค่าเริ่มต้น`/`ประวัติ` ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` (C1) → CLICK แถว BA-001 | — | drawer มี 3 แท็บ: `รายละเอียด` · `ค่าเริ่มต้น` · `ประวัติ ({n})` | ☐ |
| 2 | CLICK แท็บ `ค่าเริ่มต้น` | — | เห็น toggle จ่าย/รับ + desc `ใช้เป็นค่าเริ่มต้นในใบสำคัญจ่าย — มีได้ 1 บัญชีต่อบริษัท` | ☐ |
| 3 | CLICK แท็บ `ประวัติ` | — | list audit; footer `สร้างเมื่อ {datetime}` + ปุ่ม `ปิด` | ☐ |

#### TC-I04 — combobox #94 ค้นหาไม่เจอ (edge)
- group: view · ความสำคัญ: ต่ำ · trace: combobox empty `ไม่พบธนาคาร` / `ไม่พบบัญชี GL`
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 · files=—
- Start: OPEN `#/bank-master` → CLICK `สร้างบัญชี`
- ผ่านเมื่อ: พิมพ์คำที่ไม่มีใน combobox → empty text

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → CLICK `สร้างบัญชี` → CLICK `ธนาคาร *` → TYPE `zzz` | — | popover แสดง `ไม่พบธนาคาร` | ☐ |
| 2 | CLICK `บัญชี GL (ผังบัญชี) *` → TYPE `zzz` | — | popover แสดง `ไม่พบบัญชี GL` | ☐ |

#### TC-I05 — Esc chain: combobox popover ปิดก่อน drawer (edge, UX)
- group: view · ความสำคัญ: กลาง · trace: Esc chain (#94.3/#15)
- actor: Finance Admin
- Setup: role=finance_admin · seed=C1 · files=—
- Start: OPEN `#/bank-master` → CLICK `สร้างบัญชี`
- ผ่านเมื่อ: Esc ครั้งแรกปิด popover (drawer ยังเปิด), Esc ครั้งที่สองปิด drawer

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → CLICK `สร้างบัญชี` → CLICK `ธนาคาร *` แล้วพิมพ์ให้ popover เปิด | — | popover ตัวเลือกธนาคารเปิดอยู่ | ☐ |
| 2 | PRESS Esc | — | popover ปิด; **drawer ยังเปิดอยู่** | ☐ |
| 3 | PRESS Esc อีกครั้ง | — | drawer ปิด | ☐ |

---

### Group J — backend gate / concurrency / role (P0 security & robustness)

#### TC-J01 — backend permission gate เรียก API ตรง (P0 negative, EC-13/AC-16) ⭐
- group: permission · ความสำคัญ: **สูง (P0)** · `[AI-DEFAULT]`→OQ-04 · trace: AC-16 / EC-13 / ERR_PERMISSION_REVOKED
- actor: user without edit permission
- Setup: **(ต้อง simulate)** — prototype ไม่มี backend; ทดสอบที่ API layer: ผู้ใช้ที่ซ่อนปุ่ม UI แต่เรียก API-02/API-04 ตรง · files=—
- Start: (simulate API call)
- ผ่านเมื่อ: 403 ERR_INSUFFICIENT_ROLE / ERR_PERMISSION_REVOKED — การซ่อนปุ่มไม่ใช่การควบคุม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) เรียก POST/PUT API-02/API-04 ด้วย user ไม่มีสิทธิ์ (bypass UI) | — | ตอบ 403 ERR_INSUFFICIENT_ROLE หรือ ERR_PERMISSION_REVOKED; ไม่มีการเปลี่ยนข้อมูล | ☐ |
| 2 | (simulate) role ถูกถอนกลางคัน แล้ว mutate | — | 403 ERR_PERMISSION_REVOKED (re-check at mutation, ไม่ใช่ตอน GET) | ☐ |

#### TC-J02 — idempotent create ป้องกัน double-submit (edge, EC-16, ต้อง simulate)
- group: robustness · ความสำคัญ: ต่ำ · `[AI-DEFAULT]` (PR-4/PR-7) · trace: AC-17 / EC-16
- actor: Finance Admin
- Setup: **(ต้อง simulate)** — Idempotency-Key เป็นกลไก backend · files=—
- Start: (simulate) double POST create ด้วย key เดียวกัน
- ผ่านเมื่อ: บัญชีเดียว; ครั้งที่สองคืน cached; ไม่มี audit ซ้ำ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) POST create ×2 ด้วย Idempotency-Key เดียวกัน + body เดียวกัน | — | สร้าง 1 record; ครั้งที่ 2 คืนผลเดิม (cached); audit `created` มีรายการเดียว | ☐ |
| 2 | (simulate) POST ด้วย key เดิม + body ต่าง | — | 409 ERR_DUPLICATE_IDEMPOTENCY_KEY | ☐ |

#### TC-J03 — stale edit → 409 (edge, EC-17, ต้อง simulate)
- group: robustness · ความสำคัญ: ต่ำ · `[AI-DEFAULT]` (PR-2) · trace: AC-18 / EC-17 / ERR_STALE_DATA
- actor: Finance Admin ×2
- Setup: **(ต้อง simulate)** — optimistic lock ผ่าน If-Match/version (backend) · files=—
- Start: (simulate) 2 users edit บัญชีเดียวกัน
- ผ่านเมื่อ: edit ด้วย version เก่า → 409 ERR_STALE_DATA

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) user A + B โหลดบัญชีเดียวกัน; A บันทึกก่อน; B บันทึกด้วย If-Match เก่า | — | B ได้ 409 ERR_STALE_DATA | ☐ |

#### TC-J04 — finance_user ดู masked ได้ แต่ไม่มีปุ่ม action (P0 permission, ต้อง simulate)
- group: permission · ความสำคัญ: **สูง (P0)** · trace: permission matrix (finance_user)
- actor: finance_user (view-only)
- Setup: **(ต้อง simulate)** — prototype มี user เดียว (finance_admin). ต้อง mock role=finance_user (view masked only, canRevealFull=false, no create/edit/archive) · files=—
- Start: (simulate role) OPEN `#/bank-master`
- ผ่านเมื่อ: เห็นรายการ masked; ไม่มีปุ่ม `สร้างบัญชี`/`แก้ไข`/`เก็บถาวร`; reveal ถูกปฏิเสธ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate finance_user) OPEN `#/bank-master` → VERIFY | — | ตารางแสดง masked; **ไม่มี** ปุ่ม `สร้างบัญชี`; แถวไม่มีไอคอน `แก้ไข`/`เก็บถาวร` (หรือถูก gate ที่ backend) | ☐ |
| 2 | CLICK `ดูเต็ม` (ถ้ามี) | — | ถูกปฏิเสธ; toast `คุณไม่มีสิทธิ์ดูเลขบัญชีเต็ม`; เลขยัง masked | ☐ |

#### TC-J05 — reveal rate limit >50/วัน → 429 (error, ต้อง simulate)
- group: error · ความสำคัญ: ต่ำ · trace: ERR_REVEAL_RATE_LIMITED (BRD §17.4)
- actor: Finance Admin (canRevealFull)
- Setup: **(ต้อง simulate)** — rate limit เป็นกลไก backend (>50 reveals/user/วัน) · files=—
- Start: (simulate) reveal ครั้งที่ 51
- ผ่านเมื่อ: 429 ERR_REVEAL_RATE_LIMITED

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) reveal เลขบัญชีเกิน 50 ครั้ง/วัน | — | ครั้งที่ 51 → 429 ERR_REVEAL_RATE_LIMITED; ไม่คืนเลขเต็ม | ☐ |

---

### Group K — Scope Lock verify

#### TC-K01 — LOCK-01 ไม่มี tier / Lite-Full (verify absence)
- group: scope-lock · ความสำคัญ: สูง · trace: LOCK-01 / 05_RULES §5.3
- actor: Finance Admin
- Setup: role=finance_admin · seed=— · files=—
- Start: OPEN `#/bank-master`
- ผ่านเมื่อ: ไม่มี UI ใดพูดถึง tier/package/upgrade/Lite-Full/ไอคอน 🔗✋

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → กวาดทั้งหน้า (2 แท็บ + drawer สร้าง) | — | **ไม่มี** ข้อความ/ป้าย tier, package, upgrade, "Lite/Full", ไอคอนล็อกโหมด (🔗/✋); การเข้าถึงคุมด้วย permission ล้วน (RBAC) | ☐ |

#### TC-K02 — LOCK-02 มี 2 ระดับเท่านั้น (verify)
- group: scope-lock · ความสำคัญ: สูง · trace: LOCK-02
- actor: Finance Admin
- Setup: role=finance_admin · seed=— · files=—
- Start: OPEN `#/bank-master`
- ผ่านเมื่อ: มีแค่ 2 แท็บ = ธนาคาร (list) + บัญชีบริษัท (per company); ไม่มี level อื่น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → VERIFY แท็บ | — | มี 2 แท็บเท่านั้น: `บัญชีบริษัท` + `ธนาคาร`; ไม่มี level/entity อื่นในฟีเจอร์นี้ | ☐ |

#### TC-K03 — LOCK-03 downstream pickers + inbound CoA GL (verify)
- group: scope-lock · ความสำคัญ: สูง · trace: LOCK-03 / XT-01..04
- actor: Finance Admin
- Setup: role=finance_admin · seed=CoA 6 codes · files=—
- Start: OPEN `#/bank-master`
- ผ่านเมื่อ: มี picker จำลอง (downstream) + combobox GL จาก CoA (inbound)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → VERIFY ปุ่ม `จำลองเลือกในเอกสาร` | — | มีปุ่ม (soft-ref picker สำหรับ PV/RV/Recon/Payroll) | ☐ |
| 2 | CLICK `สร้างบัญชี` → CLICK `บัญชี GL (ผังบัญชี) *` → TYPE `1010` | — | combobox ดึง CoA (inbound): เห็น `1010-01..06` รวม `1010-06 เงินฝากธนาคาร - บัญชีเงินเดือน` (payroll) | ☐ |

#### TC-K04 — LOCK-04 OUT bank API/statement + multi-currency THB only (verify absence)
- group: scope-lock · ความสำคัญ: สูง · `[AI-DEFAULT]` (currency) · trace: LOCK-04 / OOS-1/2 / BR-BNK-10
- actor: Finance Admin
- Setup: role=finance_admin · seed=— · files=—
- Start: OPEN `#/bank-master`
- ผ่านเมื่อ: ไม่มี import statement / เชื่อม bank API; สกุลเงิน THB ล็อกอย่างเดียว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → กวาดทั้ง 2 แท็บ | — | **ไม่มี** ปุ่ม/เมนู "นำเข้า statement", "เชื่อมต่อธนาคาร/bank API", "sync ธนาคาร" | ☐ |
| 2 | CLICK `สร้างบัญชี` → VERIFY ช่องสกุลเงิน | — | เลือกได้เฉพาะ `THB — บาทไทย` (readonly); ไม่มี dropdown สกุลเงินอื่น | ☐ |

#### TC-K05 — LOCK-05 HTML = source of truth (1 route) (verify)
- group: scope-lock · ความสำคัญ: กลาง · trace: LOCK-05 / route map
- actor: Finance Admin
- Setup: role=finance_admin · seed=— · files=—
- Start: OPEN `#/bank-master`
- ผ่านเมื่อ: มี route เดียว `#/bank-master`; refresh คงหน้าเดิม (คืนแท็บ `บัญชีบริษัท`)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → CLICK แท็บ `ธนาคาร` → refresh หน้า (F5) | — | route ยังเป็น `#/bank-master`; หลัง refresh กลับมาแท็บ `บัญชีบริษัท` (แท็บเป็น in-memory ไม่ผูก hash) | ☐ |
| 2 | VERIFY breadcrumb | — | `การเงิน` › `ธนาคาร / บัญชีบริษัท` | ☐ |

#### TC-K06 — LOCK-06 no scope creep (verify sweep)
- group: scope-lock · ความสำคัญ: กลาง · trace: LOCK-06 / Coverage Manifest
- actor: Finance Admin
- Setup: role=finance_admin · seed=— · files=—
- Start: OPEN `#/bank-master`
- ผ่านเมื่อ: ไม่มีฟีเจอร์นอกขอบเขต (PromptPay/e-payment, per-account purpose tag, per-bank format table)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → CLICK `สร้างบัญชี` → กวาดฟิลด์ทั้งหมด | — | มีเฉพาะ: ธนาคาร/เลขที่บัญชี/ชื่อบัญชี/ประเภท/สาขา/สกุลเงิน/GL/default toggles. **ไม่มี** ช่อง PromptPay/e-payment ID, purpose tag (payroll-only ฯลฯ) | ☐ |
| 2 | CLICK `สร้างธนาคาร` → กวาดฟิลด์ | — | มีเฉพาะ ชื่อธนาคาร/ชื่อย่อ/รหัส ธปท./SWIFT/ประเภท. ไม่มีตาราง per-bank account-number format | ☐ |

#### TC-K07 — LOCK-07 W1 custom hard-delete เฉพาะ used=0 (verify)
- group: scope-lock · ความสำคัญ: สูง · trace: LOCK-07 / BR-BNK-08
- actor: Finance Admin
- Setup: role=finance_admin · seed=custom bank used=0 และ custom bank used>0 (สร้างตาม TC-F09/F10) · files=—
- Start: OPEN `#/bank-master` → แท็บ `ธนาคาร`
- ผ่านเมื่อ: custom used=0 ลบได้; custom used>0 ลบไม่ได้ (disabled); preset ไม่มีปุ่มลบเลย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/bank-master` → แท็บ `ธนาคาร` → VERIFY custom used=0 | — | ปุ่มลบ (trash) กดได้ (สีแดง) | ☐ |
| 2 | VERIFY custom used>0 | — | ปุ่มลบ disabled + tooltip `มี {N} บัญชีอ้างอิงธนาคารนี้ — ลบไม่ได้` | ☐ |
| 3 | VERIFY preset (BBL) | — | ไม่มีปุ่มลบเลย (cell `มาตรฐาน`) — preset ห้ามลบตลอด | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด prototype `BankMaster.html` ใน browser. ทุกเคสเริ่มด้วย `Start` (OPEN `#/bank-master`) — refresh ก่อนทุกเคสเพื่อ reset in-memory state กลับ seed (refresh-safe).
2. ทำ step ตามลำดับ; อ่าน Action (verb tag) → ทำกับ target ที่เป็น **ข้อความบนจอ** (ปุ่ม/ป้าย/หัวคอลัมน์/แท็บ). กรอก Input จาก Data Sets.
3. ตัดสิน pass/fail ต่อ step จาก **Expected ที่เห็นได้ด้วยตา** (ข้อความ/route/pill/ปุ่ม disabled/toast). ติ๊ก `☐`→ผ่าน/ไม่ผ่าน.
4. เคส **(ต้อง simulate)** = ต้องมี runner/backend เตรียมสภาพ (แก้ `currentUser.canRevealFull`, mock role, หรือเรียก API ตรง). ถ้าทำไม่ได้ → mark `blocked` + ใส่เหตุผลใน evidence.
5. เคส TC-E03/E06 (EC-14 — RESOLVED: warn+clear): ตรวจว่า confirm modal แสดง default-loss warning ก่อนยืนยัน และหลังยืนยัน flag ถูกเคลียร์ (co-bar `ยังไม่ตั้ง`). FRD กับ HTML ตรงกันแล้ว.
6. บันทึกผลตาม Result Report schema ท้ายไฟล์.

---

## Coverage Audit

| หมวด | covered / total |
|---|---|
| FR / User Stories (00 §0.12) | 9 / 9 |
| Business rules (05_RULES §5.1) | 12 / 12 |
| Field validation (§5.4) | 12 / 12 |
| Edge cases (§5.5) | 16 / 17 (ข้าม EC-11) |
| Error codes (§5.6) | 16 / 16 (ที่สังเกต/simulate ได้) |
| Permission matrix cells (§5.3) | ครบ (finance_admin ทุก action + finance_user deny + reveal deny + backend gate) |
| Cross-Module (XT §6.9) | 4 / 4 |
| Scope Lock (LOCK §7.0) | 7 / 7 |
| Cross-cutting / states / events | ครบ (status pills · empty/filtered-empty · audit newest-first/append-only · Esc chain · soft-ref) |

- **Cross-Module (XT): 4/4** — XT-01 (TC-G01), XT-02 (TC-G02 sim), XT-03 (TC-G03 sim), XT-04 (TC-G04).
- **Scope Lock (LOCK): 7/7** — LOCK-01..07 → TC-K01..K07.
- **Manifest cross-check (FRD §0.12): ✅** — Stories 9/9 · Rules 12/12 · Edges 15/15 (BRD-confirmed) ทุกแถวมีคู่ใน Ledger. (FRD 06_TESTS AC-01..AC-18 ทั้งหมด mapped: AC-01→A01, AC-02→A02/A03, AC-02b→A04/A05, AC-02c→A06, AC-03→B01, AC-04→C01-C03, AC-04b→C06, AC-05→E01/E02, AC-05b→E07/G01, AC-05c→E03, AC-06→E04, AC-06b→E05, AC-07→D02/D05/D07, AC-08→D04, AC-09→D06, AC-10→F02/F03, AC-11→F04/F05, AC-12→F10, AC-13→F09/F11, AC-14→H01/F13, AC-15→A09, AC-16→J01, AC-17→J02, AC-18→J03.)

### ข้าม (พร้อมเหตุผล)
- **EC-11 (GL disabled in CoA after binding)** — posting/warn เป็นความรับผิดชอบของ downstream consumer (PV/RV/Payroll); ไม่มี observable UI บนหน้า master นี้ → `[AI-DEFAULT]` ข้าม (ตาม 05_RULES §5.5 EC-11).
- **OOS-1..6 / LOCK-04 exclusions** (bank API, statement import, active multi-currency, PromptPay/e-payment ID, per-account purpose tag, per-bank format table) — **นอกขอบเขตใบเซ็น** → ไม่สร้างเคสทดสอบฟีเจอร์; verify การไม่มีอยู่ที่ TC-K04/K06 เท่านั้น.

### หมายเหตุ resolved / [AI-DEFAULT]
- **EC-14 / OQ-BNK-05 — RESOLVED 2026-08-06 (warn + clear):** TC-E03 + TC-E06 ตรวจว่า confirm modal แสดง default-loss warning ก่อนยืนยัน และ default flag ถูกเคลียร์เมื่อ deactivate/archive. FRD กับ HTML ตรงกันแล้ว — ไม่มี divergence.
- **`[AI-DEFAULT]` propagation:** เคสที่ derive จาก rule/edge ติด `[AI-DEFAULT]` ถูกแท็กที่หัวเคสแล้ว — TC-A02/A03 (BR-BNK-03 range), TC-A09/K04 (BR-BNK-10 currency), TC-C06 (EC-12), TC-D06 (EC-15), TC-J01 (EC-13→OQ-04), TC-J02 (EC-16), TC-J03 (EC-17). ผล fail ของเคสเหล่านี้อาจแปลว่า "default AI ผิด" ไม่ใช่ "โค้ดผิด".

---

## Result Report (schema)

```json
{
  "feature_id": "F-BNK",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-A01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 76, "pass": 0, "fail": 0, "blocked": 0 }
}
```

> `evidence` = สิ่งที่ agent **เห็นจริง** ตอน fail/blocked (ข้อความ error/toast จริง, route ที่ค้าง, ค่าที่แสดงแทน Expected). เคส `(ต้อง simulate)` ที่ runner เตรียมสภาพไม่ได้ → `blocked` + ระบุใน note ว่าต้อง inject อะไร. เคส TC-E03/E06 (EC-14 RESOLVED: warn+clear) → ตรวจ warn note + flag เคลียร์; ถ้า fail = defect ปกติ (ไม่มี divergence แล้ว).

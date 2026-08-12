# 06_TESTS — F-BNK Bank Master (บัญชีธนาคาร)

> **Audience:** QA engineer
> **Purpose:** Acceptance Criteria + DoD + Cross-Module + Microcopy-verbatim
> **Coverage source:** 02_API + 03_LOGIC + 05_RULES + HTML SoT + E2E R1 (21/21) + R2 (15/15)
> **Expected text:** ยึด **HTML verbatim** ก่อน (§6.10) แล้ว fallback microcopy กลาง html-generator-v8 — ห้ามแต่งคำเอง
> **Scenario trace:** ทุก AT map กลับ S-01..S-10 (PREBRIEF) / BR / FN

---

## §6.1 Acceptance Criteria (AC)

### AT-01: เพิ่มบัญชี — happy path (S-01 / US-01)
**Given** Finance Admin เปิด create drawer (P-02) · **When** กรอก ธนาคาร + เลขที่บัญชี (10–12 หลัก ไม่ซ้ำ) + ชื่อบัญชี + ฝั่ง ≥1, กด "ยืนยันสร้าง"
**Then** POST /bank-accounts → 201, status=active, used=0, DOA fields=null · drawer ปิด + toast success **"เพิ่มบัญชีธนาคาร "{code}" แล้ว"** · แถวใหม่โผล่ (E2E R1 #10)

### AT-02: code auto + duplicate (S-01/S-05 · BR-08)
**Given** create · **When** เว้น code → auto `{ธนาคาร}-{เลขรัน}` (เช่น KBANK-03) ไม่ชนกัน (FN-09)
**When** กรอก code ที่มีอยู่ (เช่น `KBANK-01`) → block, field `#fld-code` has-err, message **"รหัส KBANK-01 ถูกใช้แล้ว"** (E2E R2 #6, case-insensitive) · API 422/409 ERR_CODE_DUPLICATE

### AT-03: ค้นหา/กรอง/sort/pager List (S-09 · US-08 · FN-04)
**Given** P-01 (8 records) · **When** search "KBANK" → 2 rows; bank=KBANK → 2; status=ใช้งาน → 6; stat card กด → กรอง (กดซ้ำ "ทั้งหมด" reset); sort header asc/desc; pager
**Then** ทำงานร่วมกัน, footer **"แสดง N–M จาก K รายการ"**, ph-count **"{K} บัญชี"**, scroll ไม่เด้ง (Iron Rule #29) (E2E R1 #2–8)

### AT-04: account_no 10–12 หลัก (S-05 · BR-01)
**Given** create · **When** เลขบัญชี `ABCXYZ` หรือ `123` (dash-strip < 10) → block, `#fld-acct-no` has-err **"เลขบัญชี 10–12 หลัก (ใส่ขีดได้)"**, count ไม่เพิ่ม (E2E R2 #7) · API 422 ERR_ACCT_INVALID

### AT-05: account_no unique registry-wide dash-strip (S-05 · BR-01)
**Given** create · **When** เลขบัญชีตรงกับที่มี (เทียบตัดขีด, เช่น `012345678 9` vs `012-3-45678-9`) → block, `#fld-acct-no` has-err **"เลขบัญชีนี้มีในทะเบียนแล้ว (ACCT_DUPLICATE)"** · API 422 ERR_ACCT_DUPLICATE
### AT-05b: promptpay ว่าง/10/13 (S-05 · BR-06)
**Given** create · **When** promptpay = 5 หลัก → block **"ต้องเป็นเบอร์ 10 หลัก หรือเลขภาษี 13 หลัก"** · ว่าง / 10 / 13 หลัก → ผ่าน

### AT-06: ใช้ฝั่ง ≥1 (S-01/S-05 · BR-03)
**Given** create · **When** ปิดทั้ง 2 ฝั่ง (use_receive=use_pay=false) → block, `#fld-use` has-err **"ต้องเลือกอย่างน้อย 1 ฝั่ง"** · API 422 ERR_USE_IN_EMPTY

### AT-07: ★ default 1/ฝั่ง + DEFAULT_GUARD (S-03 · BR-03)
**Given** create/edit · **When** ติ๊ก ★รับ บนตัวที่ไม่เปิดฝั่งรับ **หรือ** สถานะ ≠ ใช้งาน → block + toast **"บัญชีหลักต้องอยู่ฝั่งที่เปิดใช้ และสถานะ "ใช้งาน" เท่านั้น"** (error)
**When** ตั้ง ★รับ ตัวใหม่ (active + ฝั่งเปิด) → ตัวเก่าฝั่งรับหลุด ★ อัตโนมัติ (radio ทั้งระบบ) · list โชว์ `★รับ`/`★จ่าย` หลังรหัส

### AT-08: IR-BNK-01 lock ธนาคาร+เลขบัญชี (S-04 · BR-02)
**Given** edit บัญชีที่ used>0 (เช่น KBANK-01 used=620) · **Then** `#in-bank` disabled + `#in-acct-no` disabled + 2 lock-tag **"ล็อก — มีเอกสารผ่านแล้ว"** · `#in-acct-name` ยังแก้ได้ (E2E R1 #13, R2 #9)

### AT-09: IR-BNK-01 save guard (fล็อกฝืน DOM) (S-04 · BR-02 · EC-01/EC-03)
**Given** edit used>0 · **When** ฝืนลบ `disabled` + เปลี่ยน bank/account_no ผ่าน JS + save · **Then** record ยัง `bank=KBANK`, `account_no` เดิม (save guard `if(!locked){data.bank=…}`) · field อื่น (ประเภท/ฝั่ง/★) เปลี่ยนได้ · เอกสารเก่า snapshot ไม่ retro (E2E R2 #9)

### AT-10: KTB-01 (used=0) แก้ได้ทุก field (S-04)
**Given** edit KTB-01 (used=0) · **Then** bank/account_no **ไม่** disabled · button "บันทึกการแก้ไข" · save → close + toast **"บันทึกการแก้ไข "{code}" แล้ว"** (E2E R1 #12)

### AT-11: ผูกกลุ่ม GL — active-only (S-02 · BR-04 · FN-14)
**Given** create ใหม่ · **Then** picker กลุ่ม GL options = **["— ยังไม่ผูกกลุ่ม —", "KBANK — ธนาคารกสิกรไทย"]** — **SCB (draft) ไม่โผล่** (E2E R1 #11, R2 #11)
**And** DEV: แหล่งจริง = generic F-PG-API-01 `?kind=bank&status=active` (คืน KBANK เท่านั้น) — ไม่ใช่ mock local list (3 drifts §02_API §2.6)

### AT-12: GL keep-bound draft (S-02 · BR-04 · EC-04)
**Given** edit SCB-01 (ผูก SCB=draft) · **Then** option **"SCB — ธนาคารไทยพาณิชย์ (ร่าง)"** ปรากฏ + selected (คงไว้กันหลุด) · rebind → KBANK แล้ว save → `posting_group='KBANK'` (แทนที่สะอาด ไม่มี orphan) (E2E R1 #14, R2 #11)
**And** view ที่ไม่ผูกกลุ่ม → hint **"ยังไม่ผูก — GL post ไม่ได้จนกว่าจะผูกกลุ่ม"**

### AT-13: เปลี่ยนสถานะเดี่ยว (S-06 · US-05)
**Given** P-04 view · **When** เมนู "เปลี่ยนสถานะ" เลือกค่าใหม่ (ค่าปัจจุบัน disabled) → POST /:id/status · **Then** toast **"เปลี่ยนสถานะ "{code}" เป็น {label} แล้ว"** (label: ร่าง/ใช้งาน/ไม่ใช้งาน) · menu paint เหนือ drawer body (E2E R1 #16, R2 #3)

### AT-14: side effect ★ หลุดเมื่อออก active (S-06 · BR-03)
**Given** บัญชี active + ★รับ · **When** เปลี่ยนสถานะ → ไม่ใช้งาน (เมนู/bulk/form) · **Then** `default_receive`+`default_pay` = false (★ ทั้ง 2 ฝั่งหลุด)

### AT-15: bulk ลบ + guard used>0 (S-07 · US-06 · BR-02)
**Given** เลือกรวม used>0 · **When** bulk "ลบ" → modal "ลบบัญชีธนาคาร N รายการ?" + desc **"มี {used} รายการมีเอกสารรับ/จ่ายผ่านแล้ว — จะถูกข้าม ไม่ลบ (ใช้เปลี่ยนสถานะแทน)"** · ปุ่ม **"ลบ D รายการ"** (disabled ถ้า D=0)
**When** ยืนยัน → POST /bulk-delete · **Then** used=0 ลบ, used>0 ข้าม · toast **"ลบแล้ว D รายการ · ข้าม M (มีเอกสารผ่านแล้ว)"** (warning) หรือ **"ลบแล้ว D รายการ"** (success) (E2E R1 #17/#18, R2 #10)

### AT-16: นำเข้า CSV — preview validate (S-08 · US-07 · BR-01/07/10)
**Given** "นำเข้า CSV" → P-05 · **When** เลือกไฟล์ (BULK_SAMPLE 6 แถว) · **Then** preview **"ตรวจแล้ว 6 แถว — นำเข้าได้ 3 · ติดปัญหา 3 (แถวผิดจะถูกข้าม)"** (E2E R1 #19)
**And** ต่อแถว: valid → **"✓ พร้อมนำเข้า"** · KBANK-01 → **"เลขบัญชีซ้ำทะเบียน (ACCT_DUPLICATE)"** · BAD-01 → **"ธนาคารไม่รู้จัก (BAD_BANK)"** · UOB-01 (แถว 2) → **"รหัสซ้ำในไฟล์ (IN_FILE_DUPLICATE)"** หรือ **"เลขบัญชีซ้ำในไฟล์ (IN_FILE_DUPLICATE)"**

### AT-17: นำเข้า merge-only + defaults (S-08 · BR-07)
**Given** preview ผ่าน 3 แถว · **When** "นำเข้า 3 แถว" → commit · **Then** เพิ่ม 3 record ใหม่ (ไม่แตะเดิม) · ค่าเว้น = ประเภทออมทรัพย์/ฝั่งทั้งสอง/สถานะร่าง · posting_group='' promptpay='' used=0 DOA null · toast **"นำเข้าแล้ว 3 รายการ · ข้าม 3 แถว (IMPORT_ERROR)"** (warning)
**And** **ไม่มี** Replace/Merge toggle (merge/append-only เท่านั้น — E2E R1 #19 design note)
### AT-17b: ไฟล์ ≠ .csv (S-08 · EC-10)
**When** เลือกไฟล์ ≠ .csv → toast warning **"โหมดสาธิตรองรับเฉพาะ .csv — .xlsx ให้ save as CSV ก่อน (dev: parser จริงตอน integrate)"** · ไม่ load

### AT-18: ส่งออก CSV (S-09 · US-08 · FN-13)
**Given** P-01 (filter ใด ๆ) · **When** "ส่งออก CSV" · **Then** ดาวน์โหลด `bank_export_YYYY-MM-DD.csv` (BOM, columns roundtrip กับ template, bank/type/use_in/status = ไทย) · toast **"ส่งออก {n} รายการเป็น CSV แล้ว"** (E2E R1 #20)

### AT-19: ไม่มี multi-currency/SWIFT/ยอดคงเหลือ (S-10 · BR-09 — negative)
**Then** สกุลเงิน = "THB — บาทไทย" disabled · ไม่มีตัวเลือกสกุลอื่น/SWIFT/IBAN/ยอดคงเหลือ/opening balance ที่ใดในระบบ · ไม่มี `used` แสดงบนจอ (S-10⑤)

### AT-20: Viewer/Consumer 403 (S-05 PM edge)
**Given** role=Finance Viewer เรียก POST/PUT/status/bulk/import ตรง · **Then** 403 ERR_INSUFFICIENT_ROLE

### AT-21: Empty state + close chain + no console error (robustness)
**Given** filter `ZZZ` → empty **"ไม่พบบัญชีธนาคารที่ตรงกับตัวกรอง"** + "ล้างตัวกรอง" (E2E R2 #12) · **And** Esc/backdrop/X ปิด drawer & modal (Esc chain modal>drawer>menu) · reload กลาง state → list สะอาด · **0 console errors** (E2E R1 #21, R2 #13–15)

---

## §6.2 Test Case Inventory

| TC ID | Name | Type | Maps to | Priority |
|---|---|---|---|---|
| TC-01 | List + filter/sort/pager | API/E2E | AT-03 | P0 |
| TC-02 | Create happy + auto code | API | AT-01/AT-02 | P0 |
| TC-03 | account_no invalid/dup | API neg | AT-04/AT-05 | P0 |
| TC-04 | promptpay 10/13 | API neg | AT-05b | P1 |
| TC-05 | use_in ≥1 | API neg | AT-06 | P0 |
| TC-06 | ★ default guard + radio | API | AT-07 | P0 |
| TC-07 | IR-BNK-01 lock + save guard | API/E2E | AT-08/AT-09 | P0 |
| TC-08 | edit used=0 all editable | API | AT-10 | P1 |
| TC-09 | GL picker active-only + keep-bound | API/UI | AT-11/AT-12 | P0 |
| TC-10 | status change single/bulk + ★ drop | API | AT-13/AT-14 | P0 |
| TC-11 | bulk delete guard | API | AT-15 | P0 |
| TC-12 | import preview validate (IN_FILE_DUPLICATE) | API | AT-16 | P0 |
| TC-13 | import commit merge-only + defaults | API | AT-17 | P0 |
| TC-14 | non-csv reject | UI | AT-17b | P1 |
| TC-15 | export roundtrip + BOM | API | AT-18 | P1 |
| TC-16 | no currency/used (absence) | Static | AT-19 | P1 |
| TC-CC-01 | concurrent ★ (409) | API stress | EC-08 | P1 |
| TC-ID-01 | idempotency/double-submit | API | EC-09 | P1 |
| TC-PR-01 | Viewer 403 | API | AT-20 | P1 |
| TC-UI-01 | empty + close chain + scroll #29 | E2E | AT-03/AT-21 | P1 |

---

## §6.3 Test Data Setup
- Seed 8 reference accounts (จาก HTML `state.records`): KBANK-01 (★รับ, used=620, ผูก KBANK, promptpay เลขภาษี) · SCB-01 (★จ่าย, used=340, current, ผูก SCB=draft) · BBL-01 · KTB-01 (used=0 — ลบได้) · KBANK-02 · BAY-01 (promptpay เบอร์) · TTB-01 (draft) · GSB-01 (inactive, used=15)
- BULK_SAMPLE 6 แถว (import): 3 valid + KBANK-01 (ACCT_DUPLICATE ทะเบียน) + BAD-01 (BAD_BANK) + UOB-01 แถว 2 (IN_FILE_DUPLICATE)
- Roles: `qa_finance_admin`, `qa_finance_viewer`, `qa_consumer` (downstream)
- Tenants: 2 (isolation test)

---

## §6.4 Definition of Done (DoD)

### Code
- [ ] ทุก AT (AT-01..21) implemented + unit tests
- [ ] Integration: API + DB (2 partial-unique ★ index + account_no dash-strip unique)
- [ ] E2E: happy + validations + IR-BNK-01 lock/guard + bulk + import merge-only + status ★ drop
- [ ] Server-side mirror ครบ (Control C4 — saveBank + bulkValidateRow)
- [ ] Coverage ≥ 80% logic layer

### Documentation
- [ ] API docs auto จาก 02_API · FRD 07_LOCKED สะท้อน final
- [ ] **GL contract:** consume generic F-PG-API-01 `?kind=bank&status=active` (แก้ 3 drifts) confirmed กับ F-PG owner

### QA
- [ ] P0 + P1 pass · ไม่มี P0/P1 bug open
- [ ] Security checklist D2/D5/D9/D11/D15/D17 verified · account_no masking (C11) + access log (C6)
- [ ] **Blocking OQ ปิด:** OQ-BNK-06 (GL drift), OQ-BNK-07 (used def) ก่อน dev ส่วนที่เกี่ยว

### Deployment
- [ ] Migration tested (T_bank_account + config seed BANKS/ACCT_TYPES, ห้าม hardcode)
- [ ] Downstream picker (GET /active) SLA <500ms verified

---

## §6.5 WebSocket / Realtime
- **N/A** — ไม่มี NOTIF/WebSocket (SCOPE_LOCK). Feedback = toast เท่านั้น.

---

## §6.6 Performance Benchmarks
| Endpoint | P95 | Note |
|---|---|---|
| GET /bank-accounts (list) | < 800ms | small master (~หลักสิบ/บริษัท) |
| GET /bank-accounts/active (picker) | **< 500ms** | BRD §17.1 SLA · cacheable |
| F-PG-API-01 posting-groups picker | **< 500ms** | external, cacheable |
| POST/PUT /bank-accounts | < 1000ms | validate synchronous |

---

## §6.7 Test Environment Notes
- HTML mock = client-side synchronous · production = server-side (mirror validation)
- `used` = mock counter จนกว่า OQ-BNK-07 ปิด (นิยามจริง = count Receipt/PV posted) — E2E ใช้ seed (KBANK-01=620, KTB-01=0)
- GL picker = ใน HTML ใช้ local `BANK_POSTING_GROUPS` (KBANK active/SCB draft) · production = F-PG API-01 (คืน KBANK เท่านั้น) — test both mock parity + real contract
- E2E baseline: R1 21/21 + R2 15/15, 0 console errors (ดู `02_QC/_E2E_ROUND1/2_REPORT.md`)

---

## §6.8 Trace: AC → Logic Coverage

| AT | API tested | Functions |
|---|---|---|
| AT-01/02 | API-02 | FN-01, FN-03, FN-09 |
| AT-03 | API-01 | FN-04, FN-10 |
| AT-04/05/05b/06/07 | API-02/04 | FN-03, FN-08 |
| AT-08/09/10 | API-04 | FN-02, FN-03 |
| AT-11/12 | (form picker) | FN-14 |
| AT-13/14 | API-05 | FN-05 |
| AT-15 | API-07 | FN-07 |
| AT-16 | API-08 | FN-11 |
| AT-17/17b | API-09 | FN-12 |
| AT-18 | API-10 | FN-13 |
| AT-20 | API-02/04/05/06/09 | (role guard) |
| (downstream) | API-11 | FN-13b |

> **Coverage check:** FN-01..14 (รวม FN-13b) ทุกตัวถูก trace ≥1 AT ✅ · ไม่มี engine (feature นี้ไม่มี) ✅

---

## §6.9 Cross-Module Test Cases ⭐ (จาก BRD §12.1 Downstream)

| ID | Scenario | Downstream | Expected |
|---|---|---|---|
| XT-01 | ปลายทาง (Receipt) เรียก GET /active?side=receive → เลือกบัญชี → สร้างเอกสาร | Receipt / PV | คืนเฉพาะ active + ฝั่งตรง · ★รับ pre-select · snapshot code+ค่า · master แก้ทีหลัง → เอกสารเก่า snapshot ไม่เปลี่ยน |
| XT-02 | master → inactive | picker | ไม่โผล่ใน Receipt/PV ใหม่ · เอกสารเก่า snapshot ยังใช้ได้ (EC-05) |
| XT-03 | consume F-PG API-01 (`?kind=bank&status=active`) | F-PG (GL Posting Group) | คืน KBANK เท่านั้น (SCB=draft filtered) · edit record ผูก SCB(draft) → keep-bound แสดง "(ร่าง)" (EC-04/EC-06, 3 drifts) |
| XT-04 | บัญชีผูกกลุ่ม → Receipt/PV post | external GL engine | resolve บัญชีเงินฝาก (COA) ผ่าน account_1 ของกลุ่ม · account_1=NULL → post ไม่ได้ (EC-07) · view เตือนล่วงหน้าถ้าไม่ผูก (BR-04) |
| XT-05 | ~~เส้นออก Payment Method~~ | ~~PM (F-0.20)~~ | **CUT (OQ-BNK-01=NO)** — ยืนยันว่า Bank Master ไม่ expose ให้ PM (negative) |

---

## §6.10 Microcopy-Aware Expected Text (HTML verbatim)

> ยึดข้อความจริงบนจอก่อนเสมอ. ค่าเหล่านี้ extracted จาก `01_HTML/f-bank.html` — ห้ามแต่งใหม่.

**Buttons:** "เพิ่มบัญชีธนาคาร" · "ส่งออก CSV" · "นำเข้า CSV" · "ยืนยันสร้าง" (create footer) · "บันทึกการแก้ไข" (edit footer) · "ยกเลิก" · "ปิด" (view) · "แก้ไข" · "เปลี่ยนสถานะ" · "ล้างตัวกรอง" · "ยกเลิกการเลือก" · "ดาวน์โหลด template ตัวอย่าง" · "เลือกไฟล์ CSV" · modal "นำเข้า {ok} แถว" / "ลบ {D} รายการ".

**Toasts:**
| เหตุการณ์ | ข้อความ verbatim | variant |
|---|---|---|
| สร้างสำเร็จ | `เพิ่มบัญชีธนาคาร "{code}" แล้ว` | success |
| แก้ไขสำเร็จ | `บันทึกการแก้ไข "{code}" แล้ว` | success |
| status เดี่ยว | `เปลี่ยนสถานะ "{code}" เป็น {label} แล้ว` | success |
| bulk status | `เปลี่ยนสถานะ {n} รายการ เป็น {label} แล้ว` | success |
| DEFAULT_GUARD | `บัญชีหลักต้องอยู่ฝั่งที่เปิดใช้ และสถานะ "ใช้งาน" เท่านั้น` | error |
| bulk delete (มีข้าม) | `ลบแล้ว {D} รายการ · ข้าม {M} (มีเอกสารผ่านแล้ว)` | warning |
| bulk delete (ไม่ข้าม) | `ลบแล้ว {D} รายการ` | success |
| import done (มีข้าม) | `นำเข้าแล้ว {ok} รายการ · ข้าม {err} แถว (IMPORT_ERROR)` | warning |
| import done (ไม่ข้าม) | `นำเข้าแล้ว {ok} รายการ` | success |
| export | `ส่งออก {n} รายการเป็น CSV แล้ว` | success |
| template | `ดาวน์โหลด template ตัวอย่างแล้ว` | success |
| ไฟล์ ≠ csv | `โหมดสาธิตรองรับเฉพาะ .csv — .xlsx ให้ save as CSV ก่อน (dev: parser จริงตอน integrate)` | warning |

**Field errors (inline):** code ซ้ำ = `รหัส {code} ถูกใช้แล้ว` · acct default = `เลขบัญชี 10–12 หลัก (ใส่ขีดได้)` · acct dup = `เลขบัญชีนี้มีในทะเบียนแล้ว (ACCT_DUPLICATE)` · ชื่อว่าง = `กรุณากรอกชื่อบัญชี` · promptpay = `ต้องเป็นเบอร์ 10 หลัก หรือเลขภาษี 13 หลัก` · use = `ต้องเลือกอย่างน้อย 1 ฝั่ง`.

**Import validate (per row, verbatim):** `ข้อมูลบังคับไม่ครบ (REQUIRED)` · `ธนาคารไม่รู้จัก (BAD_BANK)` · `เลขบัญชี 10–12 หลัก (ACCT_INVALID)` · `เลขบัญชีซ้ำทะเบียน (ACCT_DUPLICATE)` · `ประเภทบัญชีไม่ถูกต้อง (BAD_TYPE)` · `ฝั่งใช้งานไม่ถูกต้อง (BAD_USE — รับ/จ่าย/ทั้งสอง)` · `สถานะไม่ถูกต้อง (BAD_STATUS — ใช้ ใช้งาน/ไม่ใช้งาน/ร่าง)` · `รหัสซ้ำ (CODE_DUPLICATE)` · `รหัสซ้ำในไฟล์ (IN_FILE_DUPLICATE)` · `เลขบัญชีซ้ำในไฟล์ (IN_FILE_DUPLICATE)`. Preview cell: `✓ พร้อมนำเข้า` / `✗ {error}`.

**Import modal:** title `นำเข้าบัญชีธนาคารจากไฟล์` · preview sum `ตรวจแล้ว {n} แถว — นำเข้าได้ {ok} · ติดปัญหา {x} (แถวผิดจะถูกข้าม)` · done sum `นำเข้าเสร็จ {ok} รายการ (สถานะตามไฟล์)`.

**Bulk delete modal:** title `ลบบัญชีธนาคาร {n} รายการ?` · desc (มี used>0) `มี {used} รายการมีเอกสารรับ/จ่ายผ่านแล้ว — จะถูกข้าม ไม่ลบ (ใช้เปลี่ยนสถานะแทน)` / (ไม่มี) `การกระทำนี้ย้อนกลับไม่ได้`.

**View:** header title = `{ธนาคาร} {maskAcct}` (เช่น `กสิกรไทย xxx-x-xx78-9`) · eyebrow `บัญชีธนาคาร · {code}` · chips: ธนาคาร / เลขที่บัญชี / ใช้กับฝั่ง / กลุ่มบัญชี GL (unbound → `ยังไม่ผูก`) · GL section warning `ยังไม่ผูก — GL post ไม่ได้จนกว่าจะผูกกลุ่ม` · lock-tag `ล็อก — มีเอกสารผ่านแล้ว` · ★ `★ บัญชีรับหลัก` / `★ บัญชีจ่ายหลัก` (list badge: `★รับ` / `★จ่าย`).

**use text:** `รับ + จ่าย` / `ฝั่งรับ (Receipt)` / `ฝั่งจ่าย (PV)` / `—`.

**Empty/list:** filtered empty = `ไม่พบบัญชีธนาคารที่ตรงกับตัวกรอง` · ว่างจริง = `ยังไม่มีบัญชีธนาคารในระบบ` · footer = `แสดง {a}–{b} จาก {n} รายการ` · ph-count = `{n} บัญชี`.

**Status labels:** `ร่าง` / `ใช้งาน` / `ไม่ใช้งาน`. **Stat cards:** `บัญชีทั้งหมด` / `ใช้งานอยู่` / `ไม่ใช้งาน` / `ร่าง`.

> ผลลัพธ์: testcase ที่ ai-testcase-md-generator สร้างต่อจะ match หน้าจอจริง 1:1.

# 03_LOGIC — F-BNK Bank Master (บัญชีธนาคาร)

> **Audience:** BE dev (business logic layer)
> **Scope:** All non-HTTP business logic — functions, validations, integrations
> **CUBIC:** §3.1 Functions = scope-local (camelCase) · §3.2 Engines = **ไม่มี engine ของ feature นี้** (GL resolve = external, §3.4)
> **R8:** ทุก mutation API ต้อง trace ≥1 Function ใน §3.3

---

## §3.1 Functions (Scope-Local)

### F-BNK-FN-01: `createBankAccount`
- **Purpose:** สร้างบัญชีใหม่จาก validated payload + auto code + จัดการ ★ default-per-side uniqueness
- **Input:** `{ code?, bank, account_no, account_name, branch?, account_type, promptpay_id?, posting_group?, use_receive, use_pay, default_receive, default_pay, status }`
- **Output:** `BankAccount | ValidationError[]`
- **Invoked by:** F-BNK-API-02 POST /bank-accounts
- **Calls:** F-BNK-FN-03 (validate), F-BNK-FN-09 (auto code ถ้าเว้น), F-BNK-FN-08 (★ per-side)
- **Side effects:** INSERT T_bank_account (used=0, currency='THB', DOA null×4) · INSERT T_audit_log · **ไม่ emit event**
- **Error cases:** ERR_REQUIRED, ERR_BAD_BANK, ERR_ACCT_INVALID, ERR_ACCT_DUPLICATE, ERR_CODE_DUPLICATE, ERR_PROMPTPAY_INVALID, ERR_USE_IN_EMPTY, ERR_DEFAULT_GUARD
- **Iron rule check:** ✅ no HTTP terms

### F-BNK-FN-02: `updateBankAccount` ⭐ IR-BNK-01 guard
- **Purpose:** แก้ไขบัญชี — **ถ้า used>0 ไม่ assign `bank`/`account_no`** (mirror HTML `if(!locked){data.bank=…;data.account_no=…}`); field อื่นแก้ได้เสมอ
- **Input:** `{ id, version, ...same as create }`
- **Output:** `BankAccount | ValidationError[]`
- **Invoked by:** F-BNK-API-04 PUT /bank-accounts/:id
- **Calls:** F-BNK-FN-03 (validate; account_no dup check ข้ามถ้า locked), F-BNK-FN-08 (★ per-side)
- **Logic:** `locked = (used>0)`; assign ทุก field ยกเว้น (ถ้า locked) `bank`+`account_no` → คงค่าเดิม. Save-guard นี้ทำให้ค่าที่ client ฝืนส่งมา **ไม่ persist** (E2E R2 #9).
- **Side effects:** UPDATE T_bank_account (version++) · unset ★ เดิมฝั่งเดียวกันถ้าตั้งใหม่ · INSERT T_audit_log (diff)
- **Error cases:** ERR_STALE_DATA, ERR_VALIDATION_FAILED, ERR_CODE_DUPLICATE, ERR_DEFAULT_GUARD
- **Iron rule check:** ✅ · **Note:** ล็อกเฉพาะ 2 field (ต่างจาก Tax Code ที่ล็อกทั้งใบ) — เอกสารเก่า snapshot ไม่ retro (EC-03)

### F-BNK-FN-03: `validateBankAccount` ⭐ (mirror `saveBank()` + `bulkValidateRow()`)
- **Purpose:** ตรวจ payload ครบทุกกฎก่อน create/edit + import row (reuse) — server-side mirror ของ HTML validation
- **Input:** payload + `existingRecords` (dup check) + `recordId?` (exclude self) + `locked?` (used>0)
- **Output:** `ValidationError[]` (ว่าง = ผ่าน) — แต่ละ error: `{ field, code, message }`
- **Invoked by:** F-BNK-FN-01, F-BNK-FN-02, F-BNK-FN-11 (import)
- **Validation set (verbatim จาก HTML):**
  1. `account_name` required → `ERR_REQUIRED` (fld-acct-name)
  2. `bank` ∈ 9 enum → `ERR_BAD_BANK`
  3. `account_no`: `digits = account_no.replace(/\D/g,'')`; `10 ≤ len ≤ 12` (ข้ามถ้า locked) → `ERR_ACCT_INVALID`
  4. `account_no` **unique registry-wide เทียบตัดขีด** (`digits` เทียบ, exclude self, ข้ามถ้า locked) → `ERR_ACCT_DUPLICATE`
  5. `code` (หรือ finalCode หลัง auto) unique case-insensitive → `ERR_CODE_DUPLICATE` ("รหัส {code} ถูกใช้แล้ว")
  6. `promptpay_id`: ว่าง **หรือ** dash-strip len ∈ {10, 13} → `ERR_PROMPTPAY_INVALID`
  7. `use_receive || use_pay` = true → `ERR_USE_IN_EMPTY`
  8. **DEFAULT_GUARD:** `(default_receive && (!use_receive || status!='active')) || (default_pay && (!use_pay || status!='active'))` → `ERR_DEFAULT_GUARD` (toast "บัญชีหลักต้องอยู่ฝั่งที่เปิดใช้ และสถานะ "ใช้งาน" เท่านั้น")
- **Side effects:** — (pure; read existingRecords)
- **Iron rule check:** ✅ no HTTP terms

### F-BNK-FN-04: `buildBankListQuery`
- **Purpose:** ประกอบ query filter (search code/bankLabel/branch/account_no/account_name + bank + status) + sort + stat counts (stat 4 ใบ: all/active/inactive/draft)
- **Input:** `{ search?, bank?, status?, sort?, limit, offset, tenantId }`
- **Output:** `{ rows: BankAccount[], counts:{all,active,inactive,draft}, total }` (ไม่รวม `used` ใน rows ที่ส่งออก)
- **Invoked by:** F-BNK-API-01
- **Side effects:** — (read-only) · **Iron rule check:** ✅

### F-BNK-FN-05: `setBankStatus` ⭐ side-effect ★ drop
- **Purpose:** เปลี่ยนสถานะเดี่ยว (3 ค่าอิสระ, ทุกทิศ) + **ถ้า → non-active ให้ `default_receive=false`+`default_pay=false`** (★ ทั้ง 2 ฝั่งหลุด)
- **Input:** `{ id, status, version }`
- **Output:** `BankAccount | Error`
- **Invoked by:** F-BNK-API-05
- **Logic:** mirror HTML `setStatus`: `if(st!=='active'){ r.default_receive=false; r.default_pay=false; }`
- **Side effects:** UPDATE status (+ ★ drop) · INSERT T_audit_log · **Iron rule check:** ✅

### F-BNK-FN-06: `bulkSetBankStatus`
- **Purpose:** เปลี่ยนสถานะหลายรายการเป็นค่าเดียว (bulk bar) — ข้ามตัวที่เป็นค่าเดิมอยู่แล้ว
- **Input:** `{ ids[], status, tenantId }`
- **Output:** `{ updated:number }`
- **Invoked by:** F-BNK-API-06
- **Calls:** F-BNK-FN-05 semantics (per id: non-active → ★ drop) · **Side effects:** UPDATE many + audit · **Iron rule check:** ✅

### F-BNK-FN-07: `bulkDeleteBankAccounts` ⭐ (guard used>0)
- **Purpose:** ลบหลายรายการ — **ข้าม** ตัวที่ `used>0` (BR-02, no hard delete)
- **Input:** `{ ids[], tenantId }`
- **Output:** `{ deleted:number, skipped:number, skipped_ids[] }`
- **Invoked by:** F-BNK-API-07
- **Logic:** partition ids → deletable (used=0) vs skipped (used>0); DELETE deletable เท่านั้น
- **Side effects:** DELETE (used=0) + audit · **Iron rule check:** ✅

### F-BNK-FN-08: `enforceDefaultPerSide` ⭐ (radio-per-side system-wide)
- **Purpose:** เมื่อ set `default_receive=true` (หรือ `default_pay=true`) → unset ★ เดิมของ **ฝั่งเดียวกันทั้งระบบ** (1/ฝั่ง) + guard (ฝั่งเปิด + status=active)
- **Input:** `{ recordId, default_receive, default_pay, use_receive, use_pay, status, tenantId }`
- **Output:** `void | ERR_DEFAULT_GUARD`
- **Invoked by:** F-BNK-FN-01, F-BNK-FN-02
- **Logic:** mirror HTML: `if(defReceive) records.forEach(r=>{ if(r.id!==id) r.default_receive=false; });` (+ default_pay เช่นกัน). Guard = ส่วนหนึ่งของ FN-03 (DEFAULT_GUARD); DB enforce เพิ่มด้วย 2 partial-unique index (04_DB).
- **Side effects:** UPDATE sibling ★ (fั่งเดียวกัน) · **Iron rule check:** ✅

### F-BNK-FN-09: `generateBankCode`
- **Purpose:** สร้าง code อัตโนมัติเมื่อเว้นว่าง — `{bank}-{seq}` (seq 2 หลัก, ไม่ชนกัน)
- **Input:** `{ bank, existingCodes }`
- **Output:** `string` (เช่น `KBANK-03`)
- **Invoked by:** F-BNK-FN-01 (create)
- **Logic:** mirror HTML `autoCode`: `i=1; do{ c=bank+'-'+pad2(i); i++; }while(exists(c))`
- **Side effects:** — (pure) · **Iron rule check:** ✅

### F-BNK-FN-10: `maskAccountNo` / `normalizeAccountNo` (format helpers)
- **Purpose:** (a) `maskAccountNo` → mask เลขบัญชีที่ view header/render sensitive (`xxx-x-xx…` — mirror HTML `maskAcct`); (b) `normalizeAccountNo` → dash-strip digits สำหรับ dedup/compare
- **Input:** `account_no: string`
- **Output:** masked string / digits string
- **Invoked by:** F-BNK-API-01/03 (render), F-BNK-FN-03 (dedup)
- **Side effects:** — (pure) · **Iron rule check:** ✅

### F-BNK-FN-11: `previewImportRows` ⭐ (import validate + IN_FILE_DUPLICATE)
- **Purpose:** ตรวจ CSV rows ต่อแถว — validate (reuse FN-03 logic ผ่าน Thai-value map) + **ตรวจซ้ำกันเองในไฟล์** (รหัส/เลขบัญชี → IN_FILE_DUPLICATE)
- **Input:** `{ rows[], existingRecords }`
- **Output:** `{ rows: [{...row, error}], ok_count, err_count }`
- **Invoked by:** F-BNK-API-08
- **Logic:** mirror HTML `bulkValidateRow` + `bulkLoadRows`: map Thai (BANK_TH_MAP/TYPE_TH_MAP/USE_TH_MAP/STATUS_TH_MAP), validate REQUIRED/BAD_BANK/ACCT_INVALID/ACCT_DUPLICATE/BAD_TYPE/BAD_USE/BAD_STATUS/CODE_DUPLICATE; แล้ว track `seenCode`/`seenAcct` (dash-strip) → IN_FILE_DUPLICATE. ไฟล์**ไม่มี** posting_group/promptpay.
- **Side effects:** — (read existingRecords) · **Iron rule check:** ✅

### F-BNK-FN-12: `commitImportRows` (merge-only)
- **Purpose:** insert เฉพาะแถว valid — เพิ่มอย่างเดียว ไม่แตะแถวเดิม
- **Input:** `{ rows[] (error==null), tenantId }`
- **Output:** `{ imported:number, skipped:number }`
- **Invoked by:** F-BNK-API-09
- **Logic:** mirror HTML `bulkConfirm`: map Thai→enum; **default: account_type=savings, use=both (ทั้งสอง), status=draft (ร่าง)**; set `posting_group=''`, `promptpay_id=''`, `used=0`, `default_*=false`, DOA null×4. **ไม่มี Replace mode.**
- **Side effects:** INSERT many + audit (per row) · **Iron rule check:** ✅

### F-BNK-FN-13: `exportBankRegistry`
- **Purpose:** สร้าง CSV ตาม filter ปัจจุบัน (roundtrip columns + BOM) — mirror `exportCSV`
- **Input:** `{ filter, tenantId }`
- **Output:** CSV string (BOM, columns `code,bank,branch,account_no,account_name,account_type,use_in,status`, Thai labels)
- **Invoked by:** F-BNK-API-10
- **Side effects:** — (read-only; access-log สำหรับ Confidential) · **Iron rule check:** ✅

### F-BNK-FN-13b: `getActiveAccountsForPicker` ⭐ (downstream cross-module)
- **Purpose:** คืนบัญชีให้ Receipt/PV เลือก — **เฉพาะ status=active + ฝั่งตรง** (side=receive→use_receive / side=pay→use_pay) + ★ pre-select (BR-05)
- **Input:** `{ side: 'receive'|'pay', tenantId }`
- **Output:** `PickerAccount[]` (active + side, มี is_default = ★ ของฝั่งนั้น + snapshot fields)
- **Invoked by:** F-BNK-API-11 (downstream Receipt/PV — ยังไม่ทำ)
- **Side effects:** — (read-only, cacheable) · **Iron rule check:** ✅

### F-BNK-FN-14: `buildBankPostingGroupOptions` ⭐ (consume F-PG API-01)
- **Purpose:** สร้าง option set ของ picker "กลุ่มบัญชี GL" — เรียก **generic F-PG-API-01** `?kind=bank&status=active` แล้ว **union กับกลุ่มที่ record ผูกไว้เดิม (แม้ draft)** กัน binding หลุด
- **Input:** `{ currentPostingGroup?, tenantId }`
- **Output:** `[{ code, name_th, status }]` (active groups + current-bound แม้ draft, มี suffix "(ร่าง)" ถ้า draft)
- **Invoked by:** FE form (P-02/P-03) · validate ตอน save (posting_group ต้องเป็นค่าใน set หรือ '' — optional)
- **Logic:** mirror HTML `.filter(g=>g.status==='active'||g.code===r.posting_group)` — แต่ **แหล่งข้อมูลจริง = F-PG API-01 ไม่ใช่ local mock** (แก้ 3 drifts §2.6). Bank Master เก็บเฉพาะ `code` (NO FK). resolve บัญชีเงินฝากจริงเกิดที่ GL engine (§3.4).
- **Side effects:** — (read external API, cacheable) · **Iron rule check:** ✅ · **Ref:** OQ-BNK-06 (3 drifts)

---

## §3.2 Engines (Reusable / CUBIC-Registered)

> **ไม่มี CUBIC engine ที่ feature นี้เป็นเจ้าของ.** — Bank Master เป็น master registry ล้วน ไม่มี pure-calculation ที่ reusable ข้าม feature ต้อง register. (ต่างจาก sibling F-PAY ที่มี installment-validator / trigger-resolver.)
> logic ที่ดูเหมือน engine แต่**อยู่นอก scope feature นี้**:
> - **บัญชีเงินฝาก resolve ผ่าน posting group** = งานของ **external GL / Journal Engine** (owned โดย GL module) — ประกาศ contract ที่ §3.4 + 02_API §2.7, ไม่ implement ที่นี่.
> - **`used` counter increment** = เขียนโดย GL engine ตอน post สำเร็จ — mechanism นอก scope (OQ-BNK-07).
>
> ถ้าอนาคตต้องมี engine (เช่น cross-feature bank-account resolver ที่ standardize) → register CUBIC ตอนนั้น. ปัจจุบัน §3.2 = ว่างโดยตั้งใจ (R9: feature = registry + validation, logic ทั้งหมดเป็น scope-local function).

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| F-BNK-API-01 | GET | /bank-accounts | FN-04 (query), FN-10 (mask) | — |
| F-BNK-API-02 | POST | /bank-accounts | FN-01 (create), FN-03 (validate), FN-08 (★ per-side), FN-09 (auto code) | — |
| F-BNK-API-03 | GET | /:id | FN-10 (mask) | — |
| F-BNK-API-04 | PUT | /:id | FN-02 (update+IR guard), FN-03 (validate), FN-08 (★ per-side) | — |
| F-BNK-API-05 | POST | /:id/status | FN-05 (status + ★ drop) | — |
| F-BNK-API-06 | POST | /bulk-status | FN-06 (bulk status) | — |
| F-BNK-API-07 | POST | /bulk-delete | FN-07 (bulk delete guard) | — |
| F-BNK-API-08 | POST | /import/preview | FN-11 (preview + IN_FILE_DUPLICATE) | — |
| F-BNK-API-09 | POST | /import/commit | FN-12 (commit merge-only) | — |
| F-BNK-API-10 | GET | /export | FN-13 (export) | — |
| F-BNK-API-11 | GET | /active | FN-13b (picker) | — |
| (FE form + save) | — | picker กลุ่ม GL | FN-14 (consume F-PG API-01) | — |

### Trace Verification (Self-Check)
- [x] Every mutation API (02,04,05,06,07,09) has ≥ 1 Function ✅
- [x] No orphan Function — FN-01..14 (รวม FN-13b) ทุกตัวปรากฏใน trace ✅
- [x] No orphan Engine — ไม่มี engine (§3.2 ว่างโดยตั้งใจ) ✅
- [x] No hidden logic in 02_API — validation ทั้งหมดอยู่ FN-03; IR-BNK-01 guard ที่ FN-02; ★ per-side ที่ FN-08 ✅

---

## §3.4 Dependencies (Cross-feature / Backend Hooks)

### External Function/Engine called (Bank Master เรียกออก)
- **F-PG generic API-01** `GET /api/v1/gl/posting-groups?kind=bank&status=active` — ผ่าน F-BNK-FN-14. **3 drifts** (§2.6, OQ-BNK-06).

### External Engine ที่ทำงานนอก scope (ประกาศ contract, ไม่ implement ที่นี่)
| Hook | หน้าที่ | Owner | สถานะ |
|---|---|---|---|
| GL-Resolve | resolve บัญชีเงินฝาก (COA) ผ่าน posting group `account_1` ตอน post | external GL / Journal Engine | out of scope (contract §2.7) |
| used-Increment | เพิ่ม `used` เมื่อ Receipt/PV post ผ่านบัญชี | external GL engine + Receipt/PV | out of scope · **นิยาม = OQ-BNK-07** (AD-BNK-01: นับเฉพาะ posted) |
| Receipt/PV picker+snapshot | เลือกบัญชี active+ฝั่งตรง → snapshot | Receipt/PV feature (ยังไม่ทำ) | consume F-BNK-API-11 (OQ-BNK-04) |

### External Function/Engine that calls into this feature
- Receipt / Payment Voucher → F-BNK-FN-13b (via GET /active?side=)

---

## §3.5 Open Questions / Locked Decisions Referenced
- **OQ-BNK-06:** posting_group source = generic F-PG-API-01 (3 drifts) — DEV ห้ามลอก mock local list (กระทบ FN-14)
- **OQ-BNK-07:** นิยาม `used` (นับ draft ปลายทางด้วยไหม / เฉพาะ posted) — กระทบ FN-07 delete guard + FN-02 IR lock trigger · `[AD-BNK-01]` นับเฉพาะ posted
- **AD-BNK-02:** optimistic-lock + idempotency = conservative default (Phase 2.5 probe PR-1/PR-7) — OQ-BNK-CC-01
- **IR-BNK-01 (LOCK):** FN-02 ล็อกเฉพาะ `bank`+`account_no` เมื่อ used>0 (ไม่ล็อกทั้งใบ) — OQ-BNK-03 CONFIRMED

---

## Audience Cheat-Sheet
| Reader | Read sections |
|---|---|
| BE dev | §3.1 + §3.3 |
| QA | §3.3 + FN Side effects |
| Architect / Integration | §3.4 (GL resolve external + F-PG API-01) + §3.5 |
| PM | §3.3 (table) |

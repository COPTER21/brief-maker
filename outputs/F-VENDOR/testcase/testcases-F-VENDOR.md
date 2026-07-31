# AI Test Cases — F-VENDOR ทะเบียนคู่ค้า

เอกสาร Markdown สำหรับ AI agent (browser-use/vision + API/integration runner) ใช้ทดสอบระบบจริงตาม FRD Pack v1.1 และ HTML ที่อนุมัติแล้ว ทุก action อ้าง route หรือข้อความที่มองเห็นจริงใน `vendor.html`; รายการที่ prototype ยังไม่มี UI จะระบุ `(ต้อง simulate)` และ `⚠ ไม่พบใน HTML` อย่างชัดเจน

## Meta

| Field | Value |
|---|---|
| Feature ID | F-VENDOR |
| ชื่อ | Vendor Master / ทะเบียนคู่ค้า |
| เวอร์ชัน Test Case | 1.0 · 2026-07-31 |
| App entry | `outputs/F-VENDOR/vendor.html` |
| Routes | `#/vendors` เท่านั้น; view/create/edit เป็น drawer และ action เป็น modal |
| FRD | `outputs/F-VENDOR/FRD_F-VENDOR_Pack/` v1.1 |
| BRD | `Related context/vendor/Vendor/BRD_vendor_master.md` v1.1 (historical intent; Locked Decisions ชนะเมื่อขัดกัน) |
| HTML source | `outputs/F-VENDOR/vendor.html` · 1,541 lines |
| UI extraction | `outputs/F-VENDOR/UI_BRIEF_F-VENDOR.md` v1.1 |
| Microcopy source | `.agents/skills/html-generator-v6/knowledge/microcopy.md` v3.13 + HTML จริง |
| จำนวนเคส | 91 เคส / 11 กลุ่ม |
| Scope | เอกสารทดสอบ feature Vendor; ไม่มี codebase และไม่ทดสอบ Price List CRUD, PO/PV creation, PDF, bulk import/export, merge หรือ portal |
| AI-DEFAULT | เคสที่มาจาก conservative default ติด `[AI-DEFAULT]` ที่หัวเคส |

### Source drift note

- HTML เป็น authority ของ route, visible action และข้อความที่มองเห็น
- FRD เป็น authority ของ backend/security/integration behavior
- KYC fail โดยไม่พบ sanctions: HTML, UI, API, Logic, Rules และ Tests ตรงกันแล้วว่า `kyc=failed` และ vendor คง/กลับ `pending_kyc`
- HTML prototype ยังไม่มี loading/error/retry, server conflict, RLS, file scan, private storage, event bus และหน้าปลายทาง PO/PV; เคสเหล่านี้ต้องรันกับ implementation หรือ environment ที่ inject failure ได้

## Coverage

| Group | Cases | ความสำคัญ |
|---|---:|---|
| L — List, route, search/filter/sort/page | 10 | สูง 8 · กลาง 2 |
| C — Create/Edit wizard, validation, collections | 18 | สูง 17 · กลาง 1 |
| K — KYC and sanctions | 7 | สูง 7 |
| A — Approval, Policy Center, reject/resubmit | 9 | สูง 9 |
| B — Bank verification/deactivation | 7 | สูง 7 |
| S — Availability, inactive, blacklist | 8 | สูง 8 |
| P — Permission, masking, tenant isolation | 9 | สูง 9 |
| F — Attachment security and retention | 5 | สูง 4 · กลาง 1 |
| R — Concurrency, idempotency, audit, reliability | 7 | สูง 6 · กลาง 1 |
| X — Cross-module contracts | 6 | สูง 5 · กลาง 1 |
| LK — Scope Lock / handoff verification | 5 | สูง 5 |
| **รวม** | **91** | **สูง 85 · กลาง 6** |

## Coverage Ledger

### Acceptance / FR (06_TESTS)

| item | cases |
|---|---|
| AC-01 List/search/filter | TC-L01..TC-L10, TC-P01..TC-P04, TC-P09 |
| AC-02 Create draft/idempotent | TC-C01, TC-R03 `[AI-DEFAULT]` |
| AC-03 Invalid/duplicate tax | TC-C03, TC-C04 |
| AC-04 OT without tax | TC-C05, TC-A06 |
| AC-05 Address/bank collection safety | TC-C09..TC-C13 |
| AC-06 Submit KYC | TC-C02, TC-C06 |
| AC-07 Normal KYC pass/fail | TC-K01..TC-K03 |
| AC-08 Sanctions hit | TC-K04, TC-K05 |
| AC-09 Approval readiness/Policy | TC-A01..TC-A06 |
| AC-10 Multi-step/SoD | TC-A07, TC-A08, TC-R02 |
| AC-11 Reject/resubmit | TC-A09 |
| AC-12 Bank verification | TC-B01..TC-B07 |
| AC-13 Block/unblock/inactive | TC-S01..TC-S05 |
| AC-14 Blacklist terminal | TC-S06, TC-S07 |
| AC-15 Masking/tenant | TC-P01..TC-P05, TC-P09 |
| AC-16 Tax immutable | TC-C14 |
| AC-17 Attachment security | TC-F01..TC-F05 |
| AC-18 Concurrency/retry | TC-R01..TC-R05 |
| AC-19 Audit atomicity | TC-R06 |
| AC-20 Dependency failure | TC-A05, TC-X06 |
| UI §1.10 Accessibility | TC-C16, TC-L01 |
| Security §5.7 XSS | TC-C18 |
| Performance §6.6 | TC-R07 |

### Business Rules (05_RULES)

| rule | cases |
|---|---|
| BR-VEN-01 TH tax 13 digits/checksum | TC-C03 |
| BR-VEN-02 tax unique tenant+country | TC-C04, TC-P09 |
| BR-VEN-03 OT tax optional | TC-C05 |
| BR-VEN-04 server vendor code/non-reuse | TC-C01, TC-C06 |
| BR-VEN-05 legal name required/1..255 | TC-C01, TC-C03 |
| BR-VEN-06 bank number 10..15/immutable | TC-C12, TC-C13, TC-B03 |
| BR-VEN-07 non-OT verified bank gate | TC-A04, TC-B01, TC-X03 |
| BR-VEN-08 valid contact gate | TC-C08, TC-A03 |
| BR-VEN-09 credit≥0/WHT 0..30 | TC-C07 |
| BR-VEN-10 KYC passed before approval | TC-A02 |
| BR-VEN-11 sanctions blocks | TC-K04, TC-K05 |
| BR-VEN-12 tax immutable after KYC | TC-C14 |
| BR-VEN-13 Compliance/Admin KYC | TC-K06, TC-P07 |
| BR-VEN-14 KYC review scope | TC-K01, TC-K04 |
| BR-VEN-15 maker≠approver | TC-A08 |
| BR-VEN-16 current Policy role | TC-A07, TC-A08 |
| BR-VEN-17 Policy chain all types/no local threshold | TC-A01, TC-A05, TC-A06 |
| BR-VEN-18 classification/masking | TC-P02..TC-P05 |
| BR-VEN-19 reject reason/close round | TC-A09 |
| BR-VEN-20 blacklist terminal | TC-S06, TC-S07 |
| BR-VEN-21 editable states | TC-C14, TC-S08 |
| BR-VEN-22 reason required | TC-A09, TC-B04, TC-S02, TC-S03, TC-S05, TC-S06 |
| BR-VEN-23 soft-disable/no cascade | TC-C11, TC-B04, TC-F05, TC-S08 |
| BR-VEN-24 exactly one billing/shipping | TC-C09 |
| BR-VEN-25 designated address replacement explicit | TC-C10 |
| BR-VEN-26 verified bank read-only/new row | TC-C13, TC-B03, TC-B07 |
| BR-VEN-27 PO active+KYC | TC-X02, TC-X04 |
| BR-VEN-28 block/blacklist/inactive preserve history | TC-S08, TC-X04 |
| BR-VEN-29 tenant audit | TC-P09, TC-R06 |
| BR-VEN-30 audit failure rollback `[AI-DEFAULT]` | TC-R06 `[AI-DEFAULT]` |

### Edge Cases and Activated Probes

| item | cases / สถานะ |
|---|---|
| EC-VEN-01 duplicate tax | TC-C04 |
| EC-VEN-02 OT no tax | TC-C05 |
| EC-VEN-03 approval before KYC | TC-A02 |
| EC-VEN-04 approval no valid contact | TC-A03 |
| EC-VEN-05 approval no verified bank | TC-A04 |
| EC-VEN-06 maker self-approve | TC-A08 |
| EC-VEN-07 wrong role | TC-A08 |
| EC-VEN-08 sanctions | TC-K04, TC-K05 |
| EC-VEN-09 tax edit after KYC | TC-C14 |
| EC-VEN-10 reject after partial approval | TC-A09 |
| EC-VEN-11 block referenced vendor | TC-S08 |
| EC-VEN-12 leave blacklist | TC-S07 |
| EC-VEN-13 last verified bank | TC-B05, TC-X03 |
| PR-1 concurrent approval `[AI-DEFAULT]` | TC-R02 `[AI-DEFAULT]` |
| PR-2 stale edit `[AI-DEFAULT]` | TC-R01 `[AI-DEFAULT]` |
| PR-3 permission revoked | TC-R05 |
| PR-4 lost response/retry + 24h cache | TC-R03 `[AI-DEFAULT]` |
| PR-6 close unsaved wizard `[AI-DEFAULT]` | TC-C16 `[AI-DEFAULT]` |
| PR-7 double-click submit | TC-R03 |
| Policy Center timeout/no fallback | TC-A05 |
| sanctions provider timeout `[AI-DEFAULT]` | TC-K07 `[AI-DEFAULT]` |
| address role removed | TC-C10 |
| cross-tenant ID | TC-P09 |
| audit/outbox failure | TC-R06 |
| attachment scan failure | TC-F03 |

### Error Codes

| error | cases |
|---|---|
| ERR_VALIDATION_FAILED | TC-C03, TC-C07, TC-C08 |
| ERR_NOT_AUTHENTICATED | TC-P01 |
| ERR_INSUFFICIENT_ROLE | TC-P06..TC-P08, TC-B02, TC-K06 |
| ERR_PERMISSION_REVOKED | TC-R05 |
| ERR_VENDOR_NOT_FOUND | TC-P09, TC-S08 |
| ERR_ATTACHMENT_NOT_FOUND | TC-F05 |
| ERR_STALE_DATA | TC-R01, TC-R02 |
| ERR_IDEMPOTENCY_CONFLICT | TC-R04 |
| BR_DUPLICATE_TAX_ID | TC-C04 |
| ERR_POLICY_UNAVAILABLE | TC-A05 |
| ERR_REFERENCE_DATA_UNAVAILABLE | TC-L09 |
| ERR_PRICE_LIST_UNAVAILABLE | TC-X06 |
| BR_VENDOR_NAME_REQUIRED | TC-C03 |
| BR_VENDOR_TYPE_INVALID | TC-C03 `(ต้อง simulate API)` |
| BR_TAX_ID_INVALID | TC-C03 |
| BR_TAX_ID_IMMUTABLE | TC-C14 |
| BR_KYC_NOT_PASSED | TC-A02 |
| BR_SANCTIONS_HIT_CANNOT_PASS | TC-K04 |
| BR_KYC_SOURCE_REQUIRED | TC-K05 |
| BR_KYC_NOTE_REQUIRED | TC-K02, TC-K05 |
| BR_CONTACT_REQUIRED | TC-A03 |
| BR_VERIFIED_BANK_REQUIRED | TC-A04 |
| BR_ADDRESS_ROLE_REQUIRED | TC-C10 |
| BR_SOD_VIOLATION | TC-A08 |
| BR_WRONG_APPROVER | TC-A08 |
| BR_REASON_REQUIRED | TC-A09, TC-B04, TC-S02, TC-S03, TC-S05, TC-S06 |
| BR_INVALID_STATE_TRANSITION | TC-S07, TC-S08 |
| BR_BLACKLIST_TERMINAL | TC-S07 |
| BR_BANK_STATE_INVALID | TC-B06, TC-B07 |
| ERR_FILE_TYPE_NOT_ALLOWED | TC-F02 |
| ERR_FILE_REJECTED | TC-F03 |
| ERR_DUPLICATE_ATTACHMENT | TC-F04 |
| ENG_ERR_INVALID_INPUT | TC-R07 `(ต้อง simulate engine contract)` |
| ERR_FIELD_ACCESS_DENIED (03_LOGIC) | TC-P02, TC-P04 |
| BR_VENDOR_NOT_EDITABLE (03_LOGIC) | TC-S08 |
| BR_VENDOR_NOT_READY (02_API/FN-08) | TC-A02..TC-A04 |
| BR_ATTACHMENT_LOCKED (03_LOGIC) | TC-F05 `(ต้อง simulate)` |

### Validation Schema

| field/constraint | cases |
|---|---|
| legal_name required/trim/1..255 | TC-C01, TC-C03 |
| vendor_type 11 enums | TC-L04, TC-C03 |
| country_code active FK | TC-C15 |
| tax_id conditional/checksum | TC-C03, TC-C05 |
| tax_id unique | TC-C04 |
| branch_code conditional | TC-C03 |
| payment term active FK | TC-C15 |
| credit_limit numeric ≥0 | TC-C07 |
| WHT 0..30 | TC-C07 |
| contact name/email/phone readiness | TC-C08, TC-A03 |
| address required + exactly-one roles | TC-C08..TC-C10 |
| bank 10..15 digits + required refs/name | TC-C12 |
| attachment allowlist/size/scan | TC-F01..TC-F04 |
| reason non-blank/trimmed | TC-A09, TC-B04, TC-S02, TC-S03, TC-S05, TC-S06 |

### Permission Matrix — ทุก cell

คำย่อ role: O=Officer, M=Manager, D=Director, C=Compliance, F=Finance, A=Admin, V=Viewer

| capability × role | expected | cases |
|---|---|---|
| View O | allow | TC-P01 |
| View M | allow | TC-P01 |
| View D | allow | TC-P01 |
| View C | allow | TC-P01 |
| View F | allow | TC-P01 |
| View A | allow | TC-P01 |
| View V | allow/masked | TC-P01, TC-P02 |
| Create/edit/submit KYC O | allow | TC-C01, TC-C02 |
| Create/edit/submit KYC M | deny | TC-P06 |
| Create/edit/submit KYC D | deny | TC-P06 |
| Create/edit/submit KYC C | deny | TC-P06 |
| Create/edit/submit KYC F | deny | TC-P06 |
| Create/edit/submit KYC A | allow | TC-P06 |
| Create/edit/submit KYC V | deny | TC-P06 |
| KYC decision O | deny | TC-K06 |
| KYC decision M | deny | TC-K06 |
| KYC decision D | deny | TC-K06 |
| KYC decision C | allow | TC-K01 |
| KYC decision F | deny | TC-K06 |
| KYC decision A | allow | TC-P07 |
| KYC decision V | deny | TC-K06 |
| Submit approval O | allow | TC-A01 |
| Submit approval M | deny | TC-P06 |
| Submit approval D | deny | TC-P06 |
| Submit approval C | deny | TC-P06 |
| Submit approval F | deny | TC-P06 |
| Submit approval A | allow | TC-P06 |
| Submit approval V | deny | TC-P06 |
| Approve current O | Policy role only | TC-A07, TC-A08 |
| Approve current M | Policy role only | TC-A07, TC-A08 |
| Approve current D | Policy role/explicit override | TC-A07, TC-A08 |
| Approve current C | deny | TC-P07 |
| Approve current F | deny | TC-P07 |
| Approve current A | explicit Policy override only | TC-A08 |
| Approve current V | deny | TC-P07 |
| Block/unblock/deactivate O | allow | TC-S01..TC-S05 |
| Block/unblock/deactivate M | allow | TC-P08 |
| Block/unblock/deactivate D | allow | TC-P08 |
| Block/unblock/deactivate C | deny | TC-P08 |
| Block/unblock/deactivate F | deny | TC-P08 |
| Block/unblock/deactivate A | allow | TC-P08 |
| Block/unblock/deactivate V | deny | TC-P08 |
| Blacklist O | deny | TC-P08 |
| Blacklist M | deny | TC-P08 |
| Blacklist D | allow | TC-S06 |
| Blacklist C | deny | TC-P08 |
| Blacklist F | deny | TC-P08 |
| Blacklist A | allow | TC-S06 |
| Blacklist V | deny | TC-P08 |
| Bank/full account O | deny/masked | TC-P04 |
| Bank/full account M | deny/masked | TC-P04 |
| Bank/full account D | deny/masked | TC-P04 |
| Bank/full account C | deny/masked | TC-P04 |
| Bank/full account F | allow | TC-B01, TC-P04 |
| Bank/full account A | allow | TC-P04 |
| Bank/full account V | deny/masked | TC-P04 |
| Full tax O | deny/masked | TC-P02 |
| Full tax M | deny/masked | TC-P02 |
| Full tax D | deny/masked | TC-P02 |
| Full tax C | allow | TC-P03 |
| Full tax F | allow | TC-P03 |
| Full tax A | allow | TC-P03 |
| Full tax V | deny/masked | TC-P02 |
| Full credit O | deny/masked | TC-P05 |
| Full credit M | deny/masked | TC-P05 |
| Full credit D | deny/masked | TC-P05 |
| Full credit C | deny/masked | TC-P05 |
| Full credit F | allow | TC-P05 |
| Full credit A | allow | TC-P05 |
| Full credit V | deny/masked | TC-P05 |

### Cross-Module (XT)

| XT | Downstream | Case |
|---|---|---|
| XT-01 Price List summary | F-VENDOR-PRICE-LIST / E-002 | TC-X01 |
| XT-02 PO vendor selection | F-PO / E-007 | TC-X02 |
| XT-03 last bank deactivated | Payment/PV | TC-X03 |
| XT-04 availability change | PO/PV | TC-X04 |
| XT-05 duplicate/out-of-order events `[AI-DEFAULT]` | all consumers | TC-X05 `[AI-DEFAULT]` |
| XT-06 Price List unavailable | Vendor UI | TC-X06 |

### Scope Lock (LOCK)

| LOCK | ข้อยืนยัน | Case verify |
|---|---|---|
| LOCK-01 | ไม่มี Scope Lock เพิ่มเติม | TC-LK01 |
| LOCK-02 | BRD v1.1 เป็นฐานและ LD supersede drift | TC-LK02 |
| LOCK-03 | HTML ล่าสุดเป็น UI source of truth | TC-LK03 |
| LOCK-04 | เอกสารเท่านั้น ไม่มี implementation/codebase | TC-LK04 |
| LOCK-05 | ห้ามใช้ plan-from-spec | TC-LK05 |

### Coverage Manifest Cross-check (00_OVERVIEW §0.12)

| Manifest row | Ledger pair / cases |
|---|---|
| US-01 | AC-02 / TC-C01, TC-C02 |
| US-02 | AC-06 / TC-C02 |
| US-03 | AC-07/08 / TC-K01..TC-K05 |
| US-04 | AC-09 / TC-A01..TC-A06 |
| US-05 | AC-10 / TC-A07, TC-A08 |
| US-06 | AC-11 / TC-A09 |
| US-07 | AC-12 / TC-B01..TC-B07 |
| US-08 | AC-13 / TC-S01..TC-S04 |
| US-09 | AC-14 / TC-S06, TC-S07 |
| US-10 | AC-15 / TC-P01..TC-P05, TC-P09 |
| US-11 | XT-01 / TC-X01 |
| BR-V01 | BR-VEN-01 / TC-C03 |
| BR-V02 | BR-VEN-02 / TC-C04 |
| BR-V03 | BR-VEN-03 / TC-C05 |
| BR-V04 | BR-VEN-04 / TC-C01, TC-C06 |
| BR-V05 | BR-VEN-05 / TC-C01, TC-C03 |
| BR-V06 | BR-VEN-06 / TC-C12, TC-C13 |
| BR-V07 | BR-VEN-07 / TC-A04, TC-X03 |
| BR-V08 | BR-VEN-08 / TC-C08, TC-A03 |
| BR-V09 | BR-VEN-09 / TC-C07 |
| BR-K01 | BR-VEN-10 / TC-A02 |
| BR-K02 | BR-VEN-11 / TC-K04, TC-K05 |
| BR-K03 | BR-VEN-12 / TC-C14 |
| BR-K04 | BR-VEN-13 / TC-K06 |
| BR-K05 | BR-VEN-14 / TC-K01, TC-K04 |
| BR-A01 | BR-VEN-15 / TC-A08 |
| BR-A02 | BR-VEN-16 / TC-A07, TC-A08 |
| BR-A03 | BR-VEN-17 / TC-A01, TC-A05 |
| BR-A04 | BR-VEN-17 + LD-03 / TC-A06 |
| BR-A05 | BR-VEN-19 / TC-A09 |
| BR-M01 | BR-VEN-18 / TC-P02, TC-P03 |
| BR-M02 | BR-VEN-18 / TC-P04 |
| BR-M03 | BR-VEN-18 / TC-P02, TC-P04 |
| BR-L01 | BR-VEN-20 / TC-S06, TC-S07 |
| BR-L02 | BR-VEN-21 / TC-C14, TC-S08 |
| BR-L03 | BR-VEN-22 / TC-A09, TC-B04, TC-S02, TC-S03, TC-S05, TC-S06 |
| BR-L04 | BR-VEN-23 / TC-C11, TC-S08 |
| EC-01 | EC-VEN-01 / TC-C04 |
| EC-02 | EC-VEN-02 / TC-C05 |
| EC-03 | EC-VEN-03 / TC-A02 |
| EC-04 | EC-VEN-04 / TC-A03 |
| EC-05 | EC-VEN-05 / TC-A04 |
| EC-06 | EC-VEN-06 / TC-A08 |
| EC-07 | EC-VEN-07 / TC-A08 |
| EC-08 | EC-VEN-08 / TC-K04, TC-K05 |
| EC-09 | EC-VEN-09 / TC-C14 |
| EC-10 | EC-VEN-10 / TC-A09 |
| EC-11 | EC-VEN-11 / TC-S08 |
| EC-12 | EC-VEN-12 / TC-S07 |
| EC-13 | EC-VEN-13 / TC-B05, TC-X03 |

### Cross-cutting / Events / States

| item | cases |
|---|---|
| UI loaded/empty/filtered-empty/loading/error/read-only | TC-L01, TC-L03, TC-L08, TC-L09, TC-P01 |
| Vendor states 7 labels | TC-L05 |
| draft→draft / draft→pending_kyc | TC-C01, TC-C02 |
| pending_kyc→pending_approval | TC-A01 |
| pending_approval→pending_approval/active/pending_kyc | TC-A07, TC-A09 |
| pending_kyc→blocked sanctions | TC-K05 |
| active→blocked / blocked→active | TC-S01, TC-S04 |
| non-terminal→inactive | TC-S05 |
| allowed→blacklisted / terminal reject | TC-S06, TC-S07 |
| KYC pending/passed/failed/expired/resubmit | TC-K01..TC-K07 |
| Bank unverified/pending/verified/disabled + forbidden transitions | TC-B01..TC-B07 |
| vendor_created_event | TC-C01, TC-R03 `[AI-DEFAULT]` |
| vendor_kyc_submitted_event | TC-C02 |
| vendor_kyc_decided_event | TC-K01, TC-K03, TC-K05 |
| vendor_approval_submitted_event | TC-A01 |
| vendor_approval_decided_event | TC-A07, TC-A09 |
| vendor_status_changed_event | TC-S01, TC-S04..TC-S06, TC-X04 |
| vendor_payment_eligibility_changed_event | TC-B05, TC-X03 |
| at-least-once/dedup/version `[AI-DEFAULT]` | TC-X05 `[AI-DEFAULT]` |
| RLS/tenant anti-enumeration | TC-P09 |
| encryption/masking/sensitive-view audit | TC-P02..TC-P05 |
| private file/scan/retention | TC-F01..TC-F05 |
| WORM audit/atomic rollback `[AI-DEFAULT]` | TC-R06 `[AI-DEFAULT]` |
| performance/SLO `[AI-DEFAULT]` | TC-R07 `[AI-DEFAULT]` |

### Ledger-first Gate

- Planned cases: **91**
- Ledger rows without case: **0**
- In-scope rows marked skip: **0**
- Out of scope recorded below and intentionally has no test case
- Manifest rows paired: **50/50**
- Gate status: **✅ PASS — เริ่มเขียน Test Cases ได้**

### Out of Scope / ไม่สร้างเคส

| Item | เหตุผล |
|---|---|
| Price List CRUD | อยู่ F-VENDOR-PRICE-LIST |
| PO/PV creation or payment execution | Vendor ให้ eligibility contract เท่านั้น |
| PDF A4 output | LOCK/LD-11 ระบุไม่มี artifact |
| Bulk import/export | Phase 2 / Out of Scope |
| Vendor merge/split | Phase 2 |
| Vendor portal | Phase 3+ |
| Performance scoring | separate feature |
| KYC expiry transition | OQ-02 ยังไม่มี policy; ห้าม auto-expire |
| Production sanctions provider/SLA | OQ-01 |
| Attachment exact size/type/retention | OQ-04; ทดสอบผ่าน environment policy โดยไม่ hardcode limit |

## Data Sets

### ชุด A — Corporate valid

| ฟิลด์ | ค่า |
|---|---|
| ประเภทคู่ค้า | `TR — Trading / Reseller` |
| ประเทศ/สกุลเงิน | `TH` / `THB` |
| ชื่อตามกฎหมาย | `บริษัท ทดสอบเวนเดอร์ 2569 จำกัด` |
| ชื่อย่อ | `ทดสอบเวนเดอร์` |
| เลขประจำตัวผู้เสียภาษี | `0105556102367` (13 หลัก checksum ถูกต้อง) |
| VAT/สาขา | จด VAT / สำนักงานใหญ่ |
| ผู้ติดต่อ | `สมชาย ทดสอบ` / `vendor.qa@example.com` / `0812345678` |
| ที่อยู่ | `สำนักงานใหญ่`, `99 ถนนสุขุมวิท`, กรุงเทพมหานคร, เขตคลองเตย, แขวงคลองตัน, `10110` |
| บทบาทที่อยู่ | ที่อยู่ใบกำกับ=true, ที่อยู่จัดส่งหลัก=true |
| ธนาคาร | KBANK / `0123456789` / `บริษัท ทดสอบเวนเดอร์ 2569 จำกัด` / payment / THB |
| เงื่อนไขชำระ | NET30 |
| WHT / วงเงิน | 3% / 100,000.00 |

### ชุด B — One-time valid without tax/bank

| ฟิลด์ | ค่า |
|---|---|
| ประเภทคู่ค้า | `OT — One-time` |
| ชื่อตามกฎหมาย | `นายทดสอบ ครั้งเดียว` |
| Tax ID | ว่าง |
| ผู้ติดต่อ | `นายทดสอบ` / `onetime.qa@example.com` / `0899999999` |
| ที่อยู่ | `ที่อยู่ชั่วคราว`, `88 ถนนทดสอบ`, กรุงเทพมหานคร, เขตบางรัก, แขวงสีลม, `10500` |
| ธนาคาร | ไม่มี |
| เงื่อนไขชำระ | COD |

### ชุด C — Invalid and boundary

| ชื่อค่า | ค่า |
|---|---|
| tax สั้น | `123456789012` |
| tax checksum ผิด | `0105556102368` |
| tax ซ้ำ | tax ID ของ seed vendor tenant A |
| bank 9 หลัก | `123456789` |
| bank 16 หลัก | `1234567890123456` |
| email ผิด | `vendor@@example` |
| phone ว่าง | ว่าง |
| credit ติดลบ | `-0.01` |
| WHT ต่ำ/สูง | `-0.01` / `30.01` |
| legal_name 256 ตัว | runner เตรียมข้อความ `ก` จำนวน 256 ตัว |
| reason blank | `   ` |
| XSS text | `<img src=x onerror=alert('VEN-XSS')>` |

### ชุด D — Seed fixtures

| Seed | รายละเอียด |
|---|---|
| D-DRAFT | vendor `draft`, maker=officer-A |
| D-KYC | vendor `pending_kyc`, KYC pending, มี contact/address/bank ครบ |
| D-KYC-PASS | vendor `pending_kyc`, KYC passed, non-OT, contact/address/verified bank ครบ |
| D-APPROVAL | vendor `pending_approval`, chain Manager→Director, maker=officer-A, current=Manager |
| D-PARTIAL | vendor `pending_approval`, step Manager approved, current=Director |
| D-ACTIVE | vendor `active`, KYC passed, มี transaction history และ verified bank 1 บัญชี |
| D-BLOCKED-VALID | vendor `blocked`, KYC passed, Policy valid |
| D-BLOCKED-INVALID | vendor `blocked`, KYC failedหรือ Policy invalid |
| D-INACTIVE | vendor `inactive` |
| D-BLACKLIST | vendor `blacklisted` |
| D-TENANT-B | vendor ชื่อเหมือน D-ACTIVE แต่ tenant B และ id แยก |

### ไฟล์ทดสอบ (Files)

| ชื่อไฟล์ | ใช้ในเคส | คุณสมบัติ |
|---|---|---|
| `vendor-clean.pdf` | TC-F01, TC-F04 | PDF สะอาดและอยู่ใน allowlist ของ environment |
| `vendor-clean-copy.pdf` | TC-F04 | เนื้อหา/checksum เดียวกับ `vendor-clean.pdf` |
| `vendor-disallowed.exe` | TC-F02 | ชนิดต้องห้าม |
| `vendor-oversize.pdf` | TC-F03 | ใหญ่กว่า limit ที่ environment กำหนด |
| `vendor-eicar.txt` | TC-F03 | EICAR/malware-test fixture ที่ scanner ของ test environment รองรับ |
| `vendor-xss-name.pdf` | TC-C18 | metadata filename ถูก inject เป็น `<img src=x onerror=alert('VEN-XSS')>.pdf` ใน test fixture |

> OQ-04 ยังไม่ล็อกตัวเลขขนาด/allowlist: runner ต้องอ่าน policy ของ environment ก่อนสร้าง `vendor-oversize.pdf`; ห้ามใช้ production PII หรือบัญชีจริง

## Test Cases

### Group L — List, Route, Search, Filter, Sort and Pagination

### TC-L01 — เปิด route หลักและตรวจ loaded state (happy)
- group: รายการคู่ค้า · ความสำคัญ: สูง · trace: AC-01 / UI-01 / LOCK-03
- actor (role): Viewer
- Setup: role=viewer · seed=มี vendor อย่างน้อย 14 รายหลายสถานะ · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: D
- ผ่านเมื่อ: route คง `#/vendors`, เห็น title/subtitle/table/count และไม่มี mutation action

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/vendors` | — | เห็นหัวข้อ **ทะเบียนคู่ค้า** และข้อความ **จัดการข้อมูลคู่ค้า เอกสาร และสถานะการใช้งานในที่เดียว** | ☐ |
| 2 | VERIFY breadcrumb และ sidebar | — | เห็น **Master Data**, **Vendor Master** และเมนู Vendor Master เป็นรายการที่ active | ☐ |
| 3 | VERIFY ตารางรายการ | — | เห็นคอลัมน์ **คู่ค้า**, **ประเภท**, **เลขภาษี**, **สถานะ** และจำนวนรายการ | ☐ |
| 4 | VERIFY action ด้านบน | — | ไม่เห็นปุ่ม **เพิ่มคู่ค้า**; เห็นข้อความ **โหมดอ่านอย่างเดียว (Viewer)** | ☐ |
| 5 | PRESS Ctrl+R | — | หลัง refresh route ยังเป็น `#/vendors` และรายการกลับมาแสดง | ☐ |

### TC-L02 — ค้นหาด้วยรหัส ชื่อ และเลขภาษี (happy)
- group: รายการคู่ค้า · ความสำคัญ: สูง · trace: AC-01 / API-01
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=มี D-ACTIVE และทราบ code/name/tax masked · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: D-ACTIVE
- ผ่านเมื่อ: แต่ละคำค้นคืนเฉพาะรายการที่ตรงและ count/range สอดคล้อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/vendors` | — | เห็นช่อง **ค้นหา รหัส / ชื่อ / เลขภาษี...** | ☐ |
| 2 | TYPE รหัส vendor → ช่องค้นหา | code ของ D-ACTIVE | ตารางเหลือแถวที่มี code ตรงกันและ range แสดงจำนวนเดียวกัน | ☐ |
| 3 | TYPE ชื่อตามกฎหมาย → ช่องค้นหา | name ของ D-ACTIVE | เห็นแถว D-ACTIVE และไม่เห็นแถวชื่อไม่ตรง | ☐ |
| 4 | TYPE เลขภาษีส่วนที่มองเห็น → ช่องค้นหา | ค่าที่อนุญาตให้ role นี้เห็น | เห็น D-ACTIVE โดยไม่เปิดเผยเลขเต็มเกิน field policy | ☐ |

### TC-L03 — ค้นหาไม่พบและรีเซ็ต (negative)
- group: รายการคู่ค้า · ความสำคัญ: สูง · trace: AC-01 / UI filtered-empty
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=มี vendor อย่างน้อย 1 ราย · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: คำค้น `NO-SUCH-VENDOR-2569`
- ผ่านเมื่อ: แสดง filtered-empty และปุ่ม/คำสั่งรีเซ็ตคืนรายการทั้งหมด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `NO-SUCH-VENDOR-2569` → ช่อง **ค้นหา รหัส / ชื่อ / เลขภาษี...** | — | เห็น **ไม่พบคู่ค้า** และ **ลองปรับตัวกรอง หรือเพิ่มคู่ค้าใหม่** | ☐ |
| 2 | CLICK **รีเซ็ต** | — | คำค้นและตัวกรองกลับค่าเริ่มต้น; toast **รีเซ็ตตัวกรองแล้ว** ปรากฏ | ☐ |
| 3 | WAIT จนรายการกลับมา | ≤3s | ตารางแสดงรายการเดิมและ empty state หายไป | ☐ |

### TC-L04 — กรองครบ 11 ประเภท (enumeration)
- group: รายการคู่ค้า · ความสำคัญ: สูง · trace: AC-01 / BR-VEN-03 / validation vendor_type
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=มีอย่างน้อย 1 vendor ต่อประเภท RM, TR, SV, MN, CT, LG, SP, UT, GV, EM, OT · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: รายการประเภททั้ง 11
- ผ่านเมื่อ: ทุกค่ากรองแสดงเฉพาะ pill/รหัสประเภทนั้น และ **ทุกประเภท** คืนชุดรวม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ประเภททีละค่า → ตัวกรอง **ทุกประเภท** | RM, TR, SV, MN, CT, LG, SP, UT, GV, EM, OT | หลังเลือกแต่ละค่า ทุกแถวที่มองเห็นมีประเภทตรงค่าที่เลือก; count/range ตรงผลกรอง | ☐ |
| 2 | SELECT **ทุกประเภท** → ตัวกรองประเภท | — | เห็น vendor หลายประเภทและจำนวนกลับเป็นชุดรวม | ☐ |

### TC-L05 — กรองครบ 7 lifecycle states (enumeration)
- group: รายการคู่ค้า · ความสำคัญ: สูง · trace: AC-01 / BR-VEN-20/21 / state machine
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=มี vendor ต่อ state draft, pending_kyc, pending_approval, active, blocked, inactive, blacklisted · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: D-DRAFT, D-KYC, D-APPROVAL, D-ACTIVE, D-BLOCKED-VALID, D-INACTIVE, D-BLACKLIST
- ผ่านเมื่อ: ทุก filter แสดง label ที่ถูกต้องและไม่มี state นอกชุด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT สถานะทีละค่า → ตัวกรอง **ทุกสถานะ** | แบบร่าง, รอ KYC, รออนุมัติ, ใช้งาน, บล็อกชั่วคราว, ปิดใช้งาน, แบล็คลิสต์ | หลังเลือกแต่ละค่า ทุกแถวมีป้ายสถานะตรงค่าที่เลือก | ☐ |
| 2 | SELECT **ทุกสถานะ** → ตัวกรองสถานะ | — | เห็นหลายสถานะและจำนวนกลับเป็นชุดรวม | ☐ |

### TC-L06 — เรียงคู่ค้าและสถานะสองทิศ (happy)
- group: รายการคู่ค้า · ความสำคัญ: สูง · trace: AC-01 / API-01 sort
- actor (role): Viewer
- Setup: role=viewer · seed=มี vendor ≥3 รายชื่อ/code และสถานะต่างกัน · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: D
- ผ่านเมื่อ: คลิกหัวคอลัมน์แต่ละครั้งสลับ ascending/descending และลำดับแถวกลับทิศ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY และจดลำดับ 3 แถวแรก | — | บันทึกลำดับฐานเพื่อเทียบ step ถัดไป | ☐ |
| 2 | CLICK หัวคอลัมน์ **คู่ค้า** | — | ตัวบอกทิศเรียงเปลี่ยนและลำดับเรียงตามคู่ค้า ascending | ☐ |
| 3 | CLICK หัวคอลัมน์ **คู่ค้า** อีกครั้ง | — | ทิศเรียงกลับและลำดับแถวกลับจาก step 2 | ☐ |
| 4 | CLICK หัวคอลัมน์ **สถานะ** | — | ตารางเรียงตามสถานะและตัวบอกทิศอยู่ที่คอลัมน์สถานะ | ☐ |
| 5 | CLICK หัวคอลัมน์ **สถานะ** อีกครั้ง | — | ทิศเรียงสถานะกลับจาก step 4 | ☐ |

### TC-L07 — Page size และ pagination (boundary)
- group: รายการคู่ค้า · ความสำคัญ: สูง · trace: AC-01 / API-01 pagination
- actor (role): Viewer
- Setup: role=viewer · seed=มี vendor ≥55 ราย · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: page size 10, 20, 50
- ผ่านเมื่อ: จำนวนแถวไม่เกิน page size, range ถูก และเปลี่ยน filter แล้วกลับหน้า 1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT **10 / หน้า** | — | เห็นไม่เกิน 10 แถวและ range รูปแบบ `1 – 10 จาก {total} รายการ` | ☐ |
| 2 | CLICK ปุ่มหน้าถัดไป | — | range เริ่มที่ 11 และเลขหน้าปัจจุบันเปลี่ยน | ☐ |
| 3 | SELECT **20 / หน้า** | — | กลับหน้า 1 และเห็นไม่เกิน 20 แถว | ☐ |
| 4 | SELECT **50 / หน้า** | — | เห็นไม่เกิน 50 แถว; ปุ่มถัดไปยังใช้ได้เมื่อ total>50 | ☐ |
| 5 | SELECT สถานะ **ใช้งาน** | — | pagination กลับหน้า 1 และ range/count ตรงเฉพาะ active | ☐ |

### TC-L08 — Empty state เมื่อ tenant ไม่มี vendor (edge)
- group: รายการคู่ค้า · ความสำคัญ: กลาง · trace: AC-01 / UI empty
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=tenant ใหม่ไม่มี vendor · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น empty state ที่เข้าใจได้และยังสร้าง vendor ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/vendors` | — | เห็น **ไม่พบคู่ค้า** และ **ลองปรับตัวกรอง หรือเพิ่มคู่ค้าใหม่**; count เป็น 0 | ☐ |
| 2 | VERIFY primary action | — | เห็นปุ่ม **เพิ่มคู่ค้า** สำหรับ Procurement Officer | ☐ |

### TC-L09 — Loading และ reference/list error retry (ต้อง simulate)
- group: รายการคู่ค้า · ความสำคัญ: สูง · trace: UI-01 states / ERR_REFERENCE_DATA_UNAVAILABLE
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=inject list/refs latency แล้ว 503 ครั้งแรก, success ครั้งที่สอง · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: loading ไม่ทำ layout shift, error มีข้อความ/ลองใหม่, retry สำเร็จ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/vendors` | inject latency | ⚠ ไม่พบใน HTML prototype: implementation แสดง loading skeleton โดยโครงหน้าหลักไม่กระโดด | ☐ |
| 2 | WAIT จน request ล้มเหลว | 503 | ⚠ ไม่พบใน HTML prototype: เห็นข้อความเข้าใจได้และปุ่ม **ลองใหม่**; ไม่มีข้อมูลปลอม | ☐ |
| 3 | CLICK ปุ่ม **ลองใหม่** | backend กลับมาปกติ | ตารางโหลดสำเร็จและ error state หาย | ☐ |
| 4 | CLICK **เพิ่มคู่ค้า** | refs 503 | ⚠ ไม่พบใน HTML prototype: drawer ไม่แสดงค่าปลอมและบอกว่าโหลดข้อมูลอ้างอิงไม่ได้ | ☐ |

### TC-L10 — ค้นหาภาษาไทย/อักขระพิเศษโดยไม่เกิด XSS (security)
- group: รายการคู่ค้า · ความสำคัญ: กลาง · trace: AC-01 / §5.7 output escaping
- actor (role): Viewer
- Setup: role=viewer · seed=มีชื่อไทยและชื่อมีอักขระ `&` อย่างละ 1 ราย · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: `บริษัท`, `A&B`, `<script>alert(1)</script>`
- ผ่านเมื่อ: ค้นภาษาไทยและ `&` ได้; payload แสดงเป็น text/ไม่ execute

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `บริษัท` → ช่องค้นหา | — | เห็นเฉพาะแถวชื่อไทยที่ตรงและ UI ไม่ผิดรูป | ☐ |
| 2 | TYPE `A&B` → ช่องค้นหา | — | เห็นรายการที่มี `A&B` เป็นข้อความปกติ | ☐ |
| 3 | TYPE `<script>alert(1)</script>` → ช่องค้นหา | — | ไม่เกิด dialog/script; ผลเป็น **ไม่พบคู่ค้า** หรือผลที่ escape แล้ว | ☐ |

### Group C — Create/Edit Wizard, Validation and Collections

### TC-C01 — สร้าง draft ด้วยชื่อขั้นต่ำ (happy)
- group: สร้าง/แก้ไข · ความสำคัญ: สูง · trace: AC-02 / BR-VEN-04/05 / vendor_created_event
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=ไม่มี vendor ชื่อ `บริษัท Draft QA 2569 จำกัด` · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: legal_name=`บริษัท Draft QA 2569 จำกัด`
- ผ่านเมื่อ: สร้าง draft หนึ่งรายการ, code รูปแบบ `V-TH-{type}-NNNNN`, แสดงใน list

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **เพิ่มคู่ค้า** | — | drawer เปิด หัวข้อ **เพิ่มคู่ค้าใหม่** และ step **ข้อมูล & ภาษี** active | ☐ |
| 2 | TYPE `บริษัท Draft QA 2569 จำกัด` → ช่อง **ชื่อตามกฎหมาย** | — | ช่องแสดงชื่อครบ | ☐ |
| 3 | CLICK ปุ่ม **บันทึกร่าง** | — | drawer ปิดและ toast **บันทึกร่างแล้ว** | ☐ |
| 4 | TYPE `บริษัท Draft QA 2569 จำกัด` → ช่องค้นหา | — | เห็นหนึ่งแถวใหม่ ป้าย **แบบร่าง** และ code ขึ้นต้น `V-TH-` | ☐ |
| 5 | CLICK แถว vendor ใหม่ | — | drawer รายละเอียดแสดงชื่อ/code และ timeline มีรายการสร้าง draft | ☐ |

### TC-C02 — สร้าง Corporate ครบ 3 ขั้นและส่ง KYC (happy)
- group: สร้าง/แก้ไข · ความสำคัญ: สูง · trace: AC-06 / BR-VEN-05..09/24 / API-04 / vendor_kyc_submitted_event
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=tax ชุด A ยังไม่ซ้ำใน tenant · files=vendor-clean.pdf
- Start: OPEN `#/vendors`
- ชุดข้อมูล: A
- ผ่านเมื่อ: ผ่าน wizard ครบ, สถานะ **รอ KYC**, ข้อมูลสำคัญแสดงตรงชุด A

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **เพิ่มคู่ค้า** | — | drawer **เพิ่มคู่ค้าใหม่** เปิดที่ **ข้อมูล & ภาษี** | ☐ |
| 2 | SELECT **TR — Trading / Reseller** → ช่องประเภทคู่ค้า | A | ประเภทแสดง TR | ☐ |
| 3 | TYPE ชื่อเต็มและชื่อย่อ → ช่องชื่อทั้งสอง | A | ช่องแสดงค่าตรงชุด A | ☐ |
| 4 | TYPE `0105556102367` → ช่อง **เลขประจำตัวผู้เสียภาษี** | A | เห็น 13 หลักในช่อง | ☐ |
| 5 | TOGGLE สถานะ VAT | A | สถานะจด VATตรงชุด A | ☐ |
| 6 | SELECT สำนักงานใหญ่และ THB → ช่องสาขา/สกุลเงิน | A | สาขา/สกุลเงินตรงชุด A | ☐ |
| 7 | CLICK ปุ่ม **ถัดไป** | — | step **ติดต่อ & ธนาคาร** active; stepper label อยู่กึ่งกลางกับ dot | ☐ |
| 8 | TYPE ชื่อ อีเมล โทรศัพท์ → การ์ดผู้ติดต่อ | A | การ์ดแสดง `สมชาย ทดสอบ`, email และ phone | ☐ |
| 9 | TYPE labelและรายละเอียด → การ์ดที่อยู่ | A | ข้อความที่อยู่แสดงครบ | ☐ |
| 10 | SELECT จังหวัด/เขต/แขวง → การ์ดที่อยู่ | A | ค่าอ้างอิงสัมพันธ์กันและรหัสไปรษณีย์ `10110` | ☐ |
| 11 | TOGGLE **ใช้เป็นที่อยู่ใบกำกับ** | A | การ์ดแสดงบทบาทใบกำกับ | ☐ |
| 12 | TOGGLE **ตั้งเป็นจัดส่งหลัก** | A | การ์ดเดียวแสดงสองบทบาท | ☐ |
| 13 | SELECT ธนาคาร/purpose/currency → การ์ดบัญชี | A | ค่า KBANK/payment/THB แสดง | ☐ |
| 14 | TYPE เลขบัญชีและชื่อบัญชี → การ์ดบัญชี | A | การ์ดบัญชีแสดงข้อมูลครบ | ☐ |
| 15 | CLICK ปุ่ม **ถัดไป** | — | step **เอกสารแนบ & ชำระ** active | ☐ |
| 16 | SELECT **NET30** → **เงื่อนไขการชำระเงินเริ่มต้น** | A | ค่า NET30 แสดง | ☐ |
| 17 | TYPE WHT `3` และวงเงิน `100000` | A | ค่าไม่ติดลบและแสดงตามที่กรอก | ☐ |
| 18 | UPLOAD `vendor-clean.pdf` | — | การ์ดไฟล์ปรากฏและชื่อไฟล์มีช่องว่างจากไอคอนคลิปหนีบกระดาษ | ☐ |
| 19 | CLICK ปุ่ม **บันทึก + ส่ง KYC** | — | ปุ่มแสดง **กำลังบันทึก...** ชั่วคราว จากนั้น drawer ปิดและ toast **สร้างคู่ค้าแล้ว — ส่งเข้ากระบวนการ KYC** | ☐ |
| 20 | TYPE `บริษัท ทดสอบเวนเดอร์ 2569 จำกัด` → ช่องค้นหา | — | เห็นแถวใหม่ ป้าย **รอ KYC** | ☐ |

### TC-C03 — Required, format, enum และ boundary identity (negative)
- group: สร้าง/แก้ไข · ความสำคัญ: สูง · trace: AC-03 / BR-VEN-01/03/05 / BR_VENDOR_NAME_REQUIRED / BR_VENDOR_TYPE_INVALID / BR_TAX_ID_INVALID
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=— · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: C
- ผ่านเมื่อ: แต่ละค่าผิดถูก block โดยข้อความที่มองเห็นและไม่สร้าง vendor

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มคู่ค้า** | — | drawer เปิด | ☐ |
| 2 | CLICK **ถัดไป** โดยชื่อว่าง | — | toast **กรุณากรอกชื่อตามกฎหมาย**; ยังอยู่ step 1 | ☐ |
| 3 | TYPE ข้อความ `ก` 256 ตัว → **ชื่อตามกฎหมาย** | C | implementation แสดง validation max 255 และไม่ไป step ถัดไป `⚠ HTML prototype ยังไม่ enforce max` | ☐ |
| 4 | TYPE `บริษัท Tax Invalid จำกัด` → **ชื่อตามกฎหมาย** | — | ชื่อแสดง | ☐ |
| 5 | TYPE `123456789012` → **เลขประจำตัวผู้เสียภาษี** | C | toast **INVALID_TAX · เลขภาษีต้องเป็นตัวเลข 13 หลัก** | ☐ |
| 6 | TYPE `0105556102368` → **เลขประจำตัวผู้เสียภาษี** | C | implementation แสดง checksum error `BR_TAX_ID_INVALID`; ไม่บันทึก `⚠ HTML prototype ตรวจเพียง 13 หลัก` | ☐ |
| 7 | VERIFY direct API invalid vendor_type | ค่า `ZZ` `(ต้อง simulate API)` | response 422 `BR_VENDOR_TYPE_INVALID`; UI dropdownไม่มีค่า `ZZ`; ไม่มี record ใหม่ | ☐ |
| 8 | VERIFY branch validation | เลือกสาขาแต่ branch code ว่าง `(ต้อง simulateถ้า UI ไม่มี)` | เห็น field error/422 `BR_BRANCH_INVALID`; ไม่บันทึก | ☐ |

### TC-C04 — Tax ID ซ้ำใน tenant เดียว (negative)
- group: สร้าง/แก้ไข · ความสำคัญ: สูง · trace: AC-03 / EC-VEN-01 / BR-VEN-02 / BR_DUPLICATE_TAX_ID
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=tenant A มี vendor tax=`0105556102367` อยู่แล้ว · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: A แต่เปลี่ยนชื่อเป็น `บริษัท Tax Duplicate จำกัด`
- ผ่านเมื่อ: duplicate ถูก block และไม่มี aggregate/child บางส่วนค้าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มคู่ค้า** | — | drawer เปิด step 1 | ☐ |
| 2 | TYPE ชื่อใหม่และ tax `0105556102367` | — | ช่องแสดงค่าที่กรอก | ☐ |
| 3 | CLICK **ถัดไป** | — | toast **TAX_DUPLICATE · เลขภาษีซ้ำ — แนะนำ merge**; ยังอยู่ step 1 | ☐ |
| 4 | PRESS Esc | — | drawer ปิดตาม Esc chain | ☐ |
| 5 | TYPE `บริษัท Tax Duplicate จำกัด` → ช่องค้นหา | — | เห็น **ไม่พบคู่ค้า**; ไม่มี partial record | ☐ |

### TC-C05 — One-time ไม่มี tax และ bank (edge)
- group: สร้าง/แก้ไข · ความสำคัญ: สูง · trace: AC-04 / EC-VEN-02 / BR-VEN-03 / LD-03
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=ชื่อชุด B ยังไม่มี · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: B
- ผ่านเมื่อ: ส่ง KYC ได้โดย tax/bank ว่าง แต่ไม่ auto-approve

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มคู่ค้า** | — | drawer เปิด | ☐ |
| 2 | SELECT **OT — One-time** → ประเภทคู่ค้า | B | tax แสดงว่า optional/ไม่บังคับ | ☐ |
| 3 | TYPE `นายทดสอบ ครั้งเดียว` → **ชื่อตามกฎหมาย** | B | ชื่อแสดงครบ | ☐ |
| 4 | CLICK **ถัดไป** | tax ว่าง | ไป step **ติดต่อ & ธนาคาร** โดยไม่มี tax error | ☐ |
| 5 | TYPE contact และ address ตามชุด B | B | contact/address ครบ | ☐ |
| 6 | CLICK **ถัดไป** โดยไม่มีบัญชี | — | ไป step **เอกสารแนบ & ชำระ** | ☐ |
| 7 | SELECT **COD** → **เงื่อนไขการชำระเงินเริ่มต้น** | B | ค่า COD แสดง | ☐ |
| 8 | CLICK **บันทึก + ส่ง KYC** | — | drawer ปิด; vendor เป็น **รอ KYC**, ไม่เป็น active/อนุมัติอัตโนมัติ | ☐ |
| 9 | CLICK แถว vendor ใหม่ | — | Tax ID แสดง **ยกเว้น (One-time)** และไม่มีบัญชีได้ | ☐ |

### TC-C06 — Submit existing draft และ code ไม่ reuse (happy)
- group: สร้าง/แก้ไข · ความสำคัญ: สูง · trace: AC-06 / BR-VEN-04 / API-06
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=D-DRAFT มี minimum KYC dataset ครบ · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: D-DRAFT
- ผ่านเมื่อ: draft เดิมเปลี่ยนเป็นรอ KYC โดย code เดิม และ code รายการอื่นไม่ซ้ำ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE code ของ D-DRAFT → ช่องค้นหา | — | เห็นหนึ่งแถว ป้าย **แบบร่าง**; จด code เดิม | ☐ |
| 2 | CLICK แถว D-DRAFT | — | drawer detail เปิดและเห็นปุ่ม **ส่ง KYC** | ☐ |
| 3 | CLICK ปุ่ม **ส่ง KYC** | — | toast **ส่งเข้ากระบวนการ KYC**; ป้ายเปลี่ยนเป็น **รอ KYC** | ☐ |
| 4 | VERIFY code ใน header | — | code เท่ากับค่าที่จด step 1 ไม่สร้าง code ใหม่ | ☐ |
| 5 | VERIFY รายการทั้งหมด | — | ไม่มี vendor สองรายการใช้ code เดียวกัน | ☐ |

### TC-C07 — Credit limit และ WHT boundary (negative/boundary)
- group: สร้าง/แก้ไข · ความสำคัญ: สูง · trace: BR-VEN-09 / BR_CREDIT_LIMIT_INVALID / BR_WHT_INVALID
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=form ชุด A ไปถึง step 3 · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: C
- ผ่านเมื่อ: -0.01 และ WHT นอก 0..30 ถูก block; 0/30 ผ่าน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `-0.01` → ช่อง **วงเงินเครดิต** | C | implementation แสดง error/ไม่บันทึก `BR_CREDIT_LIMIT_INVALID` | ☐ |
| 2 | TYPE `-0.01` → ช่อง WHT | C | implementation แสดง error `BR_WHT_INVALID` | ☐ |
| 3 | TYPE `30.01` → ช่อง WHT | C | implementation แสดง error `BR_WHT_INVALID` | ☐ |
| 4 | TYPE `0` → วงเงิน และ WHT | — | ค่า boundary ต่ำสุดยอมรับได้ | ☐ |
| 5 | TYPE `30` → WHT | — | ค่า boundary สูงสุดยอมรับได้ | ☐ |

### TC-C08 — Contact/address minimum และ email+phone readiness (negative)
- group: สร้าง/แก้ไข · ความสำคัญ: สูง · trace: BR-VEN-08/24 / BR_CONTACT_REQUIRED / BR_ADDRESS_ROLE_REQUIRED
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=form non-OT ผ่าน step 1 · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: C
- ผ่านเมื่อ: ข้อมูล contact/address ไม่ครบไม่ผ่าน step/save

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ถัดไป** จาก step 1 ที่ถูกต้อง | — | step **ติดต่อ & ธนาคาร** เปิด | ☐ |
| 2 | TYPE `vendor@@example` → อีเมล และเว้น phone | C | ช่องเก็บค่าชั่วคราว | ☐ |
| 3 | CLICK **ถัดไป** | — | toast **ต้องมีผู้ติดต่ออย่างน้อย 1 ราย (ชื่อ + อีเมล)** หรือ validation ที่เจาะจงกว่า; ยังอยู่ step 2 | ☐ |
| 4 | TYPE contact ที่ถูกต้อง แต่เว้นรายละเอียดที่อยู่ | A contact | — | ☐ |
| 5 | CLICK **ถัดไป** | — | toast **ต้องมีที่อยู่อย่างน้อย 1 รายการ (ที่อยู่ + จังหวัด + ตำบล)** | ☐ |

### TC-C09 — เพิ่มหลายที่อยู่และ exactly-one roles (happy)
- group: สร้าง/แก้ไข · ความสำคัญ: สูง · trace: AC-05 / BR-VEN-24
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=form ชุด A อยู่ step 2 มีที่อยู่ 1 รายการ · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: ที่อยู่ใบที่ 2=`คลังสินค้า QA`, `77 ถนนคลัง`, กรุงเทพมหานคร/ลาดกระบัง
- ผ่านเมื่อ: เพิ่มได้, role billing/shipping มีอย่างละหนึ่ง, สลับ role แล้วใบเดิมถูกยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มที่อยู่** | — | การ์ดที่อยู่ใหม่ปรากฏและ focus อยู่ช่องรายละเอียดของใบใหม่ | ☐ |
| 2 | TYPE labelและรายละเอียดคลังสินค้า → การ์ดใบที่ 2 | ชุดข้อมูล | ข้อความที่อยู่แสดงครบ | ☐ |
| 3 | SELECT จังหวัด/เขต/แขวง → การ์ดใบที่ 2 | ชุดข้อมูล | ค่าอ้างอิงสัมพันธ์กันและ postalแสดง | ☐ |
| 4 | TOGGLE **ตั้งเป็นจัดส่งหลัก** → การ์ดใบที่ 2 | — | ใบที่ 2 เป็นจัดส่งหลัก; ใบที่ 1 ไม่เป็นจัดส่งหลัก | ☐ |
| 5 | TOGGLE **ใช้เป็นที่อยู่ใบกำกับ** → การ์ดใบที่ 2 | — | ใบที่ 2 เป็นใบกำกับ; ใบที่ 1 หลุดบทบาทใบกำกับ | ☐ |
| 6 | VERIFY การ์ดทั้งสอง | — | มี billing หนึ่งใบและ shipping หนึ่งใบเท่านั้น; ใบเดียวถือสอง role ได้ | ☐ |

### TC-C10 — ลบ designated address แล้ว clear role/บังคับเลือกใหม่ (edge)
- group: สร้าง/แก้ไข · ความสำคัญ: สูง · trace: AC-05 / BR-VEN-25 / BR_ADDRESS_ROLE_REQUIRED
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=form draft มี 2 ที่อยู่; ใบแรกเป็น billing+shipping · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: confirmation บอก role, หลังลบไม่มี auto-assign และ save ถูก blockจนเลือกใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอนลบของที่อยู่ใบแรก | — | modal **ลบที่อยู่นี้?** แสดงผลกระทบต่อที่อยู่ใบกำกับ/จัดส่งหลัก | ☐ |
| 2 | CLICK **ลบและเคลียร์การตั้งค่า** | — | toast **ลบที่อยู่แล้ว — กรุณาตรวจสอบการตั้งค่าที่อยู่**; ใบที่สองไม่ถูกตั้ง role อัตโนมัติ | ☐ |
| 3 | CLICK **ถัดไป** | — | toast **กรุณากำหนดที่อยู่ใบกำกับ** | ☐ |
| 4 | TOGGLE **ใช้เป็นที่อยู่ใบกำกับ** → ใบที่สอง | — | บทบาทใบกำกับปรากฏ | ☐ |
| 5 | CLICK **ถัดไป** | — | toast **กรุณากำหนดที่อยู่จัดส่งหลัก** | ☐ |
| 6 | TOGGLE **ตั้งเป็นจัดส่งหลัก** → ใบที่สอง | — | ผ่าน validation และไป step 3 ได้ | ☐ |

### TC-C11 — ปิดใช้ persisted address ของ active vendor (soft-disable)
- group: สร้าง/แก้ไข · ความสำคัญ: สูง · trace: AC-05 / BR-VEN-23/25 / LD-05/06
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=D-ACTIVE มี persisted addresses ≥2 และหนึ่งใบ designated · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ใช้คำว่า **ปิดใช้**, row ไม่ hard delete, designated role ถูก clear และต้องเลือกใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE code D-ACTIVE → ช่องค้นหา | — | เห็นแถว active | ☐ |
| 2 | CLICK action **แก้ไข** | — | drawer edit เปิด | ☐ |
| 3 | CLICK ไอคอนลบ/ปิดใช้ของ persisted designated address | — | modal **ปิดใช้ที่อยู่นี้?** | ☐ |
| 4 | CLICK **ปิดใช้และเคลียร์การตั้งค่า** | — | toast **ปิดใช้ที่อยู่แล้ว — กรุณาเลือกที่อยู่หลักใหม่** | ☐ |
| 5 | VERIFY ที่อยู่เดิมใน history/detailหลังบันทึก | — | record ยังอ้างอิงได้ในประวัติ/ไม่ถูก hard delete; active listไม่ใช้ที่อยู่นั้น | ☐ |

### TC-C12 — เพิ่ม/ลบบัญชี unverified ได้ทุกใบรวมใบแรก (happy/edge)
- group: สร้าง/แก้ไข · ความสำคัญ: สูง · trace: AC-05 / BR-VEN-06
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=form draft step 2 มีบัญชี unverified 1 ใบ · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: A bank + บัญชีใบสอง SCB `1234567890`
- ผ่านเมื่อ: เพิ่มและลบทุกบัญชี unverified ได้จนเหลือศูนย์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มบัญชี** | — | การ์ดบัญชีใบที่ 2 ปรากฏ | ☐ |
| 2 | SELECT **SCB** → การ์ดบัญชีใบที่ 2 | — | ธนาคาร SCB แสดง | ☐ |
| 3 | TYPE `1234567890` และชื่อบัญชี → การ์ดใบที่ 2 | — | ใบที่ 2 แสดงข้อมูลครบ | ☐ |
| 4 | CLICK ไอคอนลบบัญชีใบแรก | — | ใบแรกหาย เหลือใบที่ 2; ไม่มีข้อห้ามเพราะเป็นรายการแรก | ☐ |
| 5 | CLICK ไอคอนลบบัญชีที่เหลือ | — | เห็น **ยังไม่มีบัญชีธนาคาร** | ☐ |
| 6 | CLICK **เพิ่มบัญชี** | — | การ์ดบัญชีว่างปรากฏ | ☐ |
| 7 | TYPE เลข 9 หลัก → ช่องเลขบัญชี | C | implementation แสดง `BR_BANK_INVALID` ก่อนบันทึก | ☐ |
| 8 | TYPE เลข 16 หลัก → ช่องเลขบัญชี | C | implementation แสดง `BR_BANK_INVALID` ก่อนบันทึก | ☐ |

### TC-C13 — Verified bank read-only และแก้โดยเพิ่มบัญชีใหม่ (edge)
- group: สร้าง/แก้ไข · ความสำคัญ: สูง · trace: BR-VEN-06/26 / LD-08
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=D-ACTIVE มี verified bank · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: บัญชีใหม่ SCB `1234567890`
- ผ่านเมื่อ: บัญชี verified แก้ไม่ได้; เพิ่มบัญชีใหม่ได้; การปิดบัญชีเดิมสงวนให้ Finance

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **แก้ไข** ของ D-ACTIVE | — | drawer edit เปิด step ที่มีบัญชี | ☐ |
| 2 | VERIFY การ์ดบัญชี verified | — | เห็นข้อความ **บัญชีที่ยืนยันแล้วเป็น read-only หากต้องเปลี่ยนให้เพิ่มบัญชีใหม่และปิดใช้บัญชีเดิม**; ไม่มีช่องแก้ identity | ☐ |
| 3 | CLICK **เพิ่มบัญชี** | — | การ์ด unverified ใหม่ปรากฏ | ☐ |
| 4 | SELECT **SCB** → ธนาคารของบัญชีใหม่ | ชุดข้อมูล | ธนาคาร SCB แสดง | ☐ |
| 5 | TYPE `1234567890` และชื่อบัญชี → การ์ดใหม่ | ชุดข้อมูล | บัญชีใหม่แก้ไขได้ | ☐ |
| 6 | VERIFY action ของบัญชีเดิม | — | Procurement ไม่มีปุ่มยืนยัน/ปิดใช้ของ Finance ใน form edit | ☐ |

### TC-C14 — Edit state และ tax immutable หลัง KYC (negative)
- group: สร้าง/แก้ไข · ความสำคัญ: สูง · trace: AC-16 / BR-VEN-12/21 / EC-VEN-09
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=vendor draft, pending_kyc, active(KYC passed), pending_approval อย่างละ 1 · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: tax ใหม่ `0105540012347`
- ผ่านเมื่อ: edit เห็นเฉพาะ allowed states; active tax lock ทั้ง UI/API

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY action **แก้ไข** ของ draft/pending_kyc/active | — | ทั้งสามสถานะมี action edit สำหรับ role นี้ | ☐ |
| 2 | VERIFY action ของ pending_approval | — | ไม่มี action edit | ☐ |
| 3 | CLICK **แก้ไข** ของ active KYC passed | — | ช่องเลขภาษี read-only และเห็น **ล็อก — ผ่าน KYC แล้ว แก้ไขไม่ได้ (IR-01)** | ☐ |
| 4 | VERIFY direct API เปลี่ยน tax | `0105540012347` `(ต้อง simulate API)` | response 422 `BR_TAX_ID_IMMUTABLE`; ค่าเดิมยังแสดง | ☐ |

### TC-C15 — Reference cascade และ invalid FK (negative/edge)
- group: สร้าง/แก้ไข · ความสำคัญ: สูง · trace: validation country/payment/address FK / ERR_REFERENCE_DATA_UNAVAILABLE
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=form step 2 มีจังหวัด/เขต/แขวงเลือกครบ · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: เปลี่ยนจังหวัดจากกรุงเทพฯเป็นเชียงใหม่
- ผ่านเมื่อ: child dropdown ถูก clear และ invalid FK ถูก server block

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ค่าจังหวัด/เขต/แขวงเดิม | — | จดค่าทั้งสามก่อนเปลี่ยน | ☐ |
| 2 | SELECT **เชียงใหม่** → จังหวัด | — | เขต/อำเภอและแขวง/ตำบลเดิมถูก clear; ไม่คงค่าที่ไม่สัมพันธ์ | ☐ |
| 3 | SELECT อำเภอและตำบลที่เป็นลูกของเชียงใหม่ | — | dropdown แสดงเฉพาะค่าที่สัมพันธ์และ postal อัปเดต | ☐ |
| 4 | VERIFY direct API country/payment term ที่ไม่มีจริง | `(ต้อง simulate API)` | response validation `BR_COUNTRY_INVALID` หรือ `BR_PAYMENT_TERM_INVALID`; ไม่บันทึก | ☐ |

### TC-C16 — Wizard back, Esc/backdrop/X และ unsaved state [AI-DEFAULT]
- group: สร้าง/แก้ไข · ความสำคัญ: กลาง · trace: UI §1.10 / PR-6 `[AI-DEFAULT]`
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=— · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: ชื่อ `บริษัท Unsaved QA จำกัด`
- ผ่านเมื่อ: back คงค่า; close ของระบบจริงเตือน dirty; มีเพียงบันทึกร่างที่ persist

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มคู่ค้า** | — | drawer เปิด | ☐ |
| 2 | TYPE ชื่อ → **ชื่อตามกฎหมาย** | ชุดข้อมูล | ชื่อแสดงใน step 1 | ☐ |
| 3 | CLICK **ถัดไป** | — | ไป step 2 | ☐ |
| 4 | CLICK **กลับ** | — | กลับ step 1 และชื่อยังอยู่ | ☐ |
| 5 | PRESS Esc | — | HTML prototype ปิด drawerทันที; implementation ต้องแสดง confirm **ออกโดยไม่บันทึก?** `⚠ prototype gap` | ☐ |
| 6 | CLICK **กรอกต่อ** ใน confirm `(implementation)` | — | drawer ยังเปิดและข้อมูลยังอยู่ | ☐ |
| 7 | CLICK ปุ่ม X | — | confirm **ออกโดยไม่บันทึก?** ปรากฏใน implementation | ☐ |
| 8 | CLICK **ออกโดยไม่บันทึก** `(implementation)` | — | drawer ปิด; ค้นชื่อแล้วไม่พบ record | ☐ |
| 9 | CLICK **เพิ่มคู่ค้า** | — | drawerใหม่เปิด | ☐ |
| 10 | TYPE ชื่อเดิม → **ชื่อตามกฎหมาย** | — | ชื่อแสดง | ☐ |
| 11 | CLICK **บันทึกร่าง** | — | toast **บันทึกร่างแล้ว**; ค้นแล้วพบ draft | ☐ |

### TC-C17 — Attachment metadata ใน wizard (happy)
- group: สร้าง/แก้ไข · ความสำคัญ: สูง · trace: UI-02 / API-17 metadata
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=form ชุด A อยู่ step 3 · files=vendor-clean.pdf
- Start: OPEN `#/vendors`
- ชุดข้อมูล: document_type=หนังสือรับรอง, issued_at=2026-07-01, valid_until=2027-06-30
- ผ่านเมื่อ: ชื่อไฟล์/ชนิด/วันที่อยู่บนการ์ดและยังอยู่หลังบันทึก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `vendor-clean.pdf` | — | การ์ดเอกสารปรากฏ ชื่อไฟล์อ่านได้ | ☐ |
| 2 | SELECT ชนิดเอกสาร → การ์ดไฟล์ | หนังสือรับรอง | label ชนิดอัปเดต | ☐ |
| 3 | TYPE วันที่ออก/หมดอายุ → การ์ดไฟล์ | ชุดข้อมูล | วันที่ทั้งสองแสดง | ☐ |
| 4 | CLICK **บันทึก + ส่ง KYC** | — | บันทึกสำเร็จ | ☐ |
| 5 | CLICK tab **เอกสารแนบ** ใน view drawer | — | เห็น `vendor-clean.pdf`, ชนิดและวันที่ตรงที่กรอก | ☐ |

### TC-C18 — Escape XSS ใน name/reason/note/filename (security)
- group: สร้าง/แก้ไข · ความสำคัญ: สูง · trace: TC-VEN-027 / §5.7
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=environment อนุญาต fixture ชื่อไฟล์ที่ sanitize แล้ว · files=vendor-xss-name.pdf
- Start: OPEN `#/vendors`
- ชุดข้อมูล: C XSS text
- ผ่านเมื่อ: payload ถูกแสดงเป็น text/sanitize ไม่มี script/dialog และไม่มี markup แทรก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE XSS text → **ชื่อตามกฎหมาย** | C | เห็นอักขระเป็นข้อความ; ไม่มี alert/image request | ☐ |
| 2 | UPLOAD `vendor-xss-name.pdf` | — | filename ถูก sanitize/escape; ไม่มี HTML element จากชื่อไฟล์ | ☐ |
| 3 | TYPE XSS text → ช่องเหตุผลใน modal blockของ seed active | C | text อยู่ใน textarea; ไม่มี script execute | ☐ |
| 4 | TYPE XSS text → **รายละเอียดผลการตรวจ** ใน KYC modal | C | text อยู่ใน textarea; ไม่มี script execute | ☐ |
| 5 | VERIFY timeline/list หลังบันทึก test fixture | — | UI ยังปกติและ payloadไม่ executeเมื่อ renderซ้ำ | ☐ |

### Group K — KYC and Sanctions

### TC-K01 — Compliance ให้ผ่าน KYC ปกติ (happy)
- group: KYC · ความสำคัญ: สูง · trace: AC-07 / BR-VEN-10/13/14 / vendor_kyc_decided_event
- actor (role): Compliance
- Setup: role=compliance_officer (prototype=`compliance`) · seed=D-KYC เอกสาร/tax/sanctions พร้อมตรวจ · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: note=`ตรวจเอกสารและรายชื่อเฝ้าระวังแล้ว ไม่พบความเสี่ยง`
- ผ่านเมื่อ: modal แสดง scope, KYC เป็นผ่าน, vendor ยังรอส่งอนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE code D-KYC → ช่องค้นหา | — | เห็นแถว D-KYC | ☐ |
| 2 | CLICK แถว D-KYC | — | drawer เปิด ป้าย vendor **รอ KYC** | ☐ |
| 3 | CLICK ปุ่ม **ตรวจ KYC** | — | modal **ตรวจ KYC (Compliance)** แสดงคำแนะนำตรวจเอกสาร เลขภาษี และรายชื่อเฝ้าระวัง | ☐ |
| 4 | TYPE note → **รายละเอียดผลการตรวจ** | ชุดข้อมูล | note แสดงใน textarea | ☐ |
| 5 | CLICK **ผ่าน KYC** | — | modal ปิด; toast **บันทึกผล KYC: ผ่าน** | ☐ |
| 6 | VERIFY header และ action | — | KYC แสดง **ผ่าน**; vendor ยัง **รอ KYC** และ Procurement สามารถ **ส่งอนุมัติ** ได้ | ☐ |

### TC-K02 — KYC ไม่ผ่านโดยไม่กรอก note (negative)
- group: KYC · ความสำคัญ: สูง · trace: AC-07 / BR_KYC_NOTE_REQUIRED
- actor (role): Compliance
- Setup: role=compliance_officer · seed=D-KYC · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: note ว่าง
- ผ่านเมื่อ: ไม่สามารถยืนยัน fail และ state ไม่เปลี่ยน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ตรวจ KYC** ของ D-KYC | — | modal เปิดและ checkbox sanctions ยังไม่เลือก | ☐ |
| 2 | CLICK **ไม่ผ่าน** โดย note ว่าง | — | toast **กรุณาระบุรายละเอียดผลการตรวจ**; modal ยังเปิด | ☐ |
| 3 | CLICK **ยกเลิก** | — | modal ปิด; KYC ยัง **รอตรวจ** | ☐ |

### TC-K03 — KYC ไม่ผ่านปกติกลับ pending_kyc (happy-negative)
- group: KYC · ความสำคัญ: สูง · trace: AC-07 / LD-12 / FN-07
- actor (role): Compliance
- Setup: role=compliance_officer · seed=D-KYC · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: note=`เอกสารทะเบียนบริษัทอ่านไม่ชัด กรุณาแนบใหม่`
- ผ่านเมื่อ: KYC failed, vendorไม่ blocked, อยู่รอ KYCเพื่อแก้ไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ตรวจ KYC** ของ D-KYC | — | modal เปิด | ☐ |
| 2 | TYPE note → **รายละเอียดผลการตรวจ** | ชุดข้อมูล | note แสดง | ☐ |
| 3 | CLICK **ไม่ผ่าน** | — | modal ปิด; toast **บันทึกผล KYC: ไม่ผ่าน** | ☐ |
| 4 | VERIFY vendor state | — | KYC **ไม่ผ่าน**, vendor **รอ KYC**; ไม่เป็น **บล็อกชั่วคราว** | ☐ |
| 5 | VERIFY timeline | — | เห็นผล KYC ไม่ผ่านและ note/ผู้ตรวจ/เวลา | ☐ |

### TC-K04 — Sanctions hit บังคับ disable ผ่าน (security)
- group: KYC · ความสำคัญ: สูง · trace: AC-08 / EC-VEN-08 / BR_SANCTIONS_HIT_CANNOT_PASS
- actor (role): Compliance
- Setup: role=compliance_officer · seed=D-KYC · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: sanctions=true
- ผ่านเมื่อ: warning แสดง, ปุ่มผ่าน disabled, action เปลี่ยนข้อความ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ตรวจ KYC** ของ D-KYC | — | modal เปิด | ☐ |
| 2 | TOGGLE **ผลการคัดกรองพบข้อมูลตรงกับรายชื่อเฝ้าระวัง** | true | เห็น **ไม่สามารถให้ผ่าน KYC ได้** และข้อความคู่ค้าจะถูกระงับ | ☐ |
| 3 | VERIFY ปุ่ม action | — | ปุ่ม **ผ่าน KYC** disabled; ปุ่ม danger เป็น **ไม่ผ่านและบล็อกคู่ค้า** | ☐ |
| 4 | CLICK ปุ่ม **ผ่าน KYC** | — | actionไม่เกิด/ปุ่มกดไม่ได้; direct API attemptได้ 422 `BR_SANCTIONS_HIT_CANNOT_PASS` | ☐ |

### TC-K05 — Sanctions source/note required และ block สำเร็จ (security)
- group: KYC · ความสำคัญ: สูง · trace: AC-08 / BR-VEN-11 / BR_KYC_SOURCE_REQUIRED / BR_KYC_NOTE_REQUIRED
- actor (role): Compliance
- Setup: role=compliance_officer · seed=D-KYC · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: source=OFAC, note=`ชื่อและเลขทะเบียนตรงกับ OFAC test fixture`
- ผ่านเมื่อ: source/note validationครบ แล้ว vendor blockedพร้อม evidence

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ตรวจ KYC** | — | modalเปิด | ☐ |
| 2 | TOGGLE sanctions checkbox | — | แสดงช่อง **แหล่งข้อมูลที่ตรวจพบ** และ **รายละเอียดผลการตรวจ** | ☐ |
| 3 | CLICK **ไม่ผ่านและบล็อกคู่ค้า** โดยไม่เลือก source | — | toast **กรุณาเลือกแหล่งข้อมูลที่ตรวจพบ** | ☐ |
| 4 | SELECT **OFAC** → แหล่งข้อมูล | — | ค่า OFAC แสดง | ☐ |
| 5 | CLICK **ไม่ผ่านและบล็อกคู่ค้า** โดย note ว่าง | — | toast **กรุณาระบุรายละเอียดผลการตรวจ** | ☐ |
| 6 | TYPE note → **รายละเอียดผลการตรวจ** | ชุดข้อมูล | note แสดง | ☐ |
| 7 | CLICK **ไม่ผ่านและบล็อกคู่ค้า** | — | modal/drawer ปิด; toast **บันทึกผลแล้ว — ไม่ผ่าน KYC และบล็อกคู่ค้า** | ☐ |
| 8 | VERIFY แถวและ timeline | — | ป้าย **บล็อกชั่วคราว**, KYC **ไม่ผ่าน**; timeline มี OFAC/note/reviewer/time | ☐ |

### TC-K06 — Role อื่นตัดสิน KYC ไม่ได้ (permission)
- group: KYC · ความสำคัญ: สูง · trace: BR-VEN-13 / ERR_INSUFFICIENT_ROLE / permission matrix
- actor (role): Officer, Manager, Director, Finance, Viewer
- Setup: role=แต่ละ role ที่ระบุ · seed=D-KYC · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: mutation action ไม่ปรากฏหรือ server ปฏิเสธทุก role ที่ไม่ใช่ Compliance/Admin

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/vendors` เป็นแต่ละ role ที่ห้าม | O, M, D, F, V | รายการอ่านได้ตามสิทธิ์ | ☐ |
| 2 | CLICK แถว D-KYC | — | ไม่เห็นปุ่ม **ตรวจ KYC** สำหรับ role ที่ห้าม | ☐ |
| 3 | VERIFY direct API KYC decision `(ต้อง simulate)` | payload pass | response 403 `ERR_INSUFFICIENT_ROLE`; state/timelineไม่เปลี่ยน | ☐ |
| 4 | OPEN `#/vendors` เป็น Admin | — | listโหลดได้ | ☐ |
| 5 | CLICK D-KYC | — | เห็นปุ่ม **ตรวจ KYC** ตาม permission matrix | ☐ |

### TC-K07 — Sanctions provider timeout ห้าม auto-pass [AI-DEFAULT] (ต้อง simulate)
- group: KYC · ความสำคัญ: สูง · trace: OQ-01 / §3.4 / activated default `[AI-DEFAULT]`
- actor (role): Compliance
- Setup: role=compliance_officer · seed=D-KYC; inject sanctions provider timeout · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: timeout ไม่กลายเป็น pass; อยู่ pending/manual reviewและมี error observability

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ตรวจ KYC** ของ D-KYC | — | modal เปิด | ☐ |
| 2 | CLICK **ผ่าน KYC** ขณะ provider timeout | inject timeout | ⚠ ไม่พบใน HTML prototype: เห็น error ที่เข้าใจได้/ไม่แสดง success | ☐ |
| 3 | VERIFY vendor state | — | KYC ยัง **รอตรวจ** หรือ manual review; vendorไม่ active/blockedอัตโนมัติ | ☐ |
| 4 | VERIFY telemetry `(ต้อง simulate)` | correlation id | มี timeout/circuit-breaker logโดยไม่มี PII/sanctions noteเต็ม | ☐ |

### Group A — Approval, Policy Center and Reject/Resubmit

### TC-A01 — Submit approval พร้อมและ snapshot chain (happy)
- group: อนุมัติ · ความสำคัญ: สูง · trace: AC-09 / BR-VEN-07/08/10/17 / API-08
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=D-KYC-PASS, Policy คืน Manager→Director · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เปลี่ยนเป็นรออนุมัติและแสดง chain ตาม Policy

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว D-KYC-PASS | — | header KYC **ผ่าน** และมีปุ่ม **ส่งอนุมัติ** | ☐ |
| 2 | CLICK **ส่งอนุมัติ** | — | toast **ส่งอนุมัติ — รอ ผู้จัดการจัดซื้อ** หรือ label step แรกจาก Policy | ☐ |
| 3 | VERIFY status และ tab **การอนุมัติ** | — | vendor **รออนุมัติ**; chain Manager→Director แสดงตามลำดับ | ☐ |
| 4 | VERIFY user-facing text | — | ไม่มี threshold ภายใน Vendor, ไม่มี decision ref note และไม่มี `รออนุมัติ (0/1)` | ☐ |

### TC-A02 — Submit approval ก่อน KYC ผ่าน (negative)
- group: อนุมัติ · ความสำคัญ: สูง · trace: AC-09 / EC-VEN-03 / BR_KYC_NOT_PASSED
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=D-KYC แต่ readiness อื่นครบ · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: state คงเดิมและเห็น KYC gate

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว D-KYC | — | KYC ไม่ใช่ **ผ่าน** | ☐ |
| 2 | CLICK **ส่งอนุมัติ** | — | toast **KYC_NOT_PASSED · ต้องผ่าน KYC ก่อนส่งอนุมัติ** | ☐ |
| 3 | VERIFY status | — | vendor ยัง **รอ KYC**; tabอนุมัติไม่มี chain ใหม่ | ☐ |

### TC-A03 — Submit approval ไม่มี contact ที่ valid (negative)
- group: อนุมัติ · ความสำคัญ: สูง · trace: AC-09 / EC-VEN-04 / BR_CONTACT_REQUIRED
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=vendor pending_kyc, KYC passed, bank verified, contactไม่มี emailหรือphone · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: readiness blockและ stateไม่เปลี่ยน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว fixture | — | เห็นปุ่ม **ส่งอนุมัติ** | ☐ |
| 2 | CLICK **ส่งอนุมัติ** | — | toast **NOT_READY · ต้องมีผู้ติดต่อ (อีเมล+โทร) อย่างน้อย 1 ราย** | ☐ |
| 3 | VERIFY status | — | ยัง **รอ KYC** และไม่มี approval chain | ☐ |

### TC-A04 — Non-OT ไม่มี verified bank (negative)
- group: อนุมัติ · ความสำคัญ: สูง · trace: AC-09 / EC-VEN-05 / BR_VERIFIED_BANK_REQUIRED
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=non-OT pending_kyc, KYC passed, contact/addressครบ, bank unverified/ไม่มี · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: bank gate blockและ stateไม่เปลี่ยน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว fixture | — | KYC **ผ่าน** แต่ไม่มีบัญชี verified | ☐ |
| 2 | CLICK **ส่งอนุมัติ** | — | toast **NOT_READY · ต้องมีบัญชีธนาคารที่ยืนยันแล้วอย่างน้อย 1 บัญชี** | ☐ |
| 3 | VERIFY status | — | ยัง **รอ KYC**; ไม่มี chain | ☐ |

### TC-A05 — Policy unavailable/empty chain ไม่มี fallback (integration negative)
- group: อนุมัติ · ความสำคัญ: สูง · trace: AC-20 / LD-02 / ERR_POLICY_UNAVAILABLE
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=D-KYC-PASS; Policy timeoutหรือคืน chain ว่าง · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่สร้าง Manager fallback และ stateคง prior

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว D-KYC-PASS | — | ก่อน action vendor **รอ KYC** | ☐ |
| 2 | CLICK **ส่งอนุมัติ** | inject Policy empty/503 | HTML empty chain แสดง toast **ยังไม่พบสายอนุมัติ กรุณาลองใหม่อีกครั้ง**; implementation 503ใช้ข้อความที่ approvedในระบบจริง `⚠ ยืนยัน anchor` | ☐ |
| 3 | VERIFY status/tabอนุมัติ | — | ยัง **รอ KYC**, ไม่มี step Procurement Manager ที่ระบบแต่งเอง | ☐ |

### TC-A06 — OT ยังต้องผ่าน Policy ไม่ auto-approve (edge)
- group: อนุมัติ · ความสำคัญ: สูง · trace: AC-09 / LD-03 / BR-VEN-17
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=OT pending_kyc, KYC passed, contact/addressครบ, ไม่มี bank, Policy คืนอย่างน้อย 1 step · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: B
- ผ่านเมื่อ: bankยกเว้นได้แต่ approval chainยังถูกสร้าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว OT fixture | — | ประเภท OT, Tax **ยกเว้น (One-time)**, KYC **ผ่าน** | ☐ |
| 2 | CLICK **ส่งอนุมัติ** | — | toast ส่งอนุมัติและรอ roleจาก Policy | ☐ |
| 3 | VERIFY status | — | เป็น **รออนุมัติ**, ไม่เป็น **ใช้งาน** อัตโนมัติ | ☐ |

### TC-A07 — Multi-step approve จน active (happy)
- group: อนุมัติ · ความสำคัญ: สูง · trace: AC-10 / BR-VEN-16 / API-09
- actor (role): Procurement Manager แล้ว Procurement Director
- Setup: role=procurement_manager · seed=D-APPROVAL, maker=officer-A · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: stepกลางเลื่อน current, stepสุดท้าย active, timelineครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว D-APPROVAL | — | เห็นปุ่ม **อนุมัติ (ขั้น 1)** | ☐ |
| 2 | CLICK **อนุมัติ (ขั้น 1)** | — | modal **อนุมัติคู่ค้า — ขั้น 1/2** และ guard ผ่าน | ☐ |
| 3 | CLICK **อนุมัติขั้นนี้** | — | toast **อนุมัติขั้น 1 แล้ว — รอ ผู้อำนวยการจัดซื้อ**; statusยังรออนุมัติ | ☐ |
| 4 | OPEN `#/vendors` เป็น Procurement Director | — | D-APPROVAL มี actionอนุมัติขั้น 2 | ☐ |
| 5 | CLICK actionอนุมัติ | — | modalขั้น 2/2 เปิดและ guardผ่าน | ☐ |
| 6 | CLICK **อนุมัติ → ใช้งาน** | — | toast **อนุมัติครบทุกขั้น — "{vendor code}" → ใช้งาน** | ☐ |
| 7 | VERIFY status/timeline | — | ป้าย **ใช้งาน**; ทั้ง 2 steps approvedพร้อมผู้อนุมัติ/เวลา | ☐ |

### TC-A08 — SoD, wrong role และ Policy override (permission/negative)
- group: อนุมัติ · ความสำคัญ: สูง · trace: AC-10 / EC-VEN-06/07 / BR_SOD_VIOLATION / BR_WRONG_APPROVER
- actor (role): maker, wrong role, Director/Admin override
- Setup: role=ตาม subcase · seed=D-APPROVAL; Policy override flags false แล้ว trueใน subcaseสุดท้าย · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: maker/wrong roleถูก block; overrideทำได้เมื่อ Policyระบุเท่านั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN D-APPROVAL เป็น user ผู้สร้าง | maker officer-A | ปุ่ม confirm disabledหรือ actionไม่แสดง; direct attemptได้ `SOD_VIOLATION · ผู้อนุมัติต้องไม่ใช่ผู้สร้าง` | ☐ |
| 2 | OPEN D-APPROVAL เป็น wrong role | Finance/Compliance/Viewer | ไม่มี actionอนุมัติ; direct attemptได้ `WRONG_APPROVER · ขั้นนี้ต้อง {step label}`/403 | ☐ |
| 3 | OPEN D-APPROVAL เป็น Director/Admin เมื่อ override flag=false | — | ไม่สามารถอนุมัติ Manager step | ☐ |
| 4 | OPEN D-APPROVAL เป็น Director/Admin เมื่อ Policy explicit override=true | — | actionอนุมัติพร้อมใช้งานหาก SoD/readinessผ่าน | ☐ |
| 5 | VERIFY timeline หลัง denied attempts | — | ไม่มี step approved/audit decisionซ้ำจาก denied attempt | ☐ |

### TC-A09 — Reject หลัง partial approval และ resubmit (edge)
- group: อนุมัติ · ความสำคัญ: สูง · trace: AC-11 / EC-VEN-10 / BR-VEN-19/22
- actor (role): Procurement Director แล้ว Procurement Officer
- Setup: role=procurement_director · seed=D-PARTIAL · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: reason=`เอกสารบัญชีไม่ตรง กรุณาแก้ไขและส่งใหม่`
- ผ่านเมื่อ: reason required, กลับ pending_kyc, roundเดิมปิด, resubmitได้ chainใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว D-PARTIAL | — | detail drawerเปิด | ☐ |
| 2 | CLICK **ตีกลับ** | — | modal **ตีกลับคู่ค้า**; subtitleบอกกลับไปแก้ไขและตรวจ KYC ใหม่ | ☐ |
| 3 | CLICK **ตีกลับ** โดย reason ว่าง | — | toast **REASON_REQUIRED · กรุณาระบุเหตุผล**; modalยังเปิด | ☐ |
| 4 | TYPE reason → ช่อง **เหตุผล** | ชุดข้อมูล | reasonแสดง | ☐ |
| 5 | CLICK **ตีกลับ** | — | toast **ตีกลับคู่ค้าแล้ว → รอ KYC (แก้ไขแล้วส่งใหม่)** | ☐ |
| 6 | VERIFY tab **การอนุมัติ** | — | vendor **รอ KYC**; roundเดิมปิด/remaining steps cancelled; reasonใน timeline | ☐ |
| 7 | OPEN `#/vendors` เป็น Procurement Officer | — | listโหลดและ fixtureหลังแก้/KYCผ่านแสดง | ☐ |
| 8 | CLICK **ส่งอนุมัติ** | Policy คืน chainใหม่ | status **รออนุมัติ** และ submission roundใหม่ ไม่ reuse pending stepsเดิม | ☐ |

### Group B — Bank Verification and Deactivation

### TC-B01 — Finance ส่งตรวจและยืนยันบัญชี (happy)
- group: ธนาคาร · ความสำคัญ: สูง · trace: AC-12 / BR-VEN-06/07 / API-14/15
- actor (role): Finance
- Setup: role=finance_officer (prototype=`finance`) · seed=vendor non-OT มี bank unverified · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: unverified→pending_verification→verified, เห็นเลขเต็มเฉพาะ Finance

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว fixture | — | detail drawerเปิด | ☐ |
| 2 | CLICK tab **ธนาคาร & ติดต่อ** | — | Finance เห็นเลขบัญชีเต็มและปุ่ม **ส่งตรวจ** | ☐ |
| 3 | CLICK **ส่งตรวจ** | — | toast **ส่งบัญชีเข้าคิวตรวจสอบแล้ว**; actionเปลี่ยนเป็น **ยืนยันผล** | ☐ |
| 4 | CLICK **ยืนยันผล** | — | toast **ยืนยันบัญชีธนาคารแล้ว — PV gate ปลดล็อก** | ☐ |
| 5 | VERIFY bank card/timeline | — | ป้ายบัญชียืนยันแล้ว, verified_by/time และ auditปรากฏ | ☐ |

### TC-B02 — Role อื่นทำ bank verification ไม่ได้ (permission)
- group: ธนาคาร · ความสำคัญ: สูง · trace: permission matrix / ERR_INSUFFICIENT_ROLE
- actor (role): Officer, Manager, Director, Compliance, Viewer
- Setup: role=แต่ละ role · seed=vendor bank unverified/pending · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: action Financeไม่ปรากฏและ direct mutationถูก 403

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว fixture และ tab **ธนาคาร & ติดต่อ** เป็นแต่ละ role | O,M,D,C,V | ไม่เห็น **ส่งตรวจ**, **ยืนยันผล**, **ปิดใช้บัญชี** | ☐ |
| 2 | VERIFY direct API submit/decision/deactivate `(ต้อง simulate)` | — | response 403 `ERR_INSUFFICIENT_ROLE`; bank stateไม่เปลี่ยน | ☐ |

### TC-B03 — Verified bank identity read-only ใน view/edit (edge)
- group: ธนาคาร · ความสำคัญ: สูง · trace: BR-VEN-06/26 / LD-08
- actor (role): Finance แล้ว Procurement Officer
- Setup: role=finance_officer · seed=D-ACTIVE verified bank · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: identity fieldเดิมแก้ไม่ได้, ต้องเพิ่ม rowใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK D-ACTIVE → tab **ธนาคาร & ติดต่อ** | — | verified bank แสดงป้ายยืนยันและไม่มีช่องแก้ identity | ☐ |
| 2 | OPEN D-ACTIVE เป็น Procurement Officer | — | detail drawerเปิด | ☐ |
| 3 | CLICK **แก้ไข** | — | เห็นข้อความ read-onlyและปุ่ม **เพิ่มบัญชี** | ☐ |
| 4 | VERIFY direct API เปลี่ยนเลขบัญชี verified `(ต้อง simulate)` | — | 422 `BR_BANK_STATE_INVALID`; ค่าเดิมคงอยู่ | ☐ |

### TC-B04 — ปิดใช้บัญชีต้องมีเหตุผลและเก็บ history (negative/happy)
- group: ธนาคาร · ความสำคัญ: สูง · trace: AC-12 / BR-VEN-22/23 / API-16
- actor (role): Finance
- Setup: role=finance_officer · seed=D-ACTIVE verified bank ≥2 · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: reason=`ปิดบัญชีตามหนังสือแจ้งจากคู่ค้า`
- ผ่านเมื่อ: modal reason required, bank disabled, primary cleared, historyยังอยู่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK D-ACTIVE → tab **ธนาคาร & ติดต่อ** → **ปิดใช้บัญชี** | — | modal **ปิดใช้บัญชีธนาคาร** และข้อความประวัติเดิมยังคงอยู่ | ☐ |
| 2 | CLICK **ยืนยันปิดใช้บัญชี** โดย reasonว่าง | — | toast **กรุณาระบุเหตุผลที่ปิดใช้บัญชี** | ☐ |
| 3 | TYPE reason → **เหตุผลที่ปิดใช้บัญชี** | ชุดข้อมูล | reasonแสดง | ☐ |
| 4 | CLICK **ยืนยันปิดใช้บัญชี** | — | toast **ปิดใช้บัญชีแล้ว — ประวัติยังคงอยู่** | ☐ |
| 5 | VERIFY bank/timeline | — | bankเป็น disabled/ไม่ใช้จ่ายใหม่, primaryถูก clear, reason/timeอยู่ใน audit | ☐ |

### TC-B05 — ปิดบัญชี verified ใบสุดท้าย (edge)
- group: ธนาคาร · ความสำคัญ: สูง · trace: EC-VEN-13 / ENG-01 / vendor_payment_eligibility_changed_event
- actor (role): Finance
- Setup: role=finance_officer · seed=D-ACTIVE มี verified bankที่ activeเพียง 1 ใบ; eligible PO/payment=true · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: reason=`บัญชีถูกปิดโดยธนาคาร`
- ผ่านเมื่อ: vendorยัง active, payment eligibility false, PO eligibilityตาม active+KYC

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY และจด status/eligibility ก่อน | — | vendor=ใช้งาน, PO=true, Payment=true | ☐ |
| 2 | CLICK **ปิดใช้บัญชี** | — | เห็นกล่องยืนยันและช่องเหตุผล | ☐ |
| 3 | TYPE reason → ช่องเหตุผล | `บัญชีถูกปิดโดยธนาคาร` | ช่องแสดงค่าที่กรอก | ☐ |
| 4 | CLICK ปุ่มยืนยันในกล่อง | — | toastปิดใช้สำเร็จ | ☐ |
| 5 | VERIFY vendor status | — | ยัง **ใช้งาน** ไม่เปลี่ยนเป็น blocked/inactive | ☐ |
| 6 | VERIFY eligibility `(implementation/API-19)` | — | PO=true, Payment=false และมี reason code verified-bank missing | ☐ |
| 7 | VERIFY event `(ต้อง simulate consumer)` | — | `vendor_payment_eligibility_changed_event` มี versionใหม่ | ☐ |

### TC-B06 — Reject bank verification ต้องมีเหตุผล (negative, ต้อง simulate)
- group: ธนาคาร · ความสำคัญ: สูง · trace: Bank state machine / BR_REASON_REQUIRED / BR_BANK_STATE_INVALID
- actor (role): Finance
- Setup: role=finance_officer · seed=bank pending_verification; implementationมี verification decision reject · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: reason=`ชื่อบัญชีไม่ตรงเอกสาร`
- ผ่านเมื่อ: rejectว่างถูก block; rejectมีเหตุผลกลับ unverified

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK actionปฏิเสธผลตรวจ `⚠ ไม่พบใน HTML prototype` | — | modal/fieldเหตุผลปรากฏ | ☐ |
| 2 | CLICK confirm โดย reasonว่าง | — | เห็น validation reason required; stateยัง pending | ☐ |
| 3 | TYPE reason → ช่องเหตุผล | ชุดข้อมูล | reasonแสดง | ☐ |
| 4 | CLICK confirm | — | bankกลับ **ยังไม่ยืนยัน** และ auditมี reason | ☐ |
| 5 | VERIFY direct decisionจาก stateอื่น | verified/disabled | response 422 `BR_BANK_STATE_INVALID` | ☐ |

### TC-B07 — Disabled bank ห้าม re-enable/แก้ (negative)
- group: ธนาคาร · ความสำคัญ: สูง · trace: BR-VEN-26 / bank state machine / BR_BANK_STATE_INVALID
- actor (role): Finance
- Setup: role=finance_officer · seed=vendorมี disabled bank และ unverified bankใหม่ · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: disabledเป็น historical ไม่มี actionย้อน; new rowเดิน verificationได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK vendor → tab **ธนาคาร & ติดต่อ** | — | disabled bankแสดง historical/read-only | ☐ |
| 2 | VERIFY actionของ disabled bank | — | ไม่มี **ส่งตรวจ**, **ยืนยันผล**, re-enable หรือ edit identity | ☐ |
| 3 | VERIFY direct transition disabled→verified `(ต้อง simulate)` | — | 422 `BR_BANK_STATE_INVALID` | ☐ |
| 4 | CLICK **ส่งตรวจ** ของ bank rowใหม่ | — | rowใหม่เปลี่ยน pendingได้โดยไม่แก้ rowเก่า | ☐ |

### Group S — Availability, Inactive and Blacklist

### TC-S01 — Block active vendor พร้อมเหตุผล (happy)
- group: สถานะ · ความสำคัญ: สูง · trace: AC-13 / BR-VEN-22/28 / API-10
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=D-ACTIVE · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: reason=`ระงับชั่วคราวระหว่างตรวจสอบเอกสาร`
- ผ่านเมื่อ: active→blocked, transactionใหม่ไม่พร้อม, historyคงอยู่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK D-ACTIVE | — | detail drawerเปิด | ☐ |
| 2 | CLICK **บล็อก** | — | modal **บล็อกคู่ค้า** แสดง | ☐ |
| 3 | TYPE reason → ช่อง **เหตุผล** | ชุดข้อมูล | reasonแสดง | ☐ |
| 4 | CLICK **บล็อก** | — | toast **บล็อกคู่ค้าแล้ว** | ☐ |
| 5 | VERIFY แถว/timeline | — | ป้าย **บล็อกชั่วคราว** และ timelineมี reason/actor/time | ☐ |

### TC-S02 — Block โดยไม่กรอกเหตุผล (negative)
- group: สถานะ · ความสำคัญ: สูง · trace: BR-VEN-22 / BR_REASON_REQUIRED
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=D-ACTIVE · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: reason blank
- ผ่านเมื่อ: modalไม่ปิดและ stateไม่เปลี่ยน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK D-ACTIVE → **บล็อก** | — | modalเปิด | ☐ |
| 2 | CLICK **บล็อก** โดย reasonว่าง | — | toast **REASON_REQUIRED · กรุณาระบุเหตุผล** | ☐ |
| 3 | CLICK **ยกเลิก** | — | vendorยัง **ใช้งาน** | ☐ |

### TC-S03 — Unblock ถูกปิดเมื่อ KYC/Policy ไม่ valid (negative)
- group: สถานะ · ความสำคัญ: สูง · trace: AC-13 / API-11 precondition
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=D-BLOCKED-INVALID · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: modalบอก gateที่ไม่ผ่านและ confirm disabled/direct API rejected

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK D-BLOCKED-INVALID → **ปลดบล็อก** | — | modal **ปลดบล็อกคู่ค้า** แสดง **ยังปลดบล็อกไม่ได้ กรุณาดำเนินการตามเงื่อนไขที่แสดง** | ☐ |
| 2 | VERIFY สรุป KYC/นโยบายอนุมัติ | — | ค่าไม่พร้อมถูกระบุ เช่น **ต้องตรวจและให้ผ่านก่อน** หรือ **ต้องตรวจสอบใหม่** | ☐ |
| 3 | CLICK **ปลดบล็อก** | — | ปุ่ม disabled/ไม่มี mutation; direct APIได้ 422 state/readiness error | ☐ |
| 4 | VERIFY status | — | ยัง **บล็อกชั่วคราว** | ☐ |

### TC-S04 — Unblock valid vendor (happy)
- group: สถานะ · ความสำคัญ: สูง · trace: AC-13 / BR-VEN-22 / API-11
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=D-BLOCKED-VALID · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: reason=`ตรวจสอบครบและอนุญาตให้กลับมาใช้งาน`
- ผ่านเมื่อ: blocked→active และ payment readinessแยกตาม bank

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK D-BLOCKED-VALID → **ปลดบล็อก** | — | modalแสดง KYC **ผ่าน**, Policy **พร้อมใช้งาน** และสถานะการจ่ายเงิน | ☐ |
| 2 | TYPE reason → **เหตุผลที่ปลดบล็อก** | ชุดข้อมูล | reasonแสดง | ☐ |
| 3 | CLICK **ปลดบล็อก** | — | toast **ปลดบล็อกแล้ว → ใช้งาน** | ☐ |
| 4 | VERIFY status/timeline | — | ป้าย **ใช้งาน** และ auditมี reason | ☐ |

### TC-S05 — ปิดใช้งานคู่ค้า normal offboarding (happy/negative)
- group: สถานะ · ความสำคัญ: สูง · trace: AC-13 / BR-VEN-22/28 / API-12
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=D-ACTIVE · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: reason=`สิ้นสุดสัญญา`
- ผ่านเมื่อ: reason required, active→inactive, historyคงอยู่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK D-ACTIVE → **ปิดใช้งาน** | — | modal **ปิดใช้งานคู่ค้า** และคำอธิบายรายการใหม่ถูกระงับ | ☐ |
| 2 | CLICK **ยืนยันปิดใช้งาน** โดย reasonว่าง | — | toast **REASON_REQUIRED · กรุณาระบุเหตุผล** | ☐ |
| 3 | TYPE `สิ้นสุดสัญญา` → เหตุผล | — | reasonแสดง | ☐ |
| 4 | CLICK **ยืนยันปิดใช้งาน** | — | toast **ปิดใช้งานคู่ค้าแล้ว — รายการใหม่ถูกระงับ** | ☐ |
| 5 | VERIFY status/history | — | ป้าย **ปิดใช้งาน**; vendor ID/timelineเดิมยังอยู่ | ☐ |

### TC-S06 — Director/Admin blacklist พร้อมเหตุผล (happy)
- group: สถานะ · ความสำคัญ: สูง · trace: AC-14 / BR-VEN-20/22 / API-13
- actor (role): Procurement Director และ Admin
- Setup: role=procurement_director · seed=vendor non-terminal · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: reason=`ยืนยันความเสี่ยงร้ายแรงตามผลสอบสวน`
- ผ่านเมื่อ: actionเฉพาะ Director/Admin, status blacklisted terminal

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK vendor non-terminal → **แบล็คลิสต์** | — | modal **แบล็คลิสต์คู่ค้า** | ☐ |
| 2 | CLICK confirm โดย reasonว่าง | — | toast **REASON_REQUIRED · กรุณาระบุเหตุผล** | ☐ |
| 3 | TYPE reason → ช่องเหตุผล | ชุดข้อมูล | reasonแสดง | ☐ |
| 4 | CLICK **แบล็คลิสต์** | — | toast **แบล็คลิสต์คู่ค้าแล้ว (terminal)** | ☐ |
| 5 | VERIFY แถว/timeline | — | ป้าย **แบล็คลิสต์**, reason/actor/timeครบ | ☐ |
| 6 | OPEN fixtureใหม่เป็น Admin | — | Adminเห็น action **แบล็คลิสต์** | ☐ |
| 7 | VERIFY ทำซ้ำด้วย reasonครบ | — | Adminทำได้และได้ผล terminalเหมือนกัน | ☐ |

### TC-S07 — Blacklist ไม่มี transition ออก (negative)
- group: สถานะ · ความสำคัญ: สูง · trace: AC-14 / EC-VEN-12 / BR_BLACKLIST_TERMINAL
- actor (role): Admin
- Setup: role=admin · seed=D-BLACKLIST · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: UIไม่มี mutationเพื่อกลับ state และ APIปฏิเสธ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK D-BLACKLIST | — | drawerแสดงป้าย **แบล็คลิสต์** | ☐ |
| 2 | VERIFY header actions | — | ไม่มี **แก้ไข**, **ปลดบล็อก**, **ปิดใช้งาน**, **อนุมัติ** หรือ re-activate | ☐ |
| 3 | VERIFY direct API unblock/deactivate/update `(ต้อง simulate)` | — | 422 `BR_BLACKLIST_TERMINAL`/`BR_INVALID_STATE_TRANSITION` | ☐ |
| 4 | VERIFY statusหลัง denied attempts | — | ยัง blacklistedและไม่มี audit success | ☐ |

### TC-S08 — Invalid edit/transition และ referenced historyคงอยู่ (edge)
- group: สถานะ · ความสำคัญ: สูง · trace: EC-VEN-11 / BR-VEN-21/23/28 / ERR_VENDOR_NOT_FOUND
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=D-ACTIVE มี PO/PV history; fixture pending_approval/inactive · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มี hard delete, edit/stateผิดถูก block, historyยังอ้าง vendor ID

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK D-ACTIVE แล้ว blockตาม TC-S01 | — | vendorเป็น blocked | ☐ |
| 2 | VERIFY transaction history/reference | — | PO/PVเดิมยังแสดง vendor code/name; ไม่มีข้อความเทคนิค match keyต่อผู้ใช้ | ☐ |
| 3 | VERIFY edit pending_approval/inactive | — | ไม่มี action editตาม approved UI; direct updateได้ `BR_VENDOR_NOT_EDITABLE`/state error | ☐ |
| 4 | VERIFY hard DELETE vendor `(ต้อง simulate API)` | — | endpointไม่รองรับหรือถูกปฏิเสธ; GET vendor IDยังคืนประวัติที่มีสิทธิ์ | ☐ |
| 5 | OPEN vendor id ที่ไม่มี/tenantอื่น | — | 404 `ERR_VENDOR_NOT_FOUND` หรือหน้าว่างโดยไม่เปิดเผยข้อมูล | ☐ |

### Group P — Permission, Masking and Tenant Isolation

### TC-P01 — ทุก role เปิด list/detail ได้ตาม auth (permission)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: AC-15 / permission View cells / ERR_NOT_AUTHENTICATED
- actor (role): O, M, D, C, F, A, V
- Setup: role=แต่ละ role · seed=D-ACTIVE · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: authenticatedทุก roleเห็น list/detail; unauthenticatedไม่เห็นข้อมูล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/vendors` เป็นแต่ละ authenticated role | O,M,D,C,F,A,V | เห็น **ทะเบียนคู่ค้า** และรายการ tenantตนเอง | ☐ |
| 2 | CLICK แถว D-ACTIVE | — | detail drawerเปิด; field/actionแตกต่างตาม role | ☐ |
| 3 | OPEN `#/vendors` โดยไม่มี session `(implementation)` | — | redirect/loginหรือ 401 `ERR_NOT_AUTHENTICATED`; ไม่เห็นข้อมูล vendor | ☐ |

### TC-P02 — Tax masked สำหรับ Officer/Manager/Director/Viewer (security)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: AC-15 / BR-VEN-18 / ERR_FIELD_ACCESS_DENIED
- actor (role): Officer, Manager, Director, Viewer
- Setup: role=แต่ละ role · seed=D-ACTIVE taxเต็ม `0105556102367` · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: list/detailไม่เผย taxเต็มและรูป maskสม่ำเสมอ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/vendors` เป็นแต่ละ role | O,M,D,V | คอลัมน์เลขภาษีเป็น masked; ไม่เห็น `0105556102367` เต็ม | ☐ |
| 2 | CLICK D-ACTIVE → tab **ภาพรวม** | — | Tax ID ยัง maskedและไม่มี action reveal | ☐ |
| 3 | VERIFY response/browser source `(implementation)` | — | raw taxไม่ถูกส่งให้ unauthorized client; direct full-field requestถูกปฏิเสธ/audited | ☐ |

### TC-P03 — Compliance/Finance/Admin เห็น tax เต็มและถูก audit (security)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: AC-15 / BR-VEN-18/29
- actor (role): Compliance, Finance, Admin
- Setup: role=แต่ละ role · seed=D-ACTIVE taxเต็ม `0105556102367` · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: authorizedเห็น full taxและ sensitive-view auditหนึ่งครั้งต่อ accessตาม policy

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN D-ACTIVE เป็น Compliance | — | tabภาพรวมเห็น `0105556102367` เต็ม | ☐ |
| 2 | OPEN D-ACTIVE เป็น Finance | — | เห็น taxเต็ม | ☐ |
| 3 | OPEN D-ACTIVE เป็น Admin | — | เห็น taxเต็ม | ☐ |
| 4 | VERIFY sensitive-view audit `(implementation)` | — | auditมี actor/role/vendor/time; ไม่บันทึก taxเต็มใน application log | ☐ |

### TC-P04 — Bank account Restricted เฉพาะ Finance/Admin (security)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: AC-15 / BR-VEN-18 / permission Bank cells
- actor (role): ทุก role
- Setup: role=แต่ละ role · seed=D-ACTIVE account `0123456789` · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: Finance/Adminเห็นเลขเต็ม; roleอื่น maskedและไม่มี bank action

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN tab **ธนาคาร & ติดต่อ** เป็น O,M,D,C,V | — | เห็นเลข maskedและข้อความ **เลขบัญชีถูกปกปิด (Restricted)**; ไม่มี Finance actions | ☐ |
| 2 | OPEN tabเดียวกันเป็น Finance | — | เห็น `0123456789` และ bank actionsตาม state | ☐ |
| 3 | OPEN tabเดียวกันเป็น Admin | — | เห็นเลขเต็มและ actionsตาม policy | ☐ |
| 4 | VERIFY client payload `(implementation)` | — | unauthorized responseไม่มี ciphertext/raw account | ☐ |

### TC-P05 — Credit data เต็มเฉพาะ Finance/Admin (security)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: BR-VEN-18 / permission Full credit cells
- actor (role): ทุก role
- Setup: role=แต่ละ role · seed=D-ACTIVE credit=100000, payment term=NET30 · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: Finance/Adminเห็น full credit; roleอื่น masked/ไม่เห็นตาม field policy

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK D-ACTIVE → **ภาพรวม** เป็น O,M,D,C,V | — | creditถูก mask/exclude; ไม่มีข้อมูลเกินสิทธิ์ | ☐ |
| 2 | OPEN detailเป็น Finance | — | เห็นวงเงิน `100,000.00` และ term NET30 | ☐ |
| 3 | OPEN detailเป็น Admin | — | เห็น full creditตาม policy | ☐ |
| 4 | VERIFY sensitive-view audit `(implementation)` | — | full credit viewถูก auditโดยไม่ logค่าลับเกินจำเป็น | ☐ |

### TC-P06 — Create/edit/submit และ submit approval allow/deny (permission)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: permission matrix / ERR_INSUFFICIENT_ROLE
- actor (role): ทุก role
- Setup: role=แต่ละ role · seed=D-DRAFT และ D-KYC-PASS · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: Officer/Admin allow; M/D/C/F/V denyสำหรับ create/edit/submit

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/vendors` เป็น Officer | — | เห็น **เพิ่มคู่ค้า**, edit/submitตาม state | ☐ |
| 2 | OPEN `#/vendors` เป็น Admin | — | เห็น create/edit/submitและยังผ่าน state/SoD guard | ☐ |
| 3 | OPEN `#/vendors` เป็น M,D,C,F,V | — | ไม่เห็น **เพิ่มคู่ค้า** และ mutation actionsเหล่านี้ | ☐ |
| 4 | VERIFY direct create/edit/submit API เป็น denied roles `(ต้อง simulate)` | — | 403 `ERR_INSUFFICIENT_ROLE`; stateไม่เปลี่ยน | ☐ |

### TC-P07 — KYC/approval actions แยก role (permission)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: BR-VEN-13/16 / permission matrix
- actor (role): Compliance, Admin, Finance, Viewer
- Setup: role=แต่ละ role · seed=D-KYC และ D-APPROVAL · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: Compliance/Admin KYC; approvalเฉพาะ Policy role/explicit override

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN D-KYC เป็น Compliance/Admin | — | เห็น **ตรวจ KYC** | ☐ |
| 2 | OPEN D-KYC เป็น Finance/Viewer | — | ไม่เห็น **ตรวจ KYC** | ☐ |
| 3 | OPEN D-APPROVAL เป็น Compliance/Finance/Viewer | — | ไม่เห็น actionอนุมัติ/ตีกลับ | ☐ |
| 4 | VERIFY direct denied action `(ต้อง simulate)` | — | 403/422 และ approval/KYC stateไม่เปลี่ยน | ☐ |

### TC-P08 — Block/deactivate/blacklist role matrix (permission)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: permission matrix / API-10..13
- actor (role): ทุก role
- Setup: role=แต่ละ role · seed=D-ACTIVE · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: O/M/D/A block; D/A blacklist; C/F/V deny

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN D-ACTIVE เป็น O,M,D,A | — | เห็น block/deactivateตาม approved UI/capability | ☐ |
| 2 | OPEN D-ACTIVE เป็น C,F,V | — | ไม่เห็น block/unblock/deactivate | ☐ |
| 3 | OPEN non-terminal vendorเป็น D,A | — | เห็น **แบล็คลิสต์** | ☐ |
| 4 | OPEN recordเดียวกันเป็น O,M,C,F,V | — | ไม่เห็น **แบล็คลิสต์** | ☐ |
| 5 | VERIFY direct denied mutations `(ต้อง simulate)` | — | 403และ statusไม่เปลี่ยน | ☐ |

### TC-P09 — Tenant isolation และ anti-enumeration (security)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: AC-15 / BR-VEN-02/29 / RLS / ERR_VENDOR_NOT_FOUND
- actor (role): Admin tenant A
- Setup: role=admin tenant A · seed=D-ACTIVE tenant A + D-TENANT-Bชื่อเหมือนกัน · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: tenant B vendor_id
- ผ่านเมื่อ: list/search/IDไม่เผย tenant B; duplicate uniqueแยก tenant

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE ชื่อที่เหมือนกัน → ช่องค้นหา | — | เห็นเฉพาะ record tenant A | ☐ |
| 2 | OPEN detailด้วย tenant B vendor_id `(ต้อง simulate route/API)` | — | 404 `ERR_VENDOR_NOT_FOUND` หรือ anti-enumeration policy; ไม่เผยว่ามี record | ☐ |
| 3 | VERIFY direct listพร้อม forged tenant header `(ต้อง simulate)` | — | token tenantชนะ; ไม่คืน tenant B | ☐ |
| 4 | VERIFY สร้าง taxเดียวกันใน tenant B | — | ทำได้ตาม uniqueness tenant+countryโดยไม่กระทบ tenant A | ☐ |
| 5 | VERIFY RLS/audit `(implementation)` | — | ทุก query/mutationมี tenant scopeและ auditไม่ข้าม tenant | ☐ |

### Group F — Attachment Security and Retention

### TC-F01 — Upload clean allowed file และ private metadata (happy)
- group: เอกสารแนบ · ความสำคัญ: สูง · trace: AC-17 / API-17 / FN-13
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=editable vendor · files=vendor-clean.pdf
- Start: OPEN `#/vendors`
- ชุดข้อมูล: document_type=หนังสือรับรอง
- ผ่านเมื่อ: scan cleanก่อน active, UIเห็น metadataแต่ไม่เห็น object key

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **แก้ไข** vendor → step **เอกสารแนบ & ชำระ** | — | เห็นปุ่ม **แนบไฟล์** | ☐ |
| 2 | UPLOAD `vendor-clean.pdf` | — | เห็นชื่อไฟล์และ metadata form | ☐ |
| 3 | CLICK **บันทึก (amend)** | — | บันทึกสำเร็จหลัง scan clean | ☐ |
| 4 | CLICK tab **เอกสารแนบ** | — | เห็นไฟล์/ชนิด/สถานะตรวจ; ไม่เห็น private object key | ☐ |
| 5 | VERIFY download access `(implementation)` | — | signed accessสั้นและ re-check authorization | ☐ |

### TC-F02 — File type ไม่อนุญาต (negative)
- group: เอกสารแนบ · ความสำคัญ: สูง · trace: ERR_FILE_TYPE_NOT_ALLOWED
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=editable vendor · files=vendor-disallowed.exe
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไฟล์ไม่ activeและแสดง errorจริงของ implementation

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `vendor-disallowed.exe` | — | implementation แสดง validationชนิดไฟล์/`ERR_FILE_TYPE_NOT_ALLOWED` `⚠ HTML prototypeไม่ enforce` | ☐ |
| 2 | VERIFY attachment list | — | ไม่มี active row/downloadของไฟล์ต้องห้าม | ☐ |
| 3 | VERIFY storage/audit `(ต้อง simulate)` | — | ไม่มี public object; rejected attemptมี audit/correlationโดยไม่เก็บเนื้อหาใน log | ☐ |

### TC-F03 — Oversize/malware/scan failure (security negative)
- group: เอกสารแนบ · ความสำคัญ: สูง · trace: ERR_FILE_REJECTED / attachment scan failure
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=editable vendor + scanner test mode · files=vendor-oversize.pdf,vendor-eicar.txt
- Start: OPEN `#/vendors`
- ชุดข้อมูล: policy limitของ environment
- ผ่านเมื่อ: ทั้งสองไฟล์ไม่ active/downloadได้และไม่มี partial metadata

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `vendor-oversize.pdf` | — | เห็น errorเกินขนาดตาม environment; ไม่มี active attachment | ☐ |
| 2 | UPLOAD `vendor-eicar.txt` | — | scanner reject/`ERR_FILE_REJECTED`; ไม่มี active attachment | ☐ |
| 3 | VERIFY scanner timeout/failure `(ต้อง simulate)` | — | metadataไม่ active; UIแสดง error/pendingอย่างไม่หลอกว่า clean | ☐ |
| 4 | VERIFY orphan cleanup `(implementation)` | — | objectชั่วคราวถูก cleanupตาม job; ไม่มี public access | ☐ |

### TC-F04 — Duplicate attachment checksum (negative)
- group: เอกสารแนบ · ความสำคัญ: สูง · trace: ERR_DUPLICATE_ATTACHMENT
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=vendorมี `vendor-clean.pdf` activeแล้ว · files=vendor-clean-copy.pdf
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: duplicateถูก blockและยังมีหนึ่ง row

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY และจดจำนวนไฟล์ก่อน | — | บันทึก countฐาน N | ☐ |
| 2 | UPLOAD `vendor-clean-copy.pdf` | checksumเดียวกัน | เห็น duplicate error/409 `ERR_DUPLICATE_ATTACHMENT` | ☐ |
| 3 | VERIFY จำนวนไฟล์หลัง | — | ยัง N เท่ากับ step 1; ไม่มี rowซ้ำ | ☐ |

### TC-F05 — Soft-remove, missing/locked attachment และ retention
- group: เอกสารแนบ · ความสำคัญ: กลาง · trace: BR-VEN-23 / API-18 / ERR_ATTACHMENT_NOT_FOUND / BR_ATTACHMENT_LOCKED
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=editable vendorมี attachment activeและ locked fixtureอีก 1 · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: removeไม่ hard delete objectผิด policy; missing/lockedถูก reject

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **แก้ไข** | — | drawer editเปิด | ☐ |
| 2 | CLICK step/tab **เอกสารแนบ & ชำระ** | — | เห็นไฟล์ active | ☐ |
| 3 | CLICK ไอคอนลบไฟล์ active | — | ไฟล์หายจาก active formหลังยืนยัน/บันทึก | ☐ |
| 4 | VERIFY audit/history `(implementation)` | — | metadataถูก soft-removeและ auditมี actor/time | ☐ |
| 5 | VERIFY remove attachment idที่ไม่มี `(ต้อง simulate)` | — | 404 `ERR_ATTACHMENT_NOT_FOUND` | ☐ |
| 6 | VERIFY remove locked attachment `(ต้อง simulate)` | — | 422 `BR_ATTACHMENT_LOCKED`; active rowยังอยู่ | ☐ |
| 7 | VERIFY object retention `(implementation)` | OQ-04 policy | objectถูกเก็บ/ลบตาม policy ไม่ใช่ client hard deleteทันที | ☐ |

### Group R — Concurrency, Idempotency, Audit and Reliability

### TC-R01 — Stale aggregate edit first commit wins [AI-DEFAULT] (ต้อง simulate)
- group: Reliability · ความสำคัญ: สูง · trace: AC-18 / PR-2 / ERR_STALE_DATA `[AI-DEFAULT]`
- actor (role): Procurement Officer A และ B
- Setup: role=procurement_officerสอง session · seed=editable vendor version=5 · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: Aแก้ display name=`แก้โดย A`, Bแก้=`แก้โดย B`
- ผ่านเมื่อ: A commitเป็น version6, Bได้409, ค่าAไม่ถูกทับ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN vendorเดียวกันใน session A/B | — | ทั้งสอง detailเปิด | ☐ |
| 2 | VERIFY versionในทั้งสอง session | — | ทั้งสองเห็น version 5; จดค่าเดิม | ☐ |
| 3 | TYPE `แก้โดย A` → display nameใน A | — | ค่าใหม่แสดงใน form A | ☐ |
| 4 | CLICK **บันทึก (amend)** ใน A | — | Aสำเร็จ, versionเป็น6 | ☐ |
| 5 | TYPE `แก้โดย B` → display nameใน B | — | ค่าใหม่แสดงใน form Bที่ยัง version5 | ☐ |
| 6 | CLICK **บันทึก (amend)** ใน B | stale If-Match=5 | ⚠ ไม่พบใน HTML prototype: เห็น conflict/409 `ERR_STALE_DATA` และปุ่ม reload/resolve | ☐ |
| 7 | OPEN detailใหม่ | — | ค่าเป็น `แก้โดย A`, ไม่ใช่ B; version6 | ☐ |

### TC-R02 — Concurrent approval exactly one commit [AI-DEFAULT] (ต้อง simulate)
- group: Reliability · ความสำคัญ: สูง · trace: AC-10/18 / PR-1 / ERR_STALE_DATA `[AI-DEFAULT]`
- actor (role): Procurement Managerสอง session
- Setup: role=procurement_managerสอง session · seed=D-APPROVAL current step version=7 · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: requestแรกสำเร็จ, requestสอง 409, audit/stepมีครั้งเดียว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN D-APPROVAL ใน session A/B | — | ทั้งสองเห็น current stepเดียวกัน/version7 | ☐ |
| 2 | CLICK **อนุมัติขั้นนี้** ใน A | — | Aสำเร็จและ stepเลื่อนไป | ☐ |
| 3 | CLICK **อนุมัติขั้นนี้** ใน B | stale version | เห็น 409 stale/already decided; ไม่แสดง successซ้ำ | ☐ |
| 4 | VERIFY timeline | — | approved step/audit/eventมีหนึ่งครั้งเท่านั้น | ☐ |

### TC-R03 — Idempotent replay, lost response และ double-click [AI-DEFAULT] (resilience)
- group: Reliability · ความสำคัญ: สูง · trace: AC-02/18 / PR-4/PR-7 / idempotency cache 24h `[AI-DEFAULT]`
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=ไม่มีชื่อ/codeชุดทดสอบ; proxyตัด responseแรกหลัง commit · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: ชุด Aเปลี่ยนชื่อ=`บริษัท Idempotency QA จำกัด`
- ผ่านเมื่อ: retry same key/bodyคืนผลเดิม; มี vendor/audit/eventเดียว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK submit createสองครั้งเร็วๆ | same body/key | UIมี submitting stateและรับ actionเดียว | ☐ |
| 2 | WAIT responseแรกถูกตัดหลัง server commit | inject network loss | UIไม่ควรสร้าง recordซ้ำ | ☐ |
| 3 | CLICK retryหรือ replay same requestภายใน 24 ชั่วโมง | same Idempotency-Key/body | ได้ผลลัพธ์เดิม/codeเดิม | ☐ |
| 4 | TYPE ชื่อทดสอบ → ช่องค้นหา | — | เห็นหนึ่งแถวเท่านั้น | ☐ |
| 5 | VERIFY audit/event `(implementation)` | — | create auditและ`vendor_created_event`อย่างละหนึ่ง | ☐ |

### TC-R04 — Idempotency key เดิมแต่ body ต่าง (negative)
- group: Reliability · ความสำคัญ: สูง · trace: ERR_IDEMPOTENCY_CONFLICT
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=บันทึก responseของ key K/body Aแล้ว · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: body Bต่าง legal_name
- ผ่านเมื่อ: 409 conflictและไม่ mutate recordเดิม/ใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY baseline countและค่าจาก request A | — | จด count N และชื่อเดิม | ☐ |
| 2 | VERIFY replay key K ด้วย body B `(ต้อง simulate API)` | — | 409 `ERR_IDEMPOTENCY_CONFLICT` | ☐ |
| 3 | OPEN list/detail | — | countยัง N; ชื่อเดิมไม่ถูกเปลี่ยน | ☐ |

### TC-R05 — Permission revoked ขณะ drawerเปิด (security)
- group: Reliability · ความสำคัญ: สูง · trace: PR-3 / ERR_PERMISSION_REVOKED
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=editable vendor; adminสามารถ revoke roleระหว่างเคส · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: display nameใหม่=`ต้องไม่ถูกบันทึก`
- ผ่านเมื่อ: mutation re-check role, 403, stateไม่เปลี่ยน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **แก้ไข** | — | drawer editเปิด | ☐ |
| 2 | TYPE display nameใหม่ | — | drawerเก็บค่าชั่วคราว | ☐ |
| 3 | VERIFY admin revoke procurement role `(ต้อง simulate)` | — | sessionเดิมยังเปิด drawerแต่สิทธิ์ serverถูกถอด | ☐ |
| 4 | CLICK **บันทึก (amend)** | — | เห็น 403/`ERR_PERMISSION_REVOKED`; ไม่แสดง success | ☐ |
| 5 | OPEN detailด้วย authorized user | — | ค่าเดิมยังอยู่; ไม่มี success audit | ☐ |

### TC-R06 — Audit/outbox failure rollback [AI-DEFAULT] (ต้อง simulate)
- group: Reliability · ความสำคัญ: สูง · trace: AC-19 / BR-VEN-29/30 `[AI-DEFAULT]`
- actor (role): Procurement Officer
- Setup: role=procurement_officer · seed=D-ACTIVE; inject auditหรือoutbox write failure · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: block reason=`ทดสอบ rollback`
- ผ่านเมื่อ: business state/audit/event rollbackทั้งหมดและ logไม่มี PII

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY และจด status/versionก่อน | — | active/version N | ☐ |
| 2 | CLICK **บล็อก** | — | เห็นกล่องยืนยันและช่องเหตุผล | ☐ |
| 3 | TYPE reason → ช่องเหตุผล | `ทดสอบ rollback` | ช่องแสดงค่าที่กรอก | ☐ |
| 4 | CLICK ปุ่มยืนยันในกล่อง | inject audit failure | เห็น errorที่ observable; ไม่แสดง toast success | ☐ |
| 5 | OPEN detailใหม่ | — | statusยัง active, versionยัง Nเทียบ step1 | ☐ |
| 6 | VERIFY audit/event store | — | ไม่มี partial audit/outbox/status event | ☐ |
| 7 | VERIFY application logs | — | มี correlation id/error classแต่ไม่มี tax/bank/address/KYC note/full reason | ☐ |

### TC-R07 — Performance, engine invalid input และ observability [AI-DEFAULT]
- group: Reliability · ความสำคัญ: กลาง · trace: §6.6 / ENG_ERR_INVALID_INPUT `[AI-DEFAULT]`
- actor (role): authenticated test runner
- Setup: role=viewer + service test identity · seed=agreed staging dataset/telemetry enabled · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: SLO list/detail≤500ms, mutation≤1s(external excluded), eligibility≤200ms
- ผ่านเมื่อ: p95ตาม defaultหรือถูก mark blockedหาก platformยังไม่ยืนยัน; invalid engine inputไม่คืนผลมั่ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/vendors` ซ้ำตาม load plan | — | p95 list/detail≤500ms; UIไม่ค้างและ countถูก | ☐ |
| 2 | VERIFY local mutation timing `(ต้อง simulate)` | — | p95≤1s ไม่รวม external screening | ☐ |
| 3 | VERIFY API-19 timing `(ต้อง simulate)` | — | p95≤200ms | ☐ |
| 4 | VERIFY ENG-01 invalid input `(ต้อง simulate unit/contract)` | missing required field | `ENG_ERR_INVALID_INPUT`; ไม่คืน eligibility fabricated | ☐ |
| 5 | VERIFY telemetry | — | correlation id, latency, dependency healthและfailureมี โดยไม่มี PII | ☐ |

### Group X — Cross-Module Contracts

### TC-X01 — Price List summary read-only ของ vendorเดียวกัน (XT)
- group: Cross-module · ความสำคัญ: สูง · trace: XT-01 / E-002 / US-11
- actor (role): authenticated
- Setup: role=procurement_officer · seed=D-ACTIVE มี Price List active+expired itemsใน tenantเดียวกัน · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: tabแสดง summary vendorถูกคนและไม่มี CRUD

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK D-ACTIVE → tab **สินค้า/บริการ** | — | เห็น summary item/ราคา/หน่วย/สถานะของ D-ACTIVE | ☐ |
| 2 | VERIFY item active/expired | — | activeแสดงปกติ; non-activeแสดงสถานะ/visual inactive | ☐ |
| 3 | VERIFY actions | — | ไม่มี create/edit/delete Price Listใน Vendor Master | ☐ |
| 4 | CLICK **ดู Price List เต็ม →** | — | prototype toast **Feature Vendor Price List ยังไม่เปิดให้บริการ — Phase 2 (vendor: {vendorId})**; implementationนำไป moduleปลายทางพร้อม vendor_id | ☐ |

### TC-X02 — PO เลือกเฉพาะ eligible vendor และ default termตรง contract (XT, ต้อง simulate)
- group: Cross-module · ความสำคัญ: สูง · trace: XT-02 / E-007 / BR-VEN-27
- actor (role): PO creator
- Setup: role=ผู้สร้าง PO · seed=F-PO มี picker; D-ACTIVE eligible=true NET30 และ fixtures stateอื่น eligibility=false · files=—
- Start: OPEN หน้า create PO ของ environment `(downstream route ต้องระบุโดย F-PO)`
- ชุดข้อมูล: —
- ผ่านเมื่อ: pickerเลือกได้เฉพาะ active+KYC passedและ termตรง Vendor

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN หน้า create PO `(ต้อง simulate/downstream)` | — | vendor pickerโหลดจาก E-007/API-19 | ☐ |
| 2 | TYPE ชื่อ D-ACTIVE → vendor picker | — | D-ACTIVE selectable | ☐ |
| 3 | TYPE ชื่อ blocked/inactive/blacklisted/KYCไม่ผ่าน | — | รายการไม่ selectableหรือมี reasonที่ชัด; ไม่เปิดเผยข้อมูลเกินสิทธิ์ | ☐ |
| 4 | CLICK D-ACTIVE | — | default payment termใน POเป็น NET30ตรง contract | ☐ |

### TC-X03 — Last bank deactivated: PO true, Payment false (XT)
- group: Cross-module · ความสำคัญ: สูง · trace: XT-03 / Payment dependency / EC-VEN-13
- actor (role): Finance + Payment runner
- Setup: role=finance_officer · seed=D-ACTIVE non-OT verified bankใบสุดท้าย, downstream cache warm · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: reason=`ปิดบัญชีสำหรับ XT-03`
- ผ่านเมื่อ: Payment invalidatedและ PO eligibilityไม่เปลี่ยนเพราะ vendorยัง active/KYC passed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY และจด API-19 baseline | — | PO=true, Payment=true | ☐ |
| 2 | CLICK **ปิดใช้บัญชี** | — | เห็นกล่องยืนยันและช่องเหตุผล | ☐ |
| 3 | TYPE reason → ช่องเหตุผล | `ปิดบัญชีสำหรับ XT-03` | ช่องแสดงค่าที่กรอก | ☐ |
| 4 | CLICK ปุ่มยืนยันในกล่อง | — | bank disabledและvendorยังใช้งาน | ☐ |
| 5 | WAIT consumerรับ eligibility event | — | cache Paymentถูก invalidate | ☐ |
| 6 | VERIFY API-19/Payment | — | PO=true, Payment=falseพร้อม reason code; เทียบ baseline step1 | ☐ |

### TC-X04 — Block/Inactive/Blacklist กระทบธุรกรรมใหม่แต่ไม่ลบ history (XT)
- group: Cross-module · ความสำคัญ: สูง · trace: XT-04 / BR-VEN-28 / GR-VEN-01
- actor (role): authorized procurement
- Setup: role=procurement_director · seed=active vendors 3 ราย แต่ละรายมี historical PO/PV · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: เหตุผลทดสอบแต่ละ action
- ผ่านเมื่อ: downstreamหยุด new transactionหลัง event/lookupและ historyคงอยู่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY และจด historical PO/PV countต่อ vendor | — | จด countฐานของแต่ละราย | ☐ |
| 2 | CLICK block vendor1, inactive vendor2, blacklist vendor3 | เหตุผลครบ | ทั้งสาม stateเปลี่ยนตาม action | ☐ |
| 3 | WAIT status eventsถึง PO/PV | — | consumers refresh eligibility | ☐ |
| 4 | VERIFY สร้าง transactionใหม่ `(downstream)` | — | ทั้งสาม vendorถูก blockจากรายการใหม่ | ☐ |
| 5 | VERIFY historical records | — | countsเท่าค่าที่จด step1และ vendor_id/codeยังแสดง | ☐ |

### TC-X05 — Duplicate/out-of-order events ไม่ทำ state regress [AI-DEFAULT] (ต้อง simulate)
- group: Cross-module · ความสำคัญ: สูง · trace: XT-05 / event at-least-once `[AI-DEFAULT]`
- actor (role): integration test runner
- Setup: role=service test identity · seed=consumerเก็บ vendor version=10 blocked; event v9 active และ duplicate v10 queued · files=—
- Start: OPEN consumer test console `(ไม่มี routeใน Vendor HTML)`
- ชุดข้อมูล: events v9/v10
- ผ่านเมื่อ: consumer dedupด้วย event id/versionและไม่ย้อน blocked→activeจาก eventเก่า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY baseline consumer state/version | — | blocked/version10 | ☐ |
| 2 | VERIFY ส่ง duplicate event version10 `(ต้อง simulate)` | — | consumerไม่สร้างผลซ้ำ | ☐ |
| 3 | VERIFY ส่ง out-of-order event version9 active | — | consumerทิ้ง/ignore; stateยัง blocked/version10 | ☐ |
| 4 | VERIFY metrics/log | — | มี dedup/out-of-order metricโดยไม่มี PII | ☐ |

### TC-X06 — Price List/downstream unavailable ไม่สร้างข้อมูลปลอม (XT)
- group: Cross-module · ความสำคัญ: กลาง · trace: XT-06 / AC-20 / ERR_PRICE_LIST_UNAVAILABLE
- actor (role): authenticated
- Setup: role=procurement_officer · seed=D-ACTIVE; inject F-VENDOR-PRICE-LIST 503แล้ว empty success · files=—
- Start: OPEN `#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: unavailableชัดเจน, emptyจริงแยกจาก failure, ไม่มี mock fabricatedใน production

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK D-ACTIVE → tab **สินค้า/บริการ** | downstream 503 | ⚠ HTML prototypeมี mock: implementationแสดง unavailable/retryหรือ errorชัด ไม่แสดงรายการปลอม | ☐ |
| 2 | CLICK retry `(implementation)` | downstreamกลับ 200 empty | เห็น **ยังไม่มี Price List สำหรับคู่ค้านี้** | ☐ |
| 3 | VERIFY API-20 | — | 503 `ERR_PRICE_LIST_UNAVAILABLE`เมื่อ down; 200 empty summaryเฉพาะกรณีไม่มีรายการจริง | ☐ |

### Group LK — Scope Lock and Handoff Verification

### TC-LK01 — ยืนยันไม่มี Scope Lock เพิ่มเติม
- group: Scope Lock · ความสำคัญ: สูง · trace: LOCK-01
- actor (role): AI document reviewer
- Setup: role=document-reviewer · seed=FRD Pack v1.1 + conversation confirmations · files=—
- Start: OPEN `outputs/F-VENDOR/FRD_F-VENDOR_Pack/07_LOCKED_DECISIONS.md`
- ชุดข้อมูล: —
- ผ่านเมื่อ: scopeใช้ LOCK-01..05เท่านั้นและไม่มี constraintภายนอกถูกแต่งเพิ่ม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `07_LOCKED_DECISIONS.md` → §7.0 | — | เห็น LOCK-01 ระบุไม่มี Scope Lockเพิ่มเติม | ☐ |
| 2 | VERIFY Ledger/Test Cases ทั้งไฟล์ | — | ไม่มีเคสของ Out of Scope; ทุก in-scope itemมี case | ☐ |
| 3 | VERIFY Open Questions | — | OQถูกระบุเป็น dependency/default ไม่ถูกเปลี่ยนเป็นข้อยืนยันลูกค้า | ☐ |

### TC-LK02 — BRD v1.1 เป็นฐานและ Locked Decisions ชนะ drift
- group: Scope Lock · ความสำคัญ: สูง · trace: LOCK-02 / LD-02..LD-04/12
- actor (role): AI document reviewer
- Setup: role=document-reviewer · seed=BRD v1.1 + FRD v1.1 · files=—
- Start: OPEN `outputs/F-VENDOR/FRD_F-VENDOR_Pack/00_OVERVIEW.md`
- ชุดข้อมูล: —
- ผ่านเมื่อ: source precedenceชัดและไม่มีการนำ historical threshold/OT auto-approve/6-stateกลับมา

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `00_OVERVIEW.md` → Source precedence | — | user confirmations/Central Plan/approved HTMLมาก่อน historical BRD detail | ☐ |
| 2 | OPEN `07_LOCKED_DECISIONS.md` → LD-02/03/04/12 | — | Policy owns chain, OTไม่ auto-approve, 7 states, non-sanctions failกลับ pending_kyc | ☐ |
| 3 | VERIFY test cases TC-A05/06, TC-L05, TC-K03 | — | expectedตรง Locked Decisionsทั้งหมด | ☐ |

### TC-LK03 — HTML ล่าสุดเป็น UI source of truth
- group: Scope Lock · ความสำคัญ: สูง · trace: LOCK-03 / LD-01
- actor (role): AI document reviewer + browser agent
- Setup: role=viewer · seed=approved `vendor.html` + UI Brief v1.1 · files=—
- Start: OPEN `outputs/F-VENDOR/vendor.html#/vendors`
- ชุดข้อมูล: —
- ผ่านเมื่อ: route/visible anchors/modal typesตรง HTMLและ Test Casesไม่อ้างข้อความเก่า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/vendors` | — | title **ทะเบียนคู่ค้า**, subtitleและ routeตรง Meta | ☐ |
| 2 | VERIFY action/microcopyสำคัญ | — | เห็น **เงื่อนไขการชำระเงินเริ่มต้น**, rejectกลับแก้ KYC, bank reason modal, unblock gates | ☐ |
| 3 | VERIFY ข้อความต้องห้ามจาก driftเก่า | — | ไม่เห็น `PO ยังไม่พร้อม`, `รออนุมัติ (0/1)`, decision ref note, `กลับเป็นร่าง (draft)` | ☐ |
| 4 | OPEN `UI_BRIEF_F-VENDOR.md` → Drift Log | — | D-01..05/08/09/11/12/14เป็น RESOLVED; remaining gapsถูกระบุ | ☐ |

### TC-LK04 — Deliverable เป็นเอกสารเท่านั้น ไม่มี implementation
- group: Scope Lock · ความสำคัญ: สูง · trace: LOCK-04 / Out of Scope
- actor (role): AI document reviewer
- Setup: role=document-reviewer · seed=workspace outputs/F-VENDOR · files=—
- Start: OPEN `outputs/F-VENDOR/`
- ชุดข้อมูล: —
- ผ่านเมื่อ: deliverablesเป็น HTML prototype/Markdown docsเท่านั้นและไม่มี claimว่า implement productionแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `outputs/F-VENDOR/` | — | พบ `vendor.html`, FRD Pack, UI Brief, Test Case MD | ☐ |
| 2 | VERIFY Meta/Overview scope | — | ระบุไม่มี codebaseและเอกสารส่งต่อ AI Coding Agent | ☐ |
| 3 | VERIFY simulated cases | — | backend/security/integration gapsติด `(ต้อง simulate)`/`⚠ ไม่พบใน HTML` ไม่อ้างว่า prototypeทำแล้ว | ☐ |

### TC-LK05 — Workflow ไม่ใช้ plan-from-spec
- group: Scope Lock · ความสำคัญ: สูง · trace: LOCK-05
- actor (role): AI document reviewer
- Setup: role=document-reviewer · seed=FRD/Test Case document controls · files=—
- Start: OPEN `outputs/F-VENDOR/FRD_F-VENDOR_Pack/07_LOCKED_DECISIONS.md`
- ชุดข้อมูล: —
- ผ่านเมื่อ: handoff flowอ้างเฉพาะ six-skill workflowที่ผู้ใช้กำหนดและไม่มี plan-from-spec artifact

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN §7.0 | — | section Scope Lockแสดง | ☐ |
| 2 | VERIFY LOCK-05 | — | เห็นข้อยืนยันห้ามใช้ `plan-from-spec` | ☐ |
| 3 | VERIFY document controls/outputs | — | generatorระบุ html-generator-v6, frd-generator-v6, html-ui-brief, ai-testcase-md-generatorตามขั้น; ไม่มี outputจาก plan-from-spec | ☐ |
| 4 | VERIFY next handoff | — | ขั้นถัดไปคือ qa-friendly-html-generatorรับไฟล์นี้แบบ 1:1 | ☐ |

## วิธีที่ agent รัน (Run protocol)

1. อ่าน `Meta`, `Data Sets`, `Files` และ `Setup` ของเคสก่อนเปิดระบบ
2. เริ่มทุกเคสจาก `Start` ใหม่; ห้ามพึ่ง stateค้างจากเคสก่อน
3. ใช้ role/tenant/seedตาม `Setup`; หากไม่มี seed/failure injection ให้รายงาน `blocked` ไม่เดาผล
4. ทำ actionตามลำดับทีละ stepและติ๊ก `☐` เป็น pass/fail
5. Expected ที่มี `⚠ ไม่พบใน HTML` ต้องตรวจบน implementationจริง; ถ้าข้อความจริงต่าง ให้บันทึก verbatimใน `evidence`
6. เคส `(ต้อง simulate)` ต้องใช้ API proxy, test double, DB fixture, event harness หรือ downstream sandboxตามที่ Setupกำหนด
7. ห้ามใช้ production PII, bank account, sanctions evidence หรือไฟล์จริง
8. หลัง fail หยุดเคสนั้นที่ failed step, เก็บสิ่งที่เห็นจริง/route/role/correlation id แล้วเริ่มเคสถัดไปด้วย seedใหม่
9. เคส `[AI-DEFAULT]` ที่ fail ต้อง triageทั้ง implementationและความเหมาะสมของ defaultกับ BA/owner
10. ส่งผลตาม JSON schemaท้ายไฟล์ โดย summary totalต้องเท่ากับ 91

## Coverage Audit

| หมวด | covered / total | หลักฐาน |
|---|---:|---|
| Acceptance criteria / FR (06_TESTS) | 20 / 20 | TC-L01..TC-X06 |
| Test inventoryเดิม | 28 / 28 | mappedใน AC/กลุ่มที่เกี่ยวข้อง |
| Business rules (05_RULES) | 30 / 30 | Ledger BR-VEN-01..30 |
| BRD-confirmed edge cases | 13 / 13 | Ledger EC-VEN-01..13 |
| Activated probes/default/additional edge | 12 / 12 | PR-1/2/3/4/6/7 + additional 6 |
| Error catalog (05_RULES) | 33 / 33 | Ledger Error Codes |
| Cross-file error codesเพิ่มเติม | 4 / 4 | ERR_FIELD_ACCESS_DENIED, BR_VENDOR_NOT_EDITABLE, BR_VENDOR_NOT_READY, BR_ATTACHMENT_LOCKED |
| Validation schema | 14 / 14 | Ledger Validation Schema |
| Permission cells | 70 / 70 | 10 capabilities × 7 roles |
| UI states | 6 / 6 | loaded, empty, filtered-empty, loading, error, read-only |
| Vendor/KYC/Bank state rows | 23 / 23 | vendor 13 + KYC 5 + bank 5 |
| Integration events | 7 / 7 | created, KYC submitted/decided, approval submitted/decided, status, payment eligibility |
| Cross-Module (XT) | 6 / 6 | TC-X01..TC-X06 |
| Scope Lock (LOCK) | 5 / 5 | TC-LK01..TC-LK05 |
| `[AI-DEFAULT]` source items | 9 / 9 | 8 case headers: TC-C16, K07, R01, R02, R03, R06, R07, X05; BR-VEN-30 และ shared audit boundary co-covered by TC-R06 |

- **Manifest cross-check (FRD §0.12): ✅ 50/50** — Stories 11 + BRD Rules 26 + Edge Cases 13
- **Case count cross-check: ✅ 91/91**
- **Ledger-first gate: ✅ ทุก in-scope itemมี case**
- เคสที่ต้อง simulateยังนับ covered เพราะมี Setup/Expectedครบ; หาก environment injectไม่ได้ให้รายงาน `blocked`

### ข้าม (พร้อมเหตุผล)

- Price List CRUD — นอกขอบเขต; ทดสอบใน F-VENDOR-PRICE-LIST
- PO/PV creation/payment execution — นอกขอบเขต; Vendorทดสอบเฉพาะ eligibility/consumer contract
- PDF A4 — LD-11 ระบุไม่มี artifact
- Bulk import/export, merge/split — Phase 2/OOS
- Vendor portal — Phase 3+
- Performance scoring — separate feature
- KYC expiry — OQ-02 ยังไม่กำหนด policy จึงห้ามสร้าง expected transition
- Exact sanctions provider/SLA — OQ-01; TC-K07ตรวจ conservative timeout behaviorเท่านั้น
- Exact attachment limit/type/retention — OQ-04; TC-F02..F05ใช้ policyของ environment

## Result Report (schema)

```json
{
  "feature_id": "F-VENDOR",
  "testcase_version": "1.0",
  "run_at": "<iso datetime>",
  "environment": "<name>",
  "results": [
    {
      "id": "TC-L01",
      "status": "pass|fail|blocked",
      "failed_step": null,
      "evidence": "",
      "note": ""
    }
  ],
  "summary": {
    "total": 91,
    "pass": 0,
    "fail": 0,
    "blocked": 0
  }
}
```

`evidence` ต้องเป็นสิ่งที่ agentเห็นจริง เช่นข้อความ error verbatim, route, ป้ายสถานะ, role และ correlation id; ห้ามใส่ production PII/Restricted values

# AI Test Cases — F-PG GL Posting Group

ชุดทดสอบสำหรับ AI agent (browser-use / vision) อ่านแล้วลงมือทดสอบบนหน้าจอจริงของ `f-postgrp.html`
แล้วรายงานผลกลับตามสคีมาท้ายไฟล์. ทุกเคส independent — เริ่มจาก `Start` ของตัวเอง.

**⚠️ Routing note (สำคัญ):** `f-postgrp.html` เป็น single-page SPA แบบ **component-state routing**
(`state.tab`, `state.drawer.mode`, `state.modal.type`) — **ไม่มี** hash route (`#/...`) ที่ลิงก์ตรงได้
ทุกเคสจึงระบุ `Start` เป็นลำดับ "เปิดหน้า → คลิกอะไรเพื่อไปถึง state ที่ต้องการ" แทน URL

**⚠️ Permission-testing limitation (พบระหว่างอ่าน HTML):** มุมบนขวาของหน้าแสดงชื่อผู้ใช้ตายตัว
`"Tadswan C. · Finance Lead"` — ไม่มี UI สำหรับสลับ role เป็น Auditor ในม็อคนี้ ดังนั้นเคสกลุ่ม
Permission (P) ที่ต้องใช้ role=Auditor **ไม่สามารถยืนยันผ่าน UI ของม็อคไฟล์นี้ได้โดยตรง** —
สมมติว่า runner มี environment จริงที่ login สลับ role ได้ (ตามที่ 06_TESTS §6.3 ระบุ `qa_auditor`)
ทุกเคสกลุ่ม P จะติดธง `⚠ ยืนยัน anchor` และระบุไว้ใน Setup

## Meta

| คีย์ | ค่า |
|---|---|
| Feature ID | F-PG (F-0.19, Finance Foundation) |
| ชื่อฟีเจอร์ | GL Posting Group — Specific Posting Groups (tab 1) + General Posting Setup (tab 2) |
| เวอร์ชัน | FRD 1.0 (2026-08-10), STANDARD variant · BRD v1.0 APPROVED |
| App entry | Sidebar → module "การเงิน" → เมนู "GL Posting Group" (`data-feature="posting-group"`) — ไม่มี hash route |
| "Routes" (state, ไม่ใช่ URL) | `state.tab='groups'│'setup'` · `openDrawer('create-group'│'edit-group'│'create-setup'│'edit-setup'│'view-group'│'view-setup', id?)` · `openModal('import'│'bulk-delete')` |
| ที่มา | FRD_F-PG_Pack (00_OVERVIEW, 01_UI, 02_API, 03_LOGIC, 04_DB, 05_RULES, 06_TESTS) · BRD_F-PG_GL-Posting-Group.md v1.0 · `f-postgrp.html` (source of truth ข้อความ, Mode A) |
| Scope boundary (ย้ำ) | **ไม่รวม** VAT Posting Setup (tab 3, OQ-PG-01) และ **ไม่รวม** product-axis 6-value ของ Item Master (OQ-PG-04) — ทั้งสอง deferred ไป Phase 2 lane pass ยังไม่มีใน HTML/FRD ปัจจุบัน |
| จำนวน | 80 เคส · 14 กลุ่ม |

## Coverage

| กลุ่ม (group) | เคส | ความสำคัญเด่น |
|---|---|---|
| G · สร้าง Specific Posting Group (tab1, P-02) | TC-G01..G09 | สูง |
| E · แก้ไข Specific Posting Group (tab1, P-02) — IR-PG-01 vs R05 | TC-E01..E08 | สูง (critical) |
| S · สร้าง General Posting Setup (tab2, P-03) | TC-S01..S05 | สูง |
| ES · แก้ไข General Posting Setup (tab2, P-03) — IR-PG-01 pair-lock | TC-ES01..ES05 | สูง (critical) |
| ST · เปลี่ยนสถานะ อิสระ ไม่มีอนุมัติ (P-04/P-05/P-01) | TC-ST01..ST04 | สูง |
| BLK · Bulk delete skip used>0 (P-01/P-07) | TC-BLK01..BLK04 | สูง |
| IMP · นำเข้า CSV merge-only (P-06) | TC-IMP01..IMP08 | สูง (critical) |
| EXP · ส่งออก CSV (P-01) | TC-EXP01..EXP03 | กลาง |
| L · รายการ/ค้นหา/กรอง/สลับ tab (P-01) | TC-L01..L08 | กลาง-สูง |
| COA · COA dropdown filter accuracy (§2.5) | TC-COA01..COA05 | สูง |
| FN · Negative-absence: FN-40 banned items + Scope Lock verify | TC-FN01..FN08 | สูง (compliance) |
| P · Permission matrix (Finance Lead vs Auditor) | TC-P01..P04 | สูง (⚠ mock limitation) |
| XT · Cross-module (06_TESTS §6.9) | TC-XT01..XT04 | กลาง (ต้อง simulate) |
| UX · Interaction (dirty-close/Esc/busy-state) | TC-UX01..UX05 | กลาง |

---

## Coverage Ledger

### FR / User Stories (BRD §7, cross-checked 06_TESTS §6.1 AC)
| item | cases |
|---|---|
| S-01 / AC-01 Create Specific Posting Group (happy) | TC-G01, TC-G02 |
| S-02 / AC-04 Create General Posting Setup (happy) | TC-S01 |
| S-03 / AC-06 Edit, `used=0` | TC-E01, TC-ES01 |
| S-04 / AC-07,08,08b Edit, `used>0` (IR-PG-01 + R05) | TC-E02..E06, TC-ES02..ES05 |
| S-05 / AC-02,03,05 Validation errors | TC-G03..G07, TC-S02, TC-S03, TC-S05 |
| S-06 / AC-09 Free status change, no approval | TC-ST01, TC-ST02 |
| S-07 / AC-10 Bulk delete, skip used>0 | TC-BLK01..BLK04 |
| S-08 / AC-11..14 Import CSV merge-only | TC-IMP01..IMP06, TC-IMP08 |
| S-09 / AC-15 Export CSV roundtrip | TC-EXP01..EXP03 |
| AC-16 COA resolver filter accuracy | TC-COA01..COA03 |
| AC-17 `kind` immutable, no UI path | TC-E03, TC-E04, TC-FN03 |
| AC-18 Kind-change clears accounts (create only) | TC-G08 |

### Business Rules (05_RULES §5.1)
| rule | cases |
|---|---|
| BR-01/R01/R02 account type+leaf+postable+active match | TC-G01, TC-G02, TC-COA01..COA03, TC-G07(⚠ simulate) |
| BR-02/R03 code unique (tab1) | TC-G06 |
| BR-02/R04 combination unique (tab2) | TC-S03 |
| BR-03/R05 kind locked always, independent of `used` | TC-E03, TC-E04 |
| BR-03b/R07 clear account fields on kind-change pre-submit | TC-G08 |
| BR-04/R06 no delete when used>0, bulk skip+report | TC-BLK01, TC-BLK02, TC-FN02 |
| BR-05/IR-PG-01 partial lock code(tab1)/combination(tab2) only | TC-E02, TC-E05, TC-E06, TC-ES02, TC-ES03, TC-ES05 |
| BR-06 free 3-state transitions, no approval | TC-ST01, TC-ST02, TC-ST03, TC-ST04 |
| BR-07 import merge-only, blank status→draft | TC-IMP01, TC-IMP03, TC-FN01 |
| BR-08 no GL posting (mapping layer only) | TC-FN06 |
| R09 bus/prod value set DYNAMIC, as-built 2-value only | TC-FN05, TC-XT01(⚠ simulate) |
| Tax mapping gap (WARNING, no tab3) | TC-FN04 |

### Edge Cases — BA-confirmed (05_RULES §5.5, BRD §10.1)
| EC | cases / สถานะ |
|---|---|
| EC-01 code blank/duplicate | TC-G03, TC-G06 |
| EC-02 name_th blank | TC-G04 |
| EC-03 required primary account blank | TC-G05 |
| EC-04 (bus,prod) duplicate | TC-S03 |
| EC-05 used>0 attempt change code/combination | TC-E02, TC-ES02 |
| EC-06 kind changed before submit | TC-G08 |
| EC-07 bulk-delete includes used>0 | TC-BLK01 |
| EC-08 import row invalid | TC-IMP02, TC-IMP06 |
| EC-09 import row blank status | TC-IMP03 |
| EC-10 tab switch clears selection+filter | TC-L02 |

### Edge Cases — AI-pattern / Lane Mode (05_RULES §5.5, BRD §10.2) — all `[AI-DEFAULT]` where a case exists
| ID | Lane Mode disposition | Case |
|---|---|---|
| DI-01 | No auto-warning banner built — ข้าม (ไม่มีผลสังเกตได้บน UI, ต้อง COA reverse-lookup job นอก scope) | — ข้าม |
| DI-02 | Soft-ref only, no cascade — ข้าม (mitigation อยู่ที่ F-COA-001 ไม่ใช่ feature นี้) | — ข้าม |
| DI-03 | Live-lookup COA name display (no snapshot) | TC-COA05 (สังเกตผ่าน view drawer ปรกติ, ไม่ใช่เคสใหม่แยก) |
| DI-04 | sdd-empty generic "ไม่พบรายการ", ไม่มี reason-for-filter message | TC-COA04 `[AI-DEFAULT]` |
| CA-01 | Optimistic lock (`version`+`If-Match`) — backend/networked only, ไม่มีผลสังเกตบน mock client-array | — ข้าม (Phase 2.5 backend, ไม่มีสัญญาณ UI ให้ agent เห็น) |
| CA-07 | DB UNIQUE constraint race guard — backend/DB level เท่านั้น | — ข้าม (ไม่มี UI signal, ต้อง DB-level test) |
| ST-02 | Left unconfirmed — BR-06 อนุญาต revert active→draft บน used สูงได้โดยไม่มี warning เพิ่ม | TC-ST03 `[AI-DEFAULT]` |
| ST-04 | Left unconfirmed — ตั้ง inactive บน used สูงได้โดยไม่มี warning เพิ่ม | TC-ST04 `[AI-DEFAULT]` |
| PM-03 | Server-side role re-check ทุก mutation endpoint — API-level, ไม่มีปุ่ม/route ให้ agent เรียกตรงบน UI | — ข้าม (backend concern only, ไม่มี UI ให้กด) |
| PM-04 | Multi-company/branch scoping — left unconfirmed, ไม่มีอะไรเพิ่มจาก tenant-level RLS เดิม | — ข้าม (ไม่มี UI element ให้ทดสอบ) |
| FU-01 | Cap ไฟล์ (5MB/5000 แถว) — เป็น placeholder ที่ยังไม่ยืนยันเลข ไม่ได้ enforce จริงใน mock | — ข้าม (ไม่มี validation ให้สังเกตใน mock ปัจจุบัน; ผูก TC-IMP07 กรณีอนาคต enforce) |
| FU-02 | Validate เนื้อหาไฟล์จริง ไม่ใช่แค่ extension, parse-and-fail gracefully | TC-IMP08 `[AI-DEFAULT]` |

### Error Catalog (05_RULES §5.6)
| error | cases |
|---|---|
| `BR_FIELD_REQUIRED` | TC-G03, TC-G04, TC-G05, TC-S02 |
| `BR_CODE_DUPLICATE` | TC-G06 |
| `BR_COMBINATION_DUPLICATE` | TC-S03 |
| `BR_KIND_LOCKED` | TC-E03, TC-E04 (⚠ server-side assertion, ไม่มี UI path ให้ agent ยิง PUT ตรง — ยืนยันผ่านการไม่มี input ให้กด) |
| `BR_CODE_LOCKED_USED` | TC-E02 |
| `BR_COMBINATION_LOCKED_USED` | TC-ES02 |
| `BR_ACCOUNT_TYPE_MISMATCH` | TC-G07 (⚠ ต้อง simulate — dropdown pre-filter กันไว้แล้ว เลือกผิดประเภทไม่ได้ผ่าน UI) |
| `BR_ACCOUNT_NOT_LEAF_OR_INACTIVE` | — ข้าม (mock COA_ACCOUNTS ทั้ง 16 ตัวเป็น leaf+active หมด ไม่มีตัวอย่าง inactive ให้เลือกทดสอบผ่าน UI นี้; รอ ENG-PG-01 ต่อ COA จริง) |
| `BR_USED_GT_ZERO` (bulk skip, ไม่ใช่ error) | TC-BLK01, TC-BLK02 |
| `ERR_NOT_AUTHENTICATED` | — ข้าม (auth layer ทั่วระบบ, ไม่ใช่ของ feature นี้) |
| `ERR_INSUFFICIENT_ROLE` | TC-P04 (⚠ ข้าม — backend/API only, ไม่มี UI ให้กด) |
| `ERR_NOT_FOUND` | — ข้าม (ไม่มี deep-link ID ให้พิมพ์ตรงในม็อค state-routing นี้) |
| `ERR_DUPLICATE_IDEMPOTENCY_KEY` | — ข้าม (header-level, backend, ไม่มีผลสังเกตบน client-array mock) |
| `ERR_STALE_DATA` | — ข้าม (ผูกกับ CA-01 optimistic lock ที่ข้ามแล้ว) |

### Permission Matrix (05_RULES §5.3)
| cell | cases |
|---|---|
| Finance Lead: view/create/edit/bulk/import/export = allow | TC-P01 |
| Finance Lead: change kind = deny (locked always) | TC-E03, TC-E04 |
| Finance Lead: edit code/combination when used>0 = deny | TC-E02, TC-ES02 |
| Auditor: view/export = allow; create/edit/bulk/import = deny | TC-P02, TC-P03 (⚠ ยืนยัน anchor — mock ไม่มี role switch) |
| System: non-Finance direct API call = 403 | TC-P04 — ข้าม (backend-only, ไม่มี UI) |

### Cross-Module (XT — 06_TESTS §6.9)
| XT | Downstream | Case |
|---|---|---|
| XT-01 | Item Master `GET /gl/posting-groups?type=product` → 2-value gap | TC-XT01 (ต้อง simulate — API call, ไม่มีหน้า Item Master ให้คลิกใน pack นี้) |
| XT-02 | Item Master `GET /gl/vat-groups` → `[]` + gap meta | TC-XT02 (ต้อง simulate) |
| XT-03 | GL/Journal Engine — edit account_1 บน used>0 แล้ว post ใหม่ resolve บัญชีใหม่ ของเก่าไม่ย้อน | TC-XT03 (ต้อง simulate — ไม่มี document module ในมัคนี้) |
| XT-04 | GL/Journal Engine — set inactive แล้ว post ใหม่ resolve ไม่ได้ | TC-XT04 (ต้อง simulate) |

### Scope Lock (LOCK — 00_OVERVIEW §0.11 / BRD §3.4)
| LOCK-ID | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| LOCK-01 | IR-PG-01: used>0 ล็อกเฉพาะ code(tab1)/combination(tab2) | TC-E02, TC-E05, TC-E06, TC-ES02, TC-ES03, TC-ES05 |
| LOCK-02 | kind ล็อกหลังสร้างเสมอ ไม่ขึ้นกับ used | TC-E03, TC-E04, TC-FN03 |
| LOCK-03 | Import merge-only เท่านั้น ห้ามมีโหมด Replace | TC-FN01, TC-IMP04(รวมใน FN01) |
| LOCK-04 | 3 สถานะอิสระ ทุกทิศ ไม่มีอนุมัติ | TC-ST01, TC-ST02, TC-FN07 |
| LOCK-05 | ไม่ post บัญชีเอง — feature นี้เป็น mapping layer เท่านั้น | TC-FN06 |

### Scope Boundary — Out-of-scope verify (task instruction, not built)
| item | ข้าม/หมายเหตุ |
|---|---|
| OQ-PG-01 VAT Posting Setup (tab 3) | — ห้ามสร้างเคส (deferred Phase 2, ยังไม่ build) — ยืนยันการ "ไม่มี" ผ่าน TC-FN04 แทน (เป็นเคส negative-absence ไม่ใช่เคสทดสอบ tab3) |
| OQ-PG-04 product-axis 6-value (Item Master set) | — ห้ามสร้างเคส (deferred Phase 2) — ยืนยัน as-built 2-value (GOODS/SERVICE) ผ่าน TC-FN05/TC-S01 แทน |

### Cross-cutting / Events / States
| item | cases |
|---|---|
| empty state (list, ทั้ง 2 tab) | TC-L06 |
| tab switch clears bulk selection + status filter | TC-L02 |
| loading/error state (async, ไม่มีใน mock client-array) | — ข้าม (01_UI §1.2 P-01 ระบุ "ต้อง add ตอน implement จริง" ไม่มีใน mock ให้ agent สังเกต) |
| submitting/busy state (spinner + text) | TC-UX03, TC-UX04, TC-UX05 |
| audit log (S01-07) | — ข้าม (ไม่มี audit-log viewer UI ในฟีเจอร์นี้ ให้ agent เปิดดู — backend-only artifact) |

---

## Data Sets

### Seed data (as-built มัคปัจจุบัน — ต้องมีก่อนทุกเคสเริ่ม, มีอยู่แล้วใน `f-postgrp.html` โดย default)

**Tab 1 — Posting Groups (7 แถว):**
| code | kind | ชื่อ | status | used |
|---|---|---|---|---|
| LOCAL | vendor (เจ้าหนี้) | เจ้าหนี้ในประเทศ | ใช้งาน | 82 |
| FOREIGN | vendor | เจ้าหนี้ต่างประเทศ | ใช้งาน | 14 |
| FINISHED | inventory (สินค้าคงคลัง) | สินค้าสำเร็จรูป | ใช้งาน | 57 |
| KBANK | bank (ธนาคาร) | ธนาคารกสิกรไทย | ใช้งาน | **203** (สูงสุด — ใช้กับ ST-02/ST-04 edge) |
| DOMESTIC-C | customer (ลูกหนี้) | ลูกค้าในประเทศ | ใช้งาน | 120 |
| SCB | bank | ธนาคารไทยพาณิชย์ (เตรียมใช้) | ร่าง | **0** (used=0 — ใช้กับเคส edit ที่ต้องแก้ code ได้) |
| SCRAP | inventory | เศษซาก (เลิกใช้) | ไม่ใช้งาน | 6 |

**Tab 2 — General Posting Setup (3 แถว):**
| bus | prod | sales_acct | purchase_acct | cogs_acct | status | used |
|---|---|---|---|---|---|---|
| DOMESTIC | GOODS | 4-1-10 | 5-1 | 5-1 | ใช้งาน | 340 |
| DOMESTIC | SERVICE | 4-1-20 | 5-1 | 5-1 | ใช้งาน | 88 |
| FOREIGN | GOODS | 4-1-10 | 5-1 | 5-1 | ร่าง | **0** |

> ⚠️ combination ที่ยังไม่มีในทะเบียน (ใช้สร้างใหม่ได้): **FOREIGN × SERVICE**

**COA mock accounts (16 รายการ, จาก `COA_ACCOUNTS` ใน HTML):**
| code | name | type |
|---|---|---|
| 1-1-10-01 | เงินสดในมือ | asset |
| 1-1-10-02 | เงินฝากธนาคาร - กระแสรายวัน | asset |
| 1-1-10-03 | เงินฝากธนาคาร - ออมทรัพย์ | asset |
| 1-1-20-01 | ลูกหนี้การค้า | asset |
| 1-1-30-01 | สินค้าสำเร็จรูป | asset |
| 1-1-40 | ภาษีซื้อ | asset |
| 2-1-10-01 | เจ้าหนี้การค้า | liability |
| 2-1-10-02 | เจ้าหนี้อื่น | liability |
| 2-1-20 | ภาษีขาย | liability |
| 2-1-30 | เงินมัดจำรับล่วงหน้า | liability |
| 4-1-10 | รายได้จากการขาย | income |
| 4-1-20 | รายได้ค่าบริการ | income |
| 4-2 | รายได้อื่น | income |
| 5-1 | ต้นทุนขาย | expense |
| 5-2-10-01 | เงินเดือน | expense |
| 5-2-20 | ค่าสาธารณูปโภค | expense |

### A — สร้าง Posting Group ประเภท vendor ถูกต้อง (happy)
| ฟิลด์ | ค่า |
|---|---|
| ประเภทกลุ่ม (kind) | เจ้าหนี้ (Vendor) |
| รหัสกลุ่ม (code) | TEST-VEN |
| ชื่อกลุ่ม (TH) | เจ้าหนี้ทดสอบ |
| ชื่อกลุ่ม (EN) | Test Vendor |
| บัญชีเจ้าหนี้ (AP control) | 2-1-10-02 เจ้าหนี้อื่น (liability) |
| บัญชีภาษีซื้อ (Input VAT) | 1-1-40 ภาษีซื้อ (asset) |
| สถานะ | ใช้งาน |

### B — สร้าง Posting Group ประเภท bank ถูกต้อง (happy, 1 field เท่านั้น)
| ฟิลด์ | ค่า |
|---|---|
| ประเภทกลุ่ม (kind) | ธนาคาร (Bank) |
| รหัสกลุ่ม (code) | TEST-BANK |
| ชื่อกลุ่ม (TH) | ธนาคารทดสอบ |
| บัญชีเงินฝาก (GL) | 1-1-10-01 เงินสดในมือ (asset) |
| สถานะ | ร่าง |

### C — สร้าง Posting Group ผิด (negative)
| ฟิลด์ | ค่า |
|---|---|
| รหัสกลุ่ม | (เว้นว่าง) |
| ชื่อกลุ่ม (TH) | (เว้นว่าง) |
| รหัสซ้ำ (ใช้ทดสอบ dup) | LOCAL (ซ้ำกับ seed g1) |

### D — สร้าง General Posting Setup ถูกต้อง (happy, combination ใหม่)
| ฟิลด์ | ค่า |
|---|---|
| กลุ่มธุรกิจ (bus) | FOREIGN |
| กลุ่มสินค้า (prod) | SERVICE |
| บัญชีรายได้ (Sales) | 4-1-20 รายได้ค่าบริการ (income) |
| บัญชีซื้อ (Purchase) | 5-1 ต้นทุนขาย (expense) |
| บัญชีต้นทุนขาย (COGS) | 5-1 ต้นทุนขาย (expense) |
| สถานะ | ใช้งาน |

### E — สร้าง General Posting Setup ซ้ำ (negative)
| ฟิลด์ | ค่า |
|---|---|
| กลุ่มธุรกิจ | DOMESTIC (ซ้ำกับ s1) |
| กลุ่มสินค้า | GOODS (ซ้ำกับ s1) |

### ไฟล์ทดสอบ (Files) — runner เตรียมตามชื่อ+เนื้อหานี้ก่อนรัน (encode UTF-8 with BOM)

| ไฟล์ | เนื้อหา (คอลัมน์ตาม template จริงจาก HTML) | ใช้ในเคส |
|---|---|---|
| `pg_groups_valid.csv` | header `code,kind,name_th,name_en,account_1,account_2,status`<br>แถว1: `NEWBANK,bank,ธนาคารทดสอบ,Test Bank,1-1-10-01,,ใช้งาน`<br>แถว2: `NEWCUST,customer,ลูกค้าทดสอบ,Test Customer,1-1-20-01,2-1-20,ร่าง` | TC-IMP01 |
| `pg_groups_mixed.csv` | **= ไฟล์เดียวกับที่ปุ่ม "ดาวน์โหลด template ตัวอย่าง" สร้างให้ (tab groups)** — 5 แถว: `IMPORT-V`(valid) / `RAW`(valid, status ว่าง) / `BBL`(valid) / `LOCAL`(dup code) / `BAD1`(bad status "พร้อมใช้") | TC-IMP02, TC-IMP03, TC-IMP07 |
| `pg_setup_valid.csv` | header `bus,prod,sales_acct,purchase_acct,cogs_acct,status`<br>แถว1: `FOREIGN,SERVICE,4-1-20,5-1,5-1,ใช้งาน` | TC-IMP05 |
| `pg_setup_mixed.csv` | **= ไฟล์เดียวกับปุ่ม template (tab setup)** — 3 แถว: `FOREIGN,SERVICE`(valid) / `DOMESTIC,GOODS`(dup combination) / `FOREIGN,GOODS`(dup combination + บัญชี 9-9-99 ไม่มีใน COA) | TC-IMP06 |
| `not_a_valid.csv` | เนื้อหาไม่ใช่ CSV โครงสร้างข้อมูล — plain prose: `นี่ไม่ใช่ไฟล์ CSV ที่ถูกต้อง ไม่มีคอลัมน์ที่ตรงกับ template เลย` (บรรทัดเดียว ไม่มี comma คั่นคอลัมน์) | TC-IMP08 |

---

## Test Cases

### กลุ่ม G — สร้าง Specific Posting Group (Tab 1, P-02)

#### TC-G01 — สร้าง Posting Group ประเภท vendor ครบฟิลด์ (happy)
- group: G · ความสำคัญ: สูง · trace: S-01/AC-01 / BR-01(R01,R02)
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— (ใช้ seed ปกติ 7 กลุ่ม) · files=—
- Start: OPEN หน้า "GL Posting Group" (ค่าเริ่มต้นอยู่ tab **Posting Groups**)
- ชุดข้อมูล: A
- ผ่านเมื่อ: บันทึกได้ + toast "สร้าง Posting Group แล้ว" + drawer ปิด + แถวใหม่ TEST-VEN ปรากฏในตาราง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **"เพิ่ม Posting Group"** | — | drawer 920px เปิด หัวข้อ **"เพิ่ม Posting Group"**; ช่อง "ประเภท Posting Group" ว่าง (placeholder "— เลือกประเภท —") | ☐ |
| 2 | SELECT "เจ้าหนี้ (Vendor)" → ช่อง **"ประเภท Posting Group"** | A | render ช่องบัญชี 2 ช่อง: "บัญชีเจ้าหนี้ (AP control)" + "บัญชีภาษีซื้อ (Input VAT)" | ☐ |
| 3 | TYPE → ช่อง **"รหัสกลุ่ม (Code)"** | A: TEST-VEN | ช่องแสดงตัวพิมพ์ใหญ่ `TEST-VEN` (auto-uppercase) | ☐ |
| 4 | TYPE → ช่อง **"ชื่อกลุ่ม (TH)"** | A | ช่องแสดงค่าที่กรอก | ☐ |
| 5 | TYPE → ช่อง **"ชื่อกลุ่ม (EN)"** | A | ช่องแสดงค่าที่กรอก | ☐ |
| 6 | SELECT "2-1-10-02 เจ้าหนี้อื่น" → ช่อง **"บัญชีเจ้าหนี้ (AP control)"** | A | ช่อง sdd แสดง `2-1-10-02` + ชื่อบัญชี | ☐ |
| 7 | SELECT "1-1-40 ภาษีซื้อ" → ช่อง **"บัญชีภาษีซื้อ (Input VAT)"** | A | ช่อง sdd แสดง `1-1-40` + ชื่อบัญชี | ☐ |
| 8 | VERIFY ช่อง "สถานะ" | — | default = "ใช้งาน" | ☐ |
| 9 | CLICK ปุ่ม **"ยืนยันสร้าง"** | — | ปุ่มเปลี่ยนเป็น spinner + "กำลังบันทึก…" ชั่วคราว | ☐ |
| 10 | WAIT จน drawer ปิด | — | toast **"สร้าง Posting Group แล้ว"** ปรากฏ | ☐ |
| 11 | VERIFY ตารางรายการ tab Posting Groups | — | แถว `TEST-VEN` ปรากฏ พร้อม pill ประเภท "เจ้าหนี้ (Vendor)" และสถานะ "ใช้งาน" | ☐ |

#### TC-G02 — สร้าง Posting Group ประเภท bank (1 ช่องบัญชีเท่านั้น, happy)
- group: G · ความสำคัญ: สูง · trace: S-01/AC-01 / BR-01
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups)
- ชุดข้อมูล: B
- ผ่านเมื่อ: บันทึกสำเร็จ + toast "สร้าง Posting Group แล้ว" + แถวใหม่ TEST-BANK มีบัญชีเดียว (ไม่มีช่อง 2)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **"เพิ่ม Posting Group"** | — | drawer เปิด | ☐ |
| 2 | SELECT "ธนาคาร (Bank)" → ช่อง **"ประเภท Posting Group"** | B | render ช่องบัญชีเดียว: "บัญชีเงินฝาก (GL)" (ไม่มีช่อง 2) | ☐ |
| 3 | TYPE → **"รหัสกลุ่ม (Code)"** + **"ชื่อกลุ่ม (TH)"** | B | ช่องแสดงค่าที่กรอก | ☐ |
| 4 | SELECT "1-1-10-01 เงินสดในมือ" → **"บัญชีเงินฝาก (GL)"** | B | ช่อง sdd แสดงค่าที่เลือก | ☐ |
| 5 | SELECT "ร่าง" → ช่อง **"สถานะ"** | B | select แสดง "ร่าง" | ☐ |
| 6 | CLICK **"ยืนยันสร้าง"** | — | toast **"สร้าง Posting Group แล้ว"**; แถว `TEST-BANK` ปรากฏ pill สถานะ "ร่าง", บัญชีที่ผูกแสดง 1 chip (เงินฝาก) | ☐ |

#### TC-G03 — สร้างไม่ครบ: รหัสกลุ่มว่าง (negative, EC-01)
- group: G · ความสำคัญ: สูง · trace: S-05/AC-01 · error `BR_FIELD_REQUIRED`
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK **"เพิ่ม Posting Group"**
- ชุดข้อมูล: A (แต่เว้นรหัสกลุ่มว่างตามชุด C)
- ผ่านเมื่อ: ไม่บันทึก + ช่อง "รหัสกลุ่ม (Code)" แสดงกรอบแดง + inline error

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "เจ้าหนี้ (Vendor)" → "ประเภท Posting Group" | A | render ช่องบัญชีตาม vendor | ☐ |
| 2 | TYPE → "ชื่อกลุ่ม (TH)" + เลือกบัญชี AP + Input VAT ครบ | A | ครบทุกช่องยกเว้นรหัส | ☐ |
| 3 | VERIFY ช่อง "รหัสกลุ่ม (Code)" | C: เว้นว่าง | ยังว่างอยู่ | ☐ |
| 4 | CLICK **"ยืนยันสร้าง"** | — | drawer ไม่ปิด; ช่อง "รหัสกลุ่ม (Code)" ขอบแดง (`.is-invalid`) + ข้อความ "กรุณากรอก/เลือกข้อมูลนี้" ปรากฏใต้ช่อง; ไม่มี toast; ไม่มีแถวใหม่ในตาราง | ☐ |

#### TC-G04 — สร้างไม่ครบ: ชื่อกลุ่ม (TH) ว่าง (negative, EC-02)
- group: G · ความสำคัญ: สูง · trace: S-05/AC-01 · error `BR_FIELD_REQUIRED`
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK **"เพิ่ม Posting Group"**
- ชุดข้อมูล: A (เว้นชื่อกลุ่ม TH ว่างตามชุด C)
- ผ่านเมื่อ: ไม่บันทึก + ช่อง "ชื่อกลุ่ม (TH)" ขอบแดง + inline error

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "เจ้าหนี้ (Vendor)" → "ประเภท Posting Group" | A | render ช่องตาม vendor | ☐ |
| 2 | TYPE → "รหัสกลุ่ม (Code)" + เลือกบัญชีครบ | A | ครบยกเว้นชื่อ TH | ☐ |
| 3 | VERIFY ช่อง "ชื่อกลุ่ม (TH)" | C: เว้นว่าง | ยังว่างอยู่ | ☐ |
| 4 | CLICK **"ยืนยันสร้าง"** | — | drawer ไม่ปิด; ช่อง "ชื่อกลุ่ม (TH)" ขอบแดง + inline error "กรุณากรอก/เลือกข้อมูลนี้"; ไม่มี toast | ☐ |

#### TC-G05 — สร้างไม่ครบ: บัญชีหลักตาม kind ว่าง (negative, EC-03)
- group: G · ความสำคัญ: สูง · trace: S-05/AC-01 · error `BR_FIELD_REQUIRED`
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK **"เพิ่ม Posting Group"**
- ชุดข้อมูล: A (ไม่เลือกบัญชี AP control)
- ผ่านเมื่อ: ไม่บันทึก + ช่อง "บัญชีเจ้าหนี้ (AP control)" ขอบแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "เจ้าหนี้ (Vendor)" → "ประเภท Posting Group" | A | render ช่องบัญชีตาม vendor | ☐ |
| 2 | TYPE → รหัส+ชื่อ TH ครบ | A | ครบยกเว้นบัญชี | ☐ |
| 3 | VERIFY ช่อง "บัญชีเจ้าหนี้ (AP control)" | — | ยังว่าง (placeholder "— เลือกบัญชีจากผังบัญชี —") | ☐ |
| 4 | CLICK **"ยืนยันสร้าง"** | — | drawer ไม่ปิด; ช่อง "บัญชีเจ้าหนี้ (AP control)" ขอบแดง + inline error; ไม่มี toast | ☐ |

#### TC-G06 — สร้างรหัสกลุ่มซ้ำ (negative, EC-01, error `BR_CODE_DUPLICATE`)
- group: G · ความสำคัญ: สูง · trace: S-05/AC-02 · error `BR_CODE_DUPLICATE`
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=มี seed g1 code=LOCAL อยู่แล้ว · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK **"เพิ่ม Posting Group"**
- ชุดข้อมูล: A แต่ใช้รหัส "LOCAL" (ชุด C)
- ผ่านเมื่อ: ไม่บันทึก + toast "รหัสกลุ่มนี้มีอยู่แล้ว" + ช่องรหัสขอบแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "เจ้าหนี้ (Vendor)" → "ประเภท Posting Group" | A | render ช่องตาม vendor | ☐ |
| 2 | TYPE "LOCAL" → **"รหัสกลุ่ม (Code)"** | C | ช่องแสดง `LOCAL` | ☐ |
| 3 | TYPE → ชื่อ TH + เลือกบัญชี AP + Input VAT ครบ | A | ครบทุกช่อง | ☐ |
| 4 | CLICK **"ยืนยันสร้าง"** | — | drawer ไม่ปิด; ช่อง "รหัสกลุ่ม (Code)" ขอบแดง; toast **"รหัสกลุ่มนี้มีอยู่แล้ว"**; ไม่มีแถวใหม่ในตาราง | ☐ |

#### TC-G07 — บัญชีไม่ตรงประเภท `kind` (negative, server-side, AC-03) — ⚠ ต้อง simulate
- group: G · ความสำคัญ: กลาง · trace: S-05/AC-03 · error `BR_ACCOUNT_TYPE_MISMATCH`
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=— · **(ต้อง simulate)** — dropdown "บัญชีเจ้าหนี้ (AP control)" ถูก client-side filter ให้แสดงเฉพาะ `type=liability` เท่านั้น (ดู `acctSelect('payable_acct', ..., ['liability'])`) จึงไม่มีทางเลือกบัญชีผิดประเภทผ่าน UI ได้จริง — ต้องยิง API `POST /gl/posting-groups` ตรง (นอกเหนือการคลิกหน้าจอ) ด้วย body ที่ `account_1` เป็นบัญชี type=`asset` แทน `liability`
- Start: (ไม่มี UI path — บันทึกไว้เป็นหมายเหตุการทดสอบระดับ API)
- ชุดข้อมูล: A แต่สลับ account_1 เป็น 1-1-40 (asset) แทน 2-1-10-02 (liability)
- ผ่านเมื่อ: server ตอบ 422 `BR_ACCOUNT_TYPE_MISMATCH`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY dropdown "บัญชีเจ้าหนี้ (AP control)" (UI-level, ไม่ต้อง simulate) | — | ตัวเลือกทั้งหมดเป็นบัญชี type=liability เท่านั้น (2-1-10-01, 2-1-10-02, 2-1-20, 2-1-30) — ไม่มีบัญชี asset/income/expense ให้เลือก ยืนยันว่า client กันไว้แล้วตามที่ AC-03 อธิบาย | ☐ |
| 2 | (simulate) ยิง `POST /api/v1/gl/posting-groups` body `{kind:'vendor',account_1:'1-1-40',...}` | — | response 422 `BR_ACCOUNT_TYPE_MISMATCH` | ☐ |

#### TC-G08 — เปลี่ยน kind ก่อนบันทึก → ล้างช่องบัญชีเดิม (R07/EC-06/AC-18)
- group: G · ความสำคัญ: สูง · trace: BR-03b(R07)/AC-18
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK **"เพิ่ม Posting Group"**
- ชุดข้อมูล: A (บาง field)
- ผ่านเมื่อ: หลังเปลี่ยน kind ช่องบัญชีเดิมถูกล้างและช่องบัญชีชุดใหม่ตรงกับ kind ใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "เจ้าหนี้ (Vendor)" → "ประเภท Posting Group" | — | render ช่อง "บัญชีเจ้าหนี้ (AP control)" + "บัญชีภาษีซื้อ (Input VAT)" | ☐ |
| 2 | SELECT "2-1-10-01 เจ้าหนี้การค้า" → "บัญชีเจ้าหนี้ (AP control)" | — | ช่องแสดงค่าที่เลือกแล้ว | ☐ |
| 3 | SELECT "สินค้าคงคลัง (Inventory)" → **"ประเภท Posting Group"** (เปลี่ยน kind ก่อน submit) | — | render ช่องใหม่: "บัญชีสินค้าคงคลัง (Inventory)" + "บัญชี Interim (รับของยังไม่วางบิล)" — ช่องบัญชีเก่า (AP/Input VAT) หายไปทั้งหมด | ☐ |
| 4 | VERIFY ช่อง "บัญชีสินค้าคงคลัง (Inventory)" | — | ว่าง (ไม่มีค่าจากขั้นก่อนหน้าค้างอยู่) — ยืนยันว่าค่าบัญชีเดิมถูกล้างจริง ไม่ใช่แค่ซ่อน | ☐ |
| 5 | VERIFY ช่อง "รหัสกลุ่ม (Code)" / "ชื่อกลุ่ม (TH)" (ถ้ากรอกไว้ก่อนหน้า) | — | ค่าที่กรอกไว้ก่อนเปลี่ยน kind ยังคงอยู่ (เฉพาะช่องบัญชีเท่านั้นที่ถูกล้าง) | ☐ |

#### TC-G09 — รหัสกลุ่ม auto-uppercase ระหว่างพิมพ์
- group: G · ความสำคัญ: ต่ำ · trace: 04_DB §4.2 `code` uppercased
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK **"เพิ่ม Posting Group"**
- ชุดข้อมูล: A
- ผ่านเมื่อ: พิมพ์ตัวพิมพ์เล็กแล้วช่องแสดงตัวพิมพ์ใหญ่ทันที

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "test-ven" (พิมพ์เล็ก) → ช่อง **"รหัสกลุ่ม (Code)"** | — | ช่องแสดง `TEST-VEN` (แปลงเป็นตัวพิมพ์ใหญ่ทันทีที่พิมพ์) | ☐ |

---

### กลุ่ม E — แก้ไข Specific Posting Group (Tab 1, P-02) — IR-PG-01 vs R05

> **🚨 ย้ำ:** IR-PG-01 (BR-05, ล็อกเฉพาะ `code` เมื่อ `used>0`) และ R05 (BR-03, ล็อก `kind` เสมอไม่ว่า `used`
> เท่าไหร่) เป็น **สองกฎแยกกัน**. กลุ่มนี้แยกเคสให้พิสูจน์ทั้งสองกฎเป็นอิสระจากกันตามที่ 06_TESTS
> §6.4 DoD กำหนด (TC-07/08 ต้องแยกจาก TC-09/10 ในชื่อเคส)

#### TC-E01 — แก้ไข record ที่ `used=0` — แก้ได้ทุกฟิลด์ยกเว้น kind (happy, S-03/AC-06)
- group: E · ความสำคัญ: สูง · trace: S-03/AC-06 / BR-05(IR-PG-01 ไม่ trigger เพราะ used=0)
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียน SCB (bank, used=0) · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK ไอคอนดินสอ (แก้ไข) ที่แถว **SCB**
- ชุดข้อมูล: — (แก้ไขค่าที่มีอยู่)
- ผ่านเมื่อ: บันทึกสำเร็จ + toast "บันทึกการแก้ไขกลุ่มแล้ว" + ค่าที่แก้ทุกช่อง (รวมรหัส) เปลี่ยนจริงในตาราง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY drawer หัวข้อ | — | หัวข้อ **"แก้ไข Posting Group"** subtitle แสดงรหัส `SCB` | ☐ |
| 2 | VERIFY ช่อง "รหัสกลุ่ม (Code)" | — | เป็น `<input>` แก้ไขได้ (ไม่ใช่กล่อง locked เพราะ used=0) ไม่มี `.lock-tag` | ☐ |
| 3 | TYPE "SCB-NEW" → ช่อง **"รหัสกลุ่ม (Code)"** (แก้ code ได้จริงเพราะ used=0) | — | ช่องแสดง `SCB-NEW` | ☐ |
| 4 | TYPE ค่าใหม่ → ช่อง **"ชื่อกลุ่ม (TH)"** | — | ช่องแสดงค่าที่แก้ | ☐ |
| 5 | SELECT บัญชีใหม่ → ช่อง **"บัญชีเงินฝาก (GL)"** | — | ช่อง sdd แสดงค่าใหม่ | ☐ |
| 6 | SELECT "ใช้งาน" → ช่อง **"สถานะ"** | — | select แสดง "ใช้งาน" | ☐ |
| 7 | CLICK **"บันทึกการแก้ไข"** | — | toast **"บันทึกการแก้ไขกลุ่มแล้ว"**; แถว `SCB-NEW` ปรากฏในตารางพร้อมค่าใหม่ทั้งหมด | ☐ |

#### TC-E02 — แก้ไข record ที่ `used>0` — พยายามเปลี่ยน `code` ถูกบล็อก (negative, IR-PG-01, EC-05)
- group: E · ความสำคัญ: สูง (critical) · trace: S-04/AC-07 · error `BR_CODE_LOCKED_USED` · LOCK-01
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียน LOCAL (vendor, used=82) · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK ไอคอนดินสอ ที่แถว **LOCAL**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ช่องรหัสแสดงเป็นกล่อง locked + lock-tag, ไม่มีทางพิมพ์รหัสใหม่ได้ผ่าน UI

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง "รหัสกลุ่ม (Code)" | — | แสดงเป็น `<div>` แบบ locked (ไม่ใช่ `<input>`) มีป้าย **"ล็อก — มีการบันทึกบัญชีแล้ว"** ต่อท้าย label + ค่าเดิม `LOCAL` แสดงอยู่ (แก้ไม่ได้ผ่าน UI เพราะไม่มีช่องกรอกให้พิมพ์) | ☐ |
| 2 | VERIFY ช่อง "ชื่อกลุ่ม (TH)"/"ชื่อกลุ่ม (EN)"/บัญชี/สถานะ | — | ทุกช่องยังเป็น input/select/sdd ปรกติ แก้ไขได้ (ไม่ล็อก) | ☐ |
| 3 | TYPE ชื่อใหม่ → **"ชื่อกลุ่ม (TH)"** แล้ว CLICK **"บันทึกการแก้ไข"** (โดยไม่แตะรหัส) | — | บันทึกสำเร็จ toast **"บันทึกการแก้ไขกลุ่มแล้ว"** (พิสูจน์ว่าฟิลด์อื่นแก้ได้ปรกติแม้ used>0) — รหัสยังคงเป็น `LOCAL` เหมือนเดิม | ☐ |

#### TC-E03 — แก้ไข record ที่ `used=0` — `kind` ล็อกเสมอ (AC-08b, พิสูจน์ R05 ไม่ขึ้นกับ used)
- group: E · ความสำคัญ: สูง (critical) · trace: S-03/AC-08b · error `BR_KIND_LOCKED` · LOCK-02
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียน SCB (bank, **used=0**) · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK ไอคอนดินสอ ที่แถว **SCB**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ช่อง "ประเภท Posting Group" เป็นกล่อง static ไม่ใช่ dropdown แม้ used=0

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง "ประเภท Posting Group" | — | แสดงเป็น `<div class="sdd-trigger">` แบบ `cursor:not-allowed` ค่าคงที่ **"ธนาคาร (Bank)"** — **ไม่มี** chevron dropdown, ไม่มี sdd-panel ให้เปิด | ☐ |
| 2 | CLICK ที่ช่อง "ประเภท Posting Group" | — | ไม่มีอะไรเกิดขึ้น (ไม่เปิด dropdown, ไม่มีตัวเลือกให้เลือกใหม่) — ยืนยันว่าไม่มี UI path ให้เปลี่ยน kind เลย แม้ record นี้ `used=0` | ☐ |
| 3 | VERIFY ช่อง "รหัสกลุ่ม (Code)" (เทียบกับข้อ 1) | — | ช่องนี้เป็น `<input>` แก้ไขได้ปรกติ (ต่าง context จาก kind — ยืนยันว่า R05/kind lock และ IR-PG-01/code lock เป็นกลไกคนละตัว: ที่ used=0 code แก้ได้แต่ kind ล็อกอยู่ดี) | ☐ |

#### TC-E04 — แก้ไข record ที่ `used>0` — `kind` ล็อกเสมอ (AC-08b, พิสูจน์ R05 ที่ used>0 เช่นกัน)
- group: E · ความสำคัญ: สูง (critical) · trace: S-04/AC-08b · error `BR_KIND_LOCKED` · LOCK-02
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียน LOCAL (vendor, **used=82**) · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK ไอคอนดินสอ ที่แถว **LOCAL**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ช่อง "ประเภท Posting Group" เป็นกล่อง static เหมือน TC-E03 — พิสูจน์ว่าผลลัพธ์เหมือนกันไม่ว่า used จะเป็นเท่าไหร่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง "ประเภท Posting Group" | — | แสดงเป็นกล่อง static ค่าคงที่ **"เจ้าหนี้ (Vendor)"** เหมือนที่ TC-E03 พบตอน used=0 — ไม่มี dropdown ให้เปิดเช่นกัน | ☐ |
| 2 | CLICK ที่ช่อง "ประเภท Posting Group" | — | ไม่มีอะไรเกิดขึ้น | ☐ |
| 3 | VERIFY ช่อง "รหัสกลุ่ม (Code)" (ระเบียนนี้ used>0) | — | ช่องนี้เป็นกล่อง locked พร้อม lock-tag (ตรงกับ TC-E02) — ยืนยันว่าที่ used>0 ทั้ง kind และ code ถูกล็อก แต่ด้วย **กลไกคนละตัว** (kind ล็อกเพราะ R05 เสมอ, code ล็อกเพราะ IR-PG-01 เมื่อ used>0) | ☐ |

#### TC-E05 — แก้ไข record ที่ `used>0` — เปลี่ยนบัญชี (account_1/2) สำเร็จ (IR-PG-01 อนุญาต)
- group: E · ความสำคัญ: สูง (critical) · trace: S-04/AC-07 · BR-05(IR-PG-01) · LOCK-01
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียน DOMESTIC-C (customer, used=120) · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK ไอคอนดินสอ ที่แถว **DOMESTIC-C**
- ชุดข้อมูล: —
- ผ่านเมื่อ: เปลี่ยนบัญชี AR control สำเร็จ แม้ used>0

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง "บัญชีลูกหนี้ (AR control)" / "บัญชีภาษีขาย (Output VAT)" | — | ทั้งสองช่องเป็น sdd ปรกติ ไม่มี lock-tag (ต่างจากช่องรหัส) | ☐ |
| 2 | SELECT บัญชีใหม่ (asset อื่นใน COA) → **"บัญชีลูกหนี้ (AR control)"** | — | ช่อง sdd แสดงค่าที่เลือกใหม่ | ☐ |
| 3 | CLICK **"บันทึกการแก้ไข"** | — | บันทึกสำเร็จ toast **"บันทึกการแก้ไขกลุ่มแล้ว"** — ไม่มี toast บล็อกใดๆ; แถว DOMESTIC-C ในตารางแสดง chip บัญชี AR ใหม่ | ☐ |

#### TC-E06 — แก้ไข record ที่ `used>0` — เปลี่ยนสถานะสำเร็จผ่านหน้าแก้ไข (IR-PG-01 อนุญาต)
- group: E · ความสำคัญ: กลาง · trace: S-04/AC-07 · BR-05(IR-PG-01) · LOCK-01
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียน FINISHED (inventory, used=57) · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK ไอคอนดินสอ ที่แถว **FINISHED**
- ชุดข้อมูล: —
- ผ่านเมื่อ: เปลี่ยนสถานะสำเร็จผ่าน drawer แก้ไข แม้ used>0

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "ไม่ใช้งาน" → ช่อง **"สถานะ"** | — | select แสดง "ไม่ใช้งาน" | ☐ |
| 2 | CLICK **"บันทึกการแก้ไข"** | — | toast **"บันทึกการแก้ไขกลุ่มแล้ว"**; แถว FINISHED แสดง pill สถานะ "ไม่ใช้งาน" | ☐ |

#### TC-E07 — แก้ไข record ที่ `used>0` — รหัสยังคงเดิมแม้พยายามแก้ (double-check ผลลัพธ์จริงหลัง save)
- group: E · ความสำคัญ: สูง · trace: S-04/AC-07 · BR-05(IR-PG-01) · error `BR_CODE_LOCKED_USED`
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียน KBANK (bank, used=203) · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK ไอคอนดินสอ ที่แถว **KBANK**
- ชุดข้อมูล: —
- ผ่านเมื่อ: หลัง save รหัสในตารางยังเป็น `KBANK` เหมือนก่อนแก้ (ยืนยัน persist ไม่เปลี่ยน)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จดค่า รหัสปัจจุบันในตาราง ก่อนเข้า drawer | — | บันทึกไว้: รหัส = `KBANK` (อ้างใน step 4) | ☐ |
| 2 | TYPE ชื่อใหม่ → "ชื่อกลุ่ม (TH)" (ช่องเดียวที่แก้ได้ในเคสนี้) | — | ช่องแสดงค่าใหม่ | ☐ |
| 3 | CLICK **"บันทึกการแก้ไข"** | — | toast **"บันทึกการแก้ไขกลุ่มแล้ว"** | ☐ |
| 4 | VERIFY แถว KBANK ในตารางอีกครั้ง | — | รหัสยังคง `KBANK` เท่ากับค่าที่จดไว้ใน step 1 (ไม่เปลี่ยน) — ชื่อกลุ่มอัปเดตเป็นค่าใหม่ | ☐ |

#### TC-E08 — แก้ไข record ที่ `used=0` — เปลี่ยนรหัสเป็นค่าที่ซ้ำกับระเบียนอื่น (negative, ยังต้อง unique แม้เป็นการแก้ไข)
- group: E · ความสำคัญ: กลาง · trace: BR-02(R03) · error `BR_CODE_DUPLICATE`
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียน SCB (bank, used=0) · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK ไอคอนดินสอ ที่แถว **SCB**
- ชุดข้อมูล: C (รหัส LOCAL)
- ผ่านเมื่อ: บันทึกไม่ผ่าน + toast "รหัสกลุ่มนี้มีอยู่แล้ว"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "LOCAL" → ช่อง **"รหัสกลุ่ม (Code)"** (ซ้ำกับ record อื่นที่มีอยู่) | C | ช่องแสดง `LOCAL` | ☐ |
| 2 | CLICK **"บันทึกการแก้ไข"** | — | drawer ไม่ปิด; ช่องรหัสขอบแดง; toast **"รหัสกลุ่มนี้มีอยู่แล้ว"**; รหัสของ SCB ไม่เปลี่ยน | ☐ |

---

### กลุ่ม S — สร้าง General Posting Setup (Tab 2, P-03)

#### TC-S01 — สร้าง Setup combination ใหม่ครบฟิลด์ (happy, S-02/AC-04)
- group: S · ความสำคัญ: สูง · trace: S-02/AC-04 / BR-01(R01,R02) / R09(as-built 2-value set)
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=มี s1 s2 s3 อยู่แล้ว (ไม่มี FOREIGN×SERVICE) · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK tab **"General Posting Setup"** → CLICK ปุ่ม **"เพิ่ม Setup"**
- ชุดข้อมูล: D
- ผ่านเมื่อ: บันทึกสำเร็จ + toast "สร้าง Posting Setup แล้ว" + แถวใหม่ FOREIGN×SERVICE ปรากฏ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY drawer หัวข้อ | — | หัวข้อ **"เพิ่ม General Posting Setup"** | ☐ |
| 2 | SELECT "FOREIGN" → ช่อง **"กลุ่มธุรกิจ (Business Group)"** | D | ช่อง sdd แสดง `FOREIGN` — ตัวเลือกทั้ง dropdown มีแค่ 2 ค่า (DOMESTIC/FOREIGN) ตาม as-built value set (R09) | ☐ |
| 3 | SELECT "SERVICE" → ช่อง **"กลุ่มสินค้า (Product Group)"** | D | ช่อง sdd แสดง `SERVICE` — ตัวเลือกมีแค่ 2 ค่า (GOODS/SERVICE) | ☐ |
| 4 | SELECT "4-1-20 รายได้ค่าบริการ" → ช่อง **"บัญชีรายได้ (Sales)"** | D | ช่อง sdd แสดงค่าที่เลือก | ☐ |
| 5 | SELECT "5-1 ต้นทุนขาย" → ช่อง **"บัญชีซื้อ (Purchase)"** | D | ช่อง sdd แสดงค่าที่เลือก | ☐ |
| 6 | SELECT "5-1 ต้นทุนขาย" → ช่อง **"บัญชีต้นทุนขาย (COGS)"** | D | ช่อง sdd แสดงค่าที่เลือก | ☐ |
| 7 | CLICK **"ยืนยันสร้าง"** | — | toast **"สร้าง Posting Setup แล้ว"**; แถวใหม่ badge `FOREIGN` × `SERVICE` ปรากฏในตาราง สถานะ "ใช้งาน" | ☐ |

#### TC-S02 — สร้าง Setup ไม่ครบฟิลด์ (negative, EC required)
- group: S · ความสำคัญ: สูง · trace: S-05 · error `BR_FIELD_REQUIRED`
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK tab **"General Posting Setup"** → CLICK **"เพิ่ม Setup"**
- ชุดข้อมูล: D (แต่เว้นบัญชีซื้อว่าง)
- ผ่านเมื่อ: บันทึกไม่ผ่าน + ช่อง "บัญชีซื้อ (Purchase)" ขอบแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT bus/prod + บัญชีรายได้ + บัญชีต้นทุน ครบ (เว้นบัญชีซื้อ) | D | ครบยกเว้นบัญชีซื้อ | ☐ |
| 2 | CLICK **"ยืนยันสร้าง"** | — | drawer ไม่ปิด; ช่อง "บัญชีซื้อ (Purchase)" ขอบแดง + inline error "กรุณากรอก/เลือกข้อมูลนี้"; ไม่มี toast | ☐ |

#### TC-S03 — สร้าง Setup combination ซ้ำ (negative, EC-04, error `BR_COMBINATION_DUPLICATE`)
- group: S · ความสำคัญ: สูง · trace: S-05/AC-05 · BR-02(R04) · error `BR_COMBINATION_DUPLICATE`
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=มี s1 (DOMESTIC×GOODS) อยู่แล้ว · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK tab **"General Posting Setup"** → CLICK **"เพิ่ม Setup"**
- ชุดข้อมูล: E (bus/prod ซ้ำ) + D (บัญชี)
- ผ่านเมื่อ: บันทึกไม่ผ่าน + toast "ชุดกลุ่มนี้มีอยู่แล้ว" + **ทั้งสองช่อง** bus และ prod ขอบแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "DOMESTIC" → **"กลุ่มธุรกิจ (Business Group)"** | E | ช่องแสดง `DOMESTIC` | ☐ |
| 2 | SELECT "GOODS" → **"กลุ่มสินค้า (Product Group)"** | E | ช่องแสดง `GOODS` (ซ้ำกับ s1 ที่มีอยู่) | ☐ |
| 3 | SELECT บัญชี 3 ช่องครบ | D | ครบทุกช่อง | ☐ |
| 4 | CLICK **"ยืนยันสร้าง"** | — | drawer ไม่ปิด; ช่อง **"กลุ่มธุรกิจ"** และ **"กลุ่มสินค้า"** ขอบแดงพร้อมกันทั้งคู่; toast **"ชุดกลุ่มนี้มีอยู่แล้ว"**; ไม่มีแถวใหม่ | ☐ |

#### TC-S04 — บัญชีซื้อ (Purchase) รองรับสองประเภท expense/asset (dual-type, §2.5 as-built nuance)
- group: S · ความสำคัญ: กลาง · trace: BR-01(R02) note dual-type
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK tab **"General Posting Setup"** → CLICK **"เพิ่ม Setup"**
- ชุดข้อมูล: D แต่เปลี่ยนบัญชีซื้อเป็น 1-1-30-01 (asset)
- ผ่านเมื่อ: dropdown "บัญชีซื้อ (Purchase)" ยอมให้เลือกบัญชี type=asset ได้ (ไม่ใช่แค่ expense)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK เปิด dropdown ช่อง **"บัญชีซื้อ (Purchase)"** | — | รายการตัวเลือกมีทั้งบัญชี type=expense (5-1, 5-2-10-01, 5-2-20) และ type=asset (1-1-10-01/02/03, 1-1-20-01, 1-1-30-01, 1-1-40) — ไม่ใช่แค่ expense อย่างเดียว | ☐ |
| 2 | SELECT "1-1-30-01 สินค้าสำเร็จรูป" (asset) → **"บัญชีซื้อ (Purchase)"** | — | ช่อง sdd แสดงค่าที่เลือกได้สำเร็จ (ไม่ถูกปฏิเสธ) | ☐ |

#### TC-S05 — บัญชีไม่ตรงประเภทที่กำหนด (negative, server-side) — ⚠ ต้อง simulate
- group: S · ความสำคัญ: กลาง · trace: S-05 · error `BR_ACCOUNT_TYPE_MISMATCH`
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=— · **(ต้อง simulate)** — dropdown "บัญชีรายได้ (Sales)" ถูก filter เหลือเฉพาะ type=income เท่านั้นผ่าน UI จึงเลือกผิดประเภทไม่ได้จริง ต้องยิง API ตรง
- Start: (ไม่มี UI path)
- ชุดข้อมูล: D แต่สลับ sales_acct เป็น 5-1 (expense) แทน 4-1-20 (income)
- ผ่านเมื่อ: server ตอบ 422 `BR_ACCOUNT_TYPE_MISMATCH`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY dropdown "บัญชีรายได้ (Sales)" (UI-level) | — | ตัวเลือกทั้งหมดเป็น type=income เท่านั้น (4-1-10, 4-1-20, 4-2) | ☐ |
| 2 | (simulate) ยิง `POST /api/v1/gl/posting-setups` body `{sales_account:'5-1',...}` | — | response 422 `BR_ACCOUNT_TYPE_MISMATCH` | ☐ |

---

### กลุ่ม ES — แก้ไข General Posting Setup (Tab 2, P-03) — IR-PG-01 pair-lock

#### TC-ES01 — แก้ไข Setup ที่ `used=0` — แก้ได้ทุกฟิลด์รวม combination (happy, S-03/AC-06)
- group: ES · ความสำคัญ: สูง · trace: S-03/AC-06
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียน FOREIGN×GOODS (s3, used=0) · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK tab **"General Posting Setup"** → CLICK ไอคอนดินสอ ที่แถว **FOREIGN × GOODS**
- ชุดข้อมูล: —
- ผ่านเมื่อ: แก้ combination ได้สำเร็จเพราะ used=0

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง "กลุ่มธุรกิจ (Business Group)" / "กลุ่มสินค้า (Product Group)" | — | ทั้งสองเป็น sdd แก้ไขได้ (ไม่ใช่กล่อง locked, ไม่มี lock-tag) | ☐ |
| 2 | SELECT "DOMESTIC" → **"กลุ่มธุรกิจ"** (เปลี่ยนครึ่งคู่ เพราะ used=0 อนุญาต) — แต่ prod ยังเป็น GOODS ซึ่งจะซ้ำกับ s1 | — | ช่องแสดง `DOMESTIC` (ยังไม่ submit) | ☐ |
| 3 | SELECT "SERVICE" → **"กลุ่มสินค้า"** (เลี่ยง dup, สร้าง combination ใหม่ DOMESTIC×SERVICE — แต่ก็ซ้ำ s2! เปลี่ยนเป็นค่าที่ไม่ซ้ำจริง) SELECT "FOREIGN"+"SERVICE" แทน (ค่าที่ยังไม่มีในทะเบียน) | — | ช่องแสดง `FOREIGN`/`SERVICE` | ☐ |
| 4 | CLICK **"บันทึกการแก้ไข"** | — | toast **"บันทึกการแก้ไข setup แล้ว"**; แถวเดิม (เดิม FOREIGN×GOODS) เปลี่ยน badge เป็น `FOREIGN`×`SERVICE` | ☐ |

#### TC-ES02 — แก้ไข Setup ที่ `used>0` — พยายามเปลี่ยน combination ถูกบล็อก (negative, IR-PG-01, EC-05)
- group: ES · ความสำคัญ: สูง (critical) · trace: S-04/AC-08 · error `BR_COMBINATION_LOCKED_USED` · LOCK-01
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียน DOMESTIC×GOODS (s1, used=340) · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK tab **"General Posting Setup"** → CLICK ไอคอนดินสอ ที่แถว **DOMESTIC × GOODS**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ช่อง bus/prod แสดงเป็นกล่อง locked ทั้งคู่ + lock-tag, ไม่มีทางแก้ค่าได้ผ่าน UI

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง "กลุ่มธุรกิจ (Business Group)" | — | แสดงเป็น `<div>` locked พร้อม lock-tag **"ล็อก — มีการบันทึกบัญชีแล้ว"** ค่า `DOMESTIC` ไม่มี dropdown | ☐ |
| 2 | VERIFY ช่อง "กลุ่มสินค้า (Product Group)" | — | แสดงเป็น `<div>` locked พร้อม lock-tag เดียวกัน ค่า `GOODS` ไม่มี dropdown — **ทั้งคู่ล็อกพร้อมกัน** (pair-lock ไม่ใช่ทีละฟิลด์) | ☐ |
| 3 | TYPE ค่าใหม่ → บัญชี "บัญชีรายได้ (Sales)" แล้ว CLICK **"บันทึกการแก้ไข"** (ไม่แตะ bus/prod) | — | บันทึกสำเร็จ toast **"บันทึกการแก้ไข setup แล้ว"** — combination ยังเป็น `DOMESTIC`×`GOODS` เหมือนเดิม (พิสูจน์ว่าฟิลด์อื่นแก้ได้ปรกติ) | ☐ |

#### TC-ES03 — แก้ไข Setup ที่ `used>0` — เปลี่ยนบัญชีทั้ง 3 ช่องสำเร็จ (IR-PG-01 อนุญาต)
- group: ES · ความสำคัญ: สูง (critical) · trace: S-04/AC-07 · BR-05(IR-PG-01) · LOCK-01
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียน DOMESTIC×SERVICE (s2, used=88) · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK tab **"General Posting Setup"** → CLICK ไอคอนดินสอ ที่แถว **DOMESTIC × SERVICE**
- ชุดข้อมูล: —
- ผ่านเมื่อ: เปลี่ยนบัญชี 3 ช่องสำเร็จแม้ used>0

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "4-2 รายได้อื่น" → **"บัญชีรายได้ (Sales)"** | — | ช่อง sdd แสดงค่าใหม่ | ☐ |
| 2 | SELECT "5-2-10-01 เงินเดือน" → **"บัญชีซื้อ (Purchase)"** | — | ช่อง sdd แสดงค่าใหม่ | ☐ |
| 3 | SELECT "5-2-20 ค่าสาธารณูปโภค" → **"บัญชีต้นทุนขาย (COGS)"** | — | ช่อง sdd แสดงค่าใหม่ | ☐ |
| 4 | CLICK **"บันทึกการแก้ไข"** | — | toast **"บันทึกการแก้ไข setup แล้ว"**; combination badge ยังเป็น `DOMESTIC`×`SERVICE` เดิม แต่บัญชี 3 ช่องในตารางเปลี่ยนเป็นค่าใหม่ | ☐ |

#### TC-ES04 — แก้ไข Setup ที่ `used>0` — เปลี่ยนสถานะสำเร็จผ่านหน้าแก้ไข (IR-PG-01 อนุญาต)
- group: ES · ความสำคัญ: กลาง · trace: S-04/AC-07 · BR-05(IR-PG-01)
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียน FOREIGN×GOODS (s3) — **หมายเหตุ:** s3 used=0 ปรกติ ให้ใช้ DOMESTIC×GOODS (s1, used=340) แทนเพื่อยืนยัน used>0 · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK tab **"General Posting Setup"** → CLICK ไอคอนดินสอ ที่แถว **DOMESTIC × GOODS**
- ชุดข้อมูล: —
- ผ่านเมื่อ: เปลี่ยนสถานะสำเร็จผ่าน drawer แก้ไข แม้ used>0

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "ร่าง" → ช่อง **"สถานะ"** | — | select แสดง "ร่าง" | ☐ |
| 2 | CLICK **"บันทึกการแก้ไข"** | — | toast **"บันทึกการแก้ไข setup แล้ว"**; แถว DOMESTIC×GOODS แสดง pill สถานะ "ร่าง" | ☐ |

#### TC-ES05 — พิสูจน์ pair-lock: เปลี่ยนแค่ครึ่งคู่ (bus อย่างเดียว) เมื่อ `used>0` ยังถูกบล็อกเหมือนกัน
- group: ES · ความสำคัญ: สูง (critical) · trace: BR-05(IR-PG-01) tab2-variant · LOCK-01
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียน DOMESTIC×SERVICE (s2, used=88) · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK tab **"General Posting Setup"** → CLICK ไอคอนดินสอ ที่แถว **DOMESTIC × SERVICE**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ทั้งสองช่อง (ไม่ใช่แค่ช่องที่ "จะเปลี่ยน") ถูกล็อกพร้อมกัน — ยืนยันว่าไม่มีทางแก้แม้ครึ่งคู่เดียวได้ เพราะกลไกล็อกทั้งคู่พร้อมกัน ไม่ใช่ทีละฟิลด์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง "กลุ่มธุรกิจ (Business Group)" | — | locked box (ไม่ใช่ dropdown ที่กดเลือกค่าอื่นได้) | ☐ |
| 2 | VERIFY ช่อง "กลุ่มสินค้า (Product Group)" ในเวลาเดียวกัน | — | locked box เช่นกัน — **ไม่มีกรณีที่ช่องหนึ่งแก้ได้อีกช่องล็อก** ยืนยันว่า pair ล็อกร่วมกันเป็นหน่วยเดียว ตรงตาม 03_LOGIC.md FN-08 guard logic | ☐ |

---

### กลุ่ม ST — เปลี่ยนสถานะ อิสระ ไม่มีอนุมัติ (BR-06)

#### TC-ST01 — เปลี่ยนสถานะรายการเดียวผ่าน view drawer เมนู "เปลี่ยนสถานะ" (happy, S-06/AC-09)
- group: ST · ความสำคัญ: สูง · trace: S-06/AC-09 · BR-06 · LOCK-04
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียน SCB (bank, สถานะ "ร่าง") · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups) → CLICK แถว **SCB** (เปิด view drawer)
- ชุดข้อมูล: —
- ผ่านเมื่อ: สถานะเปลี่ยนทันที ไม่มี modal ยืนยัน + toast ระบุ label สถานะใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **"เปลี่ยนสถานะ"** ที่ header ของ view drawer | — | เมนู dropdown เปิด แสดง 3 ตัวเลือก (ร่าง/ใช้งาน/ไม่ใช้งาน) — ตัวเลือกสถานะปัจจุบัน ("ร่าง") เป็น `disabled` | ☐ |
| 2 | CLICK ตัวเลือก **"ใช้งาน"** ในเมนู | — | สถานะเปลี่ยนทันที **ไม่มี modal ยืนยันใดๆ**; toast **"เปลี่ยนสถานะเป็น ใช้งาน แล้ว"** ปรากฏ | ☐ |
| 3 | VERIFY drawer header (ไม่ต้องปิด) | — | pill/label สถานะในเนื้อ drawer แสดง "ใช้งาน" แล้ว | ☐ |
| 4 | CLICK **"ปิด"** แล้ว VERIFY แถว SCB ในตาราง | — | pill สถานะแสดง "ใช้งาน" ตรงกับที่เปลี่ยน | ☐ |

#### TC-ST02 — เปลี่ยนสถานะแบบ bulk ผ่าน bulk bar (happy, S-06/AC-09 bulk)
- group: ST · ความสำคัญ: สูง · trace: S-06/AC-09 · BR-06 · LOCK-04
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=เลือกได้ ≥2 แถวจากตาราง tab1 · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups)
- ชุดข้อมูล: —
- ผ่านเมื่อ: bulk bar ปรากฏหลังติ๊กเลือก + เปลี่ยนสถานะทุกแถวที่เลือกพร้อมกัน + toast ระบุจำนวน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox แถว **FINISHED** และ **SCRAP** | — | bulk bar สีเข้มปรากฏด้านบนตาราง แสดง **"เลือก 2 รายการ"** พร้อมปุ่ม ใช้งาน/ไม่ใช้งาน/ร่าง/ลบ/ยกเลิก | ☐ |
| 2 | CLICK ปุ่ม **"ไม่ใช้งาน"** ใน bulk bar | — | ไม่มี modal ยืนยัน; toast **"เปลี่ยนสถานะ 2 รายการเป็น ไม่ใช้งาน แล้ว"**; bulk bar หายไป (selection ถูกล้าง) | ☐ |
| 3 | VERIFY แถว FINISHED และ SCRAP | — | ทั้งสองแถวแสดง pill สถานะ "ไม่ใช้งาน" | ☐ |

#### TC-ST03 — Revert สถานะ "ใช้งาน" → "ร่าง" บนระเบียน `used` สูง โดยไม่มี warning เพิ่ม `[AI-DEFAULT]` (edge: ST-02)
- group: ST · ความสำคัญ: กลาง · trace: 05_RULES §5.5 ST-02 `[AI-DEFAULT]` · BR-06
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียน KBANK (bank, used=203, สถานะ "ใช้งาน") · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups) → CLICK แถว **KBANK**
- ชุดข้อมูล: —
- ผ่านเมื่อ: revert สำเร็จทันที ไม่มี prompt เหตุผล/คำเตือนพิเศษใดๆ แม้ `used=203` (สูงสุดในทะเบียน)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **"เปลี่ยนสถานะ"** → CLICK **"ร่าง"** | — | สถานะเปลี่ยนทันที ไม่มี modal คำเตือน/ช่องกรอกเหตุผลใดๆ (BR-06 อนุญาตไม่จำกัด); toast **"เปลี่ยนสถานะเป็น ร่าง แล้ว"** | ☐ |
| 2 | VERIFY แถว KBANK ในตาราง | — | pill สถานะแสดง "ร่าง" — ค่า `used=203` ไม่ถูกกระทบ/รีเซ็ต | ☐ |

#### TC-ST04 — ตั้งสถานะ "ไม่ใช้งาน" บนระเบียน `used` สูง โดยไม่มี warning เพิ่ม `[AI-DEFAULT]` (edge: ST-04)
- group: ST · ความสำคัญ: กลาง · trace: 05_RULES §5.5 ST-04 `[AI-DEFAULT]` · BR-06
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียน DOMESTIC×GOODS (s1, used=340, สถานะ "ใช้งาน") · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK tab **"General Posting Setup"** → CLICK แถว **DOMESTIC × GOODS**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ตั้งไม่ใช้งานสำเร็จทันที ไม่มี warning พิเศษ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **"เปลี่ยนสถานะ"** → CLICK **"ไม่ใช้งาน"** | — | สถานะเปลี่ยนทันที ไม่มี modal เตือน; toast **"เปลี่ยนสถานะเป็น ไม่ใช้งาน แล้ว"** | ☐ |
| 2 | VERIFY แถว DOMESTIC×GOODS | — | pill สถานะแสดง "ไม่ใช้งาน" | ☐ |

---

### กลุ่ม BLK — Bulk delete skip `used>0` (BR-04/R06)

#### TC-BLK01 — Bulk delete แถวผสม (บาง `used=0` บาง `used>0`) — ลบเฉพาะที่ลบได้ ข้ามที่เหลือ (happy, S-07/AC-10, EC-07)
- group: BLK · ความสำคัญ: สูง · trace: S-07/AC-10 · BR-04(R06) · error(skip) `BR_USED_GT_ZERO`
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=เลือก SCB(used=0) + LOCAL(used=82) + FOREIGN(used=14) รวม 3 แถว · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups)
- ชุดข้อมูล: —
- ผ่านเมื่อ: ลบสำเร็จเฉพาะ SCB (1 รายการ), ข้าม 2 รายการที่ `used>0`, toast ระบุยอดข้าม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox แถว **SCB**, **LOCAL**, **FOREIGN** | — | bulk bar แสดง "เลือก 3 รายการ" | ☐ |
| 2 | CLICK ปุ่ม **"ลบ"** ใน bulk bar | — | modal เปิด หัวข้อ **"ลบ Posting Group"** subtitle **"เลือกไว้ 3 รายการ · 2 รายการจะถูกข้าม (มีการบันทึกบัญชีผ่านแล้ว)"** | ☐ |
| 3 | VERIFY เนื้อ modal | — | ข้อความ **"ยืนยันการลบ — รายการที่มี journal post ผ่าน mapping แล้วจะไม่ถูกลบ (R06 soft-delete) ใช้วิธีเปลี่ยนสถานะเป็น \"ไม่ใช้งาน\" แทน"** | ☐ |
| 4 | VERIFY ปุ่มยืนยันใน footer | — | ปุ่มแสดง **"ลบ 1 รายการ"** (เฉพาะที่ลบได้จริง = SCB) | ☐ |
| 5 | CLICK **"ลบ 1 รายการ"** | — | ปุ่มเปลี่ยนเป็น spinner + "กำลังลบ…" ชั่วคราว จากนั้น modal ปิด | ☐ |
| 6 | WAIT จน toast ปรากฏ | — | toast **"ลบแล้ว 1 รายการ · ข้าม 2 (มีการบันทึกบัญชีผ่านแล้ว)"** | ☐ |
| 7 | VERIFY ตาราง Posting Groups | — | แถว `SCB` หายไปจากตาราง; แถว `LOCAL` และ `FOREIGN` ยังอยู่เหมือนเดิม | ☐ |

#### TC-BLK02 — Bulk delete ที่ทุกแถวเลือกมี `used>0` — ไม่ลบอะไรเลย
- group: BLK · ความสำคัญ: สูง · trace: S-07/AC-10 (AC2) · BR-04(R06)
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=เลือก LOCAL(used=82) + KBANK(used=203) · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups)
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปุ่มยืนยันแสดง "ลบ 0 รายการ" และเป็น disabled — ไม่มีทางกดยืนยันได้จริง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox แถว **LOCAL**, **KBANK** → CLICK **"ลบ"** | — | modal เปิด subtitle **"เลือกไว้ 2 รายการ · 2 รายการจะถูกข้าม (มีการบันทึกบัญชีผ่านแล้ว)"** | ☐ |
| 2 | VERIFY ปุ่มยืนยันใน footer | — | ปุ่มแสดง **"ลบ 0 รายการ"** และมีสถานะ `disabled` (กดไม่ได้) | ☐ |
| 3 | CLICK ปุ่ม **"ยกเลิก"** | — | modal ปิด ไม่มีการลบเกิดขึ้น; ทั้งสองแถวยังอยู่ในตารางเหมือนเดิม | ☐ |

#### TC-BLK03 — Bulk delete แถวที่ `used=0` ทั้งหมด — ลบครบ ไม่มี clause ข้าม
- group: BLK · ความสำคัญ: กลาง · trace: S-07/AC-10 · BR-04(R06)
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=SCB เป็น used=0 รายเดียวที่เหมาะ ใช้แถวเดียวก็พอพิสูจน์ · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups)
- ชุดข้อมูล: —
- ผ่านเมื่อ: toast ไม่มี " · ข้าม" clause เมื่อ skip=0

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox แถว **SCB** เท่านั้น → CLICK **"ลบ"** | — | modal subtitle **"เลือกไว้ 1 รายการ"** (ไม่มี clause ข้าม เพราะ skip=0) | ☐ |
| 2 | CLICK **"ลบ 1 รายการ"** | — | toast **"ลบแล้ว 1 รายการ"** (ไม่มี " · ข้าม" ต่อท้าย เพราะไม่มีรายการถูกข้าม) | ☐ |
| 3 | VERIFY ตาราง | — | แถว SCB หายไปจากตาราง | ☐ |

#### TC-BLK04 — Bulk delete บน tab 2 (Setup) — พฤติกรรมเดียวกันกับ tab1
- group: BLK · ความสำคัญ: กลาง · trace: S-07/AC-10 · BR-04(R06)
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=s1(used=340, ลบไม่ได้) + s3(used=0, ลบได้) · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK tab **"General Posting Setup"**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ข้าม s1 ลบเฉพาะ s3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox แถว **DOMESTIC × GOODS** (s1) และ **FOREIGN × GOODS** (s3) → CLICK **"ลบ"** | — | modal หัวข้อ **"ลบ Posting Setup"** subtitle **"เลือกไว้ 2 รายการ · 1 รายการจะถูกข้าม (มีการบันทึกบัญชีผ่านแล้ว)"** | ☐ |
| 2 | CLICK **"ลบ 1 รายการ"** | — | toast **"ลบแล้ว 1 รายการ · ข้าม 1 (มีการบันทึกบัญชีผ่านแล้ว)"** | ☐ |
| 3 | VERIFY ตาราง Setup | — | แถว `FOREIGN × GOODS` หายไป; แถว `DOMESTIC × GOODS` ยังอยู่ | ☐ |

---

### กลุ่ม IMP — นำเข้า CSV merge-only (BR-07, LOCK-03)

#### TC-IMP01 — นำเข้า Posting Groups: ไฟล์ valid ทั้งหมด (happy, S-08/AC-11)
- group: IMP · ความสำคัญ: สูง (critical) · trace: S-08/AC-11 · BR-07 · LOCK-03
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ทะเบียนปกติ 7 กลุ่ม · files=`pg_groups_valid.csv`
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups) → CLICK ปุ่ม **"นำเข้า CSV"**
- ชุดข้อมูล: —
- ผ่านเมื่อ: import ทั้ง 2 แถวสำเร็จ ไม่มีแถวถูกข้าม ทะเบียนเดิมไม่ถูกแตะ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY modal step "pick" | — | หัวข้อ **"นำเข้า Posting Groups จากไฟล์"** subtitle **"CSV — ระบุสถานะได้ในไฟล์ · เพิ่มรายการใหม่เท่านั้น ทะเบียนเดิมไม่ถูกแตะ"**; เนื้อ modal มีแค่ upload-box "เลือกไฟล์ CSV" — **ไม่มี** ตัวเลือกโหมดใดๆ | ☐ |
| 2 | UPLOAD `pg_groups_valid.csv` | — | modal เปลี่ยนไป step "preview" | ☐ |
| 3 | VERIFY summary chip | — | **"ตรวจแล้ว 2 แถว — นำเข้าได้ 2 · ติดปัญหา 0 (แถวผิดจะถูกข้าม)"** (สีเขียว is-success) | ☐ |
| 4 | VERIFY แต่ละแถวในตาราง preview | — | ทั้ง 2 แถว (`NEWBANK`, `NEWCUST`) แสดง **"✓ พร้อมนำเข้า"** | ☐ |
| 5 | VERIFY ปุ่มยืนยัน | — | ปุ่มแสดง **"นำเข้า 2 แถว"** (ไม่ disabled) | ☐ |
| 6 | CLICK **"นำเข้า 2 แถว"** | — | ปุ่มเปลี่ยนเป็น spinner + "กำลังนำเข้า…" ชั่วคราว → step เปลี่ยนเป็น "done" | ☐ |
| 7 | WAIT จน toast ปรากฏ | — | toast **"นำเข้าแล้ว 2 รายการ"** (ไม่มี " · ข้าม" เพราะไม่มีแถวถูกข้าม) | ☐ |
| 8 | VERIFY เนื้อ modal step "done" | — | **"นำเข้าเสร็จ 2 รายการ (สถานะตามไฟล์)"** ไม่มีตารางแถวข้าม (เพราะ err=0) | ☐ |
| 9 | CLICK **"ปิด"** แล้ว VERIFY ตาราง Posting Groups | — | แถวใหม่ `NEWBANK` (สถานะ "ใช้งาน") และ `NEWCUST` (สถานะ "ร่าง") ปรากฏ; ทะเบียนเดิม 7 แถวยังอยู่ครบ (รวมเป็น 9 แถว) | ☐ |

#### TC-IMP02 — นำเข้า Posting Groups: ไฟล์ผสม valid/invalid (happy+negative, S-08/AC-12, EC-08)
- group: IMP · ความสำคัญ: สูง (critical) · trace: S-08/AC-12 · error `CODE_DUPLICATE`/`BAD_STATUS`
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ทะเบียนปกติ (มี code `LOCAL` อยู่แล้ว) · files=`pg_groups_mixed.csv`
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups) → CLICK **"นำเข้า CSV"**
- ชุดข้อมูล: —
- ผ่านเมื่อ: 3 แถว valid (`IMPORT-V`,`RAW`,`BBL`) ถูก import, 2 แถว invalid (`LOCAL` dup, `BAD1` bad status) ถูกข้าม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `pg_groups_mixed.csv` | — | step เปลี่ยนเป็น "preview" | ☐ |
| 2 | VERIFY summary chip | — | **"ตรวจแล้ว 5 แถว — นำเข้าได้ 3 · ติดปัญหา 2 (แถวผิดจะถูกข้าม)"** (สีเหลือง is-warning) | ☐ |
| 3 | VERIFY แถว `IMPORT-V`, `RAW`, `BBL` | — | ทั้ง 3 แถวแสดง **"✓ พร้อมนำเข้า"** | ☐ |
| 4 | VERIFY แถว `LOCAL` | — | แสดง **"✗ รหัสซ้ำกับทะเบียน (CODE_DUPLICATE)"**; hover title แสดงรายการ error เต็ม | ☐ |
| 5 | VERIFY แถว `BAD1` | — | แสดง **"✗ สถานะไม่ถูกต้อง (BAD_STATUS — ใช้ ใช้งาน/ไม่ใช้งาน/ร่าง หรือเว้นว่าง=ร่าง)"** | ☐ |
| 6 | VERIFY ปุ่มยืนยัน | — | ปุ่มแสดง **"นำเข้า 3 แถว"** | ☐ |
| 7 | CLICK **"นำเข้า 3 แถว"** | — | toast **"นำเข้าแล้ว 3 รายการ · ข้าม 2 แถว"** | ☐ |
| 8 | VERIFY เนื้อ modal step "done" | — | **"นำเข้าเสร็จ 3 รายการ (สถานะตามไฟล์) · ข้าม 2 แถว"** + ตารางแถวข้าม 2 แถว (`LOCAL`, `BAD1`) พร้อมสาเหตุ | ☐ |
| 9 | CLICK **"ปิด"** แล้ว VERIFY ตาราง | — | แถวใหม่ `IMPORT-V`, `RAW`, `BBL` ปรากฏ; **ไม่มี** แถวชื่อ `LOCAL` ซ้ำเพิ่ม (ของเดิมยังเป็นตัวเดียว, ไม่ถูกทับ) | ☐ |

#### TC-IMP03 — นำเข้าแถว blank status → default เป็น "ร่าง" (S-08/AC-13, BR-07, EC-09)
- group: IMP · ความสำคัญ: สูง · trace: S-08/AC-13 · BR-07
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ทะเบียนปกติ · files=`pg_groups_mixed.csv` (แถว `RAW` มี status ว่าง)
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups) → CLICK **"นำเข้า CSV"**
- ชุดข้อมูล: —
- ผ่านเมื่อ: แถว `RAW` (status ว่างในไฟล์) ถูก import ด้วยสถานะ "ร่าง"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `pg_groups_mixed.csv` | — | step "preview" | ☐ |
| 2 | VERIFY คอลัมน์ "สถานะ" ของแถว `RAW` ใน preview table | — | แสดง pill **"ร่าง"** (แม้ในไฟล์ CSV ต้นฉบับช่อง status ของแถวนี้เว้นว่าง) | ☐ |
| 3 | CLICK **"นำเข้า 3 แถว"** แล้ว CLICK **"ปิด"** | — | import สำเร็จ | ☐ |
| 4 | VERIFY แถว `RAW` ในตาราง Posting Groups | — | pill สถานะแสดง **"ร่าง"** | ☐ |

#### TC-IMP04 — Import modal ไม่มีตัวเลือกโหมด Replace/Merge-overwrite (negative-absence, AC-14, LOCK-03) `[AI-DEFAULT: N]` — see FN01
> เคสนี้รวมเข้ากับ **TC-FN01** ในกลุ่ม FN ด้านล่าง (ทั้ง AC-14 และ LOCK-03 verify ผ่านเคสเดียวกัน) — ระบุ ID สำรองไว้เพื่อ trace จาก 06_TESTS แต่ไม่ derive เป็นเคสซ้ำ

#### TC-IMP05 — นำเข้า Posting Setup: ไฟล์ valid (happy)
- group: IMP · ความสำคัญ: สูง · trace: S-08/AC-11 (tab2 variant) · BR-07
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=มี s1/s2/s3 (ไม่มี FOREIGN×SERVICE) · files=`pg_setup_valid.csv`
- Start: OPEN หน้า "GL Posting Group" → CLICK tab **"General Posting Setup"** → CLICK **"นำเข้า CSV"**
- ชุดข้อมูล: —
- ผ่านเมื่อ: import 1 แถวสำเร็จ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `pg_setup_valid.csv` | — | step "preview"; summary **"ตรวจแล้ว 1 แถว — นำเข้าได้ 1 · ติดปัญหา 0 (แถวผิดจะถูกข้าม)"** | ☐ |
| 2 | VERIFY แถว preview | — | แสดง badge `FOREIGN`/`SERVICE` + **"✓ พร้อมนำเข้า"** | ☐ |
| 3 | CLICK **"นำเข้า 1 แถว"** | — | toast **"นำเข้าแล้ว 1 รายการ"** | ☐ |
| 4 | CLICK **"ปิด"** แล้ว VERIFY ตาราง Setup | — | แถวใหม่ `FOREIGN`×`SERVICE` ปรากฏ (รวมเป็น 4 แถว) | ☐ |

#### TC-IMP06 — นำเข้า Posting Setup: ไฟล์ผสม valid/invalid (negative, EC-08)
- group: IMP · ความสำคัญ: สูง · trace: S-08/AC-12 (tab2) · error `combination-duplicate (R04)`
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=มี s1(DOMESTIC×GOODS), s3(FOREIGN×GOODS) อยู่แล้ว · files=`pg_setup_mixed.csv`
- Start: OPEN หน้า "GL Posting Group" → CLICK tab **"General Posting Setup"** → CLICK **"นำเข้า CSV"**
- ชุดข้อมูล: —
- ผ่านเมื่อ: 1 แถว valid (FOREIGN×SERVICE) import สำเร็จ, 2 แถว dup ถูกข้าม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `pg_setup_mixed.csv` | — | step "preview"; summary **"ตรวจแล้ว 3 แถว — นำเข้าได้ 1 · ติดปัญหา 2 (แถวผิดจะถูกข้าม)"** | ☐ |
| 2 | VERIFY แถว `FOREIGN`×`SERVICE` | — | **"✓ พร้อมนำเข้า"** | ☐ |
| 3 | VERIFY แถว `DOMESTIC`×`GOODS` | — | **"✗ combination ซ้ำกับทะเบียน (R04)"** (ซ้ำกับ s1) | ☐ |
| 4 | VERIFY แถว `FOREIGN`×`GOODS` | — | **"✗ combination ซ้ำกับทะเบียน (R04)"** (ซ้ำกับ s3 — error แรกที่ตรวจพบ แม้บัญชี `9-9-99` ก็ไม่มีใน COA เช่นกัน แต่รายการ error ตัวแรกที่แสดงคือ combination dup ตามลำดับการตรวจในโค้ด) | ☐ |
| 5 | CLICK **"นำเข้า 1 แถว"** | — | toast **"นำเข้าแล้ว 1 รายการ · ข้าม 2 แถว"** | ☐ |
| 6 | CLICK **"ปิด"** แล้ว VERIFY ตาราง | — | แถวใหม่ `FOREIGN`×`SERVICE` ปรากฏ; s1/s3 ไม่ถูกแตะ/ทับ | ☐ |

#### TC-IMP07 — ปุ่มดาวน์โหลด template ตัวอย่าง (ทั้ง 2 tab)
- group: IMP · ความสำคัญ: กลาง · trace: 01_UI P-06
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups) → CLICK **"นำเข้า CSV"**
- ชุดข้อมูล: —
- ผ่านเมื่อ: กดดาวน์โหลด template ได้ทั้ง 2 tab พร้อม toast ยืนยัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY modal step "pick" | — | มีปุ่ม **"ดาวน์โหลด template ตัวอย่าง"** ที่ footer (secondary) | ☐ |
| 2 | CLICK **"ดาวน์โหลด template ตัวอย่าง"** | — | ไฟล์ `postgrp_groups_import_template.csv` เริ่มดาวน์โหลด; toast **"ดาวน์โหลด template ตัวอย่างแล้ว"** | ☐ |
| 3 | CLICK **"ปิด"** แล้ว CLICK tab **"General Posting Setup"** → CLICK **"นำเข้า CSV"** → CLICK **"ดาวน์โหลด template ตัวอย่าง"** | — | ไฟล์ `postgrp_setup_import_template.csv` ดาวน์โหลด; toast เดียวกัน | ☐ |

#### TC-IMP08 — อัปโหลดไฟล์ที่ไม่ใช่ CSV โครงสร้างข้อมูล — parse-and-fail แบบไม่ crash `[AI-DEFAULT]` (edge: FU-02)
- group: IMP · ความสำคัญ: กลาง · trace: 05_RULES §5.5 FU-02 `[AI-DEFAULT]`
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=`not_a_valid.csv`
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups) → CLICK **"นำเข้า CSV"**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ระบบไม่ crash — parse แล้วขึ้น preview ที่ทุกแถว/ไม่มีแถว valid (ไม่ใช่ error หน้าขาว/หยุดทำงาน)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD `not_a_valid.csv` | — | step เปลี่ยนเป็น "preview" ตามปรกติ **ไม่ crash หน้าจอ ไม่ค้าง** | ☐ |
| 2 | VERIFY summary chip | — | **"ติดปัญหา"** เท่ากับจำนวนแถวทั้งหมดที่ parse ได้ (เนื้อหาไม่ตรง column ใดๆ → ทุกแถวเป็น error REQUIRED เพราะ code/name/account_1 ว่างหมด) — ปุ่ม "นำเข้า 0 แถว" ปรากฏเป็น `disabled` | ☐ |
| 3 | CLICK **"ยกเลิก"** | — | modal ปิดปรกติ ไม่มีการนำเข้าใดๆ เกิดขึ้น ทะเบียนเดิมไม่เปลี่ยน | ☐ |

---

### กลุ่ม EXP — ส่งออก CSV (S-09/AC-15)

#### TC-EXP01 — Export tab1 กรองตาม kind=vendor (S-09/AC-15)
- group: EXP · ความสำคัญ: กลาง · trace: S-09/AC-15
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ทะเบียนปกติ (2 แถว vendor: LOCAL, FOREIGN) · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups)
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไฟล์ export มีแค่แถว vendor 2 แถว ตรงกับ filter, toast ระบุจำนวน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "เจ้าหนี้ (Vendor)" → ช่อง filter **"ประเภทกลุ่ม"** | — | ตารางกรองเหลือ 2 แถว (LOCAL, FOREIGN) | ☐ |
| 2 | CLICK ปุ่ม **"ส่งออก CSV"** | — | ไฟล์ `postgrp_groups_export_YYYY-MM-DD.csv` เริ่มดาวน์โหลด | ☐ |
| 3 | WAIT จน toast ปรากฏ | — | toast **"ส่งออก 2 รายการเป็น CSV แล้ว"** | ☐ |
| 4 | VERIFY เนื้อไฟล์ที่ดาวน์โหลด (เปิดดู) | — | header ตรงกับ template นำเข้า: `code,kind,name_th,name_en,account_1,account_2,status`; มีแค่ 2 แถว (LOCAL, FOREIGN); คอลัมน์ status เป็นภาษาไทย ("ใช้งาน"); ไฟล์มี UTF-8 BOM นำหน้า | ☐ |

#### TC-EXP02 — Export tab2 (S-09/AC-15 tab2 variant)
- group: EXP · ความสำคัญ: กลาง · trace: S-09/AC-15
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=3 setups (ไม่มี filter) · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK tab **"General Posting Setup"**
- ชุดข้อมูล: —
- ผ่านเมื่อ: export ครบ 3 แถว, toast ถูกต้อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **"ส่งออก CSV"** (ไม่ตั้ง filter) | — | ไฟล์ `postgrp_setup_export_YYYY-MM-DD.csv` ดาวน์โหลด | ☐ |
| 2 | WAIT จน toast ปรากฏ | — | toast **"ส่งออก 3 รายการเป็น CSV แล้ว"** | ☐ |
| 3 | VERIFY เนื้อไฟล์ | — | header `bus,prod,sales_acct,purchase_acct,cogs_acct,status`; 3 แถวตรงกับทะเบียน; status ภาษาไทย | ☐ |

#### TC-EXP03 — Export หลังล้าง filter — ครบทุกแถว (roundtrip columns)
- group: EXP · ความสำคัญ: ต่ำ · trace: S-09/AC-15
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ทะเบียนปกติ 7 แถว (tab1) · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups) → SELECT "ใช้งาน" ที่ stat card ก่อน (ตั้ง filter ไว้ก่อน) → CLICK stat card "ใช้งาน" อีกครั้งเพื่อล้าง (toggle กลับ)
- ชุดข้อมูล: —
- ผ่านเมื่อ: export ได้ทั้ง 7 แถวเมื่อไม่มี filter

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY filter สถานะปัจจุบัน | — | "ทุกสถานะ" (ไม่มี filter ค้าง) | ☐ |
| 2 | CLICK **"ส่งออก CSV"** | — | ไฟล์ดาวน์โหลด | ☐ |
| 3 | VERIFY toast | — | toast **"ส่งออก 7 รายการเป็น CSV แล้ว"** (ครบทุกแถวในทะเบียน) | ☐ |

---

### กลุ่ม L — รายการ/ค้นหา/กรอง/สลับ tab (P-01)

#### TC-L01 — เข้าหน้าครั้งแรก landing ที่ tab "Posting Groups" พร้อม stat cards ถูกต้อง
- group: L · ความสำคัญ: กลาง · trace: 01_UI P-01
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ทะเบียนปกติ (7 groups: 5 active, 1 draft, 1 inactive) · files=—
- Start: OPEN หน้า "GL Posting Group"
- ชุดข้อมูล: —
- ผ่านเมื่อ: ค่า stat cards ตรงกับ seed จริง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY tab bar | — | tab **"Posting Groups"** เป็น active (สีแดง underline) badge นับ = 7; tab "General Posting Setup" badge = 3 | ☐ |
| 2 | VERIFY stat card "ทั้งหมด" | — | ค่า = 7 | ☐ |
| 3 | VERIFY stat card "ใช้งาน" | — | ค่า = 5 | ☐ |
| 4 | VERIFY stat card "ไม่ใช้งาน" | — | ค่า = 1 | ☐ |
| 5 | VERIFY stat card "ร่าง" | — | ค่า = 1 | ☐ |
| 6 | VERIFY table footer | — | "แสดง 7 จาก 7 กลุ่ม" | ☐ |

#### TC-L02 — สลับ tab ล้าง bulk selection + status filter (EC-10, OB-6)
- group: L · ความสำคัญ: สูง · trace: EC-10
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups)
- ชุดข้อมูล: —
- ผ่านเมื่อ: สลับ tab แล้ว selection และ status filter ของ tab เดิมถูกล้างทั้งคู่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK stat card **"ใช้งาน"** (ตั้ง status filter) แล้ว CLICK checkbox แถวใดแถวหนึ่ง (ตั้ง bulk selection) | — | filter active บน "ใช้งาน"; bulk bar ปรากฏ "เลือก 1 รายการ" | ☐ |
| 2 | CLICK tab **"General Posting Setup"** | — | สลับไป tab setup สำเร็จ | ☐ |
| 3 | CLICK กลับมาที่ tab **"Posting Groups"** | — | stat card "ใช้งาน" **ไม่** highlight แล้ว (filter กลับเป็น "ทั้งหมด"); bulk bar **หายไป** (selection ถูกล้าง); ตารางแสดงครบ 7 แถว | ☐ |

#### TC-L03 — Stat card quick-filter toggle (คลิกซ้ำเพื่อยกเลิก filter)
- group: L · ความสำคัญ: กลาง · trace: 01_UI P-01
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups)
- ชุดข้อมูล: —
- ผ่านเมื่อ: คลิก stat card ซ้ำ toggle filter กลับเป็น "ทั้งหมด"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK stat card **"ไม่ใช้งาน"** | — | card highlight (`.is-on`); ตารางกรองเหลือ 1 แถว (SCRAP) | ☐ |
| 2 | CLICK stat card **"ไม่ใช้งาน"** อีกครั้ง (toggle) | — | filter กลับเป็น "ทั้งหมด"; ตารางแสดงครบ 7 แถว | ☐ |

#### TC-L04 — กรองด้วย kind dropdown (tab1 เท่านั้น)
- group: L · ความสำคัญ: กลาง · trace: 01_UI P-01
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups)
- ชุดข้อมูล: —
- ผ่านเมื่อ: กรองตาม kind ได้ถูกต้อง + ปุ่ม "ล้าง" ปรากฏ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "สินค้าคงคลัง (Inventory)" → dropdown **"ประเภทกลุ่ม"** ในแถบ filter | — | ตารางกรองเหลือ 2 แถว (FINISHED, SCRAP); ปุ่ม **"ล้าง"** ปรากฏขึ้น (เดิมไม่มีตอนไม่ได้ตั้ง filter) | ☐ |
| 2 | CLICK ปุ่ม **"ล้าง"** | — | filter kind กลับเป็น "ทุกประเภทกลุ่ม"; ตารางแสดงครบ 7 แถว; ปุ่ม "ล้าง" หายไป | ☐ |

#### TC-L05 — ค้นหาด้วยรหัส/ชื่อกลุ่ม (tab1)
- group: L · ความสำคัญ: กลาง · trace: 01_UI P-01
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups)
- ชุดข้อมูล: —
- ผ่านเมื่อ: ค้นหาด้วยคำที่ตรงกับ code/ชื่อ TH/ชื่อ EN เจอผลถูกต้อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "kbank" (พิมพ์เล็ก) → ช่องค้นหา placeholder **"ค้นหารหัส หรือ ชื่อกลุ่ม..."** | — | ตารางกรองเหลือ 1 แถว (KBANK) — ค้นหาไม่สนตัวพิมพ์ใหญ่/เล็ก | ☐ |
| 2 | TYPE "ธนาคาร" (ค้นหาด้วยชื่อ TH) | — | ตารางกรองเหลือ 2 แถว ที่มีคำ "ธนาคาร" ในชื่อ (KBANK, SCB) | ☐ |

#### TC-L06 — ค้นหาไม่เจอผล → empty state
- group: L · ความสำคัญ: กลาง · trace: 01_UI §1.6, EC empty
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups)
- ชุดข้อมูล: —
- ผ่านเมื่อ: แสดง empty state ตามข้อความจริงจาก HTML

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ZZZNOTEXIST" → ช่องค้นหา | — | ตารางหายไป แสดง empty state แทน: หัวข้อ **"ไม่พบรายการที่ตรงกับเงื่อนไข"** คำอธิบาย **"ลองปรับคำค้นหรือล้างตัวกรอง"** | ☐ |
| 2 | CLICK ปุ่ม **"ล้าง"** (ปรากฏเพราะมี filter ค้นหาอยู่) | — | ตารางกลับมาแสดงครบ 7 แถว | ☐ |

#### TC-L07 — ค้นหา tab2 ด้วยกลุ่มธุรกิจ/สินค้า
- group: L · ความสำคัญ: กลาง · trace: 01_UI P-01
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK tab **"General Posting Setup"**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ค้นหาด้วยคำที่ตรงกับ bus+prod concat เจอผลถูกต้อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "foreign" → ช่องค้นหา placeholder **"ค้นหากลุ่มธุรกิจ/สินค้า..."** | — | ตารางกรองเหลือ 1 แถว (FOREIGN × GOODS) | ☐ |

#### TC-L08 — Empty state บน tab2 เมื่อกรองไม่เจอ
- group: L · ความสำคัญ: ต่ำ · trace: 01_UI §1.6
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK tab **"General Posting Setup"**
- ชุดข้อมูล: —
- ผ่านเมื่อ: empty state เดียวกับ tab1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "ไม่ใช้งาน" → dropdown สถานะ (ไม่มี setup ที่สถานะนี้ในทะเบียน) | — | ตารางหายไป แสดง empty state: **"ไม่พบรายการที่ตรงกับเงื่อนไข"** / **"ลองปรับคำค้นหรือล้างตัวกรอง"** | ☐ |

---

### กลุ่ม COA — COA dropdown filter accuracy (§2.5, AC-16)

#### TC-COA01 — Vendor `account_1` dropdown แสดงเฉพาะบัญชี type=liability (AC-16)
- group: COA · ความสำคัญ: สูง · trace: AC-16 · BR-01(R01,R02) · ENG-PG-01
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups) → CLICK **"เพิ่ม Posting Group"** → SELECT "เจ้าหนี้ (Vendor)"
- ชุดข้อมูล: —
- ผ่านเมื่อ: ตัวเลือกทั้งหมดในช่อง "บัญชีเจ้าหนี้ (AP control)" เป็น liability เท่านั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK เปิด dropdown ช่อง **"บัญชีเจ้าหนี้ (AP control)"** | — | รายการที่แสดงมีแค่ 4 ตัว: `2-1-10-01`,`2-1-10-02`,`2-1-20`,`2-1-30` (ทั้งหมด type=liability) — ไม่มีบัญชี asset/income/expense ปน | ☐ |
| 2 | CLICK เปิด dropdown ช่อง **"บัญชีภาษีซื้อ (Input VAT)"** | — | รายการที่แสดงมีแค่บัญชี type=asset (6 ตัว: `1-1-10-01/02/03`,`1-1-20-01`,`1-1-30-01`,`1-1-40`) | ☐ |

#### TC-COA02 — Inventory `account_2` (Interim) dropdown แสดงทั้ง asset **และ** liability (dual-type)
- group: COA · ความสำคัญ: สูง · trace: BR-01 note dual-type (§2.5)
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK **"เพิ่ม Posting Group"** → SELECT "สินค้าคงคลัง (Inventory)"
- ชุดข้อมูล: —
- ผ่านเมื่อ: dropdown "บัญชี Interim" มีทั้ง asset และ liability

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK เปิด dropdown ช่อง **"บัญชี Interim (รับของยังไม่วางบิล)"** | — | รายการรวมทั้ง type=asset (6 ตัว) และ type=liability (4 ตัว) = 10 ตัวเลือก — ไม่ใช่แค่ asset อย่างเดียว | ☐ |

#### TC-COA03 — Customer `account_1` = asset, `account_2` = liability (AC-16, ตรวจครบชุด kind ที่เหลือ)
- group: COA · ความสำคัญ: สูง · trace: AC-16 · BR-01
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK **"เพิ่ม Posting Group"** → SELECT "ลูกหนี้ (Customer)"
- ชุดข้อมูล: —
- ผ่านเมื่อ: AR control = asset filter, Output VAT = liability filter

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK เปิด dropdown ช่อง **"บัญชีลูกหนี้ (AR control)"** | — | ตัวเลือกทั้งหมด type=asset (6 ตัว) | ☐ |
| 2 | CLICK เปิด dropdown ช่อง **"บัญชีภาษีขาย (Output VAT)"** | — | ตัวเลือกทั้งหมด type=liability (4 ตัว) | ☐ |
| 3 | SELECT "ธนาคาร (Bank)" → ประเภท Posting Group (สลับ kind ตรวจต่อ) | — | render ช่อง "บัญชีเงินฝาก (GL)" เดี่ยว | ☐ |
| 4 | CLICK เปิด dropdown ช่อง **"บัญชีเงินฝาก (GL)"** | — | ตัวเลือกทั้งหมด type=asset (6 ตัว) | ☐ |

#### TC-COA04 — ค้นหาในดรอปดาวน์ COA แล้วไม่พบ → "ไม่พบรายการ" `[AI-DEFAULT]` (edge: DI-04)
- group: COA · ความสำคัญ: กลาง · trace: 05_RULES §5.5 DI-04 `[AI-DEFAULT]`
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK **"เพิ่ม Posting Group"** → SELECT "เจ้าหนี้ (Vendor)"
- ชุดข้อมูล: —
- ผ่านเมื่อ: พิมพ์คำค้นที่ไม่มีทางตรง → เห็นข้อความ empty ทั่วไป (ไม่มีเหตุผลว่าโดน type-filter ตัดออก)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK เปิด dropdown ช่อง **"บัญชีเจ้าหนี้ (AP control)"** | — | sdd-panel เปิด | ☐ |
| 2 | TYPE "zzzไม่มีจริง999" → ช่องค้นหาใน sdd-panel (placeholder "ค้นหา...") | — | รายการกรองเหลือ 0 ตัวเลือก แสดงข้อความ **"ไม่พบรายการ"** (ข้อความทั่วไป — ไม่มีคำอธิบายเพิ่มว่าเพราะ type-filter ตัดบัญชี asset/income/expense ออกไปแล้ว ตามที่ DI-04 ระบุว่ายังไม่ implement) | ☐ |

#### TC-COA05 — View drawer resolve ชื่อบัญชีจาก COA แบบ live-lookup (DI-03, สังเกตผ่านของปรกติ)
- group: COA · ความสำคัญ: ต่ำ · trace: 05_RULES §5.5 DI-03 `[AI-DEFAULT]`
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียน LOCAL (account_1=2-1-10-01) · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups) → CLICK แถว **LOCAL**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ชื่อบัญชีที่แสดงตรงกับชื่อปัจจุบันใน `COA_ACCOUNTS` mock (สาธิตว่า resolve จาก COA แบบ live ไม่ใช่ snapshot ที่บันทึกไว้ตอนสร้าง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY การ์ดบัญชีใน section "บัญชีที่ผูก (จากผังบัญชี)" | — | แสดง `2-1-10-01` พร้อมชื่อ **"เจ้าหนี้การค้า"** (ชื่อปัจจุบันจาก COA mock ไม่ใช่ชื่อที่ถูก snapshot ไว้ตอนสร้าง — สาธิต `acctName()` live-lookup) | ☐ |

---

### กลุ่ม FN — Negative-absence: FN-40 banned items + Scope Lock verify

> เคสกลุ่มนี้ **พิสูจน์ว่าสิ่งที่ถูกแบน/deferred "ไม่มีอยู่จริง"** ในหน้าจอ — Expected คือ "ไม่พบ" ไม่ใช่
> "พบ" ตาม FN-40 list ของ BRD §3.2 Out of Scope + Scope Lock (00_OVERVIEW §0.11)

#### TC-FN01 — Import modal ไม่มีตัวเลือกโหมด Replace/Merge-overwrite เลย (AC-14, LOCK-03) — includes TC-IMP04
- group: FN · ความสำคัญ: สูง (compliance) · trace: AC-14 · LOCK-03 · BR-07
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups) → CLICK **"นำเข้า CSV"**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่พบ radio/toggle/dropdown ใดๆ ที่เกี่ยวกับ "โหมด" การนำเข้าในทั้ง 3 step (pick/preview/done)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY เนื้อ modal step "pick" ทั้งหมด | — | มีเพียง upload-box "เลือกไฟล์ CSV" + ปุ่ม "ดาวน์โหลด template ตัวอย่าง" + "ปิด" — **ไม่มี** radio button, checkbox, หรือ dropdown ที่เขียนคำว่า "โหมด"/"Replace"/"Merge"/"ทับ"/"เขียนทับ" ที่ใดเลย — นี่คือ pass condition ของเคสนี้เอง (negative test) | ☐ |
| 2 | UPLOAD `pg_groups_mixed.csv` แล้ว VERIFY เนื้อ modal step "preview" | — | ไม่มีตัวเลือกโหมดปรากฏขึ้นในขั้นนี้เช่นกัน — มีแค่ summary chip + ตาราง preview + ปุ่ม "ยกเลิก"/"นำเข้า N แถว" | ☐ |
| 3 | CLICK **"นำเข้า N แถว"** แล้ว VERIFY เนื้อ modal step "done" | — | ไม่มีตัวเลือกโหมดในขั้นนี้เช่นกัน — มีแค่สรุปผล + ตารางแถวข้าม (ถ้ามี) + ปุ่ม "ปิด" | ☐ |

#### TC-FN02 — ไม่มีปุ่มลบรายตัว (single-row delete) ที่ใดในตาราง
- group: FN · ความสำคัญ: สูง (compliance) · trace: BR-04(R06) · BRD §3.2
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" (ทั้ง 2 tab)
- ชุดข้อมูล: —
- ผ่านเมื่อ: คอลัมน์ "จัดการ" ของทุกแถวมีแค่ไอคอนดินสอ (แก้ไข) ไม่มีไอคอนถังขยะ/ลบรายตัวเลย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY คอลัมน์ "จัดการ" ของทุกแถวใน tab Posting Groups | — | มีแค่ไอคอนดินสอเดียว (title "แก้ไข") ต่อแถว — **ไม่มี** ไอคอนถังขยะ/ปุ่มลบรายตัวใดๆ | ☐ |
| 2 | CLICK tab **"General Posting Setup"** → VERIFY คอลัมน์ "จัดการ" | — | เหมือนกัน มีแค่ไอคอนดินสอ ไม่มีปุ่มลบรายตัว | ☐ |
| 3 | VERIFY view drawer header actions (เปิดแถวใดก็ได้) | — | มีแค่ "แก้ไข" + "เปลี่ยนสถานะ" — ไม่มีปุ่ม "ลบ" ในระดับรายตัวที่นี่ (การลบมีแค่ผ่าน bulk bar เท่านั้น) | ☐ |

#### TC-FN03 — ไม่มีทางเปลี่ยน `kind` หลังสร้างได้จริง แม้พยายามทุกจุดที่เป็นไปได้
- group: FN · ความสำคัญ: สูง (compliance) · trace: BR-03(R05) · LOCK-02
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียนใดก็ได้ · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups) → CLICK ไอคอนดินสอที่แถวใดแถวหนึ่ง
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มี input/dropdown ให้กดเปลี่ยน kind เลยในหน้าแก้ไข (สรุปผลจาก TC-E03/E04 มาเป็น negative-absence statement)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ช่อง "ประเภท Posting Group" ในหน้าแก้ไข | — | เป็น `<div>` static เท่านั้น ไม่มี `<select>`/sdd-trigger ที่คลิกเปิดได้ — ไม่มี event handler ใดๆ ให้เปลี่ยนค่า | ☐ |
| 2 | PRESS Tab ไล่ลำดับ focus ผ่านฟอร์มทั้งหมด | — | ช่อง kind ไม่ถูกรวมใน tab order ที่ interactive (เพราะไม่ใช่ input จริง) | ☐ |

#### TC-FN04 — ไม่มี tab/หน้า "VAT Posting Setup" ที่ใดในฟีเจอร์นี้ (OQ-PG-01, out-of-scope Phase 2)
- group: FN · ความสำคัญ: สูง (compliance) · trace: 05_RULES Tax mapping gap (WARNING) · Scope boundary verify
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group"
- ชุดข้อมูล: —
- ผ่านเมื่อ: tab bar มีแค่ 2 tab เท่านั้น ไม่มี tab ที่ 3 เกี่ยวกับ VAT ที่ใดในหน้า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY tabbar บนสุดของหน้า | — | มีแค่ 2 ปุ่ม: **"Posting Groups"** และ **"General Posting Setup"** — ไม่มีตัวเลือกที่ 3 ชื่อ "VAT" หรือ "ภาษี" ที่ใดในหน้า | ☐ |
| 2 | VERIFY sidebar เมนู "การเงิน" | — | ไม่มีเมนูย่อยชื่อ "VAT Posting Setup" แยกออกมาต่างหาก | ☐ |

#### TC-FN05 — ไม่มี UI จัดการค่ากลุ่มธุรกิจ/กลุ่มสินค้า (business/product group master, OQ-PG-04, out-of-scope Phase 2)
- group: FN · ความสำคัญ: สูง (compliance) · trace: R09 (DYNAMIC, as-built 2-value) · Scope boundary verify
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK tab **"General Posting Setup"**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่ม/หน้าใดให้เพิ่ม/แก้ไขรายการ `bus_group`/`prod_group` เอง — dropdown มีแค่ 2 ค่าคงที่ (DOMESTIC/FOREIGN, GOODS/SERVICE)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หน้า tab "General Posting Setup" ทั้งหมด | — | ไม่มีปุ่ม/ไอคอน "จัดการกลุ่มธุรกิจ" หรือ "จัดการกลุ่มสินค้า" ที่ใด (ไม่มี master-data management UI สำหรับสองแกนนี้) | ☐ |
| 2 | CLICK **"เพิ่ม Setup"** → CLICK เปิด dropdown **"กลุ่มธุรกิจ (Business Group)"** | — | ตัวเลือกมีแค่ 2 ค่า: `DOMESTIC`, `FOREIGN` — ไม่มีปุ่ม "+เพิ่มค่าใหม่" ในรายการ | ☐ |
| 3 | CLICK เปิด dropdown **"กลุ่มสินค้า (Product Group)"** | — | ตัวเลือกมีแค่ 2 ค่า: `GOODS`, `SERVICE` (ยืนยัน as-built gap ตาม OQ-PG-04 — ไม่ใช่ 6-value set ของ Item Master) | ☐ |

#### TC-FN06 — ไม่มี action "Post to GL" / journal posting จริงในฟีเจอร์นี้ (BR-08, LOCK-05)
- group: FN · ความสำคัญ: สูง (compliance) · trace: BR-08 · LOCK-05
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=ใช้ระเบียนใดก็ได้ที่ used>0 · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK แถวที่ `used>0`
- ชุดข้อมูล: —
- ผ่านเมื่อ: view drawer ไม่มีปุ่ม/ลิงก์ที่ทำให้เกิดการ post บัญชีจริง หรือดู journal entries

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY view drawer header actions + footer ทั้งหมด | — | มีแค่ "แก้ไข" / "เปลี่ยนสถานะ" / "ปิด" — ไม่มีปุ่ม "Post", "บันทึกบัญชี", หรือลิงก์ไปดู journal entries ที่ใด | ☐ |
| 2 | VERIFY ค่า `used` ที่แสดง (ถ้ามีจุดแสดงในหน้าจอ) | — | เป็นตัวเลข read-only เท่านั้น — ไม่มีปุ่ม action ผูกกับตัวเลขนี้ (ยืนยันว่า feature นี้เป็น mapping layer เท่านั้น ไม่ post เอง) | ☐ |

#### TC-FN07 — ไม่มี UI สายอนุมัติ (approval/DOA) ที่ใดในฟีเจอร์นี้ (OB-5, LOCK-04)
- group: FN · ความสำคัญ: กลาง · trace: 00_OVERVIEW §0.4 · LOCK-04
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" (ทุกหน้าจอในฟีเจอร์นี้)
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีสถานะ "รออนุมัติ"/ช่อง "ผู้อนุมัติ"/ปุ่ม "ส่งขออนุมัติ" ที่ใดเลย ในทุกฟอร์ม/drawer/modal

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY dropdown สถานะในฟอร์มสร้าง/แก้ไข (ทั้ง 2 tab) | — | มีแค่ 3 ค่า: ร่าง/ใช้งาน/ไม่ใช้งาน — ไม่มีค่า "รออนุมัติ"/"pending approval" | ☐ |
| 2 | VERIFY view drawer และฟอร์ม ทั้งหมด | — | ไม่มีช่อง "ผู้อนุมัติ" หรือปุ่ม "ส่งขออนุมัติ"/"อนุมัติ"/"ปฏิเสธ" ที่ใด | ☐ |
| 3 | CLICK เปลี่ยนสถานะรายการใดๆ (อ้างอิงผลจาก TC-ST01) | — | เปลี่ยนทันทีไม่มีขั้นตอนรออนุมัติแทรก — ยืนยันซ้ำว่าไม่มีสายอนุมัติจริง | ☐ |

#### TC-FN08 — ไม่มี hint-i / tooltip help icon ที่ใดในฟอร์มของฟีเจอร์นี้ (OB-7)
- group: FN · ความสำคัญ: ต่ำ · trace: BRD §3.1 UI pattern note (OB-7)
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK **"เพิ่ม Posting Group"**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่พบไอคอน hint-i (คำอธิบายเพิ่มเติมแบบ hover) ที่ label ฟิลด์ใดในฟอร์มนี้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ทุก field label ในฟอร์มสร้าง Posting Group | — | ไม่มีไอคอน "?" หรือไอคอน info เล็กๆ ต่อท้าย label ที่ต้อง hover เพื่อดูคำอธิบาย (`.hint-i`) ที่ใดในฟอร์มนี้ — คำอธิบายเสริม (ถ้ามี) แสดงเป็นข้อความปกติใต้ label (`.field-help`) ไม่ใช่ tooltip ที่ต้อง hover | ☐ |

---

### กลุ่ม P — Permission matrix (Finance Lead vs Auditor)

#### TC-P01 — Finance Lead เข้าถึงทุก action ได้ครบ (baseline allow)
- group: P · ความสำคัญ: สูง · trace: 05_RULES §5.3
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" (ทั้ง 2 tab)
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปุ่ม create/edit/bulk/import/export ปรากฏครบทุกจุดสำหรับ Finance Lead

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY card toolbar ทั้ง 2 tab | — | ปุ่ม **"ส่งออก CSV"**, **"นำเข้า CSV"**, **"เพิ่ม Posting Group"/"เพิ่ม Setup"** ปรากฏครบทั้ง 3 ปุ่มในทั้ง 2 tab | ☐ |
| 2 | CLICK checkbox 1 แถว → VERIFY bulk bar | — | bulk bar ปรากฏพร้อมปุ่มครบ (สถานะ×3 + ลบ + ยกเลิก) | ☐ |
| 3 | VERIFY คอลัมน์ "จัดการ" ทุกแถว | — | ไอคอนดินสอ (แก้ไข) ปรากฏทุกแถว คลิกเปิด drawer แก้ไขได้จริง | ☐ |

#### TC-P02 — Auditor: เห็นได้แต่แก้ไขไม่ได้ (view+export only) — ⚠ ยืนยัน anchor
- group: P · ความสำคัญ: สูง · trace: 05_RULES §5.3 · BRD §4.2
- actor (role): Auditor (Watcher)
- Setup: role=qa_auditor (ตาม 06_TESTS §6.3) · seed=ทะเบียนปกติ · files=— · **⚠ หมายเหตุ:** ม็อค `f-postgrp.html` ที่ใช้ทดสอบ **hardcode identity เป็น "Tadswan C. · Finance Lead"** ที่มุมบนขวา ไม่มี UI ให้สลับเป็น Auditor ภายในไฟล์นี้ — เคสนี้จึง**ต้องรันบน environment ที่มีระบบ login จริงแยกจากม็อคไฟล์เดี่ยว** (ตามที่ 06_TESTS §6.3 กำหนด role `qa_auditor`) มิฉะนั้น mark เป็น `BLOCKED` พร้อม note "ม็อคไม่มี role switch"
- Start: OPEN หน้า "GL Posting Group" (login เป็น Auditor)
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปุ่ม create/edit/import/bulk-delete ไม่ปรากฏสำหรับ Auditor, เห็นปุ่ม export ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY card toolbar ทั้ง 2 tab | — | ปุ่ม **"เพิ่ม Posting Group"/"เพิ่ม Setup"** และ **"นำเข้า CSV"** **ไม่ปรากฏ**; ปุ่ม **"ส่งออก CSV"** ยังปรากฏ | ☐ |
| 2 | VERIFY คอลัมน์ "จัดการ" ทุกแถว | — | ไม่มีไอคอนดินสอ (แก้ไข) ปรากฏสำหรับ Auditor | ☐ |
| 3 | CLICK checkbox แถวใดๆ (ถ้ามี checkbox ให้เลือก) | — | ไม่มี bulk bar ปรากฏขึ้น หรือ checkbox ถูกซ่อนไปเลยสำหรับ Auditor | ☐ |

#### TC-P03 — Auditor: เปิด view drawer ได้แต่ไม่เห็นปุ่มแก้ไข/เปลี่ยนสถานะ — ⚠ ยืนยัน anchor
- group: P · ความสำคัญ: สูง · trace: 05_RULES §5.3
- actor (role): Auditor (Watcher)
- Setup: role=qa_auditor · seed=— · files=— · ⚠ เช่นเดียวกับ TC-P02 — ต้องใช้ environment ที่มี role switch จริง
- Start: OPEN หน้า "GL Posting Group" (login เป็น Auditor) → CLICK แถวใดแถวหนึ่ง
- ชุดข้อมูล: —
- ผ่านเมื่อ: view drawer เปิดได้ (read-only) แต่ header actions ไม่มีปุ่ม "แก้ไข"/"เปลี่ยนสถานะ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY header actions ของ view drawer | — | ปุ่ม **"แก้ไข"** และ **"เปลี่ยนสถานะ"** ไม่ปรากฏสำหรับ Auditor — เหลือแค่ปุ่มปิด (X) | ☐ |
| 2 | VERIFY เนื้อ drawer (ข้อมูลกลุ่ม/บัญชีที่ผูก) | — | แสดงข้อมูลได้ครบตามปรกติ (read-only ไม่ใช่ ซ่อนข้อมูล) | ☐ |

#### TC-P04 — Non-Finance role เรียก API ตรง ถูกปฏิเสธ (PM-03) — ข้าม
- group: P · ความสำคัญ: — · trace: 05_RULES §5.5 PM-03 `[AI-DEFAULT]`
- **ข้ามการสร้างเคสจริง** — PM-03 เป็นการยิง HTTP request ตรงข้าม role guard โดยไม่ผ่านหน้าจอเลย (bypass UI) ไม่มี element ใดบนหน้าจอให้ agent แบบ browser-use/vision กดเพื่อ trigger สถานการณ์นี้ได้ — เป็นความรับผิดชอบของ API-level test suite (curl/Postman/pytest) ไม่ใช่ของชุดทดสอบ UI นี้ ลงไว้ใน Coverage Ledger เพื่อไม่ให้ item หายไปเงียบๆ ตามที่ Iron Rule R5 กำหนด

---

### กลุ่ม XT — Cross-Module (06_TESTS §6.9)

> ทั้ง 4 เคสในกลุ่มนี้ **ต้อง simulate** เพราะ pack นี้ไม่มีหน้า Item Master หรือ document module (PO/PR/Invoice)
> ให้ agent คลิกผ่านจริง — เป็น API-level/contract-level test ที่ runner ต้องเรียกเครื่องมือแยกจาก browser click

#### TC-XT01 — Item Master `GET /gl/posting-groups?type=product` คืนชุดค่า 2 ค่า (as-built gap, ไม่ใช่ bug) — ต้อง simulate
- group: XT · ความสำคัญ: กลาง · trace: 06_TESTS §6.9 XT-01 · R09 · OQ-PG-04
- actor (role): System (service-to-service)
- Setup: role=service-token · seed=มี setup 3 แถวตาม default (prod_group ที่มี = GOODS, SERVICE) · files=— · **(ต้อง simulate)** เรียก `GET /api/v1/gl/posting-groups?type=product` ตรง (F-PG-API-19) — ไม่มีหน้า Item Master ให้คลิกผ่าน UI ใน pack นี้
- Start: (ไม่มี UI — เรียก API ตรง)
- ชุดข้อมูล: —
- ผ่านเมื่อ: response คืนค่า `[{value:"GOODS",...},{value:"SERVICE",...}]` เท่านั้น (2 ค่า ไม่ใช่ 6 ค่าของ Item Master) — assert ว่านี่คือ as-built gap ที่ **คาดหวัง** ไม่ใช่ความล้มเหลวของเทส

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) เรียก `GET /api/v1/gl/posting-groups?type=product` | — | HTTP 200, `data` มี 2 รายการ: `GOODS`, `SERVICE` — ไม่มี `FINISHED/RAWMAT/PACKAGING/TRADE/EXPENSE` (ยืนยัน gap ตาม OQ-PG-04 ที่ยังไม่ sync) | ☐ |

#### TC-XT02 — Item Master `GET /gl/vat-groups` คืน empty array + gap metadata — ต้อง simulate
- group: XT · ความสำคัญ: กลาง · trace: 06_TESTS §6.9 XT-02 · OQ-PG-01
- actor (role): System (service-to-service)
- Setup: role=service-token · seed=— · files=— · **(ต้อง simulate)** เรียก `GET /api/v1/gl/vat-groups` ตรง (F-PG-API-20)
- Start: (ไม่มี UI)
- ชุดข้อมูล: —
- ผ่านเมื่อ: response 200 (ไม่ใช่ error) พร้อม `data:[]` + gap metadata

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (simulate) เรียก `GET /api/v1/gl/vat-groups` | — | HTTP 200 (ไม่ error), `data: []`, มี meta field ระบุ gap เช่น `"gap": "OQ-PG-01 not yet resolved, no VAT Posting Setup entity exists"` — Item Master ต้อง degrade gracefully ไม่ hard-fail | ☐ |

#### TC-XT03 — แก้ `account_1` บนระเบียน `used>0` แล้ว post ใหม่ resolve บัญชีใหม่, ของเก่าไม่ย้อน — ต้อง simulate
- group: XT · ความสำคัญ: กลาง · trace: 06_TESTS §6.9 XT-03 · BRD §5.2.2
- actor (role): Finance Lead + System (GL Engine, mocked/stubbed)
- Setup: role=finance_lead · seed=ระเบียน LOCAL (used=82) มี journal line เก่าอ้างบัญชี `2-1-10-01` อยู่แล้ว (mock/stub) · files=— · **(ต้อง simulate)** ไม่มี document/PO/Invoice module ใน pack นี้ให้ agent คลิก "สร้างเอกสารใหม่" จริง — ต้อง stub GL Engine
- Start: OPEN หน้า "GL Posting Group" → CLICK ไอคอนดินสอที่แถว LOCAL (ส่วนที่ทำได้ผ่าน UI จริง)
- ชุดข้อมูล: —
- ผ่านเมื่อ: การแก้ไขบัญชีเองผ่าน UI ทำได้ปรกติ (พิสูจน์แล้วใน TC-E05); ส่วนผลกระทบต่อ journal line เก่า/ใหม่ ต้อง simulate ที่ระดับ GL Engine stub

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT บัญชี AP ใหม่ → **"บัญชีเจ้าหนี้ (AP control)"** แล้ว CLICK **"บันทึกการแก้ไข"** (ส่วนนี้ทำได้จริงผ่าน UI) | — | บันทึกสำเร็จ toast "บันทึกการแก้ไขกลุ่มแล้ว" (เหมือน TC-E05) | ☐ |
| 2 | (simulate) GL Engine stub: post เอกสารใหม่ที่อ้าง code=`LOCAL` | — | journal line ใหม่ resolve ไปที่บัญชี AP **ใหม่** ที่เพิ่งแก้ | ☐ |
| 3 | (simulate) VERIFY journal line เก่า (ที่ post ก่อนแก้ไข) | — | journal line เก่ายังอ้างบัญชี AP **เดิม** (`2-1-10-01`) ไม่ถูกแก้ย้อนหลัง | ☐ |

#### TC-XT04 — ตั้งสถานะ "ไม่ใช้งาน" แล้ว post เอกสารใหม่ resolve ไม่ได้ (by design, BR-06) — ต้อง simulate
- group: XT · ความสำคัญ: กลาง · trace: 06_TESTS §6.9 XT-04 · BR-06
- actor (role): Finance Lead + System (GL Engine, mocked/stubbed)
- Setup: role=finance_lead · seed=ใช้ระเบียนใดก็ได้ · files=— · **(ต้อง simulate)** GL Engine resolve step ไม่อยู่ใน pack นี้
- Start: OPEN หน้า "GL Posting Group" → CLICK แถวใดแถวหนึ่ง (ส่วนที่ทำได้ผ่าน UI จริง)
- ชุดข้อมูล: —
- ผ่านเมื่อ: ตั้งสถานะไม่ใช้งานทำได้ปรกติผ่าน UI (พิสูจน์แล้วใน TC-ST01/ST04); การ resolve fail ที่ GL Engine ต้อง simulate

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **"เปลี่ยนสถานะ"** → CLICK **"ไม่ใช้งาน"** (ทำได้จริงผ่าน UI) | — | สถานะเปลี่ยนทันที toast "เปลี่ยนสถานะเป็น ไม่ใช้งาน แล้ว" | ☐ |
| 2 | (simulate) GL Engine stub: post เอกสารใหม่อ้างระเบียนนี้ | — | resolve ล้มเหลว (by design, เพราะ entity picker/GL resolve มองเห็นเฉพาะ status="active") — GL Engine เองไม่ใช่ scope ของฟีเจอร์นี้ แต่ data state (สถานะ≠active) ที่ทำให้ resolve fail คือสิ่งที่ฟีเจอร์นี้ต้องรับผิดชอบ และพิสูจน์แล้วผ่าน step 1 | ☐ |

---

### กลุ่ม UX — Interaction (dirty-close/Esc/busy-state)

#### TC-UX01 — ปิด drawer สร้าง 3 วิธี (X icon / Esc / backdrop click) — ไม่มี dirty-check confirm ในฟีเจอร์นี้
- group: UX · ความสำคัญ: กลาง · trace: 01_UI §1.2 (Iron Rule Esc chain)
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK **"เพิ่ม Posting Group"**
- ชุดข้อมูล: A (กรอกบางส่วน)
- ผ่านเมื่อ: ปิดได้ทั้ง 3 ทาง โดยไม่มี modal ยืนยันการปิด (feature นี้ไม่มี dirty-check ตามที่สังเกตจาก `closeDrawer()` ใน HTML — ปิดแล้วละทิ้งค่าเสมอ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE ค่าบางส่วน → "รหัสกลุ่ม (Code)" แล้ว CLICK ไอคอน **X** ที่ header drawer | A | drawer ปิดทันที **ไม่มี** modal ยืนยัน "ยังไม่บันทึกจะปิดหรือไม่" ปรากฏ | ☐ |
| 2 | CLICK **"เพิ่ม Posting Group"** อีกครั้ง → TYPE ค่าบางส่วน → PRESS **Esc** | A | drawer ปิดทันทีเหมือนกัน ไม่มี modal ยืนยัน | ☐ |
| 3 | CLICK **"เพิ่ม Posting Group"** อีกครั้ง → TYPE ค่าบางส่วน → CLICK พื้นที่มืดด้านหลัง drawer (backdrop) | A | drawer ปิดทันทีเหมือนกัน | ☐ |

#### TC-UX02 — Esc ปิดเฉพาะ layer บนสุด (sdd dropdown ก่อน ไม่ปิด drawer ทีเดียว)
- group: UX · ความสำคัญ: กลาง · trace: 01_UI §1.7 Esc chain
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK **"เพิ่ม Posting Group"**
- ชุดข้อมูล: —
- ผ่านเมื่อ: Esc ครั้งแรกปิดแค่ dropdown ที่เปิดอยู่ ไม่ปิด drawer ทั้งใบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT "เจ้าหนี้ (Vendor)" → CLICK เปิด dropdown ช่อง **"บัญชีเจ้าหนี้ (AP control)"** | — | sdd-panel เปิดอยู่ | ☐ |
| 2 | PRESS **Esc** (ครั้งที่ 1) | — | เฉพาะ sdd-panel ปิด — **drawer ยังเปิดอยู่** | ☐ |
| 3 | PRESS **Esc** (ครั้งที่ 2) | — | drawer ปิดแล้ว (layer ถัดไปที่เป็น topmost) | ☐ |

#### TC-UX03 — Submitting state ตอนสร้าง Posting Group: spinner + "กำลังบันทึก…" + ปุ่ม disabled
- group: UX · ความสำคัญ: กลาง · trace: 01_UI §1.2 Iron Rule #44
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=—
- Start: OPEN หน้า "GL Posting Group" → CLICK **"เพิ่ม Posting Group"**
- ชุดข้อมูล: A
- ผ่านเมื่อ: ระหว่าง save เห็น spinner + ข้อความ + ปุ่ม disabled ชั่วครู่ก่อนกลับสู่สถานะปรกติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | กรอกฟอร์มครบตามชุด A แล้ว CLICK **"ยืนยันสร้าง"** | A | ทันทีหลังคลิก: ปุ่มเปลี่ยนข้อความเป็น **"กำลังบันทึก…"** พร้อมไอคอนหมุน (spin) และปุ่มอยู่ในสถานะ `disabled` (กดซ้ำไม่ได้) | ☐ |
| 2 | WAIT จน drawer ปิด | — | หลังจากนั้น drawer ปิดและ toast ปรากฏตามปรกติ (สถานะ busy สิ้นสุด) | ☐ |

#### TC-UX04 — Submitting state ตอน commit import: "กำลังนำเข้า…" + ปุ่ม disabled
- group: UX · ความสำคัญ: กลาง · trace: 01_UI §1.2 P-06
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=— · files=`pg_groups_valid.csv`
- Start: OPEN หน้า "GL Posting Group" → CLICK **"นำเข้า CSV"** → UPLOAD `pg_groups_valid.csv`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ระหว่าง commit เห็น spinner + "กำลังนำเข้า…" + ปุ่ม disabled

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **"นำเข้า 2 แถว"** | — | ทันทีหลังคลิก: ปุ่มเปลี่ยนเป็น **"กำลังนำเข้า…"** พร้อมไอคอนหมุน, ปุ่ม `disabled` | ☐ |
| 2 | WAIT จน step เปลี่ยนเป็น "done" | — | เข้าสู่หน้าสรุปผลตามปรกติ | ☐ |

#### TC-UX05 — Submitting state ตอน bulk delete: "กำลังลบ…" + ปุ่ม disabled
- group: UX · ความสำคัญ: กลาง · trace: 01_UI §1.2 P-07
- actor (role): Finance Lead
- Setup: role=finance_lead · seed=เลือกแถว used=0 อย่างน้อย 1 แถว · files=—
- Start: OPEN หน้า "GL Posting Group" (tab Posting Groups) → CLICK checkbox แถว **SCB** → CLICK **"ลบ"**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ระหว่างลบเห็น spinner + "กำลังลบ…" + ปุ่ม disabled

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **"ลบ 1 รายการ"** | — | ทันทีหลังคลิก: ปุ่มเปลี่ยนเป็น **"กำลังลบ…"** พร้อมไอคอนหมุน, ปุ่ม `disabled` | ☐ |
| 2 | WAIT จน modal ปิด | — | toast ผลลัพธ์ปรากฏตามปรกติ (สถานะ busy สิ้นสุด) | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `f-postgrp.html` ในเบราว์เซอร์ (หรือ environment จริงที่ deploy ฟีเจอร์นี้) — ไม่มี hash route ให้ deep-link
   ทุกเคสเริ่มจาก **"OPEN หน้า GL Posting Group"** แล้วไล่คลิกตาม `Start` ของเคสนั้นเพื่อไปถึง state ที่ต้องการ
2. ก่อนรันแต่ละเคส ตรวจ `Setup:` — ถ้าระบุ `files=` ให้เตรียมไฟล์ตามชื่อ+เนื้อหาใน `## Data Sets` ก่อน
3. เคสที่ระบุ `(ต้อง simulate)` — เป็นการทดสอบระดับ API/backend ที่ไม่มี element ให้คลิกบนหน้าจอ runner ต้องใช้
   เครื่องมือเรียก HTTP ตรง (ไม่ใช่ browser-use คลิกจอ) หรือ mark เป็น `BLOCKED` พร้อม note ถ้าไม่มีเครื่องมือนั้น
4. เคสกลุ่ม P ที่ระบุ `⚠ ยืนยัน anchor` — ถ้า environment ที่ทดสอบเป็นไฟล์ `f-postgrp.html` เดี่ยวๆ (hardcode
   Finance Lead) ไม่มีทางสลับ role ได้ ให้ mark `BLOCKED` พร้อม note "ม็อคไม่มี role switch UI" แทนการเดา
5. ทำตามลำดับ step ในตาราง ทีละ step, บันทึกผล ☐ → ✅ หรือ ❌ ตามที่เห็นจริง
6. เคสที่มี step "VERIFY+จด/บันทึกค่า" (R17) ต้องจดค่าไว้จริงและใช้เทียบใน step ที่อ้างถึงย้อนกลับ
7. เมื่อครบทุกเคสในกลุ่ม ให้สรุปผลลง JSON ตาม `## Result Report (schema)` ท้ายไฟล์

---

## Coverage Audit

| หมวด | covered / total |
|---|---|
| FR / User Stories (BRD §7, S-01..S-09) | 9 / 9 |
| Business Rules (05_RULES §5.1, BR-01..08 + R09 + Tax gap) | 12 / 12 |
| Edge Cases — BA-confirmed (EC-01..10) | 10 / 10 |
| Edge Cases — AI-pattern (DI/CA/ST/PM/FU, 12 items) | 4 / 12 (ดูรายการข้ามด้านล่าง — เหตุผลชัดเจนทุกตัว) |
| Error Codes (05_RULES §5.6, 13 codes) | 8 / 13 (5 ข้าม — backend/auth-layer only, ไม่มี UI signal) |
| Permission Matrix (Finance Lead / Auditor / System) | 4 / 5 cell-groups (1 ข้าม — PM-03 backend-only) |
| Acceptance Criteria (06_TESTS §6.1, AC-01..18) | 18 / 18 (รวม AC-03/AC-05 บางส่วนผ่าน `(ต้อง simulate)`) |

- **Cross-Module (XT):** 4 / 4 (ทั้งหมด `(ต้อง simulate)` — ไม่มี Item Master/document module ให้คลิกใน pack นี้)
- **Scope Lock (LOCK):** 5 / 5 (LOCK-01..05 ทุกข้อมี case verify)
- **Scope boundary (OQ-PG-01 / OQ-PG-04, out-of-scope Phase 2):** 2 / 2 ยืนยันการ "ไม่มี" ผ่าน TC-FN04/TC-FN05 — **ไม่มีการสร้างเคสทดสอบ VAT tab3 หรือ 6-value product axis ตามที่ห้ามไว้**
- **Manifest cross-check (FRD `00_OVERVIEW.md` §0.12):** ✅ **26/26** — ทุกแถวในตาราง Coverage Manifest (S-01..S-09, BR-01..08/R09/Tax-gap, EC E01-E10, DI/CA/ST/PM/FU, §12.1 Upstream/Downstream ×4, P-01..P-07, Security P4) มีคู่อยู่ใน Coverage Ledger ของไฟล์นี้แล้ว ไม่มีแถวไหนตกหาย

### ข้าม (พร้อมเหตุผล — Phase 2 / OOS / backend-only / นอกขอบเขตใบเซ็น)

- **OQ-PG-01 VAT Posting Setup (tab 3)** — **นอกขอบเขตใบเซ็น**, deferred Phase 2 lane pass, ยังไม่ build ใน HTML/FRD ปัจจุบันตามคำสั่งงาน — ห้ามสร้างเคสทดสอบ tab3 โดยตรง ยืนยัน "ไม่มี" ผ่าน TC-FN04 แทน
- **OQ-PG-04 product-axis 6-value (Item Master set)** — **นอกขอบเขตใบเซ็น**, deferred Phase 2 — ห้ามสร้างเคสสำหรับ 6-value axis ยืนยัน as-built 2-value (GOODS/SERVICE) ผ่าน TC-FN05/TC-S01 แทน
- **DI-01** (COA account deactivated while referenced) — Phase 2, ไม่มีผลสังเกตได้บน UI (ต้อง COA reverse-lookup job นอก scope)
- **DI-02** (COA account deleted while referenced) — mitigation อยู่ที่ F-COA-001 ไม่ใช่ feature นี้ ไม่มี UI signal
- **CA-01** (concurrent edit optimistic lock) — Phase 2.5 backend (`version`+`If-Match`), ไม่มีผลสังเกตบน client-array mock ปัจจุบัน
- **CA-07** (concurrent create race) — DB-level UNIQUE constraint เท่านั้น ไม่มี UI signal
- **PM-03** (non-Finance role direct API call) — backend/API-only, ไม่มี element บนหน้าจอให้ agent กด (ดู TC-P04)
- **PM-04** (multi-company/branch scoping) — left unconfirmed ตาม BRD, ไม่มี UI element เพิ่มจาก tenant-level RLS เดิม
- **FU-01** (CSV file size cap) — placeholder เลขยังไม่ยืนยัน, ไม่ enforce จริงใน mock ปัจจุบัน ไม่มี validation ให้สังเกต
- **`BR_ACCOUNT_NOT_LEAF_OR_INACTIVE`** — mock `COA_ACCOUNTS` ทั้ง 16 ตัวเป็น leaf+active หมด ไม่มีตัวอย่าง inactive/non-leaf ให้เลือกทดสอบผ่าน UI นี้ รอ ENG-PG-01 ต่อ COA จริง
- **`ERR_NOT_AUTHENTICATED`** — auth layer ทั่วระบบ ไม่ใช่ของ feature นี้โดยเฉพาะ
- **`ERR_NOT_FOUND`** — ไม่มี deep-link ID ให้พิมพ์ตรงในม็อค state-routing นี้
- **`ERR_DUPLICATE_IDEMPOTENCY_KEY`** — header-level, backend, ไม่มีผลสังเกตบน client-array mock
- **`ERR_STALE_DATA`** — ผูกกับ CA-01 ที่ข้ามแล้ว
- **loading/error state (async list)** — 01_UI §1.2 ระบุชัดว่า "ต้อง add ตอน implement จริง" ไม่มีใน mock ปัจจุบันให้สังเกต
- **audit log (S01-07)** — ไม่มี audit-log viewer UI ในฟีเจอร์นี้ให้ agent เปิดดู (เป็น backend artifact, ตรวจผ่าน DB/log แทน)

> ทุกรายการที่ข้ามมีเหตุผลระบุชัด ไม่มีรายการใดหายไปแบบเงียบ (Iron Rule R5/R11)

---

## Result Report (schema)

```json
{
  "feature_id": "F-PG",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-G01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 80, "pass": 0, "fail": 0, "blocked": 0 }
}
```

> `evidence` = สิ่งที่ agent **เห็นจริง** ตอน fail/blocked (เช่น ข้อความ toast จริงที่ต่างจาก Expected, ปุ่มที่หายไป,
> element ที่หาไม่พบ). `note` = หมายเหตุเสริม (เช่น "ต้อง simulate แต่ไม่มีเครื่องมือ API ในมือ รันแค่ UI-level step").
> สำหรับเคสที่มี sub-step แบบ `(ต้อง simulate)` บางส่วน (เช่น TC-G07, TC-S05, TC-XT01..04) ให้ระบุ status ของ
> ส่วน UI-level ที่ทำได้จริงแยกจากส่วน simulate ใน `note`.


# Coverage Report — F-BNK Bank Master (รอบ 1: HTML prototype)

- วันที่: 2026-08-05 · baseline: **PREBRIEF + DECISION_LOG (D3)** (pack นี้ไม่ผ่าน plan-module-workflow-mapper → ไม่มี `workflow_graph.json`/`NODE_BRIEF`; ใช้ FN-01..06+90 · BR-01..05 · edges §9 · Global Contracts #6/#7 เป็น contract แทน)
- Artifact ที่ตรวจ: `outputs/09_Bank-Master/01_HTML/BankMaster.html` (2877 บรรทัด · gate-passed โดย qc-ux)
- Feature: Finance · Shared-Foundation master · **NO tier**
- Checklist จาก contract: FN 7 · BR 5 · edges in 1 / out 4 · contracts 2 · exception paths 5 · scope guards 3
- ขอบเขตรอบนี้: **business-scope completeness ("ทำครบมั้ย")** — ไม่ตรวจ CI/iron-rules/UX (ทำโดย qc-ux แล้ว)

## Verdict: 🟡 WARN
สรุป: ครอบ **24/25** · block gap 0 · warn/observation 2 · scope creep **0 (อยู่ในขอบเขต)** · NOT-CHECKED 0
> ไม่มี block-severity item ที่ ✗ หรือ △ → **ไม่ BLOCK**. WARN มาจาก 2 จุดที่ควรยืนยัน/บันทึกก่อนทำ FRD (ดูหมวด Warnings) — ไม่กระทบ FN/BR หลัก.

---

## Coverage Matrix

### Functions (FN)
| Item | HTML | Evidence (route/selector/function · line) |
|---|---|---|
| **FN-01** create: bank #94 combobox + validate 10-15 หลัก + GL bind จาก CoA | ✓ | bank combobox `searchSelectHTML('acc-bank')` L2404 + `initSearchSelect('acc-bank', options: banks…)` L2367-2372 (Rule #94) · validate `/^[0-9]{10,15}$/` `validateAccForm()` L2492 · GL combobox `searchSelectHTML('acc-gl')` L2446 + options จาก `coa` L2374 |
| **FN-02** company switcher + default pay/receive unique/company | ✓ | switcher `<select onchange="changeCompany(...)">` L2176 + `changeCompany()` L2153 · uniqueness `enforceDefaultUnique()` L2534-2538 + `toggleDefault()` L2641-2650 (บังคับ 1/บริษัท) |
| **FN-03** duplicate accNo block (company-scoped) | ✓ | `validateAccForm()` L2493 `accounts.some(a=>a.company===…&&a.accNo===…&&a.id!==…)` → "เลขบัญชีนี้มีอยู่แล้วในบริษัทนี้" |
| **FN-04** inactive → หายจาก new-doc picker · เอกสารเดิมยังโชว์ | ✓ | `docPickerHTML()` L2734 `.filter(a=>a.status==='active')` (โชว์เฉพาะ active) · existing-doc note L2744-2745 `PV-2025-014` อ้าง inactive account ยังแสดง |
| **FN-05** mask last-4 + reveal-on-permission + audit | ✓ | `maskAccNo()` L2076 (`•`×n + slice(-4)) · `revealAccNo()` L2273-2280 เช็ก `currentUser.canRevealFull` + `pushAudit(id,'revealed',…)` |
| **FN-06** used-in-doc → ลบไม่ได้ → soft archive + audit | ✓ | `archiveModalHTML()` usedNote L2677 "ลบถาวรไม่ได้ — soft archive" · `confirmArchive()` L2694-2701 `status='archived'` + `pushAudit(…,'archived')` · ไม่มี hard-delete บน account |
| **FN-90** audit + validation ครบ | ✓ | `pushAudit()` L2084 + `pushBankAudit()` L2085 (append-only `unshift`) · validation `validateAccForm()` L2488 + `submitBank()` L2828-2837 |

### Business Rules (golden)
| Item | HTML | Evidence |
|---|---|---|
| **BR-01** accNo unique/company | ✓ | เดียวกับ FN-03 · `validateAccForm()` L2493 |
| **BR-02** default pay/receive max 1 each/company | ✓ | `enforceDefaultUnique()` L2534-2538 · `toggleDefault()` L2645 reset ตัวอื่นในบริษัทเดียวกัน · microcopy "ตั้งค่าได้เพียง 1 บัญชีต่อบริษัท" L2456/2584 |
| **BR-03** soft-reference (แก้ชื่อไม่ย้อนเอกสารเดิม) | ✓ | สะท้อนผ่าน concept: edit ทำ `Object.assign(rec,…)` บน master L2520 (ไม่แตะเอกสาร) · microcopy "เอกสาร…เดิม…ยังแสดง…ตามปกติ" `deactivateModalHTML` L2715 + `archiveModalHTML` L2678 · picker=snapshot mock (`PV-2025-014`) — เนื้อ posting rule เก็บรอบ 2 (FRD) |
| **BR-04** inactive หายจาก new-doc picker | ✓ | เดียวกับ FN-04 · `docPickerHTML()` L2734 |
| **BR-05** used account ลบไม่ได้ (soft archive only) | ✓ | เดียวกับ FN-06 · `archiveModalHTML()` L2677 usedNote + ไม่มีปุ่มลบถาวรบน account (row-actions มีแค่ แก้ไข/เก็บถาวร L2261-2262) |

### Edges
| Item | HTML | Evidence |
|---|---|---|
| **IN: CoA → Bank Master** (GL ผูกผ่าน #94 combobox จาก `coa`) | ✓ | `coa` L2034 · `initSearchSelect('acc-gl', options: coa.map…)` L2373-2378 · view drawer แสดง "บัญชี GL" L2573 |
| **OUT: → Payment Voucher** (account-as-pay-from picker) | ✓ (mock) | `openDocPicker()`/`docPickerHTML()` L2731-2759 = mock hook "จำลอง: เลือกบัญชีในเอกสาร" · ปุ่ม "จำลองเลือกในเอกสาร" `headerHTML()` L2118 · sidebar `data-feature="payment-voucher"` L1426 · existing note `PV-2025-014` L2745 |
| **OUT: → Bank Reconciliation** (account referenced) | ✓ | sidebar `data-feature="bank-recon"` "กระทบยอดธนาคาร" L1434-1437 · acknowledged เป็น downstream ใน archive note L2678 + deactivate note L2714-2715 ("รายการกระทบยอดธนาคาร") — A3 fix ยืนยันแล้ว |
| **OUT: → Receipt Voucher** (default-receive) | ✓ | sidebar `data-feature="receipt-voucher"` L1430 · default-receive toggle "ใช้เป็นค่าเริ่มต้นในใบสำคัญรับ" L2591 |
| **OUT: → Payroll** (บัญชีจ่ายเงินเดือน) | △ | acknowledged เชิงข้อมูลเท่านั้น: CoA GL `1010-06 "เงินฝากธนาคาร - บัญชีเงินเดือน"` L2040 (ผูกได้) + generic picker ครอบ concept · **แต่ไม่มี** sidebar item / note ที่ระบุ Payroll เป็น downstream ชัดเจนเหมือน PV/RV/Recon → ดู W2 |

### Global Contracts
| Item | HTML | Evidence |
|---|---|---|
| **#6 soft-reference** (master=picker only · snapshot เข้า docs · no FK cascade) | ✓ | picker-only `docPickerHTML()` L2732 · archive/deactivate ไม่ cascade เอกสาร (`confirmArchive` เปลี่ยนแค่ status L2696) · microcopy "เอกสารเดิม…อ้างอิงบัญชีนี้ได้ตามปกติ" L2678 |
| **#7 append-only audit + soft-archive + NO hard delete** | ✓ (ดู W1) | audit ฝั่งบัญชี `pushAudit` (unshift) แสดงใน view tab "ประวัติ" L2599-2605 · **audit ฝั่ง bank-preset `pushBankAudit` L2085 wired ที่ `submitBank`→'bank-added' L2843 + `removeBank`→'bank-removed' L2348** และ **surfaced** ที่ `bankAuditSectionHTML()` L2312-2324 render ใน `banksTabHTML()` L2308 → **A1 fix ยืนยันครบทั้ง 2 แท็บ** · account ไม่มี hard-delete (soft archive เท่านั้น) |

### Exception / Edge paths (ต้องมีทางเข้าใน UI)
| Path | HTML | Evidence |
|---|---|---|
| duplicate-block | ✓ | `validateAccForm()` L2493 |
| inactive ⇄ active (reactivate) | ✓ | `confirmDeactivate()` L2722 → `activateAccount()` L2653 · ปุ่ม "เปิดใช้งาน" สำหรับ inactive `toggleAct` L2560-2561 · filter status "ปิดใช้งาน" L2203 |
| archived = terminal (reactivate ไม่ได้) | ✓ | `accountViewHTML` toggleAct L2558-2562: archived → `''` (ไม่มีปุ่มเปิดใช้งาน) · A2 fix ยืนยัน · filter "เก็บถาวร" L2204 |
| reveal-without-permission (masked ค้าง) | ✓ | `revealAccNo()` L2275 `if(!currentUser.canRevealFull){ showToast('คุณไม่มีสิทธิ์…'); return; }` — path มีจริง (mock ตั้ง canRevealFull=true L1999 ตาม AI-DEFAULT OQ-1) |
| foreign-bank add + SWIFT 8/11 | ✓ | `submitBank()` L2833 `/^[A-Z0-9]{8}$|^[A-Z0-9]{11}$/` · drawer `bankFormHTML()` field SWIFT L2803-2810 + ปุ่ม "สร้างธนาคาร" L2120 |

### Scope Guards (ต้อง **ไม่** โผล่ใน UI)
| Guard | สถานะ | Evidence |
|---|---|---|
| Bank API / auto statement import (S-06) | ✓ ไม่โผล่ | grep `statement/api/import` → ไม่พบ business feature ใด ๆ (เจอแค่ font CDN + `canRevealFull`) — อยู่ในขอบเขต |
| Multi-currency (OQ-2) | ✓ correct | currency = readonly "THB — บาทไทย" L2436 + info-tip อธิบาย OQ-2 L2434 — **ถูกต้อง ไม่ใช่ creep** |
| Lite/Full tier / linkage dual-mode | ✓ correct | ไม่มี tier logic ใด ๆ (grep tier/Lite/Full → ไม่พบ) — absence ถูกต้องสำหรับ Shared-Foundation master |

**สรุป scope: อยู่ในขอบเขตทั้งหมด — ไม่พบ scope creep.**

---

## 🟡 Warnings / Observations (ไม่ block · ควรจัดการก่อน/ระหว่างทำ FRD)

### W1 · custom bank-preset รองรับ hard-delete — ตรวจสอบกับ Contract #7
- พบ: `removeBank()` L2345-2350 ทำ `banks.splice(idx,1)` = **ลบจริงออกจาก array** (เฉพาะ `b.custom===true` เท่านั้น · preset มาตรฐานลบไม่ได้ L2331) การลบถูก audit (`pushBankAudit` 'bank-removed' L2348 → append-only ยังคงอยู่)
- ประเด็น: Contract #7 = "soft-archive + **NO hard delete**". bank-preset ที่ผู้ใช้สร้างเองถูกลบถาวร (ต่างจาก account ที่ soft-archive)
- แก้/ตัดสินที่: บันทึกใน `04_FRD` (05_RULES + LOGIC ฝั่ง bank-preset) ว่า **bank-preset lookup entry ที่ยังไม่ถูกใช้ (used=0)** ได้รับการยกเว้นจาก #7 soft-archive หรือควรเปลี่ยนเป็น archive. ปัจจุบัน `removeBank` ไม่เช็ก `used` count (bankRow แสดง used L2327) → ถ้าจะคง hard-delete ควร guard "ลบได้เฉพาะ used=0". เป็น decision ระดับ contract → ยืนยันก่อน FRD
- **✅ RESOLVED (2026-08-05, user เลือก guard used=0):** `removeBank` เพิ่ม guard — ลบ custom bank ได้เฉพาะเมื่อ `used=0`, ไม่งั้น block + warning toast; ปุ่มลบ disable เมื่อ used>0. bank-preset lookup entry ยกเว้นจาก #7 ได้เฉพาะกรณี used=0 (ไม่มีบัญชีอ้าง → ลบไม่ทำ soft-ref พัง). FRD ต้องบันทึก rule นี้เป็น exception ที่ชัดเจนของ Contract #7.

### W2 · Payroll downstream acknowledged เชิงข้อมูลเท่านั้น (ไม่ชัดเท่า PV/RV/Recon)
- พบ: OUT edge → Payroll (PREBRIEF §9) surface เพียง CoA GL "บัญชีเงินเดือน" L2040 + generic picker · ไม่มี sidebar item / note ระบุ Payroll เป็นผู้บริโภคบัญชี ต่างจาก Payment/Receipt Voucher + Bank Reconciliation ที่ระบุชัด
- ทำไมไม่ block: generic doc-picker เป็น hook รวมของ account-as-picker (ครอบ pay-from ทุกเอกสาร) + payroll GL bind ได้จริง → OUT edge ไม่ได้ขาด hook
- แก้ที่: `04_FRD` (Edges/Integration section) ระบุ Payroll เป็น downstream consumer ให้ครบ 4 เส้น · (optional) HTML เพิ่ม note/รายการใน sidebar อ้าง payroll เพื่อความชัด

---

## ⬜ NOT-CHECKED
ไม่มี — ทุก item ตรวจได้จาก HTML + baseline docs พร้อม evidence.

## 💡 เสนอเข้า baseline (ไม่ใช่ gap — ไม่กระทบ verdict)
- pack นี้ไม่มี `workflow_graph.json`/`NODE_BRIEF`. ถ้าต้องการ severity-based coverage ที่เข้มขึ้นในอนาคต เสนอรัน plan-module-workflow-mapper (แต่ D3 สั่งห้ามรันในสายนี้ — คงใช้ PREBRIEF baseline)

---

## Diff จากรอบก่อน
รอบแรก (round 1) — ไม่มี report ก่อนหน้าให้ diff. Group A conformance fixes จาก DECISION_LOG ได้รับการยืนยันในรอบนี้:
- **A1** (audit ฝั่ง bank preset) → ✓ ปิดแล้ว: `pushBankAudit` wired + surfaced ทั้ง 2 แท็บ (L2085/2348/2843/2312)
- **A2** (archived = terminal) → ✓ ปิดแล้ว: toggleAct archived→'' (L2558-2562)
- **A3** (doc-usage รับรู้ Bank Reconciliation) → ✓ ปิดแล้ว: archive/deactivate notes อ้าง "รายการกระทบยอดธนาคาร" (L2678/2714)

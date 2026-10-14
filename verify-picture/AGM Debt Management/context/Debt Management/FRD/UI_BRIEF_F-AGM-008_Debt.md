# UI BRIEF — F-AGM-008 Debt Management (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Source HTML | `debt-management.html` (v1.0, 2026-07-21 — html-generator-v6, audit FAIL=0 · WARN=2 inherited: font-size + custom timeline) |
| FRD Pack | `FRD_F-AGM-008_Pack/` (7 ไฟล์ STANDARD) — paired ✅ |
| BRD | BRD_F-AGM-008 APPROVED (LOCK-01..11) |
| Reverse | RIF v2 + invariants.md LOCKED 🔒 (T3 code-only, AS-BUILT จาก React/Vite prototype) |
| Cross-module | read Quota (verified) + Contract (contract_id 🔒) · **feed outstanding** → CBM (F-AGM-007 debtor_outstanding) + Contract deduction |
| กติกา | ทุก claim ชี้ anchor ได้ (selector/function/ข้อความ verbatim) — HTML = source of truth |

## §1 Design Tokens AS-BUILT
เหมือน F-AGM-001..007 100% (CUBE Warm Light — Ivory #FAF8F5 · Charcoal #111 · Red #FF3B30 action · Orange #FF9A1F connection = snapshot/ลิงก์โควตา). Fonts Satoshi + Noto Sans Thai · Lucide 0.469.0 loader (`loadLucide`/`bootIfReady` fallback 5s). Thai optical centering (Rule #36). Z-index: Toast 80 · ss-list 70 · modal 60 · drawer 50 · sidebar/shell 20/19 · sticky th 3.

## §2 Route Map
| Route | หน้า | Handler |
|---|---|---|
| `#/debtors` (default) | P-01 Debtor List | `render()` (`getRoute()` บรรทัด 202 default 'debtors' · `navigate`) |
| `#/debtors/:debtor_id` | P-01 + Detail drawer (P-02, 5 tabs) | parse `parts[1]` → `findDebtor()` → `mountViewDrawer()` refresh-safe · `openView(id)=navigate('debtors/'+id)` · ไม่พบ → toast "ไม่พบข้อมูลลูกหนี้" + กลับ list |
Overlay ไม่ผูก route: create-debtor drawer (`openForm('debtor')`) · create-obligation drawer (`openForm('obligation',debtorId)`) · payment modal (`openPayment`) · write-off modal (`openWriteoff`) · obligation-view modal (`viewObligation`)

## §3 Layout Shell
Sidebar 232px: module เกษตรกรรม → สมาชิก/โควตา/แปลงที่ดิน/รอบปลูก/สัญญาส่งอ้อย/แบบสำรวจ/จองรอบส่งอ้อย (disabled), **จัดการหนี้ลูกหนี้ (is-active)** + system→Settings · Breadcrumb "เกษตรกรรม › จัดการหนี้ลูกหนี้" · User chip "สมพร วงศ์ทะเบียน / เจ้าหน้าที่บริหารหนี้ · WKN" · `.content` fluid

## §4 P-01 Debtor List (`render()` → `#page-content`)
```
.ph h1 "จัดการหนี้ลูกหนี้" + count + sub "ทะเบียนลูกหนี้ตามโควตา · ภาระหนี้ · ดอกเบี้ย/ค่าปรับ · การชำระ · ตัดหนี้สูญ"
    .ph-actions: [ส่งออก CSV] [รายงาน Aging] [สร้างลูกหนี้ primary ขวาสุด]
.stats 4: ลูกหนี้ทั้งหมด(sub ทุกสถานะในระบบ) · ยอดคงค้างรวม(฿ · รวมทุกลูกหนี้) · เกินกำหนด(Aging 90+) · ตัดหนี้สูญ(สถานะตัดหนี้สูญ)
.card
 ├ filter-bar: search (debounce — โควตา/ชื่อ/เลขลูกหนี้ · `onSearchInput`) + select สถานะ(ทุกสถานะ/ใช้งาน/ระงับ/ปิด/ตัดหนี้สูญ) + select Aging(ทุกช่วง/0-30/31-60/61-90/90+) + ล้างตัวกรอง
 ├ bulk-bar (selected): "เลือก N รายการ" (`toggleSelect/toggleSelectAll`)
 ├ table: ☑ · เลขลูกหนี้(mono แดง link) · โควตา(mono) · ชื่อเกษตรกร(+`labelsChips`) · ยอดคงค้าง(฿ ขวา · `bahtCell` ติดลบ=แดง) · ภาระ(# center) · Aging(`agingPill` 4 สี) · สถานะ(`statusPill`) · อัปเดตล่าสุด(`fmtDateTime`) · การกระทำ(ดู/เพิ่มภาระ/บันทึกชำระ)
 │  row .is-clickable → openView(debtor_id) · sortable: outstanding/updated_at (`sortBy`)
 └ footer: "แสดง X จาก Y รายการ" + pagination (`getPaged/goToPage`)
```
Empty: "ไม่พบลูกหนี้" +สร้างลูกหนี้ใหม่ · filter empty: "ไม่พบรายการที่ค้นหา" + ล้างตัวกรอง

## §5 Component Inventory (R4 states)
| Component | Anchor | States |
|---|---|---|
| Status pill | `statusPill()` | success ใช้งาน(active) · warning ระงับ(suspended) · neutral ปิด(closed) · danger ตัดหนี้สูญ(written_off) · info ย้อนรายการ(reversed) |
| **Aging pill ⭐** | `agingPill()` | success 0-30 · warning 31-60 · warn-orange 61-90 · danger 90+ · "—" (ปิด/ไม่มี) |
| **Source badge ⭐** | `sourceBadge()` | info+🔒 สัญญา(contract, น้ำเงิน locked) · neutral แมนนวล(manual) · warn ปรับปรุง(adjustment) |
| **Ledger kind badge ⭐** | `kindBadge()` | ตั้งหนี้/ดอกเบี้ย/ค่าปรับ/ชำระ/ปรับปรุง/ตัดหนี้สูญ/ย้อนรายการ (7 kinds) |
| Type badge | `typeLabel()` | ปุ๋ย/เครื่องจักร/พันธุ์อ้อย/ยาปราบ/เงินส่งเสริม/อื่นๆ(+desc) |
| **Allocation preview ⭐** | `computeAllocation()`/`validatePaymentAllocation()` | table ต่อ obligation: ดอกเบี้ย→ค่าปรับ→ต้นทุน + รวมจัดสรร + "เหลือ: X ฿" |
| Baht cell | `bahtCell()`/`fmtBaht()` | th-TH 2dp + ฿ · ติดลบ = สีแดง (credit/adjustment) |
| Quota search | `initSearchSelect`/`lookupDebtorQuota`/`searchQuota`/`clearDebtorQuota` | preview verified + auto-fill / existing debtor |
| Snapshot/labels | `labelsChips()` | teal chips |
| Toast | `showToast` | success/info/warning/error |

## §6 Overlay Registry
| Overlay | ขนาด | Mount | z |
|---|---|---|---|
| Detail drawer (P-02, 5 tabs) | 920px | `mountViewDrawer()`/`renderViewDrawer()` — header + quick stats 4 + tabs (`setViewTab`: overview/obligations/ledger/documents/settings via `ovOverviewTab`/`ovObligationsTab`/`ovLedgerTab`/`ovDocumentsTab`/`ovSettingsTab`) | 50 |
| Create-debtor drawer | 680px | `openForm('debtor')`/`renderDebtorForm()` — quota search + preview + name/phone | 50 |
| Create-obligation drawer | 920px | `openForm('obligation',debtorId)`/`renderObligationForm()` — 4 sections (source/detail/rate/repay) + note | 50 |
| Manual-payment modal | 720px | `openPayment()`/`renderPaymentModal()` — date/method/amount/reference/mode + validate + alloc preview | 60 |
| Write-off modal | 560px danger | `openWriteoff()`/`renderWriteoffModal()` — alert + info + amount + reason + confirm | 60 |
| Obligation-view modal | 560px | `viewObligation()`/`renderOblViewModal()` — read detail | 60 |

## §7 Interaction Spec
- **Debtor idempotent ⭐:** `lookupDebtorQuota` → ถ้าโควตามีลูกหนี้ (`debtorByQuota`) → toast "มีลูกหนี้อยู่แล้ว" + navigate detail · else preview + auto-fill (`submitDebtor` → "สร้างลูกหนี้สำเร็จ")
- **Payment allocation waterfall ⭐:** `computeAllocation(debtor,amount)` — sort obligations by priority↑ → ต่อ obligation: interest_accrued → penalty_accrued → principal · remaining ลดจนหมด · `validatePaymentAllocation` ("ตรวจสอบการจัดสรรเรียบร้อย") ก่อน `submitPayment` (gate "กรุณาตรวจสอบการจัดสรรก่อน" + reference "กรุณากรอกเลขอ้างอิง") → `pushLedger`(payment) + "บันทึกการชำระเรียบร้อย"
- **Write-off DOA ⭐:** `submitWriteoff` — amount ≤ outstanding (inline "จำนวนเกินยอดคงเหลือ") · confirm+reason บังคับ · **amount > 100000 → toast.warning "จำนวนเกินขีดจำกัด - ต้องการอนุมัติจากผู้จัดการ"** · success "ตัดหนี้เรียบร้อย" + `pushLedger`(write_off) + status→written_off
- **Contract lock 🔒:** `editObligation` บน source=contract → toast "รายการจากสัญญาแก้ไขไม่ได้"
- **Obligation source gating:** `validateObligation` — contract→contract_id · adjustment→adjustment_type+reference · other→desc · dates disb≤start_int≤maturity (verbatim §9)
- **Ledger double-entry:** `ovLedgerTab` — dr/cr + `lastBalance`/balance_after · dr/cr "-" เมื่อ 0 · append-only (`pushLedger`)
- Esc chain (`closeTopDrawer`) · debounce · Render preservation (`preserveState/restoreState`) · Row click=view · Double-submit guard (`busy`)

## §8 State-Driven UI Matrix
| Entity | State | Pill | ปุ่ม/พฤติกรรม |
|---|---|---|---|
| Debtor | active | ใช้งาน(เขียว) | สร้างภาระหนี้ · บันทึกการชำระ |
| Debtor | suspended/closed | ระงับ(เหลือง)/ปิด(เทา) | read-mostly (closed = outstanding 0) |
| Debtor | written_off | ตัดหนี้สูญ(แดง) | — |
| Obligation | active | ใช้งาน(เขียว) | ดู · แก้ไข(🔒 ถ้า contract) · ตัดหนี้ |
| Obligation | written_off | ตัดหนี้สูญ(แดง) | read-only |
| Obligation | reversed | ย้อนรายการ(info) | read-only (via adjustment) |
| Aging | 0-30/31-60/61-90/90+ | เขียว/เหลือง/ส้ม/แดง | — |

## §9 Microcopy (verbatim)
**ปุ่ม:** `สร้างลูกหนี้` · `ส่งออก CSV` · `รายงาน Aging` · `บันทึกการชำระ` · `สร้างภาระหนี้` · `ส่งออก Statement` · `ตัดหนี้` · `ดู` · `แก้ไข` · `เพิ่มภาระ` · `บันทึกชำระ` · `ตรวจสอบการจัดสรร` · `บันทึกการชำระ` · `ยืนยันตัดหนี้` · `ปิด` · `ยกเลิก`
**Tabs:** `ภาพรวม` · `ภาระหนี้` · `บัญชีสมุด` · `เอกสาร` · `การตั้งค่า`
**Payment modal:** title `บันทึกการชำระเงิน` · วิธี `เงินสด`/`โอนเงิน`/`หักกลบ` · mode `จัดสรรอัตโนมัติ (ดอก → ค่าปรับ → ต้น ตาม priority)`/`กำหนดเอง` · alloc types `ดอกเบี้ย`/`ค่าปรับ`/`ต้นทุน` · `รวมจัดสรร` · `เหลือ: X ฿`
**Write-off modal:** title `ตัดหนี้สูญ` · alert `การตัดหนี้สูญเป็นการกระทำที่ไม่สามารถย้อนกลับได้ง่าย…` · confirm `ยืนยันการตัดหนี้สูญจำนวน X ฿ สำหรับภาระ [id]`
**Toast:** `พบข้อมูลโควตา` · `มีลูกหนี้อยู่แล้ว` · `สร้างลูกหนี้สำเร็จ` · `บันทึกภาระหนี้สำเร็จ` · `ตรวจสอบการจัดสรรเรียบร้อย` · `บันทึกการชำระเรียบร้อย` · `ตัดหนี้เรียบร้อย` · `สร้างเอกสารเรียบร้อย` · `เริ่มส่งออกรายงานแล้ว` · `กำลังสร้างรายงานอายุหนี้...` · `รายการจากสัญญาแก้ไขไม่ได้`
**Validation (verbatim):** `กรุณากรอกรหัสโควตา` · `กรุณาค้นหาโควตาก่อน` · `กรุณากรอกชื่อเกษตรกร` · `จำนวนต้นทุนต้องมากกว่า 0` · `กรุณากรอกรายละเอียดประเภทอื่นๆ` · `กรุณาระบุรหัสสัญญาเมื่อแหล่งที่มาเป็น "จากสัญญา"` · `กรุณาเลือกชนิดการปรับปรุง` · `การปรับปรุงต้องอ้างอิงรายการเดิม (ภาระหนี้หรือรายการสมุดบัญชี)` · `วันที่เบิกต้องไม่เกินวันเริ่มคิดดอกเบี้ย` · `วันเริ่มคิดดอกเบี้ยต้องไม่เกินวันครบกำหนด` · `กรุณากรอกจำนวนเงินที่ถูกต้อง` · `กรุณาตรวจสอบการจัดสรรก่อน` · `กรุณากรอกเลขอ้างอิง` · `กรุณายืนยันการตัดหนี้` · `กรุณากรอกเหตุผลการตัดหนี้` · `จำนวนเกินยอดคงเหลือ` · `จำนวนเกินขีดจำกัด - ต้องการอนุมัติจากผู้จัดการ`
**Source/type/kind:** `สัญญา`(🔒)/`แมนนวล`/`ปรับปรุง` · `ปุ๋ย`/`เครื่องจักร`/`พันธุ์อ้อย`/`ยาปราบ`/`เงินส่งเสริม`/`อื่นๆ` · ledger `ตั้งหนี้`/`ดอกเบี้ย`/`ค่าปรับ`/`ชำระ`/`ปรับปรุง`/`ตัดหนี้สูญ`/`ย้อนรายการ`

## §10 Data Binding & BACKEND anchors
| Anchor | API |
|---|---|
| `QUOTAS` const + `findQuota/debtorByQuota` ⭐ | API-04 quota-search + read Quota (F-AGM-002) |
| `state.records` seed (debtors) | API-01 GET /debt/debtors |
| `submitDebtor()` | API-02 POST (FN-02, idempotent per quota) |
| `submitObligation()` | API-OB1 POST (FN-OB, source gating) |
| `validatePaymentAllocation()`/`computeAllocation` ⭐ | API-PAY1 validate (FN-ALLOC waterfall) |
| `submitPayment()` | API-PAY2 (FN-PAY + ledger) |
| `submitWriteoff()` ⭐ | API-WO1 (FN-WO DOA gate) |
| `pushLedger()` (double-entry) | FN-LED append-only |
| `exportStatement/exportCSV/agingReport` | API-LED2/05/06 |
| **feeds CBM/Contract** | debtor.outstanding → API-EXT (CBM debtor_outstanding + Contract) |
Mock: **5 debtors** DEB-2568-0001..0005 (aging 31-60/0-30/closed/90+/61-90 · outstanding รวม 611,000฿ · 1 overdue) · **8 obligations** OBL-2568-0001..0008 (3 contract🔒/4 manual/1 adjustment −5000 · 6/6 types) · **4 ledger** LED-2568-0001..0004 (charge/interest/charge/payment, running balance) · **6 quotas** (4 chain-shared + 2 ใหม่)

## §11 Traceability + Drift Log
| FRD | HTML anchor | Brief |
|---|---|---|
| 01_UI P-01 list | render → #page-content + agingPill/sourceBadge | §4/§5 |
| 01_UI P-02 detail 5-tab | renderViewDrawer + setViewTab + ov*Tab | §6 |
| 01_UI OV create-debtor | openForm('debtor') + lookupDebtorQuota | §6/§7 |
| 01_UI OV create-obligation | openForm('obligation') + validateObligation | §6/§7 |
| 01_UI OV payment | openPayment + computeAllocation | §6/§7 |
| 01_UI OV write-off | openWriteoff + submitWriteoff (DOA) | §6/§7 |
| 02_API PAY1/PAY2 | computeAllocation/submitPayment | §10 |
| 02_API WO1 (DOA) | submitWriteoff | §7/§10 |
| 03_LOGIC FN-ALLOC waterfall | computeAllocation | §7 |
| 03_LOGIC FN-LED double-entry | pushLedger/ovLedgerTab | §7 |
| 05_RULES contract-lock | editObligation (423) | §7 |
| 06_TESTS AC-01..36 / XT-01..05 | ครบ | §8/§10 |

### ⚠️ Drift Log
| # | รายการ | ทาง | หมายเหตุ |
|---|---|---|---|
| D-01 | Stats 4 การ์ด | HTML-only | ตรง BRD §18 |
| D-02 | Quota/Contract อ่านจาก mock | HTML sim | ระบบจริง = ENG-EXT-SRC read F-AGM-002/005 |
| D-03 | outstanding = snapshot field บน debtor (list/stats) vs actual seeded rows (detail tab) | design | ระบบจริง = reconcile กับ Σ ledger (BR-10) |
| D-04 | Payment "กำหนดเอง" (manual alloc) radio มีแต่ code จำลอง auto | HTML sim | OQ-02 — manual = (ต้อง simulate) SIT |
| D-05 | DOA gate proceed-with-warning (single-user) | HTML sim | ระบบจริง = PENDING_APPROVAL + manager (API-WO1 202) |
| D-06 | Print/Statement = toast/preview | HTML sim | ระบบจริง = ENG-DOC PDF/CSV ไทย |
| D-07 | Interest/penalty accrued = seed field | HTML sim | ระบบจริง = accrual job simple_daily_365 (OQ-03) |
| D-08 | T3 code-only reverse — labels ตาม code | reverse-note | invariants §7 C-01 |

## §12 Diff จากเวอร์ชันก่อน
เทียบ legacy (React/Vite shadcn prototype): คงไว้ 100% (LOCK-01) — 3-entity ledger (Debtor/Obligation/Ledger), payment allocation waterfall (ดอก→ค่าปรับ→ต้น ตาม priority), DOA 100k, contract-lock 🔒, adjustment refs origin (principal ติดลบ), double-entry ledger, 5-tab detail, aging buckets · เปลี่ยน: full-page + modal → CUBE drawer/modal · react-router `/2berp/debt` → hash `#/debtors` · CI shadcn → CUBE Warm Light · เพิ่ม stats + snapshot + audit governance

## §13 💡 ข้อเสนอ
1. ลิงก์โควตา deep-link ไป Quota/Contract detail จริง (ตอนนี้ mock)
2. Payment "กำหนดเอง" (manual allocation editor) ให้ทำงานจริง (OQ-02)
3. Interest/penalty accrual preview (simple_daily_365) แสดง breakdown รายวัน (OQ-03)
4. Ledger reconcile indicator (debtor.outstanding = Σ ledger balance) + drift warning (D-03)
5. Write-off approval workflow (DOA) แสดง pending state + ผู้อนุมัติ (D-05)

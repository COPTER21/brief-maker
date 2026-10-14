# UI BRIEF — F-AGM-013 Cane Payment (การทำจ่ายเงินอ้อย) (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Source HTML | `cane-payment.html` (v1.0, 2026-07-21 — html-generator-v6, audit FAIL=0 · WARN=2 inherited) |
| FRD Pack | `FRD_F-AGM-013_Pack/` (7 ไฟล์ STANDARD) — paired ✅ |
| BRD | BRD_F-AGM-013 APPROVED (LOCK-01..13) |
| Reverse | RIF v2 + invariants.md LOCKED 🔒 (T4+ base code + AS-BUILT enhanced code v4.1 + FRD/UI/API-DB/Testcase + enhancement v2/v3.1/v4.1) |
| Cross-module | อ่าน **Payment Setting (F-AGM-012)** active config · **Receiving (F-AGM-011)** net_tons + cane_type · **Quota** bank branch province · **CCS** legacy · หัก **Debt (F-AGM-008)** · ออกบิลงวด1/2 + บิลโปร + ใบเสร็จรวม |
| กติกา | ทุก claim ชี้ anchor ได้ (selector/function/ข้อความ verbatim) — HTML = source of truth |

## §1 Design Tokens AS-BUILT
เหมือน F-AGM-001..012 100% (CUBE Warm Light — Ivory #FAF8F5 · Charcoal #111 · Red #FF3B30 action · Orange #FF9A1F connection). Fonts Satoshi + Noto Sans Thai · Lucide 0.469.0 loader multi-CDN (fallback 5s). Z-index: Toast 80 · modal 60 · drawer 50 · sidebar/shell 20/19 · sticky th 3.

## §2 Route Map
| Route | หน้า | Handler |
|---|---|---|
| `#/payments` (default, tab=pending) | P-01 List "รอทำจ่าย" | `getRoute()` (บรรทัด 677 default 'payments') → `render()` · `gotoTab`/`topTabBar`/`tabRoute` |
| `#/payments/completed` | P-01 "เสร็จสิ้น" | seg → state.tab |
| `#/payments/:id` | P-01 + Detail drawer (P-03) | `openView` → `navigate('payments/'+id)` → `mountViewDrawer` refresh-safe · ไม่พบ → toast "ไม่พบรายการ" + กลับ |
Overlay ไม่ผูก route: All-in-One payment modal (`openPayment(id)`→`openModalBox('payment')`) · Sync CCS modal (`openModalBox('syncccs')`) · Sync All (`openModalBox('syncall')`).

## §3 Layout Shell
Sidebar 232px: module เกษตรกรรม → สมาชิก..การรับอ้อย (is-disabled), **การทำจ่ายเงินอ้อย (is-active, icon hand-coins)** + system→Settings · Breadcrumb "เกษตรกรรม › Cane Payment › การทำจ่ายเงินอ้อย" · User chip "สมพร วงศ์ทะเบียน / Finance Officer · WKN" · **top tab-bar** (`topTabBar`): รอทำจ่าย / เสร็จสิ้น (`gotoTab`). CURRENT_ROLE='Finance Officer', canWrite=true.

## §4 P-01 Payment List (`renderListPage()` → `#page-content`)
```
.ph tab title "การทำจ่ายเงินอ้อย" + count · sub "จัดการการทำจ่ายเงินอ้อยตามสถานะและงวด (WKN)"
   .ph-actions: [Export CSV outline → exportCSV] [Sync All primary → openModalBox('syncall')]
.stats 4: รอดึงค่าความหวาน(waiting_ccs) · รอทำจ่าย(pending+inst2+promotion) · เสร็จสิ้น(completed) · ยอดจ่ายรวมวันนี้(Σ completed ฿)
.card
 ├ filter-bar: search (onSearchInput · "ค้นหา (เลขที่ชั่ง/ชื่อเกษตรกร)") + select ประเภทอ้อย(ทุกประเภท/อ้อยสด/อ้อยตอ/อ้อยไฟไหม้) + select สถานะ + ล้าง(resetFilters)
 ├ table (getPaged): ชาวไร่/เลขที่ชั่ง · ประเภทอ้อย(caneTypePill) · งวด 1(billBadge) · งวด 2(billBadge/-) · โปรโมชั่น(promoCell) · CCS(ccsCell/"รอผล") · จำนวนตัน · ยอดสุทธิรวม · สถานะ(statusPill) · การดำเนินการ
 │  Actions: waiting_ccs → [Sync CCS → openModalBox('syncccs')] · non-completed → [ทำจ่าย → openPayment(id)] · always [ดูรายละเอียด → openView(id)]
 │  row → openView(id) · pagination (getPaged/goToPage)
 └ footer: pagination
```
Empty: emptyStateHTML "ไม่มีรายการ" · filter empty "ไม่พบรายการที่ค้นหา".
Mock (5 rows): CPAY-2025-00004 (waiting_ccs, FRESH, GREEN) · 00005 (waiting_ccs, BURN, WHITE/WHITE, +promo) · 00001 (pending, FRESH, GREEN/WHITE, promo 315, CCS 11.2, ฿10,315) · 00002 (pending_inst2, RATOON, GREEN/GREEN, ฿15,000) · 00003 (completed, FRESH, WHITE/WHITE, promo 600, ฿20,600).

## §5 Component Inventory (R4 states)
| Component | Anchor | States |
|---|---|---|
| Bill badge | `billBadge()` | GREEN pill-success "บิลเขียว (จ่ายตามงวด)" · WHITE pill-muted "บิลขาว (เงินยืมระหว่างงวด)" · null "-" |
| Cane-type pill | `caneTypePill()` | อ้อยสด(FRESH) · อ้อยตอ(RATOON) · อ้อยไฟไหม้(BURN) |
| Promo cell | `promoCell()` | จ่ายแล้ว(success) · รอจ่ายโปร(warning) · ไม่มีโปร(muted) |
| CCS cell | `ccsCell()` | value · "รอผล"(waiting_ccs) |
| Status pill | `statusPill()` | รอดึงค่าความหวาน · รอทำจ่าย · เสร็จสิ้น |
| **Step calc card ⭐** | `calcCardHtml()` | 7 ขั้น (มูลค่าอ้อย→ปรับประเภทอ้อย→แบ่งงวด→ภาษี→รายการหัก→หักหนี้→ดอกเบี้ย→ค่าธนาคาร→สุทธิ) live via `payCalc()` |
| Payment method radio | `methodOption()` | TRANSFER(โอนธนาคาร) · CASH(เงินสด) · CHEQUE(เช็ค + เลขที่เช็ค*) |
| Manual charge editor | `addManualCharge`/`removeManualCharge` | desc + amount + type FLAT/PER_TON |
| Currency | `fmtBaht()` | th-TH 2-dec + ฿ |
| Toast | `showToast` (+desc) | success/info/warning/error |

## §6 Overlay Registry
| Overlay | ขนาด | Mount | z |
|---|---|---|---|
| **All-in-One Payment modal (P-02) ⭐** | 900px | `openPayment(id)`→`openModalBox('payment')`/`renderPaymentModal()` — 3 tabs (งวดที่ 1/งวดที่ 2/โปรโมชั่น via `setPayTab`) + step calc + method + confirm + สรุปยอดรวม + ยืนยันทำจ่ายทั้งหมด | 60 |
| Detail drawer (P-03) | 720px | `openView`/`mountViewDrawer`/`renderViewDrawer()` — 5 tabs (สรุป/งวด 1/งวด 2/โปรโมชัน/Timeline via `setViewTab`) + print + final receipt | 50 |
| Sync CCS modal | 480px | `openModalBox('syncccs')`/`renderSyncCcsModal()`/`syncCcsConfirm()` — confirm + scale ticket + unload date | 60 |
| Sync All modal | 640px | `openModalBox('syncall')`/`renderSyncAllModal()`/`syncAllStart()` — confirm count + progress + summary (ทั้งหมด/สำเร็จ/ล้มเหลว) | 60 |

## §7 Interaction Spec
- **All-in-One payment ⭐:** `openPayment(id)` sets `state.pay` (inst1/inst2/promo sub-state) → modal. Tabs disabled ตาม hasInst2/hasPromo; auto-tab = งวดถัดไปที่ยังไม่จ่าย (บรรทัด 1126). `installmentTab(kind)` = step calc + method + bank account(TRANSFER) + notes + [ยืนยันการจ่าย{งวด}].
- **Step calc (payCalc) ⭐:** price_per_ton × net_tons = cane_total; **+ปรับประเภทอ้อย** (net_tons × adj, v4.1) = cane_total_adjusted; × inst% = base; − VAT(7%)/หัก ณ ที่จ่าย(3%)/กองทุน = after_tax; − charges(config CFG-01/02 + manual FLAT/PER_TON) = before_debt; − หักหนี้(min(desired 90%, outstanding)) = after_debt; − **ดอกเบี้ย(บิลขาว: days_early×daily_rate)** = after_interest; − **ค่าธนาคาร(TRANSFER: จังหวัดสาขา in/out/unknown)** = final = max(0, …). โปรโมชัน: ไม่ปรับประเภทอ้อย + ไม่หักหนี้.
- **Cane type adj (v4.1):** FRESH +10 · RATOON +5 · BURN −20 บาท/ตัน; แสดง "ปรับตามประเภทอ้อย (v4.1)".
- **Bank fee (v4.1):** จังหวัดสาขา==จังหวัดโรงงาน(เชียงใหม่) → in-fee(10) IN_PROVINCE · ต่าง(เชียงราย โปร) → out-fee(20) OUT_PROVINCE · ไม่มี → out + warning UNKNOWN.
- **Interest (บิลขาว):** WHITE → days_early 30 · daily_rate 0.0001918 · ดอกเบี้ย 120; GREEN/days_early=0 → "ไม่คิดดอกเบี้ย".
- **Method gating:** CHEQUE → เลขที่เช็ค required ("กรุณากรอกเลขที่เช็ค"); CASH/CHEQUE → bank fee 0, proof optional (ไม่มีสถานะ waiting_proof — v4.1).
- **Confirm + auto-switch ⭐:** `confirmInstallment(kind)` → green alert "ยืนยันการจ่าย{งวด}แล้ว" + toast "✓ ยืนยันการจ่าย{งวด}สำเร็จ" + auto งวด1→งวด2→โปร. `finalizeAll()` → status=completed + navigate completed + toast "✓ ทำจ่ายทั้งหมดสำเร็จ".
- **Sync CCS:** `syncCcsConfirm` → toast "ดึงค่า CCS สำเร็จ (CCS: 11.2)" + row ccs + status pending.
- **Detail:** `renderViewDrawer` — สรุป(ข้อมูล+bill+สรุปยอด+bank+[ออกใบเสร็จการจ่ายเงินอ้อยรวม] enabled completed) · งวด 1/2(breakdown+[พิมพ์บิลงวด]) · โปรโมชัน([พิมพ์บิลโปรโมชัน]) · Timeline. `printReceipt` sim. Esc chain · Render preservation.

## §8 State-Driven UI Matrix
| Status | List action | Payment tabs | Final receipt |
|---|---|---|---|
| waiting_ccs (รอดึงค่าความหวาน) | Sync CCS + ดูรายละเอียด | — (CCS ก่อน) | disabled |
| pending (รอทำจ่าย) | ทำจ่าย + ดูรายละเอียด | งวด1 active · งวด2/โปร disabled จนจ่าย | disabled |
| pending_inst2 | ทำจ่าย + ดูรายละเอียด | งวด1 ✓ · งวด2 active | disabled |
| pending_promotion | ทำจ่าย + ดูรายละเอียด | งวด1/2 ✓ · โปร active | disabled |
| completed (เสร็จสิ้น) | ดูรายละเอียด | อ่าน read-only | **enabled** |

## §9 Microcopy (verbatim)
**Tabs/List:** `รอทำจ่าย` · `เสร็จสิ้น` · `การทำจ่ายเงินอ้อย` · `จัดการการทำจ่ายเงินอ้อยตามสถานะและงวด (WKN)` · `Export CSV` · `Sync All` · `รอดึงค่าความหวาน` · `ยอดจ่ายรวมวันนี้`
**Table cols:** `ชาวไร่ / เลขที่ชั่ง` · `ประเภทอ้อย` · `งวด 1` · `งวด 2` · `โปรโมชั่น` · `CCS` · `จำนวนตัน` · `ยอดสุทธิรวม` · `สถานะ` · `การดำเนินการ` · `รอผล` · `ไม่มีโปร` · `รอจ่ายโปร` · `จ่ายแล้ว`
**Bill:** `บิลเขียว (จ่ายตามงวด)` · `บิลขาว (เงินยืมระหว่างงวด)`
**Cane type:** `อ้อยสด` · `อ้อยตอ` · `อ้อยไฟไหม้`
**Payment modal:** `ทำจ่ายเงินอ้อย — {farmer} ({id})` · `งวดที่ 1` · `งวดที่ 2` · `โปรโมชั่น` · `ขั้นตอนการคำนวณ` · `ขั้นตอน 2.1 มูลค่าอ้อย` · `ราคาต่อตัน` · `น้ำหนัก (ตัน)` · `มูลค่าอ้อยรวม` · `ขั้นตอน 2.1.5 ปรับตามประเภทอ้อย (v4.1)` · `ยอดปรับรวม` · `มูลค่าหลังปรับ` · `ขั้นตอน 2.2 แบ่งงวด` · `สัดส่วนงวดนี้` · `ยอดตั้งต้นงวด (base)` · `ขั้นตอน 2.3 ภาษี` · `VAT (7%)` · `หัก ณ ที่จ่าย (3%)` · `กองทุนส่งเสริม` · `รวมภาษี` · `ยอดหลังภาษี` · `ขั้นตอน 2.4 รายการหักเพิ่มเติม` · `รวมรายการหัก` · `ยอดก่อนหักหนี้` · `ขั้นตอน 2.5 หักหนี้` · `ยอดหนี้คงเหลือ` · `เป้าหมาย (90%)` · `หักจริง` · `คงเหลือ` · `ยอดหลังหักหนี้` · `ขั้นตอน 2.6 ดอกเบี้ย` · `จำนวนวันล่วงหน้า` · `อัตราต่อวัน` · `ดอกเบี้ย` · `ไม่คิดดอกเบี้ย` · `ขั้นตอน 2.7 ค่าธนาคาร` · `จังหวัดโรงงาน` · `จังหวัดสาขาธนาคาร` · `ยอดสุทธิ`
**Method:** `วิธีจ่าย` · `โอนธนาคาร` · `เงินสด` · `เช็ค` · `เลขที่เช็ค` · `ระบบจะหักค่าธนาคาร` · `ไม่มีค่าธนาคาร — แนบหลักฐานได้ (optional)` · `กรอกเลขที่เช็ค (บังคับ) แนบรูปเช็คได้ (optional)` · `บัญชีธนาคาร` · `หมายเหตุ (ถ้ามี)`
**Confirm/finalize:** `ยืนยันการจ่ายงวดที่ 1` · `ยืนยันการจ่ายงวดที่ 2` · `ยืนยันการจ่ายโปรโมชั่น` · `ยืนยันทำจ่ายทั้งหมด` · `สรุปยอดรวมทั้งหมด`
**Drawer:** `สรุป` · `งวด 1` · `งวด 2` · `โปรโมชัน` · `Timeline` · `ข้อมูลพื้นฐาน` · `ประเภทบิล` · `สรุปยอดตามงวด` · `ยอดสุทธิรวม` · `ออกใบเสร็จการจ่ายเงินอ้อยรวม` · `พิมพ์บิลงวด 1` · `พิมพ์บิลงวด 2` · `พิมพ์บิลโปรโมชัน`
**Sync:** `ดึงค่า CCS (ยืนยัน)` · `ดึงค่า CCS สำเร็จ (CCS: 11.2)` · `ยืนยันและเริ่ม` · `ดึงค่า CCS ทั้งหมดเสร็จสิ้น` · `ทั้งหมด` · `สำเร็จ` · `ล้มเหลว`
**Warning:** `⚠️ ไม่มีข้อมูลจังหวัดสาขาธนาคาร - ใช้อัตราต่างจังหวัดเป็น default`
**Toast:** `✓ ยืนยันการจ่ายงวดที่ 1สำเร็จ` · `✓ ทำจ่ายทั้งหมดสำเร็จ` · `ดึงค่า CCS สำเร็จ` · `กำลังส่งออกข้อมูล...`

## §10 Data Binding & BACKEND anchors
| Anchor | API / FN |
|---|---|
| `state.payments` seed | API GET /agm/cane/payments (list) |
| `openView`/`renderViewDrawer` | API GET /:id (detail) |
| `syncCcsConfirm` | API POST /:id/sync-ccs (FN-CCS-SYNC) |
| `syncAllStart` | API POST /sync-all-ccs (FN-CCS-SYNCALL, X-Idempotency-Key) |
| `payCalc`/`calcCardHtml` ⭐ | POST /:id/preview (FN-PRICE/CANETYPE/VAT/CHARGE/DEBT/INTEREST/BANKFEE — ENG-CALC) |
| `confirmInstallment`/`finalizeAll` ⭐ | POST /:id/installments/{n}/pay หรือ /confirm (If-Match + Idempotency; FN-PAY + status transition + Debt deduct) |
| `printReceipt` | POST /:id/print-bill (INST1/INST2/PROMOTION) · POST /:id/final-receipt (completed) |
| `exportCSV` | GET /export?tab= |
| **read active config** | API-EXT ← Payment Setting F-AGM-012 |
Mock: 5 rows · calc uses AS-BUILT constants (price 1000, adj +10/ton FRESH, VAT 735, WHT 315, fund 50, config charges CFG-01 200 + CFG-02 100, debt 90% 4000, interest 120 white, bank fee 10 in/20 out).

## §11 Traceability + Drift Log
| FRD | HTML anchor | Brief |
|---|---|---|
| 01_UI P-01 list 2-tab + คอลัมน์ | renderListPage + topTabBar | §4 |
| 01_UI P-02 all-in-one modal 3 tabs | openPayment + renderPaymentModal | §6/§7 |
| 01_UI P-02 step calc | calcCardHtml + payCalc | §7 |
| 01_UI P-03 detail 5 tabs | renderViewDrawer + setViewTab | §6 |
| 01_UI OV sync ccs/all | renderSyncCcsModal/renderSyncAllModal | §6 |
| 02_API pay/preview/confirm | confirmInstallment/payCalc | §7/§10 |
| 03_LOGIC FN-PIPELINE/INTEREST/BANKFEE/CANETYPE | payCalc | §7 |
| 04_DB installment/promotion/cane_type | state.payments | §10 |
| 05_RULES VR-01 WHITE/GREEN, VR-05 cheque | (bill combo enforced upstream; cheque confirmInstallment) | §7 |
| 06_TESTS AC/XT | ครบ | §8/§10 |

### ⚠️ Drift Log
| # | รายการ | ทาง | หมายเหตุ |
|---|---|---|---|
| D-01 | **5-status model (ไม่มี waiting_cash_proof)** | AS-BUILT (v4.1) | proof optional · invariants §7 C-01 |
| D-02 | **Promotion = บิลแยก + ไม่หักหนี้** | AS-BUILT (v3.1/v4.0) | invariants §7 C-07/08 |
| D-03 | ปรับประเภทอ้อยก่อนแบ่งงวด (v4.1) | AS-BUILT | BR-03 |
| D-04 | ค่าธนาคารตามจังหวัดสาขา (in/out/unknown) | AS-BUILT (v4.1) | BR-10 |
| D-05 | calc = client sim (mock constants) | HTML sim | ระบบจริง = ENG-CALC (BE, shared กับ Setting) |
| D-06 | interest daily_rate = raw (ไม่ roundUp 7) | AS-BUILT code | Setting แสดง roundUp — flag OQ-01 |
| D-07 | Debt/CCS/print = toast/sim | HTML sim | ระบบจริง = ENG-DEBT + CCS legacy + PDF render |
| D-08 | summary block ใช้ base−bankFee (simple) vs card ใช้ full pipeline | AS-BUILT mock | preserved จาก enhanced code |

## §12 Diff จากเวอร์ชันก่อน (base → Enhancement v4.1 AS-BUILT)
เทียบ base (zip1, 70 files): List + Sync CCS + PaymentDialogV3 (โอน/เงินสด) + cash-proof + **waiting_cash_proof status** · จ่ายรายการเดียว (net_amount). → **Enhancement v4.1 (zip3, 115 files):** จ่าย **2 งวด (50/50)** + **บิลเขียว/ขาว** (ดอกเบี้ยล่วงหน้า) + **3 วิธีจ่าย** + **บิลโปรโมชันแยก** + **ปรับประเภทอ้อย** + **ค่าธนาคารจังหวัดสาขา** + **All-in-One modal (step calc)** + auto-switch · **ตัด waiting_cash_proof** (proof optional). เปลี่ยน: CI shadcn → CUBE Warm Light + drawer/modal + route.

## §13 💡 ข้อเสนอ
1. calc engine ควรอยู่ฝั่ง BE (ENG-CALC) shared กับ Payment Setting เพื่อ single source (OQ-01 interest rounding)
2. ยืนยัน VAT order (per-installment vs VAT-then-split) — AS-BUILT = per-installment (OQ-02)
3. White Schedule / green schedule ดึงจริงจาก F-AGM-012 (API-EXT) แทน mock (OQ-03)
4. Debt integration contract + 424 retry (OQ-04)
5. ยืนยัน proof optional จริงหรือบังคับตอนพิมพ์ใบเสร็จ (OQ-05)
6. All-in-One vs step-by-step flow — รองรับทั้งสองใน BE (/confirm confirm_all)

# UI BRIEF — F-AGM-010 Cane Check-In (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Source HTML | `cane-checkin-management.html` (v1.0, 2026-07-21 — html-generator-v6, audit FAIL=0 · WARN=2 inherited font-size) |
| FRD Pack | `FRD_F-AGM-010_Pack/` (7 ไฟล์ STANDARD) — paired ✅ |
| BRD | BRD_F-AGM-010 APPROVED (LOCK-01..11) |
| Reverse | RIF v2 + invariants.md LOCKED 🔒 (T3 code-only, AS-BUILT จาก React/Vite shadcn + Booking API integration) |
| Cross-module | **feed Cane Booking (F-AGM-007)** — event CHECK_IN → booking "รอผลการเท" (idempotent) · read CBM dispatching (pending) · read Quota/Member · weighToken จากเครื่องชั่ง |
| กติกา | ทุก claim ชี้ anchor ได้ (selector/function/ข้อความ verbatim) — HTML = source of truth |

## §1 Design Tokens AS-BUILT
เหมือน F-AGM-001..009 100% (CUBE Warm Light — Ivory #FAF8F5 · Charcoal #111 · Red #FF3B30 action · Orange #FF9A1F connection). Fonts Satoshi + Noto Sans Thai · Lucide 0.469.0 loader (`loadLucide`/`bootIfReady` fallback 5s). Z-index: Toast 80 · ss-list 70 · modal 60 · drawer 50 · sidebar/shell 20/19 · sticky th 3.

## §2 Route Map
| Route | หน้า | Handler |
|---|---|---|
| `#/checkins` (default, tab=pending) | P-01 List "ต้องส่ง" | `render()` (`getRoute()` บรรทัด 161 default 'checkins' · `gotoTab`/`topTabBar`) |
| `#/checkins/checked-in` | P-01 "เช็คอินแล้ว" | seg 'checked-in' → state.tab |
| `#/checkins/:id` | P-01 + Detail drawer (P-02) | `findItem()` → `mountViewDrawer()` refresh-safe · `openView(id)` · ไม่พบ → toast "ไม่พบรายการเช็คอิน" + กลับ tab |
Overlay ไม่ผูก route: method-chooser · CBM/Member/Central check-in · QR scan · void (ทุกตัว `openModalBox`)

## §3 Layout Shell
Sidebar 232px: module เกษตรกรรม → สมาชิก..พื้นที่ (disabled), **เช็คอินรับอ้อย (is-active)** + system→Settings · Breadcrumb "เกษตรกรรม › หน้างานโรงงาน › เช็คอินรับอ้อย" · User chip "สมพร วงศ์ทะเบียน / เจ้าหน้าที่ชั่ง · WKN" · **top tab-bar** (`topTabBar`): ต้องส่ง + เช็คอินแล้ว (route-derived `gotoTab`)

## §4 P-01 Check-In List (`renderListPage()` → `#page-content`)
```
.ph tab title (ต้องส่ง/เช็คอินแล้ว) + count "N รายการ"
   .ph-actions: [Scan QR] [Export CSV] [เช็คอิน primary]
.stats 4: รอเช็คอิน(pending count) · เช็คอินวันนี้(checked-in count) · ซิงก์ล้มเหลว(syncPending count) · เสร็จสิ้น(status เสร็จสิ้น)
.card
 ├ filter-bar: search (debounce · `onSearchInput` — placeholder "ค้นหา CBM/NBM/ทะเบียน/เหรียญ/โควต้า/คนขับ") + select สถานะ(ทุกสถานะ/จัดส่ง/รอทำจ่าย/เสร็จสิ้น) + select แผนก(ทุกแผนก/โควต้าจองคิว/ไม่ได้จองคิว/กลาง) + ล้าง
 ├ table columns (`renderListPage`): รหัสเอกสาร(mono แดง link → openView) · วันที่/เวลาเข้า(or "-") · โควต้า(`quotaCell` + badge กลาง) · เกษตรกร/ผู้ส่ง(+phone) · ทะเบียนรถ · ประเภทรถ · ชื่อคนขับ · เลขเหรียญชั่ง(or "-") · ประเภทการเข้าโรงงาน(`entryTypeBadge`) · สถานะ(`statusPill`) · [สถานะ Booking — checked-in tab only, `bookingCell`] · Actions
 │  pending: ปุ่ม "เช็คอิน" (→ CBM modal prefilled) · checked-in: รายละเอียด + ยกเลิก(void)
 └ footer: pagination (`getPaged/goToPage`)
```
Empty: "ยังไม่มีรายการเช็คอิน" · filter empty: "ไม่พบรายการที่ค้นหา" + ล้าง

## §5 Component Inventory (R4 states)
| Component | Anchor | States |
|---|---|---|
| Entry-type badge | `entryTypeBadge()` | info โควต้าจองคิว · neutral โควต้าไม่ได้จองคิว · warn โควต้ากลาง |
| Status pill | `statusPill()` | neutral จัดส่ง · warning รอทำจ่าย · success เสร็จสิ้น |
| **Booking-sync cell ⭐** | `bookingCell()` | CBM+syncPending → danger "ซิงก์ล้มเหลว" + retry (refresh-cw) · CBM ok → neutral bookingStatus(รอผลการเท) · non-CBM → "-" |
| **Retry ⭐** | `retrySync(id)` | spinner → success "ซิงก์สถานะ Booking สำเร็จ" (syncPending=false + bookingStatus=รอผลการเท) / fail "ซิงก์ล้มเหลว กรุณาลองใหม่" |
| Quota cell | `quotaCell()` | Q##### · โควต้ากลาง badge |
| Payment-bill radio | `billRadios()` | งวดที่ 1/2 · บิลเขียว/บิลขาว |
| CBM lookup | `cbmLookup/findPendingCbm` | not found "ไม่พบรหัส CBM นี้" · found → info card |
| Member lookup | `mbLookup` | not found "ไม่พบโควต้านี้" · found "พบข้อมูลสมาชิก" |
| Toast | `showToast` | success/info/warning/error |

## §6 Overlay Registry
| Overlay | ขนาด | Mount | z |
|---|---|---|---|
| Detail drawer (P-02) | 680px | `mountViewDrawer()`/`renderViewDrawer()` — เวลาเข้า/โควต้า/เกษตรกร/ทะเบียน/รถ/คนขับ/เหรียญ/ประเภทเข้า/สถานะ/สถานะ Booking + void action | 50 |
| Method-chooser | 460px | `openModalBox('method')`/`renderMethodModal()` — 3 ปุ่ม (`optBtn`) | 60 |
| CBM check-in | 560px | `openModalBox('cbm')`/`renderCbmModal()` — `cbmLookup`/`cbmConfirm` + weighToken req + sync | 60 |
| Member check-in | 680px | `openModalBox('member')`/`renderMemberModal()` — `mbLookup`/`mbConfirm` + payment bill | 60 |
| Central check-in | 680px | `openModalBox('central')`/`renderCentralModal()` — `ctConfirm` + payment bill (no quota) | 60 |
| QR scan | 460px | `openModalBox('qr')`/`renderQrModal()` — `qrGo` → CBM flow | 60 |
| Void | 460px | `openModalBox('void')`/`renderVoidModal()` — `voidConfirm` + reason(optional) | 60 |

## §7 Interaction Spec
- **3 check-in methods ⭐:** `renderMethodModal` → เช็คอินจาก CBM (`cbm`) / ไม่มีคิว-สมาชิก (`member`) / ไม่มีคิว-โควต้ากลาง (`central`)
- **CBM check-in + sync ⭐:** `cbmLookup` (findPendingCbm; not found "ไม่พบรหัส CBM นี้") → `cbmConfirm`: weighToken ว่าง "กรุณาใส่เลขเหรียญชั่ง" · success → check-in + **sync booking → bookingStatus='รอผลการเท'** + "เช็คอินสำเร็จ" · ย้ายเข้า checked-in tab (BR-03)
- **Sync fail + retry ⭐:** syncPending row → `bookingCell` badge "ซิงก์ล้มเหลว" + retry (`retrySync`) → success "ซิงก์สถานะ Booking สำเร็จ" (idempotent) (BR-04)
- **Member/Central check-in:** ข้อมูลไม่ครบ "กรุณากรอกข้อมูลให้ครบถ้วน" · payment bill งวด1+2 ไม่ครบ "กรุณาเลือกประเภทการชำระเงินให้ครบถ้วน" · success "เช็คอินสำเร็จ" (`createNbm` → NBM doc, no sync) (BR-06)
- **QR scan:** `qrGo` → เปิด CBM check-in flow (BR-10)
- **Void:** `voidConfirm` — reason optional → "ยกเลิกเช็คอินสำเร็จ" (BR-07)
- **entryType → doc:** จองคิว=CBM-#### · ไม่จองคิว/กลาง=NBM-#### (`nextNbmId`) (BR-05) · Esc chain · debounce · Render preservation

## §8 State-Driven UI Matrix
| Tab | Item state | Actions | Booking cell |
|---|---|---|---|
| ต้องส่ง (pending) | status จัดส่ง (no checkInTime) | เช็คอิน + รายละเอียด | — |
| เช็คอินแล้ว | CBM + synced | รายละเอียด + ยกเลิก | bookingStatus (รอผลการเท) |
| เช็คอินแล้ว | CBM + syncPending | รายละเอียด + ยกเลิก | ซิงก์ล้มเหลว + retry |
| เช็คอินแล้ว | non-CBM (สมาชิก/กลาง) | รายละเอียด + ยกเลิก | "-" |

## §9 Microcopy (verbatim)
**Tabs:** `ต้องส่ง` · `เช็คอินแล้ว`
**ปุ่ม:** `เช็คอิน` · `Scan QR` · `Export CSV` · `ล้าง` · `ค้นหา` · `ยืนยันเช็คอิน` · `ยืนยัน` · `ไป` · `ยกเลิก` · `รายละเอียด`
**Method chooser:** `เช็คอินจาก CBM` (ป้อนรหัส CBM หรือสแกน QR) · `เช็คอินแบบไม่มีคิว — สมาชิก` (ค้นหาโควต้าของสมาชิก) · `เช็คอินแบบไม่มีคิว — โควต้ากลาง` (ไม่มีโควต้า)
**Entry type:** `โควต้าจองคิว` · `โควต้าไม่ได้จองคิว` · `โควต้ากลาง` · **Status:** `จัดส่ง` · `รอทำจ่าย` · `เสร็จสิ้น` · **Booking:** `รอผลการเท` · `อยู่ระหว่างจัดส่ง` · `ซิงก์ล้มเหลว`
**Payment bill:** `ประเภทการชำระเงิน` · `งวดที่ 1` · `งวดที่ 2` · `บิลเขียว` · `บิลขาว` · **Vehicle:** `อีแต๋น` · `6 ล้อ` · `10 ล้อ` · `16 ล้อ`
**Fields:** `รหัส CBM` · `เลขเหรียญชั่ง` · `หมายเหตุ` · `ค้นหาโควต้า` · `ทะเบียนรถ` · `ชื่อคนขับ` · `เบอร์โทร` · `ประเภทรถ`
**Toast:** `เช็คอินสำเร็จ` · `พบข้อมูลสมาชิก` · `ซิงก์สถานะ Booking สำเร็จ` · `ยกเลิกเช็คอินสำเร็จ` · `กำลังดาวน์โหลดไฟล์ CSV`
**Errors:** `ไม่พบรหัส CBM นี้` · `ไม่พบโควต้านี้` · `กรุณาใส่เลขเหรียญชั่ง` · `กรุณากรอกข้อมูลให้ครบถ้วน` · `กรุณาเลือกประเภทการชำระเงินให้ครบถ้วน` · `ซิงก์ล้มเหลว กรุณาลองใหม่`
**Void:** `ยกเลิกเช็คอิน (Void)` · `เหตุผล (ไม่บังคับ)` · **Column:** `เลขเหรียญชั่ง` · `ประเภทการเข้าโรงงาน` · `สถานะ Booking` · **QR:** `สแกน QR — CBM`

## §10 Data Binding & BACKEND anchors
| Anchor | API |
|---|---|
| `state.items` seed | API-01 GET /checkins |
| `cbmLookup/findPendingCbm` | API-03 lookup CBM |
| `mbLookup` (member) | API-04 quota search |
| `cbmConfirm()` ⭐ | API-C1 + **API-SYNC** (FN-SYNC event CHECK_IN → รอผลการเท) |
| `mbConfirm/ctConfirm` | API-C2/C3 (FN-C2/C3 + NBM doc) |
| `retrySync()` ⭐ | API-SYNC retry (idempotent checkin_id) |
| `voidConfirm()` | API-V |
| `exportCSV()` | API-05 |
| **feed CBM** | event CHECK_IN → Cane Booking (F-AGM-007) รอผลการเท |
Mock: **3 pending** (CBM-2568-0000001..0000003, status จัดส่ง, จองคิว) · **5 checked-in** (NBM central + CBM รอผลการเท + NBM member + CBM เสร็จสิ้น + **CBM-2568-0000006 syncPending** ซิงก์ล้มเหลว) · doc CBM/NBM-2568-####

## §11 Traceability + Drift Log
| FRD | HTML anchor | Brief |
|---|---|---|
| 01_UI P-01 list 2-tab | renderListPage + topTabBar + gotoTab | §4 |
| 01_UI P-02 detail | renderViewDrawer | §6 |
| 01_UI OV method/CBM/Member/Central/QR/void | openModalBox + render*Modal | §6/§7 |
| 02_API C1 + SYNC | cbmConfirm + sync | §7/§10 |
| 02_API SYNC retry | retrySync | §7/§10 |
| 02_API C2/C3 | mbConfirm/ctConfirm | §10 |
| 03_LOGIC FN-SYNC (idempotent) | retrySync/cbmConfirm | §7 |
| 05_RULES weighToken req | cbmConfirm | §7 |
| 06_TESTS AC-01..22 / XT-01..05 | ครบ | §8/§10 |

### ⚠️ Drift Log
| # | รายการ | ทาง | หมายเหตุ |
|---|---|---|---|
| D-01 | Stats 4 การ์ด | HTML-only | ตรง BRD §18 |
| D-02 | CBM/Quota/Member อ่านจาก mock | HTML sim | ระบบจริง = ENG-BOOKING + ENG-EXT-Q |
| D-03 | weighToken = manual input | HTML sim | ระบบจริง = เครื่องชั่ง (ENG-SCALE, OQ-01) |
| D-04 | sync + retry = จำลอง (first retry success) | HTML sim | ระบบจริง = POST status-transitions idempotent + auto-retry (OQ-03) |
| D-05 | Member/Central NBM doc = client gen | HTML sim | ระบบจริง = ENG-DOC (OQ-02) |
| D-06 | void = toast | HTML sim | ระบบจริง = void + reversal event ไป Booking (OQ-04) |
| D-07 | T3 code-only reverse — labels ตาม code | reverse-note | invariants §7 C-01 |

## §12 Diff จากเวอร์ชันก่อน
เทียบ legacy (React/Vite shadcn + bookingApi.ts): คงไว้ 100% (LOCK-01) — 2-tab (ต้องส่ง/เช็คอินแล้ว), 3 check-in methods (CBM/สมาชิก/กลาง), weighToken บังคับ, **CBM sync → รอผลการเท (idempotent)**, sync-fail badge + retry, payment bill 2 งวด, QR scan, void, entry-type badge, booking-status column · เปลี่ยน: tab-state detail → CUBE drawer + route · dialogs modal → CUBE modal · pagination mock → getPaged · CI shadcn gray → CUBE Warm Light · เพิ่ม stats

## §13 💡 ข้อเสนอ
1. Scale hardware integration — weighToken auto (OQ-01)
2. Auto-retry backoff + banner สำหรับ sync fail (OQ-03)
3. Member/Central quota-lookup จริง + NBM doc service (OQ-02)
4. Void → reversal event ไป Cane Booking + audit (OQ-04)
5. Deep-link สถานะ Booking → Cane Booking detail (F-AGM-007)

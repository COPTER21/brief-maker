# UI BRIEF — F-AGM-011 Cane Receiving (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Source HTML | `cane-receiving-management.html` (v1.0, 2026-07-21 — html-generator-v6, audit FAIL=0 · WARN=2 inherited) |
| FRD Pack | `FRD_F-AGM-011_Pack/` (7 ไฟล์ STANDARD) — paired ✅ |
| BRD | BRD_F-AGM-011 APPROVED (LOCK-01..11) |
| Reverse | RIF v2 + invariants.md LOCKED 🔒 (T3 enhanced code + T1 Enhancement spec — Dump Result v2 & Sync All) |
| Cross-module | read Check-in (F-AGM-010 Draft) + Factory dump API · **write CBM (F-AGM-007)** awaiting_payment/awaiting_dump_result · free Weigh Coin · **feed Payment** (net_weight + cane_type SoT) |
| กติกา | ทุก claim ชี้ anchor ได้ (selector/function/ข้อความ verbatim) — HTML = source of truth |

## §1 Design Tokens AS-BUILT
เหมือน F-AGM-001..010 100% (CUBE Warm Light — Ivory #FAF8F5 · Charcoal #111 · Red #FF3B30 action · Orange #FF9A1F connection). Fonts Satoshi + Noto Sans Thai · Lucide 0.469.0 loader (fallback 5s). Z-index: Toast 80 · ss-list 70 · modal 60 · drawer 50 · sidebar/shell 20/19 · sticky th 3.

## §2 Route Map
| Route | หน้า | Handler |
|---|---|---|
| `#/receivings` (default, tab=draft) | P-01 List "รอผลเท" | `render()` (`getRoute()` บรรทัด 148 default 'receivings' · `gotoTab`/`topTabBar`/`tabRoute`) |
| `#/receivings/issued` \| `#/receivings/void` | P-01 "เทแล้ว"/"ยกเลิก" | seg → state.tab |
| `#/receivings/:id` | P-01 + Detail drawer (P-03) | `findItem()` → `mountViewDrawer()` refresh-safe · ไม่พบ → toast "ไม่พบรายการ" + กลับ |
Overlay ไม่ผูก route: issue drawer (`openForm('issue')`) · sync-result modal (`openModalBox('syncresult')`) · void (`void`) · pdf (`pdf`) · qr (`qr`) · search (`search`)

## §3 Layout Shell
Sidebar 232px: module เกษตรกรรม → สมาชิก..เช็คอิน (disabled), **การรับอ้อย (is-active)** + system→Settings · Breadcrumb "เกษตรกรรม › หน้างานโรงงาน › การรับอ้อย" · User chip "สมพร วงศ์ทะเบียน / เจ้าหน้าที่รับอ้อย · WKN" · **top tab-bar** (`topTabBar`): รอผลเท / เทแล้ว / ยกเลิก (`gotoTab`)

## §4 P-01 Receiving List (`renderListPage()` → `#page-content`)
```
.ph tab title (รอผลเท/เทแล้ว/ยกเลิก) + count
   .ph-actions: [Scan QR] [ค้นหาเลขเหรียญ] [Export CSV] [Sync All & ออกใบรับอ้อยอัตโนมัติ — draft tab only] [ออกใบรับอ้อย primary]
.stats 4: รอผลเท(Draft) · ออกใบวันนี้(Issued) · ยกเลิก(Void) · น้ำหนักอ้อยรวมวันนี้(Σ net กก.)
.card
 ├ filter-bar: search (debounce · `onSearchInput` — placeholder "ค้นหาเลขเหรียญ/รหัส/ทะเบียน") + select สถานะ + select ประเภทเข้า(ทุกประเภท/จองคิว/ไม่จองคิว/โควต้ากลาง) + date + ล้าง
 ├ table (draft, `renderListPage` isDraft): รหัสเกษตรกร · เลขเหรียญชั่ง · วัน/เวลาเข้า · ผู้ขนส่ง · เบอร์โทร · ทะเบียนรถ · ชื่อคนขับ · ประเภทเข้า(`entryBadge`) · Actions([ออกใบรับอ้อย → openForm('issue')][รายละเอียด])
 │  table (issued/void): + มูลค่าอ้อย(`fmtKg` net) · ประเภทการเทอ้อย(caneTypeName) · สถานะ(`statusPill`) · Actions([รายละเอียด][พิมพ์ → openPdf][Void — issued])
 │  row → openView(id) · pagination (`getPaged/goToPage`)
 └ footer: pagination
```
Empty: "ไม่มีรายการ" (ต่อแท็บ) · filter empty: "ไม่พบรายการที่ค้นหา" + ล้าง

## §5 Component Inventory (R4 states)
| Component | Anchor | States |
|---|---|---|
| Status pill | `statusPill()` | neutral รอผลเท(Draft) · success เทแล้ว(Issued) · danger ยกเลิก(Void) |
| Entry-type badge | `entryBadge()` | info จองคิว · neutral ไม่จองคิว · warn โควต้ากลาง |
| **Dump-result card v2 ⭐** | `renderFormDrawer` (dump section) | Auto badge + read-only card: ประเภทอ้อย(code+name) · เลขเหรียญชั่ง · เวลาเข้า/ออก · น.น.รวม/รถเบา/อ้อยสุทธิ |
| **Auto/Manual toggle ⭐** | `handleAutoFetch`/`setFormMode`/`resetToAuto`/`handleForceFail` | auto(locked) / manual(net+reason) |
| Manual input | `formManualInput`/`formCanIssue` | net (regex) + เหตุผล |
| Sync-result table | `renderSyncResultModal`/`syncViewFailed` | ทั้งหมด/สำเร็จ/ล้มเหลว + failed rows |
| Weight cell | `fmtKg()`/`fmtNum()` | th-TH 2-dec + กก. |
| PDF/QR | `renderPdfModal`/`openPdf` | A4 preview + QR + พิมพ์ |
| Toast | `showToast` (+desc) | success/info/warning/error |

## §6 Overlay Registry
| Overlay | ขนาด | Mount | z |
|---|---|---|---|
| Issue Receiving drawer (P-02) | 920px | `openForm('issue')`/`renderFormDrawer()` — Check-in info + Dump Result v2 + ออกใบรับอ้อย | 50 |
| Detail drawer (P-03) | 680px | `mountViewDrawer()`/`renderViewDrawer()` — dump block read-only + doc info + พิมพ์/Void | 50 |
| Sync-result modal | 680px | `openModalBox('syncresult')`/`renderSyncResultModal()` — summary + failed table | 60 |
| Void modal | 460px danger | `openModalBox('void')`/`renderVoidModal()`/`voidConfirm()` — reason≥5 + block-if-paid | 60 |
| PDF viewer modal | 720px | `openModalBox('pdf')`/`renderPdfModal()` — A4+QR | 60 |
| QR scan / Search modal | 460px | `renderQrModal`/`qrGo` · `renderSearchModal`/`searchGo` | 60 |

## §7 Interaction Spec
- **Dump v2 single sync ⭐:** `handleAutoFetch` — simulate GET /ext/factory/dump (checkin_datetime+coin+quota) → success → read-only card (ประเภทอ้อย/เวลาเข้า-ออก/gross-tare-net) + lock + Auto badge · `handleForceFail` (จำลองไม่พบผล) → "ไม่พบผลการเทจากโรงงาน — กรุณาเปลี่ยนเป็นโหมด Manual" + manual mode (BR-01/02)
- **Manual fallback:** `setFormMode('manual')` — net regex `^\d+(\.\d{1,2})?$` non-neg ("กรุณากรอกน้ำหนักสุทธิ"/"กรุณากรอกน้ำหนักสุทธิเป็นจำนวนไม่ลบและ 2 ตำแหน่ง") + เหตุผล ("กรุณากรอกเหตุผลการกรอกด้วยตนเอง")
- **Issue + side effects ⭐:** `issueSubmit` — สร้าง CRN (`nextCrn`) + status Issued + move to เทแล้ว + paymentStatus 'รอทำจ่าย' + coinReturned + PDF → toast "ออกใบรับอ้อยสำเร็จ" (desc CBM awaiting_payment + ปลดเหรียญ + PDF) (BR-04)
- **Sync All ⭐:** `syncAll` — ถ้าไม่มี `state.filters.date` → warn "กรุณาเลือกช่วงวันที่ก่อนทำ Sync All" · else toast "กำลังดึงผลการเท..." → ~70% Draft auto-issue → `renderSyncResultModal` (ทั้งหมด/สำเร็จ/ล้มเหลว + failed table "ไม่พบข้อมูลผลการเทในระบบโรงงาน") → toast "ดึงผลการเทเสร็จสิ้น (สำเร็จ X, ล้มเหลว Y)" (BR-06/07)
- **Void + rollback ⭐:** `voidConfirm` — reason<5 "เหตุผลต้องมีความยาวอย่างน้อย 5 ตัวอักษร" · paymentStatus=ชำระเงินแล้ว → block · success → status Void + note CBM awaiting_dump_result → toast "Void ใบรับอ้อยสำเร็จ" (BR-09/10)
- **Export CSV:** `exportCSV` → "กำลังส่งออกข้อมูล..." → "ส่งออกข้อมูลสำเร็จ" · Esc chain · debounce · Render preservation

## §8 State-Driven UI Matrix
| Tab | Item | Actions | Dump |
|---|---|---|---|
| รอผลเท (Draft) | dumpResultSource '-' | ออกใบรับอ้อย + รายละเอียด | ดึงผลการเท (Auto)/Manual |
| เทแล้ว (Issued) | CRN + auto/manual | รายละเอียด + พิมพ์ + Void | read-only card |
| ยกเลิก (Void) | voidReason | รายละเอียด + พิมพ์ | read-only (audit) |
| Issued + ชำระเงินแล้ว | paymentStatus | รายละเอียด + พิมพ์ (void blocked) | — |

## §9 Microcopy (verbatim)
**Tabs:** `รอผลเท` · `เทแล้ว` · `ยกเลิก`
**ปุ่ม:** `ออกใบรับอ้อย` · `ดึงผลการเท (Auto)` · `สลับเป็นโหมดกรอกมือ` · `รีเซ็ต / กลับไป Auto` · `จำลองไม่พบผล` · `Sync All & ออกใบรับอ้อยอัตโนมัติ` · `Scan QR` · `ค้นหาเลขเหรียญ` · `Export CSV` · `พิมพ์` · `Void` · `ดูรายการที่ล้มเหลว` · `ปิด` · `ยืนยันการยกเลิก`
**Dump card:** `ผลการเทจากโรงงาน (Dump Result)` · `ประเภทอ้อย` · `เลขเหรียญชั่ง` · `เวลาเข้า (Time In)` · `เวลาออก (Time Out)` · `น.น. รวม (กก.)` · `น.น. รถเบา (กก.)` · `น.น. อ้อยสุทธิ (กก.)` · badge `Auto`/`Manual`
**Check-in info:** `ข้อมูล Check-in` · `รหัส Check-in` · `ประเภทการจอง` · `รหัส Booking` · `เวลา Check-in` · `ประเภทเข้าโรงงาน` · `Quota ID`
**Sync All modal:** `ผลการ Sync All` · `ทั้งหมด` · `สำเร็จ` · `ล้มเหลว` · `รหัสสมาชิก`
**Toast:** `ออกใบรับอ้อยสำเร็จ` · `Void ใบรับอ้อยสำเร็จ` · `กำลังดึงผลการเท...` · `ดึงผลการเทเสร็จสิ้น` · `ดึงผลการเทสำเร็จ` · `กำลังส่งออกข้อมูล...` · `ส่งออกข้อมูลสำเร็จ` · `ไม่พบ PDF`
**Errors:** `ไม่พบผลการเทจากโรงงาน — กรุณาเปลี่ยนเป็นโหมด Manual` · `กรุณากรอกน้ำหนักสุทธิ` · `กรุณากรอกน้ำหนักสุทธิเป็นจำนวนไม่ลบและ 2 ตำแหน่ง` · `กรุณากรอกเหตุผลการกรอกด้วยตนเอง` · `เหตุผลต้องมีความยาวอย่างน้อย 5 ตัวอักษร` · `ไม่พบข้อมูลผลการเทในระบบโรงงาน` · `กรุณาเลือกช่วงวันที่ก่อนทำ Sync All`
**Void note:** `การยกเลิกจะย้อนสถานะ CBM เป็น awaiting_dump_result และไม่สามารถชำระเงินต่อ`

## §10 Data Binding & BACKEND anchors
| Anchor | API |
|---|---|
| `state.items` seed | API-01 GET /cane-receivings |
| `handleAutoFetch` ⭐ | API-DUMP GET /ext/factory/dump (v2, FN-DUMP) |
| `issueSubmit` ⭐ | API-C1 POST /cane-receivings (FN-C1 + FN-SIDE: CBM awaiting_payment + free coin + PDF) |
| `syncAll` ⭐ | API-SYNC POST /cane-receivings/sync-all (FN-SYNC bulk) |
| `voidConfirm` | API-V POST /:id/void (FN-V rollback awaiting_dump_result) |
| `openPdf`/`renderPdfModal` | API-PDF (A4+QR) |
| `exportCSV` | API-03 |
| **feed Payment** | net_weight_kg + cane_type_code (SoT) → Cane Payment |
Mock: **4 Draft** (CHK-####, mix CBM/NBM/CENTRAL) · **3 Issued** (CRN-2568-00001..3, dump v2 auto, 1 ชำระเงินแล้ว = void-blocked) · **1 Void** · Σ net 65,000 กก.

## §11 Traceability + Drift Log
| FRD | HTML anchor | Brief |
|---|---|---|
| 01_UI P-01 list 3-tab | renderListPage + topTabBar | §4 |
| 01_UI P-02 issue drawer (dump v2) | openForm('issue') + handleAutoFetch | §6/§7 |
| 01_UI P-03 detail | renderViewDrawer | §6 |
| 01_UI OV sync-result | renderSyncResultModal | §6 |
| 01_UI OV void/pdf/qr/search | renderVoidModal/renderPdfModal/... | §6 |
| 02_API DUMP (v2) | handleAutoFetch | §7/§10 |
| 02_API C1 + SIDE | issueSubmit | §7/§10 |
| 02_API SYNC | syncAll | §7/§10 |
| 03_LOGIC FN-VALID | formManualInput/formCanIssue | §7 |
| 05_RULES void rollback + block-paid | voidConfirm | §7/§8 |
| 06_TESTS AC-01..22 / XT-01..05 | ครบ | §8/§10 |

### ⚠️ Drift Log
| # | รายการ | ทาง | หมายเหตุ |
|---|---|---|---|
| D-01 | Stats 4 การ์ด | HTML-only | ตรง BRD §18 |
| D-02 | Factory dump / Check-in อ่านจาก mock | HTML sim | ระบบจริง = ENG-FACTORY + read F-AGM-010 |
| D-03 | dump auto = จำลอง (first success, force-fail button) | HTML sim | ระบบจริง = /ext/factory/dump v2 + BE คำนวณ net |
| D-04 | issue side effects (CBM awaiting_payment + free coin + PDF) = toast/sim | HTML sim | ระบบจริง = ENG-CBM + ENG-COIN + ENG-PDF |
| D-05 | Sync All ~70% mock success | HTML sim | ระบบจริง = POST /sync-all idempotent + lock (OQ-03) |
| D-06 | **CCS ถอดออกจาก Receiving** | AS-BUILT (v2) | ย้ายไป Payment · invariants §7 C-01 |
| D-07 | dump query key = checkin_datetime+coin+quota | AS-BUILT (v2) | invariants §7 C-02 |
| D-08 | PDF/QR = preview | HTML sim | ระบบจริง = A4 ไทย + QR verify |

## §12 Diff จากเวอร์ชันก่อน (base → Enhancement v2)
เทียบ base FRD (as-is): dump คืน {ccs, net_weight}, query date+coin, ไม่มี Sync All → **Enhancement v2 (AS-BUILT):** dump ชุดเต็ม (ประเภทอ้อย/เวลาเข้า-ออก/gross-tare-net · **ไม่มี CCS** ย้าย Payment), query checkin_datetime+coin+quota_id, + **Sync All** (bulk auto-issue), Receiving = SoT ของ net+cane_type · เปลี่ยน: in-page screens → CUBE drawer/modal + route · CI shadcn → CUBE Warm Light · เพิ่ม stats

## §13 💡 ข้อเสนอ
1. Factory dump API จริง + net cross-check (gross−tare vs net) เก็บ debug (OQ-02)
2. Sync All idempotency + lock (ไม่รันซ้อน) + progress bar (OQ-03)
3. cane_type master (1–22) ชื่อไทยจาก config (OQ-01)
4. factory_dump_logs (raw_payload) audit trail (OQ-04)
5. Receiving → Payment deep-link (net+cane_type SoT handoff)

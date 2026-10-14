# UI BRIEF — F-AGM-012 Cane Payment Setting (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Source HTML | `cane-payment-setting.html` (v1.0, 2026-07-21 — html-generator-v6, audit FAIL=0 · WARN=1 inherited) |
| FRD Pack | `FRD_F-AGM-012_Pack/` (7 ไฟล์ STANDARD) — paired ✅ |
| BRD | BRD_F-AGM-012 APPROVED (LOCK-01..11) |
| Reverse | RIF v2 + invariants.md LOCKED 🔒 (T3 enhanced code AS-BUILT + T1 Enhancement brief + FRD/UI/API-DB docs) |
| Cross-module | อ่าน masters (Season/Product/Price List — Base @10CCS) · **expose active setting → Cane Payment** (API-EXT) · เป็น SoT ของ K/ดอกเบี้ย/ค่าธนาคาร/ตารางวันจ่าย ที่ Payment runtime อ่าน |
| กติกา | ทุก claim ชี้ anchor ได้ (selector/function/ข้อความ verbatim) — HTML = source of truth |

## §1 Design Tokens AS-BUILT
เหมือน F-AGM-001..011 100% (CUBE Warm Light — Ivory #FAF8F5 · Charcoal #111 · Red #FF3B30 action · Orange #FF9A1F connection). Fonts Satoshi + Noto Sans Thai · Lucide 0.469.0 loader multi-CDN (fallback 5s, บรรทัด 75). Z-index: Toast 80 · modal 60 · sidebar/shell 20/19 · sticky th 3. หมายเหตุ: feature นี้เป็น **single-config-page** (ไม่มี list/drawer) — ใช้ inner-nav ซ้าย 6 section + card ขวา.

## §2 Route Map
| Route | หน้า | Handler |
|---|---|---|
| `#/payment-setting` (default, section=general) | P-01 Config Page | `getRoute()` (บรรทัด 173, default 'payment-setting') → `render()` → `renderConfig()` |
| section switch (ไม่ผูก route) | 6 sections | `setSection(k)` → `state.section` → `sectionBody()` switch |
| payout sub-tab (ไม่ผูก route) | บิลเขียว/บิลขาว | `setPayoutTab(t)` → `state.payoutTab` |
Overlay ไม่ผูก route: charge modal (`openModalBox('charge')`) · payout range modal (`openModalBox('payout')`). Hashchange guard: `getRoute()!=='payment-setting'` → `navigate('payment-setting')` (บรรทัด 565).

## §3 Layout Shell
Sidebar 232px: module เกษตรกรรม → สมาชิก..การรับอ้อย (is-disabled), **ตั้งค่าการจ่ายเงินอ้อย (is-active, icon banknote)** + system→Settings · Breadcrumb "เกษตรกรรม › Cane Payment › ตั้งค่าการจ่ายเงินอ้อย" · User chip "สมพร วงศ์ทะเบียน / Finance Officer · WKN" (avatar สว) · **ไม่มี top tab-bar** (single page).

## §4 P-01 Config Page (`renderConfig()` → `#page-content`)
```
phHeader():  .ph
   ├ ph-title "Payment Setting Configuration" + statusPill(true)=ใช้งาน
   ├ ph-sub "แหล่งความจริงของค่าพื้นฐานที่ Cane Payment ใช้คำนวณ"
   └ ph-actions: [บันทึก primary → saveSettings()]
contextBar():  season selector (ฤดูการหีบ (Crushing Season) → setSeason · SEASONS 2024/2025..)
   + pill "Product: อ้อยสด" + pill-info "Base @10CCS: 900.00 บาท/ตัน"
grid 240px | 1fr:
   ├ card ซ้าย: innerNav() — 6 ปุ่ม section (active = border+bg แดงอ่อน)
   └ card ขวา: sectionBody() → switch(state.section)
```
6 sections (NAV บรรทัด 92): `general` ข้อมูลทั่วไป(settings) · `ccs-delta` สูตรคำนวณ CCS(trending-up) · `additional-charges` รายการหักเพิ่มเติม(dollar-sign) · `tax` ภาษี(file-text) · `payout-schedule` ตารางกำหนดวันจ่าย(calendar) · `preview-test` ทดสอบและดูตัวอย่าง(eye).

## §4.1 Section Detail
- **General (`secGeneral`):** 3 form-section — (1) ข้อมูลสินค้า: สินค้าอ้อย(select อ้อยสด) + หมายเหตุ(textarea `setNote`). (2) ดอกเบี้ยบิลขาว: ดอกเบี้ยต่อปี(`#g-rate`)/วันฐาน(`#g-base`) → `onGeneralNum()` live → ดอกเบี้ยต่อวัน(`#g-daily` readonly = `dailyRateStr()`) + note info "ปัดขึ้น 7 ตำแหน่ง". (3) ค่าธนาคาร: จังหวัดหลัก(`setMainProvince`) + ค่าในจังหวัด(`setFeeIn`) + ค่าต่างจังหวัด(`setFeeOut`).
- **CCS Delta (`secCcs`):** note สูตร "ราคาต่อตัน = Base @10CCS + (CCS − 10) × (Base @10CCS × K)" · inputs ค่า K(`#ccs-k` 0–1)/CCS ตัวอย่าง(`#ccs-sample`) → `onCcsInput()` live · 4 stat: Base @10CCS / ราคาต่อ 1 CCS (Base×K) / ราคาต่อตัน @{c} CCS / ราคาต่อกิโลกรัม (÷1000).
- **Additional Charges (`secCharges`):** [เพิ่มรายการ] + table (ชื่อรายการ/ประเภท[จำนวนเงิน|เปอร์เซ็นต์]/ค่า/หมายเหตุ/จัดการ[แก้ไข·ลบ]) · empty "ยังไม่มีรายการ".
- **Tax (`secTax`):** note info · toggle switch "หัก VAT ก่อนแบ่งงวด" (`toggleVat`) → เปิด → field อัตรา VAT (%) (`setVatRate`).
- **Payout Schedule (`secPayout`):** 2 sub-tabs `.tabs` (ตารางวันจ่ายบิลเขียว/บิลขาว → `setPayoutTab`) → `greenTable()`/`whiteTable()`.
- **Preview & Test (`secPreview`):** form ข้อมูลทดสอบ (7 inputs) + [คำนวณ → runPreview()] → `previewResultHTML()`.

## §5 Component Inventory (R4 states)
| Component | Anchor | States |
|---|---|---|
| Status pill (header) | `statusPill()` | success ใช้งาน · muted ปิด |
| Inner-nav button | `innerNav()` | active(border+bg แดงอ่อน 6%) / idle |
| Daily-rate readonly | `#g-daily` / `dailyRateStr()` | auto = `roundUp(rate/base,7)` (บรรทัด 147–148) |
| CCS stat cards | `ccsStat`/`ccsStatL` | live: base/per1/perton(label @{c} CCS)/perkg |
| Charge row | `secCharges` rows | amount(บาท) / percent(%) |
| VAT switch | `switchHTML`/`toggleVat` | on(แดง) / off · เปิด→rate field |
| Payout tab | `.tabs .tab` | green.on / white.on |
| Green row | `greenTable()` | active toggle + pay1/pay2 (fmtThaiDate พ.ศ.) |
| White row | `whiteTable()` | FIXED_DATE(mono date) / WITH_CANE("ตามตารางบิลเขียว (ไม่คิดดอกเบี้ย)") |
| Active toggle (payout) | `switchHTML`/`togglePayoutActive` | on/off per row |
| Preview inst block | `instBlock()` | บิลเขียว(pill-success) / บิลขาว(pill-warning) + interest |
| Toast | `showToast` (+desc) | success/info/warning/error |

## §6 Overlay Registry
| Overlay | ขนาด | Mount | z |
|---|---|---|---|
| Additional-charge modal | 460px | `openModalBox('charge')`/`renderChargeModal()`/`chargeSave()` — ชื่อ/ประเภท/ค่า/หมายเหตุ | 60 |
| Payout-range modal | 520px | `openModalBox('payout')`/`renderPayoutModal()`/`payoutSave()` — เดือน/ปี พ.ศ./วันเริ่ม–สิ้นสุด + (green: วันจ่ายงวด 1/2) / (white: ประเภทวันจ่าย + วันจ่าย) | 60 |
Backdrop `#modalBackdrop` click / Esc → `closeModal()` (บรรทัด 562 ESC chain). ไม่มี drawer ใน feature นี้.

## §7 Interaction Spec
- **Daily-rate auto ⭐:** `onGeneralNum()` — พิมพ์ ดอกเบี้ยต่อปี/วันฐาน → set `#g-daily` = `dailyRateStr()` = `roundUp(rateYear/baseDays, 7)` live (readonly). เช่น 7/365 → 0.0191781 (BR-PS-05).
- **CCS live preview ⭐:** `onCcsInput()` — k+ccs → per1=Base×k · perton=Base+(ccs−10)×per1 · perkg=perton/1000 · label "ราคาต่อตัน @{c} CCS" (BR-PS-02, FN-CCS).
- **Payout white pay-type gating ⭐:** `payoutSetPayType(v)` — เลือก "วันที่กำหนด"(FIXED_DATE) → แสดง field วันจ่าย · "พร้อมค่าอ้อย"(WITH_CANE) → ซ่อน + hint "จ่ายตามตารางบิลเขียว (ไม่คิดดอกเบี้ย)". Save: FIXED_DATE ไม่กรอกวัน → "กรุณากรอกวันจ่ายเมื่อเลือกวันที่กำหนด" (VR-07).
- **Payout range save:** `payoutSave()` — from>to → "วันเริ่มต้นต้องไม่เกินวันสิ้นสุด" · add/edit merge by id (VR-06).
- **Preview calc ⭐:** `runPreview()` — perTon = FN-CCS · total = perTon×weight · half=total/2 · per งวด `calc(bill,normalDate,actualDate)`: daysEarly=บิลขาว?30:0 · after=half×(1−debt/100) · interest=บิลขาว?round2(after×(dr/100)×daysEarly):0 · fee = จังหวัด=หลัก?feeIn:feeOut · net=after−interest−fee → `previewResultHTML()` + toast "คำนวณสำเร็จ" (BR-PS-05/06/08, FN-PREVIEW/INT/BANK).
- **Save settings:** `saveSettings()` — validate: rate>0 "ดอกเบี้ยต่อปีต้องมากกว่า 0" · base>0 "วันฐานต้องมากกว่า 0" · fee used & no province "กรุณาเลือกจังหวัดหลัก" · K 0–1 "ค่า K ต้องอยู่ระหว่าง 0–1" → toast "บันทึกการตั้งค่าสำเร็จ" (desc ฤดูการหีบ + ดอกเบี้ยต่อวัน) (VR-01..05, VR-08).
- **Charge CRUD:** `addCharge`/`editCharge`/`deleteCharge`/`chargeSave` — name required + value numeric · Esc chain · Render preservation (`preserveState`/`restoreState` focus + scroll).

## §8 State-Driven UI Matrix
| Section | Live compute | Overlay | Save target |
|---|---|---|---|
| General | daily-rate readonly (onGeneralNum) | — | rate/base/province/fee (VR-01..04) |
| CCS Delta | 4 stat live (onCcsInput) | — | k (VR-05) |
| Charges | — | charge modal | charges[] |
| Tax | vatEnabled toggle → rate field | — | vat |
| Payout-green | — | payout modal (pay1/pay2) | payout.green[] |
| Payout-white | payType gating (FIXED_DATE/WITH_CANE) | payout modal | payout.white[] |
| Preview | full calc (runPreview) | — | non-persistent (BR-PS-10) |

## §9 Microcopy (verbatim)
**Header/context:** `Payment Setting Configuration` · `แหล่งความจริงของค่าพื้นฐานที่ Cane Payment ใช้คำนวณ` · `ฤดูการหีบ (Crushing Season)` · `Product: อ้อยสด` · `Base @10CCS: 900.00 บาท/ตัน`
**Sections:** `ข้อมูลทั่วไป` · `สูตรคำนวณ CCS` · `รายการหักเพิ่มเติม` · `ภาษี` · `ตารางกำหนดวันจ่าย` · `ทดสอบและดูตัวอย่าง`
**General:** `ข้อมูลสินค้า` · `สินค้าอ้อย` · `หมายเหตุ` · `ดอกเบี้ยบิลขาว` · `ดอกเบี้ยต่อปี (%)` · `วันฐาน (วัน)` · `ดอกเบี้ยต่อวัน` · `ค่าธนาคาร` · `จังหวัดหลัก` · `ค่าธรรมเนียมในจังหวัด (บาท)` · `ค่าธรรมเนียมต่างจังหวัด (บาท)`
**CCS:** `สูตร: ราคาต่อตัน = Base @10CCS + (CCS − 10) × (Base @10CCS × K)` · `ค่า K` · `ค่า CCS ตัวอย่าง` · `Base Price @10CCS` · `ราคาต่อ 1 CCS` · `ราคาต่อตัน @{c} CCS` · `ราคาต่อกิโลกรัม`
**Tax:** `หัก VAT ก่อนแบ่งงวด` · `อัตรา VAT (%)`
**Payout tabs/cols:** `ตารางวันจ่ายบิลเขียว` · `ตารางวันจ่ายบิลขาว` · `ช่วงวันที่ส่ง/ขึ้นเงิน` · `วันจ่ายงวด 1` · `วันจ่ายงวด 2` · `ช่วงวันที่เบิกบิลขาว` · `วันจ่าย` · `การใช้งาน` · `จัดการ` · `ตามตารางบิลเขียว (ไม่คิดดอกเบี้ย)`
**Payout modal:** `เพิ่ม/แก้ไขช่วงการจ่าย` · `เดือน` · `ปี พ.ศ.` · `วันเริ่มต้น` · `วันสิ้นสุด` · `ประเภทวันจ่าย` · `วันที่กำหนด` · `พร้อมค่าอ้อย`
**Preview:** `ข้อมูลทดสอบ` · `ค่า CCS` · `น้ำหนัก (ตัน)` · `วันที่ส่ง/ขึ้นเงิน` · `ประเภทบิลงวด 1` · `ประเภทบิลงวด 2` · `บิลเขียว (ปกติ)` · `บิลขาว (เบิกล่วงหน้า มีดอกเบี้ย)` · `% หักหนี้ (จาก Booking)` · `จังหวัดบัญชีเกษตรกร` · `ผลการคำนวณ` · `ยอดรวม` · `ราคาต่อตัน` · `ราคาต่อกิโลกรัม` · `ยอดรวม (price/ton × น้ำหนัก)` · `งวดที่ 1` · `งวดที่ 2` · `วันจ่ายปกติ` · `วันจ่ายจริง` · `จำนวนวันล่วงหน้า` · `ยอดก่อนหักหนี้` · `ยอดหลังหักหนี้` · `ดอกเบี้ย` · `ค่าธนาคาร` · `ยอดสุทธิ`
**ปุ่ม:** `บันทึก` · `เพิ่มรายการ` · `เพิ่มช่วง` · `คำนวณ` · `แก้ไข` · `ลบ` · `ยกเลิก`
**Toast:** `บันทึกการตั้งค่าสำเร็จ` · `คำนวณสำเร็จ` · `บันทึกช่วงการจ่ายสำเร็จ` · `ลบช่วงการจ่ายสำเร็จ` · `เพิ่มรายการสำเร็จ` · `บันทึกรายการสำเร็จ` · `ลบรายการสำเร็จ`
**Errors:** `ดอกเบี้ยต่อปีต้องมากกว่า 0` · `วันฐานต้องมากกว่า 0` · `กรุณาเลือกจังหวัดหลัก` · `ค่า K ต้องอยู่ระหว่าง 0–1` · `วันเริ่มต้นต้องไม่เกินวันสิ้นสุด` · `กรุณากรอกวันจ่ายเมื่อเลือกวันที่กำหนด` · `กรุณากรอกชื่อรายการ` · `กรุณากรอกค่าให้ถูกต้อง`

## §10 Data Binding & BACKEND anchors
| Anchor | API / FN |
|---|---|
| `state` seed (general/ccs/charges/tax/payout) | API-01 GET /cane-payment/settings?seasonId= (FN-01) |
| `saveSettings` ⭐ | API-03 PUT /settings/:id (FN-02 + FN-DAILY compute dailyRate + FN-SCHED + FN-11 unique Active + FN-10 audit) |
| `onGeneralNum`/`dailyRateVal` ⭐ | FN-DAILY roundUp(rate/base,7) — **BE คำนวณตอน save** (§2.X API-03) |
| `onCcsInput` | FN-CCS computeCcsPrice |
| `runPreview` ⭐ | (preview UI) FN-PREVIEW+INT+BANK — non-persistent |
| `chargeSave`/`deleteCharge` | API-CH /settings/:id/charges |
| `payoutSave` (green/white) | API-GS/API-WS green/white-schedules (FN-SCHED no-overlap) |
| **expose → Cane Payment** | API-EXT GET /payment-settings/active?season=&product= (ENG-EXPOSE, active only) |
| masters (Base @10CCS) | API-SEASON/PROD/PRICE |
Mock: BASE_10CCS 900.00 · SEASONS 3 · charges 2 (ค่าขนส่ง 50 บาท/ตัน, ค่าปรับความชื้น 2%) · green 3 rows · white 2 rows (1 FIXED_DATE 12 พ.ย. 2568, 1 WITH_CANE) · daily-rate default 0.0191781.

## §11 Traceability + Drift Log
| FRD | HTML anchor | Brief |
|---|---|---|
| 01_UI General+interest+bank | secGeneral / onGeneralNum | §4.1/§7 |
| 01_UI CCS Delta | secCcs / onCcsInput | §4.1/§7 |
| 01_UI Charges | secCharges / chargeSave | §4.1/§6 |
| 01_UI Tax | secTax / toggleVat | §4.1 |
| 01_UI Payout 2-subtab | secPayout / greenTable / whiteTable | §4.1/§5 |
| 01_UI Payout modal + pay-type | renderPayoutModal / payoutSetPayType | §6/§7 |
| 01_UI Preview & Test | secPreview / runPreview | §4.1/§7 |
| 02_API-03 save + dailyRate | saveSettings + dailyRateVal | §7/§10 |
| 02_API-EXT active setting | (expose) | §10 |
| 03_LOGIC FN-DAILY/CCS/INT/BANK/PREVIEW | onGeneralNum/onCcsInput/runPreview | §7 |
| 04_DB green/white schedule tables | payout.green/white | §5/§10 |
| 05_RULES VR-01..08 EC-01..14 | saveSettings/payoutSave validate | §7 |
| 06_TESTS AC-01..23 / XT-01..05 | ครบ | §8/§10 |

### ⚠️ Drift Log
| # | รายการ | ทาง | หมายเหตุ |
|---|---|---|---|
| D-01 | **Single-config-page** (ไม่ใช่ CRUD-list) | AS-BUILT (code) | FRD doc = CRUD-list/create/edit/duplicate/deactivate = backend spec · invariants §7 C-01 |
| D-02 | **CCS ย้ายจาก Receiving มา Payment** | AS-BUILT | invariants §7 · Receiving D-06 |
| D-03 | dailyRate คำนวณฝั่ง client (readonly) | HTML sim | ระบบจริง = BE คำนวณตอน save (roundUp 7) API-03 |
| D-04 | Preview calc = client sim (normal/actual date, daysEarly=30 คงที่บิลขาว) | HTML sim | ระบบจริง = FN-PREVIEW จาก schedule จริง + วันที่ส่ง |
| D-05 | bank fee = province match (in/out) | AS-BUILT | เช็ค/เงินสด → 0 (BR-PS-08, ไม่แสดงใน UI preview เพราะ default โอน) |
| D-06 | WITH_CANE → ไม่คิดดอกเบี้ย + วันจ่ายตามบิลเขียว | AS-BUILT | BR-PS-06 |
| D-07 | unique Active / optimistic lock / audit | backend | ระบบจริง = FN-11/FN-10 (UI ไม่มี list ให้เห็น status สลับ) |
| D-08 | RBAC 4 roles (Finance Manager/Officer/Operations/Auditor) | backend | UI = Finance Officer (canWrite=true) |

## §12 Diff จากเวอร์ชันก่อน (base → Enhancement AS-BUILT)
เทียบ base zip (GeneralSettings 72 บรรทัด / PayoutSchedule 317): base มีแค่ config พื้นฐาน + payout เดี่ยว → **Enhancement AS-BUILT (cpslegacy2, GeneralSettings 322 / PayoutSchedule 693):** เพิ่ม (1) กลุ่ม **ดอกเบี้ยบิลขาว** (rate/base → dailyRate roundUp 7) · (2) **ค่าธนาคาร** in/out province · (3) payout แยก **บิลเขียว (งวด 1/2)** + **บิลขาว (FIXED_DATE/WITH_CANE)** · (4) **Preview & Test** เต็ม (interest + bank fee per งวด). เปลี่ยน: CI shadcn (single page) → CUBE Warm Light + inner-nav 6 section + CUBE modal · Payment Setting = SoT ของ K/ดอกเบี้ย/ค่าธนาคาร/ตารางวันจ่าย ที่ Cane Payment runtime อ่าน (API-EXT).

## §13 💡 ข้อเสนอ
1. Backend เต็ม = CRUD-list per season×product (unique Active) — UI ปัจจุบัน edit config เดียว/รอบหีบ; ระบบจริงเพิ่มหน้า list + duplicate + deactivate (FRD doc)
2. daily-rate + preview interest ควรคำนวณฝั่ง BE (ENG-CALC shared กับ Payment runtime) เพื่อ single source
3. Preview daysEarly ควรดึงจาก schedule จริง (normal_pay_date − actual) แทนค่าคงที่ 30
4. no-overlap validation ฝั่ง BE ต่อ (setting, month_year) — UI ตอนนี้ตรวจแค่ from≤to
5. API-EXT active-setting-provider = จุด handoff สำคัญ → Cane Payment deep-link + version/etag เพื่อ audit ค่าที่ใช้จ่ายจริง

# AI Test Cases — F-AGM-013 Cane Payment (การทำจ่ายเงินอ้อย)

ชุด test case สำหรับ **AI agent (browser-use / vision)** รันบน prototype `cane-payment.html`
ทุก anchor คือข้อความที่เห็นบนจอจริง (ยืนยันกับ prototype HTML + FRD 06_TESTS/05_RULES + UI_BRIEF §9 microcopy แล้ว) · Expected เช็คได้ด้วยตา · ตัวเลขทุกตัว copy เป๊ะจาก calc engine ของ prototype
เคสที่ prototype จำลองไม่ได้ (**CCS legacy API จริง** · **Debt service จริง + 424 retry** · **BE recalc /confirm + optimistic lock 412** · **Idempotency/unique** · **RBAC role อื่น** (fixed Finance Officer) · **PDF บิล/ใบเสร็จ render จริง** · **WHITE/GREEN block VR-01** (enforce upstream) · **cane-type-specific adj (RATOON+5/BURN−20)** · **UNKNOWN branch-province warning** · **cash/cheque proof upload storage** · **config จริงจาก Payment Setting F-AGM-012**) ติด `(ต้อง simulate)` — รันซ้ำกับระบบจริงตอน SIT

> ⚠ **หมายเหตุ calc = client sim (mock constants):** ทุกขั้นคำนวณใน `payCalc()` ใช้ค่าคงที่ hard-code (price 1000 · adj +10/ตัน · VAT 735 / WHT 315 / fund 50 = 1,100 · config CFG-01 200 + CFG-02 100 · debt 90% หักจริง 4,000 · interest บิลขาว 120 · bank fee in 10 / out 20). ระบบจริง = **ENG-CALC ฝั่ง BE** (shared กับ Payment Setting) → ตัวเลข/สูตร verify ที่ SIT

> ⚠ **หมายเหตุ ปรับประเภทอ้อย (v4.1) — สำคัญ:** prototype hard-code `CANE_ADJUST_PER_TON = 10` **ทุกประเภทอ้อย** (FRESH/RATOON/BURN แสดง `+฿10.00 /ตัน` เหมือนกันหมด) → กติกา FRD BR-03 (FRESH +10 · RATOON +5 · BURN −20) และ VR-12 (cane_type ไม่พบ → adj 0 + `⚠️ ไม่มีข้อมูลประเภทอ้อย`) **reachable ไม่ได้บน prototype** = `(ต้อง simulate)`

> ⚠ **หมายเหตุ ยอดสุทธิ clamp = ฿0.00:** เพราะ debt หักจริง 4,000 > ยอดก่อนหักหนี้ (งวด base 5,000 → 3,900 → 3,600) → `ยอดหลังหักหนี้` ติดลบ `฿-400.00` → `ยอดสุทธิ = max(0, …) = ฿0.00` (EC-06 clamp). เป็นพฤติกรรม AS-BUILT ของ mock — ไม่ใช่ bug ของ test

> ⚠ **หมายเหตุ summary block ≠ step card (drift D-08):** บล็อก `สรุปยอดรวมทั้งหมด` ใช้สูตรง่าย `max(0, base − ค่าธนาคาร)` (งวดที่ 1 = `฿4,990.00`) ต่างจาก step card ที่รัน pipeline เต็ม (`ยอดสุทธิ ฿0.00`). อีกจุด: `ยอดตั้งต้นงวด (base) ฿5,000.00` = ค่า seed ไม่ใช่ `มูลค่าหลังปรับ ฿10,605.00 × 50%` — mock inconsistency (preserved)

> ⚠ **หมายเหตุ 3 tab (FRD) vs 2 tab (prototype):** FRD AC-01 ระบุ 3 แท็บ (รอความหวาน/รอทำจ่าย/เสร็จสิ้น) แต่ prototype top tab มีแค่ **2** (`รอทำจ่าย` = ทุก non-completed รวม waiting_ccs · `เสร็จสิ้น`). `รอดึงค่าความหวาน` เข้าถึงผ่าน dropdown สถานะ ไม่ใช่ top tab

> ⚠ **หมายเหตุ role:** prototype fix `CURRENT_ROLE = 'Finance Officer'` · `canWrite = true` เสมอ (user chip `สมพร วงศ์ทะเบียน / Finance Officer · WKN`) · RBAC role อื่น (Cashier/Accounting/Viewer/Admin) + 403 = `(ต้อง simulate)`

## Meta

| Field | Value |
|---|---|
| Feature ID | F-AGM-013 (AGM/CANE-PAYMENT — การทำจ่ายเงินอ้อย · 2 งวด + โปรโมชัน) |
| App entry | เปิดไฟล์ `cane-payment.html` ใน browser (Chrome desktop ≥1180px) |
| Routes | `#/payments` (tab **รอทำจ่าย** — default) · `#/payments/completed` (tab **เสร็จสิ้น**) · `#/payments/:id` (detail drawer 720px, refresh-safe) |
| Top tabs (page-level) | **รอทำจ่าย** (non-completed, count **4**) · **เสร็จสิ้น** (completed, count **1**) |
| Overlays (ไม่ผูก route) | All-in-One Payment modal 900px (`openPayment`) · Detail drawer 720px (ผูก route) · Sync CCS modal 480px · Sync All modal 640px |
| ที่มา | FRD_F-AGM-013_Pack (06_TESTS AC-01..32 + XT-01..06 · 05_RULES BR-01..19 / VR-01..13 / EC-01..14) · UI_BRIEF §9 |
| จำนวนเคส | 58 เคส / 9 groups |
| Signature ⭐⭐⭐ | **All-in-One modal + step calc 7 ขั้น + auto-switch งวด**: มูลค่าอ้อย → ปรับประเภทอ้อย → แบ่งงวด → ภาษี → รายการหัก → หักหนี้ → ดอกเบี้ย(บิลขาว) → ค่าธนาคาร(โอน) → ยอดสุทธิ |
| หัวใจ 1 — Step calc ⭐ | `calcCardHtml` การ์ด `ขั้นตอนการคำนวณ` live ตาม `payCalc(row,kind,method,manual)` — recalc ทันทีเมื่อเปลี่ยนวิธีจ่าย/เพิ่มรายการหัก |
| หัวใจ 2 — 3 วิธีจ่าย | `โอนธนาคาร`(bank fee + บัญชี) · `เงินสด`(fee 0) · `เช็ค`(fee 0 + `เลขที่เช็ค*` required → `กรุณากรอกเลขที่เช็ค`) |
| หัวใจ 3 — Confirm + auto-switch | `ยืนยันการจ่ายงวดที่ n` → green alert `ยืนยันการจ่าย{งวด}แล้ว` + toast `✓ ยืนยันการจ่าย{งวด}สำเร็จ` + auto ไป tab ถัดไป → `ยืนยันทำจ่ายทั้งหมด` → `✓ ทำจ่ายทั้งหมดสำเร็จ` |
| หัวใจ 4 — Sync CCS | เดี่ยว (`ดึงค่า CCS (ยืนยัน)` → `ดึงค่า CCS สำเร็จ (CCS: 11.2)`) + Sync All (`ยืนยันและเริ่ม` → ทั้งหมด/สำเร็จ/ล้มเหลว + `ดึงค่า CCS ทั้งหมดเสร็จสิ้น`) |
| หัวใจ 5 — Detail 5 tabs | `สรุป` / `งวด 1` / `งวด 2` / `โปรโมชัน` / `Timeline` + พิมพ์บิลงวด/โปร + `ออกใบเสร็จการจ่ายเงินอ้อยรวม` (enabled เฉพาะ completed) |
| หมายเหตุ mock | prototype in-memory: refresh (F5) = reset seed 5 รายการ — ใช้เป็นข้อดี: ทุกเคส independent โดย refresh ก่อนเริ่ม |
| Cross-module ⭐ | อ่าน config **Payment Setting (F-AGM-012)** · net_tons+cane_type **Receiving (F-AGM-011)** · CCS **legacy** · หัก **Debt (F-AGM-008)** · bank province **Quota** = `(ต้อง simulate)` |

**Seed 5 รายการ (in-memory · refresh = reset):**

| id | เกษตรกร / เลขที่ชั่ง | ประเภทอ้อย | งวด 1 | งวด 2 | โปรโมชั่น | CCS | จำนวนตัน | ยอดสุทธิรวม | สถานะ |
|---|---|---|---|---|---|---|---|---|---|
| CPAY-2025-00004 | นายวิชัย สุขสันต์ / TK-2025-00015 | อ้อยสด | บิลเขียว | - | ไม่มีโปร | รอผล | 12.50 | ฿0.00 | รอดึงค่าความหวาน |
| CPAY-2025-00005 | นางสาวมาลี ดอกไม้ / TK-2025-00016 | อ้อยไฟไหม้ | บิลขาว | บิลขาว | รอจ่ายโปร | รอผล | 18.20 | ฿0.00 | รอดึงค่าความหวาน |
| CPAY-2025-00001 | นายสมชาย ใจดี / TK-2025-00001 | อ้อยสด | บิลเขียว | บิลขาว | รอจ่ายโปร | 11.2 | 10.50 | ฿10,315.00 | รอทำจ่าย |
| CPAY-2025-00002 | นางสมหญิง รักสามัคคี / TK-2025-00002 | อ้อยตอ | บิลเขียว | บิลเขียว | ไม่มีโปร | 10.8 | 15.30 | ฿15,000.00 | รอทำจ่าย |
| CPAY-2025-00003 | นายประเสริฐ มั่งมี / TK-2025-00003 | อ้อยสด | บิลขาว | บิลขาว | จ่ายแล้ว | 12.1 | 20.00 | ฿20,600.00 | เสร็จสิ้น |

> CPAY-2025-00002 = `pending_inst2` (งวด 1 จ่ายแล้ว) → `ทำจ่าย` เปิด modal auto ไป tab งวดที่ 2. CPAY-2025-00004/00005 = `waiting_ccs` → action = `Sync CCS` (ไม่มี `ทำจ่าย`).

- **Top tab counts:** `รอทำจ่าย` = **4** (00004 · 00005 · 00001 · 00002) · `เสร็จสิ้น` = **1** (00003)
- **Stat cards (นับทั้งระบบ · เท่ากันทุก tab):** `รอดึงค่าความหวาน` = **2** · `รอทำจ่าย` = **2** · `เสร็จสิ้น` = **1** · `ยอดจ่ายรวมวันนี้` value = **20,600.00** (meta `฿20,600.00 (เสร็จสิ้น)`)

**VERBATIM microcopy (Expected anchors — copy เป๊ะจาก prototype):**
- top tabs: `รอทำจ่าย` · `เสร็จสิ้น` (มี count badge)
- page header: title `การทำจ่ายเงินอ้อย` + count `N รายการ` · sub `จัดการการทำจ่ายเงินอ้อยตามสถานะและงวด (WKN)`
- header ปุ่ม: `Export CSV` · `Sync All`
- stat cards: `รอดึงค่าความหวาน` (meta `รอผล CCS จากระบบภายนอก`) · `รอทำจ่าย` (`พร้อมทำจ่ายตามงวด`) · `เสร็จสิ้น` (`ทำจ่ายครบทุกงวดแล้ว`) · `ยอดจ่ายรวมวันนี้` (meta `฿20,600.00 (เสร็จสิ้น)`)
- table columns: `ชาวไร่ / เลขที่ชั่ง` · `ประเภทอ้อย` · `งวด 1` · `งวด 2` · `โปรโมชั่น` · `CCS` · `จำนวนตัน` · `ยอดสุทธิรวม` · `สถานะ` · `การดำเนินการ`
- bill badge: `บิลเขียว (จ่ายตามงวด)` (success) · `บิลขาว (เงินยืมระหว่างงวด)` (muted) · null → `-`
- cane-type pill: `อ้อยสด` · `อ้อยตอ` · `อ้อยไฟไหม้`
- promo cell: `จ่ายแล้ว` (success) · `รอจ่ายโปร` (warning) · `ไม่มีโปร` (muted)
- CCS cell: value (เช่น `11.2`) · `รอผล` (waiting_ccs)
- status pill: `รอดึงค่าความหวาน` (warning) · `รอทำจ่าย` (info) · `เสร็จสิ้น` (success)
- row actions: `Sync CCS` (waiting_ccs) · `ทำจ่าย` (non-completed) · `ดูรายละเอียด` (ทุกแถว)
- filter: search placeholder `ค้นหา (เลขที่ชั่ง/ชื่อเกษตรกร)` · ประเภทอ้อย `ทุกประเภท`/`อ้อยสด`/`อ้อยตอ`/`อ้อยไฟไหม้` · สถานะ `ทุกสถานะ`/`รอดึงค่าความหวาน`/`รอทำจ่าย`/`เสร็จสิ้น` · ปุ่ม `ล้าง`
- Payment modal (900): title `ทำจ่ายเงินอ้อย — {เกษตรกร} ({id})` · sub `{เลขที่ชั่ง} · {ประเภทอ้อย} · {ตัน} ตัน` · tab `งวดที่ 1` / `งวดที่ 2` / `โปรโมชั่น` (disabled แสดง ` (ไม่มี)`)
- step card หัวข้อ: `ขั้นตอนการคำนวณ`
- step 2.1: `ขั้นตอน 2.1` `มูลค่าอ้อย` · `ราคาต่อตัน` `฿1,000.00` · `น้ำหนัก (ตัน)` · `CCS` · `มูลค่าอ้อยรวม`
- step 2.1.5: `ขั้นตอน 2.1.5` `ปรับตามประเภทอ้อย (v4.1)` · `ประเภทอ้อย` `{ชื่อ} ({CODE})` · `ปรับ` `+฿10.00 /ตัน` · `ยอดปรับรวม` · `มูลค่าหลังปรับ`
- step 2.2: `ขั้นตอน 2.2` `แบ่งงวด` · `สัดส่วนงวดนี้` `50%` · `ยอดตั้งต้นงวด (base)`
- step 2.3: `ขั้นตอน 2.3` `ภาษี` · `VAT (7%)` `฿735.00` · `หัก ณ ที่จ่าย (3%)` `฿315.00` · `กองทุนส่งเสริม` `฿50.00` · `รวมภาษี` `฿1,100.00` · `ยอดหลังภาษี`
- step 2.4: `ขั้นตอน 2.4` `รายการหักเพิ่มเติม` · ตาราง `รหัส`/`รายละเอียด`/`ประเภท`/`จำนวน` · `CFG-01` `ค่าน้ำมัน` `FLAT` `฿200.00` · `CFG-02` `ค่าธรรมเนียม` `FLAT` `฿100.00` · manual: `รายละเอียด`(placeholder `เช่น ค่าปรับ`) / `จำนวนเงิน`(placeholder `0.00`) / `ประเภท` `FLAT`/`PER_TON` / ปุ่ม `เพิ่มรายการ` · `รวมรายการหัก` · `ยอดก่อนหักหนี้`
- step 2.5: `ขั้นตอน 2.5` `หักหนี้` · `ยอดหนี้คงเหลือ` `฿100,000.00` · `เป้าหมาย (90%)` `฿4,000.00` · `หักจริง` `฿4,000.00` · `คงเหลือ` `฿96,000.00` · `ยอดหลังหักหนี้`
- step 2.6: `ขั้นตอน 2.6` `ดอกเบี้ย (บิลขาว)` · บิลขาว → `วันจ่ายปกติ` `15/01/2568` / `วันจ่ายจริง` `16/12/2567` / `จำนวนวันล่วงหน้า` `30` / `อัตราต่อวัน` `0.019180%` / `ดอกเบี้ย` `฿120.00` / `ยอดหลังดอกเบี้ย` · บิลเขียว → `ไม่คิดดอกเบี้ย`
- step 2.7: `ขั้นตอน 2.7` `ค่าธนาคาร` · TRANSFER → `วิธีจ่าย` `โอนธนาคาร (TRANSFER)` / `จังหวัดโรงงาน` `เชียงใหม่` / `จังหวัดสาขาธนาคาร` / `ประเภท` `ในจังหวัด (IN_PROVINCE)` / `ค่าธนาคาร` `฿10.00` · CASH/CHEQUE → `วิธีจ่าย` `เงินสด (CASH)`/`เช็ค (CHEQUE)` + `ค่าธนาคาร` `฿0.00`
- final: `ยอดสุทธิ`
- method: `วิธีจ่าย` · `โอนธนาคาร` (sub `ระบบจะหักค่าธนาคาร ฿10.00`) · `เงินสด` (sub `ไม่มีค่าธนาคาร — แนบหลักฐานได้ (optional)`) · `เช็ค` (sub `กรอกเลขที่เช็ค (บังคับ) แนบรูปเช็คได้ (optional)`) · `เลขที่เช็ค` * (placeholder `CHK-000123`)
- bank block (TRANSFER): `บัญชีธนาคาร` · `ชื่อบัญชี` · `ธนาคาร` `ธนาคารกรุงเทพ` · `เลขบัญชี` `001-234-5678` · `จังหวัดสาขา`
- notes: `หมายเหตุ (ถ้ามี)` (placeholder `เช่น จ่ายผ่านตัวแทน, หมายเหตุพิเศษ`)
- confirm: `ยืนยันการจ่ายงวดที่ 1` · `ยืนยันการจ่ายงวดที่ 2` · `ยืนยันการจ่ายโปรโมชั่น` · readonly alert `ยืนยันการจ่ายงวดที่ 1แล้ว` · toast `✓ ยืนยันการจ่ายงวดที่ 1สำเร็จ`
- summary: `สรุปยอดรวมทั้งหมด` · `งวดที่ 1`/`งวดที่ 2`/`โปรโมชั่น` · `รวมทั้งหมด` · warn `กรุณายืนยันการจ่ายทุกงวดก่อนกดยืนยันทั้งหมด` · ปุ่ม `ยืนยันทำจ่ายทั้งหมด` · toast `✓ ทำจ่ายทั้งหมดสำเร็จ` (desc `สถานะเปลี่ยนเป็น เสร็จสิ้น`)
- detail drawer (720): eyebrow `การทำจ่ายเงินอ้อย · {id}` · tabs `สรุป`/`งวด 1`/`งวด 2`/`โปรโมชัน`/`Timeline` · sections `ข้อมูลพื้นฐาน`(เลขที่ชั่ง/วันรับอ้อย/ประเภทอ้อย/จำนวนตัน (net)/CCS/สถานะ) / `ประเภทบิล` / `สรุปยอดตามงวด`(งวด 1/งวด 2/โปรโมชัน/ยอดสุทธิรวม + `จ่ายแล้ว`/`ยังไม่จ่าย`) / `บัญชีธนาคาร` · ปุ่ม `ออกใบเสร็จการจ่ายเงินอ้อยรวม` · งวด → `พิมพ์บิลงวด 1`/`พิมพ์บิลงวด 2` · โปร → `พิมพ์บิลโปรโมชัน` · footer `ทำจ่าย`/`ปิด`
- drawer note: `ยังไม่มีค่า CCS — ไม่สามารถคำนวณยอดได้` · `รายการนี้ไม่มีงวด 2` · `รายการนี้ไม่มีโปรโมชัน`
- Sync CCS modal (480): title `ดึงค่าความหวาน (CCS)` · note `ดึงค่า CCS จากระบบภายนอกสำหรับรายการนี้?` · `Scale Ticket` / `Unload Date` · ปุ่ม `ยกเลิก` / `ดึงค่า CCS (ยืนยัน)` · toast `ดึงค่า CCS สำเร็จ (CCS: 11.2)`
- Sync All modal (640): title `Sync All — ดึงค่าความหวานทั้งหมด` · sub `ดึงค่า CCS จากระบบภายนอกสำหรับรายการที่รอผล` · note `พบรายการรอดึงค่าความหวาน 2 รายการ — ต้องการดึงค่า CCS ทั้งหมดจากระบบภายนอกหรือไม่?` · ปุ่ม `ยกเลิก` / `ยืนยันและเริ่ม` · summary chips `ทั้งหมด`/`สำเร็จ`/`ล้มเหลว` · note `ทั้งหมด 2 · สำเร็จ 2 · ล้มเหลว 0` · toast `ดึงค่า CCS ทั้งหมดเสร็จสิ้น` (desc `สำเร็จ 2 รายการ`)
- toast อื่น: `กำลังส่งออกข้อมูล...` → `ส่งออกข้อมูลสำเร็จ` · `กำลังส่งบิล{which}ไปยังเครื่องพิมพ์...` · `กรุณากรอกรายละเอียด` · `กรุณากรอกจำนวนเงินให้ถูกต้อง` · `กรุณากรอกเลขที่เช็ค` · `ไม่พบรายการ`
- empty: filtered `ไม่พบรายการที่ค้นหา` (desc `ลองปรับคำค้นหรือล้างตัวกรอง` + ปุ่ม `ล้าง`) · no-data `ไม่มีรายการ` (desc `ยังไม่มีรายการในแท็บนี้`)
- footer: `แสดง X-Y จาก Z รายการ`
- simulate: CCS legacy API · Debt service + 424 · BE recalc/optimistic 412 · idempotency · RBAC role อื่น · PDF render · WHITE/GREEN block VR-01 · cane-type adj RATOON/BURN + VR-12 · UNKNOWN province warning · config จริง F-AGM-012

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| LIST — List / 2 tabs / stats / columns / rows | TC-LIST01..06 (6) | สูงสุด |
| FLT — Search / filter / export / empty / pagination | TC-FLT01..06 (6) | สูงสุด |
| SYNC — Sync CCS เดี่ยว + Sync All | TC-SYNC01..05 (5) | สูงสุด |
| PAY — Payment modal tabs + navigation | TC-PAY01..05 (5) | สูงสุด |
| CALC — Step calc รายขั้น (2.1–2.7 + ยอดสุทธิ) ⭐ | TC-CALC01..12 (12) | สูงสุด |
| MTD — วิธีจ่าย + cheque validation | TC-MTD01..05 (5) | สูงสุด |
| CFM — Confirm + auto-switch + finalize ⭐ | TC-CFM01..05 (5) | สูงสุด |
| DTL — Detail drawer 5 tabs + print/receipt | TC-DTL01..07 (7) | สูง |
| XT — Cross-module / SIT | TC-XT01..07 (7) | สูงสุด |

---

## Coverage Ledger

### Stories/AC (06_TESTS §6.1)
| AC | รายละเอียด (ย่อ) | cases |
|---|---|---|
| AC-01 | 2 top tab (รอทำจ่าย/เสร็จสิ้น) + count + 4 stats (3 tab เต็ม = SIT) | TC-LIST01, TC-LIST02, TC-LIST06 |
| AC-02 | columns: เกษตรกร/ประเภทอ้อย/บิล 1-2/promo/CCS/สถานะ | TC-LIST03, TC-LIST04, TC-LIST05 |
| AC-03 | ค้นหา (เลขที่ชั่ง/เกษตรกร) + filter ประเภทอ้อย + สถานะ (season/date/checkin = SIT) | TC-FLT01, TC-FLT02, TC-FLT03, TC-FLT04 |
| AC-04 | Export CSV → toast (ไฟล์ `cane_payments_{tab}_{YYYYMMDD}.csv` = SIT) | TC-FLT06 |
| AC-05 | Sync CCS เดี่ยว (waiting_ccs) → ccs set + pending | TC-SYNC01, TC-SYNC02 |
| AC-06 | Sync CCS ซ้ำ → 409 `รายการนี้ได้ทำการดึงค่า CCS แล้ว` | TC-SYNC05, TC-XT03 (SIT) |
| AC-07 | Sync All → summary {total/success/failed} · ไม่มี waiting → block | TC-SYNC03, TC-SYNC04 |
| AC-08 | Payment modal 3 tabs (โปร แสดงเฉพาะมีโปร) | TC-PAY01, TC-PAY02 |
| AC-09 | step calc 7 ขั้น | TC-CALC01..12 |
| AC-10 | มูลค่าอ้อย + แบ่งงวด | TC-CALC01, TC-CALC03 |
| AC-11 | ปรับประเภทอ้อย ก่อนแบ่งงวด (RATOON/BURN = SIT) | TC-CALC02, TC-XT07 |
| AC-12 | cane_type ไม่พบ → adj 0 + `⚠️ ไม่มีข้อมูลประเภทอ้อย` | TC-XT07 (SIT) |
| AC-13 | VAT | TC-CALC04 |
| AC-14 | charge FLAT | TC-CALC05, TC-CALC06 |
| AC-15 | charge PER_TON | TC-CALC07 |
| AC-16 | หักหนี้ min(desired, outstanding) | TC-CALC08 |
| AC-17 | ดอกเบี้ยบิลขาว | TC-CALC09 |
| AC-18 | days_early 0 / บิลเขียว → `ไม่คิดดอกเบี้ย` | TC-CALC10 |
| AC-19 | ค่าธนาคาร in/out/unknown (unknown = SIT) | TC-CALC11, TC-XT05 |
| AC-20 | ยอดสุทธิ = max(0, …) clamp | TC-CALC12 |
| AC-21 | Case A GREEN/GREEN ดอกเบี้ย 0 ทั้ง 2 งวด | TC-CALC10 (CPAY-00002) |
| AC-22 | Case B GREEN/WHITE งวด 2 มีดอกเบี้ย | TC-CALC09 (CPAY-00001) |
| AC-23 | Case C WHITE/WHITE | TC-DTL01 (CPAY-00005) |
| AC-24 | WHITE/GREEN block VR-01 | TC-XT06 (SIT) |
| AC-25 | 3 วิธีจ่าย (โอน/เงินสด/เช็ค) | TC-MTD01, TC-MTD02, TC-MTD03 |
| AC-26 | ยืนยันงวด 1 → auto งวด 2 → ยืนยันทั้งหมด | TC-CFM01, TC-CFM02, TC-CFM05 |
| AC-27 | บิลโปรโมชัน (ไม่ CCS/ไม่หักหนี้/แยกใบ) | TC-CALC02, TC-DTL05, TC-CFM03 |
| AC-28 | Drawer 5 tabs + breakdown | TC-DTL01..06 |
| AC-29 | พิมพ์บิลงวด/โปร/ใบเสร็จรวม (completed) | TC-DTL03, TC-DTL05, TC-DTL07 |
| AC-30..32 | RBAC / optimistic / due / bank missing / 424 | TC-XT04, TC-XT06 (SIT) |

### Cross-Module / Event (06_TESTS §6.2)
| XT | Scenario | cases |
|---|---|---|
| XT-01 | อ่าน active setting (K/base/interest/bankFee/schedule/VAT/charges/cane type/province) | TC-XT01 (SIT) |
| XT-02 | net_tons + cane_type จาก Receiving | TC-XT02 (SIT) |
| XT-03 | ccs_value จาก Legacy CCS API | TC-XT03 (SIT) |
| XT-04 | debt deduct + 424 retry | TC-XT04 (SIT) |
| XT-05 | bank_branch_province in/out/unknown | TC-CALC11, TC-XT05 (SIT) |
| XT-06 | events ccs.synced / installment.paid / completed | TC-DTL06, TC-CFM05 |

### Business Rules (05_RULES §5.1)
| BR | cases |
|---|---|
| BR-01/02 price + cane_total | TC-CALC01 |
| BR-03 cane_type adj ก่อนแบ่งงวด (RATOON/BURN = SIT) | TC-CALC02, TC-XT07 |
| BR-04 split 50/50 | TC-CALC03 |
| BR-05 pipeline 7 ขั้นตายตัว | TC-CALC01..12 |
| BR-06 VAT | TC-CALC04 |
| BR-07 charge FLAT/PER_TON | TC-CALC05, TC-CALC07 |
| BR-08 debt (โปรไม่หักหนี้) | TC-CALC08, TC-CALC02 |
| BR-09 interest บิลขาว / เขียว 0 | TC-CALC09, TC-CALC10 |
| BR-10 bank fee โอน in/out · เงินสด/เช็ค 0 | TC-CALC11, TC-MTD02 |
| BR-11 final = max(0, …) | TC-CALC12 |
| BR-12 bill cases + ห้าม WHITE/GREEN | TC-CALC09, TC-XT06 |
| BR-13 promotion | TC-CALC02, TC-DTL05 |
| BR-14 สูงสุด 3 บิล + ใบเสร็จรวม | TC-DTL07 |
| BR-15 Sync CCS เดี่ยว+bulk | TC-SYNC01, TC-SYNC03 |
| BR-16 Debt 424 retry | TC-XT04 (SIT) |
| BR-17 snapshot ณ confirm | TC-XT01 (SIT) |
| BR-18 Idempotency + If-Match | TC-XT04 (SIT) |
| BR-19 Export CSV filename | TC-FLT06 (SIT) |

### Validation (05_RULES §5.4)
| VR | Message | cases |
|---|---|---|
| VR-01 | `ไม่อนุญาตให้งวด 1 เป็นบิลขาว (เงินยืมระหว่างงวด) และงวด 2 เป็นบิลเขียว จ่ายตามงวด` | TC-XT06 (SIT) |
| VR-03 | `ยังไม่ถึงวันที่กำหนดชำระ` | TC-XT06 (SIT) |
| VR-04 | `บัญชีธนาคารสำหรับรายการนี้ยังไม่ระบุ` | TC-XT06 (SIT) |
| VR-05 | CHEQUE ต้องมีเลขเช็ค → `กรุณากรอกเลขที่เช็ค` | TC-MTD04 |
| VR-06 | amount_final ≥ 0 clamp | TC-CALC12 |
| VR-09 | `รายการนี้ได้ทำการดึงค่า CCS แล้ว` (409) | TC-SYNC05 (SIT) |
| VR-10 | Sync All ต้องมี ≥1 waiting_ccs | TC-SYNC04 |
| VR-12 | `⚠️ ไม่มีข้อมูลประเภทอ้อย` | TC-XT07 (SIT) |
| VR-13 | `⚠️ ไม่มีข้อมูลจังหวัดสาขาธนาคาร - ใช้อัตราต่างจังหวัดเป็น default` | TC-XT05 (SIT) |

### Edge Cases (05_RULES §5.5)
| EC | Case | cases |
|---|---|---|
| EC-01 | WHITE/GREEN block | TC-XT06 (SIT) |
| EC-02 | cane_type not found → adj 0 + warn | TC-XT07 (SIT) |
| EC-03 | ไม่มี branch province → UNKNOWN + out + warn | TC-XT05 (SIT) |
| EC-04 | days_early 0 → `ไม่คิดดอกเบี้ย` | TC-CALC10 |
| EC-05 | GREEN → ไม่มีดอกเบี้ย | TC-CALC10 |
| EC-06 | after_interest − bank_fee < 0 → final 0 | TC-CALC12 |
| EC-07 | pay ก่อน due → 422 | TC-XT06 (SIT) |
| EC-08 | Quota+โอน ไม่มี bank → 422 | TC-XT06 (SIT) |
| EC-09 | stale ETag → 412/409 | TC-XT06 (SIT) |
| EC-10 | Sync CCS ซ้ำ → 409 | TC-SYNC05 (SIT) |
| EC-11 | เงินสด/เช็ค → fee 0 | TC-MTD02, TC-MTD05 |
| EC-12 | promotion แยกใบ + ไม่หักหนี้ | TC-CALC02, TC-DTL05 |
| EC-13 | Debt API fail 424 | TC-XT04 (SIT) |
| EC-14 | AA (inst2=null) pending → completed | TC-PAY02, TC-SYNC01 |

### State Machine (05_RULES §5.2)
| entity | ข้อยืนยัน (ย่อ) | cases |
|---|---|---|
| Payment | waiting_ccs → pending → (pay) → completed | TC-SYNC01, TC-CFM05 |
| Installment | pending → paid (per งวด) | TC-CFM01, TC-CFM02 |

**Manifest cross-check (FRD §0.12):** AC-01..32 32/32 · XT-01..06 6/6 · BR-01..19 19/19 · VR (observable+SIT) 9/9 · EC-01..14 14/14 → ทุกแถว manifest มีคู่ใน Ledger ✅

---

## Data Sets

### ชุด A — งวด GREEN (CPAY-2025-00001 · งวดที่ 1 · อ้อยสด · net 10.50 · CCS 11.2)
| ขั้น | anchor | ค่าที่คาด (verbatim) |
|---|---|---|
| 2.1 | ราคาต่อตัน / น้ำหนัก / CCS / มูลค่าอ้อยรวม | `฿1,000.00` / `10.50` / `11.20` / `฿10,500.00` |
| 2.1.5 | ประเภทอ้อย / ปรับ / ยอดปรับรวม / มูลค่าหลังปรับ | `อ้อยสด (FRESH)` / `+฿10.00 /ตัน` / `+฿105.00` / `฿10,605.00` |
| 2.2 | สัดส่วนงวดนี้ / ยอดตั้งต้นงวด (base) | `50%` / `฿5,000.00` |
| 2.3 | VAT / WHT / กองทุน / รวมภาษี / ยอดหลังภาษี | `฿735.00` / `฿315.00` / `฿50.00` / `฿1,100.00` / `฿3,900.00` |
| 2.4 | CFG-01 / CFG-02 / รวมรายการหัก / ยอดก่อนหักหนี้ | `฿200.00` / `฿100.00` / `฿300.00` / `฿3,600.00` |
| 2.5 | ยอดหนี้คงเหลือ / เป้าหมาย (90%) / หักจริง / คงเหลือ / ยอดหลังหักหนี้ | `฿100,000.00` / `฿4,000.00` / `฿4,000.00` / `฿96,000.00` / `฿-400.00` |
| 2.6 | GREEN → | `ไม่คิดดอกเบี้ย` |
| 2.7 | จังหวัดโรงงาน / สาขา / ประเภท / ค่าธนาคาร (TRANSFER) | `เชียงใหม่` / `เชียงใหม่` / `ในจังหวัด (IN_PROVINCE)` / `฿10.00` |
| final | ยอดสุทธิ | `฿0.00` (clamp) |

### ชุด B — งวด WHITE + ดอกเบี้ย (CPAY-2025-00001 · งวดที่ 2 · บิลขาว)
| ขั้น | anchor | ค่าที่คาด |
|---|---|---|
| 2.6 | วันจ่ายปกติ / วันจ่ายจริง / จำนวนวันล่วงหน้า / อัตราต่อวัน / ดอกเบี้ย / ยอดหลังดอกเบี้ย | `15/01/2568` / `16/12/2567` / `30` / `0.019180%` / `฿120.00` / `฿-520.00` |
| final | ยอดสุทธิ | `฿0.00` |

### ชุด C — งวด GREEN ยอดบวก (CPAY-2025-00002 · งวดที่ 2 · อ้อยตอ · net 15.30 · base 7,500)
| ขั้น | anchor | ค่าที่คาด |
|---|---|---|
| 2.1 / 2.1.5 | มูลค่าอ้อยรวม / ยอดปรับรวม / มูลค่าหลังปรับ | `฿15,300.00` / `+฿153.00` / `฿15,453.00` |
| 2.2 | ยอดตั้งต้นงวด (base) | `฿7,500.00` |
| 2.3 / 2.4 / 2.5 | ยอดหลังภาษี / ยอดก่อนหักหนี้ / ยอดหลังหักหนี้ | `฿6,400.00` / `฿6,100.00` / `฿2,100.00` |
| 2.7 / final | ค่าธนาคาร (TRANSFER) / ยอดสุทธิ | `฿10.00` / `฿2,090.00` |

### ชุด D — โปรโมชัน (CPAY-2025-00001 · promo base 315 · อัตรา ฿30/ตัน · net 10.50)
| anchor | ค่าที่คาด |
|---|---|
| อัตราโปรโมชันต่อตัน / น้ำหนักสุทธิ (ตัน) / ยอดโปรโมชันรวม (base) | `฿30.00 /ตัน` / `10.50` / `฿315.00` |
| หักหนี้ | `โปรโมชันไม่หักหนี้` |
| รายการหัก | `ไม่มีรายการหัก (โปรโมชันไม่มีค่าใช้จ่ายจากระบบ)` |
| ดอกเบี้ย | `ไม่คิดดอกเบี้ย` |
| ค่าธนาคาร (TRANSFER · สาขา เชียงราย OUT) / ยอดสุทธิ | `฿20.00` / `฿295.00` |

### ชุด E — Sync CCS
| รายการ | ผลหลัง Sync (CCS 11.2) |
|---|---|
| CPAY-2025-00004 (ไม่มีงวด 2) | inst1 = ฿12,500.00 · ยอดสุทธิรวม ฿12,500.00 · สถานะ รอทำจ่าย |
| CPAY-2025-00005 (WHITE/WHITE + promo) | inst1 ฿9,100.00 · inst2 ฿9,100.00 · promo ฿546.00 · รวม ฿18,746.00 |

---

## Test Cases

## Group LIST — List / 2 tabs / stats / columns / rows (US-01)

### TC-LIST01 — เปิดหน้า tab รอทำจ่าย (default) + top tabs + header (happy — AC-01)
- group: LIST · ความสำคัญ: สูงสุด · trace: AC-01 / route default
- Setup: seed=default (refresh) · files=—
- Start: OPEN `#/payments`
- ผ่านเมื่อ: top tabs + header + sub ตรง seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/payments` | — | top tab **รอทำจ่าย** (active · count **4**) · **เสร็จสิ้น** (count **1**) | ☐ |
| 2 | VERIFY page header | — | title **การทำจ่ายเงินอ้อย** + count **4 รายการ** · sub **จัดการการทำจ่ายเงินอ้อยตามสถานะและงวด (WKN)** | ☐ |
| 3 | VERIFY ปุ่ม header | — | **Export CSV** (outline) · **Sync All** (primary) | ☐ |
| 4 | VERIFY footer | — | **แสดง 1-4 จาก 4 รายการ** · หน้า **1** active | ☐ |

### TC-LIST02 — 4 stat cards นับทั้งระบบ (AC-01)
- group: LIST · ความสำคัญ: สูงสุด · trace: AC-01 / stats
- Setup: seed=default · files=—
- Start: OPEN `#/payments`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY การ์ด 1 | — | **รอดึงค่าความหวาน** = **2** (meta **รอผล CCS จากระบบภายนอก**) | ☐ |
| 2 | VERIFY การ์ด 2 | — | **รอทำจ่าย** = **2** (meta **พร้อมทำจ่ายตามงวด**) | ☐ |
| 3 | VERIFY การ์ด 3 | — | **เสร็จสิ้น** = **1** (meta **ทำจ่ายครบทุกงวดแล้ว**) | ☐ |
| 4 | VERIFY การ์ด 4 | — | **ยอดจ่ายรวมวันนี้** value = **20,600.00** · meta **฿20,600.00 (เสร็จสิ้น)** (หมายเหตุ: ตัวเลขใหญ่ไม่มีสัญลักษณ์ ฿ · ฿ อยู่ใน meta) | ☐ |

### TC-LIST03 — หัวคอลัมน์ + แถว CPAY-2025-00001 (AC-02)
- group: LIST · ความสำคัญ: สูงสุด · trace: AC-02 / columns
- Setup: seed=default · files=—
- Start: OPEN `#/payments`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัวคอลัมน์ (เรียง) | — | **ชาวไร่ / เลขที่ชั่ง · ประเภทอ้อย · งวด 1 · งวด 2 · โปรโมชั่น · CCS · จำนวนตัน · ยอดสุทธิรวม · สถานะ · การดำเนินการ** | ☐ |
| 2 | VERIFY แถว CPAY-2025-00001 | — | ชาวไร่ **นายสมชาย ใจดี** (ใต้ = **TK-2025-00001**) · ประเภทอ้อย **อ้อยสด** · งวด 1 **บิลเขียว (จ่ายตามงวด)** · งวด 2 **บิลขาว (เงินยืมระหว่างงวด)** · โปรโมชั่น **รอจ่ายโปร** · CCS **11.2** · จำนวนตัน **10.50** · ยอดสุทธิรวม **฿10,315.00** · สถานะ **รอทำจ่าย** | ☐ |

### TC-LIST04 — bill badge / promo cell / CCS cell ครบทุก state (AC-02)
- group: LIST · ความสำคัญ: สูงสุด · trace: AC-02 / badge states
- Setup: seed=default · files=—
- Start: OPEN `#/payments`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY งวด 2 = null (CPAY-2025-00004) | — | คอลัมน์ งวด 2 = **-** (ไม่มีบิลงวด 2) | ☐ |
| 2 | VERIFY CCS cell waiting (CPAY-2025-00004/00005) | — | CCS = pill **รอผล** (warning) | ☐ |
| 3 | VERIFY promo cell | — | CPAY-2025-00001/00005 = **รอจ่ายโปร** (warning) · CPAY-2025-00002 = **ไม่มีโปร** (muted) · (เสร็จสิ้น tab) CPAY-2025-00003 = **จ่ายแล้ว** (success) | ☐ |
| 4 | VERIFY bill badge (CPAY-2025-00005) | — | งวด 1 **บิลขาว (เงินยืมระหว่างงวด)** · งวด 2 **บิลขาว (เงินยืมระหว่างงวด)** · ประเภทอ้อย **อ้อยไฟไหม้** | ☐ |

### TC-LIST05 — status pill + row actions ตามสถานะ (AC-02)
- group: LIST · ความสำคัญ: สูงสุด · trace: AC-02 / state-driven action
- Setup: seed=default · files=—
- Start: OPEN `#/payments`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถว waiting_ccs (CPAY-2025-00004) | — | สถานะ pill **รอดึงค่าความหวาน** (warning) · action = **Sync CCS** + **ดูรายละเอียด** (ไม่มี **ทำจ่าย**) | ☐ |
| 2 | VERIFY แถว pending (CPAY-2025-00001) | — | สถานะ pill **รอทำจ่าย** (info) · action = **ทำจ่าย** + **ดูรายละเอียด** (ไม่มี Sync CCS) | ☐ |
| 3 | VERIFY แถว pending_inst2 (CPAY-2025-00002) | — | สถานะ pill **รอทำจ่าย** · action = **ทำจ่าย** + **ดูรายละเอียด** | ☐ |

### TC-LIST06 — สลับ tab เสร็จสิ้น (#/payments/completed) + CPAY-2025-00003 (AC-01)
- group: LIST · ความสำคัญ: สูง · trace: AC-01 / tab route
- Setup: seed=default · files=—
- Start: OPEN `#/payments`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK top tab **เสร็จสิ้น** | — | URL = **#/payments/completed** · title **การทำจ่ายเงินอ้อย** + count **1 รายการ** · footer **แสดง 1-1 จาก 1 รายการ** | ☐ |
| 2 | VERIFY แถว CPAY-2025-00003 | — | **นายประเสริฐ มั่งมี** (TK-2025-00003) · ประเภทอ้อย **อ้อยสด** · โปรโมชั่น **จ่ายแล้ว** · CCS **12.1** · ยอดสุทธิรวม **฿20,600.00** · สถานะ **เสร็จสิ้น** · action = **ดูรายละเอียด** เท่านั้น | ☐ |
| 3 | CLICK top tab **รอทำจ่าย** | — | URL = **#/payments** · count **4 รายการ** | ☐ |

---

## Group FLT — Search / filter / export / empty / pagination (US-01)

### TC-FLT01 — ค้นหา (เลขที่ชั่ง / ชื่อเกษตรกร / id) (AC-03)
- group: FLT · ความสำคัญ: สูงสุด · trace: AC-03 / search (debounce 300ms)
- Setup: seed=default · files=—
- Start: OPEN `#/payments`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `TK-2025-00001` → ช่องค้นหา (placeholder **ค้นหา (เลขที่ชั่ง/ชื่อเกษตรกร)**) → WAIT | — | เหลือ 1 แถว **นายสมชาย ใจดี** (CPAY-2025-00001) | ☐ |
| 2 | CLICK **ล้าง** → TYPE `มาลี` → WAIT | — | เหลือ 1 แถว **นางสาวมาลี ดอกไม้** (CPAY-2025-00005) | ☐ |
| 3 | CLICK **ล้าง** → TYPE `CPAY-2025-00002` → WAIT | — | เหลือ 1 แถว **นางสมหญิง รักสามัคคี** | ☐ |

### TC-FLT02 — filter ประเภทอ้อย (AC-03)
- group: FLT · ความสำคัญ: สูง · trace: AC-03 / cane-type filter
- Setup: seed=default · files=—
- Start: OPEN `#/payments`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ประเภทอ้อย = **อ้อยสด** | — | เหลือ 2 แถว (CPAY-2025-00004 + CPAY-2025-00001 · tab รอทำจ่าย) | ☐ |
| 2 | SELECT ประเภทอ้อย = **อ้อยไฟไหม้** | — | เหลือ 1 แถว CPAY-2025-00005 | ☐ |
| 3 | SELECT ประเภทอ้อย = **อ้อยตอ** | — | เหลือ 1 แถว CPAY-2025-00002 | ☐ |

### TC-FLT03 — filter สถานะ (รวม รอดึงค่าความหวาน) (AC-03)
- group: FLT · ความสำคัญ: สูง · trace: AC-03 / status filter
- Setup: seed=default · files=—
- Start: OPEN `#/payments`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT สถานะ = **รอดึงค่าความหวาน** | — | เหลือ 2 แถว (CPAY-2025-00004 + CPAY-2025-00005) | ☐ |
| 2 | SELECT สถานะ = **รอทำจ่าย** | — | เหลือ 2 แถว (CPAY-2025-00001 + CPAY-2025-00002) | ☐ |
| 3 | SELECT สถานะ = **เสร็จสิ้น** (บน tab รอทำจ่าย) | — | ตารางว่าง + empty **ไม่พบรายการที่ค้นหา** (completed ไม่อยู่ใน tab รอทำจ่าย) | ☐ |

### TC-FLT04 — ล้าง reset ตัวกรอง (AC-03)
- group: FLT · ความสำคัญ: กลาง · trace: AC-03 / reset
- Setup: seed=default · files=—
- Start: OPEN `#/payments`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ประเภทอ้อย = **อ้อยตอ** + TYPE `xyz` | — | ตารางว่าง / กรองเหลือน้อย | ☐ |
| 2 | CLICK **ล้าง** | — | กลับ 4 รายการ · ช่องค้นหาว่าง · dropdown = **ทุกประเภท** / **ทุกสถานะ** | ☐ |

### TC-FLT05 — empty state (filtered) (AC-03)
- group: FLT · ความสำคัญ: กลาง · trace: AC-03 / empty variant
- Setup: seed=default · files=—
- Start: OPEN `#/payments`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `ไม่มีรายการนี้แน่นอน` → WAIT | — | ตารางว่าง + empty title **ไม่พบรายการที่ค้นหา** (desc **ลองปรับคำค้นหรือล้างตัวกรอง**) + ปุ่ม **ล้าง** | ☐ |
| 2 | CLICK **ล้าง** (ใน empty) | — | กลับ 4 รายการ | ☐ |
| 3 | VERIFY (no-data variant · SIT): tab ที่ไม่มี record | — | empty title **ไม่มีรายการ** (desc **ยังไม่มีรายการในแท็บนี้**) — prototype ทุก tab มี record เสมอ | ☐ (ต้อง simulate) |

### TC-FLT06 — Export CSV toasts + filename (AC-04) (ไฟล์จริง = SIT)
- group: FLT · ความสำคัญ: กลาง · trace: AC-04 / BR-19 · **prototype: toast จำลอง · ไฟล์ + ชื่อ = SIT**
- Setup: seed=default · files=—
- Start: OPEN `#/payments`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **Export CSV** → WAIT ~1s | — | toast **กำลังส่งออกข้อมูล...** → ตามด้วย toast **ส่งออกข้อมูลสำเร็จ** | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): ไฟล์ CSV | — | ไฟล์ **cane_payments_{tab}_{YYYYMMDD}.csv** ดาวน์โหลด · คอลัมน์ไทยตรงตาราง | ☐ (ต้อง simulate) |

---

## Group SYNC — Sync CCS เดี่ยว + Sync All (US-02)

### TC-SYNC01 — Sync CCS เดี่ยว (CPAY-2025-00004 · ไม่มีงวด 2) (happy — AC-05 / BR-15 / EC-14)
- group: SYNC · ความสำคัญ: สูงสุด · trace: AC-05 / BR-15 / EC-14 (AA)
- Setup: seed=default · files=—
- Start: OPEN `#/payments`
- ผ่านเมื่อ: modal → toast + row ได้ CCS + ย้ายเป็น รอทำจ่าย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **Sync CCS** (แถว CPAY-2025-00004) | — | modal เปิด · title **ดึงค่าความหวาน (CCS)** · sub **นายวิชัย สุขสันต์ · CPAY-2025-00004** · note **ดึงค่า CCS จากระบบภายนอกสำหรับรายการนี้?** · cells **Scale Ticket** `TK-2025-00015` / **Unload Date** `2025-01-10` · ปุ่ม **ยกเลิก** / **ดึงค่า CCS (ยืนยัน)** | ☐ |
| 2 | CLICK **ดึงค่า CCS (ยืนยัน)** | — | modal ปิด · toast **ดึงค่า CCS สำเร็จ (CCS: 11.2)** | ☐ |
| 3 | VERIFY แถว CPAY-2025-00004 | — | CCS = **11.2** · ยอดสุทธิรวม = **฿12,500.00** · สถานะ **รอทำจ่าย** · action เปลี่ยนเป็น **ทำจ่าย** + **ดูรายละเอียด** | ☐ |
| 4 | VERIFY stat + top tab | — | **รอดึงค่าความหวาน** = **1** · **รอทำจ่าย** = **3** · top tab รอทำจ่าย count = **4** (คงเดิม) | ☐ |

### TC-SYNC02 — Sync CCS เดี่ยว (CPAY-2025-00005 · WHITE/WHITE + promo) แบ่งงวด (AC-05 / BR-15)
- group: SYNC · ความสำคัญ: สูง · trace: AC-05 / BR-04/13/15 (split + promo)
- Setup: seed=default · files=—
- Start: OPEN `#/payments`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **Sync CCS** (แถว CPAY-2025-00005) → CLICK **ดึงค่า CCS (ยืนยัน)** | — | toast **ดึงค่า CCS สำเร็จ (CCS: 11.2)** | ☐ |
| 2 | VERIFY แถว CPAY-2025-00005 | — | CCS = **11.2** · ยอดสุทธิรวม = **฿18,746.00** (งวด1 9,100 + งวด2 9,100 + โปร 546) · สถานะ **รอทำจ่าย** | ☐ |

### TC-SYNC03 — Sync All → summary + toast (happy — AC-07 / BR-15)
- group: SYNC · ความสำคัญ: สูงสุด · trace: AC-07 / BR-15 (bulk)
- Setup: seed=default · files=—
- Start: OPEN `#/payments`
- ผ่านเมื่อ: summary 2/2/0 + toast

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **Sync All** (header) | — | modal เปิด · title **Sync All — ดึงค่าความหวานทั้งหมด** · sub **ดึงค่า CCS จากระบบภายนอกสำหรับรายการที่รอผล** · note **พบรายการรอดึงค่าความหวาน 2 รายการ — ต้องการดึงค่า CCS ทั้งหมดจากระบบภายนอกหรือไม่?** · ปุ่ม **ยกเลิก** / **ยืนยันและเริ่ม** | ☐ |
| 2 | CLICK **ยืนยันและเริ่ม** | — | summary chips **ทั้งหมด 2** / **สำเร็จ 2** / **ล้มเหลว 0** · note **ทั้งหมด 2 · สำเร็จ 2 · ล้มเหลว 0** · toast **ดึงค่า CCS ทั้งหมดเสร็จสิ้น** (desc **สำเร็จ 2 รายการ**) · ปุ่ม **ปิด** | ☐ |
| 3 | CLICK **ปิด** → VERIFY list | — | ทั้ง CPAY-2025-00004 + 00005 = สถานะ **รอทำจ่าย** · stat **รอดึงค่าความหวาน** = **0** · **รอทำจ่าย** = **4** | ☐ |

### TC-SYNC04 — Sync All เมื่อไม่มี waiting_ccs → ปุ่ม disabled (VR-10)
- group: SYNC · ความสำคัญ: กลาง · trace: AC-07 / VR-10 (ต้องมี ≥1 waiting)
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → (TC-SYNC03 sync ครบก่อน)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (หลัง sync ครบ) CLICK **Sync All** | — | modal note **พบรายการรอดึงค่าความหวาน 0 รายการ …** · ปุ่ม **ยืนยันและเริ่ม** = **disabled** | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): message VR-10 | — | ระบบจริง → **ไม่มีรายการที่สถานะ waiting_ccs** (prototype ใช้ปุ่ม-disable แทน message) | ☐ (ต้อง simulate) |

### TC-SYNC05 — Sync CCS ซ้ำ (guard) (AC-06 / VR-09 / EC-10)
- group: SYNC · ความสำคัญ: กลาง · trace: AC-06 / VR-09 / EC-10 · **prototype: ปุ่ม Sync CCS หายหลัง sync → 409 = SIT**
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → sync CPAY-2025-00004 แล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถว CPAY-2025-00004 หลัง sync | — | ปุ่ม **Sync CCS** **หายไป** (สถานะ = รอทำจ่าย · action = ทำจ่าย) → ป้องกัน sync ซ้ำที่ระดับ UI | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): sync ซ้ำ | — | ระบบจริง POST ซ้ำ → **409 · รายการนี้ได้ทำการดึงค่า CCS แล้ว** | ☐ (ต้อง simulate) |

---

## Group PAY — Payment modal tabs + navigation (US-03)

### TC-PAY01 — เปิด All-in-One modal จาก ทำจ่าย (CPAY-2025-00001 · 3 tabs) (happy — AC-08)
- group: PAY · ความสำคัญ: สูงสุด · trace: AC-08 / modal open
- Setup: seed=default · files=—
- Start: OPEN `#/payments`
- ผ่านเมื่อ: modal 900 + title + 3 tab + auto-tab งวดที่ 1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ทำจ่าย** (แถว CPAY-2025-00001) | — | modal เปิด · title **ทำจ่ายเงินอ้อย — นายสมชาย ใจดี (CPAY-2025-00001)** · sub **TK-2025-00001 · อ้อยสด · 10.50 ตัน** | ☐ |
| 2 | VERIFY tabs | — | **งวดที่ 1** (active) · **งวดที่ 2** (enabled) · **โปรโมชั่น** (enabled) | ☐ |
| 3 | VERIFY เนื้อหา tab งวดที่ 1 | — | หัวข้อ **งวดที่ 1** + badge **บิลเขียว (จ่ายตามงวด)** · การ์ด **ขั้นตอนการคำนวณ** · บล็อก **วิธีจ่าย** · **สรุปยอดรวมทั้งหมด** ด้านล่าง | ☐ |

### TC-PAY02 — modal CPAY-2025-00004 (AA · งวด 2/โปร disabled "(ไม่มี)") (AC-08 / EC-14)
- group: PAY · ความสำคัญ: สูง · trace: AC-08 / EC-14 (AA no inst2)
- Setup: seed=default · files=— (sync CPAY-2025-00004 ให้เป็น pending ก่อน)
- Start: OPEN `#/payments` → sync CPAY-2025-00004 → CLICK **ทำจ่าย**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY tabs (CPAY-2025-00004) | — | **งวดที่ 1** (active) · **งวดที่ 2 (ไม่มี)** (disabled) · **โปรโมชั่น (ไม่มี)** (disabled) | ☐ |
| 2 | CLICK tab **งวดที่ 2 (ไม่มี)** | — | คลิกไม่ได้ (disabled · ยังอยู่ tab งวดที่ 1) | ☐ |

### TC-PAY03 — modal CPAY-2025-00002 (pending_inst2 → auto-tab งวดที่ 2) (AC-26)
- group: PAY · ความสำคัญ: สูงสุด · trace: AC-26 / auto-tab next unpaid
- Setup: seed=default · files=—
- Start: OPEN `#/payments`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ทำจ่าย** (แถว CPAY-2025-00002) | — | modal เปิด (title **… นางสมหญิง รักสามัคคี (CPAY-2025-00002)**) · auto ไป tab **งวดที่ 2** (active) เพราะงวดที่ 1 จ่ายแล้ว · tab **งวดที่ 1** มีไอคอน check (confirmed) · **โปรโมชั่น (ไม่มี)** disabled | ☐ |
| 2 | CLICK tab **งวดที่ 1** | — | แสดง green alert **ยืนยันการจ่ายงวดที่ 1แล้ว** · การ์ดคำนวณ read-only (ไม่มีปุ่มยืนยัน) | ☐ |

### TC-PAY04 — สลับ tab งวด + step card recalc (AC-08 / AC-09)
- group: PAY · ความสำคัญ: สูง · trace: AC-08, AC-09 / tab switch
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tab **งวดที่ 2** | — | หัวข้อ **งวดที่ 2** + badge **บิลขาว (เงินยืมระหว่างงวด)** · step 2.6 แสดง **ดอกเบี้ย (บิลขาว)** พร้อม **ดอกเบี้ย ฿120.00** | ☐ |
| 2 | CLICK tab **โปรโมชั่น** | — | หัวข้อ **โปรโมชั่น** + pill **โปรโมชัน** · การ์ดแสดงบล็อก **ข้อมูลโปรโมชัน** (ไม่มีขั้น 2.1.5/2.3) · **โปรโมชันไม่หักหนี้** · **ไม่คิดดอกเบี้ย** | ☐ |
| 3 | CLICK tab **งวดที่ 1** | — | กลับ **งวดที่ 1** + badge **บิลเขียว (จ่ายตามงวด)** · step 2.6 = **ไม่คิดดอกเบี้ย** | ☐ |

### TC-PAY05 — ปิด modal โดยไม่ยืนยัน (Esc / x) (AC-08)
- group: PAY · ความสำคัญ: กลาง · trace: AC-08 / dismiss
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | กด **Esc** | — | modal ปิด · list คงเดิม · CPAY-2025-00001 ยัง **รอทำจ่าย** | ☐ |
| 2 | CLICK **ทำจ่าย** อีกครั้ง → CLICK ปุ่ม x (มุมขวาบน modal) | — | modal ปิด · CPAY-2025-00001 ยัง รอทำจ่าย (ไม่มีการเปลี่ยนสถานะ) | ☐ |

---

## Group CALC — Step calc รายขั้น (2.1–2.7 + ยอดสุทธิ) ⭐ (US-03)

> ทุกเคสในกลุ่มนี้ Start: OPEN `#/payments` → CLICK **ทำจ่าย** (ระบุแถว) → เปิด All-in-One modal. ตัวเลข = ชุด A/B/C/D ด้านบน

### TC-CALC01 — ขั้น 2.1 มูลค่าอ้อย (price × net) (AC-10 / BR-01/02)
- group: CALC · ความสำคัญ: สูงสุด · trace: AC-10 / BR-01/02 / FN-PRICE
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001) → tab **งวดที่ 1**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ขั้น 2.1 | — | pill **ขั้นตอน 2.1** + **มูลค่าอ้อย** · **ราคาต่อตัน ฿1,000.00** · **น้ำหนัก (ตัน) 10.50** · **CCS 11.20** · **มูลค่าอ้อยรวม ฿10,500.00** | ☐ |

### TC-CALC02 — ขั้น 2.1.5 ปรับประเภทอ้อย (+฿10/ตัน · ก่อนแบ่งงวด) (AC-11 / BR-03)
- group: CALC · ความสำคัญ: สูงสุด · trace: AC-11 / BR-03 / FN-CANETYPE-ADJ · **RATOON/BURN adj = SIT**
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001) → tab **งวดที่ 1**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ขั้น 2.1.5 | — | pill **ขั้นตอน 2.1.5** + **ปรับตามประเภทอ้อย (v4.1)** · **ประเภทอ้อย อ้อยสด (FRESH)** · **ปรับ +฿10.00 /ตัน** · **ยอดปรับรวม +฿105.00** · **มูลค่าหลังปรับ ฿10,605.00** | ☐ |
| 2 | VERIFY ลำดับ (ก่อนแบ่งงวด) | — | 2.1.5 อยู่ **ก่อน** ขั้น 2.2 แบ่งงวด (adjusted ใช้เป็นฐานของ split) | ☐ |
| 3 | VERIFY (ระบบจริง — SIT): adj ตามประเภท | — | RATOON = **+฿5.00 /ตัน** · BURN = **−฿20.00 /ตัน** (prototype hard-code **+฿10.00 ทุกประเภท** → CPAY-2025-00002 อ้อยตอ ก็แสดง +฿10.00, CPAY-2025-00005 อ้อยไฟไหม้ ก็ +฿10.00) | ☐ (ต้อง simulate) |

### TC-CALC03 — ขั้น 2.2 แบ่งงวด 50% + base (AC-10 / BR-04)
- group: CALC · ความสำคัญ: สูงสุด · trace: AC-10 / BR-04 / split
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001) → tab **งวดที่ 1**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ขั้น 2.2 | — | pill **ขั้นตอน 2.2** + **แบ่งงวด** · **สัดส่วนงวดนี้ 50%** · **ยอดตั้งต้นงวด (base) ฿5,000.00** | ☐ |
| 2 | VERIFY drift (base = seed) | — | base = **฿5,000.00** (ค่า seed) ต่างจาก **มูลค่าหลังปรับ ฿10,605.00 × 50% = ฿5,302.50** — mock inconsistency (AS-BUILT) | ☐ |

### TC-CALC04 — ขั้น 2.3 ภาษี VAT/WHT/กองทุน (AC-13 / BR-06)
- group: CALC · ความสำคัญ: สูงสุด · trace: AC-13 / BR-06 / FN-VAT
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001) → tab **งวดที่ 1**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ขั้น 2.3 | — | pill **ขั้นตอน 2.3** + **ภาษี** · **VAT (7%) ฿735.00** · **หัก ณ ที่จ่าย (3%) ฿315.00** · **กองทุนส่งเสริม ฿50.00** · **รวมภาษี ฿1,100.00** · **ยอดหลังภาษี ฿3,900.00** | ☐ |

### TC-CALC05 — ขั้น 2.4 รายการหัก config FLAT (AC-14 / BR-07)
- group: CALC · ความสำคัญ: สูงสุด · trace: AC-14 / BR-07 / FN-CHARGE (FLAT)
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001) → tab **งวดที่ 1**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตาราง config charge | — | หัว **รหัส / รายละเอียด / ประเภท / จำนวน** · แถว **CFG-01 · ค่าน้ำมัน · FLAT · ฿200.00** · **CFG-02 · ค่าธรรมเนียม · FLAT · ฿100.00** | ☐ |
| 2 | VERIFY รวม | — | **รวมรายการหัก ฿300.00** · **ยอดก่อนหักหนี้ ฿3,600.00** | ☐ |

### TC-CALC06 — ขั้น 2.4 เพิ่มรายการหัก manual FLAT (AC-14 / BR-07)
- group: CALC · ความสำคัญ: สูง · trace: AC-14 / BR-07 / manual FLAT
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001) → tab **งวดที่ 1**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE รายละเอียด `ค่าปรับ` · จำนวนเงิน `100` · ประเภท **FLAT** → CLICK **เพิ่มรายการ** | — | แถวใหม่ **MAN-1 · ค่าปรับ · FLAT · ฿100.00** (มีปุ่มถังขยะ) · **รวมรายการหัก ฿400.00** · **ยอดก่อนหักหนี้ ฿3,500.00** | ☐ |
| 2 | CLICK ปุ่มถังขยะ (ลบ MAN-1) | — | แถว MAN-1 หาย · **รวมรายการหัก ฿300.00** กลับเดิม | ☐ |
| 3 | TYPE รายละเอียดว่าง → CLICK **เพิ่มรายการ** | — | toast **กรุณากรอกรายละเอียด** | ☐ |

### TC-CALC07 — ขั้น 2.4 เพิ่มรายการหัก manual PER_TON (AC-15 / BR-07)
- group: CALC · ความสำคัญ: สูงสุด · trace: AC-15 / BR-07 / manual PER_TON (× net_tons)
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001) → tab **งวดที่ 1**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE รายละเอียด `ค่าขนส่ง` · จำนวนเงิน `100` · ประเภท **PER_TON** → CLICK **เพิ่มรายการ** | — | แถว **MAN-1 · ค่าขนส่ง · PER_TON · ฿1,050.00** (= 100 × 10.50) · **รวมรายการหัก ฿1,350.00** · **ยอดก่อนหักหนี้ ฿2,550.00** | ☐ |
| 2 | TYPE จำนวนเงิน `-5` → CLICK **เพิ่มรายการ** | — | toast **กรุณากรอกจำนวนเงินให้ถูกต้อง** | ☐ |

### TC-CALC08 — ขั้น 2.5 หักหนี้ min(desired, outstanding) (AC-16 / BR-08)
- group: CALC · ความสำคัญ: สูงสุด · trace: AC-16 / BR-08 / FN-DEBT
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001) → tab **งวดที่ 1**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ขั้น 2.5 | — | pill **ขั้นตอน 2.5** + **หักหนี้** · **ยอดหนี้คงเหลือ ฿100,000.00** · **เป้าหมาย (90%) ฿4,000.00** · **หักจริง ฿4,000.00** · **คงเหลือ ฿96,000.00** · **ยอดหลังหักหนี้ ฿-400.00** | ☐ |

### TC-CALC09 — ขั้น 2.6 ดอกเบี้ย บิลขาว (CPAY-2025-00001 งวดที่ 2) (AC-17 / AC-22 / BR-09)
- group: CALC · ความสำคัญ: สูงสุด · trace: AC-17, AC-22 / BR-09 (Case B GREEN/WHITE) / FN-INTEREST
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001) → tab **งวดที่ 2**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ขั้น 2.6 (บิลขาว) | — | pill **ขั้นตอน 2.6** + **ดอกเบี้ย (บิลขาว)** · **วันจ่ายปกติ 15/01/2568** · **วันจ่ายจริง 16/12/2567** · **จำนวนวันล่วงหน้า 30** · **อัตราต่อวัน 0.019180%** · **ดอกเบี้ย ฿120.00** · **ยอดหลังดอกเบี้ย ฿-520.00** | ☐ |
| 2 | VERIFY Case B | — | งวดที่ 1 (GREEN) = ไม่มีดอกเบี้ย · งวดที่ 2 (WHITE) = มีดอกเบี้ย ฿120.00 | ☐ |

### TC-CALC10 — ขั้น 2.6 ไม่คิดดอกเบี้ย บิลเขียว (Case A GREEN/GREEN) (AC-18 / AC-21 / EC-04/05)
- group: CALC · ความสำคัญ: สูงสุด · trace: AC-18, AC-21 / EC-04/05 / BR-09
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00002) → tab **งวดที่ 2**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ขั้น 2.6 (บิลเขียว · CPAY-2025-00002 งวดที่ 2 GREEN) | — | pill **ขั้นตอน 2.6** + **ดอกเบี้ย (บิลขาว)** · เนื้อหา = note **ไม่คิดดอกเบี้ย** (ไม่มีบรรทัดดอกเบี้ย) | ☐ |
| 2 | VERIFY Case A (CPAY-2025-00002 GREEN/GREEN) | — | ทั้งงวดที่ 1 + งวดที่ 2 = **ไม่คิดดอกเบี้ย** | ☐ |

### TC-CALC11 — ขั้น 2.7 ค่าธนาคาร IN_PROVINCE (โอน · สาขา=โรงงาน) (AC-19 / BR-10)
- group: CALC · ความสำคัญ: สูงสุด · trace: AC-19 / BR-10 / FN-BANKFEE (IN)
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001) → tab **งวดที่ 1** (method = โอนธนาคาร default)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ขั้น 2.7 (TRANSFER) | — | pill **ขั้นตอน 2.7** + **ค่าธนาคาร** · **วิธีจ่าย โอนธนาคาร (TRANSFER)** · **จังหวัดโรงงาน เชียงใหม่** · **จังหวัดสาขาธนาคาร เชียงใหม่** · **ประเภท ในจังหวัด (IN_PROVINCE)** · **ค่าธนาคาร ฿10.00** | ☐ |
| 2 | VERIFY โปรโมชัน tab (OUT_PROVINCE) | — | (tab **โปรโมชั่น** · method โอน) → **จังหวัดสาขาธนาคาร เชียงราย** · **ประเภท ต่างจังหวัด (OUT_PROVINCE)** · **ค่าธนาคาร ฿20.00** | ☐ |

### TC-CALC12 — ยอดสุทธิ = max(0, …) clamp + ยอดบวก (AC-20 / EC-06 / BR-11 / VR-06)
- group: CALC · ความสำคัญ: สูงสุด · trace: AC-20 / EC-06 / BR-11 / VR-06 / FN-PIPELINE
- Setup: seed=default · files=—
- Start: OPEN `#/payments`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ทำจ่าย** (CPAY-2025-00001) → tab **งวดที่ 1** → VERIFY ยอดสุทธิ | — | บล็อกเขียว **ยอดสุทธิ ฿0.00** (clamp: −400 − 10 < 0 → 0) | ☐ |
| 2 | ปิด modal → CLICK **ทำจ่าย** (CPAY-2025-00002) → tab **งวดที่ 2** → VERIFY ยอดสุทธิ | — | **ยอดสุทธิ ฿2,090.00** (base 7,500 → 6,400 → 6,100 → 2,100 − ค่าธนาคาร 10) — ยอดบวก ไม่ clamp | ☐ |

---

## Group MTD — วิธีจ่าย + cheque validation (US-03)

### TC-MTD01 — โอนธนาคาร (default) + บัญชี + bank fee (AC-25)
- group: MTD · ความสำคัญ: สูงสุด · trace: AC-25 / TRANSFER
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001) → tab **งวดที่ 1**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY บล็อก วิธีจ่าย | — | หัวข้อ **วิธีจ่าย** · **โอนธนาคาร** (เลือก · sub **ระบบจะหักค่าธนาคาร ฿10.00**) · **เงินสด** · **เช็ค** | ☐ |
| 2 | VERIFY บล็อก บัญชีธนาคาร | — | หัวข้อ **บัญชีธนาคาร** · **ชื่อบัญชี นายสมชาย ใจดี** · **ธนาคาร ธนาคารกรุงเทพ** · **เลขบัญชี 001-234-5678** · **จังหวัดสาขา เชียงใหม่** | ☐ |

### TC-MTD02 — เงินสด → ค่าธนาคาร 0 + ซ่อนบัญชี (AC-25 / EC-11 / BR-10)
- group: MTD · ความสำคัญ: สูงสุด · trace: AC-25 / EC-11 / BR-10 (CASH fee 0)
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00002) → tab **งวดที่ 2**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK radio **เงินสด** | — | sub **ไม่มีค่าธนาคาร — แนบหลักฐานได้ (optional)** · ขั้น 2.7 → **วิธีจ่าย เงินสด (CASH)** · **ค่าธนาคาร ฿0.00** · บล็อก **บัญชีธนาคาร** หายไป | ☐ |
| 2 | VERIFY ยอดสุทธิ (CASH · CPAY-2025-00002 งวดที่ 2) | — | **ยอดสุทธิ ฿2,100.00** (2,100 − 0) | ☐ |

### TC-MTD03 — เช็ค → ช่องเลขที่เช็ค required ปรากฏ (AC-25)
- group: MTD · ความสำคัญ: สูงสุด · trace: AC-25 / CHEQUE
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001) → tab **งวดที่ 1**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK radio **เช็ค** | — | sub **กรอกเลขที่เช็ค (บังคับ) แนบรูปเช็คได้ (optional)** · ช่อง **เลขที่เช็ค** * (placeholder **CHK-000123**) ปรากฏ · ขั้น 2.7 → **เช็ค (CHEQUE)** · **ค่าธนาคาร ฿0.00** | ☐ |

### TC-MTD04 — เช็คว่าง → block ยืนยัน (negative — AC-25 / VR-05)
- group: MTD · ความสำคัญ: สูงสุด · trace: AC-25 / VR-05 (cheque required)
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001) → tab **งวดที่ 1** → CLICK **เช็ค**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (เลขที่เช็ค = ว่าง) CLICK **ยืนยันการจ่ายงวดที่ 1** | — | toast **กรุณากรอกเลขที่เช็ค** (warning) · งวดที่ 1 **ยังไม่ confirmed** (ไม่มี green alert) | ☐ |

### TC-MTD05 — เช็คกรอกครบ → ยืนยันได้ (AC-25 / EC-11)
- group: MTD · ความสำคัญ: สูง · trace: AC-25 / EC-11
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001) → tab **งวดที่ 1** → CLICK **เช็ค**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE เลขที่เช็ค `CHK-000123` → CLICK **ยืนยันการจ่ายงวดที่ 1** | — | toast **✓ ยืนยันการจ่ายงวดที่ 1สำเร็จ** · green alert **ยืนยันการจ่ายงวดที่ 1แล้ว** · auto ไป tab **งวดที่ 2** | ☐ |

---

## Group CFM — Confirm + auto-switch + finalize ⭐ (US-03)

### TC-CFM01 — ยืนยันงวด 1 → alert + toast + auto งวด 2 (happy — AC-26)
- group: CFM · ความสำคัญ: สูงสุด · trace: AC-26 / FN-PAY + auto-switch
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001) → tab **งวดที่ 1**
- ผ่านเมื่อ: alert + toast + auto ไป งวดที่ 2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยืนยันการจ่ายงวดที่ 1** (method โอน default) | — | toast **✓ ยืนยันการจ่ายงวดที่ 1สำเร็จ** · modal **ไม่ปิด** · auto ไป tab **งวดที่ 2** (active) · tab งวดที่ 1 มีไอคอน check | ☐ |
| 2 | CLICK tab **งวดที่ 1** | — | green alert **ยืนยันการจ่ายงวดที่ 1แล้ว** · การ์ด read-only · ไม่มีปุ่มยืนยัน · summary **งวดที่ 1** มี check | ☐ |

### TC-CFM02 — ยืนยันงวด 2 → auto โปรโมชั่น (AC-26)
- group: CFM · ความสำคัญ: สูงสุด · trace: AC-26 / auto inst2 → promo
- Setup: seed=default · files=— (ต่อจาก TC-CFM01)
- Start: (modal เปิด · tab งวดที่ 2)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยืนยันการจ่ายงวดที่ 2** | — | toast **✓ ยืนยันการจ่ายงวดที่ 2สำเร็จ** · auto ไป tab **โปรโมชั่น** (active) · tab งวดที่ 2 มี check | ☐ |

### TC-CFM03 — ยืนยันโปรโมชั่น → ครบทุกงวด (AC-27)
- group: CFM · ความสำคัญ: สูงสุด · trace: AC-27 / FN-PROMOTION
- Setup: seed=default · files=— (ต่อจาก TC-CFM02)
- Start: (modal เปิด · tab โปรโมชั่น)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยืนยันการจ่ายโปรโมชั่น** | — | toast **✓ ยืนยันการจ่ายโปรโมชั่นสำเร็จ** · green alert **ยืนยันการจ่ายโปรโมชั่นแล้ว** · ทุก tab (งวดที่ 1/งวดที่ 2/โปรโมชั่น) มี check | ☐ |

### TC-CFM04 — ยืนยันทำจ่ายทั้งหมด disabled จนครบ + warn (AC-26)
- group: CFM · ความสำคัญ: สูงสุด · trace: AC-26 / finalize gate
- Setup: seed=default · files=—
- Start: OPEN `#/payments` → CLICK **ทำจ่าย** (CPAY-2025-00001)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY summary ก่อนยืนยันครบ | — | บล็อก **สรุปยอดรวมทั้งหมด** · **งวดที่ 1 ฿4,990.00** · **งวดที่ 2 ฿4,990.00** · **โปรโมชั่น ฿295.00** · **รวมทั้งหมด ฿10,275.00** · warn **กรุณายืนยันการจ่ายทุกงวดก่อนกดยืนยันทั้งหมด** · ปุ่ม **ยืนยันทำจ่ายทั้งหมด** = **disabled** | ☐ |
| 2 | VERIFY drift summary vs card | — | summary งวดที่ 1 = **฿4,990.00** (สูตร base−ค่าธนาคาร) ต่างจาก step card **ยอดสุทธิ ฿0.00** (pipeline เต็ม) — AS-BUILT D-08 | ☐ |
| 3 | ยืนยันครบทั้ง 3 งวด → VERIFY ปุ่ม | — | warn หาย · ปุ่ม **ยืนยันทำจ่ายทั้งหมด** = **enabled** | ☐ |

### TC-CFM05 — finalizeAll → completed + navigate + toast (AC-26 / XT-06)
- group: CFM · ความสำคัญ: สูงสุด · trace: AC-26 / XT-06 (event completed) / state completed
- Setup: seed=default · files=— (ต่อจาก TC-CFM03/04 · ยืนยันครบแล้ว)
- Start: (modal เปิด · ทุกงวด confirmed)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยืนยันทำจ่ายทั้งหมด** | — | modal ปิด · URL = **#/payments/completed** · toast **✓ ทำจ่ายทั้งหมดสำเร็จ** (desc **สถานะเปลี่ยนเป็น เสร็จสิ้น**) | ☐ |
| 2 | VERIFY list เสร็จสิ้น | — | CPAY-2025-00001 อยู่ใน tab **เสร็จสิ้น** · สถานะ **เสร็จสิ้น** · โปรโมชั่น **จ่ายแล้ว** · count เสร็จสิ้น = **2** | ☐ |

---

## Group DTL — Detail drawer 5 tabs + print/receipt (US-04)

### TC-DTL01 — เปิด drawer + header + 5 tabs (Case C WHITE/WHITE) (happy — AC-28 / AC-23)
- group: DTL · ความสำคัญ: สูงสุด · trace: AC-28, AC-23 / API-02
- Setup: seed=default · files=—
- Start: OPEN `#/payments`
- ผ่านเมื่อ: drawer 720 + 5 tab + header ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ดูรายละเอียด** (แถว CPAY-2025-00005) | — | URL = **#/payments/CPAY-2025-00005** · drawer เปิด · eyebrow **การทำจ่ายเงินอ้อย · CPAY-2025-00005** · title **นางสาวมาลี ดอกไม้** + status pill **รอดึงค่าความหวาน** · sub **TK-2025-00016 · อ้อยไฟไหม้ · 18.20 ตัน** | ☐ |
| 2 | VERIFY 5 tabs | — | **สรุป** (active) · **งวด 1** · **งวด 2** · **โปรโมชัน** · **Timeline** | ☐ |
| 3 | VERIFY footer | — | ปุ่ม **ปิด** (waiting_ccs → ไม่มีปุ่ม ทำจ่าย) | ☐ |

### TC-DTL02 — tab สรุป (ข้อมูล/บิล/ยอด/บัญชี) (AC-28)
- group: DTL · ความสำคัญ: สูงสุด · trace: AC-28 / summary tab
- Setup: seed=default · files=—
- Start: OPEN `#/payments/CPAY-2025-00001`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY section **ข้อมูลพื้นฐาน** | — | เลขที่ชั่ง **TK-2025-00001** · วันรับอ้อย **2025-01-05** · ประเภทอ้อย **อ้อยสด** · จำนวนตัน (net) **10.50** · CCS **11.20** · สถานะ **รอทำจ่าย** | ☐ |
| 2 | VERIFY section **ประเภทบิล** | — | งวด 1 **บิลเขียว (จ่ายตามงวด)** · งวด 2 **บิลขาว (เงินยืมระหว่างงวด)** | ☐ |
| 3 | VERIFY section **สรุปยอดตามงวด** | — | งวด 1 **฿5,000.00** + **ยังไม่จ่าย** · งวด 2 **฿5,000.00** + **ยังไม่จ่าย** · โปรโมชัน **฿315.00** + **รอจ่ายโปร** · ยอดสุทธิรวม **฿10,315.00** | ☐ |
| 4 | VERIFY section **บัญชีธนาคาร** + ปุ่ม | — | ชื่อบัญชี **นายสมชาย ใจดี** · ธนาคาร **ธนาคารกรุงเทพ** · เลขบัญชี **001-234-5678** · จังหวัดสาขา **เชียงใหม่** · ปุ่ม **ออกใบเสร็จการจ่ายเงินอ้อยรวม** = **disabled** (ยังไม่ completed) | ☐ |

### TC-DTL03 — tab งวด 1 read-only breakdown + พิมพ์ (AC-28 / AC-29)
- group: DTL · ความสำคัญ: สูง · trace: AC-28, AC-29 / FN-PRINT
- Setup: seed=default · files=—
- Start: OPEN `#/payments/CPAY-2025-00003` (completed · งวด paid)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tab **งวด 1** | — | หัวข้อ **งวดที่ 1** + badge **บิลขาว (เงินยืมระหว่างงวด)** · สถานะ **จ่ายแล้ว** · วิธีจ่าย **โอนธนาคาร (TRANSFER)** · การ์ด **ขั้นตอนการคำนวณ** read-only (ไม่มีปุ่มเพิ่มรายการ/method) | ☐ |
| 2 | CLICK ปุ่ม **พิมพ์บิลงวด 1** | — | toast **กำลังส่งบิลงวด 1ไปยังเครื่องพิมพ์...** | ☐ |

### TC-DTL04 — tab งวด 2 / ไม่มีงวด 2 / ยังไม่มี CCS (AC-28)
- group: DTL · ความสำคัญ: สูง · trace: AC-28 / conditional tab
- Setup: seed=default · files=—
- Start: OPEN `#/payments/CPAY-2025-00001`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tab **งวด 2** (CPAY-2025-00001) | — | หัวข้อ **งวดที่ 2** + badge **บิลขาว (เงินยืมระหว่างงวด)** · การ์ดคำนวณ read-only + ปุ่ม **พิมพ์บิลงวด 2** (disabled — ยังไม่จ่าย) | ☐ |
| 2 | เปิด `#/payments/CPAY-2025-00004` → CLICK tab **งวด 2** | — | note **รายการนี้ไม่มีงวด 2** — หมายเหตุ: tab งวด 2 ของ CPAY-2025-00004 ยัง clickable (ไม่ disabled ใน drawer) แต่แสดง note ไม่มีงวด 2 | ☐ |
| 3 | (ก่อน sync) เปิด `#/payments/CPAY-2025-00005` → CLICK tab **งวด 1** | — | note **ยังไม่มีค่า CCS — ไม่สามารถคำนวณยอดได้** (waiting_ccs) | ☐ |

### TC-DTL05 — tab โปรโมชัน + พิมพ์บิลโปรโมชัน (AC-27 / AC-29 / EC-12)
- group: DTL · ความสำคัญ: สูง · trace: AC-27, AC-29 / EC-12 (promo แยกใบ)
- Setup: seed=default · files=—
- Start: OPEN `#/payments/CPAY-2025-00003` (completed · promo paid)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tab **โปรโมชัน** | — | รหัสโปรโมชัน **PROMO-2025-01** · ชื่อโปรโมชัน **ส่งเสริมอ้อยสดต้นฤดู** · อัตราต่อตัน **฿30.00 /ตัน** · น้ำหนักสุทธิ (ตัน) **20.00** · ยอดโปรโมชัน **฿600.00** · สถานะ **จ่ายแล้ว** | ☐ |
| 2 | CLICK ปุ่ม **พิมพ์บิลโปรโมชัน** | — | toast **กำลังส่งบิลโปรโมชันไปยังเครื่องพิมพ์...** | ☐ |
| 3 | เปิด `#/payments/CPAY-2025-00002` → CLICK tab **โปรโมชัน** | — | note **รายการนี้ไม่มีโปรโมชัน** (ไม่มีโปร) | ☐ |

### TC-DTL06 — tab Timeline (event entries) (AC-28 / XT-06)
- group: DTL · ความสำคัญ: กลาง · trace: AC-28 / XT-06 (events)
- Setup: seed=default · files=—
- Start: OPEN `#/payments/CPAY-2025-00003` (completed)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK tab **Timeline** | — | section **ประวัติการดำเนินการ** · entries: **สร้างรายการทำจ่าย** · **payment.ccs.synced — ดึงค่า CCS สำเร็จ (CCS: 12.1)** · **installment.paid — ยืนยันการจ่ายงวดที่ 1** · **installment.paid — ยืนยันการจ่ายงวดที่ 2** · **promotion.paid — ยืนยันการจ่ายโปรโมชัน** · **payment.completed — ทำจ่ายครบทุกงวด** | ☐ |

### TC-DTL07 — ใบเสร็จรวม enabled เฉพาะ completed (AC-29 / BR-14 / VR-11)
- group: DTL · ความสำคัญ: สูง · trace: AC-29 / BR-14 / VR-11 / FN-RECEIPT
- Setup: seed=default · files=—
- Start: OPEN `#/payments/CPAY-2025-00003` (completed) → tab **สรุป**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม ออกใบเสร็จรวม (completed) | — | ปุ่ม **ออกใบเสร็จการจ่ายเงินอ้อยรวม** = **enabled** | ☐ |
| 2 | CLICK **ออกใบเสร็จการจ่ายเงินอ้อยรวม** | — | toast **กำลังส่งบิลรวมไปยังเครื่องพิมพ์...** | ☐ |
| 3 | VERIFY (non-completed) `#/payments/CPAY-2025-00001` | — | ปุ่ม **ออกใบเสร็จการจ่ายเงินอ้อยรวม** = **disabled** | ☐ |

---

## Group XT — Cross-module / SIT (US-03/04 · NFR)

### TC-XT01 — XT-01: อ่าน active config จาก Payment Setting (F-AGM-012) (ต้อง simulate)
- group: XT · ความสำคัญ: สูงสุด · trace: XT-01 / BR-17 · **prototype: mock constants · config จริง = SIT**
- Setup: **simulate — ระบบจริง:** อ่าน K/base/interest/bankFee/schedule/VAT/charges/cane type/factory province จาก F-AGM-012
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prototype) VERIFY ค่าคงที่ | — | calc ใช้ mock: price 1,000 · VAT 735 · WHT 315 · fund 50 · CFG-01 200 · CFG-02 100 · debt 4,000 · interest 120 · fee in 10/out 20 (hard-code) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): active config | — | ทุกค่าดึงจาก Payment Setting (F-AGM-012 · API-EXT) · snapshot ณ confirm (BR-17) | ☐ (ต้อง simulate) |

### TC-XT02 — XT-02: net_tons + cane_type จาก Receiving (F-AGM-011) (ต้อง simulate)
- group: XT · ความสำคัญ: สูงสุด · trace: XT-02 · **prototype: seed local · handoff จริง = SIT**
- Setup: **simulate — ระบบจริง:** Receiving = SoT ส่ง net_tons + cane_type
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง — SIT): source net + cane_type | — | net_tons + cane_type_code ป้อนมูลค่าอ้อย + ปรับประเภทอ้อย มาจาก Receiving (ไม่ใช่ seed) | ☐ (ต้อง simulate) |

### TC-XT03 — XT-03: CCS จาก Legacy CCS API (ต้อง simulate)
- group: XT · ความสำคัญ: สูงสุด · trace: XT-03 / AC-06 / VR-09 · **prototype: sync = toast + ค่า 11.2 คงที่ · API จริง = SIT**
- Setup: seed=default (prototype = TC-SYNC01) + **simulate — ระบบจริง:** CCS legacy API
- Start: OPEN `#/payments` → sync CPAY-2025-00004

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prototype) sync → VERIFY | — | toast **ดึงค่า CCS สำเร็จ (CCS: 11.2)** — ค่า **11.2 คงที่** ทุกรายการ (mock) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): legacy API + ซ้ำ 409 | — | CCS จริงจาก legacy API (ต่างค่าตามรายการ) · sync ซ้ำ → **409 · รายการนี้ได้ทำการดึงค่า CCS แล้ว** | ☐ (ต้อง simulate) |

### TC-XT04 — XT-04: หักหนี้ Debt (F-AGM-008) + 424 retry + optimistic (ต้อง simulate)
- group: XT · ความสำคัญ: สูงสุด · trace: XT-04 / AC-31/32 / BR-16/18 / EC-09/13 · **prototype: หักจริง 4,000 คงที่ · Debt service = SIT**
- Setup: **simulate — ระบบจริง:** Debt service + Idempotency-Key + If-Match/ETag
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prototype) VERIFY หักหนี้ | — | ขั้น 2.5 **หักจริง ฿4,000.00** คงที่ (mock DEBT_ACTUAL) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): Debt integration | — | หักจริงจาก Debt service (min desired 90%, outstanding) · **424 → keep receipt + banner + retry** (EC-13) · pay ซ้ำ = idempotent · stale ETag → **412/409 CONFLICT_UPDATE_STALE** (EC-09) | ☐ (ต้อง simulate) |

### TC-XT05 — XT-05: bank branch province UNKNOWN + warning (ต้อง simulate)
- group: XT · ความสำคัญ: สูง · trace: XT-05 / AC-19 / VR-13 / EC-03 · **prototype: province มีเสมอ (in/out) · UNKNOWN = SIT**
- Setup: **simulate — ระบบจริง:** bank_branch_province_code ว่าง → UNKNOWN
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prototype) VERIFY in/out | — | สาขา=โรงงาน (เชียงใหม่) → **ในจังหวัด (IN_PROVINCE) ฿10.00** · โปร (เชียงราย) → **ต่างจังหวัด (OUT_PROVINCE) ฿20.00** — UNKNOWN path ไม่ trigger (province ตั้งเสมอ) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): UNKNOWN | — | ไม่มี branch province → **ประเภท ไม่ทราบ (UNKNOWN)** + out fee + note **⚠️ ไม่มีข้อมูลจังหวัดสาขาธนาคาร - ใช้อัตราต่างจังหวัดเป็น default** | ☐ (ต้อง simulate) |

### TC-XT06 — WHITE/GREEN block + due/bank/optimistic + RBAC + PDF (ต้อง simulate)
- group: XT · ความสำคัญ: สูงสุด · trace: AC-24/30/31/32 / VR-01/03/04 / EC-01/07/08/09 · **prototype ทำไม่ได้ — SIT**
- Setup: **simulate — ระบบจริง** (seed ไม่มี WHITE/GREEN combo · role fixed Finance Officer)
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): WHITE/GREEN block | — | inst1=WHITE & inst2=GREEN → **ไม่อนุญาตให้งวด 1 เป็นบิลขาว (เงินยืมระหว่างงวด) และงวด 2 เป็นบิลเขียว จ่ายตามงวด** (VR-01 · enforce upstream) | ☐ (ต้อง simulate) |
| 2 | VERIFY (ระบบจริง): pay ก่อน due | — | **ยังไม่ถึงวันที่กำหนดชำระ** (422 PAYMENT_NOT_DUE · VR-03/EC-07) | ☐ (ต้อง simulate) |
| 3 | VERIFY (ระบบจริง): โอน ไม่มี bank | — | **บัญชีธนาคารสำหรับรายการนี้ยังไม่ระบุ** (422 BANK_ACCOUNT_MISSING · VR-04/EC-08) | ☐ (ต้อง simulate) |
| 4 | VERIFY (ระบบจริง): RBAC + PDF | — | Cashier/Accounting/Viewer จำกัดสิทธิ์ (403 **คุณไม่มีสิทธิ์ดำเนินการนี้**) · pay โอน = Finance/Admin · PDF บิล/ใบเสร็จ render จริง (server) | ☐ (ต้อง simulate) |

### TC-XT07 — XT-07: cane-type-specific adj (RATOON+5/BURN−20) + VR-12 (ต้อง simulate)
- group: XT · ความสำคัญ: สูง · trace: AC-11/12 / BR-03 / VR-12 / EC-02 · **prototype hard-code +10 ทุกประเภท — SIT**
- Setup: **simulate — ระบบจริง:** adjustment_price_per_ton ตามประเภทอ้อย
- Start: — (SIT · prototype VERIFY hard-code)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prototype) VERIFY adj อ้อยตอ/อ้อยไฟไหม้ | — | CPAY-2025-00002 (อ้อยตอ) + CPAY-2025-00005 (อ้อยไฟไหม้) ขั้น 2.1.5 ยังแสดง **ปรับ +฿10.00 /ตัน** (hard-code ทุกประเภท) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): adj ตามประเภท | — | FRESH **+10** · RATOON **+5** · BURN **−20** บาท/ตัน · cane_type ไม่พบ → adj **0** + **⚠️ ไม่มีข้อมูลประเภทอ้อย** (VR-12/EC-02) | ☐ (ต้อง simulate) |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `cane-payment.html` ใน browser (desktop ≥1180px) — รอ ~2s ให้ font/icon โหลด
2. **ทุกเคสเริ่มด้วย refresh (F5)** แล้ว OPEN route ตาม `Start:` — mock in-memory, refresh = reset seed 5 รายการ (ทำให้เคส independent) · **ยกเว้นกลุ่มลูกโซ่ CFM01→02→03→05** ที่ต้องรันต่อเนื่องใน modal เดียว
3. ทำตาม step ตามลำดับ — Action ขึ้นต้น verb (OPEN/CLICK/TYPE/SELECT/VERIFY/WAIT)
4. `WAIT` = รอ ≤3s จน Expected ปรากฏ (toast มุมขวาล่าง · Export ~1s · toast แสดง ~3.2-4.2s)
5. **Step calc:** เปิด `ทำจ่าย` → tab งวด → การ์ด `ขั้นตอนการคำนวณ` recalc ทันทีเมื่อเปลี่ยน วิธีจ่าย / เพิ่มรายการหัก · ตัวเลข = ชุด A/B/C/D
6. **ยอดสุทธิ clamp:** งวด base 5,000 → ยอดสุทธิ `฿0.00` (debt 4,000 > before_debt 3,600) · CPAY-2025-00002 งวดที่ 2 (base 7,500) → `฿2,090.00` (ไม่ clamp)
7. **วิธีจ่าย:** โอน → บล็อกบัญชี + fee `฿10.00` · เงินสด → fee `฿0.00` ซ่อนบัญชี · เช็ค → ช่อง `เลขที่เช็ค` * (ว่าง → `กรุณากรอกเลขที่เช็ค`)
8. **Confirm chain:** ยืนยันงวด 1 → auto งวด 2 → ยืนยันงวด 2 → auto โปร → ยืนยันโปร → `ยืนยันทำจ่ายทั้งหมด` (enabled) → `✓ ทำจ่ายทั้งหมดสำเร็จ` + ไป tab เสร็จสิ้น
9. **Sync:** เดี่ยว `ดึงค่า CCS (ยืนยัน)` → `ดึงค่า CCS สำเร็จ (CCS: 11.2)` · Sync All `ยืนยันและเริ่ม` → 2/2/0 + `ดึงค่า CCS ทั้งหมดเสร็จสิ้น`
10. **Detail:** `ดูรายละเอียด` → drawer 5 tab · ใบเสร็จรวม enabled เฉพาะ completed · พิมพ์ → toast `กำลังส่งบิล{...}ไปยังเครื่องพิมพ์...`
11. step ไหน Expected ไม่ตรง = FAIL เคสนั้น → บันทึก `failed_step` + `evidence` แล้วไปเคสถัดไป
12. เคส `(ต้อง simulate)` — ถ้ารันบน prototype ทำไม่ได้ ให้ status = `blocked` + note "SIT case"

## Coverage Audit

| หมวด | covered / total |
|---|---|
| Stories/AC (06_TESTS §6.1) | 32 / 32 (AC-06/12/24/30-32 = defensive/RBAC = simulate) |
| Cross-Module / Event (XT-01..06) | 6 / 6 (XT-01..05 config/handoff/API/event จริง = simulate) |
| Business rules (BR-01..19) | 19 / 19 (BR-03/16/17/18/19 = simulate) |
| Validation (VR-01/03/04/05/06/09/10/12/13) | prototype: VR-05/06/10 reachable · VR-01/03/04/09/12/13 = simulate |
| Edge cases (EC-01..14) | 14 / 14 (EC-01/02/03/07/08/09/10/13 = simulate) |
| Error catalog (UI-observable) | prototype: `กรุณากรอกเลขที่เช็ค` / `กรุณากรอกรายละเอียด` / `กรุณากรอกจำนวนเงินให้ถูกต้อง` · 409/412/422/424/403 = simulate |
| Permission cells | Finance Officer allow ครบ · Cashier/Accounting/Viewer/Admin RBAC = simulate |
| Step calc 7 ขั้น + auto-switch + Sync + Detail | ครบทุกชั้น (price/adj/split/vat/charge FLAT+PER_TON/debt/interest white+green/bankfee in+out + clamp) |

- **Manifest cross-check (FRD §0.12): ✅ 32 AC + 6 XT + 19 BR + 13 VR + 14 EC — ทุกแถวมีคู่ใน Ledger**

### เคส (ต้อง simulate) / SIT
- TC-FLT05 step 3 (no-data variant — seed มี record เสมอ)
- TC-FLT06 step 2 (ไฟล์ CSV จริง + filename — server-side)
- TC-SYNC04 step 2 (message VR-10 — prototype ใช้ปุ่ม-disable)
- TC-SYNC05 step 2 (sync ซ้ำ 409 — ปุ่มหายที่ UI)
- TC-CALC02 step 3 (adj RATOON/BURN — hard-code +10)
- TC-XT01..XT07 (config F-AGM-012 · net/cane จาก Receiving · CCS legacy · Debt 424/optimistic · UNKNOWN province · WHITE/GREEN block · RBAC · PDF · cane-type adj + VR-12)

## Microcopy Drift Log (prototype vs FRD/UI_BRIEF)

| # | จุด | FRD/UI_BRIEF | Prototype (AS-BUILT · authoritative) |
|---|---|---|---|
| MD-01 | top tabs | FRD AC-01: 3 แท็บ (รอความหวาน/รอทำจ่าย/เสร็จสิ้น) | มีแค่ **2** (`รอทำจ่าย`/`เสร็จสิ้น`) · waiting_ccs = dropdown สถานะ `รอดึงค่าความหวาน` |
| MD-02 | bill label | FRD §6.3: `บิลเขียว จ่ายตามงวด` | `บิลเขียว (จ่ายตามงวด)` (มีวงเล็บ) |
| MD-03 | promo badge | FRD §6.3: `จ่ายโปรแล้ว` | `จ่ายแล้ว` |
| MD-04 | step 2.6 title | UI_BRIEF §9: `ขั้นตอน 2.6 ดอกเบี้ย` | `ขั้นตอน 2.6` + `ดอกเบี้ย (บิลขาว)` |
| MD-05 | step 2.1.5 / 2.3 title | FRD §6.3: `ปรับประเภทอ้อย` / `VAT / ภาษี` | `ปรับตามประเภทอ้อย (v4.1)` / `ภาษี` |
| MD-06 | โปรโมชัน spelling | — | list col + pay tab = `โปรโมชั่น` (ไม้เอก) · drawer tab + step = `โปรโมชัน` (ไม่มีไม้เอก) — inconsistent ภายใน prototype |
| MD-07 | filter | FRD AC-03: filter season/product/checkin_type/unload_date | prototype มีแค่ ประเภทอ้อย + สถานะ (+ search) · ไม่มี date/season |
| MD-08 | cane adj | FRD BR-03: FRESH+10/RATOON+5/BURN−20 | hard-code `+฿10.00 /ตัน` ทุกประเภท |
| MD-09 | stat ยอดจ่ายรวมวันนี้ | UI_BRIEF: `฿20,600.00` | ตัวเลขใหญ่ = `20,600.00` (ไม่มี ฿) · ฿ อยู่ใน meta `฿20,600.00 (เสร็จสิ้น)` |
| MD-10 | summary vs card | — | summary block ใช้ `base − ค่าธนาคาร` (งวดที่ 1 `฿4,990.00`) ≠ step card pipeline เต็ม (`ยอดสุทธิ ฿0.00`) — drift D-08 |

## Result Report (schema)

```json
{
  "feature_id": "F-AGM-013",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-LIST01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 58, "pass": 0, "fail": 0, "blocked": 0 }
}
```

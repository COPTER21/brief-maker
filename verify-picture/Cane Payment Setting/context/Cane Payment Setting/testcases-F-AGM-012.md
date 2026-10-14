# AI Test Cases — F-AGM-012 Cane Payment Setting (ตั้งค่าการจ่ายเงินอ้อย)

ชุด test case สำหรับ **AI agent (browser-use / vision)** รันบน prototype `cane-payment-setting.html`
ทุก anchor คือข้อความที่เห็นบนจอจริง (ยืนยันกับ prototype โดยตรง + FRD 06_TESTS §6.10 microcopy + 05_RULES + UI_BRIEF §9 แล้ว) · Expected เช็คได้ด้วยตา
feature นี้เป็น **หน้า config เดียว** (route `#/payment-setting`) มี inner-nav ซ้าย 6 section — **ไม่ใช่** list/CRUD page · เคสที่ prototype จำลองไม่ได้ (**unique Active per season×product (409)** · **optimistic lock (412 stale ETag)** · **RBAC 4 roles** · **no-overlap schedule ฝั่ง BE** · **BE dailyRate compute ตอน save** · **ค่าธนาคารติดลบ guard** · **API-EXT active-setting → Cane Payment runtime (XT-03/05)** · **CRUD-list/create/duplicate/deactivate เต็มตาม FRD**) ติด `(ต้อง simulate)` — รันซ้ำกับระบบจริงตอน SIT

> ⚠ **หมายเหตุ single-page:** ไม่มี top tab-bar / ไม่มี drawer · เปลี่ยน section ด้วยปุ่ม inner-nav ซ้าย (`setSection`) — ไม่เปลี่ยน URL (route คงเป็น `#/payment-setting` เสมอ · hashchange guard ดีดกลับ) · overlay มีเฉพาะ 2 modal (charge 460px / payout 520px)

> ⚠ **หมายเหตุ in-memory reset:** prototype เก็บ state ในหน่วยความจำ · refresh (F5) = reset seed ทั้งหมด (charges 2 · green 3 · white 2 · rate 7.00/base 365 · K 0.060 · จังหวัดหลักว่าง) — ใช้เป็นข้อดี: **ทุกเคส independent โดย refresh ก่อนเริ่ม** · state คงอยู่ข้ามการสลับ section (ไม่ reset จนกว่าจะ F5)

> ⚠ **หมายเหตุ role:** prototype fix `CURRENT_ROLE = 'Finance Officer'` · `canWrite = true` เสมอ · ปุ่ม บันทึก/เพิ่ม/แก้ไข/ลบ แสดงครบ · RBAC ฝั่ง Finance Manager (CRUD+status) / Operations (view+preview) / Auditor (read-only) = `(ต้อง simulate)` ที่ SIT

> ⚠ **หมายเหตุ save guard (สำคัญ):** seed ตั้งต้น **จังหวัดหลักว่าง** แต่มีค่าธรรมเนียม (ในจังหวัด 5.00 · ต่างจังหวัด 15.00) → กด **บันทึก** ทันทีจะ **ไม่สำเร็จ** ขึ้น `กรุณาเลือกจังหวัดหลัก` — ต้องเลือกจังหวัดหลักก่อนจึงจะ save สำเร็จ

> ⚠ **หมายเหตุ drift ที่ยืนยันกับ code:** (1) selector context = `ฤดูการหีบ (Crushing Season)` (FRD เขียน "รอบหีบ" — prototype ชนะ) · (2) pill = `Base @10CCS: 900.00 บาท/ตัน` (FRD เขียน "Base: 900.00" — prototype ชนะ) · (3) label ค่าธนาคาร verbatim = `ค่าธรรมเนียมในจังหวัด (บาท)` / `ค่าธรรมเนียมต่างจังหวัด (บาท)` · (4) **ตารางวันจ่าย seed เดือน render เป็น `พฤศจิกายน`/`ธันวาคม 2568`** (เก็บ month แบบ 0-index → `THAI_MONTHS[10]`=พฤศจิกายน · `THAI_MONTHS[11]`=ธันวาคม) — ไม่ใช่ ต.ค./พ.ย.

## Meta

| Field | Value |
|---|---|
| Feature ID | F-AGM-012 (AGM/PAYMENT — ตั้งค่าการจ่ายเงินอ้อย · Payment Setting) |
| App entry | เปิดไฟล์ `cane-payment-setting.html` ใน browser (Chrome desktop ≥1180px) |
| Route | `#/payment-setting` (default · section=general) — route เดียว · section/payout-tab ไม่ผูก URL |
| Inner-nav 6 section | **ข้อมูลทั่วไป** (general) · **สูตรคำนวณ CCS** (ccs-delta) · **รายการหักเพิ่มเติม** (additional-charges) · **ภาษี** (tax) · **ตารางกำหนดวันจ่าย** (payout-schedule) · **ทดสอบและดูตัวอย่าง** (preview-test) |
| Overlays | charge modal 460px (`openModalBox('charge')`) · payout-range modal 520px (`openModalBox('payout')`) — backdrop click / Esc → `closeModal()` |
| User | สมพร วงศ์ทะเบียน / Finance Officer · WKN (avatar สว · canWrite=true) |
| ที่มา | FRD_F-AGM-012_Pack (06_TESTS AC-01..23 + XT-01..05 · 05_RULES BR-PS-01..12 / VR-01..08 / EC-01..14) + UI_BRIEF_F-AGM-012 |
| จำนวนเคส | 56 เคส / 10 groups (รันได้ 47 · ต้อง simulate 9) |
| Signature ⭐⭐⭐ | **หน้า config SoT ของ Cane Payment**: ดอกเบี้ยต่อวัน auto (roundUp 7) · สูตร CCS delta live · ตารางวันจ่ายบิลเขียว/บิลขาว · Preview & Test คำนวณ interest + ค่าธนาคาร per งวด |
| หัวใจ 1 — Daily rate auto | ดอกเบี้ยต่อปี ÷ วันฐาน (ปัดขึ้น 7 ตำแหน่ง) → readonly `ดอกเบี้ยต่อวัน` = **0.0191781** (7/365) live |
| หัวใจ 2 — CCS delta | `ราคาต่อตัน = Base @10CCS + (CCS − 10) × (Base @10CCS × K)` → 4 stat live (900.00 / 54.00 / 1,008.00 / 1.01) |
| หัวใจ 3 — Payout 2-subtab | บิลเขียว (งวด 1/2) · บิลขาว (FIXED_DATE / WITH_CANE="ตามตารางบิลเขียว (ไม่คิดดอกเบี้ย)") |
| หัวใจ 4 — Preview & Test | คำนวณ → ยอดรวม + งวด 1/2 · บิลขาว มีดอกเบี้ย (daysEarly 30 sim) · บิลเขียว ไม่มี · ค่าธนาคาร in/out จังหวัด |
| หัวใจ 5 — Save | validate (rate>0 · base>0 · จังหวัดหลัก · K 0–1) → `บันทึกการตั้งค่าสำเร็จ` (desc ฤดูการหีบ + ดอกเบี้ยต่อวัน) |
| Cross-module ⭐ | อ่าน masters (Season/Product/Base @10CCS) · **expose active setting → Cane Payment (API-EXT)** = SoT ของ K/ดอกเบี้ย/ค่าธนาคาร/ตารางวันจ่าย = `(ต้อง simulate)` ที่ SIT |

**Seed ตั้งต้น (หลัง F5):**

| กลุ่ม | ค่า |
|---|---|
| Context | ฤดูการหีบ **2024/2025** (จาก 2024/2025, 2023/2024, 2022/2023) · Product **อ้อยสด** · Base @10CCS **900.00 บาท/ตัน** |
| General | ดอกเบี้ยต่อปี **7.00** · วันฐาน **365** · ดอกเบี้ยต่อวัน **0.0191781** (readonly) · จังหวัดหลัก **(ว่าง)** · ค่าในจังหวัด **5.00** · ค่าต่างจังหวัด **15.00** |
| CCS | ค่า K **0.060** · ค่า CCS ตัวอย่าง **12** → 900.00 / 54.00 / 1,008.00 / 1.01 |
| Charges (2 แถว) | ค่าขนส่ง · จำนวนเงิน · **50.00 บาท** · หักต่อตัน — ค่าปรับความชื้น · เปอร์เซ็นต์ · **2.00 %** · หักจากยอดรวม |
| Tax | หัก VAT ก่อนแบ่งงวด = **ปิด** (อัตรา VAT default 7 เมื่อเปิด) |
| Payout green (3 แถว) | พฤศจิกายน 2568 / วันที่ 1–15 · พฤศจิกายน 2568 / วันที่ 16–30 · ธันวาคม 2568 / วันที่ 1–15 (ทุกแถว การใช้งาน=เปิด) |
| Payout white (2 แถว) | พฤศจิกายน 2568 / วันที่ 1–7 · วันจ่าย **12 พ.ย. 2568** (FIXED_DATE) — พฤศจิกายน 2568 / วันที่ 8–15 · วันจ่าย **ตามตารางบิลเขียว (ไม่คิดดอกเบี้ย)** (WITH_CANE) |
| Preview | CCS **12** · น้ำหนัก **30** · บิลงวด 1 **บิลเขียว (ปกติ)** · บิลงวด 2 **บิลขาว (เบิกล่วงหน้า มีดอกเบี้ย)** · % หักหนี้ **10** · จังหวัดบัญชี **(ว่าง)** |

**VERBATIM microcopy (Expected anchors — copy เป๊ะจาก prototype):**
- header: title `Payment Setting Configuration` + status pill `ใช้งาน` · sub `แหล่งความจริงของค่าพื้นฐานที่ Cane Payment ใช้คำนวณ` · ปุ่ม `บันทึก`
- context bar: `ฤดูการหีบ (Crushing Season)` (select) · pill `Product: อ้อยสด` · pill `Base @10CCS: 900.00 บาท/ตัน`
- inner-nav: `ข้อมูลทั่วไป` · `สูตรคำนวณ CCS` · `รายการหักเพิ่มเติม` · `ภาษี` · `ตารางกำหนดวันจ่าย` · `ทดสอบและดูตัวอย่าง`
- General: `ข้อมูลสินค้า` · `สินค้าอ้อย` (select `อ้อยสด`) · `หมายเหตุ` (placeholder `กรอกหมายเหตุเพิ่มเติม (ถ้าต้องการ)`) · `ดอกเบี้ยบิลขาว` · `ดอกเบี้ยต่อปี (%)` · `วันฐาน (วัน)` · `ดอกเบี้ยต่อวัน` · note `ระบบคำนวณ ดอกเบี้ยต่อวัน อัตโนมัติ = ดอกเบี้ยต่อปี ÷ วันฐาน (ปัดขึ้น 7 ตำแหน่ง) — ใช้คำนวณดอกเบี้ยของบิลขาว (เบิกล่วงหน้า)` · `ค่าธนาคาร` · `จังหวัดหลัก` (placeholder `เลือกจังหวัด`) · `ค่าธรรมเนียมในจังหวัด (บาท)` · `ค่าธรรมเนียมต่างจังหวัด (บาท)`
- CCS: note `สูตร: ราคาต่อตัน = Base @10CCS + (CCS − 10) × (Base @10CCS × K)` + `โดยที่ K คือค่าคงที่สำหรับคำนวณราคาต่อ 1 CCS` · `ค่า K` · `ค่า CCS ตัวอย่าง` · stat `Base Price @10CCS` (meta `บาท/ตัน (ค่าคงที่)`) · `ราคาต่อ 1 CCS` (meta `บาท (Base × K)`) · `ราคาต่อตัน @12 CCS` (meta `บาท/ตัน`) · `ราคาต่อกิโลกรัม` (meta `บาท/กก. (÷1000)`)
- Charges: `รายการหักเพิ่มเติม` · ปุ่ม `เพิ่มรายการ` · cols `ชื่อรายการ`·`ประเภท`·`ค่า`·`หมายเหตุ`·`จัดการ` · type `จำนวนเงิน`/`เปอร์เซ็นต์` · modal title `เพิ่มรายการ`/`แก้ไขรายการ` · sub `รายการหักเพิ่มเติม` · `ชื่อรายการ *` (placeholder `เช่น ค่าขนส่ง`) · `ประเภท` · `ค่า *` (placeholder `0.00`) · `หมายเหตุ` (placeholder `หมายเหตุ (ถ้าต้องการ)`) · ปุ่ม `ยกเลิก`/`บันทึก` · empty `ยังไม่มีรายการ` (desc `กดปุ่ม เพิ่มรายการ เพื่อเพิ่มรายการหักเพิ่มเติม`)
- Tax: note `หากเลือกหัก VAT → ระบบจะคำนวณ VAT ก่อน แล้วค่อยแบ่งยอดเป็นงวด 1/2` · `หัก VAT ก่อนแบ่งงวด` (desc `เปิดเพื่อคำนวณภาษีมูลค่าเพิ่มก่อนแบ่งยอดงวด`) · `อัตรา VAT (%)`
- Payout: tabs `ตารางวันจ่ายบิลเขียว`/`ตารางวันจ่ายบิลขาว` · ปุ่ม `เพิ่มช่วง` · green desc `กำหนดวันจ่ายงวด 1 และ งวด 2 สำหรับบิลเขียว` · white desc `กำหนดวันจ่ายสำหรับบิลขาว (เบิกล่วงหน้า)` · green cols `#`·`ช่วงวันที่ส่ง/ขึ้นเงิน`·`วันจ่ายงวด 1`·`วันจ่ายงวด 2`·`การใช้งาน`·`จัดการ` · white cols `#`·`ช่วงวันที่เบิกบิลขาว`·`วันจ่าย`·`การใช้งาน`·`จัดการ` · WITH_CANE cell `ตามตารางบิลเขียว (ไม่คิดดอกเบี้ย)` · active pill (row toggle เป็น switch)
- Payout modal: title `เพิ่ม/แก้ไขช่วงการจ่าย` · sub `ตารางวันจ่ายบิลเขียว`/`ตารางวันจ่ายบิลขาว` · `เดือน` · `ปี พ.ศ.` · `วันเริ่มต้น` · `วันสิ้นสุด` · (green) `วันจ่ายงวด 1`/`วันจ่ายงวด 2` · (white) `ประเภทวันจ่าย` (select `วันที่กำหนด`/`พร้อมค่าอ้อย`) · `วันจ่าย` · hint `เลือก พร้อมค่าอ้อย — จ่ายตามตารางบิลเขียว (ไม่คิดดอกเบี้ย)`
- Preview: `ข้อมูลทดสอบ` · `ค่า CCS` · `น้ำหนัก (ตัน)` · `วันที่ส่ง/ขึ้นเงิน` · `ประเภทบิลงวด 1` · `ประเภทบิลงวด 2` · options `บิลเขียว (ปกติ)`/`บิลขาว (เบิกล่วงหน้า มีดอกเบี้ย)` · `% หักหนี้ (จาก Booking)` · `จังหวัดบัญชีเกษตรกร` · ปุ่ม `คำนวณ` · result `ผลการคำนวณ` · note `วิธีจ่าย: โอนเข้าบัญชี (ค่าเริ่มต้น) · ค่าธนาคาร ในจังหวัด/ต่างจังหวัด N บาท` · `ยอดรวม` · `ราคาต่อตัน` · `ราคาต่อกิโลกรัม` · `ยอดรวม (price/ton × น้ำหนัก)` · `งวดที่ 1` (pill `บิลเขียว`) · `งวดที่ 2` (pill `บิลขาว`) · `วันจ่ายปกติ` · `วันจ่ายจริง` · `จำนวนวันล่วงหน้า` · `ยอดก่อนหักหนี้` · `ยอดหลังหักหนี้` · `ดอกเบี้ย` · `ค่าธนาคาร` · `ยอดสุทธิ`
- Toast success: `บันทึกการตั้งค่าสำเร็จ` · `คำนวณสำเร็จ` · `บันทึกช่วงการจ่ายสำเร็จ` · `ลบช่วงการจ่ายสำเร็จ` · `เพิ่มรายการสำเร็จ` · `บันทึกรายการสำเร็จ` · `ลบรายการสำเร็จ`
- Toast warning (validate): `ดอกเบี้ยต่อปีต้องมากกว่า 0` · `วันฐานต้องมากกว่า 0` · `กรุณาเลือกจังหวัดหลัก` · `ค่า K ต้องอยู่ระหว่าง 0–1` · `วันเริ่มต้นต้องไม่เกินวันสิ้นสุด` · `กรุณากรอกวันจ่ายเมื่อเลือกวันที่กำหนด` · `กรุณากรอกชื่อรายการ` · `กรุณากรอกค่าให้ถูกต้อง`
- simulate (SIT): unique Active `มีการตั้งค่า Active สำหรับรอบหีบ+สินค้านี้อยู่แล้ว` · stale `ข้อมูลไม่ตรงปัจจุบัน กรุณารีเฟรช` · overlap `ช่วงวันที่ซ้อนทับกัน` · bank fee `ค่าธนาคารต้องไม่ติดลบ` · forbidden `คุณไม่มีสิทธิ์ดำเนินการนี้`

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| NAV — Shell / config page / context / inner-nav | TC-NAV-01..05 (5) | สูงสุด |
| GEN — General: interest + daily rate + bank fee | TC-GEN-01..06 (6) | สูงสุด |
| CCS — CCS Delta live compute | TC-CCS-01..05 (5) | สูงสุด |
| CHG — Additional Charges CRUD | TC-CHG-01..07 (7) | สูงสุด |
| TAX — VAT toggle | TC-TAX-01..03 (3) | สูง |
| PAY — Payout Schedule green/white | TC-PAY-01..09 (9) | สูงสุด |
| PRV — Preview & Test | TC-PRV-01..07 (7) | สูงสุด |
| SAVE — Save validate + success | TC-SAVE-01..06 (6) | สูงสุด |
| XT — Cross-module / Event + simulate | TC-XT-01..05 (5) | สูงสุด |
| MC — Microcopy / drift / regression | TC-MC-01..04 (4) | สูง |

---

## Coverage Ledger

### Stories/AC (06_TESTS §6.1)
| AC | รายละเอียด (ย่อ) | cases |
|---|---|---|
| AC-01 | section ข้อมูลทั่วไป: สินค้าอ้อย + หมายเหตุ + Base @10CCS (read-only) | TC-NAV-03, TC-GEN-01 |
| AC-02 | กลุ่มดอกเบี้ยบิลขาว: ต่อปี + วันฐาน + ต่อวัน (readonly auto) | TC-GEN-01, TC-GEN-02 |
| AC-03 | ต่อปี 7 + วันฐาน 365 → ต่อวัน = roundUp(7/365,7) | TC-GEN-02, TC-XT-04 |
| AC-04 | ต่อปี ≤ 0 → `ดอกเบี้ยต่อปีต้องมากกว่า 0` | TC-SAVE-02 |
| AC-05 | กลุ่มค่าธนาคาร: จังหวัดหลัก + ในจังหวัด + ต่างจังหวัด | TC-GEN-04 |
| AC-06 | bank fee ไม่เลือกจังหวัดหลัก → `กรุณาเลือกจังหวัดหลัก` | TC-SAVE-04 |
| AC-07 | สูตร CCS แสดง · K default 0.060 | TC-CCS-01 |
| AC-08 | CCS preview 4 stat ตาม K | TC-CCS-01, TC-CCS-02, TC-CCS-03 |
| AC-09 | Charges table + เพิ่ม/แก้ไข/ลบ | TC-CHG-01, TC-CHG-02, TC-CHG-05, TC-CHG-06 |
| AC-10 | VAT switch `หัก VAT ก่อนแบ่งงวด` → เปิด → rate | TC-TAX-01, TC-TAX-02 |
| AC-11 | 2 sub-tabs บิลเขียว/บิลขาว | TC-PAY-01 |
| AC-12 | บิลเขียว columns | TC-PAY-01 |
| AC-13 | บิลขาว columns | TC-PAY-02 |
| AC-14 | บิลขาว WITH_CANE → `ตามตารางบิลเขียว (ไม่คิดดอกเบี้ย)` | TC-PAY-02 |
| AC-15 | เพิ่มช่วง (modal) เดือน/ปี/วันเริ่ม/สิ้นสุด + green pay1/2 / white paytype | TC-PAY-04, TC-PAY-06 |
| AC-16 | white วันที่กำหนด → ต้องกรอกวันจ่าย · พร้อมค่าอ้อย → ไม่กรอก | TC-PAY-07, TC-PAY-08 |
| AC-17 | toggle การใช้งาน เปิด/ปิด row | TC-PAY-03 |
| AC-18 | Preview inputs (7 ช่อง) | TC-PRV-01, TC-PRV-02 |
| AC-19 | คำนวณ → ราคาต่อตัน/กก. + ยอดรวม + ต่องวด | TC-PRV-01, TC-PRV-02 |
| AC-20 | บิลขาว → มีดอกเบี้ย · บิลเขียว → ไม่มี | TC-PRV-03, TC-PRV-04 |
| AC-21 | จังหวัดบัญชี=หลัก → in-fee · ต่าง → out-fee | TC-PRV-05 |
| AC-22 | บันทึก → validate + toast success | TC-SAVE-01 |
| AC-23 | unique Active ซ้ำ → `มีการตั้งค่า Active…` | TC-XT-05 (ต้อง simulate) |

### Cross-Module / Event (06_TESTS §6.9) ⭐
| XT | Scenario | cases |
|---|---|---|
| XT-01 | Base @10CCS อ่านจาก Price List (read-only) | TC-XT-01 |
| XT-02 | Season/Product selector (masters read) | TC-XT-02 |
| XT-03 | Cane Payment อ่าน active setting (K/interest/fee/pay dates) | TC-XT-03 (ต้อง simulate) |
| XT-04 | daily_rate = roundUp(rate/base,7) | TC-XT-04 |
| XT-05 | Receiving net+cane_type → Payment ใช้ config นี้ (chain SoT) + unique Active | TC-XT-05 (ต้อง simulate) |

### Validation (05_RULES §5.4)
| VR | Message | cases |
|---|---|---|
| VR-01 | `ดอกเบี้ยต่อปีต้องมากกว่า 0` | TC-SAVE-02 |
| VR-02 | `วันฐานต้องมากกว่า 0` | TC-SAVE-03 |
| VR-03 | `กรุณาเลือกจังหวัดหลัก` | TC-SAVE-04 |
| VR-04 | `ค่าธนาคารต้องไม่ติดลบ` (prototype ไม่ validate) | TC-XT-05 (ต้อง simulate) |
| VR-05 | `ค่า K ต้องอยู่ระหว่าง 0–1` | TC-SAVE-05 |
| VR-06 | Green from≤to → `วันเริ่มต้นต้องไม่เกินวันสิ้นสุด` · no-overlap `ช่วงวันที่ซ้อนทับกัน` (BE) | TC-PAY-05, TC-XT-05 (overlap = simulate) |
| VR-07 | White FIXED_DATE → `กรุณากรอกวันจ่ายเมื่อเลือกวันที่กำหนด` | TC-PAY-07 |
| VR-08 | unique Active → `มีการตั้งค่า Active…` | TC-XT-05 (ต้อง simulate) |
| (charge) | `กรุณากรอกชื่อรายการ` / `กรุณากรอกค่าให้ถูกต้อง` | TC-CHG-03, TC-CHG-04 |

### Edge Cases (05_RULES §5.5)
| EC | Case | cases |
|---|---|---|
| EC-01 | daily_rate auto roundUp 7 readonly | TC-GEN-02 |
| EC-02 | rate ≤ 0 → VR-01 | TC-SAVE-02 |
| EC-03 | bank fee ไม่เลือกจังหวัดหลัก → VR-03 | TC-SAVE-04 |
| EC-04 | CCS preview ตามสูตร | TC-CCS-01, TC-CCS-02 |
| EC-05 | Green schedule overlap → VR-06 (BE) | TC-XT-05 (ต้อง simulate) |
| EC-06 | White FIXED_DATE ไม่กรอกวัน → VR-07 | TC-PAY-07 |
| EC-07 | White WITH_CANE → `ตามตารางบิลเขียว (ไม่คิดดอกเบี้ย)` | TC-PAY-02, TC-PAY-08 |
| EC-08 | Preview บิลขาว → days_early + interest | TC-PRV-01, TC-PRV-04 |
| EC-09 | Preview บิลเขียว → ไม่มีดอกเบี้ย | TC-PRV-03 |
| EC-10 | Preview จังหวัด=หลัก → in-fee | TC-PRV-05 |
| EC-11 | Preview จังหวัดต่าง → out-fee | TC-PRV-01 |
| EC-12 | Save unique Active ซ้ำ → 409 | TC-XT-05 (ต้อง simulate) |
| EC-13 | Edit Inactive → guard 403 | TC-XT-05 (ต้อง simulate) |
| EC-14 | Save stale ETag → 412 | TC-XT-05 (ต้อง simulate) |

**Manifest cross-check:** AC 23/23 · XT-01..05 5/5 · VR-01..08 8/8 · EC-01..14 14/14 → ทุกแถวมีคู่ใน Ledger ✅ (unique Active/optimistic lock/RBAC/no-overlap/API-EXT = simulate ตาม Drift Log D-01/D-03/D-04/D-07/D-08)

---

## Data Sets

### ชุด GEN — daily rate
| กรณี | ต่อปี | วันฐาน | ดอกเบี้ยต่อวัน (readonly) |
|---|---|---|---|
| G1 (default) | 7.00 | 365 | 0.0191781 |
| G2 | 10 | 365 | 0.0273973 |
| G3 | 7 | 360 | 0.0194445 |

### ชุด CCS — 4 stat
| กรณี | K | CCS | ราคาต่อ 1 CCS | ราคาต่อตัน @CCS | ราคาต่อกก. |
|---|---|---|---|---|---|
| C1 (default) | 0.060 | 12 | 54.00 | 1,008.00 | 1.01 |
| C2 | 0.080 | 12 | 72.00 | 1,044.00 | 1.04 |
| C3 | 0.060 | 14 | 54.00 | 1,116.00 | 1.12 |
| C4 | 0.060 | 8 | 54.00 | 792.00 | 0.79 |

### ชุด CHG — charge modal
| กรณี | ชื่อรายการ | ค่า | คาดหวัง |
|---|---|---|---|
| H1 (happy add) | ค่าคัดคุณภาพ | 30 | `เพิ่มรายการสำเร็จ` |
| H2 (name ว่าง) | *(เว้นว่าง)* | 30 | `กรุณากรอกชื่อรายการ` |
| H3 (value ว่าง) | ค่าคัดคุณภาพ | *(เว้นว่าง)* | `กรุณากรอกค่าให้ถูกต้อง` |

### ชุด PRV — preview (default seed เว้นระบุ)
| กรณี | bill1 | bill2 | จังหวัดหลัก | จังหวัดบัญชี | งวด1 net | งวด2 net |
|---|---|---|---|---|---|---|
| P1 (default) | บิลเขียว | บิลขาว | (ว่าง) | (ว่าง) | 13,593.00 | 13,514.71 |
| P2 (all เขียว) | บิลเขียว | บิลเขียว | (ว่าง) | (ว่าง) | 13,593.00 | 13,593.00 |
| P3 (all ขาว) | บิลขาว | บิลขาว | (ว่าง) | (ว่าง) | 13,514.71 | 13,514.71 |
| P4 (in-province) | บิลเขียว | บิลขาว | ขอนแก่น | ขอนแก่น | 13,603.00 | 13,524.71 |

---

## Test Cases

## Group NAV — Shell / Config page / Context / Inner-nav (US-01..07)

### TC-NAV-01 — เปิดหน้า config + header + context bar (happy — AC-01)
- group: NAV · ความสำคัญ: สูงสุด · trace: AC-01 / page loaded
- Setup: F5 (seed default) · Start: OPEN `cane-payment-setting.html`
- ผ่านเมื่อ: header + context bar + inner-nav ตรง seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN ไฟล์ | — | route = **#/payment-setting** · title **Payment Setting Configuration** + pill **ใช้งาน** · sub **แหล่งความจริงของค่าพื้นฐานที่ Cane Payment ใช้คำนวณ** · ปุ่ม **บันทึก** (primary) | ☐ |
| 2 | VERIFY context bar | — | label **ฤดูการหีบ (Crushing Season)** + select = **2024/2025** · pill **Product: อ้อยสด** · pill **Base @10CCS: 900.00 บาท/ตัน** | ☐ |
| 3 | VERIFY inner-nav 6 ปุ่ม (ซ้าย) | — | **ข้อมูลทั่วไป** (active) · **สูตรคำนวณ CCS** · **รายการหักเพิ่มเติม** · **ภาษี** · **ตารางกำหนดวันจ่าย** · **ทดสอบและดูตัวอย่าง** | ☐ |
| 4 | VERIFY sidebar/user | — | sidebar feature **ตั้งค่าการจ่ายเงินอ้อย** (active) · user **สมพร วงศ์ทะเบียน** / **Finance Officer · WKN** | ☐ |

### TC-NAV-02 — สลับ section ด้วย inner-nav (AC-01)
- group: NAV · ความสำคัญ: สูงสุด · trace: AC-01 / setSection
- Setup: F5 · Start: OPEN หน้า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สูตรคำนวณ CCS** | — | card ขวาเปลี่ยนเป็น section CCS · แสดง note **สูตร: ราคาต่อตัน = Base @10CCS + (CCS − 10) × (Base @10CCS × K)** · ปุ่ม **สูตรคำนวณ CCS** = active (border/bg แดงอ่อน) · route ยัง **#/payment-setting** | ☐ |
| 2 | CLICK **ตารางกำหนดวันจ่าย** | — | แสดง 2 tabs **ตารางวันจ่ายบิลเขียว**/**ตารางวันจ่ายบิลขาว** · route ไม่เปลี่ยน | ☐ |
| 3 | CLICK **ทดสอบและดูตัวอย่าง** | — | แสดง section **ข้อมูลทดสอบ** + ปุ่ม **คำนวณ** | ☐ |
| 4 | CLICK **ข้อมูลทั่วไป** | — | กลับ section General (**ข้อมูลสินค้า** + **ดอกเบี้ยบิลขาว** + **ค่าธนาคาร**) | ☐ |

### TC-NAV-03 — General section anatomy (AC-01/05)
- group: NAV · ความสำคัญ: สูง · trace: AC-01, AC-05 / general layout
- Setup: F5 · Start: OPEN หน้า (section=general)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY form-section titles | — | **ข้อมูลสินค้า** · **ดอกเบี้ยบิลขาว** · **ค่าธนาคาร** | ☐ |
| 2 | VERIFY ข้อมูลสินค้า | — | field **สินค้าอ้อย** (select **อ้อยสด**) · field **หมายเหตุ** (textarea placeholder **กรอกหมายเหตุเพิ่มเติม (ถ้าต้องการ)**) | ☐ |
| 3 | VERIFY ดอกเบี้ยบิลขาว | — | **ดอกเบี้ยต่อปี (%)** = **7.00** · **วันฐาน (วัน)** = **365** · **ดอกเบี้ยต่อวัน** = **0.0191781** (readonly) | ☐ |
| 4 | VERIFY ค่าธนาคาร | — | **จังหวัดหลัก** (placeholder **เลือกจังหวัด**) · **ค่าธรรมเนียมในจังหวัด (บาท)** = **5.00** · **ค่าธรรมเนียมต่างจังหวัด (บาท)** = **15.00** | ☐ |

### TC-NAV-04 — เปลี่ยน ฤดูการหีบ selector (AC-01 / XT-02)
- group: NAV · ความสำคัญ: กลาง · trace: XT-02 / season select
- Setup: F5 · Start: OPEN หน้า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN select **ฤดูการหีบ (Crushing Season)** | — | 3 ตัวเลือก: **2024/2025** · **2023/2024** · **2022/2023** | ☐ |
| 2 | SELECT **2023/2024** | — | selector แสดง **2023/2024** · pill Base @10CCS/Product คงเดิม (ค่าคงที่) | ☐ |

### TC-NAV-05 — hashchange guard (route ล็อก) (AC-01)
- group: NAV · ความสำคัญ: กลาง · trace: single-route guard
- Setup: F5 · Start: OPEN หน้า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET hash = **#/other-route** (พิมพ์ใน address bar) | — | ระบบดีดกลับ route = **#/payment-setting** · หน้า config แสดงตามปกติ | ☐ |

---

## Group GEN — General: interest + daily rate + bank fee (US-01)

### TC-GEN-01 — ค่า default ดอกเบี้ย + ค่าธนาคาร (happy — AC-01/02/05)
- group: GEN · ความสำคัญ: สูงสุด · trace: AC-01, AC-02, AC-05
- Setup: F5 · Start: OPEN หน้า (general)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY กลุ่มดอกเบี้ยบิลขาว | — | ดอกเบี้ยต่อปี (%) **7.00** · วันฐาน (วัน) **365** · ดอกเบี้ยต่อวัน **0.0191781** | ☐ |
| 2 | VERIFY note คำนวณ | — | **ระบบคำนวณ ดอกเบี้ยต่อวัน อัตโนมัติ = ดอกเบี้ยต่อปี ÷ วันฐาน (ปัดขึ้น 7 ตำแหน่ง) — ใช้คำนวณดอกเบี้ยของบิลขาว (เบิกล่วงหน้า)** | ☐ |
| 3 | VERIFY ช่อง ดอกเบี้ยต่อวัน = readonly | — | คลิกช่อง **ดอกเบี้ยต่อวัน** พิมพ์ไม่ได้ (readonly · พื้นเทา) | ☐ |

### TC-GEN-02 — daily rate live recompute (AC-03 / EC-01)
- group: GEN · ความสำคัญ: สูงสุด · trace: AC-03 / EC-01 / roundUp 7
- Setup: F5 · Start: OPEN หน้า (general)
- ผ่านเมื่อ: ดอกเบี้ยต่อวัน อัปเดตทันทีตามชุด GEN

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET ดอกเบี้ยต่อปี (%) = **10** (วันฐาน 365) | G2 | ดอกเบี้ยต่อวัน อัปเดตเป็น **0.0273973** | ☐ |
| 2 | SET ดอกเบี้ยต่อปี = **7** · วันฐาน = **360** | G3 | ดอกเบี้ยต่อวัน = **0.0194445** | ☐ |
| 3 | SET กลับ ต่อปี **7** · วันฐาน **365** | G1 | ดอกเบี้ยต่อวัน = **0.0191781** | ☐ |

### TC-GEN-03 — วันฐาน = 0 → daily rate = 0 (AC-02)
- group: GEN · ความสำคัญ: กลาง · trace: AC-02 / guard div0
- Setup: F5 · Start: OPEN หน้า (general)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET วันฐาน (วัน) = **0** | — | ดอกเบี้ยต่อวัน แสดง **0.0000000** (base≤0 → 0) | ☐ |

### TC-GEN-04 — จังหวัดหลัก + ค่าธรรมเนียม (AC-05)
- group: GEN · ความสำคัญ: สูง · trace: AC-05 / bank fee
- Setup: F5 · Start: OPEN หน้า (general)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN select **จังหวัดหลัก** | — | 4 ตัวเลือก: **ขอนแก่น** · **กาญจนบุรี** · **ราชบุรี** · **นครปฐม** | ☐ |
| 2 | SELECT **ขอนแก่น** | — | select แสดง **ขอนแก่น** | ☐ |
| 3 | SET ค่าธรรมเนียมในจังหวัด = **8.00** · ต่างจังหวัด = **20.00** | — | ค่ารับเข้า field (mono) — ไม่มี error | ☐ |

### TC-GEN-05 — หมายเหตุ textarea (AC-01)
- group: GEN · ความสำคัญ: ต่ำ · trace: AC-01 / note field
- Setup: F5 · Start: OPEN หน้า (general)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE ในช่อง **หมายเหตุ** = "ทดสอบหมายเหตุ" | — | textarea รับข้อความ · สลับ section แล้วกลับมา General → ข้อความยังอยู่ (state คงข้าม section) | ☐ |

### TC-GEN-06 — state คงข้ามการสลับ section (regression)
- group: GEN · ความสำคัญ: สูง · trace: in-memory persistence
- Setup: F5 · Start: OPEN หน้า (general)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET ดอกเบี้ยต่อปี = **9** → CLICK **สูตรคำนวณ CCS** → CLICK **ข้อมูลทั่วไป** | — | ดอกเบี้ยต่อปี ยัง **9** · ดอกเบี้ยต่อวัน = **0.0246576** (9/365 roundUp 7) | ☐ |
| 2 | F5 (refresh) → VERIFY | — | reset: ดอกเบี้ยต่อปี กลับ **7.00** · ต่อวัน **0.0191781** | ☐ |

---

## Group CCS — CCS Delta live compute (US-02)

### TC-CCS-01 — สูตร + 4 stat default (happy — AC-07/08 / EC-04)
- group: CCS · ความสำคัญ: สูงสุด · trace: AC-07, AC-08 / EC-04
- Setup: F5 · Start: OPEN หน้า → CLICK **สูตรคำนวณ CCS**
- ผ่านเมื่อ: 4 stat = ชุด CCS C1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY note สูตร | — | **สูตร: ราคาต่อตัน = Base @10CCS + (CCS − 10) × (Base @10CCS × K)** + **โดยที่ K คือค่าคงที่สำหรับคำนวณราคาต่อ 1 CCS** | ☐ |
| 2 | VERIFY inputs | — | **ค่า K** = **0.060** · **ค่า CCS ตัวอย่าง** = **12** | ☐ |
| 3 | VERIFY 4 stat | — | **Base Price @10CCS 900.00** (บาท/ตัน (ค่าคงที่)) · **ราคาต่อ 1 CCS 54.00** (บาท (Base × K)) · **ราคาต่อตัน @12 CCS 1,008.00** (บาท/ตัน) · **ราคาต่อกิโลกรัม 1.01** (บาท/กก. (÷1000)) | ☐ |

### TC-CCS-02 — เปลี่ยน K → per1/perton recompute (AC-08 / EC-04)
- group: CCS · ความสำคัญ: สูงสุด · trace: AC-08 / FN-CCS
- Setup: F5 · Start: section CCS

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET ค่า K = **0.080** (CCS 12) | C2 | ราคาต่อ 1 CCS **72.00** · ราคาต่อตัน @12 CCS **1,044.00** · ราคาต่อกิโลกรัม **1.04** | ☐ |

### TC-CCS-03 — เปลี่ยน CCS → label + perton (AC-08)
- group: CCS · ความสำคัญ: สูง · trace: AC-08 / label live
- Setup: F5 · Start: section CCS

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET ค่า CCS ตัวอย่าง = **14** (K 0.060) | C3 | stat label เปลี่ยนเป็น **ราคาต่อตัน @14 CCS** · ค่า **1,116.00** · ราคาต่อกิโลกรัม **1.12** | ☐ |
| 2 | SET ค่า CCS ตัวอย่าง = **8** | C4 | label **ราคาต่อตัน @8 CCS** · ค่า **792.00** · ราคาต่อกิโลกรัม **0.79** | ☐ |

### TC-CCS-04 — CCS = 10 → perton = Base (edge)
- group: CCS · ความสำคัญ: กลาง · trace: EC-04 / boundary
- Setup: F5 · Start: section CCS

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET ค่า CCS ตัวอย่าง = **10** | — | ราคาต่อตัน @10 CCS = **900.00** (= Base · delta 0) · ราคาต่อกิโลกรัม **0.90** | ☐ |

### TC-CCS-05 — Base Price = ค่าคงที่ (XT-01)
- group: CCS · ความสำคัญ: กลาง · trace: XT-01 / Base read-only
- Setup: F5 · Start: section CCS

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปลี่ยน K/CCS ไปมา แล้ว VERIFY Base | — | **Base Price @10CCS** = **900.00** เสมอ (ไม่มีช่องแก้ · มาจาก master) | ☐ |

---

## Group CHG — Additional Charges CRUD (US-03)

### TC-CHG-01 — ตาราง + seed 2 แถว (happy — AC-09)
- group: CHG · ความสำคัญ: สูงสุด · trace: AC-09 / table
- Setup: F5 · Start: OPEN หน้า → CLICK **รายการหักเพิ่มเติม**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY header + ปุ่ม | — | หัวข้อ **รายการหักเพิ่มเติม** + ปุ่ม **เพิ่มรายการ** | ☐ |
| 2 | VERIFY หัวคอลัมน์ | — | **ชื่อรายการ · ประเภท · ค่า · หมายเหตุ · จัดการ** | ☐ |
| 3 | VERIFY แถว 1 | — | **ค่าขนส่ง** · **จำนวนเงิน** · **50.00 บาท** · **หักต่อตัน** + ปุ่ม แก้ไข/ลบ | ☐ |
| 4 | VERIFY แถว 2 | — | **ค่าปรับความชื้น** · **เปอร์เซ็นต์** · **2.00 %** · **หักจากยอดรวม** | ☐ |

### TC-CHG-02 — เพิ่มรายการ (modal) สำเร็จ (AC-09)
- group: CHG · ความสำคัญ: สูงสุด · trace: AC-09 / add
- Setup: F5 · Start: section Charges
- ผ่านเมื่อ: modal + toast + แถวใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มรายการ** | — | modal เปิด · title **เพิ่มรายการ** · sub **รายการหักเพิ่มเติม** · field **ชื่อรายการ \*** (placeholder **เช่น ค่าขนส่ง**) · **ประเภท** (select) · **ค่า \*** (placeholder **0.00**) · **หมายเหตุ** (placeholder **หมายเหตุ (ถ้าต้องการ)**) · ปุ่ม **ยกเลิก**/**บันทึก** | ☐ |
| 2 | TYPE ชื่อรายการ **ค่าคัดคุณภาพ** · ค่า **30** · CLICK **บันทึก** | H1 | modal ปิด · toast **เพิ่มรายการสำเร็จ** · ตารางมีแถวใหม่ **ค่าคัดคุณภาพ · จำนวนเงิน · 30.00 บาท** | ☐ |

### TC-CHG-03 — เพิ่มรายการ: ชื่อว่าง → block (negative — VR/charge)
- group: CHG · ความสำคัญ: สูง · trace: charge validate name
- Setup: F5 · Start: section Charges → CLICK **เพิ่มรายการ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เว้นช่อง ชื่อรายการ · TYPE ค่า **30** · CLICK **บันทึก** | H2 | toast **กรุณากรอกชื่อรายการ** · modal ยังเปิด | ☐ |

### TC-CHG-04 — เพิ่มรายการ: ค่าว่าง/ไม่ใช่ตัวเลข → block (negative)
- group: CHG · ความสำคัญ: สูง · trace: charge validate value
- Setup: F5 · Start: section Charges → CLICK **เพิ่มรายการ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE ชื่อรายการ **ค่าคัดคุณภาพ** · เว้นช่อง ค่า · CLICK **บันทึก** | H3 | toast **กรุณากรอกค่าให้ถูกต้อง** · modal ยังเปิด | ☐ |

### TC-CHG-05 — แก้ไขรายการ (AC-09)
- group: CHG · ความสำคัญ: สูง · trace: AC-09 / edit
- Setup: F5 · Start: section Charges

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม แก้ไข (แถว **ค่าขนส่ง**) | — | modal title **แก้ไขรายการ** · ช่อง ชื่อรายการ = **ค่าขนส่ง** · ค่า = **50** | ☐ |
| 2 | เปลี่ยนค่า = **60** · CLICK **บันทึก** | — | toast **บันทึกรายการสำเร็จ** · แถว ค่าขนส่ง = **60.00 บาท** | ☐ |

### TC-CHG-06 — ลบรายการ (AC-09)
- group: CHG · ความสำคัญ: สูง · trace: AC-09 / delete
- Setup: F5 · Start: section Charges

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม ลบ (แถว **ค่าปรับความชื้น**) | — | toast **ลบรายการสำเร็จ** · เหลือ 1 แถว (ค่าขนส่ง) | ☐ |

### TC-CHG-07 — empty state หลังลบครบ (AC-09)
- group: CHG · ความสำคัญ: กลาง · trace: AC-09 / empty
- Setup: F5 · Start: section Charges

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ลบทั้ง 2 แถว | — | empty title **ยังไม่มีรายการ** · desc **กดปุ่ม เพิ่มรายการ เพื่อเพิ่มรายการหักเพิ่มเติม** | ☐ |

---

## Group TAX — VAT toggle (US-04)

### TC-TAX-01 — toggle VAT เปิด → field rate (happy — AC-10)
- group: TAX · ความสำคัญ: สูง · trace: AC-10 / VAT switch
- Setup: F5 · Start: OPEN หน้า → CLICK **ภาษี**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY default | — | note **หากเลือกหัก VAT → ระบบจะคำนวณ VAT ก่อน แล้วค่อยแบ่งยอดเป็นงวด 1/2** · แถว **หัก VAT ก่อนแบ่งงวด** (desc **เปิดเพื่อคำนวณภาษีมูลค่าเพิ่มก่อนแบ่งยอดงวด**) + switch (ปิด) · **ไม่มี** ช่อง อัตรา VAT | ☐ |
| 2 | CLICK switch (เปิด) | — | switch เปลี่ยนเป็นเปิด (แดง) · แสดง field **อัตรา VAT (%)** = **7** | ☐ |

### TC-TAX-02 — ปิด VAT → ซ่อน rate (AC-10)
- group: TAX · ความสำคัญ: กลาง · trace: AC-10 / toggle off
- Setup: F5 · Start: section Tax → เปิด VAT

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK switch (ปิด) | — | field **อัตรา VAT (%)** หายไป | ☐ |

### TC-TAX-03 — แก้อัตรา VAT (AC-10)
- group: TAX · ความสำคัญ: ต่ำ · trace: AC-10 / rate edit
- Setup: F5 · Start: section Tax → เปิด VAT

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET อัตรา VAT (%) = **10** | — | field รับค่า 10 · สลับ section แล้วกลับมา (เปิด VAT) → ยัง 10 | ☐ |

---

## Group PAY — Payout Schedule green/white (US-05) ⭐

### TC-PAY-01 — tab บิลเขียว: columns + seed 3 แถว (happy — AC-11/12)
- group: PAY · ความสำคัญ: สูงสุด · trace: AC-11, AC-12 / green table
- Setup: F5 · Start: OPEN หน้า → CLICK **ตารางกำหนดวันจ่าย**
- ผ่านเมื่อ: columns + 3 แถว seed ตรง (เดือน render พฤศจิกายน/ธันวาคม)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY tabs + desc | — | tab **ตารางวันจ่ายบิลเขียว** (active) + **ตารางวันจ่ายบิลขาว** · desc **กำหนดวันจ่ายงวด 1 และ งวด 2 สำหรับบิลเขียว** + ปุ่ม **เพิ่มช่วง** | ☐ |
| 2 | VERIFY หัวคอลัมน์ | — | **# · ช่วงวันที่ส่ง/ขึ้นเงิน · วันจ่ายงวด 1 · วันจ่ายงวด 2 · การใช้งาน · จัดการ** | ☐ |
| 3 | VERIFY แถว 1 | — | # **1** · **พฤศจิกายน 2568 / วันที่ 1–15** · วันจ่ายงวด 1 **15 พ.ย. 2568** · วันจ่ายงวด 2 **30 พ.ย. 2568** · การใช้งาน = เปิด | ☐ |
| 4 | VERIFY แถว 2–3 | — | แถว 2 **พฤศจิกายน 2568 / วันที่ 16–30** (งวด1 **30 พ.ย. 2568** · งวด2 **15 ธ.ค. 2568**) · แถว 3 **ธันวาคม 2568 / วันที่ 1–15** (งวด1 **15 ธ.ค. 2568** · งวด2 **30 ธ.ค. 2568**) | ☐ |

### TC-PAY-02 — tab บิลขาว: columns + WITH_CANE cell (AC-13/14 / EC-07)
- group: PAY · ความสำคัญ: สูงสุด · trace: AC-13, AC-14 / EC-07
- Setup: F5 · Start: section Payout → CLICK **ตารางวันจ่ายบิลขาว**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY desc + หัวคอลัมน์ | — | desc **กำหนดวันจ่ายสำหรับบิลขาว (เบิกล่วงหน้า)** · คอลัมน์ **# · ช่วงวันที่เบิกบิลขาว · วันจ่าย · การใช้งาน · จัดการ** | ☐ |
| 2 | VERIFY แถว 1 (FIXED_DATE) | — | **พฤศจิกายน 2568 / วันที่ 1–7** · วันจ่าย **12 พ.ย. 2568** | ☐ |
| 3 | VERIFY แถว 2 (WITH_CANE) | — | **พฤศจิกายน 2568 / วันที่ 8–15** · วันจ่าย **ตามตารางบิลเขียว (ไม่คิดดอกเบี้ย)** | ☐ |

### TC-PAY-03 — toggle การใช้งาน per row (AC-17)
- group: PAY · ความสำคัญ: สูง · trace: AC-17 / active toggle
- Setup: F5 · Start: section Payout (green)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK switch การใช้งาน (แถว 1) | — | switch แถว 1 สลับเป็นปิด (เทา) · ไม่มี toast · แถวอื่นคงเดิม | ☐ |
| 2 | CLICK switch อีกครั้ง | — | กลับเป็นเปิด (แดง) | ☐ |

### TC-PAY-04 — เพิ่มช่วงบิลเขียว (modal) สำเร็จ (AC-15)
- group: PAY · ความสำคัญ: สูงสุด · trace: AC-15 / green add
- Setup: F5 · Start: section Payout (green)
- ผ่านเมื่อ: modal + toast + แถวใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มช่วง** | — | modal title **เพิ่ม/แก้ไขช่วงการจ่าย** · sub **ตารางวันจ่ายบิลเขียว** · fields **เดือน**/**ปี พ.ศ.**/**วันเริ่มต้น**/**วันสิ้นสุด** + **วันจ่ายงวด 1**/**วันจ่ายงวด 2** | ☐ |
| 2 | SET วันเริ่มต้น **1** · วันสิ้นสุด **15** · วันจ่ายงวด 1 (date) · วันจ่ายงวด 2 (date) · CLICK **บันทึก** | — | modal ปิด · toast **บันทึกช่วงการจ่ายสำเร็จ** · ตารางมีแถวเพิ่ม | ☐ |

### TC-PAY-05 — เพิ่มช่วง: วันเริ่มต้น > วันสิ้นสุด → block (negative — VR-06)
- group: PAY · ความสำคัญ: สูงสุด · trace: VR-06 / from>to
- Setup: F5 · Start: section Payout (green) → CLICK **เพิ่มช่วง**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET วันเริ่มต้น **20** · วันสิ้นสุด **5** · CLICK **บันทึก** | — | toast **วันเริ่มต้นต้องไม่เกินวันสิ้นสุด** · modal ยังเปิด · ไม่เพิ่มแถว | ☐ |

### TC-PAY-06 — เพิ่มช่วงบิลขาว: ประเภทวันจ่าย gating (AC-15/16)
- group: PAY · ความสำคัญ: สูงสุด · trace: AC-15, AC-16 / white pay-type
- Setup: F5 · Start: section Payout → tab บิลขาว → CLICK **เพิ่มช่วง**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY modal (default FIXED_DATE) | — | sub **ตารางวันจ่ายบิลขาว** · field **ประเภทวันจ่าย** (select **วันที่กำหนด**/**พร้อมค่าอ้อย**) · แสดง field **วันจ่าย** (date) | ☐ |
| 2 | SELECT ประเภทวันจ่าย = **พร้อมค่าอ้อย** | — | field **วันจ่าย** หายไป · แสดง hint **เลือก พร้อมค่าอ้อย — จ่ายตามตารางบิลเขียว (ไม่คิดดอกเบี้ย)** | ☐ |
| 3 | SELECT ประเภทวันจ่าย = **วันที่กำหนด** | — | field **วันจ่าย** (date) กลับมา · hint หาย | ☐ |

### TC-PAY-07 — บิลขาว FIXED_DATE ไม่กรอกวันจ่าย → block (negative — AC-16 / VR-07 / EC-06)
- group: PAY · ความสำคัญ: สูงสุด · trace: AC-16 / VR-07 / EC-06
- Setup: F5 · Start: section Payout → tab บิลขาว → CLICK **เพิ่มช่วง**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ประเภทวันจ่าย = **วันที่กำหนด** · เว้นช่อง วันจ่าย · SET วันเริ่มต้น **1** · สิ้นสุด **10** · CLICK **บันทึก** | — | toast **กรุณากรอกวันจ่ายเมื่อเลือกวันที่กำหนด** · modal ยังเปิด | ☐ |

### TC-PAY-08 — บิลขาว WITH_CANE บันทึกสำเร็จ (AC-16 / EC-07)
- group: PAY · ความสำคัญ: สูง · trace: AC-16 / EC-07 / WITH_CANE
- Setup: F5 · Start: section Payout → tab บิลขาว → CLICK **เพิ่มช่วง**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ประเภทวันจ่าย = **พร้อมค่าอ้อย** · SET วันเริ่มต้น **16** · สิ้นสุด **20** · CLICK **บันทึก** | — | toast **บันทึกช่วงการจ่ายสำเร็จ** · แถวใหม่ วันจ่าย = **ตามตารางบิลเขียว (ไม่คิดดอกเบี้ย)** | ☐ |

### TC-PAY-09 — ลบช่วงการจ่าย (AC-15)
- group: PAY · ความสำคัญ: กลาง · trace: AC-15 / delete
- Setup: F5 · Start: section Payout (green)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม ลบ (แถว 3 · ธันวาคม 2568) | — | toast **ลบช่วงการจ่ายสำเร็จ** · เหลือ 2 แถว | ☐ |

---

## Group PRV — Preview & Test (US-06) ⭐

### TC-PRV-01 — คำนวณ default (happy — AC-18/19/20 · EC-08/11)
- group: PRV · ความสำคัญ: สูงสุด · trace: AC-18, AC-19, AC-20 / EC-08, EC-11
- Setup: F5 · Start: OPEN หน้า → CLICK **ทดสอบและดูตัวอย่าง**
- ผ่านเมื่อ: ผลตรงชุด PRV P1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY inputs default | — | ค่า CCS **12** · น้ำหนัก (ตัน) **30** · ประเภทบิลงวด 1 **บิลเขียว (ปกติ)** · ประเภทบิลงวด 2 **บิลขาว (เบิกล่วงหน้า มีดอกเบี้ย)** · % หักหนี้ (จาก Booking) **10** · จังหวัดบัญชีเกษตรกร (ว่าง) | ☐ |
| 2 | CLICK **คำนวณ** | P1 | toast **คำนวณสำเร็จ** · section **ผลการคำนวณ** ปรากฏ · note **วิธีจ่าย: โอนเข้าบัญชี (ค่าเริ่มต้น) · ค่าธนาคาร ต่างจังหวัด 15.00 บาท** | ☐ |
| 3 | VERIFY **ยอดรวม** | — | ราคาต่อตัน **1,008.00 บาท** · ราคาต่อกิโลกรัม **1.01 บาท** · **ยอดรวม (price/ton × น้ำหนัก) 30,240.00 บาท** | ☐ |
| 4 | VERIFY **งวดที่ 1** (pill **บิลเขียว**) | — | วันจ่ายปกติ **15 พ.ย. 2568** · วันจ่ายจริง **15 พ.ย. 2568** · จำนวนวันล่วงหน้า **0 วัน** · ยอดก่อนหักหนี้ **15,120.00 บาท** · ยอดหลังหักหนี้ **13,608.00 บาท** · ดอกเบี้ย **0.00 บาท** · ค่าธนาคาร **15.00 บาท** · ยอดสุทธิ **13,593.00 บาท** | ☐ |
| 5 | VERIFY **งวดที่ 2** (pill **บิลขาว**) | — | วันจ่ายปกติ **30 พ.ย. 2568** · วันจ่ายจริง **31 ต.ค. 2568** · จำนวนวันล่วงหน้า **30 วัน** · ยอดหลังหักหนี้ **13,608.00 บาท** · ดอกเบี้ย **78.29 บาท** · ค่าธนาคาร **15.00 บาท** · ยอดสุทธิ **13,514.71 บาท** | ☐ |

### TC-PRV-02 — โครงสร้างผล + pill สี (AC-18/19)
- group: PRV · ความสำคัญ: สูง · trace: AC-18, AC-19 / structure
- Setup: F5 · Start: section Preview → CLICK **คำนวณ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY 8 fields ต่องวด | — | แต่ละงวดมี: **วันจ่ายปกติ · วันจ่ายจริง · จำนวนวันล่วงหน้า · ยอดก่อนหักหนี้ · ยอดหลังหักหนี้ · ดอกเบี้ย · ค่าธนาคาร · ยอดสุทธิ** | ☐ |
| 2 | VERIFY pill | — | งวดที่ 1 pill **บิลเขียว** (success) · งวดที่ 2 pill **บิลขาว** (warning) | ☐ |

### TC-PRV-03 — ทั้ง 2 งวด บิลเขียว → ไม่มีดอกเบี้ย (AC-20 / EC-09)
- group: PRV · ความสำคัญ: สูงสุด · trace: AC-20 / EC-09
- Setup: F5 · Start: section Preview

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET ประเภทบิลงวด 2 = **บิลเขียว (ปกติ)** · CLICK **คำนวณ** | P2 | งวดที่ 1 pill **บิลเขียว** · งวดที่ 2 pill **บิลเขียว** · ทั้งสองงวด จำนวนวันล่วงหน้า **0 วัน** · ดอกเบี้ย **0.00 บาท** · ยอดสุทธิ **13,593.00 บาท** ทั้งคู่ | ☐ |

### TC-PRV-04 — ทั้ง 2 งวด บิลขาว → มีดอกเบี้ยทั้งคู่ (AC-20 / EC-08)
- group: PRV · ความสำคัญ: สูงสุด · trace: AC-20 / EC-08
- Setup: F5 · Start: section Preview

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET ประเภทบิลงวด 1 = **บิลขาว (เบิกล่วงหน้า มีดอกเบี้ย)** · CLICK **คำนวณ** | P3 | งวดที่ 1 pill **บิลขาว** · จำนวนวันล่วงหน้า **30 วัน** · ดอกเบี้ย **78.29 บาท** · ยอดสุทธิ **13,514.71 บาท** · งวดที่ 2 = เหมือนกัน (13,514.71) | ☐ |

### TC-PRV-05 — จังหวัดบัญชี = จังหวัดหลัก → in-province fee (AC-21 / EC-10)
- group: PRV · ความสำคัญ: สูงสุด · trace: AC-21 / EC-10 · **ต้องตั้งจังหวัดหลักที่ General ก่อน**
- Setup: F5 · Start: OPEN หน้า
- ผ่านเมื่อ: ค่าธนาคาร = 5.00 (ในจังหวัด) + net ตามชุด P4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ข้อมูลทั่วไป** → SET จังหวัดหลัก = **ขอนแก่น** | — | select แสดง **ขอนแก่น** | ☐ |
| 2 | CLICK **ทดสอบและดูตัวอย่าง** → SET จังหวัดบัญชีเกษตรกร = **ขอนแก่น** → CLICK **คำนวณ** | P4 | note **… ค่าธนาคาร ในจังหวัด 5.00 บาท** · งวดที่ 1 ค่าธนาคาร **5.00 บาท** · ยอดสุทธิ **13,603.00 บาท** · งวดที่ 2 ยอดสุทธิ **13,524.71 บาท** | ☐ |
| 3 | เปลี่ยน จังหวัดบัญชี = **กาญจนบุรี** (≠ หลัก) → CLICK **คำนวณ** | — | note **… ค่าธนาคาร ต่างจังหวัด 15.00 บาท** · งวดที่ 1 ยอดสุทธิ **13,593.00 บาท** | ☐ |

### TC-PRV-06 — เปลี่ยน CCS/น้ำหนัก → ยอดรวม recompute (AC-19)
- group: PRV · ความสำคัญ: สูง · trace: AC-19 / total recompute
- Setup: F5 · Start: section Preview

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET ค่า CCS = **14** · น้ำหนัก = **50** · ประเภทบิลงวด 2 = **บิลเขียว (ปกติ)** · CLICK **คำนวณ** | — | ราคาต่อตัน **1,116.00 บาท** · ราคาต่อกิโลกรัม **1.12 บาท** · **ยอดรวม (price/ton × น้ำหนัก) 55,800.00 บาท** | ☐ |

### TC-PRV-07 — เปลี่ยน % หักหนี้ → ยอดหลังหักหนี้ recompute (AC-19)
- group: PRV · ความสำคัญ: สูง · trace: AC-19 / debt recompute
- Setup: F5 · Start: section Preview

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET % หักหนี้ (จาก Booking) = **20** · CLICK **คำนวณ** | — | งวดที่ 1 ยอดก่อนหักหนี้ **15,120.00 บาท** · ยอดหลังหักหนี้ **12,096.00 บาท** · ยอดสุทธิ **12,081.00 บาท** (บิลเขียว) | ☐ |

---

## Group SAVE — Save validate + success (US-07)

### TC-SAVE-01 — บันทึกสำเร็จ (happy — AC-22)
- group: SAVE · ความสำคัญ: สูงสุด · trace: AC-22 / save success
- Setup: F5 · Start: OPEN หน้า
- ผ่านเมื่อ: toast success + desc

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ข้อมูลทั่วไป** → SET จังหวัดหลัก = **ขอนแก่น** (ปลด save guard) | — | select = ขอนแก่น | ☐ |
| 2 | CLICK **บันทึก** (header) | — | toast **บันทึกการตั้งค่าสำเร็จ** · desc **ฤดูการหีบ 2024/2025 · ดอกเบี้ยต่อวัน 0.0191781** | ☐ |

### TC-SAVE-02 — ดอกเบี้ยต่อปี ≤ 0 → block (negative — AC-04 / VR-01 / EC-02)
- group: SAVE · ความสำคัญ: สูงสุด · trace: AC-04 / VR-01 / EC-02
- Setup: F5 · Start: OPEN หน้า (general)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET ดอกเบี้ยต่อปี (%) = **0** · CLICK **บันทึก** | — | toast **ดอกเบี้ยต่อปีต้องมากกว่า 0** · ไม่มี toast success | ☐ |

### TC-SAVE-03 — วันฐาน ≤ 0 → block (negative — VR-02)
- group: SAVE · ความสำคัญ: สูง · trace: VR-02 / base>0
- Setup: F5 · Start: OPEN หน้า (general)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET วันฐาน (วัน) = **0** (ดอกเบี้ยต่อปี ยัง 7) · CLICK **บันทึก** | — | toast **วันฐานต้องมากกว่า 0** | ☐ |

### TC-SAVE-04 — ไม่เลือกจังหวัดหลัก + มีค่าธรรมเนียม → block (negative — AC-06 / VR-03 / EC-03)
- group: SAVE · ความสำคัญ: สูงสุด · trace: AC-06 / VR-03 / EC-03
- Setup: F5 · Start: OPEN หน้า (seed จังหวัดหลักว่าง · fee 5/15)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **บันทึก** ทันที (ไม่แตะจังหวัดหลัก) | — | toast **กรุณาเลือกจังหวัดหลัก** (เพราะ fee > 0 แต่จังหวัดหลักว่าง) | ☐ |

### TC-SAVE-05 — ค่า K นอกช่วง 0–1 → block (negative — VR-05)
- group: SAVE · ความสำคัญ: สูง · trace: VR-05 / K range
- Setup: F5 · Start: OPEN หน้า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ข้อมูลทั่วไป** → SET จังหวัดหลัก **ขอนแก่น** (ปลด guard fee) · CLICK **สูตรคำนวณ CCS** → SET ค่า K = **1.5** · CLICK **บันทึก** | — | toast **ค่า K ต้องอยู่ระหว่าง 0–1** | ☐ |

### TC-SAVE-06 — ลำดับ validate (rate ก่อน base ก่อน province ก่อน K)
- group: SAVE · ความสำคัญ: กลาง · trace: VR order
- Setup: F5 · Start: OPEN หน้า (general)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET ดอกเบี้ยต่อปี = **0** · วันฐาน = **0** · CLICK **บันทึก** | — | toast **ดอกเบี้ยต่อปีต้องมากกว่า 0** (แสดง rate ก่อน · ยังไม่ถึง base) | ☐ |
| 2 | แก้ ดอกเบี้ยต่อปี = **7** (วันฐาน ยัง 0) · CLICK **บันทึก** | — | toast **วันฐานต้องมากกว่า 0** | ☐ |

---

## Group XT — Cross-module / Event + simulate (§6.9) ⭐

### TC-XT-01 — Base @10CCS อ่านจาก Price List (XT-01)
- group: XT · ความสำคัญ: สูง · trace: XT-01 / master read
- Setup: F5 · Start: OPEN หน้า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY Base ทุกจุด | — | context pill **Base @10CCS: 900.00 บาท/ตัน** · CCS stat **Base Price @10CCS 900.00** — read-only (ไม่มีช่องแก้ · มาจาก master Price List) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): Base มาจาก Price List ต่อ season×product | — | ค่าเปลี่ยนตาม master จริง (prototype fix 900.00) | ☐ (ต้อง simulate) |

### TC-XT-02 — Season/Product selector (XT-02)
- group: XT · ความสำคัญ: กลาง · trace: XT-02 / masters
- Setup: F5 · Start: OPEN หน้า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY selector | — | **ฤดูการหีบ (Crushing Season)** = 2024/2025, 2023/2024, 2022/2023 · **Product: อ้อยสด** (fix) | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): เปลี่ยน season โหลด config ต่อ season×product | — | โหลด setting ของรอบหีบที่เลือก (prototype = config เดียว in-memory) | ☐ (ต้อง simulate) |

### TC-XT-03 — Cane Payment อ่าน active setting (XT-03) (ต้อง simulate)
- group: XT · ความสำคัญ: สูงสุด · trace: XT-03 / API-EXT
- Setup: — · Start: —

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (SIT): Cane Payment runtime อ่าน active config นี้ | — | API-EXT GET /payment-settings/active?season=&product= ส่ง K/ดอกเบี้ยต่อวัน/ค่าธนาคาร/ตารางวันจ่าย ให้ Payment ใช้คำนวณจริง (prototype ไม่มี handoff) | ☐ (ต้อง simulate) |

### TC-XT-04 — daily_rate = roundUp(rate/base,7) (XT-04)
- group: XT · ความสำคัญ: สูง · trace: XT-04 / AC-03 / FN-DAILY
- Setup: F5 · Start: OPEN หน้า (general)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY สูตร client-side | — | ดอกเบี้ยต่อวัน = **0.0191781** (7/365 ปัดขึ้น 7 ตำแหน่ง) · เปลี่ยนเป็น 10/365 → **0.0273973** | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): BE คำนวณ daily_rate ตอน save | — | ค่า persist = roundUp(rate_year/base_days,7) ฝั่ง BE (prototype = client readonly) | ☐ (ต้อง simulate) |

### TC-XT-05 — unique Active / overlap / lock / RBAC / VR-04 (XT-05 / AC-23 / EC-05/12/13/14) (ต้อง simulate)
- group: XT · ความสำคัญ: สูงสุด · trace: XT-05 / AC-23 / VR-04, VR-06(overlap), VR-08 / EC-05, EC-12, EC-13, EC-14
- Setup: — · Start: —

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (SIT) Save ทับ Active ที่มีอยู่แล้ว (season×product) | — | 409 **มีการตั้งค่า Active สำหรับรอบหีบ+สินค้านี้อยู่แล้ว** | ☐ (ต้อง simulate) |
| 2 | (SIT) Green schedule ช่วงซ้อนทับ | — | **ช่วงวันที่ซ้อนทับกัน** (prototype ตรวจแค่ from≤to) | ☐ (ต้อง simulate) |
| 3 | (SIT) ค่าธนาคารติดลบ | — | **ค่าธนาคารต้องไม่ติดลบ** (prototype ไม่ validate) | ☐ (ต้อง simulate) |
| 4 | (SIT) Save ด้วย ETag เก่า | — | 412 **ข้อมูลไม่ตรงปัจจุบัน กรุณารีเฟรช** | ☐ (ต้อง simulate) |
| 5 | (SIT) Edit ตอน Inactive / role Operations/Auditor | — | guard 403 **คุณไม่มีสิทธิ์ดำเนินการนี้** · Receiving net+cane_type → Payment ใช้ config นี้ (chain SoT) | ☐ (ต้อง simulate) |

---

## Group MC — Microcopy / drift / regression

### TC-MC-01 — header + context microcopy verbatim (regression)
- group: MC · ความสำคัญ: สูง · trace: §6.10 microcopy
- Setup: F5 · Start: OPEN หน้า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY header | — | **Payment Setting Configuration** + pill **ใช้งาน** · **แหล่งความจริงของค่าพื้นฐานที่ Cane Payment ใช้คำนวณ** · ปุ่ม **บันทึก** | ☐ |
| 2 | VERIFY context (drift check) | — | **ฤดูการหีบ (Crushing Season)** (ไม่ใช่ "รอบหีบ") · **Base @10CCS: 900.00 บาท/ตัน** (ไม่ใช่ "Base: 900.00") | ☐ |

### TC-MC-02 — inner-nav labels verbatim (regression)
- group: MC · ความสำคัญ: กลาง · trace: §6.10 sections
- Setup: F5 · Start: OPEN หน้า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY 6 label | — | **ข้อมูลทั่วไป · สูตรคำนวณ CCS · รายการหักเพิ่มเติม · ภาษี · ตารางกำหนดวันจ่าย · ทดสอบและดูตัวอย่าง** | ☐ |

### TC-MC-03 — payout เดือน render drift (พฤศจิกายน/ธันวาคม)
- group: MC · ความสำคัญ: สูง · trace: seed month 0-index drift
- Setup: F5 · Start: section Payout (green)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY เดือนใน seed | — | แถว render เป็น **พฤศจิกายน 2568** (แถว 1–2) · **ธันวาคม 2568** (แถว 3) — ไม่ใช่ ต.ค./พ.ย. (month เก็บ 0-index → THAI_MONTHS[10]=พฤศจิกายน) | ☐ |

### TC-MC-04 — Esc / backdrop ปิด modal (regression)
- group: MC · ความสำคัญ: กลาง · trace: Esc chain / closeModal
- Setup: F5 · Start: section Charges → CLICK **เพิ่มรายการ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | กด **Esc** | — | modal ปิด · ไม่มีแถวเพิ่ม · ตารางคงเดิม 2 แถว | ☐ |
| 2 | CLICK **เพิ่มรายการ** → CLICK backdrop (นอก modal) | — | modal ปิด (ไม่บันทึก) | ☐ |
| 3 | CLICK **เพิ่มรายการ** → CLICK **ยกเลิก** | — | modal ปิด | ☐ |

---

## Result Schema (สำหรับ AI runner สรุปผล)

```json
{
  "feature": "F-AGM-012",
  "total": 56,
  "runnable": 47,
  "simulate": 9,
  "cases": [
    { "id": "TC-NAV-01", "status": "pass|fail|blocked", "notes": "" }
  ]
}
```

**เกณฑ์ผ่าน:** ทุก Expected ในเคสตรงตามข้อความ verbatim บนจอ · เคส `(ต้อง simulate)` = ข้าม (บันทึก `blocked` + เหตุผล SIT) · เคส validate ต้องได้ toast ข้อความตรงเป๊ะ (ไม่ใช่แค่ "มี error")

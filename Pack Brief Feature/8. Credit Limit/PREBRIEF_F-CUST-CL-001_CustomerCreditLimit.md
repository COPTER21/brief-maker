# PREBRIEF · Customer Credit Limit — วงเงินเครดิตลูกค้า
> Sales Module (O2C) · Wave S2 · จาก WAVE_PLAN_SALES + Central Plan · 2026-08-13
> เอกสารนี้คือ source of truth เชิง business ของ feature — ข้อ [AI-DRAFT] รอเคาะผ่าน wireframe/หัวหน้า
> ประเภท: **Governance/Workflow** — เจ้าของวงเงินเครดิต + สายอนุมัติ (DOA) · ไม่ใช่ master ธรรมดา · ไม่ใช่เอกสารธุรกรรม
> DOA registration = **F-CL-001** (ดู DOA_BRIEF_F-CL-001.md) · pair: Customer Master ⑦ (F-CUST-001)

---

## 0. Obligations — พันธะจากต้นทาง (ทุกแถวต้องถูกอ้างกลับ)
| # | พันธะ | จาก | ตอบที่ § |
|---|---|---|---|
| OB-1 | **เจ้าของวงเงินเครดิต** — ตั้ง/ปรับวงเงินทำที่นี่ (⑦ อ่านอย่างเดียว) | มติ OQ-CM-01 RESOLVED (2026-08-13) | §2 S-01/S-02, §4 BR-13 |
| OB-2 | ทุกการตั้ง/ปรับวงเงินผ่าน **สายอนุมัติ DOA** ตามจำนวนเงิน | knowledge contract · doa:1 amt:1 | §2 S-04..07, §4 BR-01/03 |
| OB-3 | สิทธิ์อนุมัติ (ใครเซ็นช่วงวงเงินไหน) **ตั้งที่ DOA (F-CL-001)** — ฟีเจอร์แค่เรียก resolve | DOA_Wiring_Guide · precedent Purchase | §4 BR-03/04, §10 |
| OB-4 | DOA เก็บแค่ **role-id** · ชื่อ/ลายเซ็นมาจาก My Profile ตอนเซ็น | กฎเหล็ก DOA | §4 BR-04 |
| OB-5 | ห้าม hardcode สายอนุมัติในฟีเจอร์ | กติกากลาง (DOA placeholder) | §2 S-23, §4 BR-03 |
| OB-6 | เส้นเข้า: profile เกิดจาก Customer Master ⑦ (1 ลูกค้า = 1 profile) | contract ⑦↔⑧ | §2 S-18, §4 BR-11 |
| OB-7 | เส้นเข้า: ยอดใช้ **อ่านจาก** ธุรกรรม (AR Invoice + SO ยังไม่วางบิล) | contract · ERP std | §2 S-16, §4 BR-07 |
| OB-8 | เส้นออก: วงเงินที่อนุมัติ → ⑦ Customer Master อ่านไปแสดง | contract ⑦↔⑧ | §4 BR-13, §9 |
| OB-9 | เส้นออก: credit check (block/warn ขายเชื่อ) ใช้วงเงินนี้ที่ **Sales Order ⑨** | knowledge contract | §4 BR-09, §9 |
| OB-10 | แจ้งเตือน (ntf:1) เมื่อคำขอเข้าสาย/อนุมัติ/ไม่อนุมัติ | WAVE (ntf:1) | §2 S-22 [AI-DRAFT] |
| OB-11 | pattern กลาง: audit append-only · fail-closed · DOA placeholder | cube-master-knowledge | §4, §7 |
| OB-12 | **สถานะกลาง** ทุกคนเห็นเหมือนกัน (ไม่มี My Approval รายคน) | มติแชท 2026-08-13 | §2 S-17, §4 BR-12 |

---

## 1. สรุป + ผู้ใช้ + สิทธิ์
ฟีเจอร์เจ้าของ **วงเงินเครดิตต่อลูกค้า** — เจ้าหน้าที่ตั้ง/ปรับวงเงินที่นี่ ผ่าน**สายอนุมัติ DOA** (สายเปลี่ยนตามจำนวนเงิน) · แสดงสถานะเครดิต ยอดใช้จริง (จาก AR) ความเสี่ยง และประวัติวงเงิน · เป็นแหล่งวงเงินที่ ⑦ Customer Master + Sales Order ⑨ อ้างถึง

| Role | เห็นอะไร | ทำอะไรได้ |
|---|---|---|
| เจ้าหน้าที่เครดิต/แอดมินขาย | ทะเบียนวงเงิน + รายละเอียด + AR | สร้างคำขอปรับวงเงิน · ระงับ/ปลดเครดิต · ทบทวน |
| ผู้อนุมัติ (role ตาม DOA) | คำขอที่รออนุมัติ (สถานะกลาง) | อนุมัติ/ไม่อนุมัติ ตามขั้นที่ตนมีสิทธิ์ (สิทธิ์จริงจาก DOA) |
> **สถานะกลาง** — ทุกคนเห็นคำขอ + ปุ่มอนุมัติเหมือนกัน · สิทธิ์เซ็นจริง resolve จาก role ใน DOA (prototype โชว์ให้ทุกคนเพื่อสาธิต flow)

---

## 2. Scenarios — ทุกกรณี (derive จาก D1-D6)
> D1(จำนวน)→S-04..07 (DOA tier) + S-15 (util) · D2(state)→S-09 (approve chain), S-10 (reject), S-11/12 (hold) · D3(validate)→S-08,S-10,S-11 · D4(เส้นเข้า)→S-18,S-16 · D5(เส้นออก)→§9 · D6[STD]→S-13 (review), risk/DSO

| S | ประเภท | ชื่อ | เกิดอะไร | **ข้อมูลที่ต้องมี** | ผลปลายทาง |
|---|---|---|---|---|---|
| S-01 | Happy | ตั้งวงเงินครั้งแรก (เงินสด → มีวงเงิน) | ลูกค้า limit 0 → ขอตั้ง → อนุมัติ | จำนวน* + เหตุผล* | ผ่าน DOA → วงเงินตั้งค่า · audit |
| S-02 | Happy | ปรับ**เพิ่ม**วงเงิน | ขอเพิ่ม → DOA → อนุมัติครบสาย | จำนวนใหม่ + เหตุผล | วงเงินเปลี่ยน (หลังครบสาย) |
| S-03 | Alt | ปรับ**ลด**วงเงิน | ขอลด → DOA | จำนวนใหม่ (< เดิม) | delta ติดลบ · เข้าสายเดียวกัน |
| S-04 | Alt (tier) | วงเงิน **≤200k** | resolve → 1 ขั้น | จำนวน | สาย = ผจก.ฝ่ายขาย (1) |
| S-05 | Alt (tier) | วงเงิน **≤1M** | resolve → 2 ขั้น | จำนวน | + ผอ.ฝ่ายขาย (2) |
| S-06 | Alt (tier) | วงเงิน **>1M** | resolve → 3 ขั้น | จำนวน | + CFO (3) |
| S-07 | Exception | วงเงิน**เกินเพดาน** DOA | resolve = no_amount_tier | จำนวนเกินสูงสุด | **block ส่ง** + แจ้งไปตั้งช่วงที่ DOA |
| S-08 | Exception | ส่งคำขอไม่ครบ | เหตุผลว่าง / จำนวนเท่าเดิม | — | ปุ่มส่ง disabled |
| S-09 | Happy | **อนุมัติทีละขั้น** | เซ็นผ่านทีละ step | — | advance step · **วงเงินเปลี่ยนเฉพาะเมื่อครบสาย** · audit ต่อขั้น |
| S-10 | Alt | **ไม่อนุมัติ** (reject) | เซ็นไม่ผ่าน | เหตุผล* | คำขอจบ (rejected) · **วงเงินคงเดิม** · audit |
| S-11 | Alt | **ระงับเครดิต** (hold) | บล็อกขายเชื่อใหม่ | เหตุผล* | hold=true · สถานะ "ระงับเครดิต" · (enforce ที่ SO ⑨) |
| S-12 | Alt | **ปลดระงับ** | คืนสิทธิ์ขายเชื่อ | เหตุผล* | hold=false · audit |
| S-13 | Alt | **ทบทวนเครดิต** (review) | ยืนยันโปรไฟล์ปัจจุบัน | — | last_review = วันนี้ · audit |
| S-14 | Happy (อ่าน) | ดูวงเงิน/ใช้/คงเหลือ/util | คำนวณจากธุรกรรมจริง | limit + open txns | คงเหลือ = limit − used · แถบเครดิต |
| S-15 | Alt (จำนวน) | สถานะการใช้: ปกติ/ใกล้เต็ม/เกิน | util ≥85%/>100% | — | สีเตือน · filter ใกล้เต็ม/เกิน |
| S-16 | Happy (อ่าน) | ดูธุรกรรม AR ที่กินเครดิต | ตาราง INV/SO ค้าง | เลขที่·ครบกำหนด·มูลค่า·ค้าง·วิธีชำระ | aging (ยังไม่ถึง/เกินกำหนด) · DSO |
| S-17 | Happy | list + filter + search + sort (**สถานะกลาง**) | filter สถานะ/ความเสี่ยง | — | ทุกคนเห็นสถานะเดียวกัน (ปกติ/รออนุมัติ/ระงับ) |
| S-18 | เส้นเข้า | ลูกค้าใหม่จาก ⑦ → auto profile | สร้างลูกค้าที่ ⑦ | รหัสลูกค้า | มา profile ที่นี่ (limit 0/เงินสด) รอตั้งวงเงิน |
| S-19 | Alt | ลูกค้าเงินสด (ไม่ใช้เครดิต) | limit 0 | — | แสดง "เงินสด" · ไม่มีแถบ/AR |
| S-20 | ไม่รองรับ | ตั้งวงเงิน**โดยไม่อนุมัติ** | — | — | **ไม่รองรับ** (ทุกการเปลี่ยนผ่าน DOA) · ยกเว้น OQ-CL-02 direct-set band |
| S-21 | ไม่รองรับ | แก้วงเงินที่ **Customer Master ⑦** | — | — | **ไม่รองรับโดยตั้งใจ** (⑦ read-only · ⑧ เจ้าของ) |
| S-22 | ไม่รองรับ | ลบ credit profile | — | — | **ไม่รองรับ** (profile ผูกลูกค้า · audit append-only) |
| S-23 | ไม่รองรับ | แก้สายอนุมัติในฟีเจอร์ | — | — | **ไม่รองรับ** (สิทธิ์ตั้งที่ DOA เท่านั้น) |

---

## 3. Data — full data dict

### 3.1 Credit Profile (1 ต่อลูกค้า · เจ้าของ limit)
| Field | ชนิด | บังคับ | Default | ที่มา | ที่มาข้อ |
|---|---|---|---|---|---|
| รหัส/ชื่อลูกค้า `code`/`name` | อ้างอิง ⑦ | auto | — | Customer Master ⑦ | [OB-6] |
| กลุ่ม/พนักงานขาย `group`/`rep` | อ้างอิง ⑦ | — | — | ⑦ | [OB-6] |
| วงเงินเครดิต `limit` | จำนวนเงิน | — | 0 | ตั้งผ่าน DOA ที่นี่ | [OB-1] |
| ระดับความเสี่ยง `risk` | enum | — | low | ประเมิน | low/mid/high [STD] |
| ระงับเครดิต `hold` | bool | — | false | action | [OB-9] |
| เงื่อนไขชำระ `payment_term` | soft-ref | — | เครดิต 30 วัน | ⑦/master | [STD] |
| ระยะเครดิต `credit_period` | จำนวนวัน | — | 30 | — | [STD] |
| ทบทวนล่าสุด `last_review` | วันที่ | — | — | action review | [STD] |
| คำขอค้าง `pending` | อ็อบเจ็กต์/null | — | null | action | ดู §3.2 |
| ประวัติ `audit[]` | รายการ | auto | [] | ระบบ | append-only [OB-11] |

### 3.2 คำขอปรับวงเงิน (pending request · เกิดตอน submit)
| Field | ชนิด | ที่มา |
|---|---|---|
| เลขคำขอ `req_id` (CLR-YYYY-NNNN) · วงเงินปัจจุบัน `current` · ขอเป็น `requested` · เหตุผล `reason`* · ผู้ขอ `by` · เวลา `at` | ระบบ+กรอก |
| สถานะ `status` (pending_approval/approved/rejected) | ระบบ |
| สายอนุมัติ `chain[]` = **snapshot จาก DOA resolve** {order, roles:[role-id], role(label), by, at, status(wait/pass/rej)} | DOA (F-CL-001) |
| ขั้นปัจจุบัน `step` | ระบบ |

### 3.3 ธุรกรรม AR (อ่านอย่างเดียว · จาก SO/Invoice)
เลขที่ · ประเภท(ใบแจ้งหนี้/คำสั่งขาย) · วันที่ · ครบกำหนด · วิธีชำระ · มูลค่า · ชำระแล้ว → **อ่าน** จาก Sales Order S4 / AR Invoice S6 (ตอนนี้ mock TXNS)

### 3.4 Computed / แสดงอย่างเดียว
- **ยอดใช้** = Σ (มูลค่า − ชำระ) ของ open txns = ใบแจ้งหนี้ค้าง + SO ยังไม่วางบิล
- **คงเหลือ** = limit − used · **util%** · **สถานะการใช้** ปกติ/ใกล้เต็ม(≥85%)/เกิน/เงินสด
- **aging** ยังไม่ถึง/เกินกำหนด · **DSO** (derived)

### 3.5 DOA (F-CL-001 · matrix ตั้งที่หน้า DOA)
- `resolveDoa(amount)` → steps[{roles:[role-id], type:approval}] ตาม tier วงเงิน · merged (ทุกแผนก) · top ไม่จำกัด
- role-id: `role-mgr-sales`/`role-dir-sales`/`role-cfo` (ต้องมีใน User Roles master)
- **amount ที่ส่ง = วงเงินใหม่ absolute** [AI-DRAFT · OQ-CL-01]

---

## 4. Business Rules
| BR | กติกา | พฤติกรรมเมื่อชน | scenario | ที่มา |
|---|---|---|---|---|
| BR-01 | ทุกการตั้ง/ปรับวงเงิน **ผ่านสายอนุมัติ DOA** | ส่งคำขอ → pending (ไม่เปลี่ยนทันที) | S-01..03 | [OB-2] |
| BR-02 | วงเงินเปลี่ยนจริง**เฉพาะเมื่ออนุมัติครบสาย** | ระหว่างสาย = คงเดิม | S-09 | [OB-2] |
| BR-03 | สาย resolve จาก **DOA (F-CL-001)** ตามวงเงิน — ไม่ hardcode | เกินเพดาน = block | S-04..07,S-23 | [OB-3/5] |
| BR-04 | DOA เก็บ role-id · ชื่อ/ลายเซ็นจาก My Profile ตอนเซ็น | — | S-09 | [OB-4] |
| BR-05 | เกินเพดาน DOA (no_amount_tier) → **block ส่ง** (fail-closed) | แจ้งไปตั้งที่ DOA | S-07 | [OB-11] |
| BR-06 | change/reject/hold/unhold **บังคับเหตุผล** | ปุ่มยืนยัน disabled จนกรอก | S-08,S-10,S-11 | [STD] |
| BR-07 | ยอดใช้ = ใบแจ้งหนี้ค้าง + SO ยังไม่วางบิล (derived) | — | S-14,S-16 | [OB-7] |
| BR-08 | สถานะการใช้ near ≥85% · over >100% · เงินสด (limit 0) | สีเตือน | S-15,S-19 | [STD] |
| BR-09 | credit hold **block ขายเชื่อใหม่** — enforce ที่ **Sales Order ⑨** | ที่นี่ตั้ง flag + audit | S-11 | [OB-9] |
| BR-10 | audit append-only ทุก action (ส่งคำขอ/อนุมัติ/ไม่อนุมัติ/ระงับ/ปลด/ทบทวน) | ไม่ลบประวัติ | ทุก S | [OB-11] |
| BR-11 | 1 ลูกค้า = 1 credit profile · **auto-create จาก ⑦** (default 0/เงินสด) | — | S-18 | [OB-6] |
| BR-12 | **สถานะกลาง** (ปกติ/รออนุมัติ/ระงับ) ทุกคนเห็นเหมือนกัน — ไม่มี My Approval รายคน | ปุ่มอนุมัติแสดงเมื่อมีคำขอค้างเสมอ | S-17 | [OB-12] |
| BR-13 | วงเงิน **read-only ที่ ⑦** (⑧ เจ้าของ) | ⑦ แก้ไม่ได้ | S-21 | [OB-1/8] |

---

## 5. State Machine
```
คำขอปรับวงเงิน:  (ไม่มี) → draft → pending_approval → approved  (วงเงินเปลี่ยน)
                                                    └→ rejected  (วงเงินคงเดิม)
บัญชีเครดิต:     active ⇄ hold (ระงับ/ปลด)
```
| จาก | ไป | ใครกด | เงื่อนไข | scenario |
|---|---|---|---|---|
| — | pending_approval | เจ้าหน้าที่ | กรอกจำนวน+เหตุผล · tier resolve ได้ | S-01..03 |
| pending (ขั้น n) | pending (ขั้น n+1) | ผู้อนุมัติขั้น n | เซ็นผ่าน (ยังไม่ครบสาย) | S-09 |
| pending (ขั้นสุดท้าย) | approved | ผู้อนุมัติขั้นสุดท้าย | เซ็นครบ → **วงเงินเปลี่ยน** | S-09 |
| pending | rejected | ผู้อนุมัติ | ไม่อนุมัติ + เหตุผล → **วงเงินคงเดิม** | S-10 |
| active | hold | เจ้าหน้าที่ | ระงับ + เหตุผล | S-11 |
| hold | active | เจ้าหน้าที่ | ปลด + เหตุผล | S-12 |
> วงเงินไม่ผูกกับ state ของ profile — เปลี่ยนผ่านคำขอ+DOA เท่านั้น

---

## 6. Actions ต่อหน้า
| หน้า | action | enable เมื่อ | ผล |
|---|---|---|---|
| List | ค้นหา/filter (สถานะ·ความเสี่ยง)/sort | เสมอ | กรอง (สถานะกลาง) |
| List row | เปิดดูโปรไฟล์ | เสมอ | drawer |
| View · header | ปรับวงเงิน | เสมอ | เปิด change drawer |
| View · header | ระงับ/ปลดเครดิต | เสมอ | modal (บังคับเหตุผล) |
| View · header | ทบทวนเครดิต | เสมอ | update last_review |
| View · แท็บอนุมัติ | อนุมัติขั้น N / ไม่อนุมัติ | มีคำขอค้าง | advance / reject (บังคับเหตุผล) |
| Change drawer | ส่งอนุมัติ | จำนวน≠เดิม + เหตุผล + tier resolve ได้ | สร้าง pending · เข้าสาย DOA |

---

## 7. Data behaviour
- **DOA placeholder** — สายจาก resolve (F-CL-001) ไม่ hardcode · role-id · fail-closed (เกินเพดาน block)
- **append-only audit** ทุก action · **soft state** (hold ไม่ลบ) · วงเงิน/ธุรกรรม = อ่านข้าม feature
- เลขคำขอ CLR-YYYY-NNNN (auto)

---

## 8. Mock Data Spec — พิสูจน์ทุก scenario
| ชุด | prove |
|---|---|
| 0033 ธนาโฮเรก้า 1.2M · pending →1.5M (tier 3 · ผ่านขั้น 1 แล้ว) | S-06,S-09 (chain 3 ขั้น) |
| 0021 วิชัยเทรด 500k · pending →800k (tier 2 · step 0) | S-05,S-10 |
| 0012 สมชาย 80k · **hold** · util 89% (ใกล้เต็ม) + overdue | S-11,S-15,S-16 |
| 0055 เมธี 150k (tier 1) | S-04,S-02 |
| 0056 กัลยา **เงินสด (0)** | S-19,S-01 (ตั้งครั้งแรก) |
| 0044/0061/0058 วงเงินปกติหลากระดับ | S-14,S-17 |
> ทุกรายผูกรหัสลูกค้าจริงจาก ⑦ (contract codesMatch ✓)

---

## 9. Edges + ผลปลายทาง
| ทิศ | คู่ | จุดใน UI | ผลปลายทาง |
|---|---|---|---|
| เข้า | ⑦ สร้างลูกค้า → auto profile | (list เพิ่มราย) | profile ใหม่ limit 0 |
| เข้า | SO/Invoice → ยอดใช้ | แท็บ AR | คงเหลือ/util เปลี่ยนตาม |
| เข้า | DOA (F-CL-001) → สายอนุมัติ | change/approval | สายเปลี่ยนตามวงเงิน+matrix |
| ออก | วงเงินอนุมัติ → ⑦ Customer Master | (⑦ อ่านแสดง) | ⑦ แสดงวงเงินล่าสุด |
| ออก | วงเงิน → Sales Order ⑨ credit check | (SO ตอนเปิดบิล) | block/warn ถ้าเกิน/hold |

---

## 10. OQ + [AI-DRAFT] register
| # | ประเด็น | เจ้าภาพ |
|---|---|---|
| OQ-CL-01 | amount ที่ส่ง resolve = วงเงินใหม่ absolute (default) หรือส่วนต่างที่เพิ่ม | Strike |
| OQ-CL-02 | มี "ช่วงตั้งได้เลยไม่ต้องอนุมัติ" (tier 0 · approvers ว่าง) ไหม | Strike |
| OQ-CL-03 | role-dir-sales มีใน User Roles master | พี่เบิร์ด |
| OQ-CL-04 | ค่าช่วงวงเงิน 200k/1M เป็นจริงหรือ [DEFAULT] | Strike |
| OQ-CL-05 | ระงับ/ปลดเครดิต (hold) ผ่าน DOA ด้วยไหม หรือสิทธิ์ role-credit-officer ตรง | Strike/Compliance |
| OQ-CL-06 | เกณฑ์ risk (low/mid/high) มาจากไหน — ประเมินมือ หรือ auto จาก aging/DSO | Strike |
| OQ-CL-07 | ntf:1 — event แจ้งเตือน (คำขอเข้าสาย/อนุมัติ/ไม่อนุมัติ) ส่งใคร ช่องไหน | พี่เบิร์ด |
| CT-⑦↔⑧ | wire: ⑦ auto-create profile + อ่าน limit จาก ⑧ · used จาก SO/Invoice จริง | พี่เบิร์ด |

---

## 11. Coverage Matrix (ledger — gate)
| S | BR | transition | หน้าจอ/ปุ่ม | FN |
|---|---|---|---|---|
| S-01 | BR-01,02,03 | →pending→approved | change→ส่งอนุมัติ→อนุมัติ | FN-01,FN-09 |
| S-02 | BR-01,02 | →approved | ปรับเพิ่ม | FN-02 |
| S-03 | BR-01 | →pending | ปรับลด | FN-03 |
| S-04..06 | BR-03 | — | tier chip (1/2/3 ขั้น) | FN-04 |
| S-07 | BR-03,05 | — | block ส่ง | FN-05 |
| S-08 | BR-06 | — | ปุ่มส่ง disabled | FN-06 |
| S-09 | BR-02,04 | pending→approved | อนุมัติทีละขั้น | FN-09,FN-10 |
| S-10 | BR-06 | pending→rejected | ไม่อนุมัติ+เหตุผล | FN-11 |
| S-11 | BR-06,09 | active→hold | ระงับ | FN-12 |
| S-12 | BR-06 | hold→active | ปลด | FN-13 |
| S-13 | BR-10 | — | ทบทวน | FN-14 |
| S-14 | BR-07 | — | แถบเครดิต+คงเหลือ | FN-15 |
| S-15 | BR-08 | — | สถานะการใช้+filter | FN-16 |
| S-16 | BR-07 | — | ตาราง AR+aging+DSO | FN-17 |
| S-17 | BR-12 | — | list+filter (สถานะกลาง) | FN-18 |
| S-18 | BR-11 | — | (auto จาก ⑦) | FN-19 |
| S-19 | BR-08 | — | list "เงินสด" | FN-20 |
| S-20..23 | (ไม่รองรับ) | — | — | หมวด "ไม่รองรับ" |
> ผ่าน: BR-01..13 โผล่ ≥1 ✓ · transition (pending/approved/rejected/hold/active) ครบ ✓ · ทุก S รองรับมี FN ✓ · OB-1..12 ถูกอ้าง ✓

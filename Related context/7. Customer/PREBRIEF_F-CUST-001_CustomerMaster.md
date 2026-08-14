# PREBRIEF · Customer Master — ลูกค้า
> Sales Module (O2C) · Wave S2 · จาก WAVE_PLAN_SALES + Central Plan · 2026-08-13
> เอกสารนี้คือ source of truth เชิง business ของ feature — ข้อ [AI-DRAFT] รอเคาะผ่าน wireframe/หัวหน้า
> ประเภท: **Master (ทะเบียน)** — ไม่ใช่เอกสารธุรกรรม จึงไม่มี Header/Line grid แบบ B2 · แต่มีส่วน "อ่านค่า" จากฟีเจอร์อื่น (เครดิต ⑧ / ธุรกรรม AR)

---

## 0. Obligations — พันธะจากต้นทาง (ทุกแถวต้องถูกอ้างกลับ)
| # | พันธะ | จาก | ถูกตอบที่ § |
|---|---|---|---|
| OB-1 | เส้นเข้า: Prospect → convert → Customer (ต้องมีลูกค้าก่อนถึง convert ได้) | Central Plan / WAVE (มติ 2026-08-11) | §2 S-03, §9 |
| OB-2 | เส้นเข้า(เสริม): อ้างอิง Prospect ที่ยังไม่ convert ตอนสร้างลูกค้า | มติแชท 2026-08-13 | §2 S-02, §3.1, §9 |
| OB-3 | dep: Customer Group ⑥ (soft-ref picker) | WAVE (dep) | §3.1, §4 BR-06 |
| OB-4 | dep: Territory (soft-ref) + address dataset seed | WAVE (dep) | §3.1 |
| OB-5 | dep: Sales Team/Salesperson ⑩ (soft-ref · ยัง gap) | WAVE (dep) | §3.1, §10 OQ-CM-02 |
| OB-6 | เส้นออก: วงเงินเครดิต **อ่านจาก** Customer Credit Limit ⑧ (⑧ เป็นเจ้าของ + DOA) | knowledge contract 2026-08-13 | §2 S-12/S-15, §4 BR-01, §10 |
| OB-7 | เส้นออก: ยอดใช้เครดิต **อ่านจาก** ธุรกรรม (AR Invoice S6 + Sales Order S4 ยังไม่วางบิล) | knowledge contract · ERP std | §2 S-12/S-14, §4 BR-02 |
| OB-8 | เส้นออก: Customer เป็น master ให้ Quotation/SO/Invoice เลือกใช้ (soft-ref) | Central Plan §chain | §9 |
| OB-9 | Payment Terms (ACC·S0) + Payment Method (FIN·S0) = ประเภทการจ่าย (soft-ref) | WAVE done S0 | §3.1, §4 BR-06 |
| OB-10 | credit check (block/warn ขายเชื่อ) อยู่ที่ Sales Order ⑨ — **ไม่ใช่** ที่นี่ | knowledge contract | §4 BR-11, §2 S-13 |
| OB-11 | pattern กลาง: soft-ref LD-4C-02 · soft archive · audit append-only · DOA placeholder | cube-master-knowledge | §4, §5, §7 |
| OB-12 | OQ-CM-01 (วงเงินอยู่ ⑧ แยก หรือ inline) = RESOLVED → ยึด ⑧ แยก (SAP-style) | knowledge contract | §4 BR-01, §10 |

---

## 1. สรุป + ผู้ใช้ + สิทธิ์
ทะเบียนลูกค้ากลางของ Sales — เก็บข้อมูลลูกค้า (ติดต่อ/ที่อยู่/ภาษี), จับกลุ่ม-ช่องทาง-เขต-พนักงานขาย, และ **แสดงผล** วงเงินเครดิต + ธุรกรรมค้างชำระ (AR) เพื่อดูสถานะเครดิตก่อนขาย · เป็น master ที่เอกสารขายทุกใบอ้างถึง · รองรับที่มา 3 ทาง (convert จากลีด / อ้างอิงลีด / สร้างเอง) [แผน]

| Role | เห็นอะไร | ทำอะไรได้ |
|---|---|---|
| พนักงานขาย/แอดมินขาย | ทะเบียน + รายละเอียด + เครดิต/AR | สร้าง · แก้ไข · เก็บถาวร/กู้คืน · นำเข้า/ส่งออก |
| ผู้ดูราคา/เครดิต (สิทธิ์เห็นเครดิต) | เห็นวงเงิน/ยอดใช้/AR | ดูอย่างเดียว — ปรับวงเงินไปทำที่ ⑧ [AI-DRAFT: การคุมสิทธิ์เห็นเครดิตอิง Roles & Permissions POL·S0] |

---

## 2. Scenarios — ทุกกรณีที่เกิดได้ (derive จาก D1-D6)
> บันทึกการ derive: D1(จำนวน)→S-13 (utilization) + S-08..10 (import rows) · D2(state)→S-06,S-07 · D3(validate)→S-05,S-10 · D4(เส้นเข้า)→S-01,S-02,S-03,S-16 · D5(เส้นออก)→S-12,S-14,S-15 + §9 · D6[STD]→S-18,S-19 (dedupe/ship-to) + credit-used สูตร

| S | ประเภท | ชื่อ | เกิดอะไร | **ข้อมูลที่ scenario นี้ต้องมี** | ผลปลายทาง |
|---|---|---|---|---|---|
| S-01 | Happy | สร้างลูกค้าใหม่ (สร้างเอง) | เพิ่มลูกค้าเข้าทะเบียน ไม่อ้างลีด | ชื่อ*·เบอร์*·กลุ่ม*·พนักงานขาย* + ข้อมูลเสริม | active · from_lead=null · ป้าย "สร้างเอง" · audit "สร้างลูกค้า" |
| S-02 | Alt | สร้างลูกค้า **อ้างอิงผู้สนใจ/ลีด** ที่ยังไม่ convert | เลือกลีดจาก picker → prefill ชื่อ+พนักงานขาย | ลีดที่เลือก (code·source) | from_lead set · ป้าย "จากลีด" · audit "สร้างลูกค้าจากลีด LEAD-xxxx" |
| S-03 | Alt (เส้นเข้า) | ลูกค้าเกิดจาก **convert ฝั่ง Prospect** | Prospect กด convert → สร้างลูกค้าที่นี่ | lead_code·source·วันที่·ผู้ทำ | ป้าย "จากลีด" · view แสดง lead-box + ปุ่มเปิดลีดต้นทาง |
| S-04 | Alt | แก้ไขลูกค้า | แก้ข้อมูลได้ทุกช่อง **ยกเว้นวงเงินเครดิต** (read-only) | ช่องที่แก้ | บันทึก · วงเงินคงเดิม · audit "แก้ไขข้อมูลลูกค้า" |
| S-05 | Exception | สร้าง/แก้ validation ไม่ผ่าน | ชื่อ/เบอร์/กลุ่ม/พนักงานขาย ว่าง | — | บล็อก + ไฮไลต์ช่องผิด + toast เตือน (กัน double-submit) |
| S-06 | Alt | เก็บถาวร (archive) ลูกค้า | soft — พักการใช้งาน | ยืนยันผ่าน modal · ถ้ามียอดค้าง = เตือนก่อน | status=archived · หายจาก list ปกติ · เห็นที่ filter "เก็บถาวร" · audit |
| S-07 | Alt | กู้คืน (restore) | คืนสถานะใช้งาน | — | status=active · audit |
| S-08 | Alt | นำเข้า CSV — **Merge (upsert by code)** | code ซ้ำ=อัปเดต · ไม่ซ้ำ=เพิ่ม | ไฟล์ 11 คอลัมน์ | รายงาน เพิ่ม/อัปเดต/ข้าม · audit ต่อราย |
| S-09 | Alt | นำเข้า CSV — **Replace** | ล้างทะเบียนเดิมก่อนโหลดใหม่ | ไฟล์ | ทะเบียนใหม่ทั้งชุด (destructive) |
| S-10 | Exception | นำเข้า CSV — บาง row ไม่ผ่าน | ชื่อ/เบอร์ว่าง หรือ กลุ่ม/พนักงาน/เงื่อนไข/วงเงินผิด | เหตุผลต่อแถว | ข้ามแถวเสีย · นับ ผ่าน/ไม่ผ่าน · ไม่ล้มทั้งไฟล์ |
| S-11 | Alt | ส่งออก CSV | export ตาม filter ปัจจุบัน | — | ไฟล์รวม payment_method/credit_used/credit_avail/from_lead |
| S-12 | Happy (อ่าน) | ดูวงเงิน + ยอดใช้ + คงเหลือ | คำนวณจากธุรกรรมจริง | limit(จาก⑧)·open txns | คงเหลือ = limit − used · util% · แถบเครดิต |
| S-13 | Alt (จำนวน) | สถานะเครดิต ปกติ/ใกล้เต็ม/เกิน | util ≥85% = ใกล้เต็ม · >100% = เกิน | — | สีเตือน · filter "ใกล้เต็ม/เกินวงเงิน" · (บล็อกจริงที่ SO ⑨) |
| S-14 | Happy (อ่าน) | ดูธุรกรรมที่กินเครดิต (AR) | ตารางใบแจ้งหนี้/คำสั่งขายค้าง | เลขที่·ประเภท·ครบกำหนด·มูลค่า·ค้าง·วิธีชำระ·สถานะ | aging (ยังไม่ถึง/เกินกำหนด) · DSO · แยกวิธีชำระ |
| S-15 | Alt (เส้นออก) | กดไปจัดการวงเงินที่ ⑧ | soft-link ข้ามฟีเจอร์ | รหัสลูกค้า | ตอนนี้ placeholder (toast) จน ⑧ พร้อม |
| S-16 | Alt | ลูกค้าเงินสด (ไม่ใช้เครดิต) | วงเงิน = 0 | — | list แสดง "เงินสด" · ไม่มีแถบเครดิต/AR |
| S-17 | Happy | ค้นหา/กรอง/เรียง | search + filter สถานะ/กลุ่ม/พนักงาน + sort รหัส/ชื่อ/คงเหลือ | — | list กรองถูก + empty state |
| S-18 | ไม่รองรับ | เตือนซ้ำตอนสร้าง (dedupe เลขภาษี/เบอร์) | — | — | **ยังไม่รองรับ** [AI-DRAFT][STD] — SAP/Odoo เตือน dup · OQ-CM-03 |
| S-19 | ไม่รองรับ | ที่อยู่จัดส่งหลายแห่ง (multiple ship-to) | — | — | **ยังไม่รองรับ** phase นี้ (1 bill + 1 ship) [AI-DRAFT][STD] · OQ-CM-04 |
| S-20 | ไม่รองรับ | แก้วงเงินเครดิตที่หน้านี้ | — | — | **ไม่รองรับโดยตั้งใจ** — วงเงินอยู่ ⑧ ผ่าน DOA [มติ OQ-CM-01] |
| S-21 | ไม่รองรับ | ลบลูกค้าถาวร | — | — | **ไม่รองรับ** — soft archive เท่านั้น (audit append-only) [กติกากลาง] |
| S-22 | ไม่รองรับ | เพิ่ม/แก้ผู้ติดต่อหลายคนในฟอร์ม | — | — | สร้างได้ 1 ผู้ติดต่อหลัก · view เป็น list · **จัดการหลายผู้ติดต่อยังไม่ทำ** [AI-DRAFT] · OQ-CM-05 |

---

## 3. Data — full data dict

### 3.1 Customer (header — master ไม่มี line grid)
| Field | ชนิด | บังคับ | Default | ที่มา | Validation | ที่มาข้อ |
|---|---|---|---|---|---|---|
| รหัสลูกค้า `code` | ข้อความ | auto | CUST-YYYY-NNNN | ระบบ | ไม่ซ้ำ · แก้ไม่ได้ | [แผน] |
| ประเภท `ctype` | enum | ✅ | นิติบุคคล | เลือก | นิติบุคคล/บุคคลธรรมดา | [แผน] |
| ชื่อลูกค้า `name` | ข้อความ | ✅ | — | กรอก | ไม่ว่าง | [แผน] |
| เลขผู้เสียภาษี `tax_id` | ข้อความ | ⬜ (นิติบุคคล) | — | กรอก | 13 หลัก (ไม่บังคับ) | [STD] |
| สำนักงาน `branch`/`branch_code` | enum | ⬜ | สำนักงานใหญ่/00000 | เลือก | — | [STD] |
| ผู้ติดต่อหลัก `contact` | ข้อความ | ⬜ | — | กรอก | — | [แผน] |
| เบอร์โทร `phone` | ข้อความ | ✅ | — | กรอก | ไม่ว่าง | [แผน] |
| อีเมล `email` | ข้อความ | ⬜ | — | กรอก | — | [แผน] |
| ที่อยู่ออกบิล `bill_addr` | ข้อความยาว | ⬜ | — | กรอก | — | [แผน] |
| ที่อยู่จัดส่ง `ship_addr` | ข้อความยาว | ⬜ | =ออกบิล | กรอก | — | [แผน] |
| กลุ่มลูกค้า `group` | soft-ref ⑥ | ✅ | — | picker | ต้องเลือกจาก master | [แผน] |
| ช่องทางการขาย `channel` | soft-ref | ⬜ | — | picker | — | [แผน] |
| พนักงานขาย `rep` | soft-ref ⑩ | ✅ | — | picker | ต้องเลือก | [แผน] |
| เขตขาย `territory` | soft-ref | ⬜ | — | picker | — | [แผน] |
| กลุ่มราคา `price_group` | enum | ⬜ | ราคาขายส่ง | เลือก | — | [STD] |
| เงื่อนไขชำระเงิน `payment_term` | soft-ref (ACC) | ⬜ | เครดิต 30 วัน | picker | — | [แผน·OB-9] |
| วิธีชำระเงิน `payment_method` | soft-ref (FIN) | ⬜ | โอนเงิน | picker | — | [แผน·OB-9] |
| วงเงินเครดิต `credit.limit` | จำนวนเงิน | — | 0 | **อ่านจาก ⑧** | **read-only** ที่นี่ | [มติ·OB-6] |
| สถานะ `status` | enum | auto | active | ระบบ | active/archived | [กติกากลาง] |
| ที่มา `from_lead` | อ็อบเจ็กต์/null | auto | null | convert/ref | {lead_code,source,at,by} | [OB-1,OB-2] |
| อ้างอิงผู้สนใจ `prospect_ref` | soft-ref (input) | ⬜ (create เท่านั้น) | — | picker (ลีดยังไม่ convert) | → set from_lead ตอนบันทึก | [OB-2] |
| ผู้ติดต่อ `contacts[]` | รายการ | ⬜ | [primary] | — | — | [แผน] |
| เอกสารแนบ `docs[]` | รายการ (ref Document Center) | ⬜ | [] | soft-ref | ไม่เก็บสำเนา | [แผน] |
| ประวัติ `audit[]` | รายการ | auto | [สร้าง] | ระบบ | append-only | [กติกากลาง] |

### 3.2 ธุรกรรม AR (อ่านอย่างเดียว — ไม่ได้เป็นเจ้าของ · จาก SO/Invoice)
| Field | ชนิด | ที่มา |
|---|---|---|
| เลขที่ `no` · ประเภท `type` (ใบแจ้งหนี้/คำสั่งขาย) · วันที่ · ครบกำหนด `due` · เงื่อนไข `term` · วิธีชำระ `method` · มูลค่า `amount` · ชำระแล้ว `paid` | อ่าน | Sales Order S4 / AR Invoice S6 (ตอนนี้ mock `TXNS`) |

### 3.3 Computed / แสดงอย่างเดียว
- **ยอดใช้เครดิต** = Σ (มูลค่า − ชำระแล้ว) ของธุรกรรม open = ใบแจ้งหนี้ค้าง + คำสั่งขายที่ยังไม่วางบิล [STD·OB-7]
- **คงเหลือใช้ได้** = วงเงิน − ยอดใช้ · **util%** = ยอดใช้/วงเงิน
- **สถานะเครดิต** = ปกติ / ใกล้เต็ม(≥85%) / เกิน(>100%) / เงินสด(วงเงิน 0)
- **Aging** = ยังไม่ถึงกำหนด (due ≥ วันนี้) / เกินกำหนด (due < วันนี้) · **DSO** (mock derived)

### 3.4 Config ที่ feature นี้อ่าน
- วงเงินเครดิต ← **Customer Credit Limit ⑧** (ยัง gap → mock) · เกณฑ์ near 85% = [AI-DRAFT] (ควร config ที่ ⑧/Sales Config)
- ธุรกรรม open ← Sales Order/AR Invoice (ยังไม่สร้าง → mock `TXNS`)
- master พjson: Customer Group/Channel/Territory/Salesperson/Payment Terms/Payment Method (soft-ref)

---

## 4. Business Rules
| BR | กติกา | พฤติกรรมเมื่อชน | scenario | ที่มา |
|---|---|---|---|---|
| BR-01 | วงเงินเครดิต **อ่านจาก ⑧ เท่านั้น** — แก้ที่ Customer Master ไม่ได้ | ช่อง read-only · edit ไม่ทับค่า | S-04,S-12,S-20 | [มติ·OB-6·OB-12] |
| BR-02 | ยอดใช้ = ใบแจ้งหนี้ค้าง + คำสั่งขายที่ยืนยันแล้วยังไม่วางบิล | derive อัตโนมัติ | S-12,S-14 | [STD·OB-7] |
| BR-03 | คงเหลือ = วงเงิน − ยอดใช้ · near ≥85% · over >100% | สี/ป้ายเตือน | S-13 | [STD] |
| BR-04 | บังคับ: ชื่อ·เบอร์·กลุ่ม·พนักงานขาย | บล็อกบันทึก + ไฮไลต์ | S-05,S-10 | [แผน] |
| BR-05 | รหัส auto CUST-YYYY-NNNN — ไม่แก้ | — | S-01 | [แผน] |
| BR-06 | soft-ref (LD-4C-02): group/channel/rep/territory/payterm/paymethod = picker เท่านั้น ไม่ FK validate | เลือกจาก master | S-01,S-04 | [กติกากลาง·OB-3/9] |
| BR-07 | เก็บถาวร = soft (status) · กู้คืนได้ · ไม่ลบถาวร | ผ่าน confirm modal | S-06,S-07,S-21 | [กติกากลาง] |
| BR-08 | import: Merge = upsert by code · Replace = ล้าง+โหลด · validate ต่อแถว | ข้ามแถวเสีย | S-08,S-09,S-10 | [แผน·STD] |
| BR-09 | from_lead set เมื่อ convert(ฝั่ง Prospect) หรือ ref ลีดตอนสร้าง · null = สร้างเอง | ป้าย "จากลีด"/"สร้างเอง" | S-01,S-02,S-03 | [OB-1,OB-2] |
| BR-10 | audit append-only ทุก create/edit/archive/restore/import | ไม่ลบประวัติ | ทุก S | [กติกากลาง·OB-11] |
| BR-11 | credit check (block/warn ขายเชื่อ) อยู่ที่ **Sales Order ⑨** ไม่ใช่ที่นี่ | ที่นี่แค่แสดงสถานะ | S-13 | [แผน·OB-10] |
| BR-12 | ปรับวงเงินเข้าสายอนุมัติ (DOA) ที่ ⑧ — placeholder ไม่ hardcode chain | soft-link ไป ⑧ | S-15,S-20 | [แผน·OB-11] |
| BR-13 | อ้างอิงลีด (prospect_ref) เลือกได้เฉพาะลีดที่ **ยังไม่ convert** · เลือกแล้ว prefill ชื่อ+พนักงานขาย | picker กรอง converted ออก | S-02 | [มติ·OB-2] |

---

## 5. State Machine
```
(สร้าง) → active ⇄ archived
                └ archived → active (กู้คืน)
```
| จาก | ไป | ใครกด | เงื่อนไข | scenario |
|---|---|---|---|---|
| — | active | แอดมิน/พนักงานขาย | บันทึกสร้างสำเร็จ (ผ่าน validate) | S-01,S-02,S-03 |
| active | archived | แอดมิน | ยืนยัน (เตือนถ้ามียอดค้าง) | S-06 |
| archived | active | แอดมิน | ยืนยันกู้คืน | S-07 |
> ไม่มีสถานะ draft (master ใช้งานทันทีเมื่อสร้าง) · ไม่มีสถานะลบถาวร · DOA ไม่เกี่ยวกับ state ของ master (เกี่ยวเฉพาะวงเงินที่ ⑧)

---

## 6. Actions ต่อหน้า
| หน้า | action | enable เมื่อ | ทำอะไร | toast/ผล |
|---|---|---|---|---|
| List | ค้นหา/filter/sort | เสมอ | กรองทะเบียน | list อัปเดต + empty state |
| List | สร้างลูกค้า | เสมอ | เปิดฟอร์มสร้าง | drawer |
| List | Import / Export CSV | เสมอ | นำเข้า/ส่งออก | modal / ดาวน์โหลด |
| List row | แก้ไข / เก็บถาวร / กู้คืน | ตามสถานะ | เปิด edit / archive modal / restore | drawer/modal + toast |
| View drawer | สลับแท็บ (ภาพรวม/ที่อยู่-ผู้ติดต่อ/เครดิต&ธุรกรรม/เอกสาร/ประวัติ) | เสมอ | แสดงข้อมูล | — |
| View · แท็บเครดิต | จัดการวงเงินที่ ⑧ | เสมอ | soft-link ไป ⑧ | toast (placeholder) |
| View · ภาพรวม (จากลีด) | เปิดลีดต้นทาง | มี from_lead | soft-link ไป Prospect | toast (placeholder) |
| Form | บันทึก | ผ่าน validate | สร้าง/แก้ | toast + กัน double-submit |
| Form (create) | เลือกอ้างอิงลีด | เสมอ | prefill + set from_lead | — |

---

## 7. Data behaviour
- **เลขรัน** CUST-YYYY-NNNN (auto · ปี พ.ศ. ในหน้าจอ) · **soft reference LD-4C-02** ทุก master field (picker ไม่ FK) · **soft archive** (status ไม่ลบ) · **audit append-only** · **Document Center** แนบไฟล์แบบ ref ไม่เก็บสำเนา · วงเงิน/ธุรกรรม = อ่านข้าม feature (ไม่เป็นเจ้าของ)

---

## 8. Mock Data Spec — ชุดข้อมูลที่ prove ทุก scenario
| ชุด | รายการ | prove scenario |
|---|---|---|
| CUST-2026-0055 เมธีเทรดดิ้ง (จาก LEAD-0009) วงเงิน 150k · ใช้ 82k (INV 45k + SO 37k) | จากลีด + เครดิตปกติ + AR 2 ใบ | S-03,S-12,S-14 |
| CUST-2026-0012 ร้านค้าปลีกสมชาย วงเงิน 80k · ใช้ 71.5k (89%) | ใกล้เต็มวงเงิน + มี overdue | S-13, aging |
| CUST-2026-0033 ธนาโฮเรก้า วงเงิน 1.2M · ใช้ 640k | เครดิตใหญ่ + SO ยังไม่วางบิล | S-12,S-14 |
| CUST-2026-0056 ร้านกัลยาพาณิชย์ (จาก LEAD-0010) เงินสด | จากลีด + เงินสด | S-03,S-16 |
| CUST-2026-0044 ซุปเปอร์มาร์เก็ตประสิทธิ์ (สร้างเอง) | สร้างเอง | S-01 |
| CUST-2026-0009 (archived) | เก็บถาวร/กู้คืน | S-06,S-07 |
| PROSPECTS_OPEN (LEAD-2026-0014..0018) ยังไม่ convert | picker อ้างอิงลีด | S-02 |
| CSV: code ซ้ำ 1 + ใหม่ 1 + เสีย 1 | import merge/validate | S-08,S-10 |
> ตัวเลข/ชื่อหน้าตาธุรกิจจริง · KPI (คงเหลือ/util/aging/DSO) คำนวณจากชุดนี้แล้วสมเหตุผล

---

## 9. Edges + Hotspot + ผลปลายทาง
| ทิศ | คู่ | จุดใน UI | เกิดอะไรที่ปลายทาง (wireframe demo แม้ mock) |
|---|---|---|---|
| เข้า | Prospect → Customer (convert) | ป้าย "จากลีด" + lead-box + ปุ่มเปิดลีด | เปิดลีดต้นทางที่ Prospect (placeholder) |
| เข้า | Prospect(ยังไม่ convert) → ref ตอนสร้าง | picker "อ้างอิงผู้สนใจ/ลีด" | prefill + set from_lead |
| ออก | Customer → ⑧ Credit Limit | ปุ่ม "จัดการวงเงินที่ ⑧" | เปิดหน้า ⑧ (placeholder) |
| ออก | Customer → Sales Order/Quotation | (soft-ref) | SO/QT เลือกลูกค้ารายนี้เป็น master |
| อ่าน | AR Invoice/SO → แท็บเครดิต | ตารางธุรกรรม | ยอดใช้/คงเหลือ/aging เปลี่ยนตามธุรกรรม (mock) |

---

## 10. OQ + [AI-DRAFT] register → pin
| # | ประเด็น | เจ้าภาพ | pin ที่ |
|---|---|---|---|
| OQ-CM-01 | วงเงินอยู่ ⑧ แยก vs inline | Strike | **RESOLVED** → ⑧ แยก (SAP) · knowledge |
| OQ-CM-02 | Salesperson soft-ref: bind master จริงเมื่อสร้าง ⑩ (Sales Team) | Architect/พี่เบิร์ด | §3.1 rep |
| OQ-CM-03 | dedupe ตอนสร้าง (เตือนซ้ำ เลขภาษี/เบอร์)? | Strike | S-18 [STD] |
| OQ-CM-04 | ที่อยู่จัดส่งหลายแห่ง (multiple ship-to)? | Strike/Chin | S-19 [STD] |
| OQ-CM-05 | จัดการผู้ติดต่อหลายคนในฟอร์ม (เพิ่ม/แก้/ลบ)? | Chin | S-22 |
| OQ-CM-06 | เกณฑ์ near 85% + tolerance ตั้งที่ไหน (⑧ / Sales Config)? | Strike | §3.4 [AI-DRAFT] |
| OQ-CM-07 | สิทธิ์เห็นวงเงิน/AR อิง Roles & Permissions อย่างไร | พี่เบิร์ด | §1 |
| CT-⑧ | Contract: ⑦ อ่าน credit_limit จาก ⑧ + ธุรกรรมจาก SO/Invoice (ตอนนี้ mock) | พี่เบิร์ด | OB-6,OB-7 |

---

## 11. Coverage Matrix (ledger — gate)
| S | BR ที่ใช้ | transition | หน้าจอ/ปุ่ม | FN |
|---|---|---|---|---|
| S-01 | BR-04,05,06,09,10 | →active | ฟอร์มสร้าง + บันทึก | FN-01,FN-11 |
| S-02 | BR-09,13 | →active | picker อ้างอิงลีด | FN-02 |
| S-03 | BR-09 | (มาจาก Prospect) | lead-box + ปุ่มเปิดลีด | FN-03 |
| S-04 | BR-01,06,10 | — | ฟอร์มแก้ (วงเงิน read-only) | FN-04,FN-12 |
| S-05 | BR-04 | — | validate | FN-13 |
| S-06 | BR-07,10 | active→archived | archive modal | FN-05 |
| S-07 | BR-07,10 | archived→active | ปุ่มกู้คืน + filter | FN-06 |
| S-08 | BR-08,10 | — | import merge | FN-07 |
| S-09 | BR-08 | — | import replace | FN-08 |
| S-10 | BR-04,08 | — | import validate | FN-09 |
| S-11 | — | — | export | FN-10 |
| S-12 | BR-01,02,03 | — | แท็บเครดิต (แถบ+คงเหลือ) | FN-14,FN-15 |
| S-13 | BR-03,11 | — | สีเตือน + filter ใกล้เต็ม | FN-16 |
| S-14 | BR-02 | — | ตารางธุรกรรม+aging+DSO | FN-17 |
| S-15 | BR-01,12 | — | ปุ่มไป ⑧ | FN-18 |
| S-16 | BR-03 | — | list "เงินสด" | FN-19 |
| S-17 | — | — | search/filter/sort | FN-20 |
| S-18..22 | (ไม่รองรับ) | — | — | หมวด "ไม่รองรับ" |
> ผ่าน: ทุก BR-01..13 โผล่ ≥1 แถว ✓ · ทุก transition (→active/archive/restore) โผล่ ✓ · ทุก S มี UI+FN (ยกเว้นกลุ่มไม่รองรับ ระบุชัด) ✓ · ทุก OB-1..12 ถูกอ้าง ✓

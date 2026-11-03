# AI Test Cases — F-TMP-001 แบบประเมินความพึงพอใจลูกค้า

ชุดทดสอบสำหรับ AI agent (browser-use/vision) รันบน prototype `feature.html` — anchor = ข้อความที่เห็นบนจอ (ตัวหนา) · ข้อมูลตัวอย่างทั้งหมดเป็นข้อมูลสมมติ · เคสที่ติด `[AI-DEFAULT]` = เกณฑ์มาจากมติที่ AI ตัดสินแทน (รอลูกค้าเซ็นยืนยัน OQ-02) ถ้า fail อาจแปลว่ามติผิด ไม่ใช่โค้ดผิด
> ⚠ [NO-BROWSER] รอบนี้ยังไม่ได้รัน verify_anchors.py — anchor เขียนจาก source HTML + inventory (UI Brief §9) · ต้อง verify บนเครื่องที่มี browser

## Meta
| Field | Value |
|---|---|
| Feature ID | F-TMP-001 (ชั่วคราว) |
| ชื่อ | แบบประเมินความพึงพอใจลูกค้า (FM-SAL-06) |
| เวอร์ชัน | v1.0 (2026-10-08) |
| App entry | feature.html |
| Routes | `#/customer-satisfaction` · `#/customer-satisfaction/new` · `#/customer-satisfaction/view/:id` |
| ที่มา | FRD_F-TMP-001_Pack (FULL) · BRD-TMP-001 · HTML · DECISIONS.lock |
| จำนวนเคส | 52 |
| ตัวสลับผู้ใช้ | มุมขวาบน หรือ `__QA__.setMe`: สมหญิง ตั้งใจงาน (E01 เจ้าของ) · วิชัย ขายดี (E02 พนักงานอื่น) · ประเสริฐ มั่นคง (E03 role-mgr-sales) |

## Coverage
| group | เคส | สูง/กลาง/ต่ำ |
|---|---|---|
| รายการ | 8 | 1/4/3 |
| สร้าง | 8 | 3/4/1 |
| ตรวจข้อมูล | 5 | 2/3/0 |
| ไฟล์ | 2 | 0/2/0 |
| ส่ง | 4 | 2/2/0 |
| ยกเลิก | 4 | 1/2/1 |
| สิทธิ์ | 5 | 3/2/0 |
| PDF | 4 | 1/1/2 |
| ขอบ | 6 | 0/2/4 |
| ล็อกมติ | 4 | 0/2/2 |
| ข้ามโมดูล | 2 | 0/0/2 |

## Coverage Ledger
### AC (06_TESTS)
| item | cases |
|---|---|
| AC-01 | TC-C03 |
| AC-02 | TC-V01 |
| AC-03 | TC-C04 |
| AC-04 | TC-V03 |
| AC-05 | TC-C01 |
| AC-06 | TC-C02 |
| AC-07 | TC-D01, TC-D02 |
| AC-08 | TC-X01 |
| AC-09 | TC-L01, TC-X03, TC-P03 |
| AC-10 | TC-K04 |
| AC-11 | TC-E01 |
| AC-12 | TC-F02 |
| AC-13 | TC-C08 |
### Business Rules (05_RULES)
| item | cases |
|---|---|
| BR-01 | TC-D01, TC-K02 |
| BR-02 | TC-L04, TC-C04 |
| BR-03 | TC-C05, TC-V03 |
| BR-04 | TC-C01, TC-S01, TC-S03 |
| BR-05 | TC-C02 |
| BR-06 | TC-L01, TC-P01 |
| BR-07 | TC-X02, TC-X03, TC-X04 |
| BR-08 | TC-S04, TC-D01 |
| BR-09 | TC-K01 |
| BR-10 | TC-K03 |
| BR-11 | TC-K03 |
| BR-12 | TC-K01 |
### Validation
| item | cases |
|---|---|
| VR-01 | TC-C02, TC-V01, TC-V04 |
| VR-02 | TC-V01, TC-V05 |
| VR-03 | TC-V01, TC-V02, TC-V05 |
| VR-04 | TC-V01, TC-V03, TC-V05 |
| VR-05 | TC-X01 |
| VR-06 | TC-F02 |
### Edge Cases
| item | cases |
|---|---|
| EC-01 | TC-C03, TC-E02 |
| EC-02 | TC-E03 |
| EC-03 | TC-V03 |
| EC-04 | TC-D04 |
| EC-05 | TC-E06 |
| EC-06 | TC-E01 |
| EC-07 | TC-S02, TC-E05 |
| EC-08 | — ข้าม (นอก scope — DOA กลางตั้งขั้น = enhancement (FRD EC-08)) |
### Permission (06 §6.2)
| item | cases |
|---|---|
| TC-D01 | TC-P01, TC-P02 |
| TC-D02 | TC-P01 |
| TC-D03 | TC-P05 |
| TC-D04 | TC-S03 |
| TC-D05 | TC-P04 |
### Cross-Module (XT)
| item | cases |
|---|---|
| XT-01 | TC-T01 |
| XT-02 | TC-T02 |
| XT-03 | TC-T02 |
### Scope Lock (DEC)
| item | cases |
|---|---|
| DEC-01 | TC-K03 |
| DEC-02 | TC-K03, TC-T02 |
| DEC-03 | TC-S01 |
| DEC-04 | TC-K02 |
| DEC-05 | TC-K01 |
| DEC-06 | TC-K01 |
| DEC-07 | TC-K03 |
| DEC-08 | TC-P01, TC-P03 |
| DEC-09 | TC-K03 |
| DEC-10 | TC-F01, TC-K03 |
| DEC-11 | TC-E06, TC-K02 |
| DEC-12 | TC-C04, TC-E03 |
| DEC-13 | TC-V03 |

## Data Sets
| ชุด | ฟิลด์ | ค่า |
|---|---|---|
| A (ครบ) | ร้าน / ประเภท / ระยะเวลา / คะแนน / ข้อเสนอแนะ | ซูเปอร์มาร์เก็ตสมมติ / Supermarket / 3-5 ปี / 4 ทุกข้อ / "ขอรอบส่งที่แน่นอน" |
| B (ร่าง) | ร้าน | ร้านทดสอบใหม่ (ไม่อยู่ในทะเบียน) |
### ไฟล์ทดสอบ (Files)
| ไฟล์ | ใช้ |
|---|---|
| ภาพหน้าร้าน.jpg | ไฟล์ถูกต้อง |
| bad-file.exe | ชนิดไม่รองรับ |

## Test Cases

### กลุ่ม: รายการ

#### TC-L01 — รายการแสดงตามสิทธิ์ของเจ้าของ
- group: รายการ · ความสำคัญ: สูง · trace: AC-09 / FN-08 / BR-06
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=มาตรฐาน 10 ใบ
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 6 ใบของตัวเอง (auto: e2e S2)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | VERIFY badge ข้างคำอธิบาย | — | **6 รายการ · ร่าง 2** | ☐ |
| 3 | VERIFY ไม่มีแถว **CSE-2569-0006** | — | ไม่พบร่างของคนอื่น (วิชัย) | ☐ |

#### TC-L02 — ค้นหาด้วยชื่อร้าน
- group: รายการ · ความสำคัญ: กลาง · trace: FN-08 / API-01
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=มาตรฐาน
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เหลือแถวที่ตรงคำค้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | TYPE → ช่อง **ค้นหาเลขที่ / ห้าง-ร้านค้า / ผู้บันทึก...** | ไฮเปอร์ทดสอบ | เหลือ 1 แถว **CSE-2569-0005** | ☐ |

#### TC-L03 — กรองสถานะ = ส่งแล้ว
- group: รายการ · ความสำคัญ: กลาง · trace: FN-08
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=มาตรฐาน
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เหลือเฉพาะใบส่งแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | SELECT **สถานะทั้งหมด** → **ส่งแล้ว** | — | เหลือ 3 แถว pill **ส่งแล้ว** | ☐ |

#### TC-L04 — กรองประเภทธุรกิจ + รีเซ็ต
- group: รายการ · ความสำคัญ: กลาง · trace: FN-08 / BR-02
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=มาตรฐาน
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: กรองและรีเซ็ตได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | SELECT **ทุกประเภทธุรกิจ** → **Hypermarket** | — | เหลือ 2 แถว คอลัมน์ประเภทธุรกิจ = Hypermarket | ☐ |
| 3 | CLICK **รีเซ็ต** | — | กลับมา 6 แถว | ☐ |

#### TC-L05 — เรียงตามความพึงพอใจโดยรวม
- group: รายการ · ความสำคัญ: ต่ำ · trace: FN-08
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=มาตรฐาน
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สลับลำดับได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK หัวคอลัมน์ **ความพึงพอใจโดยรวม** | — | เรียงจากน้อยไปมาก แถวที่ยังไม่มีคะแนน (—) อยู่บน · ที่มีคะแนนเรียง 2 → 3 → 4 → 5 | ☐ |
| 3 | CLICK หัวคอลัมน์เดิมอีกครั้ง | — | เรียงกลับด้าน | ☐ |

#### TC-L06 — ไม่พบผลค้นหา = แผงว่าง
- group: รายการ · ความสำคัญ: ต่ำ · trace: FN-08 / U23
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=มาตรฐาน
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: มี empty state ไม่ใช่หัวตารางลอย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | TYPE → ช่องค้นหา | zzz | แผง **ไม่พบรายการที่ตรงกับเงื่อนไข** · footer **0 รายการ** | ☐ |

#### TC-L07 — pagination + แสดงต่อหน้า
- group: รายการ · ความสำคัญ: ต่ำ · trace: U6
- actor (role): ผู้จัดการฝ่ายขาย
- Setup: role=admin role-mgr-sales (ประเสริฐ มั่นคง · E03 · `__QA__.setMe('E03')`) · seed=มาตรฐาน
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: pager ทำงานแม้มี 1 หน้า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | SELECT **แสดงต่อหน้า** → 10 | — | footer **1 – 10 จาก 10 รายการ** · pager ‹ 1 › | ☐ |

#### TC-L08 — คลิกแถวเปิด drawer + ⋮
- group: รายการ · ความสำคัญ: กลาง · trace: P-03 / U5
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=มาตรฐาน
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เปิด drawer และเมนูได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK แถว **CSE-2569-0001** | — | drawer เปิด หัวข้อ **CSE-2569-0001** pill **ส่งแล้ว** · บรรทัดรอง **ความพึงพอใจโดยรวม 4/5** | ☐ |
| 3 | PRESS Esc | — | drawer ปิด | ☐ |
| 4 | CLICK ⋮ ของแถว **CSE-2569-0008** | — | เมนู **ดูรายละเอียด** · **แก้ไข** · **พิมพ์** · **ยกเลิกเอกสาร** | ☐ |

### กลุ่ม: สร้าง

#### TC-C01 — สร้างครบแล้วบันทึกและส่ง (happy path) [AI-DEFAULT]
- group: สร้าง · ความสำคัญ: สูง · trace: AC-05 / S-07 / BR-04 / FN-02 / FN-03
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=มาตรฐาน
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: ชุด A
- ผ่านเมื่อ: ได้เลข CSE-2569-0011 สถานะส่งแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | TYPE → ช่อง **1. ชื่อห้าง/ร้านค้า:** | ซูเปอร์ | popup แสดง **ซูเปอร์มาร์เก็ตสมมติ** | ☐ |
| 4 | CLICK **ซูเปอร์มาร์เก็ตสมมติ** ใน popup | — | ช่องชื่อร้านเติม · การ์ด **Supermarket** ถูกเลือก | ☐ |
| 5 | CLICK การ์ด **3-5 ปี** | — | การ์ด 3-5 ปี ถูกเลือก | ☐ |
| 6 | CLICK ปุ่ม **4** ทุกแถวทั้ง 9 หัวข้อ | — | การ์ดสรุป **ให้คะแนนแล้ว** = 9/9 | ☐ |
| 7 | TYPE → ช่อง **ท่านมีข้อเสนอแนะเพื่อการปรับปรุงหรือพัฒนาเพิ่มเติมหรือไม่?** | ชุด A ข้อเสนอแนะ | ข้อความแสดง | ☐ |
| 8 | CLICK **ถัดไป** | — | ขั้น **เอกสารแนบ** | ☐ |
| 9 | CLICK **ถัดไป** | — | ขั้น **ตรวจสอบและยืนยัน** · แถบไม่มีสายพิจารณา | ☐ |
| 10 | CLICK **บันทึกและส่ง** | — | modal **ส่งแบบประเมิน CSE-2569-0011** · ข้อความ **ไม่มีสายพิจารณา** | ☐ |
| 11 | CLICK **ยืนยันส่ง** | — | toast **ส่ง CSE-2569-0011 แล้ว** · แถวใหม่ pill **ส่งแล้ว** ลายเซ็น 1/1 | ☐ |

#### TC-C02 — บันทึกแบบร่างด้วยชื่อร้านอย่างเดียว
- group: สร้าง · ความสำคัญ: สูง · trace: AC-06 / S-08 / BR-05 / VR-01
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=มาตรฐาน
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: ชุด B
- ผ่านเมื่อ: ร่างได้เลขตอนบันทึกครั้งแรก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | TYPE → ช่อง **1. ชื่อห้าง/ร้านค้า:** | ร้านทดสอบใหม่ | ช่องมีข้อความ · popup **ไม่พบในทะเบียนลูกค้า — ใช้ชื่อที่พิมพ์ได้เลย** | ☐ |
| 4 | CLICK **บันทึกแบบร่าง** | — | toast **บันทึกร่าง CSE-2569-0011 แล้ว** · แถวใหม่ pill **ร่าง** | ☐ |

#### TC-C03 — เลือกร้านจากทะเบียนเติมประเภทธุรกิจ
- group: สร้าง · ความสำคัญ: กลาง · trace: AC-01 / S-01 / S-02 / EC-01
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ประเภทธุรกิจเติมให้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | CLICK ช่อง **1. ชื่อห้าง/ร้านค้า:** | — | popup รายชื่อลูกค้า 8 ราย | ☐ |
| 4 | CLICK **ร้านค้าส่งตัวอย่าง** | — | การ์ด **Wholesales** ถูกเลือก · การ์ดสรุป **ห้าง/ร้านค้า** = ร้านค้าส่งตัวอย่าง | ☐ |

#### TC-C04 — เลือกการ์ดได้ทีละ 1
- group: สร้าง · ความสำคัญ: กลาง · trace: AC-03 / BR-02 / DEC-12
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: single select ทั้ง 2 กลุ่ม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | CLICK การ์ด **Hypermarket** | — | Hypermarket ถูกเลือก | ☐ |
| 4 | CLICK การ์ด **Convenience** | — | Convenience ถูกเลือก · Hypermarket ไม่ถูกเลือก | ☐ |
| 5 | CLICK การ์ด **1-3 ปี** แล้ว **3-5 ปี** | — | เหลือ **3-5 ปี** ตัวเดียว | ☐ |

#### TC-C05 — ให้คะแนนอัปเดตการ์ดสรุปสด
- group: สร้าง · ความสำคัญ: กลาง · trace: S-04 / BR-03
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เปลี่ยนคะแนนได้ สรุปตาม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | CLICK ปุ่ม **5** ของแถว **ความพึงพอใจโดยรวมต่อบริษัทคู่ค้า** | — | การ์ดสรุป **ความพึงพอใจโดยรวม** = 5 · ดีมาก · **ให้คะแนนแล้ว** 1/9 | ☐ |
| 4 | CLICK ปุ่ม **3** แถวเดิม | — | เปลี่ยนเป็น 3 · ปานกลาง | ☐ |

#### TC-C06 — แก้ร่างของตัวเอง
- group: สร้าง · ความสำคัญ: สูง · trace: S-08 / FN-01 / U15
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=CSE-2569-0008 (ร่าง)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: prefill ค่าเดิม เลขเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK แถว **CSE-2569-0008** | — | drawer ปุ่ม **แก้ไข** **ส่งแบบประเมิน** | ☐ |
| 3 | CLICK **แก้ไข** | — | drawer ดูปิด · drawer แก้ไข kicker **แก้ไขเอกสาร** หัวข้อ **CSE-2569-0008** · ช่องร้าน = ร้านสะดวกซื้อตัวอย่าง | ☐ |
| 4 | CLICK การ์ด **มากกว่า 5 ปี** → CLICK **บันทึกแบบร่าง** | — | toast **บันทึกร่าง CSE-2569-0008 แล้ว** | ☐ |

#### TC-C07 — ย้อนขั้นจาก stepper
- group: สร้าง · ความสำคัญ: ต่ำ · trace: P-02 / #100F
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ข้อมูลไม่หาย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | TYPE → ช่อง **1. ชื่อห้าง/ร้านค้า:** | ซูเปอร์ | popup แสดง **ซูเปอร์มาร์เก็ตสมมติ** | ☐ |
| 4 | CLICK **ซูเปอร์มาร์เก็ตสมมติ** ใน popup | — | ช่องชื่อร้านเติม · การ์ด **Supermarket** ถูกเลือก | ☐ |
| 5 | CLICK การ์ด **3-5 ปี** | — | การ์ด 3-5 ปี ถูกเลือก | ☐ |
| 6 | CLICK ปุ่ม **4** ทุกแถวทั้ง 9 หัวข้อ | — | การ์ดสรุป **ให้คะแนนแล้ว** = 9/9 | ☐ |
| 7 | CLICK **ถัดไป** | — | ขั้น 2 | ☐ |
| 8 | CLICK วงกลมขั้น 1 ใน stepper | — | กลับขั้น **ข้อมูลแบบประเมิน** ค่าเดิมครบ | ☐ |

#### TC-C08 — ปิดตอนกรอกค้างต้องถาม
- group: สร้าง · ความสำคัญ: กลาง · trace: AC-13 / P-02
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: กันข้อมูลหายเงียบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | TYPE → ช่อง **1. ชื่อห้าง/ร้านค้า:** | ร้านค้าง | — | ☐ |
| 4 | PRESS Esc | — | popup ปิดก่อน | ☐ |
| 5 | PRESS Esc | — | modal **ทิ้งข้อมูลที่กรอกไว้?** | ☐ |
| 6 | CLICK **ทิ้งข้อมูล** | — | drawer ปิด ไม่มีแถวใหม่ | ☐ |

### กลุ่ม: ตรวจข้อมูล

#### TC-V01 — กดถัดไปตอนว่าง
- group: ตรวจข้อมูล · ความสำคัญ: สูง · trace: AC-02 / VR-01..04
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก + ช่อง invalid + toast (auto: e2e S7)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | CLICK **ถัดไป** | — | ยังอยู่ขั้น 1 · toast **กรอกข้อมูลไม่ครบ — กรุณาระบุชื่อห้าง/ร้านค้า** · ช่องร้านขอบแดง · การ์ดเลือกขอบแดง · แถวคะแนนขอบแดง | ☐ |

#### TC-V02 — ไม่เลือกระยะเวลา
- group: ตรวจข้อมูล · ความสำคัญ: กลาง · trace: VR-03
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อกเฉพาะข้อ 4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | TYPE → ช่อง **1. ชื่อห้าง/ร้านค้า:** | ร้าน V02 | — | ☐ |
| 4 | CLICK การ์ด **Supermarket** | — | — | ☐ |
| 5 | CLICK ปุ่ม **3** ทุกแถวทั้ง 9 หัวข้อ | — | การ์ดสรุป **ให้คะแนนแล้ว** = 9/9 | ☐ |
| 6 | CLICK **ถัดไป** | — | ข้อความ **กรุณาเลือกระยะเวลาที่ทำธุรกิจ 1 ข้อ** ใต้การ์ด | ☐ |

#### TC-V03 — ให้คะแนนไม่ครบ 9 ข้อ
- group: ตรวจข้อมูล · ความสำคัญ: สูง · trace: AC-04 / VR-04 / BR-03 / EC-03 / DEC-13
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ต้องครบ 9 หัวข้อ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | TYPE → ช่อง **1. ชื่อห้าง/ร้านค้า:** | ร้าน V03 | — | ☐ |
| 4 | CLICK การ์ด **Convenience** และ **น้อยกว่า 1 ปี** | — | — | ☐ |
| 5 | CLICK ปุ่ม **4** 8 แถวแรก | — | ให้คะแนนแล้ว 8/9 | ☐ |
| 6 | CLICK **ถัดไป** | — | ข้อความ **ยังไม่ได้ให้คะแนน 1 หัวข้อ** · แถว **ความพึงพอใจโดยรวมต่อบริษัทคู่ค้า** ขอบแดง | ☐ |

#### TC-V04 — บันทึกร่างโดยไม่มีชื่อร้าน
- group: ตรวจข้อมูล · ความสำคัญ: กลาง · trace: VR-01
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ร่างต้องมีชื่อร้าน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | CLICK **บันทึกแบบร่าง** | — | toast **กรุณาระบุชื่อห้าง/ร้านค้า** · ไม่มีแถวใหม่ | ☐ |

#### TC-V05 — ส่งร่างที่ยังไม่ครบจาก drawer
- group: ตรวจข้อมูล · ความสำคัญ: กลาง · trace: VR-02..04 / API-05
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=CSE-2569-0010 (ร่างไม่มีคะแนน)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ส่งไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK แถว **CSE-2569-0010** | — | แถบ **ให้คะแนนแล้ว 0/9** | ☐ |
| 3 | CLICK **ส่งแบบประเมิน** | — | modal แถบแดง **ข้อมูลยังไม่ครบ** | ☐ |
| 4 | CLICK **ยืนยันส่ง** | — | toast **ข้อมูลยังไม่ครบ — กลับไปแก้ไขก่อนส่ง** · pill ยังเป็น **ร่าง** | ☐ |

### กลุ่ม: ไฟล์

#### TC-F01 — แนบไฟล์ที่ถูกต้อง
- group: ไฟล์ · ความสำคัญ: กลาง · trace: S-06 / FN-09 / DEC-10
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · files=ภาพหน้าร้าน.jpg
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แนบได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | TYPE → ช่อง **1. ชื่อห้าง/ร้านค้า:** | ซูเปอร์ | popup แสดง **ซูเปอร์มาร์เก็ตสมมติ** | ☐ |
| 4 | CLICK **ซูเปอร์มาร์เก็ตสมมติ** ใน popup | — | ช่องชื่อร้านเติม · การ์ด **Supermarket** ถูกเลือก | ☐ |
| 5 | CLICK การ์ด **3-5 ปี** | — | การ์ด 3-5 ปี ถูกเลือก | ☐ |
| 6 | CLICK ปุ่ม **4** ทุกแถวทั้ง 9 หัวข้อ | — | การ์ดสรุป **ให้คะแนนแล้ว** = 9/9 | ☐ |
| 7 | CLICK **ถัดไป** | — | ขั้น **เอกสารแนบ** · **ยังไม่มีเอกสารแนบ** | ☐ |
| 8 | UPLOAD ภาพหน้าร้าน.jpg ผ่าน **คลิกเพื่อเลือกไฟล์** | ภาพหน้าร้าน.jpg | แถวไฟล์ **ภาพหน้าร้าน.jpg** | ☐ |

#### TC-F02 — ไฟล์ชนิดไม่รองรับ
- group: ไฟล์ · ความสำคัญ: กลาง · trace: AC-12 / VR-06
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · files=bad-file.exe
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่รับไฟล์ผิดชนิด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | TYPE → ช่อง **1. ชื่อห้าง/ร้านค้า:** | ซูเปอร์ | popup แสดง **ซูเปอร์มาร์เก็ตสมมติ** | ☐ |
| 4 | CLICK **ซูเปอร์มาร์เก็ตสมมติ** ใน popup | — | ช่องชื่อร้านเติม · การ์ด **Supermarket** ถูกเลือก | ☐ |
| 5 | CLICK การ์ด **3-5 ปี** | — | การ์ด 3-5 ปี ถูกเลือก | ☐ |
| 6 | CLICK ปุ่ม **4** ทุกแถวทั้ง 9 หัวข้อ | — | การ์ดสรุป **ให้คะแนนแล้ว** = 9/9 | ☐ |
| 7 | CLICK **ถัดไป** | — | ขั้นเอกสารแนบ | ☐ |
| 8 | UPLOAD bad-file.exe | bad-file.exe | toast **ไฟล์ไม่ผ่านเงื่อนไข: bad-file.exe** · ไม่มีแถวไฟล์ | ☐ |

### กลุ่ม: ส่ง

#### TC-S01 — ส่งร่างที่เติมครบ (DOA 0 ขั้น) [AI-DEFAULT]
- group: ส่ง · ความสำคัญ: สูง · trace: S-07 / BR-04 / DEC-03 / FN-03
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=CSE-2569-0008
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ส่งแล้ว = เสร็จ ไม่มีขั้นพิจารณา (auto: e2e S8)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK ⋮ ของ **CSE-2569-0008** → **แก้ไข** | — | drawer แก้ไข | ☐ |
| 3 | CLICK การ์ด **1-3 ปี** | — | — | ☐ |
| 4 | CLICK ปุ่ม **5** ทุกแถวทั้ง 9 หัวข้อ | — | การ์ดสรุป **ให้คะแนนแล้ว** = 9/9 | ☐ |
| 5 | CLICK **ถัดไป** 2 ครั้ง → **บันทึกและส่ง** | — | modal **ส่งแบบประเมิน CSE-2569-0008** ไม่มีแถวผู้พิจารณา | ☐ |
| 6 | CLICK **ยืนยันส่ง** | — | toast **ส่ง CSE-2569-0008 แล้ว** · pill **ส่งแล้ว** | ☐ |

#### TC-S02 — ส่งไม่สำเร็จ (ระบบขัดข้อง)
- group: ส่ง · ความสำคัญ: กลาง · trace: EC-07 / API-05
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · `__QA__.sim('error')` (ต้อง simulate)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สถานะไม่เปลี่ยน (auto: e2e S9)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | TYPE → ช่อง **1. ชื่อห้าง/ร้านค้า:** | ซูเปอร์ | popup แสดง **ซูเปอร์มาร์เก็ตสมมติ** | ☐ |
| 4 | CLICK **ซูเปอร์มาร์เก็ตสมมติ** ใน popup | — | ช่องชื่อร้านเติม · การ์ด **Supermarket** ถูกเลือก | ☐ |
| 5 | CLICK การ์ด **3-5 ปี** | — | การ์ด 3-5 ปี ถูกเลือก | ☐ |
| 6 | CLICK ปุ่ม **4** ทุกแถวทั้ง 9 หัวข้อ | — | การ์ดสรุป **ให้คะแนนแล้ว** = 9/9 | ☐ |
| 7 | CLICK **ถัดไป** 2 ครั้ง → **บันทึกและส่ง** | — | modal ส่ง | ☐ |
| 8 | VERIFY console `__QA__.sim('error')` แล้ว CLICK **ยืนยันส่ง** | — | toast **ส่งไม่สำเร็จ — ระบบขัดข้อง กรุณาลองใหม่ (สถานะเอกสารไม่เปลี่ยน)** · pill **ร่าง** | ☐ |

#### TC-S03 — ส่งแล้วแก้ไม่ได้ [AI-DEFAULT]
- group: ส่ง · ความสำคัญ: สูง · trace: BR-04 / TC-D04
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=CSE-2569-0001 (ส่งแล้ว)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ล็อกหลังส่ง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK แถว **CSE-2569-0001** | — | ไม่มีปุ่ม **แก้ไข** · มี **ยกเลิกเอกสาร** | ☐ |
| 3 | CLICK ⋮ ของแถว (ปิด drawer ก่อน) | — | เมนูไม่มี **แก้ไข** | ☐ |

#### TC-S04 — แท็บลายเซ็นหลังส่ง
- group: ส่ง · ความสำคัญ: กลาง · trace: BR-08 / U13
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=CSE-2569-0001
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: timeline มาตรฐาน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK แถว **CSE-2569-0001** → แท็บ **ลายเซ็น / อนุมัติ** | — | DOA entry **ไม่มีสายพิจารณา (DEC-03)** · ความคืบหน้า 1/1 · timeline **ส่งแบบประเมิน (ผู้ประเมิน)** pill **ส่งในระบบแล้ว** + วงกลมรูปคน **สมหญิง ตั้งใจงาน** | ☐ |

### กลุ่ม: ยกเลิก

#### TC-X01 — ยกเลิกต้องมีเหตุผล
- group: ยกเลิก · ความสำคัญ: สูง · trace: AC-08 / VR-05
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=CSE-2569-0002
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อกเมื่อไม่มีเหตุผล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK แถว **CSE-2569-0002** → **ยกเลิกเอกสาร** | — | modal **ยกเลิกเอกสาร CSE-2569-0002?** | ☐ |
| 3 | CLICK ปุ่ม **ยกเลิกเอกสาร** ใน modal | — | toast **กรุณาระบุเหตุผล** · กล่องเหตุผลขอบแดง | ☐ |

#### TC-X02 — ยกเลิกใบส่งแล้วของตน [AI-DEFAULT]
- group: ยกเลิก · ความสำคัญ: กลาง · trace: S-10 / BR-07 / FN-04
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=CSE-2569-0002
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ยกเลิกสำเร็จ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK แถว **CSE-2569-0002** → **ยกเลิกเอกสาร** | — | modal | ☐ |
| 3 | CLICK chip **ข้อมูลไม่ถูกต้อง** → CLICK **ยกเลิกเอกสาร** | — | toast **ยกเลิก CSE-2569-0002 แล้ว** · pill **ยกเลิก** · แถบ **ยกเลิกแล้ว — เหตุผล: ข้อมูลไม่ถูกต้อง** | ☐ |

#### TC-X03 — ผู้จัดการยกเลิกร่างของพนักงาน [AI-DEFAULT]
- group: ยกเลิก · ความสำคัญ: กลาง · trace: BR-07 / AC-09
- actor (role): ผู้จัดการฝ่ายขาย
- Setup: role=admin role-mgr-sales (ประเสริฐ มั่นคง · E03 · `__QA__.setMe('E03')`) · seed=CSE-2569-0006 (ร่างของวิชัย)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: admin ยกเลิกได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK แถว **CSE-2569-0006** | — | มี **ยกเลิกเอกสาร** ไม่มี **แก้ไข** | ☐ |
| 3 | CLICK **ยกเลิกเอกสาร** → chip **บันทึกซ้ำ** → **ยกเลิกเอกสาร** | — | pill **ยกเลิก** | ☐ |

#### TC-X04 — ใบยกเลิกแล้วไม่มีปุ่ม
- group: ยกเลิก · ความสำคัญ: ต่ำ · trace: BR-07
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=CSE-2569-0004 (ยกเลิก)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มี action

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK แถว **CSE-2569-0004** | — | แถบ **ยกเลิกแล้ว — เหตุผล: บันทึกซ้ำ** · ไม่มีปุ่ม **ยกเลิกเอกสาร** **แก้ไข** | ☐ |

### กลุ่ม: สิทธิ์

#### TC-P01 — พนักงานอื่นไม่เห็นร่างของ owner [AI-DEFAULT]
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D01 / TC-D02 / BR-06 / DEC-08
- actor (role): พนักงานขายอื่น
- Setup: role=พนักงานขายอื่น (วิชัย ขายดี · E02 · `__QA__.setMe('E02')`) · seed=มาตรฐาน
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นเฉพาะของตัวเอง (auto: e2e S2/S3)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | VERIFY badge | — | **3 รายการ · ร่าง 1** | ☐ |
| 3 | VERIFY ไม่มีแถว **CSE-2569-0008** และ **CSE-2569-0001** | — | ไม่เห็นร่างของคนอื่น และไม่พบใบส่งแล้วของคนอื่น | ☐ |

#### TC-P02 — เปิด route ใบที่ไม่มีสิทธิ์
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D01 / API-02
- actor (role): พนักงานขายอื่น
- Setup: role=พนักงานขายอื่น (วิชัย ขายดี · E02 · `__QA__.setMe('E02')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่เปิดเผยเอกสาร (auto: e2e S6)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | VERIFY console `__QA__.setMe('E02')` → เปลี่ยน URL เป็น `#/customer-satisfaction/view/r8` (ร่างของ E01) | — | ไม่เปิด drawer · toast **ไม่พบเอกสาร หรือคุณไม่มีสิทธิ์เห็นเอกสารนี้** | ☐ |

#### TC-P03 — admin เห็นทุกใบ [AI-DEFAULT]
- group: สิทธิ์ · ความสำคัญ: สูง · trace: AC-09 / S-11 / DEC-08
- actor (role): ผู้จัดการฝ่ายขาย
- Setup: role=admin role-mgr-sales (ประเสริฐ มั่นคง · E03 · `__QA__.setMe('E03')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นครบ 10

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | VERIFY badge | — | **10 รายการ · ร่าง 3** | ☐ |

#### TC-P04 — admin แก้ร่างคนอื่นไม่ได้
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: TC-D05
- actor (role): ผู้จัดการฝ่ายขาย
- Setup: role=admin role-mgr-sales (ประเสริฐ มั่นคง · E03 · `__QA__.setMe('E03')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แก้ได้เฉพาะเจ้าของ (auto: e2e S5)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK แถว **CSE-2569-0008** | — | ไม่มีปุ่ม **แก้ไข** และ **ส่งแบบประเมิน** | ☐ |

#### TC-P05 — พนักงานยกเลิกใบคนอื่นไม่ได้
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: TC-D03
- actor (role): พนักงานขายอื่น
- Setup: role=พนักงานขายอื่น (วิชัย ขายดี · E02 · `__QA__.setMe('E02')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีทางยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | VERIFY ไม่มีแถว **CSE-2569-0002** ให้กด | — | ไม่พบใบของคนอื่น → ยกเลิกไม่ได้ | ☐ |

### กลุ่ม: PDF

#### TC-D01 — PDF ใบส่งแล้ว [AI-DEFAULT]
- group: PDF · ความสำคัญ: สูง · trace: AC-07 / S-09 / FN-06 / BR-01 / BR-08
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=CSE-2569-0001
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ตรงแบบฟอร์ม + ไม่มี {{ }} (auto: e2e S4)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK แถว **CSE-2569-0001** → แท็บ **PDF Preview** | — | กระดาษ A4 หัวเรื่อง **แบบฟอร์มประเมินความพึงพอใจของบริษัทตัวอย่างการค้า จำกัด (มหาชน)** · ข้อ 2 = **บริษัท ตัวอย่างการค้า จำกัด (มหาชน)** · ☑ Hypermarket · ☑ 3-5 ปี · คะแนน 5 4 4 3 4 3 4 5 4 · ช่องลงชื่อ **ผู้ประเมิน** บรรทัด **ส่งในระบบ** · footer **Doc.No.FM-SAL-06** | ☐ |

#### TC-D02 — PDF ร่างมีป้ายร่าง
- group: PDF · ความสำคัญ: กลาง · trace: AC-07
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=CSE-2569-0008
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ร่างแยกออกชัด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK แถว **CSE-2569-0008** → แท็บ **PDF Preview** | — | footer **เลขที่ CSE-2569-0008 · ร่าง** · ช่องลงชื่อบรรทัด **วันที่ ........./........./.........** · คะแนนแถวที่ยังไม่ให้ว่าง | ☐ |

#### TC-D03 — พิมพ์จาก drawer
- group: PDF · ความสำคัญ: ต่ำ · trace: S-09 / API-07
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: พิมพ์ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK แถว **CSE-2569-0005** → ไอคอนพิมพ์ | — | หน้าต่างพิมพ์ของเบราว์เซอร์เปิด (ชื่อ CSE-2569-0005) | ☐ |

#### TC-D04 — PDF ข้อเสนอแนะยาว
- group: PDF · ความสำคัญ: ต่ำ · trace: EC-04
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · ใช้ `print/long-suggestion.data.json` (server render)
- Start: OPEN `print/` (server render)
- ชุดข้อมูล: —
- ผ่านเมื่อ: ยัง 1 หน้า (รอรันรอบเต็ม · NO-BROWSER)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY render `print/long-suggestion.data.json` ด้วย render_states.py บนเครื่องที่มี browser | — | 1 หน้า · กล่องข้อเสนอแนะตัดบรรทัด ไม่ล้น | ☐ |

### กลุ่ม: ขอบ

#### TC-E01 — แบบเอกสารปิดใช้
- group: ขอบ · ความสำคัญ: กลาง · trace: AC-11 / EC-06
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · `__QA__.setDocActive(false)` (ต้อง simulate)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สร้างไม่ได้ ดูได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | VERIFY console `__QA__.setDocActive(false)` | — | แถบแดง **แบบเอกสาร CSE ยังไม่เปิดใช้งาน** · ปุ่ม **สร้างแบบประเมิน** กดไม่ได้ | ☐ |

#### TC-E02 — ร้านไม่อยู่ในทะเบียน
- group: ขอบ · ความสำคัญ: กลาง · trace: EC-01
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=CSE-2569-0010
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ชื่อพิมพ์เองบันทึกได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK แถว **CSE-2569-0010** | — | ข้อ 1 = **ร้านใหม่ยังไม่อยู่ในทะเบียน** ไม่มีรหัสลูกค้า | ☐ |

#### TC-E03 — 3 ปีพอดีเลือก 3-5 ปี [AI-DEFAULT]
- group: ขอบ · ความสำคัญ: ต่ำ · trace: EC-02 / DEC-12
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: คำบนกระดาษคงเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | VERIFY ป้ายการ์ดข้อ 4 | — | ป้ายตรงกระดาษ **1-3 ปี** **3-5 ปี** (ไม่แก้คำ) · คู่มือ: 3 ปีพอดี เลือก 3-5 ปี | ☐ |

#### TC-E04 — Esc ปิด modal ก่อน drawer
- group: ขอบ · ความสำคัญ: ต่ำ · trace: U8
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed=CSE-2569-0008
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ลำดับ Esc ถูก (auto: e2e S10)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK แถว **CSE-2569-0008** → **ส่งแบบประเมิน** | — | modal เปิดบน drawer | ☐ |
| 3 | PRESS Esc | — | modal ปิด drawer ยังอยู่ | ☐ |
| 4 | PRESS Esc | — | drawer ปิด | ☐ |

#### TC-E05 — ส่งชนกัน (stale)
- group: ขอบ · ความสำคัญ: ต่ำ · trace: EC-07
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) (ต้อง simulate — ระดับ API)
- Start: OPEN API-05
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่ทับข้อมูล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY API-05 ด้วย version เก่า | — | 409 STALE · สถานะไม่เปลี่ยน | ☐ |

#### TC-E06 — ชื่อบริษัทเปลี่ยนหลังออกเลข [AI-DEFAULT]
- group: ขอบ · ความสำคัญ: ต่ำ · trace: EC-05 / DEC-11
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) (ต้อง simulate — ระดับ API)
- Start: OPEN API-07
- ชุดข้อมูล: —
- ผ่านเมื่อ: snapshot คงที่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY เปลี่ยน Organization.legal_name แล้วเปิด PDF ใบเดิม | — | ใบเดิมยังใช้ชื่อจาก header_snapshot | ☐ |

### กลุ่ม: ล็อกมติ

#### TC-K01 — ช่องตรงกระดาษ 1:1 [AI-DEFAULT]
- group: ล็อกมติ · ความสำคัญ: กลาง · trace: DEC-06 / BR-09 / DEC-05 / BR-12
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีช่องเกิน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | VERIFY ป้ายในฟอร์ม | — | **1. ชื่อห้าง/ร้านค้า:** · **3. ประเภทธุรกิจของบริษัทคู่ค้า:** · **4. ระยะเวลาที่ทำธุรกิจกับบริษัทคู่ค้า:** · 9 หัวข้อตามกระดาษ · **ท่านมีข้อเสนอแนะเพื่อการปรับปรุงหรือพัฒนาเพิ่มเติมหรือไม่?** · ไม่มีช่องหมายเหตุ/ช่องอื่น | ☐ |

#### TC-K02 — ชื่อบริษัทมาจากระบบ [AI-DEFAULT]
- group: ล็อกมติ · ความสำคัญ: กลาง · trace: DEC-04 / DEC-11 / BR-01
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีช่องให้พิมพ์ชื่อบริษัท

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | VERIFY การ์ดสรุป | — | **2. ชื่อบริษัทคู่ค้า** = **บริษัท ตัวอย่างการค้า จำกัด (มหาชน)** · **ชื่อบริษัทคู่ค้าอ่านจากข้อมูลบริษัท (Organization) — ไม่ต้องกรอก** | ☐ |

#### TC-K03 — ไม่มีทำซ้ำ · มี CSV [AI-DEFAULT]
- group: ล็อกมติ · ความสำคัญ: ต่ำ · trace: DEC-10 / BR-11 / BR-10 / DEC-01 / DEC-02 / DEC-07 / DEC-09
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ของเสริมตามมติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK ⋮ ของ **CSE-2569-0001** | — | ไม่มีเมนูทำซ้ำ | ☐ |
| 3 | CLICK **ส่งออก CSV** | — | toast **ส่งออก 6 รายการแล้ว** · ได้ไฟล์ customer-satisfaction.csv | ☐ |

#### TC-K04 — CSV ของ admin
- group: ล็อกมติ · ความสำคัญ: ต่ำ · trace: AC-10 / S-12 / FN-07
- actor (role): ผู้จัดการฝ่ายขาย
- Setup: role=admin role-mgr-sales (ประเสริฐ มั่นคง · E03 · `__QA__.setMe('E03')`)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ตามสิทธิ์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **ส่งออก CSV** | — | toast **ส่งออก 10 รายการแล้ว** | ☐ |

### กลุ่ม: ข้ามโมดูล

#### TC-T01 — แจ้งผู้จัดการเมื่อส่ง
- group: ข้ามโมดูล · ความสำคัญ: ต่ำ · trace: XT-01 / FN-05
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) · seed ENG-NOTIFY (ต้อง simulate)
- Start: OPEN `#/customer-satisfaction`
- ชุดข้อมูล: —
- ผ่านเมื่อ: event ยิงที่ draft→submitted

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/customer-satisfaction` | — | หัวข้อ **แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)** | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer กว้างเปิด หัวข้อ **สร้างเอกสารใหม่** · stepper 3 ขั้น **ข้อมูลแบบประเมิน** · **เอกสารแนบ** · **ตรวจสอบและยืนยัน** | ☐ |
| 3 | TYPE → ช่อง **1. ชื่อห้าง/ร้านค้า:** | ซูเปอร์ | popup แสดง **ซูเปอร์มาร์เก็ตสมมติ** | ☐ |
| 4 | CLICK **ซูเปอร์มาร์เก็ตสมมติ** ใน popup | — | ช่องชื่อร้านเติม · การ์ด **Supermarket** ถูกเลือก | ☐ |
| 5 | CLICK การ์ด **3-5 ปี** | — | การ์ด 3-5 ปี ถูกเลือก | ☐ |
| 6 | CLICK ปุ่ม **4** ทุกแถวทั้ง 9 หัวข้อ | — | การ์ดสรุป **ให้คะแนนแล้ว** = 9/9 | ☐ |
| 7 | CLICK **ถัดไป** 2 ครั้ง → **บันทึกและส่ง** → **ยืนยันส่ง** | — | toast **ส่ง CSE-2569-0011 แล้ว** (ระบบจริง: ประเสริฐได้รับแจ้ง cse_submitted) | ☐ |

#### TC-T02 — ไม่ส่งคะแนนต่อ CRM [AI-DEFAULT]
- group: ข้ามโมดูล · ความสำคัญ: ต่ำ · trace: XT-02 / XT-03 / DEC-02
- actor (role): เจ้าหน้าที่ขาย
- Setup: role=owner (สมหญิง ตั้งใจงาน · E01 · `__QA__.setMe('E01')`) (ต้อง simulate — ระดับ API)
- Start: OPEN API-05
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปิดรอบนี้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หลังส่ง (TC-C01) ไม่มีการเรียก API CRM/Customer | — | ไม่มี event `cse.submitted` ออกนอก module · Customer master อ่านอย่างเดียว | ☐ |

## วิธีที่ agent รัน (Run protocol)
1. เปิด `feature.html` ใหม่ทุกเคส (seed กลับค่าเริ่ม) · เริ่มที่ Start
2. สลับผู้ใช้ตาม Setup (`__QA__.setMe('E0x')` หรือเมนูมุมขวาบน)
3. เคส `(ต้อง simulate)` ใช้ console: `__QA__.sim('error')` / `__QA__.setDocActive(false)` · เคสระดับ API ทดสอบบนระบบจริง
4. ทำทีละ step เทียบ Expected ด้วยตา · ไม่ตรง = fail + จด evidence

## Coverage Audit
| หมวด | covered / total |
|---|---|
| AC (06_TESTS) | 13 / 13 |
| Business Rules (05_RULES) | 12 / 12 |
| Validation | 6 / 6 |
| Edge Cases | 7 / 8 |
| Permission (06 §6.2) | 5 / 5 |
| Cross-Module (XT) | 3 / 3 |
| Scope Lock (DEC) | 13 / 13 |

- **Manifest cross-check (FRD §0.12): ✅ 6/6** (ช่องในฟอร์ม · stories · rules · DEC · declaration · หน้าจอ)
### ข้าม (พร้อมเหตุผล)
- EC-08 — นอก scope — DOA กลางตั้งขั้น = enhancement (FRD EC-08)

## Result Report (schema)
```json
{"feature_id": "F-TMP-001", "run_at": "<iso>", "results": [{"id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": ""}], "summary": {"total": 52, "pass": 0, "fail": 0, "blocked": 0}}
```

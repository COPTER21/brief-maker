# AI Test Cases — F-TMP-003 ฟอร์มแจ้งงานขนส่งนอก

ชุดทดสอบสำหรับ AI agent (browser-use/vision) รันบน prototype `feature.html` — anchor = ข้อความที่เห็นบนจอ (ตัวหนา) · ข้อมูลตัวอย่างทั้งหมดเป็นข้อมูลสมมติ · เคสที่ติด `[AI-DEFAULT]` = เกณฑ์มาจากมติที่ AI ตัดสินแทน (รอลูกค้าเซ็นยืนยัน OQ-02) ถ้า fail อาจแปลว่ามติผิด ไม่ใช่โค้ดผิด

## Meta
| Field | Value |
|---|---|
| Feature ID | F-TMP-003 (ชั่วคราว) |
| ชื่อ | ฟอร์มแจ้งงานขนส่งนอก (FM-SAL-16) |
| เวอร์ชัน | v1.0 (2026-10-10) |
| App entry | feature.html |
| Routes | `#/outsourced-transport` · `#/outsourced-transport/create` · `#/outsourced-transport/edit/:id` · `#/outsourced-transport/view/:id` |
| ที่มา | FRD_F-TMP-003_Pack (STANDARD) · BRD-SAL-OTN-001 · HTML · DECISIONS.lock |
| จำนวนเคส | 32 |
| ตัวสลับผู้ใช้ | มุมขวาบน: สุนิสา ตัวอย่าง (เจ้าของ) · กิตติ สมมติ (Sales Admin คนอื่น) · วรวุฒิ ทองดี (ผู้จัดการฝ่ายขาย · เห็นทุกใบ) |

## Coverage
| group | เคส | สูง/กลาง/ต่ำ |
|---|---|---|
| รายการ | 6 | 1/2/3 |
| สร้างและส่ง | 6 | 3/2/1 |
| ตรวจข้อมูล | 4 | 2/2/0 |
| วันที่นัดส่ง | 2 | 1/1/0 |
| ไฟล์ | 1 | 0/1/0 |
| ยกเลิก | 3 | 0/3/0 |
| สิทธิ์ | 4 | 2/2/0 |
| PDF | 3 | 1/1/1 |
| แจ้งเตือน | 1 | 0/1/0 |
| ขอบ | 2 | 0/0/2 |

## Coverage Ledger
### AC (06_TESTS)
| item | cases |
|---|---|
| AC-01 | TC-L01, TC-C01, TC-C02 |
| AC-02 | TC-V01 |
| AC-03 | TC-C05, TC-V02 |
| AC-04 | TC-V03 |
| AC-05 | TC-C03 |
| AC-06 | TC-V04 |
| AC-07 | TC-C01, TC-C04, TC-K01 |
| AC-08 | TC-W01, TC-W02 |
| AC-09 | TC-D01, TC-D02 |
| AC-10 | TC-X01, TC-X03 |
| AC-11 | TC-L05 |
| AC-12 | TC-E01 |
### Business Rules (05_RULES)
| item | cases |
|---|---|
| BR-01 | TC-C05, TC-V02 |
| BR-02 | TC-C01, TC-C02 |
| BR-03 | TC-V03 |
| BR-04 | TC-W01, TC-W02 |
| BR-05 | TC-C01, TC-C04, TC-D03 |
| BR-06 | TC-C01 |
| BR-07 | — ข้าม (snapshot ชื่อผู้ขนส่ง ทดสอบระดับ API) |
| BR-08 | TC-X01, TC-X03 |
| BR-09 | TC-L01, TC-P01 |
| BR-10 | TC-D01 |
| BR-11 | TC-L05 |
| BR-12 | TC-D01 |
| BR-13 | — ข้าม (ไม่มีการเปลี่ยนค่า/ส่งต่อ ไม่มีอะไรให้ตรวจบน UI) |
### Validation
| item | cases |
|---|---|
| VR-01 | TC-V01 |
| VR-02 | TC-C01 |
| VR-03 | TC-V02 |
| VR-04 | TC-V03 |
| VR-05 | TC-V04 |
| VR-06 | TC-X02 |
### Edge Cases
| item | cases |
|---|---|
| EC-01 | TC-C05 |
| EC-02 | — ข้าม (เกิน 20 แถว/ใบต่อ ทดสอบที่แบบพิมพ์ (รอ OQ-05)) |
| EC-03 | — ข้าม (รอ OQ-06) |
| EC-04 | — ข้าม (snapshot ทดสอบระดับ API) |
| EC-05 | TC-E02 |
| EC-06 | TC-E01 |
| EC-07 | TC-W01 |
| EC-08 | TC-E02 |
### Scope Lock (DEC — 07 §7.0)
| item | cases |
|---|---|
| DEC-01 | — ข้าม (ไม่เปลี่ยนค่า — ไม่มีอะไรให้ตรวจบน UI) |
| DEC-02 | — ข้าม (ไม่ส่งต่อ) |
| DEC-03 | TC-C01, TC-D03 |
| DEC-04 | TC-V03 |
| DEC-05 | TC-D01 |
| DEC-06 | TC-D01 |
| DEC-07 | TC-D03 |
| DEC-08 | TC-L01, TC-P01, TC-P03 |
| DEC-09 | TC-C01 |
| DEC-10 | TC-F01, TC-L05 |
| DEC-11 | TC-D01 |
| DEC-12 | TC-V03 |
| DEC-13 | TC-W01 |
| DEC-14 | TC-C01 |
| DEC-15 | TC-D01 |
### Error Codes
| error | cases |
|---|---|
| LINES_INCOMPLETE | TC-V02 |
| QTY_INVALID | TC-V03 |
| NO_LINES | TC-V04 |
| NOT_FOUND | TC-P02 |
| NOT_DRAFT | TC-P04 |
| REASON_REQUIRED | TC-X02 |
| DOC_TYPE_INACTIVE | TC-E01 |
| STALE_VERSION | TC-E02 |
| NOT_OWNER | — ระดับ API (UI ไม่มีปุ่มส่งใบของผู้อื่น · TC-P03 ตรวจว่าไม่มีปุ่ม) |
### Permission Matrix (role × action)
| cell | cases |
|---|---|
| Sales Admin คนอื่น ดูใบ/ร่างของคนอื่น = deny | TC-P01, TC-P02 |
| ผู้จัดการ ดูทั้งหมด = allow | TC-P03 |
| ผู้จัดการ ส่งแจ้งงานแทน = deny | TC-P03 |
| เจ้าของ แก้ใบส่งแล้ว = deny | TC-P04 |
| เจ้าของ ยกเลิก = allow | TC-X01 |
| ผู้จัดการ ยกเลิก = allow | TC-X03 |

## Data Sets
| ชุด | ข้อมูล |
|---|---|
| ชุด A | ต้นทาง คลังสินค้า บางนา · ปลายทาง ร้านทดสอบการค้า (ชลบุรี) · เลขที่PO PO-TEST-0001 · จำนวน 120 |
| ชุด B | ต้นทาง โรงงาน วังน้อย · ปลายทาง ร้านทดสอบ 2 (สระบุรี) · เลขที่PO PO-TEST-0002 · จำนวน 0 · วันที่นัดส่ง วันพรุ่งนี้ |

### ไฟล์ทดสอบ (Files)
| ไฟล์ | ใช้ |
|---|---|
| test.exe | TC-F01 ชนิดไฟล์ไม่รองรับ |

## Test Cases

### กลุ่ม: รายการ

#### TC-L01 — รายการแสดงเฉพาะใบที่มีสิทธิ์เห็น (เจ้าของ) [AI-DEFAULT]
- group: รายการ · ความสำคัญ: สูง · trace: AC-01 · BR-09 · DEC-08
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นเฉพาะใบของตนเอง 7 ใบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport` | — | หน้า **ฟอร์มแจ้งงานขนส่งนอก** · badge **7 รายการ · ร่าง 2** | ☐ |
| 2 | VERIFY คอลัมน์ **ผู้จัดทำ** ทุกแถว | — | ทุกแถวเป็น **สุนิสา ตัวอย่าง** | ☐ |
| 3 | VERIFY แท็บ **ร่าง** | — | count = 2 | ☐ |

#### TC-L02 — segmented tabs กรองตามสถานะ
- group: รายการ · ความสำคัญ: กลาง · trace: 01 P-01 · #117
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แสดงเฉพาะสถานะที่เลือก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport` | — | แท็บ **ทั้งหมด** active | ☐ |
| 2 | CLICK แท็บ **ส่งแจ้งงานแล้ว** | — | ทุกแถว pill **ส่งแจ้งงานแล้ว** | ☐ |
| 3 | CLICK แท็บ **ยกเลิก** | — | ทุกแถว pill **ยกเลิก** | ☐ |

#### TC-L03 — ค้นหาด้วยเลขที่PO + รีเซ็ต
- group: รายการ · ความสำคัญ: กลาง · trace: 01 P-01 · API-01
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport`
- ชุดข้อมูล: เลขที่PO "PO-6909-0072"
- ผ่านเมื่อ: ค้นด้วยเลขที่PO แล้วเจอใบที่มี PO นั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport` | — | ตาราง | ☐ |
| 2 | TYPE ช่อง **ค้นหาเลขที่ / ผู้ขนส่ง / เลขที่PO / ปลายทาง** | PO-6909-0072 | เหลือ 1 แถว **OTN-2569-0007** | ☐ |
| 3 | CLICK **รีเซ็ต** | — | กลับมาครบ 7 แถว | ☐ |

#### TC-L04 — ค้นหาไม่เจอ = empty state
- group: รายการ · ความสำคัญ: ต่ำ · trace: 05 · U23
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แสดงแผงค้นหาไม่พบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport` | — | ตาราง | ☐ |
| 2 | TYPE ช่อง **ค้นหาเลขที่ / ผู้ขนส่ง / เลขที่PO / ปลายทาง** | zzzz | ข้อความ **ไม่พบรายการที่ค้นหา** + ปุ่ม **ล้างตัวกรอง** | ☐ |

#### TC-L05 — ส่งออก CSV 1 แถวต่อรายการ
- group: รายการ · ความสำคัญ: ต่ำ · trace: AC-11 · BR-11 · FN-08
- actor (role): admin (วรวุฒิ ทองดี · ผู้จัดการฝ่ายขาย)
- Setup: role=admin · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ได้ไฟล์ CSV

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport` | — | ตาราง 12 แถว | ☐ |
| 2 | CLICK **ส่งออก CSV** | — | toast **ส่งออก 12 ใบ** · ไฟล์ outsourced-transport.csv คอลัมน์ ต้นทาง/ปลายทาง/เลขที่PO/จำนวน/วันที่นัดส่ง | ☐ |

#### TC-L06 — กรองตามผู้ขนส่ง
- group: รายการ · ความสำคัญ: ต่ำ · trace: 01 P-01
- actor (role): admin (วรวุฒิ ทองดี · ผู้จัดการฝ่ายขาย)
- Setup: role=admin · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เหลือเฉพาะผู้ขนส่งที่เลือก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport` | — | ตาราง | ☐ |
| 2 | SELECT ตัวกรอง **ผู้ขนส่งทั้งหมด** | หจก. รถร่วมตัวอย่าง | ทุกแถวคอลัมน์ **ผู้ขนส่ง** = **หจก. รถร่วมตัวอย่าง** | ☐ |

### กลุ่ม: สร้างและส่ง

#### TC-C01 — สร้างใบแจ้งงานครบแล้วส่ง (happy path) [AI-DEFAULT]
- group: สร้างและส่ง · ความสำคัญ: สูง · trace: AC-01 · AC-07 · BR-02 · BR-05 · BR-06 · VR-02 · DEC-03 · DEC-09
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport`
- ชุดข้อมูล: ชุด A
- ผ่านเมื่อ: ได้เลข OTN สถานะส่งแจ้งงานแล้ว ไม่มีขั้นผู้พิจารณา

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport` | — | ตาราง | ☐ |
| 2 | CLICK **สร้างใบแจ้งงาน** | — | drawer กว้าง stepper 3 ขั้น **ข้อมูลหลักใบแจ้งงาน** · รอบวันที่ = วันนี้ | ☐ |
| 3 | SELECT ช่อง **ฟอร์มแจ้งงานขนส่งนอก (ผู้ขนส่ง)** | บริษัท ขนส่งตัวอย่าง จำกัด | การ์ดสรุปขวาแสดงผู้ขนส่ง | ☐ |
| 4 | TYPE แถว 1 ช่อง **ต้นทาง** / **ปลายทาง** / **เลขที่PO** / **จำนวน** | ชุด A | สรุปขวา **1 รายการ** · จำนวนรวม 120 | ☐ |
| 5 | SELECT แถว 1 **วันที่นัดส่ง** | วันพรุ่งนี้ | ไม่มีข้อความเตือนใต้แถว | ☐ |
| 6 | CLICK **ถัดไป** → CLICK **ถัดไป** | — | ขั้น **ตรวจสอบและยืนยัน** ตาราง 1 รายการ | ☐ |
| 7 | CLICK **บันทึกและส่งแจ้งงาน** | — | modal **ส่งแจ้งงานขนส่ง?** ข้อความ **เอกสารนี้ไม่มีขั้นอนุมัติ — ส่งแล้วมีผลทันทีและแก้ไขไม่ได้** ไม่มีแถวเลือกผู้พิจารณา | ☐ |
| 8 | CLICK **ส่งแจ้งงาน** | — | toast **ส่งแจ้งงานแล้ว · OTN-2569-0013** · แถวใหม่ pill **ส่งแจ้งงานแล้ว** | ☐ |

#### TC-C02 — บันทึกแบบร่างเมื่อยังไม่มีรายการ
- group: สร้างและส่ง · ความสำคัญ: สูง · trace: AC-01 · S-02 · BR-02
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ได้ร่างเลข OTN

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport` | — | ตาราง | ☐ |
| 2 | CLICK **สร้างใบแจ้งงาน** | — | drawer | ☐ |
| 3 | SELECT ช่อง **ฟอร์มแจ้งงานขนส่งนอก (ผู้ขนส่ง)** | หจก. รถร่วมตัวอย่าง | เลือกแล้ว | ☐ |
| 4 | CLICK **ถัดไป** → CLICK **ถัดไป** | — | แถบเตือน **ยังไม่มีรายการ — บันทึกแบบร่างได้ · ส่งแจ้งงานต้องครบทุกแถว** | ☐ |
| 5 | CLICK **บันทึกแบบร่าง** | — | toast **บันทึกร่างแล้ว** · แถวใหม่ pill **ร่าง** | ☐ |

#### TC-C03 — เพิ่มรายการยกต้นทางและวันที่นัดส่งจากแถวก่อน
- group: สร้างและส่ง · ความสำคัญ: กลาง · trace: AC-05 · 01 P-02
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แถวใหม่มีต้นทาง + วันที่นัดส่งเท่าแถวก่อน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/create` | — | drawer สร้าง ตาราง 3 แถว | ☐ |
| 2 | TYPE แถว 3 ช่อง **ต้นทาง** | คลังสินค้า บางนา | — | ☐ |
| 3 | SELECT แถว 3 **วันที่นัดส่ง** | วันพรุ่งนี้ | — | ☐ |
| 4 | CLICK **เพิ่มรายการ** | — | แถว 4 ต้นทาง **คลังสินค้า บางนา** · วันที่นัดส่งเท่าแถว 3 · เคอร์เซอร์อยู่ช่อง **ปลายทาง** | ☐ |

#### TC-C04 — ส่งร่างที่กรอกครบจากหน้าดู
- group: สร้างและส่ง · ความสำคัญ: สูง · trace: AC-07 · BR-05
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/view/R11`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ร่างกลายเป็นส่งแจ้งงานแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/view/R11` | — | drawer **OTN-2569-0011** pill **ร่าง** | ☐ |
| 2 | CLICK **ส่งแจ้งงาน** | — | modal **ส่งแจ้งงานขนส่ง?** | ☐ |
| 3 | CLICK **ส่งแจ้งงาน** ใน modal | — | pill **ส่งแจ้งงานแล้ว** · ข้อความล่าง **ส่งแจ้งงานแล้ว ล็อกแก้ไข** | ☐ |

#### TC-C05 — แก้ร่างที่แถวไม่ครบแล้วส่ง
- group: สร้างและส่ง · ความสำคัญ: กลาง · trace: AC-03 · BR-01 · EC-01
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/view/R12`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แก้ครบแล้วส่งได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/view/R12` | — | แบนเนอร์ **กรอกไม่ครบ 1 แถว** | ☐ |
| 2 | CLICK **แก้ไข** | — | drawer **แก้ไขใบแจ้งงาน OTN-2569-0012** | ☐ |
| 3 | TYPE แถว 2 ช่อง **ปลายทาง** / **เลขที่PO** / **จำนวน** | ร้านทดสอบ (ชลบุรี) / PO-TEST-02 / 30 | — | ☐ |
| 4 | SELECT แถว 2 **วันที่นัดส่ง** | 11 ต.ค. 2569 | — | ☐ |
| 5 | CLICK **ถัดไป** → CLICK **ถัดไป** → CLICK **บันทึกและส่งแจ้งงาน** → CLICK **ส่งแจ้งงาน** | — | pill **ส่งแจ้งงานแล้ว** | ☐ |

#### TC-C06 — ปิด drawer ตอนกรอกค้าง = ถามทิ้งข้อมูล
- group: สร้างและส่ง · ความสำคัญ: ต่ำ · trace: 01 P-02 · U25
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: มี modal ยืนยันก่อนทิ้ง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/create` | — | drawer | ☐ |
| 2 | TYPE แถว 1 ช่อง **ต้นทาง** | คลังสินค้า บางนา | — | ☐ |
| 3 | CLICK ปุ่ม **ยกเลิก** ท้าย drawer | — | modal **ทิ้งข้อมูลที่กรอกไว้?** | ☐ |
| 4 | CLICK **กลับไปกรอกต่อ** | — | drawer ยังอยู่ ข้อมูลไม่หาย | ☐ |

### กลุ่ม: ตรวจข้อมูล

#### TC-V01 — ไม่เลือกผู้ขนส่ง = บล็อก
- group: ตรวจข้อมูล · ความสำคัญ: สูง · trace: AC-02 · VR-01
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไปขั้นถัดไปไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/create` | — | drawer | ☐ |
| 2 | CLICK **ถัดไป** | — | ช่องผู้ขนส่งขอบแดง **กรุณาเลือกผู้ขนส่ง** · toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |

#### TC-V02 — แถวกรอกไม่ครบ = บล็อก + ข้อความใต้แถว
- group: ตรวจข้อมูล · ความสำคัญ: สูง · trace: AC-03 · BR-01 · VR-03
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บอกแถวที่ไม่ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/create` | — | drawer | ☐ |
| 2 | SELECT ช่อง **ฟอร์มแจ้งงานขนส่งนอก (ผู้ขนส่ง)** | บริษัท ส่งไวทดสอบ จำกัด | — | ☐ |
| 3 | TYPE แถว 1 ช่อง **ต้นทาง** | โรงงาน วังน้อย | — | ☐ |
| 4 | CLICK **ถัดไป** | — | ใต้แถว 1 **แถว 1: กรอกปลายทาง** · toast **กรอกรายการให้ครบ 5 ช่อง หรือลบแถวที่ไม่ใช้** | ☐ |

#### TC-V03 — จำนวน 0 = บล็อก [AI-DEFAULT]
- group: ตรวจข้อมูล · ความสำคัญ: กลาง · trace: AC-04 · BR-03 · VR-04 · DEC-04 · DEC-12
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/create`
- ชุดข้อมูล: ชุด B
- ผ่านเมื่อ: จำนวนต้องมากกว่า 0

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/create` | — | drawer | ☐ |
| 2 | TYPE แถว 1 ครบทุกช่อง แต่ **จำนวน** = 0 | ชุด B | — | ☐ |
| 3 | CLICK **ถัดไป** | — | ใต้แถว **แถว 1: จำนวนต้องเป็นจำนวนเต็มมากกว่า 0** · ช่องจำนวนขอบแดง | ☐ |

#### TC-V04 — ส่งใบที่ไม่มีรายการ = บล็อก
- group: ตรวจข้อมูล · ความสำคัญ: กลาง · trace: AC-06 · VR-05
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ส่งไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/create` | — | drawer | ☐ |
| 2 | SELECT ช่อง **ฟอร์มแจ้งงานขนส่งนอก (ผู้ขนส่ง)** | บริษัท ขนส่งตัวอย่าง จำกัด | — | ☐ |
| 3 | CLICK **ถัดไป** → CLICK **ถัดไป** → CLICK **บันทึกและส่งแจ้งงาน** | — | กลับขั้น 1 · toast **ต้องมีรายการงานขนส่งอย่างน้อย 1 รายการ** | ☐ |

### กลุ่ม: วันที่นัดส่ง

#### TC-W01 — วันที่นัดส่งก่อนรอบวันที่ = เตือน ไม่บล็อก [AI-DEFAULT]
- group: วันที่นัดส่ง · ความสำคัญ: สูง · trace: AC-08 · BR-04 · DEC-13 · EC-07
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/create`
- ชุดข้อมูล: ชุด A
- ผ่านเมื่อ: เตือนแต่ไปต่อได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/create` | — | drawer รอบวันที่ = วันนี้ | ☐ |
| 2 | SELECT ผู้ขนส่ง + TYPE แถว 1 ครบ | ชุด A | — | ☐ |
| 3 | SELECT แถว 1 **วันที่นัดส่ง** | เมื่อวาน | ใต้แถว **แถว 1: วันที่นัดส่งก่อนรอบวันที่ — บันทึกได้ (เตือน)** · สรุปขวา **1 รายการนัดส่งก่อนรอบวันที่** | ☐ |
| 4 | CLICK **ถัดไป** | — | ไปขั้น **เอกสารแนบ** ได้ | ☐ |

#### TC-W02 — ใบที่ส่งแล้วมีแถวนัดส่งก่อนรอบ = แบนเนอร์
- group: วันที่นัดส่ง · ความสำคัญ: กลาง · trace: AC-08 · BR-04
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แบนเนอร์เตือน + แถวสีเตือน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/view/R7` | — | แบนเนอร์ **มี 1 รายการที่วันที่นัดส่งก่อนรอบวันที่ — แจ้งผู้จัดการฝ่ายขายแล้ว** | ☐ |
| 2 | VERIFY ตาราง **รายการงานขนส่ง** แถว 2 | — | วันที่นัดส่ง 14 ก.ย. 2569 เป็นสีเตือน | ☐ |

### กลุ่ม: ไฟล์

#### TC-F01 — แนบไฟล์ชนิดไม่รองรับ
- group: ไฟล์ · ความสำคัญ: กลาง · trace: DEC-10 · Document Center
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=test.exe
- Start: OPEN `#/outsourced-transport/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไฟล์ไม่ถูกแนบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/create` | — | drawer | ☐ |
| 2 | SELECT ผู้ขนส่ง → CLICK **ถัดไป** | — | ขั้น **เอกสารแนบ** | ☐ |
| 3 | UPLOAD ที่ **คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)** | test.exe | toast **test.exe — ชนิดไฟล์ไม่รองรับ** · ไม่มีไฟล์ในรายการ | ☐ |

### กลุ่ม: ยกเลิก

#### TC-X01 — เจ้าของยกเลิกร่าง (เหตุผลบังคับ)
- group: ยกเลิก · ความสำคัญ: กลาง · trace: AC-10 · BR-08
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/view/R12`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สถานะยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/view/R12` | — | drawer ร่าง | ☐ |
| 2 | CLICK **ยกเลิก** | — | modal **ยกเลิกเอกสาร?** | ☐ |
| 3 | CLICK ชิป **แจ้งงานซ้ำ** → CLICK **ยกเลิกเอกสาร** | — | toast **ยกเลิกเอกสารแล้ว** · pill **ยกเลิก** | ☐ |

#### TC-X02 — ยกเลิกโดยไม่ใส่เหตุผล = บล็อก
- group: ยกเลิก · ความสำคัญ: กลาง · trace: VR-06 · REASON_REQUIRED
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/view/R10`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ยกเลิกไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/view/R10` | — | drawer ส่งแจ้งงานแล้ว | ☐ |
| 2 | CLICK **ยกเลิกเอกสาร** | — | modal | ☐ |
| 3 | CLICK **ยกเลิกเอกสาร** ใน modal | — | ช่องเหตุผลขอบแดง **กรุณาระบุเหตุผล** · สถานะไม่เปลี่ยน | ☐ |

#### TC-X03 — ผู้จัดการยกเลิกใบที่ส่งแล้วของพนักงาน
- group: ยกเลิก · ความสำคัญ: กลาง · trace: AC-10 · BR-08
- actor (role): admin (วรวุฒิ ทองดี · ผู้จัดการฝ่ายขาย)
- Setup: role=admin · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/view/R10`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สถานะยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/view/R10` | — | drawer **OTN-2569-0010** | ☐ |
| 2 | CLICK **ยกเลิกเอกสาร** → CLICK ชิป **ลูกค้าเลื่อนนัดส่ง** → CLICK **ยกเลิกเอกสาร** | — | pill **ยกเลิก** · ประวัติมี **ยกเลิกเอกสาร** โดย วรวุฒิ ทองดี | ☐ |

### กลุ่ม: สิทธิ์

#### TC-P01 — Sales Admin คนอื่นไม่เห็นใบของเจ้าของ [AI-DEFAULT]
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D01 · DEC-08 · BR-09
- actor (role): other (กิตติ สมมติ · Sales Admin คนอื่น)
- Setup: role=other · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นเฉพาะใบของตน 3 ใบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport` | — | badge **3 รายการ · ร่าง 1** | ☐ |
| 2 | VERIFY คอลัมน์ **ผู้จัดทำ** | — | ทุกแถวเป็น **กิตติ สมมติ** · ไม่มี **OTN-2569-0011** | ☐ |

#### TC-P02 — เปิด route ใบของคนอื่น = ไม่เปิด
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D02 · NOT_FOUND
- actor (role): other (กิตติ สมมติ · Sales Admin คนอื่น)
- Setup: role=other · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: drawer ไม่เปิด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/view/R1` | — | อยู่หน้ารายการ ไม่มี drawer เปิด | ☐ |

#### TC-P03 — ผู้จัดการเห็นทุกใบรวมร่างของทุกคน [AI-DEFAULT]
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: DEC-08 · 05 §5.3
- actor (role): admin (วรวุฒิ ทองดี · ผู้จัดการฝ่ายขาย)
- Setup: role=admin · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 12 ใบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport` | — | badge **12 รายการ · ร่าง 3** | ☐ |
| 2 | CLICK แถว **OTN-2569-0009** | — | drawer ร่างของ กิตติ สมมติ · ไม่มีปุ่ม **แก้ไข** และ **ส่งแจ้งงาน** | ☐ |

#### TC-P04 — ใบที่ส่งแล้วแก้ไขไม่ได้
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: TC-D05 · NOT_DRAFT
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีเมนูแก้ไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport` | — | ตาราง | ☐ |
| 2 | CLICK ⋮ แถว **OTN-2569-0010** | — | เมนูมี **ดูรายละเอียด** · **พิมพ์** · **ยกเลิกเอกสาร** — ไม่มี **แก้ไข** | ☐ |

### กลุ่ม: PDF

#### TC-D01 — PDF ตรงแบบฟอร์ม FM-SAL-16
- group: PDF · ความสำคัญ: สูง · trace: AC-09 · BR-10 · BR-12 · DEC-06 · DEC-11 · DEC-15
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แบบพิมพ์ 1 หน้า 5 คอลัมน์ 20 บรรทัด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/view/R7` | — | drawer | ☐ |
| 2 | CLICK แท็บ **PDF Preview** | — | หัว **ฟอร์มแจ้งงานขนส่งนอก** + ชื่อผู้ขนส่ง · บรรทัด **รอบวันที** · ตาราง ต้นทาง/ปลายทาง/เลขที่PO/จำนวน/วันที่นัดส่ง 4 แถวข้อมูล + แถวว่างรวม 20 · footer **Doc. No. : FM-SAL-16 · Rev.00 : 01/07/2569** | ☐ |
| 3 | VERIFY ช่อง **ผู้จัดทำ** ท้ายหน้า | — | (สุนิสา ตัวอย่าง) · **ส่งในระบบ 15/09/2569 10:42** | ☐ |

#### TC-D02 — PDF ร่างมีคำว่าร่าง
- group: PDF · ความสำคัญ: กลาง · trace: AC-09
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/view/R11`
- ชุดข้อมูล: —
- ผ่านเมื่อ: footer ร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/view/R11` | — | drawer | ☐ |
| 2 | CLICK แท็บ **PDF Preview** | — | footer **เลขที่ OTN-2569-0011 · ร่าง** · ช่องผู้จัดทำบรรทัดวันที่เป็นเส้นประ | ☐ |

#### TC-D03 — แท็บลายเซ็นแสดงไม่มีขั้นอนุมัติ [AI-DEFAULT]
- group: PDF · ความสำคัญ: ต่ำ · trace: DEC-03 · DEC-07 · BR-05
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีสายอนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/view/R1` | — | drawer | ☐ |
| 2 | CLICK แท็บ **ลายเซ็น / อนุมัติ** | — | สายอนุมัติ (DOA) **ไม่มี · 0 ขั้น** · timeline **ผู้จัดทำ · ส่งแจ้งงาน** → **ผลลัพธ์** | ☐ |

### กลุ่ม: แจ้งเตือน

#### TC-K01 — ส่งแจ้งงานแล้วผู้จัดการได้รับแจ้ง
- group: แจ้งเตือน · ความสำคัญ: กลาง · trace: AC-07 · FN-06 · otn_submitted · otn_early_delivery_date
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/view/R11`
- ชุดข้อมูล: —
- ผ่านเมื่อ: มี event ถึง role-mgr-sales

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/view/R11` | — | drawer | ☐ |
| 2 | CLICK **ส่งแจ้งงาน** → CLICK **ส่งแจ้งงาน** | — | toast **ส่งแจ้งงานแล้ว · OTN-2569-0011 · แจ้งผู้จัดการฝ่ายขาย** · (ระบบจริง) ENG-NOTIFY otn_submitted ถึง role-mgr-sales | ☐ |

### กลุ่ม: ขอบ

#### TC-E01 — แบบเอกสารปิดใช้ = สร้างไม่ได้
- group: ขอบ · ความสำคัญ: ต่ำ · trace: AC-12 · EC-06 · DOC_TYPE_INACTIVE
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปุ่มสร้าง disabled

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport` | — | ตาราง | ☐ |
| 2 | VERIFY หลัง (ต้อง simulate) `__QA__.setDocActive(false)` | — | แถบ **แบบเอกสารนี้ยังไม่เปิดใช้งาน — สร้างใบแจ้งงานใหม่ไม่ได้** · ปุ่ม **สร้างใบแจ้งงาน** กดไม่ได้ | ☐ |

#### TC-E02 — บันทึกชนกัน / ส่งไม่สำเร็จ = ไม่เปลี่ยนสถานะ
- group: ขอบ · ความสำคัญ: ต่ำ · trace: EC-05 · EC-08 · STALE_VERSION
- actor (role): owner (สุนิสา ตัวอย่าง · Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/outsourced-transport/view/R11`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สถานะไม่เปลี่ยน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/outsourced-transport/view/R11` | — | drawer | ☐ |
| 2 | CLICK **ส่งแจ้งงาน** → CLICK **ส่งแจ้งงาน** ใน modal | — | (ต้อง simulate `__QA__.sim('stale')`) toast **ข้อมูลถูกแก้โดยผู้อื่น** · pill ยัง **ร่าง** | ☐ |

## วิธีที่ agent รัน (Run protocol)
1. เปิดไฟล์ prototype ใหม่ทุกเคส (seed กลับค่าเริ่ม) · เริ่มที่ Start
2. สลับผู้ใช้ที่มุมขวาบนตาม actor
3. เคส `(ต้อง simulate)` ใช้ console: `__QA__.sim('stale'|'error')` / `__QA__.setDocActive(false)` · ระบบจริงทดสอบระดับ API
4. ทำทีละ step เทียบ Expected ด้วยตา · ไม่ตรง = fail + จด evidence

## Coverage Audit
| หมวด | covered / total |
|---|---|
| AC (06_TESTS) | 12 / 12 |
| Business Rules (05_RULES) | 11 / 13 |
| Validation | 6 / 6 |
| Edge Cases | 5 / 8 |
| Scope Lock (DEC — 07 §7.0) | 13 / 15 |
| Error codes | 8 / 9 (NOT_OWNER ระดับ API) |
| Permission cells | 6 / 6 |

### ข้าม (พร้อมเหตุผล)
- BR-07 — snapshot ชื่อผู้ขนส่ง ทดสอบระดับ API
- BR-13 — ไม่มีการเปลี่ยนค่า/ส่งต่อ ไม่มีอะไรให้ตรวจบน UI
- EC-02 — เกิน 20 แถว/ใบต่อ ทดสอบที่แบบพิมพ์ (รอ OQ-05)
- EC-03 — รอ OQ-06
- EC-04 — snapshot ทดสอบระดับ API
- DEC-01 — ไม่เปลี่ยนค่า — ไม่มีอะไรให้ตรวจบน UI
- DEC-02 — ไม่ส่งต่อ

## Result Report (schema)
```json
{ "feature_id": "F-TMP-003", "run_at": "<iso>", "results": [ { "id": "TC-C01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" } ], "summary": { "total": 32, "pass": 0, "fail": 0, "blocked": 0 } }
```

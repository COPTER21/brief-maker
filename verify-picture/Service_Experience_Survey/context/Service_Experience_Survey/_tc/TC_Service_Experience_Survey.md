# AI Test Cases — F-TMP-006 Service Experience Survey (แบบประเมินความพึงพอใจ Sales Admin — ลูกค้าต่างประเทศ)

ชุดทดสอบสำหรับ AI agent (browser-use/vision) รันบน prototype `feature.html` — anchor = ข้อความที่เห็นบนจอ (ตัวหนา) · ข้อมูลตัวอย่างทั้งหมดเป็นข้อมูลสมมติ · เคสที่ติด `[AI-DEFAULT]` = เกณฑ์มาจากมติที่ AI ตัดสินแทน (รอลูกค้าเซ็นยืนยัน OQ-02) ถ้า fail อาจแปลว่ามติผิด ไม่ใช่โค้ดผิด

## Meta
| Field | Value |
|---|---|
| Feature ID | F-TMP-006 (ชั่วคราว) |
| ชื่อ | Service Experience Survey (แบบประเมินความพึงพอใจ Sales Admin — ลูกค้าต่างประเทศ) (FM-SAL-22) |
| เวอร์ชัน | v1.0 (2026-10-11) |
| App entry | feature.html |
| Routes | `#/sa-csat-ovs` · `#/sa-csat-ovs/create` · `#/sa-csat-ovs/edit/:id` · `#/sa-csat-ovs/view/:id` |
| ที่มา | FRD_F-TMP-006_Pack (STANDARD) · BRD-SAL-SEA-001 · HTML · DECISIONS.lock |
| จำนวนเคส | 30 |
| ตัวสลับผู้ใช้ | มุมขวาบน: สมศรี ตั้งใจดี (เจ้าของ) · ธนพล รอบคอบ (Sales Admin คนอื่น) · วรวุฒิ ทองดี (ผู้จัดการฝ่ายขาย · เห็นทุกใบ) |

## Coverage
| group | เคส | สูง/กลาง/ต่ำ |
|---|---|---|
| รายการ | 5 | 1/2/2 |
| สร้าง | 7 | 3/3/1 |
| ไฟล์ | 1 | 0/1/0 |
| ตรวจข้อมูล | 2 | 1/1/0 |
| คะแนนต่ำ | 2 | 1/0/1 |
| ยกเลิก | 3 | 0/3/0 |
| สิทธิ์ | 5 | 2/3/0 |
| PDF | 3 | 1/1/1 |
| ขอบ | 2 | 0/0/2 |

## Coverage Ledger
### AC (06_TESTS)
| item | cases |
|---|---|
| AC-01 | TC-L01, TC-C01, TC-C02 |
| AC-02 | TC-V01 |
| AC-03 | TC-C01 |
| AC-04 | TC-C03 |
| AC-05 | TC-C01 |
| AC-06 | TC-K01 |
| AC-07 | TC-C04 |
| AC-08 | TC-D01, TC-D02 |
| AC-09 | TC-X01, TC-X03 |
| AC-10 | TC-L05 |
| AC-11 | TC-E01 |
### Business Rules (05_RULES)
| rule | cases |
|---|---|
| BR-01 | TC-C01 |
| BR-02 | TC-C01, TC-C02, TC-C03 |
| BR-03 | TC-C04 (ไม่มีช่องวันที่ · Month ค่าเริ่ม) |
| BR-04 | TC-K01 |
| BR-05 | TC-C01 |
| BR-06 | TC-C01 (ได้เลข SEA ตอนบันทึกครั้งแรก) |
| BR-07 | TC-X01, TC-X03 |
| BR-08 | TC-L01, TC-P01 |
| BR-09 | — ข้าม (snapshot ทดสอบระดับ API) |
| BR-10 | TC-L05 (คะแนนเฉลี่ยใน list/CSV เท่านั้น) |
| BR-11 | TC-D01 |
| BR-12 | TC-V02 (Contact Person บังคับ) |
| BR-13 | — ข้าม (ไม่มีการส่งต่อ ทดสอบไม่ได้บน UI) |
### Validation
| VR | cases |
|---|---|
| VR-01 | TC-C04 (ประจำเดือนมีค่าเริ่มเสมอ) |
| VR-02 | TC-V01 |
| VR-03 | TC-V02 |
| VR-04 | TC-C03 |
| VR-05 | TC-X02 |
### Edge Cases
| EC | cases / สถานะ |
|---|---|
| EC-01 | TC-C02, TC-C03 |
| EC-02 | TC-C07 |
| EC-03 | — ข้าม (OQ-06 ยังไม่ตัดสิน) |
| EC-04 | — ข้าม (snapshot ทดสอบระดับ API) |
| EC-05 | TC-E02 |
| EC-06 | TC-E01 |
| EC-07 | TC-V02 (ผู้ติดต่อเป็นช่องว่างล้วน) |
| EC-08 | — ข้าม (ฟอนต์อักษรต่างประเทศในแบบพิมพ์ — ตรวจรอบเต็มบนเครื่องที่มี browser) |
### Error Codes
| error | cases |
|---|---|
| SCORES_INCOMPLETE | TC-C03 |
| NOT_FOUND | TC-P02 |
| NOT_OWNER | TC-P04 |
| NOT_DRAFT | TC-P05 |
| REASON_REQUIRED | TC-X02 |
| DOC_TYPE_INACTIVE | TC-E01 |
| STALE_VERSION | TC-E02 |
| SCORE_OUT_OF_RANGE | — ระดับ API (UI ให้เลือกได้แค่ 1–5) |
### Permission Matrix (role × action)
| cell | cases |
|---|---|
| Sales Admin คนอื่น ดูใบ/ร่างของคนอื่น = deny | TC-P01, TC-P02 |
| ผู้จัดการ ดูทั้งหมด = allow | TC-P03 |
| ผู้จัดการ บันทึกผลแทน = deny | TC-P04 |
| เจ้าของ แก้ใบบันทึกผล = deny | TC-P05 |
| เจ้าของ ยกเลิก = allow | TC-X01 |
| ผู้จัดการ ยกเลิก = allow | TC-X03 |
### Scope Lock (DEC — 07 §7.0)
| DEC | cases |
|---|---|
| DEC-01 | — ข้าม (ไม่เปลี่ยนค่า — ไม่มีอะไรให้ตรวจบน UI) |
| DEC-02 | — ข้าม (ไม่ส่งต่อ) |
| DEC-03 | TC-D03 |
| DEC-04 | TC-C02 |
| DEC-05 | TC-C01 (หัวข้อคงที่ 10 ข้อ) |
| DEC-06 | TC-D01 |
| DEC-07 | TC-D03 |
| DEC-08 | TC-L01, TC-P01, TC-P03 |
| DEC-09 | TC-C01 |
| DEC-10 | TC-F01 |
| DEC-11 | TC-C01 (ข้อละ 1 คะแนน) |
| DEC-12 | TC-C04 |
| DEC-13 | TC-C04 |
| DEC-14 | TC-D01 (แบบพิมพ์ภาษาอังกฤษ) |

## Data Sets
| ชุด | ข้อมูล |
|---|---|
| ชุด A | ลูกค้า Placeholder Dairy Pty Ltd · ผู้ติดต่อ Mr. Chris Placeholder · คะแนน 10 ข้อ = 5, 4, 5, 4, 5, 4, 5, 4, 5, 5 · Additional Feedback "Quick responses" |
| ชุด B | ลูกค้า Test Bakery Co., Ltd. · ผู้ติดต่อ Ms. Linh Test · 2 ข้อแรก = 4 |
| ชุด C | Additional Feedback ยาว ~900 ตัวอักษร (ข้อความสมมติภาษาอังกฤษ) |
| ชุด D | ลูกค้า Example Foods Pte. Ltd. · ผู้ติดต่อ Ms. Jane Example · คะแนน 10 ข้อ = 3, 2, 3, 1, 2, 3, 2, 3, 4, 2 |

### ไฟล์ทดสอบ (Files)
| ไฟล์ | ใช้ |
|---|---|
| test.exe | TC-F01 ชนิดไฟล์ไม่รองรับ |
| survey-reply.pdf | แนบปกติ |

## Test Cases

### กลุ่ม: รายการ

#### TC-L01 — รายการแสดงเฉพาะใบที่มีสิทธิ์เห็น (เจ้าของ) [AI-DEFAULT]
- group: รายการ · ความสำคัญ: สูง · trace: AC-01 · BR-08 · DEC-08
- actor (role): owner (สมศรี ตั้งใจดี · เจ้าหน้าที่ Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นเฉพาะใบของตนเอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs` | — | หน้า **Service Experience Survey (แบบประเมินความพึงพอใจ Sales Admin — ลูกค้าต่างประเทศ)** · badge จำนวนรายการใน sub | ☐ |
| 2 | VERIFY คอลัมน์ **ผู้บันทึก** ทุกแถว | — | ทุกแถวเป็น **สมศรี ตั้งใจดี** | ☐ |
| 3 | VERIFY แท็บ **ร่าง** | — | มี count ตรงกับจำนวนร่างของตน | ☐ |

#### TC-L02 — segmented tabs กรองตามสถานะ
- group: รายการ · ความสำคัญ: กลาง · trace: 01 P-01 · #117
- actor (role): owner
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แสดงเฉพาะสถานะที่เลือก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs` | — | แท็บ **ทั้งหมด** active | ☐ |
| 2 | CLICK แท็บ **บันทึกผลแล้ว** | — | ทุกแถว pill **บันทึกผลแล้ว** | ☐ |
| 3 | CLICK แท็บ **ยกเลิก** | — | ทุกแถว pill **ยกเลิก** | ☐ |

#### TC-L03 — ค้นหาด้วยชื่อลูกค้า + รีเซ็ต
- group: รายการ · ความสำคัญ: กลาง · trace: 01 P-01
- actor (role): owner
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: ลูกค้า "Sample Trading Co., Ltd."
- ผ่านเมื่อ: ค้นหาแล้วรีเซ็ตได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs` | — | ตาราง | ☐ |
| 2 | TYPE ช่อง **ค้นหาเลขที่ / ลูกค้า / ผู้ติดต่อ / ผู้บันทึก** | Sample Trading | เหลือแถวลูกค้า **Sample Trading Co., Ltd.** | ☐ |
| 3 | CLICK **รีเซ็ต** | — | กลับมาครบทุกแถว | ☐ |

#### TC-L04 — ค้นหาไม่เจอ = empty state
- group: รายการ · ความสำคัญ: ต่ำ · trace: 05 · U23
- actor (role): owner
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แสดงแผงค้นหาไม่พบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs` | — | ตาราง | ☐ |
| 2 | TYPE ช่อง **ค้นหาเลขที่ / ลูกค้า / ผู้ติดต่อ / ผู้บันทึก** | zzzz | ข้อความ **ไม่พบรายการที่ค้นหา** + ปุ่ม **ล้างตัวกรอง** | ☐ |

#### TC-L05 — ส่งออก CSV
- group: รายการ · ความสำคัญ: ต่ำ · trace: AC-10 · FN-08
- actor (role): admin
- Setup: role=admin · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ได้ไฟล์ CSV

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs` | — | ตาราง | ☐ |
| 2 | CLICK **ส่งออก CSV** | — | toast **ส่งออก** + ไฟล์ service-experience-survey-overseas.csv มีคอลัมน์ Contact Person + 10 หัวข้อ + คะแนนเฉลี่ย | ☐ |

### กลุ่ม: สร้าง

#### TC-C01 — สร้างแบบประเมินครบ 10 ข้อ แล้วบันทึกผล (happy) [AI-DEFAULT]
- group: สร้าง · ความสำคัญ: สูง · trace: AC-01 · AC-03 · AC-05 · BR-01 · BR-02 · BR-05 · FN-02 · FN-03
- actor (role): owner (สมศรี ตั้งใจดี · เจ้าหน้าที่ Sales Admin)
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: ชุด A
- ผ่านเมื่อ: สถานะ **บันทึกผลแล้ว** ได้เลข SEA

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs` | — | ตาราง | ☐ |
| 2 | CLICK **สร้างแบบประเมิน** | — | drawer **บันทึก Service Experience Survey (Sales Admin ต่างประเทศ)** stepper 3 ขั้น | ☐ |
| 3 | SELECT ช่อง **ชื่อลูกค้า (Company Name)** | ชุด A ลูกค้า | สรุปขวาแสดงลูกค้า | ☐ |
| 4 | TYPE ช่อง **ผู้ติดต่อ (Contact Person)** | ชุด A ผู้ติดต่อ | รับข้อความ | ☐ |
| 5 | CLICK ปุ่มคะแนน 10 ข้อ (3 กลุ่ม) ตามชุด A | ชุด A คะแนน | สรุปขวา **ตอบแล้ว** 10/10 · คะแนนเฉลี่ยรวมแสดง | ☐ |
| 6 | CLICK **ถัดไป** 2 ครั้ง | — | ขั้น **ตรวจสอบและยืนยัน** แสดงตารางคะแนน 3 กลุ่มครบ | ☐ |
| 7 | CLICK **บันทึกผลแบบประเมิน** | — | modal **บันทึกผลแบบประเมิน?** ไม่มีแถวผู้พิจารณา | ☐ |
| 8 | CLICK **บันทึกผล** ใน modal | — | toast **บันทึกผลแล้ว** · แถวใหม่ pill **บันทึกผลแล้ว** | ☐ |

#### TC-C02 — บันทึกแบบร่างเมื่อตอบไม่ครบ [AI-DEFAULT]
- group: สร้าง · ความสำคัญ: สูง · trace: AC-01 · BR-02 · DEC-04
- actor (role): owner
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: ชุด B
- ผ่านเมื่อ: ได้ร่างเลข SEA

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs/create` | — | drawer สร้าง | ☐ |
| 2 | SELECT **ชื่อลูกค้า (Company Name)** + TYPE **ผู้ติดต่อ (Contact Person)** | ชุด B | เลือก/กรอกได้ | ☐ |
| 3 | CLICK ปุ่มคะแนน 2 ข้อแรก | ชุด B | **ตอบแล้ว** 2/10 | ☐ |
| 4 | CLICK **ถัดไป** 2 ครั้ง | — | แถบเตือน **ยังเลือกคะแนนไม่ครบ** | ☐ |
| 5 | CLICK **บันทึกแบบร่าง** | — | toast **บันทึกร่างแล้ว** · แถวใหม่ pill **ร่าง** | ☐ |

#### TC-C03 — บันทึกผลตอนตอบไม่ครบ = บล็อก (negative) [AI-DEFAULT]
- group: สร้าง · ความสำคัญ: สูง · trace: AC-04 · VR-04 · BR-02
- actor (role): owner
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: ชุด B
- ผ่านเมื่อ: ไม่บันทึกผล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs/create` | — | drawer สร้าง | ☐ |
| 2 | SELECT **ชื่อลูกค้า (Company Name)** + TYPE **ผู้ติดต่อ (Contact Person)** | ชุด B | เลือก/กรอกได้ | ☐ |
| 3 | CLICK **ถัดไป** 2 ครั้ง | — | ขั้นตรวจสอบ | ☐ |
| 4 | CLICK **บันทึกผลแบบประเมิน** | — | กลับขั้น 1 · แถวหัวข้อที่ขาดเป็นสีแดง · toast **เลือกคะแนนให้ครบ** | ☐ |

#### TC-C04 — ไม่มีช่องวันที่ · ประจำเดือนค่าเริ่ม = เดือนปัจจุบัน [AI-DEFAULT]
- group: สร้าง · ความสำคัญ: กลาง · trace: AC-07 · BR-03 · DEC-12 · DEC-13
- actor (role): owner
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ฟอร์มตรงกระดาษ (Month · Company Name · Contact Person) ไม่มีวันที่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs/create` | — | drawer สร้าง · การ์ด **ประจำเดือนและลูกค้า** | ☐ |
| 2 | VERIFY ช่อง **ประจำเดือน (Month)** | — | มีค่าเดือนปัจจุบันแล้ว · ไม่มีช่อง **วันที่** ในการ์ด | ☐ |
| 3 | CLICK X ปิด drawer แล้ว VERIFY หัวตาราง | — | คอลัมน์ **วันที่บันทึก** (มาจากระบบ) | ☐ |

#### TC-C05 — ปิดตอนกรอกค้าง = ถามทิ้งข้อมูล
- group: สร้าง · ความสำคัญ: กลาง · trace: 01 P-02 · U25
- actor (role): owner
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ข้อมูลไม่หายถ้ากลับไปกรอกต่อ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs/create` | — | drawer สร้าง | ☐ |
| 2 | CLICK ปุ่มคะแนน **5** ของข้อแรก (Communication clarity) | — | ปุ่มเป็นสีเข้ม | ☐ |
| 3 | CLICK **ยกเลิก** ที่ footer | — | modal **ทิ้งข้อมูลที่กรอกไว้?** | ☐ |
| 4 | CLICK **กลับไปกรอกต่อ** | — | ยังอยู่ drawer คะแนนที่เลือกเดิมคงอยู่ | ☐ |

#### TC-C06 — แก้ร่างของตัวเอง
- group: สร้าง · ความสำคัญ: กลาง · trace: 01 P-02 · U15
- actor (role): owner
- Setup: role=owner · seed=ร่าง SEA-2569-0013 · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แก้แล้วบันทึกได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs` | — | ตาราง | ☐ |
| 2 | CLICK แถว **SEA-2569-0013** | — | drawer ดู pill **ร่าง** · ปุ่ม **แก้ไข** | ☐ |
| 3 | CLICK **แก้ไข** | — | drawer ดูปิดแล้ว drawer **แก้ไขแบบประเมิน SEA-2569-0013** เปิด | ☐ |
| 4 | TYPE **Additional Feedback** | Please send a monthly summary | ค่าเปลี่ยน | ☐ |
| 5 | CLICK **ถัดไป** 2 ครั้ง → CLICK **บันทึกแบบร่าง** | — | toast **บันทึกร่างแล้ว** | ☐ |

#### TC-C07 — Additional Feedback ยาว → PDF ยัง 1 หน้า
- group: สร้าง · ความสำคัญ: ต่ำ · trace: EC-02 · FN-07
- actor (role): owner
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: ชุด C
- ผ่านเมื่อ: PDF 1 หน้า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs/create` | — | drawer สร้าง | ☐ |
| 2 | TYPE ช่อง **Additional Feedback** | ชุด C | รับข้อความยาวได้ | ☐ |
| 3 | VERIFY PDF Preview หลังบันทึกร่าง | — | Feedback ต่อบรรทัด (> 5 บรรทัด) · หน้าเดียว | ☐ |

### กลุ่ม: ไฟล์

#### TC-F01 — แนบไฟล์ผิดชนิด = ปฏิเสธ
- group: ไฟล์ · ความสำคัญ: กลาง · trace: DEC-10 · file_policy
- actor (role): owner
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: ไฟล์ .exe
- ผ่านเมื่อ: ไฟล์ไม่ถูกแนบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs/create` | — | drawer สร้าง | ☐ |
| 2 | SELECT **ชื่อลูกค้า (Company Name)** + TYPE **ผู้ติดต่อ (Contact Person)** แล้ว CLICK **ถัดไป** | ลูกค้าใดก็ได้ · Mr. Test | ขั้น **เอกสารแนบ** | ☐ |
| 3 | UPLOAD ไฟล์ | test.exe | toast **ชนิดไฟล์ไม่รองรับ** | ☐ |

### กลุ่ม: ตรวจข้อมูล

#### TC-V01 — กดถัดไปตอนว่าง (negative)
- group: ตรวจข้อมูล · ความสำคัญ: สูง · trace: AC-02 · VR-02 · VR-03
- actor (role): owner
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs/create` | — | drawer สร้าง | ☐ |
| 2 | CLICK **ถัดไป** | — | ยังอยู่ขั้น 1 · ช่อง **ชื่อลูกค้า (Company Name)** แดง **กรุณาเลือกลูกค้า** · ช่อง **ผู้ติดต่อ (Contact Person)** แดง **กรุณากรอกชื่อผู้ติดต่อ** · toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |

#### TC-V02 — ผู้ติดต่อเป็นช่องว่างล้วน = บล็อก (negative)
- group: ตรวจข้อมูล · ความสำคัญ: กลาง · trace: VR-03 · BR-12 · EC-07
- actor (role): owner
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: ผู้ติดต่อ = เว้นวรรค 3 ตัว
- ผ่านเมื่อ: บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs/create` | — | drawer สร้าง | ☐ |
| 2 | SELECT **ชื่อลูกค้า (Company Name)** + TYPE **ผู้ติดต่อ (Contact Person)** | ลูกค้าใดก็ได้ · "   " | — | ☐ |
| 3 | CLICK **ถัดไป** | — | ยังอยู่ขั้น 1 · **กรุณากรอกชื่อผู้ติดต่อ** · toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |

### กลุ่ม: คะแนนต่ำ

#### TC-K01 — บันทึกผลที่มีคะแนน ≤ 2 → แบนเนอร์ + แจ้งผู้จัดการ [AI-DEFAULT]
- group: คะแนนต่ำ · ความสำคัญ: สูง · trace: AC-06 · BR-04 · sea_low_score_recorded
- actor (role): owner
- Setup: role=owner · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: ชุด D
- ผ่านเมื่อ: แจ้งผู้จัดการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs/create` | — | drawer สร้าง | ☐ |
| 2 | SELECT ลูกค้า + TYPE ผู้ติดต่อ + CLICK คะแนน 10 ข้อ | ชุด D | **ตอบแล้ว** 10/10 · ข้อความ **คะแนน ≤ 2** ในสรุป | ☐ |
| 3 | CLICK **ถัดไป** 2 ครั้ง → **บันทึกผลแบบประเมิน** → **บันทึกผล** | — | toast **บันทึกผลแล้ว** + แจ้งผู้จัดการฝ่ายขาย | ☐ |
| 4 | CLICK แถวใหม่ | — | แบนเนอร์ **มีหัวข้อที่ได้คะแนน ≤ 2** · หัวข้อคะแนน ≤ 2 สีแดง | ☐ |

#### TC-K02 — ผู้จัดการได้รับ in-app (ENG-NOTIFY)
- group: คะแนนต่ำ · ความสำคัญ: ต่ำ · trace: sea_low_score_recorded · FN-06
- actor (role): admin
- Setup: role=admin · seed=หลัง TC-K01 · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: มีแจ้งเตือน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs` | — | (ต้อง simulate) ระบบจริงตรวจที่ Notification Center | ☐ |

### กลุ่ม: ยกเลิก

#### TC-X01 — เจ้าของยกเลิกร่างของตัวเอง [AI-DEFAULT]
- group: ยกเลิก · ความสำคัญ: กลาง · trace: AC-09 · BR-07
- actor (role): owner
- Setup: role=owner · seed=ร่าง SEA-2569-0013 · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: pill **ยกเลิก**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs` | — | ตาราง | ☐ |
| 2 | CLICK แถว **SEA-2569-0013** | — | drawer ดู | ☐ |
| 3 | CLICK **ยกเลิก** | — | modal **ยกเลิกเอกสาร?** | ☐ |
| 4 | CLICK chip **บันทึกซ้ำ** → CLICK **ยกเลิกเอกสาร** ใน modal | — | toast **ยกเลิกเอกสารแล้ว** · pill **ยกเลิก** | ☐ |

#### TC-X02 — ยกเลิกต้องมีเหตุผล (negative)
- group: ยกเลิก · ความสำคัญ: กลาง · trace: VR-05
- actor (role): owner
- Setup: role=owner · seed=ใบบันทึกผล SEA-2569-0014 · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่ยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs` | — | ตาราง | ☐ |
| 2 | CLICK แถว **SEA-2569-0014** → CLICK **ยกเลิกเอกสาร** | — | modal | ☐ |
| 3 | CLICK **ยกเลิกเอกสาร** ใน modal โดยไม่ใส่เหตุผล | — | **กรุณาระบุเหตุผล** · modal ไม่ปิด | ☐ |

#### TC-X03 — ผู้จัดการยกเลิกใบของเจ้าหน้าที่ [AI-DEFAULT]
- group: ยกเลิก · ความสำคัญ: กลาง · trace: AC-09 · BR-07 · sea_cancelled
- actor (role): admin (วรวุฒิ ทองดี · ผู้จัดการฝ่ายขาย)
- Setup: role=admin · seed=ใบบันทึกผล SEA-2569-0012 (ของกมลวรรณ) · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: pill **ยกเลิก**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs` | — | สลับผู้ใช้เป็น **วรวุฒิ ทองดี** | ☐ |
| 2 | CLICK แถว **SEA-2569-0012** → CLICK **ยกเลิกเอกสาร** | — | modal | ☐ |
| 3 | CLICK chip **บันทึกผิดลูกค้า** → CLICK **ยกเลิกเอกสาร** | — | toast **ยกเลิกเอกสารแล้ว** (ระบบจริง: เจ้าของได้รับแจ้ง) | ☐ |

### กลุ่ม: สิทธิ์

#### TC-P01 — Sales Admin คนอื่นไม่เห็นใบ/ร่างของคนอื่น [AI-DEFAULT]
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D01 · DEC-08 · BR-08
- actor (role): approver-persona (ธนพล รอบคอบ · Sales Admin คนอื่น)
- Setup: role=approver-persona · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่เห็นร่างของคนอื่น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs` | — | สลับผู้ใช้เป็น **ธนพล รอบคอบ** | ☐ |
| 2 | VERIFY คอลัมน์ **ผู้บันทึก** | — | ทุกแถวเป็น **ธนพล รอบคอบ** · ไม่เห็นร่างของคนอื่น | ☐ |

#### TC-P02 — เปิด route ใบที่ไม่มีสิทธิ์ = ไม่เปิด
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D02 · NOT_FOUND
- actor (role): approver-persona (ธนพล รอบคอบ · Sales Admin คนอื่น)
- Setup: role=approver-persona · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: drawer ไม่เปิด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs/view/R13` | — | สลับผู้ใช้เป็น **ธนพล รอบคอบ** · drawer ไม่เปิด (ไม่เห็น) | ☐ |

#### TC-P03 — ผู้จัดการเห็นทุกใบรวมร่าง
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: DEC-08
- actor (role): admin
- Setup: role=admin · seed=seed เริ่มต้น · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs` | — | สลับผู้ใช้เป็น **วรวุฒิ ทองดี** | ☐ |
| 2 | VERIFY คอลัมน์ **ผู้บันทึก** | — | มีหลายผู้บันทึก · แท็บ **ร่าง** มีร่างของเจ้าหน้าที่ | ☐ |

#### TC-P04 — ผู้จัดการบันทึกผลแทนไม่ได้
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: TC-D03 · NOT_OWNER
- actor (role): admin (วรวุฒิ ทองดี · ผู้จัดการฝ่ายขาย)
- Setup: role=admin · seed=ร่าง SEA-2569-0011 (ของธนพล รอบคอบ) · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มบันทึกผล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs` | — | สลับผู้ใช้เป็น **วรวุฒิ ทองดี** | ☐ |
| 2 | CLICK แถว **SEA-2569-0011** | — | ไม่มีปุ่ม **บันทึกผล** และ **แก้ไข** (API 403 NOT_OWNER ทดสอบระดับระบบ) | ☐ |

#### TC-P05 — ใบบันทึกผลแล้วแก้ไม่ได้
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: TC-D05 · NOT_DRAFT
- actor (role): owner
- Setup: role=owner · seed=ใบบันทึกผล SEA-2569-0014 · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มแก้ไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs` | — | ตาราง | ☐ |
| 2 | CLICK ⋮ ที่แถว **SEA-2569-0014** | — | เมนูไม่มี **แก้ไข** | ☐ |
| 3 | OPEN `#/sa-csat-ovs/edit/R14` | — | toast **แก้ไขได้เฉพาะร่างของตัวเอง** | ☐ |

### กลุ่ม: PDF

#### TC-D01 — PDF Preview ตรงแบบ FM-SAL-22 [AI-DEFAULT]
- group: PDF · ความสำคัญ: สูง · trace: AC-08 · BR-11 · DEC-06 · DEC-14
- actor (role): owner
- Setup: role=owner · seed=ใบบันทึกผล SEA-2569-0004 · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แบบพิมพ์ตรงกระดาษ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs/view/R4` | — | drawer ดู | ☐ |
| 2 | CLICK แท็บ **PDF Preview** | — | หัว **Service Experience Survey** · **Month :** · **Company Name:** · **Contact Person:** · 3 ตาราง **COMMUNICATION & RESPONSIVENESS** / **DOCUMENTATION & EXECUTION** / **PROFESSIONALISM** หัวคอลัมน์ 1–5 · 10 ข้อ หน้าเดียว · ✓ ตรงคะแนน | ☐ |
| 3 | VERIFY ข้อความภาษาอังกฤษ | — | **Shipment coordination support** · **Additional Feedback :** · footer **Doc No.FM-SAL-22** | ☐ |

#### TC-D02 — PDF ร่าง/ยกเลิก มีป้ายใน footer
- group: PDF · ความสำคัญ: กลาง · trace: AC-08 · FN-07
- actor (role): owner
- Setup: role=owner · seed=ร่าง SEA-2569-0013 · ยกเลิก SEA-2569-0009 · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ป้ายถูก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs/view/R13` | — | drawer | ☐ |
| 2 | CLICK แท็บ **PDF Preview** | — | footer มี **DRAFT** | ☐ |
| 3 | OPEN `#/sa-csat-ovs/view/R9` → CLICK **PDF Preview** | — | footer มี **CANCELLED** | ☐ |

#### TC-D03 — แท็บลายเซ็น / อนุมัติ = ไม่มีขั้นอนุมัติ [AI-DEFAULT]
- group: PDF · ความสำคัญ: ต่ำ · trace: DEC-03 · DEC-07
- actor (role): owner
- Setup: role=owner · seed=ใบบันทึกผล SEA-2569-0014 · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แสดง 0 ขั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs/view/R14` | — | drawer | ☐ |
| 2 | CLICK แท็บ **ลายเซ็น / อนุมัติ** | — | **ไม่มี · 0 ขั้น** · timeline **บันทึกผลแบบประเมิน** → **ผลลัพธ์** | ☐ |

### กลุ่ม: ขอบ

#### TC-E01 — แบบเอกสารปิดใช้ = สร้างไม่ได้
- group: ขอบ · ความสำคัญ: ต่ำ · trace: AC-11 · EC-06 · DOC_TYPE_INACTIVE
- actor (role): owner
- Setup: role=owner · seed=__QA__.setDocActive(false) (ต้อง simulate) · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปุ่มสร้าง disabled

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs` | — | (ต้อง simulate) แถบ **แบบเอกสารนี้ยังไม่เปิดใช้งาน** · ปุ่ม **สร้างแบบประเมิน** กดไม่ได้ | ☐ |

#### TC-E02 — บันทึกชนกัน (stale) = toast รีเฟรช
- group: ขอบ · ความสำคัญ: ต่ำ · trace: EC-05 · STALE_VERSION
- actor (role): owner
- Setup: role=owner · seed=__QA__.sim('stale') (ต้อง simulate) · files=—
- Start: OPEN `#/sa-csat-ovs`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สถานะไม่เปลี่ยน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/sa-csat-ovs/view/R13` | — | drawer | ☐ |
| 2 | CLICK **บันทึกผล** → CLICK **บันทึกผล** ใน modal | — | (ต้อง simulate) toast **ข้อมูลถูกแก้โดยผู้อื่น** · pill ยัง **ร่าง** | ☐ |

## วิธีที่ agent รัน (Run protocol)
1. เปิดไฟล์ prototype ใหม่ทุกเคส (seed กลับค่าเริ่ม) · เริ่มที่ Start
2. สลับผู้ใช้ที่มุมขวาบนตาม actor
3. เคส `(ต้อง simulate)` ใช้ console: `__QA__.sim('stale'|'error')` / `__QA__.setDocActive(false)` · ระบบจริงทดสอบระดับ API
4. ทำทีละ step เทียบ Expected ด้วยตา · ไม่ตรง = fail + จด evidence

## Coverage Audit
| หมวด | covered / total |
|---|---|
| AC (06_TESTS) | 11 / 11 |
| Business rules | 11 / 13 (BR-09 · BR-13 ข้าม) |
| Validation | 5 / 5 |
| Edge cases | 6 / 8 |
| Error codes | 7 / 8 (1 ระดับ API) |
| Permission cells | 6 / 6 |
| Scope Lock (DEC) | 12 / 14 (DEC-01/02 ไม่มีสิ่งให้ตรวจบน UI) |

### ข้าม (พร้อมเหตุผล)
- BR-09 / EC-04 — snapshot ชื่อลูกค้า ทดสอบระดับ API
- BR-13 · DEC-01 · DEC-02 — ไม่เปลี่ยนค่า/ไม่ส่งต่อ ไม่มีอะไรให้ตรวจบน UI
- EC-03 — รอ OQ-06
- EC-08 — ฟอนต์อักษรต่างประเทศในแบบพิมพ์ ตรวจรอบเต็มบนเครื่องที่มี browser

## Result Report (schema)
```json
{ "feature_id": "F-TMP-006", "run_at": "<iso>", "results": [ { "id": "TC-C01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" } ], "summary": { "total": 30, "pass": 0, "fail": 0, "blocked": 0 } }
```

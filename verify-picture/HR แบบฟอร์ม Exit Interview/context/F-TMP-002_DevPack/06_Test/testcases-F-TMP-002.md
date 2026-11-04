# AI Test Cases — F-TMP-002 แบบสอบถามบุคลากรที่พ้นจากงาน (Exit Interview)

ชุดเคสสำหรับ AI agent (browser-use/vision) ทดสอบบน prototype `feature.html` · anchor = ข้อความบนจอจริง (HTML > 01_UI) · เคสที่ derive จากมติ AI-DEFAULT ติดป้าย [AI-DEFAULT] — fail อาจแปลว่า "ค่าเริ่มผิด" ไม่ใช่โค้ดผิด

## Meta
| รายการ | ค่า |
|---|---|
| Feature ID | F-TMP-002 |
| ชื่อ | แบบสอบถามบุคลากรที่พ้นจากงาน (Exit Interview) |
| เวอร์ชัน | 1.0 |
| App entry | feature.html |
| Routes | `#/exit-interview` · `#/exit-interview/create` · `#/exit-interview/edit/:id` · `#/exit-interview/view/:id` |
| ที่มา | FRD_F-TMP-002_Pack · BRD_F-TMP-002 · feature.html · DECISIONS.lock |
| จำนวนเคส | 58 |
| หมวด | L ดูรายการ · C สร้างแบบสอบถาม · V กรอกไม่ครบ / ผิด · R ลำดับปัจจัย · S ส่งแบบสอบถาม · X ยกเลิก · P ใครเห็นอะไร · D แบบพิมพ์ PDF · E การใช้งานทั่วไป · K สายอนุมัติ (DOA) · H ประวัติ · XT เชื่อมระบบอื่น |

## Coverage
| group | เคส | สูง/กลาง/ต่ำ |
|---|---|---|
| L ดูรายการ | 7 | 2/4/1 |
| C สร้างแบบสอบถาม | 7 | 5/2/0 |
| V กรอกไม่ครบ / ผิด | 11 | 5/3/3 |
| R ลำดับปัจจัย | 3 | 1/2/0 |
| S ส่งแบบสอบถาม | 3 | 1/2/0 |
| X ยกเลิก | 4 | 3/1/0 |
| P ใครเห็นอะไร | 6 | 5/1/0 |
| D แบบพิมพ์ PDF | 6 | 3/3/0 |
| E การใช้งานทั่วไป | 4 | 0/2/2 |
| K สายอนุมัติ (DOA) | 3 | 1/2/0 |
| H ประวัติ | 2 | 0/2/0 |
| XT เชื่อมระบบอื่น | 2 | 0/2/0 |

## Coverage Ledger
### FR / AC (06_TESTS)
| item | cases |
|---|---|
| AC-01 | TC-C01 |
| AC-02 | — |
| AC-03 | — |
| AC-04 | — |
| AC-05 | — |
| AC-06 | — |
| AC-07 | TC-C03 |
| AC-08 | TC-L07 |
| AC-09 | TC-L01, TC-P01 |
| AC-10 | TC-D01, TC-D02 |
| AC-11 | TC-X01 |
| AC-12 | TC-S01 |
| AC-13 | TC-D06, TC-K01 |
### Business Rules (05_RULES)
| rule | cases |
|---|---|
| BR-01 | TC-C05, TC-C06 |
| BR-02 | TC-C02, TC-V02, TC-V03 |
| BR-03 | TC-V05 |
| BR-04 | TC-R01, TC-R02, TC-R03, TC-V06 |
| BR-05 | TC-C01, TC-D05 |
| BR-06 | TC-L01, TC-L02, TC-P01, TC-P03 |
| BR-07 | TC-C04, TC-XT02, TC-E04 |
| BR-08 | TC-S01, TC-K01, TC-K02, TC-D06 |
| BR-09 | TC-D01, TC-D02, TC-D06 |
| BR-10 | TC-H02 (ไม่มีปุ่มส่งต่อ/เปลี่ยนค่า) |
| BR-11 | TC-X01, TC-X02, TC-X03, TC-K03 |
| BR-12 | TC-C07, TC-L07 |
| BR-13 | TC-D01 (ถ้อยคำบนแบบพิมพ์) |
| BR-14 | TC-P05 |
### Validation (VR)
| VR | cases |
|---|---|
| VR-01 | TC-C03 |
| VR-02 | TC-V01, TC-V02 |
| VR-03 | TC-V03 |
| VR-04 | TC-V04 |
| VR-05 | TC-V08, TC-V09 |
| VR-06 | TC-V05 |
| VR-07 | TC-V06 |
| VR-08 | TC-V07 |
| VR-09 | TC-X02 |
### Edge Cases
| EC | cases / สถานะ |
|---|---|
| EC-01 | — ข้าม (seed ต้นแบบมีวันเกิดทุกคน — ทดสอบตอน UAT ระบบจริง) |
| EC-02 | TC-V02 |
| EC-03 | — ข้าม (seed ไม่มีกรณีนี้ — UAT ระบบจริง) |
| EC-04 | TC-D04 |
| EC-05 | TC-D05 |
| EC-06 | TC-P02 |
| EC-07 | TC-P04 |
| EC-08 | TC-X03 |
| EC-09 | TC-E04 |
| EC-10 | TC-D06 |
### Permission Matrix (role × action)
| cell | cases |
|---|---|
| owner ดู/สร้าง/แก้ร่าง/ส่ง/ยกเลิก = allow | TC-L01, TC-C01, TC-C04, TC-X01 |
| ผู้ให้ข้อมูล (HR สร้างแทน) แก้ร่าง = deny | TC-P04 |
| role-mgr-hr ดูทุกใบ/ยกเลิก/CSV = allow | TC-L02, TC-X03, TC-L07 |
| ผู้บังคับบัญชา ดูใบลูกน้อง = deny | TC-P01, TC-P02 |
| พนักงานอื่น ดูร่างคนอื่น = deny | TC-P03 |
| แก้ใบส่งแล้ว = deny | TC-P05 |
| CSV ตามสิทธิ์ | TC-P06 |
| ผู้ให้ข้อมูลตัดสินขั้น DOA ใบตัวเอง = deny (BR-DOA-04) | TC-K01 (รายชื่อผู้พิจารณาไม่มีผู้ให้ข้อมูล) |
### Cross-Module (XT — 06 §6.9)
| XT | Downstream | Case |
|---|---|---|
| ENG-NOTIFY exi_submitted | role-mgr-hr | TC-XT01 |
| F-DOCCFG / ENG-DOC-NUM | เลข EXI | TC-XT02 |
| F-EMP-001 prefill | ข้อมูลบุคลากร | TC-C01 step 2 |
### Scope Lock (DEC — 07 §7.0)
| DEC | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| DEC-01 | ไม่เปลี่ยนค่าในระบบ | TC-H02 |
| DEC-02 | ไม่ส่งต่อ | TC-XT01 |
| DEC-03 | 0 ขั้น DOA [AI-DEFAULT] | TC-S01, TC-K01 |
| DEC-04 | คำนวณ/HR สร้างแทน [AI-DEFAULT] | TC-C05, TC-C03 |
| DEC-05 | ปัจจัยไม่จำกัด | TC-D04 |
| DEC-06 | ข้อเสนอแนะไม่จำกัด | TC-D05 |
| DEC-07 | ช่อง 1:1 | TC-C01 |
| DEC-08 | ลงชื่อไม่ใช้ภาพ | TC-D02 |
| DEC-09 | การมองเห็น | TC-L02, TC-P01 |
| DEC-10 | เลขตอนบันทึกครั้งแรก | TC-C04 |
| DEC-11 | แนบ ✓ CSV ✓ | TC-C07, TC-L07 |
| DEC-12 | โปรดกรอก | TC-D01 |
| DEC-13 | ✓ แทน P | TC-D02 |
| DEC-14 | ข้อ 5 เฉพาะครบสัญญา | TC-V03, TC-D03 |
| DEC-15 | ลำดับปัจจัย | TC-R01, TC-R02 |
| DEC-16 | ครบ 26 ข้อ | TC-V05 |
| DEC-17 | ผู้บังคับบัญชาไม่เห็น | TC-P01, TC-P02 |
### Cross-cutting / Events / States
| item | cases |
|---|---|
| empty state | TC-L06, TC-P01 |
| dirty-check ปิด wizard | TC-E01 |
| Esc chain | TC-E02 |
| backdrop mousedown | TC-E03 |
| API error | TC-S03 |
| state cancelled | TC-X04 |
| ประวัติ append-only | TC-H01 |

## Data Sets
### ชุด A
| ฟิลด์ | ค่า |
|---|---|
| วันที่ลาออก | 31 ต.ค. 2569 |
| ส่วนที่ 2 | ตอบครบ 26 ข้อ (ข้อละ 1 ระดับ) |
| ส่วนที่ 3 | 1 = เงินเดือน/ค่าตอบแทนน้อยกว่าที่ต้องการ · 2 = ได้งานใหม่ที่ชอบมากกว่า |
| ข้อเสนอแนะ ข้อ 1 | การวางแผนเส้นทางเยี่ยมลูกค้า · ให้ระบบช่วยจัดเส้นทาง |
### ชุด B
| ฟิลด์ | ค่า |
|---|---|
| ผู้ให้ข้อมูล | ณัฐชา บุญมา (EMP-00456) |
| ข้อ 5 | อื่น ๆ · ครบโครงการชั่วคราว |
| ส่วนที่ 3 | 1 = ปัญหาการเดินทาง |
### ชุด C
| ฟิลด์ | ค่า |
|---|---|
| ส่วนที่ 3 | เลือกครบ 21 ปัจจัย · อื่นๆ = เหตุผลอื่นที่ระบุยาว |
### ชุด D
| ฟิลด์ | ค่า |
|---|---|
| ส่วนที่ 4 | 12 แถว: ประเด็นที่ควรปรับปรุงข้อที่ 1..12 |
### ไฟล์ทดสอบ (Files)
| ไฟล์ | ใช้ |
|---|---|
| หนังสือลาออก.pdf | TC-C07 |
| script.exe | TC-V10 |
| big-25MB.pdf | TC-V11 |

## Test Cases

### กลุ่ม L — ดูรายการ

#### TC-L01 — รายการของผู้ให้ข้อมูลเห็นเฉพาะใบของตัวเอง
- group: ดูรายการ · ความสำคัญ: สูง · trace: AC-09 / BR-06 / DEC-09 (auto: e2e S2)
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นเฉพาะใบ EXI-2569-0006 ของตัวเอง + คอลัมน์ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/exit-interview` | — | หัวข้อ **แบบสอบถามบุคลากรที่พ้นจากงาน** + (Exit Interview) · ปุ่ม **ส่งออก CSV** · **สร้างแบบสอบถาม** | ☐ |
| 2 | VERIFY หัวตาราง | — | คอลัมน์ **เลขที่ · วันที่สร้าง · ผู้ให้ข้อมูล · ฝ่าย · ลักษณะการพ้นงาน · วันที่พ้นจากงาน · สถานะเอกสาร · ลายเซ็น** | ☐ |
| 3 | VERIFY แถวในตาราง | — | มี 1 แถว **EXI-2569-0006** pill **ร่าง** · ไม่เห็นใบของคนอื่น | ☐ |

#### TC-L02 — ฝ่ายบุคคลเห็นทุกใบ + ตัวเลขใต้หัวข้อ
- group: ดูรายการ · ความสำคัญ: สูง · trace: DEC-09 / U1 (auto: e2e S2)
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 7 ใบ · badge "7 รายการ" "ร่าง 2" "ส่งแล้ว 4" · ไม่มีการ์ดตัวเลข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/exit-interview` | — | ตารางมี 7 แถว (EXI-2569-0001..0007) | ☐ |
| 2 | VERIFY บรรทัดคำอธิบายใต้หัวข้อ | — | ข้อความ **ความเห็นของผู้พ้นจากงาน เพื่อปรับปรุงการบริหารบุคคล · เอกสารลับ** + badge **7 รายการ** **ร่าง 2** **ส่งแล้ว 4** · ไม่มีแถวการ์ดตัวเลข | ☐ |

#### TC-L03 — ค้นหาด้วยชื่อ/รหัสพนักงาน
- group: ดูรายการ · ความสำคัญ: กลาง · trace: P-01 search
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview`
- ชุดข้อมูล: ค้นหา: EMP-00305
- ผ่านเมื่อ: เหลือแถว EXI-2569-0004

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่อง **ค้นหาเลขที่ / ชื่อ / รหัสพนักงาน / แผนก** | EMP-00305 | ตารางเหลือ 1 แถว **EXI-2569-0004** (วรวุฒิ ทองดี) | ☐ |
| 2 | CLICK ปุ่ม **รีเซ็ต** | — | ช่องค้นหาว่าง · กลับมา 7 แถว | ☐ |

#### TC-L04 — กรองสถานะ / ลักษณะการพ้นงาน / ฝ่าย
- group: ดูรายการ · ความสำคัญ: กลาง · trace: P-01 filter
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ผลกรองตรงเงื่อนไขทุกตัว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ตัวกรอง **ทุกสถานะ** → **ยกเลิก** | — | เหลือ 1 แถว **EXI-2569-0003** pill **ยกเลิก** | ☐ |
| 2 | CLICK **รีเซ็ต** แล้ว SELECT **ทุกลักษณะการพ้นงาน** → **ไม่จ้างต่อ (ครบสัญญา)** | — | เหลือ 2 แถว (EXI-2569-0002, 0005) | ☐ |
| 3 | CLICK **รีเซ็ต** แล้ว SELECT **ทุกฝ่าย** → **ฝ่ายปฏิบัติการ** | — | เหลือแถวของฝ่ายปฏิบัติการ (0002, 0004, 0007) | ☐ |

#### TC-L05 — แบ่งหน้า + แสดงต่อหน้า
- group: ดูรายการ · ความสำคัญ: ต่ำ · trace: U6
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview`
- ชุดข้อมูล: —
- ผ่านเมื่อ: footer มีแสดงต่อหน้า 25 + "1 – 7 จาก 7 รายการ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY footer ตาราง | — | **แสดงต่อหน้า** ค่า 25 · ข้อความ **1 – 7 จาก 7 รายการ** · ปุ่มหน้า 1 | ☐ |
| 2 | SELECT **แสดงต่อหน้า** → 10 | — | ยังแสดง 7 แถว หน้าเดียว | ☐ |

#### TC-L06 — ค้นหาไม่พบ = empty state
- group: ดูรายการ · ความสำคัญ: กลาง · trace: U23 / 01 §1.6
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview`
- ชุดข้อมูล: ค้นหา: ไม่มีชื่อนี้
- ผ่านเมื่อ: แสดง "ไม่พบรายการที่ค้นหา" + ปุ่มล้างตัวกรอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา | ไม่มีชื่อนี้ | ตารางว่าง แสดง **ไม่พบรายการที่ค้นหา** · **ลองปรับคำค้นหรือล้างตัวกรอง** | ☐ |
| 2 | CLICK ปุ่ม **ล้างตัวกรอง** | — | กลับมา 7 แถว | ☐ |

#### TC-L07 — ส่งออก CSV ตามสิทธิ์
- group: ดูรายการ · ความสำคัญ: กลาง · trace: AC-08 / DEC-11 / API-11
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ดาวน์โหลด exit-interview.csv + toast ส่งออก 7 รายการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งออก CSV** | — | toast **ส่งออก 7 รายการ** · ไฟล์ exit-interview.csv | ☐ |
| 2 | VERIFY หัวคอลัมน์ในไฟล์ | — | มี เลขที่ · รหัสพนักงาน · คะแนนเฉลี่ย · ข้อ 1..ข้อ 26 · ปัจจัยอันดับ 1–3 | ☐ |

### กลุ่ม C — สร้างแบบสอบถาม

#### TC-C01 — สร้างแบบสอบถามกรณีลาออก ครบทุกส่วนแล้วส่ง (happy)
- group: สร้างแบบสอบถาม · ความสำคัญ: สูง · trace: AC-01/02/12 / FN-01..04 / DEC-04 [AI-DEFAULT]
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: A
- ผ่านเมื่อ: สถานะ "ส่งแล้ว" · เลข EXI-2569-0008 · toast ส่งแบบสอบถามแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/exit-interview` → CLICK **สร้างแบบสอบถาม** | — | drawer **สร้างเอกสารใหม่** · ขั้น **ข้อมูลแบบสอบถาม › เอกสารแนบ › ตรวจสอบและยืนยัน** | ☐ |
| 2 | VERIFY การ์ด **1 ข้อมูลบุคลากร** | — | ชื่อ **สมชาย ทดสอบดี** · **EMP-00123** · **เจ้าหน้าที่ขาย** · **ฝ่ายขายและการตลาด** · **แผนกขายในประเทศ** · วันเริ่มงาน **1 มิ.ย. 2566** (อ่านอย่างเดียว) | ☐ |
| 3 | CLICK ช่อง **วันที่ลาออก** → เลือกวัน | A: 31 ต.ค. 2569 | ช่องแสดง **31 ต.ค. 2569** · บรรทัด **อายุตัว 29 ปี · อายุงาน 3 ปี 4 เดือน** | ☐ |
| 4 | CLICK ปุ่มวงกลมทุกข้อในการ์ด **2** | A: ข้อละ 1 ระดับ ครบ 26 ข้อ | ตัวนับ **ตอบ 26/26** · การ์ดสรุปขวา **เฉลี่ย … จาก 5** | ☐ |
| 5 | CLICK ปัจจัยในการ์ด **3** ตามลำดับ | A: เงินเดือน/ค่าตอบแทนน้อยกว่าที่ต้องการ → ได้งานใหม่ที่ชอบมากกว่า | เลข **1** และ **2** ขึ้นที่ปัจจัยตามลำดับที่กด | ☐ |
| 6 | TYPE → **สิ่งที่ควรปรับปรุง** / **เหตุผล/แนวทางการปรับปรุง** ข้อ 1 | A | ช่องแสดงค่าที่กรอก | ☐ |
| 7 | CLICK **ถัดไป** 2 ครั้ง → CLICK **บันทึกและส่งแบบสอบถาม** | — | modal **ส่งแบบสอบถาม?** แสดง **ไม่มีขั้นพิจารณา** · **ส่งถึงฝ่ายบุคคล (HR) รับทราบ · ผู้บังคับบัญชาไม่เห็นคำตอบ** | ☐ |
| 8 | CLICK **ส่งแบบสอบถาม** → WAIT toast | — | toast **ส่งแบบสอบถามแล้ว · EXI-2569-0008** · แถวใหม่ pill **ส่งแล้ว** ลายเซ็น **1/1** | ☐ |

#### TC-C02 — กรณีไม่จ้างต่อ (ครบสัญญาจ้าง) เลือกเหตุผล "อื่น ๆ"
- group: สร้างแบบสอบถาม · ความสำคัญ: สูง · trace: US-03 / BR-02 / DEC-14
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: B
- ผ่านเมื่อ: บันทึกได้ · ข้อ 5 = อื่น ๆ + ข้อความ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างแบบสอบถาม** → SELECT **ผู้ให้ข้อมูล (HR สร้างแทน)** | B: ณัฐชา บุญมา | การ์ด 1 แสดงข้อมูลของ ณัฐชา · เลือก **ไม่จ้างต่อ(ครบสัญญาจ้าง)** ให้อัตโนมัติ (ลูกจ้างชั่วคราว) | ☐ |
| 2 | CLICK chip **อื่น ๆ** → TYPE ช่อง **อื่น ๆ** | B: ครบโครงการชั่วคราว | ช่องแสดงข้อความ | ☐ |
| 3 | VERIFY บรรทัดคำนวณ | — | ข้อความ **คำนวณอัตโนมัติถึง**วันสิ้นสุดสัญญา | ☐ |
| 4 | CLICK/TYPE ตามลำดับ: ตอบการ์ด 2 ครบ + เลือกปัจจัย 1 ข้อ → CLICK **ถัดไป** 2 ครั้ง → **บันทึกแบบร่าง** | B | toast **บันทึกร่างแล้ว · EXI-2569-…** · แถวใหม่ pill **ร่าง** | ☐ |

#### TC-C03 — HR สร้างแทนต้องเลือกผู้ให้ข้อมูลก่อน [AI-DEFAULT]
- group: สร้างแบบสอบถาม · ความสำคัญ: สูง · trace: AC-07 / DEC-04 [AI-DEFAULT]
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่เลือก = บล็อก · เลือกแล้วการ์ดแสดงข้อมูล · ประวัติ "สร้างแทน …"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างแบบสอบถาม** → CLICK **ถัดไป** ทันที | — | toast **กรุณากรอกข้อมูลให้ครบถ้วน** · ช่อง **ผู้ให้ข้อมูล (HR สร้างแทน)** ขอบแดง **กรุณาเลือกผู้ให้ข้อมูล** | ☐ |
| 2 | SELECT ผู้ให้ข้อมูล | สมชาย ทดสอบดี | การ์ด 1 แสดงข้อมูล EMP-00123 · การ์ด 2–4 ปรากฏ | ☐ |
| 3 | CLICK/TYPE ตามลำดับ: ทำต่อจนบันทึกแบบร่าง → เปิดใบ → แท็บ **ประวัติ** | — | รายการ **สร้างเอกสาร** หมายเหตุ **สร้างแทน** สมชาย ทดสอบดี | ☐ |

#### TC-C04 — บันทึกร่าง → แก้ไข → ส่ง (เลขเดิม)
- group: สร้างแบบสอบถาม · ความสำคัญ: สูง · trace: BR-07 / DEC-10 / FN-03
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แก้ร่างได้ · ส่งแล้วเลขยังเป็น EXI-2569-0006

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/exit-interview/view/R6` | — | drawer **EXI-2569-0006** pill **ร่าง** · ปุ่ม **ยกเลิก · แก้ไข · ส่งแบบสอบถาม** | ☐ |
| 2 | CLICK **แก้ไข** | — | drawer ดูปิด แล้ว wizard เปิด หัว **แก้ไขเอกสาร** **EXI-2569-0006** ค่าเดิมครบ | ☐ |
| 3 | TYPE → **ความคิดเห็น/ข้อเสนอแนะอื่นๆ เพิ่มเติม** → CLICK **ถัดไป** 2 ครั้ง → **บันทึกและส่งแบบสอบถาม** → **ส่งแบบสอบถาม** | ขอบคุณครับ | toast **ส่งแบบสอบถามแล้ว · EXI-2569-0006** (เลขเดิม) | ☐ |

#### TC-C05 — คำนวณอายุตัว/อายุงานอัตโนมัติจากวันที่ลาออก [AI-DEFAULT]
- group: สร้างแบบสอบถาม · ความสำคัญ: สูง · trace: BR-01 / DEC-04 [AI-DEFAULT] / FN-02
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เปลี่ยนวันที่ลาออก → ตัวเลขเปลี่ยนตาม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง **วันที่ลาออก** → เลือก | 31 ต.ค. 2569 | บรรทัด **อายุตัว 29 ปี · อายุงาน 3 ปี 4 เดือน** | ☐ |
| 2 | CLICK ช่อง **วันที่ลาออก** → เลือกใหม่ | 30 มิ.ย. 2570 | บรรทัดเปลี่ยนเป็น **อายุตัว 30 ปี · อายุงาน 4 ปี 0 เดือน** | ☐ |

#### TC-C06 — ปรับอายุตัว/อายุงานเอง [AI-DEFAULT]
- group: สร้างแบบสอบถาม · ความสำคัญ: กลาง · trace: BR-01 / DEC-04 [AI-DEFAULT]
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ค่าปรับเองไม่ถูกคำนวณทับ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ลิงก์ **ปรับ** ในบรรทัดคำนวณ | — | ช่อง **อายุตัว (ปี)** **อายุงาน (ปี)** **(เดือน)** ปรากฏ | ☐ |
| 2 | TYPE → **อายุตัว (ปี)** | 31 | บรรทัดแสดง **อายุตัว 31 ปี** · ข้อความ **ปรับเอง** | ☐ |
| 3 | CLICK **เสร็จ** → เปลี่ยนวันที่ลาออก | — | อายุตัวยังเป็น **31** (ไม่คำนวณทับ) | ☐ |

#### TC-C07 — แนบไฟล์ประกอบ
- group: สร้างแบบสอบถาม · ความสำคัญ: กลาง · trace: DEC-11 / API-12
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=หนังสือลาออก.pdf
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: files=หนังสือลาออก.pdf
- ผ่านเมื่อ: ไฟล์ขึ้นในรายการ + ขั้นตรวจสอบนับ 1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK/TYPE ตามลำดับ: กรอกขั้น 1 ครบ → CLICK **ถัดไป** | A | หัว **แนบเอกสารประกอบ (ถ้ามี)** | ☐ |
| 2 | UPLOAD → กล่อง **คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)** | หนังสือลาออก.pdf | แถวไฟล์ **หนังสือลาออก.pdf** + ขนาด | ☐ |
| 3 | CLICK **ถัดไป** | — | การ์ด **เอกสารแนบ** นับ **1** | ☐ |

### กลุ่ม V — กรอกไม่ครบ / ผิด

#### TC-V01 — กดถัดไปโดยไม่ตอบ = บล็อก
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: สูง · trace: VR-02/06/07 (auto: e2e S7)
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก + toast + การ์ดขอบแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างแบบสอบถาม** → CLICK **ถัดไป** | — | toast **กรุณากรอกข้อมูลให้ครบถ้วน** · ช่อง **วันที่ลาออก** แดง **กรุณาเลือกวันที่ลาออก (ไม่ก่อนวันเริ่มงาน)** · การ์ด 2 **ยังไม่ได้ตอบ 26 ข้อ — ตอบให้ครบทุกข้อ** · การ์ด 3 **เลือกอย่างน้อย 1 ปัจจัย** | ☐ |

#### TC-V02 — วันที่ลาออกก่อนวันเริ่มงานเลือกไม่ได้
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: สูง · trace: VR-02 / EC-02
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: วันก่อน 1 มิ.ย. 2566 กดไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง **วันที่ลาออก** → เลื่อนไปเดือน **พฤษภาคม 2566** | — | ทุกวันในเดือนเป็นสีจาง กดไม่ได้ | ☐ |

#### TC-V03 — ไม่จ้างต่อแต่ไม่เลือกเหตุผลข้อ 5
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: สูง · trace: VR-03 / DEC-14
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก "เลือกเหตุผลกรณีครบสัญญาจ้าง"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ไม่จ้างต่อ(ครบสัญญาจ้าง)** → ตอบส่วนอื่นครบ → CLICK **ถัดไป** | — | ข้อความแดง **เลือกเหตุผลกรณีครบสัญญาจ้าง** · ไม่ไปขั้นถัดไป | ☐ |

#### TC-V04 — เลือก "อื่น ๆ" ข้อ 5 แต่ไม่ระบุ
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: กลาง · trace: VR-04
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก "กรุณาระบุ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ไม่จ้างต่อ(ครบสัญญาจ้าง)** → CLICK chip **อื่น ๆ** → CLICK **ถัดไป** | — | ช่อง **อื่น ๆ** ขอบแดง **กรุณาระบุ** | ☐ |

#### TC-V05 — ตอบส่วนที่ 2 ไม่ครบ 1 ข้อ
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: สูง · trace: VR-06 / DEC-16
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก + แถวที่ขาดเป็นสีแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK/TYPE ตามลำดับ: ตอบการ์ด 2 ทุกข้อยกเว้นข้อ 26 → กรอกส่วนอื่นครบ → CLICK **ถัดไป** | — | ข้อความ **ยังไม่ได้ตอบ 1 ข้อ — ตอบให้ครบทุกข้อ** · แถว **26. ความพร้อมของอุปกรณ์ เครื่องมือเครื่องใช้ในการทำงาน** ตัวแดง | ☐ |
| 2 | CLICK วงกลมข้อ 26 | — | ตัวนับ **ตอบ 26/26** · การ์ด 2 ไม่มีขอบแดง | ☐ |

#### TC-V06 — ไม่เลือกปัจจัยส่วนที่ 3
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: สูง · trace: VR-07 / DEC-15
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก "เลือกอย่างน้อย 1 ปัจจัย"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK/TYPE ตามลำดับ: กรอกส่วนอื่นครบ ไม่เลือกปัจจัย → CLICK **ถัดไป** | — | การ์ด 3 ขอบแดง **เลือกอย่างน้อย 1 ปัจจัย** | ☐ |

#### TC-V07 — เลือกปัจจัย "อื่นๆ โปรดระบุ" แต่ไม่ระบุ
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: กลาง · trace: VR-08
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก "กรุณาระบุ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปัจจัย **อื่นๆ โปรดระบุ** → CLICK **ถัดไป** | — | ช่อง **อื่นๆ โปรดระบุ** ขอบแดง **กรุณาระบุ** | ☐ |

#### TC-V08 — อายุตัวเกินช่วง 15–80
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: ต่ำ · trace: VR-05
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก "15–80 ปี"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ปรับ** → TYPE **อายุตัว (ปี)** → CLICK **ถัดไป** | 95 | ช่องขอบแดง **15–80 ปี** | ☐ |

#### TC-V09 — อายุงานเดือนเกิน 11
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: ต่ำ · trace: VR-05
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก "เดือน 0–11"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ปรับ** → TYPE **(เดือน)** → CLICK **ถัดไป** | 12 | ช่องขอบแดง **เดือน 0–11** | ☐ |

#### TC-V10 — แนบไฟล์ชนิดไม่รองรับ
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: กลาง · trace: API-12 file policy
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=script.exe
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: files=script.exe
- ผ่านเมื่อ: ไม่แนบ + toast

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD → กล่องแนบไฟล์ | script.exe | toast **script.exe — ชนิดไฟล์ไม่รองรับ** · ไม่มีแถวไฟล์ | ☐ |

#### TC-V11 — แนบไฟล์เกิน 20 MB
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: ต่ำ · trace: API-12 file policy
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=big-25MB.pdf
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: files=big-25MB.pdf
- ผ่านเมื่อ: ไม่แนบ + toast

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD → กล่องแนบไฟล์ | big-25MB.pdf | toast **big-25MB.pdf — ไฟล์ใหญ่เกินกำหนด (สูงสุด 20 MB)** | ☐ |

### กลุ่ม R — ลำดับปัจจัย

#### TC-R01 — กดปัจจัยตามลำดับได้หมายเลข 1,2,3
- group: ลำดับปัจจัย · ความสำคัญ: สูง · trace: BR-04 / DEC-15 / LD-03
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: หมายเลขตามลำดับกด + การ์ดสรุปอันดับ 1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปัจจัย 3 ตัวตามลำดับ | ไม่เห็นโอกาสความก้าวหน้าในอาชีพการงาน → ปัญหาการเดินทาง → ศึกษาต่อ | เลข **1 2 3** ตามลำดับ · รายการลำดับด้านล่าง 3 แถว | ☐ |
| 2 | VERIFY การ์ดสรุปขวา **ส่วนที่ 3** | — | **3 ปัจจัย · อันดับ 1 ไม่เห็นโอกาสความก้าวหน้าในอาชีพการงาน** | ☐ |

#### TC-R02 — กดซ้ำเอาออก → เลขเรียงใหม่ต่อเนื่อง
- group: ลำดับปัจจัย · ความสำคัญ: กลาง · trace: BR-04
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีเลขซ้ำ/เว้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK/TYPE ตามลำดับ: เลือก 3 ปัจจัยแบบ TC-R01 → CLICK ปัจจัยอันดับ **1** ซ้ำ | — | ตัวนั้นไม่มีเลข · ที่เหลือเป็น **1 2** | ☐ |

#### TC-R03 — เลื่อนลำดับขึ้น/ลง
- group: ลำดับปัจจัย · ความสำคัญ: กลาง · trace: BR-04
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ลำดับสลับ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK/TYPE ตามลำดับ: เลือก 2 ปัจจัย → CLICK ปุ่ม **เลื่อนลง** ที่แถวลำดับ 1 | — | สองแถวสลับกัน · เลขที่ปุ่มปัจจัยสลับตาม | ☐ |

### กลุ่ม S — ส่งแบบสอบถาม

#### TC-S01 — modal ส่ง: 0 ขั้นพิจารณา (DOA ค่าเริ่ม)
- group: ส่งแบบสอบถาม · ความสำคัญ: สูง · trace: AC-12 / DEC-03 [AI-DEFAULT] (auto: e2e S8)
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีแถวเลือกผู้พิจารณา + ข้อความส่งถึง HR

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งแบบสอบถาม** | — | modal **ส่งแบบสอบถาม?** · แถว **0 ไม่มีขั้นพิจารณา** · **ส่งถึงฝ่ายบุคคล (HR) รับทราบ · ผู้บังคับบัญชาไม่เห็นคำตอบ** · **ส่วนที่ 2 ตอบ 26/26** | ☐ |

#### TC-S02 — ร่างที่ยังไม่ครบ ส่งไม่ได้
- group: ส่งแบบสอบถาม · ความสำคัญ: กลาง · trace: BR-03/04 / FN-04
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/view/R5`
- ชุดข้อมูล: seed=R5 ร่างของ HR (ตอบครบ ไม่มีปัจจัย)
- ผ่านเมื่อ: ปุ่มส่ง disabled + แถบแจ้ง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งแบบสอบถาม** | — | แถบแดง **ข้อมูลยังไม่ครบ — แก้ไขร่างให้ครบก่อนส่ง** · ปุ่ม **ส่งแบบสอบถาม** กดไม่ได้ | ☐ |

#### TC-S03 — ส่งไม่สำเร็จ (API ล้ม) สถานะไม่เปลี่ยน
- group: ส่งแบบสอบถาม · ความสำคัญ: กลาง · trace: 06 §6.10 (auto: e2e S9)
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=__QA__.sim('error') · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: toast error + ยังเป็นร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งแบบสอบถาม** → CLICK ปุ่ม **ส่งแบบสอบถาม** ใน modal | — | toast **ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง** · pill ยัง **ร่าง** | ☐ |

### กลุ่ม X — ยกเลิก

#### TC-X01 — เจ้าของยกเลิกร่างพร้อมเหตุผล
- group: ยกเลิก · ความสำคัญ: สูง · trace: AC-11 / BR-11 [AI-DEFAULT]
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สถานะยกเลิก + แบนเนอร์เหตุผล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ⋮ แถว **EXI-2569-0006** → **ยกเลิกเอกสาร** | — | modal **ยกเลิกเอกสาร?** · chip **บันทึกผิดคน · พนักงานเปลี่ยนใจไม่ลาออก · บันทึกซ้ำ** | ☐ |
| 2 | CLICK chip **บันทึกซ้ำ** → CLICK **ยกเลิกเอกสาร** | — | toast **ยกเลิกเอกสารแล้ว · EXI-2569-0006** · pill **ยกเลิก** | ☐ |
| 3 | OPEN ใบนั้น | — | แบนเนอร์ **ยกเลิกแล้ว — บันทึกซ้ำ** | ☐ |

#### TC-X02 — ยกเลิกโดยไม่ใส่เหตุผล = บล็อก
- group: ยกเลิก · ความสำคัญ: สูง · trace: VR-09
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ช่องเหตุผลแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ⋮ → **ยกเลิกเอกสาร** → CLICK **ยกเลิกเอกสาร** ทันที | — | ช่อง **เหตุผล** ขอบแดง **กรุณาระบุเหตุผล** · modal ไม่ปิด | ☐ |

#### TC-X03 — HR ยกเลิกใบที่ส่งแล้ว
- group: ยกเลิก · ความสำคัญ: สูง · trace: BR-11 / exi_cancelled
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ยกเลิกได้ · สถานะยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/exit-interview/view/R1` | — | ปุ่มหัว **ยกเลิกเอกสาร** | ☐ |
| 2 | CLICK **ยกเลิกเอกสาร** → TYPE เหตุผล → CLICK **ยกเลิกเอกสาร** | บันทึกผิดคน | toast **ยกเลิกเอกสารแล้ว · EXI-2569-0001** · pill **ยกเลิก** | ☐ |

#### TC-X04 — ใบที่ยกเลิกแล้วไม่มีปุ่มยกเลิก/แก้ไข
- group: ยกเลิก · ความสำคัญ: กลาง · trace: 05 §5.2
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่ม action

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/exit-interview/view/R3` | — | แบนเนอร์ **ยกเลิกแล้ว — พนักงานเปลี่ยนใจไม่ลาออก — ได้รับการปรับตำแหน่ง** · ไม่มีปุ่มยกเลิก/แก้ไข · มีปุ่มพิมพ์/ดาวน์โหลด | ☐ |

### กลุ่ม P — ใครเห็นอะไร

#### TC-P01 — ผู้บังคับบัญชาไม่เห็นใบของลูกน้อง (ความลับ)
- group: ใครเห็นอะไร · ความสำคัญ: สูง · trace: AC-09 / DEC-17 / TC-D01 (auto: e2e S2/S3)
- actor (role): ผู้บังคับบัญชาของ E01
- Setup: role=ผู้บังคับบัญชาของ E01 (__QA__.setMe('E02')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีใบ EXI-2569-0006 ในรายการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/exit-interview` | — | ตารางว่าง **ยังไม่มีแบบสอบถาม** · ไม่เห็น EXI-2569-0006 ของสมชาย | ☐ |

#### TC-P02 — ผู้บังคับบัญชาเปิด URL ใบลูกน้องตรง ๆ ไม่ได้
- group: ใครเห็นอะไร · ความสำคัญ: สูง · trace: EC-06 / TC-D02 (auto: e2e S6)
- actor (role): ผู้บังคับบัญชาของ E01
- Setup: role=ผู้บังคับบัญชาของ E01 (__QA__.setMe('E02')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่เปิด drawer

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/exit-interview/view/R6` | — | อยู่ที่หน้ารายการ ไม่มี drawer เปิด (ไม่พบใบ) | ☐ |

#### TC-P03 — ผู้ให้ข้อมูลไม่เห็นร่างของคนอื่น
- group: ใครเห็นอะไร · ความสำคัญ: สูง · trace: TC-D03 (auto: e2e S3)
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่เห็น EXI-2569-0005 (ร่างของ HR)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตาราง | — | ไม่มี **EXI-2569-0005** และ **EXI-2569-0007** | ☐ |

#### TC-P04 — ผู้ให้ข้อมูลเห็นใบที่ HR สร้างแทน แต่แก้ร่างไม่ได้
- group: ใครเห็นอะไร · ความสำคัญ: สูง · trace: EC-07 / TC-D04 / LD-02
- actor (role): ผู้ให้ข้อมูล E09
- Setup: role=ผู้ให้ข้อมูล E09 (ต้องเพิ่ม persona — ต้อง simulate) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/view/R5`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นใบ · ไม่มีปุ่มแก้ไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/exit-interview/view/R5` | — | drawer **EXI-2569-0005** · ไม่มีปุ่ม **แก้ไข** · มีปุ่ม **ยกเลิกเอกสาร** | ☐ |

#### TC-P05 — ใบส่งแล้วล็อกแก้ไข
- group: ใครเห็นอะไร · ความสำคัญ: สูง · trace: BR-14 / TC-D05
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview`
- ชุดข้อมูล: seed=ส่ง EXI-2569-0006 ก่อน (TC-C04)
- ผ่านเมื่อ: ไม่มีปุ่มแก้ไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN ใบที่ส่งแล้วของตัวเอง | — | footer **ส่งแล้ว ล็อกแก้ไข** · ไม่มีปุ่ม **แก้ไข** · เมนู ⋮ ไม่มี **แก้ไข** | ☐ |

#### TC-P06 — ผู้ใช้ทั่วไปส่งออก CSV ได้เฉพาะใบที่เห็น
- group: ใครเห็นอะไร · ความสำคัญ: กลาง · trace: TC-D07
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview`
- ชุดข้อมูล: —
- ผ่านเมื่อ: toast ส่งออก 1 รายการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งออก CSV** | — | toast **ส่งออก 1 รายการ** | ☐ |

### กลุ่ม D — แบบพิมพ์ PDF

#### TC-D01 — PDF ร่าง: มี "ร่าง" + ช่องลงชื่อว่าง
- group: แบบพิมพ์ PDF · ความสำคัญ: สูง · trace: AC-10 / BR-09 (auto: e2e S4)
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: footer มี "· ร่าง" · ช่องวันที่ลงชื่อเป็นเส้นประ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | เห็นแบบฟอร์ม **แบบสอบถามบุคลากรที่พ้นจากงาน ( Exit Interview)** · **Doc No. FM-HRM-06 · Rev. 00 : 01/07/2569** | ☐ |
| 2 | VERIFY ท้ายเอกสาร | — | **เลขที่ EXI-2569-0006 · ร่าง** · ช่อง **ผู้ให้ข้อมูล** บรรทัด **วันที่ ........./........./.........** | ☐ |

#### TC-D02 — PDF ส่งแล้ว: ค่าครบ + ส่งในระบบ
- group: แบบพิมพ์ PDF · ความสำคัญ: สูง · trace: AC-10 / DEC-08
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ทุกช่องตรงข้อมูล · ✓ ครบ 26 ข้อ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | ส่วนที่ 1 ชื่อ **ปิยะนุช แก้วมณี** · ☑ **วันที่ลาออก 31 สิงหาคม 2569** · ☑ **ลูกจ้างประจำ** | ☐ |
| 2 | VERIFY ส่วนที่ 2 และ 3 | — | ทุกข้อมี ✓ 1 ช่อง · กล่องปัจจัยที่เลือกมีหมายเลข [1], [2], [3] | ☐ |
| 3 | VERIFY ช่องลงชื่อ | — | **ส่งในระบบ 25 ส.ค. 2569 10:30 น.** · ไม่มีภาพลายเซ็น | ☐ |

#### TC-D03 — PDF กรณีครบสัญญา: ☑ ข้อ 5 ถูกช่อง
- group: แบบพิมพ์ PDF · ความสำคัญ: กลาง · trace: DEC-14 / FN-08
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/view/R2`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ☑ ไม่จ้างต่อ + ☑ เป็นความประสงค์ของหน่วยงาน/ส่วนงาน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | ☑ **ไม่จ้างต่อ(ครบสัญญาจ้าง)** · ช่องวันที่ลาออกว่าง · ข้อ 5 ☑ **เป็นความประสงค์ของหน่วยงาน/ส่วนงาน** | ☐ |

#### TC-D04 — PDF เลือกครบ 21 ปัจจัย
- group: แบบพิมพ์ PDF · ความสำคัญ: กลาง · trace: EC-04 / DEC-05
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: C: เลือกครบ 21
- ผ่านเมื่อ: PDF แสดง [1]..[21]

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK/TYPE ตามลำดับ: สร้างใบ เลือกปัจจัยครบ 21 ตัว (ระบุอื่นๆ) → บันทึกแบบร่าง → เปิดแท็บ **PDF Preview** | C | ทุกกล่องปัจจัยมีหมายเลข **[1]**…**[21]** ไม่ซ้ำ · ข้อความอื่นๆ แสดงในบรรทัด | ☐ |

#### TC-D05 — PDF ข้อเสนอแนะ 12 แถว ไม่ตัดแถว
- group: แบบพิมพ์ PDF · ความสำคัญ: กลาง · trace: EC-05 / DEC-06
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: D: 12 แถว
- ผ่านเมื่อ: ครบ 12 แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK/TYPE ตามลำดับ: สร้างใบ เพิ่มข้อเสนอแนะ 12 ข้อ → บันทึกแบบร่าง → **PDF Preview** | D | ตารางส่วนที่ 4 มี 12 แถวเรียง 1–12 | ☐ |

#### TC-D06 — ช่องลงชื่อ PDF งอกตามขั้น DOA
- group: แบบพิมพ์ PDF · ความสำคัญ: สูง · trace: BR-08/09 / DEC-03 [AI-DEFAULT] / AC-13
- actor (role): ผู้ให้ข้อมูล · seed=__QA__.doa.push
- Setup: role=ผู้ให้ข้อมูล · seed=__QA__.doa.push('ฝ่ายบุคคลรับทราบ') (ต้อง simulate ที่ DOA กลาง) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สร้างใบใหม่หลังตั้งขั้น → PDF มี 2 ช่องลงชื่อ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK/TYPE ตามลำดับ: สร้างและส่งใบใหม่ (เลือกผู้พิจารณา **ศศิธร มีสุข**) → แท็บ **PDF Preview** | A | ช่องลงชื่อ 2 ช่อง: **ผู้ให้ข้อมูล** + **ฝ่ายบุคคลรับทราบ** (☐ รับทราบ ☐ ส่งกลับ) | ☐ |

### กลุ่ม E — การใช้งานทั่วไป

#### TC-E01 — ปิด wizard ตอนกรอกค้าง = ถามก่อนทิ้ง
- group: การใช้งานทั่วไป · ความสำคัญ: กลาง · trace: U15 / 01 §1.2
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal ทิ้งข้อมูล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → **สาขา** → CLICK ปุ่ม x | ทดสอบ | modal **ทิ้งข้อมูลที่กรอกไว้?** · ปุ่ม **กลับไปกรอกต่อ** / **ทิ้งข้อมูล** | ☐ |
| 2 | CLICK **กลับไปกรอกต่อ** | — | ค่า **ทดสอบ** ยังอยู่ | ☐ |

#### TC-E02 — Esc ปิด modal ก่อน drawer
- group: การใช้งานทั่วไป · ความสำคัญ: ต่ำ · trace: U8 (auto: e2e S10)
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: Esc ครั้งแรกปิด modal ครั้งที่สองปิด drawer

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งแบบสอบถาม** → PRESS Esc | — | modal ปิด drawer ยังเปิด | ☐ |
| 2 | PRESS Esc | — | drawer ปิด | ☐ |

#### TC-E03 — ลากเมาส์จากใน drawer ไปปล่อยนอก ไม่ปิด
- group: การใช้งานทั่วไป · ความสำคัญ: ต่ำ · trace: U25
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: drawer ยังเปิด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS เมาส์ค้างในข้อความ drawer → ลากไปปล่อยที่พื้นหลัง | — | drawer ยังเปิด | ☐ |

#### TC-E04 — แบบเอกสารปิดใช้งาน สร้างไม่ได้
- group: การใช้งานทั่วไป · ความสำคัญ: กลาง · trace: EC-09 / BR-07
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=__QA__.setDocActive(false) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปุ่มสร้าง disabled + แถบแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัวหน้ารายการ | — | ปุ่ม **สร้างแบบสอบถาม** กดไม่ได้ · แถบ **แบบเอกสารนี้ยังไม่เปิดใช้งาน — สร้างแบบสอบถามใหม่ไม่ได้** | ☐ |

### กลุ่ม K — สายอนุมัติ (DOA)

#### TC-K01 — เพิ่มขั้น DOA → modal ส่งมีแถวเลือกผู้พิจารณาเพิ่ม
- group: สายอนุมัติ (DOA) · ความสำคัญ: สูง · trace: AC-13 / BR-08 (auto: e2e S8)
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=__QA__.doa.push('ฝ่ายบุคคลรับทราบ') · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แถวผู้พิจารณา 1 แถว ค่าเริ่ม ศศิธร มีสุข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งแบบสอบถาม** | — | แถว **1 ฝ่ายบุคคลรับทราบ** ช่องเลือกผู้พิจารณาค่าเริ่ม **ศศิธร มีสุข** · **ค่าเริ่มต้นจากสายอนุมัติ (DOA กลาง)** | ☐ |

#### TC-K02 — ผู้พิจารณารับทราบ → พิจารณาแล้ว
- group: สายอนุมัติ (DOA) · ความสำคัญ: กลาง · trace: FN-05 / BR-08
- actor (role): HR · seed=ตั้งขั้น DOA 1 ขั้น + ใบ pending
- Setup: role=HR · seed=ตั้งขั้น DOA 1 ขั้น + ใบ pending · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview`
- ชุดข้อมูล: —
- ผ่านเมื่อ: pill พิจารณาแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK/TYPE ตามลำดับ: เปิดใบรอพิจารณา → CLICK **รับทราบ** → CLICK **รับทราบ** ใน modal | — | toast **รับทราบแล้ว · EXI-…** · pill **พิจารณาแล้ว** | ☐ |

#### TC-K03 — ส่งกลับแก้ไข → ร่างเลขเดิม
- group: สายอนุมัติ (DOA) · ความสำคัญ: กลาง · trace: FN-06 / BR-11 [AI-DEFAULT]
- actor (role): HR · seed=ตั้งขั้น DOA 1 ขั้น + ใบ pending
- Setup: role=HR · seed=ตั้งขั้น DOA 1 ขั้น + ใบ pending · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview`
- ชุดข้อมูล: —
- ผ่านเมื่อ: กลับเป็นร่าง เลขเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK/TYPE ตามลำดับ: เปิดใบรอพิจารณา → CLICK **ส่งกลับแก้ไข** → TYPE เหตุผล → CLICK **ส่งกลับ** | ข้อมูลไม่ครบ ขอรายละเอียดเพิ่ม | toast **ส่งกลับแล้ว · EXI-…** · pill **ร่าง** เลขเดิม | ☐ |

### กลุ่ม H — ประวัติ

#### TC-H01 — ประวัติเป็นลำดับเวลา append-only
- group: ประวัติ · ความสำคัญ: กลาง · trace: 01 §1.4 / audit
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ประวัติ 3 รายการ ล่าสุดอยู่บน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **ประวัติ** | — | ลำดับบนลงล่าง **ยกเลิกเอกสาร** (เหตุผล) → **ส่งแบบสอบถาม** → **สร้างเอกสาร** · แต่ละรายการมีวงกลมรูปคน + ชื่อ + เวลา | ☐ |

#### TC-H02 — แท็บลายเซ็น / อนุมัติ แสดงไม่มีสาย
- group: ประวัติ · ความสำคัญ: กลาง · trace: BR-08 / §6.1
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สรุป "ไม่มีสาย · 0 ขั้น" + ผลลัพธ์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **ลายเซ็น / อนุมัติ** | — | การ์ดสรุป **ไม่มีสาย · 0 ขั้น** · **1/1** · timeline **ส่งแบบสอบถาม (ผู้ให้ข้อมูล)** → **ผลลัพธ์ ฝ่ายบุคคลได้รับแบบสอบถามแล้ว** | ☐ |

### กลุ่ม XT — เชื่อมระบบอื่น

#### TC-XT01 — ส่งแล้วแจ้ง HR (exi_submitted)
- group: เชื่อมระบบอื่น · ความสำคัญ: กลาง · trace: NTF exi_submitted / FN-09 (ต้อง simulate)
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: HR ได้แจ้งเตือน in-app ไม่มีคำตอบในข้อความ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK/TYPE ตามลำดับ: ส่งใบ EXI-2569-0006 → สลับเป็น HR → VERIFY กระดิ่ง/เมนู | — | (ต้นแบบ) ตัวเลขเมนู **Exit Interview** เพิ่ม 1 · ระบบจริง: แจ้งเตือนตาม NTF_BRIEF (exi_submitted) ⚠ ยืนยัน anchor | ☐ |

#### TC-XT02 — เลขเอกสารจาก F-DOCCFG รูปแบบ EXI-ปี-ลำดับ
- group: เชื่อมระบบอื่น · ความสำคัญ: กลาง · trace: BR-07 / DOCCFG EXI
- actor (role): ผู้ให้ข้อมูล
- Setup: role=ผู้ให้ข้อมูล (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/exit-interview/create`
- ชุดข้อมูล: A
- ผ่านเมื่อ: เลขรูปแบบ EXI-2569-NNNN

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK/TYPE ตามลำดับ: สร้างและบันทึกแบบร่าง | A | toast **บันทึกร่างแล้ว · EXI-2569-0008** (รูปแบบตามที่ตั้งไว้ที่ Document Configuration) | ☐ |

## วิธีที่ agent รัน (Run protocol)
1. เปิด feature.html → ไปที่ `#/exit-interview`
2. ตั้ง role ตาม Setup ด้วย `__QA__.setMe('E01'|'E02'|'E08')` (ตัวสลับผู้ใช้มุมขวาบนก็ได้)
3. seed พิเศษ: `__QA__.sim('error')` · `__QA__.setDocActive(false)` · `__QA__.doa.push(label)` — รีโหลดหน้าเพื่อล้าง
4. ทำ step ตามลำดับ · บันทึกผลตาม schema · เคส (auto: e2e …) ใช้ผล e2e_standard.py ได้

## Coverage Audit
| หมวด | covered / total |
|---|---|
| AC (06_TESTS) | 13 / 13 |
| Business rules (05_RULES) | 14 / 14 |
| Validation | 9 / 9 |
| Edge cases | 8 / 10 |
| Permission cells | 8 / 8 |
| Cross-cutting / events / states | ครบ |

- Cross-Module (XT): 3/3
- Scope Lock (DEC): 17/17
- **Manifest cross-check (FRD §0.12): ✅ 8/8**

### ข้าม (พร้อมเหตุผล)
- EC-01 ไม่มี birth_date · EC-03 ไม่มี contract_end_date — seed ต้นแบบไม่มีกรณีนี้ → ทดสอบตอน UAT ระบบจริง

## Result Report (schema)
```json
{
 "feature_id": "F-TMP-002",
 "run_at": "<iso datetime>",
 "results": [
  {
   "id": "TC-L01",
   "status": "pass|fail|blocked",
   "failed_step": null,
   "evidence": "",
   "note": ""
  }
 ],
 "summary": {
  "total": 58,
  "pass": 0,
  "fail": 0,
  "blocked": 0
 }
}
```

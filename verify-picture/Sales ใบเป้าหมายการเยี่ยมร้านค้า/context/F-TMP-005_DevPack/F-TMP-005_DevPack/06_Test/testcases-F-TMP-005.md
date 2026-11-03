# AI Test Cases — F-TMP-005 ใบเป้าหมายการเยี่ยมร้านค้า : เขตการขาย General Trade

ชุดเคสสำหรับ AI agent (browser-use/vision) ทดสอบบน prototype `feature.html` · anchor = ข้อความบนจอจริง (HTML > 01_UI) · เคสที่ derive จากมติ AI-DEFAULT ติดป้าย [AI-DEFAULT] — fail อาจแปลว่า "ค่าเริ่มผิด" ไม่ใช่โค้ดผิด

## Meta
| รายการ | ค่า |
|---|---|
| Feature ID | F-TMP-005 |
| ชื่อ | ใบเป้าหมายการเยี่ยมร้านค้า : เขตการขาย General Trade |
| เวอร์ชัน | 1.0 |
| App entry | feature.html |
| Routes | `#/visit-target` · `#/visit-target/create` · `#/visit-target/edit/:id` · `#/visit-target/view/:id` |
| ที่มา | FRD_F-TMP-005_Pack · BRD_F-TMP-005 · feature.html · DECISIONS.lock |
| จำนวนเคส | 41 |
| หมวด | L ดูรายการ · C สร้างใบเป้าหมาย · V กรอกไม่ครบ / ผิด · S ส่งอนุมัติ · A อนุมัติ / ไม่อนุมัติ · X ยกเลิก · P ใครเห็นอะไร · D แบบพิมพ์ PDF · E การใช้งานทั่วไป · H ประวัติ · XT เชื่อมระบบอื่น |

## Coverage
| group | เคส | สูง/กลาง/ต่ำ |
|---|---|---|
| L ดูรายการ | 6 | 2/3/1 |
| C สร้างใบเป้าหมาย | 7 | 4/3/0 |
| V กรอกไม่ครบ / ผิด | 7 | 4/3/0 |
| S ส่งอนุมัติ | 3 | 2/1/0 |
| A อนุมัติ / ไม่อนุมัติ | 3 | 3/0/0 |
| X ยกเลิก | 2 | 1/1/0 |
| P ใครเห็นอะไร | 4 | 3/1/0 |
| D แบบพิมพ์ PDF | 3 | 2/1/0 |
| E การใช้งานทั่วไป | 3 | 0/3/0 |
| H ประวัติ | 1 | 0/1/0 |
| XT เชื่อมระบบอื่น | 2 | 0/1/1 |

## Coverage Ledger
### FR / AC (06_TESTS)
| item | cases |
|---|---|
| AC-01 | TC-C01 |
| AC-02 | TC-C02 |
| AC-03 | TC-C01, TC-C03 |
| AC-04 | TC-V03, TC-V04 |
| AC-05 | TC-C01, TC-S01 |
| AC-06 | TC-A01 |
| AC-07 | TC-A02 |
| AC-08 | TC-XT01, TC-P02 |
| AC-09 | TC-L02, TC-L06 |
| AC-10 | TC-D01 |
| AC-11 | TC-X01, TC-X02 |
| AC-12 | TC-A03 |
| AC-13 | TC-C07 |
| AC-14 | TC-S02 |
### Business Rules (05_RULES)
| rule | cases |
|---|---|
| BR-01 | TC-C01, TC-V06 |
| BR-02 | TC-C01, TC-V01 |
| BR-03 | TC-V01, TC-V05 |
| BR-04 | TC-V03, TC-V04 |
| BR-05 | TC-V02 |
| BR-06 | TC-C03 |
| BR-07 | TC-C02, TC-C07, TC-V06 |
| BR-08 | TC-S01, TC-S02 |
| BR-09 | TC-S01, TC-P03 |
| BR-10 | TC-A02 |
| BR-11 | TC-A03, TC-C06, TC-XT01 |
| BR-12 | TC-L01, TC-L02, TC-P01, TC-P02 |
| BR-13 | TC-C04, TC-E03 |
| BR-14 | TC-D02 |
| BR-15 | TC-X01, TC-X02, TC-L06, TC-C05, TC-D01 |
### Validation (VR)
| VR | cases |
|---|---|
| VR-01 | TC-C01 |
| VR-02 | TC-V01 |
| VR-03 | TC-C01 |
| VR-04 | TC-V01, TC-V05 |
| VR-05 | TC-V04 |
| VR-06 | TC-V03 |
| VR-07 | TC-V02 |
| VR-08 | TC-V02, TC-C02 |
| VR-09 | TC-S01 |
| VR-10 | TC-A02, TC-X01 |
### Edge Cases
| EC | cases / สถานะ |
|---|---|
| EC-01 | TC-V06 |
| EC-02 | — ข้าม (seed ทุกคนมีผู้บังคับบัญชา — UAT ระบบจริง) |
| EC-03 | TC-C06, TC-A03 |
| EC-04 | TC-D03 (แบบพิมพ์ long-31rows) |
| EC-05 | TC-S02 (+ แบบพิมพ์ doa6steps) |
| EC-06 | TC-P02 |
| EC-07 | TC-V05 |
| EC-08 | TC-A02, TC-X01 |
| EC-09 | TC-E03 |
| EC-10 | TC-V03 |
### Permission Matrix (role × action)
| cell | cases |
|---|---|
| owner ดู/สร้าง/แก้ร่าง/ส่ง/ยกเลิก = allow | TC-L01, TC-C01, TC-C04, TC-X01 |
| owner อนุมัติใบตัวเอง/แก้ใบส่งแล้ว = deny (BR-DOA-04) | TC-S01, TC-P03 |
| ผู้อนุมัติ อนุมัติ/ไม่อนุมัติ ขั้นปัจจุบัน = allow | TC-A01, TC-A02 |
| ผู้อนุมัติ ดูร่างคนอื่น = deny | TC-P01 |
| ผู้อนุมัติขั้น 2 ก่อนถึงขั้น = deny | TC-P04 |
| TO/CC ดูใบอนุมัติแล้ว = allow · ใบรออนุมัติ = deny | TC-P02 |
| role-mgr-sales ดูทุกใบ/ยกเลิก/CSV/ทุกเขต = allow | TC-L02, TC-X02, TC-L06, TC-V06 |
### Cross-Module (XT — 06 §6.9)
| XT | Downstream | Case |
|---|---|---|
| ENG-NOTIFY svt_plan_published | TO + CC | TC-XT01 |
| ENG-NOTIFY svt_cancelled | ผู้อนุมัติขั้นปัจจุบัน | TC-X02 |
| F-DOCCFG / ENG-DOC-NUM | เลข SVT | TC-XT02 |
| Sales Territory / Customer prefill | เขต · ร้าน | TC-C01, TC-C02 |
### Scope Lock (DEC — 07 §7.0)
| DEC | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| DEC-01 | ไม่แก้ Customer/Sales Territory | TC-C02 |
| DEC-02 | ไม่ส่งต่อ | TC-XT01 |
| DEC-03 | DOA 2 ขั้น [AI-DEFAULT] | TC-S01, TC-A01 |
| DEC-04 | master/TO/CC/วันที่/ร้าน/ใบเดียวต่อเขต+รอบ [AI-DEFAULT] | TC-C01, TC-C02, TC-A03 |
| DEC-05 | สูงสุด 31 วัน | TC-V05 |
| DEC-06 | ช่อง 1:1 | TC-D01 |
| DEC-07 | ลงนามไม่ใช้ภาพ | TC-D02 |
| DEC-08 | ไม่อนุมัติ = กลับร่าง [AI-DEFAULT] | TC-A02, TC-X01 |
| DEC-09 | การมองเห็น [AI-DEFAULT] | TC-L02, TC-P01, TC-P02 |
| DEC-10 | เลขตอนบันทึกครั้งแรก | TC-C04 |
| DEC-11 | แนบ ✓ CSV ✓ | TC-C05, TC-L06 |
| DEC-12 | คอลัมน์ว่างไม่ใช่ช่อง | TC-D01 |
| DEC-13 | ทุกแถวมี "=" | TC-D01 |
| DEC-14 | จำนวนลูกค้านับจากร้าน | TC-C03 |
| DEC-15 | ร้าน >7 เตือน | TC-C07 |
| DEC-16 | วันที่ในรอบ/ไม่ซ้ำ | TC-V03, TC-V04 |
| DEC-17 | แถวรวม | TC-D01 |
| DEC-18 | ผู้อนุมัติ 2 ขั้น | TC-S01 |
### Cross-cutting / Events / States
| item | cases |
|---|---|
| empty state | TC-L04 |
| dirty-check ปิด wizard | TC-E01 |
| Esc chain | TC-E02 |
| API error | TC-S03 |
| state cancelled | TC-X01, TC-X02 |
| state superseded | TC-A03, TC-H01 |
| ประวัติ append-only | TC-H01 |

## Data Sets
### ชุด A
| ฟิลด์ | ค่า |
|---|---|
| เขต | GT-NE01 · เขตตะวันออกเฉียงเหนือ 1 (ค่าเริ่ม) |
| รอบการขาย | พฤศจิกายน 2569 |
| TO | หัวหน้าเขต ทดสอบสอง (ค่าเริ่ม) |
| CC | ผู้ประสานงานขาย ทดสอบห้า |
| วันทำงานที่ 1 | 2 พ.ย. 2569 · ตลาดสดเทศบาล = ตลาดนัดชุมชน · ร้าน NE01-01..04 · ที่พัก ขอนแก่น |
| วันทำงานที่ 2 | 3 พ.ย. 2569 · ตลาดเช้า = ตลาดโต้รุ่ง · ร้าน NE01-05..08 · ที่พัก (ว่าง) |
### ไฟล์ทดสอบ (Files)
| ไฟล์ | ใช้ |
|---|---|
| เส้นทางตลาด.pdf | TC-C05 |
| script.exe | TC-V07 |

## Test Cases

### กลุ่ม L — ดูรายการ

#### TC-L01 — ผู้นำเสนอเห็นเฉพาะใบของตัวเอง
- group: ดูรายการ · ความสำคัญ: สูง · trace: BR-12 / DEC-09 (auto: e2e S2)
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 4 ใบ (SVT-2569-0001, 0003, 0004, 0007) + คอลัมน์ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/visit-target` | — | หัวข้อ **ใบเป้าหมายการเยี่ยมร้านค้า** · ปุ่ม **ส่งออก CSV** · **สร้างใบเป้าหมาย** | ☐ |
| 2 | VERIFY หัวตาราง | — | คอลัมน์ **เลขที่ · รอบการขาย · เขต · ผู้รับผิดชอบเขต · วันทำงาน · จำนวนลูกค้า · สถานะเอกสาร · ลายเซ็น** | ☐ |
| 3 | VERIFY แถวในตาราง | — | 4 แถว **SVT-2569-0007** ร่าง · **0004** อนุมัติแล้ว · **0003** ถูกแทนที่ · **0001** อนุมัติแล้ว | ☐ |

#### TC-L02 — ผู้จัดการฝ่ายขายเห็นทุกใบ + ตัวเลขใต้หัวข้อ
- group: ดูรายการ · ความสำคัญ: สูง · trace: AC-09 / DEC-09 / U1 (auto: e2e S2)
- actor (role): ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2
- Setup: role=ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2 (__QA__.setMe('E04')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 8 ใบ · badge "8 รายการ" "รออนุมัติ 2" "รอคุณ 1" · ไม่มีการ์ดตัวเลข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/visit-target` | — | ตารางมี 8 แถว (SVT-2569-0001..0008) | ☐ |
| 2 | VERIFY บรรทัดคำอธิบายใต้หัวข้อ | — | ข้อความ **แผนเยี่ยมร้านรายวันของเขตการขาย General Trade** + badge **8 รายการ** **รออนุมัติ 2** **รอคุณ 1** · ไม่มีแถวการ์ดตัวเลข | ☐ |

#### TC-L03 — ค้นหา / กรองเขต / รีเซ็ต
- group: ดูรายการ · ความสำคัญ: กลาง · trace: P-01 search + filter
- actor (role): ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2
- Setup: role=ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2 (__QA__.setMe('E04')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ผลค้นหา/กรองตรงเงื่อนไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่อง **ค้นหาเลขที่ / เขต / รอบการขาย / ผู้รับผิดชอบเขต** | ภาคกลาง | เหลือ 2 แถว **SVT-2569-0008** · **0006** | ☐ |
| 2 | CLICK ปุ่ม **รีเซ็ต** แล้ว SELECT ตัวกรอง **ทุกสถานะ** → **ถูกแทนที่** | — | เหลือ 1 แถว **SVT-2569-0003** pill **ถูกแทนที่** | ☐ |
| 3 | CLICK ปุ่ม **รีเซ็ต** แล้ว SELECT **ทุกเขต** → **GT-NE02** | — | เหลือ 2 แถว **SVT-2569-0005** · **0002** | ☐ |

#### TC-L04 — ค้นหาไม่พบ = empty state
- group: ดูรายการ · ความสำคัญ: กลาง · trace: U23 / 01 §1.6
- actor (role): ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2
- Setup: role=ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2 (__QA__.setMe('E04')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target`
- ชุดข้อมูล: ค้นหา: ไม่มีเขตนี้
- ผ่านเมื่อ: แสดง "ไม่พบรายการที่ค้นหา" + ปุ่มล้างตัวกรอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา | ไม่มีเขตนี้ | ตารางว่าง แสดง **ไม่พบรายการที่ค้นหา** · **ลองปรับคำค้นหรือล้างตัวกรอง** | ☐ |
| 2 | CLICK ปุ่ม **ล้างตัวกรอง** | — | กลับมา 8 แถว | ☐ |

#### TC-L05 — แบ่งหน้า + แสดงต่อหน้า
- group: ดูรายการ · ความสำคัญ: ต่ำ · trace: U6
- actor (role): ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2
- Setup: role=ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2 (__QA__.setMe('E04')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target`
- ชุดข้อมูล: —
- ผ่านเมื่อ: footer มีแสดงต่อหน้า 25 + "1 – 8 จาก 8 รายการ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY footer ตาราง | — | **แสดงต่อหน้า** ค่า 25 · ข้อความ **1 – 8 จาก 8 รายการ** · ปุ่มหน้า 1 | ☐ |

#### TC-L06 — ส่งออก CSV ตามสิทธิ์ (1 แถวต่อวันทำงาน)
- group: ดูรายการ · ความสำคัญ: กลาง · trace: AC-09 / DEC-11 / API-11
- actor (role): ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2
- Setup: role=ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2 (__QA__.setMe('E04')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ดาวน์โหลด visit-target.csv + toast ส่งออก 8 รายการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งออก CSV** | — | toast **ส่งออก 8 รายการ** · ไฟล์ visit-target.csv | ☐ |
| 2 | VERIFY หัวคอลัมน์ในไฟล์ | — | มี เลขที่ · รอบการขาย · เขต · ผู้รับผิดชอบเขต · TO · CC · สถานะ · วันทำงาน · วันที่ · เริ่มต้นตลาด · สิ้นสุดตลาด · จำนวนลูกค้า · รายชื่อร้านค้า · ที่พัก (จังหวัด) | ☐ |

### กลุ่ม C — สร้างใบเป้าหมาย

#### TC-C01 — สร้างใบเป้าหมายครบแล้วส่งอนุมัติ (happy)
- group: สร้างใบเป้าหมาย · ความสำคัญ: สูง · trace: AC-01/03/05 / FN-01..04 / DEC-04 [AI-DEFAULT]
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/create`
- ชุดข้อมูล: A
- ผ่านเมื่อ: สถานะ "รออนุมัติ" · เลข SVT-2569-0009 · toast ส่งอนุมัติแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/visit-target` → CLICK **สร้างใบเป้าหมาย** | — | drawer **สร้างเอกสารใหม่** · ขั้น **ข้อมูลแผนเยี่ยม › เอกสารแนบ › ตรวจสอบและยืนยัน** | ☐ |
| 2 | VERIFY การ์ด **ส่วนหัวเอกสาร** | — | ช่อง **เขต** ค่า GT-NE01 · เขตตะวันออกเฉียงเหนือ 1 · **ผู้รับผิดชอบเขต** พนักงานขาย ทดสอบหนึ่ง · **TO** หัวหน้าเขต ทดสอบสอง | ☐ |
| 3 | SELECT ช่อง **รอบการขาย** | A: พฤศจิกายน 2569 | ช่องแสดง **พฤศจิกายน 2569** | ☐ |
| 4 | SELECT วันที่ + TYPE ตลาด + SELECT ร้าน 4 ร้าน (วันทำงานที่ 1) | A วันที่ 1 | การ์ดวันแสดง **จำนวนลูกค้า 4** · chip ร้าน 4 อัน | ☐ |
| 5 | CLICK **เพิ่มวันทำงาน** → กรอกวันที่ 2 ตามชุด A | A วันที่ 2 | การ์ดสรุป **วันทำงาน 2/31** · **จำนวนลูกค้ารวม 8** | ☐ |
| 6 | CLICK **ถัดไป** 2 ครั้ง → CLICK **บันทึกและส่งอนุมัติ** | — | modal **ส่งอนุมัติใบเป้าหมายการเยี่ยมร้านค้า?** · 2 ช่องผู้อนุมัติ ค่าเริ่ม **หัวหน้าเขต ทดสอบสอง** · **ผู้จัดการขาย ทดสอบสี่** · **ค่าเริ่มต้นจากสายอนุมัติ (DOA กลาง)** | ☐ |
| 7 | CLICK **ส่งอนุมัติ** → WAIT toast | — | toast **ส่งอนุมัติแล้ว · SVT-2569-0009** · แถวใหม่ pill **รออนุมัติ** ลายเซ็น **1/3** | ☐ |

#### TC-C02 — เลือกร้านจาก Customer ในเขต · กันร้านซ้ำ [AI-DEFAULT]
- group: สร้างใบเป้าหมาย · ความสำคัญ: สูง · trace: AC-02 / BR-07 / DEC-04 [AI-DEFAULT] / FN-01
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นเฉพาะร้านในเขต · ร้านที่เลือกแล้วไม่อยู่ในตัวเลือก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง **ค้นหาร้านค้าในเขตเพื่อเพิ่ม** | — | รายการร้านลงท้าย **NE01-xx** เท่านั้น (16 ร้าน) | ☐ |
| 2 | SELECT ร้าน | ร้านสะดวกซื้อสมมติ NE01-01 | chip **ร้านสะดวกซื้อสมมติ NE01-01** · **จำนวนลูกค้า 1** | ☐ |
| 3 | CLICK ช่องร้านค้าอีกครั้ง | — | ไม่มี **ร้านสะดวกซื้อสมมติ NE01-01** ในตัวเลือก (เลือกซ้ำไม่ได้) | ☐ |

#### TC-C03 — จำนวนลูกค้านับจากรายชื่อร้าน
- group: สร้างใบเป้าหมาย · ความสำคัญ: สูง · trace: AC-03 / BR-06 / DEC-14 / DEC-17
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: นับสดทุกครั้งที่เพิ่ม/ลบร้าน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ร้าน 3 ร้าน | ร้านในเขต 3 ร้าน | **จำนวนลูกค้า 3** · การ์ดสรุป **จำนวนลูกค้ารวม 3** | ☐ |
| 2 | CLICK ปุ่ม x บน chip ร้านแรก | — | **จำนวนลูกค้า 2** · **จำนวนลูกค้ารวม 2** | ☐ |

#### TC-C04 — บันทึกร่าง → แก้ไข → ส่ง (เลขเดิม)
- group: สร้างใบเป้าหมาย · ความสำคัญ: สูง · trace: BR-13 / DEC-10 / FN-03
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แก้ร่างได้ · ส่งแล้วเลขยังเป็น SVT-2569-0007

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/visit-target/view/R7` | — | drawer **SVT-2569-0007** pill **ร่าง** · ปุ่ม **ยกเลิก · แก้ไข · ส่งอนุมัติ** | ☐ |
| 2 | CLICK **แก้ไข** | — | drawer ดูปิด แล้ว wizard เปิด หัว **แก้ไขเอกสาร** **SVT-2569-0007** · 5 การ์ดวันทำงานค่าเดิมครบ | ☐ |
| 3 | CLICK **ถัดไป** 2 ครั้ง → **บันทึกและส่งอนุมัติ** → **ส่งอนุมัติ** | — | toast **ส่งอนุมัติแล้ว · SVT-2569-0007** (เลขเดิม) | ☐ |

#### TC-C05 — แนบไฟล์ประกอบ
- group: สร้างใบเป้าหมาย · ความสำคัญ: กลาง · trace: DEC-11 / API-12
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=เส้นทางตลาด.pdf
- Start: OPEN `#/visit-target/create`
- ชุดข้อมูล: files=เส้นทางตลาด.pdf
- ผ่านเมื่อ: ไฟล์ขึ้นในรายการ + ขั้นตรวจสอบนับ 1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK กรอกขั้น 1 ครบ → CLICK **ถัดไป** | A | หัว **แนบเอกสารประกอบ (ถ้ามี)** | ☐ |
| 2 | UPLOAD → กล่อง **คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)** | เส้นทางตลาด.pdf | แถวไฟล์ **เส้นทางตลาด.pdf** + ขนาด | ☐ |
| 3 | CLICK **ถัดไป** | — | การ์ด **เอกสารแนบ** นับ **1** | ☐ |

#### TC-C06 — เขต+รอบที่มีใบใช้งานแล้ว แจ้งว่าจะถูกแทนที่
- group: สร้างใบเป้าหมาย · ความสำคัญ: กลาง · trace: EC-03 / BR-11 / DEC-04 [AI-DEFAULT]
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: การ์ดสรุปเตือนเลขใบเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ช่อง **รอบการขาย** | ตุลาคม 2569 | การ์ดสรุปแสดง **เขตและรอบนี้มีใบใช้งาน SVT-2569-0004 — อนุมัติใบนี้แล้วใบเดิมจะถูกแทนที่** | ☐ |

#### TC-C07 — ร้านเกิน 7 ร้านต่อวัน = เตือนแต่ส่งได้
- group: สร้างใบเป้าหมาย · ความสำคัญ: กลาง · trace: AC-13 / BR-07 / DEC-15 / W-01
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แถบเตือน · ไม่บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ร้าน 8 ร้านในวันทำงานที่ 1 | ร้านในเขต 8 ร้าน | แถบเตือน **เกิน 7 ร้าน — แบบพิมพ์มี 7 ช่อง ชื่อที่เกินจะต่อในช่องสุดท้าย (ไม่บล็อกการส่ง)** | ☐ |
| 2 | CLICK กรอกวันที่ + ตลาด → CLICK **ถัดไป** | A | ไปขั้น **เอกสารแนบ** ได้ (ไม่บล็อก) | ☐ |

### กลุ่ม V — กรอกไม่ครบ / ผิด

#### TC-V01 — กดถัดไปโดยไม่เลือกรอบการขาย / ไม่มีแผน = บล็อก
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: สูง · trace: VR-02 / VR-04 (auto: e2e S7)
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก + toast + ช่องแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างใบเป้าหมาย** → CLICK **ถัดไป** | — | toast **กรุณากรอกข้อมูลให้ครบถ้วน** · ช่อง **รอบการขาย** แดง **กรุณาเลือกรอบการขาย** · ข้อความ **ต้องมีแผนเยี่ยมอย่างน้อย 1 วัน** | ☐ |

#### TC-V02 — วันที่มีแผนแต่ไม่กรอกตลาด/ร้าน = บล็อก
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: สูง · trace: VR-07 / VR-08 / BR-05 [AI-DEFAULT]
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: การ์ดวันขอบแดง + ข้อความ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT รอบ → SELECT วันที่ในวันทำงานที่ 1 · เว้นตลาดและร้าน → CLICK **ถัดไป** | พฤศจิกายน 2569 · 2 พ.ย. 2569 | การ์ด **วันทำงานที่ 1** ขอบแดง **กรุณากรอกวันที่ · เริ่มต้นตลาด · สิ้นสุดตลาด และร้านค้าอย่างน้อย 1 ร้าน** | ☐ |

#### TC-V03 — วันที่ซ้ำกัน 2 วัน = บล็อกทั้งสองการ์ด
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: สูง · trace: VR-06 / BR-04 / DEC-16 / EC-10
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/create`
- ชุดข้อมูล: A
- ผ่านเมื่อ: ทั้งสองการ์ดแดง "วันที่ซ้ำกับวันทำงานอื่น"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK กรอกวันทำงานที่ 1 และ 2 ด้วยวันที่เดียวกัน (ตลาด/ร้านครบ) → CLICK **ถัดไป** | 2 พ.ย. 2569 ทั้งสองวัน | การ์ดวันที่ 1 และ 2 แสดง **วันที่ซ้ำกับวันทำงานอื่น** | ☐ |

#### TC-V04 — ปฏิทินเลือกได้เฉพาะวันในรอบการขาย
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: สูง · trace: VR-05 / BR-04 / DEC-16
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: วันนอกรอบกดไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT รอบ → CLICK ช่อง **วันที่** (วันทำงานที่ 1) | พฤศจิกายน 2569 | ปฏิทินเปิดที่ **พฤศจิกายน 2569** · วันของเดือนอื่นกดไม่ได้ | ☐ |

#### TC-V05 — ครบ 31 วันแล้วเพิ่มไม่ได้
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: กลาง · trace: BR-03 / DEC-05 / EC-07
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปุ่มเพิ่มวันทำงาน disabled ที่ 31

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มวันทำงาน** 30 ครั้ง | — | มี 31 การ์ด · ปุ่ม **เพิ่มวันทำงาน** กดไม่ได้ | ☐ |

#### TC-V06 — เปลี่ยนเขตแล้วร้านนอกเขตถูกนำออก
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: กลาง · trace: EC-01 / BR-07
- actor (role): ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2
- Setup: role=ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2 (__QA__.setMe('E04')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: toast จำนวนร้านที่ถูกนำออก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ร้าน 2 ร้านในเขต GT-NE01 | — | chip 2 อัน | ☐ |
| 2 | SELECT ช่อง **เขต** | GT-C01 · เขตภาคกลาง 1 | toast **นำร้านนอกเขตออก 2 ร้าน** · chip หายหมด | ☐ |

#### TC-V07 — แนบไฟล์ผิดชนิด = ปฏิเสธ
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: กลาง · trace: file policy (Document Center)
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=script.exe
- Start: OPEN `#/visit-target/create`
- ชุดข้อมูล: files=script.exe
- ผ่านเมื่อ: toast ชนิดไฟล์ไม่รองรับ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไปขั้น **เอกสารแนบ** → UPLOAD | script.exe | toast **script.exe — ชนิดไฟล์ไม่รองรับ** · ไม่มีแถวไฟล์ | ☐ |

### กลุ่ม S — ส่งอนุมัติ

#### TC-S01 — modal ส่งอนุมัติ 2 ขั้น · ผู้นำเสนอไม่อยู่ในรายชื่อ
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: AC-05 / BR-08 / BR-09 / DEC-03 [AI-DEFAULT]
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: 2 slot ค่าเริ่มจาก DOA · ไม่มีชื่อผู้นำเสนอให้เลือก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** | — | modal **ส่งอนุมัติใบเป้าหมายการเยี่ยมร้านค้า?** · 2 แถว **ผู้อนุมัติ (ขั้นที่ 1)** · **ผู้อนุมัติ (ขั้นที่ 2)** | ☐ |
| 2 | CLICK ช่องผู้อนุมัติขั้นที่ 1 | — | ไม่มี **พนักงานขาย ทดสอบหนึ่ง** ในรายชื่อ | ☐ |

#### TC-S02 — DOA เพิ่มขั้น → slot และช่องลงนามเพิ่มตาม
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: AC-14 / BR-12 / EC-05 (auto: e2e S8)
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/view/R7` (หลัง __QA__.doa.push())
- ชุดข้อมูล: —
- ผ่านเมื่อ: slot 3 แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console `__QA__.doa.push('ผู้อนุมัติ')` → CLICK **ส่งอนุมัติ** | — | modal มี 3 แถวผู้อนุมัติ (ขั้นที่ 1–3) | ☐ |

#### TC-S03 — ส่งไม่สำเร็จ (API ล้ม) แจ้งเตือนและไม่เปลี่ยนสถานะ
- group: ส่งอนุมัติ · ความสำคัญ: กลาง · trace: 06 §6.10 (auto: e2e S9)
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: toast error · ยังเป็นร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console `__QA__.sim('error')` → CLICK **ส่งอนุมัติ** → **ส่งอนุมัติ** | — | toast **ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง** · pill ยัง **ร่าง** | ☐ |

### กลุ่ม A — อนุมัติ / ไม่อนุมัติ

#### TC-A01 — อนุมัติขั้น 1 แล้วไปขั้น 2 · ขั้น 2 อนุมัติ = อนุมัติแล้ว
- group: อนุมัติ / ไม่อนุมัติ · ความสำคัญ: สูง · trace: AC-06 / FN-05 / DEC-03
- actor (role): ผู้อนุมัติขั้น 1 ผู้บังคับบัญชาของ E01
- Setup: role=ผู้อนุมัติขั้น 1 ผู้บังคับบัญชาของ E01 (__QA__.setMe('E02')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ขั้น 1 → รออนุมัติขั้น 2 · ขั้น 2 → อนุมัติแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **อนุมัติ** → CLICK **อนุมัติ** (ใน modal) | — | toast **อนุมัติแล้ว · SVT-2569-0008** · pill ยัง **รออนุมัติ** · ลายเซ็น **2/3** | ☐ |
| 2 | PRESS `__QA__.setMe('E04')` → OPEN `#/visit-target/view/R8` → CLICK **อนุมัติ** → **อนุมัติ** | — | modal มีข้อความ **อนุมัติขั้นสุดท้าย — ระบบแจ้ง TO/CC อัตโนมัติ** · pill **อนุมัติแล้ว** · ลายเซ็น **3/3** | ☐ |

#### TC-A02 — ไม่อนุมัติต้องมีเหตุผล → กลับเป็นร่างเลขเดิม [AI-DEFAULT]
- group: อนุมัติ / ไม่อนุมัติ · ความสำคัญ: สูง · trace: AC-07 / BR-10 / DEC-08 [AI-DEFAULT] / VR-10
- actor (role): ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2
- Setup: role=ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2 (__QA__.setMe('E04')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/view/R5`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อกเมื่อไม่มีเหตุผล · มีแล้วกลับเป็นร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ไม่อนุมัติ** → CLICK **ไม่อนุมัติ** (ใน modal) โดยไม่กรอก | — | ช่อง **เหตุผล** แดง **กรุณาระบุเหตุผล** | ☐ |
| 2 | CLICK chip **จำนวนร้านต่อวันน้อยเกินไป** → CLICK **ไม่อนุมัติ** | — | toast **ไม่อนุมัติ — ส่งกลับเป็นร่างแล้ว · SVT-2569-0005** · pill **ร่าง** เลขเดิม | ☐ |

#### TC-A03 — อนุมัติใบใหม่ของเขต+รอบเดิม → ใบเดิมถูกแทนที่
- group: อนุมัติ / ไม่อนุมัติ · ความสำคัญ: สูง · trace: AC-12 / BR-11 / FN-09 / DEC-04 [AI-DEFAULT]
- actor (role): ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2
- Setup: role=ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2 (__QA__.setMe('E04')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ใบเดิม "ถูกแทนที่"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ให้ E01 สร้างใบ GT-NE01 รอบ ตุลาคม 2569 แล้วส่ง → E02 อนุมัติขั้น 1 → E04 อนุมัติขั้น 2 | ชุด A (รอบ ตุลาคม 2569) | ใบใหม่ pill **อนุมัติแล้ว** | ☐ |
| 2 | OPEN `#/visit-target/view/R4` | — | pill **ถูกแทนที่** · แถบ **ใบนี้ถูกแทนที่ด้วย** + เลขใบใหม่ | ☐ |

### กลุ่ม X — ยกเลิก

#### TC-X01 — ยกเลิกร่างต้องมีเหตุผล
- group: ยกเลิก · ความสำคัญ: สูง · trace: AC-11 / BR-15 / DEC-08 / VR-10
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อกถ้าไม่มีเหตุผล · มีแล้วยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยกเลิก** → CLICK **ยกเลิกเอกสาร** (ใน modal) โดยไม่กรอก | — | **กรุณาระบุเหตุผล** | ☐ |
| 2 | CLICK chip **บันทึกซ้ำ** → CLICK **ยกเลิกเอกสาร** | — | toast **ยกเลิกเอกสารแล้ว · SVT-2569-0007** · pill **ยกเลิก** | ☐ |

#### TC-X02 — ผู้จัดการฝ่ายขายยกเลิกใบที่รออนุมัติ (แจ้งผู้อนุมัติ)
- group: ยกเลิก · ความสำคัญ: กลาง · trace: AC-11 / BR-15 / NTF svt_cancelled
- actor (role): ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2
- Setup: role=ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2 (__QA__.setMe('E04')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ยกเลิก + svt_cancelled

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ⋮ ที่แถว **SVT-2569-0008** → **ยกเลิกเอกสาร** | — | modal **ยกเลิกเอกสาร?** ข้อความ **รออนุมัติอยู่ — ผู้อนุมัติจะได้รับแจ้ง** | ☐ |
| 2 | TYPE เหตุผล → CLICK **ยกเลิกเอกสาร** | เปลี่ยนผู้รับผิดชอบเขต | pill **ยกเลิก** · ประวัติ **ยกเลิกเอกสาร** | ☐ |

### กลุ่ม P — ใครเห็นอะไร

#### TC-P01 — ผู้อนุมัติไม่เห็นร่างของคนอื่น
- group: ใครเห็นอะไร · ความสำคัญ: สูง · trace: TC-D01 / BR-12 / DEC-09 (auto: e2e S3)
- actor (role): ผู้อนุมัติขั้น 1 ผู้บังคับบัญชาของ E01
- Setup: role=ผู้อนุมัติขั้น 1 ผู้บังคับบัญชาของ E01 (__QA__.setMe('E02')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 7 ใบ ไม่มี SVT-2569-0007 (ร่าง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/visit-target` | — | ตาราง 7 แถว · ไม่พบ **SVT-2569-0007** | ☐ |
| 2 | OPEN `#/visit-target/view/R7` | — | ไม่เปิด drawer (ไม่มีสิทธิ์) | ☐ |

#### TC-P02 — CC เห็นเฉพาะใบที่อนุมัติแล้ว
- group: ใครเห็นอะไร · ความสำคัญ: สูง · trace: TC-D03 / EC-06 / DEC-09 [AI-DEFAULT]
- actor (role): ผู้รับสำเนา CC
- Setup: role=ผู้รับสำเนา CC (__QA__.setMe('E05')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 4 ใบ (approved/superseded)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/visit-target` | — | ตาราง 4 แถว **SVT-2569-0001..0004** | ☐ |
| 2 | OPEN `#/visit-target/view/R5` | — | ไม่เปิด drawer (ไม่มีสิทธิ์) | ☐ |

#### TC-P03 — ผู้นำเสนอแก้ใบที่ส่งแล้วไม่ได้ / อนุมัติใบตัวเองไม่ได้
- group: ใครเห็นอะไร · ความสำคัญ: สูง · trace: TC-D04 / TC-D05 / BR-09
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/view/R4`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มแก้ไข/อนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/visit-target/view/R4` | — | หัว drawer ไม่มีปุ่ม **แก้ไข** · **อนุมัติ** · ท้าย drawer **ส่งแล้ว ล็อกแก้ไข** | ☐ |

#### TC-P04 — ผู้อนุมัติขั้น 2 ยังอนุมัติไม่ได้ขณะขั้น 1 ค้าง
- group: ใครเห็นอะไร · ความสำคัญ: กลาง · trace: TC-D06
- actor (role): ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2
- Setup: role=ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2 (__QA__.setMe('E04')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มอนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/visit-target/view/R8` | — | แถบ **รอ หัวหน้าเขต ทดสอบสอง อนุมัติ** · ไม่มีปุ่ม **อนุมัติ** (มีแค่ **ยกเลิกเอกสาร**) | ☐ |

### กลุ่ม D — แบบพิมพ์ PDF

#### TC-D01 — PDF Preview ร่าง ตรงแบบฟอร์ม FM-SAL-09
- group: แบบพิมพ์ PDF · ความสำคัญ: สูง · trace: AC-10 / DEC-06 / FN-08
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ถ้อยคำตามกระดาษ · 31 แถว · footer ร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | แถบ **ตัวอย่าง PDF · A4 · แบบพิมพ์ FM-SAL-09** · ในกระดาษ: **ใบเป้าหมายการเยี่ยมร้านค้า : เขตการขาย General Trade** · TO : · CC : · ผู้รับผิดชอบเขต : · ตำแหน่ง : · เขต : · รอบการขาย : | ☐ |
| 2 | VERIFY ตาราง | — | หัว **วันทำงาน · วันที่ · เริ่มต้นตลาด · สิ้นสุดตลาด · จำนวนลูกค้า · รายชื่อร้านค้า · ที่พัก (จังหวัด)** · แถว 1–31 · แถวรวม **5 วัน** **26** | ☐ |
| 3 | VERIFY ท้ายกระดาษ | — | ช่องลงนาม 3 ช่อง **ผู้นำเสนอ · ผู้อนุมัติ · ผู้อนุมัติ** · footer **เลขที่ SVT-2569-0007 · ร่าง** | ☐ |

#### TC-D02 — PDF ใบอนุมัติแล้ว: ลงนามด้วยข้อความ ไม่ใช้ภาพ
- group: แบบพิมพ์ PDF · ความสำคัญ: สูง · trace: BR-14 / DEC-07
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/view/R4`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ☑ อนุมัติ + พิจารณาในระบบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | ช่องผู้นำเสนอ **ส่งในระบบ** + วันเวลา · ช่องผู้อนุมัติ 2 ช่อง **☑ อนุมัติ** + **พิจารณาในระบบ** · ไม่มีภาพลายมือ | ☐ |

#### TC-D03 — แบบพิมพ์ 31 วัน + ร้านเกิน 7 / DOA 6 ขั้น
- group: แบบพิมพ์ PDF · ความสำคัญ: กลาง · trace: EC-04 / EC-05 / DEC-15
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: เปิด print/out/long-31rows.html และ approved-doa6steps.html
- ชุดข้อมูล: —
- ผ่านเมื่อ: 31 แถว · ช่องที่ 7 ต่อชื่อ · ลงนาม 4+3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN print/out/long-31rows.html | — | แถวที่มี 12 ร้าน: ช่องร้านที่ 7 มีชื่อร้านที่ 7–12 คั่นด้วยจุลภาค | ☐ |
| 2 | OPEN print/out/approved-doa6steps.html | — | ช่องลงนาม 7 ช่อง 2 แถว (4+3) | ☐ |

### กลุ่ม E — การใช้งานทั่วไป

#### TC-E01 — ปิด wizard ที่กรอกค้าง ต้องยืนยัน
- group: การใช้งานทั่วไป · ความสำคัญ: กลาง · trace: U8 / 01 §1.6
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal ทิ้งข้อมูล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT รอบ → CLICK ปุ่ม x | — | modal **ทิ้งข้อมูลที่กรอกไว้?** · ปุ่ม **กลับไปกรอกต่อ** · **ทิ้งข้อมูล** | ☐ |

#### TC-E02 — Esc ปิดตามลำดับ (ปฏิทิน → modal → drawer)
- group: การใช้งานทั่วไป · ความสำคัญ: กลาง · trace: U8 Esc chain (auto: e2e S10)
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปิดทีละชั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** → PRESS Esc | — | modal ปิด drawer ยังอยู่ | ☐ |
| 2 | PRESS Esc | — | drawer ปิด | ☐ |

#### TC-E03 — แบบเอกสารถูกปิดที่ F-DOCCFG = สร้างไม่ได้
- group: การใช้งานทั่วไป · ความสำคัญ: กลาง · trace: EC-09 / BR-13
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปุ่มสร้าง disabled + แถบแจ้ง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console `__QA__.setDocActive(false)` | — | แถบ **แบบเอกสารนี้ยังไม่เปิดใช้งาน — สร้างใบเป้าหมายใหม่ไม่ได้** · ปุ่ม **สร้างใบเป้าหมาย** กดไม่ได้ | ☐ |

### กลุ่ม H — ประวัติ

#### TC-H01 — ประวัติ append-only ครบทุกการกระทำ
- group: ประวัติ · ความสำคัญ: กลาง · trace: BR-11 / ประวัติ
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นสร้าง → ส่ง → อนุมัติ 2 ขั้น → ถูกแทนที่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **ประวัติ** | — | รายการ **ถูกแทนที่** (แทนที่ด้วย SVT-2569-0004) · **อนุมัติ (ขั้น 2)** · **อนุมัติ (ขั้น 1)** · **ส่งอนุมัติ** · **สร้างเอกสาร** | ☐ |

### กลุ่ม XT — เชื่อมระบบอื่น

#### TC-XT01 — อนุมัติขั้นสุดท้ายแจ้ง TO/CC (svt_plan_published)
- group: เชื่อมระบบอื่น · ความสำคัญ: กลาง · trace: NTF svt_plan_published / FN-09 (ต้อง simulate)
- actor (role): ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2
- Setup: role=ผู้จัดการฝ่ายขาย role-mgr-sales · ขั้น 2 (__QA__.setMe('E04')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/view/R5`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ประวัติมี "แจ้ง TO/CC"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **อนุมัติ** → **อนุมัติ** | — | แท็บ **ประวัติ** มี **แจ้ง TO/CC** + ชื่อผู้รับ | ☐ |

#### TC-XT02 — เลข SVT ออกตอนบันทึกครั้งแรก (ENG-DOC-NUM)
- group: เชื่อมระบบอื่น · ความสำคัญ: ต่ำ · trace: DEC-10 / FN-03
- actor (role): ผู้นำเสนอ เจ้าของเขต GT-NE01
- Setup: role=ผู้นำเสนอ เจ้าของเขต GT-NE01 (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/visit-target/create`
- ชุดข้อมูล: A
- ผ่านเมื่อ: ร่างใหม่ได้เลข SVT-2569-0009

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK กรอกครบ → **บันทึกแบบร่าง** | — | toast **บันทึกร่างแล้ว · SVT-2569-0009** | ☐ |

## วิธีที่ agent รัน (Run protocol)
1. เปิด feature.html → ไปที่ `#/visit-target`
2. ตั้ง role ตาม Setup ด้วย `__QA__.setMe('E01'|'E02'|'E04'|'E05')` (ตัวสลับผู้ใช้มุมขวาบนก็ได้)
3. seed พิเศษ: `__QA__.sim('error')` · `__QA__.setDocActive(false)` · `__QA__.doa.push(label)` — รีโหลดหน้าเพื่อล้าง
4. ทำ step ตามลำดับ · บันทึกผลตาม schema · เคส (auto: e2e …) ใช้ผล e2e_standard.py ได้

## Coverage Audit
| หมวด | covered / total |
|---|---|
| AC (06_TESTS) | 14 / 14 |
| Business rules (05_RULES) | 15 / 15 |
| Validation | 10 / 10 |
| Edge cases | 9 / 10 |
| Permission cells | 7 / 7 |
| Cross-cutting / events / states | ครบ |

- Cross-Module (XT): 4/4
- Scope Lock (DEC): 18/18
- **Manifest cross-check (FRD §0.12): ✅ 8/8**

### ข้าม (พร้อมเหตุผล)
- EC-02 resolve ผู้บังคับบัญชาไม่ได้ — seed ต้นแบบทุกคนมีผู้บังคับบัญชา → ทดสอบตอน UAT ระบบจริง

## Result Report (schema)
```json
{
 "feature_id": "F-TMP-005",
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
  "total": 41,
  "pass": 0,
  "fail": 0,
  "blocked": 0
 }
}
```

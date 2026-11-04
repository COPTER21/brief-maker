# AI Test Cases — F-TMP-004 ใบกำหนดหน้าที่งานประจำตำแหน่ง (Job Description)

ชุดเคสสำหรับ AI agent (browser-use/vision) ทดสอบบน prototype `feature.html` · anchor = ข้อความบนจอจริง (HTML > 01_UI) · เคสที่ derive จากมติ AI-DEFAULT ติดป้าย [AI-DEFAULT] — fail อาจแปลว่า "ค่าเริ่มผิด" ไม่ใช่โค้ดผิด

## Meta
| รายการ | ค่า |
|---|---|
| Feature ID | F-TMP-004 |
| ชื่อ | ใบกำหนดหน้าที่งานประจำตำแหน่ง (Job Description) |
| เวอร์ชัน | 1.0 |
| App entry | feature.html |
| Routes | `#/job-description` · `#/job-description/create` · `#/job-description/edit/:id` · `#/job-description/view/:id` |
| ที่มา | FRD_F-TMP-004_Pack · BRD_F-TMP-004 · feature.html · DECISIONS.lock |
| จำนวนเคส | 54 |
| หมวด | L ดูรายการ · C สร้างใบกำหนดหน้าที่งาน · V กรอกไม่ครบ / ผิด · S ส่งอนุมัติ · A อนุมัติ / ไม่อนุมัติ · K ผู้ดำรงตำแหน่งรับทราบ · X ยกเลิก · P ใครเห็นอะไร · D แบบพิมพ์ PDF · E การใช้งานทั่วไป · H ประวัติ · XT เชื่อมระบบอื่น |

## Coverage
| group | เคส | สูง/กลาง/ต่ำ |
|---|---|---|
| L ดูรายการ | 7 | 2/4/1 |
| C สร้างใบกำหนดหน้าที่งาน | 6 | 4/2/0 |
| V กรอกไม่ครบ / ผิด | 9 | 5/3/1 |
| S ส่งอนุมัติ | 3 | 2/1/0 |
| A อนุมัติ / ไม่อนุมัติ | 4 | 3/1/0 |
| K ผู้ดำรงตำแหน่งรับทราบ | 3 | 2/1/0 |
| X ยกเลิก | 3 | 2/1/0 |
| P ใครเห็นอะไร | 6 | 4/2/0 |
| D แบบพิมพ์ PDF | 5 | 2/3/0 |
| E การใช้งานทั่วไป | 4 | 0/3/1 |
| H ประวัติ | 2 | 0/2/0 |
| XT เชื่อมระบบอื่น | 2 | 0/2/0 |

## Coverage Ledger
### FR / AC (06_TESTS)
| item | cases |
|---|---|
| AC-01 | TC-C01, TC-C02 |
| AC-02 | TC-V02 |
| AC-03 | TC-D03 |
| AC-04 | TC-C01, TC-C03 |
| AC-05 | TC-C01, TC-S01 |
| AC-06 | TC-A01 |
| AC-07 | TC-A02 |
| AC-08 | TC-K01 |
| AC-09 | TC-K02 |
| AC-10 | TC-L02, TC-L07 |
| AC-11 | TC-D01 |
| AC-12 | TC-X01, TC-X02 |
| AC-13 | TC-A03 |
| AC-14 | TC-V07 |
| AC-15 | TC-S02 |
### Business Rules (05_RULES)
| rule | cases |
|---|---|
| BR-01 | TC-C02 |
| BR-02 | TC-V02, TC-V03 |
| BR-03 | TC-V04, TC-V07 |
| BR-04 | TC-V05 |
| BR-05 | TC-C03 |
| BR-06 | TC-D03 |
| BR-07 | TC-S01, TC-S02 |
| BR-08 | TC-A02 |
| BR-09 | TC-S01, TC-P05 |
| BR-10 | TC-A03, TC-C06 |
| BR-11 | TC-K01, TC-K02, TC-K03 |
| BR-12 | TC-L01, TC-L02, TC-P01, TC-P02, TC-P03 |
| BR-13 | TC-C04, TC-E04 |
| BR-14 | TC-D02 |
| BR-15 | TC-X01, TC-X02, TC-X03, TC-L07, TC-C05 |
| BR-16 | TC-D01, TC-P04 |
### Validation (VR)
| VR | cases |
|---|---|
| VR-01 | TC-V01 |
| VR-02 | TC-V03 |
| VR-03 | TC-C02 |
| VR-04 | TC-V02 |
| VR-05 | TC-V04 |
| VR-06 | TC-V05 |
| VR-07 | TC-V05 |
| VR-08 | TC-S01 |
| VR-09 | TC-A02, TC-X01 |
### Edge Cases
| EC | cases / สถานะ |
|---|---|
| EC-01 | — ข้าม (seed ต้นแบบ: กรรมการผู้จัดการไม่มีหัวหน้า — ทดสอบตอน UAT) |
| EC-02 | — ข้าม (seed ทุกคนมีผู้บังคับบัญชา — UAT ระบบจริง) |
| EC-03 | TC-C06, TC-A03 |
| EC-04 | TC-D03 |
| EC-05 | TC-S02 (+ แบบพิมพ์ doa6steps) |
| EC-06 | TC-P02 |
| EC-07 | TC-K01 |
| EC-08 | TC-A02, TC-X01 |
| EC-09 | TC-E04 |
| EC-10 | TC-V05 |
### Permission Matrix (role × action)
| cell | cases |
|---|---|
| owner ดู/สร้าง/แก้ร่าง/ส่ง/ยกเลิก = allow | TC-L01, TC-C01, TC-C04, TC-X01 |
| owner อนุมัติใบตัวเอง = deny (BR-DOA-04) | TC-S01, TC-P05 |
| owner แก้ใบส่งแล้ว = deny | TC-P04 |
| ผู้อนุมัติ อนุมัติ/ไม่อนุมัติ ขั้นปัจจุบัน = allow | TC-A01, TC-A02 |
| ผู้อนุมัติ ดูร่างคนอื่น = deny | TC-P01 |
| ผู้ดำรงตำแหน่ง รับทราบ = allow · ดูใบรออนุมัติ = deny | TC-K01, TC-P02 |
| role-mgr-hr ดูทุกใบ/ยกเลิก/ระบุผู้ดำรงตำแหน่ง/CSV = allow | TC-L02, TC-X02, TC-K02, TC-L07 |
| ผู้ใช้อื่น ดูใบหน่วยงานอื่น = deny | TC-P03 |
### Cross-Module (XT — 06 §6.9)
| XT | Downstream | Case |
|---|---|---|
| ENG-NOTIFY jd_ack_requested | ผู้ดำรงตำแหน่ง | TC-XT01 |
| ENG-NOTIFY jd_cancelled | ผู้อนุมัติขั้นปัจจุบัน | TC-X02 |
| F-DOCCFG / ENG-DOC-NUM | เลข JD | TC-XT02 |
| Position & Tier prefill | ข้อมูลตำแหน่ง | TC-C02 |
### Scope Lock (DEC — 07 §7.0)
| DEC | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| DEC-01 | ไม่แก้ Position master | TC-C02 |
| DEC-02 | ไม่ส่งต่อ | TC-XT01 |
| DEC-03 | DOA 1 ขั้น role-line-manager [AI-DEFAULT] | TC-S01, TC-S02 |
| DEC-04 | ดึง master/ฉบับใหม่แทนเดิม/รับทราบ [AI-DEFAULT] | TC-C02, TC-A03, TC-K02 |
| DEC-05 | หัวหน้าไม่จำกัด | TC-V04 |
| DEC-06 | ลูกน้องไม่จำกัด | TC-D03 |
| DEC-07 | ช่อง 1:1 | TC-D01 |
| DEC-08 | ลงนามไม่ใช้ภาพ | TC-D02 |
| DEC-09 | ไม่อนุมัติ = กลับร่าง [AI-DEFAULT] | TC-A02, TC-X01 |
| DEC-10 | การมองเห็น | TC-L02, TC-P01, TC-P02 |
| DEC-11 | เลขตอนบันทึกครั้งแรก | TC-C04 |
| DEC-12 | แนบ ✓ CSV ✓ | TC-C05, TC-L07 |
| DEC-13 | ผู้ใต้บังคับบัญชาคำนวณ | TC-C03 |
| DEC-14 | หัวหน้า ≥1 · เตือนไม่ตรง | TC-V04, TC-V07 |
| DEC-15 | จำนวนคนจำนวนเต็ม ≥1 | TC-V05 |
| DEC-16 | รับทราบหลังอนุมัติ | TC-K01, TC-K03 |
| DEC-17 | ถ้อยคำตรงตัว | TC-D01, TC-V03 |
### Cross-cutting / Events / States
| item | cases |
|---|---|
| empty state | TC-L06 |
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
| ชื่อตำแหน่ง (ไทย) | เจ้าหน้าที่บัญชีลูกหนี้ |
| ชื่อตำแหน่งอังกฤษ | Accounts Receivable Officer |
| วัตถุประสงค์ | ดูแลการวางบิลและติดตามรับชำระ |
| ขอบเขตความรับผิดชอบหลัก | 1. ออกใบวางบิล · 2. ติดตามรับชำระ |
| คุณสมบัติประจำตำแหน่ง | ปริญญาตรี สาขาการบัญชี |
| KPI | 1. ลูกหนี้เกินกำหนด ≤ 5% |
| ลูกน้อง | ผู้ช่วยเจ้าหน้าที่บัญชี · 2 คน |
### ไฟล์ทดสอบ (Files)
| ไฟล์ | ใช้ |
|---|---|
| ผังโครงสร้าง.pdf | TC-C05 |
| script.exe | TC-V08 |
| big-25MB.pdf | TC-V09 |

## Test Cases

### กลุ่ม L — ดูรายการ

#### TC-L01 — ผู้จัดทำเห็นเฉพาะใบที่ตัวเองจัดทำ
- group: ดูรายการ · ความสำคัญ: สูง · trace: BR-12 / DEC-10 (auto: e2e S2)
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 4 ใบ (JD-2569-0001, 0002, 0005, 0006) + คอลัมน์ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/job-description` | — | หัวข้อ **ใบกำหนดหน้าที่งานประจำตำแหน่ง** + (Job Description) · ปุ่ม **ส่งออก CSV** · **สร้างใบกำหนดหน้าที่งาน** | ☐ |
| 2 | VERIFY หัวตาราง | — | คอลัมน์ **เลขที่ · วันที่สร้าง · ตำแหน่ง · แผนก · ฝ่าย · ผู้จัดทำ · สถานะเอกสาร · ลายเซ็น** | ☐ |
| 3 | VERIFY แถวในตาราง | — | 4 แถว **JD-2569-0006** ร่าง · **0005** รออนุมัติ · **0002** อนุมัติแล้ว · **0001** รับทราบแล้ว | ☐ |

#### TC-L02 — ฝ่ายบุคคลเห็นทุกใบ + ตัวเลขใต้หัวข้อ
- group: ดูรายการ · ความสำคัญ: สูง · trace: AC-10 / DEC-10 / U1 (auto: e2e S2)
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 9 ใบ · badge "9 รายการ" "รออนุมัติ 2" · ไม่มีการ์ดตัวเลข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/job-description` | — | ตารางมี 9 แถว (JD-2569-0001..0009) | ☐ |
| 2 | VERIFY บรรทัดคำอธิบายใต้หัวข้อ | — | ข้อความ **หน้าที่ ความรับผิดชอบ คุณสมบัติ และ KPI ของแต่ละตำแหน่ง** + badge **9 รายการ** **รออนุมัติ 2** · ไม่มีแถวการ์ดตัวเลข | ☐ |

#### TC-L03 — ค้นหาด้วยชื่อตำแหน่ง
- group: ดูรายการ · ความสำคัญ: กลาง · trace: P-01 search
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description`
- ชุดข้อมูล: ค้นหา: คลังสินค้า
- ผ่านเมื่อ: เหลือแถวตำแหน่งคลังสินค้า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่อง **ค้นหาเลขที่ / ตำแหน่ง / แผนก / ผู้จัดทำ** | พนักงานคลังสินค้า | ตารางเหลือ 1 แถว **JD-2569-0003** | ☐ |
| 2 | CLICK ปุ่ม **รีเซ็ต** | — | ช่องค้นหาว่าง · กลับมา 9 แถว | ☐ |

#### TC-L04 — กรองสถานะ / ฝ่าย
- group: ดูรายการ · ความสำคัญ: กลาง · trace: P-01 filter
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ผลกรองตรงเงื่อนไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ตัวกรอง **ทุกสถานะ** → **ถูกแทนที่** | — | เหลือ 1 แถว **JD-2569-0008** pill **ถูกแทนที่** | ☐ |
| 2 | CLICK **รีเซ็ต** แล้ว SELECT **ทุกฝ่าย** → **ฝ่ายทรัพยากรบุคคล** | — | เหลือ 1 แถว **JD-2569-0004** | ☐ |

#### TC-L05 — แบ่งหน้า + แสดงต่อหน้า
- group: ดูรายการ · ความสำคัญ: ต่ำ · trace: U6
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description`
- ชุดข้อมูล: —
- ผ่านเมื่อ: footer มีแสดงต่อหน้า 25 + "1 – 9 จาก 9 รายการ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY footer ตาราง | — | **แสดงต่อหน้า** ค่า 25 · ข้อความ **1 – 9 จาก 9 รายการ** · ปุ่มหน้า 1 | ☐ |

#### TC-L06 — ค้นหาไม่พบ = empty state
- group: ดูรายการ · ความสำคัญ: กลาง · trace: U23 / 01 §1.6
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description`
- ชุดข้อมูล: ค้นหา: ไม่มีตำแหน่งนี้
- ผ่านเมื่อ: แสดง "ไม่พบรายการที่ค้นหา" + ปุ่มล้างตัวกรอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา | ไม่มีตำแหน่งนี้ | ตารางว่าง แสดง **ไม่พบรายการที่ค้นหา** · **ลองปรับคำค้นหรือล้างตัวกรอง** | ☐ |
| 2 | CLICK ปุ่ม **ล้างตัวกรอง** | — | กลับมา 9 แถว | ☐ |

#### TC-L07 — ส่งออก CSV ตามสิทธิ์
- group: ดูรายการ · ความสำคัญ: กลาง · trace: AC-10 / DEC-12 / API-11
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ดาวน์โหลด job-description.csv + toast ส่งออก 9 รายการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งออก CSV** | — | toast **ส่งออก 9 รายการ** · ไฟล์ job-description.csv | ☐ |
| 2 | VERIFY หัวคอลัมน์ในไฟล์ | — | มี เลขที่ · ชื่อตำแหน่ง (ไทย) · ชื่อตำแหน่งอังกฤษ · รายงานต่อ · ผู้ใต้บังคับบัญชา · ผู้ดำรงตำแหน่ง · สถานะ | ☐ |

### กลุ่ม C — สร้างใบกำหนดหน้าที่งาน

#### TC-C01 — สร้างใบกำหนดหน้าที่งานครบทุกหัวข้อแล้วส่งอนุมัติ (happy)
- group: สร้างใบกำหนดหน้าที่งาน · ความสำคัญ: สูง · trace: AC-01/04/05 / FN-01..04 / DEC-04 [AI-DEFAULT]
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/create`
- ชุดข้อมูล: A
- ผ่านเมื่อ: สถานะ "รออนุมัติ" · เลข JD-2569-0010 · toast ส่งอนุมัติแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/job-description` → CLICK **สร้างใบกำหนดหน้าที่งาน** | — | drawer **สร้างเอกสารใหม่** · ขั้น **ข้อมูลใบกำหนดหน้าที่ › เอกสารแนบ › ตรวจสอบและยืนยัน** | ☐ |
| 2 | SELECT ช่อง **ชื่อตำแหน่ง (ไทย)** | A: เจ้าหน้าที่บัญชีลูกหนี้ | แสดง **แผนก** แผนกบัญชี · **ฝ่าย** ฝ่ายบัญชีและการเงิน · **รายงานต่อ** หัวหน้าแผนกบัญชี · แถวหัวหน้าแรก หัวหน้าแผนกบัญชี 1 | ☐ |
| 3 | TYPE → **ชื่อตำแหน่งอังกฤษ** | A | ช่องแสดงค่า | ☐ |
| 4 | TYPE → การ์ด 2–5 | A | การ์ดสรุป **หัวข้อที่ต้องกรอก 4/4** | ☐ |
| 5 | CLICK **เพิ่มลูกน้อง** → TYPE ตำแหน่ง/จำนวน | A: ผู้ช่วยเจ้าหน้าที่บัญชี · 2 | บรรทัด **ผู้ใต้บังคับบัญชา 1 ตำแหน่ง · 2 คน** | ☐ |
| 6 | CLICK **ถัดไป** 2 ครั้ง → CLICK **บันทึกและส่งอนุมัติ** | — | modal **ส่งอนุมัติใบกำหนดหน้าที่งาน?** · ช่อง **ผู้อนุมัติ (Approved By)** ค่าเริ่ม **วิชัย บริหารดี** · ข้อความ **ค่าเริ่มต้นจากสายอนุมัติ (DOA กลาง)** | ☐ |
| 7 | CLICK **ส่งอนุมัติ** → WAIT toast | — | toast **ส่งอนุมัติแล้ว · JD-2569-0010** · แถวใหม่ pill **รออนุมัติ** ลายเซ็น **1/3** | ☐ |

#### TC-C02 — เลือกตำแหน่งแล้วระบบดึงข้อมูลจากผังองค์กร [AI-DEFAULT]
- group: สร้างใบกำหนดหน้าที่งาน · ความสำคัญ: สูง · trace: AC-01 / BR-01 / DEC-04 [AI-DEFAULT] / FN-01
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แผนก/ฝ่ายอ่านอย่างเดียว · รายงานต่อแก้ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ช่อง **ชื่อตำแหน่ง (ไทย)** | พนักงานคลังสินค้า | **แผนก** แผนกคลังสินค้า · **ฝ่าย** ฝ่ายปฏิบัติการ (ไม่มีช่องให้พิมพ์) · **รายงานต่อ** หัวหน้าแผนกคลังสินค้า | ☐ |
| 2 | TYPE → **รายงานต่อ** (แก้) | ผู้จัดการฝ่ายปฏิบัติการ | การ์ดสรุป **รายงานต่อ** เปลี่ยนตาม · เตือน **หัวหน้าแถวแรกไม่ตรงกับ "รายงานต่อ"** | ☐ |

#### TC-C03 — ผู้ใต้บังคับบัญชาคำนวณจากตารางลูกน้อง
- group: สร้างใบกำหนดหน้าที่งาน · ความสำคัญ: สูง · trace: AC-04 / BR-05 / DEC-13
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สรุป "N ตำแหน่ง · M คน" ทันทีที่พิมพ์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ตำแหน่ง → VERIFY บรรทัดผู้ใต้บังคับบัญชา | หัวหน้าแผนกบัญชี | ข้อความ **ผู้ใต้บังคับบัญชา ไม่มี** | ☐ |
| 2 | CLICK **เพิ่มลูกน้อง** 2 ครั้ง → TYPE ทั้ง 2 แถว | เจ้าหน้าที่บัญชีเจ้าหนี้ 1 · เจ้าหน้าที่บัญชีลูกหนี้ 2 | บรรทัด **2 ตำแหน่ง · 3 คน** และการ์ดสรุปตรงกัน | ☐ |

#### TC-C04 — บันทึกร่าง → แก้ไข → ส่ง (เลขเดิม)
- group: สร้างใบกำหนดหน้าที่งาน · ความสำคัญ: สูง · trace: BR-13 / DEC-11 / FN-03
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แก้ร่างได้ · ส่งแล้วเลขยังเป็น JD-2569-0006

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/job-description/view/R6` | — | drawer **JD-2569-0006** pill **ร่าง** · ปุ่ม **ยกเลิก · แก้ไข · ส่งอนุมัติ** | ☐ |
| 2 | CLICK **แก้ไข** | — | drawer ดูปิด แล้ว wizard เปิด หัว **แก้ไขเอกสาร** **JD-2569-0006** ค่าเดิมครบ | ☐ |
| 3 | CLICK **ถัดไป** 2 ครั้ง → **บันทึกและส่งอนุมัติ** → **ส่งอนุมัติ** | — | toast **ส่งอนุมัติแล้ว · JD-2569-0006** (เลขเดิม) | ☐ |

#### TC-C05 — แนบไฟล์ประกอบ
- group: สร้างใบกำหนดหน้าที่งาน · ความสำคัญ: กลาง · trace: DEC-12 / API-12
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=ผังโครงสร้าง.pdf
- Start: OPEN `#/job-description/create`
- ชุดข้อมูล: files=ผังโครงสร้าง.pdf
- ผ่านเมื่อ: ไฟล์ขึ้นในรายการ + ขั้นตรวจสอบนับ 1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK กรอกขั้น 1 ครบ → CLICK **ถัดไป** | A | หัว **แนบเอกสารประกอบ (ถ้ามี)** | ☐ |
| 2 | UPLOAD → กล่อง **คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)** | ผังโครงสร้าง.pdf | แถวไฟล์ **ผังโครงสร้าง.pdf** + ขนาด | ☐ |
| 3 | CLICK **ถัดไป** | — | การ์ด **เอกสารแนบ** นับ **1** | ☐ |

#### TC-C06 — ตำแหน่งที่มีฉบับใช้งานแล้ว แจ้งว่าจะถูกแทนที่
- group: สร้างใบกำหนดหน้าที่งาน · ความสำคัญ: กลาง · trace: EC-03 / BR-10 / DEC-04 [AI-DEFAULT]
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: การ์ดสรุปเตือนเลขฉบับเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ช่อง **ชื่อตำแหน่ง (ไทย)** | เจ้าหน้าที่บัญชีเจ้าหนี้ | การ์ดสรุปแสดง **ตำแหน่งนี้มีฉบับใช้งาน JD-2569-0001 — อนุมัติฉบับนี้แล้วฉบับเดิมจะถูกแทนที่** | ☐ |

### กลุ่ม V — กรอกไม่ครบ / ผิด

#### TC-V01 — กดถัดไปโดยไม่เลือกตำแหน่ง = บล็อก
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: สูง · trace: VR-01 (auto: e2e S7)
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก + toast + ช่องแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างใบกำหนดหน้าที่งาน** → CLICK **ถัดไป** | — | toast **กรุณากรอกข้อมูลให้ครบถ้วน** · ช่อง **ชื่อตำแหน่ง (ไทย)** แดง **กรุณาเลือกตำแหน่ง** | ☐ |

#### TC-V02 — ไม่กรอก KPI / หัวข้อบังคับ
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: สูง · trace: AC-02 / VR-04 / BR-02 [AI-DEFAULT]
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก การ์ด KPI ขอบแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ตำแหน่ง → กรอกชื่ออังกฤษ + การ์ด 2–4 · เว้น KPI → CLICK **ถัดไป** | A ยกเว้น KPI | การ์ด **5 ตัวชี้วัดผลการดำเนินงาน (KPI)** ขอบแดง **กรุณากรอกตัวชี้วัดผลการดำเนินงาน** · เลื่อนไปที่การ์ดนั้น | ☐ |

#### TC-V03 — ไม่ระบุชื่อตำแหน่งอังกฤษ
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: สูง · trace: VR-02 / DEC-17
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ตำแหน่ง → กรอกการ์ด 2–5 · เว้นชื่ออังกฤษ → CLICK **ถัดไป** | — | ช่อง **ชื่อตำแหน่งอังกฤษ** แดง **กรุณาระบุชื่อตำแหน่งภาษาอังกฤษ** | ☐ |

#### TC-V04 — ไม่มีผู้บังคับบัญชาโดยตรงเลย
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: สูง · trace: VR-05 / DEC-14
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก "ต้องมีผู้บังคับบัญชาโดยตรงอย่างน้อย 1 แถว"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ตำแหน่ง → ลบข้อความตำแหน่งในแถวหัวหน้า + จำนวน → กรอกการ์ด 2–5 ตามชุด A → CLICK **ถัดไป** | — | ข้อความแดง **ต้องมีผู้บังคับบัญชาโดยตรงอย่างน้อย 1 แถว** | ☐ |

#### TC-V05 — จำนวน (คน) ไม่ถูกต้อง
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: สูง · trace: VR-06 / DEC-15 / EC-10
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: 0 = บล็อก · ตัวอักษรถูกตัด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มลูกน้อง** → TYPE ตำแหน่ง + จำนวน | ผู้ช่วย · 0 | หลังกด **ถัดไป**: แถวแดง **จำนวน (คน) ต้องเป็นจำนวนเต็มตั้งแต่ 1** | ☐ |
| 2 | TYPE → จำนวน | abc | ช่องว่าง (ตัดตัวอักษรออก) | ☐ |

#### TC-V06 — กรอกจำนวนแต่ไม่กรอกตำแหน่ง
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: กลาง · trace: VR-07 / DEC-15
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มลูกน้อง** → TYPE จำนวนอย่างเดียว → CLICK **ถัดไป** | 3 | แถวแดง **กรอกจำนวนแล้วต้องระบุตำแหน่ง** | ☐ |

#### TC-V07 — หัวหน้าแถวแรกไม่ตรงรายงานต่อ = เตือนแต่ส่งได้
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: กลาง · trace: AC-14 / DEC-14 / W-01
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/create`
- ชุดข้อมูล: A
- ผ่านเมื่อ: มีข้อความเตือน · ไปขั้นถัดไปได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ตำแหน่ง → TYPE → ตำแหน่งแถวหัวหน้าแรก | ผู้จัดการทั่วไป | เตือน **หัวหน้าแถวแรกไม่ตรงกับ "รายงานต่อ" — ตรวจสอบอีกครั้ง (ไม่บล็อกการส่ง)** | ☐ |
| 2 | CLICK กรอกที่เหลือครบ → CLICK **ถัดไป** | A | ไปขั้น **เอกสารแนบ** ได้ | ☐ |

#### TC-V08 — แนบไฟล์ชนิดไม่รองรับ
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: กลาง · trace: API-12 file policy
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=script.exe
- Start: OPEN `#/job-description/create`
- ชุดข้อมูล: files=script.exe
- ผ่านเมื่อ: toast แจ้งชนิดไฟล์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD → กล่องแนบไฟล์ | script.exe | toast **script.exe — ชนิดไฟล์ไม่รองรับ** · ไม่มีแถวไฟล์ | ☐ |

#### TC-V09 — แนบไฟล์ใหญ่เกิน 20 MB
- group: กรอกไม่ครบ / ผิด · ความสำคัญ: ต่ำ · trace: API-12 file policy
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=big-25MB.pdf
- Start: OPEN `#/job-description/create`
- ชุดข้อมูล: files=big-25MB.pdf
- ผ่านเมื่อ: toast แจ้งขนาด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD → กล่องแนบไฟล์ | big-25MB.pdf | toast **ไฟล์ใหญ่เกินกำหนด (สูงสุด 20 MB)** | ☐ |

### กลุ่ม S — ส่งอนุมัติ

#### TC-S01 — ส่งอนุมัติ: ผู้อนุมัติค่าเริ่มจาก DOA และผู้จัดทำไม่อยู่ในรายชื่อ [AI-DEFAULT]
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: AC-05 / BR-07 / BR-09 / DEC-03 [AI-DEFAULT]
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ช่องผู้อนุมัติ 1 ขั้น ค่าเริ่มวิชัย · รายชื่อไม่มีสมศรี

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** | — | modal แถว **1** **ผู้อนุมัติ (Approved By)** ค่า **วิชัย บริหารดี** | ☐ |
| 2 | CLICK ช่องผู้อนุมัติ → พิมพ์ค้นหา | สมศรี | ไม่พบ **สมศรี ทดสอบงาน** ในรายการ | ☐ |
| 3 | CLICK **ส่งอนุมัติ** | — | toast **ส่งอนุมัติแล้ว · JD-2569-0006** · pill **รออนุมัติ** | ☐ |

#### TC-S02 — เพิ่มขั้นที่ DOA กลาง → ช่องผู้อนุมัติเพิ่มตาม
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: AC-15 / BR-07 (auto: e2e S8)
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description`
- ชุดข้อมูล: __QA__.doa.push('ฝ่ายบุคคล')
- ผ่านเมื่อ: modal มี 2 แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console `__QA__.doa.push('ฝ่ายบุคคล')` → OPEN `#/job-description/view/R6` → CLICK **ส่งอนุมัติ** | — | modal มี 2 แถว **1 ผู้อนุมัติ (Approved By)** · **2 ฝ่ายบุคคล** | ☐ |

#### TC-S03 — ส่งไม่สำเร็จ (API ล้ม)
- group: ส่งอนุมัติ · ความสำคัญ: กลาง · trace: 06 §6.10 (auto: e2e S9)
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R6`
- ชุดข้อมูล: __QA__.sim('error')
- ผ่านเมื่อ: toast error · สถานะยังร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console `__QA__.sim('error')` → CLICK **ส่งอนุมัติ** → **ส่งอนุมัติ** | — | toast **ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง** · pill ยังเป็น **ร่าง** | ☐ |

### กลุ่ม A — อนุมัติ / ไม่อนุมัติ

#### TC-A01 — ผู้อนุมัติอนุมัติ
- group: อนุมัติ / ไม่อนุมัติ · ความสำคัญ: สูง · trace: AC-06 / FN-05
- actor (role): ผู้อนุมัติ ผู้บังคับบัญชาของ E01
- Setup: role=ผู้อนุมัติ ผู้บังคับบัญชาของ E01 (__QA__.setMe('E02')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R5`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สถานะ "อนุมัติแล้ว" · ลายเซ็น 2/3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/job-description/view/R5` | — | แบนเนอร์ **รอ วิชัย บริหารดี อนุมัติ — คุณเป็นผู้อนุมัติ** · ปุ่ม **ไม่อนุมัติ** **อนุมัติ** | ☐ |
| 2 | CLICK **อนุมัติ** → CLICK **อนุมัติ** ใน modal | — | toast **อนุมัติแล้ว · JD-2569-0005** · pill **อนุมัติแล้ว** | ☐ |
| 3 | CLICK แท็บ **ลายเซ็น / อนุมัติ** | — | **2/3** · ขั้น 1 pill **อนุมัติ** · ผู้ดำรงตำแหน่ง **รอรับทราบ** | ☐ |

#### TC-A02 — ไม่อนุมัติ = กลับเป็นร่างเลขเดิม [AI-DEFAULT]
- group: อนุมัติ / ไม่อนุมัติ · ความสำคัญ: สูง · trace: AC-07 / BR-08 / DEC-09 [AI-DEFAULT]
- actor (role): ผู้อนุมัติ ผู้บังคับบัญชาของ E01
- Setup: role=ผู้อนุมัติ ผู้บังคับบัญชาของ E01 (__QA__.setMe('E02')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R5`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สถานะกลับเป็นร่าง · ผู้จัดทำแก้ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ไม่อนุมัติ** → CLICK **ไม่อนุมัติ** ใน modal ทันที | — | ช่อง **เหตุผล** แดง **กรุณาระบุเหตุผล** | ☐ |
| 2 | CLICK chip **KPI ยังวัดผลไม่ได้ ขอปรับให้มีตัวเลข** → CLICK **ไม่อนุมัติ** | — | toast **ไม่อนุมัติ — ส่งกลับเป็นร่างแล้ว · JD-2569-0005** · ใบหายจากรายการของผู้อนุมัติ | ☐ |
| 3 | PRESS `__QA__.setMe('E01')` → OPEN `#/job-description/view/R5` | — | pill **ร่าง** · ปุ่ม **แก้ไข** · ประวัติ **ไม่อนุมัติ — กลับเป็นร่าง** | ☐ |

#### TC-A03 — อนุมัติฉบับใหม่ → ฉบับเดิมถูกแทนที่ [AI-DEFAULT]
- group: อนุมัติ / ไม่อนุมัติ · ความสำคัญ: สูง · trace: AC-13 / BR-10 / DEC-04 [AI-DEFAULT] / FN-09
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: JD-2569-0001 กลายเป็น "ถูกแทนที่"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** → **ส่งอนุมัติ** | — | modal แจ้ง **อนุมัติแล้ว JD-2569-0001 (ฉบับใช้งานของตำแหน่งนี้) จะถูกแทนที่** · ส่งแล้ว pill **รออนุมัติ** | ☐ |
| 2 | PRESS `__QA__.setMe('E02')` → OPEN `#/job-description/view/R6` → CLICK **อนุมัติ** → **อนุมัติ** | — | toast **อนุมัติแล้ว · JD-2569-0006** | ☐ |
| 3 | OPEN `#/job-description` → VERIFY แถว JD-2569-0001 | — | pill **ถูกแทนที่** · เปิดดูแบนเนอร์ **ฉบับนี้ถูกแทนที่ด้วย JD-2569-0006** | ☐ |

#### TC-A04 — อนุมัติเรียงขั้นเมื่อ DOA มี 2 ขั้น
- group: อนุมัติ / ไม่อนุมัติ · ความสำคัญ: กลาง · trace: BR-07 / FN-05
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description`
- ชุดข้อมูล: __QA__.doa.push('ฝ่ายบุคคล')
- ผ่านเมื่อ: ขั้น 2 รอจนขั้น 1 อนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS `__QA__.doa.push('ฝ่ายบุคคล')` → ส่ง JD-2569-0006 (ขั้น 2 = ศศิธร มีสุข) | — | ลายเซ็น **1/4** | ☐ |
| 2 | PRESS `__QA__.setMe('E02')` → อนุมัติ | — | pill ยัง **รออนุมัติ** · แบนเนอร์ **รอ ศศิธร มีสุข อนุมัติ** | ☐ |

### กลุ่ม K — ผู้ดำรงตำแหน่งรับทราบ

#### TC-K01 — ผู้ดำรงตำแหน่งกดรับทราบ
- group: ผู้ดำรงตำแหน่งรับทราบ · ความสำคัญ: สูง · trace: AC-08 / BR-11 / DEC-16 / FN-11
- actor (role): ผู้ดำรงตำแหน่ง
- Setup: role=ผู้ดำรงตำแหน่ง (__QA__.setMe('E05')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สถานะ "รับทราบแล้ว" · ลายเซ็น 3/3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/job-description` | — | เห็น 1 แถว **JD-2569-0002** pill **อนุมัติแล้ว** · badge **รอคุณ 1** | ☐ |
| 2 | CLICK แถว → CLICK **รับทราบ** → **รับทราบ** ใน modal | — | toast **รับทราบแล้ว · JD-2569-0002** · pill **รับทราบแล้ว** | ☐ |
| 3 | CLICK แท็บ **PDF Preview** | — | ช่อง **ผู้ดำรงตำแหน่ง (Acknowledged By)** มี (วรวุฒิ ทองดี) + **รับทราบในระบบ** วันเวลา | ☐ |

#### TC-K02 — ฝ่ายบุคคลระบุผู้ดำรงตำแหน่งหลังอนุมัติ [AI-DEFAULT]
- group: ผู้ดำรงตำแหน่งรับทราบ · ความสำคัญ: สูง · trace: AC-09 / BR-11 / DEC-04 [AI-DEFAULT] / FN-10
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R2`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บันทึกได้ · ผู้ดำรงตำแหน่งใหม่เห็นใบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **ลายเซ็น / อนุมัติ** → CLICK **เปลี่ยนผู้ดำรงตำแหน่ง** | — | modal **เปลี่ยนผู้ดำรงตำแหน่ง** · ช่อง **พนักงานที่ดำรงตำแหน่ง** | ☐ |
| 2 | CLICK **บันทึกและแจ้งเตือน** โดยไม่เลือก | — | ช่องแดง **กรุณาเลือกพนักงาน** | ☐ |
| 3 | SELECT พนักงาน → CLICK **บันทึกและแจ้งเตือน** | ปิยะนุช แก้วมณี | toast **แจ้งผู้ดำรงตำแหน่งให้รับทราบแล้ว** · ปิยะนุช แก้วมณี · ประวัติ **ระบุผู้ดำรงตำแหน่ง** | ☐ |

#### TC-K03 — รับทราบไม่ได้ก่อนอนุมัติ
- group: ผู้ดำรงตำแหน่งรับทราบ · ความสำคัญ: กลาง · trace: DEC-16 / BR-11
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มรับทราบในใบรออนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **ลายเซ็น / อนุมัติ** | — | แถว **ผู้ดำรงตำแหน่ง (Acknowledged By)** pill **ยังไม่ถึง** · ไม่มีปุ่ม **รับทราบ** | ☐ |

### กลุ่ม X — ยกเลิก

#### TC-X01 — ผู้จัดทำยกเลิกร่าง (เหตุผลบังคับ)
- group: ยกเลิก · ความสำคัญ: สูง · trace: AC-12 / BR-15 / DEC-09 [AI-DEFAULT]
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: pill ยกเลิก + เหตุผลในแบนเนอร์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยกเลิก** → CLICK **ยกเลิกเอกสาร** ทันที | — | ช่อง **เหตุผล** แดง **กรุณาระบุเหตุผล** | ☐ |
| 2 | CLICK chip **บันทึกซ้ำ** → CLICK **ยกเลิกเอกสาร** | — | toast **ยกเลิกเอกสารแล้ว · JD-2569-0006** · แบนเนอร์ **ยกเลิกแล้ว — บันทึกซ้ำ** | ☐ |

#### TC-X02 — ฝ่ายบุคคลยกเลิกใบที่รออนุมัติ
- group: ยกเลิก · ความสำคัญ: สูง · trace: BR-15 / NTF jd_cancelled
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: pill ยกเลิก · ผู้อนุมัติได้แจ้ง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยกเลิกเอกสาร** | — | modal **ยกเลิกเอกสาร?** หัวรอง **รออนุมัติอยู่ — ผู้อนุมัติจะได้รับแจ้ง** | ☐ |
| 2 | TYPE → **เหตุผล** → CLICK **ยกเลิกเอกสาร** | เลือกตำแหน่งผิด | toast **ยกเลิกเอกสารแล้ว · JD-2569-0003** | ☐ |

#### TC-X03 — ใบอนุมัติแล้วไม่มีปุ่มยกเลิก
- group: ยกเลิก · ความสำคัญ: กลาง · trace: BR-15 / 05 §5.2
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R2`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/job-description/view/R2` | — | หัว drawer ไม่มี **ยกเลิกเอกสาร** · เมนู ⋮ ไม่มี **ยกเลิกเอกสาร** | ☐ |

### กลุ่ม P — ใครเห็นอะไร

#### TC-P01 — ผู้อนุมัติไม่เห็นร่างของคนอื่น
- group: ใครเห็นอะไร · ความสำคัญ: สูง · trace: TC-D01 / BR-12 / DEC-10 (auto: e2e S3)
- actor (role): ผู้อนุมัติ ผู้บังคับบัญชาของ E01
- Setup: role=ผู้อนุมัติ ผู้บังคับบัญชาของ E01 (__QA__.setMe('E02')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 3 ใบ ไม่มี JD-2569-0006 (ร่าง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/job-description` | — | ตาราง 3 แถว (0001, 0002, 0005) · ไม่พบ **JD-2569-0006** | ☐ |
| 2 | OPEN `#/job-description/view/R6` | — | ไม่เปิด drawer (ไม่มีสิทธิ์) | ☐ |

#### TC-P02 — ผู้ดำรงตำแหน่งไม่เห็นใบที่ยังไม่อนุมัติ
- group: ใครเห็นอะไร · ความสำคัญ: สูง · trace: TC-D03 / EC-06 / DEC-16
- actor (role): ผู้ดำรงตำแหน่ง
- Setup: role=ผู้ดำรงตำแหน่ง (__QA__.setMe('E05')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นแค่ใบอนุมัติแล้วของตน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/job-description` | — | ตาราง 1 แถว **JD-2569-0002** เท่านั้น | ☐ |
| 2 | OPEN `#/job-description/view/R5` | — | ไม่เปิด drawer (ไม่มีสิทธิ์) | ☐ |

#### TC-P03 — ผู้จัดทำไม่เห็นใบของหน่วยงานอื่น
- group: ใครเห็นอะไร · ความสำคัญ: สูง · trace: TC-D02 / DEC-10 (auto: e2e S6)
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่เปิด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/job-description/view/R3` | — | ไม่เปิด drawer · รายการไม่มี **JD-2569-0003** | ☐ |

#### TC-P04 — ส่งแล้วแก้ไม่ได้
- group: ใครเห็นอะไร · ความสำคัญ: สูง · trace: TC-D05 / BR-16
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R5`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มแก้ไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/job-description/view/R5` | — | ไม่มีปุ่ม **แก้ไข** · footer **ส่งแล้ว ล็อกแก้ไข** | ☐ |

#### TC-P05 — ผู้ที่ไม่ใช่ผู้อนุมัติขั้นปัจจุบันไม่มีปุ่มอนุมัติ
- group: ใครเห็นอะไร · ความสำคัญ: กลาง · trace: TC-D04/D06 / BR-09
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R5`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มอนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **ลายเซ็น / อนุมัติ** | — | ขั้น 1 pill **รออนุมัติ** · ไม่มีปุ่ม **อนุมัติ** สำหรับผู้จัดทำ | ☐ |

#### TC-P06 — CSV ส่งออกเฉพาะใบที่เห็น
- group: ใครเห็นอะไร · ความสำคัญ: กลาง · trace: TC-D09 / API-11
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ส่งออก 4 รายการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งออก CSV** | — | toast **ส่งออก 4 รายการ** | ☐ |

### กลุ่ม D — แบบพิมพ์ PDF

#### TC-D01 — PDF Preview ร่าง ตรงแบบฟอร์ม FM-HRM-32
- group: แบบพิมพ์ PDF · ความสำคัญ: สูง · trace: AC-11 / DEC-07 / FN-08
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ถ้อยคำตามกระดาษ · footer ร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | หัว **ใบกำหนดหน้าที่งานประจำตำแหน่ง (Job Description)** · หัวข้อ **1.ข้อมูลทั่วไป (Job Title)** ถึง **6.คุณสมบัติอื่น ๆ (Other)** · ตาราง **ผู้บังคับบัญชาโดยตรง(หัวหน้า)** / **ผู้ใต้บังคับบัญชาโดยตรง(ลูกน้อง)** | ☐ |
| 2 | VERIFY ท้ายกระดาษ | — | **เลขที่ JD-2569-0006 · ร่าง** · **Doc No. FM-HRM-32 · Rev. 00 : 01/07/2569** · ไม่มีวงเล็บปีกกา {{ }} | ☐ |

#### TC-D02 — PDF ลงนาม 3 ช่องตามกระดาษ ไม่ใช้ภาพ
- group: แบบพิมพ์ PDF · ความสำคัญ: สูง · trace: BR-14 / DEC-08
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ผู้จัดทำ · ผู้อนุมัติ · ผู้ดำรงตำแหน่ง มีข้อความในระบบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** → VERIFY ตารางลงนาม | — | **ผู้จัดทำ (Prepared By)** ส่งในระบบ · **ผู้อนุมัติ (Approved By)** ☑ อนุมัติ พิจารณาในระบบ · **ผู้ดำรงตำแหน่ง (Acknowledged By)** รับทราบในระบบ | ☐ |

#### TC-D03 — PDF ลูกน้องหลายแถว + บรรทัดข้อความ
- group: แบบพิมพ์ PDF · ความสำคัญ: กลาง · trace: BR-06 / EC-04 / DEC-06
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R9`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ตารางแสดงแถวครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | ตารางลูกน้องมี **หัวหน้าแผนกคลังสินค้า 1** · **หัวหน้าแผนกขนส่ง 1** · ช่อง **ผู้ใต้บังคับบัญชา** = **2 ตำแหน่ง · 2 คน** | ☐ |

#### TC-D04 — PDF DOA 6 ขั้น = ช่องลงนาม 2 แถว
- group: แบบพิมพ์ PDF · ความสำคัญ: กลาง · trace: EC-05 / BR-14
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description`
- ชุดข้อมูล: __QA__.doa.push ×5
- ผ่านเมื่อ: ลงนาม 8 ช่อง 4+4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS `__QA__.doa.push()` 5 ครั้ง → ส่ง JD-2569-0006 → CLICK แท็บ **PDF Preview** | — | ตารางลงนาม 2 แถว แถวละ 4 ช่อง | ☐ |

#### TC-D05 — ดาวน์โหลด / พิมพ์
- group: แบบพิมพ์ PDF · ความสำคัญ: กลาง · trace: API-10
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เปิดหน้าต่างพิมพ์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอน **พิมพ์** ที่หัว drawer | — | toast **กำลังเปิดหน้าต่างพิมพ์ · JD-2569-0001** | ☐ |

### กลุ่ม E — การใช้งานทั่วไป

#### TC-E01 — ปิดหน้ากรอกที่ค้างอยู่ถามก่อนทิ้ง
- group: การใช้งานทั่วไป · ความสำคัญ: กลาง · trace: 01 §1.2 dirty-check
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal ทิ้งข้อมูล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ตำแหน่ง → CLICK ปุ่ม x | — | modal **ทิ้งข้อมูลที่กรอกไว้?** · ปุ่ม **กลับไปกรอกต่อ** **ทิ้งข้อมูล** | ☐ |

#### TC-E02 — Esc ปิด modal ก่อน drawer
- group: การใช้งานทั่วไป · ความสำคัญ: กลาง · trace: U8 (auto: e2e S10)
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: Esc ครั้งแรกปิด modal

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยกเลิก** → PRESS Esc | — | modal ปิด drawer ยังเปิด | ☐ |
| 2 | PRESS Esc | — | drawer ปิด | ☐ |

#### TC-E03 — ลากเมาส์ออกนอก drawer ไม่ปิด
- group: การใช้งานทั่วไป · ความสำคัญ: ต่ำ · trace: U25
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: drawer ยังเปิด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK กดเมาส์ในช่องค้นหาของ drawer แล้วลากไปปล่อยบนพื้นมืด | — | drawer ยังเปิดอยู่ | ☐ |

#### TC-E04 — แบบเอกสารยังไม่เปิดใช้ สร้างไม่ได้
- group: การใช้งานทั่วไป · ความสำคัญ: กลาง · trace: EC-09 / BR-13
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description`
- ชุดข้อมูล: __QA__.setDocActive(false)
- ผ่านเมื่อ: ปุ่มสร้าง disabled + แถบแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console `__QA__.setDocActive(false)` | — | แถบแดง **แบบเอกสารนี้ยังไม่เปิดใช้งาน — สร้างใบกำหนดหน้าที่งานใหม่ไม่ได้** · ปุ่ม **สร้างใบกำหนดหน้าที่งาน** กดไม่ได้ | ☐ |

### กลุ่ม H — ประวัติ

#### TC-H01 — ประวัติเรียงเวลา append-only
- group: ประวัติ · ความสำคัญ: กลาง · trace: 01 §1.4 / audit
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ล่าสุดอยู่บน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **ประวัติ** | — | บนสุด **ถูกแทนที่** (แทนที่ด้วย JD-2569-0009) → **ผู้ดำรงตำแหน่งรับทราบ** → **อนุมัติ (ขั้น 1)** → **ส่งอนุมัติ** → **สร้างเอกสาร** | ☐ |

#### TC-H02 — แท็บลายเซ็นแสดงสาย DOA
- group: ประวัติ · ความสำคัญ: กลาง · trace: U13 / §6.1
- actor (role): ฝ่ายบุคคล role-mgr-hr
- Setup: role=ฝ่ายบุคคล role-mgr-hr (__QA__.setMe('E08')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สรุป DOA-JD-01 · 1 ขั้น · 3/3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **ลายเซ็น / อนุมัติ** | — | การ์ดสรุป **DOA-JD-01 · 1 ขั้น** · **3/3** · timeline ผู้จัดทำ → ขั้น 1 → ผู้ดำรงตำแหน่ง | ☐ |

### กลุ่ม XT — เชื่อมระบบอื่น

#### TC-XT01 — อนุมัติแล้วแจ้งผู้ดำรงตำแหน่ง (jd_ack_requested)
- group: เชื่อมระบบอื่น · ความสำคัญ: กลาง · trace: NTF jd_ack_requested / FN-09 (ต้อง simulate)
- actor (role): ผู้อนุมัติ ผู้บังคับบัญชาของ E01
- Setup: role=ผู้อนุมัติ ผู้บังคับบัญชาของ E01 (__QA__.setMe('E02')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/view/R5`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ผู้ดำรงตำแหน่งได้แจ้งเตือน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK อนุมัติ JD-2569-0005 → สลับเป็นผู้ดำรงตำแหน่ง | — | (ต้นแบบ) ตัวเลขเมนู **ใบกำหนดหน้าที่งาน (JD)** เพิ่ม 1 · ระบบจริง: แจ้งเตือนตาม NTF_BRIEF ⚠ ยืนยัน anchor | ☐ |

#### TC-XT02 — เลขเอกสารจาก F-DOCCFG รูปแบบ JD-ปี-ลำดับ
- group: เชื่อมระบบอื่น · ความสำคัญ: กลาง · trace: BR-13 / DOCCFG JD
- actor (role): ผู้จัดทำ
- Setup: role=ผู้จัดทำ (__QA__.setMe('E01')) · seed=prototype seed · files=—
- Start: OPEN `#/job-description/create`
- ชุดข้อมูล: A
- ผ่านเมื่อ: เลขรูปแบบ JD-2569-NNNN

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK สร้างและบันทึกแบบร่าง | A | toast **บันทึกร่างแล้ว · JD-2569-0010** | ☐ |

## วิธีที่ agent รัน (Run protocol)
1. เปิด feature.html → ไปที่ `#/job-description`
2. ตั้ง role ตาม Setup ด้วย `__QA__.setMe('E01'|'E02'|'E05'|'E08')` (ตัวสลับผู้ใช้มุมขวาบนก็ได้)
3. seed พิเศษ: `__QA__.sim('error')` · `__QA__.setDocActive(false)` · `__QA__.doa.push(label)` — รีโหลดหน้าเพื่อล้าง
4. ทำ step ตามลำดับ · บันทึกผลตาม schema · เคส (auto: e2e …) ใช้ผล e2e_standard.py ได้

## Coverage Audit
| หมวด | covered / total |
|---|---|
| AC (06_TESTS) | 15 / 15 |
| Business rules (05_RULES) | 16 / 16 |
| Validation | 9 / 9 |
| Edge cases | 8 / 10 |
| Permission cells | 8 / 8 |
| Cross-cutting / events / states | ครบ |

- Cross-Module (XT): 4/4
- Scope Lock (DEC): 17/17
- **Manifest cross-check (FRD §0.12): ✅ 8/8**

### ข้าม (พร้อมเหตุผล)
- EC-01 ตำแหน่งสูงสุดไม่มีหัวหน้า · EC-02 resolve ผู้บังคับบัญชาไม่ได้ — seed ต้นแบบไม่มีกรณีนี้ในเส้นทางผู้จัดทำ → ทดสอบตอน UAT ระบบจริง

## Result Report (schema)
```json
{
 "feature_id": "F-TMP-004",
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
  "total": 54,
  "pass": 0,
  "fail": 0,
  "blocked": 0
 }
}
```

# AI Test Cases — F-TMP-007 แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าต่างประเทศ

ชุดทดสอบสำหรับ AI agent (browser-use/vision) บน prototype `feature.html` · ข้อมูลทั้งหมดเป็นข้อมูลสมมติ · เคสที่ derive จากมติ AI-DEFAULT ติด `[AI-DEFAULT]` (ผล fail อาจแปลว่าค่า default ผิด ไม่ใช่โค้ดผิด)

## Meta
| Field | Value |
|---|---|
| Feature ID | F-TMP-007 (ชั่วคราว) |
| ชื่อ | แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าต่างประเทศ (doc SES · FM-SAL-23) |
| เวอร์ชัน | 1.0 (2026-10-10) |
| App entry | feature.html |
| Routes | `#/csat-overseas-summary` · `#/csat-overseas-summary/create` · `#/csat-overseas-summary/edit/:id` · `#/csat-overseas-summary/view/:id` |
| ที่มา | FRD_F-TMP-007_Pack v1.0 · BRD-SAL-SES-001 · feature.html (html-generator-v9.4 Q-form) · DECISIONS.lock 15 DEC |
| จำนวนเคส | 45 |
| หมายเหตุ | anchor อ้างจากข้อความใน feature.html · verify_anchors.py ยังไม่รัน (NO-BROWSER) · ค่าที่คาดหวังตรวจกับ prototype ในคอนเทนเนอร์แล้ว |

## Coverage
| group | เคส | สูง/กลาง/ต่ำ |
|---|---|---|
| รายการ | 8 | 1/5/2 |
| สร้าง | 8 | 4/3/1 |
| ตรวจสอบข้อมูล | 5 | 4/1/0 |
| ส่งอนุมัติ | 6 | 3/2/1 |
| อนุมัติ | 4 | 2/2/0 |
| ยกเลิก | 2 | 1/1/0 |
| สิทธิ์ | 6 | 5/1/0 |
| PDF | 3 | 1/2/0 |
| ขอบเขต | 3 | 0/1/2 |

## Coverage Ledger
### Acceptance (06_TESTS)
| item | cases |
|---|---|
| AC-01 | TC-C01 |
| AC-02 | TC-C02 |
| AC-03 | TC-C04 |
| AC-04 | TC-C05 |
| AC-05 | TC-V01, TC-V05 |
| AC-06 | TC-V02, TC-V03 |
| AC-07 | TC-C06 |
| AC-08 | TC-S03 |
| AC-09 | TC-S01, TC-S05 |
| AC-10 | TC-A01 |
| AC-11 | TC-A02, TC-A03 |
| AC-12 | TC-X01 |
| AC-13 | TC-D01, TC-D03 |
| AC-14 | TC-P05 |
### Business Rules (05_RULES)
| item | cases |
|---|---|
| BR-01 | TC-C02 |
| BR-02 | TC-C05, TC-V02 |
| BR-03 | TC-C03, TC-V03 |
| BR-04 | TC-C04 |
| BR-05 | TC-C04 |
| BR-06 | TC-S03 |
| BR-07 | TC-V05, TC-S04 |
| BR-08 | TC-S01 |
| BR-09 | TC-A02, TC-A03 |
| BR-10 | TC-C01 |
| BR-11 | TC-L01, TC-P01 |
| BR-12 | TC-D01, TC-D03, TC-S05 |
| BR-13 | TC-A01 |
| BR-14 | TC-L07, TC-E03 |
| BR-15 | TC-D02 |
### Validation
| item | cases |
|---|---|
| VR-01 | TC-V01 |
| VR-02 | TC-V01 |
| VR-03 | TC-V02 |
| VR-04 | TC-V03 |
| VR-05 | TC-V04, TC-V05, TC-S04 |
| VR-06 | TC-S02 |
| VR-07 | TC-A02 |
### Edge Cases
| item | cases |
|---|---|
| EC-01 | — (ข้าม: seed ไม่มีเดือนว่าง — ดู Coverage Audit) |
| EC-02 | TC-C03 |
| EC-03 | TC-C05 |
| EC-04 | TC-S03 |
| EC-05 | TC-C06 |
| EC-06 | TC-E03 (บันทึกผล — ยังไม่มีกฎ OQ-06) |
| EC-07 | TC-E03 |
| EC-08 | TC-E03 |
| EC-09 | TC-S06, TC-E02 |
| EC-10 | TC-E01 |
| EC-11 | TC-S05, TC-D03 |
| EC-12 | TC-V04 |
### Permission / Deny
| item | cases |
|---|---|
| TC-D01 | TC-P01 |
| TC-D02 | TC-P02 |
| TC-D03 | TC-P03 |
| TC-D04 | TC-P04 |
| TC-D05 | TC-P06 |
| TC-D06 | TC-X02 |
### Scope Lock (DEC)
| item | cases |
|---|---|
| DEC-01 | TC-C02, TC-E03 |
| DEC-02 | TC-E03 |
| DEC-03 | TC-S01, TC-S05 |
| DEC-04 | TC-C02, TC-S03 |
| DEC-05 | TC-C03, TC-V03, TC-D01 |
| DEC-06 | TC-D02 |
| DEC-07 | TC-D01 |
| DEC-08 | TC-A02, TC-X01 |
| DEC-09 | TC-L01, TC-P01, TC-P05 |
| DEC-10 | TC-C01 |
| DEC-11 | TC-L07, TC-C07 |
| DEC-12 | TC-C06, TC-D02 |
| DEC-13 | TC-C04 |
| DEC-14 | TC-C05, TC-V02 |
| DEC-15 | TC-D01 |
### Cross-Module / Events (XT)
| item | cases |
|---|---|
| ses_cancelled | TC-X01 (ต้อง simulate — เห็นผลฝั่งต้นทาง) |
| ses_low_score_approved | TC-A01 |
| ses.approved ไม่ยิง (DEC-02) | TC-E03 |
| F-DOCCFG status | TC-E01 |
| F-TMP-006 SEA (อ่านอย่างเดียว) | TC-C02, TC-S03 |

## Data Sets
| ชุด | ฟิลด์ | ค่า |
|---|---|---|
| A | ประจำเดือน · ลูกค้า | กันยายน 2569 (ลูกค้ามีแบบประเมินบันทึกผลแล้ว 12 ราย · ลูกค้า 03 มี 2 ใบ · ลูกค้า 09 ถูกยกเลิก) |
| B | ลูกค้าเกิน | สิงหาคม 2569 (14 ราย) |
| C | ข้อความ | สรุปผล "ทดสอบ" · ข้อความยาว 1,050 ตัวอักษร |
### ไฟล์ทดสอบ (Files)
- สรุปคะแนน.xlsx (50 KB) · virus.exe (ชนิดไม่รองรับ)

## Test Cases
### TC-L01 — รายการแสดงเฉพาะใบที่มีสิทธิ์ (owner) [AI-DEFAULT]
- group: รายการ · ความสำคัญ: สูง · trace: FN-09 / BR-11 / DEC-09 (auto: e2e S2)
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 8 แถว ไม่เห็นร่างของคนอื่น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary` | — | หัว **แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าต่างประเทศ** + badge **8 รายการ** | ☐ |
| 2 | VERIFY หัวคอลัมน์ | — | **เลขที่** **ประจำเดือน** **ผู้สรุปผล** **หน่วยงาน** **ลูกค้าที่ประเมิน** **คะแนนต่ำ** **สถานะเอกสาร** **ลายเซ็น** | ☐ |
| 3 | VERIFY ไม่มีแถว SES-2569-0009 | — | ใบร่างของคนอื่นไม่อยู่ในรายการ (ไม่เห็นร่างของคนอื่น) | ☐ |

### TC-L02 — ไม่มีแถบการ์ดสถิติ ตัวเลขอยู่ใน badge
- group: รายการ · ความสำคัญ: กลาง · trace: U1 / U22
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: —
- ผ่านเมื่อ: badge ≤ 3 ไม่มีการ์ดตัวเลข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary` | — | ใต้หัวเห็น badge **8 รายการ** และ **รออนุมัติ 2** | ☐ |
| 2 | VERIFY พื้นที่ระหว่างหัวกับตาราง | — | ไม่มีการ์ดสถิติ ถัดไปคือแถบค้นหา | ☐ |

### TC-L03 — ค้นหาด้วยเลขที่
- group: รายการ · ความสำคัญ: กลาง · trace: API-01 q
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: q=0008
- ผ่านเมื่อ: เหลือ 1 แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา **ค้นหาเลขที่ / ผู้สรุป / เดือน / ลูกค้า** | 0008 | เหลือแถว **SES-2569-0008** | ☐ |
| 2 | VERIFY ท้ายตาราง | — | **1 – 1 จาก 1 รายการ** | ☐ |

### TC-L04 — ค้นหาไม่พบ แสดง empty state แล้วรีเซ็ต
- group: รายการ · ความสำคัญ: กลาง · trace: U23
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: q=ไม่มีจริง
- ผ่านเมื่อ: เห็นข้อความไม่พบ แล้วกลับครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา | ไม่มีจริง | ตารางแสดง **ไม่พบรายการที่ค้นหา** | ☐ |
| 2 | CLICK ปุ่ม **รีเซ็ต** | — | ช่องค้นหาว่าง ตารางกลับ 8 แถว | ☐ |

### TC-L05 — กรองสถานะรออนุมัติ
- group: รายการ · ความสำคัญ: กลาง · trace: API-01 status
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: สถานะ=รออนุมัติ
- ผ่านเมื่อ: เหลือ 2 แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ตัวกรอง **ทุกสถานะ** | รออนุมัติ | เหลือ **SES-2569-0007** และ **SES-2569-0008** | ☐ |

### TC-L06 — เมนู ⋮ ของร่างตัวเอง
- group: รายการ · ความสำคัญ: ต่ำ · trace: U5 / 05 §5.3
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เมนูครบ 4 รายการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ⋮ ที่แถว **SES-2569-0010** | — | เมนู **ดูรายละเอียด** **แก้ไข** **พิมพ์** **ยกเลิกเอกสาร** | ☐ |

### TC-L07 — ส่งออก CSV [AI-DEFAULT]
- group: รายการ · ความสำคัญ: กลาง · trace: API-10 / BR-14 / DEC-11
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ได้ไฟล์ CSV + toast

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งออก CSV** | — | ดาวน์โหลด **csat-overseas-summary.csv** · toast **ส่งออก 8 รายการ** | ☐ |

### TC-L08 — เปลี่ยนจำนวนต่อหน้า
- group: รายการ · ความสำคัญ: ต่ำ · trace: U6
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: แสดงต่อหน้า=10
- ผ่านเมื่อ: pager ถูกต้อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT **แสดงต่อหน้า** | 10 | ท้ายตาราง **1 – 8 จาก 8 รายการ** | ☐ |

### TC-C01 — บันทึกร่างโดยยังไม่เขียนสรุปผล ได้เลขที่ SES [AI-DEFAULT]
- group: สร้าง · ความสำคัญ: สูง · trace: FN-03 / BR-10 / DEC-10 / AC-01
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: ชุด A (1 ลูกค้า)
- ผ่านเมื่อ: ได้เลข SES-2569-0012 สถานะร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบสรุป** | — | drawer **ใบสรุปความพึงพอใจ ลูกค้าต่างประเทศ** ขั้น 1 **ข้อมูลหลักใบสรุป** | ☐ |
| 2 | SELECT ช่อง **ประจำเดือน** | กันยายน 2569 | แสดง **กันยายน 2569** | ☐ |
| 3 | SELECT ช่อง **เพิ่มลูกค้าทีละราย** | ลูกค้าตัวอย่าง ต่างประเทศ 01 | แถว 1 **ลูกค้าตัวอย่าง ต่างประเทศ 01** · **12 ก.ย. 69 · SEA-2569-0135** | ☐ |
| 4 | CLICK ปุ่ม **ถัดไป** 2 ครั้ง | — | ขั้น 3 **ตรวจสอบและยืนยัน** | ☐ |
| 5 | CLICK ปุ่ม **บันทึกแบบร่าง** | — | toast **บันทึกร่างแล้ว · SES-2569-0012** · แถวใหม่สถานะ **ร่าง** | ☐ |

### TC-C02 — ดึงแบบประเมินที่บันทึกผลแล้วของเดือน [AI-DEFAULT]
- group: สร้าง · ความสำคัญ: สูง · trace: FN-02 / BR-01 / DEC-01 / DEC-04 / AC-02
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: กันยายน 2569
- ผ่านเมื่อ: เพิ่ม 8 ราย แจ้งเหลือ 4 · ไม่มีลูกค้าที่แบบประเมินถูกยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบสรุป** | — | drawer **ใบสรุปความพึงพอใจ ลูกค้าต่างประเทศ** ขั้น 1 **ข้อมูลหลักใบสรุป** | ☐ |
| 2 | SELECT ช่อง **ประจำเดือน** | กันยายน 2569 | แสดง **กันยายน 2569** | ☐ |
| 3 | CLICK ปุ่ม **ดึงแบบประเมินที่บันทึกผลแล้วของเดือนนี้** | — | toast **เพิ่มลูกค้า 8 ราย · ยังเหลือ 4 ราย (เกิน 8 — ทำใบสรุปเพิ่ม)** · การ์ดสรุป **ลูกค้า 8 / 8 ราย** | ☐ |
| 4 | VERIFY รายชื่อ | — | ไม่มี **ลูกค้าตัวอย่าง ต่างประเทศ 09** (แบบประเมินถูกยกเลิก) | ☐ |

### TC-C03 — ลูกค้าเกิน 8 ราย ดึงได้ 8 และแจ้งที่เหลือ [AI-DEFAULT]
- group: สร้าง · ความสำคัญ: สูง · trace: BR-03 / EC-02 / DEC-05
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: สิงหาคม 2569 (มี 14 ราย)
- ผ่านเมื่อ: เพิ่ม 8 แจ้งเหลือ 6

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบสรุป** | — | drawer **ใบสรุปความพึงพอใจ ลูกค้าต่างประเทศ** ขั้น 1 **ข้อมูลหลักใบสรุป** | ☐ |
| 2 | SELECT ช่อง **ประจำเดือน** | สิงหาคม 2569 | แสดง **สิงหาคม 2569** | ☐ |
| 3 | CLICK ปุ่ม **ดึงแบบประเมินที่บันทึกผลแล้วของเดือนนี้** | — | toast **เพิ่มลูกค้า 8 ราย · ยังเหลือ 6 ราย (เกิน 8 — ทำใบสรุปเพิ่ม)** | ☐ |

### TC-C04 — ตารางหัวข้อ × ลูกค้า อ่านอย่างเดียว + ไฮไลต์คะแนนต่ำ
- group: สร้าง · ความสำคัญ: สูง · trace: BR-04 / BR-05 / DEC-13 / AC-03
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: กันยายน 2569
- ผ่านเมื่อ: คะแนนเป็นตัวเลข ช่องต่ำไฮไลต์ แก้ไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบสรุป** | — | drawer **ใบสรุปความพึงพอใจ ลูกค้าต่างประเทศ** ขั้น 1 **ข้อมูลหลักใบสรุป** | ☐ |
| 2 | SELECT ช่อง **ประจำเดือน** | กันยายน 2569 | แสดง **กันยายน 2569** | ☐ |
| 3 | CLICK ปุ่ม **ดึงแบบประเมินที่บันทึกผลแล้วของเดือนนี้** | — | ตารางมีแถวกลุ่ม **ด้านการสื่อสารและการตอบสนอง** **ด้านเอกสารและการดำเนินงาน** **ด้านความเป็นมืออาชีพ** + หัวข้อ **ความชัดเจนในการสื่อสาร** … **ความพึงพอใจในบริการ** (10 ข้อ) | ☐ |
| 4 | VERIFY ช่องในตาราง | — | ค่าเป็นตัวเลข **1–5** · ไม่มีช่องกรอก | ☐ |
| 5 | VERIFY ช่องคะแนน **1** หรือ **2** | — | พื้นสีเตือน · ท้ายตาราง **คะแนน 1–2 จำนวน 6 ช่อง** | ☐ |

### TC-C05 — ลูกค้ามีแบบประเมินหลายใบ ใช้ใบล่าสุด [AI-DEFAULT]
- group: สร้าง · ความสำคัญ: กลาง · trace: BR-02 / EC-03 / DEC-14 / AC-04
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: กันยายน 2569 · ลูกค้าตัวอย่าง ต่างประเทศ 03
- ผ่านเมื่อ: ใช้ใบ 28 ก.ย. 69

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบสรุป** | — | drawer **ใบสรุปความพึงพอใจ ลูกค้าต่างประเทศ** ขั้น 1 **ข้อมูลหลักใบสรุป** | ☐ |
| 2 | SELECT ช่อง **ประจำเดือน** | กันยายน 2569 | แสดง **กันยายน 2569** | ☐ |
| 3 | CLICK ปุ่ม **ดึงแบบประเมินที่บันทึกผลแล้วของเดือนนี้** | — | แถว **ลูกค้าตัวอย่าง ต่างประเทศ 03** **28 ก.ย. 69 · SEA-2569-0161 · มีหลายใบ ใช้ใบล่าสุด** | ☐ |
| 4 | TYPE → ช่อง **สรุปผลการประเมิน** | ทดสอบ | ตัวนับ **5/1000** | ☐ |
| 5 | CLICK ปุ่ม **ถัดไป** 2 ครั้ง | — | ขั้น 3 มีแถบ **ลูกค้า 1 รายมีแบบประเมินหลายใบในเดือนนี้ — ใช้ใบล่าสุด** | ☐ |

### TC-C06 — เปลี่ยนเดือนหลังดึงลูกค้า ล้างรายชื่อเดิม [AI-DEFAULT]
- group: สร้าง · ความสำคัญ: กลาง · trace: EC-05 / DEC-12 / AC-07
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: กันยายน → สิงหาคม 2569
- ผ่านเมื่อ: รายชื่อเดิมถูกล้าง + toast

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบสรุป** | — | drawer **ใบสรุปความพึงพอใจ ลูกค้าต่างประเทศ** ขั้น 1 **ข้อมูลหลักใบสรุป** | ☐ |
| 2 | SELECT ช่อง **ประจำเดือน** | กันยายน 2569 | แสดง **กันยายน 2569** | ☐ |
| 3 | CLICK ปุ่ม **ดึงแบบประเมินที่บันทึกผลแล้วของเดือนนี้** | — | 8 ราย | ☐ |
| 4 | SELECT ช่อง **ประจำเดือน** | สิงหาคม 2569 | toast **เปลี่ยนเดือนแล้ว — ล้างรายชื่อลูกค้าเดิม 8 ราย** · รายชื่อว่าง | ☐ |

### TC-C07 — แนบไฟล์ และกันชนิดไฟล์ไม่รองรับ
- group: สร้าง · ความสำคัญ: กลาง · trace: API-11 / DEC-11
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=สรุปคะแนน.xlsx · virus.exe
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: ไฟล์ทดสอบ
- ผ่านเมื่อ: แนบ xlsx ได้ exe ไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบสรุป** | — | drawer **ใบสรุปความพึงพอใจ ลูกค้าต่างประเทศ** ขั้น 1 **ข้อมูลหลักใบสรุป** | ☐ |
| 2 | SELECT ช่อง **ประจำเดือน** | กันยายน 2569 | แสดง **กันยายน 2569** | ☐ |
| 3 | SELECT ช่อง **เพิ่มลูกค้าทีละราย** | ลูกค้าตัวอย่าง ต่างประเทศ 01 | แถว 1 | ☐ |
| 4 | CLICK ปุ่ม **ถัดไป** | — | ขั้น 2 **เอกสารแนบ** | ☐ |
| 5 | UPLOAD → **คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)** | สรุปคะแนน.xlsx | แถวไฟล์ **สรุปคะแนน.xlsx** | ☐ |
| 6 | UPLOAD → **แนบไฟล์เพิ่ม** | virus.exe | toast **virus.exe — ชนิดไฟล์ไม่รองรับ** | ☐ |

### TC-C08 — ปิด wizard ที่กรอกค้างต้องยืนยันทิ้งข้อมูล
- group: สร้าง · ความสำคัญ: ต่ำ · trace: U8 / U25
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: —
- ผ่านเมื่อ: มี modal ยืนยัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบสรุป** | — | drawer **ใบสรุปความพึงพอใจ ลูกค้าต่างประเทศ** ขั้น 1 **ข้อมูลหลักใบสรุป** | ☐ |
| 2 | SELECT ช่อง **ประจำเดือน** | กันยายน 2569 | แสดง **กันยายน 2569** | ☐ |
| 3 | CLICK ปุ่ม **ยกเลิก** ท้าย drawer | — | modal **ทิ้งข้อมูลที่กรอกไว้?** | ☐ |
| 4 | CLICK ปุ่ม **ทิ้งข้อมูล** | — | drawer ปิด | ☐ |

### TC-V01 — กดถัดไปตอนว่าง
- group: ตรวจสอบข้อมูล · ความสำคัญ: สูง · trace: FN-01 / VR-01 / VR-02 / AC-05 (auto: e2e S7)
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: —
- ผ่านเมื่อ: อยู่ขั้น 1 + ช่องแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบสรุป** | — | drawer **ใบสรุปความพึงพอใจ ลูกค้าต่างประเทศ** ขั้น 1 **ข้อมูลหลักใบสรุป** | ☐ |
| 2 | CLICK ปุ่ม **ถัดไป** | — | toast **กรุณากรอกข้อมูลให้ครบถ้วน** · **กรุณาเลือกเดือน** · **เพิ่มลูกค้าที่ประเมินอย่างน้อย 1 ราย** | ☐ |

### TC-V02 — ตัวเลือกลูกค้าไม่แสดงลูกค้าที่อยู่ในใบแล้ว (กันซ้ำ)
- group: ตรวจสอบข้อมูล · ความสำคัญ: สูง · trace: VR-03 / BR-02 / DEC-14 / AC-06
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: กันยายน 2569
- ผ่านเมื่อ: ไม่มีตัวเลือกซ้ำ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบสรุป** | — | drawer **ใบสรุปความพึงพอใจ ลูกค้าต่างประเทศ** ขั้น 1 **ข้อมูลหลักใบสรุป** | ☐ |
| 2 | SELECT ช่อง **ประจำเดือน** | กันยายน 2569 | แสดง **กันยายน 2569** | ☐ |
| 3 | CLICK ปุ่ม **ดึงแบบประเมินที่บันทึกผลแล้วของเดือนนี้** | — | 8 ราย | ☐ |
| 4 | VERIFY ช่องเพิ่มลูกค้า | — | ข้อความ **ไม่มีลูกค้าเหลือ** (ลูกค้าที่อยู่ในใบแล้วไม่ถูกเสนอซ้ำ) | ☐ |

### TC-V03 — เพิ่มลูกค้าคนที่ 9 ถูกบล็อก [AI-DEFAULT]
- group: ตรวจสอบข้อมูล · ความสำคัญ: สูง · trace: VR-04 / BR-03 / DEC-05
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: สิงหาคม 2569
- ผ่านเมื่อ: บล็อก + toast

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบสรุป** | — | drawer **ใบสรุปความพึงพอใจ ลูกค้าต่างประเทศ** ขั้น 1 **ข้อมูลหลักใบสรุป** | ☐ |
| 2 | SELECT ช่อง **ประจำเดือน** | สิงหาคม 2569 | — | ☐ |
| 3 | CLICK ปุ่ม **ดึงแบบประเมินที่บันทึกผลแล้วของเดือนนี้** | — | 8 ราย | ☐ |
| 4 | SELECT ช่อง **เพิ่มลูกค้าทีละราย** | ลูกค้าที่เหลือรายแรก | toast **ใบสรุป 1 ใบมีลูกค้าได้สูงสุด 8 ราย — ทำใบสรุปเพิ่ม** · ยังคง 8 ราย | ☐ |

### TC-V04 — สรุปผล/ข้อเสนอแนะ จำกัด 1,000 ตัวอักษร
- group: ตรวจสอบข้อมูล · ความสำคัญ: กลาง · trace: VR-05 / EC-12
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: ข้อความ 1,000 ตัว
- ผ่านเมื่อ: ตัวนับตรง พิมพ์เกินไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบสรุป** | — | drawer **ใบสรุปความพึงพอใจ ลูกค้าต่างประเทศ** ขั้น 1 **ข้อมูลหลักใบสรุป** | ☐ |
| 2 | TYPE → ช่อง **สรุปผลการประเมิน** | ทดสอบ | ตัวนับ **5/1000** | ☐ |
| 3 | TYPE → ช่อง **สรุปผลการประเมิน** | ข้อความ 1,050 ตัวอักษร | รับได้ 1,000 ตัว · ตัวนับ **1000/1000** | ☐ |

### TC-V05 — ส่งโดยไม่มีสรุปผลการประเมิน [AI-DEFAULT]
- group: ตรวจสอบข้อมูล · ความสำคัญ: สูง · trace: VR-05 / BR-07 / AC-05
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: กันยายน 2569
- ผ่านเมื่อ: กลับขั้น 1 ช่องสรุปผลแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบสรุป** | — | drawer **ใบสรุปความพึงพอใจ ลูกค้าต่างประเทศ** ขั้น 1 **ข้อมูลหลักใบสรุป** | ☐ |
| 2 | SELECT ช่อง **ประจำเดือน** | กันยายน 2569 | แสดง **กันยายน 2569** | ☐ |
| 3 | CLICK ปุ่ม **ดึงแบบประเมินที่บันทึกผลแล้วของเดือนนี้** | — | 8 ราย | ☐ |
| 4 | CLICK ปุ่ม **ถัดไป** 2 ครั้ง | — | ขั้น 3 | ☐ |
| 5 | CLICK ปุ่ม **บันทึกและส่งอนุมัติ** | — | กลับขั้น 1 · **กรุณาเขียนสรุปผลการประเมิน** · toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |

### TC-S01 — บันทึกและส่งอนุมัติ ค่าเริ่มผู้รับทราบจาก DOA [AI-DEFAULT]
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: FN-04 / BR-08 / DEC-03 / AC-09
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: กันยายน 2569 + สรุปผล
- ผ่านเมื่อ: สถานะรออนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบสรุป** | — | drawer **ใบสรุปความพึงพอใจ ลูกค้าต่างประเทศ** ขั้น 1 **ข้อมูลหลักใบสรุป** | ☐ |
| 2 | SELECT ช่อง **ประจำเดือน** | กันยายน 2569 | แสดง **กันยายน 2569** | ☐ |
| 3 | CLICK ปุ่ม **ดึงแบบประเมินที่บันทึกผลแล้วของเดือนนี้** | — | 8 ราย | ☐ |
| 4 | TYPE → ช่อง **สรุปผลการประเมิน** | ทดสอบ | — | ☐ |
| 5 | CLICK ปุ่ม **ถัดไป** 2 ครั้ง | — | ขั้น 3 | ☐ |
| 6 | CLICK ปุ่ม **บันทึกและส่งอนุมัติ** | — | modal **ส่งอนุมัติ?** แถว **ผู้รับทราบและอนุมัติ** ค่าเริ่ม **ตัวอย่าง บริหารงาน** · **ค่าเริ่มต้นจากสายอนุมัติ (DOA) และผังองค์กร** | ☐ |
| 7 | VERIFY รายชื่อในช่องผู้พิจารณา | — | ไม่มี **สมมติ ใจดี** (ผู้สรุปเอง) | ☐ |
| 8 | CLICK ปุ่ม **ส่งอนุมัติ** | — | toast **ส่งอนุมัติแล้ว · SES-2569-0012** · สถานะ **รออนุมัติ** | ☐ |

### TC-S02 — ไม่เลือกผู้พิจารณา
- group: ส่งอนุมัติ · ความสำคัญ: กลาง · trace: VR-06
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: SES-2569-0010
- ผ่านเมื่อ: บล็อก + ข้อความ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary/view/R10` | — | drawer **SES-2569-0010** | ☐ |
| 2 | CLICK ปุ่ม **ส่งอนุมัติ** | — | modal **ส่งอนุมัติ?** | ☐ |
| 3 | CLICK ล้างค่าในช่องผู้พิจารณา | — | ช่องว่าง | ☐ |
| 4 | CLICK ปุ่ม **ส่งอนุมัติ** ใน modal | — | **กรุณาเลือกผู้พิจารณา** · ยังอยู่ใน modal | ☐ |

### TC-S03 — ร่างที่แบบประเมินต้นทางถูกยกเลิก ส่งไม่ได้ [AI-DEFAULT]
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: BR-06 / EC-04 / AC-08 / DEC-04
- actor (role): Sales Admin Supervisor
- Setup: role=other Sales Admin Supervisor (__QA__.setMe('E03')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: SES-2569-0009
- ผ่านเมื่อ: แบนเนอร์ + บล็อกส่ง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary/view/R9` | — | แบนเนอร์ **แบบประเมินของ ลูกค้าตัวอย่าง ต่างประเทศ 09 ถูกยกเลิกแล้ว — แก้ไขแล้วเอาคอลัมน์นั้นออกก่อนส่ง** | ☐ |
| 2 | CLICK ปุ่ม **ส่งอนุมัติ** | — | toast **มีแบบประเมินที่ถูกยกเลิก — แก้ไขแล้วเอาคอลัมน์นั้นออกก่อนส่ง** · ไม่มี modal | ☐ |

### TC-S04 — ส่งร่างที่ยังไม่มีสรุปผลจากหน้าดู
- group: ส่งอนุมัติ · ความสำคัญ: กลาง · trace: BR-07 / VR-05
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: SES-2569-0011
- ผ่านเมื่อ: เปิด wizard ให้แก้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary/view/R11` | — | drawer **SES-2569-0011** | ☐ |
| 2 | CLICK ปุ่ม **ส่งอนุมัติ** | — | toast **กรอกลูกค้าและสรุปผลการประเมินให้ครบก่อนส่ง** · เปิด wizard **แก้ไขเอกสาร** | ☐ |

### TC-S05 — จำนวนแถวผู้พิจารณาตามขั้น DOA (dynamic) [AI-DEFAULT]
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: BR-12 / DEC-03 / EC-11 (auto: e2e S8)
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: __QA__.doa.push() 5 ครั้ง
- ผ่านเมื่อ: แถว = 6

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary/view/R10` | — | drawer **SES-2569-0010** | ☐ |
| 2 | PRESS console `__QA__.doa.push()` 5 ครั้ง | — | DOA 6 ขั้น | ☐ |
| 3 | CLICK ปุ่ม **ส่งอนุมัติ** | — | modal มีแถวผู้พิจารณา 6 แถว | ☐ |

### TC-S06 — ส่งไม่สำเร็จ สถานะไม่เปลี่ยน
- group: ส่งอนุมัติ · ความสำคัญ: ต่ำ · trace: EC-09 (auto: e2e S9)
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: __QA__.sim('error')
- ผ่านเมื่อ: toast error ยังเป็นร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary/view/R10` | — | — | ☐ |
| 2 | CLICK ปุ่ม **ส่งอนุมัติ** | — | modal | ☐ |
| 3 | PRESS console `__QA__.sim('error')` | — | — | ☐ |
| 4 | CLICK ปุ่ม **ส่งอนุมัติ** ใน modal | — | toast **ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง** · สถานะ **ร่าง** | ☐ |

### TC-A01 — รับทราบและอนุมัติ + แจ้งคะแนนต่ำ [AI-DEFAULT]
- group: อนุมัติ · ความสำคัญ: สูง · trace: FN-05 / BR-13 / DEC-01 / AC-10
- actor (role): Managing Director
- Setup: role=approver Managing Director (__QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: SES-2569-0008
- ผ่านเมื่อ: อนุมัติแล้ว + แจ้งฝ่ายขาย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary` | — | badge **รอฉันพิจารณา 2** | ☐ |
| 2 | OPEN `#/csat-overseas-summary/view/R8` | — | ปุ่ม **รับทราบและอนุมัติ** · **ไม่อนุมัติ** | ☐ |
| 3 | CLICK ปุ่ม **รับทราบและอนุมัติ** | — | modal **รับทราบและอนุมัติใบสรุปนี้?** | ☐ |
| 4 | CLICK ปุ่ม **รับทราบและอนุมัติ** ใน modal | — | toast **อนุมัติแล้ว · SES-2569-0008 · แจ้งฝ่ายขาย: คะแนนต่ำ 4 ช่อง** · สถานะ **อนุมัติแล้ว** | ☐ |

### TC-A02 — ไม่อนุมัติต้องมีเหตุผล แล้วกลับเป็นร่างเลขเดิม [AI-DEFAULT]
- group: อนุมัติ · ความสำคัญ: สูง · trace: FN-06 / BR-09 / VR-07 / DEC-08 / AC-11
- actor (role): Managing Director
- Setup: role=approver Managing Director (__QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: SES-2569-0007
- ผ่านเมื่อ: กลับร่างเลขเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary/view/R7` | — | — | ☐ |
| 2 | CLICK ปุ่ม **ไม่อนุมัติ** | — | modal **ไม่อนุมัติใบสรุปนี้?** | ☐ |
| 3 | CLICK ปุ่ม **ไม่อนุมัติ** ใน modal | — | **กรุณาระบุเหตุผล** | ☐ |
| 4 | TYPE → ช่อง **เหตุผล** | ขอข้อเสนอแนะเพิ่มเติม | — | ☐ |
| 5 | CLICK ปุ่ม **ไม่อนุมัติ** ใน modal | — | toast **ไม่อนุมัติ — กลับเป็นร่าง · SES-2569-0007** · สถานะ **ร่าง** | ☐ |

### TC-A03 — ร่างที่ถูกไม่อนุมัติแสดงเหตุผล และแก้ไขได้
- group: อนุมัติ · ความสำคัญ: กลาง · trace: BR-09 / AC-11
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: SES-2569-0011
- ผ่านเมื่อ: แบนเนอร์เหตุผล + ปุ่มแก้ไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary/view/R11` | — | แบนเนอร์ **ไม่อนุมัติ — กลับเป็นร่าง (เลขเดิม): ลูกค้าไม่ครบ — ขาดลูกค้าที่ตอบแบบประเมินปลายเดือน** | ☐ |
| 2 | CLICK ปุ่ม **แก้ไข** | — | wizard **แก้ไขเอกสาร** **SES-2569-0011** | ☐ |

### TC-A04 — แท็บลายเซ็น / อนุมัติ แสดงลำดับ
- group: อนุมัติ · ความสำคัญ: กลาง · trace: U13 / BR-12
- actor (role): Managing Director
- Setup: role=approver Managing Director (__QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: SES-2569-0001
- ผ่านเมื่อ: timeline ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary/view/R1` | — | — | ☐ |
| 2 | CLICK แท็บ **ลายเซ็น / อนุมัติ** | — | **ส่งอนุมัติ (ผู้สรุปผลการประเมิน)** → **ขั้น 1 · ผู้รับทราบและอนุมัติ** pill **รับทราบและอนุมัติ** → **ผลลัพธ์** **อนุมัติแล้ว** | ☐ |

### TC-X01 — เจ้าของยกเลิกใบรออนุมัติ [AI-DEFAULT]
- group: ยกเลิก · ความสำคัญ: สูง · trace: FN-06 / FN-08 / DEC-08 / AC-12
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: SES-2569-0007
- ผ่านเมื่อ: สถานะยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary/view/R7` | — | ปุ่ม **ยกเลิกเอกสาร** | ☐ |
| 2 | CLICK ปุ่ม **ยกเลิกเอกสาร** | — | modal **ยกเลิกเอกสาร?** | ☐ |
| 3 | TYPE → ช่อง **เหตุผล** | ไม่ใช้เอกสารนี้แล้ว | — | ☐ |
| 4 | CLICK ปุ่ม **ยกเลิกเอกสาร** ใน modal | — | toast **ยกเลิกเอกสารแล้ว · SES-2569-0007** · สถานะ **ยกเลิก** | ☐ |

### TC-X02 — ใบอนุมัติแล้วยกเลิก/แก้ไขไม่ได้
- group: ยกเลิก · ความสำคัญ: กลาง · trace: TC-D06 / 05 §5.2
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: SES-2569-0001
- ผ่านเมื่อ: เมนูไม่มียกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ⋮ ที่แถว **SES-2569-0001** | — | เมนูมีเพียง **ดูรายละเอียด** **พิมพ์** | ☐ |
| 2 | OPEN `#/csat-overseas-summary/view/R1` | — | ท้าย drawer **อนุมัติแล้ว ล็อกแก้ไข** | ☐ |

### TC-P01 — ผู้อนุมัติไม่เห็นร่างของคนอื่น [AI-DEFAULT]
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D01 / BR-11 / DEC-09 (auto: e2e S3)
- actor (role): Managing Director
- Setup: role=approver Managing Director (__QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 8 แถว ไม่มีร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary` | — | badge **8 รายการ** · ไม่มี **SES-2569-0009** **SES-2569-0010** **SES-2569-0011** | ☐ |

### TC-P02 — เปิด route ใบที่ไม่มีสิทธิ์
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D02 (auto: e2e S6)
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: R9 (ร่างของ E03)
- ผ่านเมื่อ: ไม่เปิด drawer

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary/view/R9` | — | อยู่หน้ารายการ ไม่มี drawer เปิด | ☐ |

### TC-P03 — เจ้าของอนุมัติใบตัวเองไม่ได้
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D03 / SoD
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: SES-2569-0008
- ผ่านเมื่อ: ไม่มีปุ่มอนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary/view/R8` | — | ไม่มีปุ่ม **รับทราบและอนุมัติ** · มีเพียง **ยกเลิกเอกสาร** | ☐ |

### TC-P04 — ผู้อนุมัติแก้ไขร่างของผู้สรุปไม่ได้
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D04
- actor (role): Managing Director
- Setup: role=approver Managing Director (__QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: SES-2569-0008
- ผ่านเมื่อ: ไม่มีปุ่มแก้ไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary/view/R8` | — | ไม่มีปุ่ม **แก้ไข** | ☐ |

### TC-P05 — ผู้จัดการฝ่ายขายเห็นทุกใบ [AI-DEFAULT]
- group: สิทธิ์ · ความสำคัญ: สูง · trace: AC-14 / FN-09 / DEC-09
- actor (role): ผู้จัดการฝ่ายขาย
- Setup: role=admin ผู้จัดการฝ่ายขาย (__QA__.setMe('E05')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 11 แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary` | — | badge **11 รายการ** รวมร่าง **SES-2569-0009** | ☐ |

### TC-P06 — ผู้ใช้อื่นยกเลิกใบของคนอื่นไม่ได้
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: TC-D05
- actor (role): Sales Admin Supervisor
- Setup: role=other Sales Admin Supervisor (__QA__.setMe('E03')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่เห็นใบของ E01

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary` | — | badge **3 รายการ** · ไม่มี **SES-2569-0007** (จึงไม่มีเมนูยกเลิก) | ☐ |

### TC-D01 — PDF 2 หน้า 8 คอลัมน์ + คำตัดสินรับทราบและอนุมัติ [AI-DEFAULT]
- group: PDF · ความสำคัญ: สูง · trace: FN-07 / AC-13 / BR-12 / DEC-05 / DEC-07 / DEC-15
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: SES-2569-0001
- ผ่านเมื่อ: โครงตรง print-spec

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary/view/R1` | — | — | ☐ |
| 2 | CLICK แท็บ **PDF Preview** | — | หน้า 1 ตาราง 2 ชุด × 4 คอลัมน์ หัวตารางซ้ำ (แถวกลุ่ม 3 + หัวข้อ 10) · **มีต่อหน้าถัดไป** · **หน้า 1/2** | ☐ |
| 3 | VERIFY หน้า 2 | — | **สรุปผลการประเมิน** **ข้อเสนอแนะ** · ช่องลงชื่อ **ผู้สรุปผลการประเมิน** + **ผู้รับทราบและอนุมัติ** ☑ **รับทราบและอนุมัติ** · **หน้า 2/2** | ☐ |

### TC-D02 — PDF ร่างมีป้ายร่าง + ประจำเดือน
- group: PDF · ความสำคัญ: กลาง · trace: DEC-06 / DEC-12
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: SES-2569-0010
- ผ่านเมื่อ: footer มีร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary/view/R10` | — | — | ☐ |
| 2 | CLICK แท็บ **PDF Preview** | — | **ประจำเดือน ตุลาคม 2569** · footer **เลขที่ SES-2569-0010 · ร่าง** | ☐ |

### TC-D03 — PDF ช่องลงชื่อตาม DOA 6 ขั้น
- group: PDF · ความสำคัญ: กลาง · trace: EC-11 / BR-12
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: __QA__.doa.push() 5 ครั้ง แล้วส่ง
- ผ่านเมื่อ: 7 ช่อง 4+3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary/view/R10` | — | — | ☐ |
| 2 | PRESS console `__QA__.doa.push()` 5 ครั้ง | — | — | ☐ |
| 3 | CLICK ปุ่ม **ส่งอนุมัติ** แล้ว **ส่งอนุมัติ** ใน modal | — | สถานะ **รออนุมัติ** | ☐ |
| 4 | CLICK แท็บ **PDF Preview** | — | ช่องลงชื่อ 7 ช่อง 2 แถว (4 + 3) | ☐ |

### TC-E01 — แบบเอกสารปิดใช้ สร้างไม่ได้
- group: ขอบเขต · ความสำคัญ: กลาง · trace: EC-10 / F-DOCCFG
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: __QA__.setDocActive(false)
- ผ่านเมื่อ: ปุ่มสร้าง disabled

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console `__QA__.setDocActive(false)` | — | แถบ **แบบเอกสารนี้ยังไม่เปิดใช้งาน — สร้างใหม่ไม่ได้** · ปุ่ม **สร้างใบสรุป** กดไม่ได้ | ☐ |

### TC-E02 — ข้อมูลถูกแก้โดยผู้อื่น (stale)
- group: ขอบเขต · ความสำคัญ: ต่ำ · trace: EC-09
- actor (role): Sales Administrative Manager
- Setup: role=owner Sales Administrative Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: __QA__.sim('stale')
- ผ่านเมื่อ: toast รีเฟรช

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary/view/R10` | — | — | ☐ |
| 2 | CLICK ปุ่ม **ส่งอนุมัติ** | — | modal | ☐ |
| 3 | PRESS console `__QA__.sim('stale')` | — | — | ☐ |
| 4 | CLICK ปุ่ม **ส่งอนุมัติ** ใน modal | — | toast **ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่** | ☐ |

### TC-E03 — อนุมัติแล้วไม่เปลี่ยนค่า/ไม่ส่งต่อ · ใบเดิมใช้ snapshot [AI-DEFAULT]
- group: ขอบเขต · ความสำคัญ: ต่ำ · trace: DEC-01 / DEC-02 / EC-07 / EC-08 / BR-14
- actor (role): Managing Director
- Setup: role=approver Managing Director (__QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-overseas-summary`
- ชุดข้อมูล: SES-2569-0008
- ผ่านเมื่อ: ไม่มีการส่งต่อ ค่าในใบคงเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-overseas-summary/view/R8` | — | — | ☐ |
| 2 | CLICK ปุ่ม **รับทราบและอนุมัติ** แล้วยืนยัน | — | toast **อนุมัติแล้ว · SES-2569-0008 …** ไม่มีข้อความส่งต่อระบบอื่น | ☐ |
| 3 | VERIFY ตารางในแท็บ **รายละเอียด** | — | คะแนนในตารางเท่าเดิมก่อนอนุมัติ (snapshot) · ระบบจริง: เปลี่ยน DOA/config หลังส่งไม่กระทบใบนี้ | ☐ |

## วิธีที่ agent รัน (Run protocol)
1. เปิด feature.html ใหม่ทุกเคส (seed กลับค่าเริ่ม) · 2. ตั้ง persona ตาม Setup ด้วย `__QA__.setMe()` · 3. ทำทีละ step บันทึก ☐ → ✅/❌ · 4. fail = แนบภาพหน้าจอ + ข้อความที่เห็นจริง

## Coverage Audit
| หมวด | covered / total |
|---|---|
| AC | 14 / 14 |
| BR | 15 / 15 |
| VR | 7 / 7 |
| EC | 11 / 12 |
| Deny TC-D | 6 / 6 |
| DEC | 15 / 15 |
| XT / events | 5 / 5 |

- **Manifest cross-check (FRD 06 §6.1–6.2): ✅**
### ข้าม (พร้อมเหตุผล)
- EC-01 (เดือนที่ไม่มีแบบประเมิน) — seed ทุกเดือนมีแบบประเมิน · ทดสอบระดับ API-05 ตอน dev (คืนรายการว่าง → VR-02)

## Result Report (schema)
```json
{ "feature_id": "F-TMP-007", "run_at": "<iso datetime>", "results": [ { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" } ], "summary": { "total": 0, "pass": 0, "fail": 0, "blocked": 0 } }
```

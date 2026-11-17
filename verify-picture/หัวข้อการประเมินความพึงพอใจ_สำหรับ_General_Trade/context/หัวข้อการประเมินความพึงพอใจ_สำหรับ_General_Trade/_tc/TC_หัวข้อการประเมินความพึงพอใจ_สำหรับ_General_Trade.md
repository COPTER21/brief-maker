# AI Test Cases — F-TMP-002 หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade

ชุดทดสอบสำหรับ AI agent (browser-use/vision) บน prototype `feature.html` · ข้อมูลทั้งหมดเป็นข้อมูลสมมติ · เคสที่ derive จากมติ AI-DEFAULT ติด `[AI-DEFAULT]` (ผล fail อาจแปลว่าค่า default ผิด ไม่ใช่โค้ดผิด)

## Meta
| Field | Value |
|---|---|
| Feature ID | F-TMP-002 (ชั่วคราว) |
| ชื่อ | หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade (doc CSM · FM-SAL-11) |
| เวอร์ชัน | 1.0 (2026-10-10) |
| App entry | feature.html |
| Routes | `#/csat-gt` · `#/csat-gt/create` · `#/csat-gt/edit/:id` · `#/csat-gt/view/:id` |
| ที่มา | FRD_F-TMP-002_Pack v1.0 · BRD-SAL-CSM-001 · feature.html (html-generator-v9.4 Q-form) · DECISIONS.lock 20 DEC |
| จำนวนเคส | 64 |
| หมายเหตุ | anchor อ้างจากข้อความใน feature.html · verify_anchors.py ยังไม่รัน (NO-BROWSER) |

## Coverage
| group | เคส | สูง/กลาง/ต่ำ |
|---|---|---|
| รายการ | 10 | 1/7/2 |
| สร้าง | 8 | 4/3/1 |
| ตรวจสอบข้อมูล | 7 | 2/4/1 |
| คำนวณ | 6 | 4/2/0 |
| ลูกค้า | 3 | 2/1/0 |
| ส่งอนุมัติ | 6 | 3/2/1 |
| อนุมัติ | 5 | 3/2/0 |
| ยกเลิก | 4 | 1/3/0 |
| สิทธิ์ | 6 | 5/1/0 |
| PDF | 4 | 1/3/0 |
| ขอบเขต | 5 | 0/2/3 |

## Coverage Ledger
### Acceptance (06_TESTS)
| item | cases |
|---|---|
| AC-01 | TC-C01 |
| AC-02 | TC-K01 |
| AC-03 | TC-K03 |
| AC-04 | TC-K05 |
| AC-05 | TC-V01 |
| AC-06 | TC-V02 |
| AC-07 | TC-U02 |
| AC-08 | TC-U03 |
| AC-09 | TC-S01 |
| AC-10 | TC-A01 |
| AC-11 | TC-A02 |
| AC-12 | TC-X01 |
| AC-13 | TC-D01 |
| AC-14 | TC-P05 |
### Business Rules (05_RULES)
| rule | cases |
|---|---|
| BR-01 | TC-K01 |
| BR-02 | TC-K01 |
| BR-03 | TC-K01, TC-K02 |
| BR-04 | TC-K03 |
| BR-05 | TC-C04, TC-K04 |
| BR-06 | TC-U03 |
| BR-07 | TC-K06 |
| BR-08 | TC-S04 |
| BR-09 | TC-A02 |
| BR-10 | TC-C01 |
| BR-11 | TC-L01, TC-P01 |
| BR-12 | TC-D01, TC-D04 |
| BR-13 | TC-A05 |
| BR-14 | TC-D01 |
| BR-15 | TC-E04 |
| BR-16 | TC-L10 |
| BR-17 | TC-D01 |
### Validation
| VR | cases |
|---|---|
| VR-01 | TC-V01 |
| VR-02 | TC-V02, TC-V03, TC-V04 |
| VR-03 | TC-V01, TC-V05 |
| VR-04 | TC-V01, TC-V06, TC-V07 |
| VR-05 | TC-S02, TC-S03 |
| VR-06 | TC-A03 |
### Edge Cases
| EC | cases |
|---|---|
| EC-01 | TC-K05, TC-E04 |
| EC-02 | TC-V05, TC-E04 |
| EC-03 | TC-V02, TC-S01, TC-S04 |
| EC-04 | TC-V02, TC-U03 |
| EC-05 | TC-K06 |
| EC-06 | TC-K06, TC-E05 |
| EC-07 | TC-K06, TC-E05 |
| EC-08 | TC-D01, TC-E05 |
| EC-09 | TC-K06, TC-S05, TC-S06 |
| EC-10 | TC-D01, TC-E01 |
| EC-11 | TC-A02, TC-X02, TC-D04 |
### Permission / Deny
| cell | cases |
|---|---|
| TC-D01 | TC-P01 |
| TC-D02 | TC-P02 |
| TC-D03 | TC-P03 |
| TC-D04 | TC-P04 |
| TC-D05 | TC-P06 |
| TC-D06 | TC-X04 |
### Scope Lock (DEC)
| DEC | cases |
|---|---|
| DEC-01 | TC-E04 |
| DEC-02 | TC-E04 |
| DEC-03 | TC-S01, TC-S04 |
| DEC-04 | TC-V02 |
| DEC-05 | TC-K06 |
| DEC-06 | TC-K06 |
| DEC-07 | TC-K06 |
| DEC-08 | TC-D01 |
| DEC-09 | TC-K06 |
| DEC-10 | TC-D01 |
| DEC-11 | TC-A02, TC-X02 |
| DEC-12 | TC-L01, TC-P01, TC-P05 |
| DEC-13 | TC-E01 |
| DEC-14 | TC-L09, TC-L10, TC-C07 |
| DEC-15 | TC-D01 |
| DEC-16 | TC-K01 |
| DEC-17 | TC-K02 |
| DEC-18 | TC-K01 |
| DEC-19 | TC-K03 |
| DEC-20 | TC-U03 |
### Cross-Module / Events (XT)
| item | cases |
|---|---|
| csm_cancelled | TC-X01 (ต้อง simulate — เห็นผลฝั่งต้นทาง) |
| csm_low_csat | TC-A05 |
| csm.approved ไม่ยิง (DEC-02) | TC-E04 |
| F-DOCCFG status | TC-E01 |

## Data Sets
| ชุด | ฟิลด์ | ค่า |
|---|---|---|
| A | ประจำเดือน · คะแนนด้านคุณภาพ · ลูกค้า | กันยายน 2569 · 6,4,2,0,0 / 5,5,2,0,0 / 4,6,1,1,0 / 5,4,3,0,0 · ดึงลูกค้าถึงเกณฑ์ |
| B | คะแนนต่ำ | แถว 1 = 0,0,0,0,5 (โดยรวม 20.00%) |
| C (ผิด) | จำนวน | -1 · 2.5 · ก · 0 ทุกช่อง |
### ไฟล์ทดสอบ (Files)
- สรุปแบบสำรวจ.xlsx (50 KB) · virus.exe (ชนิดไม่รองรับ)

## Test Cases
### TC-L01 — รายการแสดงเฉพาะใบที่มีสิทธิ์ (owner) [AI-DEFAULT]
- group: รายการ · ความสำคัญ: สูง · trace: FN-10 / BR-11 / DEC-12 (auto: e2e S2)
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 7 แถว ไม่เห็นร่างของคนอื่น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หัว **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** + badge **7 รายการ** | ☐ |
| 2 | VERIFY หัวคอลัมน์ | — | **เลขที่** **ประจำเดือน** **ผู้จัดทำ** **หน่วยงาน** **ลูกค้าที่ประเมิน** **% โดยรวม** **ผลการแปลผล** **สถานะเอกสาร** **ลายเซ็น** | ☐ |
| 3 | VERIFY ไม่มีแถว CSM-2569-0009 | — | ใบร่างของคนอื่นไม่อยู่ในรายการ (ไม่เห็นร่างของคนอื่น) | ☐ |

### TC-L02 — ไม่มีแถบการ์ดสถิติ ตัวเลขอยู่ใน badge
- group: รายการ · ความสำคัญ: กลาง · trace: U1 / U22
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: badge ≤ 3 ไม่มีการ์ดตัวเลข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | ใต้หัวเห็น badge **7 รายการ** และ **รออนุมัติ 1** | ☐ |
| 2 | VERIFY พื้นที่ระหว่างหัวกับตาราง | — | ไม่มีการ์ดสถิติ ถัดไปคือแถบค้นหา | ☐ |

### TC-L03 — ค้นหาด้วยเลขที่
- group: รายการ · ความสำคัญ: กลาง · trace: API-01 q
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: q=0008
- ผ่านเมื่อ: เหลือ 1 แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา **ค้นหาเลขที่ / ผู้จัดทำ / เดือน / ลูกค้า** | 0008 | เหลือแถว **CSM-2569-0008** | ☐ |
| 2 | VERIFY ท้ายตาราง | — | **1 – 1 จาก 1 รายการ** | ☐ |

### TC-L04 — ค้นหาไม่พบ แสดง empty state แล้วรีเซ็ต
- group: รายการ · ความสำคัญ: กลาง · trace: U23
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: q=ไม่มีจริง
- ผ่านเมื่อ: เห็นข้อความไม่พบ แล้วกลับครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา | ไม่มีจริง | ตารางแสดง **ไม่พบรายการที่ค้นหา** | ☐ |
| 2 | CLICK ปุ่ม **รีเซ็ต** | — | ช่องค้นหาว่าง ตารางกลับ 7 แถว | ☐ |

### TC-L05 — กรองสถานะรออนุมัติ
- group: รายการ · ความสำคัญ: กลาง · trace: API-01 status
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เหลือ CSM-2569-0008

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่องกรอง **ทุกสถานะ** | — | ตัวเลือก **ร่าง** **รออนุมัติ** **อนุมัติแล้ว** **ยกเลิก** | ☐ |
| 2 | SELECT **รออนุมัติ** | — | เหลือ **CSM-2569-0008** pill **รออนุมัติ** | ☐ |

### TC-L06 — กรองตามเดือน
- group: รายการ · ความสำคัญ: กลาง · trace: API-01 period
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: กรกฎาคม 2569
- ผ่านเมื่อ: เหลือ CSM-2569-0003

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่องกรอง **ทุกเดือน** | — | เห็น **กรกฎาคม 2569** | ☐ |
| 2 | SELECT **กรกฎาคม 2569** | — | เหลือ **CSM-2569-0003** **85.83%** pill **ลูกค้ามีความพึงพอใจสูง** | ☐ |

### TC-L07 — เรียงตาม % โดยรวม
- group: รายการ · ความสำคัญ: ต่ำ · trace: sort
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เรียงได้ทั้งสองทาง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK หัวคอลัมน์ **% โดยรวม** | — | แถวแรกเป็นใบที่ไม่มี % หรือต่ำสุด **57.29%** | ☐ |
| 2 | CLICK หัวคอลัมน์ **% โดยรวม** อีกครั้ง | — | เรียงกลับจากมากไปน้อย | ☐ |

### TC-L08 — pagination และจำนวนต่อหน้า
- group: รายการ · ความสำคัญ: ต่ำ · trace: U6
- actor (role): Sales admin
- Setup: role=admin Sales admin (__QA__.setMe('E05')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ค่าเริ่ม 25 เปลี่ยนเป็น 10 ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ท้ายตาราง | — | **แสดงต่อหน้า** 25 · **1 – 11 จาก 11 รายการ** | ☐ |
| 2 | SELECT แสดงต่อหน้า = 10 | 10 | **1 – 10 จาก 11 รายการ** | ☐ |
| 3 | CLICK ปุ่มหน้า 2 | — | **11 – 11 จาก 11 รายการ** | ☐ |

### TC-L09 — ส่งออก CSV
- group: รายการ · ความสำคัญ: กลาง · trace: API-10 / DEC-14
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไฟล์ดาวน์โหลด + toast

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งออก CSV** | — | toast **ส่งออก 7 รายการ** | ☐ |

### TC-L10 — เมนู ⋮ ไม่มีทำซ้ำ [AI-DEFAULT]
- group: รายการ · ความสำคัญ: กลาง · trace: U5 / DEC-14 · BR-16
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เมนูถูกต้อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ⋮ ท้ายแถว CSM-2569-0010 | — | เมนู **ดูรายละเอียด** **แก้ไข** **พิมพ์** **ยกเลิกเอกสาร** | ☐ |
| 2 | VERIFY รายการเมนู | — | ไม่มีเมนูทำซ้ำ (DEC-14) | ☐ |

### TC-C01 — สร้างแบบสรุปครบ บันทึกแบบร่าง (happy)
- group: สร้าง · ความสำคัญ: สูง · trace: S-01 S-02 S-04 · FN-01..03 · AC-01 · BR-10
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: A
- ผ่านเมื่อ: ได้ใบร่าง CSM-2569-0012

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | SELECT ช่อง **ประจำเดือน** | กันยายน 2569 | การ์ดสรุปแสดง **กันยายน 2569** | ☐ |
| 4 | TYPE ตาราง **1) ด้านคุณภาพสินค้า/บริการ** แถว 1–4 | A | รวมแต่ละแถว 12 · แถวรวม 20 19 8 1 0 · 48 · **86.67%** | ☐ |
| 5 | CLICK ปุ่ม **ดึงลูกค้าที่สั่งซื้อถึงเกณฑ์ในเดือนนี้** | — | แถวลูกค้าเพิ่ม · toast ขึ้นต้น **เพิ่มลูกค้า** | ☐ |
| 6 | CLICK ปุ่ม **ถัดไป** | — | ขั้น **แนบเอกสารประกอบ (ถ้ามี)** | ☐ |
| 7 | CLICK ปุ่ม **ถัดไป** | — | ขั้น **ตรวจสอบและยืนยัน** มี **สรุปผลการประเมิน** **รายชื่อลูกค้า** | ☐ |
| 8 | CLICK ปุ่ม **บันทึกแบบร่าง** | — | ปุ่มแสดง **กำลังบันทึก…** แล้ว drawer ปิด | ☐ |
| 9 | WAIT จน toast ปรากฏ | — | toast **บันทึกร่างแล้ว · CSM-2569-0012** | ☐ |
| 10 | VERIFY แถวบนสุด | — | **CSM-2569-0012** pill **ร่าง** | ☐ |

### TC-C02 — บันทึกและส่งอนุมัติต่อเนื่อง
- group: สร้าง · ความสำคัญ: สูง · trace: FN-03 FN-05 · S-06
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: A
- ผ่านเมื่อ: เปิดหน้าต่างส่งอนุมัติต่อทันที

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | SELECT ช่อง **ประจำเดือน** | กันยายน 2569 | — | ☐ |
| 4 | TYPE ตารางคุณภาพแถว 1 | 6,4,2,0,0 | **86.67%** | ☐ |
| 5 | SELECT แถวลูกค้า 1 ช่อง **ค้นหาลูกค้า GT** | ร้านค้าตัวอย่าง GT-01 | แสดง **สั่งซื้อ** n **ครั้ง** | ☐ |
| 6 | CLICK **ถัดไป** 2 ครั้ง | — | ขั้น **ตรวจสอบและยืนยัน** | ☐ |
| 7 | CLICK ปุ่ม **บันทึกและส่งอนุมัติ** | — | หน้าต่าง **ส่งอนุมัติ?** แถว **ผู้อำนวยการสายงานการขาย** | ☐ |

### TC-C03 — คำนวณสดไม่ทำให้ช่องหลุด focus
- group: สร้าง · ความสำคัญ: กลาง · trace: Rule #107
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: พิมพ์ต่อเนื่องได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | TYPE ช่องแรกตารางคุณภาพทีละตัว | 1 แล้ว 2 | เคอร์เซอร์ค้างในช่อง ค่า 12 · การ์ดสรุป **โดยรวม** **100.00%** | ☐ |

### TC-C04 — การ์ดสรุปแปลผลตามช่วง [AI-DEFAULT]
- group: สร้าง · ความสำคัญ: สูง · trace: BR-05 · S-03
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: B
- ผ่านเมื่อ: ข้อความแปลผลถูกช่วง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | TYPE ตารางคุณภาพแถว 1 | B | **20.00%** ข้อความ **ลูกค้าอาจมีความไม่พึงพอใจ** | ☐ |
| 4 | TYPE แก้แถว 1 | 5,0,0,0,0 | **100.00%** ข้อความ **ลูกค้ามีความพึงพอใจสูง** | ☐ |

### TC-C05 — แก้ไขร่างของตัวเอง
- group: สร้าง · ความสำคัญ: สูง · trace: API-04 · U15
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=CSM-2569-0011 ร่าง · files=—
- Start: OPEN `#/csat-gt/view/R11`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บันทึกได้เลขเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt/view/R11` | — | drawer **CSM-2569-0011** pill **ร่าง** | ☐ |
| 2 | CLICK ปุ่ม **แก้ไข** | — | drawer กว้าง หัว **CSM-2569-0011** ค่าเดิมครบ เดือน **เมษายน 2569** | ☐ |
| 3 | CLICK **ถัดไป** 2 ครั้ง แล้ว CLICK **บันทึกการแก้ไข** | — | toast **บันทึกร่างแล้ว · CSM-2569-0011** | ☐ |

### TC-C06 — ปิดฟอร์มที่กรอกค้าง ถามก่อนทิ้ง
- group: สร้าง · ความสำคัญ: กลาง · trace: UX dirty-check
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ยืนยันก่อนทิ้ง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | TYPE ช่องแรกตารางคุณภาพ | 3 | ค่าแสดง | ☐ |
| 4 | PRESS Esc | — | หน้าต่าง **ทิ้งข้อมูลที่กรอกไว้?** | ☐ |
| 5 | CLICK **กลับไปกรอกต่อ** | — | ฟอร์มยังอยู่ ค่าเดิม | ☐ |
| 6 | PRESS Esc แล้ว CLICK **ทิ้งข้อมูล** | — | drawer ปิด | ☐ |

### TC-C07 — แนบไฟล์และลบไฟล์
- group: สร้าง · ความสำคัญ: กลาง · trace: DEC-14 · API-11
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=สรุปแบบสำรวจ.xlsx (50 KB)
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: A
- ผ่านเมื่อ: แนบ/ลบได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | SELECT เดือน + TYPE คะแนน 1 แถว + SELECT ลูกค้า 1 ราย แล้ว CLICK **ถัดไป** | A | ขั้น **แนบเอกสารประกอบ (ถ้ามี)** | ☐ |
| 4 | UPLOAD ผ่าน **คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)** | สรุปแบบสำรวจ.xlsx | แถวไฟล์ **สรุปแบบสำรวจ.xlsx** | ☐ |
| 5 | CLICK ไอคอนถังขยะ **ลบไฟล์** | — | ไฟล์หาย | ☐ |

### TC-C08 — แนบไฟล์ชนิดไม่รองรับ (negative)
- group: สร้าง · ความสำคัญ: ต่ำ · trace: file_policy
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=virus.exe
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แนบไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | UPLOAD ในขั้นเอกสารแนบ | virus.exe | toast **virus.exe — ชนิดไฟล์ไม่รองรับ** | ☐ |

### TC-V01 — กดถัดไปตอนว่าง บล็อก (negative)
- group: ตรวจสอบข้อมูล · ความสำคัญ: สูง · trace: VR-01 VR-03 VR-04 · AC-05 (auto: e2e S7)
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: อยู่ขั้น 1 + ช่องแดง + toast

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | CLICK ปุ่ม **ถัดไป** | — | toast **กรุณากรอกข้อมูลให้ครบถ้วน** · **กรุณาเลือกเดือน** · **กรอกคะแนนอย่างน้อย 1 ด้าน** · **เลือกลูกค้า** | ☐ |
| 4 | VERIFY stepper | — | ยังอยู่ขั้น **ข้อมูลหลักแบบสรุป** | ☐ |

### TC-V02 — จำนวนติดลบ (negative) [AI-DEFAULT]
- group: ตรวจสอบข้อมูล · ความสำคัญ: สูง · trace: VR-02 · EC-03 · AC-06 · DEC-04
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: C
- ผ่านเมื่อ: ช่องแดง + บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | TYPE ช่องแรกตารางคุณภาพ | -1 | ช่องขอบแดงทันที | ☐ |
| 4 | CLICK **ถัดไป** | — | **ใส่เป็นจำนวนเต็ม 0 ขึ้นไป (จำนวนลูกค้า)** · ยังอยู่ขั้น 1 | ☐ |

### TC-V03 — จำนวนทศนิยม (boundary)
- group: ตรวจสอบข้อมูล · ความสำคัญ: กลาง · trace: VR-02
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: C
- ผ่านเมื่อ: บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | TYPE ช่องแรกตารางคุณภาพ | 2.5 | ช่องขอบแดง | ☐ |
| 4 | CLICK **ถัดไป** | — | **ใส่เป็นจำนวนเต็ม 0 ขึ้นไป (จำนวนลูกค้า)** | ☐ |

### TC-V04 — ตัวอักษรในช่องจำนวน (negative)
- group: ตรวจสอบข้อมูล · ความสำคัญ: กลาง · trace: VR-02
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: C
- ผ่านเมื่อ: ช่องแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | TYPE ช่องแรกตารางคุณภาพ | ก | ช่องขอบแดง รวมแถวยัง 0 | ☐ |

### TC-V05 — ค่าศูนย์ทั้งเอกสาร (boundary)
- group: ตรวจสอบข้อมูล · ความสำคัญ: กลาง · trace: VR-03 · EC-02
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: C
- ผ่านเมื่อ: บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | SELECT เดือน + TYPE 0 ทุกช่องแถว 1 + SELECT ลูกค้า 1 ราย | 0 | % ด้านนี้แสดง — | ☐ |
| 4 | CLICK **ถัดไป** | — | **กรอกคะแนนอย่างน้อย 1 ด้าน** | ☐ |

### TC-V06 — เลือกลูกค้าซ้ำ (negative)
- group: ตรวจสอบข้อมูล · ความสำคัญ: กลาง · trace: VR-04
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: ร้านค้าตัวอย่าง GT-01 สองแถว
- ผ่านเมื่อ: แถว 2 แดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | SELECT แถวลูกค้า 1 | ร้านค้าตัวอย่าง GT-01 | — | ☐ |
| 4 | CLICK **เพิ่มลูกค้า** แล้ว SELECT แถว 2 | ร้านค้าตัวอย่าง GT-01 | — | ☐ |
| 5 | CLICK **ถัดไป** | — | แถว 2 **ลูกค้าซ้ำกับแถวที่ 1** | ☐ |

### TC-V07 — แถวลูกค้าเดียวลบไม่ได้
- group: ตรวจสอบข้อมูล · ความสำคัญ: ต่ำ · trace: VR-04
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มลบเมื่อเหลือแถวเดียว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | VERIFY แถวลูกค้าแถวเดียว | — | ไม่มีปุ่ม **ลบแถวนี้** | ☐ |
| 4 | CLICK **เพิ่มลูกค้า** | — | 2 แถว มีปุ่ม **ลบแถวนี้** | ☐ |

### TC-K01 — รวมและ % ด้านคุณภาพ (ตัวอย่าง) [AI-DEFAULT]
- group: คำนวณ · ความสำคัญ: สูง · trace: BR-01 BR-02 BR-03 · AC-02 · DEC-16 DEC-18
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=CSM-2569-0003 · files=—
- Start: OPEN `#/csat-gt/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แถวรวม 20/19/8/1/0 · 48 · 86.67%

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt/view/R3` | — | แท็บ **รายละเอียด** หัว **1) ด้านคุณภาพสินค้า/บริการ** | ☐ |
| 2 | VERIFY แถว **รวม** ตารางคุณภาพ | — | 20 · 19 · 8 · 1 · 0 · 48 ครบ 5 คอลัมน์ | ☐ |
| 3 | VERIFY ท้ายตาราง | — | **86.67%** | ☐ |

### TC-K02 — % ด้านส่งมอบและเจ้าหน้าที่ [AI-DEFAULT]
- group: คำนวณ · ความสำคัญ: สูง · trace: BR-03 · DEC-17
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=CSM-2569-0003 · files=—
- Start: OPEN `#/csat-gt/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: 87.50% และ 84.58%

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตาราง **2) ด้านการส่งมอบสินค้า** | — | รวม 48 · **87.50%** | ☐ |
| 2 | VERIFY ตาราง **3) ด้านเจ้าหน้าที่ผู้ให้บริการ/พนักงานขาย** | — | รวม 96 · **84.58%** | ☐ |

### TC-K03 — % โดยรวมถ่วงตามจำนวนคำตอบ [AI-DEFAULT]
- group: คำนวณ · ความสำคัญ: สูง · trace: BR-04 · DEC-19 · AC-03
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=CSM-2569-0003 · files=—
- Start: OPEN `#/csat-gt/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: 85.83% สูง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ส่วน **สรุปผลการประเมิน** | — | **โดยรวม** **85.83%** pill **ลูกค้ามีความพึงพอใจสูง** | ☐ |
| 2 | VERIFY บรรทัดเกณฑ์ | — | **ประเมินจากลูกค้าที่มีการสั่งซื้อจำนวนตั้งแต่ 3 ครั้งขึ้นไป / เดือน** | ☐ |

### TC-K04 — ผลต่ำกว่าช่วงกลาง [AI-DEFAULT]
- group: คำนวณ · ความสำคัญ: สูง · trace: BR-05
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=CSM-2569-0001 · files=—
- Start: OPEN `#/csat-gt/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: 57.29% อาจไม่พึงพอใจ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt/view/R1` | — | **โดยรวม** **57.29%** pill **ลูกค้าอาจมีความไม่พึงพอใจ** | ☐ |

### TC-K05 — ด้านที่ไม่มีคำตอบแสดงขีด
- group: คำนวณ · ความสำคัญ: กลาง · trace: EC-01 · AC-04
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=CSM-2569-0010 คะแนนว่าง · files=—
- Start: OPEN `#/csat-gt/view/R10`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ทุกด้านไม่มีตัวเลข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt/view/R10` | — | ช่องคะแนนเป็นขีด · การ์ด **โดยรวม** ไม่มีตัวเลข | ☐ |

### TC-K06 — หัวข้อตรงกระดาษ 16 ข้อ [AI-DEFAULT]
- group: คำนวณ · ความสำคัญ: กลาง · trace: BR-07 · DEC-05 DEC-06 DEC-07 DEC-09
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: หัวข้อ 4/4/8

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | VERIFY ตารางคุณภาพ | — | **1. คุณภาพของสินค้าโดยรวม** ถึง **4. ความรวดเร็วในการแก้ไขปัญหาและหาทางป้องกันไม่ให้เกิดซ้ำ** | ☐ |
| 4 | VERIFY ตารางเจ้าหน้าที่ | — | ถึง **8. พนักงานตรงต่อเวลาและปฏิบัติตามเงื่อนไข ที่ให้กับลูกค้า** | ☐ |
| 5 | VERIFY หัวคอลัมน์ | — | **มากที่สุด** **มาก** **ปานกลาง** **น้อย** **ต้องปรับปรุง** **รวม** | ☐ |

### TC-U01 — ปุ่มดึงลูกค้าต้องเลือกเดือนก่อน
- group: ลูกค้า · ความสำคัญ: กลาง · trace: FN-04
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปุ่มกดได้หลังเลือกเดือน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | VERIFY ปุ่ม **ดึงลูกค้าที่สั่งซื้อถึงเกณฑ์ในเดือนนี้** | — | ปุ่มเทากดไม่ได้ | ☐ |
| 4 | SELECT ช่อง **ประจำเดือน** | กันยายน 2569 | ปุ่มกดได้ | ☐ |

### TC-U02 — ดึงลูกค้าซ้ำไม่เพิ่มแถวซ้ำ
- group: ลูกค้า · ความสำคัญ: สูง · trace: FN-04 · S-05 · AC-07
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: กดซ้ำไม่มีลูกค้าเพิ่ม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | SELECT เดือนแล้ว CLICK **ดึงลูกค้าที่สั่งซื้อถึงเกณฑ์ในเดือนนี้** | กันยายน 2569 | toast ขึ้นต้น **เพิ่มลูกค้า** · การ์ดสรุป **ลูกค้าที่ประเมิน** | ☐ |
| 4 | CLICK ปุ่มเดิมอีกครั้ง | — | toast **ไม่มีลูกค้าเพิ่ม** | ☐ |

### TC-U03 — ลูกค้าต่ำกว่าเกณฑ์ เตือนไม่บล็อก [AI-DEFAULT]
- group: ลูกค้า · ความสำคัญ: สูง · trace: BR-06 · DEC-20 · EC-04 · AC-08
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: ลูกค้าที่สั่งซื้อน้อยกว่าเกณฑ์
- ผ่านเมื่อ: ป้ายเตือนแต่ไปต่อได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | SELECT เดือน + คะแนน 1 แถว + SELECT ลูกค้าที่ตัวเลือกบอกสั่งซื้อ 1–2 ครั้ง | — | แถวแสดง **· ต่ำกว่าเกณฑ์** | ☐ |
| 4 | CLICK **ถัดไป** 2 ครั้ง | — | ขั้นตรวจสอบมีแถบเตือนขึ้นต้น **มีลูกค้า** และบันทึกได้ | ☐ |

### TC-S01 — ส่งอนุมัติ ค่าเริ่มผู้พิจารณาจาก DOA [AI-DEFAULT]
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: FN-05 · AC-09 · DEC-03 (auto: e2e S8)
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=CSM-2569-0011 ร่าง · files=—
- Start: OPEN `#/csat-gt/view/R11`
- ชุดข้อมูล: —
- ผ่านเมื่อ: รออนุมัติ + toast

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt/view/R11` | — | แบนเนอร์ขึ้นต้น **ไม่อนุมัติ — กลับเป็นร่าง (เลขเดิม)** | ☐ |
| 2 | CLICK ปุ่ม **ส่งอนุมัติ** | — | หน้าต่าง **ส่งอนุมัติ?** แถว **ผู้อำนวยการสายงานการขาย** ค่าเริ่ม **ตัวอย่าง บริหารงาน** · **ค่าเริ่มต้นจากสายอนุมัติ (DOA) และผังองค์กร** | ☐ |
| 3 | CLICK ปุ่ม **ส่งอนุมัติ** ในหน้าต่าง | — | toast **ส่งอนุมัติแล้ว · CSM-2569-0011** · pill **รออนุมัติ** | ☐ |

### TC-S02 — ผู้จัดทำไม่อยู่ในรายชื่อผู้พิจารณา (SoD)
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: BR-DOA-04 · VR-05
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=CSM-2569-0010 · files=—
- Start: OPEN `#/csat-gt/view/R10`
- ชุดข้อมูล: สมมติ
- ผ่านเมื่อ: ไม่พบชื่อตัวเอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งอนุมัติ** | — | หน้าต่าง **ส่งอนุมัติ?** | ☐ |
| 2 | TYPE ค้นหาในช่องผู้พิจารณา | สมมติ | ไม่พบชื่อผู้จัดทำในตัวเลือก | ☐ |

### TC-S03 — ล้างผู้พิจารณาแล้วส่ง (negative)
- group: ส่งอนุมัติ · ความสำคัญ: กลาง · trace: VR-05
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=CSM-2569-0010 · files=—
- Start: OPEN `#/csat-gt/view/R10`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** แล้วล้างช่องผู้พิจารณา | — | ช่องว่าง | ☐ |
| 2 | CLICK ปุ่ม **ส่งอนุมัติ** ในหน้าต่าง | — | **กรุณาเลือกผู้พิจารณา** · หน้าต่างยังเปิด | ☐ |

### TC-S04 — DOA หลายขั้น แถวผู้พิจารณาเพิ่มตาม
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: Rule #108 · BR-08 · DEC-03 (auto: e2e S8)
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=__QA__.doa.push('ขั้นทดสอบ') · files=—
- Start: OPEN `#/csat-gt/view/R10`
- ชุดข้อมูล: —
- ผ่านเมื่อ: 2 แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** | — | หน้าต่างมี 2 แถว **ผู้อำนวยการสายงานการขาย** และ **ขั้นทดสอบ** | ☐ |

### TC-S05 — ส่งไม่สำเร็จ (API error)
- group: ส่งอนุมัติ · ความสำคัญ: กลาง · trace: EC-09 (auto: e2e S9)
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=__QA__.sim('error') · files=—
- Start: OPEN `#/csat-gt/view/R10`
- ชุดข้อมูล: —
- ผ่านเมื่อ: toast error สถานะยังร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** แล้ว CLICK **ส่งอนุมัติ** ในหน้าต่าง | — | toast **ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง** | ☐ |
| 2 | VERIFY pill | — | ยังเป็น **ร่าง** | ☐ |

### TC-S06 — ข้อมูลถูกแก้โดยผู้อื่น (stale)
- group: ส่งอนุมัติ · ความสำคัญ: ต่ำ · trace: EC-09
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=__QA__.sim('stale') · files=—
- Start: OPEN `#/csat-gt/view/R10`
- ชุดข้อมูล: —
- ผ่านเมื่อ: toast stale

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** แล้ว CLICK **ส่งอนุมัติ** ในหน้าต่าง | — | toast **ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่** | ☐ |

### TC-A01 — ผู้พิจารณาอนุมัติ
- group: อนุมัติ · ความสำคัญ: สูง · trace: FN-06 · AC-10 · S-07
- actor (role): ผู้อำนวยการสายงานการขาย
- Setup: role=approver ผู้อำนวยการสายงานการขาย (__QA__.setMe('E02')) · seed=CSM-2569-0008 รออนุมัติ · files=—
- Start: OPEN `#/csat-gt/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: อนุมัติแล้วและล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt/view/R8` | — | แบนเนอร์มี **คุณเป็นผู้พิจารณาเอกสารนี้** · ปุ่ม **อนุมัติ** **ไม่อนุมัติ** | ☐ |
| 2 | CLICK ปุ่ม **อนุมัติ** | — | หน้าต่าง **อนุมัติแบบสรุปนี้?** มี **% โดยรวม** | ☐ |
| 3 | CLICK **อนุมัติ** ในหน้าต่าง | — | toast ขึ้นต้น **อนุมัติแล้ว · CSM-2569-0008** · pill **อนุมัติแล้ว** | ☐ |
| 4 | VERIFY ท้าย drawer | — | **อนุมัติแล้ว ล็อกแก้ไข** | ☐ |

### TC-A02 — ไม่อนุมัติ กลับเป็นร่างเลขเดิม [AI-DEFAULT]
- group: อนุมัติ · ความสำคัญ: สูง · trace: FN-07 · BR-09 · DEC-11 · AC-11
- actor (role): ผู้อำนวยการสายงานการขาย
- Setup: role=approver ผู้อำนวยการสายงานการขาย (__QA__.setMe('E02')) · seed=CSM-2569-0008 · files=—
- Start: OPEN `#/csat-gt/view/R8`
- ชุดข้อมูล: เหตุผล ตัวเลขไม่ตรงกับแบบสำรวจ
- ผ่านเมื่อ: ร่างเลขเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ไม่อนุมัติ** | — | หน้าต่าง **ไม่อนุมัติแบบสรุปนี้?** ชิป **ตัวเลขไม่ตรงกับแบบสำรวจ** | ☐ |
| 2 | CLICK ชิป **ตัวเลขไม่ตรงกับแบบสำรวจ** แล้ว CLICK ปุ่ม **ไม่อนุมัติ** | — | toast **ไม่อนุมัติ — กลับเป็นร่าง · CSM-2569-0008** | ☐ |
| 3 | CLICK แท็บ **ประวัติ** | — | มี **ไม่อนุมัติ** และ **กลับเป็นร่าง (เลขเดิม)** | ☐ |

### TC-A03 — ไม่อนุมัติไม่ใส่เหตุผล (negative)
- group: อนุมัติ · ความสำคัญ: สูง · trace: VR-06
- actor (role): ผู้อำนวยการสายงานการขาย
- Setup: role=approver ผู้อำนวยการสายงานการขาย (__QA__.setMe('E02')) · seed=CSM-2569-0008 · files=—
- Start: OPEN `#/csat-gt/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ไม่อนุมัติ** แล้ว CLICK ปุ่ม **ไม่อนุมัติ** ในหน้าต่างทันที | — | **กรุณาระบุเหตุผล** · หน้าต่างยังเปิด | ☐ |

### TC-A04 — อนุมัติจากแท็บลายเซ็น
- group: อนุมัติ · ความสำคัญ: กลาง · trace: U13
- actor (role): ผู้อำนวยการสายงานการขาย
- Setup: role=approver ผู้อำนวยการสายงานการขาย (__QA__.setMe('E02')) · seed=CSM-2569-0007 · files=—
- Start: OPEN `#/csat-gt/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ตัดสินใน timeline ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **ลายเซ็น / อนุมัติ** | — | **สายอนุมัติ (DOA)** **DOA-CSM-01 · 1 ขั้น** · **ส่งอนุมัติ (ผู้จัดทำ)** · **ขั้น 1 · ผู้อำนวยการสายงานการขาย** **รอพิจารณา** | ☐ |
| 2 | CLICK **อนุมัติ** ใน timeline แล้วยืนยัน | — | ผลลัพธ์ **อนุมัติแล้ว** | ☐ |

### TC-A05 — อนุมัติผลต่ำ แจ้งฝ่ายขาย [AI-DEFAULT]
- group: อนุมัติ · ความสำคัญ: กลาง · trace: BR-13 · csm_low_csat (ต้อง simulate)
- actor (role): ผู้อำนวยการสายงานการขาย
- Setup: role=approver ผู้อำนวยการสายงานการขาย (__QA__.setMe('E02')) · seed=ใบรออนุมัติที่ % < 60 (สร้างตาม TC-C04 ชุด B แล้วส่ง) · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: B
- ผ่านเมื่อ: toast มีคำแจ้งฝ่ายขาย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN ใบที่ % < 60 แล้ว CLICK **อนุมัติ** + ยืนยัน | — | toast มี **แจ้งฝ่ายขาย: ผลต่ำกว่า 60%** | ☐ |

### TC-X01 — เจ้าของยกเลิกใบรออนุมัติ
- group: ยกเลิก · ความสำคัญ: สูง · trace: FN-07 · AC-12 · csm_cancelled
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=CSM-2569-0008 · files=—
- Start: OPEN `#/csat-gt/view/R8`
- ชุดข้อมูล: เหตุผล เลือกเดือนผิด
- ผ่านเมื่อ: สถานะยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยกเลิกเอกสาร** | — | หน้าต่าง **ยกเลิกเอกสาร?** | ☐ |
| 2 | CLICK ชิป **เลือกเดือนผิด** แล้ว CLICK ปุ่ม **ยกเลิกเอกสาร** | — | toast **ยกเลิกเอกสารแล้ว · CSM-2569-0008** · pill **ยกเลิก** | ☐ |

### TC-X02 — ยกเลิกจากเมนูแล้วเปลี่ยนใจ
- group: ยกเลิก · ความสำคัญ: กลาง · trace: DEC-11
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=CSM-2569-0010 · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สถานะเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ⋮ แถว CSM-2569-0010 แล้ว CLICK **ยกเลิกเอกสาร** | — | หน้าต่าง **ยกเลิกเอกสาร?** | ☐ |
| 2 | CLICK **ไม่ยกเลิก** | — | หน้าต่างปิด สถานะ **ร่าง** | ☐ |

### TC-X03 — Sales admin ยกเลิกใบคนอื่นได้
- group: ยกเลิก · ความสำคัญ: กลาง · trace: 05 §5.3
- actor (role): Sales admin
- Setup: role=admin Sales admin (__QA__.setMe('E05')) · seed=CSM-2569-0007 · files=—
- Start: OPEN `#/csat-gt/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: มีปุ่มยกเลิก ไม่มีปุ่มอนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt/view/R7` | — | ปุ่ม **ยกเลิกเอกสาร** แสดง · ไม่มีปุ่มอนุมัติ | ☐ |

### TC-X04 — ใบอนุมัติแล้วยกเลิกไม่ได้
- group: ยกเลิก · ความสำคัญ: กลาง · trace: TC-D06
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=CSM-2569-0003 · files=—
- Start: OPEN `#/csat-gt/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัว drawer | — | ไม่มีปุ่มยกเลิกเอกสาร · ท้าย drawer **อนุมัติแล้ว ล็อกแก้ไข** | ☐ |

### TC-P01 — ผู้พิจารณาไม่เห็นร่างของคนอื่น (deny) [AI-DEFAULT]
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D01 · BR-11 · DEC-12 (auto: e2e S3)
- actor (role): ผู้อำนวยการสายงานการขาย
- Setup: role=approver ผู้อำนวยการสายงานการขาย (__QA__.setMe('E02')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่เห็นร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | badge **8 รายการ** · ไม่เห็นร่าง CSM-2569-0009 0010 0011 | ☐ |
| 2 | VERIFY badge | — | **รอฉันพิจารณา 2** | ☐ |

### TC-P02 — เปิด route ใบที่ไม่มีสิทธิ์ (deny)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D02 (auto: e2e S6)
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt/view/R9`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่เปิด drawer

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt/view/R9` | — | เห็นหน้ารายการ ไม่มี drawer (ไม่พบใบ) | ☐ |

### TC-P03 — เจ้าของไม่เห็นปุ่มอนุมัติใบตัวเอง (SoD)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D03 (auto: e2e S5)
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=CSM-2569-0008 · files=—
- Start: OPEN `#/csat-gt/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มอนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt/view/R8` | — | แบนเนอร์ขึ้นต้น **รอ ตัวอย่าง บริหารงาน พิจารณา** · ไม่มีปุ่มอนุมัติ | ☐ |

### TC-P04 — ผู้พิจารณาไม่มีปุ่มแก้ไข (deny)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D04 (auto: e2e S5)
- actor (role): ผู้อำนวยการสายงานการขาย
- Setup: role=approver ผู้อำนวยการสายงานการขาย (__QA__.setMe('E02')) · seed=CSM-2569-0008 · files=—
- Start: OPEN `#/csat-gt/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มแก้ไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัว drawer | — | ไม่มีปุ่มแก้ไข (ไม่มีสิทธิ์) | ☐ |

### TC-P05 — Sales admin เห็นทุกใบ
- group: สิทธิ์ · ความสำคัญ: สูง · trace: AC-14 · DEC-12
- actor (role): Sales admin
- Setup: role=admin Sales admin (__QA__.setMe('E05')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 11 ใบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | badge **11 รายการ** · มีแถว **CSM-2569-0009** | ☐ |

### TC-P06 — Sales Manager เขตอื่นไม่เห็นใบของ E01 (deny)
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: TC-D05
- actor (role): Sales Manager เขตอื่น
- Setup: role=other (__QA__.setMe('E03')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่เห็นใบของคนอื่น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | ไม่เห็น CSM-2569-0008 (ไม่มีสิทธิ์) · เห็น **CSM-2569-0009** ของตน | ☐ |

### TC-D01 — PDF Preview 2 หน้าตรงแบบฟอร์ม [AI-DEFAULT]
- group: PDF · ความสำคัญ: สูง · trace: FN-08 · AC-13 · BR-12 BR-14 BR-17 · DEC-08 DEC-10 DEC-15 (auto: e2e S4)
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=CSM-2569-0003 · files=—
- Start: OPEN `#/csat-gt/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แบบพิมพ์ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | **ตัวอย่าง PDF · A4 · 2 หน้า** · หัว **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** · **ประจำเดือน** **กรกฎาคม 2569** | ☐ |
| 2 | VERIFY หน้า 1 | — | ตาราง 3 ด้าน คอลัมน์ % ผสานแนวตั้ง · **มีต่อหน้าถัดไป** · **หน้า 1/2** | ☐ |
| 3 | VERIFY หน้า 2 | — | **สรุปผลการประเมิน - โดยรวม 85.83 % ลูกค้ามีความพึงพอใจสูง** · **การแปลผลคะแนน CSAT:** · หัวตาราง **โดยมีรายชื่อดังนี้** **จำนวนการสั่งซื้อ** · **หน้า 2/2** | ☐ |
| 4 | VERIFY ช่องลงชื่อ | — | **Sales Manager** · **ผู้อำนวยการสายงานการขาย** ☑ **อนุมัติ** · footer **Doc.No.FM-SAL-11** | ☐ |

### TC-D02 — PDF ร่างมีคำว่าร่าง
- group: PDF · ความสำคัญ: กลาง · trace: thai-doc states
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=CSM-2569-0010 · files=—
- Start: OPEN `#/csat-gt/view/R10`
- ชุดข้อมูล: —
- ผ่านเมื่อ: footer ร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | footer มี **· ร่าง ·** · บรรทัดวันที่ช่องลงชื่อเป็นเส้นประ | ☐ |

### TC-D03 — พิมพ์ PDF
- group: PDF · ความสำคัญ: กลาง · trace: API-09
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=CSM-2569-0003 · files=—
- Start: OPEN `#/csat-gt/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: หน้าต่างพิมพ์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** แล้ว CLICK **พิมพ์** | — | toast ขึ้นต้น **กำลังเปิดหน้าต่างพิมพ์** | ☐ |

### TC-D04 — PDF DOA 6 ขั้น ช่องลงชื่อ 2 แถว
- group: PDF · ความสำคัญ: กลาง · trace: BR-12 · EC-11
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=__QA__.doa.push 5 ครั้งแล้วส่งใบร่าง · files=—
- Start: OPEN `#/csat-gt/view/R10`
- ชุดข้อมูล: —
- ผ่านเมื่อ: 7 ช่อง 4+3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** (หลังส่งใบด้วยสาย 6 ขั้น) | — | หน้า 2 ช่องลงชื่อ 2 แถว (4+3) ยัง **หน้า 2/2** | ☐ |

### TC-E01 — แบบเอกสารปิดใช้ สร้างไม่ได้
- group: ขอบเขต · ความสำคัญ: กลาง · trace: EC-10 · F-DOCCFG · DEC-13
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=__QA__.setDocActive(false) · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปุ่มสร้างกดไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หน้า | — | แถบ **แบบเอกสารนี้ยังไม่เปิดใช้งาน — สร้างใหม่ไม่ได้** · ปุ่ม **สร้างแบบสรุป** เทา | ☐ |

### TC-E02 — Esc ปิด modal ก่อน drawer
- group: ขอบเขต · ความสำคัญ: ต่ำ · trace: U8 (auto: e2e S10)
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=CSM-2569-0010 · files=—
- Start: OPEN `#/csat-gt/view/R10`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ลำดับปิดถูก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** แล้ว PRESS Esc | — | หน้าต่างปิด drawer ยังเปิด | ☐ |
| 2 | PRESS Esc | — | drawer ปิด | ☐ |

### TC-E03 — ลากเมาส์ออกนอกหน้าต่างไม่ปิด
- group: ขอบเขต · ความสำคัญ: ต่ำ · trace: U25
- actor (role): ผู้อำนวยการสายงานการขาย
- Setup: role=approver ผู้อำนวยการสายงานการขาย (__QA__.setMe('E02')) · seed=CSM-2569-0008 · files=—
- Start: OPEN `#/csat-gt/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: หน้าต่างไม่ปิด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ไม่อนุมัติ** แล้วลากคลุมข้อความในช่องเหตุผลไปปล่อยนอกหน้าต่าง | — | หน้าต่าง **ไม่อนุมัติแบบสรุปนี้?** ยังเปิด | ☐ |

### TC-E04 — อนุมัติแล้วไม่เปลี่ยนค่า/ไม่ส่งต่อ [AI-DEFAULT]
- group: ขอบเขต · ความสำคัญ: กลาง · trace: DEC-01 DEC-02 · BR-15 (ต้อง simulate)
- actor (role): ผู้อำนวยการสายงานการขาย
- Setup: role=approver ผู้อำนวยการสายงานการขาย (__QA__.setMe('E02')) · seed=CSM-2569-0007 · files=—
- Start: OPEN `#/csat-gt/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีผลข้างเคียงนอกเอกสาร

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **อนุมัติ** + ยืนยัน | — | toast ขึ้นต้น **อนุมัติแล้ว** · ประวัติไม่มีรายการส่งต่อระบบอื่น | ☐ |

### TC-E05 — สร้างเดือนที่มีใบแล้ว (ไม่บล็อก)
- group: ขอบเขต · ความสำคัญ: ต่ำ · trace: EC-06 EC-07 EC-08 (บันทึกผล OQ-06)
- actor (role): Sales Manager
- Setup: role=owner Sales Manager (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/csat-gt`
- ชุดข้อมูล: A
- ผ่านเมื่อ: บันทึกได้ (ยังไม่มีกฎกันซ้ำ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/csat-gt` | — | หน้า **หัวข้อการประเมินความพึงพอใจ สำหรับ General Trade** แสดงตาราง | ☐ |
| 2 | CLICK ปุ่ม **สร้างแบบสรุป** | — | drawer กว้างเปิด หัว **แบบสรุปความพึงพอใจ General Trade** · stepper 3 ขั้น **ข้อมูลหลักแบบสรุป** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 3 | SELECT เดือน **กันยายน 2569** + คะแนน + ลูกค้า แล้วบันทึกแบบร่าง | A | toast ขึ้นต้น **บันทึกร่างแล้ว** | ☐ |

## วิธีที่ agent รัน (Run protocol)
1. เปิด feature.html · ทำ Setup ก่อน (เช่น `__QA__.setMe('E02')` · `__QA__.sim('error')`) แล้ว OPEN route ใน Start
2. ทำทีละ step เทียบ Expected กับสิ่งที่เห็นบนจอ (ตัวหนา = ข้อความบนจอ)
3. โหลดหน้าใหม่ระหว่างเคสเพื่อคืน seed มาตรฐาน
4. กรอกผลตาม Result Report schema

## Coverage Audit
| หมวด | covered / total |
|---|---|
| AC | 14 / 14 |
| BR | 17 / 17 |
| VR | 6 / 6 |
| EC | 11 / 11 |
| Deny TC-D | 6 / 6 |
| DEC | 20 / 20 |
| XT / events | 4 / 4 |

- **Manifest cross-check (FRD 06 §6.1–6.2): ✅**
### ข้าม (พร้อมเหตุผล)
- ไม่มี — EC-06 (สร้างซ้ำเดือน) ยังไม่มีกฎบล็อก (OQ-06) ทดสอบเป็นการบันทึกผลใน TC-E05

## Result Report (schema)
```json
{ "feature_id": "F-TMP-002", "run_at": "<iso datetime>", "results": [ { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" } ], "summary": { "total": 0, "pass": 0, "fail": 0, "blocked": 0 } }
```

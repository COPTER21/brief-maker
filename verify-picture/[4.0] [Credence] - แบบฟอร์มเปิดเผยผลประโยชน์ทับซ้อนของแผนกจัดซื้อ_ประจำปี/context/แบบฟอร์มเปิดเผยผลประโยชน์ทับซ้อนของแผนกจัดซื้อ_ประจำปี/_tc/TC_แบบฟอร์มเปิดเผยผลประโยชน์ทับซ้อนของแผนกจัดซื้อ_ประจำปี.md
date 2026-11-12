# AI Test Cases — F-TMP-006 แบบฟอร์มเปิดเผยผลประโยชน์ทับซ้อนของแผนกจัดซื้อ ประจำปี

ชุดทดสอบสำหรับ AI agent (browser-use/vision) รันบน prototype `feature.html` · anchor = ข้อความที่เห็นบนจอ (verbatim จาก HTML) · สลับผู้ใช้ด้วย `window.__QA__.setMe()` · เคสที่ derive จากมติ AI-DEFAULT ติดป้าย `[AI-DEFAULT]` (fail อาจแปลว่ามติต้องเปลี่ยน ไม่ใช่บั๊ก) · ทุกชื่อเป็นชื่อสมมติ

> ⚠ [NO-BROWSER] รอบนี้ยังไม่ได้รัน `verify_anchors.py` (ต้องใช้ browser) — anchor ตรวจด้วย jsdom smoke (reports/smoke_jsdom_report.txt 39/39) + อ่านโค้ด · ต้องรัน verify_anchors บนเครื่องที่มี browser ก่อนส่ง QA

## Meta
| Field | Value |
|---|---|
| Feature ID | F-TMP-006 (ชั่วคราว) |
| ชื่อ | แบบฟอร์มเปิดเผยผลประโยชน์ทับซ้อนของแผนกจัดซื้อ ประจำปี (Annual Conflict of Interest Disclosure) |
| เวอร์ชัน | v1.0 · 2026-10-10 |
| App entry | `feature.html` |
| Routes | `#/coi-disclosure` · `#/coi-disclosure/create` · `#/coi-disclosure/edit/:id` · `#/coi-disclosure/view/:id` |
| ที่มา | FRD_F-TMP-006_Pack (06_TESTS AC-01..15 · TC-D01..09) · BRD-PUR-COI-001 · feature.html · DECISIONS.lock (18) |
| จำนวนเคส | 50 |
| หมวด | 9 |

## Coverage
| group | เคส | สูง | กลาง | ต่ำ |
|---|---|---|---|---|
| รายการ | 8 | 4 | 3 | 1 |
| ยื่น/แก้ไข | 10 | 4 | 5 | 1 |
| ตรวจความถูกต้อง | 5 | 4 | 1 | 0 |
| ส่งและรับทราบ | 5 | 4 | 0 | 1 |
| ส่งกลับแก้ไข | 2 | 2 | 0 | 0 |
| ยกเลิก | 3 | 1 | 2 | 0 |
| สิทธิ์ | 8 | 4 | 3 | 1 |
| PDF/พิมพ์ | 5 | 3 | 1 | 1 |
| Cross-Module | 4 | 1 | 2 | 1 |

## Coverage Ledger
### FR (06_TESTS §6.1)
| item | cases |
|---|---|
| AC-01 | TC-C01, TC-C07 |
| AC-02 | TC-V01 |
| AC-03 | TC-V02 |
| AC-04 | TC-C04 |
| AC-05 | TC-C05 |
| AC-06 | TC-C01 |
| AC-07 | TC-C02 |
| AC-08 | TC-S01, TC-S05 |
| AC-09 | TC-R01, TC-R02 |
| AC-10 | TC-D01, TC-D02 |
| AC-11 | TC-S03, TC-D03 |
| AC-12 | TC-X01, TC-X02 |
| AC-13 | TC-L01, TC-L05, TC-L06, TC-P06 |
| AC-14 | TC-V03 |
| AC-15 | TC-D02 |
### Business Rules (05_RULES)
| rule | cases |
|---|---|
| BR-01 | TC-D02 |
| BR-02 | TC-D02 |
| BR-03 | TC-C04 |
| BR-04 | TC-C02, TC-C04 |
| BR-05 | TC-V01 |
| BR-06 | TC-C03 |
| BR-07 | TC-C05, TC-S05 |
| BR-08 | TC-C02, TC-XT01 |
| BR-09 | TC-S03 |
| BR-10 | TC-R01 |
| BR-11 | TC-X03 |
| BR-12 | TC-XT03 |
| BR-13 | TC-L02, TC-L06 |
| BR-14 | TC-S03, TC-D03 |
| BR-15 | TC-S01 |
| BR-16 | TC-D01 |
| BR-DOA-01 | TC-C01 |
| BR-DOA-02 | TC-C01 |
| BR-DOA-03 | TC-R01 |
| BR-DOA-04 | TC-S02 |
### Validation Rules
| VR | cases |
|---|---|
| VR-01 | TC-V01 |
| VR-02 | TC-V02 |
| VR-03 | TC-V01 |
| VR-04 | TC-V04 |
| VR-05 | TC-V05 |
| VR-06 | TC-V03 |
### Edge Cases
| EC | cases |
|---|---|
| EC-01 | TC-C04 |
| EC-02 | TC-V02 |
| EC-03 | TC-V03 |
| EC-04 | TC-C05 |
| EC-05 | TC-V04 |
| EC-06 | TC-S03 |
| EC-07 | — ข้าม (ดู Coverage Audit) |
| EC-08 | TC-S04 |
| EC-09 | TC-L08 |
| EC-10 | — ข้าม (ดู Coverage Audit) |
| EC-11 | TC-P03 |
| EC-12 | — ข้าม (ดู Coverage Audit) |
### Error Codes (02_API)
| error | cases |
|---|---|
| CHOICE_REQUIRED | TC-V01 |
| DETAIL_REQUIRED | TC-V02 |
| CONFIRM_REQUIRED | TC-V01, TC-V03 |
| NOT_EDITABLE | TC-P05 |
| NOT_OWNER | TC-P05, TC-P07 |
| ASSIGNEE_REQUIRED | TC-V04 |
| SELF_APPROVAL | TC-S02 |
| NOT_CURRENT_APPROVER | TC-P04 |
| REASON_REQUIRED | TC-V05 |
| NOT_CANCELLABLE | TC-X03 |
| NOT_FOUND | TC-P01 |
| STALE | TC-S04 |
| 403 | TC-P08 |
### Scope Lock (DEC — 07 §7.0 = DECISIONS.lock)
| DEC | cases |
|---|---|
| DEC-01 | TC-XT03 |
| DEC-02 | TC-XT03 |
| DEC-03 | TC-C03, TC-S03 |
| DEC-04 | TC-C03, TC-D02 |
| DEC-05 | TC-D01 |
| DEC-06 | TC-D01 |
| DEC-07 | TC-S01, TC-D03 |
| DEC-08 | TC-R01, TC-R02, TC-X01 |
| DEC-09 | TC-L01, TC-P01, TC-P03, TC-P06 |
| DEC-10 | TC-C01 |
| DEC-11 | TC-L06, TC-C09 |
| DEC-12 | TC-C05, TC-D02 |
| DEC-13 | TC-S03 |
| DEC-14 | TC-C04 |
| DEC-15 | TC-C02, TC-C04, TC-V02 |
| DEC-16 | TC-L01, TC-L02, TC-L06, TC-P02, TC-P03 |
| DEC-17 | TC-L07, TC-C05, TC-C06, TC-S05 |
| DEC-18 | TC-D01 |
### Permission Matrix (role × action · 05 §5.3)
| cell | cases |
|---|---|
| owner ดูร่างของตน = allow | TC-L01 |
| ผู้อยู่ในสาย ดูร่าง = deny | TC-P01 |
| owner ดูใบคนอื่น = deny | TC-P02 |
| ผู้จัดการฝ่ายจัดซื้อ (ไม่อยู่ในสาย) ดู = deny | TC-P03 |
| ผู้อยู่ในสาย ดูหลังส่ง = allow | TC-L05, TC-S01 |
| compliance ดูทั้งหมด = allow | TC-P06 |
| owner แก้ไข draft/returned = allow | TC-C08, TC-R02 |
| แก้ไข pending = deny | TC-P05 |
| ตัดสิน ขั้นปัจจุบัน = allow | TC-S01, TC-R01 |
| ตัดสิน ไม่ใช่ขั้นปัจจุบัน = deny | TC-P04 |
| owner ยกเลิก = allow | TC-X01 |
| compliance ยกเลิก = allow | TC-X02 |
| ผู้อยู่ในสาย ยกเลิก = deny | TC-P07 |
| ยกเลิก approved = deny | TC-X03 |
| CSV ไม่มีรายละเอียด | TC-L06 |
### Cross-Module (XT — 06_TESTS §6.9)
| XT | Downstream | Case |
|---|---|---|
| XT-01 | ENG-NOTIFY coi_conflict_declared / coi_cancelled | TC-XT01, TC-C02, TC-X02 |
| XT-02 | ENG-DOC-STORE approved_final | TC-XT02 |
| XT-03 | ทะเบียน COI / Vendor master (ไม่ยิง) | TC-XT03 |
| XT-04 | DOA resolve role-line-manager | TC-XT04, TC-C03 |
### Cross-cutting / States
| item | cases |
|---|---|
| state draft→pending→approved | TC-C01, TC-S01 |
| state pending→returned→pending | TC-R01, TC-R02 |
| state →cancelled | TC-X01, TC-X02 |
| state approved→superseded | TC-S05 |
| empty state (ค้นหาไม่พบ) | TC-L03, TC-P02 |
| dirty-check ปิด drawer | TC-C10 |
| upload ไฟล์ผิดชนิด | TC-C09 |
| แจ้งเตือน upload ล้มเหลว | — ข้าม (ใช้ __QA__.sim('upload_fail') ได้ · ความสำคัญต่ำ) |

## Data Sets
### ชุด A (ไม่มี)
| ฟิลด์ | ค่า |
|---|---|
| การมีผลประโยชน์ทับซ้อน | ไม่มี |
| ยืนยันถ้อยคำ | ติ๊ก |
### ชุด B (มี)
| ฟิลด์ | ค่า |
|---|---|
| การมีผลประโยชน์ทับซ้อน | มี |
| รายละเอียด | น้องสาว (ชื่อสมมติ) เป็นหุ้นส่วนผู้จัดการ หจก. ทดสอบระบบ ผู้ขายวัสดุ |
| ยืนยันถ้อยคำ | ติ๊ก |
### ชุดผิด
| ฟิลด์ | ค่า | คาด |
|---|---|---|
| ไม่มี/มี | (ไม่เลือก) | กรุณาเลือก ไม่มี หรือ มี |
| รายละเอียด (มี) | สั้น | ระบุรายละเอียดอย่างน้อย 10 ตัวอักษร |
| ยืนยัน | (ไม่ติ๊ก) | กรุณายืนยันถ้อยคำรับรองก่อนส่ง |
| เหตุผล | (ว่าง) | กรุณาระบุเหตุผล |
### ไฟล์ทดสอบ (Files)
| ไฟล์ | ขนาด |
|---|---|
| หนังสือรับรองบริษัท.pdf | 300 KB |
| โปรแกรม.exe | 1 MB (ชนิดไม่รองรับ) |
### Personas (ชื่อสมมติ)
| id | ชื่อ | role |
|---|---|---|
| E01 | นายสมมติ ใจตรง | ผู้เปิดเผย (owner) |
| E02 | นางสาวตัวอย่าง ซื้อดี | ผู้เปิดเผย |
| E03 | นายทดสอบ หาของ | ผู้เปิดเผย |
| E04 | นางจำลอง คัดสรร | ผู้เปิดเผย (mgr E06) |
| E05 | นางสาวสมมุติ ดูแลดี | ผู้บังคับบัญชา (role-line-manager) |
| E06 | นายตัวอย่าง บริหารซื้อ | ผู้จัดการฝ่ายจัดซื้อ (ไม่ใช่ admin) |
| E07 | นางสาวทดสอบ กำกับงาน | ฝ่ายกฎหมาย/กำกับดูแล (role-compliance · admin) |

## Test Cases

### กลุ่ม: รายการ

#### TC-L01 — รายการของผู้เปิดเผยแสดงเฉพาะใบของตัวเอง
- group: รายการ · ความสำคัญ: สูง · trace: AC-13 / FN-11 / DEC-09 DEC-16
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 3 ใบของตัวเอง ไม่เห็นใบคนอื่น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/coi-disclosure` | — | หัว **แบบฟอร์มเปิดเผยผลประโยชน์ทับซ้อนของแผนกจัดซื้อ ประจำปี** + badge **3 รายการ · เปิดอยู่ 1** | ☐ |
| 2 | VERIFY ตาราง | — | 3 แถว: COI-2569-0004 · COI-2569-0003 · COI-2568-0011 | ☐ |
| 3 | VERIFY ไม่มีแถวการ์ดตัวเลขใต้หัว | — | มีแค่ segmented **ทั้งหมด 3** · **รอฉันพิจารณา 0** | ☐ |

#### TC-L02 — คอลัมน์ไม่มีรายละเอียดลับ
- group: รายการ · ความสำคัญ: สูง · trace: BR-13 / DEC-16
- actor (role): ฝ่ายกฎหมาย/กำกับดูแล
- Setup: role=ฝ่ายกฎหมาย/กำกับดูแล (__QA__.setMe('E07')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีคอลัมน์รายละเอียดในตาราง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัวตาราง | — | **เลขที่** · **ประจำปี** · **วันที่ยื่น** · **ผู้เปิดเผย** · **ตำแหน่ง** · **ผลประโยชน์ทับซ้อน** · **สถานะเอกสาร** · **ลายเซ็น** · ⋮ | ☐ |
| 2 | VERIFY แถว COI-2569-0002 | — | pill **มี** · ไม่มีข้อความ "คู่สมรส" ในตาราง | ☐ |

#### TC-L03 — ค้นหาเลขที่ ชื่อ ตำแหน่ง ปี
- group: รายการ · ความสำคัญ: กลาง · trace: FN-11
- actor (role): ฝ่ายกฎหมาย/กำกับดูแล
- Setup: role=ฝ่ายกฎหมาย/กำกับดูแล (__QA__.setMe('E07')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure`
- ชุดข้อมูล: —
- ผ่านเมื่อ: กรองตามคำค้น + empty state เมื่อไม่พบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE ช่อง **ค้นหาเลขที่ / ชื่อผู้เปิดเผย / ตำแหน่ง / ปี** | 2568 | เหลือ 1 แถว COI-2568-0011 | ☐ |
| 2 | TYPE ช่องค้นหา | ไม่มีจริง | **ไม่พบรายการที่ค้นหา** + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 3 | CLICK **ล้างตัวกรอง** | — | กลับมา 11 แถว | ☐ |

#### TC-L04 — กรองสถานะและผลการเปิดเผย
- group: รายการ · ความสำคัญ: กลาง · trace: FN-11
- actor (role): ฝ่ายกฎหมาย/กำกับดูแล
- Setup: role=ฝ่ายกฎหมาย/กำกับดูแล (__QA__.setMe('E07')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ตัวกรองทำงานร่วมกัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT **ทุกสถานะ** → **รอพิจารณา** | — | 3 แถว (0005 · 0006 · 0010) | ☐ |
| 2 | SELECT **ทุกผลการเปิดเผย** → **มี** | — | 1 แถว COI-2569-0006 | ☐ |

#### TC-L05 — แถบ "รอฉันพิจารณา" ของผู้บังคับบัญชา
- group: รายการ · ความสำคัญ: สูง · trace: AC-13 / FN-11
- actor (role): ผู้บังคับบัญชา
- Setup: role=ผู้บังคับบัญชา (__QA__.setMe('E05')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นใบที่ต้องพิจารณา

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY segmented | — | **ทั้งหมด 7** · **รอฉันพิจารณา 1** | ☐ |
| 2 | CLICK **รอฉันพิจารณา** | — | 1 แถว COI-2569-0006 สถานะ **รอพิจารณา** | ☐ |

#### TC-L06 — ส่งออก CSV ไม่มีรายละเอียด [AI-DEFAULT]
- group: รายการ · ความสำคัญ: สูง · trace: AC-13 / BR-13 / DEC-11 DEC-16
- actor (role): ฝ่ายกฎหมาย/กำกับดูแล
- Setup: role=ฝ่ายกฎหมาย/กำกับดูแล (__QA__.setMe('E07')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure`
- ชุดข้อมูล: —
- ผ่านเมื่อ: CSV ไม่มีคอลัมน์รายละเอียด/ข้อคิดเห็น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งออก CSV** | — | toast **ส่งออก 11 รายการ (ไม่มีช่องรายละเอียด — ข้อมูลลับ)** | ☐ |
| 2 | VERIFY ไฟล์ coi-disclosures.csv | — | หัว: เลขที่ · ประจำปี · วันที่ยื่น · ผู้เปิดเผย · ตำแหน่ง · ผลประโยชน์ทับซ้อน · สถานะ · ผู้พิจารณา · แทนฉบับ (ไม่มีรายละเอียด) | ☐ |

#### TC-L07 — เมนู ⋮ ตามสถานะ
- group: รายการ · ความสำคัญ: กลาง · trace: FN-11 / DEC-17
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เมนูตรงสิทธิ์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ⋮ แถว COI-2569-0004 (ร่าง) | — | **แก้ไข** · **พิมพ์** · **ยกเลิกเอกสาร** | ☐ |
| 2 | CLICK ⋮ แถว COI-2569-0003 (รับทราบแล้ว) | — | **พิมพ์** เท่านั้น (มีใบใหม่ค้างอ้างอยู่แล้ว ไม่มี แจ้งเปลี่ยนแปลง) | ☐ |

#### TC-L08 — แบบเอกสารยังไม่เปิดใช้
- group: รายการ · ความสำคัญ: ต่ำ · trace: EC-09 / FN-03
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สร้างไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console `__QA__.setDocActive(false)` | — | แถบแดง **แบบเอกสารนี้ยังไม่เปิดใช้งาน — ยื่นแบบเปิดเผยใหม่ไม่ได้** · ปุ่ม **ยื่นแบบเปิดเผย** disabled | ☐ |

### กลุ่ม: ยื่น/แก้ไข

#### TC-C01 — ยื่นแบบเปิดเผย "ไม่มี" (happy)
- group: ยื่น/แก้ไข · ความสำคัญ: สูง · trace: AC-01 AC-06 / FN-01..05 / BR-DOA-01 BR-DOA-02 / DEC-10
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E02')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure`
- ชุดข้อมูล: ชุด A
- ผ่านเมื่อ: ได้เลข COI-2569-NNNN สถานะรอพิจารณา

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยื่นแบบเปิดเผย** | — | drawer **ยื่นแบบเปิดเผยผลประโยชน์ทับซ้อน ประจำปี 2569** · stepper 3 ขั้น | ☐ |
| 2 | VERIFY การ์ด ① | — | **ข้าพเจ้า นางสาวตัวอย่าง ซื้อดี ตำแหน่ง เจ้าหน้าที่จัดซื้อ** · **ประจำปี 2569** · ถ้อยคำรับรอง | ☐ |
| 3 | CLICK การ์ด **ไม่มี** | — | การ์ดเลือก · สรุปขวา **ไม่มี** | ☐ |
| 4 | TOGGLE **ข้าพเจ้ายืนยันว่าข้อมูลข้างต้นเป็นความจริง และรับทราบถ้อยคำรับรองทั้งหมด** | — | ติ๊กแล้ว | ☐ |
| 5 | CLICK **ถัดไป** ×2 | — | ขั้น **ตรวจสอบและยืนยัน** | ☐ |
| 6 | CLICK **บันทึกและส่งพิจารณา** | — | modal **ส่งพิจารณา?** slot 1 แถว **ผู้บังคับบัญชา** = นางสาวสมมุติ ดูแลดี | ☐ |
| 7 | CLICK **ส่งพิจารณา** | — | toast **ส่งพิจารณาแล้ว · COI-2569-0012** · สถานะ **รอพิจารณา** | ☐ |

#### TC-C02 — ยื่นแบบเปิดเผย "มี" พร้อมรายละเอียด
- group: ยื่น/แก้ไข · ความสำคัญ: สูง · trace: AC-07 / BR-04 BR-08 / DEC-15
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E03')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure`
- ชุดข้อมูล: ชุด B
- ผ่านเมื่อ: ส่งได้ + แจ้งฝ่ายกฎหมาย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยื่นแบบเปิดเผย** → การ์ด **มี (กรุณาระบุรายละเอียดด้านล่าง)** | — | ช่อง **รายละเอียด*** + ป้าย **ข้อมูลลับ — เห็นเฉพาะผู้เปิดเผย ผู้พิจารณา และฝ่ายกฎหมาย/กำกับดูแล** | ☐ |
| 2 | TYPE **รายละเอียด** | ชุด B | ไม่มี error | ☐ |
| 3 | TOGGLE ยืนยัน → CLICK **ถัดไป** ×2 → **บันทึกและส่งพิจารณา** | — | modal แถบ **ตอบ "มี" — ระบบแจ้งฝ่ายกฎหมาย/กำกับดูแลให้ทราบ** | ☐ |
| 4 | CLICK **ส่งพิจารณา** → แท็บ **ประวัติ** | — | **แจ้งฝ่ายกฎหมาย/กำกับดูแล (coi_conflict_declared)** · ข้อความแจ้งเตือนไม่มีรายละเอียด | ☐ |

#### TC-C03 — การ์ดสรุปดึงจากระบบ
- group: ยื่น/แก้ไข · ความสำคัญ: กลาง · trace: BR-06 / DEC-03 DEC-04
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ผู้บังคับบัญชาและปีจากระบบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY **สรุปแบบเปิดเผย** | — | ผู้เปิดเผย นายสมมติ ใจตรง · **ผู้บังคับบัญชา** นางสาวสมมุติ ดูแลดี · ประจำปี 2569 · **ยังไม่เลือก** | ☐ |

#### TC-C04 — เปลี่ยน มี → ไม่มี ล้างรายละเอียด
- group: ยื่น/แก้ไข · ความสำคัญ: สูง · trace: AC-04 / BR-03 BR-04 / EC-01 / DEC-14 DEC-15
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E02')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เลือกได้ 1 · รายละเอียดหาย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **มี (กรุณาระบุรายละเอียดด้านล่าง)** → TYPE รายละเอียด | ญาติเป็นหุ้นส่วนบริษัทผู้ขาย | แสดงช่องรายละเอียด | ☐ |
| 2 | CLICK **ไม่มี** | — | การ์ด มี ไม่ถูกเลือก · ช่องรายละเอียดหาย | ☐ |
| 3 | CLICK **มี (กรุณาระบุรายละเอียดด้านล่าง)** | — | ช่องรายละเอียดว่าง (ถูกล้าง) | ☐ |

#### TC-C05 — มีใบปีนี้แล้ว → เตือน + แทนฉบับ [AI-DEFAULT]
- group: ยื่น/แก้ไข · ความสำคัญ: สูง · trace: AC-05 / BR-07 / EC-04 / DEC-12 DEC-17
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เตือน ไม่บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยื่นแบบเปิดเผย** | — | แถบ **คุณมีแบบเปิดเผยปี 2569 แล้ว (COI-2569-0003, COI-2569-0004) — ส่งได้ · เมื่อรับทราบ ใบนี้จะแทนฉบับ COI-2569-0003** | ☐ |
| 2 | VERIFY สรุปขวา | — | **แทนฉบับ** COI-2569-0003 | ☐ |

#### TC-C06 — แจ้งเปลี่ยนแปลงจากใบที่รับทราบแล้ว
- group: ยื่น/แก้ไข · ความสำคัญ: กลาง · trace: S-09 / DEC-17
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E02')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ใบใหม่อ้างใบเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **แจ้งเปลี่ยนแปลง** | — | drawer ยื่นใหม่ · แถบ **แทนฉบับ COI-2569-0001** · ค่า ไม่มี ยกมาจากใบเดิม | ☐ |

#### TC-C07 — บันทึกร่างโดยยังไม่เลือก
- group: ยื่น/แก้ไข · ความสำคัญ: กลาง · trace: AC-01 / FN-01 FN-03
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E02')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ร่างได้เลข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **บันทึกแบบร่าง** | — | toast **บันทึกร่างแล้ว · COI-2569-0012** · แถวใหม่ pill **ยังไม่เลือก** · **ร่าง** | ☐ |

#### TC-C08 — แก้ไขร่างเดิม
- group: ยื่น/แก้ไข · ความสำคัญ: กลาง · trace: FN-04 / U15
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R4`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เปิด wizard เดียวกัน prefill

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **แก้ไข** | — | drawer **แก้ไขแบบเปิดเผย COI-2569-0004** · การ์ด **มี** ถูกเลือก · รายละเอียด "พี่ชาย (ชื่อสมมติ)…" | ☐ |

#### TC-C09 — แนบไฟล์และไฟล์ผิดชนิด
- group: ยื่น/แก้ไข · ความสำคัญ: กลาง · trace: DEC-11
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=หนังสือรับรองบริษัท.pdf · โปรแกรม.exe
- Start: OPEN `#/coi-disclosure/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แนบได้เฉพาะชนิดที่รองรับ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ถัดไป** (หลังเลือก+ยืนยัน) → UPLOAD | หนังสือรับรองบริษัท.pdf | แถวไฟล์ 1 รายการ | ☐ |
| 2 | UPLOAD | โปรแกรม.exe | toast **โปรแกรม.exe — ชนิดไฟล์ไม่รองรับ** | ☐ |

#### TC-C10 — ปิดตอนกรอกค้าง
- group: ยื่น/แก้ไข · ความสำคัญ: ต่ำ · trace: U9 / U25
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ถามก่อนทิ้ง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ไม่มี** → CLICK ปุ่ม X | — | modal **ทิ้งข้อมูลที่กรอกไว้?** | ☐ |
| 2 | CLICK **กลับไปกรอกต่อ** | — | ยังอยู่ใน drawer ค่าเดิม | ☐ |

### กลุ่ม: ตรวจความถูกต้อง

#### TC-V01 — ไม่เลือกและไม่ยืนยัน = บล็อก
- group: ตรวจความถูกต้อง · ความสำคัญ: สูง · trace: AC-02 / VR-01 VR-03 / BR-05 / CHOICE_REQUIRED CONFIRM_REQUIRED
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: error ที่การ์ด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ถัดไป** | — | toast **กรุณากรอกข้อมูลให้ครบถ้วน** · **กรุณาเลือก ไม่มี หรือ มี** · **กรุณายืนยันถ้อยคำรับรองก่อนส่ง** · การ์ดขอบแดง | ☐ |

#### TC-V02 — มี + รายละเอียดสั้น = บล็อก
- group: ตรวจความถูกต้อง · ความสำคัญ: สูง · trace: AC-03 / VR-02 / EC-02 / DETAIL_REQUIRED / DEC-15
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ช่องรายละเอียดแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **มี (กรุณาระบุรายละเอียดด้านล่าง)** → TYPE รายละเอียด | สั้น | — | ☐ |
| 2 | TOGGLE ยืนยัน → CLICK **ถัดไป** | — | **ระบุรายละเอียดอย่างน้อย 10 ตัวอักษร** · ช่องขอบแดง | ☐ |
| 3 | TYPE รายละเอียด | ชุด B | ขอบแดงหาย | ☐ |

#### TC-V03 — ส่งร่างที่ยังไม่ยืนยันจากหน้าดู
- group: ตรวจความถูกต้อง · ความสำคัญ: สูง · trace: AC-14 / VR-06 / EC-03 / CONFIRM_REQUIRED
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R4`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เตือน + เปิดแก้ไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งพิจารณา** | — | toast **เลือก ไม่มี/มี กรอกรายละเอียด และยืนยันถ้อยคำรับรองก่อนส่ง** → เปิด drawer แก้ไข | ☐ |

#### TC-V04 — ไม่เลือกผู้พิจารณา
- group: ตรวจความถูกต้อง · ความสำคัญ: กลาง · trace: VR-04 / ASSIGNEE_REQUIRED / EC-05
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R4`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อกจนเลือก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **แก้ไข** → TOGGLE ยืนยัน → **ถัดไป** ×2 → **บันทึกและส่งพิจารณา** | — | modal slot **ผู้บังคับบัญชา** | ☐ |
| 2 | CLICK ปุ่ม x ใน slot → CLICK **ส่งพิจารณา** | — | **กรุณาเลือกผู้พิจารณา** | ☐ |

#### TC-V05 — เหตุผลบังคับเมื่อส่งกลับ/ยกเลิก
- group: ตรวจความถูกต้อง · ความสำคัญ: สูง · trace: VR-05 / REASON_REQUIRED
- actor (role): ผู้บังคับบัญชา
- Setup: role=ผู้บังคับบัญชา (__QA__.setMe('E05')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อกเมื่อว่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งกลับแก้ไข** → CLICK **ส่งกลับแก้ไข** ใน modal | (ว่าง) | **กรุณาระบุเหตุผล** | ☐ |

### กลุ่ม: ส่งและรับทราบ

#### TC-S01 — ผู้บังคับบัญชารับทราบพร้อมข้อคิดเห็น
- group: ส่งและรับทราบ · ความสำคัญ: สูง · trace: AC-08 / FN-06 / BR-15 / DEC-07
- actor (role): ผู้บังคับบัญชา
- Setup: role=ผู้บังคับบัญชา (__QA__.setMe('E05')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: รับทราบแล้ว + ข้อคิดเห็นใน PDF

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว | — | **ส่งกลับแก้ไข** · **รับทราบ** | ☐ |
| 2 | CLICK **รับทราบ** → TYPE **ข้อคิดเห็นของผู้บังคับบัญชา** | รับทราบ ให้งดร่วมพิจารณาผู้ขายรายนี้ | — | ☐ |
| 3 | CLICK **รับทราบ** ใน modal | — | toast **รับทราบ · COI-2569-0006** · สถานะ **รับทราบแล้ว** | ☐ |
| 4 | CLICK แท็บ **PDF Preview** | — | กรอบ ข้อคิดเห็นของผู้บังคับบัญชา: **ผู้บังคับบัญชา : รับทราบ ให้งดร่วมพิจารณาผู้ขายรายนี้** · ☑ รับทราบ | ☐ |

#### TC-S02 — ผู้เปิดเผยไม่อยู่ในรายชื่อผู้พิจารณา
- group: ส่งและรับทราบ · ความสำคัญ: สูง · trace: BR-DOA-04 / SELF_APPROVAL
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R4`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เลือกตัวเองไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **แก้ไข** → TOGGLE ยืนยัน → **ถัดไป** ×2 → **บันทึกและส่งพิจารณา** → CLICK slot | — | รายชื่อไม่มี นายสมมติ ใจตรง | ☐ |

#### TC-S03 — DOA กลางเพิ่มขั้นฝ่ายกฎหมาย [AI-DEFAULT]
- group: ส่งและรับทราบ · ความสำคัญ: สูง · trace: AC-11 / BR-09 BR-14 / EC-06 / DEC-03 DEC-13
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure`
- ชุดข้อมูล: —
- ผ่านเมื่อ: slot และช่องลงชื่อเพิ่มตาม DOA

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console `__QA__.doa.push('ฝ่ายกฎหมาย')` → ยื่นใบใหม่ (ชุด A) → **บันทึกและส่งพิจารณา** | — | modal slot 2 แถว **ผู้บังคับบัญชา** · **ฝ่ายกฎหมาย** (นางสาวทดสอบ กำกับงาน) | ☐ |
| 2 | CLICK **ส่งพิจารณา** → แท็บ **PDF Preview** | — | แถวลงชื่อ 3 ช่อง: ผู้เปิดเผย (ลงชื่อ) · ผู้บังคับบัญชา · ฝ่ายกฎหมาย | ☐ |

#### TC-S04 — ส่ง/ตัดสินชนกัน (stale)
- group: ส่งและรับทราบ · ความสำคัญ: ต่ำ · trace: EC-08 / STALE
- actor (role): ผู้บังคับบัญชา
- Setup: role=ผู้บังคับบัญชา (__QA__.setMe('E05')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่เปลี่ยนสถานะ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console `__QA__.sim('stale')` → CLICK **รับทราบ** → **รับทราบ** | — | toast **ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่** · สถานะยัง **รอพิจารณา** | ☐ |

#### TC-S05 — รับทราบใบใหม่ → ใบเดิมถูกแทนที่
- group: ส่งและรับทราบ · ความสำคัญ: สูง · trace: AC-08 / BR-07 / DEC-17
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R4`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ใบเดิมมี pill ถูกแทนที่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **แก้ไข** → TOGGLE ยืนยัน → **ถัดไป** ×2 → **บันทึกและส่งพิจารณา** → **ส่งพิจารณา** | — | สถานะ **รอพิจารณา** | ☐ |
| 2 | PRESS console `__QA__.setMe('E05')` → OPEN `#/coi-disclosure/view/R4` → CLICK **รับทราบ** → **รับทราบ** | — | สถานะ **รับทราบแล้ว** | ☐ |
| 3 | OPEN `#/coi-disclosure/view/R3` | — | pill **ถูกแทนที่** · แถบ **ใบนี้ถูกแทนที่ด้วย COI-2569-0004** | ☐ |

### กลุ่ม: ส่งกลับแก้ไข

#### TC-R01 — ส่งกลับแก้ไข = กลับร่างเลขเดิม
- group: ส่งกลับแก้ไข · ความสำคัญ: สูง · trace: AC-09 / FN-07 / BR-10 BR-DOA-03 / DEC-08
- actor (role): ผู้บังคับบัญชา
- Setup: role=ผู้บังคับบัญชา (__QA__.setMe('E05')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: returned เลขเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งกลับแก้ไข** → CLICK chip **โปรดระบุชื่อบุคคล/กิจการ และความสัมพันธ์ให้ครบ** → **ส่งกลับแก้ไข** | — | toast **ส่งกลับแก้ไขแล้ว · COI-2569-0006** · สถานะ **ส่งกลับแก้ไข** เลขเดิม | ☐ |

#### TC-R02 — ผู้เปิดเผยเห็นเหตุผลและแก้ส่งใหม่
- group: ส่งกลับแก้ไข · ความสำคัญ: สูง · trace: AC-09 / FN-07 / DEC-08
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E03')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แก้แล้วส่งใหม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถบ | — | **ส่งกลับแก้ไข — โปรดระบุชื่อบุคคล/กิจการ และความสัมพันธ์ให้ครบ · แก้แล้วส่งพิจารณาใหม่ได้ (เลขที่เดิม)** | ☐ |
| 2 | CLICK **แก้ไข** → TYPE รายละเอียด | ชุด B | — | ☐ |
| 3 | CLICK **ถัดไป** ×2 → **บันทึกและส่งพิจารณา** → **ส่งพิจารณา** | — | สถานะ **รอพิจารณา** · เลขที่ COI-2569-0007 เดิม | ☐ |

### กลุ่ม: ยกเลิก

#### TC-X01 — เจ้าของยกเลิกร่าง
- group: ยกเลิก · ความสำคัญ: สูง · trace: AC-12 / FN-08 / DEC-08
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R4`
- ชุดข้อมูล: —
- ผ่านเมื่อ: cancelled

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยกเลิก** → TYPE เหตุผล | ยื่นซ้ำโดยไม่ได้ตั้งใจ | — | ☐ |
| 2 | CLICK **ยกเลิกเอกสาร** | — | toast **ยกเลิกเอกสารแล้ว · COI-2569-0004** · สถานะ **ยกเลิก** | ☐ |

#### TC-X02 — ฝ่ายกฎหมายยกเลิกใบรอพิจารณา
- group: ยกเลิก · ความสำคัญ: กลาง · trace: AC-12 / FN-08 FN-10 / coi_cancelled
- actor (role): ฝ่ายกฎหมาย/กำกับดูแล
- Setup: role=ฝ่ายกฎหมาย/กำกับดูแล (__QA__.setMe('E07')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R5`
- ชุดข้อมูล: —
- ผ่านเมื่อ: cancelled + แจ้งผู้พิจารณา

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยกเลิกเอกสาร** → TYPE เหตุผล → **ยกเลิกเอกสาร** | ยื่นผิดคน | สถานะ **ยกเลิก** (BE: coi_cancelled ถึงผู้พิจารณาขั้นปัจจุบัน) | ☐ |

#### TC-X03 — ใบรับทราบแล้วยกเลิกไม่ได้
- group: ยกเลิก · ความสำคัญ: กลาง · trace: BR-11 / NOT_CANCELLABLE
- actor (role): ฝ่ายกฎหมาย/กำกับดูแล
- Setup: role=ฝ่ายกฎหมาย/กำกับดูแล (__QA__.setMe('E07')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว drawer | — | ไม่มี **ยกเลิกเอกสาร** · footer **รับทราบแล้ว ล็อกแก้ไข** | ☐ |

### กลุ่ม: สิทธิ์

#### TC-P01 — ผู้บังคับบัญชาไม่เห็นร่างของลูกน้อง
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D01 / DEC-09 / NOT_FOUND
- actor (role): ผู้บังคับบัญชา
- Setup: role=ผู้บังคับบัญชา (__QA__.setMe('E05')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R9`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่เห็นร่าง ไม่เปิด drawer

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/coi-disclosure/view/R9` | — | ไม่เปิด drawer · รายการไม่มี COI-2569-0009 | ☐ |

#### TC-P02 — ผู้เปิดเผยไม่เห็นใบคนอื่น
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D02 / DEC-16
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่พบใบคนอื่น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE ช่องค้นหา | COI-2569-0006 | **ไม่พบรายการที่ค้นหา** | ☐ |

#### TC-P03 — ผู้จัดการฝ่ายจัดซื้อไม่เห็นทั้งหมดโดยตำแหน่ง [AI-DEFAULT]
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D03 / DEC-09 DEC-16 / EC-11
- actor (role): ผู้จัดการฝ่ายจัดซื้อ
- Setup: role=ผู้จัดการฝ่ายจัดซื้อ (__QA__.setMe('E06')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นเฉพาะใบที่ตนพิจารณา

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตาราง | — | 3 แถว: COI-2569-0010 · 0008 · 0005 (ไม่เห็น 0002 ที่ตอบ มี) | ☐ |
| 2 | OPEN `#/coi-disclosure/view/R2` | — | ไม่เปิด drawer (ไม่มีสิทธิ์) | ☐ |

#### TC-P04 — ผู้อยู่ในสายแต่ไม่ใช่ขั้นปัจจุบันตัดสินไม่ได้
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: TC-D04 / NOT_CURRENT_APPROVER
- actor (role): ผู้บังคับบัญชา
- Setup: role=ผู้บังคับบัญชา (__QA__.setMe('E05')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มตัดสิน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว | — | ไม่มี **รับทราบ** / **ส่งกลับแก้ไข** | ☐ |

#### TC-P05 — แก้ใบที่ไม่ใช่ร่างไม่ได้
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: TC-D06 / NOT_EDITABLE NOT_OWNER
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E02')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มแก้ไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว | — | ไม่มี **แก้ไข** · มี **ยกเลิกเอกสาร** | ☐ |

#### TC-P06 — ฝ่ายกฎหมาย/กำกับดูแลเห็นทุกใบ [AI-DEFAULT]
- group: สิทธิ์ · ความสำคัญ: สูง · trace: AC-13 / DEC-09
- actor (role): ฝ่ายกฎหมาย/กำกับดูแล
- Setup: role=ฝ่ายกฎหมาย/กำกับดูแล (__QA__.setMe('E07')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 11 ใบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY badge | — | **11 รายการ** | ☐ |
| 2 | OPEN `#/coi-disclosure/view/R2` | — | แท็บรายละเอียดเห็น **คู่สมรส (ชื่อสมมติ)…** + ป้ายข้อมูลลับ | ☐ |

#### TC-P07 — คนนอกสายยกเลิกไม่ได้
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: TC-D05 / NOT_OWNER
- actor (role): ผู้บังคับบัญชา
- Setup: role=ผู้บังคับบัญชา (__QA__.setMe('E05')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R10`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เฉพาะเจ้าของ/compliance

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัวของใบตัวเอง COI-2569-0010 (รอพิจารณา) | — | มี **ยกเลิกเอกสาร** (เจ้าของ) | ☐ |
| 2 | PRESS console `__QA__.setMe('E06')` → OPEN `#/coi-disclosure/view/R10` | — | มี **ส่งกลับแก้ไข** · **รับทราบ** · ไม่มี **ยกเลิกเอกสาร** | ☐ |

#### TC-P08 — ไม่มีสิทธิ์ทำรายการ (403)
- group: สิทธิ์ · ความสำคัญ: ต่ำ · trace: TC-D09 / 403
- actor (role): ผู้บังคับบัญชา
- Setup: role=ผู้บังคับบัญชา (__QA__.setMe('E05')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่เปลี่ยนสถานะ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console `__QA__.sim('denied')` → CLICK **รับทราบ** → **รับทราบ** | — | toast **คุณไม่มีสิทธิ์ทำรายการนี้** | ☐ |

### กลุ่ม: PDF/พิมพ์

#### TC-D01 — PDF ตรงแบบฟอร์ม FM-PUR-04
- group: PDF/พิมพ์ · ความสำคัญ: สูง · trace: AC-10 / FN-09 / BR-16 / DEC-05 DEC-06 DEC-18
- actor (role): ฝ่ายกฎหมาย/กำกับดูแล
- Setup: role=ฝ่ายกฎหมาย/กำกับดูแล (__QA__.setMe('E07')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R2`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ถ้อยคำตามกระดาษ 1 หน้า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | **ตัวอย่าง PDF · A4 1 หน้า** · หัว **แบบฟอร์มเปิดเผยผลประโยชน์ทับซ้อนของแผนกจัดซื้อ** / **ประจำปี 2569** | ☐ |
| 2 | VERIFY เนื้อหา | — | **ข้าพเจ้า นาย/นาง/นางสาว** · ย่อหน้ารับรอง · ☐ ไม่มี ☑ มี · **รายละเอียด** + เส้นประ 3 บรรทัด · กรอบ **ข้อคิดเห็นของผู้บังคับบัญชา** · DOC.No. : FM-PUR-04 · REV.00 : 01/07/2569 | ☐ |

#### TC-D02 — ปีบนแบบพิมพ์เป็นตัวแปร
- group: PDF/พิมพ์ · ความสำคัญ: สูง · trace: AC-10 AC-15 / BR-01 BR-02 / DEC-04 DEC-12
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R11`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่ hardcode 2569

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | หัว **ประจำปี 2568** · เลขที่ COI-2568-0011 | ☐ |

#### TC-D03 — ลายเซ็นผูก role · ช่องตาม DOA
- group: PDF/พิมพ์ · ความสำคัญ: สูง · trace: AC-11 / BR-14 / DEC-07
- actor (role): ฝ่ายกฎหมาย/กำกับดูแล
- Setup: role=ฝ่ายกฎหมาย/กำกับดูแล (__QA__.setMe('E07')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: คำตัดสินถูกคน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | 2 ช่อง: **ผู้เปิดเผย (ลงชื่อ)** "ส่งในระบบ …" · **ผู้บังคับบัญชา** ☑ รับทราบ ☐ ส่งกลับแก้ไข "พิจารณาในระบบ …" | ☐ |

#### TC-D04 — ร่างแสดงช่องว่าง
- group: PDF/พิมพ์ · ความสำคัญ: กลาง · trace: FN-09
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R4`
- ชุดข้อมูล: —
- ผ่านเมื่อ: footer ร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | footer **เลขที่ COI-2569-0004 · ร่าง · แทนฉบับ COI-2569-0003 · เอกสารลับ** · ช่องวันที่ **วันที่ ........./........./.........** | ☐ |

#### TC-D05 — พิมพ์/ดาวน์โหลด
- group: PDF/พิมพ์ · ความสำคัญ: ต่ำ · trace: S-10
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E01')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เปิดหน้าต่างพิมพ์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ดาวน์โหลด PDF** | — | toast **เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ · COI-2569-0003** | ☐ |

### กลุ่ม: Cross-Module

#### TC-XT01 — แจ้งฝ่ายกฎหมายเมื่อตอบ มี
- group: Cross-Module · ความสำคัญ: สูง · trace: XT-01 / BR-08
- actor (role): ฝ่ายกฎหมาย/กำกับดูแล
- Setup: role=ฝ่ายกฎหมาย/กำกับดูแล (__QA__.setMe('E07')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: event ไม่มีรายละเอียด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **ประวัติ** | — | **แจ้งฝ่ายกฎหมาย/กำกับดูแล (coi_conflict_declared)** · **ข้อความแจ้งเตือนไม่มีรายละเอียด (ข้อมูลลับ)** | ☐ |

#### TC-XT02 — รับทราบแล้วเก็บ PDF
- group: Cross-Module · ความสำคัญ: กลาง · trace: XT-02 / FN-06
- actor (role): ผู้จัดการฝ่ายจัดซื้อ
- Setup: role=ผู้จัดการฝ่ายจัดซื้อ (__QA__.setMe('E06')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R5`
- ชุดข้อมูล: —
- ผ่านเมื่อ: approved_final

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **รับทราบ** → **รับทราบ** | — | สถานะ **รับทราบแล้ว** (BE: ENG-DOC-STORE approved_final — ตรวจที่ระบบจริง) | ☐ |

#### TC-XT03 — ไม่ส่งต่อทะเบียน/Vendor master รอบนี้ [AI-DEFAULT]
- group: Cross-Module · ความสำคัญ: ต่ำ · trace: XT-03 / BR-12 / DEC-01 DEC-02
- actor (role): ฝ่ายกฎหมาย/กำกับดูแล
- Setup: role=ฝ่ายกฎหมาย/กำกับดูแล (__QA__.setMe('E07')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/view/R2`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีการเปลี่ยนค่า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ประวัติ | — | ไม่มีรายการส่งต่อ (coi.disclosure_acknowledged ไม่ยิง) | ☐ |

#### TC-XT04 — DOA resolve ผู้บังคับบัญชาจากผังองค์กร
- group: Cross-Module · ความสำคัญ: กลาง · trace: XT-04 / FN-05
- actor (role): ผู้เปิดเผย
- Setup: role=ผู้เปิดเผย (__QA__.setMe('E04')) · seed=prototype 11 ใบ (COI-2569-0001..0010 · COI-2568-0011) · วันนี้ 10 ต.ค. 2569 · files=—
- Start: OPEN `#/coi-disclosure/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: slot = mgr ของผู้ส่ง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยื่นแบบเปิดเผย** → กรอกชุด A → **บันทึกและส่งพิจารณา** | — | slot **ผู้บังคับบัญชา** = นายตัวอย่าง บริหารซื้อ (mgr ของ E04) | ☐ |

## Coverage Audit
| หมวด | covered / total |
|---|---|
| FR (06_TESTS AC) | 15 / 15 |
| Business rules (05_RULES) | 20 / 20 |
| Validation rules | 6 / 6 |
| Edge cases | 9 / 12 |
| Error codes | 13 / 13 |
| Permission cells | 15 / 15 |
| Cross-cutting / states | 7 / 8 |

- Cross-Module (XT): 4/4
- Scope Lock (DEC): 18/18
- **Manifest cross-check (FRD §0.12): ✅ 6/6** (ช่องในฟอร์ม · ตัวเลือก · ค่าคงที่ · ลายเซ็น · Doc No. · DEC)

### ข้าม (พร้อมเหตุผล)
- EC-07 · EC-10 · EC-12 — ทดสอบที่ BE/ไม่มีหน้าจอใน prototype (เช่น แก้ DOA ระหว่างรอ · config เปลี่ยนกลางปี · รายละเอียดยาวใน PDF ดูที่ print/long-12lines)
- BR-DOA-05 — ไม่มีวงเงิน (DEC-03)
- upload_fail — ความสำคัญต่ำ (hook มีใน prototype)

## Result Report (schema)
```json
{
  "feature_id": "F-TMP-006",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 50, "pass": 0, "fail": 0, "blocked": 0 }
}
```

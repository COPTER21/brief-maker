# AI Test Cases — F-TMP-003 แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี

ชุดทดสอบสำหรับ AI agent (browser-use/vision) รันบน prototype `feature.html` — anchor = ข้อความที่เห็นบนจอ (ตัวหนา) · ข้อมูลตัวอย่างทั้งหมดเป็นชื่อสมมติ · เคสที่ติด `[AI-DEFAULT]` = เกณฑ์มาจากมติที่ AI ตัดสินแทน (รอลูกค้าเซ็นยืนยัน OQ-02) ถ้า fail อาจแปลว่ามติผิด ไม่ใช่โค้ดผิด · เคส `(auto: e2e S#)` มีชุดอัตโนมัติ e2e_standard.py คู่กัน

## Meta
| Field | Value |
|---|---|
| Feature ID | F-TMP-003 |
| ชื่อ | แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี (FM-ACC-01) |
| เวอร์ชัน | v1.0 (2026-10-11) |
| App entry | feature.html |
| Routes | `#/account-code-request` · `#/account-code-request/create` · `#/account-code-request/edit/:id` · `#/account-code-request/view/:id` |
| ที่มา | FRD_F-TMP-003_Pack (FULL) · BRD-ACC-ACR-001 · HTML · DECISIONS.lock (14 DEC) |
| จำนวนเคส | 62 |
| ตัวสลับผู้ใช้ | มุมขวาบน: กิตติ ศรีสุข (ผู้ขอ · E01) · วรวุฒิ ทองดี (ผู้ตรวจสอบ · E05) · มานี รักษ์ทรัพย์ (ผู้อนุมัติ · E02) · ศศิธร มีสุข (admin บัญชี · E08) · หรือ console `__QA__.setMe('E0x')` |

## Coverage
| group | เคส | สูง/กลาง/ต่ำ |
|---|---|---|
| รายการ | 11 | 3/4/4 |
| สร้าง | 14 | 8/5/1 |
| ส่ง/อนุมัติ | 10 | 6/4/0 |
| บันทึกเข้าระบบ | 4 | 2/2/0 |
| ยกเลิก | 3 | 1/2/0 |
| PDF | 5 | 1/3/1 |
| สิทธิ์ | 7 | 3/4/0 |
| ข้อผิดพลาด | 3 | 0/3/0 |
| UX | 2 | 0/0/2 |
| Cross-module | 3 | 0/2/1 |

## Coverage Ledger
### AC (06_TESTS)
| item | cases |
|---|---|
| AC-01 | TC-C01 |
| AC-02 | TC-C02 |
| AC-03 | TC-C04 |
| AC-04 | TC-C07 |
| AC-05 | TC-C08, TC-F03 |
| AC-06 | TC-C09 |
| AC-07 | TC-L06, TC-A01 |
| AC-08 | TC-A05, TC-A06 |
| AC-09 | TC-A08 |
| AC-10 | TC-L07, TC-R01 |
| AC-11 | TC-F01, TC-F02 |
| AC-12 | TC-X01, TC-X02, TC-X03 |
| AC-13 | TC-L01, TC-P03 |
| AC-14 | TC-A04, TC-A09, TC-F05 |
| AC-15 | TC-E03 |
### Business Rules (05_RULES)
| rule | cases |
|---|---|
| BR-01 | TC-L08, TC-C09 |
| BR-02 | TC-C03, TC-C04, TC-C06 |
| BR-03 | TC-C07 |
| BR-04 | TC-C08, TC-F03 |
| BR-05 | TC-A08, TC-T01 |
| BR-06 | TC-L09, TC-C11 |
| BR-07 | TC-A07 |
| BR-08 | TC-C01 |
| BR-09 | TC-R01, TC-X01, TC-X03, TC-P06 |
| BR-10 | TC-A04, TC-A09, TC-A10, TC-F01, TC-F05 |
| BR-11 | TC-R01, TC-R02 |
| BR-12 | TC-L01, TC-P01, TC-P02, TC-P07 |
| BR-13 | TC-T02 |
| BR-DOA-01 | TC-A01 |
| BR-DOA-02 | TC-A05, TC-P04 |
| BR-DOA-03 | TC-C14, TC-A08 |
| BR-DOA-04 | TC-A03 |
| BR-DOA-05 | — ข้าม (ไม่มีวงเงิน DEC-03) |
### Validation
| VR | cases |
|---|---|
| VR-01 | TC-C02 |
| VR-02 | TC-C03 |
| VR-03 | TC-C04 |
| VR-04 | TC-C08 |
| VR-05 | TC-C07 |
| VR-06 | TC-C08 |
| VR-07 | TC-A02, TC-A03 |
| VR-08 | TC-A07, TC-X01 |
| VR-09 | TC-R02 |
### Edge Cases
| EC | cases |
|---|---|
| EC-01 | TC-C09 |
| EC-02 | TC-C06 |
| EC-03 | — ข้าม (ทดสอบระดับ API (resolve ข้ามตัวเอง)) |
| EC-04 | — ข้าม (ต้องแก้ DOA กลาง ทดสอบระดับ API) |
| EC-05 | TC-E01, TC-E02 |
| EC-06 | TC-E03 |
| EC-07 | — ข้าม (นอกขอบเขต DEC-01 / OQ-04) |
| EC-08 | — ข้าม (PDF 2 หน้า ตรวจในแบบพิมพ์ (.build/long-12rows-doa6steps)) |
| EC-09 | TC-L07 |
### Error Codes
| error | cases |
|---|---|
| NOT_FOUND | TC-P01 |
| NOT_CURRENT_APPROVER | TC-P04 |
| NOT_OWNER | TC-P05 |
| SELF_APPROVAL | TC-A03 |
| NOT_RECORDER | TC-R03 |
| NOT_APPROVED | TC-R04 |
| NOT_CANCELLABLE | TC-X03 |
| ASSIGNEE_REQUIRED | TC-A02 |
| REASON_REQUIRED | TC-A07, TC-X01 |
| STALE | TC-E02 |
| DOC_TYPE_INACTIVE | TC-E03 |
### Permission Matrix (role × action)
| cell | cases |
|---|---|
| ผู้อนุมัติ ดู draft คนอื่น = deny | TC-P01 |
| owner ดู draft คนอื่น = deny | TC-P02 |
| admin ดูทั้งหมด = allow | — ข้าม () |
| ผู้พิจารณาไม่ใช่ขั้นปัจจุบัน ตัดสิน = deny | TC-P04 |
| ผู้อนุมัติ ยกเลิก = deny | TC-P05 |
| ผู้อนุมัติ บันทึกเข้าระบบ = deny | TC-R03 |
| admin บันทึกเข้าระบบ = allow | TC-L07, TC-R01 |
| admin ยกเลิก = allow | — ข้าม () |
| ผู้ตรวจสอบ เห็นเฉพาะใบในสาย | — ข้าม () |
### Cross-Module (XT — 06_TESTS §6.9)
| XT | Downstream | Case |
|---|---|---|
| XT-01 | ENG-NOTIFY (acr_cancelled · acr_ready_to_record · acr_recorded) | TC-A06, TC-R01, TC-X02, TC-T02 |
| XT-02 | ENG-DOC-STORE approved_final | TC-T03 |
| XT-03 | COA ไม่ส่งต่อ | TC-T01 |
### Scope Lock (DEC — 07 §7.0)
| DEC | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| DEC-01 | ไม่เปลี่ยนค่าในระบบ | TC-R01, TC-T01 |
| DEC-02 | ไม่ส่งต่อ | TC-T01 |
| DEC-03 | DOA dynamic 2 ขั้น | TC-C10, TC-A01, TC-A04, TC-F05 |
| DEC-04 | กฎตรวจ | TC-C03 |
| DEC-05 | ไม่จำกัดแถว | TC-C05, TC-C06 |
| DEC-06 | 1:1 | TC-F01 |
| DEC-07 | ลายเซ็นแถวล่าง | TC-A10, TC-F01, TC-F05 |
| DEC-08 | ไม่อนุมัติ→ร่าง | TC-C14, TC-A08, TC-X01 |
| DEC-09 | การมองเห็น | TC-L01, TC-P01, TC-P03, TC-P07 |
| DEC-10 | เลข ACR | TC-C01 |
| DEC-11 | แนบ/CSV · ไม่มีทำซ้ำ | TC-L09, TC-C11, TC-C12 |
| DEC-12 | ป้ายวัตถุประสงค์ในการยกเลิก | TC-C08, TC-F03 |
| DEC-13 | 1 ใบ 1 ประเภท | TC-C09 |
| DEC-14 | ไม่อนุมัติต้องมีเหตุผล | TC-A07 |
### Coverage Manifest (FRD §0.12)
| แถว | cases |
|---|---|
| ช่องในฟอร์ม F01–F13 | 0 เคส |
| ลายเซ็น S1–S4 | 0 เคส |
| BRD S-01..S-14 | 15 เคส |
| BR/VR/EC | 44 เคส |
| DEC-01..14 | 26 เคส |
| declaration | 7 เคส |
| หน้าจอ P-01..03 M-01..06 | 14 เคส |

## Data Sets
| ชุด | ฟิลด์ | ค่า |
|---|---|---|
| A | ชื่อบัญชีที่ต้องการขอเพิ่ม (A.name1 · A.name2) · วัตถุประสงค์ในการเพิ่ม (A.purpose) | รายได้ค่าบริการทดสอบ · ต้นทุนบริการทดสอบ · แยกรายได้งานบริการ |
| B | รหัสบัญชี · แก้ไขเป็น · วัตถุประสงค์ในการแก้ไข | 5210-01 · ค่าซ่อมแซมอาคาร · แยกต้นทุน |
| D | ชื่อบัญชี 2 บรรทัดซ้ำ · วัตถุประสงค์ | รายได้ทดสอบ + รายได้ทดสอบ · ทดสอบซ้ำ |
### ไฟล์ทดสอบ (Files)
| ไฟล์ | ใช้ใน |
|---|---|
| รายงานเคลื่อนไหวบัญชี.pdf (≤1 MB) | TC-C11 |
| โปรแกรม.exe | TC-C12 |

## Test Cases

### กลุ่ม: รายการ

#### TC-L01 — รายการแสดงตามสิทธิ์ของผู้ขอ (auto: e2e S2/S3)
- group: รายการ · ความสำคัญ: สูง · trace: AC-13 / BR-12 / FN-10 / DEC-09
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 5 แถว ไม่มี ACR-2569-0008

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/account-code-request` | — | หัว **แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี** + badge **5 รายการ** | ☐ |
| 2 | VERIFY แถวในตาราง | — | 5 แถว: ACR-2569-0007, 0006, 0005, 0003, 0001 | ☐ |
| 3 | VERIFY ไม่มีแถว ACR-2569-0008 | — | ไม่พบ ACR-2569-0008 (ร่างของคนอื่น) | ☐ |
| 4 | VERIFY ใต้หัวหน้า | — | ไม่มี stat card (มีแค่ badge ข้างชื่อ) | ☐ |

#### TC-L02 — ค้นหาด้วยรหัสบัญชี
- group: รายการ · ความสำคัญ: กลาง · trace: 01_UI P-01 / FN-10
- actor (role): admin
- Setup: role=admin บัญชี (ศศิธร มีสุข · __QA__.setMe('E08')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เหลือแถวที่มีรหัส 5390-09

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/account-code-request` | — | badge **11 รายการ** | ☐ |
| 2 | TYPE → ช่อง **ค้นหาเลขที่ / ผู้ขอ / รหัสหรือชื่อบัญชี** | 5390-09 | ตารางกรองทันที | ☐ |
| 3 | VERIFY แถว | — | เหลือ ACR-2569-0003 แถวเดียว | ☐ |

#### TC-L03 — กรองสถานะ = บันทึกเข้าระบบแล้ว
- group: รายการ · ความสำคัญ: กลาง · trace: 01_UI P-01 / FN-10
- actor (role): admin
- Setup: role=admin บัญชี (ศศิธร มีสุข · __QA__.setMe('E08')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เหลือ 2 แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง **ทุกสถานะ** | — | ตัวเลือก ร่าง · รออนุมัติ · อนุมัติแล้ว · รอบันทึก · บันทึกเข้าระบบแล้ว · ยกเลิก | ☐ |
| 2 | SELECT **บันทึกเข้าระบบแล้ว** | — | เหลือ ACR-2569-0010, 0001 · pill **บันทึกเข้าระบบแล้ว** | ☐ |

#### TC-L04 — กรองประเภทคำขอ + ล้างตัวกรอง
- group: รายการ · ความสำคัญ: กลาง · trace: 01_UI P-01 / S-13
- actor (role): admin
- Setup: role=admin บัญชี (ศศิธร มีสุข · __QA__.setMe('E08')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: กรองแล้วล้างกลับ 11 แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง **ทุกประเภทคำขอ** → SELECT **ยกเลิกรหัสบัญชี** | — | เหลือ ACR-2569-0010, 0008, 0003 · pill **ยกเลิกรหัสบัญชี** | ☐ |
| 2 | CLICK ปุ่ม **ล้างตัวกรอง** | — | กลับเป็น 11 แถว | ☐ |

#### TC-L05 — ค้นหาไม่เจอ = empty state
- group: รายการ · ความสำคัญ: ต่ำ · trace: U23 / 01_UI §1.6
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นแผง ไม่พบรายการที่ค้นหา

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่อง **ค้นหาเลขที่ / ผู้ขอ / รหัสหรือชื่อบัญชี** | zzzz | ตารางว่าง | ☐ |
| 2 | VERIFY แผงในตาราง | — | **ไม่พบรายการที่ค้นหา** + ปุ่ม **ล้างตัวกรอง** | ☐ |

#### TC-L06 — badge รอฉันพิจารณา ของผู้อนุมัติ
- group: รายการ · ความสำคัญ: สูง · trace: AC-07 / FN-10
- actor (role): ผู้อนุมัติ
- Setup: role=ผู้อนุมัติ (มานี รักษ์ทรัพย์ · __QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: badge รอฉันพิจารณา 1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/account-code-request` | — | badge **8 รายการ** | ☐ |
| 2 | VERIFY badge ข้างชื่อหน้า | — | **รอฉันพิจารณา 1** | ☐ |

#### TC-L07 — badge รอบันทึกเข้าระบบ ของ admin
- group: รายการ · ความสำคัญ: สูง · trace: EC-09 / AC-10 / FN-10
- actor (role): admin
- Setup: role=admin บัญชี (ศศิธร มีสุข · __QA__.setMe('E08')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: badge รอบันทึกเข้าระบบ 2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY badge ข้างชื่อหน้า | — | **รอบันทึกเข้าระบบ 2** | ☐ |
| 2 | VERIFY สถานะ ACR-2569-0011 และ ACR-2569-0002 | — | pill **อนุมัติแล้ว · รอบันทึก** | ☐ |

#### TC-L08 — คอลัมน์ประเภทคำขอ + รหัส / ชื่อบัญชี
- group: รายการ · ความสำคัญ: กลาง · trace: 01_UI P-01 / BR-01
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แสดงสรุปตามประเภท

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถว ACR-2569-0007 | — | pill **แก้ไขรหัสบัญชี** · 4110-03 → รายได้ค่าขนส่งเรียกเก็บลูกค้า | ☐ |
| 2 | VERIFY แถว ACR-2569-0006 | — | pill **เพิ่มรหัสบัญชี** · เงินมัดจำค่าเช่าคลังสินค้า +1 | ☐ |
| 3 | VERIFY แถว ACR-2569-0003 | — | pill **ยกเลิกรหัสบัญชี** · 5390-09 ค่าใช้จ่ายเบ็ดเตล็ดอื่น (เดิม) | ☐ |

#### TC-L09 — ส่งออก CSV
- group: รายการ · ความสำคัญ: ต่ำ · trace: S-14 / DEC-11 / BR-06
- actor (role): admin
- Setup: role=admin บัญชี (ศศิธร มีสุข · __QA__.setMe('E08')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: toast ส่งออก 11 เอกสาร

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งออก CSV** | — | ไฟล์ account-code-request.csv ถูกดาวน์โหลด | ☐ |
| 2 | WAIT toast | — | **ส่งออก 11 เอกสาร** | ☐ |

#### TC-L10 — เปลี่ยนจำนวนต่อหน้า + pager
- group: รายการ · ความสำคัญ: ต่ำ · trace: U6
- actor (role): admin
- Setup: role=admin บัญชี (ศศิธร มีสุข · __QA__.setMe('E08')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: 10 ต่อหน้า = 2 หน้า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ท้ายตาราง | — | **แสดง** 25 **รายการต่อหน้า** · **1–11 จาก 11** | ☐ |
| 2 | SELECT จำนวนต่อหน้า | 10 | **1–10 จาก 11** | ☐ |
| 3 | CLICK ปุ่มหน้า **2** | — | **11–11 จาก 11** · 1 แถว | ☐ |

#### TC-L11 — เรียงตามวันที่ขอ
- group: รายการ · ความสำคัญ: ต่ำ · trace: 01_UI P-01
- actor (role): admin
- Setup: role=admin บัญชี (ศศิธร มีสุข · __QA__.setMe('E08')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เรียงจากเก่าไปใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK หัวคอลัมน์ **วันที่ขอ** | — | ลูกศร ↑ · แถวแรก ACR-2569-0001 (2 ก.ย. 2569) | ☐ |
| 2 | CLICK หัวคอลัมน์ **วันที่ขอ** อีกครั้ง | — | ลูกศร ↓ · แถวแรก ACR-2569-0007 (11 ต.ค. 2569) | ☐ |

### กลุ่ม: สร้าง

#### TC-C01 — สร้างคำขอเพิ่มรหัสบัญชี บันทึกร่างได้เลข ACR
- group: สร้าง · ความสำคัญ: สูง · trace: AC-01 / S-01 / S-02 / S-05 / FN-01 / FN-02 / FN-03 / DEC-10 / BR-08
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request`
- ชุดข้อมูล: A
- ผ่านเมื่อ: ได้ร่าง ACR-2569-0012

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างคำขอ** | — | drawer กว้าง **สร้างเอกสารใหม่** · stepper **ข้อมูลหลักคำขอ** › **เอกสารแนบ** › **ตรวจสอบและยืนยัน** | ☐ |
| 2 | CLICK การ์ด **เพิ่มรหัสบัญชี** | — | การ์ด ② **กรณีขอเพิ่มรหัสบัญชี** ปรากฏ | ☐ |
| 3 | TYPE → บรรทัด 1 ของ **ชื่อบัญชีที่ต้องการขอเพิ่ม** | A.name1 | สรุปขวา 1 บัญชี | ☐ |
| 4 | CLICK ปุ่ม **เพิ่มอีกบัญชี** → TYPE บรรทัด 2 | A.name2 | สรุปขวา 2 บัญชี | ☐ |
| 5 | TYPE → **วัตถุประสงค์ในการเพิ่ม** | A.purpose | — | ☐ |
| 6 | CLICK **ถัดไป** ×2 | — | ขั้น **ตรวจสอบและยืนยัน** แสดง **กรณีขอเพิ่มรหัสบัญชี** | ☐ |
| 7 | CLICK **บันทึกแบบร่าง** | — | toast **บันทึกร่างแล้ว · ACR-2569-0012** · แถวใหม่ pill **ร่าง** | ☐ |

#### TC-C02 — กดถัดไปตอนยังไม่เลือกประเภท = บล็อก (auto: e2e S7)
- group: สร้าง · ความสำคัญ: สูง · trace: AC-02 / VR-01
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ยังอยู่ขั้น 1 + แดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/account-code-request/create` | — | การ์ด ② **เลือกประเภทคำขอก่อน แล้วช่องที่ต้องกรอกจะแสดงที่นี่** | ☐ |
| 2 | CLICK **ถัดไป** | — | ยังอยู่ขั้น 1 · **กรุณาเลือกประเภทคำขอ** · toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |

#### TC-C03 — เพิ่ม: ไม่ใส่ชื่อบัญชี = บล็อก
- group: สร้าง · ความสำคัญ: สูง · trace: VR-02 / BR-02 / DEC-04 [AI-DEFAULT]
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แดงที่ชื่อบัญชี + วัตถุประสงค์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK การ์ด **เพิ่มรหัสบัญชี** | — | บรรทัดว่าง 1 บรรทัด | ☐ |
| 2 | CLICK **ถัดไป** | — | **กรุณาระบุชื่อบัญชีอย่างน้อย 1 บัญชี** · **กรุณาระบุวัตถุประสงค์ในการเพิ่ม** | ☐ |

#### TC-C04 — เพิ่ม: ชื่อบัญชีซ้ำในใบ = บล็อก
- group: สร้าง · ความสำคัญ: สูง · trace: AC-03 / VR-03 / BR-02 [AI-DEFAULT]
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/create`
- ชุดข้อมูล: D
- ผ่านเมื่อ: ข้อความชื่อซ้ำใต้บรรทัด 2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK การ์ด **เพิ่มรหัสบัญชี** | — | — | ☐ |
| 2 | TYPE บรรทัด 1 · CLICK **เพิ่มอีกบัญชี** · TYPE บรรทัด 2 · TYPE วัตถุประสงค์ | D | — | ☐ |
| 3 | CLICK **ถัดไป** | — | บรรทัด 2 ขอบแดง + **ชื่อบัญชีซ้ำกับบรรทัดที่ 1** | ☐ |

#### TC-C05 — เพิ่ม: ลบบรรทัด
- group: สร้าง · ความสำคัญ: ต่ำ · trace: 01_UI P-02 / DEC-05
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เหลือ 1 บรรทัด ไม่มีปุ่มลบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK การ์ด **เพิ่มรหัสบัญชี** → CLICK **เพิ่มอีกบัญชี** | — | 2 บรรทัด · มีปุ่มลบท้ายบรรทัด | ☐ |
| 2 | CLICK ปุ่มลบบรรทัด 2 | — | 1 บรรทัด · ไม่มีปุ่มลบ | ☐ |

#### TC-C06 — เพิ่ม: ไม่จำกัดบรรทัด (12 บัญชี)
- group: สร้าง · ความสำคัญ: กลาง · trace: DEC-05 / BR-02 / EC-02
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: 12 บรรทัด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK การ์ด **เพิ่มรหัสบัญชี** → CLICK **เพิ่มอีกบัญชี** 11 ครั้ง | — | 12 บรรทัด | ☐ |
| 2 | TYPE ชื่อทุกบรรทัด (ไม่ซ้ำ) + วัตถุประสงค์ → **ถัดไป** | — | ไปขั้น **เอกสารแนบ** ได้ | ☐ |

#### TC-C07 — แก้ไข: เว้นแก้ไขเป็น = บล็อก
- group: สร้าง · ความสำคัญ: สูง · trace: AC-04 / S-03 / VR-05 / BR-03 (รหัสบัญชีพิมพ์อิสระ ไม่ตรวจกับ COA)
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แดงที่แก้ไขเป็น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK การ์ด **แก้ไขรหัสบัญชี** | — | การ์ด ② **กรณีขอแก้ไขรหัสบัญชี** · ช่อง **รหัสบัญชี** **แก้ไขเป็น** **วัตถุประสงค์ในการแก้ไข** | ☐ |
| 2 | TYPE รหัสบัญชี + วัตถุประสงค์ | 5210-01 · แยกต้นทุน | — | ☐ |
| 3 | CLICK **ถัดไป** | — | **กรุณาระบุว่าแก้ไขเป็นอะไร** · ยังอยู่ขั้น 1 | ☐ |

#### TC-C08 — ยกเลิก: ป้ายวัตถุประสงค์ในการยกเลิก + บังคับครบ
- group: สร้าง · ความสำคัญ: สูง · trace: AC-05 / S-04 / VR-06 / VR-04 / DEC-12 / BR-04
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ป้ายถูก · บังคับ 3 ช่อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK การ์ด **ยกเลิกรหัสบัญชี** | — | ช่อง **รหัสบัญชี** · **ชื่อบัญชี** · **วัตถุประสงค์ในการยกเลิก** | ☐ |
| 2 | CLICK **ถัดไป** | — | **กรุณาระบุรหัสบัญชี** · **กรุณาระบุชื่อบัญชี** · **กรุณาระบุวัตถุประสงค์ในการยกเลิก** | ☐ |

#### TC-C09 — เปลี่ยนประเภทกลางทาง ส่วนเดิมไม่ถูกบันทึก
- group: สร้าง · ความสำคัญ: สูง · trace: AC-06 / BR-01 / EC-01 / DEC-13 / FN-02
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/create`
- ชุดข้อมูล: A + B
- ผ่านเมื่อ: ใบใหม่เป็นแก้ไขเท่านั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มรหัสบัญชี** → TYPE ชื่อบัญชี | A.name1 | — | ☐ |
| 2 | CLICK **แก้ไขรหัสบัญชี** → TYPE ครบ 3 ช่อง | B | สรุปขวา ประเภท **แก้ไขรหัสบัญชี** | ☐ |
| 3 | CLICK **ถัดไป** ×2 → **บันทึกแบบร่าง** | — | toast **บันทึกร่างแล้ว · ACR-2569-0012** | ☐ |
| 4 | OPEN แถว ACR-2569-0012 → แท็บ **PDF Preview** | — | ☑ แก้ไขรหัสบัญชี · ช่องกรณีขอเพิ่มว่าง | ☐ |

#### TC-C10 — สรุปขวาแสดงผู้พิจารณาค่าเริ่มจาก DOA
- group: สร้าง · ความสำคัญ: กลาง · trace: DEC-03 / FN-04 / 01_UI P-02
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ผู้ตรวจสอบ = วรวุฒิ · ผู้อนุมัติ = มานี

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY การ์ด **สรุปคำขอ** | — | **ผู้ตรวจสอบ (ค่าเริ่มต้นจาก DOA)** วรวุฒิ ทองดี · **ผู้อนุมัติ (ค่าเริ่มต้นจาก DOA)** มานี รักษ์ทรัพย์ | ☐ |

#### TC-C11 — แนบไฟล์ถูกชนิด
- group: สร้าง · ความสำคัญ: กลาง · trace: DEC-11 / BR-06 / API-12
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน · files=รายงานเคลื่อนไหวบัญชี.pdf
- Start: OPEN `#/account-code-request/create`
- ชุดข้อมูล: B
- ผ่านเมื่อ: ไฟล์ขึ้นในรายการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **แก้ไขรหัสบัญชี** · TYPE ครบ · CLICK **ถัดไป** | B | ขั้น **แนบเอกสารประกอบ (ถ้ามี)** | ☐ |
| 2 | UPLOAD ไฟล์ | รายงานเคลื่อนไหวบัญชี.pdf | แถวไฟล์ รายงานเคลื่อนไหวบัญชี.pdf + ขนาด | ☐ |

#### TC-C12 — แนบไฟล์ผิดชนิด = ปฏิเสธ
- group: สร้าง · ความสำคัญ: กลาง · trace: DEC-11 / 01_UI P-02
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน · files=โปรแกรม.exe
- Start: OPEN `#/account-code-request/create`
- ชุดข้อมูล: B
- ผ่านเมื่อ: toast error

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **แก้ไขรหัสบัญชี** · TYPE ครบ · CLICK **ถัดไป** | B | — | ☐ |
| 2 | UPLOAD ไฟล์ | โปรแกรม.exe | toast โปรแกรม.exe — **ชนิดไฟล์ไม่รองรับ** · ไม่มีแถวไฟล์ | ☐ |

#### TC-C13 — ปิด drawer ตอนกรอกค้าง = ถามทิ้งข้อมูล
- group: สร้าง · ความสำคัญ: กลาง · trace: 01_UI P-02 / U25
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal ทิ้งข้อมูล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เพิ่มรหัสบัญชี** · TYPE ชื่อบัญชี | ทดสอบ | — | ☐ |
| 2 | PRESS Esc | — | modal **ทิ้งข้อมูลที่กรอกไว้?** | ☐ |
| 3 | CLICK **กลับไปกรอกต่อ** | — | ยังอยู่ในฟอร์ม ค่าเดิมอยู่ | ☐ |
| 4 | PRESS Esc → CLICK **ทิ้งข้อมูล** | — | drawer ปิด | ☐ |

#### TC-C14 — แก้ไขร่างที่ถูกส่งกลับ แสดงเหตุผล + ค่าเดิม
- group: สร้าง · ความสำคัญ: สูง · trace: S-09 / DEC-08 / BR-DOA-03
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นแถบเหตุผล แก้ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แบนเนอร์ | — | **ไม่อนุมัติ กลับเป็นร่าง** — ข้อมูลไม่ครบ ขอรายละเอียดเพิ่ม | ☐ |
| 2 | CLICK **แก้ไข** | — | drawer **แก้ไขคำขอ ACR-2569-0006** · การ์ด **เพิ่มรหัสบัญชี** ถูกเลือก · 2 บรรทัดเดิม | ☐ |

### กลุ่ม: ส่ง/อนุมัติ

#### TC-A01 — ส่งอนุมัติ: modal 1 แถวต่อขั้น DOA (auto: e2e S8)
- group: ส่ง/อนุมัติ · ความสำคัญ: สูง · trace: AC-07 / S-06 / FN-04 / DEC-03 [AI-DEFAULT] / BR-DOA-01
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ส่งแล้วรออนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** | — | modal **ส่งอนุมัติ?** · 2 แถว: 1 **ผู้ตรวจสอบ** วรวุฒิ ทองดี · 2 **ผู้อนุมัติ** มานี รักษ์ทรัพย์ · **ค่าเริ่มต้นจากสายอนุมัติ (DOA) และผังองค์กร** | ☐ |
| 2 | CLICK **ส่งอนุมัติ** ใน modal | — | toast **ส่งอนุมัติแล้ว · ACR-2569-0007** · pill **รออนุมัติ** · ลายเซ็น 0/2 | ☐ |

#### TC-A02 — ส่งอนุมัติ: ไม่เลือกผู้พิจารณา = บล็อก
- group: ส่ง/อนุมัติ · ความสำคัญ: กลาง · trace: VR-07 / API-06 ASSIGNEE_REQUIRED
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แดงที่ช่อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** | — | modal | ☐ |
| 2 | CLICK × ล้างผู้พิจารณาขั้น 1 → CLICK **ส่งอนุมัติ** | — | **กรุณาเลือกผู้พิจารณา** · สถานะยังเป็นร่าง | ☐ |

#### TC-A03 — ผู้ขอไม่อยู่ในรายชื่อผู้พิจารณา
- group: ส่ง/อนุมัติ · ความสำคัญ: สูง · trace: TC-D06 / BR-DOA-04 / VR-07
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีชื่อกิตติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** → CLICK ช่องผู้พิจารณาขั้น 1 | — | รายชื่อไม่มี กิตติ ศรีสุข | ☐ |

#### TC-A04 — DOA เพิ่มขั้น → แถวผู้พิจารณาเพิ่ม (dynamic · ต้อง simulate · auto: e2e S8)
- group: ส่ง/อนุมัติ · ความสำคัญ: กลาง · trace: AC-14 / DEC-03 / BR-10
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=— · console __QA__.doa.push('ขั้นทดสอบ')
- Start: OPEN `#/account-code-request/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: 3 แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console `__QA__.doa.push('ขั้นทดสอบ')` | — | — | ☐ |
| 2 | CLICK **ส่งอนุมัติ** | — | modal 3 แถว · แถว 3 **ขั้นทดสอบ** | ☐ |

#### TC-A05 — ผู้ตรวจสอบกด ตรวจสอบแล้ว → ส่งต่อขั้น 2
- group: ส่ง/อนุมัติ · ความสำคัญ: สูง · trace: AC-08 / S-07 / FN-05 / BR-DOA-02
- actor (role): ผู้ตรวจสอบ
- Setup: role=ผู้ตรวจสอบ (วรวุฒิ ทองดี · __QA__.setMe('E05')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R5`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ขั้น 2 รอมานี

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แบนเนอร์ | — | รอ วรวุฒิ ทองดี (ผู้ตรวจสอบ) พิจารณา — **คุณเป็นผู้พิจารณาคำขอนี้** | ☐ |
| 2 | CLICK **ตรวจสอบแล้ว** | — | modal หัวข้อ "ตรวจสอบแล้วคำขอนี้?" (ประกอบตอนรันจากคำตาม role) · **ส่งต่อให้ขั้นถัดไปพิจารณา** | ☐ |
| 3 | CLICK **ตรวจสอบแล้ว** ใน modal | — | toast **ตรวจสอบแล้ว · ส่งต่อขั้น 2 · ACR-2569-0005** · แบนเนอร์ รอ มานี รักษ์ทรัพย์ (ผู้อนุมัติ) | ☐ |

#### TC-A06 — ผู้อนุมัติอนุมัติขั้นสุดท้าย → อนุมัติแล้ว · รอบันทึก
- group: ส่ง/อนุมัติ · ความสำคัญ: สูง · trace: AC-08 / S-08 / FN-05 / FN-09 / XT-01
- actor (role): ผู้อนุมัติ
- Setup: role=ผู้อนุมัติ (มานี รักษ์ทรัพย์ · __QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: อนุมัติแล้ว · รอบันทึก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **อนุมัติ** | — | modal หัวข้อ "อนุมัติคำขอนี้?" (ประกอบตอนรันจากคำตาม role) · **ขั้นสุดท้าย — ต่อไปฝ่ายบัญชีบันทึกเข้าระบบ** | ☐ |
| 2 | CLICK **อนุมัติ** ใน modal | — | toast **อนุมัติแล้ว · รอบันทึกเข้าระบบ · ACR-2569-0003** · pill **อนุมัติแล้ว · รอบันทึก** · ลายเซ็น 2/2 | ☐ |
| 3 | VERIFY แบนเนอร์ | — | **อนุมัติแล้ว — รอฝ่ายบัญชีบันทึกเข้าระบบ** | ☐ |

#### TC-A07 — ไม่อนุมัติ ไม่ใส่เหตุผล = บล็อก
- group: ส่ง/อนุมัติ · ความสำคัญ: สูง · trace: VR-08 / DEC-14 / BR-07
- actor (role): ผู้อนุมัติ
- Setup: role=ผู้อนุมัติ (มานี รักษ์ทรัพย์ · __QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แดงที่เหตุผล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ไม่อนุมัติ** | — | modal หัวข้อ "ไม่อนุมัติตามคำขอนี้?" (ประกอบตอนรันจากคำตาม role) · chip เหตุผลสำเร็จรูป | ☐ |
| 2 | CLICK **ไม่อนุมัติ** ใน modal | — | **กรุณาระบุเหตุผล** · modal ยังเปิด | ☐ |

#### TC-A08 — ไม่อนุมัติ → กลับเป็นร่างเลขเดิม
- group: ส่ง/อนุมัติ · ความสำคัญ: สูง · trace: AC-09 / S-09 / FN-06 / DEC-08 [AI-DEFAULT] / BR-05 / BR-DOA-03
- actor (role): ผู้อนุมัติ
- Setup: role=ผู้อนุมัติ (มานี รักษ์ทรัพย์ · __QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ACR-2569-0003 เป็นร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ไม่อนุมัติ** → CLICK chip **ยังมีรายการค้างในบัญชีนี้** | — | ช่องเหตุผลเติมข้อความ | ☐ |
| 2 | CLICK **ไม่อนุมัติ** ใน modal | — | toast **ส่งกลับเป็นร่างแล้ว · ACR-2569-0003** · drawer ปิด (ร่างไม่เห็นโดยผู้อนุมัติ) | ☐ |
| 3 | PRESS สลับเป็น กิตติ ศรีสุข → OPEN `#/account-code-request/view/R3` | — | pill **ร่าง** · แบนเนอร์ **ไม่อนุมัติ กลับเป็นร่าง** — ยังมีรายการค้างในบัญชีนี้ | ☐ |

#### TC-A09 — ผู้ตรวจสอบไม่ผ่าน ใช้คำตาม role
- group: ส่ง/อนุมัติ · ความสำคัญ: กลาง · trace: AC-14 / BR-10 / LD-02
- actor (role): ผู้ตรวจสอบ
- Setup: role=ผู้ตรวจสอบ (วรวุฒิ ทองดี · __QA__.setMe('E05')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R5`
- ชุดข้อมูล: —
- ผ่านเมื่อ: คำว่า ไม่ผ่านการตรวจสอบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว | — | **ไม่ผ่านการตรวจสอบ** · **ตรวจสอบแล้ว** | ☐ |
| 2 | CLICK **ไม่ผ่านการตรวจสอบ** | — | modal หัวข้อ "ไม่ผ่านการตรวจสอบตามคำขอนี้?" (ประกอบตอนรันจากคำตาม role) | ☐ |

#### TC-A10 — แท็บลายเซ็น / อนุมัติ แสดง timeline ตามขั้น
- group: ส่ง/อนุมัติ · ความสำคัญ: กลาง · trace: 01_UI P-03 / DEC-07 / BR-10
- actor (role): ผู้อนุมัติ
- Setup: role=ผู้อนุมัติ (มานี รักษ์ทรัพย์ · __QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ขั้น 1 ผ่าน ขั้น 2 รอ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **ลายเซ็น / อนุมัติ** | — | **ลำดับการอนุมัติ** · **ผู้ขอ · ส่งอนุมัติ** · ขั้น 1 · ผู้ตรวจสอบ **ตรวจสอบแล้ว** · ขั้น 2 · ผู้อนุมัติ **รอพิจารณา** + ปุ่ม **อนุมัติ** · **ผู้บันทึกเข้าระบบ (ฝ่ายบัญชี · ไม่ใช่ขั้นอนุมัติ)** | ☐ |

### กลุ่ม: บันทึกเข้าระบบ

#### TC-R01 — admin บันทึกเข้าระบบแล้ว
- group: บันทึกเข้าระบบ · ความสำคัญ: สูง · trace: AC-10 / S-10 / FN-11 / BR-11 / DEC-01 [AI-DEFAULT] / BR-09 / XT-01
- actor (role): admin
- Setup: role=admin บัญชี (ศศิธร มีสุข · __QA__.setMe('E08')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R2`
- ชุดข้อมูล: —
- ผ่านเมื่อ: บันทึกเข้าระบบแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **บันทึกเข้าระบบแล้ว** | — | modal **บันทึกเข้าระบบแล้ว?** · ข้อความ ระบบไม่แก้ผังบัญชีให้อัตโนมัติ · **กรณีขอแก้ไขรหัสบัญชี** 5210-01 | ☐ |
| 2 | CLICK **บันทึกเข้าระบบแล้ว** ใน modal | — | toast **บันทึกเข้าระบบแล้ว · ACR-2569-0002** · pill **บันทึกเข้าระบบแล้ว** · ล็อกแก้ไข | ☐ |

#### TC-R02 — บันทึกเข้าระบบ: วันที่เกินวันนี้เลือกไม่ได้
- group: บันทึกเข้าระบบ · ความสำคัญ: กลาง · trace: VR-09 / BR-11
- actor (role): admin
- Setup: role=admin บัญชี (ศศิธร มีสุข · __QA__.setMe('E08')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R11`
- ชุดข้อมูล: —
- ผ่านเมื่อ: วันหลัง 11 ต.ค. 2569 กดไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **บันทึกเข้าระบบแล้ว** → CLICK ช่อง **วันที่** | — | ปฏิทิน พ.ศ. · วันหลัง 11 ต.ค. 2569 เป็นสีจาง กดไม่ได้ | ☐ |

#### TC-R03 — ผู้ขอ/ผู้อนุมัติไม่มีปุ่มบันทึกเข้าระบบ
- group: บันทึกเข้าระบบ · ความสำคัญ: สูง · trace: TC-D07 / 05 §5.3
- actor (role): ผู้อนุมัติ
- Setup: role=ผู้อนุมัติ (มานี รักษ์ทรัพย์ · __QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R11`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่ม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว | — | ไม่มี **บันทึกเข้าระบบแล้ว** | ☐ |
| 2 | CLICK ⋮ แถว ACR-2569-0011 ในรายการ | — | เมนูมีแค่ **พิมพ์** | ☐ |

#### TC-R04 — ใบรออนุมัติบันทึกเข้าระบบไม่ได้
- group: บันทึกเข้าระบบ · ความสำคัญ: กลาง · trace: TC-D08 / API-09 NOT_APPROVED
- actor (role): admin
- Setup: role=admin บัญชี (ศศิธร มีสุข · __QA__.setMe('E08')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R4`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่ม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว | — | **ยกเลิกเอกสาร** · ไม่มี **บันทึกเข้าระบบแล้ว** | ☐ |

### กลุ่ม: ยกเลิก

#### TC-X01 — เจ้าของยกเลิกร่าง (เหตุผลบังคับ)
- group: ยกเลิก · ความสำคัญ: สูง · trace: AC-12 / S-12 / FN-07 / BR-09 / VR-08 / DEC-08
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ยกเลิกแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยกเลิก** | — | modal **ยกเลิกเอกสาร?** | ☐ |
| 2 | CLICK **ยกเลิกเอกสาร** ใน modal | — | **กรุณาระบุเหตุผล** | ☐ |
| 3 | CLICK chip **ไม่ต้องการแล้ว** → CLICK **ยกเลิกเอกสาร** | — | toast **ยกเลิกเอกสารแล้ว · ACR-2569-0007** · pill **ยกเลิก** | ☐ |

#### TC-X02 — admin ยกเลิกใบรออนุมัติ → แจ้งผู้พิจารณา
- group: ยกเลิก · ความสำคัญ: กลาง · trace: AC-12 / FN-07 / FN-09 / XT-01 / acr_cancelled
- actor (role): admin
- Setup: role=admin บัญชี (ศศิธร มีสุข · __QA__.setMe('E08')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R4`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ยกเลิกแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยกเลิกเอกสาร** → TYPE เหตุผล → CLICK **ยกเลิกเอกสาร** | ข้อมูลผิด จะทำใบใหม่ | toast **ยกเลิกเอกสารแล้ว · ACR-2569-0004** · ระบบจริงยิง acr_cancelled ถึงผู้ตรวจสอบ (ต้อง simulate) | ☐ |

#### TC-X03 — ใบอนุมัติแล้วไม่มีปุ่มยกเลิก
- group: ยกเลิก · ความสำคัญ: กลาง · trace: AC-12 / BR-09 / API-08 NOT_CANCELLABLE
- actor (role): admin
- Setup: role=admin บัญชี (ศศิธร มีสุข · __QA__.setMe('E08')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R2`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มียกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว | — | **บันทึกเข้าระบบแล้ว** · ไม่มี **ยกเลิกเอกสาร** | ☐ |

### กลุ่ม: PDF

#### TC-F01 — PDF ใบบันทึกเข้าระบบแล้ว ครบทุกส่วน
- group: PDF · ความสำคัญ: สูง · trace: AC-11 / S-11 / FN-08 / BR-10 / DEC-07 / DEC-06
- actor (role): admin
- Setup: role=admin บัญชี (ศศิธร มีสุข · __QA__.setMe('E08')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ☑ เพิ่ม · 2 บัญชี · ลงชื่อ 3 ช่อง · ผู้บันทึก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | A4 **แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี** · **เลขที่เอกสาร** ACR-2569-0001 | ☐ |
| 2 | VERIFY ตัวเลือก | — | ☑ เพิ่มรหัสบัญชี ☐ แก้ไขรหัสบัญชี ☐ ยกเลิกรหัสบัญชี | ☐ |
| 3 | VERIFY **ชื่อบัญชีที่ต้องการขอเพิ่ม** | — | รายได้ค่าบริการติดตั้ง · ต้นทุนบริการติดตั้ง + บรรทัดว่างจนครบ 4 | ☐ |
| 4 | VERIFY **สำหรับผู้อนุมัติ** | — | ☑ อนุมัติ ☐ ไม่อนุมัติ | ☐ |
| 5 | VERIFY แถวลงชื่อ | — | 3 ช่อง: **ผู้ขอเพิ่ม/แก้ไข/ยกเลิกรหัสบัญชี** · **ผู้ตรวจสอบ** (☑ ตรวจสอบแล้ว) · **ผู้อนุมัติ** (☑ อนุมัติ) · ส่งในระบบ/พิจารณาในระบบ | ☐ |
| 6 | VERIFY บรรทัด **ผู้บันทึกเข้าระบบ** | — | บันทึกแล้ว ( ศศิธร มีสุข ) / วันที่ 5 ก.ย. 2569 | ☐ |
| 7 | VERIFY footer | — | **Doc. No. : FM-ACC-01 · Rev.00 : 01/07/2569** | ☐ |

#### TC-F02 — PDF ใบร่าง
- group: PDF · ความสำคัญ: กลาง · trace: AC-11 / FN-08
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: footer ร่าง · ลงชื่อเส้นประ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | ☑ แก้ไขรหัสบัญชี · รหัสบัญชี 4110-03 · ส่วนเพิ่ม/ยกเลิกว่าง | ☐ |
| 2 | VERIFY แถวลงชื่อ | — | วันที่ ........./........./......... ทุกช่อง · footer มี · ร่าง | ☐ |

#### TC-F03 — PDF ส่วนยกเลิกใช้ป้าย วัตถุประสงค์ในการยกเลิก
- group: PDF · ความสำคัญ: กลาง · trace: DEC-12 / BR-04 / AC-05
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ป้ายถูก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | ☑ ยกเลิกรหัสบัญชี · รหัสบัญชี 5390-09 · ชื่อบัญชี ค่าใช้จ่ายเบ็ดเตล็ดอื่น (เดิม) · **วัตถุประสงค์ในการยกเลิก** ไม่มีการใช้งานเกิน 12 เดือน… | ☐ |

#### TC-F04 — พิมพ์ / ดาวน์โหลด PDF
- group: PDF · ความสำคัญ: ต่ำ · trace: S-11 / API-10
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: หน้าต่างพิมพ์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** → CLICK **ดาวน์โหลด PDF** | — | toast เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ · ACR-2569-0001 | ☐ |

#### TC-F05 — DOA 6 ขั้น → ช่องลงชื่อ 7 ช่อง 2 แถว (ต้อง simulate)
- group: PDF · ความสำคัญ: กลาง · trace: AC-14 / BR-10 / DEC-07 / DEC-03
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=— · console __QA__.doa.push ×4
- Start: OPEN `#/account-code-request/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: PDF 4+3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console `__QA__.doa.push('ขั้น 3')` … ×4 → ส่งอนุมัติ (เลือกผู้พิจารณาทุกแถว) | — | modal 6 แถว | ☐ |
| 2 | CLICK แท็บ **PDF Preview** | — | ช่องลงชื่อ 7 ช่อง แถวบน 4 แถวล่าง 3 · ยัง 1 หน้า (ตรวจกับ print/out/approved-doa6steps.pdf) | ☐ |

### กลุ่ม: สิทธิ์

#### TC-P01 — ผู้อนุมัติเปิด route ร่างของคนอื่น (auto: e2e S6)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D01 / BR-12 / API-02 NOT_FOUND / DEC-09
- actor (role): ผู้อนุมัติ
- Setup: role=ผู้อนุมัติ (มานี รักษ์ทรัพย์ · __QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่เปิด drawer

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/account-code-request/view/R8` | — | หน้ารายการ ไม่มี drawer เปิด | ☐ |
| 2 | VERIFY ตาราง | — | ไม่พบ ACR-2569-0008 — ร่างไม่เห็น | ☐ |

#### TC-P02 — ผู้ขอไม่เห็นร่างของคนอื่น
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D02 / BR-12
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่พบใบ 0008

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE ค้นหา | ACR-2569-0008 | **ไม่พบรายการที่ค้นหา** | ☐ |

#### TC-P03 — admin เห็นทุกใบรวมร่างของคนอื่น
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: DEC-09 / AC-13 / S-13
- actor (role): admin
- Setup: role=admin บัญชี (ศศิธร มีสุข · __QA__.setMe('E08')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: 11 แถว รวม 0008

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY badge | — | **11 รายการ** | ☐ |
| 2 | CLICK แถว ACR-2569-0008 | — | drawer เปิด · ไม่มีปุ่ม **แก้ไข** (ไม่ใช่เจ้าของ) | ☐ |

#### TC-P04 — ผู้อนุมัติขั้น 2 กดไม่ได้ขณะขั้น 1 ยังรอ
- group: สิทธิ์ · ความสำคัญ: สูง · trace: TC-D03 / API-07 NOT_CURRENT_APPROVER / BR-DOA-02
- actor (role): ผู้อนุมัติ
- Setup: role=ผู้อนุมัติ (มานี รักษ์ทรัพย์ · __QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R5`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มตัดสิน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แบนเนอร์ | — | รอ วรวุฒิ ทองดี (ผู้ตรวจสอบ) พิจารณา | ☐ |
| 2 | VERIFY ปุ่มหัว | — | ไม่มี **อนุมัติ** / **ตรวจสอบแล้ว** | ☐ |

#### TC-P05 — ผู้อนุมัติยกเลิกใบไม่ได้
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: TC-D04 / 05 §5.3 / API-08 NOT_OWNER
- actor (role): ผู้อนุมัติ
- Setup: role=ผู้อนุมัติ (มานี รักษ์ทรัพย์ · __QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ⋮ แถว ACR-2569-0004 | — | เมนูไม่มี **ยกเลิกเอกสาร** | ☐ |

#### TC-P06 — แก้ใบที่ไม่ใช่ร่าง/ไม่ใช่ของตนไม่ได้ (auto: e2e S5)
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: TC-D05 / BR-09
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มแก้ไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว | — | ไม่มี **แก้ไข** · footer **อนุมัติแล้ว ล็อกแก้ไข** | ☐ |

#### TC-P07 — ผู้ตรวจสอบเห็นเฉพาะใบในสาย
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: DEC-09 / BR-12 / FN-10
- actor (role): ผู้ตรวจสอบ
- Setup: role=ผู้ตรวจสอบ (วรวุฒิ ทองดี · __QA__.setMe('E05')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: 4 แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY badge | — | **4 รายการ** · **รอฉันพิจารณา 1** | ☐ |
| 2 | VERIFY แถว | — | ACR-2569-0011, 0005, 0003, 0001 · ไม่มีร่าง | ☐ |

### กลุ่ม: ข้อผิดพลาด

#### TC-E01 — ส่งไม่สำเร็จ → toast error สถานะไม่เปลี่ยน (auto: e2e S9 · ต้อง simulate)
- group: ข้อผิดพลาด · ความสำคัญ: กลาง · trace: EC-05 / 01_UI §1.6
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=— · console __QA__.sim('error')
- Start: OPEN `#/account-code-request/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ยังเป็นร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console `__QA__.sim('error')` → CLICK **ส่งอนุมัติ** → **ส่งอนุมัติ** ใน modal | — | toast **ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง** · pill **ร่าง** | ☐ |

#### TC-E02 — ข้อมูลถูกแก้โดยผู้อื่น (STALE · ต้อง simulate)
- group: ข้อผิดพลาด · ความสำคัญ: กลาง · trace: EC-05 / API STALE
- actor (role): ผู้อนุมัติ
- Setup: role=ผู้อนุมัติ (มานี รักษ์ทรัพย์ · __QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=— · console __QA__.sim('stale')
- Start: OPEN `#/account-code-request/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: toast รีเฟรช

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console `__QA__.sim('stale')` → CLICK **อนุมัติ** → **อนุมัติ** ใน modal | — | toast **ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่** · pill **รออนุมัติ** | ☐ |

#### TC-E03 — แบบเอกสารยังไม่เปิดใช้งาน (ต้อง simulate)
- group: ข้อผิดพลาด · ความสำคัญ: กลาง · trace: AC-15 / EC-06 / FN-03 DOC_TYPE_INACTIVE
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=— · console __QA__.setDocActive(false)
- Start: OPEN `#/account-code-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สร้างไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console `__QA__.setDocActive(false)` | — | แถบแดง **แบบเอกสารนี้ยังไม่เปิดใช้งาน — สร้างคำขอใหม่ไม่ได้** · ปุ่ม **สร้างคำขอ** กดไม่ได้ | ☐ |

### กลุ่ม: UX

#### TC-U01 — Esc ปิด modal ก่อน drawer (auto: e2e S10)
- group: UX · ความสำคัญ: ต่ำ · trace: U25 / 01_UI P-03
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปิดทีละชั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** | — | modal เปิดบน drawer | ☐ |
| 2 | PRESS Esc | — | modal ปิด drawer ยังอยู่ | ☐ |
| 3 | PRESS Esc | — | drawer ปิด | ☐ |

#### TC-U02 — แท็บประวัติ append-only
- group: UX · ความสำคัญ: ต่ำ · trace: 01_UI P-03 / 04_DB audit
- actor (role): ผู้ขอ
- Setup: role=owner (กิตติ ศรีสุข · __QA__.setMe('E01')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: 5 รายการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **ประวัติ** | — | **ประวัติ (append-only)** · บันทึกเข้าระบบแล้ว · อนุมัติ (ขั้น 2) · ตรวจสอบแล้ว (ขั้น 1) · ส่งอนุมัติ · สร้างเอกสาร | ☐ |

### กลุ่ม: Cross-module

#### TC-T01 — อนุมัติแล้วไม่แก้ผังบัญชี ไม่ส่งต่อระบบอื่น (ต้อง simulate)
- group: Cross-module · ความสำคัญ: กลาง · trace: XT-03 / DEC-01 [AI-DEFAULT] / DEC-02 / BR-05
- actor (role): admin
- Setup: role=admin บัญชี (ศศิธร มีสุข · __QA__.setMe('E08')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R2`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มี action แก้ COA

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **บันทึกเข้าระบบแล้ว** | — | modal แจ้ง ระบบไม่แก้ผังบัญชีให้อัตโนมัติ | ☐ |
| 2 | VERIFY หลังบันทึก | — | ไม่มีหน้าจอ/toast อ้างการส่งต่อ COA · ระบบจริงไม่ยิง acr.approved | ☐ |

#### TC-T02 — แจ้งเตือน acr_ready_to_record / acr_recorded (ต้อง simulate)
- group: Cross-module · ความสำคัญ: กลาง · trace: XT-01 / BR-13 / FN-09 / acr_ready_to_record / acr_recorded
- actor (role): ผู้อนุมัติ
- Setup: role=ผู้อนุมัติ (มานี รักษ์ทรัพย์ · __QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สถานะต้นทางเปลี่ยนถูก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **อนุมัติ** → **อนุมัติ** ใน modal | — | pill **อนุมัติแล้ว · รอบันทึก** (ระบบจริง: acr_ready_to_record ถึง admin บัญชี) | ☐ |
| 2 | PRESS สลับเป็น ศศิธร มีสุข → บันทึกเข้าระบบแล้ว | — | pill **บันทึกเข้าระบบแล้ว** (ระบบจริง: acr_recorded ถึงผู้ขอ) | ☐ |

#### TC-T03 — PDF เก็บสำเนาตอนอนุมัติ (approved_final · ต้อง simulate)
- group: Cross-module · ความสำคัญ: ต่ำ · trace: XT-02 / FN-05 / DOCCFG snapshot
- actor (role): ผู้อนุมัติ
- Setup: role=ผู้อนุมัติ (มานี รักษ์ทรัพย์ · __QA__.setMe('E02')) · seed=มาตรฐาน 11 ใบ · files=—
- Start: OPEN `#/account-code-request/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ระบบจริงเรียก ENG-DOC-STORE

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **อนุมัติ** → **อนุมัติ** | — | pill **อนุมัติแล้ว · รอบันทึก** · ตรวจการเก็บไฟล์ระดับ API | ☐ |

## วิธีที่ agent รัน (Run protocol)
1. เปิด `feature.html` ใหม่ทุกเคส (seed กลับค่าเริ่ม · วันนี้ของ prototype = 11 ต.ค. 2569) · เริ่มที่ Start
2. สลับผู้ใช้ตาม Setup (มุมขวาบน หรือ console `__QA__.setMe('E01'|'E05'|'E02'|'E08')`)
3. เคส `(ต้อง simulate)` ใช้ console: `__QA__.sim('error'|'stale')` · `__QA__.setDocActive(false)` · `__QA__.doa.push('…')` · ระบบจริงทดสอบระดับ API
4. ทำทีละ step เทียบ Expected ด้วยตา · ไม่ตรง = fail + จด evidence

## Coverage Audit
| หมวด | covered / total |
|---|---|
| AC (06_TESTS) | 15 / 15 |
| Business rules | 17 / 18 (BR-DOA-05 ข้าม) |
| Validation | 9 / 9 |
| Edge cases | 5 / 9 |
| Error codes | 11 / 11 (ระดับ UI) |
| Permission cells | 9 / 9 |

- Cross-Module (XT): 3/3
- Scope Lock (DEC): 14/14
- **Manifest cross-check (FRD §0.12): ✅ 7/7**

### ข้าม (พร้อมเหตุผล)
- BR-DOA-05 — ไม่มีวงเงิน (DEC-03)
- EC-03 · EC-04 — ทดสอบระดับ API (resolve ข้ามตัวเอง · แก้ DOA กลาง)
- EC-07 — นอกขอบเขต (DEC-01 / OQ-04)
- EC-08 — PDF 2 หน้า ตรวจในแบบพิมพ์ ไม่มีเคสบนจอ

## Result Report (schema)
```json
{ "feature_id": "F-TMP-003", "run_at": "<iso>", "results": [ { "id": "TC-C01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" } ], "summary": { "total": 62, "pass": 0, "fail": 0, "blocked": 0 } }
```

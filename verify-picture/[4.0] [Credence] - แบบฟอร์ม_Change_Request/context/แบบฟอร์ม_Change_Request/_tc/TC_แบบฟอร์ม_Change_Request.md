# AI Test Cases — F-TMP-005 แบบฟอร์ม Change Request (Change Request Form)

เคสสำหรับ AI agent (browser-use/vision) รันบน prototype `feature.html` — anchor ด้วยข้อความที่เห็นบนจอ + route จริง · เคสที่มี [AI-DEFAULT] = เกณฑ์มาจากมติที่ AI ตัดสินแทนลูกค้า (fail อาจแปลว่า default ผิด ไม่ใช่โค้ดผิด)

## Meta
| Field | Value |
|---|---|
| Feature ID | F-TMP-005 (ชั่วคราว) |
| ชื่อ | แบบฟอร์ม Change Request (FM-ITS-07) |
| เวอร์ชัน | 1.0 (2026-10-10) |
| App entry | feature.html |
| Routes | `#/change-request` · `#/change-request/create` · `#/change-request/edit/:id` · `#/change-request/view/:id` |
| ที่มา | FRD_F-TMP-005_Pack v1.0 · BRD-TMP-005 · DECISIONS.lock REQ-TMP-005 · feature.html (v9.4) · microcopy html-generator-v9 |
| จำนวนเคส | 61 |
| หมวด | รายการ 11 · สร้าง 5 · ตรวจข้อมูล 7 · ไฟล์แนบ 3 · ส่งอนุมัติ 5 · อนุมัติ 5 · ยกเลิก 4 · สิทธิ์ 7 · แบบพิมพ์ 6 · Error/UX 5 · Cross-module 3 |

## Coverage
| group | เคส | สูง | กลาง | ต่ำ |
|---|---|---|---|---|
| รายการ | 11 | 3 | 6 | 2 |
| สร้าง | 5 | 2 | 2 | 1 |
| ตรวจข้อมูล | 7 | 4 | 3 | 0 |
| ไฟล์แนบ | 3 | 0 | 2 | 1 |
| ส่งอนุมัติ | 5 | 3 | 2 | 0 |
| อนุมัติ | 5 | 4 | 0 | 1 |
| ยกเลิก | 4 | 2 | 2 | 0 |
| สิทธิ์ | 7 | 4 | 3 | 0 |
| แบบพิมพ์ | 6 | 1 | 3 | 2 |
| Error/UX | 5 | 0 | 3 | 2 |
| Cross-module | 3 | 0 | 2 | 1 |

## Coverage Ledger
### FR / Acceptance (BRD S-01..S-11 · 06_TESTS §6.1)
| item | cases |
|---|---|
| S-01 | TC-C01, TC-C02 |
| S-02 | TC-R03 |
| S-05 | TC-F01, TC-F02, TC-F03 |
| S-06 | TC-C02, TC-D01 |
| S-07 | TC-L02, TC-L03, TC-A01, TC-A02 |
| S-08 | TC-A04 |
| S-09 | TC-K01 |
| S-10 | TC-R01, TC-R02 |
| S-11 | TC-L01, TC-L05, TC-L06, TC-L07, TC-L10 |
| S-03 วันที่/สถานที่ส่งมอบ | TC-C01, TC-V05 |
| S-04 ผลกระทบ + แผน | TC-C04, TC-V06, TC-V01 |
### Business Rules (05_RULES)
| rule | cases |
|---|---|
| BR-01 | TC-L07, TC-V02, TC-V03 |
| BR-02 | TC-V04, TC-R04 |
| BR-03 | TC-V05 |
| BR-04 | TC-D01, TC-D03, TC-A01 |
| BR-05 | TC-D05, TC-A04 |
| BR-06 | TC-C01 |
| BR-07 | TC-P01 |
| BR-08 | TC-R01, TC-R05 |
| BR-10 | TC-R01 |
| BR-11 | TC-R01 |
| BR-09 ไม่เปลี่ยนค่า/ไม่ส่งต่อ · แจ้ง IT | TC-X01, TC-X03 |
| BR-12 แนบ/CSV/ไม่มีทำซ้ำ | TC-F01, TC-L10, TC-L11 |
| BR-13 ไม่มีรายการซ้ำ | — ข้าม (ไม่มีบนกระดาษ ไม่มีพฤติกรรมให้ทดสอบ) |
| BR-DOA-01..05 | TC-D01, TC-D04, TC-A01, TC-A04, TC-P03 |
### Validation (05 §5.4)
| VR | cases |
|---|---|
| VR-01 | TC-V01 |
| VR-02 | TC-V02 |
| VR-03 | TC-V04 |
| VR-04 | TC-V01 |
| VR-05 | TC-V01 |
| VR-06 | TC-V07 |
| VR-07 | TC-V06 |
| VR-08 | TC-V06 |
| VR-09 | TC-V01 |
| VR-10 | TC-D02 |
| VR-11 | TC-A03, TC-K02 |
### Edge Cases (05 §5.5)
| EC | cases / สถานะ |
|---|---|
| EC-01 | TC-V05 |
| EC-02 | TC-V04 |
| EC-03 | TC-V02 |
| EC-04 ข้อความยาวเกินบรรทัดกระดาษ | — ข้าม (ตรวจที่แบบพิมพ์ long-text.data.json · print-spec §8) |
| EC-05 | TC-D03, TC-R05 |
| EC-06 | TC-D04 |
| EC-07 แก้ DOA ระหว่างรอ | — ข้าม (ไม่มีผลบน UI prototype · ตรวจ BE) |
| EC-08 | TC-E02 |
| EC-09 | TC-P07 |
| EC-10 | TC-P02 |
| EC-11 | TC-A04 |
### Error Codes (05 §5.6)
| error | cases |
|---|---|
| DOC_TYPE_INACTIVE | TC-P07 |
| NOT_OWNER | TC-P06 |
| NOT_DRAFT | TC-K03 |
| STALE | TC-E02 |
| ASSIGNEE_REQUIRED | TC-D02 |
| SELF_APPROVE | TC-D04 |
| NOT_CURRENT_APPROVER | TC-P03, TC-P04 |
| REASON_REQUIRED | TC-A03, TC-K02 |
| NOT_FOUND | TC-P02 |
### Permission Matrix (05 §5.3)
| cell | cases |
|---|---|
| ผู้ตรวจสอบ ดูร่างคนอื่น = deny | TC-P01 |
| ผู้ตรวจสอบ เปิด route ร่าง = deny | TC-P02 |
| เจ้าของ อนุมัติใบตัวเอง = deny | TC-P03 |
| ขั้น 2 ตัดสินก่อนขั้น 1 = deny | TC-P04 |
| IT ดูทั้งหมด = allow | TC-P05 |
| IT แก้ร่างคนอื่น = deny | TC-P06 |
| ผู้พิจารณาขั้นปัจจุบัน อนุมัติ = allow | TC-A01, TC-A02 |
| เจ้าของ ยกเลิกร่าง = allow | TC-K01 |
| IT ยกเลิกใบรอ = allow | TC-K04 |
| ยกเลิกหลังอนุมัติ = deny | TC-K03 |
| เจ้าของ แก้ร่างตน = allow | TC-C05 |
### Cross-Module (XT)
| XT | Downstream | Case |
|---|---|---|
| itcr_approved_for_it | เจ้าหน้าที่ IT (ENG-NOTIFY) | TC-X01 |
| itcr_cancelled | ผู้พิจารณา (ENG-NOTIFY) | TC-X02 |
| itcr.approved → CMDB | ปิดรอบนี้ (DEC-02) | TC-X03 |
### Scope Lock (DEC — DECISIONS.lock แทน LOCK)
| DEC | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| DEC-01 [AI-DEFAULT] | ไม่เปลี่ยนค่าในระบบ | TC-X03 |
| DEC-02 [AI-DEFAULT] | ไม่ส่งต่อระบบอื่น | TC-X03 |
| DEC-03 [AI-DEFAULT] | DOA dynamic 2 ขั้น | TC-D01, TC-D03 |
| DEC-04 [AI-DEFAULT] | เตือน · ประเภท ≥1 หลายข้อ | TC-V02, TC-V03, TC-V05 |
| DEC-05 [AI-DEFAULT] | ไม่มีรายการซ้ำ | TC-R01 (ตารางไม่มีแถวรายการ) |
| DEC-06 [AI-DEFAULT] | ช่อง 1:1 | TC-C03, TC-C04, TC-R01 |
| DEC-07 [AI-DEFAULT] | ลายเซ็นต่อขั้น ไม่ใช้ภาพ | TC-R01, TC-R05 |
| DEC-08 [AI-DEFAULT] | ไม่อนุมัติ = กลับร่าง · ยกเลิกร่าง/รอ | TC-A04, TC-K01, TC-K03 |
| DEC-09 [AI-DEFAULT] | การมองเห็น | TC-P01, TC-P05 |
| DEC-10 [AI-DEFAULT] | เลข ITCR ตอนบันทึก | TC-C01 |
| DEC-11 [AI-DEFAULT] | แนบ ✓ CSV ✓ ทำซ้ำ ✗ | TC-F01, TC-L10, TC-L11 |
| DEC-12 | สะกด ตำแหน่ง | TC-R01, TC-C03 |
| DEC-13 | ป้าย ผู้ขอซื้อ | TC-R01 |
| DEC-14 | ส่งมอบก่อนวันที่ขอ = เตือน | TC-V05 |
| DEC-15 | อื่นๆ ต้องระบุ | TC-V04 |
| DEC-16 | ประเภท ≥1 | TC-V02 |
| DEC-17 | เลขที่ที่ footer | TC-R01, TC-R02 |
### Cross-cutting / States
| item | cases |
|---|---|
| state ร่าง→รออนุมัติ→อนุมัติแล้ว | TC-C02, TC-A01, TC-A02 |
| ร่าง→ยกเลิก / รอ→ยกเลิก | TC-K01, TC-X02 |
| empty state (ค้นไม่พบ) | TC-L08 |
| pagination | TC-L09 |
| dirty-check | TC-E04 |
| Esc chain | TC-E03 |
| backdrop mousedown | TC-E05 |

## Data Sets
### ชุด A (ถูกต้อง — ข้อมูลสมมติ)
| ฟิลด์ | ค่า |
|---|---|
| subject | อัปเดตเวอร์ชันระบบเงินเดือน |
| types | ระบบซอฟต์แวร์ + ความปลอดภัย |
| due | 24 ต.ค. 2569 |
| place | ห้อง Server อาคาร 1 |
| detail | อัปเดตโปรแกรมเงินเดือนเป็นเวอร์ชันล่าสุด |
| objective | แก้ไขข้อผิดพลาด · เพิ่มความปลอดภัย |
| impact | ระบบเงินเดือน หยุดประมาณ 1 ชั่วโมง |
| plan | สำรองข้อมูล (บรรทัด 1) / ติดตั้งนอกเวลาทำการ (บรรทัด 2) |
### ชุด B (อื่นๆ)
| ฟิลด์ | ค่า |
|---|---|
| types | อื่นๆ |
| other | นโยบายบัญชีผู้ใช้ |
| ที่เหลือ | เหมือนชุด A |
### ไฟล์ทดสอบ (Files)
| ไฟล์ | ใช้ใน |
|---|---|
| แผนติดตั้ง-ระบบบัญชี.pdf (120 KB) | TC-F01, TC-F03 |
| setup.exe | TC-F02 |

## Test Cases

### กลุ่ม รายการ

#### TC-L01 — หน้ารายการแสดงหัวตารางและแถวตามสิทธิ์
- group: รายการ · ความสำคัญ: สูง · trace: S-11 / FN-09 / P-01
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นหัวคอลัมน์ครบ + แถวเฉพาะใบที่มีสิทธิ์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/change-request` | — | หัวข้อ **แบบฟอร์ม Change Request** + **(Change Request Form)** | ☐ |
| 2 | VERIFY หัวตาราง | — | เห็น **เลขที่** · **วันที่** · **ผู้ขอ** · **เรื่องที่ต้องการ** · **ประเภท** · **วันที่ต้องการส่งมอบ** · **สถานะเอกสาร** · **ลายเซ็น** | ☐ |
| 3 | VERIFY แถว | — | เห็น **ITCR-2569-0006** และ **ITCR-2569-0008** · ไม่เห็น **ITCR-2569-0009** ⚠ (ร่างของคนอื่น — ต้องไม่ปรากฏ) | ☐ |
| 4 | VERIFY ไม่มีแถวการ์ดตัวเลขใต้หัวหน้า | — | ตัวเลขอยู่ใน badge เช่น **5 รายการ** (ไม่มี stat cards) | ☐ |

#### TC-L02 — แท็บ รอฉันพิจารณา (ขั้น 1)
- group: รายการ · ความสำคัญ: สูง · trace: S-07 / FN-09 tab act / DEC-09
- actor (role): ผู้ตรวจสอบ
- Setup: role=ผู้ตรวจสอบ ขั้น 1 (__QA__.setMe('E02')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เหลือเฉพาะใบที่ผู้ใช้เป็นผู้พิจารณาขั้นปัจจุบัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/change-request` | — | เห็นแท็บ **ทั้งหมด** · **รอฉันพิจารณา** · **คำขอของฉัน** | ☐ |
| 2 | CLICK แท็บ **รอฉันพิจารณา** | — | ตารางเหลือ **ITCR-2569-0006** แถวเดียว · สถานะ **รออนุมัติ** · ลายเซ็น **0/2** | ☐ |

#### TC-L03 — แท็บ รอฉันพิจารณา (ขั้น 2)
- group: รายการ · ความสำคัญ: สูง · trace: S-07 / FN-09 tab act
- actor (role): ผู้จัดการฝ่าย IT
- Setup: role=ผู้จัดการฝ่าย IT ขั้น 2 (__QA__.setMe('E10')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นใบที่ขั้น 1 อนุมัติแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **รอฉันพิจารณา** | — | เห็น **ITCR-2569-0003** และ **ITCR-2569-0012** · ลายเซ็น **1/2** | ☐ |

#### TC-L04 — แท็บ คำขอของฉัน
- group: รายการ · ความสำคัญ: กลาง · trace: FN-09 tab mine
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นเฉพาะใบของตัวเอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **คำขอของฉัน** | — | ทุกแถวคอลัมน์ผู้ขอ = **สมชาย ตัวอย่างดี** | ☐ |

#### TC-L05 — ค้นหาด้วยเรื่องที่ต้องการ
- group: รายการ · ความสำคัญ: กลาง · trace: S-11 / FN-09 q
- actor (role): เจ้าหน้าที่ IT
- Setup: role=เจ้าหน้าที่ IT (__QA__.setMe('E08')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: คำค้น: VPN
- ผ่านเมื่อ: เหลือแถวที่เรื่องตรงคำค้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา **ค้นหาเลขที่ / ผู้ขอ / เรื่องที่ต้องการ** | VPN | เหลือ **ITCR-2569-0008** (เปิดสิทธิ์ VPN ให้ทีมบัญชีทำงานนอกสถานที่) | ☐ |

#### TC-L06 — กรองสถานะ
- group: รายการ · ความสำคัญ: กลาง · trace: S-11 / FN-09 status
- actor (role): เจ้าหน้าที่ IT
- Setup: role=เจ้าหน้าที่ IT (__QA__.setMe('E08')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: สถานะ: อนุมัติแล้ว
- ผ่านเมื่อ: ทุกแถวสถานะตรงตัวกรอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ตัวกรอง **ทุกสถานะ** | — | เห็นตัวเลือก **อนุมัติแล้ว** | ☐ |
| 2 | SELECT **อนุมัติแล้ว** | — | ตารางเหลือ **ITCR-2569-0001** · **ITCR-2569-0002** · **ITCR-2569-0011** | ☐ |

#### TC-L07 — กรองประเภท
- group: รายการ · ความสำคัญ: กลาง · trace: S-11 / BR-01
- actor (role): เจ้าหน้าที่ IT
- Setup: role=เจ้าหน้าที่ IT (__QA__.setMe('E08')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: ประเภท: เครือข่าย
- ผ่านเมื่อ: เหลือใบที่มีประเภทนั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ตัวกรอง **ทุกประเภท** | — | เห็นตัวเลือก **เครือข่าย** | ☐ |
| 2 | SELECT **เครือข่าย** | — | เหลือ **ITCR-2569-0003** · **ITCR-2569-0008** · **ITCR-2569-0010** | ☐ |

#### TC-L08 — ค้นไม่พบแสดง empty state
- group: รายการ · ความสำคัญ: ต่ำ · trace: U23
- actor (role): เจ้าหน้าที่ IT
- Setup: role=เจ้าหน้าที่ IT (__QA__.setMe('E08')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: คำค้น: ไม่มีคำนี้
- ผ่านเมื่อ: เห็นแผงไม่พบรายการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา | ไม่มีคำนี้ | เห็น **ไม่พบรายการที่ค้นหา** + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 2 | CLICK **ล้างตัวกรอง** | — | กลับมาเห็นทุกใบ | ☐ |

#### TC-L09 — เรียงลำดับและแบ่งหน้า
- group: รายการ · ความสำคัญ: ต่ำ · trace: U4/U6
- actor (role): เจ้าหน้าที่ IT
- Setup: role=เจ้าหน้าที่ IT (__QA__.setMe('E08')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: แสดงต่อหน้า 10
- ผ่านเมื่อ: pager ทำงาน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT **แสดงต่อหน้า** | 10 | เห็น **1 – 10 จาก 12 รายการ** | ☐ |
| 2 | CLICK ปุ่มหน้า **2** | — | เห็น **11 – 12 จาก 12 รายการ** | ☐ |
| 3 | CLICK หัวคอลัมน์ **วันที่** | — | ลูกศรเรียงเปลี่ยน · แถวเรียงตามวันที่ | ☐ |

#### TC-L10 — ส่งออก CSV [AI-DEFAULT]
- group: รายการ · ความสำคัญ: กลาง · trace: S-11 / DEC-11 / API-10
- actor (role): เจ้าหน้าที่ IT
- Setup: role=เจ้าหน้าที่ IT (__QA__.setMe('E08')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ได้ไฟล์ change-requests.csv

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งออก CSV** | — | toast **ส่งออก 12 รายการ** · ดาวน์โหลด change-requests.csv | ☐ |

#### TC-L11 — เมนู ⋮ ตามสถานะ [AI-DEFAULT]
- group: รายการ · ความสำคัญ: กลาง · trace: U5 / DEC-11
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เมนูมีเฉพาะคำสั่งที่ทำได้ · ไม่มีทำซ้ำ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ⋮ แถว **ITCR-2569-0008** (ร่าง) | — | เห็น **ดูรายละเอียด** · **แก้ไข** · **พิมพ์** · **ยกเลิกเอกสาร** · ไม่มี "ทำซ้ำ" ⚠ | ☐ |
| 2 | CLICK ⋮ แถว **ITCR-2569-0002** (อนุมัติแล้ว) | — | เห็น **ดูรายละเอียด** · **พิมพ์** เท่านั้น | ☐ |

### กลุ่ม สร้าง

#### TC-C01 — สร้างคำขอแล้วบันทึกแบบร่าง ได้เลข ITCR [AI-DEFAULT]
- group: สร้าง · ความสำคัญ: สูง · trace: S-01 / FN-02 / DEC-10 / BR-06
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: ชุด A
- ผ่านเมื่อ: ได้ใบร่างเลข ITCR-2569-0013

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างคำขอ** | — | drawer **สร้าง Change Request** · ขั้น **ข้อมูลหลักคำขอ** | ☐ |
| 2 | TYPE → **เรื่องที่ต้องการ** | อัปเดตเวอร์ชันระบบเงินเดือน | ช่องแสดงข้อความ | ☐ |
| 3 | TOGGLE **ระบบซอฟต์แวร์** + **ความปลอดภัย** | — | ติ๊ก 2 ช่อง · การ์ดสรุป **ประเภทของการเปลี่ยนแปลง** = ระบบซอฟต์แวร์ · ความปลอดภัย | ☐ |
| 4 | SELECT **วันที่ต้องการส่งมอบ** | 24 ต.ค. 2569 | ช่องแสดง 24 ต.ค. 2569 | ☐ |
| 5 | TYPE → **สถานที่ส่งมอบ** | ห้อง Server อาคาร 1 | การ์ดสรุปแสดง ห้อง Server อาคาร 1 | ☐ |
| 6 | TYPE → **รายละเอียดของการเปลี่ยนแปลง** / **วัตถุประสงค์ของการเปลี่ยนแปลง** / **ระบบที่ได้รับผลกระทบและ ผลกระทบที่อาจเกิดขึ้น** / **แผนการดำเนินการ** | ตามชุด A | ทุกช่องไม่มีขอบแดง | ☐ |
| 7 | CLICK **ถัดไป** | — | ขั้น **เอกสารแนบ** | ☐ |
| 8 | CLICK **ถัดไป** | — | ขั้น **ตรวจสอบและยืนยัน** | ☐ |
| 9 | CLICK **บันทึกแบบร่าง** | — | toast **บันทึกร่างแล้ว · ITCR-2569-0013** · แถวใหม่สถานะ **ร่าง** | ☐ |

#### TC-C02 — บันทึกและส่งอนุมัติต่อเนื่อง
- group: สร้าง · ความสำคัญ: สูง · trace: S-01 / S-06 / FN-03
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: ชุด A
- ผ่านเมื่อ: ใบเข้าสถานะรออนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างคำขอ** | — | drawer เปิด | ☐ |
| 2 | TYPE → **เรื่องที่ต้องการ** | อัปเดตเวอร์ชันระบบเงินเดือน | ช่องแสดงข้อความ | ☐ |
| 3 | TOGGLE **ระบบซอฟต์แวร์** + **ความปลอดภัย** | — | ติ๊ก 2 ช่อง · การ์ดสรุป **ประเภทของการเปลี่ยนแปลง** = ระบบซอฟต์แวร์ · ความปลอดภัย | ☐ |
| 4 | SELECT **วันที่ต้องการส่งมอบ** | 24 ต.ค. 2569 | ช่องแสดง 24 ต.ค. 2569 | ☐ |
| 5 | TYPE → **สถานที่ส่งมอบ** | ห้อง Server อาคาร 1 | การ์ดสรุปแสดง ห้อง Server อาคาร 1 | ☐ |
| 6 | TYPE → **รายละเอียดของการเปลี่ยนแปลง** / **วัตถุประสงค์ของการเปลี่ยนแปลง** / **ระบบที่ได้รับผลกระทบและ ผลกระทบที่อาจเกิดขึ้น** / **แผนการดำเนินการ** | ตามชุด A | ทุกช่องไม่มีขอบแดง | ☐ |
| 7 | CLICK **ถัดไป** | — | ขั้น 2 | ☐ |
| 8 | CLICK **ถัดไป** | — | ขั้น 3 | ☐ |
| 9 | CLICK **บันทึกและส่งอนุมัติ** | — | modal **ส่งอนุมัติ?** · 2 แถวผู้พิจารณา **ตรวจสอบโดย** · **อนุมัติโดย** | ☐ |
| 10 | CLICK **ส่งอนุมัติ** | — | toast **ส่งอนุมัติแล้ว · ITCR-2569-0013** · สถานะ **รออนุมัติ** | ☐ |

#### TC-C03 — การ์ดสรุปแสดงข้อมูลจากระบบ ไม่ใช่ช่องกรอก [AI-DEFAULT]
- group: สร้าง · ความสำคัญ: กลาง · trace: DEC-06 / DEC-12 / 01 §1.3
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ชื่อ/ตำแหน่ง/วันที่/ผู้พิจารณาอยู่ในการ์ดสรุป

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างคำขอ** | — | การ์ด **สรุปคำขอ** ด้านขวา | ☐ |
| 2 | VERIFY การ์ดสรุป | — | เห็น **สมชาย ตัวอย่างดี** · **เจ้าหน้าที่บัญชี** · **ตรวจสอบโดย (ค่าเริ่มจากสายอนุมัติ)** · **อนุมัติโดย (ค่าเริ่มจากสายอนุมัติ)** · **อนุชา ระบบดี** | ☐ |
| 3 | VERIFY ป้ายช่อง | — | เห็น **เรื่องที่ต้องการ** · **ประเภทของการเปลี่ยนแปลง** · **วันที่ต้องการส่งมอบ** · **สถานที่ส่งมอบ** · ไม่มีช่องกรอกชื่อ ⚠ | ☐ |

#### TC-C04 — คำอธิบายใต้ช่องตรงกระดาษ
- group: สร้าง · ความสำคัญ: ต่ำ · trace: DEC-06 / 01 §1.3
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นคำอธิบายตามแบบฟอร์ม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างคำขอ** | — | drawer เปิด | ☐ |
| 2 | VERIFY ใต้ช่องรายละเอียด | — | เห็น **(อธิบายรายละเอียดเกี่ยวกับการเปลี่ยนแปลง เช่น การอัปเดตซอฟต์แวร์ การเปลี่ยนอุปกรณ์ ฯลฯ)** | ☐ |
| 3 | VERIFY ใต้ช่องแผน | — | เห็น **(ระบุขั้นตอน เช่น การสำรองข้อมูล การทดสอบ การติดตั้ง การตรวจสอบหลังดำเนินการ)** | ☐ |

#### TC-C05 — แก้ไขร่างของตัวเอง
- group: สร้าง · ความสำคัญ: กลาง · trace: API-04 / U15
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R8`
- ชุดข้อมูล: เรื่อง: เปิดสิทธิ์ VPN (แก้)
- ผ่านเมื่อ: บันทึกแล้วข้อความใหม่แสดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **แก้ไข** | — | drawer **แก้ไขคำขอ ITCR-2569-0008** · ช่องมีค่าเดิม | ☐ |
| 2 | TYPE → **เรื่องที่ต้องการ** | เปิดสิทธิ์ VPN (แก้) | ช่องแสดงค่าใหม่ | ☐ |
| 3 | CLICK **ถัดไป** ×2 แล้ว **บันทึกแบบร่าง** | — | toast **บันทึกร่างแล้ว · ITCR-2569-0008** | ☐ |

### กลุ่ม ตรวจข้อมูล

#### TC-V01 — กดถัดไปตอนฟอร์มว่าง
- group: ตรวจข้อมูล · ความสำคัญ: สูง · trace: VR-01 / VR-04 / VR-05 / VR-09 (auto: e2e S7)
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: ว่างทั้งหมด
- ผ่านเมื่อ: บล็อก + ช่องแดง + toast

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างคำขอ** | — | drawer เปิด | ☐ |
| 2 | CLICK **ถัดไป** | — | อยู่ขั้น 1 · toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |
| 3 | VERIFY ข้อความใต้ช่อง | — | เห็น **ระบุเรื่องที่ต้องการ** · **เลือกวันที่ต้องการส่งมอบ** · **ระบุสถานที่ส่งมอบ** · **ระบุแผนการดำเนินการ** | ☐ |

#### TC-V02 — ไม่ติ๊กประเภทของการเปลี่ยนแปลง [AI-DEFAULT]
- group: ตรวจข้อมูล · ความสำคัญ: สูง · trace: VR-02 / BR-01 / DEC-16 / EC-03
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: ชุด A แต่ไม่ติ๊กประเภท
- ผ่านเมื่อ: บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างคำขอ** | — | drawer เปิด | ☐ |
| 2 | TYPE → ทุกช่องตามชุด A (ไม่ติ๊กประเภท) | ชุด A | — | ☐ |
| 3 | CLICK **ถัดไป** | — | เห็น **เลือกประเภทของการเปลี่ยนแปลงอย่างน้อย 1 ข้อ** | ☐ |

#### TC-V03 — ติ๊กหลายประเภทได้ [AI-DEFAULT]
- group: ตรวจข้อมูล · ความสำคัญ: กลาง · trace: BR-01 / DEC-04
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: ฮาร์ดแวร์ + เครือข่าย
- ผ่านเมื่อ: ติ๊กได้ทั้งสอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างคำขอ** | — | drawer เปิด | ☐ |
| 2 | TOGGLE **ฮาร์ดแวร์** แล้ว **เครือข่าย** | — | ติ๊กทั้งคู่ · การ์ดสรุป **ฮาร์ดแวร์ · เครือข่าย** | ☐ |
| 3 | VERIFY คำช่วย | — | เห็น **เลือกได้มากกว่า 1 ข้อ** | ☐ |

#### TC-V04 — ติ๊ก อื่นๆ แต่ไม่ระบุ
- group: ตรวจข้อมูล · ความสำคัญ: สูง · trace: VR-03 / BR-02 / DEC-15 / EC-02
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: ชุด B (ช่องอื่นๆ ว่าง)
- ผ่านเมื่อ: บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างคำขอ** | — | drawer เปิด | ☐ |
| 2 | TOGGLE **อื่นๆ** | — | ช่องกรอก placeholder **ระบุประเภทอื่นๆ** โผล่ | ☐ |
| 3 | CLICK **ถัดไป** (กรอกช่องอื่นครบ เว้นอื่นๆ) | — | เห็น **ระบุประเภทอื่นๆ** ใต้ช่อง | ☐ |
| 4 | TYPE → ช่องอื่นๆ | นโยบายบัญชีผู้ใช้ | ขอบแดงหาย · กดถัดไปได้ | ☐ |

#### TC-V05 — วันที่ต้องการส่งมอบก่อนวันที่ขอ = เตือน ไม่บล็อก [AI-DEFAULT]
- group: ตรวจข้อมูล · ความสำคัญ: สูง · trace: BR-03 / DEC-04 / DEC-14 / EC-01
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: ส่งมอบ 5 ต.ค. 2569
- ผ่านเมื่อ: ส่งได้ แต่เห็นข้อความเตือน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างคำขอ** | — | drawer เปิด | ☐ |
| 2 | SELECT **วันที่ต้องการส่งมอบ** | 5 ต.ค. 2569 | ใต้ช่องเห็น **ก่อนวันที่ขอ — ตรวจอีกครั้ง (เตือน ไม่บล็อก)** | ☐ |
| 3 | CLICK **ถัดไป** ×2 (ช่องอื่นครบ) | ชุด A | ขั้น 3 เห็น **วันที่ต้องการส่งมอบอยู่ก่อนวันที่ขอ — ส่งได้ แต่ตรวจอีกครั้ง** | ☐ |

#### TC-V06 — เว้นวัตถุประสงค์และผลกระทบ
- group: ตรวจข้อมูล · ความสำคัญ: กลาง · trace: VR-07 / VR-08
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: ชุด A เว้น 2 ช่อง
- ผ่านเมื่อ: บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างคำขอ** | — | drawer เปิด | ☐ |
| 2 | CLICK **ถัดไป** (เว้นวัตถุประสงค์+ผลกระทบ) | — | เห็น **ระบุวัตถุประสงค์ของการเปลี่ยนแปลง** · **ระบุระบบที่ได้รับผลกระทบและผลกระทบที่อาจเกิดขึ้น** | ☐ |

#### TC-V07 — เว้นรายละเอียดของการเปลี่ยนแปลง
- group: ตรวจข้อมูล · ความสำคัญ: กลาง · trace: VR-06
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: ชุด A เว้นรายละเอียด
- ผ่านเมื่อ: บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างคำขอ** | — | drawer เปิด | ☐ |
| 2 | CLICK **ถัดไป** | — | เห็น **ระบุรายละเอียดของการเปลี่ยนแปลง** | ☐ |

### กลุ่ม ไฟล์แนบ

#### TC-F01 — แนบไฟล์ PDF [AI-DEFAULT]
- group: ไฟล์แนบ · ความสำคัญ: กลาง · trace: S-05 / DEC-11 / API-11
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=แผนติดตั้ง-ระบบบัญชี.pdf
- Start: OPEN `#/change-request`
- ชุดข้อมูล: แผนติดตั้ง-ระบบบัญชี.pdf
- ผ่านเมื่อ: ไฟล์อยู่ในรายการแนบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างคำขอ** → กรอกชุด A → **ถัดไป** | ชุด A | ขั้น **เอกสารแนบ** เห็น **คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)** | ☐ |
| 2 | UPLOAD ไฟล์ | แผนติดตั้ง-ระบบบัญชี.pdf | เห็นแถว **แผนติดตั้ง-ระบบบัญชี.pdf** | ☐ |

#### TC-F02 — แนบไฟล์ชนิดไม่รองรับ
- group: ไฟล์แนบ · ความสำคัญ: กลาง · trace: S-05 / file_policy
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=setup.exe
- Start: OPEN `#/change-request`
- ชุดข้อมูล: setup.exe
- ผ่านเมื่อ: ไม่รับไฟล์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างคำขอ** → กรอกชุด A → **ถัดไป** | ชุด A | ขั้น 2 | ☐ |
| 2 | UPLOAD ไฟล์ | setup.exe | toast **setup.exe — ชนิดไฟล์ไม่รองรับ** · ไม่มีแถวไฟล์ | ☐ |

#### TC-F03 — ลบไฟล์ที่แนบ
- group: ไฟล์แนบ · ความสำคัญ: ต่ำ · trace: S-05
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=แผนติดตั้ง-ระบบบัญชี.pdf
- Start: OPEN `#/change-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไฟล์หายจากรายการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | UPLOAD ไฟล์ในขั้น 2 | แผนติดตั้ง-ระบบบัญชี.pdf | เห็นแถวไฟล์ | ☐ |
| 2 | CLICK ปุ่มถังขยะ **ลบไฟล์** | — | แถวไฟล์หาย | ☐ |

### กลุ่ม ส่งอนุมัติ

#### TC-D01 — modal ส่งอนุมัติ = 1 แถวต่อขั้น DOA (ค่าเริ่ม 2) [AI-DEFAULT]
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: S-06 / FN-03 / BR-04 / DEC-03 (auto: e2e S8)
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: 2 แถว ค่าเริ่มจากผัง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** | — | modal **ส่งอนุมัติ?** | ☐ |
| 2 | VERIFY แถวผู้พิจารณา | — | แถว 1 **ตรวจสอบโดย** = **วิไลวรรณ ทดสอบงาน** · แถว 2 **อนุมัติโดย** = **อนุชา ระบบดี** · เห็น **ค่าเริ่มต้นจากสายอนุมัติและผังองค์กร** | ☐ |
| 3 | CLICK **ส่งอนุมัติ** | — | toast **ส่งอนุมัติแล้ว · ITCR-2569-0008** · แบนเนอร์ **รอ วิไลวรรณ ทดสอบงาน พิจารณา (ขั้น 1 · ตรวจสอบโดย)** | ☐ |

#### TC-D02 — ไม่เลือกผู้พิจารณา
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: VR-10 / ASSIGNEE_REQUIRED
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R8`
- ชุดข้อมูล: ล้างแถว 2
- ผ่านเมื่อ: บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** | — | modal เปิด | ☐ |
| 2 | SELECT แถว **อนุมัติโดย** → ล้างค่า | — | ช่องว่าง | ☐ |
| 3 | CLICK **ส่งอนุมัติ** | — | เห็น **กรุณาเลือกผู้พิจารณา** · สถานะยังร่าง | ☐ |

#### TC-D03 — DOA เพิ่มเป็น 3 ขั้น (dynamic) [AI-DEFAULT]
- group: ส่งอนุมัติ · ความสำคัญ: กลาง · trace: BR-04 / DEC-03 / EC-05 (auto: e2e S8)
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · PRESS console `__QA__.doa.push('ขั้นทดสอบ')` · files=—
- Start: OPEN `#/change-request/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal มี 3 แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console | __QA__.doa.push('ขั้นทดสอบ') | — | ☐ |
| 2 | CLICK **ส่งอนุมัติ** | — | modal มี 3 แถว แถว 3 **ขั้นทดสอบ** | ☐ |

#### TC-D04 — ผู้ขอไม่อยู่ในรายชื่อผู้พิจารณา
- group: ส่งอนุมัติ · ความสำคัญ: สูง · trace: BR-DOA-04 / SELF_APPROVE / EC-06
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีชื่อตัวเองให้เลือก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** | — | modal เปิด | ☐ |
| 2 | CLICK ช่องแถว **ตรวจสอบโดย** | — | รายชื่อไม่มี **สมชาย ตัวอย่างดี** ⚠ | ☐ |

#### TC-D05 — ส่งใบที่ถูกตีกลับใหม่ resolve สายใหม่ [AI-DEFAULT]
- group: ส่งอนุมัติ · ความสำคัญ: กลาง · trace: BR-05 / DEC-08
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ส่งได้ เริ่มขั้น 1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แบนเนอร์ | — | **ไม่อนุมัติ — กลับเป็นร่าง: แผนการดำเนินการยังไม่ชัดเจน — ระบุวันเวลาที่ปิดระบบ** | ☐ |
| 2 | CLICK **ส่งอนุมัติ** → **ส่งอนุมัติ** | — | toast **ส่งอนุมัติแล้ว · ITCR-2569-0007** · แท็บ **ลายเซ็น / อนุมัติ** ขั้น 1 **รอพิจารณา** | ☐ |

### กลุ่ม อนุมัติ

#### TC-A01 — ขั้น 1 อนุมัติ → ไปขั้น 2 [AI-DEFAULT]
- group: อนุมัติ · ความสำคัญ: สูง · trace: S-07 / FN-04 / BR-04
- actor (role): ผู้ตรวจสอบ
- Setup: role=ผู้ตรวจสอบ ขั้น 1 (__QA__.setMe('E02')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ยังรออนุมัติ · ขั้น 2 เป็นขั้นปัจจุบัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **อนุมัติ** | — | modal **อนุมัติคำขอนี้?** | ☐ |
| 2 | CLICK **อนุมัติ** | — | toast **อนุมัติแล้ว · ITCR-2569-0006** | ☐ |
| 3 | VERIFY แบนเนอร์ | — | **รอ อนุชา ระบบดี พิจารณา (ขั้น 2 · อนุมัติโดย)** · ลายเซ็น **1/2** | ☐ |

#### TC-A02 — ขั้น 2 อนุมัติ → อนุมัติแล้ว [AI-DEFAULT]
- group: อนุมัติ · ความสำคัญ: สูง · trace: S-07 / FN-04 / DEC-01
- actor (role): ผู้จัดการฝ่าย IT
- Setup: role=ผู้จัดการฝ่าย IT ขั้น 2 (__QA__.setMe('E10')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R12`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สถานะอนุมัติแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **อนุมัติ** → **อนุมัติ** | — | toast **อนุมัติแล้ว · ITCR-2569-0012** | ☐ |
| 2 | VERIFY แบนเนอร์ | — | **อนุมัติครบทุกขั้นแล้ว — แจ้งฝ่าย IT ดำเนินการเปลี่ยนแปลงตามแผน** · pill **อนุมัติแล้ว** | ☐ |
| 3 | CLICK แท็บ **ลายเซ็น / อนุมัติ** | — | ผลลัพธ์ **อนุมัติครบ — แจ้งฝ่าย IT ดำเนินการ** | ☐ |

#### TC-A03 — ไม่อนุมัติโดยไม่ใส่เหตุผล
- group: อนุมัติ · ความสำคัญ: สูง · trace: VR-11 / REASON_REQUIRED
- actor (role): ผู้ตรวจสอบ
- Setup: role=ผู้ตรวจสอบ ขั้น 1 (__QA__.setMe('E02')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R6`
- ชุดข้อมูล: เหตุผลว่าง
- ผ่านเมื่อ: บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ไม่อนุมัติ** | — | modal **ไม่อนุมัติคำขอนี้?** | ☐ |
| 2 | CLICK **ไม่อนุมัติ** (เหตุผลว่าง) | — | เห็น **กรุณาระบุเหตุผล** · สถานะไม่เปลี่ยน | ☐ |

#### TC-A04 — ไม่อนุมัติขั้น 2 → กลับร่างเลขเดิม [AI-DEFAULT]
- group: อนุมัติ · ความสำคัญ: สูง · trace: S-08 / FN-05 / BR-05 / DEC-08 / EC-11
- actor (role): ผู้จัดการฝ่าย IT
- Setup: role=ผู้จัดการฝ่าย IT ขั้น 2 (__QA__.setMe('E10')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R12`
- ชุดข้อมูล: เหตุผล: แผนยังไม่ชัด
- ผ่านเมื่อ: ใบกลับเป็นร่าง · ผู้พิจารณาไม่เห็น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ไม่อนุมัติ** | — | modal เห็น **เอกสารจะกลับเป็นร่างเลขเดิม ให้ผู้ขอแก้แล้วส่งใหม่** | ☐ |
| 2 | TYPE → **เหตุผล** | แผนยังไม่ชัด | — | ☐ |
| 3 | CLICK **ไม่อนุมัติ** | — | toast **ไม่อนุมัติ — ส่งกลับเป็นร่าง · ITCR-2569-0012** · drawer ปิด (ไม่มีสิทธิ์เห็นร่าง) | ☐ |

#### TC-A05 — เลือกเหตุผลสำเร็จรูป [AI-DEFAULT]
- group: อนุมัติ · ความสำคัญ: ต่ำ · trace: U9
- actor (role): ผู้ตรวจสอบ
- Setup: role=ผู้ตรวจสอบ ขั้น 1 (__QA__.setMe('E02')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ช่องเหตุผลเติมข้อความ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ไม่อนุมัติ** | — | เห็นชิป **ข้อมูลไม่ครบ ขอรายละเอียดเพิ่ม** · **แผนการดำเนินการยังไม่ชัดเจน** · **ผลกระทบสูงเกินไปในช่วงนี้** | ☐ |
| 2 | CLICK ชิป **แผนการดำเนินการยังไม่ชัดเจน** | — | ช่องเหตุผลขึ้นต้น **แผนการดำเนินการยังไม่ชัดเจน** | ☐ |

### กลุ่ม ยกเลิก

#### TC-K01 — เจ้าของยกเลิกร่าง [AI-DEFAULT]
- group: ยกเลิก · ความสำคัญ: สูง · trace: S-09 / FN-06 / DEC-08
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R8`
- ชุดข้อมูล: เหตุผล: บันทึกผิด
- ผ่านเมื่อ: สถานะยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยกเลิก** | — | modal **ยกเลิกเอกสาร?** | ☐ |
| 2 | CLICK ชิป **บันทึกผิด** → **ยกเลิกเอกสาร** | — | toast **ยกเลิกเอกสารแล้ว · ITCR-2569-0008** · pill **ยกเลิก** | ☐ |

#### TC-K02 — ยกเลิกโดยไม่ใส่เหตุผล
- group: ยกเลิก · ความสำคัญ: กลาง · trace: VR-11 / REASON_REQUIRED
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R8`
- ชุดข้อมูล: เหตุผลว่าง
- ผ่านเมื่อ: บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยกเลิก** → **ยกเลิกเอกสาร** | — | เห็น **กรุณาระบุเหตุผล** | ☐ |

#### TC-K03 — ใบอนุมัติแล้วยกเลิกไม่ได้ [AI-DEFAULT]
- group: ยกเลิก · ความสำคัญ: สูง · trace: DEC-08 / NOT_DRAFT / DN-06
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R2`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว drawer | — | ไม่มี **ยกเลิกเอกสาร** ⚠ · footer เห็น **อนุมัติแล้ว ล็อกแก้ไข** | ☐ |

#### TC-K04 — เจ้าหน้าที่ IT ยกเลิกใบรออนุมัติ [AI-DEFAULT]
- group: ยกเลิก · ความสำคัญ: กลาง · trace: FN-06 / DEC-08 / 05 §5.3
- actor (role): เจ้าหน้าที่ IT
- Setup: role=เจ้าหน้าที่ IT (__QA__.setMe('E08')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R5`
- ชุดข้อมูล: เหตุผล: ส่งคำขอใหม่แทน
- ผ่านเมื่อ: สถานะยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยกเลิกเอกสาร** | — | modal **ยกเลิกเอกสาร?** | ☐ |
| 2 | TYPE → **เหตุผล** → CLICK **ยกเลิกเอกสาร** | ส่งคำขอใหม่แทน | toast **ยกเลิกเอกสารแล้ว · ITCR-2569-0005** | ☐ |

### กลุ่ม สิทธิ์

#### TC-P01 — ผู้ตรวจสอบไม่เห็นร่างของคนอื่น [AI-DEFAULT]
- group: สิทธิ์ · ความสำคัญ: สูง · trace: DEC-09 / BR-07 / DN-01 (auto: e2e S3)
- actor (role): ผู้ตรวจสอบ
- Setup: role=ผู้ตรวจสอบ ขั้น 1 (__QA__.setMe('E02')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่เห็นร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตาราง | — | ไม่เห็น **ITCR-2569-0007** และ **ITCR-2569-0008** ⚠ (ร่างของผู้ขอ) | ☐ |

#### TC-P02 — เปิด route ใบร่างของคนอื่นตรง ๆ [AI-DEFAULT]
- group: สิทธิ์ · ความสำคัญ: สูง · trace: DN-02 / NOT_FOUND / EC-10 (auto: e2e S6)
- actor (role): ผู้ตรวจสอบ
- Setup: role=ผู้ตรวจสอบ ขั้น 1 (__QA__.setMe('E02')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: drawer ไม่เปิด

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/change-request/view/R8` | — | ยังอยู่หน้ารายการ ไม่มี drawer ⚠ | ☐ |

#### TC-P03 — ผู้ขออนุมัติใบตัวเองไม่ได้
- group: สิทธิ์ · ความสำคัญ: สูง · trace: DN-03 / BR-DOA-04
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มอนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว drawer | — | ไม่มี **อนุมัติ** ⚠ · มี **ยกเลิกเอกสาร** | ☐ |

#### TC-P04 — ผู้พิจารณาขั้น 2 ตัดสินก่อนขั้น 1 ไม่ได้
- group: สิทธิ์ · ความสำคัญ: สูง · trace: DN-04 / NOT_CURRENT_APPROVER
- actor (role): ผู้จัดการฝ่าย IT
- Setup: role=ผู้จัดการฝ่าย IT ขั้น 2 (__QA__.setMe('E10')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มอนุมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แบนเนอร์ | — | **รอ วิไลวรรณ ทดสอบงาน พิจารณา (ขั้น 1 · ตรวจสอบโดย)** · ไม่มีปุ่ม **อนุมัติ** ⚠ | ☐ |

#### TC-P05 — เจ้าหน้าที่ IT เห็นทุกใบ [AI-DEFAULT]
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: DEC-09 / 05 §5.3
- actor (role): เจ้าหน้าที่ IT
- Setup: role=เจ้าหน้าที่ IT (__QA__.setMe('E08')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 12 ใบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY badge | — | **12 รายการ** · เห็น **ITCR-2569-0009** (ร่างของคนอื่น) | ☐ |

#### TC-P06 — เจ้าหน้าที่ IT แก้ร่างของคนอื่นไม่ได้
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: DN-05 / NOT_OWNER
- actor (role): เจ้าหน้าที่ IT
- Setup: role=เจ้าหน้าที่ IT (__QA__.setMe('E08')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R9`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มแก้ไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว drawer | — | ไม่มี **แก้ไข** ⚠ · มี **ยกเลิกเอกสาร** | ☐ |

#### TC-P07 — แบบเอกสารปิดใช้ สร้างไม่ได้
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: DN-07 / EC-09 / DOC_TYPE_INACTIVE
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · PRESS console `__QA__.setDocActive(false)` · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปุ่มสร้าง disabled

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console | __QA__.setDocActive(false) | เห็น **แบบเอกสารนี้ยังไม่เปิดใช้งาน — สร้างคำขอใหม่ไม่ได้** · ปุ่ม **สร้างคำขอ** กดไม่ได้ | ☐ |

### กลุ่ม แบบพิมพ์

#### TC-R01 — PDF ใบอนุมัติแล้ว ตรงแบบฟอร์ม FM-ITS-07 [AI-DEFAULT]
- group: แบบพิมพ์ · ความสำคัญ: สูง · trace: S-10 / FN-07 / DEC-06 / DEC-07 / DEC-12 / DEC-13 / DEC-17 / BR-08 / BR-10 / BR-11
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R2`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ช่อง/ป้ายตามกระดาษ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | เห็นหัว **Change Request Form** | ☐ |
| 2 | VERIFY ตาราง | — | เห็น **วันที่** · **ตำแหน่ง** · **ชื่อ-นามสกุล** · **วันที่ต้องการส่งมอบ** · **สถานที่ส่งมอบ** · **เรื่องที่ต้องการ** · **ประเภทของการเปลี่ยนแปลง:** ☑ **ฮาร์ดแวร์** | ☐ |
| 3 | VERIFY ช่องลงชื่อ | — | 3 ช่อง **ผู้ขอซื้อ** · **ตรวจสอบโดย** · **อนุมัติโดย** · ข้อความ **พิจารณาในระบบ** (ไม่มีภาพลายเซ็น) | ☐ |
| 4 | VERIFY footer | — | **เลขที่ ITCR-2569-0002** · **Doc. No. : FM-ITS-07 · Rev.00 : 01/07/2569** | ☐ |

#### TC-R02 — PDF ใบร่างมีคำว่า ร่าง
- group: แบบพิมพ์ · ความสำคัญ: กลาง · trace: S-10 / FN-07
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: footer มี ร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | footer **เลขที่ ITCR-2569-0008 · ร่าง** · ช่องผู้พิจารณาบรรทัดวันที่ **วันที่ ........./........./.........** | ☐ |

#### TC-R03 — PDF ติ๊กประเภทตรงที่เลือก
- group: แบบพิมพ์ · ความสำคัญ: กลาง · trace: S-02 / FN-07
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ☑ 2 ช่อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | ☑ **ระบบซอฟต์แวร์** · ☑ **ความปลอดภัย** · ☐ **ฮาร์ดแวร์** · ☐ **เครือข่าย** | ☐ |

#### TC-R04 — PDF ใบ อื่นๆ แสดงข้อความระบุ
- group: แบบพิมพ์ · ความสำคัญ: ต่ำ · trace: BR-02 / FN-07
- actor (role): เจ้าหน้าที่ IT
- Setup: role=เจ้าหน้าที่ IT (__QA__.setMe('E08')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R9`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นข้อความอื่นๆ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | ☑ **อื่นๆ** ตามด้วย **นโยบายบัญชีผู้ใช้** | ☐ |

#### TC-R05 — PDF ช่องลงชื่อตามจำนวนขั้น DOA [AI-DEFAULT]
- group: แบบพิมพ์ · ความสำคัญ: กลาง · trace: DEC-07 / EC-05 / BR-08
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · PRESS console `__QA__.doa.push('ขั้นทดสอบ')` · files=—
- Start: OPEN `#/change-request/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ลายเซ็นเพิ่มตามขั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console | __QA__.doa.push('ขั้นทดสอบ') | — | ☐ |
| 2 | CLICK **ส่งอนุมัติ** → **ส่งอนุมัติ** | — | ส่งแล้ว | ☐ |
| 3 | CLICK แท็บ **PDF Preview** | — | ช่องลงชื่อ 4 ช่อง รวม **ขั้นทดสอบ** | ☐ |

#### TC-R06 — พิมพ์/ดาวน์โหลด PDF
- group: แบบพิมพ์ · ความสำคัญ: ต่ำ · trace: API-09
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R2`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เปิดหน้าต่างพิมพ์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ดาวน์โหลด PDF** | — | toast **เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ · ITCR-2569-0002** | ☐ |

### กลุ่ม Error/UX

#### TC-E01 — ส่งอนุมัติแล้ว API ล้มเหลว
- group: Error/UX · ความสำคัญ: กลาง · trace: ER-01 (auto: e2e S9)
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · PRESS console `__QA__.sim('error')` · files=—
- Start: OPEN `#/change-request/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สถานะยังร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console | __QA__.sim('error') | — | ☐ |
| 2 | CLICK **ส่งอนุมัติ** → **ส่งอนุมัติ** | — | toast **ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง** · pill **ร่าง** | ☐ |

#### TC-E02 — ข้อมูลชนกัน (stale)
- group: Error/UX · ความสำคัญ: กลาง · trace: ER-02 / STALE / EC-08
- actor (role): ผู้ตรวจสอบ
- Setup: role=ผู้ตรวจสอบ ขั้น 1 (__QA__.setMe('E02')) · seed=RECS · PRESS console `__QA__.sim('stale')` · files=—
- Start: OPEN `#/change-request/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สถานะไม่เปลี่ยน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console | __QA__.sim('stale') | — | ☐ |
| 2 | CLICK **อนุมัติ** → **อนุมัติ** | — | toast **ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่** · ลายเซ็น **0/2** | ☐ |

#### TC-E03 — Esc ปิด modal ก่อน drawer
- group: Error/UX · ความสำคัญ: ต่ำ · trace: ER-03 (auto: e2e S10)
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปิดทีละชั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งอนุมัติ** | — | modal เปิด | ☐ |
| 2 | PRESS Esc | — | modal ปิด drawer ยังเปิด | ☐ |
| 3 | PRESS Esc | — | drawer ปิด | ☐ |

#### TC-E04 — ปิดฟอร์มที่กรอกค้าง
- group: Error/UX · ความสำคัญ: กลาง · trace: U8 dirty-check
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · files=—
- Start: OPEN `#/change-request`
- ชุดข้อมูล: เรื่อง: ทดสอบ
- ผ่านเมื่อ: ถามก่อนทิ้ง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างคำขอ** → TYPE **เรื่องที่ต้องการ** | ทดสอบ | — | ☐ |
| 2 | PRESS Esc | — | modal **ทิ้งข้อมูลที่กรอกไว้?** | ☐ |
| 3 | CLICK **กลับไปกรอกต่อ** | — | ข้อความ ทดสอบ ยังอยู่ | ☐ |

#### TC-E05 — คลิกพื้นหลังขณะกรอกเหตุผลค้าง modal ไม่ปิด
- group: Error/UX · ความสำคัญ: ต่ำ · trace: U25
- actor (role): ผู้ตรวจสอบ
- Setup: role=ผู้ตรวจสอบ ขั้น 1 (__QA__.setMe('E02')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal ไม่ปิดเมื่อพิมพ์เหตุผลค้าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ไม่อนุมัติ** → TYPE **เหตุผล** | ทดสอบ | — | ☐ |
| 2 | CLICK พื้นหลังมืดนอก modal | — | modal ยังเปิด (กรอกเหตุผลค้าง) | ☐ |

### กลุ่ม Cross-module

#### TC-X01 — อนุมัติครบ แจ้งเจ้าหน้าที่ IT (itcr_approved_for_it) [AI-DEFAULT]
- group: Cross-module · ความสำคัญ: กลาง · trace: XT · NTF itcr_approved_for_it / FN-04 / FN-08
- actor (role): ผู้จัดการฝ่าย IT
- Setup: role=ผู้จัดการฝ่าย IT ขั้น 2 (__QA__.setMe('E10')) · seed=RECS · ENG-NOTIFY (ต้อง simulate) · files=—
- Start: OPEN `#/change-request/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สถานะอนุมัติแล้ว (แจ้งเตือนตรวจที่ระบบจริง)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **อนุมัติ** → **อนุมัติ** | — | toast **อนุมัติแล้ว · ITCR-2569-0003** · pill **อนุมัติแล้ว** | ☐ |
| 2 | CLICK แท็บ **ประวัติ** | — | เห็น **อนุมัติ** โดย **อนุชา ระบบดี** (event itcr_approved_for_it ยิงที่ระบบจริง ⚠) | ☐ |

#### TC-X02 — ยกเลิกใบรออนุมัติ แจ้งผู้พิจารณา (itcr_cancelled)
- group: Cross-module · ความสำคัญ: กลาง · trace: XT · NTF itcr_cancelled / FN-06
- actor (role): ผู้ขอ
- Setup: role=ผู้ขอ (__QA__.setMe('E01')) · seed=RECS · ENG-NOTIFY (ต้อง simulate) · files=—
- Start: OPEN `#/change-request/view/R6`
- ชุดข้อมูล: เหตุผล: ไม่ต้องการเปลี่ยนแปลงแล้ว
- ผ่านเมื่อ: สถานะยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยกเลิกเอกสาร** → ชิป **ไม่ต้องการเปลี่ยนแปลงแล้ว** → **ยกเลิกเอกสาร** | — | toast **ยกเลิกเอกสารแล้ว · ITCR-2569-0006** · แท็บ **ลายเซ็น / อนุมัติ** ขั้น 1 **ข้าม** | ☐ |

#### TC-X03 — อนุมัติแล้วไม่ส่งต่อระบบอื่น [AI-DEFAULT]
- group: Cross-module · ความสำคัญ: ต่ำ · trace: DEC-01 / DEC-02 / XT itcr.approved (ปิดรอบนี้)
- actor (role): เจ้าหน้าที่ IT
- Setup: role=เจ้าหน้าที่ IT (__QA__.setMe('E08')) · seed=RECS · files=—
- Start: OPEN `#/change-request/view/R1`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่ม/ลิงก์ส่งต่อ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว drawer | — | มีเฉพาะพิมพ์/ดาวน์โหลด/ปิด · ไม่มีปุ่มส่งต่อระบบอื่น ⚠ | ☐ |

## วิธีที่ agent รัน (Run protocol)
1. เปิด feature.html (ถ้า CDN ไอคอนถูกบล็อก ระบบยังใช้ได้)
2. สลับผู้ใช้ด้วย `__QA__.setMe('E01'|'E02'|'E10'|'E08')` ตาม Setup (E01 ผู้ขอ · E02 ผู้ตรวจสอบ ขั้น 1 · E10 ผู้จัดการฝ่าย IT ขั้น 2 · E08 เจ้าหน้าที่ IT)
3. รีโหลดหน้าก่อนแต่ละเคส (seed กลับค่าเริ่ม)
4. step PRESS console = เรียก hook ใน DevTools
5. บันทึกผลตาม schema ด้านล่าง · ⚠ = anchor เชิงปฏิเสธ/ต้องยืนยันด้วยตา

## Coverage Audit
| หมวด | covered / total |
|---|---|
| FR / Acceptance (S-01..S-11) | 11 / 11 |
| Business rules (BR-01..13 + BR-DOA) | 13 / 14 |
| Validation (VR) | 11 / 11 |
| Edge cases | 9 / 11 |
| Error codes | 9 / 9 |
| Permission cells | 11 / 11 |
| Cross-cutting / states | ครบ |

- Cross-Module (XT): 3/3
- Scope Lock (DEC): 17/17
- **Manifest cross-check (FRD §0.12): ✅ 5/5** (ช่องในฟอร์ม · ลายเซ็น · BRD stories · BR/VR/EC · DEC)

### ข้าม (พร้อมเหตุผล)
- BR-13 — ไม่มีรายการซ้ำบนกระดาษ ไม่มีพฤติกรรมให้ทดสอบ
- EC-04 — ข้อความยาวเกินบรรทัด ตรวจที่แบบพิมพ์ (long-text) ไม่ใช่หน้าจอ
- EC-07 — แก้ DOA ระหว่างรอ ไม่มีผลบน UI prototype (ตรวจ BE)

## Result Report (schema)
```json
{
  "feature_id": "F-TMP-005",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 61, "pass": 0, "fail": 0, "blocked": 0 }
}
```

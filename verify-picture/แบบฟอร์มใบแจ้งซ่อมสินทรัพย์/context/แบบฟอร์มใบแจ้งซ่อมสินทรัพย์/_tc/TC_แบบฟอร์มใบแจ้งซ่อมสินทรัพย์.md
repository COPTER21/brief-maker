# AI Test Cases — F-TMP-001 แบบฟอร์มใบแจ้งซ่อมสินทรัพย์

ชุดทดสอบสำหรับ AI agent (browser-use / vision) ทดสอบ prototype `feature.html` ของใบแจ้งซ่อมสินทรัพย์ (FM-ASM-03) — anchor ทุกจุดเป็นข้อความที่เห็นบนจอ (คัดจาก HTML จริง) · สลับผู้ใช้ด้วย `__QA__.setMe('E0x')` · เคสที่ derive จากมติ AI-DEFAULT ติด `[AI-DEFAULT]` (ผล fail อาจแปลว่า "ค่าเริ่มผิด" ไม่ใช่โค้ดผิด)

## Meta
| Field | Value |
|---|---|
| Feature ID | F-TMP-001 (รหัสชั่วคราว) |
| ชื่อ | แบบฟอร์มใบแจ้งซ่อมสินทรัพย์ (Asset Repair Request · RPR) |
| เวอร์ชัน | 1.0 · ai-testcase-md-generator v1.3 · Mode 0 |
| App entry | `feature.html` |
| Routes | `#/asset-repair` · `#/asset-repair/create` · `#/asset-repair/edit/:id` · `#/asset-repair/view/:id` |
| ที่มา | FRD_F-TMP-001_Pack v1.0 · BRD-ASM-RPR-001 · DECISIONS.lock (16 DEC) · feature.html (html-generator-v9.4) |
| จำนวนเคส | 50 |
| หมวด | L 7 · C 9 · V 5 · S 4 · A 6 · R 3 · X 3 · P 4 · D 7 · XT 2 |

## Coverage
| group | เคส | ความสำคัญ |
|---|---|---|
| L รายการ | 7 | สูง/กลาง |
| C สร้าง/แก้ร่าง | 9 | สูง |
| V ดูรายละเอียด | 5 | กลาง |
| S ส่งขออนุมัติ | 4 | สูง |
| A ตรวจสอบ/อนุมัติ | 6 | สูง |
| R ตีกลับเป็นร่าง | 3 | สูง |
| X ยกเลิก | 3 | กลาง |
| P แบบพิมพ์ PDF | 4 | สูง |
| D สิทธิ์ (deny) | 7 | สูง |
| XT cross-module | 2 | กลาง |

## Coverage Ledger
### FR / AC (06_TESTS §6.1)
| item | cases |
|---|---|
| AC-01 สร้าง + สรุปสด + เลข RPR | TC-C01, TC-C02 |
| AC-02 ถัดไปตอนว่าง = บล็อก | TC-C03 |
| AC-03 จำนวนไม่ถูกต้อง | TC-C04, TC-C05 |
| AC-04 ทะเบียนว่างได้ | TC-C06 |
| AC-05 modal ส่ง slot ต่อขั้น | TC-S01, TC-S02, TC-S03 |
| AC-06 ผู้ตรวจสอบกรอกประวัติซ่อม | TC-A01, TC-A02 |
| AC-07 ตรวจสอบแล้ว → อนุมัติ | TC-A03, TC-A04 |
| AC-08 ตีกลับเป็นร่าง | TC-R01, TC-R02, TC-R03 |
| AC-09 PDF ทุกสถานะ | TC-P01, TC-P02, TC-P03 |
| AC-10 DOA dynamic → ช่องลงชื่อ | TC-P04, TC-S04 |
| AC-11 ยกเลิก | TC-X01, TC-X02, TC-X03 |
| AC-12 admin เห็นทุกใบ + CSV + แท็บ | TC-L03, TC-L06, TC-L07 |
| AC-13 doc_type ปิดใช้ | TC-L05 |
### Business Rules (05_RULES)
| rule | cases |
|---|---|
| BR-01 ≥1 รายการ + ช่องบังคับ | TC-C03 |
| BR-02 จำนวน > 0 | TC-C04, TC-C05 |
| BR-03 ทะเบียนกรอกเอง [AI-DEFAULT] | TC-C06 |
| BR-04 ประวัติซ่อมขั้นแรก [AI-DEFAULT] | TC-A01, TC-A02, TC-A05 |
| BR-05 resolve + freeze | TC-S01, TC-R03 |
| BR-06 ไม่อนุมัติ → ร่างเลขเดิม | TC-R01, TC-R02 |
| BR-07 ออกเลขตอนบันทึกแรก | TC-C01 |
| BR-08 ร่างเห็นเฉพาะเจ้าของ | TC-D01, TC-D02 |
| BR-09 ช่องลงชื่อ dynamic + คำตาม role | TC-P02, TC-P04, TC-A03 |
| BR-10 ผู้แจ้ง 2 จุด | TC-P02 |
| BR-11 ป้ายตามกระดาษ | TC-C02, TC-P01 |
| BR-12 ไม่ส่งต่อระบบอื่น | TC-XT02 |
| BR-13 แนบไฟล์ · CSV · ไม่มีทำซ้ำ | TC-C07, TC-L06, TC-V05 |
| BR-DOA-01..05 | TC-S01, TC-D06, TC-D03, TC-R01 |
### Validation
| VR | cases |
|---|---|
| VR-01 | TC-C03 |
| VR-02 | TC-C04, TC-C05 |
| VR-03 | TC-S02, TC-D06 |
| VR-04 | TC-R02, TC-X02 |
| VR-05 | TC-A02 |
### Edge Cases
| EC | cases / สถานะ |
|---|---|
| EC-01 ไม่มีทะเบียน | TC-C06 |
| EC-02 รายการ > 10 | TC-P03 |
| EC-03 ผู้แจ้งถือ role-mgr-acc | — ข้าม (seed ไม่มีผู้แจ้งที่ถือ role-mgr-acc · ครอบด้วย TC-D06 SoD) |
| EC-04 แก้ DOA ระหว่างรอ | TC-S04 |
| EC-05 stale / error | TC-S03, TC-A06 |
| EC-06 doc_type ปิดใช้ | TC-L05 |
| EC-07 DOA หลายขั้น | TC-P04 |
| EC-08 แจ้งซ้ำ | — ข้าม (OQ-04 · ไม่ตรวจรอบนี้) |
| EC-09 ไม่กรอกประวัติ | TC-A05 |
### Error Codes
| error | cases |
|---|---|
| NOT_CURRENT_APPROVER | TC-D03 |
| NOT_OWNER | TC-D04 |
| SELF_APPROVAL | TC-D06 |
| REASON_REQUIRED | TC-R02 |
| HISTORY_INVALID | TC-A02 |
| STALE (409) | TC-A06 |
| 500 | TC-S03 |
| NOT_FOUND (404 route) | TC-D01 |
| DOC_TYPE_INACTIVE | TC-L05 |
| NOT_DRAFT / NOT_CANCELLABLE | TC-D05, TC-X03 |
### Permission Matrix (role × action)
| cell | cases |
|---|---|
| owner ดูร่างตน = allow | TC-V01 |
| approver ดูร่างคนอื่น = deny | TC-D01 |
| owner ดูร่างคนอื่น = deny | TC-D02 |
| assignee ไม่ใช่ขั้นปัจจุบัน ตัดสิน = deny | TC-D03 |
| คนนอก ยกเลิก = deny | TC-D04 |
| แก้ใบไม่ใช่ร่าง = deny | TC-D05 |
| admin ดูทั้งหมด + ยกเลิก = allow | TC-L03, TC-X03 |
| ขั้น 2 ส่งประวัติซ่อม = ไม่บันทึก | TC-D07 |
### Cross-Module (XT — 06_TESTS §6.9)
| XT | Downstream | Case |
|---|---|---|
| XT-01 | ENG-NOTIFY (rpr_ready_for_repair / rpr_cancelled) | TC-XT01 (ต้อง simulate) |
| XT-02 | ENG-DOC-STORE approved_final | TC-XT01 (ต้อง simulate) |
| XT-03 | ไม่ยิง rpr.approved | TC-XT02 |
### Scope Lock (DEC — 07 §7.0)
| DEC | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| DEC-01/02 [AI-DEFAULT] | ไม่เปลี่ยนค่า/ไม่ส่งต่อ | TC-XT02 |
| DEC-03 [AI-DEFAULT] | DOA 2 ขั้น dynamic | TC-S01, TC-P04 |
| DEC-04 [AI-DEFAULT] | ทะเบียนกรอกเอง · ประวัติขั้นแรก | TC-C06, TC-A01 |
| DEC-05/06 [AI-DEFAULT] | PDF ≥10 / ≥6 แถว | TC-P01 |
| DEC-07/16 | ช่อง 1:1 ถ้อยคำตามกระดาษ | TC-C02, TC-P01 |
| DEC-08 [AI-DEFAULT] | ลายเซ็นต่อขั้น ไม่ใช้ภาพ | TC-P02 |
| DEC-09 [AI-DEFAULT] | กลับร่าง · ยกเลิกเจ้าของ/admin | TC-R01, TC-X01, TC-X03 |
| DEC-10 [AI-DEFAULT] | การมองเห็น | TC-D01, TC-D02, TC-L03 |
| DEC-11 [AI-DEFAULT] | เลข RPR ตอนบันทึกแรก | TC-C01 |
| DEC-12 [AI-DEFAULT] | แนบ · CSV · ไม่มีทำซ้ำ | TC-C07, TC-L06, TC-V05 |
| DEC-13 | ผู้แจ้ง 2 จุด | TC-P02 |
| DEC-14 | เหตุผลบังคับ | TC-R02 |
| DEC-15 | ≥1 แถว จำนวน > 0 | TC-C03, TC-C04 |
### Cross-cutting / Events / States
| item | cases |
|---|---|
| empty state รายการ (ค้นหาไม่พบ) | TC-L04 |
| empty sub-table ประวัติซ่อม | TC-V03 |
| dirty-check ปิด wizard | TC-C08 |
| Esc ปิด modal ก่อน drawer | TC-C09 (auto: e2e S10) |
| สถานะ ร่าง/ตีกลับแก้ไข/รออนุมัติ/อนุมัติแล้ว/ยกเลิก | TC-L02 |

## Data Sets
| ชุด | ฟิลด์ | ค่า |
|---|---|---|
| A (ถูก) | รายการ / ทะเบียนสินทรัพย์ / จำนวน / อาการชำรุด / สถานที่ตั้ง / หมายเหตุ | เครื่องปรับอากาศ ห้องอบรม / AS-0000-0050 / 1 / ไม่เย็น / อาคาร B ชั้น 1 / — |
| A2 (แถว 2) | รายการ / ทะเบียนสินทรัพย์ / จำนวน / อาการชำรุด / สถานที่ตั้ง | ไฟเพดาน / (ว่าง) / 3 / หลอดขาด / อาคาร B ชั้น 1 |
| B (ผิด — จำนวน) | จำนวน | 0 · -1 · 1.5 · ก |
| H (ประวัติซ่อม) | ซ่อมครั้งสุดท้าย / จำนวนครั้งที่ซ่อม | วันที่ 1 ของเดือนปัจจุบัน / 2 |
| H-bad | จำนวนครั้งที่ซ่อม | สอง |
| Rsn (เหตุผล) | เหตุผล | ข้อมูลรายการไม่ครบ |
### ไฟล์ทดสอบ (Files)
| ไฟล์ | ใช้ |
|---|---|
| ภาพอาการแอร์.jpg (≤1MB) | TC-C07 แนบได้ |
| สคริปต์.exe | TC-C07 ชนิดไม่รองรับ |

## Test Cases
### กลุ่ม L — รายการ

### TC-L01 — เปิดรายการ เห็นหัวหน้าและคอลัมน์ครบ (happy)
- group: รายการ · ความสำคัญ: สูง · trace: 01_UI P-01 / FN-10
- actor (role): ผู้แจ้งซ่อม (owner)
- Setup: role=owner (__QA__.setMe('E01')) · seed=มาตรฐาน 12 ใบ · files=—
- Start: OPEN `#/asset-repair`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นหัวเรื่อง ปุ่มหลัก แท็บ และหัวตารางครบ ไม่มีแถบตัวเลขสถิติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/asset-repair` | — | หัวเรื่อง **แบบฟอร์มใบแจ้งซ่อมสินทรัพย์** + **(Asset Repair Request)** | ☐ |
| 2 | VERIFY ปุ่มขวาบน | — | ปุ่ม **ส่งออก CSV** และ **สร้างใบแจ้งซ่อม** | ☐ |
| 3 | VERIFY แท็บเหนือตาราง | — | **ทั้งหมด** (active) และ **รอฉันพิจารณา** | ☐ |
| 4 | VERIFY หัวตาราง | — | **เลขที่** · **วันที่แจ้ง** · **ผู้แจ้งซ่อม** · **ฝ่าย/แผนก** · **รายการ** · **จำนวน** · **สถานะเอกสาร** · **ลายเซ็น** | ☐ |
| 5 | VERIFY ใต้หัวเรื่อง | — | ไม่มีการ์ดตัวเลขสถิติเรียงแถว (no-scorecard) | ☐ |

### TC-L02 — pill สถานะครบทุกค่า
- group: รายการ · ความสำคัญ: กลาง · trace: 05 §5.2 / docPill
- actor (role): admin
- Setup: role=admin (__QA__.setMe('E08')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair`
- ชุดข้อมูล: —
- ผ่านเมื่อ: พบ pill 5 แบบในตาราง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถว **RPR-2569-0011** | — | pill **ร่าง** | ☐ |
| 2 | VERIFY แถว **RPR-2569-0010** | — | pill **ตีกลับแก้ไข** | ☐ |
| 3 | VERIFY แถว **RPR-2569-0008** | — | pill **รออนุมัติ** · ลายเซ็น 0/2 | ☐ |
| 4 | VERIFY แถว **RPR-2569-0003** | — | pill **อนุมัติแล้ว** · ลายเซ็น 2/2 | ☐ |
| 5 | VERIFY แถว **RPR-2569-0004** | — | pill **ยกเลิก** | ☐ |

### TC-L03 — admin เห็นทุกใบ (permission allow)
- group: รายการ · ความสำคัญ: สูง · trace: DEC-10 [AI-DEFAULT] / BR-08 / FN-10
- actor (role): admin ฝ่ายบริหารสินทรัพย์
- Setup: role=admin (__QA__.setMe('E08')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 12 ใบ รวมร่างของคนอื่น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ป้ายจำนวนข้างหัวเรื่อง | — | **12 รายการ** | ☐ |
| 2 | VERIFY แถว **RPR-2569-0012** (ร่างของผู้อื่น) | — | แสดงในตาราง | ☐ |

### TC-L04 — ค้นหาไม่พบ → empty state + ล้างตัวกรอง
- group: รายการ · ความสำคัญ: กลาง · trace: 01_UI P-01
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair`
- ชุดข้อมูล: คำค้น "zzzz"
- ผ่านเมื่อ: เห็นแผงว่างและกลับมาครบหลังล้าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่อง **ค้นหาเลขที่ / ผู้แจ้ง / รายการ / ทะเบียนสินทรัพย์** | zzzz | ตารางว่าง แสดง **ไม่พบรายการที่ค้นหา** | ☐ |
| 2 | CLICK ปุ่ม **ล้างตัวกรอง** | — | แถวกลับมาครบ 6 แถว | ☐ |
| 3 | TYPE → ช่องค้นหา | AS-0000-0140 | เหลือแถว **RPR-2569-0003** | ☐ |

### TC-L05 — แบบเอกสารปิดใช้ → สร้างไม่ได้ (edge: EC-06)
- group: รายการ · ความสำคัญ: กลาง · trace: EC-06 / AC-13 / DOC_TYPE_INACTIVE
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=__QA__.setDocActive(false) · files=—
- Start: OPEN `#/asset-repair`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปุ่มสร้าง disabled + แถบแดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ใต้หัวเรื่อง | — | แถบ **แบบเอกสารนี้ยังไม่เปิดใช้งาน — สร้างใบแจ้งซ่อมใหม่ไม่ได้** | ☐ |
| 2 | VERIFY ปุ่ม **สร้างใบแจ้งซ่อม** | — | กดไม่ได้ (disabled) | ☐ |

### TC-L06 — ส่งออก CSV (DEC-12)
- group: รายการ · ความสำคัญ: ต่ำ · trace: BR-13 / API-10 / DEC-12 [AI-DEFAULT]
- actor (role): admin
- Setup: role=admin (__QA__.setMe('E08')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ดาวน์โหลดไฟล์ + toast จำนวนรายการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งออก CSV** | — | ดาวน์โหลด asset-repair-requests.csv | ☐ |
| 2 | WAIT toast | — | toast **ส่งออก** 12 รายการ | ☐ |

### TC-L07 — แท็บรอฉันพิจารณา
- group: รายการ · ความสำคัญ: สูง · trace: AC-12 / FN-10 mine_to_act
- actor (role): ผู้ตรวจสอบ
- Setup: role=approver (__QA__.setMe('E02')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair`
- ชุดข้อมูล: —
- ผ่านเมื่อ: แท็บแสดงเฉพาะใบที่รอผู้ใช้นี้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แท็บ **รอฉันพิจารณา** | — | ตัวเลข 2 | ☐ |
| 2 | CLICK แท็บ **รอฉันพิจารณา** | — | เหลือ **RPR-2569-0009** และ **RPR-2569-0008** | ☐ |
| 3 | CLICK แท็บ **ทั้งหมด** | — | กลับมา 4 ใบ | ☐ |

### กลุ่ม C — สร้าง/แก้ร่าง

### TC-C01 — สร้างใบแจ้งซ่อม 2 รายการ บันทึกแบบร่าง ได้เลข RPR (happy)
- group: สร้าง · ความสำคัญ: สูง · trace: AC-01 / BR-07 / FN-01, FN-03 / DEC-11 [AI-DEFAULT]
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair` แล้ว CLICK **สร้างใบแจ้งซ่อม**
- ชุดข้อมูล: A, A2
- ผ่านเมื่อ: บันทึกได้ เลข RPR-2569-0013 เป็นแถวบนสุด สถานะร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างใบแจ้งซ่อม** | — | drawer กว้าง หัว **แจ้งซ่อมสินทรัพย์** ขั้น **ข้อมูลหลักใบแจ้งซ่อม** | ☐ |
| 2 | TYPE → แถว 1 ช่อง **รายการ** **ทะเบียนสินทรัพย์** **จำนวน** **อาการชำรุด** **สถานที่ตั้ง** | A | การ์ดสรุปขวาแสดง **1 รายการ** | ☐ |
| 3 | CLICK ปุ่ม **เพิ่มรายการ** | — | มีแถว 2 · cursor อยู่ช่องรายการแถว 2 | ☐ |
| 4 | TYPE → แถว 2 | A2 | การ์ดสรุป **2 รายการ** · **รวม 4 ชิ้น** | ☐ |
| 5 | CLICK ปุ่ม **ถัดไป** | — | ขั้น **เอกสารแนบ** | ☐ |
| 6 | CLICK ปุ่ม **ถัดไป** | — | ขั้น **ตรวจสอบและยืนยัน** เห็นตารางรายการ 2 แถว | ☐ |
| 7 | CLICK ปุ่ม **บันทึกแบบร่าง** | — | drawer ปิด | ☐ |
| 8 | WAIT toast | — | toast **บันทึกร่างแล้ว** · RPR-2569-0013 | ☐ |
| 9 | VERIFY แถวบนสุด | — | **RPR-2569-0013** pill **ร่าง** | ☐ |

### TC-C02 — ป้ายช่องตรงกระดาษ + ข้อมูลผู้แจ้งจากระบบ
- group: สร้าง · ความสำคัญ: กลาง · trace: BR-11 / DEC-07 / DEC-16 / 01_UI §1.2
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: หัวตารางกรอกตรงกระดาษ · ไม่มีช่องกรอกชื่อ/ตำแหน่ง/ฝ่าย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/asset-repair/create` | — | หัวตาราง **ลําดับ** · **รายการ** · **ทะเบียนสินทรัพย์** · **จำนวน** · **อาการชำรุด** · **สถานที่ตั้ง** · **หมายเหตุ** | ☐ |
| 2 | VERIFY การ์ด **สรุปใบแจ้งซ่อม** | — | **สมศรี ใจดี** · **เจ้าหน้าที่ธุรการ · ฝ่ายธุรการ** | ☐ |
| 3 | VERIFY การ์ดสรุปส่วนผู้พิจารณา | — | **ขั้น 1 · ผู้ตรวจสอบ** = **สมชาย ตรวจงาน** · **ขั้น 2 · ผู้อนุมัติ** = **วิไล บริหารทรัพย์** | ☐ |

### TC-C03 — กดถัดไปตอนว่าง = บล็อก (negative)
- group: สร้าง · ความสำคัญ: สูง · trace: AC-02 / VR-01 / BR-01 / DEC-15 (auto: e2e S7)
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair/create`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่ไปขั้นถัดไป + ช่องแดง + ข้อความใต้แถว + toast

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ถัดไป** | — | ยังอยู่ขั้น **ข้อมูลหลักใบแจ้งซ่อม** · ช่องรายการ/อาการชำรุด/สถานที่ตั้ง ขอบแดง | ☐ |
| 2 | VERIFY ใต้แถว 1 | — | ข้อความ **กรอกรายการ · อาการชำรุด · สถานที่ตั้ง** | ☐ |
| 3 | WAIT toast | — | toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |

### TC-C04 — จำนวน 0 / ติดลบ (boundary)
- group: สร้าง · ความสำคัญ: สูง · trace: AC-03 / VR-02 / BR-02 / DEC-15
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair/create`
- ชุดข้อมูล: A แต่จำนวน = B (0 แล้ว -1)
- ผ่านเมื่อ: ทั้งสองค่าถูกบล็อกพร้อมข้อความ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → แถว 1 ครบทุกช่อง จำนวน | A · จำนวน 0 | ช่องแสดง 0 | ☐ |
| 2 | CLICK ปุ่ม **ถัดไป** | — | ใต้แถว **จำนวนต้องเป็นตัวเลขมากกว่า 0** | ☐ |
| 3 | TYPE → ช่อง **จำนวน** | -1 | — | ☐ |
| 4 | CLICK ปุ่ม **ถัดไป** | — | ยังบล็อก ข้อความเดิม | ☐ |
| 5 | TYPE → ช่อง **จำนวน** | 1 | — | ☐ |
| 6 | CLICK ปุ่ม **ถัดไป** | — | ไปขั้น **เอกสารแนบ** | ☐ |

### TC-C05 — จำนวนทศนิยม/ตัวอักษร (negative)
- group: สร้าง · ความสำคัญ: กลาง · trace: VR-02 / BR-02
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair/create`
- ชุดข้อมูล: A · จำนวน = 1.5 แล้ว ก
- ผ่านเมื่อ: ถูกบล็อกทั้งสองค่า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → แถว 1 จำนวน | A · 1.5 | — | ☐ |
| 2 | CLICK ปุ่ม **ถัดไป** | — | **จำนวนต้องเป็นตัวเลขมากกว่า 0** | ☐ |
| 3 | TYPE → ช่อง **จำนวน** | ก | — | ☐ |
| 4 | CLICK ปุ่ม **ถัดไป** | — | ยังบล็อก | ☐ |

### TC-C06 — ไม่มีทะเบียนสินทรัพย์ บันทึกได้ (edge: EC-01) [AI-DEFAULT]
- group: สร้าง · ความสำคัญ: กลาง · trace: AC-04 / BR-03 / EC-01 / DEC-04 [AI-DEFAULT]
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair/create`
- ชุดข้อมูล: A2 (ทะเบียนว่าง)
- ผ่านเมื่อ: ผ่านไปขั้นถัดไปได้ · ในรายละเอียดทะเบียนแสดง —

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → แถว 1 | A2 | ช่องทะเบียนว่าง | ☐ |
| 2 | VERIFY ใต้ตาราง | — | **ทะเบียนสินทรัพย์: กรอกเลขเอง (ยังไม่มีทะเบียนสินทรัพย์ในระบบ) · ไม่มีทะเบียนเว้นว่างได้** | ☐ |
| 3 | CLICK ปุ่ม **ถัดไป** | — | ไปขั้น **เอกสารแนบ** | ☐ |

### TC-C07 — แนบไฟล์ได้/ชนิดไม่รองรับ
- group: สร้าง · ความสำคัญ: กลาง · trace: BR-13 / DEC-12 [AI-DEFAULT] / API-11
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=มาตรฐาน · files=ภาพอาการแอร์.jpg, สคริปต์.exe
- Start: OPEN `#/asset-repair/create` กรอก A แล้ว CLICK **ถัดไป**
- ชุดข้อมูล: A
- ผ่านเมื่อ: jpg แนบได้ · exe ถูกปฏิเสธ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ขั้น **เอกสารแนบ** | — | **คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)** · **PDF, Word, Excel หรือรูปภาพ ไม่เกิน 20 MB ต่อไฟล์** | ☐ |
| 2 | UPLOAD ภาพอาการแอร์.jpg | ไฟล์ | แถวไฟล์ ภาพอาการแอร์.jpg พร้อมขนาด | ☐ |
| 3 | UPLOAD สคริปต์.exe | ไฟล์ | toast ข้อความ ชนิดไฟล์ไม่รองรับ · ไม่เพิ่มแถว | ☐ |

### TC-C08 — ปิด wizard ตอนกรอกค้าง ถามก่อนทิ้ง (UX dirty-check)
- group: สร้าง · ความสำคัญ: กลาง · trace: 01_UI M-05
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair/create`
- ชุดข้อมูล: A (บางช่อง)
- ผ่านเมื่อ: modal ทิ้งข้อมูลขึ้น · กลับไปกรอกต่อได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่อง **รายการ** แถว 1 | เครื่องปรับอากาศ | — | ☐ |
| 2 | CLICK ปุ่ม **ยกเลิก** ท้าย drawer | — | modal **ทิ้งข้อมูลที่กรอกไว้?** | ☐ |
| 3 | CLICK ปุ่ม **กลับไปกรอกต่อ** | — | modal ปิด ข้อความยังอยู่ | ☐ |
| 4 | CLICK ปุ่ม **ยกเลิก** แล้ว CLICK **ทิ้งข้อมูล** | — | drawer ปิด กลับ `#/asset-repair` | ☐ |

### TC-C09 — แก้ไขร่างของตัวเอง (edit = ฟอร์มเดิม)
- group: สร้าง · ความสำคัญ: สูง · trace: U15 / API-04 / FN-01
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=RPR-2569-0011 ร่าง · files=—
- Start: OPEN `#/asset-repair/view/R11`
- ชุดข้อมูล: อาการชำรุด = ขาโต๊ะโยก ลิ้นชักหลุด
- ผ่านเมื่อ: เปิด wizard ด้วยค่าเดิม บันทึกแล้วค่าใหม่แสดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **แก้ไข** | — | drawer **แก้ไขใบแจ้งซ่อม RPR-2569-0011** · ช่องรายการ = โต๊ะทำงาน | ☐ |
| 2 | TYPE → ช่อง **อาการชำรุด** | ขาโต๊ะโยก ลิ้นชักหลุด | — | ☐ |
| 3 | CLICK **ถัดไป** ×2 แล้ว **บันทึกแบบร่าง** | — | toast **บันทึกร่างแล้ว** | ☐ |
| 4 | OPEN `#/asset-repair/view/R11` → VERIFY ตารางรายการ | — | อาการชำรุด ขาโต๊ะโยก ลิ้นชักหลุด | ☐ |

### กลุ่ม V — ดูรายละเอียด

### TC-V01 — owner เปิดร่างของตน เห็นปุ่มตามสถานะ
- group: ดู · ความสำคัญ: สูง · trace: 01_UI P-03 / 05 §5.3 (auto: e2e S4/S5)
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair/view/R11`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นแท็บ 4 และปุ่มร่างครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/asset-repair/view/R11` | — | หัว **RPR-2569-0011** pill **ร่าง** | ☐ |
| 2 | VERIFY ปุ่มหัว | — | **ยกเลิก** · **แก้ไข** · **ส่งขออนุมัติ** | ☐ |
| 3 | VERIFY แท็บ | — | **รายละเอียด** · **PDF Preview** · **ลายเซ็น / อนุมัติ** · **ประวัติ** | ☐ |

### TC-V02 — แท็บรายละเอียดแสดงข้อมูลผู้แจ้งและรายการ
- group: ดู · ความสำคัญ: กลาง · trace: 01_UI P-03
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นส่วนข้อมูลครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ส่วน **ผู้แจ้งซ่อม** | — | **ชื่อ-นามสกุล** สมศรี ใจดี · **ตําแหน่ง** · **ฝ่าย/แผนก** | ☐ |
| 2 | VERIFY ส่วน **รายการแจ้งซ่อม (2)** | — | 2 แถว · **รวม 2 ชิ้น** | ☐ |
| 3 | VERIFY ส่วน **ประวัติการซ่อม** | — | 1 แถว เครื่องปรับอากาศ ห้องประชุม 2 · **15 มี.ค. 2569** · 2 | ☐ |

### TC-V03 — ประวัติการซ่อมว่าง แสดงแผงว่าง (empty sub-table)
- group: ดู · ความสำคัญ: ต่ำ · trace: U23 / EC-09
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นข้อความแผงว่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ส่วน **ประวัติการซ่อม** | — | **ยังไม่มีประวัติการซ่อม — ผู้ตรวจสอบกรอกตอนพิจารณา** | ☐ |

### TC-V04 — แท็บประวัติ (audit) เรียงล่าสุดก่อน
- group: ดู · ความสำคัญ: ต่ำ · trace: 04 §4.2 audit
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็น 4 เหตุการณ์

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **ประวัติ** | — | หัวข้อ **ประวัติ (append-only)** | ☐ |
| 2 | VERIFY รายการบนสุด | — | **อนุมัติ (ขั้น 2)** · วิไล บริหารทรัพย์ | ☐ |
| 3 | VERIFY รายการล่างสุด | — | **สร้างเอกสาร** | ☐ |

### TC-V05 — ไม่มีปุ่มทำซ้ำ (DEC-12)
- group: ดู · ความสำคัญ: ต่ำ · trace: BR-13 / DEC-12 [AI-DEFAULT]
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เมนู ⋮ ไม่มีทำซ้ำ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม ⋮ แถว RPR-2569-0003 | — | เมนู **ดูรายละเอียด** · **พิมพ์** | ☐ |
| 2 | VERIFY เมนู | — | ไม่มีเมนู ทำซ้ำ | ☐ |

### กลุ่ม S — ส่งขออนุมัติ

### TC-S01 — ส่งร่าง เลือกผู้พิจารณา 2 ขั้น (happy)
- group: ส่ง · ความสำคัญ: สูง · trace: AC-05 / BR-05 / FN-04 / DEC-03 [AI-DEFAULT] (auto: e2e S8)
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=RPR-2569-0011 ร่าง · files=—
- Start: OPEN `#/asset-repair/view/R11`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ใบเป็นรออนุมัติ ขั้น 1 = สมชาย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งขออนุมัติ** | — | modal **ส่งขออนุมัติ?** มี 2 แถว **ผู้ตรวจสอบ** · **ผู้อนุมัติ** | ☐ |
| 2 | VERIFY ค่าเริ่ม | — | **สมชาย ตรวจงาน** · **วิไล บริหารทรัพย์** · **ค่าเริ่มต้นจากสายอนุมัติ (DOA กลาง) และผังองค์กร** | ☐ |
| 3 | CLICK ปุ่ม **ส่งขออนุมัติ** ใน modal | — | ปุ่มขึ้น **กำลังบันทึก…** | ☐ |
| 4 | WAIT toast | — | toast **ส่งขออนุมัติแล้ว** · RPR-2569-0011 | ☐ |
| 5 | VERIFY หัว drawer | — | pill **รออนุมัติ** | ☐ |

### TC-S02 — ไม่เลือกผู้พิจารณา = บล็อก (negative)
- group: ส่ง · ความสำคัญ: สูง · trace: VR-03 / ASSIGNEE_REQUIRED
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=RPR-2569-0011 ร่าง · files=—
- Start: OPEN `#/asset-repair/view/R11` แล้ว CLICK **ส่งขออนุมัติ**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ล้างช่องแล้วส่งไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่องผู้พิจารณาขั้น 1 แล้วลบค่า | — | ช่องว่าง (**เลือกผู้พิจารณา**) | ☐ |
| 2 | CLICK ปุ่ม **ส่งขออนุมัติ** ใน modal | — | ข้อความ **กรุณาเลือกผู้พิจารณา** · modal ไม่ปิด | ☐ |

### TC-S03 — ส่งไม่สำเร็จ (500) สถานะไม่เปลี่ยน (edge: EC-05)
- group: ส่ง · ความสำคัญ: กลาง · trace: EC-05 / 02 §2.3 (auto: e2e S9)
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=__QA__.sim('error') · files=—
- Start: OPEN `#/asset-repair/view/R11` แล้ว CLICK **ส่งขออนุมัติ**
- ชุดข้อมูล: —
- ผ่านเมื่อ: toast error และยังเป็นร่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งขออนุมัติ** ใน modal | — | — | ☐ |
| 2 | WAIT toast | — | toast **ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง** | ☐ |
| 3 | VERIFY pill | — | ยัง **ร่าง** | ☐ |

### TC-S04 — DOA เพิ่มขั้น → slot เพิ่มตาม (edge: EC-04/EC-07)
- group: ส่ง · ความสำคัญ: กลาง · trace: AC-10 / DEC-03 [AI-DEFAULT] / Rule #108 (auto: e2e S8)
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=__QA__.doa.push('ขั้นทดสอบ') · files=—
- Start: OPEN `#/asset-repair/view/R11`
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal มี 3 แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ส่งขออนุมัติ** | — | 3 แถวผู้พิจารณา แถว 3 **ขั้นทดสอบ** | ☐ |
| 2 | PRESS Esc | — | modal ปิด (หลังทดสอบเรียก __QA__.doa.pop()) | ☐ |

### กลุ่ม A — ตรวจสอบ/อนุมัติ

### TC-A01 — ผู้ตรวจสอบเห็นตารางประวัติการซ่อมใน modal [AI-DEFAULT]
- group: ตรวจสอบ · ความสำคัญ: สูง · trace: AC-06 / BR-04 / FN-02 / DEC-04 [AI-DEFAULT]
- actor (role): ผู้ตรวจสอบ
- Setup: role=approver (__QA__.setMe('E02')) · seed=RPR-2569-0008 รอขั้น 1 · files=—
- Start: OPEN `#/asset-repair/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal มีตารางประวัติแถวตั้งต้นจากรายการ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว | — | **ไม่ผ่านการตรวจสอบ** · **ตรวจสอบแล้ว** | ☐ |
| 2 | CLICK ปุ่ม **ตรวจสอบแล้ว** | — | modal หัวข้อ **ตรวจสอบแล้ว** + **ใบแจ้งซ่อมนี้?** | ☐ |
| 3 | VERIFY ตาราง **ประวัติการซ่อม** | — | หัว **ซ่อมครั้งสุดท้าย** · **จำนวนครั้งที่ซ่อม** · แถว 1 = เครื่องพิมพ์เลเซอร์ | ☐ |
| 4 | CLICK ช่อง **เลือกวันที่** | — | ปฏิทิน พ.ศ. + ปุ่ม **วันนี้** · วันหลังวันนี้กดไม่ได้ | ☐ |

### TC-A02 — จำนวนครั้งที่ซ่อมไม่ใช่ตัวเลข (negative)
- group: ตรวจสอบ · ความสำคัญ: กลาง · trace: VR-05 / HISTORY_INVALID
- actor (role): ผู้ตรวจสอบ
- Setup: role=approver (__QA__.setMe('E02')) · seed=RPR-2569-0008 · files=—
- Start: OPEN `#/asset-repair/view/R8` แล้ว CLICK **ตรวจสอบแล้ว**
- ชุดข้อมูล: H-bad
- ผ่านเมื่อ: บล็อก + toast

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องจำนวนครั้งที่ซ่อม แถว 1 | สอง | — | ☐ |
| 2 | CLICK ปุ่ม **ตรวจสอบแล้ว** ใน modal | — | ช่องขอบแดง · modal ไม่ปิด | ☐ |
| 3 | WAIT toast | — | toast **จำนวนครั้งที่ซ่อมต้องเป็นตัวเลข** | ☐ |

### TC-A03 — ตรวจสอบแล้ว + ประวัติ → ขั้น 2 (happy)
- group: ตรวจสอบ · ความสำคัญ: สูง · trace: AC-07 / FN-05 / BR-09 คำตาม role
- actor (role): ผู้ตรวจสอบ
- Setup: role=approver (__QA__.setMe('E02')) · seed=RPR-2569-0008 · files=—
- Start: OPEN `#/asset-repair/view/R8` แล้ว CLICK **ตรวจสอบแล้ว**
- ชุดข้อมูล: H
- ผ่านเมื่อ: ขั้น 1 ผ่าน · ประวัติแสดงในรายละเอียด · ลายเซ็น 1/2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เลือกวันที่** → เลือกวันที่ 1 | H | ช่องแสดงวันที่แบบ พ.ศ. | ☐ |
| 2 | TYPE → ช่องจำนวนครั้งที่ซ่อม | 2 | — | ☐ |
| 3 | CLICK ปุ่ม **ตรวจสอบแล้ว** ใน modal | — | modal ปิด | ☐ |
| 4 | WAIT toast | — | toast **ตรวจสอบแล้ว** · RPR-2569-0008 | ☐ |
| 5 | VERIFY ส่วน **ประวัติการซ่อม** | — | 1 แถว จำนวน 2 | ☐ |
| 6 | CLICK แท็บ **ลายเซ็น / อนุมัติ** | — | ขั้น 1 pill **ตรวจสอบแล้ว** · ขั้น 2 **รอพิจารณา — ขั้นปัจจุบัน** | ☐ |

### TC-A04 — ผู้อนุมัติอนุมัติขั้นสุดท้าย → อนุมัติแล้ว (happy)
- group: อนุมัติ · ความสำคัญ: สูง · trace: AC-07 / FN-05 / FN-09
- actor (role): ผู้อนุมัติ (role-mgr-acc)
- Setup: role=ผู้อนุมัติ (__QA__.setMe('E09')) · seed=RPR-2569-0006 รอขั้น 2 · files=—
- Start: OPEN `#/asset-repair/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: อนุมัติแล้ว 2/2 ล็อกแก้ไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว | — | **ไม่อนุมัติ** · **อนุมัติ** | ☐ |
| 2 | CLICK ปุ่ม **อนุมัติ** | — | modal หัวข้อ **อนุมัติ** + **ใบแจ้งซ่อมนี้?** ไม่มีตารางประวัติ | ☐ |
| 3 | CLICK ปุ่ม **อนุมัติ** ใน modal | — | — | ☐ |
| 4 | WAIT toast | — | toast **อนุมัติแล้ว** · RPR-2569-0006 | ☐ |
| 5 | VERIFY ท้าย drawer | — | **อนุมัติแล้ว ล็อกแก้ไข** | ☐ |

### TC-A05 — ตรวจสอบโดยไม่กรอกประวัติ (edge: EC-09) [AI-DEFAULT]
- group: ตรวจสอบ · ความสำคัญ: กลาง · trace: EC-09 / BR-04 / DEC-04 [AI-DEFAULT]
- actor (role): ผู้ตรวจสอบ
- Setup: role=approver (__QA__.setMe('E02')) · seed=RPR-2569-0009 · files=—
- Start: OPEN `#/asset-repair/view/R9` แล้ว CLICK **ตรวจสอบแล้ว**
- ชุดข้อมูล: —
- ผ่านเมื่อ: ผ่านได้ · ประวัติยังว่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ตรวจสอบแล้ว** ใน modal (ไม่กรอกอะไร) | — | toast **ตรวจสอบแล้ว** | ☐ |
| 2 | VERIFY ส่วน **ประวัติการซ่อม** | — | **ยังไม่มีประวัติการซ่อม — ผู้ตรวจสอบกรอกตอนพิจารณา** | ☐ |

### TC-A06 — ตัดสินชนกัน (409 stale) (edge: EC-05)
- group: ตรวจสอบ · ความสำคัญ: ต่ำ · trace: EC-05 / STALE
- actor (role): ผู้ตรวจสอบ
- Setup: role=approver (__QA__.setMe('E02')) · seed=__QA__.sim('stale') · files=—
- Start: OPEN `#/asset-repair/view/R8` แล้ว CLICK **ตรวจสอบแล้ว**
- ชุดข้อมูล: —
- ผ่านเมื่อ: toast รีเฟรช สถานะไม่เปลี่ยน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ตรวจสอบแล้ว** ใน modal | — | toast **ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่** | ☐ |
| 2 | VERIFY pill | — | ยัง **รออนุมัติ** | ☐ |

### กลุ่ม R — ตีกลับเป็นร่าง

### TC-R01 — ไม่ผ่านการตรวจสอบ → กลับร่าง เลขเดิม [AI-DEFAULT]
- group: ตีกลับ · ความสำคัญ: สูง · trace: AC-08 / BR-06 / FN-06 / DEC-09 [AI-DEFAULT] / BR-DOA-03
- actor (role): ผู้ตรวจสอบ
- Setup: role=approver (__QA__.setMe('E02')) · seed=RPR-2569-0009 · files=—
- Start: OPEN `#/asset-repair/view/R9`
- ชุดข้อมูล: Rsn
- ผ่านเมื่อ: ใบกลับเป็นร่าง ผู้ตรวจสอบไม่เห็นใบนั้นแล้ว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ไม่ผ่านการตรวจสอบ** | — | modal **ไม่ผ่านการตรวจสอบ — ตีกลับเป็นร่าง?** | ☐ |
| 2 | CLICK chip **ข้อมูลรายการไม่ครบ** | Rsn | ช่องเหตุผลถูกเติม | ☐ |
| 3 | CLICK ปุ่ม **ไม่ผ่านการตรวจสอบ** ใน modal | — | toast **ตีกลับเป็นร่างแล้ว** | ☐ |
| 4 | VERIFY รายการ | — | ไม่เห็น RPR-2569-0009 แล้ว (ร่างของผู้อื่น) | ☐ |

### TC-R02 — ไม่ใส่เหตุผล = บล็อก (negative)
- group: ตีกลับ · ความสำคัญ: สูง · trace: VR-04 / DEC-14 / REASON_REQUIRED
- actor (role): ผู้ตรวจสอบ
- Setup: role=approver (__QA__.setMe('E02')) · seed=RPR-2569-0008 · files=—
- Start: OPEN `#/asset-repair/view/R8` แล้ว CLICK **ไม่ผ่านการตรวจสอบ**
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal ไม่ปิด + ข้อความ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ไม่ผ่านการตรวจสอบ** ใน modal | — | **กรุณาระบุเหตุผล** | ☐ |

### TC-R03 — ผู้แจ้งเห็นใบตีกลับ แก้แล้วส่งใหม่
- group: ตีกลับ · ความสำคัญ: สูง · trace: AC-08 / BR-05 / BR-06
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=RPR-2569-0010 ตีกลับ · files=—
- Start: OPEN `#/asset-repair/view/R10`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เห็นเหตุผล · ส่งใหม่ได้เลขเดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถบบน | — | **ไม่พบทะเบียนสินทรัพย์ที่ระบุ — ตรวจเลข AS อีกครั้ง** · **แก้แล้วส่งขออนุมัติใหม่ได้ (เลขที่เดิม)** | ☐ |
| 2 | CLICK ปุ่ม **ส่งขออนุมัติ** แล้ว **ส่งขออนุมัติ** ใน modal | — | toast **ส่งขออนุมัติแล้ว** · RPR-2569-0010 | ☐ |
| 3 | VERIFY pill | — | **รออนุมัติ** | ☐ |

### กลุ่ม X — ยกเลิก

### TC-X01 — owner ยกเลิกใบรออนุมัติของตน [AI-DEFAULT]
- group: ยกเลิก · ความสำคัญ: กลาง · trace: AC-11 / FN-07 / DEC-09 [AI-DEFAULT]
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=RPR-2569-0008 · files=—
- Start: OPEN `#/asset-repair/view/R8`
- ชุดข้อมูล: เหตุผล "ซ่อมเองได้แล้ว"
- ผ่านเมื่อ: สถานะยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยกเลิกเอกสาร** | — | modal **ยกเลิกเอกสาร?** | ☐ |
| 2 | CLICK chip **ซ่อมเองได้แล้ว** แล้ว CLICK ปุ่ม **ยกเลิกเอกสาร** ใน modal | — | toast **ยกเลิกเอกสารแล้ว** | ☐ |
| 3 | VERIFY pill | — | **ยกเลิก** | ☐ |

### TC-X02 — ยกเลิกไม่ใส่เหตุผล (negative)
- group: ยกเลิก · ความสำคัญ: กลาง · trace: VR-04
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=RPR-2569-0011 · files=—
- Start: OPEN `#/asset-repair/view/R11` แล้ว CLICK **ยกเลิก**
- ชุดข้อมูล: —
- ผ่านเมื่อ: บล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ยกเลิกเอกสาร** ใน modal | — | **กรุณาระบุเหตุผล** | ☐ |
| 2 | CLICK ปุ่ม **ไม่ยกเลิก** | — | modal ปิด ยังเป็นร่าง | ☐ |

### TC-X03 — admin ยกเลิกได้ · ใบอนุมัติแล้วยกเลิกไม่ได้ (permission)
- group: ยกเลิก · ความสำคัญ: กลาง · trace: DEC-09 / NOT_CANCELLABLE / 05 §5.3
- actor (role): admin
- Setup: role=admin (__QA__.setMe('E08')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair/view/R7`
- ชุดข้อมูล: —
- ผ่านเมื่อ: R7 มีปุ่มยกเลิก · R3 ไม่มี

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว R7 | — | **ยกเลิกเอกสาร** | ☐ |
| 2 | OPEN `#/asset-repair/view/R3` | — | ไม่มีปุ่ม **ยกเลิกเอกสาร** | ☐ |

### กลุ่ม P — แบบพิมพ์ PDF

### TC-P01 — PDF ถ้อยคำและแถวตามกระดาษ
- group: PDF · ความสำคัญ: สูง · trace: AC-09 / DEC-05/06 [AI-DEFAULT] / DEC-07 / DEC-16
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=มาตรฐาน · files=—
- Start: OPEN `#/asset-repair/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ถ้อยคำครบ · รายการ 10 แถว · ประวัติ 6 แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **PDF Preview** | — | กระดาษ A4 หัว **แบบฟอร์มใบแจ้งซ่อมสินทรัพย์** | ☐ |
| 2 | VERIFY ข้อความในกระดาษ | — | **มีความประสงค์จะขอแจ้งซ่อมทรัพย์สิน ดังนี้** · **ทั้งนี้ทรัพย์สิน ดังกล่าวมีประวัติการซ่อมดังนี้** | ☐ |
| 3 | VERIFY ตารางรายการ | — | ลําดับ 1–10 ครบ (มีข้อมูล 2 แถว) | ☐ |
| 4 | VERIFY ท้ายกระดาษ | — | **Doc. No. : FM-ASM-03** | ☐ |

### TC-P02 — ช่องลงชื่อ + ผู้แจ้ง 2 จุด (DEC-13)
- group: PDF · ความสำคัญ: สูง · trace: BR-09 / BR-10 / DEC-08 [AI-DEFAULT] / DEC-13
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=RPR-2569-0003 อนุมัติแล้ว · files=—
- Start: OPEN `#/asset-repair/view/R3` แล้ว CLICK **PDF Preview**
- ชุดข้อมูล: —
- ผ่านเมื่อ: 3 ช่องลงชื่อ · ผู้แจ้งแสดงทั้งบรรทัดลงชื่อและช่องล่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY บรรทัดลงชื่อใต้ตาราง | — | **ลงชื่อ** สมศรี ใจดี **ผู้แจ้งซ่อม** · วันที่ 9 เดือน กันยายน พ.ศ. 2569 | ☐ |
| 2 | VERIFY แถวลงชื่อล่าง | — | **ผู้แจ้งซ่อม** · **ผู้ตรวจสอบ** · **ผู้อนุมัติ** | ☐ |
| 3 | VERIFY คำตัดสิน | — | ช่องผู้ตรวจสอบ ☑ **ตรวจสอบแล้ว** · ช่องผู้อนุมัติ ☑ **อนุมัติ** · ข้อความ **พิจารณาในระบบ** | ☐ |

### TC-P03 — รายการเกิน 10 แถว ยัง 1 หน้า (edge: EC-02)
- group: PDF · ความสำคัญ: กลาง · trace: EC-02 / FN-08 layout.dense
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=สร้างร่างใหม่ 12 รายการ · files=—
- Start: OPEN `#/asset-repair/create`
- ชุดข้อมูล: A ×12 (เพิ่มรายการ 11 ครั้ง)
- ผ่านเมื่อ: PDF แสดง 12 แถว หน้าเดียว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE แถว 1 แล้ว CLICK **เพิ่มรายการ** ×11 กรอกครบ | A | การ์ดสรุป **12 รายการ** | ☐ |
| 2 | CLICK **ถัดไป** ×2 แล้ว **บันทึกแบบร่าง** | — | toast **บันทึกร่างแล้ว** | ☐ |
| 3 | OPEN ใบใหม่ → CLICK แท็บ **PDF Preview** | — | ตาราง 12 แถว · ช่องลงชื่ออยู่หน้าเดียวกัน | ☐ |

### TC-P04 — DOA 6 ขั้น → ช่องลงชื่อ 7 ช่อง 2 แถว (edge: EC-07)
- group: PDF · ความสำคัญ: กลาง · trace: AC-10 / BR-09 / DEC-03 [AI-DEFAULT]
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=__QA__.doa.push() ×4 แล้วสร้าง+ส่งใบใหม่ · files=—
- Start: OPEN `#/asset-repair/create`
- ชุดข้อมูล: A
- ผ่านเมื่อ: PDF มี 7 ช่อง (4+3)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE แถว 1 แล้ว **ถัดไป** ×2 แล้ว **บันทึกและส่งขออนุมัติ** | A | modal ส่ง มี 6 แถว | ☐ |
| 2 | CLICK ปุ่ม **ส่งขออนุมัติ** ใน modal | — | toast **ส่งขออนุมัติแล้ว** | ☐ |
| 3 | OPEN ใบนั้น → CLICK **PDF Preview** | — | ช่องลงชื่อ 7 ช่อง แถวบน 4 แถวล่าง 3 | ☐ |

### กลุ่ม D — สิทธิ์ (deny)

### TC-D01 — ผู้อนุมัติเปิด route ร่างของคนอื่น = ไม่เห็น (permission)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: BR-08 / DEC-10 / NOT_FOUND (auto: e2e S6)
- actor (role): ผู้ตรวจสอบ
- Setup: role=approver (__QA__.setMe('E02')) · seed=RPR-2569-0011 ร่างของ E01 · files=—
- Start: OPEN `#/asset-repair/view/R11`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่เปิด drawer · ผู้อนุมัติไม่เห็นร่างของคนอื่น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/asset-repair/view/R11` | — | ไม่เปิด drawer · อยู่หน้ารายการ | ☐ |
| 2 | VERIFY รายการ | — | ไม่พบ RPR-2569-0011 | ☐ |

### TC-D02 — owner ไม่เห็นร่างของคนอื่น (permission)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: BR-08 / DEC-10 (auto: e2e S3)
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=RPR-2569-0012 ร่างของ E05 · files=—
- Start: OPEN `#/asset-repair`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่พบใบของผู้อื่น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องค้นหา | RPR-2569-0012 | **ไม่พบรายการที่ค้นหา** | ☐ |

### TC-D03 — ผู้อยู่ในสายแต่ไม่ใช่ขั้นปัจจุบัน ไม่มีปุ่มตัดสิน (permission)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: NOT_CURRENT_APPROVER / BR-DOA (auto: e2e S5)
- actor (role): ผู้อนุมัติขั้น 2
- Setup: role=ผู้อนุมัติ (__QA__.setMe('E09')) · seed=RPR-2569-0008 รอขั้น 1 · files=—
- Start: OPEN `#/asset-repair/view/R8`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มตัดสิน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว | — | ไม่มีปุ่ม **อนุมัติ** | ☐ |
| 2 | CLICK แท็บ **ลายเซ็น / อนุมัติ** | — | ขั้น 1 **รอพิจารณา — ขั้นปัจจุบัน** · ขั้น 2 **รอคิว** | ☐ |

### TC-D04 — คนนอก/ผู้พิจารณายกเลิกไม่ได้ (permission)
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: NOT_OWNER / DEC-09
- actor (role): ผู้ตรวจสอบ
- Setup: role=approver (__QA__.setMe('E02')) · seed=RPR-2569-0008 · files=—
- Start: OPEN `#/asset-repair`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เมนู ⋮ ไม่มียกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม ⋮ แถว RPR-2569-0008 | — | เมนู **ดูรายละเอียด** · **พิมพ์** | ☐ |
| 2 | VERIFY เมนู | — | ไม่มีเมนู **ยกเลิกเอกสาร** | ☐ |

### TC-D05 — แก้ใบที่ไม่ใช่ร่างไม่ได้ (permission)
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: NOT_DRAFT / 05 §5.3 (auto: e2e S5)
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=RPR-2569-0003 อนุมัติแล้ว · files=—
- Start: OPEN `#/asset-repair/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่มแก้ไข

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว | — | ไม่มีปุ่ม **แก้ไข** | ☐ |
| 2 | OPEN `#/asset-repair/edit/R3` | — | toast **แก้ไขได้เฉพาะร่างของตัวเอง** | ☐ |

### TC-D06 — ผู้แจ้งไม่อยู่ในรายชื่อผู้พิจารณา (SoD)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: SELF_APPROVAL / BR-DOA-04 / VR-03
- actor (role): owner
- Setup: role=owner (__QA__.setMe('E01')) · seed=RPR-2569-0011 · files=—
- Start: OPEN `#/asset-repair/view/R11` แล้ว CLICK **ส่งขออนุมัติ**
- ชุดข้อมูล: คำค้น "สมศรี"
- ผ่านเมื่อ: ค้นหาชื่อตัวเองไม่พบในตัวเลือก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → ช่องผู้พิจารณาขั้น 1 | สมศรี | ไม่มีตัวเลือก สมศรี ใจดี | ☐ |

### TC-D07 — ขั้น 2 ไม่มีตารางประวัติการซ่อม (permission)
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: BR-04 / 02 §2.2 history เฉพาะขั้นแรก
- actor (role): ผู้อนุมัติ
- Setup: role=ผู้อนุมัติ (__QA__.setMe('E09')) · seed=RPR-2569-0006 รอขั้น 2 · files=—
- Start: OPEN `#/asset-repair/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal อนุมัติไม่มีตารางประวัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **อนุมัติ** | — | modal หัวข้อ **อนุมัติ** + **ใบแจ้งซ่อมนี้?** แสดง **รายการ** และ **จำนวน** · ไม่มีหัว **ซ่อมครั้งสุดท้าย** | ☐ |

### กลุ่ม XT — cross-module

### TC-XT01 — อนุมัติครบ → แจ้งผู้ดูแลงานซ่อม + เก็บ PDF (ต้อง simulate)
- group: cross-module · ความสำคัญ: กลาง · trace: XT-01 / XT-02 / FN-05 / FN-09 / rpr_ready_for_repair
- actor (role): ผู้อนุมัติ
- Setup: role=ผู้อนุมัติ (__QA__.setMe('E09')) · seed=RPR-2569-0006 รอขั้น 2 · ENG-NOTIFY/ENG-DOC-STORE = (ต้อง simulate) · files=—
- Start: OPEN `#/asset-repair/view/R6`
- ชุดข้อมูล: —
- ผ่านเมื่อ: สถานะต้นทางอนุมัติแล้ว + timeline ผลลัพธ์บอกการแจ้ง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **อนุมัติ** แล้ว **อนุมัติ** ใน modal | — | toast **อนุมัติแล้ว** | ☐ |
| 2 | CLICK แท็บ **ลายเซ็น / อนุมัติ** | — | ผลลัพธ์ **อนุมัติให้ซ่อม — แจ้งผู้ดูแลงานซ่อม (rpr_ready_for_repair)** | ☐ |

### TC-XT02 — อนุมัติแล้วไม่ส่งต่อระบบอื่น [AI-DEFAULT]
- group: cross-module · ความสำคัญ: ต่ำ · trace: XT-03 / BR-12 / DEC-01 / DEC-02 [AI-DEFAULT]
- actor (role): admin
- Setup: role=admin (__QA__.setMe('E08')) · seed=RPR-2569-0003 อนุมัติแล้ว · files=—
- Start: OPEN `#/asset-repair/view/R3`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไม่มีปุ่ม/ลิงก์ไปสร้างใบงานซ่อมหรือ module อื่น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่มหัว drawer | — | มีเพียงไอคอน พิมพ์ · ดาวน์โหลด · ปิด | ☐ |
| 2 | CLICK แท็บ **ประวัติ** | — | ไม่มีเหตุการณ์ส่งต่อระบบอื่น | ☐ |

## วิธีที่ agent รัน (Run protocol)
1. เปิด `feature.html` ใหม่ทุกเคส (state เป็น seed ใหม่) · ตั้งผู้ใช้ตาม Setup ด้วย `window.__QA__.setMe('E0x')` ก่อน OPEN route
2. seed พิเศษ (`__QA__.sim(...)`, `__QA__.setDocActive(false)`, `__QA__.doa.push()`) เรียกก่อน step 1 และคืนค่าหลังจบเคส
3. ทำทีละ step · เช็ค Expected ด้วยสิ่งที่เห็น · toast ใช้ WAIT ≤3 วิ · ข้อความ **ตัวหนา** = ข้อความบนจอจริง
4. เคส `(auto: e2e S#)` มี e2e_standard.py ทดสอบคู่ — ยังต้องรันเพื่อยืนยันมุมมองผู้ใช้
5. กรอกผลตาม schema ด้านล่าง · fail ให้ใส่ evidence = ข้อความ/สถานะที่เห็นจริง

## Coverage Audit
| หมวด | covered / total |
|---|---|
| AC (06_TESTS) | 13 / 13 |
| Business rules (05_RULES) | 13 / 13 (+ BR-DOA 5/5) |
| Validation | 5 / 5 |
| Edge cases | 7 / 9 |
| Error codes | 10 / 10 |
| Permission cells (สำคัญ) | 8 / 8 |
| Cross-cutting / events / states | ครบ |

- Cross-Module (XT): 3/3
- Scope Lock (DEC): 16/16 (DEC-01..16 ทุกข้อมีเคส verify)
- **Manifest cross-check (FRD §0.12): ✅ 5/5 แถว (ช่องในฟอร์ม · ลายเซ็น · DEC · Story · route/modal)**

### ข้าม (พร้อมเหตุผล)
- EC-03 ผู้แจ้งถือ role-mgr-acc — seed ไม่มี persona ที่เป็นทั้งผู้แจ้งและ role-mgr-acc · กฎ SoD ครอบโดย TC-D06
- EC-08 แจ้งซ้ำทรัพย์สินเดิม — นอกขอบเขตรอบนี้ (ไม่มี Asset Master · OQ-04)

## Result Report (schema)
```json
{
  "feature_id": "F-TMP-001",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-L01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 50, "pass": 0, "fail": 0, "blocked": 0 }
}
```

# 02_API — F-WH-GRN · GRN รับของ

> Audience: BE dev (HTTP layer เท่านั้น) · business logic อยู่ที่ `03_LOGIC.md`
> Base path: `/api/v1/warehouse/grn`

## §2.1 Endpoint list

| ID | Method · Path | สาระ | Mutation |
|---|---|---|:--:|
| `F-WH-GRN-API-01` | `GET /grn` | รายการใบรับของ + ตัวกรอง + KPI | — |
| `F-WH-GRN-API-02` | `GET /grn/{id}` | รายละเอียดใบเดียว (ทุกแท็บ) | — |
| `F-WH-GRN-API-03` | `GET /grn/selectable-pos` | ใบสั่งซื้อที่เลือกได้ + เหตุผลของใบที่เลือกไม่ได้ | — |
| `F-WH-GRN-API-04` | `POST /grn` | สร้างฉบับร่างจากใบสั่งซื้อ | ✅ |
| `F-WH-GRN-API-05` | `PUT /grn/{id}` | แก้ฉบับร่าง (จำนวน · ผลตรวจ · ข้อมูลหลัก) | ✅ |
| `F-WH-GRN-API-06` | `POST /grn/{id}/refresh-from-po` | ดึงข้อมูลจากใบสั่งซื้อใหม่ | ✅ |
| `F-WH-GRN-API-07` | `POST /grn/{id}/post` | **บันทึกรับเข้าคลัง** — ออกเลข + movement + ตัดยอด PO | ✅ |
| `F-WH-GRN-API-08` | `POST /grn/{id}/reverse` | กลับรายการทั้งใบ | ✅ |
| `F-WH-GRN-API-09` | `POST /grn/{id}/discard` | ทิ้งฉบับร่าง (soft archive) | ✅ |
| `F-WH-GRN-API-10` | `POST /grn/{id}/attachments` · `DELETE .../{fileId}` | เอกสารแนบ | ✅ |
| `F-WH-GRN-API-11` | `GET /grn/{id}/print` | ข้อมูลเอกสารพิมพ์ A4 | — |
| `F-WH-GRN-API-12` | `GET /grn/check-dn` | ตรวจเลขใบส่งของซ้ำ (เตือน ไม่บล็อก) | — |

## §2.2 Contract blocks

### `F-WH-GRN-API-04` · `POST /grn`
- **Request:** `{ po_ref, receive_date?, warehouse_ref? }`
- **Request validation (HTTP layer, trivial):** `po_ref` required · `receive_date` ISO date
- **Response 201:** `GrnDetail`
- **Logic:** → `FN-03 buildDraftFromPo` (ดู `03_LOGIC §3.3`)
- **Errors:** `PO_NOT_SELECTABLE` (409) · `PO_NOT_FOUND` (404)

### `F-WH-GRN-API-05` · `PUT /grn/{id}`
- **Request:** `{ header: {...}, lines: [{ line_id, qty_received_now, qc_result, qty_rejected, reject_reason, quarantine_ref, line_note }] }`
- **Precondition:** `status = draft` เท่านั้น
- **Response 200:** `GrnDetail`
- **Logic:** → `FN-04 updateDraft` · `FN-05 validateLines` · `ENG-GRN-01` · `ENG-GRN-02`
- **Errors:** `GRN_NOT_DRAFT` (409) · `QTY_OVER_CAP` (422) · `QC_INCOMPLETE` (422) · `LINE_NOTE_REQUIRED` (422)

### `F-WH-GRN-API-07` · `POST /grn/{id}/post` ★ หัวใจ
- **Request:** `{ receiver, qc_inspector?, idempotency_key }`
- **Precondition:** `status = draft` · ใบสั่งซื้อยังพร้อมรับของ ณ เวลาบันทึก
- **Response 200:** `{ grn_no, status: 'posted', movements[], po_sync: { po_ref, new_status, lines[] } }`
- **Logic:** → `FN-11 postGrn` → `ENG-DOC-NUM.next('GRN')` · `ENG-GRN-03` · `ENG-GRN-04` · `ENG-NOTIFY.emit` · `ENG-CSQ.emit`
- **Idempotency:** `idempotency_key` **required** — กดซ้ำคืนผลเดิม ไม่สร้างใบ/movement ซ้ำ (VR16)
- **Transaction:** ออกเลข + movement + ตัดยอด PO อยู่ใน transaction เดียว — ล้มเหลวต้อง rollback ทั้งชุด
- **Errors:** `GRN_NOT_DRAFT` (409) · `PO_NOT_RECEIVABLE` (409) · `NO_LINE_WITH_QTY` (422) · `RECEIVER_REQUIRED` (422) · `QC_INCOMPLETE` (422) · `DOC_NUMBER_UNAVAILABLE` (503)

### `F-WH-GRN-API-08` · `POST /grn/{id}/reverse`
- **Request:** `{ reason, idempotency_key }` — `reason` **required** (VR15)
- **Precondition:** `status = posted` · ผู้ใช้เป็นหัวหน้าคลัง · ของยังไม่ถูกใช้ต่อ (R16)
- **Response 200:** `{ status: 'reversed', counter_movements[], po_sync: {...} }`
- **Logic:** → `FN-13 reverseGrn` → `ENG-GRN-03` (แถวตรงข้าม ชี้ `reversal_of`) · `ENG-GRN-04` (หักยอดคืน + ถอยสถานะ) · `ENG-NOTIFY` · `ENG-CSQ`
- **Errors:** `GRN_NOT_POSTED` (409) · `REASON_REQUIRED` (422) · `GOODS_ALREADY_CONSUMED` (409) · `FORBIDDEN_ROLE` (403)

### `F-WH-GRN-API-12` · `GET /grn/check-dn?vendor_ref=&delivery_note_no=`
- **Response 200:** `{ duplicate: bool, existing: [{ grn_id, grn_no, receive_date }] }`
- **เตือนอย่างเดียว ไม่บล็อก** (R18 · VR03) — เกณฑ์มาจากกติกากลาง (NC rules · **CF-06**)

## §2.3 Request validation ที่อยู่ชั้น HTTP (trivial เท่านั้น)

`required` / รูปแบบวันที่ / ชนิดตัวเลข / ขนาดไฟล์แนบ — **กติกาธุรกิจทั้งหมดอยู่ที่ `03_LOGIC` + `05_RULES`** (Logic Placement Matrix #1–2)

## §2.4 สิทธิ์ต่อ endpoint (จาก BRD §4.2)

| Endpoint | จนท.คลัง | หัวหน้าคลัง | ผู้ตรวจคุณภาพ | จัดซื้อ | บัญชี | ผู้ดูแล |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| API-01/02 (อ่าน) | ✅ คลังตัวเอง | ✅ ทุกคลัง | ✅ ที่ตัวเองตรวจ | ✅ PO ของตน | ✅ | ✅ |
| API-04/05 (ร่าง) | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| API-05 เฉพาะ field ผลตรวจ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| API-07 (บันทึกรับเข้า) | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| API-08 (กลับรายการ) | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| API-09 (ทิ้งร่าง) | ✅ ของตัวเอง | ✅ | ❌ | ❌ | ❌ | ❌ |
| API-10 (แนบ) | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |

> **Confidential field (`unit_price` · `discount_pct` · `gr_ir_*`) ต้องถูกตัดออกจาก response ของผู้ตรวจคุณภาพ** (04_DB §4.6)

## §2.5 Error catalog

| Code | HTTP | ข้อความบนจอ |
|---|---|---|
| `PO_NOT_SELECTABLE` | 409 | "เลือกไม่ได้ — {เหตุผล}" |
| `PO_NOT_RECEIVABLE` | 409 | "ใบสั่งซื้อต้นทางไม่พร้อมรับของแล้ว" |
| `GRN_NOT_DRAFT` | 409 | "แก้ไขได้เฉพาะฉบับร่าง — ใบที่รับเข้าแล้วต้องกลับรายการแล้วออกใบใหม่" |
| `GRN_NOT_POSTED` | 409 | "กลับรายการได้เฉพาะใบที่รับเข้าแล้ว" |
| `QTY_OVER_CAP` | 422 | "รับได้ไม่เกิน {เพดาน} {หน่วย} (เผื่อ {เปอร์เซ็นต์}%)" |
| `NO_LINE_WITH_QTY` | 422 | "ต้องมีอย่างน้อย 1 บรรทัดที่รับ > 0" |
| `LINE_NOTE_REQUIRED` | 422 | "รับเกินยอดค้างรับ ต้องระบุหมายเหตุบรรทัด" |
| `QC_INCOMPLETE` | 422 | "จำนวนที่ไม่ผ่านต้องไม่เกินจำนวนที่รับ" / "เลือกเหตุผลที่ไม่ผ่าน" / "ระบุโซนกักของก่อนบันทึก" / "ระบุผู้ตรวจคุณภาพ (บุคคลจริง)" |
| `RECEIVER_REQUIRED` | 422 | "ระบุผู้รับของ (บุคคลจริง) ก่อน" |
| `RECEIVE_DATE_FUTURE` | 422 | "วันที่รับจริงต้องไม่เป็นอนาคต" |
| `REASON_REQUIRED` | 422 | "ต้องระบุเหตุผลก่อน" |
| `GOODS_ALREADY_CONSUMED` | 409 | "ของถูกใช้ต่อแล้ว — กลับรายการไม่ได้" |
| `DOC_NUMBER_UNAVAILABLE` | 503 | "ออกเลขเอกสารไม่สำเร็จ — ลองใหม่อีกครั้ง" |
| `FORBIDDEN_ROLE` | 403 | "สิทธิ์ไม่พอสำหรับการกระทำนี้" |

## §2.6 Idempotency & concurrency

- `POST .../post` และ `POST .../reverse` **ต้องส่ง `idempotency_key`** — เก็บผลลัพธ์ 24 ชม. · กดซ้ำคืนผลเดิม
- `PUT /grn/{id}` ใช้ **optimistic lock** ด้วย `updated_at` — ไม่ตรง → `409 CONFLICT_STALE_RECORD` พร้อมข้อมูลล่าสุด
- การตัดยอด `PO.received` ต้อง **lock บรรทัดใบสั่งซื้อ** ระหว่าง transaction กัน 2 GRN รับพร้อมกันแล้วยอดเกิน

## §2.7 Cross-Module Contract (R12 · จาก BRD §12.1)

### ขาเข้า (Inbound · IS-01..IS-13) — อ้างรหัสจาก BRD §3.1 ครบทุกข้อ

| IS | สาระ | อยู่ที่ไหนในแพ็กนี้ |
|---|---|---|
| **IS-01** | สร้างใบรับโดยอ้างใบสั่งซื้อที่ส่งแล้วและยังค้างรับ · 1 ใบรับ = 1 ใบสั่งซื้อ | `API-03` · `API-04` · `FN-02` · `BR-01/02` |
| **IS-02** | ดึงบรรทัดพร้อมจำนวนสั่ง/รับแล้ว/คงเหลือ/ราคา/ภาษี **อ่านอย่างเดียว** | `FN-03 buildDraftFromPo` · `BR-03` · `AT-05` |
| **IS-03** | รับครบ · รับบางส่วน · รับเกินในกรอบ · ไม่รับบางบรรทัด — ตัดยอดกลับทุกกรณี | `ENG-GRN-02` · `ENG-GRN-04` · `AT-27/28` |
| **IS-04** | บันทึกผลตรวจรายบรรทัด 3 ค่า + บังคับจำนวน/เหตุผล/ที่พักของ | `ENG-GRN-01` · `BR-09` · `AT-14/15` |
| **IS-05** | ของไม่ผ่านเข้าโซนกัก · ออกได้ทางเดียวคือคืนผู้ขาย | `ENG-GRN-01` ข้อ 4–5 · `BR-10` · `AT-17/18` |
| **IS-06** | ความเคลื่อนไหวต่อท้ายอย่างเดียว + กลับรายการทั้งใบ | `ENG-GRN-03` · `BR-14/15` · `AT-25` |
| **IS-07** | ตัดยอดค้างรับ + เดินสถานะใบสั่งซื้อ (รวมการถอยสถานะ) | `ENG-GRN-04` · `BR-13` · `AT-29` |
| **IS-08** | ข้อมูลการส่งจริง + ผู้รับของ/ผู้ตรวจเป็นบุคคลจริง | `04_DB §4.2` header · `BR-23` · `AT-31` |
| **IS-09** | เลขเอกสารจากศูนย์ตั้งค่า `GRN-YYYY-NNNN` ออกตอนบันทึกรับเข้า | `ENG-DOC-NUM` · `FN-11` ข้อ 3 · `AT-21` |
| **IS-10** | เอกสารพิมพ์ A4 · 3 ช่องลงชื่อ · ปี ค.ศ. ทุกจุด | `FN-15 buildPrintModel` · `API-11` · `AT-33` |
| **IS-11** | เอกสารแนบ แสดงในหน้ารายละเอียด | `API-10` · `AT-34` |
| **IS-12** | ป้าย "รอตั้ง GR/IR" พร้อมมูลค่า (**จำลอง**) | `FN-11` ข้อ 6 · `AT-35` · `07_LOCKED LD-05` |
| **IS-13** | บรรทัดบริการปิดยอดค้างโดยไม่เกิดความเคลื่อนไหว (ตอบ `OQ-PO-06`) | `FN-10 isServiceLine` · `BR-08` · `AT-37` |

**สัญญาข้อมูลที่รับเข้ามาจริง**

| จาก | สัญญา | ถ้าต้นทางเปลี่ยนกลางทาง |
|---|---|---|
| **F078 PO** | `GET /purchase/po/{id}/receivable-lines` → `{ line_no, item_ref, qty_ordered, received, tolerance_pct, unit_price, discount_pct, vat_mode, vat_pct, want_date, kind }` | แก้แล้วอนุมัติใหม่ → เตือน + `API-06 refresh-from-po` · ยกเลิก/ปิดก่อนครบ → `PO_NOT_RECEIVABLE` |
| ทะเบียนกลาง | ผู้ขาย · สินค้า · หน่วย · ตำแหน่ง · ศูนย์ต้นทุน · พนักงาน | **soft-ref** — ค่าที่หายยังแสดงข้อความเดิม ใบเก่าไม่พัง |
| คอนฟิกโซนกักต่อคลัง (**CF-04**) | ปลายทางของของไม่ผ่าน | เปลี่ยนค่าไม่กระทบใบที่บันทึกแล้ว (เก็บ snapshot) |

### ขาออก (Outbound · OS-01..OS-08) — อ้างรหัสจาก BRD §3.2 ครบทุกข้อ

| OS | สาระ | สถานะในรอบนี้ |
|---|---|---|
| **OS-01** | ลงบัญชีจริง (สมุดรายวัน/แยกประเภท) | ❌ **นอกขอบเขต** — ระบบบัญชีคลื่น W5 · รอบนี้เป็นป้ายจำลอง (`LD-05`) |
| **OS-02** | การจับคู่สามทางกับใบแจ้งหนี้ | ❌ **นอกขอบเขต** — งานฝั่งเจ้าหนี้ (W5) · ทดสอบสัญญาที่ `AT-X-07` |
| **OS-03** | คืนของผู้ขาย (RTV) | ❌ **นอกขอบเขต** — `F080` feature ถัดไปในเลน · สัญญาที่ `AT-X-05` |
| **OS-04** | จัดเก็บลงช่องเก็บ (bin) + กลยุทธ์จัดเก็บ | ❌ **นอกขอบเขต** — `F-WH-PUTAWAY` คลื่น W3Q · สัญญาที่ `AT-X-04` |
| **OS-05** | ล็อต / ซีเรียล / วันหมดอายุ | ❌ **ไม่ทำ** — ยังไม่มีทะเบียนล็อตในเลนนี้ · กันไว้ที่ `AT-39` |
| **OS-06** | ต้นทุนแฝงและต้นทุนเฉลี่ย | ❌ **นอกขอบเขต** — `F069`/`F070` คลื่น W4 · ผูกกับ `Q6` |
| **OS-07** | รับของโดยไม่มีใบสั่งซื้อ · 1 ใบรับข้ามหลายใบสั่งซื้อ · ASN · สแกนบาร์โค้ด | ❌ **ตัดสินแล้วว่าไม่ทำ** — บังคับกันไว้ที่ `AT-38` · `AT-39` |
| **OS-08** | สายอนุมัติของการรับของ | ❌ **ตัดสินแล้วว่าไม่มี** — การรับของไม่ใช่การอนุมัติ · `LOCK-04` · `LD-04` · กันไว้ที่ `AT-32` |

> ทุกข้อข้างบนเป็น **ขอบเขตที่ตัดออกอย่างตั้งใจ** ไม่ใช่งานที่ตกหล่น — `OS-05` `OS-07` `OS-08` มีเคสทดสอบคอยกันไม่ให้งอกกลับเข้ามา

**สัญญาข้อมูลที่ส่งออกจริง**

| ไป | สัญญา | ตอนกลับรายการ |
|---|---|---|
| **F078 PO** | `PATCH /purchase/po/{id}/received` — **เขียนได้จาก GRN เท่านั้น (R13)** | หักยอดคืน + ถอยสถานะ `closed → partially received → sent` |
| ยอดคงคลัง (F009) | movement `in` bucket `stock` + `quarantine` | movement ตรงข้าม ชี้ `reversal_of` — **ของเดิมยังอยู่** |
| **F081 Putaway (W3Q)** | เหตุการณ์ `grn_posted` + บรรทัดที่ผ่านตรวจ → คิวจัดเก็บ | คิวจัดเก็บต้องถูกยกเลิก — **ยังไม่ต่อจริงในรอบนี้** |
| **F080 RTV** | ของในโซนกักรอคืนผู้ขาย | ถ้าคืนไปแล้ว **ห้ามกลับรายการ** (R16) |
| บัญชี GR/IR (W5) | ตั้งพักหนี้ = ยอดก่อนภาษี | ต้องกลับรายการบัญชีด้วย — **ยังไม่ต่อจริงในรอบนี้** |
| **F095 AP Invoice (W5)** | ขาที่สองของการจับคู่สามทาง | การจับคู่ต้องไม่นับใบที่ถูกกลับรายการ |
| **ENG-NOTIFY** | 7 เหตุการณ์ตาม `NTF_BRIEF_F-WH-GRN.md` | `grn_reversed` |
| **ENG-CSQ** | 3 เหตุการณ์ตาม `CSQ_BRIEF_F-WH-GRN.md` | เหตุการณ์ที่ชี้กลับเหตุการณ์เดิม — **ห้ามลบผลเดิม** |

> **สถานะการต่อจริง:** สัญญาทั้งหมดข้างบน **ประกาศครบ** แต่ปลายทางที่เป็นคลื่นถัดไป (Putaway · RTV · GR/IR) **ยังเป็นการจำลองในต้นแบบ** ตาม LOCK-07 — ดู `07_LOCKED LD-05`

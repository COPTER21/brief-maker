# 02_API — F-PUR-PO · ใบสั่งซื้อ

> **Audience:** BE dev (HTTP layer)
> **ขอบเขตไฟล์นี้:** routing · request/response · authz · error mapping **เท่านั้น**
> business logic อยู่ที่ `03_LOGIC` (R8 · Logic Placement Matrix)

Base path: `/api/v1/purchase-orders`

---

## §2.1 API Inventory

| ID | Method · Path | หน้าที่ | Mutation |
|---|---|---|---|
| API-01 | `GET /purchase-orders` | รายการ + ตัวกรอง + แถบสรุป | — |
| API-02 | `POST /purchase-orders` | สร้างใบใหม่ (ร่าง) | ✅ |
| API-03 | `GET /purchase-orders/:id` | รายละเอียดใบเดียว | — |
| API-04 | `PUT /purchase-orders/:id` | แก้ใบ (ร่าง หรือ แก้หลังอนุมัติ) | ✅ |
| API-05 | `POST /purchase-orders/:id/submit` | ส่งอนุมัติ | ✅ |
| API-06 | `POST /purchase-orders/:id/approve` | อนุมัติ 1 ขั้น | ✅ |
| API-07 | `POST /purchase-orders/:id/reject` | ไม่อนุมัติ / ส่งกลับแก้ | ✅ |
| API-08 | `POST /purchase-orders/:id/send` | ส่งให้ผู้ขาย | ✅ |
| API-09 | `POST /purchase-orders/:id/cancel` | ยกเลิก | ✅ |
| API-10 | `POST /purchase-orders/:id/short-close` | ปิดใบก่อนกำหนด | ✅ |
| API-11 | `GET /purchase-orders/:id/document` | ไฟล์เอกสาร A4 | — |
| API-12 | `GET /purchase-orders/:id/audit` | ประวัติ | — |
| API-13 | `POST /purchase-orders/:id/attachments` | แนบไฟล์ | ✅ |
| API-14 | `GET /purchase-orders/duplicate-check` | ตรวจใบซ้ำ (เตือน) | — |
| API-15 | `GET /purchase-orders/:id/doa-preview` | ดูสายอนุมัติที่จะใช้ตามยอด | — |

---

## §2.2 API-01 · GET /purchase-orders

**Query:** `q` · `status` · `receipt_status` · `buyer_ref` · `date_from` · `date_to` · `page` · `page_size` · `sort`
**Authz:** ทุก role ที่ล็อกอิน — **คลังเห็นเฉพาะ `status ∈ {sent, partially_received, closed}`** (§2.8)
**Response:** `{ items[], summary{ pending_approval_count, sent_or_partial_count, open_commitment_amount, overdue_count }, page{} }`
> `open_commitment_amount` = ภาระผูกพันคงค้าง (S-12) — คำนวณที่ `03_LOGIC FN-25`

---

## §2.3 API-02 · POST /purchase-orders

**Body:** `{ source_type, pr_ref?, compare_ref?, vendor_ref, doc_date, need_date, payment_term_ref, warehouse_ref, ship_to_address, cost_center_ref?, buyer_ref, external_ref?, note?, lines[], header_discount?, wht? }`
**Authz:** จัดซื้อ · หัวหน้าจัดซื้อ
**Calls:** `FN-01 createPurchaseOrder` → `FN-05 validatePoDraft` → `FN-20 calcPoTotals`
**Response `201`:** ใบที่สร้าง (status `draft` · **ยังไม่มี `po_no`**)
**Errors:** `VALIDATION_FAILED` · `FORBIDDEN`

---

## §2.4 API-04 · PUT /purchase-orders/:id

**Body:** เหมือน API-02 + `reapprove_reason?` + `override_note?` + `version` (optimistic lock)
**Authz:** จัดซื้อ · หัวหน้าจัดซื้อ
**พฤติกรรมตามสถานะ:**

| สถานะปัจจุบัน | ผล |
|---|---|
| `draft` | แก้ตรง ๆ |
| `approved` · `sent` | **Transition Guard** — บังคับ `reapprove_reason` → ใบกลับเป็น `draft` + ล้างผลอนุมัติเดิมเข้าประวัติ (BR-10 · R12) |
| `partially_received` · `closed` · `cancelled` | `409 PO_LOCKED` |

**Calls:** `FN-16 applyTransitionGuard` → `FN-17 revertToDraft` → `FN-20 calcPoTotals`
**Errors:** `PO_LOCKED` · `REASON_REQUIRED` · `CONFLICT_VERSION` (`[AI-DEFAULT]` PR-1)

---

## §2.5 API-05 · POST /purchase-orders/:id/submit

**Body:** `{ approvers: [{ step_no, person_ref }], idempotency_key }`
**Authz:** จัดซื้อ · หัวหน้าจัดซื้อ (**ต้องไม่ใช่ผู้อนุมัติของใบเดียวกัน** — R09)
**Calls:** `FN-05 validatePoDraft` → `FN-06 checkPrRemaining` → `FN-10 resolveDoaChain` → `FN-11 snapshotApprovalChain`

**Hard controls (บล็อกจริง):**

| เงื่อนไข | Error |
|---|---|
| ไม่มีบรรทัด | `NO_LINES` (R02) |
| ช่องบังคับขาด | `VALIDATION_FAILED` (R03) |
| มีขั้นที่ยังไม่เลือกคน | `APPROVER_REQUIRED` (R08 · VR09) |
| **ยอดสุทธิ > ยอดคงเหลือใบขอซื้อ** | **`EXCEEDS_PR_REMAINING`** (E02 · VR12 · L-09) |
| ผู้ส่ง = ผู้อนุมัติ | `SOD_VIOLATION` (R09) |
| แก้ราคาแต่ไม่มีเหตุผล | `OVERRIDE_NOTE_REQUIRED` (VR11) |
| ไม่มี entry ใน ทะเบียน DOA | `DOA_ENTRY_NOT_FOUND` |

**Soft (เตือนอย่างเดียว ไม่บล็อก):** `over_budget` · `vendor_suspended` · `pr_cancelled` · `possible_duplicate`
→ ส่งกลับใน `warnings[]` ของ response `200` **ไม่ทำให้ request ล้มเหลว** (R17 · L-09)

**Response:** status → `pending_approval` + `approval_chain[]` (ภาพนิ่ง)

---

## §2.6 API-06 · POST /purchase-orders/:id/approve

**Body:** `{ comment?, idempotency_key }`
**Authz:** **เฉพาะ `person_ref` ของขั้นปัจจุบัน** และต้องไม่ใช่ `submitted_by`
**Calls:** `FN-12 approveStep` → (ถ้าครบสาย) `FN-13 finalizeApproval`

**เมื่ออนุมัติครบสาย — ผลข้างเคียงตามลำดับ:**
1. `FN-14 issueDocumentNumber` → ขอเลขจากทะเบียนเอกสารกลาง `PO-YYYY-NNNN` (LOCK-03)
2. สถานะ → `approved` · เติม `approved_by` / `approved_at`
3. **เกิดภาระผูกพัน** (R11) → ยิง event ไป ระบบควบคุมงบ (§2.7)
4. ยิง event ไป 7C Consequence + ศูนย์แจ้งเตือน
5. เก็บสำเนาเอกสารตามนโยบาย `DOCCFG`

**Errors:** `NOT_CURRENT_APPROVER` · `SOD_VIOLATION` · `ALREADY_DECIDED` · `DOC_NUMBER_UNAVAILABLE`

---

## §2.7 Cross-Module Contract (R12 — จาก BRD §12.1)

> ทุกแถวใน Downstream Impact Map ต้องมี contract ที่นี่

### 2.7.1 → ใบรับของ (F079 · W3P)

`GET /purchase-orders/receivable` — คืนใบที่สถานะ `sent` หรือ `partially_received` เท่านั้น (R16 · BR-14)

```json
{ "po_no": "PO-2026-0003", "vendor_ref": "V-1001", "warehouse_ref": "WH-01",
  "lines": [ { "line_id": "...", "item_ref": "PVC-4001", "uom_ref": "เส้น",
               "qty_ordered": 100, "qty_received": 100, "qty_open": 0,
               "over_receipt_tolerance_pct": 0, "line_status": "received" } ] }
```

> **`over_receipt_tolerance_pct` — PO เป็นผู้เก็บค่า · ใบรับของเป็นผู้บังคับเพดาน** (BR-08 · R10 · HANDOFF §7)
> PO **ไม่มี** ตรรกะเทียบยอดรับกับเพดานโดยเจตนา

**ถ้าใบถูกแก้/ยกเลิก/ปิดก่อนกำหนด:** `PUT` สถานะแล้ว ใบรับของเปิดใหม่ไม่ได้ — ใบรับของต้องเช็คสถานะทุกครั้งก่อนเปิด

### 2.7.2 → ระบบควบคุมงบ (F117 · W7) — **ยังไม่มีจริง**

event `po.commitment.changed`
```json
{ "po_no": "...", "cost_center_ref": "CC-210", "delta_amount": 1517688.00,
  "reason": "approved | cancelled | short_closed | amount_revised" }
```
| trigger | delta |
|---|---|
| อนุมัติครบสาย | **+ ยอดสุทธิ** |
| ยกเลิก | **− ยอดคงค้างทั้งหมด** |
| ปิดใบก่อนกำหนด | **− มูลค่าของยอดค้างรับที่ถูกยกเลิก** |
| แก้ยอดหลังอนุมัติ | **± ส่วนต่าง** |

> รอบนี้ผู้บริโภคยังไม่มี — **ยิง event ออกได้เลย ฝั่งรับมาทีหลัง** · ผลตรวจงบขาเข้าเป็นข้อมูลจำลอง ไม่บล็อก (R17)

### 2.7.3 → 7C Consequence (ENG-CSQ)
5 event ตาม `CSQ_BRIEF_F-PUR-PO-001.md` — อนุมัติ · ยกเลิก · ปิดใบก่อนกำหนด · ปรับยอดหลังอนุมัติ · ปิดใบเมื่อรับครบ
**ไม่มีท่อบัญชี (AC)** — ใบสั่งซื้อไม่ลงบัญชี (LOCK-07)

### 2.7.4 → ศูนย์แจ้งเตือน (ENG-NOTIFY)
10 event ตาม `NTF_BRIEF_F-PUR-PO-001.md` — **feature ประกาศ event เท่านั้น ห้าม hardcode ช่องทาง/ผู้รับ**
event ของสาย DOA (`doa_pending` / `doa_result`) มาจาก DOA engine อัตโนมัติ — **ห้ามประกาศซ้ำ**

### 2.7.5 → ทะเบียนเอกสารกลาง (F-DOCCFG)
`ENG-DOC-NUM.next('PO')` ตอนอนุมัติครบ · `ENG-DOC-STORE.store()` ตอนอนุมัติและตอนส่งผู้ขาย
**ห้าม feature สร้างเลขเอง** (LOCK-03 · R22)

### 2.7.6 → ผู้ขาย (ภายนอก)
API-08 ส่งเอกสาร A4 ผ่านบริการอีเมล · **แก้หลังส่งแล้วต้องส่งฉบับแก้ไขอีกครั้ง**

### 2.7.7 ✗ บัญชีแยกประเภท (W5)
**ไม่มี contract โดยเจตนา** — LOCK-07 (ดู `07_LOCKED LD-07`)

---

## §2.8 Authorization Matrix

| API | จัดซื้อ | หน.จัดซื้อ | ผอ. | CFO | คลัง | บัญชี | ผู้ดูแล |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| API-01 list | ✅ | ✅ | ✅ | ✅ | ✅ * | ✅ | ✅ |
| API-02 create · API-04 update | ✅ | ✅ | ✗ | ✗ | ✗ | ✗ | ✗ |
| API-05 submit | ✅ | ✅ | ✗ | ✗ | ✗ | ✗ | ✗ |
| API-06 approve · API-07 reject | ✗ | ✅ ** | ✅ ** | ✅ ** | ✗ | ✗ | ✗ |
| API-08 send · API-09 cancel · API-10 short-close | ✅ | ✅ | ✗ | ✗ | ✗ | ✗ | ✗ |
| API-03 detail · API-11 document · API-12 audit | ✅ | ✅ | ✅ | ✅ | ✅ * | ✅ | ✅ |

\* คลัง — เห็นเฉพาะใบสถานะ `sent` ขึ้นไป และ **response ตัดฟิลด์ราคา/ยอดรวมออก** (§4.6.3)
\*\* เฉพาะใบที่ตนถูกเลือกเป็นผู้อนุมัติในขั้นนั้น และไม่ใช่ผู้ส่งอนุมัติ (R09)

---

## §2.9 Concurrency & Idempotency `[AI-DEFAULT]`

| ประเด็น | ข้อกำหนด | ที่มา |
|---|---|---|
| แก้ใบเดียวกันพร้อมกัน | ทุก `PUT` ส่ง `version` — ไม่ตรง → **`409 CONFLICT_VERSION`** | `[AI-DEFAULT]` PR-1 |
| กดส่ง/อนุมัติซ้ำ | ทุก mutation ที่เปลี่ยนสถานะต้องมี `idempotency_key` — คีย์ซ้ำคืนผลเดิม ไม่ทำซ้ำ | `[AI-DEFAULT]` PR-7 · VR18 |
| ผู้อนุมัติถูกถอดสิทธิ์หลังส่ง | ใช้**ภาพนิ่ง**สายอนุมัติ ณ เวลาส่ง ไม่ re-resolve จากทะเบียน DOA | `[AI-DEFAULT]` PR-9 |

> ทั้ง 3 ข้อรอ BA ยืนยัน — ดู `00_OVERVIEW §0.13`

---

## §2.10 Error Catalog

| Code | HTTP | ข้อความที่ผู้ใช้เห็น |
|---|---|---|
| `VALIDATION_FAILED` | 422 | ตาม VR ที่ไม่ผ่าน (ชี้ช่องแรกที่ขาด) |
| `NO_LINES` | 422 | `กรุณาเพิ่มรายการสินค้าอย่างน้อย 1 รายการ` |
| `APPROVER_REQUIRED` | 422 | `เลือกผู้อนุมัติให้ครบทุกขั้น` |
| `EXCEEDS_PR_REMAINING` | 422 | `เกินยอดคงเหลือของใบขอซื้อ — บันทึกร่างได้ ส่งอนุมัติไม่ได้` |
| `OVERRIDE_NOTE_REQUIRED` | 422 | `ระบุเหตุผลการแก้ราคาก่อนบันทึก` |
| `REASON_REQUIRED` | 422 | `กรุณาระบุเหตุผล` |
| `SOD_VIOLATION` | 403 | `ผู้ส่งอนุมัติเป็นผู้อนุมัติใบเดียวกันไม่ได้` |
| `NOT_CURRENT_APPROVER` | 403 | `ใบนี้ยังไม่ถึงขั้นอนุมัติของคุณ` |
| `PO_LOCKED` | 409 | `มีการรับของแล้ว — ยกเลิกไม่ได้ ให้ใช้ปิดใบก่อนกำหนด` |
| `CONFLICT_VERSION` | 409 | `มีคนอื่นแก้ใบนี้ไปแล้ว — โหลดใหม่แล้วลองอีกครั้ง` |
| `ALREADY_DECIDED` | 409 | `ขั้นนี้ถูกตัดสินไปแล้ว` |
| `CANCEL_NOT_ALLOWED` | 409 | `มีการรับของแล้ว — ยกเลิกไม่ได้` |
| `SHORT_CLOSE_NOT_ALLOWED` | 409 | `ปิดใบก่อนกำหนดทำได้เฉพาะใบที่รับของบางส่วน` |
| `DOA_ENTRY_NOT_FOUND` | 424 | `ยังไม่ได้ตั้งค่าสายอนุมัติสำหรับยอดนี้` |
| `DOC_NUMBER_UNAVAILABLE` | 424 | `ออกเลขเอกสารไม่สำเร็จ — ลองอีกครั้ง` |

# 02_API — F-PUR-PR · PR ใบขอซื้อ

> Audience: BE dev (**HTTP layer เท่านั้น**) · business logic อยู่ที่ `03_LOGIC.md`
> Base path: `/api/v1/purchase-requisitions`
> **ยอดเงินทุกตัวคำนวณฝั่งเซิร์ฟเวอร์เสมอ — ห้ามเชื่อค่าที่ส่งมาจากหน้าจอ** (BRD §14.3)

## §2.1 API-01 · GET `/purchase-requisitions` — รายการ

| key | value |
|---|---|
| Method / Path | `GET /api/v1/purchase-requisitions` |
| Auth | required |
| Query | `q` · `status` · `department` · `requester_id` · `sort` (`code`\|`doc_date`\|`required_date`\|`grand_total`) · `dir` · `page` · `size` |
| Response 200 | `{ items: PrListItem[], total, page, size }` |
| `PrListItem` | `pr_no · doc_date · requester{id,name} · department · required_date · status · pr_type · sign_progress{done,total} · grand_total` |
| Errors | `401 UNAUTHORIZED` · `403 FORBIDDEN` |
| Calls | `03_LOGIC` FN-01 `buildPrListQuery` |
| Reads | `t_pr_header` · `t_pr_approval_slot` (นับ n/N) |

> **Scope filter:** ผู้ขอเห็นเฉพาะใบของตนและหน่วยงานตน · หัวหน้าเห็นใบที่ตนอยู่ในสาย · จนท.จัดซื้อ/ผู้ตรวจสอบเห็นทั้งหมด (BRD §4.2)

## §2.2 API-02 · GET `/purchase-requisitions/:id` — รายละเอียด

| key | value |
|---|---|
| Response 200 | `{ header, lines[], slots[], attachments[], vendor_suggests[], history[] }` |
| Errors | `401` · `403 PR_NOT_VISIBLE` · `404 PR_NOT_FOUND` |
| Calls | FN-02 `getPrDetail` · FN-11 `resolveCurrentActor` (คำนวณว่าผู้เรียกกดอนุมัติได้ไหม) |
| Response พิเศษ | `can_approve: bool` · `can_edit: bool` · `can_recall: bool` · `can_cancel: bool` — **UI ใช้ field นี้ตัดสินปุ่ม ไม่คำนวณสิทธิ์เอง** |

> **Confidential masking:** ผู้ที่ไม่มีสิทธิ์ดูราคา → ตัด `unit_price_est` · `subtotal` · `grand_total` · `budget_check_result` ออกจาก response (`04_DB §4.6.2`)

## §2.3 API-03 · POST `/purchase-requisitions` — สร้างร่าง

| key | value |
|---|---|
| Body | `{ doc_date, required_date, department, cost_center_id?, pr_type, reason, ref_external?, note?, lines[], vendor_suggests[] }` |
| Response 201 | `{ pr_id, status: 'draft', pr_no: null }` |
| Errors | `400 PR_VALIDATION_FAILED` (รวม V-01..V-05) · `401` · `403` |
| Calls | FN-03 `createPrDraft` · FN-04 `validatePrHeader` · FN-05 `validatePrLines` · **ENG-PR-CALC** |
| Writes | `t_pr_header` · `t_pr_line` · `t_pr_vendor_suggest` · `t_pr_history` (`create`) |

> **ไม่ออกเลขที่** — `pr_no` เป็น null จนกว่าจะส่งอนุมัติ (BR-05 · DOCCFG)

## §2.4 API-04 · PUT `/purchase-requisitions/:id` — แก้ไขร่าง

| key | value |
|---|---|
| Body | เหมือน API-03 + `version` |
| Response 200 | `{ pr_id, version }` |
| Errors | `400 PR_VALIDATION_FAILED` · `409 PR_VERSION_CONFLICT` `[AI-DEFAULT]` PR-9 · `409 PR_NOT_EDITABLE` (สถานะไม่ใช่ร่าง — BR-04) |
| Calls | FN-06 `updatePrDraft` · FN-04 · FN-05 · **ENG-PR-CALC** |
| Writes | `t_pr_header` · `t_pr_line` · `t_pr_history` (`update` + before/after) |

## §2.5 API-05 · POST `/purchase-requisitions/:id/submit` — ส่งอนุมัติ ★

| key | value |
|---|---|
| Body | `{ slots: [{ slot_seq, approver_id }], idempotency_key }` `[AI-DEFAULT]` PR-7 |
| Response 200 | `{ pr_no, status: 'pending_approval', slots[] }` |
| Errors | `400 PR_SLOTS_INCOMPLETE` (V-08) · `400 PR_NO_USABLE_LINE` (V-03) · `403 PR_SELF_APPROVAL_FORBIDDEN` (BR-03) · `409 PR_NOT_DRAFT` (BR-01) · `409 PR_DUPLICATE_SUBMIT` |
| Calls | FN-08 `submitPr` · FN-05 · FN-07 `checkBudgetMock` · **ENG-PR-CALC** · **ENG-DOA-RESOLVE** · `ENG-DOC-NUM` · `ENG-NOTIFY` |
| Writes | `t_pr_header` (status · `pr_no` · `doa_entry_ref`) · `t_pr_approval_slot` (**แช่แข็ง**) · `t_pr_history` (`submit`) |

**ลำดับที่ต้องทำ (สำคัญ):**
1. ตรวจสถานะ = `draft` ไม่งั้น `409`
2. คำนวณยอดใหม่ฝั่งเซิร์ฟเวอร์ (**ENG-PR-CALC**) — ห้ามใช้ยอดจาก client
3. `ENG-DOA-RESOLVE(grand_total)` → ได้ชั้นอนุมัติ + จำนวนขั้น
4. ตรวจว่า `slots` ที่ส่งมาครบทุกขั้นและ **ผู้ขอไม่ได้เลือกตัวเอง** (BR-03)
5. `pr_no = ENG-DOC-NUM.next('PR', company_ctx)` — **ห้าม format เอง ห้าม +1 เอง**
6. เขียน slot แบบ snapshot (ชื่อ + ตำแหน่ง) · **แช่แข็ง** (BR-02)
7. `ENG-NOTIFY.emit('pr_submitted', {...})` + ถ้างบไม่พอ → `pr_budget_warning`

## §2.6 API-06 · POST `/purchase-requisitions/:id/approve` — อนุมัติ

| key | value |
|---|---|
| Body | `{ slot_seq, note?, idempotency_key }` |
| Response 200 | `{ status, slots[] }` |
| Errors | `403 PR_NOT_CURRENT_APPROVER` (BR-03 · SC-10) · `409 PR_SLOT_ALREADY_DECIDED` `[AI-DEFAULT]` PR-1 · `409 PR_NOT_PENDING` |
| Calls | FN-09 `approvePrSlot` · FN-11 · `ENG-NOTIFY` · `ENG-CSQ` · `ENG-DOC-STORE` |
| Writes | `t_pr_approval_slot` · `t_pr_header` (ถ้าขั้นสุดท้าย → `approved`) · `t_pr_history` |

> **ขั้นสุดท้ายเท่านั้น** จึงยิง `pr_approved` + `ENG-CSQ doc.approved (EC/estimated)` + `ENG-DOC-STORE.store(pdf,'PR',id,'approved_final')`
> **PR-1 optimistic lock:** ถ้า slot ถูกตัดสินไปแล้ว → `409` พร้อมข้อความว่าถูกพิจารณาแล้ว (คนแรกชนะ)

## §2.7 API-07..API-10 · transition ที่เหลือ

| API | Path | Body | สถานะปลายทาง | Errors หลัก | Calls |
|---|---|---|---|---|---|
| API-07 | `POST /:id/reject` | `{ slot_seq, reason }` **เหตุผลบังคับ ≥3** | `rejected` | `400 PR_REASON_REQUIRED` (V-07) · `403 PR_NOT_CURRENT_APPROVER` | FN-13 `rejectPr` · `ENG-NOTIFY` |
| API-08 | `POST /:id/recall` | `{}` | `draft` | `403 PR_NOT_REQUESTER` · `409 PR_NOT_PENDING` | FN-10 `recallPr` · `ENG-NOTIFY` |
| API-09 | `POST /:id/cancel` | `{ reason }` **บังคับ ≥3** | `cancelled` | `400 PR_REASON_REQUIRED` · `409 PR_HAS_PO_REFERENCE` | FN-14 `cancelPr` · `ENG-NOTIFY` · `ENG-CSQ` |
| API-10 | `POST /:id/duplicate` | `{}` | ร่างใหม่ | `403` | FN-12 `duplicatePr` |

> **API-08 recall:** slot ทั้งหมด → `decision='void'` **ไม่ลบแถว** (EC-03) · ต้องเลือกสายใหม่ตอน submit ครั้งถัดไป (BR-04)
> **API-09 cancel:** `PR_HAS_PO_REFERENCE` เป็นข้อกำหนดเชิงกติกา — ตรวจจริงได้เมื่อ W3 พร้อม (รอบนี้ผ่านเสมอ)
> **API-10 duplicate:** คัดลอกหัว + รายการ · **ไม่คัดลอก** `pr_no` · slot · history · attachment (AC-13)

## §2.8 API-11..API-12 · เอกสารแนบ

| API | Path | หมายเหตุ |
|---|---|---|
| API-11 | `POST /:id/attachments` (multipart) | ตรวจ **ชนิดและขนาดซ้ำฝั่งเซิร์ฟเวอร์** — ห้ามเชื่อ client (S-07) · `400 PR_FILE_REJECTED` · ยิง `pr_attachment_added` ถ้าเพิ่มหลังส่งอนุมัติ |
| API-12 | `DELETE /:id/attachments/:aid` | **ลบได้เฉพาะสถานะร่าง** · `409 PR_NOT_EDITABLE` |

## §2.9 ★ Cross-Module Contract (R12 · จาก BRD §12.1)

| XT | ปลายทาง | สัญญา | สถานะรอบนี้ |
|---|---|---|---|
| **XT-01** | **F073 เทียบราคาผู้ขาย** | `GET /purchase-requisitions?status=approved` → F073 ดึงใบที่อนุมัติแล้ว + รายการ + จำนวน + ราคาประมาณ + ผู้ขายที่แนะนำ | **จุดเชื่อมเท่านั้น** — ปุ่มบนจอขึ้น `การเทียบราคาผู้ขายยังไม่เปิดใช้งานในระบบช่วงนี้` |
| **XT-02** | **W3 ใบสั่งซื้อ** | ใบที่อนุมัติแล้วเป็นเอกสารต้นทาง · PO ต้องอ้าง `pr_id` กลับมาเพื่อให้ `PR_HAS_PO_REFERENCE` ทำงาน | **จุดเชื่อมเท่านั้น** |
| **XT-03** | **W7 ควบคุมงบ (F117)** | `ENG-BUDGET.check({cost_center, amount, period})` → `{ok, remaining, budget_code}` `[ASSUMED contract]` A-01 | **จำลอง + `TODO: budget-control hook`** — ห้าม implement (LOCK-FW) |
| **XT-04** | **7C ประทับผล** | `ENG-CSQ` รับ `doc.approved` (EC · kind=`estimated`) และ `doc.cancelled` (EC · kind=`avoided`) · basis=`declared` · **feature ไม่คำนวณมูลค่าเอง** | ประกาศแล้วใน `CSQ_BRIEF` |
| **XT-05** | **ศูนย์แจ้งเตือน** | `ENG-NOTIFY.emit(event_id, {ref, vars})` 7 event ตาม `NTF_BRIEF` · **ห้ามเช็ค preference เอง ห้ามระบุช่องทาง** | ประกาศแล้ว |
| **XT-06** | **ทะเบียนเลขเอกสาร** | `ENG-DOC-NUM.next('PR', company_ctx)` ตอน submit · `ENG-DOC-STORE.store(...,'approved_final')` ตอนอนุมัติครบ | ประกาศแล้วใน `DOCCFG_BRIEF` |

> **ยกเลิก/แก้กลางทาง:** ยกเลิกใบที่อนุมัติแล้ว → `doc.cancelled` (EC/avoided) · ถ้า W7 พร้อมต้องคืนงบที่จองไว้ด้วย (OQ-04)

## §2.10 Error Catalog

| Code | HTTP | ความหมาย | trace |
|---|---|---|---|
| `PR_VALIDATION_FAILED` | 400 | V-01..V-05 ไม่ผ่าน | `05_RULES` V-01..05 |
| `PR_NO_USABLE_LINE` | 400 | ไม่มีรายการที่ครบ | V-03 |
| `PR_SLOTS_INCOMPLETE` | 400 | เลือกผู้อนุมัติไม่ครบทุกขั้น | V-08 |
| `PR_REASON_REQUIRED` | 400 | เหตุผล < 3 ตัวอักษร | V-07 |
| `PR_FILE_REJECTED` | 400 | ชนิด/ขนาดไฟล์ไม่ผ่าน | V-06 · EC-05 |
| `PR_NOT_VISIBLE` | 403 | ไม่มีสิทธิ์ดูใบนี้ | EC-06 |
| `PR_NOT_CURRENT_APPROVER` | 403 | ไม่ใช่ผู้อนุมัติขั้นปัจจุบัน | BR-03 · SC-10 |
| `PR_SELF_APPROVAL_FORBIDDEN` | 403 | ผู้ขอเลือกตัวเองเป็นผู้อนุมัติ | BR-03 |
| `PR_NOT_REQUESTER` | 403 | ไม่ใช่ผู้ขอ (เรียกคืน) | — |
| `PR_NOT_FOUND` | 404 | ไม่พบเอกสาร | — |
| `PR_NOT_DRAFT` | 409 | ส่งอนุมัติได้เฉพาะร่าง | BR-01 |
| `PR_NOT_EDITABLE` | 409 | แก้ได้เฉพาะร่าง | BR-04 |
| `PR_NOT_PENDING` | 409 | ใบไม่ได้อยู่สถานะรออนุมัติ | — |
| `PR_SLOT_ALREADY_DECIDED` | 409 | ขั้นนี้ถูกตัดสินไปแล้ว | CA-01 `[AI-DEFAULT]` |
| `PR_VERSION_CONFLICT` | 409 | แก้ชนกัน 2 หน้าต่าง | PR-9 `[AI-DEFAULT]` |
| `PR_DUPLICATE_SUBMIT` | 409 | idempotency key ซ้ำ | PR-7 `[AI-DEFAULT]` |
| `PR_HAS_PO_REFERENCE` | 409 | มีใบสั่งซื้ออ้างถึงแล้ว | BRD §5.2.3 |

# 02_API — F-HR-OSW แบบขออนุญาตออกปฏิบัติงานนอกสถานที่

> Audience: BE dev (HTTP layer only) · business logic อยู่ 03_LOGIC · ทุก API: `Authorization: Bearer` + `X-Tenant-Id` · ID scope-local `F-OSW-API-NN` (ดู 07 CD-01)

## §2.1 API Overview
| ID | Method | Path | Summary | Roles | Mutation |
|---|---|---|---|---|:---:|
| F-OSW-API-01 | GET | /api/v1/osw | รายการ + กรอง + stats | ทุก role (scope BR-OSW-19) | — |
| F-OSW-API-02 | GET | /api/v1/osw/{id} | รายละเอียด + lines + attachments + chain + audit | ตาม scope | — |
| F-OSW-API-03 | POST | /api/v1/osw | สร้าง (ร่าง) · ออกเลข · ทำซ้ำได้ | พนักงาน | ✅ |
| F-OSW-API-04 | PUT | /api/v1/osw/{id} | แก้ไขร่าง | เจ้าของ | ✅ |
| F-OSW-API-05 | GET | /api/v1/osw/{id}/approval-preview | resolve DOA → ขั้น + ผู้พิจารณาเริ่มต้น | เจ้าของ | — |
| F-OSW-API-06 | POST | /api/v1/osw/{id}/submit | ส่งขออนุญาต (assignees ต่อขั้น) | เจ้าของ | ✅ |
| F-OSW-API-07 | POST | /api/v1/osw/{id}/approve | อนุญาตขั้นปัจจุบัน | ผู้พิจารณาขั้นปัจจุบัน | ✅ |
| F-OSW-API-08 | POST | /api/v1/osw/{id}/reject | ไม่อนุญาต + เหตุผล | ผู้พิจารณาขั้นปัจจุบัน | ✅ |
| F-OSW-API-09 | POST | /api/v1/osw/{id}/cancel | ยกเลิก + เหตุผล | เจ้าของ / HR | ✅ |
| F-OSW-API-10 | GET | /api/v1/osw/{id}/pdf | PDF FM-HRM-02 (render หรือ approved_final) | ตาม scope | — |
| F-OSW-API-11 | GET | /api/v1/osw/export.csv | ส่งออกตามตัวกรอง | ตาม scope | — |
| F-OSW-API-12 | GET | /api/v1/osw/form-context | ข้อมูลผู้ขอ + ผู้บังคับบัญชา + อัตรา + เวลาเริ่มต้น + สถานะแบบเอกสาร | พนักงาน | — |
| F-OSW-API-13 | POST | /internal/v1/osw/doa-callback | callback จาก DOA engine (ตัดสินจาก My Approval) | service (DOA) | ✅ |
ไฟล์แนบ: อัปโหลดผ่าน Document Center API เดิม → ส่ง `file_id[]` ใน API-03/04

## §2.2 Per-API Contract

### F-OSW-API-01: GET /api/v1/osw
| Field | Value |
|---|---|
| auth | required · roles: any (scope by FN-01) |
**Query:** `q` (เลขที่/ผู้ขอ/เพื่อ) · `status` · `mode` · `org_unit_id` · `mine_pending` (bool — รอฉันพิจารณา) · `sort` (osw_no·req_date·employee_name·range_from·per_diem_amount) · `dir` · `page` · `page_size`=20
**Response 200:** `{ items:[{ id, osw_no, req_date, employee_name, range_from, range_to, line_count, total_days, mode, status, sign:{done,total}, per_diem_amount }], total, stats:{ all, pending, mine_pending }, page }`
**Errors:** 400 ERR_VALIDATION_FAILED
**Calls:** FN-01 buildOswList

### F-OSW-API-02: GET /api/v1/osw/{id}
**Response 200:** header ทั้งหมด (04 §4.2) + `lines[]` + `attachments[]` + `approval_chain[]` + `audit[]` + `can:{ edit, submit, decide, cancel }`
**Errors:** 404 ERR_NOT_FOUND (รวมกรณีไม่มีสิทธิ์ — ไม่เปิดเผยการมีอยู่) 
**Calls:** FN-01 (scope check `canView`)

### F-OSW-API-03: POST /api/v1/osw
| auth | required · `Idempotency-Key` required (PR-7) |
|---|---|
**Body:**
```json
{ "lines":[{ "d_from":"2026-10-12", "d_to":"2026-10-14", "t_from":"08:30", "t_to":"17:30", "purpose":"ตรวจงานติดตั้ง (โรงงานลูกค้า ขอนแก่น)" }],
  "mode":"overnight", "nights":2, "paid_nights":2, "nights_auto":true,
  "attachments":["file-uuid"], "copy_of":null }
```
**Validation (field-level):** lines ≥1 · dates ISO · times HH:mm · purpose 1–300 · mode enum · **ซับซ้อน → FN-03 validateOswDraft**
**Response 201:** `{ id, osw_no, status:"draft", version:1, per_diem_amount }`
**Errors:** 400 ERR_VALIDATION_FAILED (`errors[]` ต่อช่วง: line_no + code) · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 BR_DOCTYPE_INACTIVE · 422 BR_PERDIEM_POLICY_MISSING
**Side effects:** ENG-DOC-NUM.next('OSW') · header_snapshot จาก Organization · INSERT request/lines/attachments · audit `created`
**Calls:** FN-02 snapshotRequester · FN-03 · FN-04 computeNightsAndPerDiem · FN-05 createOswDraft · FN-15 appendOswAudit

### F-OSW-API-04: PUT /api/v1/osw/{id}
Body เหมือน API-03 + `version` · **Errors:** 403 ERR_NOT_OWNER · 409 ERR_VERSION_CONFLICT · 422 BR_NOT_DRAFT · 400 ERR_VALIDATION_FAILED
**Calls:** FN-03 · FN-04 · FN-06 updateOswDraft · FN-15

### F-OSW-API-05: GET /api/v1/osw/{id}/approval-preview
**Response 200:** `{ doa_entry_ref, chain_mode:"sequential", steps:[{ step, role_id, role_label, default_assignee:{id,name,position,dept} | null }] }`
**Errors:** 422 BR_DOA_ENTRY_MISSING
**Calls:** FN-07 resolveApprovalPreview (→ DOA engine)

### F-OSW-API-06: POST /api/v1/osw/{id}/submit
**Body:** `{ "version":3, "assignees":["emp-uuid-step1", "..."] }` · `Idempotency-Key`
**Validation:** assignees.length = จำนวนขั้น · ไม่มีค่าว่าง · ไม่มี requester (BR-OSW-11)
**Response 200:** `{ status:"pending_approval", approval_chain:[...], doa_ref }`
**Errors:** 422 BR_NOT_DRAFT · 422 BR_SOD_SELF_APPROVER · 400 ERR_ASSIGNEE_REQUIRED · 409 ERR_VERSION_CONFLICT · 400 ERR_VALIDATION_FAILED (re-validate)
**Side effects:** snapshot chain · DOA engine `doa.submit` (DOA ยิง `doa_pending`) · audit `submitted`
**Calls:** FN-03 · FN-08 submitOsw · FN-15

### F-OSW-API-07: POST /api/v1/osw/{id}/approve
**Body:** `{ "version":4, "note":"อนุญาต เดินทางปลอดภัย" }` · `Idempotency-Key`
**Response 200:** `{ status:"pending_approval"|"approved", current_step, approval_chain }`
**Errors:** 403 ERR_NOT_CURRENT_APPROVER · 409 ERR_VERSION_CONFLICT · 422 BR_NOT_PENDING
**Side effects:** อัปเดตขั้น · เปิดขั้นถัดไป หรือ approved → FN-12/FN-13 เก็บ PDF · audit
**Calls:** FN-09 decideOswStep · FN-13 storeApprovedPdf (ขั้นสุดท้าย) · FN-15

### F-OSW-API-08: POST /api/v1/osw/{id}/reject
**Body:** `{ "version":4, "reason":"ข้อมูลไม่ครบ ขอรายละเอียดเพิ่ม" }` (reason required, 1–500)
**Errors:** 400 ERR_REASON_REQUIRED · 403 ERR_NOT_CURRENT_APPROVER · 409 · 422 BR_NOT_PENDING
**Calls:** FN-09 · FN-15

### F-OSW-API-09: POST /api/v1/osw/{id}/cancel
**Body:** `{ "version":5, "reason":"งานเลื่อนหรือยกเลิก" }`
**Errors:** 400 ERR_REASON_REQUIRED · 403 ERR_NOT_OWNER_OR_HR · 409 · 422 BR_ALREADY_CLOSED (rejected/cancelled)
**Side effects:** ขั้นค้าง → skipped · DOA engine `doa.cancel(doa_ref)` (ถ้า pending) · ENG-NOTIFY `osw_cancelled` · audit
**Calls:** FN-10 cancelOsw · FN-15

### F-OSW-API-10: GET /api/v1/osw/{id}/pdf
**Query:** `disposition=inline|attachment` · **Response:** `application/pdf` (filename = `{osw_no}.pdf`) — approved → ไฟล์ approved_final จาก ENG-DOC-STORE · อื่น → render สด
**Calls:** FN-11 buildOswPrintData · FN-12 renderOswPdf (→ F-OSW-ENG-01)

### F-OSW-API-11: GET /api/v1/osw/export.csv
Query เดียวกับ API-01 · CSV UTF-8 BOM · คอลัมน์: เลขที่ · วันที่ขอ · ผู้ขอ · ฝ่าย · ช่วงที่ไป · จำนวนช่วง · ลักษณะ · สถานะ · เบี้ยเลี้ยง · audit `exported` (D9)
**Calls:** FN-01 · FN-14 exportOswCsv

### F-OSW-API-12: GET /api/v1/osw/form-context
**Response 200:** `{ employee:{id,name,position,dept}, line_manager:{id,name,position}|null, per_diem_rate:150.00, default_time:{from:"08:30",to:"17:30"}, doc_type_active:true }`
**Calls:** FN-02 snapshotRequester (preview mode) · F-DOCCFG `status('OSW')`

### F-OSW-API-13: POST /internal/v1/osw/doa-callback
**Body:** `{ doa_ref, step, decision:"approved"|"rejected", by, at, note }` · auth: service token DOA
**Rule:** ignore ถ้า doa_ref ไม่ตรง/ใบไม่ pending (ถอน/ยกเลิกแล้ว) — ตอบ 200 `ignored`
**Calls:** FN-16 applyDoaCallback → FN-09

## §2.3 Common Concerns
### Idempotency (PR-7)
`Idempotency-Key` บังคับ: API-03, 06, 07, 08, 09 · เก็บ 24 ชม. · ซ้ำ = คืนผลเดิม
### Optimistic Locking (PR-2)
ทุก mutation บนใบเดิมส่ง `version` · ไม่ตรง → 409 ERR_VERSION_CONFLICT (UI: "ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่")
### Multi-Tenant
RLS + `X-Tenant-Id` ตรงกับ JWT
### Audit Log
ทุก mutation → T_osw_audit (who/what/when/where/result) · read PDF/export → audit view (Confidential)

## §2.4 API → Logic Trace (Anchor for R8)
ดู 03 §3.3

## §2.X Cross-Module Contract (จาก BRD §12.1)
| ปลายทาง | ช่องทาง | Payload | Trigger | ยกเลิก/แก้กลางทาง |
|---|---|---|---|---|
| DOA engine (F-DLG-001) | call `doa.resolve` / `doa.submit` / `doa.decide` / `doa.cancel` + callback API-13 | `{type:'osw', osw_id, osw_no, requester, dept, mode, range_from, range_to}` (ไม่มียอดเงิน — DEC-03) | resolve: เปิด M-01 · submit: API-06 · decide: API-07/08 | cancel → `doa.cancel` · งานหายจาก My Approval |
| ENG-NOTIFY | event `osw_cancelled` | `{osw_id, osw_no, cancelled_by, reason, notify:[current_assignee]}` | API-09 ขณะ pending | — · (`doa_pending`/`doa_result` = ของ DOA engine ห้ามประกาศซ้ำ) |
| ENG-DOC-NUM | call `next('OSW', company_ctx)` | — | API-03 | เลขไม่คืน (immutable) |
| ENG-DOC-STORE | call `store(pdf,'OSW',osw_id,'approved_final')` | PDF bytes | approved | ยกเลิกหลังอนุญาต → สำเนาคงอยู่ + metadata status=cancelled |
| F-DOCCFG (F003) | call `status('OSW')` · `print_config('OSW')` | — | API-03 · API-12 · API-10 | — |
| Organization | read company header | — | API-03 (snapshot ตอนออกเลข) | ไม่ดึงสดหลังออกเลข |
| (อนาคต) F-ATTEND-001 / F-PAYROLL-001 | event `osw.approved` **ประกาศไว้ ยังไม่ยิง** (DEC-02) | `{osw_id, employee_id, lines[], mode, paid_nights, rate, per_diem_amount}` | approved | ต้องมี `osw.cancelled_after_approval` คู่เมื่อเปิดใช้ |

# 03_LOGIC — F-HR-OSW แบบขออนุญาตออกปฏิบัติงานนอกสถานที่

> Audience: BE dev (business logic layer) · ไม่มีคำ HTTP ในไฟล์นี้ · ID `F-OSW-FN-NN` / `F-OSW-ENG-NN` (global ENG id ออกตอน register CUBIC)
> prototype reference: function ชื่อเดียวกัน/ใกล้เคียงใน HTML (`validateMain`, `perDiem`, `maxNights`, `resolveDoa`, `confirmApprove`, `oswPdfData`, `tplRender`)

## §3.1 Functions (Scope-Local)

### F-OSW-FN-01: `buildOswList`
- **Purpose:** รายการตามตัวกรอง + scope การมองเห็น (BR-OSW-19) + stats
- **Input:** `{ actor, q, status, mode, orgUnitId, minePending, sort, dir, page, pageSize }`
- **Output:** `{ items[], total, stats{ all, pending, minePending } }`
- **Logic:** scope = `employee_id = actor` OR actor อยู่ใน `approval_chain[].assignee` OR actor มีสิทธิ์ HR · `minePending` = ขั้น `pending` ที่ assignee = actor · ค้นหาใน osw_no/employee_name/lines.purpose · `canView(actor, req)` ใช้ซ้ำใน API-02/10/11
- **Invoked by:** API-01, API-02 (canView), API-10 (canView), API-11 · **Side effects:** none

### F-OSW-FN-02: `snapshotRequester`
- **Purpose:** ดึงผู้ขอ/ตำแหน่ง/ฝ่าย/ผู้บังคับบัญชา/อัตรา/เวลาเริ่มต้น
- **Input:** `{ actor, mode:'preview'|'create' }` · **Output:** `{ employee{id,name,position}, orgUnit{id,name}, lineManager|null, rate, defaultTime, docTypeActive }`
- **Rules:** rate ไม่มี → `BR_PERDIEM_POLICY_MISSING` เฉพาะเมื่อ mode overnight (EC-18) · docTypeActive=false → `BR_DOCTYPE_INACTIVE` (BR-OSW-15)
- **Invoked by:** API-03, API-12 · **Calls:** F-EMP-001, F-ORG-001, ExpensePolicy, F-DOCCFG `status('OSW')` (read)

### F-OSW-FN-03: `validateOswDraft`
- **Purpose:** validation รวมศูนย์ VR-01..VR-11 (ฝั่ง server — ไม่พึ่ง UI)
- **Input:** `{ lines[], mode, nights, paidNights, today }` · **Output:** `{ errors:[{ lineNo?, code, field }], warnings:[{ code }] }`
- **Logic (ตาม HTML `validateMain`):**
  1. ต่อช่วง: วันที่ว่าง+เพื่อว่าง → `ERR_LINE_DATE_PURPOSE_REQUIRED` · วันที่ว่าง → `ERR_LINE_DATE_REQUIRED` · เพื่อว่าง → `ERR_LINE_PURPOSE_REQUIRED` · d_to < d_from → `ERR_LINE_DATE_ORDER` · เวลาว่าง → `ERR_LINE_TIME_REQUIRED` · วันเดียวและ t_to ≤ t_from → `ERR_LINE_TIME_ORDER`
  2. ทุกคู่ช่วง: ทับกัน (a.from ≤ b.to และ b.from ≤ a.to) → `ERR_LINE_OVERLAP` ที่ช่วงหลัง
  3. overnight: nights < 1 → `ERR_NIGHTS_MIN` · paidNights > nights → `ERR_PAID_EXCEEDS_NIGHTS`
  4. warnings: nights > maxNights → `WARN_NIGHTS_EXCEED_RANGE` · มี d_from < today → `WARN_BACKDATED`
- **Invoked by:** API-03, API-04, API-06

### F-OSW-FN-04: `computeNightsAndPerDiem`
- **Purpose:** วัน/คืน/เบี้ยเลี้ยง (pure)
- **Input:** `{ lines[], mode, nights, paidNights, nightsAuto, rate }` · **Output:** `{ linesDays[], totalDays, maxNights, nights, paidNights, perDiemAmount }`
- **Logic:** days = d_to − d_from + 1 · maxNights = Σ max(0, days − 1) · nightsAuto && overnight → nights = paidNights = maxNights · day → nights = paidNights = 0 · perDiem = overnight ? round2(paidNights × rate) : 0
- **Invoked by:** API-03, API-04 · **Note:** pure + สั้น → Function (ไม่ถึงเกณฑ์ Engine)

### F-OSW-FN-05: `createOswDraft`
- **Purpose:** สร้างใบร่าง + ออกเลข (+ทำซ้ำ)
- **Input:** `{ actor, payload, snapshot, calc, idempotencyKey }` · **Output:** `{ id, oswNo, version:1 }`
- **Logic:** transaction: `ENG-DOC-NUM.next('OSW', company_ctx)` → อ่านหัวกระดาษจาก Organization เก็บ `header_snapshot` (DOCCFG_BRIEF v1.1) → INSERT request (status draft, snapshot, rate, per_diem) + lines + attachments · copy_of ตามที่ส่ง (ทำซ้ำ: client ส่งช่วงที่มี purpose/เวลาเดิม วันที่ใหม่) · rollback ทั้งก้อนถ้าล้ม (PR-4)
- **Invoked by:** API-03 · **Calls:** ENG-DOC-NUM · FN-15

### F-OSW-FN-06: `updateOswDraft`
- **Purpose:** แก้ไขร่างของตัวเอง
- **Logic:** ตรวจ owner + status=draft (BR-OSW-13) + version → replace lines/attachments · audit `draft_updated` พร้อม diff · version+1
- **Invoked by:** API-04 · **Calls:** FN-15

### F-OSW-FN-07: `resolveApprovalPreview`
- **Purpose:** ขั้นอนุมัติ + ผู้พิจารณาเริ่มต้น สำหรับ M-01
- **Logic:** `DOA.resolve({type:'osw', requester, dept})` → steps[] · ต่อขั้น resolve role → คน (เช่น `role-line-manager` → ผู้บังคับบัญชาตรงจาก F-ORG-001) · ตัด requester ออกจากค่าเริ่มต้น (BR-OSW-11) · ไม่มีคน → null (EC-17)
- **Invoked by:** API-05 · **Calls:** DOA engine (existing)

### F-OSW-FN-08: `submitOsw`
- **Purpose:** ส่งขออนุญาต
- **Logic:** draft only · re-validate (FN-03) · assignees ครบ/ไม่ใช่ requester · snapshot `approval_chain` (BR-OSW-09 freeze) ขั้น 1 = pending ที่เหลือ waiting · `DOA.submit(...)` → doa_ref · status pending_approval · submitted_at
- **Invoked by:** API-06 · **Calls:** FN-03, DOA engine, FN-15

### F-OSW-FN-09: `decideOswStep`
- **Purpose:** อนุญาต/ไม่อนุญาตขั้นปัจจุบัน (sequential — BR-OSW-10)
- **Input:** `{ actor|callbackBy, decision, note, version }`
- **Logic:** current = ขั้น pending · actor ต้อง = assignee (ยกเว้นมาจาก callback ที่ DOA ตรวจแล้ว) · approve → current approved(at,note) → ถ้ามี waiting ถัดไป → pending (status คง pending_approval) · ไม่มี → status approved + approved_by/at → FN-13 · reject → current rejected(note บังคับ) · waiting ที่เหลือ → skipped · status rejected · `DOA.decide` เมื่อตัดสินจากหน้า feature
- **Invoked by:** API-07, API-08, FN-16 · **Calls:** DOA engine, FN-13, FN-15

### F-OSW-FN-10: `cancelOsw`
- **Purpose:** ยกเลิก (เจ้าของ/HR) จาก draft/pending/approved
- **Logic:** reason บังคับ · pending → `DOA.cancel(doa_ref)` + ขั้น pending/waiting → skipped + emit ENG-NOTIFY `osw_cancelled` ถึง assignee ปัจจุบัน · approved → ไม่ลบสำเนา PDF (update metadata cancelled) · status cancelled · `[AI-DEFAULT]` ยกเลิกได้แม้วันเดินทางผ่านแล้ว (OQ-09)
- **Invoked by:** API-09 · **Calls:** DOA engine, ENG-NOTIFY, ENG-DOC-STORE (metadata), FN-15

### F-OSW-FN-11: `buildOswPrintData`
- **Purpose:** สร้าง data contract ของแบบพิมพ์ (print-spec §2) — ตรงกับ `oswPdfData()` ใน prototype ทุก key
- **Output:** `{ company{name,logo}, doc{title,no,is_draft,form_code,revision}, req_date, to_name, employee{name,position,dept}, lines[≥5]{no,date,time_from,time_to,purpose}, mode{day_box,overnight_box}, per_diem{nights,paid_nights,rate,amount}, signs[]{role,name,position,date,decision|null}, layout{dense} }`
- **Logic:** อ่าน `print_config` จาก F-DOCCFG (form_code · revision · min_rows · sign_boxes) · `company.*` จาก `header_snapshot` · lines เติมแถวว่างให้ครบ min_rows (ค่าเริ่ม 5) · signs ตาม sign_boxes: requester + 1 ช่องต่อขั้นใน approval_chain (decision ☑/☐ · label/การแสดงวันที่ตาม config) · dense = lines > min_rows · วันที่เต็ม พ.ศ. · ไม่มีค่า → ช่องว่าง (ไม่ใช่ "null")
- **Invoked by:** API-10, FN-13

### F-OSW-FN-12: `renderOswPdf`
- **Purpose:** data → PDF
- **Logic:** `F-OSW-ENG-01.render('osw_body.tpl.html', data)` → body → wrap head/CSS/Sarabun (thai-doc base.css + FORM REPLICA patch) → PDF A4
- **Invoked by:** API-10, FN-13 · **Calls:** F-OSW-ENG-01

### F-OSW-FN-13: `storeApprovedPdf`
- **Purpose:** เก็บ PDF ฉบับอนุญาตครบ (BR-OSW-18)
- **Logic:** FN-11 → FN-12 → `ENG-DOC-STORE.store(pdf,'OSW',id,'approved_final')` → pdf_store_ref · ล้ม → retry queue (ไม่ rollback การอนุญาต) + alert
- **Invoked by:** FN-09 (ขั้นสุดท้าย)

### F-OSW-FN-14: `exportOswCsv`
- **Purpose:** CSV ตามตัวกรอง + audit export · **Invoked by:** API-11

### F-OSW-FN-15: `appendOswAudit`
- **Purpose:** INSERT T_osw_audit (append-only) · **Invoked by:** FN-05/06/08/09/10/14

### F-OSW-FN-16: `applyDoaCallback`
- **Purpose:** รับผลจาก My Approval (DOA กลาง)
- **Logic:** หา request ด้วย doa_ref · ไม่ pending หรือขั้นไม่ตรง → ignored (EC-31 แบบ F185) · ตรง → FN-09 ด้วย callbackBy
- **Invoked by:** API-13

## §3.2 Engines (Reusable / CUBIC-Registered)

### F-OSW-ENG-01: `doc-print-template-render` [NEW — CUBIC candidate]
- **code:** `doc-print-template-render` · **category:** document-rendering
- **input schema:** `{ templateRef, data }` · **output schema:** `{ bodyHtml }` (+ PDF ผ่าน renderer ของ platform)
- **logic outline:** logic-less subset — `{{a.b}}` escape · `{{{a.b}}}` raw (โลโก้เท่านั้น) · `{{#list}}…{{/list}}` loop/if · `{{^x}}…{{/x}}` if-not · context stack (ค่าในแถวก่อน แล้ว root)
- **Reference impl:** `print/render_osw.py` = `tplRender()` ใน HTML (ทดสอบแล้วตรงกันทุก byte · 2 ตัวอย่าง)
- **Used by features:** F-HR-OSW · (ผู้สมัคร) ทุกเอกสารที่ขึ้นแบบฟอร์มลูกค้าผ่าน thai-doc-pdf-generator
- **Iron rule check:** ✅ pure · ไม่มี HTTP · ไม่มี I/O

### Existing engines (เรียกใช้ ไม่สร้างใหม่)
| Engine | ใช้ทำ | เรียกจาก |
|---|---|---|
| DOA engine (F-DLG-001) | resolve · submit · decide · cancel · callback | FN-07/08/09/10/16 |
| ENG-DOC-NUM | เลขที่ | FN-05 |
| ENG-DOC-STORE | approved_final | FN-13 · FN-10 |
| ENG-NOTIFY | osw_cancelled | FN-10 |

## §3.3 API ↔ Logic Trace Table (R8 Anchor)
| API | Calls Functions | Calls Engines |
|---|---|---|
| API-01 GET /osw | FN-01 | — |
| API-02 GET /osw/{id} | FN-01 (canView) | — |
| API-03 POST /osw | FN-02, FN-03, FN-04, FN-05, FN-15 | ENG-DOC-NUM |
| API-04 PUT /osw/{id} | FN-03, FN-04, FN-06, FN-15 | — |
| API-05 GET approval-preview | FN-07 | DOA |
| API-06 POST submit | FN-03, FN-08, FN-15 | DOA |
| API-07 POST approve | FN-09, FN-13, FN-15 | DOA, ENG-DOC-STORE, F-OSW-ENG-01 |
| API-08 POST reject | FN-09, FN-15 | DOA |
| API-09 POST cancel | FN-10, FN-15 | DOA, ENG-NOTIFY, ENG-DOC-STORE |
| API-10 GET pdf | FN-01, FN-11, FN-12 | F-OSW-ENG-01, ENG-DOC-STORE (read) |
| API-11 GET export.csv | FN-01, FN-14, FN-15 | — |
| API-12 GET form-context | FN-02 | — |
| API-13 POST doa-callback | FN-16, FN-09, FN-13, FN-15 | — |

### Trace Verification (Self-Check)
- mutation API (03, 04, 06, 07, 08, 09, 13) → มี Function ทุกตัว ✅
- FN-01..FN-16 ถูกเรียกอย่างน้อย 1 ที่ ✅ · F-OSW-ENG-01 ผ่าน FN-12 ✅ · ไม่มี orphan ✅

## §3.4 Dependencies
### External Function/Engine called
DOA engine · ENG-DOC-NUM · ENG-DOC-STORE · ENG-NOTIFY · F-DOCCFG (status · print_config) · Organization · F-EMP-001 · F-ORG-001 · ExpensePolicy
### External that calls into this feature
DOA engine → API-13 (callback)

## §3.5 Open Questions / Locked Decisions Referenced
LD-01 (DOA sequential), LD-02 (เลขตอนร่าง), LD-03 (rate snapshot ตอนสร้าง), LD-04 (template logic-less) · OQ-03, OQ-09, OQ-10

## Audience Cheat-Sheet
BE เริ่ม: FN-02 → FN-03/04 → FN-05 → FN-08 → FN-09 → FN-11/12 · ทดสอบ FN-03/FN-04/ENG-01 แบบ unit ก่อน (pure)

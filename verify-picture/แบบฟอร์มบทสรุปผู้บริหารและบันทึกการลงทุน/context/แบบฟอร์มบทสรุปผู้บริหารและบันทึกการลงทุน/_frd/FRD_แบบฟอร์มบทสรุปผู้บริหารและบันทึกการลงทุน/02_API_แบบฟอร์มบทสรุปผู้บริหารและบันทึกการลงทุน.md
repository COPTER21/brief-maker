# 02_API — F-TMP-005
> base `/api/v1/investment-memos` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/investment-memos?q&status&cond_state&dept&mine_to_act&page&size&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/investment-memos/{id}` | รายละเอียด + conditions + chain + audit | FN-10 |
| API-03 | POST `/investment-memos` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-03 |
| API-04 | PUT `/investment-memos/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/investment-memos/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) + open_conditions | FN-04 |
| API-06 | POST `/investment-memos/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-04 |
| API-07 | POST `/investment-memos/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-05, FN-06 |
| API-08 | POST `/investment-memos/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-09 | GET `/investment-memos/{id}/pdf` | PDF FM-BDM-05 (2 หน้า) | FN-08 |
| API-10 | GET `/investment-memos/export.csv` | CSV ตามตัวกรอง | FN-10 |
| API-11 | POST/DELETE `/investment-memos/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ project_name, project_type, proposer_id, estimated_amount (decimal ≥ 0), decision_requested, project_summary, strategic_rationale, market_opportunity, business_model, implementation_plan, financial_analysis, investment_framework, key_risks, alternatives, pre_approval_conditions, bd_recommendation, next_steps, conditions:[{item, owner_id, due_date, status, remark}], attachment_ids[] }` · 422 ตาม VR-01..05 · server ตัดแถวว่างและรันลำดับ seq ใหม่ (FN-02)
- API-05/06 response มี `open_conditions` (จำนวนเงื่อนไขยังไม่แล้วเสร็จ — เตือน ไม่บล็อก)
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- response มี `open_conditions` · `conditions[].owner_name` · `conditions[].status` (label snapshot)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| DOA กลาง | GET /doa/resolve?feature_id=F-TMP-005&amount= | estimated_amount | ✓ (matrix เดียว · TODO: DOA engine ถ้าตั้งตามวงเงิน) |
| ENG-NOTIFY | ivm_cancelled · ivm_approved_open_conditions | {ref: investment_memo_id, vars} | ✓ |
| ENG-DOC-STORE | store(pdf,'IVM',id,'approved_final') | | ✓ |
| ระบบอื่น / งบลงทุน / โครงการต้นทาง | — | | ไม่ส่งต่อ (DEC-02) |

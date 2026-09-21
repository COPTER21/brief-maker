# 05_RULES — F084 Stocktake

## §5.1 Business Rules

| ID | Statement | Enforced by |
|---|---|---|
| BR-ST-01 | freeze ได้เฉพาะ draft, scope ไม่ทับ active lock, snapshot ว่าง | API-03/FN-03 |
| BR-ST-02 | snapshot qty/cost/watermark ถูกเก็บ atomically และ immutable | FN-04/DB |
| BR-ST-03 | counter DTO ห้ามมี system qty/cost/diff; zero valid, blank/negative invalid | API-05/projection |
| BR-ST-04 | `abs(diff)>threshold_version` ต้อง recount; equality ไม่ trigger | ENG-01 |
| BR-ST-05 | submit ได้เฉพาะ active assignee และ re-check ตอน mutation | FN-06 |
| BR-ST-06 | recount assignee ต้องต่างจาก first counter | FN-05 |
| BR-ST-07 | DOA basis=sum(abs(diff×cost snapshot)) | ENG-01/FN-09 |
| BR-ST-08 | DOA resolve+freeze ตอน submit; slot ต้องครบ/unique/not counters | FN-09 |
| BR-ST-09 | decision เฉพาะ current person/step; reject ต้องมี reason | FN-10 |
| BR-ST-10 | handoff หลัง approved ครั้งเดียว; close/release หลัง F082 draft ack | FN-11 |

## §5.2 State Machine

| From | Action | To | Role/Condition |
|---|---|---|---|
| draft | freeze | frozen | supervisor, no overlap |
| frozen | assign | counting | supervisor |
| counting | submit | recount | assigned counter + over threshold |
| counting | submit | review | assigned counter + within/equal threshold |
| recount | assign | recount | supervisor + independent person |
| recount | submit | review | assigned recount counter |
| review | submit approval | pending | supervisor + valid resolved slots |
| pending | approve intermediate | pending | current approver |
| pending | approve final | approved | current approver |
| pending | reject | rejected | current approver + reason; unlock |
| approved | F082 ack | closed | supervisor; unlock |

Transitions อื่นทั้งหมด 422 `BR_INVALID_STATE`

## §5.3 Permission Matrix

| Action | Counter | Recount counter | Supervisor | Current approver | Other supervisor |
|---|:---:|:---:|:---:|:---:|:---:|
| enter own count | allow assigned | allow assigned | deny | deny | deny |
| see snapshot/variance | deny | deny | allow | policy | policy |
| freeze/assign/submit DOA/handoff | deny | deny | allow | deny | allow by role+state |
| approve/reject | deny | deny | only if current | allow | deny if not current person |

## §5.4 Validation

- round name trimmed required; scope must resolve and contain ≥1 stock line
- counted quantity numeric ≥0 and every snapshot line present
- selected person must exist/active at mutation time
- approval slot count and role slots must equal DOA resolve result
- reject reason trimmed non-empty
- handoff lines use final accepted count and captured cost, never current inventory cost

## §5.5 Edge/Error Catalog

| Code | HTTP | Visible result |
|---|---:|---|
| ERR_REQUIRED_FIELD | 400 | กรุณาระบุชื่อรอบนับและพื้นที่นับ |
| ERR_SCOPE_OVERLAP | 409 | พื้นที่นี้ทับซ้อนกับรอบนับที่กำลังใช้งาน |
| ERR_SCOPE_EMPTY | 422 | ไม่พบสินค้าในพื้นที่นับ |
| ERR_NOT_ASSIGNED_COUNTER | 403 | ไม่ใช่ผู้ได้รับมอบหมายให้นับในขั้นนี้ |
| BR_COUNT_INCOMPLETE / NEGATIVE | 422 | กรุณากรอกผลนับทุกสินค้าเป็นศูนย์หรือมากกว่า |
| BR_RECOUNT_SAME_PERSON | 422 | ผู้นับซ้ำต้องเป็นคนละคนกับผู้นับครั้งแรก |
| BR_APPROVAL_SLOT_MISSING | 422 | กรุณาเลือกผู้อนุมัติทุกขั้น |
| BR_APPROVER_IS_COUNTER | 422 | ผู้อนุมัติต้องไม่ใช่ผู้นับ |
| BR_APPROVER_DUPLICATE | 422 | ผู้อนุมัติแต่ละขั้นต้องเป็นคนละคน |
| ERR_NOT_CURRENT_APPROVER | 403 | ไม่ใช่ผู้มีสิทธิ์ในขั้นนี้ |
| BR_REJECT_REASON_REQUIRED | 422 | กรุณาระบุเหตุผล |
| ERR_STALE_DATA | 409 | ข้อมูลเปลี่ยนแล้ว กรุณาโหลดใหม่ |
| ERR_HANDOFF_ALREADY_EXISTS | 409 | ต้องอนุมัติผลต่างก่อน และสร้างใบปรับได้ครั้งเดียว |
| ERR_F082_UNAVAILABLE | 502 | สร้างร่างใบปรับยอดไม่สำเร็จ รอบยังไม่ปิดและพื้นที่ยังล็อก |

## §5.6 `[AI-DEFAULT]` Technical Rules

Optimistic version on all state mutations; idempotency key 24h; atomic scope lock/snapshot; permission re-check; failed F082 call leaves approved/locked and permits safe retry with same key

## §5.7 Security / Data Classification

- Confidential fields excluded from counter projection and unauthorized export
- every view of variance and every mutation is audited
- role/session is revalidated at mutation time; demo selector never trusted
- tenant RLS and canonical scope prevent cross-company locks
- DOA chain and decisions are append-only snapshots

## §5.8 DOA

Apply BR-DOA-01..05: submit only review, freeze resolved chain, reject append-only, counters cannot approve, any recalculation before resubmit requires re-resolve. See `DOA_BRIEF_F-WH-STOCKTAKE.md`

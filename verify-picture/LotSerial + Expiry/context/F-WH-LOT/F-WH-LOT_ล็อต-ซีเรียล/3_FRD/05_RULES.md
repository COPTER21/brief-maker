# 05_RULES — F-WH-LOT

## §5.1 Business rules
| ID | Invariant/algorithm | Source | Error or outcome |
|---|---|---|---|
| BR-01 | Per-item tracking none/lot/serial; expiry requires active tracking | W4 §2 | INVALID_POLICY |
| BR-02 | Expiry date required iff item policy expiry_enabled | W4 §2 | EXPIRY_REQUIRED |
| BR-03 | Serial required in serial mode; unique tenant+item; qty=1 | [ASSUMED] Product Owner | SERIAL_REQUIRED/SERIAL_DUPLICATE |
| BR-04 | Available=max(0,on_hand-held)>0; expiry-enabled lots must be unexpired | W4 OQ/QHold + [ASSUMED] | excluded candidate |
| BR-05 | Expiry-enabled FEFO; non-expiry receipt order; deterministic tie-break | OQ-LOT-01 + [ASSUMED] tie | ranked result |
| BR-06 | Recommendation read-only; no stock/hold/reservation write | W4 scope | invariant |
| BR-07 | GRN/Transfer movement refs read-only mock | W4 dep | SOURCE_UNAVAILABLE or empty |
| BR-08 | Audit/movement append-only, no hard delete | Golden 4 | immutable event |
| BR-09 | Near-expiry threshold/channel centrally NC rule; no local numeric constant | Golden/W4 | NC soft hook |

## §5.2 Validation and errors
| Field/action | Guard | UI microcopy verbatim | API error |
|---|---|---|---|
| item picker | selected item exists in policy snapshot | “เลือกสินค้าจากรายการ” | ITEM_NOT_FOUND |
| mode none+expiry | invalid combination | “เปิดวันหมดอายุต้องติดตามล็อตหรือซีเรียล” | INVALID_POLICY |
| lot_code | required when tracking active | “กรอกรหัสล็อต” | LOT_REQUIRED |
| serial_code | required in serial mode, unique tenant+item | “กรอกซีเรียล” / “ซีเรียลนี้ถูกใช้แล้ว” | SERIAL_REQUIRED/SERIAL_DUPLICATE |
| expiry_date | required iff expiry_enabled | “กรอกวันหมดอายุ” | EXPIRY_REQUIRED |
| create replay | same key returns prior result | “รายการนี้ส่งแล้ว” | IDEMPOTENCY_CONFLICT only if key/payload mismatch |
| no eligible lots | zero candidates | “ไม่มีล็อตที่พร้อมใช้” | NO_ELIGIBLE_LOTS semantic empty, not HTTP 500 |
| no movements | zero refs | “ยังไม่มีการเคลื่อนไหวของล็อตนี้” | empty list |

## §5.3 Cross-module boundaries
W3-LITE movement/QHold availability adapters are mock/TODO, only payload/ref/empty/ack testable in this lane. Picking must revalidate at execution. NC/CSQ own event rule evaluation. No external feature is implemented here.

## §5.4 Concurrency/idempotency
Server transaction enforces partial unique serial index and stores idempotency key/result before response. Failed validation inserts no identity or audit. Policy update uses expected_version; conflict leaves previous version active. Prototype local guard is illustrative, not production concurrency proof.

## §5.5 Effective dates and reversal
Policy effective_date defaults to server tenant date [ASSUMED], no rewriting historical records. Upstream GRN/Transfer reversal appears as new movement ref; this feature cannot edit/delete it.

## §5.6 Result of CSQ (7C)
When successful policy change commits, emit `master.changed` envelope with tenant_id,item_code,tracking_mode,expiry_enabled,effective_date,idempotency_key per CSQ_BRIEF. ENG-CSQ evaluates consequence; feature stores no EC/AC/FC/DC/SC result. OC belongs to OP; document DC belongs to DOA; SC never declared. Reversal, if policy changed again, is a new event referencing prior event, not a deletion. Declaration is [ASSUMED] because skill contract reference is absent.

## §5.7 Data classification
### D-CLASS
All DB fields have Internal/Confidential + PII flags in 04_DB §4.2. CSQ/NC producers send minimal refs, mask Confidential before publication. Actor IDs are internal operational PII; Security owner reviews Restricted Resources classification before deployment. No default Public classification.

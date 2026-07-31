# 02_API — F-PR-001 ใบขอซื้อ (Purchase Requisition)

> **Audience:** Backend developer (HTTP layer)
> **Purpose:** API contracts — CUBIC API Entity format
> **🚨 Iron Rule:** ห้าม business logic >5 lines ที่นี่ — ย้ายไป 03_LOGIC §3.1
> **🚨 R8:** ทุก mutation API ต้องระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth |
|---|---|---|---|---|
| F-PR-API-01 | GET | /api/v1/purchase-requisitions | List PR + filters | required |
| F-PR-API-02 | POST | /api/v1/purchase-requisitions | Create draft PR | required (requester) |
| F-PR-API-03 | GET | /api/v1/purchase-requisitions/:id | Get detail | required |
| F-PR-API-04 | PUT | /api/v1/purchase-requisitions/:id | Update draft | required (requester, owner) |
| F-PR-API-05 | POST | /api/v1/purchase-requisitions/:id/submit | Submit (DOA + hard control) | required (requester) |
| F-PR-API-06 | POST | /api/v1/purchase-requisitions/:id/approve | Approve step | required (approver) |
| F-PR-API-07 | POST | /api/v1/purchase-requisitions/:id/reject | Reject | required (approver) |
| F-PR-API-08 | POST | /api/v1/purchase-requisitions/:id/cancel | Cancel | required (requester/approver) |
| F-PR-API-09 | POST | /api/v1/purchase-requisitions/:id/route | Set route (cp/po_direct) | required (buyer) |
| F-PR-API-10 | GET | /api/v1/purchase-requisitions/:id/pdf | Render PDF (A4) | required |

> Master lookups (budget-releases remaining / products / employees / branches / vendors) = upstream APIs ของ master features (ดู 00_OVERVIEW §0.5) — ไม่ owned โดย F-PR

---

## §2.2 Per-API Contract

### F-PR-API-01: GET /api/v1/purchase-requisitions
| Field | Value |
|---|---|
| method | GET · auth required · roles ทุก role (employee = own scope) |

**Request — Query params:** `status?` (draft/pending/approved/rejected/cancelled) · `type?` (สินค้า/บริการ) · `branch_id?` · `release_ref?` · `q?` (เลข/ผู้ขอ/สาขา) · `limit?` (default 20, max 100) · `offset?`
**Headers:** `X-Tenant-Id` (required)
**Response 200:** `{ data: PR[], total, limit, offset }` (PR row: id, pr_no, pr_date, requester, dept, branch_name, type, release_ref, status, grand_total, updated_at)
**Errors:** 400 ERR_INVALID_QUERY_PARAMS · 401 ERR_NOT_AUTHENTICATED · 403 ERR_INSUFFICIENT_ROLE
**Side effects:** — (read-only)
**Calls (Logic):** F-PR-FN-04 buildPrListQuery → 03_LOGIC §3.1

---

### F-PR-API-02: POST /api/v1/purchase-requisitions
| Field | Value |
|---|---|
| method | POST · auth required · roles requester |

**Headers:** `X-Tenant-Id` (required) · `Idempotency-Key` (required)
**Body:**
```json
{
  "pr_date": "2026-06-06",
  "need_date": "2026-06-13",
  "type": "สินค้า",
  "requester_id": "uuid",
  "dept": "Business & Development",
  "branch_id": "uuid",
  "release_ref": "BRT-20260502-0051",
  "vendor_id": null,
  "purpose": "จัดซื้อวัสดุสำนักงาน",
  "wht_enabled": false,
  "endbill_discount_mode": null,
  "endbill_discount_value": 0,
  "lines": [
    { "item_code": "PPR-A4", "qty": 20, "unit": "รีม", "unit_price": 115, "discount_pct": 0, "vat_mode": "add", "vat_pct": 7 }
  ]
}
```
**Validation (field-level ≤5 lines):** `branch_id` required uuid · `requester_id` required uuid · `need_date` ≥ `pr_date` · `lines` ≥ 1 · `release_ref` required **เมื่อ** Purchase Config.require_unlock_ref=true → complex gating ใน F-PR-FN-03
**Response 201:** `{ id, pr_no, status: "draft", subtotal, vat_total, grand_total, created_at }`
**Errors:** 400 ERR_VALIDATION_FAILED · 403 ERR_INSUFFICIENT_ROLE · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 BR_RELEASE_REF_REQUIRED (BR-PR-04)
**Preconditions:** branch active · release (ถ้ามี) active · products purchasable
**Side effects:** INSERT T_pr_header + T_pr_line · gen pr_no (Document Numbering) · INSERT T_audit_log
**Calls (Logic):** F-PR-FN-01 createPurchaseRequisition · F-PR-FN-03 validatePurchaseRequisition · ENG-DOC-AMT doc-amount-engine

---

### F-PR-API-03: GET /api/v1/purchase-requisitions/:id
**Response 200:** PR_Header + lines[] + attachments[] + approval_chain + branch(address) + budget(remaining snapshot)
**Errors:** 403 ERR_INSUFFICIENT_ROLE · 404 ERR_NOT_FOUND
**Calls (Logic):** F-PR-FN-04 (hydrate) — read-only

---

### F-PR-API-04: PUT /api/v1/purchase-requisitions/:id
| roles | requester (owner) · เฉพาะ status=draft/rejected |

**Headers:** `X-Tenant-Id` · `If-Match` (updated_at — optimistic lock, EC-04)
**Body:** เหมือน API-02 (partial allowed)
**Response 200:** updated PR (recalculated)
**Errors:** 403 · 404 · 409 ERR_STALE_DATA · 422 BR_PR_NOT_EDITABLE (status ≠ draft/rejected)
**Side effects:** UPDATE T_pr_header + replace T_pr_line · INSERT T_audit_log (diff)
**Calls (Logic):** F-PR-FN-02 updatePurchaseRequisition · F-PR-FN-03 validate · ENG-DOC-AMT

---

### F-PR-API-05: POST /api/v1/purchase-requisitions/:id/submit
| roles | requester (owner) · status=draft/rejected → pending |

**Headers:** `X-Tenant-Id` · `Idempotency-Key`
**Body:** `{}` (no payload — operates on saved draft)
**Response 200:** `{ id, status: "pending", approval_chain: [...] }`
**Errors:** 403 · 404 · 422 BR_OVER_BUDGET (BR-PR-05) · 422 BR_SOD_VIOLATION (BR-PR-09) · 422 BR_RELEASE_REF_REQUIRED · 422 BR_EMPTY_LINES
**Preconditions:** valid draft · Σ(PR active per release_ref) + this ≤ งบคงเหลือ · DOA resolver returns chain
**Side effects:** UPDATE status=pending, submitted_at · write approval_chain · notify approver · INSERT T_audit_log
**Calls (Logic):** F-PR-FN-06 submitPurchaseRequisition → (F-PR-FN-03 validate · ENG-BUDGET budget-availability-engine · ENG-DOA doa-resolver)

---

### F-PR-API-06: POST /api/v1/purchase-requisitions/:id/approve
| roles | approver (ตรงชั้นปัจจุบันใน chain) · status=pending |

**Headers:** `X-Tenant-Id` · `If-Match`
**Body:** `{ "comment": "..." }` (optional)
**Response 200:** `{ id, status: "pending" | "approved", current_step, chain_complete }`
**Errors:** 403 ERR_NOT_CURRENT_APPROVER · 404 · 409 ERR_STALE_DATA · 422 BR_INVALID_STATE
**Side effects:** advance approval_chain step · ถ้าครบ → status=approved, approved_at/by · **emit `procurement.pr_linked {releaseRef,docNo,amount,source}`** → Budget committed · notify · audit
**Calls (Logic):** F-PR-FN-07 approvePurchaseRequisition → (ENG-BUDGET commit) — R8 ✅

---

### F-PR-API-07: POST /api/v1/purchase-requisitions/:id/reject
| roles | approver · status=pending → rejected |

**Body:** `{ "reason": "..." }` (**required** — BR-PR-10)
**Response 200:** `{ id, status: "rejected" }`
**Errors:** 403 · 404 · 422 BR_REJECT_REASON_REQUIRED
**Side effects:** UPDATE status=rejected, reject_reason · notify requester · audit
**Calls (Logic):** F-PR-FN-08 rejectPurchaseRequisition

---

### F-PR-API-08: POST /api/v1/purchase-requisitions/:id/cancel
| roles | requester (status draft/pending) · approver (status approved) |

**Body:** `{ "reason": "..." }`
**Response 200:** `{ id, status: "cancelled" }`
**Errors:** 403 · 404 · 422 BR_CANCEL_NOT_ALLOWED
**Side effects:** UPDATE status=cancelled · ถ้า cancel หลัง approved → **reverse budget committed** (compensating) · audit
**Calls (Logic):** F-PR-FN-09 cancelPurchaseRequisition → (ENG-BUDGET reverse ถ้า approved)

---

### F-PR-API-09: POST /api/v1/purchase-requisitions/:id/route
| roles | buyer · status=approved |

**Body:** `{ "route": "cp" | "po_direct" }`
**Response 200:** `{ id, route }`
**Errors:** 403 · 404 · 422 BR_ROUTE_LOCKED (po_direct ตั้งแล้ว — BR-PR-07)
**Side effects:** UPDATE route · ถ้า po_direct → lock PR (CP อ้างไม่ได้) · audit
**Calls (Logic):** F-PR-FN-10 setRoute

---

### F-PR-API-10: GET /api/v1/purchase-requisitions/:id/pdf
**Response 200:** `application/pdf` (A4, Sarabun) — header(org+logo จาก Organization) + branch ship-to + lines + totals + baht text + signature slots (= N ชั้นจาก approval_chain)
**Errors:** 403 (Restricted amounts — ต้องผ่าน ACL) · 404
**Side effects:** audit (view/export Restricted — D-CLASS)
**Calls (Logic):** F-PR-FN-11 buildPrDocumentModel → render

---

## §2.3 Common Concerns
- **Idempotency:** mutation รับ `Idempotency-Key` (cache 24h; same key+body → cached; same key+diff body → 409)
- **Optimistic Locking:** PUT/approve/cancel ต้องมี `If-Match` (updated_at) → mismatch 409 ERR_STALE_DATA
- **Multi-Tenant:** ทุก endpoint ต้องมี `X-Tenant-Id` → RLS
- **Audit Log:** ทุก mutation → T_audit_log (actor/action/resource/diff/timestamp) middleware

---

## §2.4 API → Logic Trace (Anchor for R8)

> Authoritative: `03_LOGIC.md §3.3`

| API | Calls Functions | Calls Engines |
|---|---|---|
| F-PR-API-01 GET list | F-PR-FN-04 | — |
| F-PR-API-02 POST create | F-PR-FN-01, F-PR-FN-03 | ENG-DOC-AMT |
| F-PR-API-03 GET detail | F-PR-FN-04 | — |
| F-PR-API-04 PUT update | F-PR-FN-02, F-PR-FN-03 | ENG-DOC-AMT |
| F-PR-API-05 POST submit | F-PR-FN-06 | ENG-BUDGET, ENG-DOA |
| F-PR-API-06 POST approve | F-PR-FN-07 | ENG-BUDGET |
| F-PR-API-07 POST reject | F-PR-FN-08 | — |
| F-PR-API-08 POST cancel | F-PR-FN-09 | ENG-BUDGET |
| F-PR-API-09 POST route | F-PR-FN-10 | — |
| F-PR-API-10 GET pdf | F-PR-FN-11 | — |

> **R8 Check:** ทุก mutation row มี ≥ 1 entry ✅

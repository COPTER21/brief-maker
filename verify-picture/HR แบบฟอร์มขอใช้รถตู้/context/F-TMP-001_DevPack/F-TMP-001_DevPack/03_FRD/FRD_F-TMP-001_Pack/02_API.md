# 02_API — F-TMP-001 แบบฟอร์มขอใช้รถตู้

Base: `/api/hr/van-requests`

## 1. Endpoint
| # | Method · Path | ใช้ทำอะไร | สิทธิ์ |
|---|---|---|---|
| A1 | `GET /api/hr/van-requests` | ทะเบียน (q · status · trip_mode · division · page · sort) | ทุก role — กรองตาม §05 BR-VIS-01 |
| A2 | `GET /api/hr/van-requests/{id}` | รายละเอียดใบเดียว | ตาม BR-VIS-01 |
| A3 | `POST /api/hr/van-requests` | สร้างร่าง (ออกเลขที่ครั้งแรก) | ผู้ใช้ที่ login |
| A4 | `PUT /api/hr/van-requests/{id}` | แก้ไขร่างของตัวเอง | เจ้าของ · สถานะ `draft` |
| A5 | `POST /api/hr/van-requests/{id}/submit` | ส่งอนุมัติ (payload: `assignees[]` ต่อขั้น) | เจ้าของ · สถานะ `draft` |
| A6 | `POST /api/hr/van-requests/{id}/approve` | อนุมัติขั้นปัจจุบัน (payload: `note`) | ผู้พิจารณาขั้นปัจจุบัน |
| A7 | `POST /api/hr/van-requests/{id}/reject` | ไม่อนุมัติ (payload: `reason` **บังคับ**) | ผู้พิจารณาขั้นปัจจุบัน |
| A8 | `POST /api/hr/van-requests/{id}/cancel` | ยกเลิกเอกสาร (payload: `reason` **บังคับ**) | เจ้าของ หรือ admin role · สถานะ `draft`/`pending` |
| A9 | `GET /api/hr/van-requests/{id}/pdf` | แบบพิมพ์ PDF (render ฝั่ง server จาก template เดียวกับ prototype) | ตาม BR-VIS-01 |
| A10 | `GET /api/hr/van-requests/export` | ส่งออก CSV ตามตัวกรองเดียวกับ A1 | ตาม BR-VIS-01 |
| A11 | `POST /api/hr/van-requests/{id}/attachments` | แนบไฟล์ผ่าน Document Center | เจ้าของ · สถานะ `draft` |
| A12 | `GET /api/hr/van-requests/{id}/audit` | ประวัติ append-only | ตาม BR-VIS-01 |

## 2. Payload — A3 / A4
```json
{
  "use_date_from": "2026-10-15",
  "use_date_to": "2026-10-16",
  "trip_mode": "round_trip",
  "purpose": "ประชุมตรวจรับงานติดตั้งเครื่องจักรที่โรงงาน",
  "travelers": [ { "seq": 1, "name": "สมชาย ใจดี", "division": "ฝ่ายปฏิบัติการ" } ],
  "outbound": { "pickup_place": "สำนักงานใหญ่", "pickup_time": "07:00", "dropoff_place": "โรงงานลูกค้า", "dropoff_time": "09:30" },
  "return":   { "pickup_place": "โรงงานลูกค้า", "pickup_time": "16:30", "dropoff_place": "สำนักงานใหญ่", "dropoff_time": "19:00" }
}
```
- `total_days` **ไม่รับจาก client** — server คำนวณเสมอ (FN-02)
- ช่องผู้ขอ (ชื่อ · รหัสพนักงาน · ตำแหน่ง · ฝ่าย · แผนก) **ไม่รับจาก client** — server snapshot จาก Employee/OrgUnit (FN-01)
- เที่ยวที่ไม่ได้เลือกตาม `trip_mode` → server บังคับเป็นค่าว่าง (FN-03)

## 3. Response — A2 (ย่อ)
```json
{
  "id": "…", "doc_no": "VAN-2569-0007", "doc_date": "2026-10-07", "status": "pending",
  "requester": { "name": "…", "code": "…", "position": "…", "division": "…", "department": "…" },
  "use_date_from": "2026-10-15", "use_date_to": "2026-10-16", "total_days": 2,
  "trip_mode": "round_trip", "purpose": "…",
  "travelers": [ … ], "outbound": { … }, "return": { … },
  "approval_status": "pending_approval", "doa_entry_ref": "DOA-VAN-01", "doa_ref": "…",
  "approver_role": "role-line-manager",
  "approval_chain": [
    { "step": 1, "role_id": "role-line-manager", "role_label": "ผู้บังคับบัญชา", "assignee_id": "…", "decision": "pending", "reject_reason": null, "decided_at": null },
    { "step": 2, "role_id": "role-mgr-hr", "role_label": "ผู้จัดการฝ่ายทรัพยากรบุคคล", "assignee_id": "…", "decision": "waiting", "reject_reason": null, "decided_at": null }
  ],
  "attachments": [ … ], "header_snapshot": { "company_name": "…", "logo": "…" }
}
```

## 4. รหัสผลลัพธ์
| HTTP | code | เมื่อไหร่ |
|---|---|---|
| 400 | `VALIDATION_FAILED` | ช่องบังคับไม่ครบ / ถึงวันที่ก่อนวันที่เริ่ม / ไม่มีผู้เดินทาง |
| 403 | `NOT_OWNER` | แก้ไขร่างที่ไม่ใช่ของตัวเอง |
| 403 | `NOT_CURRENT_APPROVER` | กดอนุมัติ/ไม่อนุมัติทั้งที่ไม่ใช่ผู้พิจารณาขั้นปัจจุบัน |
| 403 | `SELF_APPROVAL_DENIED` | ผู้ขอกดอนุมัติใบตัวเอง (BR-DOA-04) |
| 404 | `NOT_FOUND` | ไม่มีสิทธิ์เห็นใบนั้น (คืน 404 แทน 403 เพื่อไม่เปิดเผยการมีอยู่ของใบ) |
| 409 | `INVALID_STATE` | ส่งอนุมัติใบที่ไม่ใช่ `draft` / ยกเลิกใบที่ `approved` |
| 409 | `DOCTYPE_INACTIVE` | doc_type `VAN` ยังไม่เปิดใช้ที่ F-DOCCFG |
| 422 | `REASON_REQUIRED` | ไม่อนุมัติ/ยกเลิกโดยไม่ใส่เหตุผล |

## 5. Event ที่ยิงออก
| event | เมื่อไหร่ | ปลายทาง |
|---|---|---|
| `van_cancelled` | ยกเลิกใบระหว่างสถานะ `pending` | ENG-NOTIFY → ผู้พิจารณาขั้นปัจจุบัน |
| `doa_pending` / `doa_result` / `doa_escalate` | DOA engine ยิงเอง | **feature ห้ามประกาศซ้ำ** |

> ไม่มี event ส่งต่อระบบอื่นเมื่ออนุมัติ (DEC-02) และไม่มีการเขียนค่าตั้งค่าใด ๆ (DEC-01)

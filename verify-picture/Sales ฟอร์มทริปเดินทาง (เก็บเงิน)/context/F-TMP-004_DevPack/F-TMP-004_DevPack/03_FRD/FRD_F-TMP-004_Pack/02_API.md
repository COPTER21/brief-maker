# 02_API — F-TMP-004 ใบเดินทาง : เขตการขาย General Trade

## 1. Endpoint
| # | Method · Path | ใช้เมื่อ | หมายเหตุ |
|---|---|---|---|
| A1 | `GET /sales/travel-sheets` | หน้าทะเบียน | filter: `q` · `status` · `territory` · `dept` · `mine_to_approve` · page/size · sort · กรองสิทธิ์ตาม §05 |
| A2 | `GET /sales/travel-sheets/{id}` | เปิด drawer ดู | 403 เมื่อไม่มีสิทธิ์เห็น |
| A3 | `POST /sales/travel-sheets` | บันทึกร่างครั้งแรก | ออกเลขที่ด้วย `ENG-DOC-NUM.next('TRV')` |
| A4 | `PUT /sales/travel-sheets/{id}` | แก้ไขร่าง | เฉพาะ `status = draft` และเป็นเจ้าของ |
| A5 | `POST /sales/travel-sheets/{id}/submit` | ส่งอนุมัติ | body = ผู้พิจารณาต่อขั้น |
| A6 | `POST /sales/travel-sheets/{id}/approve` | อนุมัติขั้นปัจจุบัน | |
| A7 | `POST /sales/travel-sheets/{id}/reject` | ไม่อนุมัติ → กลับเป็นร่าง (DEC-08) | เหตุผลบังคับ |
| A8 | `POST /sales/travel-sheets/{id}/cancel` | ยกเลิกเอกสาร | เหตุผลบังคับ · สถานะ draft/pending เท่านั้น |
| A9 | `GET /sales/travel-sheets/{id}/pdf` | ดาวน์โหลด/พิมพ์ | server render `form.tpl.html` + data contract เดียวกับ prototype |
| A10 | `GET /sales/travel-sheets/export.csv` | ส่งออก CSV (DEC-11) | หัวคอลัมน์ตามกระดาษ + รวมยอด 13 ช่อง |
| A11 | `POST /sales/travel-sheets/{id}/attachments` | แนบไฟล์ | ผ่าน Document Center · file_policy เดียวกัน |

## 2. Payload — A3 / A4
```json
{
  "to": "ฝ่ายขาย สำนักงานใหญ่",
  "cc": "ฝ่ายบัญชี",
  "territory": "เขต GT-01 ภาคกลาง",
  "sales_period": "ตุลาคม 2569",
  "lines": [
    { "seq": 1, "work_date": "2026-10-01", "market_from": "ตลาดกลางเขต A", "market_to": "ตลาดชุมชน C",
      "qty": 5, "billing_plan_count": 3, "billing_plan_amount": 12000.00,
      "billing_actual_count": 2, "billing_actual_amount": 10500.00,
      "cheque_plan_count": 2, "cheque_plan_amount": 9000.00,
      "cheque_actual_count": 1, "cheque_actual_amount": 8200.00,
      "sales_target_shop": 6, "sales_target_amount": 20000.00,
      "sales_actual_shop": 5, "sales_actual_amount": 18500.00,
      "work_province": "นครปฐม", "stay_province": "ราชบุรี" }
  ],
  "attachments": ["<document_center_file_id>"]
}
```
- `owner_name` · `owner_position` · `owner_department` **ไม่รับจาก client** — server snapshot จาก Employee ของผู้สร้าง
- `total_*` **ไม่รับจาก client** — server คำนวณจาก `lines` ทุกแถวเสมอ (DEC-04 · DEC-12)

## 3. Payload — A5 submit
```json
{ "approvers": [ { "step": 1, "assignee_id": "<employee_id>" }, { "step": 2, "assignee_id": "<employee_id>" } ] }
```
จำนวนขั้น = จำนวนขั้นที่ DOA กลาง resolve ให้ — **ห้าม fix จำนวนขั้นในโค้ด**

## 4. Response — A2 (ย่อ)
```json
{
  "id": "...", "doc_no": "TRV-2569-0007", "status": "pending", "returned": false,
  "req_date": "2026-10-01", "to": "...", "cc": "...", "territory": "...", "sales_period": "...",
  "owner": { "employee_id": "...", "name": "...", "position": "...", "department": "..." },
  "lines": [ ... ],
  "totals": { "total_qty": 0, "total_billing_plan_count": 0, "total_billing_plan_amount": 0, "total_billing_actual_count": 0,
              "total_billing_actual_amount": 0, "total_cheque_plan_count": 0, "total_cheque_plan_amount": 0,
              "total_cheque_actual_count": 0, "total_cheque_actual_amount": 0, "total_sales_target_shop": 0,
              "total_sales_target_amount": 0, "total_sales_actual_shop": 0, "total_sales_actual_amount": 0 },
  "approval_chain": [ { "step": 1, "role_id": "role-line-manager", "label": "ผู้อนุมัติ (ลำดับ 1)", "assignee_id": "...", "status": "pending", "at": null, "note": "" } ],
  "doa_ref": "DOA-TRV-01",
  "header_snapshot": { "company_name": "...", "company_logo": "...", "snapshot_at": "2026-10-01T09:15" },
  "attachments": [], "audit": [], "permissions": { "can_edit": false, "can_submit": false, "can_approve": true, "can_cancel": false }
}
```

## 5. รหัสผลลัพธ์
| รหัส | HTTP | ความหมาย |
|---|---|---|
| `OK` | 200/201 | สำเร็จ |
| `VALIDATION_FAILED` | 422 | ข้อมูลไม่ครบ/ผิดกติกา (ดู 05_RULES §2) |
| `NOT_OWNER` | 403 | ไม่ใช่เจ้าของร่าง — แก้ไข/ส่งไม่ได้ |
| `NOT_CURRENT_APPROVER` | 403 | ไม่ใช่ผู้พิจารณาขั้นปัจจุบัน |
| `NOT_FOUND` | 404 | ไม่พบใบ หรือไม่มีสิทธิ์เห็น (ไม่เปิดเผยว่ามีอยู่) |
| `INVALID_STATE` | 409 | สถานะไม่อนุญาตให้ทำรายการนี้ |
| `STALE` | 409 | ข้อมูลถูกแก้โดยผู้อื่น |
| `DOCTYPE_INACTIVE` | 409 | doc_type `TRV` ยังไม่เปิดใช้ที่ F-DOCCFG |
| `REASON_REQUIRED` | 422 | ไม่อนุมัติ/ยกเลิก โดยไม่ระบุเหตุผล |

## 6. Event ที่ยิงออก
| Event | เมื่อ | เจ้าของ |
|---|---|---|
| `trv_cancelled` | `pending → cancelled` (A8) | feature นี้ → ENG-NOTIFY (ดู `NTF_BRIEF_F-TMP-004.md`) |
| `doa_pending` · `doa_result` · `doa_escalate` | ตามสาย DOA | **DOA engine ยิงเอง — feature ห้ามประกาศซ้ำ** |
- DEC-01 / DEC-02: อนุมัติครบแล้ว **ไม่** เรียก API เปลี่ยนค่าในระบบ และ **ไม่** ส่งข้อมูลต่อระบบอื่น

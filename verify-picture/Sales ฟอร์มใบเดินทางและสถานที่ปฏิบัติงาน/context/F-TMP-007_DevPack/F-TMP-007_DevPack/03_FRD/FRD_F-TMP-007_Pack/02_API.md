# 02_API — F-TMP-007 ใบเดินทางและสถานที่ปฎิบัติงาน  สำหรับ General Trade

## 1. Endpoint
| # | Method · Path | ใช้เมื่อ | หมายเหตุ |
|---|---|---|---|
| A1 | `GET /sales/travel-workplace-sheets` | หน้าทะเบียน | filter: `q` · `status` · `sales_period` · `dept` · `mine_to_approve` · page/size · sort · กรองสิทธิ์ตาม §05 |
| A2 | `GET /sales/travel-workplace-sheets/{id}` | เปิด drawer ดู | 403/404 เมื่อไม่มีสิทธิ์เห็น |
| A3 | `POST /sales/travel-workplace-sheets` | บันทึกร่างครั้งแรก | ออกเลขที่ด้วย `ENG-DOC-NUM.next('TWP')` |
| A4 | `PUT /sales/travel-workplace-sheets/{id}` | แก้ไขร่าง | เฉพาะ `status = draft` และเป็นเจ้าของ |
| A5 | `POST /sales/travel-workplace-sheets/{id}/submit` | ส่งอนุมัติ | body = ผู้พิจารณาต่อขั้น |
| A6 | `POST /sales/travel-workplace-sheets/{id}/approve` | อนุมัติขั้นปัจจุบัน | |
| A7 | `POST /sales/travel-workplace-sheets/{id}/reject` | ไม่อนุมัติ → กลับเป็นร่าง (DEC-09) | เหตุผลบังคับ |
| A8 | `POST /sales/travel-workplace-sheets/{id}/cancel` | ยกเลิกเอกสาร | เหตุผลบังคับ · สถานะ draft/pending เท่านั้น · ยิง `twp_cancelled` |
| A9 | `GET /sales/travel-workplace-sheets/{id}/pdf` | ดาวน์โหลด/พิมพ์ | server render `form.tpl.html` + data contract เดียวกับ prototype |
| A10 | `GET /sales/travel-workplace-sheets/export.csv` | ส่งออก CSV (DEC-12) | หัวคอลัมน์ตามกระดาษ + รวมยอด + สรุปท้ายใบ |
| A11 | `POST /sales/travel-workplace-sheets/{id}/files` | แนบไฟล์ | ผ่าน Document Center · file_policy เดียวกัน |

## 2. Payload — A3 / A4
```json
{
  "to": "ผู้จัดการฝ่ายขาย สำนักงานใหญ่",
  "to_line2": "ฝ่ายบัญชีและการเงิน",
  "from_phone": "0X-XXX-XXXX",
  "sales_period": "10/2569",
  "phone_cost": 350.00,
  "advance_received": 15000.00,
  "remark": "เดินทางตามแผนรอบการขาย",
  "cc": "ฝ่ายบัญชี",
  "lines": [
    { "seq": 1, "work_day_name": "จันทร์", "work_date": "2026-10-01",
      "route_from": "ตลาดกลางเขต A", "route_mid": "ตลาดชุมชน B", "route_to": "ตลาดสดเขต C",
      "stay_place": "โรงแรมตัวอย่าง 1",
      "cost_lodging": 300.00, "cost_hotel": 0.00, "cost_perdiem": 250.00, "cost_laundry": 50.00,
      "cost_fee": 20.00, "cost_post": 15.00, "cost_parking": 40.00, "cost_other": 30.00,
      "remark": "เยี่ยมร้านค้าตามแผน",
      "odometer_start": 52000, "odometer_end": 52150, "fuel_liter": 18, "fuel_amount": 650.00 }
  ],
  "attachment_lines": [ { "seq": 1, "title": "ใบเสร็จค่าที่พัก" }, { "seq": 2, "title": "ใบเสร็จค่าน้ำมัน" } ],
  "files": ["<document_center_file_id>"]
}
```
- `from_name` · `from_position` · `from_department` · `doc_date` **ไม่รับจาก client** — server snapshot จาก Employee ของผู้สร้าง
- `line_total` · `total_*` · `grand_total` · `balance` **ไม่รับจาก client** — server คำนวณจาก `lines` ทุกแถวเสมอ (DEC-04 · DEC-13 · DEC-14)

## 3. Payload — A5 submit
```json
{ "approvers": [ { "step": 1, "assignee_id": "<employee_id>" } ] }
```
จำนวนขั้น = จำนวนขั้นที่ DOA กลาง resolve ให้ — **ห้าม fix จำนวนขั้นในโค้ด**

## 4. Response — A2 (ย่อ)
```json
{
  "id": "...", "doc_no": "TWP-2569-0007", "status": "pending", "returned": false,
  "doc_date": "2026-10-01", "to": "...", "to_line2": "...", "sales_period": "10/2569",
  "from": { "employee_id": "...", "name": "...", "position": "...", "department": "...", "phone": "..." },
  "lines": [ ... ],
  "totals": { "total_lodging": 0, "total_hotel": 0, "total_perdiem": 0, "total_laundry": 0, "total_fee": 0,
              "total_post": 0, "total_parking": 0, "total_other": 0, "total_claim": 0,
              "total_fuel_liter": 0, "total_fuel_amount": 0 },
  "summary": { "phone_cost": 0, "grand_total": 0, "advance_received": 0, "balance": 0 },
  "remark": "...", "cc": "...",
  "attachment_lines": [ { "seq": 1, "title": "..." } ],
  "approval_chain": [ { "step": 1, "role_id": "role-line-manager", "label": "ผู้อนุมัติ", "assignee_id": "...", "status": "pending", "at": null, "note": "" } ],
  "doa_ref": "DOA-TWP-01",
  "header_snapshot": { "company_name": "...", "company_logo": "...", "snapshot_at": "2026-10-01T09:15" },
  "files": [], "audit": [], "permissions": { "can_edit": false, "can_submit": false, "can_approve": true, "can_cancel": false }
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
| `DOCTYPE_INACTIVE` | 409 | doc_type `TWP` ยังไม่เปิดใช้ที่ F-DOCCFG |
| `REASON_REQUIRED` | 422 | ไม่อนุมัติ/ยกเลิก โดยไม่ระบุเหตุผล |

## 6. Event ที่ยิงออก
| Event | เมื่อ | เจ้าของ |
|---|---|---|
| `twp_cancelled` | `pending → cancelled` (A8 · FN-11) | feature นี้ → ENG-NOTIFY (ดู `NTF_BRIEF_F-TMP-007.md`) |
| `doa_pending` · `doa_result` · `doa_escalate` | ตามสาย DOA | **DOA engine ยิงเอง — feature ห้ามประกาศซ้ำ** |
- DEC-01 / DEC-02: อนุมัติครบแล้ว **ไม่** เรียก API เปลี่ยนค่าในระบบ และ **ไม่** ส่งข้อมูลต่อระบบอื่น (การตั้งหนี้/คืนเงินสำรองทำนอกใบนี้)

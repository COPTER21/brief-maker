# 02_API — F-TMP-006 หนังสือสัญญายืม (LOA)

> base: `/sales/loan-agreements` · ตรวจสิทธิ์ที่ server ทุก endpoint (UI ซ่อนปุ่มเป็นชั้นแรกเท่านั้น)

## 1. Endpoint
| # | Method · Path | ใช้ทำอะไร | สิทธิ์ | FN |
|---|---|---|---|---|
| A1 | `GET /sales/loan-agreements` | ทะเบียน (ค้นหา · กรอง · เรียง · แบ่งหน้า) | ตาม 05 §4 | FN-10 |
| A2 | `GET /sales/loan-agreements/{id}` | ดูเอกสาร 1 ใบ | ตาม 05 §4 | FN-10 |
| A3 | `POST /sales/loan-agreements` | สร้างร่าง + ออกเลขครั้งแรก | พนักงานขาย | FN-01 · FN-04 |
| A4 | `PUT /sales/loan-agreements/{id}` | แก้ร่างของตัวเอง | เจ้าของ + สถานะ `draft` | FN-02 |
| A5 | `POST /sales/loan-agreements/{id}/submit` | ส่งให้ผู้ส่งมอบลงนาม | เจ้าของ + สถานะ `draft` | FN-05 · FN-06 |
| A6 | `POST /sales/loan-agreements/{id}/sign` | ลงนาม (ขั้นปัจจุบัน) | ผู้ถึงคิว | FN-07 |
| A7 | `POST /sales/loan-agreements/{id}/return` | ส่งกลับแก้ไข (ยังไม่ลงนาม) | ผู้ถึงคิว | FN-08 |
| A8 | `POST /sales/loan-agreements/{id}/cancel` | ยกเลิกเอกสาร | เจ้าของ หรือ admin role | FN-09 |
| A9 | `GET /sales/loan-agreements/{id}/pdf?copy=original\|copy` | แบบพิมพ์ 1 ชุด (ไม่ส่ง `copy` = ออกทั้ง 2 ชุด) | ตาม 05 §4 | FN-11 |
| A10 | `POST /sales/loan-agreements/{id}/attachments` | แนบไฟล์ | เจ้าของ หรือ admin role | FN-12 |
| A11 | `GET /sales/loan-agreements/export.csv` | ส่งออก CSV ตามตัวกรองปัจจุบัน | ตาม 05 §4 | FN-10 |

## 2. Payload — สร้าง / แก้ไข (A3 · A4)
```json
{
  "customer_code": "C-00012",
  "customer_address": "99/9 หมู่ 5 ถนนตัวอย่าง …",
  "doc_date": "2026-10-07",
  "receiver_name": "สุชาติ ทดสอบระบบ",
  "receiver_position": "ผู้จัดการร้าน",
  "damage_exception": "งานตามปกติ",
  "lines": [ { "seq": 1, "detail": "กล่องบรรจุกระดาษ ขนาด 40 x 30 x 30 ซม. จำนวน 50 ใบ" } ]
}
```
- `customer_name` ไม่รับจาก client — server อ่านจาก `Customer` ตาม `customer_code` แล้ว snapshot
- `free_replace_pct` ไม่รับจาก client — server อ่านจาก `SalesPolicy.box_free_replace_pct` แล้ว snapshot ตอนออกเลข (DEC-04)
- ถ้อยคำเงื่อนไขข้อ 1 และ 2 ไม่รับจาก client — เป็นข้อความคงที่ของแบบพิมพ์ (DEC-06)

## 3. Payload — ส่งให้ลงนาม (A5)
```json
{ "approvers": [ { "step": 1, "assignee_id": "E02" } ] }
```
จำนวนขั้นมาจาก `GET /doa/resolve?feature_id=F-TMP-006` — **ห้าม fix จำนวนขั้นที่ client หรือ server ของ feature นี้**

## 4. Payload — ลงนาม / ส่งกลับแก้ไข / ยกเลิก
```json
{ "note": "ไม่บังคับ" }                         // A6 ลงนาม
{ "reason": "รายละเอียดกล่องไม่ครบ …" }          // A7 ส่งกลับแก้ไข (บังคับ)
{ "reason": "ลูกค้ายกเลิกการขอยืม" }             // A8 ยกเลิก (บังคับ)
```

## 5. รหัสผลลัพธ์
| HTTP | เมื่อไร | ข้อความที่ UI แสดง |
|---|---|---|
| 200 / 201 | สำเร็จ | — |
| 400 | ข้อมูลไม่ครบตาม 05 §2 | ตามช่องที่ผิด |
| 403 | ไม่มีสิทธิ์ (รวมผู้จัดทำพยายามลงนามใบตัวเอง — BR-DOA-04) | คุณไม่มีสิทธิ์ทำรายการนี้ |
| 404 | ไม่พบเอกสาร หรือไม่มีสิทธิ์เห็น | — |
| 409 | เอกสารถูกแก้โดยผู้อื่น หรือสถานะเปลี่ยนไปแล้ว | ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่ |
| 422 | แบบเอกสารยังไม่เปิดใช้ที่ F-DOCCFG | แบบเอกสารนี้ยังไม่เปิดใช้งาน |
| 500 | ระบบขัดข้อง | ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง |

## 6. Event ที่ยิง
| Event | ยิงที่ | เจ้าของ | หมายเหตุ |
|---|---|---|---|
| `doa_pending` · `doa_result` · `doa_escalate` | A5 · A6 · A7 | **DOA engine** | feature ไม่ประกาศซ้ำ (N2 ของ ntf-declaration) |
| `loa_cancelled` | A8 เมื่อสถานะเดิมเป็น `pending` | feature | ผู้รับ = ผู้พิจารณาขั้นปัจจุบัน |
| `loa_signed_copy_attached` | A10 เมื่อสถานะเป็น `approved` | feature | ผู้รับ = ผู้จัดทำ + `role-mgr-sales` |

> **ไม่มี event หรือ API ใดที่ไปเปลี่ยนค่าตั้งต้นในระบบ หรือส่งข้อมูลต่อระบบอื่นเมื่อลงนามครบ** (DEC-01 · DEC-02)

## 7. Engine ที่เรียก
| Engine | เรียกที่ | ทำอะไร |
|---|---|---|
| `ENG-DOC-NUM.next('LOA')` | A3 (บันทึกครั้งแรก) | ออกเลขที่เอกสารและเลขที่บนแบบพิมพ์ (DEC-10) |
| `ENG-DOC-STORE.store()` | A6 (ลงนามครบ) และ A9 (ส่งออกนอกองค์กร) | เก็บสำเนา PDF ตาม snapshot flag ของ F-DOCCFG |
| `ENG-NOTIFY.emit()` | A8 · A10 | ยิง event ตาม §6 — ห้ามเช็ค preference เองในฝั่ง feature |
| `GET /doa/resolve` | A5 | คืนจำนวนขั้นและ role ปัจจุบันจาก DOA กลาง |

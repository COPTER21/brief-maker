# 02 API — F-TMP-010

> prefix `/media-consent` · ทุก endpoint ตรวจสิทธิ์ตาม 05 §BR-SEC · ตอบ 403 เมื่อไม่มีสิทธิ์ · 409 เมื่อข้อมูลถูกแก้โดยผู้อื่น

| # | Method | Path | ใช้ทำอะไร | FN |
|---|---|---|---|---|
| A-01 | GET | `/media-consent` | รายการ + ค้นหา + ตัวกรอง + แบ่งหน้า | FN-01 |
| A-02 | GET | `/media-consent/export.csv` | ส่งออก CSV (ไม่มีคอลัมน์เลขบัตรประชาชน) | FN-01 |
| A-03 | GET | `/media-consent/{id}` | รายละเอียดใบ (ตรวจการมองเห็น) | FN-11 |
| A-04 | POST | `/media-consent` | สร้างร่าง → ออกเลขที่ครั้งแรก | FN-02 · FN-03 |
| A-05 | PUT | `/media-consent/{id}` | แก้ร่าง (เฉพาะเจ้าของ · สถานะ draft) | FN-02 |
| A-06 | POST | `/media-consent/{id}/confirm` | ยืนยันความยินยอม → `confirmed` / `pending` | FN-06 |
| A-07 | POST | `/media-consent/{id}/approve` | ขั้น DOA รับหนังสือ | FN-07 |
| A-08 | POST | `/media-consent/{id}/reject` | ขั้น DOA ไม่รับหนังสือ (เหตุผลบังคับ) | FN-07 |
| A-09 | POST | `/media-consent/{id}/withdraw` | ถอนความยินยอม (scope + เหตุผลบังคับ) | FN-08 |
| A-10 | POST | `/media-consent/{id}/cancel` | ยกเลิกเอกสาร (เหตุผลบังคับ) | FN-09 |
| A-11 | GET | `/media-consent/{id}/pdf` | แบบพิมพ์ Replica (render ฝั่ง server จาก `form.tpl.html`) | FN-10 |
| A-12 | POST | `/media-consent/{id}/attachments` | แนบไฟล์ผ่าน Document Center | FN-12 |

## Payload — A-04 / A-05
```json
{
  "written_place": "ลานโปรโมชัน ชั้น 1 ศูนย์การค้าตัวอย่าง",
  "data_subject_name": "ชื่อ-นามสกุลผู้ให้ความยินยอม",
  "data_subject_age": 34,
  "data_subject_citizen_id": "<เลขบัตรประชาชน>",
  "booth_location": "บูธกิจกรรม A1 ศูนย์การค้าตัวอย่าง",
  "activity_date_from": "2026-10-10",
  "activity_date_to": "2026-10-12",
  "guardian_name": "", "guardian_age": null, "guardian_citizen_id": "",
  "minor_name": "", "minor_age": null, "minor_citizen_id": "",
  "lines": [ { "no": 1, "choice": "consent" }, { "no": 2, "choice": "consent" }, { "no": 3, "choice": "withdraw" } ]
}
```
- `data_subject_name_printed` และ `guardian_name_printed` เป็นค่า computed ฝั่ง server (ไม่รับจาก client)
- `written_date` / `signed_date` ระบบใส่ตอนยืนยัน (DEC-14)

## Payload — A-09 withdraw
```json
{ "scope": [3], "reason": "ผู้ให้ความยินยอมแจ้งถอนด้วยตนเอง" }
```
`scope` ว่าง = ถอนทั้งฉบับ · `reason` บังคับ

## Event ที่ยิง (ENG-NOTIFY · ntf-declaration)
| Event | ยิงที่ | FN |
|---|---|---|
| `imc_consent_recorded` | A-06 สำเร็จ และใบเป็น `confirmed` | FN-06 |
| `imc_minor_consent_recorded` | A-06 สำเร็จ และผู้ให้ความยินยอมเป็นผู้เยาว์ | FN-06 |
| `imc_consent_withdrawn` | A-09 สำเร็จ (ปิดไม่ได้) | FN-08 |
| `imc_cancelled` | A-10 สำเร็จ | FN-09 |
- event ของสายอนุมัติ (`doa_*`) เป็นของ DOA engine — feature ไม่ยิงเอง

## รหัสข้อผิดพลาด
| รหัส | ความหมาย |
|---|---|
| `NOT_OWNER` | แก้/ยกเลิกใบที่ไม่ใช่ของตน |
| `NOT_CURRENT_APPROVER` | ไม่ใช่ผู้พิจารณาขั้นปัจจุบัน |
| `IMMUTABLE` | ใบที่ยืนยันแล้วแก้ไขไม่ได้ |
| `CONSENT_INCOMPLETE` | ยังเลือกความยินยอมไม่ครบทุกข้อ |
| `GUARDIAN_REQUIRED` | ผู้เยาว์แต่ไม่มีผู้ปกครองรับรอง |
| `DATE_RANGE_INVALID` | วันสิ้นสุดก่อนวันเริ่มกิจกรรม |
| `DOC_TYPE_DISABLED` | แบบเอกสาร IMC ปิดใช้งานที่ F-DOCCFG |

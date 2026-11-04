# 02_API — F-TMP-008

## §2.1 API Overview
| Method | Path | ใช้ทำอะไร | Logic |
|---|---|---|---|
| GET | `/pdpa-consent` | รายการที่ผู้ใช้มีสิทธิ์เห็น (ค้นหา/ตัวกรอง/แบ่งหน้า) | FN-10 |
| GET | `/pdpa-consent/{id}` | รายละเอียด 1 ฉบับ | FN-10 |
| POST | `/pdpa-consent` | สร้างร่าง + ออกเลขที่ครั้งแรก | FN-01 · FN-03 |
| PUT | `/pdpa-consent/{id}` | แก้ไขร่างของตัวเอง | FN-01 |
| POST | `/pdpa-consent/{id}/confirm` | ยืนยันความยินยอม (บันทึกวันที่ + snapshot ฉบับ + เก็บสำเนา) | FN-02 · FN-04 · FN-08 · FN-09 |
| POST | `/pdpa-consent/{id}/decide` | พิจารณาตามขั้น DOA (เมื่อมีขั้น) | FN-05 |
| POST | `/pdpa-consent/{id}/withdraw` | ถอนความยินยอม (ทั้งฉบับ/รายข้อ) | FN-06 · FN-09 |
| POST | `/pdpa-consent/{id}/cancel` | ยกเลิกเอกสารที่ยังไม่มีผล | FN-07 |
| GET | `/pdpa-consent/{id}/pdf` | แบบพิมพ์ A4 (render จาก template เดียวกับ FE) | FN-08 |
| GET | `/pdpa-consent/export` | ส่งออก CSV ตามตัวกรองปัจจุบัน | FN-10 |

## §2.2 Contract สำคัญ
```jsonc
// POST /pdpa-consent  (สร้างร่าง)
{ "data_subject_name": "…", "lines": [ { "item_no": 1, "choice": "consent|refuse|" } ], "attachments": ["file-id"] }
// → 201 { "id", "doc_no", "form_code", "form_revision", "status": "draft" }

// POST /pdpa-consent/{id}/confirm
{} // → 200 { "status": "confirmed|pending", "consented_at", "form_revision", "stored_copy_id" }
//   409 CONSENT_INCOMPLETE เมื่อยังเลือกไม่ครบ · 403 NOT_OWNER เมื่อผู้เรียกไม่ใช่เจ้าของข้อมูล

// POST /pdpa-consent/{id}/withdraw
{ "scope": [4, 6], "reason": "…" }   // scope ว่าง = ทั้งฉบับ
// → 200 { "status": "withdrawn", "withdrawn_at", "withdrawn_by" } · 422 REASON_REQUIRED
```

## §2.3 Common
- ตอบ error ตาม Error Catalog (05_RULES §5.6) · ทุก mutation ต้องมี `If-Match`/version กัน lost update (409 STALE)
- สิทธิ์ตรวจที่ server ทุกครั้ง ไม่เชื่อ FE

## §2.4 API → Logic Trace
| API | FN |
|---|---|
| POST `/pdpa-consent` | FN-01 validateConsent · FN-03 issueNumber |
| POST `/{id}/confirm` | FN-02 lockConsentSnapshot · FN-04 resolveAndSubmit · FN-08 docPrintData+renderPdf · FN-09 emitEvents |
| POST `/{id}/decide` | FN-05 decideStep |
| POST `/{id}/withdraw` | FN-06 withdrawConsent · FN-09 emitEvents |
| POST `/{id}/cancel` | FN-07 cancelConsent |
| GET `/{id}/pdf` | FN-08 |
| GET `/pdpa-consent`, `/export` | FN-10 listVisible |

## §2.X Cross-Module Contract
| ปลายทาง | สัญญา | รอบนี้ |
|---|---|---|
| Policy Center › PDPA | `GET /pdpa-consent?subject={person_id}&active=true` คืนรายการข้อที่ความยินยอมยังมีผล | เปิดอ่านได้ |
| HR › Recruit / Onboard / Attendance | ใช้ contract เดียวกันตรวจก่อนประมวลผลข้อมูลอ่อนไหว | **ยังไม่ผูก (DEC-02)** — ประกาศไว้เพื่อรอบถัดไป |

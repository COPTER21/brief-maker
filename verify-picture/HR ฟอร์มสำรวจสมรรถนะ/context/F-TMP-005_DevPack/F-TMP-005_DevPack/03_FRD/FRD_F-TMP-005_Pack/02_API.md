# FRD 02 · API — F-TMP-005 แบบฟอร์มสำรวจสมรรถนะ

base: `/api/hr/competency-survey`

| # | Method · Path | ใช้เมื่อ | หมายเหตุ |
|---|---|---|---|
| A1 | `GET /` | หน้ารายการ | query: `q · status · development_plan · division · page · size` · กรองตามสิทธิ์ (DEC-10) ที่ชั้น service เสมอ |
| A2 | `GET /{id}` | เปิดลิ้นชัก | 403 `NOT_VISIBLE` ถ้าไม่เข้าเกณฑ์การมองเห็น |
| A3 | `POST /` | บันทึกร่างครั้งแรก | เรียก FN-01 → ออกเลขที่ด้วย ENG-DOC-NUM (DEC-11) |
| A4 | `PUT /{id}` | แก้ร่าง | 409 `NOT_DRAFT` ถ้าไม่ใช่ร่าง · 403 `NOT_OWNER` ถ้าไม่ใช่เจ้าของ |
| A5 | `POST /{id}/submit` | ส่งอนุมัติ | body `{ approvers: [emp_id] }` ตามจำนวนขั้นที่ DOA resolve · FN-03 |
| A6 | `POST /{id}/approve` | เห็นชอบขั้นปัจจุบัน | body `{ note? }` · 403 `NOT_CURRENT_APPROVER` · FN-04 |
| A7 | `POST /{id}/reject` | ส่งกลับแก้ไข | body `{ reason }` (บังคับ) · FN-05 → กลับเป็นร่างเลขเดิม |
| A8 | `POST /{id}/cancel` | ยกเลิกเอกสาร | body `{ reason }` (บังคับ) · เฉพาะ draft/pending โดยเจ้าของ/admin role · FN-06 (ยิง `cmp_cancelled`) |
| A9 | `GET /{id}/pdf` | ดาวน์โหลด/พิมพ์ | render ฝั่ง server จาก `form.tpl.html` + `docPrintData` · FN-07 (ENG-DOC-STORE) |
| A10 | `GET /export.csv` | ส่งออก CSV (DEC-12) | ใช้ filter ชุดเดียวกับ A1 |
| A11 | `POST /{id}/attachments` · `DELETE /{id}/attachments/{aid}` | แนบ/ลบไฟล์ (DEC-12) | file_policy เดียวกับ Document Center |

## อ่านจาก feature อื่น (อ่านอย่างเดียว · DEC-01 ไม่เขียนกลับ)
| ปลายทาง | ใช้ทำอะไร |
|---|---|
| `GET /api/hr/employees/{id}` (F-HR-EMP) | `employee_name` · `position_name` · `department_name` ของผู้รับประเมิน |
| `GET /api/org/units` (F-ORG-001) | ผังองค์กร → resolve `role-line-manager` |
| `GET /api/config/competency-levels` | `CompetencyLevelConfig.levels[]` — ตารางระดับ 1–4 (DEC-04) |
| `GET /api/doa/resolve?doc_type=CMP&requester={id}` (F-DLG-001) | สายอนุมัติ ณ เวลาส่ง (DEC-03) — **ห้าม fix จำนวนขั้นใน feature** |
| `ENG-DOC-NUM.next('CMP', ctx)` (F-DOCCFG) | เลขที่เอกสาร |
| `ENG-DOC-STORE.store(...)` (F-DOCCFG) | สำเนา PDF เมื่ออนุมัติครบ |
| `ENG-NOTIFY.emit('cmp_cancelled', ...)` (F-NOTIFY) | แจ้งผู้พิจารณาขั้นปัจจุบันเมื่อถูกยกเลิกระหว่างรอ |

## รหัสข้อผิดพลาด
`NOT_VISIBLE` (403) · `NOT_OWNER` (403) · `NOT_DRAFT` (409) · `NOT_CURRENT_APPROVER` (403) ·
`REASON_REQUIRED` (422) · `LEVEL_REQUIRED` (422) · `DOC_TYPE_INACTIVE` (409) · `STALE` (409)

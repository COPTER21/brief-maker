# 02_API — F-AGM-005 Contract Management

> REST · snake_case · legacy routes preserved (invariants §9) · R8: mutation → Function

## §2.1 Endpoints
| API | Method | Path | Purpose | Legacy |
|---|---|---|---|---|
| API-01 | GET | /contracts | list search/filter/sort/page | GET /api/contracts |
| API-02 | POST | /contracts | สร้าง (build-path + write crop license) | POST /api/contracts |
| API-04 | GET | /contracts/:id | detail | GET /api/contracts/:id |
| API-05 | PUT | /contracts/:id | แก้ไข (optimistic) | PUT /api/contracts/:id |
| API-07 | POST | /contracts/:id/approve | อนุมัติ (ไม่ต้องมีเหตุผล) | POST :id/approve |
| API-08 | POST | /contracts/:id/reject | ปฏิเสธ (reason บังคับ + revert license) | POST :id/reject |
| API-09 | POST | /contracts/bulk-action | bulk approve/reject | POST bulk-action |
| API-11 | DELETE | /contracts/:id | ลบ + attachments | DELETE :id |
| API-12 | GET | /contracts/:id/history | audit | (view) |
| API-13 | GET | /contracts/quota-search | ⭐ cross-module: quota + farmer | (flow) |
| API-14 | GET | /contracts/available-items | ⭐ cross-module: plots + crops verified (ยังไม่ contracted) ของโควตา | (flow) |
| API-15 | GET | /contracts/export | export CSV — **backend Pending Spec (TC-522)** · prototype ทำ client-side CSV | export svc |
| API-16 | POST | /contracts/:id/attachments | upload | (flow) |

## §2.X Cross-Module Contract ⭐ (read + WRITE-BACK, → BRD §4)
| API | รายละเอียด |
|---|---|
| API-13 quota-search | `GET ?q=` → quota + farmer snapshot (F-AGM-002 read) |
| API-14 available-items | `GET ?quota_id=` → `{plots[](verified), crops[](verified, license≠contracted)}` (F-AGM-003/004 read) · กัน crop ที่ผูกสัญญาแล้ว |
| **API-02 write** ⭐ | หลัง insert contract → `PATCH crop.license_status='contracted'` ทุก crop ที่ผูก + sync external |
| **API-08 reject write** ⭐ | หลัง set Reject → `PATCH crop.license_status='none'` (revert) + sync external |
| API-07 approve | keep license='contracted' (ไม่เปลี่ยน) |

## §2.2 Contracts (ย่อ)
- **API-02**: body = quota_id + plots[] + crops[] + contract_type + **total_tons (manual, required > 0 ทุก type)** + attachments? + (support_items|promotion7_period|selected_crane ตาม type) · required quota+plots(≥1)+crops(≥1)+type+total_tons → 400 "Missing required fields" · Idempotency-Key → 201 {contract_id, status:'Waiting for verify'} + crop license write
  - **support_items[]** (type=support, structured, ≥1): `{support_type, price, received_date, item_attachments[]}` · support_type ∈ 5 masters (`ปุ๋ย/ยาปราบ`/`เครื่องจักร`/`พันธุ์อ้อย`/`ยาปราบ`/`เงินส่งเสริม`) · แต่ละ item บังคับ support_type + price(≥0) + received_date
  - **promotion7_period** (type=promotion-7) ∈ 4 ค่า: `โปรโมชัน 7 วันหลังเปิดหีบ`/`โปรโมชัน 7 วันก่อนปิดปีใหม่`/`โปรโมชัน 7 วันหลังเปิดปีใหม่`/`โปรโมชัน 7 วันก่อนปิดหีบ`
  - **selected_crane** (type=promotion-crane) ∈ crane master: `กุดโดน`/`ชื่นชม2`/`หนองกุงสวรรค์`/`โนนสำราญ`
  - **early-purchase** = total_tons เท่านั้น (ไม่มี attachments, ไม่มี type field)
- **API-07 approve**: `{userId, userName}` → 200 status=Verified (no reason)
- **API-08 reject**: `{userId, userName, reason}` reason บังคับ → 400 "Rejection reason is required" · → 200 status=Reject + crop license revert none
- **API-09 bulk**: `{action:'approve'|'reject', contractIds[], reason?}` · reject reason บังคับ · skip non-waiting · `{success[], skipped[]}`
- **API-11 delete**: + ลบ attachments · audit

## §2.X Export (Pending Spec)
- **API-15 export**: backend **Pending Spec** ต่อ Testcase TC-522 · prototype ทำ **client-side CSV** (UTF-8 BOM) คอลัมน์: `contract_id, quota_id, farmer_name, contract_type, total_tons, plots_count, crops_count, status, created_by, created_at`

## §2.3 Errors → 05_RULES §5.6
ERR_MISSING_FIELDS · ERR_CROP_NOT_VERIFIED · ERR_CROP_ALREADY_CONTRACTED · ERR_REJECT_NO_REASON · ERR_STALE(409) · ERR_STATUS_CONFLICT · ERR_LICENSE_WRITE_FAIL(rollback)

# 02_API — F-AGM-003 Plot Management

> REST · snake_case · legacy FN names preserved (invariants §9) · R8: ทุก mutation → Function (03_LOGIC)

## §2.1 Endpoints
| API | Method | Path | Purpose | Legacy FN |
|---|---|---|---|---|
| API-01 | GET | /plots | list + search/filter/sort/page | SFN-CF-SER-00050 |
| API-02 | POST | /plots | สร้างแปลง (ผูก quota) | SFN-CF-CRE-00042 |
| API-03 | POST | /plots/validate | validate ก่อนบันทึก (client-first) | SFN-CF-VAL-00041 |
| API-04 | GET | /plots/:id | detail | SFN-CF-VIEW-00046 |
| API-05 | PUT | /plots/:id | แก้ไข (optimistic, status คงเดิม) | SFN-CF-UPT-00047 |
| API-06 | GET | /plots/check-deed | deed_number unique | (VR-07) |
| API-07 | POST | /plots/:id/verify | verify เดี่ยว (pass/fail+reason) | SFN-CF-UPT-00048 |
| API-08 | POST | /plots/bulk-verify | verify กลุ่ม (shared reason) | SFN-CF-UPT-00048(bulk) |
| API-09 | POST | /plots/import | CSV commit (partial success) | SFN-CF-CRE-00045 |
| API-10 | GET | /plots/import/template | ดาวน์โหลดแม่แบบ (UTF-8 BOM) | (config) |
| API-11 | DELETE | /plots/:id?mode=soft\|hard | ลบ + reason | SFN-CF-DEL-00049 |
| API-12 | GET | /plots/:id/history | audit log | (view) |
| API-13 | GET | /plots/quota-search | ⭐ cross-module: autocomplete quota + farmer snapshot | SFN-CF-SER-00039 |
| API-14 | GET | /plots/export | export CSV (respect filter) | SFN-CF-GEN-00051 |

## §2.X Cross-Module Contract (⭐ → BRD §4)
| API-13 | `GET /plots/quota-search?q=` |
|---|---|
| อ่านจาก | F-AGM-002 Quota (verified quotas) ผ่าน ENG-EXT-Q01 |
| return | `[{ quota_id, quota_no, farmer_name, citizen_id_masked, phone, address }]` (read-only snapshot) |
| ใช้ตอน | create quota-binding · store `plot.quota_id` + `quota_no` |
| **ไม่มี PATCH/write** ไป quota | Plot อ่านอย่างเดียว |
| quota ถูกลบภายหลัง | plot คง quota_no snapshot + flag (ไม่ error) |

## §2.2 Contracts (ย่อ)
- **API-02 POST /plots**: body = 14 fields + quota_id + shapefile_ref (+doc_ref?) · header `Idempotency-Key` · → 201 {plot_code, status:'Waiting for verify'} · 409 deed dup · 422 validation
- **API-05 PUT /plots/:id**: + `expected_version` → 200 (version++, status ไม่เปลี่ยน) · 409 stale "ข้อมูลล้าสมัย กรุณารีเฟรช"
- **API-07 verify**: `{result:'pass'|'fail', fail_reason?}` · fail ต้องมี reason → 422 · status ≠ waiting → 409 "สถานะเปลี่ยนแปลงแล้ว"
- **API-08 bulk-verify**: `{ids[], result, fail_reason?}` · partial → `{success[], failed[{id,reason}]}`
- **API-09 import**: multipart CSV → `{total, created, failed[{row,reason}]}` ทุกแถว Waiting for verify
  - **คอลัมน์แม่แบบ 13 (G1/G3, ตามลำดับ):** `quota_no, ownership_type, deed_number, deed_issue_date, deed_owner_name, address, province, district, subdistrict, latitude, longitude, area, shapefile_url`
  - **`shapefile_url` = required** (แถวว่าง → failed reason "กรุณาแนบไฟล์ลักษณะแปลง (Shapefile)") · **`postal_code` ไม่อยู่ในคอลัมน์** (derive จาก subdistrict · VR-10) · AS-BUILT canonical fields (dev): `quotaNo, ownershipType, deedNumber, deedIssueDate, deedOwnerName, addressLine, province, district, subdistrict, latitude, longitude, area, shapeFileUrl`
- **API-10 template** `GET /plots/import/template`: UTF-8 BOM · header = 13 คอลัมน์ข้างต้น (`shapefile_url` บังคับ) + 2 แถวตัวอย่าง
- **API-11 delete**: `?mode=soft|hard` + `{reason?}` · idempotent · audit

## §2.3 Errors → 05_RULES §5.6
ERR_QUOTA_NOT_FOUND · BR_DEED_DUPLICATE · ERR_VALIDATION_FAILED · BR_VERIFY_FAIL_NO_REASON · ERR_STALE_DATA(409) · BR_STATUS_CONFLICT · ERR_CSV_INVALID · ERR_SHAPEFILE_REQUIRED

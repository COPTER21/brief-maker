# 02_API — F-AGM-004 Crop Management

> REST · snake_case · legacy AT/SEQ preserved · R8: mutation → Function

## §2.1 Endpoints
| API | Method | Path | Purpose | Legacy |
|---|---|---|---|---|
| API-01 | GET | /crops | list search/filter/sort/page | FN-AT-CROP-191 |
| API-02 | POST | /crops | สร้าง (double-bind) | AT-189 (SEQ-203) |
| API-03 | POST | /crops/validate | validate payload | AT-188 |
| API-04 | GET | /crops/:id | Landing detail | AT-190 |
| API-05 | PUT | /crops/:id | แก้ไข (verified→waiting) | AT-198 (SEQ-206) |
| API-07 | POST | /crops/:id/verify | verify/reject เดี่ยว | AT-200 |
| API-08 | POST | /crops/bulk-verify | verify/reject กลุ่ม | SEQ-205→AT-200 |
| API-09 | POST | /crops/upload-csv | CSV per-row create | AT-196/197 (SEQ-204) |
| API-10 | GET | /crops/csv-template | แม่แบบ | (config) |
| API-11 | POST | /crops/:id/cancel-delete | cancel/delete soft | AT-199 |
| API-12 | GET | /crops/:id/history | audit | (view) |
| API-13 | GET | /crops/quota-search | ⭐ cross-module: quota exact verified + farmer snapshot | AT-184 |
| API-14 | GET | /crops/plots | ⭐ cross-module: plots ของเจ้าของ quota + verified | AT-185/186 |
| API-15 | GET | /crops/:id/etcd | ⭐ ETCD bookings + remaining compute (fail-soft) | AT-193/194 |
| API-16 | GET | /crops/:id/surveys | ⭐ Survey (fail-soft) | AT-195 |
| API-17 | GET | /crops/export | export CSV (respect filter) · prototype = client-side · **backend Pending Spec** (TC-581) | export svc |
| API-18 | POST | /crops/:id/photos | upload photos | AT-202 |

## §2.X Cross-Module Contract ⭐ (double read + external, → BRD §4)
| API | รายละเอียด |
|---|---|
| API-13 quota-search | `GET ?quota_id=&exact=1` → verified quota + `{farmer_name, phone, quota_owner_id}` (F-AGM-002 read) · ไม่พบ/ไม่ verified → 404/409 |
| API-14 plots | `GET ?quota_owner_id=&verified=1` → plots ของเจ้าของ + `{plot_id, address, size_rai}` (F-AGM-003 read) · owner mismatch → excluded |
| API-15 etcd | `GET` → `{bookings[], total_booked_tons}` → remaining = total_tons − total_booked · **fail-soft** (คืน null + flag) |
| API-16 surveys | `GET` → `{surveys[], latest_synced}` · **fail-soft** |
| **ไม่มี write** ทุก external | Crop อ่านอย่างเดียว |

## §2.2 Contracts (ย่อ)
- **API-02**: body = quota_id + plot_id + production_year_be + planted_month + total_tons + plot_code? + variety? + cane_type? + found_disease_insect? + disease_details? + geo? + photos[] · Idempotency-Key → 201 {crop_id, status:'waiting_for_verify'} · 409 CONFLICT · 422 validation
  - `variety` → cane_variety (enum khon-kaen-3/lk-92-11/ut-8) · `cane_type` (enum new/ratoon) · `found_disease_insect` → disease_pest_found (boolean) · `disease_details` → disease_pest_detail · ทั้งหมด optional
  - `cane_age_months` = **derived preview** เท่านั้น (FN-AT-CROP-188/192 คำนวณจาก planted_month + production_year_be) · read-only · ไม่รับจาก body
  - `geo` = prototype รับ lat+long 2 ช่องแยก (เก็บละเอียด) → map เป็น geo_coordinate "lat,long" บน contract (functionally equivalent)
- **API-05 PUT**: body เดียวกับ API-02 (create fields ทั้งหมด editable) + expected_version → 200 (**verified→waiting_for_verify** LOCK-05, quota/plot ignored) · 409 stale
- **API-07 verify**: `{result:'verify'|'reject', reason?}` · reject ต้องมี reason → 422 · status≠waiting → 409
- **API-08 bulk**: `{ids[], result, reason?}` · skip non-waiting · `{success[], skipped[]}`
- **API-11 cancel-delete**: `{action:'cancel'|'delete', reason}` reason บังคับ · soft · audit
- **API-09 csv**: multipart → per-row validate (quota/plot verified) → `{total, created, failed[{row,reason}]}` ทุกแถว waiting
  - **CSV schema = create form (8 คอลัมน์, ลำดับเป๊ะ):** `quota_id, plot_id, production_year_be, plot_code, variety, cane_type, planted_month, total_tons` (เดิม 5 คอลัมน์ · `year_be` เปลี่ยนชื่อเป็น `production_year_be` ตาม authoritative naming)
  - reconciliation: AS-BUILT expectedHeaders ตัด `plot_id` (mock simplification) แต่ prototype คง `plot_id` ไว้เพราะ plot linkage ต้องใช้ · `geo_coordinate`/`plot_size_rai` จาก AS-BUILT 9-col เป็น plot snapshot ไม่ใช่ CSV input
- **API-17 export**: client-side CSV export ใน prototype (เคารพ filter ปัจจุบัน) · ⚠️ **backend export endpoint/idempotency = Pending Spec** (per Testcase TC-581 — follow-up question ทีม dev)

## §2.3 Errors → 05_RULES §5.6
ERR_QUOTA_NOT_VERIFIED · ERR_PLOT_OWNER_MISMATCH · ERR_PLOT_NOT_VERIFIED · ERR_VALIDATION · ERR_REJECT_NO_REASON · ERR_STALE(409) · ERR_STATUS_CONFLICT · ERR_CSV_INVALID · ERR_ETCD_UNAVAILABLE(fail-soft)

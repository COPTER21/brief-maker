# 02_API — F-AGM-006 Survey Management

> REST · snake_case · R8: mutation → Function

## §2.1 Endpoints
| API | Method | Path | Purpose |
|---|---|---|---|
| API-01 | GET | /surveys | list search/filter/sort/page |
| API-02 | POST | /surveys | สร้าง (cascade) |
| API-04 | GET | /surveys/:id | detail |
| API-05 | PUT | /surveys/:id | แก้ไข (verified→waiting) |
| API-07 | POST | /surveys/:id/verify | verify/reject เดี่ยว |
| API-08 | POST | /surveys/bulk-verify | verify/reject กลุ่ม |
| API-09 | POST | /surveys/upload-csv | CSV per-row |
| API-10 | GET | /surveys/csv-template | แม่แบบ |
| API-11 | POST | /surveys/:id/cancel-delete | cancel/delete soft |
| API-12 | GET | /surveys/:id/history | audit |
| API-13 | GET | /surveys/quota-search | ⭐ cross-module: quota + farmer |
| API-14 | GET | /surveys/cascade | ⭐ cross-module: plots ของ quota + crops ของ plot |
| API-15 | GET | /surveys/export | export CSV |
| API-16 | POST | /surveys/:id/photos | upload photos (4 หมวด) |

## §2.X Cross-Module Contract ⭐ (→ BRD §4)
| API | รายละเอียด |
|---|---|
| API-13 quota-search | quota + farmer snapshot (F-AGM-002 read) |
| API-14 cascade | `?quota_id=` → plots(F-AGM-003) · `?plot_id=` → crops(F-AGM-004) · read-only |
| **feeds Crop** | survey verified → Crop F-AGM-004 อ่าน (แท็บสำรวจ) — Crop pull-read, ไม่มี write จาก Survey |

## §2.2 Contracts (ย่อ)
- **API-02**: body = quota_id+plot_id+crop_id + survey_date+surveyor(↔recorder req)+year + cane_variety+yield(↔total_tons req ≥0)+plot_size + **agronomic panel (optional):** planted_month(1–12)?+cane_type(อ้อยใหม่/อ้อยตอ)?+row_spacing_cm?+cane_height_head_cm?/mid_cm?/tail_cm?+internode_length_cm?+diameter_cm?+average_stalks_per_clump?+clumps_in_10m?+soil_color?+soil_type?+leaf_color?+weed_density?+disease_pest?(level)+disease_pest_found?+disease_pest_detail?+survey_postal_code(^\d{5}$)?+geo? + photos[] · required cascade+พื้นฐาน+พืชผล → 201 {survey_id, status:'waiting_for_verify'} · Idempotency-Key · **`cane_age_months` = derived preview เท่านั้น — ไม่รับจาก body** (server คำนวณ FN-AT-CROP-192)
- **API-05 PUT**: same agronomic panel + expected_version → 200 (**verified→waiting** LOCK-07) · 409 stale · `cane_age_months` derived (ไม่รับจาก body)
- **API-07 verify**: `{result:'verify'|'reject', reason?}` · reject reason บังคับ → 422 · status≠waiting → 409
- **API-08 bulk**: `{ids[], result, reason?}` · skip non-waiting · partial
- **API-11 cancel-delete**: `{action, reason}` reason บังคับ · soft
- **API-09 csv**: per-row cascade+field validate → partial · ทุกแถว waiting
- **API-15 export**: List page มีปุ่ม Export CSV (data-test-id `btn-export`) · prototype = **client-side CSV** (สร้างจากผลกรอง list) · **backend export endpoint + idempotency = Pending Spec** (per Testcase TC-606)

## §2.3 Errors → 05_RULES §5.6
ERR_CASCADE_INVALID · ERR_VALIDATION · ERR_REJECT_NO_REASON · ERR_STALE(409) · ERR_STATUS_CONFLICT · ERR_CSV_INVALID

# BRD — F-AGM-003 Plot Management (จัดการแปลงที่ดิน)

| Field | Value |
|---|---|
| Feature ID | F-AGM-003 |
| Module | AGM · Site WKN |
| Status | **APPROVED** (Refactor Wave — constraint mode จาก invariants.md 🔒) |
| Type | Refactor (legacy v0 → CUBE NATIVE) |
| Upstream | F-AGM-002 Quota (read), F-AGM-001 Farmer (indirect via quota) |
| Author | brd-generator-full (SOW3.2) |

---

## §1 Executive Summary
ระบบลงทะเบียนและบริหารจัดการ "แปลงที่ดิน (Plot)" ของชาวไร่อ้อย เชื่อมกับทะเบียนโควตา (F-AGM-002): ผู้ใช้ต้องค้นหาและยืนยัน "เลขโควตาชาวไร่" ก่อนกรอกข้อมูลแปลง เพื่อยืนยันความเป็นเจ้าของ · หนึ่งโควตา/เกษตรกรมีได้หลายแปลง (1:N) · รองรับ CRUD, นำเข้า CSV (wizard), ตรวจสอบยืนยันเดี่ยว/กลุ่ม, ค้นหา/กรอง/ส่งออก, soft/hard delete และ audit log ครบทุก mutation

## §2 Objectives & Success Metrics
| # | Objective | Metric (วัดได้) |
|---|---|---|
| 2.1 | ยืนยันความเป็นเจ้าของก่อนสร้างแปลง | 100% ของ plot มี quota_id ผูก (ไม่มี orphan) |
| 2.2 | ลดข้อผิดพลาดพิกัด/ที่อยู่ | lat/long/postal/area validation reject 100% ค่านอกช่วง |
| 2.3 | เร่งงานภาคสนาม | CSV import 1,000 แถว < 60s · create < 1s |
| 2.4 | ตรวจสอบย้อนหลังได้ | audit log ครบ 100% ของ create/edit/verify/delete |
| 2.5 | คุณภาพข้อมูล | deed_number ซ้ำ = 0 (unique enforce) |

## §3 Scope

### §3.1 In Scope
CRUD plot · Quota search+select + Farmer snapshot (read-only) · address 5-field · lat/long + area · Shapefile (mandatory) + Document (optional) upload · CSV wizard · verify single/bulk (Pass/Fail+reason) · search/filter/sort/export CSV · pagination · soft/hard delete + reason · audit log + view

### §3.2 Out of Scope
เขียนกลับไป Quota (Plot อ่านอย่างเดียว) · แก้ไขข้อมูล Farmer/Quota · GIS map rendering (เก็บ lat/long + shapefile ref เท่านั้น) · offline mode (OQ)

### §3.4 Scope Lock (→ FRD 00_OVERVIEW, สืบทอดใบเซ็น)
| LOCK | ข้อความ locked |
|---|---|
| **LOCK-01** | capability legacy v0 คงครบ 100% (CRUD/CSV/verify/bulk/delete/search/export) |
| **LOCK-02** | สถานะ 3 ระดับ: Waiting for verify (init) → Verified / Verification failed(+reason) · state machine ตาม invariants §4 |
| **LOCK-03** | **Quota binding บังคับ** — ต้อง search+select valid quota ก่อนกรอกข้อมูลแปลง · ผูก quota_id (READ-ONLY cross-module, ไม่ write-back) |
| **LOCK-04** | address = single `address_line` + province + district + subdistrict + postal_code (5 fields) · ยึด code AS-BUILT (Stage10 line1/2 = drift) |
| **LOCK-05** | Shapefile = แนบ **บังคับ** · Document = optional |
| **LOCK-06** | 1 quota/farmer : N plots (ไม่จำกัดจำนวนแปลง) |
| **LOCK-07** | edit สำเร็จ → status **ไม่เปลี่ยนอัตโนมัติ** |
| **LOCK-08** | verify (เดี่ยว/กลุ่ม) มี Confirm เสมอ · Fail ต้องมี reason · Bulk Fail = เหตุผลเดียวทุกรายการ |
| **LOCK-09** | soft + hard delete + reason · audit ทุกครั้ง |
| **LOCK-10** | CSV import → ทุกแถว Waiting for verify · partial success + error report |
| **LOCK-11** | optimistic lock (version) + idempotency ทุก mutation · audit log ครบ (actor/time/count) |
| **LOCK-12** | deed_number unique ต่อ tenant · duplicate → reject |

## §4 Cross-Module Contract ⭐ (→ FRD 02_API §2.X)
| Item | รายละเอียด |
|---|---|
| Provider | F-AGM-002 Quota (+ F-AGM-001 Farmer ผ่าน quota) |
| Consumer | F-AGM-003 Plot |
| Read 1 | `GET quota-search?q=` — autocomplete Quota No. (verified quota) |
| Read 2 | `GET quota/:id/farmer-snapshot` — ชื่อ/เลขบัตร/ที่อยู่ farmer (read-only panel) |
| Store | `plot.quota_id` FK → T_quota.id · `quota_no` denormalized |
| **ไม่มี write-back** | Plot ไม่แก้ไข quota/farmer ใด ๆ (ต่างจาก Quota→Farmer) |
| Failure | quota ไม่พบ → block create · quota ถูกลบภายหลัง → plot อ้าง quota_no เดิม (snapshot) + flag |
| Engine | ENG-EXT-Q01 `quota-plot-connector` (read-only adapter) |

## §5 Personas & Permissions (→ invariants §6)
Field Officer (create/edit/delete/import/export) · Agriculture Admin/Data Steward (+verify/bulk verify) · verify = checker role

## §6 Data Requirements
T_plot (27 fields — invariants §1) · T_plot_history (audit append-only) · T_plot_document (shapefile + docs) · FK quota_id, province/district/subdistrict (M-01)

## §7 Functional Stories
| US | Story |
|---|---|
| US-01 | Field Officer สร้างแปลง: ค้นหา+เลือก quota → farmer snapshot → กรอก 14 fields + shapefile → save → Waiting for verify |
| US-02 | Quota ไม่พบ → inline error, block |
| US-03 | นำเข้า CSV wizard → N แปลง Waiting for verify + error report |
| US-04 | ดูรายละเอียดแปลง (3 tab: ข้อมูล/ไฟล์/ประวัติ) + farmer snapshot |
| US-05 | Verify เดี่ยว: Pass→Verified / Fail→Verification failed+reason |
| US-06 | Bulk verify: เลือกหลายรายการ → Pass/Fail (เหตุผลเดียว) + partial result |
| US-07 | แก้ไขแปลง → status คงเดิม + audit |
| US-08 | ลบแปลง (soft/hard) + reason + audit |
| US-09 | ค้นหา/กรอง(status/province)/sort/export CSV + pagination |
| US-10 | ดู audit log ของแปลง |

## §11 Non-Functional (→ FRD 06_TESTS §6.6)
GET list (p95<3s) · create/update <1s · CSV 1,000<60s · shapefile ≤50MB · doc ≤5MB · coordinates 6 decimals · UTF-8 · desktop ≥1180px

## §12 Value Stream Impact
### §12.1 Downstream Map
Plot (verified) → [future] สัญญาส่งอ้อย → การส่งอ้อยเข้าโรงงาน · Plot อ่าน Quota (verified) · Quota อ่าน Farmer (approved) — โซ่ AGM: Farmer → Quota → **Plot** → สัญญา

## §17 Open Questions (→ invariants §8, locked defaults) OQ-P1..P7

## §18 Dashboard Widgets (stats)
แปลงทั้งหมด · รอตรวจสอบ (+aging) · ตรวจแล้ว · ไม่ผ่าน (+reason)

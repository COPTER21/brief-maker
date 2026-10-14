# BRD — F-AGM-005 Contract Management (จัดการสัญญาส่งอ้อย)

| Field | Value |
|---|---|
| Feature ID | F-AGM-005 |
| Module | AGM · Site WKN |
| Status | **APPROVED** (Refactor Wave — constraint mode จาก invariants.md 🔒) |
| Type | Refactor (legacy Next.js+API → CUBE NATIVE) |
| Upstream | F-AGM-002 Quota + F-AGM-003 Plot + F-AGM-004 Crop (read) · **write-back crop license** ⭐ |
| Author | brd-generator-full (SOW3.2) |

---

## §1 Executive Summary
ระบบจัดการสัญญาส่งอ้อยของชาวไร่ — ปลายทางของโซ่ AGM (Farmer→Quota→Plot→Crop→Contract): เจ้าหน้าที่เลือกโควตา → เลือกแปลง (≥1) และรอบปลูกที่ตรวจสอบแล้ว (verified, ≥1) → เลือกประเภทสัญญา 1 ใน 5 (ตันสูญเปล่า/ส่งเสริม/โปร 7 วัน/เครน/ตกเขียว) → กรอกข้อมูลเฉพาะประเภท + กรอกจำนวนตันที่ทำสัญญา (manual > 0, มี helper รวมตันจาก crop) + แนบเอกสาร → สร้างสัญญา (รอการตรวจสอบ) → อนุมัติ/ปฏิเสธ (เดี่ยว/กลุ่ม) · เมื่อสร้าง ระบบตั้งสถานะสิทธิ์ (license) ของรอบปลูกเป็น "ทำสัญญาแล้ว" (contracted) · เมื่อปฏิเสธ คืนสถานะเป็น "ไม่มีสัญญา" (none)

## §2 Objectives & Metrics
| # | Objective | Metric |
|---|---|---|
| 2.1 | รวมผลผลิตที่ตรวจแล้วเป็นสัญญา | 100% contract ผูก crop verified (ไม่มี orphan) |
| 2.2 | คุมสิทธิ์ crop ไม่ซ้ำสัญญา | 1 crop : 1 active contract (license contracted) |
| 2.3 | ควบคุมประเภทสัญญาถูกต้อง | type-specific fields ครบ 100% ตามประเภท |
| 2.4 | ตรวจสอบย้อนหลัง | audit ครบ create/approve/reject/delete |
| 2.5 | ความถูกต้อง license sync | crop license (contracted/none) ตรงกับสถานะ contract 100% |

## §3 Scope

### §3.1 In Scope
CRUD contract · build path (quota→plots→crops verified→type) · 5 contract types + type-specific (support = รายการส่งเสริมแบบ **structured**: ประเภท/ราคา/วันที่รับ + แนบต่อรายการ) · **total_tons manual input บังคับ > 0** (crop-sum เป็น helper) + plot/crop count · attachments (ยกเว้น early-purchase) · approve/reject single+bulk (reject reason บังคับ) · **write-back crop license** · search/filter/sort · **Export CSV ที่หน้า List (client-side, backend Pending Spec)** · delete + audit

### §3.2 Out of Scope
แก้ไข Quota/Plot/Crop (อ่าน + เขียนเฉพาะ crop license) · คำนวณราคา/จ่ายเงิน (นอกขอบเขต phase นี้) · e-signature จริง

### §3.4 Scope Lock (→ FRD 00_OVERVIEW)
| LOCK | ข้อความ |
|---|---|
| **LOCK-01** | capability legacy คงครบ 100% |
| **LOCK-02** | status 3: Waiting for verify(รอการตรวจสอบ,init)/Verified(อนุมัติแล้ว)/Reject(ปฏิเสธ) |
| **LOCK-03** | **build path บังคับ**: โควตา → แปลง(≥1) → รอบปลูก verified(≥1) → ประเภทสัญญา |
| **LOCK-04** | **5 ประเภทสัญญา**: ตันสูญเปล่า/ส่งเสริม/โปร 7 วัน/เครน/ตกเขียว · type-specific fields |
| **LOCK-05** | total_tons = manual input บังคับ > 0 ทุกประเภท (crop-sum เป็น helper "ใช้ค่านี้") · plot_count/crop_count นับ |
| **LOCK-06** | approve/reject: Waiting เท่านั้น · approve ไม่ต้องมีเหตุผล · **reject reason บังคับ** · เดี่ยว+bulk |
| **LOCK-07** | **cross-module write-back**: create → crop license='contracted' · reject → revert 'none' · approve → keep · sync external |
| **LOCK-08** | 1 crop : 1 active contract (กัน crop license=contracted เลือกซ้ำ) |
| **LOCK-09** | delete + ลบไฟล์แนบ + audit |
| **LOCK-10** | optimistic lock + idempotency + audit ทุก mutation |

## §4 Cross-Module Contract ⭐ (read + WRITE-BACK, → FRD 02_API §2.X)
| Item | รายละเอียด |
|---|---|
| Read Quota | quota + farmer snapshot |
| Read Plot | แปลงของโควตา (verified) |
| Read Crop | รอบปลูก verified ของโควตา (+ total_tons) |
| **WRITE Crop license** ⭐ | create → `PATCH crop.license_status='contracted'` · reject → `='none'` · approve → keep · sync external |
| Engine | ENG-EXT-AGM `agm-chain-connector` (read quota/plot/crop) + `crop-license-writer` (write-back) |
| Failure | write fail → rollback + retry (OQ) |

## §5 Personas & Permissions (→ invariants §6)
เจ้าหน้าที่สัญญา (create/edit/delete) · ผู้อนุมัติ (+approve/reject)

## §6 Data Requirements
T_contract (invariants §1) · T_contract_plot (M:N) · T_contract_crop (M:N) · type-specific tables · T_contract_attachment · T_contract_history · read+write Crop

## §7 Functional Stories
| US | Story |
|---|---|
| US-01 | เลือกโควตา → แปลง(≥1) → รอบปลูก verified(≥1) → ประเภทสัญญา + type fields + แนบเอกสาร → สร้าง (Waiting) + crop license=contracted |
| US-02 | quota/crop invalid (ไม่ verified/ไม่ครบ) → block |
| US-03 | ดูรายละเอียดสัญญา (ข้อมูล/แปลง/รอบปลูก/เอกสาร/ประวัติ) |
| US-04 | อนุมัติ (Verified) — ไม่ต้องมีเหตุผล |
| US-05 | ปฏิเสธ (+reason บังคับ) → Reject + คืน crop license=none |
| US-06 | Bulk approve/reject (skip non-eligible + summary) |
| US-07 | แก้ไขสัญญา |
| US-08 | ลบสัญญา (+ไฟล์แนบ) + audit |
| US-09 | ค้นหา/กรอง(status/type)/sort/export |

## §11 Non-Functional
list p95<3s · create/approve<1s · write-back crop license <500ms sync · attachments policy · optimistic lock

## §12 Value Stream Impact
Farmer → Quota → Plot → Crop → **Contract (สัญญาส่งอ้อย)** → [downstream] การส่งอ้อยเข้าโรงงาน — Contract เขียน crop license (contracted) ปิดโซ่ทะเบียน AGM

## §17 Open Questions → invariants §8 (OQ-CT1..CT6)

## §18 Dashboard Widgets
สัญญาทั้งหมด · รอการตรวจสอบ · อนุมัติแล้ว · ปฏิเสธ · (แยกตามประเภทสัญญา)

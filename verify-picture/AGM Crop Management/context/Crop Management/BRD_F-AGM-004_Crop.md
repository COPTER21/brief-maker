# BRD — F-AGM-004 Crop Management (การจัดการรอบปลูก)

| Field | Value |
|---|---|
| Feature ID | F-AGM-004 |
| Module | AGM · Site WKN |
| Status | **APPROVED** (Refactor Wave — constraint mode จาก invariants.md 🔒) |
| Type | Refactor (legacy Next.js → CUBE NATIVE) |
| Upstream | F-AGM-002 Quota + F-AGM-003 Plot (double read-only) · ETCD/Survey (external read) |
| Author | brd-generator-full (SOW3.2) |

---

## §1 Executive Summary
ระบบจัดการรอบปลูก/ผลผลิตอ้อยรายปีของชาวไร่ เชื่อมโยงทั้งทะเบียนโควตา (F-AGM-002) และทะเบียนแปลง (F-AGM-003): เจ้าหน้าที่ค้นหาโควตา (verified, exact) → เลือกแปลงของเจ้าของโควตา (verified) → กรอกข้อมูลรอบปลูก (ปี พ.ศ. เดือนปลูก ปริมาณรวมตัน) + แนบรูป → สร้าง Crop (waiting_for_verify) → ตรวจสอบยืนยัน/ปฏิเสธ (เดี่ยว/กลุ่ม) · หน้า Landing รวมข้อมูล + แท็บ ETCD (การจอง) และ Survey (สำรวจ) แบบ read-only · แสดง remaining_unbooked = total_tons − ΣETCD (ติดลบได้พร้อมเตือน)

## §2 Objectives & Metrics
| # | Objective | Metric |
|---|---|---|
| 2.1 | ยืนยันสายสัมพันธ์ quota→plot ก่อนสร้าง | 100% crop มี quota_id+plot_id verified (ไม่มี orphan/owner mismatch) |
| 2.2 | ควบคุมปริมาณจองไม่เกินผลผลิต | remaining_unbooked แสดง/เตือนเมื่อ < 0 ครบ 100% |
| 2.3 | คุณภาพข้อมูล | year 2500-2600 · month 1-12 · tons ≥ 0 reject 100% ค่านอกช่วง |
| 2.4 | ตรวจสอบย้อนหลัง | audit ครบ create/edit/verify/reject/cancel/delete |
| 2.5 | ประสิทธิภาพ | list p95<3s · create<1s · CSV 1,000<60s · ETCD/Survey fail-soft |

## §3 Scope

### §3.1 In Scope
CRUD crop · double-binding (quota→plot→form) · snapshot read-only · year/month/tons + photos · ข้อมูลลักษณะอ้อย (สายพันธุ์/ประเภทอ้อย/อายุอ้อยคำนวณอัตโนมัติ/พบโรค-ศัตรูพืช + รายละเอียด · รหัสแปลง) · remaining compute + negative badge · verify/reject single+bulk · CSV upload wizard (schema = create form 8 คอลัมน์) · Landing (Overview/Photos/ETCD/Survey/Audit) · soft cancel/delete + reason · search/filter/sort/export (Export CSV จากหน้า List)

### §3.2 Out of Scope
เขียนกลับ Quota/Plot (อ่านอย่างเดียว) · จัดการ ETCD booking / Survey (แสดงเท่านั้น) · คำนวณ/แก้ยอดจอง

### §3.4 Scope Lock (→ FRD 00_OVERVIEW)
| LOCK | ข้อความ |
|---|---|
| **LOCK-01** | capability legacy คงครบ 100% |
| **LOCK-02** | canonical status 5: waiting_for_verify(init)/verified/rejected/cancelled/deleted |
| **LOCK-03** | **double-binding บังคับ**: Quota(verified,exact) → Plot(ของเจ้าของ quota + verified) → form · READ-ONLY (ไม่ write-back) |
| **LOCK-04** | snapshot farmer/address/size read-only จาก quota/plot |
| **LOCK-05** | **edit crop ที่ verified แล้ว save → กลับ waiting_for_verify** (ต่างจาก Plot) |
| **LOCK-06** | quota_id/plot_id แก้ไม่ได้ตอน edit |
| **LOCK-07** | verify/reject: status=waiting เท่านั้น · reject **reason บังคับ** · เดี่ยว+bulk (skip non-eligible) |
| **LOCK-08** | remaining_unbooked_tons = total_tons − ΣETCD · **ติดลบได้ + badge เตือน** (list+landing) |
| **LOCK-09** | ETCD + Survey = read-only tab · external fail-soft |
| **LOCK-10** | CSV schema = create form · ทุกแถว waiting_for_verify · idempotent per-row · partial + report |
| **LOCK-11** | soft cancel/delete + เหตุผลบังคับ + audit |
| **LOCK-12** | optimistic lock + idempotency + audit ทุก mutation |
| **LOCK-13** | year 2500-2600 · month 1-12 · total_tons ≥ 0 |

## §4 Cross-Module Contract ⭐ (double, → FRD 02_API §2.X)
| Item | รายละเอียด |
|---|---|
| Read Quota (F-AGM-002) | `GET quota-search?exact=` — verified quota + farmer owner snapshot (AT-184) |
| Read Plot (F-AGM-003) | `GET plots?quota_owner=&verified=1` — แปลงของเจ้าของ quota + address/size (AT-185/186) |
| Read ETCD (external) | `GET crop/:id/etcd` — bookings → compute remaining (AT-193/194) fail-soft |
| Read Survey (external) | `GET crop/:id/surveys` (AT-195) fail-soft |
| Store | crop.quota_id + plot_id + snapshots (farmer/address/size denormalized) |
| **ไม่มี write-back** ทุกทิศ | Crop อ่านอย่างเดียว |
| Engine | ENG-EXT-QP `crop-source-connector` (read quota+plot) · ENG-EXT-ES `etcd-survey-reader` (fail-soft) |

## §5 Personas & Permissions (→ invariants §6)
เจ้าหน้าที่ crop (create/edit/CSV/cancel/delete) · ผู้ตรวจสอบ (+verify/reject)

## §6 Data Requirements
T_crop (invariants §1) · T_crop_photo · T_crop_history (audit) · read T_quota/T_plot + external ETCD/Survey

## §7 Functional Stories
| US | Story |
|---|---|
| US-01 | ค้นหา quota verified (exact) → เลือก plot ของเจ้าของ (verified) → กรอก crop + รูป → waiting_for_verify |
| US-02 | quota ไม่พบ/ไม่ verified → block · plot owner mismatch → block |
| US-03 | CSV upload wizard → N crop waiting_for_verify + error report |
| US-04 | Landing: Overview + Photos + ETCD tab + Survey tab + Audit |
| US-05 | Verify เดี่ยว → verified |
| US-06 | Reject เดี่ยว (+reason บังคับ) → rejected |
| US-07 | Bulk verify/reject (skip non-eligible + summary) |
| US-08 | Edit crop → quota/plot read-only · verified → save กลับ waiting |
| US-09 | Cancel/Delete (+reason) → cancelled/deleted (soft) |
| US-10 | ค้นหา/กรอง/sort/export + negative remaining badge |

## §11 Non-Functional
list p95<3s · create/update<1s · CSV 1,000<60s · ETCD/Survey fail-soft (≤1.5s) · photos policy · optimistic lock

## §12 Value Stream Impact
Farmer → Quota → Plot → **Crop** (รอบปลูก+ผลผลิต) → [ETCD จอง] → [future] สัญญาส่งอ้อย → ส่งเข้าโรงงาน

## §17 Open Questions → invariants §8 (OQ-C1..C6)

## §18 Dashboard Widgets
Crop ทั้งหมด · รอตรวจสอบ · ตรวจแล้ว · ปฏิเสธ · (เตือน remaining ติดลบ N รายการ)

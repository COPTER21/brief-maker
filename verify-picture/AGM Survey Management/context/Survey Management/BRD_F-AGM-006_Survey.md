# BRD — F-AGM-006 Survey Management (จัดการแบบสำรวจ)

| Field | Value |
|---|---|
| Feature ID | F-AGM-006 |
| Module | AGM · Site WKN |
| Status | **APPROVED** (Refactor Wave — constraint mode จาก invariants.md 🔒) |
| Type | Refactor (legacy Next.js → CUBE NATIVE) |
| Upstream | F-AGM-002/003/004 (read cascade) · feeds Crop survey tab |
| Author | brd-generator-full (SOW3.2) |

---

## §1 Executive Summary
ระบบบันทึกแบบสำรวจแปลงและรอบปลูกภาคสนามของชาวไร่อ้อย — เจ้าหน้าที่ภาคสนามเลือกโควตา → แปลง → รอบปลูก → บันทึกข้อมูลเชิงเกษตร (พันธุ์อ้อย, ประมาณการผลผลิต, ขนาดแปลง, สีดิน, การตรวจสีใบ, การพบโรค/ศัตรูพืช, พิกัด) พร้อมแนบรูปประกอบ 4 หมวด → สร้างแบบสำรวจ (รอตรวจสอบ) → ตรวจสอบยืนยัน/ปฏิเสธ (เดี่ยว/กลุ่ม) · ข้อมูลที่ผ่านการยืนยันจะป้อนเข้าแท็บ "สำรวจ" ของรอบปลูก (F-AGM-004)

## §2 Objectives & Metrics
| # | Objective | Metric |
|---|---|---|
| 2.1 | เก็บข้อมูลสำรวจครบถ้วน | 100% survey ผูก quota/plot/crop (ไม่มี orphan) |
| 2.2 | คุณภาพข้อมูลเกษตร | yield ≥ 0 · plot_size > 0 · lat/long valid reject 100% นอกช่วง |
| 2.3 | ตรวจสอบย้อนหลัง | audit ครบ create/verify/reject/cancel/delete |
| 2.4 | ป้อนข้อมูลเข้ารอบปลูก | survey verified แสดงในแท็บสำรวจของ Crop 100% |

## §3 Scope

### §3.1 In Scope
CRUD survey · cascade (quota→plot→crop) · agronomic fields · photos 4 หมวด · verify/reject single+bulk · CSV upload · search/filter/sort/export · soft cancel/delete + reason
- **Full agronomic measurement panel:** ประเภทอ้อย (อ้อยใหม่/อ้อยตอ) · อายุอ้อยแบบคำนวณอัตโนมัติ (derived) · ขนาดลำ-ปล้อง-เส้นผ่านศูนย์กลาง-ความสูงหัว/กลาง/ท้าย · ชนิดดิน/ความหนาแน่นวัชพืช · พบโรค/ศัตรูพืช + รายละเอียด · รหัสไปรษณีย์ (ทั้งหมด optional)
- List รองรับ **Export CSV** (client-side ใน prototype · backend export = Pending Spec)

### §3.2 Out of Scope
แก้ไข Quota/Plot/Crop (อ่านอย่างเดียว) · วิเคราะห์/พยากรณ์ผลผลิตขั้นสูง · GIS map rendering

### §3.4 Scope Lock (→ FRD 00_OVERVIEW)
| LOCK | ข้อความ |
|---|---|
| **LOCK-01** | capability legacy คงครบ 100% |
| **LOCK-02** | canonical status 5: waiting_for_verify(init)/verified/rejected/cancelled/deleted |
| **LOCK-03** | **cascade บังคับ**: โควตา → แปลง(ของโควตา) → รอบปลูก(ของแปลง) → ฟอร์ม |
| **LOCK-04** | agronomic fields: พันธุ์อ้อย/ประมาณการผลผลิต/ขนาดแปลง + สีดิน/การตรวจสีใบ/โรค-ศัตรูพืช/พิกัด |
| **LOCK-05** | **photos 4 หมวด**: รูปกับแปลง/รูปพืชผล/รูปลำต้นในกอ/รูปสีดิน |
| **LOCK-06** | verify/reject: waiting เท่านั้น · verify note optional · **reject reason บังคับ** · เดี่ยว+bulk |
| **LOCK-07** | edit survey verified + save → กลับ waiting (สอดคล้อง Crop) |
| **LOCK-08** | CSV schema = create · ทุกแถว waiting · partial + report |
| **LOCK-09** | soft cancel/delete + reason + audit |
| **LOCK-10** | optimistic lock + idempotency + audit |
| **LOCK-11** | survey verified feeds Crop survey tab (read) |

## §4 Cross-Module Contract (→ FRD 02_API §2.X)
| Item | รายละเอียด |
|---|---|
| Read Quota→Plot→Crop | cascade bind (verified crops ของแปลงของโควตา) |
| Snapshot | farmer/plot/crop info read-only |
| Feeds Crop | survey verified → Crop F-AGM-004 อ่าน (แท็บสำรวจ) — **ไม่มี write-back** (Crop pull-read) |
| Engine | ENG-EXT-AGM `survey-source-connector` (read cascade) |

## §5 Personas & Permissions (→ invariants §6)
เจ้าหน้าที่สำรวจ (create/edit/csv/cancel/delete) · ผู้ตรวจสอบ (+verify/reject)

## §6 Data Requirements
T_survey (invariants §1) · T_survey_photo (4 หมวด) · T_survey_history · read Quota/Plot/Crop

## §7 Functional Stories
| US | Story |
|---|---|
| US-01 | เลือกโควตา→แปลง→รอบปลูก → กรอกข้อมูลสำรวจ + รูป → waiting |
| US-02 | cascade invalid → block |
| US-03 | CSV upload → N survey waiting + report |
| US-04 | ดูรายละเอียดสำรวจ (ข้อมูล/รูป/ประวัติ) |
| US-05 | Verify เดี่ยว → verified |
| US-06 | Reject เดี่ยว (+reason บังคับ) → rejected |
| US-07 | Bulk verify/reject (skip non-eligible + summary) |
| US-08 | แก้ไข survey → verified กลับ waiting |
| US-09 | Cancel/Delete (+reason) → cancelled/deleted |
| US-10 | ค้นหา/กรอง/sort/export |

## §11 Non-Functional
list p95<3s · create<1s · CSV 1,000<60s · photos policy · optimistic lock

## §12 Value Stream Impact
Farmer → Quota → Plot → Crop → **Survey (สำรวจภาคสนาม)** ⇢ ป้อนข้อมูลเข้า Crop (แท็บสำรวจ) → สนับสนุนการทำสัญญา/ประเมินผลผลิต

## §17 Open Questions → invariants §8 (OQ-SV1..SV5)

## §18 Dashboard Widgets
สำรวจทั้งหมด · รอตรวจสอบ · ยืนยันแล้ว · ปฏิเสธ

# 06_TESTS — F-AGM-009 Area & Permission Management

> Audience: QA + ai-testcase-md-generator · microcopy-aware · RBAC + geography + guard heavy

## §6.1 Acceptance Criteria

### Areas List (US-01)
- **AC-01** list แสดงพื้นที่ + 4 stats (พื้นที่ทั้งหมด/เปิดใช้งาน/Extension Codes/Area Heads)
- **AC-02** ค้นหา (ชื่อ/รหัส) · กรอง จังหวัด + สถานะ
- **AC-03** คอลัมน์ครบ (☑/ชื่อพื้นที่ link/จังหวัด/#Heads/#Codes/สถานะ pill/⋯)
- **AC-04** Export CSV → "กำลังเตรียมไฟล์ CSV"
- **AC-05** bulk select → "เลือกแล้ว N รายการ" · pagination "แสดง X-Y จาก Z รายการ"
- **AC-06** empty filter → "ยังไม่มีพื้นที่" / "ไม่พบรายการที่ค้นหา"

### Area Create (US-02)
- **AC-07** geography cascade: จังหวัด → อำเภอ(ของจังหวัด) → ตำบล(ของอำเภอ) → postal auto-fill
- **AC-08** สร้างสำเร็จ → เปิด detail ของพื้นที่ใหม่

### Area Detail + toggle (US-03)
- **AC-09** 4 แท็บ (Overview/Area Heads/Extension Codes/Audit) + header (status/อัปเดต)
- **AC-10** Overview: ข้อมูลพื้นที่ครบ + สรุป (Heads/Codes/เวอร์ชัน)
- **AC-11** toggle Active→Inactive, codes>0 → "ไม่สามารถปิดใช้งานพื้นที่ที่มีโค้ดที่ถูกใช้" (guard)
- **AC-12** toggle Inactive→Active → "เปลี่ยนสถานะสำเร็จ"

### Area Heads (US-04)
- **AC-13** เพิ่มหัวหน้า: ค้น ERP (ชื่อ/รหัส/email) → เลือก → "เพิ่มหัวหน้าพื้นที่สำเร็จ"
- **AC-14** ไม่เลือกพนักงาน → "กรุณาเลือกพนักงาน"
- **AC-15** employee inactive → "พนักงานไม่active"
- **AC-16** ลบหัวหน้า → confirm → "ลบหัวหน้าพื้นที่สำเร็จ"

### Extension Codes (US-05)
- **AC-17** สร้างโค้ด: เลือกพื้นที่(Active เท่านั้น) + 4 หลัก + หมายเหตุ → "สร้างโค้ดสำเร็จ"
- **AC-18** ไม่เลือกพื้นที่ → "กรุณาเลือกพื้นที่"
- **AC-19** โค้ดไม่ใช่ 4 หลัก → "รูปแบบหมายเลขโค้ดไม่ถูกต้อง"
- **AC-20** codes tab: EMPTY(ว่าง)/OCCUPIED(ใช้งานอยู่) + assigned + note

### Roles (US-06)
- **AC-21** Roles tab แสดงเฉพาะ SA/Director (ซ่อนถ้าไม่ใช่)
- **AC-22** Directors: เพิ่ม (ERP active) → "เพิ่ม Director สำเร็จ" · ลบ → "ลบ Director สำเร็จ"
- **AC-23** Extension Officers: codes cross-area + filter (พื้นที่/สถานะ EMPTY/OCCUPIED)
- **AC-24** Area Heads (global): รายการ head ทุกพื้นที่

### Audit (US-07)
- **AC-25** Audit timeline: action badge + actor_name + timestamp + details

### RBAC (US-08)
- **AC-26** SA/Director: เห็นปุ่ม สร้างพื้นที่/แก้ไข/toggle/เพิ่มหัวหน้า/Roles tab
- **AC-27** Area Head/Officer/Audit-QA: read-only (ปุ่ม write ซ่อน · Roles tab ซ่อน)

## §6.9 Cross-Module / Event Test Cases ⭐
| XT | Scenario | Source | Expected |
|---|---|---|---|
| XT-01 | เพิ่มหัวหน้า/director | ERP HR (read) | ค้นพนักงาน active · snapshot ชื่อ/email |
| XT-02 | geography cascade | Geo master (read) | อำเภอ/ตำบล/postal ตรงลำดับ |
| XT-03 | area scope | → Farmer/Quota (F-AGM-001/002) | area_id ใช้ scope เกษตรกร/โควตา (idempotent) |
| XT-04 | RBAC enforce | session role | write = 403 ถ้าไม่ใช่ SA/Director (server) |
| XT-05 | audit append | ทุก mutation | AuditEntry append-only + before/after (ไม่แก้ของเดิม) |

## §6.10 Microcopy-Aware Expected (verbatim)
| จุด | ข้อความ |
|---|---|
| tabs (root) | `Areas` · `Roles` |
| tabs (detail) | `Overview` · `Area Heads` · `Extension Codes` · `Audit` |
| tabs (roles) | `Directors` · `Area Heads` · `Extension Officers` |
| ปุ่ม | `สร้างพื้นที่` · `Export CSV` · `แก้ไข` · `เพิ่มหัวหน้าพื้นที่` · `สร้าง Extension Code` / `Create Code` · `เพิ่ม Director` · `เพิ่ม` · `ลบ` · `ยืนยัน` · `ยกเลิก` |
| area status | `เปิดใช้งาน`(Active) · `ปิดใช้งาน`(Inactive) |
| code status | `ว่าง`(EMPTY) · `ใช้งานอยู่`(OCCUPIED) |
| toast success | `เปลี่ยนสถานะสำเร็จ` · `เพิ่มหัวหน้าพื้นที่สำเร็จ` · `ลบหัวหน้าพื้นที่สำเร็จ` · `สร้างโค้ดสำเร็จ` · `เพิ่ม Director สำเร็จ` · `ลบ Director สำเร็จ` · `กำลังเตรียมไฟล์ CSV` |
| guard/error | `ไม่สามารถปิดใช้งานพื้นที่ที่มีโค้ดที่ถูกใช้` · `รูปแบบหมายเลขโค้ดไม่ถูกต้อง` · `กรุณาเลือกพื้นที่` · `กรุณาเลือกพนักงาน` · `พนักงานไม่active` |
| empty | `ยังไม่มีพื้นที่` · `ยังไม่มีหัวหน้าพื้นที่` · `ยังไม่มี Extension Codes ในพื้นที่นี้` |
| confirm | `ยืนยันลบหัวหน้าพื้นที่?` |

## §6.8 Trace: AC → Logic
| AC | API | FN |
|---|---|---|
| AC-01..06 | API-01/06 | FN-01 |
| AC-07..08 | API-02/GEO | FN-02,GEO |
| AC-09..12 | API-03/05 | FN-04(guard) |
| AC-13..16 | API-H1/H2 | FN-H,ERP |
| AC-17..20 | API-C1/C2 | FN-C |
| AC-21..24 | API-D1/D2/C2 | FN-D,C,RBAC |
| AC-25 | API-A1 | FN-AUDIT |
| AC-26..27 | (all write) | FN-RBAC |
> Coverage FN + FN-RBAC + FN-AUDIT ✅ · XT-01..05 ✅

## §6.6 Performance
list p95<3s · action<1s · RBAC server-enforced · audit append-only · geography integrity · optimistic lock

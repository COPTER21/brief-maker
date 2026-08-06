# _final-docs — Warehouse & Bin / คลังและตำแหน่ง

**Feature:** F-LOCATION-MASTER-001 · **Node:** Warehouse & Bin (Central Plan, Warehouse module W3)
**WF-01 pipeline: COMPLETE** (steps 1-9) · รวมเล่ม 2026-08-07

ชุดเอกสารส่งมอบ สกัดจาก HTML prototype (source of truth) ผ่าน pipeline HTML-first · ทุกไฟล์สอดคล้อง Decision Log (D1-D15) + Scope Lock

## ไฟล์ในชุดนี้
| # | ไฟล์ | คืออะไร | ใช้โดย |
|---|---|---|---|
| 01 | `01_WarehouseBin_prototype.html` | **HTML prototype** (source of truth) — เปิดใน browser เล่นได้ | ทุกฝ่าย / dev อ้าง UI จริง |
| 03 | `03_BRD_Warehouse_Bin.md` | **BRD** ฉบับสมบูรณ์ (18 sections, APPROVED) | PM / BA / stakeholder |
| 04 | `04_FRD_Pack/` | **FRD** pack 9 ไฟล์ (UI/API/Logic/DB/Rules/Tests/Locked/Index) | dev / architect |
| 05 | `05_UI_BRIEF_F-LOCATION-MASTER-001.md` | **UI Brief** สกัด 1:1 จาก HTML (tokens/z-index/route/anatomy/microcopy) | frontend dev |
| 06 | `06_testcases-F-LOCATION-MASTER-001.md` | **Test cases** 70 TC (สำหรับ AI browser agent / QA) | QA / automation |
| 07 | `07_UAT_testcase-warehouse-bin.html` | **UAT doc** end-user friendly (self-contained, ภาพจริง + ติ๊กผล + export PDF) | ผู้ทดสอบ / ลูกค้า |

## key facts (locked)
- 5 ระดับ: **Warehouse → Zone → Area → Rack → Location (ตำแหน่ง)** · flexible parent (rack XOR area, allows_direct gate)
- **branch_id** required บนคลังเท่านั้น (D3) · ไม่มี company_id · RBAC role-only 5 roles · delete = Manager/Admin
- **ไม่มี hard delete** — node = soft archive, location = soft decommission (GC#7/D11)
- dual-view: List (drill-down) + Hierarchy Tree (NON-STANDARD approved deviation, D12)
- **D15:** role switcher ถอดออก (production role มาจาก auth) · breadcrumb/full_path = ชื่อ (zone/area/rack) + code (WH/location), **ไม่มี branch ใน path** · branch เหลือเป็น field คลัง + คอลัมน์/filter List

## หมายเหตุ / known gaps
- BRD `.docx` ไม่ได้ gen (สคริปต์ md_to_docx.py ในตัว skill อ้าง path Linux ไม่มีบน Windows) — `.md` ครบสมบูรณ์
- UX-08: tree row ยังไม่มี keyboard/arrow-key nav (dev-handoff note)
- FRD FN-18 (applyTypeDefaults) = deferred Phase 3 · EC-14/15 + XT-01..04 ต้อง simulate (ยังไม่มี downstream page)

> ต้นฉบับแต่ละ step อยู่ที่ `../03_BRD` … `../07_UAT` · context/decisions อยู่ `../00_CONTEXT`

# 07_LOCKED_DECISIONS — F-LOCATION-MASTER-001 (v2)

| LD | Decision | Rationale |
|---|---|---|
| LD-01 | Flexible parent = rack XOR area, enforced by DB CHECK + app FN-13 | Bible §10.0 Iron Rule; differentiator vs SAP/Manhattan |
| LD-02 | parent=area requires area.allows_direct_location=true (trigger) | prevent uncontrolled floor placement |
| LD-03 | Location type enum = **10 core** (9 + PACK); ส่วนที่เหลือ schema-ready (drop CHECK เมื่อเปิดใช้) | controlled rollout; PACK รองรับ pick-pack-ship |
| LD-04 | Create/Edit = drawer slide-in (NOT modal) | html-generator-v3 Iron Rule #14 |
| LD-05 | Bulk-gen atomic with preview; no partial commit | data integrity |
| LD-06 | Deactivate/Decommission require stock=0; decommission soft-keeps history | audit + integrity |
| LD-07 | No DOA — operational master, RBAC only (Warehouse Manager owner) | Bible §11.1 |
| LD-08 | Global Engine IDs (ENG-LOC-GEN, ENG-HIER-PATH) assigned at CUBIC registration | convention |
| **LD-09** ⭐ | **CRUD เต็มทั้ง 5 ระดับ** (WH/Zone/Area/Rack/Location) ผ่าน UI เดียว; node code unique within parent; referential-safe delete | v2 enhancement — จัดการลำดับชั้นครบโดยไม่แตะ DB |
| **LD-10** ⭐ | **Dual-view** List (Pattern A) + Hierarchy tree+summary (**NON-STANDARD**) แชร์ state เดียวกัน | UX สำหรับ hierarchy; flag OQ-2 (อนุมัติ tree หรือไม่) |
| **LD-11** ⭐ | **Warehouse address** ดึงจาก **Geo Master** (read-only) แบบ cascade; postcode auto; เก็บ snapshot code+postcode | structured address; Geo Master เป็น feature แยก (OQ-1) |
| **LD-12** ⭐ | **Delete = Manager/Admin** เท่านั้น (Supervisor สร้าง/แก้ได้ ไม่ลบ) | SoD — แยกสิทธิ์ทำลายจากสิทธิ์สร้าง (ไม่มี approval ตาม LD-07) |

## Convention Deviations
- **LD-10 Hierarchy Tree view = NON-STANDARD** (ไม่มี tree pattern ใน html-generator-v3 A–I). คง CI/token มาตรฐาน + Iron Rules 31/31; รอ approve ที่ OQ-2. ถ้าไม่อนุมัติ → ตัด Tree view เหลือ List อย่างเดียว (ไม่กระทบ API/Logic/DB).
- อื่น ๆ follow CUBIC API/Engine + html-generator-v3 layout standards.

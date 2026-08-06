# AI_DEFAULTS — 11_Warehouse (F-LOCATION-MASTER-001)

> ค่า default ที่ AI ตั้งแทนคำตอบที่ยังไม่มี (Open Questions) — **user override ได้ทุกข้อ**
> ทุกข้อจะ propagate ลง HTML → BRD → FRD → testcase · ถ้าเปลี่ยน แก้ที่นี่แล้ว regen

| ID | ประเด็น (OQ เดิมใน FRD) | `[AI-DEFAULT]` ที่ใช้ | ผลต่อการ implement |
|---|---|---|---|
| **AD-1** | OQ-1: Geo Master feature ยังไม่มี — timeline/schema? | ใช้ **subset TH_GEO ฝังใน prototype** (จังหวัด/อำเภอ/ตำบล/ไปรษณีย์ ตัวอย่าง) · consume read-only · API จริง = Phase 2 | UI cascade ทำงานได้เลย · BE mock endpoint `/geo/*` |
| **AD-2** | OQ-2: Tree view NON-STANDARD เก็บไหม? | **เก็บ — dual-view (List + Hierarchy tree)** ตาม D12 (user ขอกลับ) · NON-STANDARD = approved deviation | 2 view แชร์ state · tree pane + summary panel |
| **AD-3** | OQ-3: type-driven default behavior flags auto-set เมื่อไหร่? | **Phase 3** — Phase นี้ตั้ง flags เอง (manual) · type=PACK/HOLD/DAMAGED ฯลฯ กำหนด default ไว้ใน contract แต่ยัง**ไม่ auto-apply** | FN-23 (applyTypeDefaults) = schema-ready แต่ยังไม่เปิดใช้ |
| **AD-4** | OQ-4: deactivate Zone ที่มี Area active → cascade หรือ block? | **BLOCK** (referential-safe) — ต้องจัดการลูกก่อน | สอดคล้อง BR-005/GC#7 |
| **AD-5** | OQ-5: reparent location — require empty vs live migration? | **require source empty** (ไม่มี live migration ในเฟสนี้) | FN-19 reparent block ถ้า stock≠0 |
| **AD-6** | branch master (Company/Organization) ยังไม่ต่อจริง | consume read-only + **mock branch list** ใน prototype (เช่น สนญ. / สาขา 1-2) · picker required ตอนสร้าง WH | เหมือน geo — BE mock จนกว่า Company พร้อม |
| **AD-7** | `loc_require_barcode` (BR-014 configurable) | **ON** by default (location ต้องมี barcode ก่อน activate) · admin ปิดได้ | config key |
| **AD-8** | branch มีผลต่อสิทธิ์ไหม? | **branch = filter/UX เท่านั้น** — ไม่ scope สิทธิ์ (role-only, D8) · branch-scoped RBAC = ฝาก Permission Matrix (Policy & Security) เป็น system-wide (future) | ทุก role เห็น/จัดการได้ทุกสาขา (กรองได้แต่ไม่ถูกบังคับ) |
| **AD-9** | default location ต่อคลัง | **DEFER** (D9) → pick-pack-ship phase | type enum เว้นที่ไว้ (RECEIVING_DOCK/STAGING/PACK) |

## Data classification (คงจาก legacy)
- ทุก owned column = **Internal** · geo reference = **Public** · ไม่มี Confidential/Restricted · PII overlay = created_by/modified_by
- `branch_id` = Internal (soft-ref code)

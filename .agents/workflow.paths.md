# แผนที่โฟลเดอร์ของ workspace นี้

> ไฟล์นี้คือที่เดียวที่เก็บ path จริงของ workflow หากย้ายโฟลเดอร์ให้แก้ที่นี่ไฟล์เดียว

| บทบาท | path จริง | สถานะ |
|---|---|---|
| `CENTRAL_PLAN` | `Central Plan v2/` | ยืนยันแล้ว 2026-08-14 |
| `BRIEF_ROOT` | `Pack Brief Feature/` | ยืนยันแล้ว 2026-08-14 |
| `OUTPUT_ROOT` | `outputs/` | ยืนยันแล้ว 2026-08-14 |
| `SHARED_E2E` | `outputs/_SHARED/_e2e/` | ยืนยันแล้ว 2026-08-14 |
| `PENDING_REGISTRY` | `outputs/_SHARED/DESIGN_SYSTEM_PENDING.md` | ยืนยันแล้ว 2026-08-14 |
| `LEGACY_CONTEXT` | `Related context/` | ยืนยันแล้ว 2026-08-14 |
| `SKILL_ROOT` | `.agents/skills/` | project-scoped |
| `VENV_PY` | `.tools/python.cmd` | workspace wrapper |
| `PLAYWRIGHT` | `.tools/playwright.cmd` | workspace wrapper |

## กติกาการอ้างถึง

- อ่าน `CENTRAL_PLAN` โดย list ก่อนและอ่านทุกไฟล์ที่พบ ห้ามล็อกรายชื่อไฟล์ไว้ล่วงหน้า
- `BRIEF_ROOT` เป็นจุดเริ่มค้นหาเท่านั้น ต้องให้ผู้ใช้ยืนยันแพ็กของแต่ละ feature ทุกครั้ง
- หนึ่ง feature ใช้หนึ่งโฟลเดอร์ใน `OUTPUT_ROOT`
- กฎและ skills อ้างชื่อบทบาท ห้ามฝัง path ธุรกิจจริงซ้ำไว้ที่อื่น

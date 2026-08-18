# แผนที่โฟลเดอร์ของ workspace นี้

> ⚠️ **ไฟล์นี้คือที่เดียวที่มี path จริง** — ย้ายโฟลเดอร์เมื่อไหร่ให้แก้ที่นี่ไฟล์เดียว
> `CLAUDE.md` และ `.claude/commands/kickoff.md` อ้างชื่อบทบาทเท่านั้น ห้ามเขียน path ลงไป
>
> 🪟 **เครื่องนี้เป็น Windows** — python ของ venv อยู่ที่ `Scripts/python.exe` (ไม่ใช่ `bin/python`)

| บทบาท | path จริง | สถานะ |
|---|---|---|
| `CENTRAL_PLAN` | `Central Plan v2/` | ✅ ยืนยันแล้ว 2026-08-18 |
| `BRIEF_ROOT` | `Pack Brief Feature/` | ✅ ยืนยันแล้ว 2026-08-18 |
| `OUTPUT_ROOT` | `outputs/` | ✅ ยืนยันแล้ว 2026-08-18 |
| `SHARED_E2E` | `outputs/_SHARED/_e2e/` | ✅ (มี `uikit.py`) |
| `PENDING_REGISTRY` | `outputs/_SHARED/DESIGN_SYSTEM_PENDING.md` | ✅ |
| `LEGACY_CONTEXT` | `Related context/` | ✅ ยืนยันแล้ว 2026-08-18 |
| `MEMORY_DIR` | `C:\Users\Admin\.claude\projects\C--Users-Admin-Desktop-Work-brief-maker\memory\` | ✅ |
| `VENV_PY` | `.claude/venv/Scripts/python.exe` | 🪟 Windows |

## กติกาการอ้างถึง

- อ่าน `CENTRAL_PLAN` = **`ls` ก่อนเสมอ แล้วอ่านทุกไฟล์ที่เจอ** — ห้ามล็อกรายชื่อไฟล์ไว้ในเอกสารใด ๆ
- `BRIEF_ROOT` เป็นแค่ **ที่ตั้งต้นของการค้นหา** — โฟลเดอร์ย่อยของแต่ละ feature ยัง **ต้องถามผู้ใช้ทุกครั้ง**
- feature หนึ่งตัว = 1 โฟลเดอร์ใน `OUTPUT_ROOT` ชื่อเดียวกับรหัส feature

## หมายเหตุ Windows (สำคัญ)

- รัน script ที่ใช้ browser/รูป: `.claude/venv/Scripts/python.exe <script>` (ไม่ใช่ `bin/python`)
- `self_audit.py` · `audit.sh` · `static_scan.py` · `coverage_checklist.py` เป็น stdlib ล้วน — ใช้ `python` (system) ได้ ต้องตั้ง `PYTHONIOENCODING=utf-8` กันปัญหา encoding ภาษาไทยบน Windows
- `python3` ไม่มีบนเครื่องนี้ — system python คือคำสั่ง `python` (3.13)
- pandoc อยู่ที่ `C:\Users\Admin\AppData\Local\Pandoc\pandoc` (นอก venv)

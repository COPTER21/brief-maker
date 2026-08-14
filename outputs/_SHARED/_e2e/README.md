# Shared E2E tools — Codex workspace

ไฟล์นี้เป็นคู่มือรันกลางของทุก feature อย่าคัดลอกวิธีรันไปไว้ใน README ราย feature

## โครงสร้าง

| ตำแหน่ง | หน้าที่ | อยู่ใน step 5 |
|---|---|:--:|
| `outputs/_SHARED/_e2e/uikit.py` | ตัวตรวจและ helper กลาง | — |
| `outputs/<FEATURE>/_e2e/e2e-<xx>.py` | เดินหน้าจอและ assert ทุก FN/FN-40 | ใช่ |
| `outputs/<FEATURE>/_e2e/ui-audit-<xx>.py` | geometry, contrast และ a11y | ตามเงื่อนไข |
| `outputs/<FEATURE>/_e2e/render-gate.py` | ภาพ before/after | ไม่อยู่ในเส้นทางปกติ |

## คำสั่งบน Windows

ใช้ wrapper ของ workspace เสมอ:

```powershell
.tools\python.cmd outputs\<FEATURE>\_e2e\e2e-<xx>.py outputs\<FEATURE>\<feature>.html
.tools\python.cmd outputs\<FEATURE>\_e2e\ui-audit-<xx>.py outputs\<FEATURE>\<feature>.html --quick
.tools\playwright.cmd install chromium
```

สำหรับ shell-based checks ของ skills ให้ใช้ `.tools\bash.cmd` ห้ามใช้ WSL `bash`

## Contract ของ E2E

- เปิด `FUNCTION_CHECKLIST_*.md` ก่อนเขียน E2E; ถ้าไม่มีให้สกัด FN จาก PREBRIEF
- ทุก FN ต้องมีอย่างน้อยหนึ่งเคสและใส่รหัสในชื่อเคส
- ทุก FN-40 ต้องเป็น negative case ที่ตรวจบน DOM ที่ render จริง
- ปิดท้ายด้วย `FN ครอบ x/y · เคสรวม n · ผ่าน p/n`
- Step 5 รัน feature E2E ตัวเดียว; `ui-audit` รันเพิ่มเมื่อ BASE-KIT เปลี่ยน,
  มี page CSS ใหม่มาก, ผู้ใช้พบ UI เพี้ยน, ก่อนส่งนอกทีม หรือผู้ใช้สั่งตรวจ UI
- Feature ใหม่ไม่ต้องสร้าง `render-gate.py` หรือ `_render/`

## Timing helpers

- `ready(pg, url)` หลังเปิดหน้า
- `settle(pg)` หลัง action ที่ทำให้ UI เปลี่ยน
- `after(pg, js)` หลัง evaluate JavaScript
- `hush(pg)` ก่อน screenshot

ห้ามเพิ่ม `wait_for_timeout`; helper เหล่านี้รอเงื่อนไขจริงและกรอง animation วนไม่รู้จบ

## การแก้ตัวตรวจ

- ห้ามสร้าง checker กลางตัวใหม่ ให้เพิ่มความสามารถใน `uikit.py`
- เมื่อเพิ่ม detector ให้พิสูจน์กับเวอร์ชันที่พังก่อน แล้วจึงคืนโค้ดที่แก้แล้ว
- ถ้าจะเปลี่ยน timing ของตัวตรวจ ให้เทียบอย่างน้อยสามรอบก่อนและหลัง ผลต้องคงที่
- `ui-brief-check.py` เป็น inventory/verification gate ไม่ใช้แทนการอ่าน HTML และคอมเมนต์จริง

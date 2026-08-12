# \_e2e — ทะเบียนหน่วยวัด (F-UOM-001)

## รันยังไง

```bash
# ตัวหลักของ step 5 — เดินจอจริง + assert (≈ 0:50)
.claude/venv/bin/python _final-docs/F-UOM-001/_e2e/e2e-uom.py _final-docs/F-UOM-001/uom-master.html

# หลักฐานภาพให้ด่าน qc-ux Pass R (≈ 0:25) — เขียนทับ _shots/
.claude/venv/bin/python _final-docs/F-UOM-001/_e2e/shots-uom.py _final-docs/F-UOM-001/uom-master.html
```

> ⚠️ **ต้องใช้ python ของ venv** — เครื่องนี้ไม่มี `python` และ `/usr/bin/python3` ไม่มี playwright
> ⚠️ **ต้องมี `_SHARED/_e2e/uikit.py`** — ทั้ง 2 ไฟล์ `import` จากที่นั่น (อยู่นอกโฟลเดอร์ feature)
> ถ้าแตกไฟล์จากซองส่งมอบแล้วอยากรัน ต้อง copy `uikit.py` มาไว้ที่ `_SHARED/_e2e/` ก่อน

## ไฟล์ในโฟลเดอร์นี้

| ไฟล์ | ทำอะไร |
|---|---|
| `e2e-uom.py` | **49 เคส** — เดินจอจริงแล้ว assert · ครอบ **22/22 FN ที่ทดสอบบนจอนี้ได้** + **FN-40 ครบ 6/6** |
| `shots-uom.py` | จับ **22 ภาพ** (1440 + 1024) ให้ Pass R ของ `qc-ux` — All-Tabs · Sticky-vs-Overlay · Bottom-Edge · Dropdown Anatomy · Responsive |

## ตัวหาร (บังคับตั้งแต่ 2026-08-10)

อ้าง `Brief Feature/2. UOM/FUNCTION_CHECKLIST_F-UOM_UoM-Master.md`

| | จำนวน | หมายเหตุ |
|---|:--:|---|
| FN บวก | 23 | FN-01…19 + FN-13b + FN-90/92/93 |
| **ทดสอบบนจอนี้ได้** | **22** | |
| ทดสอบที่นี่ไม่ได้ | 1 | **FN-07** — checklist เขียนเองว่า *"(ตรวจฝั่งสินค้า)"* คือ combobox ของ `F-PDM-001` · ดู `GAP-03` ใน `_COVERAGE_REPORT.md` |
| FN-40 (เคสเชิงลบ) | 6 | E37–E42 |
| ทะเบียนตั้งต้น | 35 หน่วย | 25 แถว/หน้า → แบ่งหน้า 2 หน้า (Strike 2026-08-10) |
| **รวมเคส** | **49** | |

## ผลล่าสุด

```
ผ่าน 49/49 · console errors = 0        (ทะเบียน 35 หน่วย · 25 แถว/หน้า · ≈ 0:55 ต่อรอบ)
```

## ทำไม FN-40 ต้องอยู่ที่ e2e ไม่ใช่แค่ step 4

`qc-coverage` grep โค้ดได้แค่ *"ไม่เจอคำนี้"* — **จับไม่ได้ถ้าปุ่มมีอยู่แต่ถูกซ่อน หรือโผล่เฉพาะบาง state**
`E37` / `E40` / `E41` จึงใช้ helper `walk_all_states()` เดิน **10 สถานะ** ต่อเคส
(list · list+bulk bar · create · edit · view×3 แท็บ · view+เมนูสถานะ · import จอเลือกไฟล์ · import จอ preview)
แล้วอ่าน **เฉพาะข้อความที่มองเห็นจริง** (กรอง `display:none` / `visibility:hidden` / `opacity:0` / ขนาด 0)

## เคสที่มีไว้ดักบั๊กที่เคยเกิดจริง

| เคส | ดักอะไร |
|---|---|
| **E47** | เมนูที่ `portalMenu()` แล้ว **จมใต้ลิ้นชัก** — เจอจริงตอน gen ไฟล์นี้ (page CSS ทับ z-index ของ `.menu-fixed` เพราะ specificity เท่ากันแล้วอยู่หลังในไฟล์) · ตรวจด้วย `elementFromPoint` ไม่ใช่แค่อ่านค่า z |
| **E48** | Esc ปิดลิ้นชักทั้งใบในครั้งเดียว — บั๊กเดิมของ template upstream ที่โปรเจกต์แพตช์ไปแล้ว |
| **E46** | หัวตาราง sticky **ทะลุ**ลิ้นชัก — เจอจริงที่ `F-COA-001` ตอน BASE-KIT ไม่ประกาศ `--z-*` |
| **E17** | กดปุ่มบันทึกรัว ๆ แล้วได้ record ซ้ำ |
| **E20** | แก้ไข record แล้วรหัสเดิมของตัวเองถูกตีว่า "ซ้ำ" |

## ข้อควรรู้เรื่อง state

mock อยู่ในหน่วยความจำล้วน (**ไม่มี localStorage/sessionStorage**) → `reset(pg)` = `ready(pg, HTML)`
คือการคืนข้อมูลตั้งต้น 35 หน่วย · เคสที่เปลี่ยนข้อมูล (สร้าง/ลบ/นำเข้า) จึงเรียก `reset()` ต้นกลุ่มเสมอ

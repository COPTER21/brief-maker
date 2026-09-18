# UX Check Report — F-WH-STKTRF / Stock Transfer

- วันที่: 2026-09-16 · Iteration: re-gate หลังปรับ landing filters / line editor / upload ตาม visual review
- Generator spec: `html-generator-v9.1` · Pattern Q + B2 v2 · compact form / placeholder / lean-cell / z-index registry
- Passes run: `audit.sh` · `static_scan.py` · render shots · visual inspection · feature E2E
- ไฟล์ที่ตรวจ: `F-WH-STKTRF.html`

## Verdict: 🟢 PASS (with 2 warnings)

| BLOCK | WARN | INFO | NOT-CHECKED |
|---:|---:|---:|---:|
| 0 | 2 | 3 | 0 |

## ผลตรวจหลัก

| Gate | ผล | Evidence |
|---|---|---|
| Iron rules | PASS | `audit.sh`: FAIL=0 · WARN=1 |
| Pattern Q / B2 v2 | PASS | wizard 5 ขั้น · view tabs detail/transit/pdf/sign/history · attachment ใน landing · line widths contract ครบ |
| Runtime | PASS | PM/BA re-gate 2026-09-17: E2E 19/19 · console error 0 · FN 61/61 · FIX-01–FIX-06/FIX-08 ผ่านครบ |
| Visual list | PASS | `_shots/landing_filter_expanded.png`: filter grid สมมาตรทั้งย่อ/ขยาย; ตารางมีผู้จัดทำ+เหตุผลย้าย; attachment strip ไม่ชน/ไม่ล้น |
| Visual wizard | PASS | `_shots/wizard_line_editor_aligned.png` + `_shots/wizard_upload_file.png`: line columns ใช้ colgroup เดียวกัน; file input เลือกไฟล์จริงและแสดงรายการไฟล์ |
| Visual re-gate | PASS | `_shots/feedback_regate.png`: landing/table/filter/attachment ยังนิ่งหลังแก้ PM/BA feedback |
| Offline icons | PASS | local SVG fallback render จริงเมื่อ CDN ใช้ไม่ได้; E2E พบ `svg.lucide` และภาพ fresh แสดง icon |
| Printable A4 | PASS | `_trf-preview.png`: 1 หน้า A4, route ผ่าน in-transit, totals และลายเซ็น 4 ช่องไม่ล้น |

## 🟡 WARN

### UX-01 · Token hygiene — hardcoded font-size เดิมใน BASE-KIT/Pattern Q

- `audit.sh` แจ้ง WARN 1 กลุ่มจาก `font-size` แบบ px ที่มีอยู่ใน seed component เดิม
- ไม่มีค่านอก CI ที่เป็น user-visible defect และไม่ทำให้ density/layout fail; จึงไม่บล็อก gate รอบนี้
- `self_audit.py` รุ่นเดิมนับ dynamic inline layout/template strings และ class tab ของ Pattern Q เป็น failure จำนวนมาก แม้ `audit.sh` v9.1, static facts, render และ runtime ผ่าน จึงบันทึกเป็น checker-compatibility warning ไม่แกล้งรายงานว่าเป็นศูนย์

### UX-02 · External font/CDN resilience

- ฟอนต์ Satoshi/Noto Sans Thai ยังโหลดจาก CDN; offline จะใช้ system fallback ตาม CSS
- Lucide ได้เพิ่ม local SVG fallback แล้ว จึงไม่เหลือช่อง icon ว่างในโหมด offline

## ℹ️ INFO — สิ่งที่แก้จาก fresh gate

- เติม v9.1 contract: `--c-placeholder`, compact field error, `.nw`, header flex และ z-index registry
- จัด filter ใหม่เป็น grid หลัก 1 แถว + advanced panel 3 ช่อง; ย้ายผู้จัดทำเข้า search หลักและตัด dropdown ซ้ำซ้อนออก
- เพิ่มคอลัมน์ `ผู้จัดทำ` และ `เหตุผลย้าย` เพื่อให้ผู้ทดสอบเทียบผล filter กับข้อมูลในตารางได้ทันที
- ล็อกแนว line editor ด้วย `table-layout: fixed` + `colgroup` และเปลี่ยน step เอกสารแนบเป็น file picker/drag-and-drop จริง (PDF/JPG/PNG)
- คง “เอกสารแนบล่าสุด” บน landing เพราะเป็น FN-53/Pattern Q แต่ปรับ copy/spacing ให้กลมกลืนกับหน้า

## สรุป

ไม่มี BLOCK เหลือบน HTML bytes ล่าสุด; PASS นี้คำนวณใหม่จากเครื่องมือและภาพ fresh ไม่ได้นำคำว่า PASS ที่ฝังอยู่ใน pack มาใช้แทนการตรวจ

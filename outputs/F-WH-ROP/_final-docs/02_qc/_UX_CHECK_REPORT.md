# UX Check Report — F-WH-ROP

- วันที่: 2026-09-18 · Iteration: 12 (PM/BA re-gate)
- Generator spec: html-generator-v9.1
- Passes run: self_audit.py · audit.sh · static_scan.py · render-check 1440×900 · render-check 1024×768 · feature E2E
- ไฟล์ที่ตรวจ: `F-WH-ROP.html`

## Verdict: 🟢 PASS (with 1 warning)

| BLOCK | WARN | INFO | NOT-CHECKED |
|---:|---:|---:|---:|
| 0 | 1 | 2 | 0 |

## หลักฐานที่ผ่าน

- Mechanical self-audit: ตัวนับทุกหมวดเป็น 0 และมี PREFLIGHT v9.1
- CI/structure: sidebar 232/58, topbar 52, drawer 920, scrollbar 5, hash routes 3 เส้น, Escape handler, overlay root และ portal dropdown ครบ
- Render 1440×900: ตารางชิดพื้นที่ล่างและเลื่อนภายใน; header/pill/ปุ่มและข้อความไทยไม่ชนขอบ
- Render 1024×768: sidebar ย่อเป็น rail โดยโลโก้และไอคอนยังเห็น; ไม่มี horizontal overflow
- Drawer คำแนะนำ: แสดง ATP, จุดสั่งเติม, ที่มาจาก Safety+ADU×Lead Time, On-Order, เป้าหมาย Max+Safety, Pack Size และจำนวนแนะนำครบ
- ตารางคำแนะนำ: แยกสถานะต่ำกว่าจุด/ใกล้จุด/ปกติด้วยสีแดง/ส้ม/เขียว และมี KPI ใกล้จุด
- Loading: รันตรวจ/สร้าง PR/ส่งแจ้งเตือน disable ปุ่มและแสดง “กำลัง…” 500ms ป้องกันกดซ้ำ
- Demo-only: ซ่อน `.demo-only` แล้วไม่เหลือข้อความตัวอย่างบนจอและ layout ไม่เปลี่ยน
- Offline icons: ฝัง Lucide fallback สำหรับ warehouse/search/reset/close; ไม่มีช่องไอคอนว่าง
- E2E: FN 8/8, cases 8/8, console errors 0

## 🟡 WARN

### UX-01 · Fixed token migration · CSS line 3

- พบ: CSS ของ seed เดิมยังใช้ค่า `font-size` แบบตัวเลขบางจุดแทน `--fs-*`
- ผล: audit.sh แจ้ง WARN แต่ค่าที่ใช้ตรงกับสเกลปัจจุบันและ render ไม่ผิดรูป
- ส่งต่อ: ย้ายเป็น token กลางเมื่อ BASE-KIT ของ seed ถูก migrate; ไม่ควรแก้ shared convention จาก feature นี้

## Loop Diff

| สถานะ | รายการ |
|---|---|
| ✓ แก้แล้ว | ตารางยาวทะลุ viewport → internal scroll |
| ✓ แก้แล้ว | sidebar 1024 เหลือแถบแดงว่าง → rail icon |
| ✓ แก้แล้ว | Lucide ไม่ render offline → inline fallback |
| ✓ แก้แล้ว | Validation รวมท้ายฟอร์ม → error ใต้ช่องที่ผิด + กรอบแดง + aria-invalid |
| ✓ แก้แล้ว | Dropdown สินค้าเปิดเองและค้างบน overlay หลังปิด Drawer → ไม่ auto-focus combobox และล้าง portal ตอน close |
| ✓ แก้แล้ว | ข้อความ Drawer/ประวัติแสดงรหัส event ฝั่ง Dev → ใช้ข้อความผู้ใช้ “ส่งแจ้งเตือนแล้ว” และชื่อกิจกรรมภาษาไทย |
| ✓ แก้แล้ว | ตารางประวัติแสดง kind/ref ภายใน → แทนด้วยรายการ รายละเอียด สินค้า คลัง เวลา และสถานะภาษาคน |
| ✓ แก้แล้ว | ผลแจ้งเตือนสำเร็จซ้ำใน Drawer → แสดงเฉพาะ Toast; Drawer สงวนไว้สำหรับ error |
| ✓ แก้แล้ว | ผลสร้าง PR Draft สำเร็จซ้ำใน Drawer → แสดงเฉพาะ Toast; เลข Draft และรายละเอียดดูในแท็บประวัติ |
| ✓ แก้แล้ว | Search dropdown ในหน้าตรวจคู่สินค้า×คลังอยู่ใต้ Drawer → ยก layer ให้ตัวเลือกแสดงเหนือ Drawer และเลือกได้จริง |
| ✓ แก้แล้ว | ผลตรวจ “ยังไม่มีนโยบาย” ชิดช่องเลือกเกินไป → แยกส่วนด้วยระยะห่าง 24px และเส้นคั่น โดยไม่กินพื้นที่ก่อนตรวจ |
| ✓ แก้แล้ว | ผลตรวจไม่มีนโยบายดูเป็นข้อความชั่วคราว → ปรับเป็น status card พร้อมสินค้า คลัง และปุ่มเพิ่มนโยบายที่ prefill ค่าเดิม |
| ✓ แก้แล้ว | Safety Stock ตั้งค่าได้แต่ไม่กระทบผล → ใช้ในจุดสั่งเติมและเป้าหมาย Max+Safety พร้อมแสดงที่มาบนจอ |
| ✓ แก้แล้ว | มีเพียง 2 ระดับสถานะ → เพิ่ม “ใกล้จุด” พร้อม KPI และสีสถานะ 3 ระดับ |
| ✓ แก้แล้ว | ไม่มี automation/contract/CSQ anchors → เพิ่ม scheduler+movement, F009→F085→F072 และแก้ CSQ ตามมติล่าสุดให้เหลือ `master.changed → SecC` เท่านั้น |
| ✓ แก้แล้ว | ฟอร์มตั้งผู้ขายหลักไม่ได้ → เพิ่ม search dropdown แบบ optional และส่งเข้า `vendor_suggests` |
| ✓ แก้แล้ว | ปุ่ม automation กดรัวได้ → เพิ่ม `_busy`, disabled และ loading label |
| ✓ แก้แล้ว | Scaffold ของ feature อื่นค้างในไฟล์ → ลบทั้งหมด; grep 4 รหัสต้องห้าม = 0 |

## ภาพหลักฐาน

- `_shots/desktop.png`
- `_shots/viewport-1024.png`
- `_shots/suggestion-drawer.png`
- `_shots/validation-field.png`
- `_shots/history-human.png`
- `_shots/re-gate-1440.png`
- `_shots/re-gate-1024.png`

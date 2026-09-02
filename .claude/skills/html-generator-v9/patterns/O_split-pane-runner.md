# Pattern O — Split-Pane Runner (Checklist / Execution Page)

> **v6.1** — สกัดจาก Checklist Test Run (F-QA-002). ใช้กับหน้า "ทำงานไล่ทีละรายการ"
> ที่มี navigator รายการอยู่ข้าง ๆ + พื้นที่ทำงานหลัก เช่น test-case runner, UAT checklist,
> approval queue, document review queue, onboarding checklist.
> อ้างอิง convention เดียวกับ test runner มาตรฐาน (TestRail/qTest): **list ซ้าย · execution ขวา**

---

## 🎯 When to Use

✅ ผู้ใช้ต้องไล่ทำ/ตรวจรายการทีละตัวจนครบชุด (run test, approve batch, review docs)
✅ ต้องเห็นภาพรวมความคืบหน้า + กระโดดข้ามรายการได้ตลอดเวลา
✅ แต่ละรายการมี sub-steps ที่ต้องติ๊กผลรายขั้น

❌ list ธรรมดาที่เปิด view ทีละตัว (ใช้ Pattern A + C)
❌ ฟอร์มสร้าง/แก้ไข (ใช้ Pattern B)

---

## 🏗️ Structure (ตำแหน่งตายตัว)

```
.ph  — ชื่อชุด + status pill + actions (กลับรายการ = secondary · action หลัก = primary ขวาสุด)
.run-shell (flex, gap 18px)
  ├─ aside.run-aside  ← ★ ซ้ายเสมอ · 300px · position:sticky top=calc(shell+16px)
  │   └─ .card
  │       ├─ .aside-head   — ชื่อ "รายการ…" + ตัวนับ X/Y + progress bar 7px + legend จุดสี
  │       └─ .aside-list   — จัดกลุ่ม: .aside-grp (caption + ตัวนับต่อกลุ่ม X/Y)
  │                          → .aside-case (id + title truncate + .rdot สถานะ)
  └─ .run-main (flex:1, min-width:0)  ← เนื้อหารายการปัจจุบัน
      ├─ .card รายการปัจจุบัน
      │   ├─ header: id + pri-chip + result pill → title (--fs-h2) → meta บรรทัดเล็ก
      │   ├─ .case-meta (grid 118px/1fr) — บริบท เช่น ทำไมต้องทำ / เตรียมก่อนเริ่ม
      │   ├─ .step-head — หัวตารางขั้นตอน (บังคับ ห้าม list ลอยไร้หัว)
      │   └─ .step-row × N — checklist รายขั้น
      ├─ .card ข้อมูลประกอบ (data sample + ปุ่ม copy รายค่า)
      ├─ .card หมายเหตุ (textarea)
      └─ แถวปุ่มนำทาง: ก่อนหน้า (secondary) · spacer · action รวม (secondary) · ถัดไป/สรุปผล (primary)
```

## 📐 Grid ของ step checklist (ค่าที่จูนแล้ว)

```css
.step-head, .step-row { display:grid; grid-template-columns: 40px 1.2fr 1fr 92px 150px; gap:14px; }
/* ลำดับ | สิ่งที่ทำ (กว้างสุด) | สิ่งที่ต้องเห็น | ภาพ | ผล (ชิดขวา) */
.step-head { padding:9px 18px 7px; background:var(--c-bg-off); border-bottom:1px solid var(--c-line-2);
  font-size:var(--fs-cap); font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:var(--c-mute-2); }
.step-row  { padding:14px 18px 12px; border-bottom:1px solid var(--c-line-2); align-items:start; }
.step-row.is-pass { background: rgba(31,157,85,0.04); }
.step-row.is-fail { background: rgba(230,46,36,0.04); }
```
- **head กับ row ต้องใช้ grid เดียวกันเป๊ะ** — verify ด้วย bounding-box ว่า x ของคอลัมน์ตรงกัน
- ผลรายขั้น = ปุ่มคู่ toggle (`ผ่าน`/`ไม่ผ่าน` — กดซ้ำ = ยกเลิก), เลือกแล้วทั้งแถวติด tint + วงลำดับเปลี่ยนเป็น check/x
- ภาพประกอบ = thumbnail คลิกขยายผ่าน modal (`.modal.is-shot` ~860px) — cursor:zoom-in

## 🧭 Navigator (aside) rules

- **ซ้ายเสมอ** 300px sticky (`top: calc(var(--shell-h) + 16px)`, `max-height: calc(100vh - shell - 34px)`, list ภายใน scroll เอง)
- จุดสถานะ `.rdot` 9px: เทา=ยังไม่ทำ · เขียว=ผ่าน · แดง=ไม่ผ่าน · ส้ม=ค้างกลางคัน — สีตรง semantic tokens
- รายการปัจจุบัน: bg tint primary 7% + แถบซ้าย 3px primary (ภาษาเดียวกับ sidebar active)
- หัวกลุ่ม: caption uppercase + ตัวนับ `เสร็จ/ทั้งหมด` ต่อกลุ่ม
- Resume rule: เข้า runner ให้เปิด "รายการแรกที่ยังไม่เสร็จ" ไม่ใช่รายการแรกเสมอ

## 🔁 Behavior

- ติ๊กผลแล้ว **บันทึกอัตโนมัติ** (ไม่มีปุ่ม save) + `// BACKEND:` anchor สำหรับ sync
- "ผ่านทุกขั้นตอน" = mass-pass ของรายการปัจจุบัน + toast + auto-advance ไปรายการถัดไป
- ครบทุกรายการ → สถานะชุดเปลี่ยนเป็นเสร็จสิ้น + จดประวัติรัน + ปุ่มถัดไปกลายเป็น "สรุปผล" → หน้า report (Pattern K)
- textarea หมายเหตุ: `oninput` เขียน state ตรง ๆ ห้าม re-render ทั้งหน้า (กัน focus หลุด — Rule #29)

## ⚠️ Common Mistakes

1. ❌ วาง list ไว้ขวา — convention ของ execution tool คือ navigator ซ้าย
2. ❌ step list ไม่มีหัวตาราง → ผู้ใช้ไม่รู้ว่าคอลัมน์ไหนคืออะไร
3. ❌ head/row คนละ grid → คอลัมน์เหลื่อม (ตรวจ x-align ก่อนส่ง)
4. ❌ ปุ่มผลเป็น checkbox เดี่ยว (แยกไม่ออกว่า "ไม่ผ่าน" หรือ "ยังไม่ทำ") — ต้อง 3 สถานะ
5. ❌ aside ไม่ sticky → เลื่อนลงแล้วหลงว่าอยู่รายการไหน

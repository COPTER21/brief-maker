# PRINT SPEC — แบบฟอร์มรายงานผลการสอบทานคำขอซื้อและใบสั่งซื้อค้างนาน (PR/PO Outstanding) (PPO)

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD/Brief ของ F-TMP-005
> ไฟล์คู่: `FM-PUR-03_template.html` (template build แล้ว · fonts ฝัง) · `out/<state>.html` (5 สถานะ) · `out/_states_sheet.png`
> **โหมด:** Replica (แบบฟอร์มลูกค้า) · **2 หน้า** (thai-doc R10)
> ⚠ **[NO-BROWSER]** เครื่อง workspace ไม่มี browser → ไม่ได้รัน `render_pdf.py` (ใน render_states) / `compare_original.py` · ภาพ `out/_states_sheet.png` render จาก `out/<state>.html` ชุดเดียวกันด้วย Chromium ใน container ของ agent (ทุกสถานะ 2 หน้า ไม่ล้น) — ต้องรัน `render_states.py --max-pages 2` + `compare_original.py` บนเครื่องที่มี browser ก่อนส่งมอบจริง

## 1. สรุป
- **ประเภทเอกสาร:** รายงานผลการสอบทาน PR/PO ค้างนาน (report archetype · มีผู้จัดทำ + ผู้มีอำนาจอนุมัติ)
- **ขนาด:** A4 แนวตั้ง · **2 หน้า ทุกสถานะ** — ต้นฉบับ A4 แนวนอน (ชีต 1 Rev.02) แต่ engine ล็อก A4 แนวตั้ง (base.css ห้ามแก้) → จัดคอลัมน์ใหม่ตามสัดส่วนเดิม
- **ฟอนต์:** Sarabun ฝัง · เนื้อ 8pt (ไม่ต่ำกว่า 8pt) · หัวเรื่อง 11pt

## 2. Field Mapping
| ช่องในเอกสาร | Source | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| หัวกระดาษ (โลโก้) + ชื่อเอกสาร 2 บรรทัด | Organization snapshot · doccfg | — | ✓ | |
| ข้อมูลคำขอซื้อ/ใบสั่งซื้อค้างนาน | ข้อความคงที่ | — | — | หัวข้อส่วน |
| วันที่รายงาน : | ppo.report_date | วันที่ไทยเต็ม | ✓ | |
| หน่วยงาน : | ppo.org_unit_name | ข้อความ | ✓ | ผังองค์กร |
| ผู้จัดทำรายงาน : · ตำแหน่ง : | Employee snapshot | ข้อความ | ✓ | |
| ตาราง 13 คอลัมน์ (ลำดับ … แนวทางการแก้ไข) | ppo_items | ดู data contract | ✓ | ถ้อยคำหัวตาราง 1:1 |
| ลงชื่อ ผู้จัดทำ : | ผู้สร้างใบ | "ส่งในระบบ วันที่ เวลา" | ✓ | |
| ลงชื่อ ผู้มีอำนาจอนุมัติ (+ขั้น DOA อื่น) | approval_chain | ☑ อนุมัติ / ☑ ไม่อนุมัติ + "พิจารณาในระบบ …" | ✓ | 1 ช่องต่อขั้น DOA |
| Doc No. / Rev. | print_config | `FM-PUR-03 · Rev. 02 : 16/6/2026` | ✓ | footer ขวา + "หน้า n/2" |

## 3. กติกาคำนวณ
- ไม่มีสูตร · แถวว่าง/การแบ่งหน้าทำใน data (template ไม่นับ)

## 4. กติกาการพิมพ์ (R10 — 2 หน้า)
- หน้า 1: หัวกระดาษ + 4 บรรทัดข้อมูลผู้จัดทำ + ตารางแถว 1–12 (เติมแถวว่างขั้นต่ำ 8 = จำนวนบรรทัดบนกระดาษ) + "มีต่อหน้าถัดไป"
- `.page-break` ตั้งใจหลังตารางหน้า 1
- หน้า 2 (ใบต่อ): หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่ + วันที่รายงาน) + หัวตารางซ้ำ + แถว 13–24 (ขั้นต่ำ 5 แถวว่าง · สูงสุด 12) + บล็อกลงชื่อทั้งก้อน (`.signs-block`)
- footer ทุกหน้า: เลขที่ · (ร่าง) · Doc. No. · Rev. · "หน้า n/2"
- ตาราง 37 คอลัมน์ฐาน (ลำดับ 2 · PR 3 · PO 3 · วันที่สั่งซื้อ 3 · วันที่รับ 3 · ผู้ผลิต 3 · รายละเอียด 4 · จำนวน 2 · หน่วย 2 · ฝ่าย/แผนก 3 · สาเหตุ 3 · สถานะ 3 · แนวทาง 3) — ไม่มี style ใน body
- รายการ > 24 แถว: แบบพิมพ์ 2 หน้ารับไม่ได้ → OQ (ใบต่อหน้า 3+ หรือแนบ CSV) · prototype เตือนตอนเปิด PDF
- รอบแรก 18+20 แถว/หน้า → ภาพ Chromium ล้นเป็น 3–4 หน้า (ข้อความในคอลัมน์แคบตัด 3 บรรทัด) → ปรับเป็น 12+12 และขยายคอลัมน์วันที่ → 2 หน้าทุกสถานะ

## 5. วิธี build ใหม่
```bash
python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มรายงานผลการสอบทานคำขอซื้อและใบสั่งซื้อค้างนาน (PR/PO Outstanding)" --max-pages 2
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare --region 0:0.72
```

## 6. Checklist ก่อนส่งมอบ
- [x] parity IDENTICAL 5/5 · ไม่มี `{{}}` หลง · ไม่มี key ขาด
- [x] โครง 2 หน้าเท่ากันทุกสถานะ (นับ `.doc-page` + ภาพ Chromium 2 หน้าทุกสถานะ)
- [ ] **ยังไม่ได้ทำบนเครื่อง workspace (NO-BROWSER):** PDF จาก render_states · compare_original

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `3. FM-PUR-03 PR-PO_Outstanding.xlsx` ชีต 1 `PR-PO_(Outstanding)_Form` · พิมพ์ FM-PUR-003 · Rev. 02 : 16/6/2026 (ชีต 2 REV.00 แนวตั้ง = ฉบับเก่า)
- Profile token ที่ต่างจาก default: form_fs 8pt · form_lh 1.3 · title 11pt · logo 11mm ชิดซ้าย · grid pad 2px · row 7mm (dense 5.6mm) · หัวตารางพื้นเทา #D9DEE7 (ตามกระดาษ) · fill_l 90mm
- ความต่างจากกระดาษ (ตั้งใจ):
  1. A4 แนวนอน → แนวตั้ง (engine ล็อก) · คอลัมน์/ถ้อยคำ/ลำดับครบ 1:1
  2. แบ่ง 2 หน้า (R10): ตารางหน้า 1 + ใบต่อ/ลงชื่อ DOA N ขั้นหน้า 2 · รองรับแถวเกินกระดาษ (G4)
  3. ลายเซ็นเป็นแถวล่าง 1 ช่องต่อขั้น DOA · "ส่งในระบบ/พิจารณาในระบบ" แทนลายมือ (G6) · ผู้จัดทำ/ผู้มีอำนาจอนุมัติ บนกระดาษวางซ้อนแนวตั้ง → ระบบวางเรียงแถว
  4. รหัสฟอร์มใช้ FM-PUR-03 จาก doccfg (กระดาษพิมพ์ FM-PUR-003) — รอลูกค้ายืนยัน
- ผล compare_original: **ยังไม่ได้รัน [NO-BROWSER]** · คาดว่า WARN เพราะเปลี่ยนแนวกระดาษ — ต้องให้คนดูภาพวางคู่

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- ตาราง contract: `PPO_data-contract.md` · parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: ร่าง (3 แถว) · อนุมัติแล้ว (8 แถว = กระดาษ) · ไม่อนุมัติ (5 แถว) · ยาว 24 แถว (dense · หน้า 2 มี 12 แถว) · DOA 6 ขั้น (12 แถว · 7 ช่อง 4+3) → 2 หน้าทุกสถานะ

## 9. (Replica) print_config
ดู `print_config.json` (doc_type PPO · pages 2 · rows_page1 12 · rows_page1_min 8 · rows_page2_min 5 · rows_page2_max 12 · sign_boxes requester + doa_step:* · decision_words by_role role-mgr-pur)

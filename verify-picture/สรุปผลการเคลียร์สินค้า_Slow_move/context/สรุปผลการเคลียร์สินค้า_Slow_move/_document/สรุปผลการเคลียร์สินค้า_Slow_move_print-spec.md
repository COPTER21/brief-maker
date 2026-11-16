# PRINT SPEC — สรุปผลการเคลียร์สินค้า Slow move (SMC)

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD/Brief ของ F-TMP-003
> ไฟล์คู่: `FM-WHS-09_template.html` (template build แล้ว · fonts ฝัง) · `out/<state>.html` (5 สถานะ) · `out/_states_sheet.png`
> **โหมด:** Replica (แบบฟอร์มลูกค้า) · **2 หน้า** (thai-doc R10)
> ⚠ **[NO-BROWSER]** เครื่อง workspace ไม่มี browser → ไม่ได้รัน `render_pdf.py` (ใน render_states) / `compare_original.py` · ภาพ `out/_states_sheet.png` render จาก `out/<state>.html` ชุดเดียวกันด้วย Chromium ใน container ของ agent (ทุกสถานะ 2 หน้า) — ต้องรัน `render_states.py --max-pages 2` + `compare_original.py` บนเครื่องที่มี browser ก่อนส่งมอบจริง

## 1. สรุป
- **ประเภทเอกสาร:** สรุปผลการเคลียร์สินค้า Slow move ประจำเดือน
- **ขนาด:** A4 แนวตั้ง (210×297mm) · **2 หน้า ทุกสถานะ** — ต้นฉบับ A4 แนวนอน 1 หน้า (scale 78%) แต่ engine ล็อก A4 แนวตั้ง (base.css ห้ามแก้) → จัดคอลัมน์ใหม่ตามสัดส่วนเดิม
- **ฟอนต์:** Sarabun ฝัง · เนื้อ 8.5pt (ไม่ต่ำกว่า 8pt) · หัวเรื่อง 11pt

## 2. Field Mapping
| ช่องในเอกสาร | Source | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| หัวกระดาษ (โลโก้ · ชื่อบริษัท · ที่อยู่) | Organization snapshot | — | ✓ | ตอนออกเลข |
| ประจำเดือน | smc.clearance_month | เดือนไทย พ.ศ. | ✓ | ต่อท้ายหัวเรื่องบรรทัดเดียวกัน (ตามกระดาษ) |
| ลำดับ | smc_items.seq | 1..n | ✓ | |
| รหัสสินค้า · รายละเอียด | T_product (F-PRODUCT-MASTER-001) | ข้อความ | ✓ | snapshot ตอนบันทึก |
| วันที่ติดตาม | smc_items.follow_up_date | dd/mm/yy | ✓ | |
| แนวทางการเคลียร์ | smc_items.clearance_method | ข้อความ | ✓ | ตัวเลือกจาก SlowMoveConfig |
| วันที่ · จำนวน | smc_items.cleared_date · cleared_qty | dd/mm/yy · #,##0 | คู่กัน | ผลการเคลียร์ (DEC-13) |
| วันหมดอายุ | smc_items.expiry_date | dd/mm/yy | — | |
| หมายเหตุ | smc_items.remark | ข้อความ | — | |
| ลงชื่อ ผู้จัดทำ | ผู้สร้างใบ | "ส่งในระบบ วันที่ เวลา" | ✓ | |
| ลงชื่อ ผู้อนุมัติ (+ขั้น DOA อื่น) | approval_chain | ☑ อนุมัติ / ☑ ไม่อนุมัติ + "พิจารณาในระบบ …" | ✓ | 1 ช่องต่อขั้น DOA |
| Doc. No. / Rev. | print_config | `FM-WHS-09 · Rev.00 : 01/07/2569` | ✓ | footer ขวา + "หน้า n/2" |

## 3. กติกาคำนวณ
- ไม่มีสูตรตัวเลข · แถวว่างเติมใน data (template ไม่นับ)

## 4. กติกาการพิมพ์ (R10 — 2 หน้า)
- หน้า 1: หัวกระดาษ + หัวเรื่อง/ประจำเดือน + ตาราง 23 แถว (เท่ากระดาษ) + "มีต่อหน้าถัดไป"
- `.page-break` ตั้งใจหลังตารางหน้า 1
- หน้า 2 (ใบต่อ): หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่ + ประจำเดือน) + หัวตารางซ้ำ + แถว 24 ขึ้นไป (ขั้นต่ำ 5 แถวว่าง · สูงสุด 30) + บล็อกลงชื่อทั้งก้อน (`.signs-block`)
- footer ทุกหน้า: เลขที่ · (ร่าง) · Doc. No. · Rev. · "หน้า n/2"
- ตาราง 27 คอลัมน์ฐานเท่ากัน (ลำดับ 2 · รหัส 3 · รายละเอียด 6 · วันที่ติดตาม 2 · แนวทาง 5 · วันที่ 2 · จำนวน 2 · วันหมดอายุ 2 · หมายเหตุ 3) — ไม่มี style ใน body
- ภาพ Chromium (container): หน้า 1 ≈ 250mm (23 แถว มีตัดบรรทัด) · หน้า 2 ≈ 175mm (22 แถว + ลงชื่อ) / DOA 6 ขั้น 2 แถว พอดีหน้า

## 5. วิธี build ใหม่
```bash
python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "สรุปผลการเคลียร์สินค้า Slow move" --max-pages 2
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare --region 0:0.72
```

## 6. Checklist ก่อนส่งมอบ
- [x] parity IDENTICAL 5/5 · ไม่มี `{{}}` หลง · ไม่มี key ขาด
- [x] โครง 2 หน้าเท่ากันทุกสถานะ (นับ `.doc-page` + ภาพ Chromium 2 หน้าทุกสถานะ)
- [ ] **ยังไม่ได้ทำบนเครื่อง workspace (NO-BROWSER):** PDF จาก render_states · compare_original

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `9. FM-WHS-09 สรุปผลการเคลียร์สินค้า Slow Move.xlsx` · Doc No. FM-WHS-09 · Rev.00 : 01/07/2569
- Profile token ที่ต่างจาก default: form_fs 8.5pt · form_lh 1.3 · title 11pt · logo 11mm ชิดซ้าย · grid pad 2px · row 6.2mm (dense 5.4mm) · fill_m 45mm
- ความต่างจากกระดาษ (ตั้งใจ):
  1. A4 แนวนอน → แนวตั้ง (engine ล็อก) · คอลัมน์/ถ้อยคำ/ลำดับครบ 1:1
  2. แบ่ง 2 หน้า (R10): ตาราง 23 แถวเต็มหน้า 1 + ใบต่อ/ลงชื่อ DOA N ขั้นหน้า 2 · รองรับแถวเกินกระดาษ (DEC-05)
  3. ลายเซ็นเป็นแถวล่าง 1 ช่องต่อขั้น DOA · "ส่งในระบบ/พิจารณาในระบบ" แทนลายมือ (DEC-07)
  4. ไม่ใช้หัวตารางร่างแถว 4 ของไฟล์ (ไม่มีเส้น · ไม่แสดงในภาพต้นฉบับ) (DEC-12)
- ผล compare_original: **ยังไม่ได้รัน [NO-BROWSER]** · คาดว่า WARN เพราะเปลี่ยนแนวกระดาษ — ต้องให้คนดูภาพวางคู่

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- ตาราง contract: `SMC_data-contract.md`
- parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: ร่าง (ต.ค. 69 · 6 แถว เคลียร์แล้ว 2) · อนุมัติแล้ว (ก.ย. 69 · 12 แถว) · ไม่อนุมัติ (9 แถว เคลียร์ 5) · ยาว 45 แถว (dense · หน้า 2 มี 22 แถว) · DOA 6 ขั้น (7 ช่อง 4+3) → 2 หน้าทุกสถานะ

## 9. (Replica) print_config
ดู `print_config.json` (doc_type SMC · pages 2 · rows_page1 23 · rows_page2_min 5 · rows_page2_max 30 · sign_boxes requester + doa_step:* · decision_words by_role role-mgr-wh)

# UX CHECK REPORT — F-WH-PICK Picking

**วันที่ตรวจ:** 18 สิงหาคม 2569
**ไฟล์:** `f-wh-picking.html`
**ผล:** PASS WITH WARN — ไม่พบ BLOCK

## Gate summary

| Gate | ผล | Evidence |
|---|---|---|
| html-generator-v8 self-audit | PASS | ทุก counter = 0; มี PREFLIGHT stamp |
| Iron Rules shell audit | PASS WITH WARN | FAIL=0, WARN=2 |
| Static scan | PASS | hashchange, Esc, drawer/backdrop, disabled, empty/loading/confirm markers ครบ |
| Runtime | PASS | ไม่มี page error หลังแก้ responsive; resource error มีเฉพาะ Google Fonts ที่ถูกปิด network และมี fallback |
| Render 1440 | PASS | `_qa/render-1440.png` |
| Render 1024 adaptive | PASS | `_qa/render-1024.png` |
| List + SO modal | PASS | `_qa/ux-shots/route_list.png`, `_qa/ux-shots/route_list__overlay_tbody tr.png` |
| Create drawer + combobox | PASS | `_qa/ux-evidence/create-step2.png`, `_qa/ux-evidence/assignee-combobox.png` |
| View drawer ทุก tab | PASS | `_qa/ux-evidence/view-lines.png`, `view-detail.png`, `view-pdf.png`, `view-history.png` |
| Pick-line modal + overlay stack | PASS | `_qa/ux-evidence/pick-line-modal.png` |
| A4 print output | PASS | `_qa/PICK_template.png`, `PICK_sample.pdf` |

## Finding ที่แก้แล้ว

| ID | ระดับ | Finding | การแก้และผล rerun |
|---|---|---|---|
| UX-001 | BLOCK | จอ 1024px เคยเหลือพื้นที่เนื้อหาว่างจาก JavaScript syntax error ระหว่างปรับชื่อ class tab | คืน state property เป็น `viewState.tab`; rerun browser ไม่มี page error และ `render-1024.png` แสดงรายการครบ |
| UX-002 | MAJOR | ตาราง list มีจำนวน cell ไม่ตรง header และมีข้อมูลแหล่งงานที่ไม่ใช่ SO ค้างจาก seed | ปรับทั้ง queue/pick เป็น 8 คอลัมน์ และตัด transfer branch; render list/modal ผ่าน |
| UX-003 | MAJOR | inline layout, z-index และ component audit ไม่เป็นศูนย์ | ย้าย static layout เป็น reusable utility, ใช้ z registry, canonical drawer tabs และ dynamic progress hydration; self-audit ผ่านทุก counter |
| UX-004 | BLOCK | dropdown ค้นหา “ผู้หยิบ” เปิดอยู่แต่ option ถูก drawer บัง เพราะ portal ใช้ชั้น `dropdown` ต่ำกว่า drawer | เพิ่มชั้น `portal` เหนือ drawer, เพิ่ม `.combo-pop` ใน shared layout detector และเพิ่ม E2E ตรวจ option + stacking; proof ก่อนแก้ FAIL / หลังแก้ PASS และ `_qa/ux-evidence/assignee-combobox.png` แสดงรายการครบ |
| UX-005 | MINOR | เนื้อหา option ผู้หยิบสองบรรทัดชิดขอบบน–ล่างและเส้นแบ่งรายการ; รอบแรก 11px ยังต่างจากเดิมน้อยเกินไป | เพิ่ม padding แนวตั้งจาก 8px เป็น 14px พร้อม line-height/ระยะระหว่างชื่อกับรายละเอียด; ยกระดับ `optionCrowded` ใน shared layout detector เป็นขั้นต่ำ 14px โดยพิสูจน์ค่า 11px FAIL 4 รายการ / หลังแก้ PASS 0 รายการ |
| UX-006 | MINOR | กล่องแสดงผู้หยิบหลังเลือกมีความสูงตายตัว 38px และ padding บน–ล่าง 0px ทำให้ข้อความสองบรรทัดชิดขอบ | เปลี่ยนเป็น min-height 54px + padding แนวตั้ง 8px และเพิ่ม `selectionCrowded` ใน shared layout detector; proof ก่อนแก้ FAIL / หลังแก้ PASS |
| UX-007 | REVIEW | PM/BA ขอเอาปุ่มไอคอน “ใบเติม” รูปดาวน์โหลดออกจาก action รายบรรทัด | ลบเฉพาะปุ่ม `arrow-down-to-line` ที่เปิดขอเติม/โอนออกจากตาราง; ปุ่มหาใหม่/เลือกตำแหน่งและกลไก mock ภายในคงเดิม |

## WARN ที่ยอมรับในรอบนี้

1. `audit.sh` เตือน hardcoded `font-size` เพราะ BASE-KIT/print block ยังใช้ค่าขนาดตรงบางจุด; ค่าอยู่ในชุดขนาดที่ self-audit อนุญาตและไม่พบความเพี้ยนจากภาพจริง
2. `audit.sh` มอง stepper ว่าไม่มี `.step-dot`; หน้าจอนี้ใช้ canonical `.stepper-item/.stepper-circle/.stepper-label` ซึ่งตัวตรวจ geometry กลางรองรับ และภาพ create แสดง dot/label/connector ถูกต้อง
3. Google Fonts โหลดไม่ได้ใน sandbox แบบปิด network แต่ stack มี `Noto Sans Thai`, `Satoshi`, system fallback; เอกสาร A4 ฝัง Sarabun ในไฟล์และไม่พึ่ง network

## Scope/interaction checks

- Source queue เป็น Sales Order เท่านั้น; ไม่มี Transfer/Replenishment/Return/Production ใน UI หรือ data path
- Payment gate และ hold ทำให้ checkbox disabled และไม่มีปุ่มสร้างใบหยิบ
- Manual location override ใช้ hard eligibility เดียวกับ auto allocation
- Assignee แสดงพนักงานทั้งหมดก่อนตาม Scope Lock และบอกจำนวนงานค้าง
- Picker ที่ได้รับมอบหมายมี flow เริ่มหยิบ, บันทึกหยิบ, เปลี่ยนตำแหน่ง และปิดงานแบบขาด
- Customer pickup ยังส่งต่อ Packing และ Delivery Note ตามปกติ; ไม่มี logic DN ใน Pick

## Verdict

PASS WITH WARN — rerun หลังแก้ dropdown ผู้หยิบแล้ว; ไม่มี finding ที่บล็อกการ manual test

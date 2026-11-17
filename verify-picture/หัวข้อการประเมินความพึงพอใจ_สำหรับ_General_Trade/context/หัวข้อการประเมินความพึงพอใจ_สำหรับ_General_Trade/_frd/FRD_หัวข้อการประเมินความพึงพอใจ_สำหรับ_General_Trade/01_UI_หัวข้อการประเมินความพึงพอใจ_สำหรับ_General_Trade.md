# 01_UI — F-TMP-002
> Source of truth = `01_Prototype/feature.html` (html-generator-v9.4 · Q-form) · ช่องตรง FORM_SPEC 1:1 (DEC-09)

## §1.1 Page Inventory
| ID | Route | หน้าที่ |
|---|---|---|
| P-01 | `#/csat-gt` | รายการ (no-scorecard · ตัวเลขเป็น badge ≤3 · ค้นหา · กรอง สถานะ/เดือน · CSV · pagination 25) |
| P-02 | `#/csat-gt/create` · `#/csat-gt/edit/:id` | drawer wide wizard 3 ขั้น: ข้อมูลหลักแบบสรุป › เอกสารแนบ › ตรวจสอบและยืนยัน |
| P-03 | `#/csat-gt/view/:id` | drawer 920 · tabs รายละเอียด › PDF Preview › ลายเซ็น / อนุมัติ › ประวัติ |
| M-01..05 | modal | ส่งอนุมัติ (slot ต่อขั้น DOA) · อนุมัติ · ไม่อนุมัติ (เหตุผล) · ยกเลิก (เหตุผล) · ทิ้งข้อมูล |

## §1.2 P-01 คอลัมน์ (1 cell = 1 บรรทัด)
เลขที่ · ประจำเดือน · ผู้จัดทำ · หน่วยงาน · ลูกค้าที่ประเมิน · % โดยรวม · ผลการแปลผล (pill) · สถานะเอกสาร · ลายเซ็น x/y · ⋮ (ดูรายละเอียด · แก้ไข[ร่างของตน] · พิมพ์ · ยกเลิกเอกสาร)

## §1.3 P-02 ขั้น 1 — ฟิลด์ (ป้ายตามกระดาษ)
| การ์ด | ป้าย | key | control | กติกา |
|---|---|---|---|---|
| ① | ประจำเดือน | period_month | search combobox เดือน (12 เดือนล่าสุด) | required |
| ② ×3 ด้าน | หัวข้อ (1.–8.) | items[].topic | ข้อความจาก config (อ่านอย่างเดียว) | snapshot |
| ② | มากที่สุด · มาก · ปานกลาง · น้อย · ต้องปรับปรุง | items[].c5 · c4 · c3 · c2 · c1 | input text inputmode=numeric | จำนวนเต็ม ≥ 0 · ว่าง = 0 |
| ② | รวม (ต่อแถว / แถวรวม) | total · sum.c5..c1 · sum.total | ข้อความคำนวณสด | — |
| ② | % | pct (q_pct · d_pct · s_pct) | ข้อความคำนวณสด (soft update ไม่ rebuild) | "—" เมื่อรวม = 0 |
| ③ | โดยมีรายชื่อดังนี้ | customers[].customer | search combobox Customer | required · ไม่ซ้ำ |
| ③ | จำนวนการสั่งซื้อ | customers[].order_count | ข้อความจาก Sale Order | < เกณฑ์ config = ป้ายเตือน |
| ③ | (ปุ่ม) ดึงลูกค้าที่สั่งซื้อถึงเกณฑ์ | — | btn secondary | ต้องเลือกเดือนก่อน |
| การ์ดสรุป | ผู้จัดทำ · ผู้รับรอง (DOA) · เดือน · % 3 ด้าน · โดยรวม (overall_pct) · ข้อความแปลผล (overall_level) | — | sticky ขวา | อัปเดตสด |

## §1.4 P-03 แท็บ
- รายละเอียด: แบนเนอร์ตามสถานะ (รอ/ร่างกลับจากไม่อนุมัติ/ยกเลิก) · ข้อมูลเอกสาร · ตาราง 3 ด้าน · สรุปผล (การ์ด % + ช่วงแปลผล) · รายชื่อลูกค้า · เอกสารแนบ · ข้อมูลระบบ
- PDF Preview: iframe srcdoc จาก `form.tpl.html` + `docPrintData(r)` · 2 หน้า · ดาวน์โหลด/พิมพ์
- ลายเซ็น / อนุมัติ: summary card (DOA entry · x/y) + timeline ส่ง → ขั้น 1..N → ผลลัพธ์ · ปุ่มตัดสิน inline เฉพาะผู้พิจารณาขั้นปัจจุบัน
- ประวัติ: append-only

## §1.5 ปุ่มหัว drawer ตามสถานะ
ร่าง (เจ้าของ) = ยกเลิก · แก้ไข · ส่งอนุมัติ · รอ (ผู้พิจารณาขั้นปัจจุบัน) = ไม่อนุมัติ · อนุมัติ · รอ (เจ้าของ/admin) = ยกเลิกเอกสาร · อนุมัติแล้ว = ล็อก

## §1.6 UI Standard
CUBE Warm Light (html-generator-v9.4) · คน = วงกลม icon · backdrop ปิดด้วย mousedown · Esc: combobox → modal → drawer

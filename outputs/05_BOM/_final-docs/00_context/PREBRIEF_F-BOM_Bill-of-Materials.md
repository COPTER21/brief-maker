# PREBRIEF · BOM — สูตรการผลิต
> Sales lane · F-0.2 · **recheck + vibe r3 จาก pack v3.5** (FRD STANDARD 7 ไฟล์ ต้นทาง · Reverse Mode: HTML คือของจริงหลัง vibe) · [AI-DRAFT] รอเคาะ
> **บทบาท**: สูตรว่า 1 หน่วยผลผลิต (สินค้า FG) ประกอบจากวัตถุดิบ (RM/PM/TR) อะไร × ปริมาณเท่าไร — 1 สินค้ามีได้หลายสูตร · ป้อน Production (ใบสั่งผลิต MO) + Costing · single-level (ไม่มี BOM ซ้อนชั้น)

## 0. Obligations — พันธะจากต้นทาง
| # | พันธะ | จาก | ถูกตอบที่ § |
|---|---|---|---|
| OB-1 | FRD BR-01..09: 1 FG หลายสูตร (version unique/parent) · 1 สูตรหลัก/FG · parent=FG active · component=RM/PM/TR active · component≠parent (single-level กัน BOM วน) · uom หมวดเดียวกับวัตถุดิบ · cost=Σ(std_cost×qty×(1+scrap%)) · **BR-08 ไม่มีอนุมัติ** · std_cost read-only จาก Product Master | FRD 05 | §3,§4 |
| OB-2 | FRD VR-01..08: parent/version/name required · version unique/parent · lines≥1 · qty>0 · ไม่ซ้ำ component · component≠parent · uom กรอง dropdown | FRD 05 | §4, S-05 |
| OB-3 | **Pattern เลน (recheck 2026-08-09)**: สถานะ obsolete→**inactive** 3 ค่าอิสระ + statusMenu ใน view + stat 4 ใบกดกรอง + bulk (3 สถานะ+ลบ · used>0 ข้าม) + side effect หลุด active→สูตรหลักหลุด + ตัด hint · DOA null (BR-08) | มติเลน | §2,§5,§6 |
| OB-4 | **CI rebrand** Navy→Warm Light + Satoshi (icons SVG ฝังเดิม renderIcons เอง — ไม่ใช่ lucide CDN) | มติ v8 | §6 |
| OB-5 | v8: #96 full-height + sticky thead · #97 responsive · #29 `_keepScroll` · Esc chain (modal>statusMenu>drawer) | มติ v8 | §6 |
| OB-6 | **มติ vibe r3 (2026-08-09)**: ① **#95 Overlay Portal** — combobox suggest (เลือก FG + ค้นวัตถุดิบ line editor) เป็น portal จริงท้าย body (fixed จาก rect · กัน transform เพี้ยน + กัน clip ใต้ตาราง) + fix focus loop ② spacing line editor gap 14 ③ ตัด note/hint หมด ④ **FG แสดงรูปสินค้า** (SVG data-URI mock · จริง sync F-PDM · onerror fallback ตัวอักษร) | user สั่ง | §6 |
| OB-7 | **มติ recheck: ไม่เพิ่ม import/export** — BOM = structured doc หลายบรรทัด (ต่าง flat master · precedent ตัด io ที่ PayTerm) | มติ BA | §2 S-10, OQ-BOM-02 |
| OB-8 | **fix ช่องโหว่ recheck**: saveForm เดิมไม่ enforce VR-01/02/03 (สร้าง ver ซ้ำ/ค่าว่างได้) — เพิ่ม guard ครบ | recheck | §4 |

## 1. สรุป + ผู้ใช้
ทะเบียนสูตรการผลิต · ผู้ตั้งค่า: Planner/วางแผนผลิต · ผู้ใช้ทางอ้อม: Production (เปิด MO เลือกสูตร), Costing (อ่านต้นทุน)
**โครงสร้าง**: 1 FG → หลายสูตร (v1/v2…) → 1 สูตรหลัก (★) · แต่ละสูตร → หลาย lines (วัตถุดิบ×qty×scrap%) · single-level

## 2. Scenarios
| S | ประเภท | ชื่อ | เกิดอะไร | ข้อมูลที่ต้องมี | ผลปลายทาง |
|---|---|---|---|---|---|
| S-01 | Happy | สร้างสูตร (wizard 2 step) | Step 1 ข้อมูลสูตร: เลือกสินค้า FG (**combobox portal + รูปสินค้า**) + version + ชื่อสูตร + ผลผลิต/สูตร + สูตรหลัก(★) → Step 2 line editor: เพิ่มวัตถุดิบ (combobox portal ค้น RM/PM/TR) + qty + UoM (กรองหมวดเดียวกับวัตถุดิบ) + scrap% → cost rollup สด · บันทึกร่าง / บันทึก+เปิดใช้ | FG\* version\* (unique/parent) ชื่อ\* lines≥1 qty>0 | สูตรพร้อมให้ MO เลือก (ถ้า active) |
| S-02 | Happy | ตั้งสูตรหลัก (★) | 1 FG มีสูตรหลัก 1 ตัว — ตั้งใหม่ปลดเก่าอัตโนมัติ (BR-02/EC-01) | — | MO ดึงสูตรหลักเป็น default |
| S-03 | Alt | หลายสูตรต่อสินค้า | view "ภาพรวม" โชว์ทุก version ของ FG นั้น + ป้ายสูตรหลัก/สถานะ | — | เทียบ v1/v2 ได้ |
| S-04 | Alt | แก้สูตร (amend) | **แก้ได้ทุก field รวม lines แม้ used>0** — [AI-DRAFT] MO snapshot สูตรตอนเปิดใบ (ไม่ล็อกโครงแบบ Tax/COA) → OQ-BOM-01 · version ล็อกแก้ได้แต่ต้องไม่ซ้ำ | — | MO ใหม่ใช้สูตรล่าสุด · MO เก่าไม่ย้อน |
| S-05 | Exception | ข้อมูลผิด | ไม่เลือก FG (VR-01) · version ว่าง/ซ้ำต่อ parent (VR-02 · **fix recheck**) · ชื่อว่าง (VR-03) · lines 0 (VR-04) · qty≤0 (VR-05) · component ซ้ำ (VR-06) · component=parent (VR-07 กัน BOM วน) | — | บล็อก + toast ชี้จุด |
| S-06 | Alt | เปลี่ยนวัตถุดิบในบรรทัด | เลือกวัตถุดิบใหม่ → UoM reset = base uom ตัวใหม่ + กรองหมวดใหม่ (EC-05) | — | cost คำนวณใหม่ |
| S-07 | Alt | เปลี่ยนสถานะอิสระ (statusMenu view / bulk 3 ค่า) | ทุกทิศ ไม่มีอนุมัติ (BR-08) · side effect: หลุด active → สูตรหลัก(★) หลุดตาม | — | inactive = MO ใหม่เลือกไม่ได้ |
| S-08 | Exception | bulk ลบ | confirm บอกยอดข้าม — used>0 (มี MO อ้างสูตร) ไม่ลบ (ใช้ inactive แทน) | เลือก ≥1 | — |
| S-09 | Edge (ประกาศ) | ต้นทุน/สถานะ master เพี้ยน | std_cost วัตถุดิบ=0/null → ต้นทุนเพี้ยน (EC-CL-01) · scrap 100% → ต้นทุน×2 (EC-CL-02) · FG/วัตถุดิบ deactivate หลังมีสูตร (EC-ST-01/02) | — | รอเคาะ block/warn → OQ-BOM-04 |
| S-10 | **ไม่รองรับ** (ตัดสินแล้ว) | ① multi-level BOM (สูตรซ้อนสูตร — single-level เท่านั้น BR-05) ② อนุมัติสูตร (BR-08) ③ import/export CSV (structured doc — OB-7) ④ routing/operation/แรงงาน (นอก BOM) ⑤ co-product/by-product ⑥ effective date overlap resolver ⑦ ลบเดี่ยว ⑧ สูตรหลักหลายตัว/FG | | | |

## 3. Data — full data dict
| Field | บังคับ | กติกา | หมายเหตุ |
|---|---|---|---|
| parent (FG) | ✅ | = สินค้า type FG · active (BR-03) · **combobox portal + รูป** | soft-ref Item Master (F-PDM) — mock ฝัง |
| version | ✅ | unique ต่อ parent (BR-01 · เทียบ case-insensitive) | ล็อกแก้ได้แต่ห้ามซ้ำ |
| ชื่อสูตร (name) | ✅ | — | — |
| out_qty / out_uom | — | ผลผลิตต่อสูตร (default 1) | — |
| is_default (★ สูตรหลัก) | — | 1 ตัว/FG · ตั้งใหม่ปลดเก่า · หลุดตามสถานะ (ไม่ active → หลุด) | radio pattern เลน |
| status (3 ค่า) | — | draft/active/inactive อิสระทุกทิศ | เดิม obsolete → inactive |
| lines[] | ≥1 (BR/VR-04) | item (RM/PM/TR active BR-04) · qty>0 · uom (หมวดเดียวกับวัตถุดิบ BR-06/VR-08) · scrap% · **ไม่ซ้ำ component · component≠parent** | soft-ref Item + UoM Master |
| cost (rollup) | คำนวณ | Σ(std_cost×qty×(1+scrap%)) (BR-07) · std_cost read-only จาก Product Master (BR-09) | Confidential (mask ตาม role — Policy Center D-CLASS) |
| audit[] | ระบบ | create/activate/amend/status — append-only | — |
| ระบบ | | `used` (count MO อ้างสูตร — mock · guard ลบ) · DOA null 4 fields (BR-08) | |

## 4. Business Rules
| BR/VR | กติกา | S | ที่มา |
|---|---|---|---|
| BR-01/VR-02 | version unique ต่อ parent — **fix recheck: saveForm enforce แล้ว** (เดิมไม่เช็ค) | S-05 | FRD + fix |
| BR-02/EC-01 | 1 สูตรหลัก/FG — ตั้งใหม่ปลดเก่าอัตโนมัติ | S-02 | FRD |
| BR-05/VR-07 | component≠parent — single-level กัน BOM วน | S-05 | FRD |
| BR-06/VR-08 | uom line หมวดเดียวกับ base uom วัตถุดิบ (กรอง dropdown + reset ตอนเปลี่ยนวัตถุดิบ) | S-06 | FRD |
| BR-07 | cost=Σ(std_cost×qty×(1+scrap%)) · std_cost read-only (BR-09) | — | FRD |
| BR-08 | **ไม่มีอนุมัติ** — บันทึก=เปิดใช้ได้เลย · DOA null | S-07 | FRD (มติทีม) |
| VR-01/03/04/05/06 | parent/ชื่อ required · lines≥1 · qty>0 · ไม่ซ้ำ component | S-05 | FRD |
| BR-DEL [AI-DRAFT] | used>0 (มี MO อ้าง) ลบไม่ได้ (bulk ข้าม) แต่**แก้ lines ได้** (MO snapshot) | S-04,S-08 | OQ-BOM-01 |

## 5. State Machine
draft ⇄ active ⇄ inactive **อิสระทุกทิศ** (statusMenu/bulk/บันทึกฟอร์ม) · side effect เดียว: หลุดจาก active → is_default(★) = false · ไม่มี approval gate (BR-08)

## 6. Actions ต่อหน้า
| หน้า | Action |
|---|---|
| List | stat 4 ใบกดกรอง (ทั้งหมด/ใช้งาน/ไม่ใช้งาน/ร่าง) · ค้นหา (รหัส/ชื่อ/สินค้า) + filter สินค้า + สถานะ · sort · checkbox + bulk (3 สถานะ+ลบ) · **แถว: รูปสินค้า FG** + version + ★สูตรหลัก + ต้นทุน + สถานะ · #96 sticky thead · #29 |
| Wizard form (2 step) | Step 1 ข้อมูลสูตร (**FG combobox portal+รูป** + version + ชื่อ + ผลผลิต + ★) · Step 2 line editor (**combobox portal ค้นวัตถุดิบ** + qty + UoM กรองหมวด + scrap% · spacing 14 · cost rollup สด) · validate VR ครบ |
| View (3 tab) | ภาพรวม (ข้อมูลสูตร + **รูปสินค้า header** + รายการ version อื่นของ FG) · ส่วนประกอบ (ตาราง lines + cost) · ประวัติ (audit timeline) · header: แก้ไข + **statusMenu เปลี่ยนสถานะ** · Esc chain |
| Modal | confirm ลบ bulk (บอกยอดข้าม used>0) |

## 7. Data behaviour
soft-ref + **snapshot**: MO เก็บ bom_id + สำเนาสูตร (lines/qty ณ วันเปิดใบ) — แก้สูตรกระทบเฉพาะ MO ใหม่ (S-04) · PRODUCTS (FG+วัตถุดิบ) + UOMS mock ฝังในไฟล์ → จริง sync Item Master (F-PDM) active + UoM Master (0.1) · std_cost read-only จาก Product Master · cost = Confidential (mask ตาม role) · `used` mock → count MO จริง

## 8. Mock Data Spec
4 สูตร: b1 FG-1001 v1 สูตรมาตรฐาน (active ★ used 14 · 5 lines) · b2 FG-1001 v2 สูตรประหยัด (draft · 4 lines) · b3 FG-1020 v1 (active ★ SET used 6) · b4 FG-1005 v1 สูตรต้นแบบ (draft · std_cost FG=0 พิสูจน์ EC-CL-01) · PRODUCTS 9 (FG 3 มีรูป SVG + RM/PM/TR 6) · UOMS 7 (3 หมวด count/weight/volume)

## 9. Edges + ผลปลายทาง
| ทิศ | คู่ | ผ่านอะไร |
|---|---|---|
| เข้า | ← **Item Master (F-PDM)** | combobox FG (type=FG active) + วัตถุดิบ (RM/PM/TR active) + std_cost read-only + **รูปสินค้า** — mock ฝัง → sync จริง (OQ-BOM-03) |
| เข้า | ← **UoM Master (0.1)** | dropdown หน่วย line (กรองหมวดเดียวกับ base uom วัตถุดิบ) |
| ออก | → **Production / ใบสั่งผลิต (MO)** — ยังไม่ทำ | MO เลือกสูตร (active · default=สูตรหลัก) → snapshot lines · `used` = count MO (edge ประกาศ) |
| ออก | → **Costing** | cost rollup Σ(std_cost×qty×(1+scrap%)) → ต้นทุนมาตรฐานผลิต |
| — | Policy Center | cost = Confidential (mask ตาม role · D-CLASS) — ไม่ใช่ DOA |
| — | DOA / NOTIF | ไม่มี (BR-08) |

## 10. OQ + [AI-DRAFT] register
| # | ประเด็น | เจ้าภาพ | สถานะ |
|---|---|---|---|
| OQ-BOM-01 | `used` = count MO — [AI-DRAFT] used>0 ลบไม่ได้·**แก้ lines ได้** (MO snapshot สูตรตอนเปิดใบ) ยืนยันหลักการ + MO module ยังไม่ทำ | Strike | pin |
| OQ-BOM-02 | ไม่มี import/export (BOM = structured doc หลายบรรทัด · ตัด io แบบ PayTerm) — ต้องการ io แบบ flat (1 แถว=1 line group by parent+ver) มั้ย | Strike | pin |
| OQ-BOM-03 | PRODUCTS (FG+วัตถุดิบ+**รูป**) + UOMS mock ฝัง → sync จริง Item Master (F-PDM) active + UoM Master (0.1) · รูปสินค้าจาก field ไหนใน F-PDM | Strike | pin |
| OQ-BOM-04 | Edge master เพี้ยน (FRD EC-CL/ST): std_cost=0/null · scrap 100% · FG/วัตถุดิบ deactivate หลังมีสูตร active — **block หรือ warn?** (ตอนนี้ปล่อยผ่าน) | Strike | pin |
| OQ-BOM-05 | FRD STANDARD 7 ไฟล์ (pack v3.5) **stale** vs HTML as-built (rebrand + สถานะ 3 ค่า + bulk + portal + รูป + fix VR) — regen FRD | BA | เปิด |

## 11. Coverage Matrix
| S | BR/VR | transition | UI | FN |
|---|---|---|---|---|
| S-01 | VR-01..05, BR-01 | สร้าง→draft/active | wizard 2 step + FG portal+รูป + cost rollup | FN-01..FN-07 |
| S-02 | BR-02/EC-01 | ★ ปลดเก่า | badge สูตรหลัก | FN-08 |
| S-03 | — | — | view รายการ version | FN-09 |
| S-04 | BR-DEL | amend | แก้ lines ได้ (used>0) | FN-10 |
| S-05 | VR-01..07 | — | validate + fix VR recheck | FN-11..FN-14 |
| S-06 | BR-06/EC-05 | uom reset | dropdown กรองหมวด | FN-15 |
| S-07 | BR-08 | ทุกทิศ + side effect | statusMenu + bulk | FN-16..FN-18 |
| S-08 | BR-DEL | ลบ | bulk confirm ข้าม | FN-19 |
| S-09 | EC-CL/ST | — | (ประกาศรอ OQ) | FN-30 |
| S-10 | — | — | (ตรวจว่าไม่มี) | FN-40 |
ผ่าน: BR/VR ครบ ✓ · state+side effect ครบ ✓ · S↔UI↔FN ครบ ✓ · OB-1..8 อ้างครบ ✓ · มติ r3 (portal/spacing/note/รูป) สะท้อนใน OB-6/§6 ✓ · fix VR recheck ใน OB-8/BR-01 ✓

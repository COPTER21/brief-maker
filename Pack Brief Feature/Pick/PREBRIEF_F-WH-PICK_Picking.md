# PREBRIEF · Picking — ใบหยิบสินค้า (Warehouse Outbound)
> Warehouse · Wave S5 · จาก WAVE_PLAN_SALES (S5 ส่งมอบ) + HTML `f-wh-picking.html` (source of truth · md5 9e1a5384 · UX = SO/PO reference · Warm Light v8) + f-loc.html (Location Hierarchy) + f-inv.html (สต็อกตามสินค้าและตำแหน่ง) + F-SALES-SO (จองระดับคลัง · payment trigger) + มติแชท 19 ส.ค. 2569
> เอกสารนี้คือ source of truth เชิง business — ทีมย่อยใช้เขียน FRD/TC ต่อ · [มติ] เคาะแล้ว · [AI-DRAFT] รอ Strike/หัวหน้าคลัง · [STD] มาตรฐาน WMS (SAP WM Transfer Order · Odoo Picking · D365 Work)

---

## 0. Obligations
| # | พันธะ | จาก | ตอบที่ § |
|---|---|---|---|
| OB-1 | เส้นเข้า **Sales Order (S4)**: SO ที่ ยืนยัน + จองระดับคลัง (reserved) + ไม่พัก + **payment trigger ผ่าน** (ทันที / หลังมัดจำ / หลังชำระเต็ม — Finance/AR Receipt ปล่อย) → เข้าคิวหยิบอัตโนมัติ · บริการไม่หยิบ · pickup ก็หยิบ | มติ 19 ส.ค. · F-SALES-SO | S-01..S-04, BR-01..03 |
| OB-2 | เส้นเข้า **Location Hierarchy (f-loc)**: Warehouse → Zone → Area → Rack → Location · type (PICK_FACE/RESERVE/BULK/STAGING/PACK/HOLD) · rotation ต่อตำแหน่ง · 1 location 1 uom | f-loc | §3.3, BR-05..07 |
| OB-3 | เส้นเข้า **Inventory balance (f-inv)**: product × location × lot (exp) · on_hand / allocated · FEFO · movement pick/allocation/putaway | f-inv | §3.3, BR-06, BR-11 |
| OB-4 | เส้นเข้า **Item Master**: goods vs service · มีล็อต/วันหมดอายุ (→ FEFO) · units/factor · สินค้าแช่เย็น | Item Master | BR-05 |
| OB-5 | มติ: **กลยุทธ์หยิบไม่เลือกต่อใบ** — auto จาก master (มีล็อต = FEFO · ไม่มี = FIFO · Pick Face ก่อน Reserve/Bulk = กฎคลัง) · override รายบรรทัดได้ (audit) · ไม่ต้องมี Warehouse Config ก่อน | มติ 19 ส.ค. | BR-05, S-06 |
| OB-6 | มติ: **จองสองชั้น** — SO = reserve จำนวนระดับคลัง · **Pick = ล็อกจริงระดับตำแหน่ง (allocated)** · หยิบ = ตัด on_hand | มติ 19 ส.ค. | BR-06, S-05, S-10 |
| OB-7 | มติ scope: **คิวจาก SO → สร้างใบหยิบ → assign → หยิบ → ปิดงาน (ครบ / ขาด)** → Packing · ไม่รวม จองระดับคลัง/เติม Pick Face/นับสต๊อก/แพ็ค/DN | มติ 19 ส.ค. | §1, S-20 |
| OB-8 | เส้นเข้า **Employee/HR**: ผู้หยิบ (search dropdown · ตำแหน่ง · งานค้าง · เกิน) · หัวหน้าคลัง | HTML | §1, S-08 |
| OB-9 | เส้นออก **Packing → Delivery Note (S5)**: หยิบครบ/ปิดขาด → ส่งต่อ Packing (แยกต่อ SO) · SO สถานะจัดส่ง | WAVE_PLAN | S-16, S-17 |
| OB-10 | เส้นออก **Inventory**: movement `allocation`/`pick`/release · replenishment / transfer task · cycle count เมื่อรายงานขาด/หาไม่เจอ | f-inv | S-11..S-15, BR-11..13 |
| OB-11 | เส้นออก **Sales**: หยิบไม่ครบ/ปิดขาด → SO backorder + แจ้ง Sales · ENG-NOTIFY (pick.assigned · pick.short · pick.done · pick.short_close · so.released) | HTML | S-12, S-17, §9 |
| OB-12 | แหล่งงานอื่นในอนาคต: **Transfer / Replenish / RTV / เบิกผลิต** ใช้ใบหยิบชนิดเดียวกัน (srcType + อ้างอิง) — คิวรับงานตอนนี้ SO เท่านั้น | HTML seed PICK-0889 | S-19, §3.1 |
| OB-13 | มติ UI: SO idiom · list 2 แท็บ (คิว SO / ใบหยิบ) · wizard 3 ขั้น · landing 4 แท็บ · ใช้ง่าย ไม่ overload · action รายบรรทัด (ไม่มี banner) · Document Config เลขรัน PICK- | มติ 19 ส.ค. | §6, §7 |
| OB-14 | มติ process: BA ส่ง HTML + PREBRIEF | มติ 16 ส.ค. | ทั้งฉบับ |

---

## 1. สรุป + ผู้ใช้ + สิทธิ์
**ทำอะไร** [มติ] — รับงานหยิบจากใบสั่งขายที่ปล่อยแล้ว → หัวหน้าคลังสร้างใบหยิบ (เดี่ยว/รวม wave) → ระบบ**จัดสรรตำแหน่ง+ล็อตอัตโนมัติ**ตาม master (FEFO/FIFO · Pick Face ก่อน) เรียงเส้นทาง Zone›Area›Rack›Location และ**ล็อกสต๊อกระดับตำแหน่ง** → มอบหมายผู้หยิบ/อุปกรณ์/priority → ผู้หยิบเริ่มงาน บันทึกหยิบทีละบรรทัด (สแกนตำแหน่ง+สินค้า/ล็อต · จำนวนจริง · ไม่ครบ = เหตุผล + รายงานขาด / ไปตำแหน่งอื่น) → ของขาดจัดการรายบรรทัด (หาใหม่ · เลือกตำแหน่งเอง · ขอเติม/โอน) → **ปิดงาน**: หยิบครบ หรือ **ปิดแบบขาด** → ส่งต่อ Packing (แยกต่อ SO) · พัก · ยกเลิก (ปล่อยจอง)

**หน้าจอ** — list 2 แท็บ: **คิวรอหยิบ (SO)** (checkbox เลือกหลาย SO · สถานะคิว พร้อม/มีใบหยิบ/บางส่วน/รอชำระ/พัก · drill SO) / **ใบหยิบ** (ประเภท·อ้างอิง · ผู้หยิบ · progress · priority) · wizard 3 ขั้น (เลือก SO → มอบหมายงาน → ตรวจสอบรายการหยิบ) · landing 4 แท็บ (รายการหยิบ·เส้นทาง / รายละเอียด·SO / ใบหยิบพิมพ์ / ประวัติ) · modals: บันทึกหยิบ · เปลี่ยนตำแหน่ง/เลือกเอง · ขอเติม/โอน · มอบหมาย · พัก · ปิดขาด · ยกเลิก · SO drill

| Role | ทำอะไรได้ |
|---|---|
| หัวหน้าคลัง (`wh_lead`) | สร้างใบหยิบ (เดี่ยว/wave) · มอบหมาย/เปลี่ยนผู้หยิบ · override ตำแหน่งรายบรรทัด · หาใหม่/ขอเติม/โอน · ส่งต่อ Packing · พัก/ยกเลิก · ทำแทนผู้หยิบได้ทุกอย่าง |
| พนักงานคลัง (`picker`) | เห็น "งานของฉัน" · เริ่มหยิบ · บันทึกหยิบ/รายงานขาด/เปลี่ยนตำแหน่ง · หยิบครบ · พัก/หยิบต่อ · ปิดแบบขาด (เฉพาะใบที่ได้รับมอบหมาย) |
| Sales / อื่น | ดูอย่างเดียว |
> สิทธิ์จริงจาก IAM — **OQ-2**

---

## 2. Scenarios (derive D1-D6)
> D1 (จำนวน/ตำแหน่ง/ล็อต) → S-05..S-07, S-10..S-15 · D2 (state) → S-08..S-20 · D3 (มอบหมาย/สิทธิ์) → S-08, S-09 · D4 (ต้นทาง SO/gate/transfer) → S-01..S-04, S-19 · D5 (ปลายทาง Packing/Inventory/Sales) → S-16..S-18 · D6 [STD] → S-05 (TO creation FEFO), S-06 (manual override), S-11 (short pick → backorder), S-13 (replenishment), S-17 (close short)

| S | ประเภท | ชื่อ | เกิดอะไร | **ข้อมูลที่ต้องมี** | ผลปลายทาง |
|---|---|---|---|---|---|
| S-01 | Happy | SO เข้าคิวหยิบ | SO ยืนยัน+จอง+ไม่พัก+trigger ผ่าน | so.reserved ต่อบรรทัด · warehouse · deliveryDate · method | สถานะคิว "พร้อมหยิบ" |
| S-02 | Alt | SO รอปล่อย (payment gate) | term after_full/after_deposit ยังไม่รับเงิน | paid vs total | "รอชำระก่อนส่ง" · เลือกไม่ได้ · Finance/AR รับเงิน → ปล่อย (so.released) |
| S-03 | Alt | SO พัก / เลยกำหนด / มารับเอง / บริการ | hold → เลือกไม่ได้ · เลยกำหนดแดง · pickup หยิบปกติ · service ไม่ขึ้นบรรทัด | | |
| S-04 | Alt | SO หยิบบางส่วนแล้ว / มีใบหยิบค้าง | คงเหลือ = reserved − picked − ในใบหยิบเปิดอยู่ | openPickQty | "หยิบบางส่วน·เหลือคิว" เลือกได้ · "มีใบหยิบค้าง" เลือกไม่ได้ |
| S-05 | Happy [STD] | สร้างใบหยิบ + จัดสรรอัตโนมัติ | เลือก SO (1 หรือหลายใบ คลังเดียวกัน ≤ waveMax) → allocate ต่อบรรทัด: candidate = balance ในคลัง type PICK_FACE/RESERVE/BULK ที่ avail>0 · เรียง FEFO(exp) หรือ FIFO(lot) → type rank → route · แบ่งหลายตำแหน่งได้ · เรียงเส้นทาง | BAL · itemStrategy | บรรทัดหยิบ {ตำแหน่ง, ล็อต, exp, qty, rule} · บันทึก = **allocated += qty** ระดับตำแหน่ง |
| S-06 | Alt [STD] | override รายบรรทัด (ขั้น 3 / ในใบ) | 📍 เปลี่ยนตำแหน่ง/ล็อต จากรายการที่มีของ (เรียงตามกลยุทธ์) | | ปล่อยจองเดิม จองใหม่ · audit |
| S-07 | Exception | ไม่มีตำแหน่งที่หยิบได้ (short ตั้งแต่สร้าง) | ไม่มี balance หยิบได้ในคลัง | | บรรทัด "ขาด — ไม่มีตำแหน่ง" · สร้างใบได้ · action รายบรรทัด: หาใหม่ / เลือกตำแหน่งเอง / ขอเติม-โอน |
| S-08 | Happy | มอบหมาย | search dropdown ผู้หยิบ (avatar · ตำแหน่ง · งานค้าง · badge เกิน ≥N) · อุปกรณ์ · priority · หมายเหตุ · ว่างได้ = ร่าง | workload | ร่าง → มอบหมายแล้ว · pick.assigned |
| S-09 | Exception | สิทธิ์ | picker เห็น/ทำเฉพาะใบของตน · หัวหน้าคลังทำได้ทั้งหมด · Sales ดูอย่างเดียว | ME.role | ปุ่มซ่อน |
| S-10 | Happy [STD] | เริ่มหยิบ · บันทึกหยิบครบต่อบรรทัด | สแกนตำแหน่ง ✓ + สินค้า/ล็อต ✓ → จำนวน (stepper · ปุ่มครบ · เต็มหน่วยขาย) → ยืนยัน | | on_hand −q · allocated −q · movement `pick` · SO line picked += q · บรรทัด "หยิบแล้ว" |
| S-11 | Exception [STD] | หยิบได้ไม่ครบ → รายงานขาด | จำนวน < ต้อง → เหตุผล chip (ของไม่พอ / เสียหาย-หมดอายุ / หาไม่เจอ-ตำแหน่งผิด / ล็อตไม่ตรง) → "รายงานขาด" | | ส่วนที่ขาด: ปล่อยจอง · **SO reserved −, backorder +** · แจ้ง Sales · งานเติม/นับสต๊อก · pick.short |
| S-12 | Alt | หยิบได้ไม่ครบ → ไปหยิบตำแหน่งอื่น | เลือก "ไปหยิบตำแหน่งอื่น" → modal ตำแหน่งที่มีของ | | หยิบส่วนแรกบันทึก · ส่วนเหลือย้ายตำแหน่ง/ล็อต (จองใหม่) |
| S-13 | Alt [STD] | บรรทัดไม่มีตำแหน่ง: หาใหม่ (refresh) | กดเมื่อของเข้า/เติมแล้ว → allocate ใหม่ | BAL ล่าสุด | พบ → **จองระดับตำแหน่ง** อัตโนมัติ · ไม่พบ → แจ้ง "ขอเติม/โอน หรือรอ GRN" |
| S-14 | Alt | บรรทัดไม่มีตำแหน่ง: เลือกตำแหน่งเอง (manual) | ทุกตำแหน่งในคลังที่มีของ รวม HOLD/STAGING (badge ไม่ใช่ตำแหน่งหยิบ) | | จอง + audit (OQ-3 สิทธิ์/เหตุผล) |
| S-15 | Alt [STD] | บรรทัดไม่มีตำแหน่ง: ขอเติม Pick Face / โอนจากคลังอื่น | modal: ขาดเท่าไร · Reserve/Bulk ในคลัง · คลังอื่นมี · งานที่จะสร้าง (เติม / โอน / รอ GRN-แจ้ง Sales) | whAvail | Inventory task (inv.replenish_request) · เดโมจำลองของเข้า (putaway) → หาใหม่ |
| S-16 | Happy | หยิบครบ → ส่งต่อ Packing | ทุกบรรทัด picked/short และมี picked → "หยิบครบ" → หัวหน้า/ผู้หยิบ "ส่งต่อ Packing" | | pick.done · PACK-xxxx (แยกต่อ SO) · SO picked เมื่อครบทั้งใบ |
| S-17 | Alt [STD] | ปิดงานแบบขาด (close short) | ระหว่างหยิบ มีของหยิบแล้วบางส่วน ลูกค้ารอไม่ได้ → เหตุผล | | บรรทัดค้าง = ขาด · ปล่อยจอง · SO backorder · แจ้ง Sales · สถานะหยิบครบ → Packing เฉพาะที่ได้ · pick.short_close |
| S-18 | Alt | หยิบครบทั้งหมด (mock scan) · พัก/หยิบต่อ · ยกเลิก | พัก = คงจอง · ยกเลิก (ร่าง/มอบหมาย) = ปล่อยจองทุกบรรทัด SO กลับคิว | | |
| S-19 | Alt | ใบหยิบจากงานอื่น (Transfer/Replenish/RTV/ผลิต) | srcType + อ้างอิง (TR-xxxx) · บรรทัด/หยิบ/ปิดเหมือนกัน · ไม่มี SO backorder | | รายละเอียดแสดงข้อมูลอ้างอิงตามประเภท (OQ-6 คิวรับงาน) |
| S-20 | ไม่รองรับ | แพ็ค/DN · จองระดับคลัง · เติม Pick Face จริง · นับสต๊อก · Zone picking หลายคนต่อใบ · RF gun จริง | — | — | Packing/DN (S5 ถัดไป) · Inventory · phase ถัดไป |

---

## 3. Data
### 3.1 ใบหยิบ (header)
| Field | ชนิด | บังคับ | Default | หมายเหตุ |
|---|---|---|---|---|
| รหัส `PICK-YYYY-NNNN` | auto | | Document Config | |
| wh | soft-ref Warehouse (f-loc) | ✓ | จาก SO | SO ใช้ WH-BKK/WH-CNX ↔ f-loc WH-01/02 — **LD-01 ให้ SO ใช้รหัสตาม Location master** |
| srcType | SO / TRANSFER / REPLENISH / RETURN / PRODUCTION | ✓ | SO | |
| sos[] (อ้างอิง) | list รหัสเอกสารต้นทาง | ✓ | | wave = หลาย SO คลังเดียวกัน ≤ waveMax |
| strategy | 'AUTO' | | | ไม่เลือกต่อใบ (มติ) |
| assignee · equipment · priority (high/normal/low) · note | | assignee ⬜ | | ว่าง = ร่าง |
| status | draft / assigned / in_progress / picked / to_pack / on_hold / cancelled | | | §5 |
| startedAt · pickedAt · packRef · holdReason · cancel{by,at,reason} · audit[] | | | | |
### 3.2 บรรทัดหยิบ
| Field | หมายเหตุ |
|---|---|
| id · so (อ้างอิง) · soLine · pid · name · unit · factor · is_free | จาก SO line |
| bal (balance id) · loc · lot · exp · rule (FEFO/FIFO) | จัดสรร |
| qty (หน่วยฐาน) · picked · status (pending/partial/picked/short) · note · by · at | |
### 3.3 อ้างอิง master (read)
Location: id · code · parent (rack/area) · type · seq · rotation · Warehouse/Zone/Area/Rack seq (เส้นทาง) · Balance: pid × loc × lot(exp) · on_hand · alloc · Item: kind · lot flag · uoms/factor · cold · Employee: name · role · workload
### 3.4 Config
pickFaceFirst true · allowShortPick true · waveMax 10 · WORKLOAD_MAX 4 (badge เกิน) · TYPE_RANK PICK_FACE<RESERVE<BULK · ตำแหน่งหยิบได้ = PICK_FACE/RESERVE/BULK (manual รวม HOLD/STAGING)

---

## 4. Business Rules
| BR | กติกา | S | ที่มา |
|---|---|---|---|
| BR-01 | เข้าคิวเมื่อ SO ยืนยัน + มี reserved + ไม่พัก + gate ผ่าน (immediate / after_deposit ต้องรับมัดจำ / after_full ต้องรับครบ — Finance/AR ปล่อย) | S-01, S-02 | [มติ] F-PAYTERM |
| BR-02 | คงเหลือต้องหยิบ = reserved − picked − ในใบหยิบเปิดอยู่ · service ไม่นับ · backorder ไม่หยิบ | S-03, S-04 | |
| BR-03 | สร้างใบหยิบ/มอบหมาย = หัวหน้าคลัง · wave ได้เฉพาะคลังเดียวกัน ≤ waveMax · SO ที่มีใบหยิบค้างเลือกไม่ได้ | S-04, S-05 | [AI-DRAFT] |
| BR-04 | เลขรัน PICK- จาก Document Config · เอกสารต้นทางเป็น "อ้างอิง" (srcType) ไม่ผูกกับ SO เท่านั้น | S-19 | [มติ] |
| BR-05 | กลยุทธ์ต่อบรรทัดจาก master: สินค้ามีล็อต/exp = FEFO · ไม่มี = FIFO · Pick Face ก่อน Reserve ก่อน Bulk · เรียงเส้นทาง Zone›Area›Rack›Location · ไม่มี dropdown ต่อใบ · override รายบรรทัด (audit) | S-05, S-06 | [มติ 19 ส.ค.][STD] |
| BR-06 | จองสองชั้น: SO reserved ระดับคลัง · ใบหยิบ allocated ระดับตำแหน่ง (บันทึกใบ = alloc+) · หยิบ = on_hand− alloc− · ปล่อยเมื่อ ยกเลิก/รายงานขาด/ปิดขาด/เปลี่ยนตำแหน่ง | S-05, S-10, S-11, S-18 | [มติ 19 ส.ค.] |
| BR-07 | ตำแหน่งหยิบได้ = PICK_FACE/RESERVE/BULK ที่ avail>0 · HOLD/STAGING/PACK ไม่จัดสรรอัตโนมัติ (manual เท่านั้น + badge) | S-05, S-14 | f-loc |
| BR-08 | ผู้หยิบ = search dropdown แสดง workload · เกิน N งาน = badge เตือน (ไม่บล็อก) · picker ทำได้เฉพาะใบของตน | S-08, S-09 | [AI-DRAFT] OQ-4 |
| BR-09 | บันทึกหยิบต้องสแกนตำแหน่ง+สินค้า/ล็อตครบก่อนยืนยัน · จำนวน ≤ ต้องหยิบ · น้อยกว่า = ต้องระบุเหตุผล + เลือก รายงานขาด/ไปตำแหน่งอื่น | S-10..S-12 | [STD] |
| BR-10 | รายงานขาด → ปล่อยจองส่วนที่ขาด · SO reserved − / backorder + · ENG-NOTIFY pick.short · งาน replenish/cycle count · หยิบได้บางส่วนบันทึกตามจริง | S-11 | [มติ] |
| BR-11 | บรรทัดไม่มีตำแหน่ง: หาใหม่ = allocate ใหม่จาก balance ล่าสุด → พบ = จองระดับตำแหน่งทันที (hard allocate) + audit · ไม่พบ = คงขาด | S-13 | [มติ 19 ส.ค.] |
| BR-12 | ขอเติม/โอน: สร้าง Inventory task (เติม Pick Face ถ้ามีใน Reserve/Bulk · โอนถ้าคลังอื่นมี · ไม่มี = รอ GRN + แจ้ง Sales) · ใบหยิบไม่บล็อก | S-15 | [STD] |
| BR-13 | หยิบครบ = ทุกบรรทัด picked/short และมี picked · ส่งต่อ Packing แยกต่อ SO (PACK-) · SO picked เมื่อครบทั้งใบ · movement pick ref ใบหยิบ | S-16 | |
| BR-14 | ปิดงานแบบขาด: ระหว่างหยิบ + มีของหยิบแล้ว → บรรทัดค้าง = ขาด (BR-10) → หยิบครบ → Packing เฉพาะที่ได้ · เหตุผลบังคับ | S-17 | [มติ] |
| BR-15 | พัก = คงจอง · ยกเลิก (ร่าง/มอบหมาย) = ปล่อยจองทุกบรรทัด SO กลับคิว · หลังเริ่มหยิบยกเลิกไม่ได้ (ใช้ปิดขาด) | S-18 | [AI-DRAFT] |
| BR-16 | audit append-only ทุกเหตุการณ์ · movement Inventory มี ref ใบหยิบ+SO | ทุก S | กติกากลาง |

---

## 5. State Machine
`ร่าง` → `มอบหมายแล้ว` → `กำลังหยิบ` ⇄ `พัก` → `หยิบครบ` → `ส่ง Packing แล้ว` · แขนง: `ยกเลิก` (ร่าง/มอบหมาย)
| จาก | ไป | ใครกด | เงื่อนไข |
|---|---|---|---|
| — | ร่าง / มอบหมายแล้ว | หัวหน้าคลัง | บันทึก / บันทึกและมอบหมาย · alloc ระดับตำแหน่ง |
| ร่าง | มอบหมายแล้ว | หัวหน้าคลัง | เลือกผู้หยิบ |
| มอบหมายแล้ว | กำลังหยิบ | ผู้หยิบ | เริ่มหยิบ |
| กำลังหยิบ | พัก | ผู้หยิบ/หัวหน้า | เหตุผล · คงจอง |
| พัก | กำลังหยิบ | ผู้หยิบ | หยิบต่อ |
| กำลังหยิบ | หยิบครบ | ผู้หยิบ | ทุกบรรทัด picked/short · หรือ ปิดงานแบบขาด (เหตุผล) |
| หยิบครบ | ส่ง Packing แล้ว | หัวหน้าคลัง/ผู้หยิบ | PACK- ต่อ SO |
| ร่าง/มอบหมายแล้ว | ยกเลิก | หัวหน้าคลัง | เหตุผล · ปล่อยจอง |
สถานะบรรทัด: รอหยิบ → หยิบแล้ว / หยิบบางส่วน / ขาด (มีตำแหน่ง=รายงานขาด · ไม่มีตำแหน่ง=รอ หาใหม่/เลือกเอง/เติม-โอน) · สถานะคิว SO: พร้อมหยิบ / มีใบหยิบค้าง / หยิบบางส่วน / หยิบครบ / รอชำระ / พัก

---

## 6. Actions ต่อหน้า
| หน้า | action |
|---|---|
| list แท็บคิว SO | ค้นหา · กรองคลัง/สถานะคิว · checkbox เลือกหลาย SO → สร้างใบหยิบ (n SO) · แถว = drill SO (สั่ง/จอง/หยิบ/ในใบหยิบ/คงเหลือ/backorder/ATP + ใบหยิบที่เกี่ยวข้อง) · ปุ่ม + สร้างใบหยิบ · ปุ่ม Finance ยืนยันรับเงิน (mock gate) |
| list แท็บใบหยิบ | ค้นหา · กรองคลัง/สถานะ/ผู้หยิบ (งานของฉัน) · export · แถว: ประเภท·อ้างอิง · ผู้หยิบ · progress · priority · กำหนดส่ง · สถานะ |
| wizard ขั้น 1 | ตาราง SO พร้อมหยิบ (คลังเดียวกัน) checkbox · ขั้น 2 การ์ดสรุป + ผู้หยิบ (search dropdown) + อุปกรณ์ + priority + หมายเหตุ · ขั้น 3 ตารางเส้นทาง (📍 เปลี่ยน · หาใหม่ · ขอเติม/โอน รายบรรทัด) → บันทึกร่าง / บันทึกและมอบหมาย |
| landing header | ตามสถานะ/สิทธิ์: ยกเลิก·มอบหมาย / เริ่มหยิบ / พัก·หยิบครบทั้งหมด·ปิดงานแบบขาด·หยิบครบ→Packing / หยิบต่อ / ส่งต่อ Packing · พิมพ์ · ปิด |
| แท็บ รายการหยิบ | progress · ตารางเส้นทาง · บันทึกหยิบ (modal สแกน+stepper+เหตุผล+ทางเลือก) · 📍 · หาใหม่ · ขอเติม/โอน (+จำลองของเข้า) |
| แท็บ รายละเอียด·SO | ข้อมูลใบ · ต่อ SO: gate/trigger · ตาราง สั่ง/จอง/ในใบนี้/หยิบแล้ว/backorder · หรือข้อมูลใบโอน |
| แท็บ ใบหยิบ (พิมพ์) A4 · ประวัติ | |

---

## 7. Data behaviour
เลขรัน PICK- · soft-ref SO/TR/Location/Balance/Employee · ไม่มี hard delete · audit append-only · allocation ระดับตำแหน่ง persist บนบรรทัด · movement Inventory (allocation/pick/putaway) ref ใบหยิบ · SO line picked/reserved/backorder อัพเดตผ่าน contract (ไม่แก้ SO ตรง) · สถานะคิว SO derive ณ runtime

---

## 8. Mock Data Spec (prove)
คลัง WH-01 บางนา (Storage: FM pick face 6 · Aisle A/B reserve 7 · Bulk 2 · Outbound pack/staging · QC hold) · WH-02 ลำพูน (chiller) · balance ~27 แถว (product×loc×lot·exp) · SO 8 ใบ: 0202 Tops (wave · มีบริการ · นม short) · 0203 หัวหิน (มีใบหยิบ 0891 กำลังหยิบ FEFO L007+ short) · 0201 ทองดี (หยิบบางส่วน 0890 → Packing) · 0205 PREPAY รอชำระ (mock ปล่อย) · 0206 DEP50 รอมัดจำ · 0207 มารับเอง CASH · 0200 พัก+backorder · 0208 WH-02 chiller · PICK-0889 จาก TR-2026-0012 (Transfer) · e2e: gate ปล่อย · wave 2 SO · FEFO+FIFO ในใบเดียว · reloc ในขั้น 3 · dropdown ผู้หยิบ · หยิบ 710/720 → ขาด 10 backorder · หาใหม่ก่อน/หลังของเข้า (+600 alloc) · manual · ขอเติม/โอน · ปิดงานแบบขาด · Packing · ยกเลิกปล่อยจอง

---

## 9. Edges + Hotspot
| ทิศ | คู่ | ปลายทาง |
|---|---|---|
| เข้า | Sales Order (S4) | คิว · reserved · gate (payment term/Finance) · hold · picked/backorder กลับ |
| เข้า | Location Hierarchy · Inventory balance · Item Master · Employee | จัดสรร/ล็อก/หยิบ · workload |
| เข้า (อนาคต) | Transfer · Replenish · RTV · Production | srcType |
| ออก | Packing → DN (S5) | PACK- ต่อ SO |
| ออก | Inventory | movement allocation/pick · replenish/transfer task · cycle count |
| ออก | Sales | backorder · แจ้ง |
| ออก | ENG-NOTIFY | pick.assigned · pick.short · pick.done · pick.short_close · so.released · inv.replenish_request |
| ออก | Document Config | เลขรัน PICK- / PACK- |

---

## 10. OQ register
| # | ประเด็น | เจ้าภาพ |
|---|---|---|
| OQ-1 | กลยุทธ์อยู่ที่ Item Master (lot flag) + Location rotation (ตอนนี้) — ต้องมี Warehouse Config สำหรับ Pick Face ก่อน / waveMax / workload ไหม | Strike/หัวหน้าคลัง |
| OQ-2 | สิทธิ์: picker ปิดงานแบบขาด/เปลี่ยนตำแหน่งเองได้ไหม หรือหัวหน้าเท่านั้น | Strike |
| OQ-3 | เลือกตำแหน่งเอง (manual · รวม Hold/Staging) ต้องเหตุผล/สิทธิ์หัวหน้าไหม | หัวหน้าคลัง |
| OQ-4 | workload เกิน N = เตือนหรือบล็อกมอบหมาย · N มาจากไหน | หัวหน้าคลัง |
| OQ-5 | wave: ส่ง Packing แยกต่อ SO อัตโนมัติ หรือ sorting station | หัวหน้าคลัง |
| OQ-6 | คิวรับงานจาก Transfer/Replenish/RTV เข้าแท็บเดียวกันหรือแยก · ใครสร้าง | Strike/WH |
| OQ-7 | ปิดงานแบบขาด/รายงานขาด → SO backorder แล้ว Sales ทำอะไร (แจ้งลูกค้า/close short SO) · replenishment task อัตโนมัติไหม | Strike/Sales |
| OQ-8 | pickup (ลูกค้ามารับเอง): หยิบ→รอรับที่ staging · DN ออกตอนไหน | WH/Sales |
| OQ-9 | SO ใช้ WH-BKK/WH-CNX ↔ Location master WH-01/02 — LD ให้ SO ใช้รหัสตาม master | Strike |
| OQ-10 | สินค้าแช่เย็น/สินค้าหนัก: หยิบท้ายสุด/แยกใบ อัตโนมัติไหม | หัวหน้าคลัง |
| OQ-11 | ลงทะเบียน ENG `pick-allocation-engine` (FEFO/FIFO/route) · `inventory-reserve` ร่วมกับ SO | Architect |

---

## 11. Coverage Matrix
| S | BR | transition | UI | FN |
|---|---|---|---|---|
| S-01 | BR-01 | คิว | แท็บคิว | FN-01 |
| S-02 | BR-01 | คิว | รอชำระ · mock Finance | FN-02 |
| S-03 | BR-02 | คิว | | FN-03 |
| S-04 | BR-02, BR-03 | คิว | | FN-04 |
| S-05 | BR-03, BR-04, BR-05, BR-06, BR-07 | —→ร่าง/มอบหมาย | wizard 3 ขั้น | FN-05, FN-06, FN-07 |
| S-06 | BR-05, BR-06 | | 📍 เปลี่ยน | FN-08 |
| S-07 | BR-07 | | บรรทัดขาด | FN-09 |
| S-08 | BR-08 | ร่าง→มอบหมาย | dropdown · modal | FN-10 |
| S-09 | BR-08 | | ปุ่มซ่อน | FN-11 |
| S-10 | BR-06, BR-09 | มอบหมาย→กำลังหยิบ | เริ่ม · modal บันทึกหยิบ | FN-12, FN-13 |
| S-11 | BR-09, BR-10 | | เหตุผล · รายงานขาด | FN-14 |
| S-12 | BR-09 | | ไปตำแหน่งอื่น | FN-15 |
| S-13 | BR-11 | | หาใหม่ | FN-16 |
| S-14 | BR-07 | | เลือกเอง | FN-17 |
| S-15 | BR-12 | | ขอเติม/โอน | FN-18 |
| S-16 | BR-13 | กำลังหยิบ→หยิบครบ→ส่ง Packing | | FN-19, FN-20 |
| S-17 | BR-14, BR-10 | กำลังหยิบ→หยิบครบ | ปิดงานแบบขาด | FN-21 |
| S-18 | BR-15, BR-06 | พัก/ยกเลิก | | FN-22, FN-23 |
| S-19 | BR-04 | | ประเภท·อ้างอิง | FN-24 |
| S-20 | — | ไม่รองรับ | — | — |
| ทุก S | BR-16 | | audit | FN-94 |
ผ่าน: ทุก BR/transition ถูกอ้าง · ทุก S มี FN · OB-1..14 ถูกอ้าง

# Coverage Report — F-INV-001 Stock by Location (รอบ 1: HTML)

> **หมายเหตุการปรับใช้ (adaptation notice):** feature นี้ไม่มี `workflow_graph.json` / `NODE_BRIEF` จาก
> plan-module-workflow-mapper (ยืนยันแล้ว — เป็น HTML-first reverse-mode pack) จึงใช้
> **PREBRIEF_F-INV_Stock-by-Location.md เป็น contract โดยตรง** ตามแบบอย่าง F-CUST-001 —
> แทนที่ node/edge/golden-rule ด้วย: **Obligations (OB-1..12), Scenarios (S-01..12 รวม S-05b/S-08b),
> FUNCTION_CHECKLIST (FN-01..40), §1 Scope (in/out), §5 Coverage Matrix ที่ประกาศไว้เองใน PREBRIEF**
> รอบนี้ตอบคำถามเดียว: **"UI มีทาง/ปุ่ม/สถานะรองรับครบตามที่ PREBRIEF ประกาศไว้มั้ย"** — ไม่ใช่ว่า FRD/TC
> เขียนครบหรือยัง (รอบ 2 ยังไม่เกิด — ทั้ง FRD pack และ testcase ยังไม่ถูกผลิตสำหรับแพ็กนี้)

- วันที่: 2026-08-10 · contract: `PREBRIEF_F-INV_Stock-by-Location.md` (101 บรรทัด, OB-1..12 · S-01..12
  (+S-05b, S-08b) · §1 Scope · §5 Coverage Matrix ที่ผู้ผลิตประกาศเอง · §6 OQ-INV-01..05 · §7 Precedents)
- Artifact ที่ตรวจ: `StockByLocation.html` (3,124 บรรทัด) — ผ่าน qc-ux-html-checker แล้ว (อ้างอิงเท่านั้น
  ไม่ใช่ scope ของรอบนี้) + `FUNCTION_CHECKLIST_F-INV_Stock-by-Location.md` (FN-01..23, FN-30, FN-40)
- Checklist จาก contract: OB 12 · Scenario 12 (14 นับ S-05b/S-08b แยก) · FN 26 รายการ (มี gap เลขตามที่
  checklist ประกาศเอง: FN-01..23, FN-30, FN-40) · Scope-out 4 กลุ่ม (GRN/Putaway/RTV stub ·
  Multi-UOM bucket display · costing engine · allocation/reservation UI จริง/transfer flow เต็ม)

## Verdict: 🟡 WARN

สรุป: **OB 12/12 ✓ มี UI evidence จริงทุกข้อ · Scenario 12/12 (+S-05b/S-08b) ✓ ครบ · FN 26/26 ✓ ครบ
(ตรงกับที่ FUNCTION_CHECKLIST ติ๊กเอง)** — ไม่มี block-severity gap ด้าน obligation/scenario/function
แต่พบ **scope creep 1 รายการระดับ real-feature** ที่ขัดกับ §1 "ไม่ทำ" อย่างชัดเจน (valuation/costing
display ในจอ balance drawer) ซึ่งไม่ถูกประกาศไว้ใน PREBRIEF เลยไม่ว่าจุดใด — นี่คือเหตุผลที่ปรับ verdict
จาก PASS เป็น **WARN** (ไม่ถึง BLOCK เพราะไม่กระทบ OB/S/FN ที่ประกาศไว้ แต่ต้องตัดสินใจก่อนเข้า FRD stage
เพราะขัดกับ scope-out ที่ระบุชื่อไว้ตรง ๆ)

---

## Coverage Matrix — Obligations (OB-1..12)

| OB | พันธะ | UI Evidence | สถานะ |
|---|---|---|---|
| OB-1 | ENC HTML = base superset (adjust modal+log+break/pack) rebrand Warm Light/CUBE4.0 | CSS `:root` CUBE Warm Light tokens (L16-24) · adjust modal (`renderAdjModal` L2653) · ADJ log (`renderAdjLogView` L2736) · break/pack (`renderBreakPackView` L2475) ทั้งหมดมีจริงในไฟล์เดียว | ✓ |
| OB-2 | 2-code model (code + old_code) — ตัด code_item/code_sku | `PRODUCTS` records มีแค่ `code`/`old_code` (เช่น L817 `code:'FG-1001', old_code:'OLD-DESK-001'`) · `fourCodeChips()` L2572 render 2 ชุด · ไม่พบ `code_item`/`code_sku` ในไฟล์ | ✓ |
| OB-3 | Service exclusion — SV ห้ามมี balance/โผล่จอ/ปรับไม่ได้ | `isStockable(p){return p&&p.type!=='SV';}` L830 ใช้ guard ใน `getFiltered()` L1154, `skuAgg()` L1224, `adjLineHTML` prodOpts L2614 (filter isStockable) · comment "BACKEND exclude ตั้งแต่ query" L1153 | ✓ |
| OB-4 | 1 location 1 uom — ledger ฐานเสมอ, จอแสดงตามหน่วย loc + ฐานกำกับเมื่อ factor>1 | `locUomIdx()` L1088, `rowUnit()` L1062, `qtyCell()` L1068 (`f>1` แสดง `<span class="q-base">`) · `renderUomLocTab` L2149 แสดงตามหน่วย loc + สรุปฐาน | ✓ |
| OB-5 | List "ตามสินค้า" = 1 สินค้า 1 แถว (agg หน่วยฐาน) — ตัด stat "คงเหลือรวม" ข้ามหน่วย | `skuAgg()` L1221 รวมด้วย `r.on_hand`/`r.allocated` (ฐานเสมอ) 1 แถวต่อ pid · comment "ตัด 'คงเหลือรวมข้ามหน่วย'" L1496 · ไม่พบ stat การ์ดที่รวม on_hand ข้ามหน่วยแยกกัน | ✓ |
| OB-6 | Low stock จาก `min_stock` (Item Master) เทียบ "พร้อมใช้" | `PRODUCTS['FG-1001'].min_stock:200` เป็นต้น (L817-825) · `skuAgg()` L1233 `low = (p.min_stock>0) && av<p.min_stock` | ✓ |
| OB-7 | สถานะ list = คำสั้น 3 ค่า ปกติ/ต้องเติม/ขาดสต็อก | L1610-1615 เงื่อนไข `av<0→ขาดสต็อก` / `low→ต้องเติม` / else `ปกติ` (chip เดียว dot+คำ) | ✓ |
| OB-8 | Adjust สร้าง balance ใหม่ได้ + line editor grid v8 B2 + summary bar | `submitAdjust()` L2696 branch `else` สร้าง `row` ใหม่ (L2715-2720) เมื่อไม่มี match · modal grid `renderAdjModal` L2653 · summary bar (พร้อมบันทึก/เพิ่มรวม/ลดรวม/รายการใหม่) ต้องดูใน `renderAdjModal` body | ✓ |
| OB-9 | #95 Overlay Portal ทุก dropdown + Esc chain (①ปิด dd ②ปิด modal) | `.dd-panel.is-portal` CSS L326 + `ddTog()`/`ddCloseAll()` L2264-2290 · keydown handler L2287-2288 (Esc ปิด dd ก่อน, `stopImmediatePropagation`) + L3100-3101 (Esc ปิด modal/drawer ลำดับถัดไป) | ✓ |
| OB-10 | #67.1 Hint opt-in — ไม่มี hint สอนใช้งาน | ไม่พบ `.hint`/คำอธิบายเชิงสอนใช้งานในหน้า overview/drawer (มีเฉพาะ business alert ต่ำกว่าขั้นต่ำ/ติดลบ ซึ่งเป็น business note ไม่ใช่ hint) | ✓ |
| OB-11 | Allocated แตะไม่ได้ + append-only ADJ log | `adjLineError()` L2606-2608 block `inf.base > inf.on - inf.al` พร้อมข้อความ "ห้ามแตะยอดจอง" · `ADJLOG.unshift(batch)` L2727 ไม่มี update/delete บน ADJLOG ที่ใดในไฟล์ | ✓ |
| OB-12 | RBAC ปรับสต็อกเฉพาะ warehouse_staff+finance | `canAdjust(){return ['warehouse_staff','finance'].includes(CURRENT_ROLE);}` L1032 · ปุ่มปรับสต็อกถูก gate ทุกจุด (L1524, L1932, L2041, L2762) · error toast L2578 เมื่อกดตรงไม่ผ่าน role | ✓ |

**OB coverage: 12/12 ✓ มี UI evidence จริงทุกข้อ ไม่มีข้อใดขาด**

---

## Coverage Matrix — Scenarios (S-01..12, รวม S-05b/S-08b)

| Scenario | UI Evidence | สถานะ |
|---|---|---|
| S-01 เปิดจอครั้งแรก | `renderList()` L1488 — stat 4 ใบ (SKU/low/neg/HOLD) L1534-1552 · `skuAgg()` 1 แถว/สินค้า · คอลัมน์ list L1600-1615 | ✓ |
| S-02 product drawer | `renderProductDrawer()` L1903, `renderDrawer()` L2010 tabs [ภาพรวม/ตำแหน่งจัดเก็บ/การเคลื่อนไหว] ผ่าน `setTab()` L1358 · route `/sku/{pid}` ผ่าน `openDrawer()` L1337 + `syncRouteToState()` L1275 (refresh-safe) | ✓ |
| S-03 ดูตามตำแหน่ง + loc drawer | `renderLocationView()` L1653 (การ์ด/แถว+utilization `.util-bar` L400) · `renderLocationDrawer()` L1797 "สิ่งที่อยู่ในตำแหน่งนี้" · เจาะเป็น balance drawer ผ่าน `/sku/S{id}` (ปุ่มในตาราง drawer เรียก `openDrawer`) | ✓ |
| S-04 ค้นหา+กรอง | `applyFilter()` L1216, `toggleHideZero()` L1217, `quickFlag()` L1219 (toggle ซ้ำ=ยกเลิก เพราะ `flag===f?'':f`) · sort คอลัมน์ผ่าน `key` map ใช้ `a.on/a.alloc/a.av` (ค่าฐาน) L1242 | ✓ |
| S-05 ปรับเพิ่ม/ลด multi-line | `openAdjust()` L2577, `adjAddLine()`/`adjDelLine()` L2586-2587, `adjLineHTML()` L2612 คงเหลือ live "ปัจจุบัน→หลังปรับ" L2646-2648, `submitAdjust()` L2696 ADJ doc 1 ใบหลายบรรทัด | ✓ |
| S-05b เพิ่มเข้าตำแหน่งว่าง | `locOpts` label "· ว่าง — เพิ่มเข้าได้/· มีของ/· ล็อกอยู่" L2624 · `isNew` flag L2633 → "รายการใหม่ในตำแหน่งนี้" L2647 · `submitAdjust()` branch สร้าง `row` ใหม่ L2715-2720 | ✓ |
| S-06 ลดชนเพดานจอง (blocked) | `adjLineError()` L2608 `"ลดได้สูงสุด ${maxRed}...ห้ามแตะยอดจอง"` — allocated ไม่ถูกแตะ (คำนวณจาก `on-al` เท่านั้น) | ✓ |
| S-07 ตำแหน่ง/มาสเตอร์ไม่พร้อม (blocked) | `adjLineError()` L2601-2603: `LOCKED_LOCS`, `blocked/frozen/inactive/maintenance/decommissioned`, master inactive · `prodOpts` กรอง `isStockable` ตัด SV ออกจาก picker L2614 + ถ้าฝืนก็ error เพราะไม่มีใน dropdown ให้เลือก | ✓ |
| S-08 Low stock | badge "ต้องเติม" L1614 + stat ใบ L1539-1542 + note ใน drawer (`renderOverviewTab` — ov-warn class L1950/2080 area) | ✓ |
| S-08b ขาดสต็อก (ติดลบ) | badge แดง "ขาดสต็อก" L1612 + stat ติดลบ L1544-1547 · ไม่มี block บนการจองย้อนหลัง (เป็นแค่ display flag `neg`) | ✓ |
| S-09 สินค้าบริการไม่โผล่ | `isStockable` guard ที่ทุกจุด query/picker/bpProducts (`bpProducts()` L2218 ใช้ `Object.keys(UOMCONV)` ซึ่งไม่มี SV) | ✓ |
| S-10 สิทธิ์ | `canAdjust()` L1032 gate ปุ่มทุกจุด — role อื่นไม่เห็นปุ่ม (conditional render ไม่ใช่แค่ disable) | ✓ |
| S-11 Break/Pack | `renderBreakPackView()` L2475, `submitBPOrder()` L2327 lock ผ่าน `LOCKED_LOCS.add()` L2343-2344, badge นับ locked (L2505) · เชื่อมกับ S-07 ผ่าน `adjLineError` เช็ค `LOCKED_LOCS` | ✓ |
| S-12 Audit log | `renderAdjLogView()` L2736, ADJ doc format `ADJ-2026-NNNN` L2708, append-only (`unshift` ไม่มี edit/delete), ค้น/กรองผ่าน `applyLogFilter()` L2735 | ✓ |

**Scenario coverage: 12/12 (+S-05b, S-08b) ✓ ครบทุกข้อมี UI evidence จริง**

---

## Coverage Matrix — FUNCTION_CHECKLIST (FN-01..23, FN-30, FN-40)

| FN | UI Evidence | สถานะ |
|---|---|---|
| FN-01 Stat 4 ใบ | L1534-1552 (SKU/low/neg/HOLD, 3 ใบแรกกดกรองผ่าน `quickFlag`) | ✓ |
| FN-02 ตาราง 1 สินค้า 1 แถว | `skuAgg()` L1221, คอลัมน์ list ส่วน render ~L1600+ | ✓ |
| FN-03 กรอง SV ทุกจุด | `isStockable` ที่ `getFiltered`/`skuAgg`/`adjLineHTML`/`bpProducts` | ✓ |
| FN-04 สถานะสั้น 3 ค่า | L1610-1615 | ✓ |
| FN-05 รหัส 2 ชุด | `fourCodeChips()` L2572 + `PRODUCTS` schema (code/old_code เท่านั้น) | ✓ |
| FN-06 Tabs บนสุด full-width + route refresh-safe | `renderDrawer()`/`setTab()` L1358 + `syncRouteToState()` L1275 | ✓ |
| FN-07 ภาพรวม 3 ใบฐาน+note+conv+รายละเอียด | `renderOverviewTab()` L2080 (คงเหลือรวม/จองแล้ว/พร้อมใช้ L1949-1951) | ✓ |
| FN-08 ตำแหน่งจัดเก็บ ตาราง | `renderUomLocTab()` L2149 (Σ ตรงสรุปผ่าน `grandBase`/`grandAlloc`) | ✓ |
| FN-09 Low stock badge+stat+note | ครอบคลุมร่วมกับ OB-6/S-08 ด้านบน | ✓ |
| FN-10 การเคลื่อนไหว merge+@ตำแหน่ง | `renderMovesTab()` L2191, `getMoves()` L1129 | ✓ |
| FN-11 การ์ดต่อตำแหน่ง+utilization | `renderLocationView()` L1653, `.util-bar`/`.util-fill` CSS L399-405, `utilClass()` L992 | ✓ |
| FN-12 Loc drawer ตามหน่วย loc+ฐานกำกับ+เจาะ balance | `renderLocationDrawer()` L1797 | ✓ |
| FN-13 Modal grid v8 B2 | `renderAdjModal()` L2653 | ✓ |
| FN-14 เหตุผลบังคับ 6 ค่า+หมายเหตุ+เพิ่ม/ลบบรรทัด | `ADJ_REASONS` (6 ค่า) L1031, `adjAddLine/adjDelLine` L2586-2587, บรรทัดสุดท้ายลบไม่ได้ (`is-disabled` เมื่อ `lines.length===1` L2649) | ✓ |
| FN-15 Validation ต่อบรรทัด live | `adjLineError()` L2598-2610 ครบทุกเงื่อนไขที่ระบุ | ✓ |
| FN-16 คงเหลือ live ปัจจุบัน→หลังปรับ | L2646-2648 | ✓ |
| FN-17 เพิ่มเข้าตำแหน่งว่าง | L2624, L2633, L2647, L2715-2720 | ✓ |
| FN-18 บันทึก RAW+ADJ doc+movement+toast | `submitAdjust()` L2696-2731 | ✓ |
| FN-19 RBAC ปุ่ม/action staff+finance | `canAdjust()` L1032 + gate 4+ จุด | ✓ |
| FN-20 Overlay Portal+Esc chain+outside click | `.dd-panel.is-portal` L326, `ddTog/ddCloseAll` L2264-2290, keydown L2287-2288 & L3100-3101, `render()` เคลียร์ portal (ต้อง cross-check ใน `render()` L3049 — ไม่พบ orphan DOM เพิ่มเติมจากการอ่าน) | ✓ |
| FN-21 #67.1 ไม่มี hint | ไม่พบ hint/คำอธิบายสอนใช้งานในทุกจอที่ตรวจ | ✓ |
| FN-22 ค้นหา+ซ่อน0+sort+pagination | `applyFilter`, `toggleHideZero`, `sortBy` L1246, `getPaginated()` L1199, `goToPage/setPageSize` L1247-1248 | ✓ |
| FN-23 Break/Pack picker กรอง SV+lock+movement แยก | `bpProducts()` L2218 (เฉพาะ multi-uom, ไม่มี SV), `submitBPOrder` lock L2327+, `MOVE_LABEL` มี `transfer` แยกประเภท L944 | ✓ |
| FN-30 Edge (pid,loc) unique/neg เฉพาะ EC-07/bucketsFor Σ=on_hand/stat ไม่ hardcode | `submitAdjust` เช็คซ้ำ `keys` (pid+loc unique ต่อ 1 submit) L2700-2701 · `bucketsFor()` L1096 คำนวณจริงจาก RAW ไม่ hardcode · stat คำนวณจาก `agg`/`all` runtime | ✓ |
| FN-40 Gate (node/lint/E2E/md5) | นอกขอบเขต UI coverage (deployment/test-infra gate) — อ้างอิงจาก FUNCTION_CHECKLIST ว่าผ่านแล้ว ไม่ตรวจซ้ำในรอบนี้ (เป็นหน้าที่ qc-ux-html-checker/CI ไม่ใช่ coverage-checker) | ⬜ NOT-CHECKED (out-of-scope ของ skill นี้) |

**FN coverage: 25/26 ✓ มี UI evidence ตรง + 1/26 (FN-40) NOT-CHECKED เพราะเป็น gate เชิง build/test infra ไม่ใช่ business coverage — ไม่กระทบ verdict**

---

## Scope Guard — §1 ไม่ทำ (out-of-scope)

| รายการนอก scope | ตรวจพบใน HTML | ผลตรวจ |
|---|---|---|
| GRN/Putaway/RTV | sidebar item `data-feature="grn"/"putaway"/"rtv"` (L672-683) — ไม่มี `onclick`/route handler ผูกกับ item เหล่านี้ (ต่างจาก `data-feature="stock-by-location"` ที่ active) — เป็น stub เมนูเฉย ๆ ตามที่ประกาศ | ✓ ตรงตาม scope (stub only) |
| Multi-UOM bucket ราย UoM (VD-PDM-05 ตัดแล้ว) | `bucketsFor()`/`UOMCONV` มีอยู่ แต่ใช้เพื่อคำนวณ "หน่วยตามตำแหน่ง" (OB-4, in-scope) ไม่ใช่แสดง breakdown ต่อ UoM แยกในหน้า list — `skuAgg()` ยัง 1 แถว/สินค้าด้วยฐานเดียว | ✓ ไม่พบการ leak เป็นฟีเจอร์ bucket-per-uom ในจอ list |
| Costing engine (VD-PDM-07) | **พบจริง** — `canValuation()` L801, ปุ่ม "ดูมูลค่า/ซ่อนมูลค่า" L2047-2050, กล่อง `.val-box` แสดง "ต้นทุน/หน่วย" + "มูลค่าคงเหลือ" (`on_hand × cost`) L2135-2144, `canValExport()` L803 + toggle "รวมมูลค่า" ตอน export L1368 — อ้าง comment `// FRD §0.3 + BR-D02` (L790) ซึ่ง**ไม่มีอยู่จริงในเอกสาร PREBRIEF ชุดนี้เลย** | 🔴 **SCOPE CREEP — ดูรายละเอียดใน Gaps ด้านล่าง** |
| Allocation/reservation UI จริง (อ่านอย่างเดียว) | ไม่พบปุ่ม/ฟอร์มสร้าง-แก้ allocation ใด ๆ — `allocated` เป็น read-only field ทุกจุดที่ตรวจ (`avail()`, `adjLineInfo()` ใช้เพื่อคำนวณเพดานเท่านั้น) | ✓ ตรงตาม scope |
| Location transfer flow เต็ม (เกิน mock timeline) | `MOVE_LABEL.transfer` มีแค่ label ใน timeline (L944) ไม่มีฟอร์ม "ย้ายตำแหน่ง" แยกต่างหาก | ✓ ตรงตาม scope |

**สรุป scope guard: 4/5 หัวข้อผ่านสะอาด · 1/5 (costing/valuation) พบ scope creep จริงที่ต้องจัดการก่อนเข้า FRD**

---

## 🔴 Gaps

### G-01 · Scope creep: Valuation/Costing feature ไม่ได้ประกาศใน PREBRIEF และขัดกับ §1 "ไม่ทำ" ตรง ๆ
**ที่พบ:** `StockByLocation.html`
- L790: comment `// FRD §0.3 + BR-D02: valuation + export = finance/auditor only.` — อ้างอิงเอกสารที่ไม่มีอยู่ในแพ็กนี้
- L801-803: `canValuation()`, `canValExport()`
- L2047-2050: ปุ่ม "ดูมูลค่า/ซ่อนมูลค่า" ใน balance drawer (เฉพาะ finance/auditor)
- L2135-2144: กล่อง `.val-box` แสดง "ต้นทุน/หน่วย" (`p.cost`) และ "มูลค่าคงเหลือ" (`r.on_hand * p.cost`)
- L1360-1374: export modal มี toggle "รวมมูลค่า" (`inclVal`) ที่ finance เท่านั้นกดได้

**ทำไมเป็นปัญหา:** PREBRIEF §1 ระบุชัดว่า **"ไม่ทำ: ... costing engine (VD-PDM-07)"** — ฟีเจอร์นี้คือ costing/valuation
display ตรงตัว (ต้นทุน × จำนวน = มูลค่า) ซึ่งไม่ถูกกล่าวถึงใน OB ใด ๆ, Scenario ใด ๆ, หรือ FUNCTION_CHECKLIST
เลยแม้แต่ข้อเดียว — ดูเหมือนเป็นโค้ดตกค้างจาก ENC base pack (OB-1 ระบุว่า ENC = "superset" ที่ควรถูกตัดออกส่วนที่
เกิน scope) ที่ไม่ถูก trim ออกตอน rebrand

**ผลกระทบ:** ถ้าไปต่อ FRD/dev โดยไม่แก้ จะกลายเป็นฟีเจอร์ costing ที่ไม่มี business rule/security review รองรับ
(BR-D02/FRD §0.3 ที่ code อ้างถึงไม่มีอยู่จริง) — เสี่ยงข้อมูลต้นทุนรั่วไหลโดยไม่ได้ตั้งใจ และเสี่ยง scope
mismatch ตอนเทียบ FRD กับ HTML ในรอบ 2

**แนะนำ (ไม่ได้แก้เอง เพราะเป็น business decision):**
1. ถ้าทีมต้องการ valuation จริง → ต้องเพิ่มเป็น OB/S/FN ใหม่ใน PREBRIEF ก่อน (พร้อม security review เพราะเป็น
   ข้อมูลอ่อนไหว) แล้วเขียน FRD ให้ตรง
2. ถ้าไม่ต้องการ (ตรงตาม §1 เดิม) → ต้องตัดออกจาก HTML ก่อนส่งต่อ FRD stage (ปุ่ม, val-box, canValuation/
   canValExport, inclVal toggle)

**Severity:** ไม่ใช่ block-severity ต่อ OB/S/FN ที่ประกาศไว้ (ทุกข้อยังผ่านครบ) แต่เป็น **scope-governance
issue ที่ต้องปิดก่อนรอบ 2 (FRD)** — จึงปรับ verdict เป็น WARN ไม่ใช่ PASS

## 🟡 Warnings / Observations (ไม่กระทบ verdict เพิ่มเติม)

### W-01 · FN-40 (build/test gate) ไม่ได้ตรวจซ้ำในรอบนี้
FN-40 เป็นสิ่งที่ FUNCTION_CHECKLIST ระบุว่าผ่านแล้ว (`node --check`, audit navy=0, Playwright 60+ PASS, md5)
— นี่คือขอบเขตของ qc-ux-html-checker/CI ไม่ใช่ coverage-checker เชิง business scope จึงไม่ตรวจซ้ำในรอบนี้
ตามหลักการแบ่งงานของสอง skill (ไม่ใช่ gap แต่เป็นการชี้แจงขอบเขต)

### W-02 · OQ-INV-01..05 ยังไม่เคาะ — ตามที่ PREBRIEF ระบุไว้แล้วว่าเป็นหนี้ก่อน dev handoff
ไม่ใช่ gap ใหม่ที่พบจากรอบนี้ — PREBRIEF §6 และ FUNCTION_CHECKLIST "หนี้/รอเคาะ" ระบุไว้ตรงไปตรงมาอยู่แล้วว่า
ต้องปิดก่อนเข้า FRD/dev — บันทึกไว้เป็น reminder เดียวกับต้นทาง ไม่ใช่การค้นพบใหม่

## ⬜ NOT-CHECKED

- FN-40 (build/test/gate infra) — เหตุผลตามที่ระบุใน W-01
- ไม่มีรายการ business-facing (OB/S/FN) ที่ NOT-CHECKED — ทุกข้อมี UI evidence ชี้ตำแหน่งจริง

## 💡 ข้อเสนอ (ไม่กระทบ verdict)

- ควรตัดสินใจเรื่อง G-01 (valuation/costing) ก่อนเริ่ม brd-generator-full/frd-generator-v6 สำหรับแพ็กนี้
  เพื่อไม่ให้ scope mismatch ไหลต่อไปที่ FRD/TC ในรอบ 2 — เสนอให้ทีม (Strike) เคาะพร้อมกับ OQ-INV-01..05
  ในรอบเดียวกันเพราะเป็นการตัดสินใจระดับ business เหมือนกัน

---
---

# Coverage Report — F-INV-001 Stock by Location (รอบ 2: FRD vs PREBRIEF)

> **หมายเหตุการปรับใช้ (adaptation notice, ต่อเนื่องจากรอบ 1):** feature นี้ไม่มี `workflow_graph.json` /
> `NODE_BRIEF` จึงใช้ **PREBRIEF_F-INV_Stock-by-Location.md เป็น contract โดยตรงต่อเนื่อง** ตามแบบอย่าง
> F-CUST-001 round 2 — แทนที่ node/edge/golden-rule ด้วย: **Obligations (OB-1..12), block-severity
> Scenarios (S-05/05b/06/07/09/10/11), Business Rules (BR-01..11), Edge Cases (EC-INV-01..07),
> Open Questions (OQ-INV-01..06), Locked Decisions (LD-01/LD-02)**. รอบ 2 นี้ตอบคำถามคนละข้อกับรอบ 1:
> รอบ 1 ถาม "UI มีทาง/ปุ่ม/สถานะรองรับครบมั้ย" (ตอบแล้ว WARN เพราะ G-01) — รอบ 2 ถาม **"FRD spec เขียนเนื้อหา
> จริงครบมั้ย (ไม่ใช่แค่ชื่อ rule) และมี test scenario ผูกกลับแต่ละ block rule/exception path จริงมั้ย"**

## ⚠️ Sequencing Limitation (ต้องเปิดเผยตรง ๆ ก่อนอ่านต่อ)

**`testcases-f-inv.md` (จาก `ai-testcase-md-generator`) ยังไม่ถูกผลิตสำหรับแพ็กนี้ ณ จุดนี้ของ pipeline** —
ตามลำดับงานจริง SOW3.5 (ai-testcase-md-generator) เกิดหลัง SOW3.3 (frd-generator-v6) เสมอ ดังนั้นทุกคอลัมน์
**"TC (dedicated testcases-f-inv.md)"** ในรายงานนี้ถูก mark เป็น **`⬜ PENDING — NOT-CHECKED-YET`** อย่างตรงไปตรงมา
ไม่มีการสร้าง TC-ID ปลอมขึ้นมาเพื่อให้ตารางดูครบ สิ่งที่ตรวจแทนได้ ณ จุดนี้คือ **FRD `06_TESTS.md`
(Acceptance Criteria AC-01..AC-17 + XT-01/02, เขียนโดย frd-generator-v6.1 เอง ไม่ใช่ AI testcase generator)**
ซึ่งเป็นหลักฐานที่มีอยู่จริงในมือตอนนี้ — ใช้เป็น **proxy evidence ชั้นที่ 1** เท่านั้น ไม่ใช่ตัวแทนของ
dedicated TC file รอบถัดไปยังต้องมาตรวจ dedicated TC อีกครั้งแยกจากรอบนี้

- วันที่: 2026-08-10 · contract: `PREBRIEF_F-INV_Stock-by-Location.md` (เดียวกับรอบ 1)
- Artifacts ที่ตรวจรอบนี้: `03_FRD/` ทั้ง 9 ไฟล์ + INDEX (เน้น `05_RULES.md`, `06_TESTS.md`,
  `07_LOCKED_DECISIONS.md`, `00_OVERVIEW.md §0.8/§0.12`) — **ไม่มี** `testcases-f-inv.md` (ยังไม่ผลิต)
- Checklist จาก contract: OB 12 (เทียบเนื้อหาจริงใน `05_RULES`) · block-severity scenario 7
  (S-05/05b, S-06, S-07, S-09, S-10, S-11) · OQ-INV-01..05 (+ OQ-INV-06 ใหม่จากรอบ 1) · LOCKED
  decisions 2 (LD-01, LD-02)

## Verdict: 🟡 WARN (คงระดับเดิมจากรอบ 1 — ไม่ upgrade เป็น PASS เพราะ G-01 ยังไม่ปิด)

สรุป: **OB 12/12 ✓ มีเนื้อหาจริงใน FRD ไม่เจือจาง (9 ข้อลง BR-01..11 ตรง ๆ, OB-1/9/10 เป็น UI/interaction
pattern ที่ไปลง `01_UI.md`/`06_TESTS.md AC-15` แทนแทนที่จะเป็น BR — ไม่ใช่การหาย) · block-severity scenario
7/7 มีเนื้อหา FRD จริง + มี Acceptance Criteria ใน `06_TESTS.md` ผูกกลับตรงจุดทุกข้อ (proxy evidence ชั้น 1) ·
OQ-INV-01..05 ทั้งหมดถูก carry เข้า FRD `00_OVERVIEW.md §0.8` แบบ verbatim-in-meaning ไม่มีข้อใดถูกเคาะคำตอบเอง
(ตรวจแล้วว่าไม่มีการ "ปิดเงียบ") + OQ-INV-06 (G-01) ใหม่ถูกสร้างและผูกกับ LD-02 ตรงตามที่รอบ 1 คาดหวัง ·
LD-01/LD-02 มีจริงใน `07_LOCKED_DECISIONS.md` และไม่ขัดกับ PREBRIEF** — **ไม่มี block rule ใดถูกเจือจางหรือหาย
จาก FRD** จึงไม่ยกระดับเป็น BLOCK แต่ verdict **คงเป็น WARN ต่อเนื่องจากรอบ 1** เพราะ (a) G-01/OQ-INV-06 เอง
ยังเป็น open item ที่ "must close before dev sign-off" ตามคำพูดของ FRD เอง — การ carry-forward ถูกต้องไม่ทำให้
ปัญหาต้นตอหายไป และ (b) **TC ระดับ dedicated (testcases-f-inv.md) ยังไม่มีอยู่จริง** — coverage ที่แท้จริงต่อ
block rule ยังพิสูจน์ไม่ได้เต็มร้อย จนกว่าไฟล์นั้นจะถูกผลิตและตรวจซ้ำ

---

## Coverage Matrix — Obligations vs FRD Content Depth (OB-1..12)

| OB | FRD content จริง (ไม่ใช่แค่ชื่อ) | Section | TC (dedicated) |
|---|---|---|---|
| OB-1 ENC superset rebrand | ✓ ไม่ใช่ business rule — ลงใน `01_UI.md §1.0` (Sync Read CI note) ตามคาด ไม่ใช่ gap | `01_UI §1.0` | ⬜ PENDING |
| OB-2 2-code model | ✓ BR-01 เต็ม statement + enforcement point (`04_DB` field shape + FN-05) — ไม่เจือจาง | `05_RULES` BR-01 | ⬜ PENDING (proxy: `06_TESTS` AC-01 pt.5) |
| OB-3 Service exclusion | ✓ BR-02 เต็ม — ระบุทั้ง client-side guard (`isStockable`) และ server-side requirement (`is_stock_item=false`) + error code `ERR_SERVICE_ITEM_NOT_STOCKABLE` | `05_RULES` BR-02 | ⬜ PENDING (proxy: AC-01 pt.4, AC-06) |
| OB-4 1 loc 1 uom + base ledger | ✓ BR-03 เต็ม + ผูก Engine จริง (`ENG-INV-01`) + เปิด OQ-INV-03 ไว้ตรง ๆ (ไม่ปิดเงียบเรื่อง governance การเปลี่ยนหน่วย) | `05_RULES` BR-03 | ⬜ PENDING (proxy: AC-02, AC-03) |
| OB-5 List 1 แถว/สินค้า | ✓ BR-04 เต็ม — ระบุชัดว่าตัด "total ข้ามหน่วย" ตรงตาม PREBRIEF คำต่อคำ | `05_RULES` BR-04 | ⬜ PENDING (proxy: AC-01 pt.3) |
| OB-6 Low stock (min_stock) | ✓ BR-05 เต็ม + เปิด OQ-INV-02 ไว้ตรง ๆ (per-item vs per-warehouse ยังไม่เคาะ แต่บอกพฤติกรรมที่ built จริงตอนนี้) | `05_RULES` BR-05 | ⬜ PENDING (proxy: AC-07) |
| OB-7 สถานะ 3 ค่า | ✓ BR-06 เต็ม — ระบุ priority (negative > low) ชัดเจน ไม่มีใน PREBRIEF ตรง ๆ แต่เป็นการอนุมานที่สมเหตุผลจาก S-08/S-08b ไม่ขัดแย้ง | `05_RULES` BR-06 | ⬜ PENDING (proxy: AC-01, AC-07, AC-08) |
| OB-8 Adjust สร้าง balance ใหม่ | ✓ BR-07 เต็ม (create-new-balance) — เนื้อหาตรง ไม่เจือจาง | `05_RULES` BR-07 | ⬜ PENDING (proxy: AC-09) |
| OB-9 Overlay Portal + Esc chain | ✓ ไม่ใช่ business rule — ลงใน `01_UI.md` component note + มี AC เฉพาะ (`AC-15` two-stage Esc) — ครบ ไม่ใช่ gap | `01_UI §1.0`, `06_TESTS` AC-15 | ⬜ PENDING |
| OB-10 No hint | ✓ ไม่ใช่ business rule — ลงใน `01_UI.md` (verified absent) — ครบ | `01_UI §1.0` | ⬜ PENDING |
| OB-11 Allocated untouchable + append-only | ✓ แยกเป็น **2 rules ชัดเจนกว่า PREBRIEF เดิม**: BR-08 (allocated ceiling, เนื้อหาละเอียดกว่าเดิมด้วยรายการ error code 5 ตัว) + BR-09 (append-only, ผูก DB-permission-level ไม่ใช่แค่ UI convention) — ไม่เจือจาง แน่นกว่าเดิม | `05_RULES` BR-08, BR-09 | ⬜ PENDING (proxy: AC-10, AC-11, AC-12) |
| OB-12 RBAC | ✓ BR-10 เต็ม — ระบุ 3 roles ที่ถูกกัน + server-side re-check ที่ endpoint ระดับ (API-08/11/14/15/16) ไม่ใช่แค่ page-load | `05_RULES` BR-10 | ⬜ PENDING (proxy: AC-13) |

**OB coverage รอบ 2: 12/12 ✓ ทุกข้อมีเนื้อหาจริงใน FRD (9 ลง BR ตรง ๆ + 3 ลง UI/interaction pattern อย่างถูกที่)
ไม่มีข้อใดเจือจางหรือหายไป · TC dedicated 0/12 (PENDING ทั้งหมดตามลำดับ pipeline ที่ประกาศไว้)**

---

## Coverage Matrix — Block-Severity Scenarios (S-05/05b, S-06, S-07, S-09, S-10, S-11)

| Scenario | FRD content (BR + engine) | FRD `06_TESTS.md` AC (proxy evidence) | TC (dedicated) |
|---|---|---|---|
| S-05/05b create-new-balance | ✓ BR-07 เต็ม + `FN-17 detectNewBalanceLine`/`FN-18 submitAdjustmentBatch` (upsert path) ระบุชื่อฟังก์ชันจริง | ✓ AC-09 — ครบ 4 ขั้นตอน รวม label suffix verbatim "· ว่าง — เพิ่มเข้าได้" | ⬜ PENDING |
| S-06 ลดชนเพดานจอง (block) | ✓ BR-08(e) เต็ม — "allocated is never touched by this rule, only read as a ceiling" ระบุชัด + error code `ERR_EXCEEDS_ALLOCATED_CEILING` พร้อม verbatim message | ✓ AC-10 — 5 ขั้นตอน รวมการยืนยันว่า allocated ไม่เปลี่ยนหลัง submit (ผ่าน audit log before/after) | ⬜ PENDING |
| S-07 loc/master ไม่พร้อม (block) | ✓ BR-08(a)(b)(c) เต็ม — แยก 3 เงื่อนไข (locked/blocked-frozen/master-inactive) + นัยสำคัญ "reduce ยังทำได้แม้ master inactive" ระบุชัดไม่กำกวม | ✓ AC-11 — 3 sub-cases ครบ รวม cross-link ไป AC-14 (BP lock) | ⬜ PENDING |
| S-09 สินค้าบริการไม่โผล่ picker | ✓ BR-02 (ร่วมกับ OB-3) — enforcement ระบุทั้ง client+server | ✓ AC-06 — ยืนยันว่า `SV-8001` ไม่โผล่แม้ค้นด้วย code ตรง | ⬜ PENDING |
| S-10 สิทธิ์ (RBAC) | ✓ BR-10 เต็ม — ระบุ conditional-render (ไม่ใช่ disabled) + server-side re-check ทุก endpoint | ✓ AC-13 — 3 ขั้นตอน รวมข้อ 3 ที่ระบุชัดว่าต้องทดสอบ server-side 403 ด้วย ไม่ใช่แค่ UI | ⬜ PENDING |
| S-11 Break/Pack lock (bounded exception) | ✓ BR-11 เต็ม — ระบุ transaction-atomicity nuance (PR-8, "partial failure would strand a locked location") ที่ PREBRIEF เดิมไม่ได้พูดถึงระดับนี้ + precondition `ERR_UNASSIGNED` | ✓ AC-14/AC-14b — ครบทั้ง create/complete/cancel รวม toast verbatim | ⬜ PENDING |

**Block-severity scenario coverage รอบ 2: 7/7 ✓ มีเนื้อหา FRD จริง (ไม่เจือจาง, บางข้อละเอียดกว่า PREBRIEF เดิม
ในทางที่สอดคล้องกัน ไม่ขัดแย้ง) + 7/7 มี AC ใน `06_TESTS.md` ผูกกลับตรงจุด (proxy evidence) · TC dedicated
0/7 (PENDING) — **ไม่มี block rule ใดหายหรือถูกลดเป็น warn** จึงไม่ยกระดับเป็น BLOCK**

---

## Coverage Matrix — Open Questions (OQ-INV-01..06)

| OQ | สถานะใน PREBRIEF | สถานะใน FRD `00_OVERVIEW.md §0.8` | ตรวจแล้วว่า... |
|---|---|---|---|
| OQ-INV-01 (DOA threshold) | Open, owner Strike | ✓ Carried verbatim-in-meaning, ไม่ blocking, owner คงเดิม | ไม่ถูกเคาะคำตอบเองโดย FRD |
| OQ-INV-02 (min_stock scope) | Open, owner Strike+พี่เบิร์ด | ✓ Carried, ไม่ blocking, owner คงเดิม | ไม่ถูกเคาะคำตอบเองโดย FRD (BR-05 ระบุพฤติกรรม as-built เท่านั้น ไม่ใช่การตัดสิน) |
| OQ-INV-03 (unit change governance) | Open, owner Strike | ✓ Carried, ไม่ blocking, owner คงเดิม | ไม่ถูกเคาะคำตอบเองโดย FRD (BR-03 ระบุตรงว่า "describes current runtime behavior, not the governance") |
| OQ-INV-04 (negative stock ownership) | Open, owner Strike+ทีมขาย | ✓ Carried, **upgrade เป็น blocking-for-go-live** ใน FRD (เดิม PREBRIEF ไม่ได้ระบุ blocking flag ชัด) | ไม่ถูกเคาะคำตอบเอง — FRD เพิ่มความเข้มงวดขึ้น ไม่ใช่ลดทอน |
| OQ-INV-05 (low-stock downstream action) | Open, owner Strike | ✓ Carried, ไม่ blocking, owner คงเดิม + มี XT-01 ใน `06_TESTS.md` กำชับ QA ว่าไม่ใช่ bug | ไม่ถูกเคาะคำตอบเอง |
| OQ-INV-06 (G-01, ใหม่จากรอบ 1) | ไม่มีใน PREBRIEF (พบระหว่าง round 1) | ✓ สร้างใหม่ตรงตามที่รอบ 1 คาดหวัง, ผูกกับ LD-02, ระบุ **"blocking — must close before dev sign-off"** | ไม่ถูกเคาะคำตอบเอง — FRD ปฏิเสธเลือกข้างอย่างชัดเจน (ดู LD-02) |

**OQ coverage รอบ 2: 6/6 ✓ ถูก carry เป็น pending คำถามจริง ไม่มีข้อใดถูก "เคาะคำตอบเงียบ ๆ" โดย FRD** — ตรงตาม
เกณฑ์ที่ round 2 ต้องตรวจ (§0.12.4 ของ FRD เองก็ยืนยันตัวเลข 5/5 + 1 ใหม่ ตรงกับที่ตรวจอิสระในรายงานนี้)

---

## Coverage Matrix — Locked Decisions (LD-01, LD-02)

| LD | เนื้อหาใน `07_LOCKED_DECISIONS.md` | ขัดกับ PREBRIEF มั้ย |
|---|---|---|
| LD-01 (1440px modal, ไม่ใช่ drawer) | ✓ มีจริง — อ้าง OB-8 "มติ 2026-08-09" ตรงกับ PREBRIEF ที่ระบุ "modal กว้าง ~1392px" (ตัวเลขจริงจาก CSS คือ `min(1440px, calc(100vw-48px))` — ต่างจาก "~1392px" เล็กน้อยเพราะ "~" เป็นค่าประมาณใน PREBRIEF เอง ไม่ใช่การขัดแย้ง) + อ้างอิง `_UX_CHECK_REPORT.md` corroboration | ✗ ไม่ขัด — สอดคล้องกันโดยตรง |
| LD-02 (G-01 ไม่ถูกเคาะ) | ✓ มีจริง — ระบุชัดว่า FRD **ไม่เลือกข้าง** (ไม่ spec ว่าเก็บ ไม่ spec ว่าต้องตัดออก) พร้อมเงื่อนไขทั้งสองทางถ้าจะปิดในอนาคต (keep → ต้องมี OB/S/FN ใหม่ + Security Bible D5; remove → ต้อง patch HTML) | ✗ ไม่ขัด — ตรงตาม PREBRIEF §1 "ไม่ทำ: costing engine" (FRD ไม่ได้ spec มันเป็น in-scope) |

**LD coverage: 2/2 ✓ มีจริง ไม่ขัดกับ PREBRIEF ทั้งคู่**

---

## 🔴 Gaps

**ไม่มี block-severity gap ใหม่ในรอบนี้** — ไม่มี block rule (BR-08(a-e), BR-02, BR-10, BR-11) ที่ขาดเนื้อหาจริง
ใน FRD หรือถูกเจือจาง (เช่น block→warn) และไม่มี OQ ใดถูกเคาะคำตอบเองอย่างเงียบ ๆ

## 🟡 Warnings / Observations

### W-07 · G-01/OQ-INV-06 ยังไม่ปิด — carry ถูกต้อง แต่ยังเป็นหนี้จริงก่อน dev sign-off
รอบ 1 พบ scope creep (costing/valuation) → รอบ 2 ยืนยันว่า FRD **ไม่ได้ปิดเงียบ** เรื่องนี้ — สร้าง OQ-INV-06 +
LD-02 ตรงตามที่ควร แต่ตัวปัญหาเองยังไม่ถูกตัดสินใจ (เก็บหรือทิ้ง feature valuation)
**แก้ที่:** ต้องให้ Strike เคาะก่อน dev handoff ตามที่ `00_OVERVIEW.md §0.8` ระบุว่า "blocking" — ไม่ใช่งานของ
coverage checker ที่จะเลือกแทน

### W-08 · TC ระดับ dedicated (testcases-f-inv.md) ยังไม่มี — coverage ยังพิสูจน์ไม่ได้เต็มร้อย
`06_TESTS.md` (AC-01..17 + XT-01/02) เป็นเนื้อหาที่ดีและ trace กลับ BR ได้ครบ 7/7 block scenario แต่มันคือ
Acceptance Criteria ที่ frd-generator เขียนเอง ไม่ใช่ dedicated test-case markdown ที่ผ่าน
`ai-testcase-md-generator` ซึ่งจะ anchor กับหน้าจอจริง + มี TC-ID + ตาราง ☐ ผลแยกกันสำหรับ AI agent รัน
**แก้ที่:** ต้องรัน `ai-testcase-md-generator` เป็นขั้นถัดไปตาม pipeline แล้วเทียบ `testcases-f-inv.md`
กับ AC-01..17 อีกรอบ (round 3 หรือ round 2.5) ก่อนเข้า dev — โดยเฉพาะ 7 block scenario ที่ตารางนี้ระบุไว้ต้องมี
TC-ID จริงอย่างน้อย 1 เคสต่อ scenario

## ⬜ NOT-CHECKED

- **TC (dedicated) ทุกแถวในทุกตาราง** — เหตุผล: `testcases-f-inv.md` ยังไม่ถูกผลิต ณ จุดนี้ของ pipeline
  (ตามลำดับงานที่ประกาศไว้ ai-testcase-md-generator เกิดหลัง frd-generator-v6) — นี่คือ disclosed limitation
  ไม่ใช่การมองข้าม ต้องตรวจซ้ำเมื่อไฟล์นั้นถูกผลิต
- EC-INV-01..04 (concurrency/idempotency) — ตรงตามที่ `06_TESTS.md §6.7` ระบุเองว่า "not expressible as UI
  acceptance criteria in this pass" ต้องเป็น server-side integration test ตอน build จริง ไม่ใช่ NOT-CHECKED
  เพราะมองข้าม แต่เพราะเป็นข้อจำกัดของ client-side prototype ที่ FRD เองก็ระบุตรง ๆ

## 💡 ข้อเสนอ (ไม่กระทบ verdict)

- เมื่อ `ai-testcase-md-generator` ผลิต `testcases-f-inv.md` แล้ว ควรรัน qc-coverage-checker รอบ 2 ซ้ำ
  (หรือรอบ "2.5") เฉพาะคอลัมน์ TC dedicated เทียบกับตาราง block-severity scenario 7 ข้อในรายงานนี้ —
  ไม่ต้องตรวจ FRD content ซ้ำเพราะรอบนี้ยืนยันแล้วว่าเนื้อหาไม่เจือจาง
- G-01/OQ-INV-06 ควรถูก track เป็น blocking backlog item แยกจาก OQ-INV-01..05 (ที่ไม่ blocking) เพื่อไม่ให้
  ปนกันตอน Strike เคาะ

---

## Diff จากรอบ 1 (HTML vs PREBRIEF) → รอบ 2 (FRD vs PREBRIEF)

| หัวข้อ | รอบ 1 (HTML) | รอบ 2 (FRD) |
|---|---|---|
| G-01 scope creep (costing/valuation) | 🔴 Gap — พบใน HTML, ไม่มี business rule รองรับ, ขัด PREBRIEF §1 ตรง ๆ | **ยังเปิดอยู่ (ไม่ปิด)** — แต่ carry ถูกต้องเป็น OQ-INV-06 + LD-02 ที่ระบุ "blocking — must close before dev sign-off" อย่างตรงไปตรงมา ไม่ถูกเคาะคำตอบเองในทางใดทางหนึ่ง |
| OQ-INV-01..05 | ระบุใน PREBRIEF §6 ว่ายังไม่เคาะ (ไม่ใช่ gap ที่รอบ 1 ค้นพบใหม่) | ✓ Carried ครบ 5/5 verbatim-in-meaning ใน FRD §0.8 — ไม่มีข้อใดถูกปิดเงียบ (OQ-INV-04 ถูกยกระดับเป็น blocking-for-go-live โดย FRD เอง ซึ่งเข้มงวดขึ้น ไม่ใช่ลดทอน) |
| Block-severity behavior (BR-08 ceiling/lock, BR-02 SV exclusion, BR-10 RBAC, BR-11 BP lock) | ไม่ได้ตรวจในรอบ 1 (รอบ 1 ตรวจ OB/S/FN ระดับ UI evidence เท่านั้น) | ใหม่ในรอบนี้ — ตรวจแล้ว 7/7 ✓ มีเนื้อหา FRD จริงไม่เจือจาง + มี AC ใน `06_TESTS.md` ผูกกลับ (proxy evidence) |
| LD-01 (1440px modal) | ไม่ได้ประกาศเป็น LD ในรอบ 1 (แค่สังเกตเป็น UX deviation ผ่าน `_UX_CHECK_REPORT.md`) | ใหม่ — formalize เป็น LD-01 ใน `07_LOCKED_DECISIONS.md` ตรงกับ PREBRIEF OB-8 ไม่ขัดแย้ง |
| Gap ที่ปิดแล้ว | — | **ไม่มี** — G-01 ยังไม่ถูกปิด เพียงถูก carry ถูกต้อง |
| Gap ที่ยังค้าง | G-01 (WARN) | G-01/OQ-INV-06 (WARN ต่อเนื่อง) — ไม่ upgrade เป็น BLOCK เพราะไม่มีการเจือจาง/ปิดเงียบ แต่ยังไม่ resolve |
| Gap ใหม่ | — | **W-08 (TC dedicated ยังไม่มี)** — เป็น sequencing limitation ที่ประกาศไว้ล่วงหน้า ไม่ใช่การค้นพบ block-severity ใหม่ |

**สรุป diff:** verdict คงเป็น 🟡 WARN ทั้งสองรอบ ด้วยเหตุผลคนละมิติ — รอบ 1 WARN เพราะ **พบ** G-01 ในของจริง (HTML)
รอบ 2 WARN เพราะ G-01 **ยังไม่ถูกปิด** แม้จะถูก document ไว้ถูกต้องแล้ว (ไม่ใช่ coverage failure ของ FRD-writing
เอง — เป็น business-decision debt ที่ carry ต่อ) ส่วนเนื้อหา FRD เอง (BR/EC/error catalog/D-CLASS) ผ่านทุกจุดที่
ตรวจได้ ณ ตอนนี้ — ข้อจำกัดเดียวที่แท้จริงของรอบนี้คือ **TC dedicated ยังไม่มี** ซึ่งเป็นลำดับ pipeline ที่รู้
ล่วงหน้าอยู่แล้ว ไม่ใช่สิ่งที่ทีมพลาด

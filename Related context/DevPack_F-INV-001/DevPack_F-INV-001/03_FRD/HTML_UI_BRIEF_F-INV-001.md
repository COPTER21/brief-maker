# HTML UI Brief — F-INV-001 สต็อกตามตำแหน่ง (Stock by Location)

> สำหรับ FE dev เริ่มงานเร็ว — อ่านไฟล์นี้ก่อน `FRD_F-INV-001_Pack/01_UI.md` เต็ม ๆ
> Source: `StockByLocation.html` (gate-passed: UX **PASS with WARNINGS** · Coverage round 1+2 **WARN** —
> ดู §7 ก่อนเริ่มงาน มี known gap ระดับ business ที่ยังไม่เคาะ) · FRD Pack (9 ไฟล์, `03_FRD/`)

---

## 1. Entry & Routing

✅ **มี hash routing จริง** — ไม่ใช่ SPA state-only แบบ F-CUST-001 sibling. `StockByLocation.html` ใช้
router ที่ประกาศไว้ชัดใน comment (L1251-1260):

```
#/stock                        → GATE (เลือกคลังอย่างเดียว)
#/stock/{ctx}/sku              → by-SKU (ctx = all | WH-01 | WH-02)
#/stock/{ctx}/sku/{balanceId}  → by-SKU + balance drawer
#/stock/{wh}/loc               → by-location (wh = WH-01 | WH-02)
#/stock/{wh}/loc/{locId}       → by-location + location detail drawer
```

**ต่างจาก PREBRIEF เล็กน้อย** — PREBRIEF §2 เขียนย่อว่า route คือ `#/stock/{wh}` และ product drawer คือ
`/sku/{pid}` — ของจริงในโค้ดคือ `#/stock/{ctx}/sku` (ctx รวม `all` ด้วย ไม่ใช่แค่ wh) และ balance drawer
route ใช้ `balanceId` ไม่ใช่ `pid` ตรง ๆ (ดู `openDrawer()` L1337: `navigate('stock/' + (state.whCtx||'all') +
'/sku/' + id)`) — เป็นการเขียนย่อของ PREBRIEF ไม่ใช่ความขัดแย้งเชิง business

**หลักฐานเป็น router จริง ไม่ใช่ state-only:**
- `getRoute()` L1261 อ่าน `location.hash` จริง + parse path segments
- `navigate(path)` L1271: `location.hash = '#/' + path`
- `syncRouteToState()` L1275 sync hash → `state.view`/`state.whCtx`/`state.drawer` ทุกครั้งที่ `render()` (L3052)
- `window.addEventListener('hashchange', render)` L3107 — comment ระบุ "Check B — refresh-safe routing"
- default route: `if (!location.hash) location.hash = '#/stock';` (L3112) — **refresh-safe จริง**: เปิด URL
  ตรง ๆ ที่มี hash (เช่น `#/stock/WH-01/sku/S011`) แล้ว refresh ก็ยังเปิด balance drawer เดิมอยู่ (ผ่าน
  `render()` → `renderDrawer()` + apply `.is-open` class L3061-3067)
- scoped role (`warehouse_staff`) ข้าม gate อัตโนมัติ ล็อก ctx = คลังตัวเอง (`roleScope()` ใน `syncRouteToState`
  L1278-1282)

**Esc handling:** `window.addEventListener('keydown', ...)` L3100-3101 — ปิด modal ก่อน ถ้าไม่มี modal เปิดถึงปิด
drawer (Iron Rule #15) — เป็นคนละชั้นกับ Esc chain ของ dropdown-in-modal (ดู §4 Manual Adjustment)

**จุดเข้า:** เปิดไฟล์ → ไม่มี hash → auto-set `#/stock` → `renderGate()` (เลือกคลัง) ถ้า role ไม่ scoped;
role `warehouse_staff` ข้าม gate ตรงเข้า list ของคลังตัวเอง

---

## 2. CI Snapshot (Warm Light — Sync Read จาก html-generator-v8)

| Token | ค่า |
|---|---|
| Ground | Ivory `#FAF8F5` |
| Text/Sidebar | Charcoal `#111111` (flat) |
| Action/Priority | Red `#FF3B30` |
| Connection | Orange `#FF9A1F` |
| Font | Satoshi + Noto Sans Thai (fixed post-QC — ดู §7) |
| Sidebar | 232px flat charcoal · Shell-bar 52px ขาว |
| Drawer | **920px** (v2 standard — fixed จาก legacy 540px โดย qc-ux-html-checker, ดู §7) |
| Manual Adjustment Modal | **`min(1440px, calc(100vw - 48px))`** — ไม่ใช่ 440px มาตรฐาน (Pattern D) หรือ drawer — ดู deviation ที่ยอมรับแล้วใน §7 |

ค่าจริงยึด Sync Read จาก `html-generator-v8/knowledge/ci-tokens.md` เสมอ — ไม่ hardcode ซ้ำในไฟล์นี้
เพื่อกัน spec โกหกถ้า CI เปลี่ยนรุ่น

---

## 3. Pages / Routes / Patterns

| Page/Overlay ID | ชื่อ | Pattern | ความกว้าง | Role ที่เข้าได้ |
|---|---|---|---|---|
| GATE | เลือกคลัง | A variant (gate) | full | ทุก role ที่ไม่ scoped (`renderGate()` L1425); `warehouse_staff` ข้าม gate อัตโนมัติ |
| P-01 | สต็อกตามสินค้า (list, agg) | A (list-view) | full | ทุก role เห็น; scoped role ล็อกคลังตัวเอง (`renderList()`) |
| P-02 | สต็อกตามตำแหน่ง (location view) | A variant | full | ทุก role (`renderLocationView()` L1653) |
| P-03 | แตก/แพ็ค (Break/Pack) | A variant | full | ทุก role ดู; สร้างคำสั่งจริงตาม `canAdjust()` guard ภายใน form (`renderBreakPackView()` L2475) |
| P-04 | ประวัติการปรับสต็อก (Audit log) | A variant (read-only) | full | ทุก role ดู; append-only (`renderAdjLogView()` L2736) |
| D-01 | Product drawer (3 แท็บ) | C (view tabbed) | 920px | ทุก role; ปุ่มปรับสต็อก gate ด้วย `canAdjust()`, ปุ่มดูมูลค่า gate ด้วย `canValuation()` (`renderProductDrawer()` L1903) |
| D-02 | Location drawer | C variant | 920px | ทุก role (`renderLocationDrawer()` L1797) |
| D-03 | Balance drawer (ต่อ pid+loc) | C variant | 920px | ทุก role; header actions ปรับสต็อก/ดูมูลค่า gate ตาม role (`renderDrawer()` L2010-2068) |
| M-01 | Manual Adjustment (line editor) | B2 variant (**modal ไม่ใช่ drawer** — deviation) | `min(1440px, 100vw−48px)` | เฉพาะ `canAdjust()`=true เข้าถึงปุ่ม (`openAdjust()` L2577, `renderAdjModal()` L2653) |
| M-02 | Break/Pack order form | modal/inline form | — (อยู่ใน `renderBreakPackView`) | ปุ่มสร้างคำสั่งจริง gate เช่นเดียวกับ adjust |
| Confirm | ยืนยัน complete/cancel BP order | D (confirm) | 440px | ผู้ที่กด "เสร็จ"/"ยกเลิก" บน order ที่ locked (`completeBPOrder`/`cancelBPOrder` L2368-2379) |

รายละเอียดเต็ม + evidence (function/line) → `FRD_F-INV-001_Pack/01_UI.md`

---

## 4. Component Map ต่อหน้า

### P-01 สต็อกตามสินค้า (list, aggregate)
- Stat row 4 ใบ: สินค้า (SKU) · ต่ำกว่าขั้นต่ำ · สต็อกติดลบ · ตำแหน่ง HOLD (L1535-1552) — 3 ใบแรกกดกรอง
  toggle ผ่าน `quickFlag()` (toggle ซ้ำ = ยกเลิก)
- ตาราง **1 สินค้า 1 แถว** (`skuAgg()` L1221 — รวมด้วยหน่วยฐานเสมอ) คอลัมน์: สินค้า · คงเหลือ · จองแล้ว ·
  พร้อมใช้ · สถานะสต็อก
- **สถานะสต็อก 3 ค่า** (chip เดียว, mutually exclusive, L1610-1615): `ขาดสต็อก` (แดง, `av<0`) →
  `ต้องเติม` (ส้ม, `low`) → `ปกติ` (ไม่มี badge/เขียว) — ลำดับ priority negative > low ตายตัว
- รหัสอ้างอิง 2 ชุดเสมอ (`fourCodeChips()` L2572) — ไม่มี `code_item`/`code_sku` หลงเหลือ
- ค้นหา/กรอง: `applyFilter()`, `toggleHideZero()`, sort ด้วยค่าฐาน (`key` map ใช้ `a.on/a.alloc/a.av`)
- Empty state 2 แบบ: ไม่พบสินค้าตามเงื่อนไข (filtered-to-zero, L1592) — ต่างจาก truly-empty (ยังไม่มีสินค้าเลย)
- แถวที่ inactive แสดงไอคอนเตือน `flag-warn` พร้อม title `"Master หยุดใช้งาน"` (L1604)

### P-02 สต็อกตามตำแหน่ง (location view)
- การ์ด/แถวต่อตำแหน่ง + utilization bar (`.util-bar`/`.util-fill`, 3 ระดับสี low/mid/high)
- Stat: ตำแหน่งมีของ · (ว่าง/มีของ แยกใน stat-meta L1699) · blocked count
- Empty state: `"ไม่พบตำแหน่งตามเงื่อนไข"` (L1758)
- คลิกแถว/การ์ด → เปิด Location drawer (D-02)

### D-02 Location Drawer
- Section หลัก: **"สิ่งที่อยู่ในตำแหน่งนี้"** พร้อม pill นับจำนวน SKU (`ph-count`, L1850)
- แสดงจำนวนตามหน่วยของ location (OB-4) — ฐานกำกับเมื่อ factor > 1 (`.q-base`)
- เจาะแต่ละแถวต่อเป็น Balance drawer (D-03) ได้ (route `/sku/S{id}`)

### D-01 Product Drawer (3 แท็บ, full-width tabs บนสุดนอก body — L1942-1944)
- Tabs: **ภาพรวม** (default) | **ตำแหน่งจัดเก็บ** | **การเคลื่อนไหว** — สลับด้วย `setTab()` L1358
- Header: title + pill `"Master หยุดใช้งาน"` ถ้า inactive (L1924) · จำนวนตำแหน่งจัดเก็บ (L1927)
- **ภาพรวม** (`renderOverviewTab()` L2080): สรุป 3 ใบฐาน (คงเหลือรวม/จองแล้ว/พร้อมใช้) + note ต่ำกว่าขั้นต่ำ
  ถ้าเข้าเงื่อนไข (ดู verbatim ใน §6) + การแปลงหน่วย + threshold + รหัส 2 ชุด — ไม่มี hint (OB-10)
- **ตำแหน่งจัดเก็บ** (`renderUomLocTab()` L2149): ตารางต่อ location แสดงหน่วยของ loc + สรุปเป็นฐาน
  (`grandBase`/`grandAlloc` ให้ Σ ตรงกับสรุปในภาพรวม)
- **การเคลื่อนไหว** (`renderMovesTab()` L2191, `getMoves()`): merge ทุก balance ของสินค้า + ใหม่สุดก่อน;
  empty state: `"ยังไม่มีการเคลื่อนไหว"` (L1995, L2194)

### D-03 Balance Drawer (ต่อ pid+loc คู่หนึ่ง)
- Header actions ตาม role: ปุ่ม **"ปรับสต็อก"** เมื่อ `canAdjust()`=true (L2041) → เปิด M-01 พร้อม
  pre-fill pid/loc; ปุ่ม **"ดูมูลค่า"/"ซ่อนมูลค่า"** toggle เมื่อ `canValuation()`=true (L2047-2050) —
  ดูหมายเหตุ scope creep ที่ §7 (G-01)
- แท็บ overview/moves/uomloc เหมือนกับ D-01 แต่ scope เฉพาะ balance เดียว

### M-01 Manual Adjustment (`renderAdjModal()` L2653 — modal 1440px, ไม่ใช่ drawer)
- Header: title "ปรับสต็อก (Manual Adjustment)" + subtitle verbatim: **"เพิ่ม/ลดสต็อกหลายรายการในครั้งเดียว —
  ปรับเฉพาะยอดคงเหลือ ห้ามแตะยอดจอง · บันทึก log ทุกครั้ง"** (L2660)
- เหตุผลการปรับ (บังคับ, dropdown 6 ค่า จาก `ADJ_REASONS` L1031): นับสต็อกประจำงวด (Cycle Count) · พบของเกิน ·
  ของหาย / สูญหาย · ของชำรุด / เสียหาย · รับเข้า manual (ไม่มีเอกสารรับ) · อื่นๆ
- **Line editor grid** (v8 B2, `adjg-head` L2674): หัวคอลัมน์ **สินค้า | ตำแหน่งจัดเก็บ | ปรับ | จำนวน |
  คงเหลือ | (ปุ่มลบ)** — เพิ่ม/ลบบรรทัดผ่าน `adjAddLine()`/`adjDelLine()` (L2586-2587); บรรทัดสุดท้ายลบไม่ได้
- **Live validation ต่อบรรทัด** (`adjLineError()` L2598-2610):
  - ลดเกิน `on_hand - allocated` → error (verbatim ดู §6)
  - location ล็อกจากคำสั่ง BP ที่ active → `"ตำแหน่งถูกล็อกโดยคำสั่งแตก/แพ็ค — รอดำเนินการเสร็จก่อน"` (L2601)
  - location blocked/frozen/master inactive → error ต่อบรรทัด
  - service (SV) ไม่มีใน dropdown สินค้าเลย (`prodOpts` กรองด้วย `isStockable`)
- **คงเหลือ live**: `"ปัจจุบัน n → หลังปรับ m"` (L2648) หรือ `"ลดได้สูงสุด X"` เมื่อจะเกินเพดาน (L2648)
- **เพิ่มเข้าตำแหน่งว่าง (new-balance flow)**: dropdown ตำแหน่งทุกตัวติด label ต่อท้าย
  `"· ว่าง — เพิ่มเข้าได้"` / `"· มีของ"` / `"· ล็อกอยู่"` (L2624) — เลือก loc ที่ยังไม่มีสินค้านี้ →
  แสดง `"รายการใหม่ในตำแหน่งนี้"` + `"ปัจจุบัน 0 → n"` (L2647); `isNew` flag คำนวณจาก `!inf.row` (L2633)
- **Summary bar** (`adj-summary`, L2682) — verbatim template:
  `"พร้อมบันทึก {ok}/{total} บรรทัด"` + `"เพิ่มรวม +{x} ชิ้นฐาน"` + `"ลดรวม −{y} ชิ้นฐาน"` +
  `"รายการใหม่ {z} ตำแหน่ง"` (แต่ละ span แสดงเฉพาะเมื่อค่า > 0)
- Submit (`submitAdjust()` L2696): update RAW ที่มีอยู่ หรือสร้างแถวใหม่ (branch `else` L2715-2720) →
  สร้าง ADJ doc เดียวหลายบรรทัด (`ADJLOG.unshift`) → movement ต่อ balance → toast เลขเอกสาร (รูปแบบ
  `ADJ-2026-NNNN`, zero-padded 4 หลัก, L2708)

### P-03 Break/Pack View (`renderBreakPackView()` L2475)
- Stat: รายการค้าง (ล็อกอยู่) (L2504) นับจาก `LOCKED_LOCS.size`
- ฟอร์มสร้างคำสั่ง: เลือกต้นทาง (ตำแหน่งที่มีของ) — error ถ้าไม่มี: `"เลือกต้นทางที่มีของก่อน"` (L2329);
  ถ้าไม่มีตัวเลือกเลย: `"ไม่มีของพร้อมใช้สำหรับสินค้านี้"` (L2939)
- Note คำเตือนผลกระทบ (exempt จาก no-hint rule ตาม Rule #33.3 — เป็น action-consequence ไม่ใช่ tutorial hint):
  verbatim **"เมื่อสร้าง: ของต้นทางถูกจอง (lock) + ตำแหน่งต้นทาง/ปลายทางถูกล็อก จนกดดำเนินการเสร็จ"** (L2970)
- `submitBPOrder()` (L2327) → ล็อก location ทั้งต้นทาง-ปลายทางผ่าน `LOCKED_LOCS.add()`
- Order list: pill สถานะ `"ล็อกอยู่"` (warning) / `"เสร็จแล้ว"` หรือ `"เสร็จ"` (ok) — `completeBPOrder`/
  `cancelBPOrder` ปลดล็อกด้วย `LOCKED_LOCS.delete()` (L2368-2379)
- Empty state: `"ยังไม่มีคำสั่งแตก/แพ็ค"` (L2546)

### P-04 Audit Log (`renderAdjLogView()` L2736)
- แสดง ADJ doc ทั้งหมด (`ADJLOG`, append-only — ไม่มี edit/delete path ใดในไฟล์) เรียงใหม่สุดก่อน
- แต่ละ record: docNo (`ADJ-YYYY-NNNN`), ผู้ทำ + role (เช่น `"สมชาย คลัง WH-01" / "Warehouse Staff"`), เหตุผล,
  หมายเหตุ, รายบรรทัด (สินค้า/ตำแหน่ง/±จำนวนหน่วย loc/before→after ฐาน)
- ค้น/กรองผ่าน `applyLogFilter()`
- Empty state: `"ยังไม่มีประวัติการปรับสต็อก"` (L2811)

---

## 5. Role & Permission Notes (สำหรับ FE wiring)

| Role | เห็น | เขียนได้ |
|---|---|---|
| warehouse_staff | คลังตัวเองเท่านั้น (scoped, ข้าม gate อัตโนมัติ — `ROLE_META.warehouse_staff.scope='WH-01'`) | ปรับสต็อก (M-01), สร้าง/complete/cancel Break-Pack order |
| finance | ทุกคลัง | ปรับสต็อก (M-01) เหมือน warehouse_staff + ดูมูลค่า (`canValuation`) + export พร้อม toggle "รวมมูลค่า" (`canValExport` — เฉพาะ finance) |
| auditor | ทุกคลัง | อ่านอย่างเดียว + ดูมูลค่า (`canValuation` ครอบคลุม auditor ด้วย) — **ปรับสต็อกไม่ได้** |
| inventory_viewer, procurement | ทุกคลัง | อ่านอย่างเดียวทั้งหมด — ไม่เห็นปุ่มปรับสต็อก/ดูมูลค่า |

**Guard function จริง:**
- `canAdjust()` (L1032): `return ['warehouse_staff', 'finance'].includes(CURRENT_ROLE);` — comment
  `// BACKEND: สิทธิ์จริงผูก Policy Center — mock: staff (ปฏิบัติ) + finance (controller)`
- ใช้ conditional-render ปุ่ม (ไม่ใช่แค่ disabled) ที่ทุกจุดเรียก `openAdjust()`
- `openAdjust()` (L2577) มี guard ซ้ำอีกชั้น: ถ้ากดเข้ามาโดยไม่ผ่านเงื่อนไข → toast error verbatim:
  **"ไม่มีสิทธิ์ปรับสต็อก (Warehouse Staff / Finance เท่านั้น)"** (L2578, tagged `// BACKEND: Policy Center RBAC`)
- `canValuation()` (L801): `['finance','auditor'].includes(CURRENT_ROLE)`
- `canValExport()` (L803): `CURRENT_ROLE === 'finance'` เท่านั้น (ไม่รวม auditor)

⚠️ **BACKEND note:** ทุก guard ข้างต้นเป็น **client-side mock เท่านั้น** — ต้อง re-check server-side จริงที่
endpoint ระดับตอน build (ตาม comment ในโค้ดเอง อ้าง Policy Center)

---

## 6. Empty / Error / Validation States Checklist

ดูตารางเต็มที่ `FRD_F-INV-001_Pack/01_UI.md` และ `06_TESTS.md` (AC-01..17) — ไฮไลต์ verbatim ที่ FE ต้อง
handle ให้ครบ (คัดลอกตรงตัวจาก HTML):

| จุด | ข้อความจริง | ที่มา |
|---|---|---|
| ลดเกินเพดานจอง (block) | `ลดได้สูงสุด ${X} ${unit} — ห้ามแตะยอดจอง (จองอยู่ ${allocated} ชิ้นฐาน)` | `adjLineError()` L2608 |
| Location ถูกล็อกจาก BP order | `ตำแหน่งถูกล็อกโดยคำสั่งแตก/แพ็ค — รอดำเนินการเสร็จก่อน` | L2601 |
| Low stock note (drawer) | `ต่ำกว่าขั้นต่ำ — พร้อมใช้ ${av} ${unit} < threshold ${min_stock} ${unit} (ตั้งจาก Item Master)` | L1955 |
| Stat "ต่ำกว่าขั้นต่ำ" meta | `ต่ำกว่า threshold จาก Item Master` (เมื่อ >0) / `ปกติ` (เมื่อ =0) | L1542 |
| Stat "สต็อกติดลบ" meta | `ต้อง reconcile` (เมื่อ >0) / `ปกติ` (เมื่อ =0) | L1547 |
| Filtered-to-zero: list สินค้า | `ไม่พบสินค้าตามเงื่อนไข` | L1592 |
| Filtered-to-zero: ตำแหน่ง | `ไม่พบตำแหน่งตามเงื่อนไข` | L1758 |
| Filtered-to-zero: คลัง (gate) | `ไม่พบคลังตามคำค้น` | L1460 |
| Empty: การเคลื่อนไหว | `ยังไม่มีการเคลื่อนไหว` | L1995 / L2194 |
| Empty: Break/Pack order | `ยังไม่มีคำสั่งแตก/แพ็ค` | L2546 |
| Empty: Audit log | `ยังไม่มีประวัติการปรับสต็อก` | L2811 |
| Break/Pack — ไม่มีต้นทาง | `เลือกต้นทางที่มีของก่อน` (toast error) | L2329 |
| Break/Pack — ไม่มีตัวเลือกต้นทาง | `ไม่มีของพร้อมใช้สำหรับสินค้านี้` | L2939 |
| Break/Pack — ผลกระทบ (action-consequence, ไม่ใช่ hint) | `เมื่อสร้าง: ของต้นทางถูกจอง (lock) + ตำแหน่งต้นทาง/ปลายทางถูกล็อก จนกดดำเนินการเสร็จ` | L2970 |
| RBAC — ไม่มีสิทธิ์ปรับสต็อก | `ไม่มีสิทธิ์ปรับสต็อก (Warehouse Staff / Finance เท่านั้น)` (toast) | L2578 |
| Adjust line — สถานะตำแหน่งว่าง | `· ว่าง — เพิ่มเข้าได้` / `· มีของ` / `· ล็อกอยู่` (ต่อท้าย label dropdown) | L2624 |
| Adjust line — new balance | `รายการใหม่ในตำแหน่งนี้` + `ปัจจุบัน 0 → n` | L2647 |
| Adjust — summary bar | `พร้อมบันทึก n/m บรรทัด` · `เพิ่มรวม +x ชิ้นฐาน` · `ลดรวม −y ชิ้นฐาน` · `รายการใหม่ z ตำแหน่ง` | L2682 |
| Master inactive badge | `Master หยุดใช้งาน` (pill/tooltip) | L1924, L1604 |

---

## 7. Known Gaps

1. **🔴 G-01 / OQ-INV-06 — Scope creep: Valuation/Costing ยังไม่ปิด (ต้องเคาะก่อน dev sign-off)** —
   PREBRIEF §1 ระบุชัดว่า **"ไม่ทำ: ... costing engine (VD-PDM-07)"** แต่ HTML มีฟีเจอร์ valuation/costing
   จริง: `canValuation()` (L801), `canValExport()` (L803), comment อ้างเอกสารที่ไม่มีอยู่จริง
   `// FRD §0.3 + BR-D02` (L790), ปุ่ม "ดูมูลค่า/ซ่อนมูลค่า" ใน balance drawer (L2047-2050), กล่อง
   `.val-box` แสดงต้นทุน/หน่วย + มูลค่าคงเหลือ (`on_hand × cost`, L2135-2144), toggle "รวมมูลค่า" ตอน
   export (L1368). Coverage round 1 พบเป็น 🔴 gap ระดับ real-feature (verdict WARN ไม่ใช่ PASS) — round 2
   ยืนยันว่า FRD **ไม่ได้ปิดเงียบ** เรื่องนี้ (สร้าง OQ-INV-06 + LD-02 ผูกไว้ ระบุ "blocking — must close
   before dev sign-off") แต่ **ตัวปัญหาเองยังไม่ถูกตัดสินใจ** (เก็บหรือทิ้ง feature). **FE ต้องรอ Strike
   เคาะก่อน** — ถ้าตัดสินใจทิ้ง ต้องลบ 5 จุดโค้ดข้างต้นก่อนขึ้น production; ถ้าตัดสินใจเก็บ ต้องมี
   OB/S/FN ใหม่ + security review (ข้อมูลต้นทุนเป็นข้อมูลอ่อนไหว)
2. **OQ-INV-01..05 (จาก PREBRIEF §6, carried เข้า FRD `00_OVERVIEW.md §0.8` แบบ verbatim-in-meaning, ยังไม่เคาะ):**
   - OQ-INV-01: Manual Adjustment มูลค่าสูงต้องมี DOA (สายอนุมัติ) ไหม — ตอนนี้บันทึกตรง ไม่มี approval flow
   - OQ-INV-02: `min_stock` เป็น per-item รวมทุกคลัง หรือ per-item-per-warehouse — โค้ดปัจจุบันเทียบ avail
     ของคลังที่เปิดอยู่กับ threshold ก้อนเดียว
   - OQ-INV-03: หน่วยของตำแหน่ง (1-loc-1-uom) เปลี่ยนได้เมื่อไหร่/ใครมีสิทธิ์ — ยังไม่มี governance UI
   - OQ-INV-04: สต็อกติดลบ (จองเกิน) — ใครเป็นเจ้าภาพ reconcile + ควร block การจองเกินตั้งแต่ต้นทางไหม
     (FRD ยกระดับเป็น **blocking-for-go-live**, เข้มงวดกว่า PREBRIEF เดิม)
   - OQ-INV-05: Low stock ควรต่อ action อะไร (แจ้งเตือน/สร้าง PR อัตโนมัติ/รายงานเฉย ๆ) — ยังไม่ตัดสินใจ
3. **UX known-deviations (ยอมรับแล้ว จาก `_UX_CHECK_REPORT.md`, ไม่ใช่บั๊กที่ FE ต้องแก้เอง):**
   - **Manual Adjustment เป็น modal 1440px ไม่ใช่ drawer** — เป็นความตึงเครียดกับ Rule #14 (multi-line
     create ควรเป็น drawer/B2 pattern) แต่ formalize เป็น **LD-01** ใน `07_LOCKED_DECISIONS.md` แล้ว —
     สอดคล้องกับ PREBRIEF OB-8 ("มติ 2026-08-09") ไม่ใช่การมองข้าม
   - Extended badge palette (20 hex values สำหรับ 10 location types + 4 stock-substatuses) เกินกว่า 5 คู่
     ที่ ci-tokens ปัจจุบัน whitelist ไว้ — เป็นความจำเป็นทางธุรกิจจริง (ต้องแยกภาพ 7-10 ประเภทตำแหน่งให้
     แยกแยะได้) ไม่ได้ remap ในรอบ QC นี้เพราะเสี่ยง visual regression — แนะนำ formalize extended palette
     ใน ci-tokens.md ต่อ ไม่ใช่บีบเหลือ 5 สี
   - Typography/spacing drift (11 font-size นอก scale, 122 spacing values นอก 8pt grid) — pre-existing,
     ปล่อยเป็น WARN เพื่อไม่ให้กระทบ layout ของหน้าจอที่ business sign-off แล้ว ต้องมี follow-up pass
     แยกตอน build จริงถ้าต้องการ normalize เต็ม
   - Legacy 540px drawer, missing scrollbar block, font stack ผิดลำดับ/ import Inter ที่ไม่ได้ใช้ — **แก้แล้ว**
     โดย qc-ux-html-checker ก่อน hand-off นี้ (drawer = 920px, scrollbar block ใส่แล้ว, font stack
     `'Satoshi', 'Noto Sans Thai', system-ui, sans-serif` ทุกจุด)
4. **TC dedicated ยังไม่มี** — `testcases-f-inv.md` (จาก `ai-testcase-md-generator`) ยังไม่ถูกผลิต ณ จุดนี้
   ของ pipeline — `06_TESTS.md` (AC-01..17 + XT-01/02) เป็น proxy evidence ชั้นที่ 1 เท่านั้น ยังต้องตรวจซ้ำ
   เมื่อไฟล์ dedicated TC ถูกผลิต
5. **EC-INV-01..04 (concurrency/idempotency)** — ตาม `06_TESTS.md §6.7` ระบุเองว่าไม่สามารถแสดงเป็น UI
   acceptance criteria ได้ในรอบนี้ — ต้องเป็น server-side integration test ตอน build จริง ไม่ใช่ prototype
   scope
6. **FN-40 (build/test gate)** — นอกขอบเขต business coverage (qc-coverage-checker ไม่ตรวจซ้ำ) แต่
   FUNCTION_CHECKLIST ระบุว่าผ่านแล้ว (`node --check`, audit navy=0/console=0/hint=0, Playwright 60+ PASS)

---

## 8. References

- **Layout Decision Log เต็ม + evidence รายบรรทัด:** `FRD_F-INV-001_Pack/01_UI.md`
- **Business rules ที่ผูกกับ UI (BR-01..11):** `FRD_F-INV-001_Pack/05_RULES.md`
- **Locked decisions (LD-01 modal 1440px, LD-02 G-01 ไม่เคาะ):** `FRD_F-INV-001_Pack/07_LOCKED_DECISIONS.md`
- **Open Questions รวม status:** `FRD_F-INV-001_Pack/00_OVERVIEW.md §0.8`
- **Acceptance Criteria (proxy TC ชั้น 1, AC-01..17 + XT-01/02):** `FRD_F-INV-001_Pack/06_TESTS.md`
- **PREBRIEF (business source of truth, OB-1..12 · S-01..12 · OQ-INV-01..05):**
  `02_BRD/PREBRIEF_F-INV_Stock-by-Location.md`
- **FUNCTION_CHECKLIST (FN-01..40):** `02_BRD/FUNCTION_CHECKLIST_F-INV_Stock-by-Location.md`
- **Gate reports:** `01_HTML/_UX_CHECK_REPORT.md` (PASS with WARNINGS), `01_HTML/_COVERAGE_REPORT.md`
  (รอบ 1+2 WARN — G-01 ต้องปิดก่อน dev sign-off)
- **Source HTML:** `01_HTML/StockByLocation.html` (3,124 บรรทัด)

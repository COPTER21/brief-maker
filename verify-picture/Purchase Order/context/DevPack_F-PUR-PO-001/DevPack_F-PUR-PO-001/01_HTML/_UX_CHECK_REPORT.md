# _UX_CHECK_REPORT — F-PUR-PO · ใบสั่งซื้อ (F078)

**ขั้น:** WF-01 ขั้น 7R (re-gate หลัง vibe · Mode B)
**ไฟล์ที่ตรวจ:** `01_HTML/F-PUR-PO.html` (267,063 bytes · 3,618 บรรทัด)
**วันที่ตรวจ:** 2026-09-14
**Sync Read จาก:** `html-generator-v9` (`.claude/skills/html-generator-v9/`)
— `knowledge/iron-rules.md` (101.1K) · `layout-integrity.md` · `component-contracts.md` · `page-anatomy.md` · `ci-tokens.md` · `microcopy.md`
— `patterns/Q_transaction-document-archetype.md` · `patterns/B2_document-line-editor.md`
— `references/document-archetype/_SOURCE_so-reference.html` (golden reference)
**archetype:** `Q-document` (ตรงกับ registry `F078.arch`)

---

## VERDICT (รอบที่ 2 · หลังแก้): **PASS with 8 warnings** — BLOCK = 0

> รอบที่ 1 พบ **BLOCK 2 ข้อที่ต้นน้ำ (S3a) รายงานว่า PASS** — ทั้งสองเป็นหมวดที่ `audit.sh`/`self_audit.py` มองไม่เห็นโดยโครงสร้าง
> (UX-01 ต้อง Playwright วัดพิกัดจริง · UX-02 ต้องอ่านข้อความที่ render จริง)
> **ไม่ได้ใช้รายงานเดิมจาก `0_DIRECTION/` แทนการรันใหม่** ตามข้อบังคับ §7R ข้อ 3
> ผู้ใช้อนุมัติให้แก้ทั้ง 2 ข้อ (2026-09-14) → แก้แบบ surgical แล้ว **ตรวจซ้ำด้วยการทดสอบชุดเดิมที่เป็นคนจับได้**

### Loop Diff — รอบ 1 → รอบ 2

| id | รอบ 1 | รอบ 2 | หลักฐานการตรวจซ้ำ |
|---|---|---|---|
| **UX-01** #66 bottom-edge | ❌ BLOCK — ล้นขอบล่าง **+104.5px** ทั้ง 900/768 · รายการที่ 2–3 กดไม่ได้ | ✅ **แก้แล้ว** | วัดใหม่: `overflowPx` = **−49.5** (อยู่ในจอ) ทั้ง 2 viewport · `lastItemBelowFold: false` · ภาพ `21_bottom_edge_900.png` เห็นเมนูพลิกขึ้นบน ครบทั้ง 3 รายการ |
| **UX-02** #81 jargon | ❌ BLOCK — `FWD-WIRE`/`W7`/`W3P` บนจอ 3 จุด | ✅ **แก้แล้ว** | สแกน `innerText` ทุก surface ซ้ำ (15 ใบ × 5 แท็บ + wizard 5 ขั้น + modal 5) → **`FWD-WIRE` = 0 hit** · เหลือแต่ `DOA` ซึ่งเป็นคำของผลิตภัณฑ์ (ดู §6) · ภาพ `04_view_recv.png` · `02_wizard_step5.png` |
| UX-03..UX-10 | WARN | WARN (คงเดิม) | ไม่ได้แก้ตามขอบเขตที่ตกลง — แก้เฉพาะ 2 BLOCK |

**สิ่งที่แก้ (surgical · 4 บรรทัด · ไม่แตะ L-01..L-09):**

| จุด | เดิม → ใหม่ |
|---|---|
| `openRowMenu()` | ย้าย `menu.style.top` ออกจากก่อน `appendChild` → หลัง append แล้วคำนวณ `const up = window.innerHeight - rect.bottom < menu.offsetHeight + 12;` แล้วเลือก `bottom`/`top` (รูปแบบเดียวกับ `comboOpen`/`showItemSuggestions` ในไฟล์เดียวกัน) |
| banner งบ | `(ข้อมูลจำลอง · FWD-WIRE Budget Control W7)` → `(ข้อมูลจำลอง · ยังไม่เชื่อมระบบควบคุมงบประมาณ)` |
| `field-help` การ์ดงบ | `FWD-WIRE · Budget Control W7` → `ข้อมูลจำลอง · ยังไม่เชื่อมระบบควบคุมงบประมาณ` |
| `.note` แท็บรับของ | `· FWD-WIRE รอเชื่อม GRN (W3P)` → `· ยังไม่เชื่อมระบบรับของ` |

**ตรวจสุขภาพไฟล์หลังแก้:** `node --check` **4/4 OK** · `audit.sh` **FAIL=0 · WARN=3** (เท่าเดิม) · `FWD-WIRE` เหลือเฉพาะ code comment 2 จุด ([`:1943`](F-PUR-PO.html#L1943) · [`:2029`](F-PUR-PO.html#L2029)) ซึ่งถูกต้องแล้ว · pageerror = 0

> ⚠️ ไฟล์ในแพ็ก **ไม่ byte-identical กับ `input/09142026-po/1_HTML/` อีกต่อไป** — ต่างกัน 4 จุดข้างบน
> `_TECH_CHECK.md` ของต้นน้ำยังอ้างได้ในส่วนที่ไม่เกี่ยวกับ 4 จุดนี้ · รายละเอียดใน README

| หมวด | ผล |
|---|---|
| `audit.sh` | **FAIL = 0** · WARN = 3 |
| `self_audit.py` | 6 หมวดไม่เป็นศูนย์ — ตรวจรายข้อแล้ว **จริง 1 · false-positive 5** (ดู §4) |
| PREFLIGHT stamp | **ตรงกับการนับจริงทุกตัว** (156/2/1/8/0/0) — stamp เชื่อถือได้ |
| Pass D (archetype) | **27/27 ผ่าน** |
| Pass R (render) | pageerror = 0 · 21 ภาพ |

---

## 1. BLOCK ที่พบในรอบ 1 — ✅ แก้แล้วทั้ง 2 ข้อ (บันทึกไว้เป็นประวัติการตรวจ)

### UX-01 · Rule #66 (Bottom-Edge) — เมนูรายแถวจมใต้จอ ไม่มี flip-up
**สถานะ: ✅ แก้แล้ว · ตรวจซ้ำผ่าน** (ดู Loop Diff ด้านบน)
**severity เดิม:** BLOCK · **ตำแหน่ง:** [`F-PUR-PO.html:3327`](F-PUR-PO.html#L3327) `openRowMenu()`

```js
menu.style.top  = (rect.bottom + 4) + 'px';
menu.style.left = Math.min(rect.left - 150, window.innerWidth - 210) + 'px';
```

clamp **แกนนอน** (`window.innerWidth - 210`) แต่ **ไม่มี clamp/flip แกนตั้ง** —
เมนูวางที่ `rect.bottom + 4` เสมอ ไม่ว่าปุ่มจะอยู่ใกล้ขอบล่างแค่ไหน

**หลักฐานที่วัดได้ (Playwright · แถวสุดท้ายของลิสต์):**

| viewport | menu top | menu bottom | ล้นขอบล่าง | รายการสุดท้ายอยู่ใต้ fold |
|---|---|---|---|---|
| 1440×900 | 886.5 | 1004.5 | **+104.5px** | ✅ ใช่ (top 963.5 > vh 900) |
| 1440×768 | 754.5 | 872.5 | **+104.5px** | ✅ ใช่ (top 831.5 > vh 768) |

ภาพ: `_shots/21_bottom_edge_900.png` · `_shots/21_bottom_edge_768.png` — เห็นเมนูโผล่แค่เสี้ยวบนสุดที่ขอบล่างจอ
เมนูมี 3 รายการ (`เปิดดู` · `ทำสำเนา` · `พิมพ์ / ดู PDF`) — **รายการที่ 2 และ 3 กดไม่ได้ทั้งคู่**

**ทำไม scanner ไม่จับ:** `self_audit.menu_no_flip = 0` เพราะตัวตรวจดูเฉพาะเมนูของ kit (`.menu-fixed`)
`.row-menu` เป็น element ที่หน้าสร้างเอง จึงอยู่นอกขอบเขตตัวตรวจ

**ความไม่สอดคล้องภายในไฟล์เอง** — popover อีก 2 ตัวในไฟล์เดียวกัน *มี* flip-up ครบ:
- [`:2437`](F-PUR-PO.html#L2437) `comboOpen()` → `const up = window.innerHeight - rect.bottom < 280;`
- [`:2306`](F-PUR-PO.html#L2306) `showItemSuggestions()` → `const up = window.innerHeight - rect.bottom < 260;`

**วิธีแก้ (surgical · ยกรูปแบบจากฟังก์ชันข้างบนในไฟล์เดียวกัน):**
```js
const menuH = 44 * (จำนวนปุ่ม) + 8;              // หรือวัดหลัง appendChild
const up = window.innerHeight - rect.bottom < menuH + 12;
if (up) menu.style.bottom = (window.innerHeight - rect.top + 4) + 'px';
else    menu.style.top    = (rect.bottom + 4) + 'px';
```
> ไม่แตะ L-01..L-09 — ไม่ใช่ flow / สถานะ / สายอนุมัติ / line editor / hard control / scope

---

### UX-02 · Rule #81 — marker ภายใน `FWD-WIRE` + รหัส wave รั่วขึ้นจอผู้ใช้
**สถานะ: ✅ แก้แล้ว · ตรวจซ้ำผ่าน** (ดู Loop Diff ด้านบน)
**severity เดิม:** BLOCK · **ตำแหน่ง:** 3 จุดที่เป็น *ข้อความ render* (ไม่ใช่ comment)

| บรรทัด | จุดที่โผล่ | ข้อความที่ผู้ใช้เห็น |
|---|---|---|
| [`:2341`](F-PUR-PO.html#L2341) | banner เตือนงบ (wizard/detail) | `… (ข้อมูลจำลอง · **FWD-WIRE Budget Control W7**)` |
| [`:2677`](F-PUR-PO.html#L2677) | `field-help` ใต้หัวการ์ดผลตรวจงบ | `**FWD-WIRE · Budget Control W7**` |
| [`:3030`](F-PUR-PO.html#L3030) | `.note` ในแท็บ **การรับของ** | `… แก้ด้วยมือไม่ได้ · **FWD-WIRE รอเชื่อม GRN (W3P)**` |

(อีก 2 จุด — [`:1943`](F-PUR-PO.html#L1943) และ [`:2029`](F-PUR-PO.html#L2029) — เป็น code comment **ถูกต้องแล้ว** ไม่ต้องแก้)

**หลักฐาน:** สแกน `document.body.innerText` ทุก surface (list · wizard 5 ขั้น · view 5 แท็บ × 15 ใบทุกสถานะ · modal 5 ชนิด)
→ พบ `FWD-WIRE` **6 unique context** ที่เป็นข้อความบนจอ · ภาพ: `_shots/04_view_recv.png`

**ประเด็นเชิงกระบวนการ:** HANDOFF §4.2 บันทึกว่าเปลี่ยน `TODO` → `FWD-WIRE` เพราะ
*"`audit.sh` Rule #24 ตั้ง literal `TODO` เป็น FAIL และ S3c บังคับ FAIL = 0"*
— การเปลี่ยนคำเพื่อให้ผ่านตัวตรวจ **แต่ยังวางไว้ในข้อความที่ผู้ใช้เห็น** ทำให้ gate ผ่านโดยที่ปัญหาเดิม (marker ภายในอยู่บนจอ) ยังอยู่ครบ
`W7` / `W3P` เป็นรหัส wave ภายใน ผู้ใช้ปลายทางไม่รู้จัก

**วิธีแก้ (ข้อความอย่างเดียว ไม่แตะตรรกะ — อยู่ใน §5 "แก้ได้เลย" ของ HANDOFF):**

| เดิม | เสนอใหม่ |
|---|---|
| `(ข้อมูลจำลอง · FWD-WIRE Budget Control W7)` | `(ข้อมูลจำลอง · ยังไม่เชื่อมระบบควบคุมงบประมาณ)` |
| `FWD-WIRE · Budget Control W7` | `ข้อมูลจำลอง · ยังไม่เชื่อมระบบควบคุมงบประมาณ` |
| `· FWD-WIRE รอเชื่อม GRN (W3P)` | `· ยังไม่เชื่อมระบบรับของ` |

> สัญญา forward-wire ไม่หาย — บันทึกไว้ครบใน `03_FRD/07_LOCKED_DECISIONS.md` + `CSQ_BRIEF` + comment ที่ `:1943`/`:2029`

---

## 2. WARN

| id | rule | ตำแหน่ง | พบอะไร | วิธีแก้ |
|---|---|---|---|---|
| UX-03 | #67 ความยาว note | [`:3031`](F-PUR-PO.html#L3031) | `.note.warn` วัดด้วย `innerText` ได้ **121 ตัวอักษร** (เพดาน 120) — เกิน 1 ตัว | ตัด `(ค่าตั้งต้นต่อผู้เช่า 0%)` ออก → 97 ตัว |
| UX-04 | #21 | [`:1704`](F-PUR-PO.html#L1704) `ss-caret` · [`:1813`](F-PUR-PO.html#L1813) `empty-icon` | `<i data-lucide>` ไม่มี class `w-{N} h-{N}` (2 จุดจริง · จุดที่ 3 ที่ audit.sh รายงานคือ comment) | เติม `class="w-4 h-4"` / `class="w-12 h-12"` |
| UX-05 | #40 | [`:700`](F-PUR-PO.html#L700) `.uc-email` | เซลล์ตารางมี sub-line ซ้อน | บรรทัดรองเป็น meta ของข้อมูลเดียวกัน (V-code ใต้ชื่อผู้ขาย) — **ยอมรับได้ตาม #103** แต่คง WARN ไว้ตาม audit.sh |
| UX-06 | CI token | `:88` `:135` `:136` `:151` `:174` | `font-size` เป็นค่า px ตรง ไม่ใช่ `var(--fs-*)` (5 จุด · ทั้งหมดอยู่ใน sidebar/shell) | เปลี่ยนเป็น token — *หมายเหตุ: อยู่นอก BASE-KIT marker จึงแก้ได้* |
| UX-07 | #96 List Full-Height | หน้า list | `.table-wrap` ขอบล่างอยู่ที่ 1030.5px ขณะ viewport 900 → **ล้น fold 130.5px** หน้าเลื่อนทั้งหน้าแทนที่ตารางจะ scroll ในตัว | KPI row + filter สูงรวมเกิน — ถ้าจะบังคับ #96 ต้องให้ `.table-wrap` คิด `calc(100dvh - …)` · **ไม่บล็อก** เพราะ `overflow-y:auto` มีแล้วและไม่มี h-scroll |
| UX-08 | #63 density | `tbody tr` | สูง **63px** (มาตรฐาน ~44px) | แถวเป็น 2 บรรทัดตาม archetype (เลขที่+วันที่ · ชื่อผู้ขาย+รหัส) — สอดคล้อง golden reference · **ยอมรับ** |
| UX-09 | dead CSS | ทั้งไฟล์ | 101 คลาสที่หาการอ้างอิงไม่เจอ | **ตรวจไม่น่าเชื่อถือในไฟล์นี้** — มี `classList.*` 24 จุด + สร้างชื่อคลาสแบบต่อสตริง 10 จุด · และเกือบทั้งหมดเป็น surface ของ BASE-KIT (`drawer-*`, `btn-sm`, `is-current`) ที่ **Rule #69 ห้ามแก้** → ไม่ต้องลบ |
| UX-10 | #69 inline layout | ทั้งไฟล์ | `inline_layout = 156` | golden reference `_SOURCE_so-reference.html` มี **444** (2.3×) — ความหนาแน่นนี้ **สืบทอดจาก archetype** ไม่ใช่ความมักง่าย · ดู §3 |

---

## 3. หมายเหตุเรื่อง `inline_layout = 156` — stamp เขียนกำกวม

PREFLIGHT stamp เขียนว่า `inline-layout=156(PatternQ+B2-verbatim #98/#99)`
ตรวจจริงแล้ว **มีเพียง 10 จุดที่เป็น grid ของ B2 ตามตัวอักษร** — คำอธิบายใน stamp จึงกว้างเกินจริง

แต่ **ข้อสรุปยังยืนได้** เมื่อเทียบกับ golden reference ของ archetype เอง:

| ไฟล์ | ขนาด | `style=` ทั้งหมด | ที่เป็น layout |
|---|---|---|---|
| `_SOURCE_so-reference.html` (golden) | 260,677 B | 700 | **444** |
| `F-PUR-PO.html` (ไฟล์นี้) | 267,063 B | 292 | **193** |

สำนวนที่ใช้ตรงกัน (`vertical-align: top` · `width:1px;height:20px;background:…` divider · `font-size:13px;margin-top:4px;color:…`)
→ ไฟล์นี้ **สะอาดกว่า reference 2.3 เท่า** · จัดเป็น WARN ไม่ใช่ BLOCK

---

## 4. รายการที่ scanner รายงาน แต่ตรวจแล้วเป็น false-positive

| scanner | ค่า | ผลตรวจจริง |
|---|---|---|
| `long_banners` | 14 | วัด `innerText` ทุก surface ได้ banner จริง 18 จุด — **เกิน 120 ตัวอักษรแค่ 1 จุด** (UX-03) · regex จับ source ของ template literal ยาวข้าม element |
| `missing_ids` | 7 | ทั้งหมดเป็น id ที่ JS ต่อสตริงตอน runtime: `id="cbi-' + key + '"` · `item-input-' + l.id` · `ss-input-' + key` → ไม่ใช่ id ที่หายจริง |
| `fullwidth_select` | 1 | literal `<select>` 2 จุด อยู่ใน **CSS comment** ([`:560`](F-PUR-PO.html#L560)) และ **JS comment** ([`:1677`](F-PUR-PO.html#L1677)) — ไม่ใช่ element · `<select>` จริง 12 ตัว ไม่มีตัวไหน options > 7 (`audit.sh` ไม่ยก WARN #102) |
| `spacing_off` | 2 | `1180` = breakpoint ของ media query #97 ([`:352`](F-PUR-PO.html#L352)) · `52` = fallback `var(--shellbar-h, 52px)` ([`:371`](F-PUR-PO.html#L371)) — ไม่ใช่ค่า padding/margin/gap |
| `hex_off` | 1 | `#E7E2DB` ([`:381`](F-PUR-PO.html#L381)) อยู่ใน BASE-KIT (บรรทัด 28–1355) และ **ตรงกับ `file-skeleton.template.html:375` ทุกตัวอักษร** — เป็น fallback ของ kit เอง |
| `.drawer-panel` z-index = `auto` | — | **ไม่ใช่บั๊ก** — stacking เป็นของ `.overlay-wrap` (`position:fixed; z-index:51` = `--z-drawer`) ตาม #95 Overlay Portal · ยืนยันด้วย ancestor chain + `elementFromPoint` |

---

## 5. Pass D — Document Archetype (Rules #98–#101) · **27/27 ผ่าน**

`audit.sh` ส่วน `doc_archetype` ทริกเกอร์แล้ว (ไฟล์มี `line-tbl`) และไม่พิมพ์ FAIL แม้ข้อเดียว
ตรวจซ้ำด้วยมือในข้อที่เป็น LOCK:

| ข้อ | เกณฑ์ (จาก `iron-rules.md` / `Q_*.md` โดยตรง) | ในไฟล์ | ผล |
|---|---|---|---|
| **#100** wizard 5 ขั้น | `① เลือกแหล่งที่มา · ② ข้อมูลหลัก[เอกสาร] · ③ รายการสินค้า · ④ เอกสารแนบ · ⑤ ตรวจสอบและยืนยัน` | [`:2540-2541`](F-PUR-PO.html#L2540-L2541) `เลือกแหล่งที่มา` · `ข้อมูลหลัก PO` · `รายการสินค้า` · `เอกสารแนบ` · `ตรวจสอบและยืนยัน` | ✅ **ตรงทุกตัวอักษร** |
| **#101** view tabs | `detail › [domain ≤2] › pdf › sign › history` | `detail` › `recv` › `pdf` › `sign` › `history` | ✅ ตรง |
| **#101** เอกสารแนบไม่เป็น tab แยก | ต้องเป็น section ใน detail | `SEC('paperclip', \`เอกสารแนบ…` ✓ · ไม่มี `tabBtn('attach')` | ✅ |
| **#99** grid B2 v2 | `26/—/64/92/92/78/72/104/54` | th ที่ประกาศ: `26/64/92/92/78/72/104/54` + คอลัมน์ชื่อยืดหยุ่น | ✅ ตรงสัญญา |
| **#99** VAT engine | `calcLineVat` · `migrateLine` · `totals()` · `taxBadgeV` · `renderLineSummary` | มีครบทั้ง 5 | ✅ |
| **#98** list | `docPill` + `renderSignProgress` | มีทั้งคู่ · เห็นในภาพ `01_list.png` (0/2 · 1/4 · 2/2 · 3/3) | ✅ |
| **#98** DOA slot picker | `.slot-row` ใน submit modal เลือก **คนจริง** | `.slot-row` = 1 ใน modal ส่งอนุมัติ · combobox แสดง รูปย่อ→ชื่อ→ตำแหน่ง·แผนก | ✅ **ตรง L-03** |
| **#98** drawer สร้าง `.wide` | 1290px | วัดจริง **1290px** (`drawer-panel wide`) · view drawer = **920px** | ✅ |
| **#98** ไม่มี hardcoded approval chain | ต้อง resolve จาก DOA | `audit.sh` ไม่ยก FAIL · มี `resolveDoa()`/`chainOf()` | ✅ |

---

## 6. Pass R — Render Gate · 21 ภาพ · pageerror = 0

รัน Playwright/Chromium เก็บภาพจริงครบทุก surface (ไม่ใช้ภาพเดิมจากต้นน้ำเป็นหลักฐานของรอบนี้)

**ภาพที่เก็บ:** `01_list` · `02_wizard_step1..5` · `03_view_detail` · `04_view_recv` · `05_view_pdf` · `06_view_sign` · `07_view_history` · `08_modal_submit` · `09_modal_approve` · `10_combo_vendor/buyer/cc` · `11_line_expand` · `12_line_editor` · `13_item_combo` · `14_list_1024` · `15_view_1024` · `20_sticky_vs_drawer` · `21_bottom_edge_900/768`

| test | วิธีวัด | ผล |
|---|---|---|
| pageerror / console.error | ตลอด 15 ใบ × 5 แท็บ + wizard 5 ขั้น + modal 5 ชนิด | **0** ✅ |
| **Responsive (#97)** | `documentElement.scrollWidth` vs `innerWidth` ที่ 1600/1440/1280/1180/1024/900/**768** | **เท่ากันทุกความกว้าง — ไม่มี h-scroll แม้ที่ 768** ✅ |
| **Sticky vs Overlay (#62.1)** | `elementFromPoint` 3 จุดบนหัว drawer | คืน element ใน drawer ทุกจุด — หัวตารางไม่ทะลุ ✅ |
| **Modal เหนือ drawer** | computed z-index | `.modal-overlay` = **60** > `.overlay-wrap` = **51** · `elementFromPoint` กลาง modal = INSIDE ✅ |
| **Dropdown anatomy (#65/#102)** | เปิดทั้ง 4 dropdown วัด 4 มุมด้วย `elementFromPoint` | ทุกตัว `position:fixed` · `z-index:70` · `max-height:280px` · 4 มุม = IN · fits viewport ✅ |
| — ผู้ขาย | | icon → ชื่อ → `V-1001 · วัสดุก่อสร้าง · เครดิต 30 วัน` ✅ |
| — ผู้จัดซื้อ (คน) | | ตัวย่อ `ธว` → `ธนกฤต วัฒนชัย` → `เจ้าหน้าที่จัดซื้อ · จัดซื้อ · EMP-0142` ✅ ตรง #102 |
| — ศูนย์ต้นทุน | | icon → ชื่อ → `CC-100 · งบสำนักงาน 2026` ✅ |
| — สินค้า | | package icon → `PVC-4001 · วัสดุก่อสร้าง` → ชื่อ → `฿285.00/เส้น · VAT 7%` ✅ |
| **คลิกนอกเมนู → ปิด** | click (200,200) | ปิดครบทุกตัว ✅ |
| **Bottom-Edge (#66)** | เปิดเมนูแถวล่างสุด 2 viewport | รอบ 1 ❌ BLOCK · **รอบ 2 ✅ ผ่าน** (`overflowPx` −49.5 · เมนูพลิกขึ้นบน) |
| **#81 jargon** | `innerText` ทุก surface เทียบ 25 pattern | รอบ 1 ❌ BLOCK · **รอบ 2 ✅ ผ่าน** (`FWD-WIRE` = 0 hit) |
| `DOA` บนจอ (22 จุด) | ตรวจกับ `DOA_BRIEF §5 UI Contract` | **ไม่ใช่ leak** — `ทะเบียน DOA` / `หน้า DOA กลาง` เป็นคำที่ผลิตภัณฑ์ใช้กับผู้ใช้จริง (brief §3/§5 กำหนดเอง) · ที่ห้ามคือ *รหัส role* ซึ่งไม่โผล่ ✅ |

---

## 7. DIVERGENCE check (§7R ข้อ 4) — **ไม่พบ**

registry `F078`: `arch: Q-document` · `dec: [doa, ntf, csq, doccfg, pdfdoc]`

| surface ที่โผล่ในจอ | registry ประกาศไว้ไหม |
|---|---|
| DOA slot picker + สายอนุมัติตามวงเงิน | ✅ ชิป `doa` |
| แจ้งเตือน (event) | ✅ ชิป `ntf` |
| เลขเอกสาร `PO-YYYY-NNNN` จากทะเบียนกลาง | ✅ ชิป `doccfg` |
| PDF Preview `.a4` + ช่องลงนาม | ✅ ชิป `pdfdoc` |
| ท่อ consequence | ✅ ชิป `csq` |
| wizard 5 ขั้น · view 5 แท็บ · line editor B2 | ✅ `arch: Q-document` |

→ **ไม่มี surface ที่ registry ไม่ได้ประกาศ** · ไม่ต้องส่งกลับ BA

---

## 8. NOT-CHECKED (ไม่นับเป็นผ่าน)

| หมวด | เหตุผล |
|---|---|
| Golden Compare เชิงสายตา (#3.6 Taste) | เทียบเชิงกล (โครง tab/step/grid/inline-style density) แล้วตรงทุกข้อ · ยังไม่ได้วางภาพคู่กันทีละใบกับ `_SOURCE_so-reference.html` |
| `TASTE_LOG.md` | ไม่มีไฟล์นี้ในโฟลเดอร์งาน |
| การพิมพ์จริงของ `.a4` (print CSS) | ตรวจบนจอเท่านั้น ยังไม่ได้สั่ง print preview — สเปกอยู่ที่ `print-spec-po.md` |

---

## 9. สรุปสถานะรายการ

| ลำดับ | รายการ | ระดับ | สถานะ |
|---|---|---|---|
| 1 | **UX-01** เติม flip-up ให้ `openRowMenu()` | BLOCK | ✅ **แก้แล้ว · ตรวจซ้ำผ่าน** |
| 2 | **UX-02** เปลี่ยนถ้อยคำ 3 จุดที่มี `FWD-WIRE`/`W7`/`W3P` | BLOCK | ✅ **แก้แล้ว · ตรวจซ้ำผ่าน** |
| 3 | UX-03 ตัด note ให้ ≤120 ตัว (เกินเพดาน 1 ตัวอักษร) | WARN | ⏸ ไม่ได้แก้ — ขอบเขตที่ตกลงคือแก้เฉพาะ BLOCK |
| 4 | UX-04 เติม `w-/h-` ให้ icon 2 จุด | WARN | ⏸ ไม่ได้แก้ — เหตุผลเดียวกัน |
| 5 | UX-05 · UX-07 · UX-08 | WARN | ⏸ ยอมรับตามเหตุผลใน §2 (archetype / ไม่บล็อก) |
| 6 | UX-06 font-size token 5 จุด | WARN | ⏸ ไม่ได้แก้ — อยู่ใน shell CSS แก้ได้แต่ไม่อยู่ในขอบเขตรอบนี้ |
| 7 | UX-09 · UX-10 | WARN | ⏸ **ห้ามแก้** — BASE-KIT verbatim ตาม Rule #69 / archetype-inherited |

**เกณฑ์ผ่าน gate: BLOCK = 0** → ✅ **ผ่านแล้ว**
WARN 8 ข้อคงเหลือ — ยกไปบันทึกใน `README.md` ของแพ็กเพื่อให้ทีมถัดไปเห็น

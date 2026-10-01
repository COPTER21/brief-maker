# HTML UI BRIEF — F-WH-PUTAWAY · จัดเก็บเข้าที่

> **EXTRACTION-BASED** — ทุกบรรทัดสกัดจาก `01_HTML/F-WH-PUTAWAY.html` (ฉบับในแพ็ก · หลังแก้ตาม LD-03)
> **HTML คือ source of truth ของ UI** · FRD `01_UI` คือสัญญาเชิงธุรกิจ · ไฟล์นี้คือสะพานระดับ selector
> **ห้ามแต่งสเปคเอง** — ถ้าตรงไหนไม่มีใน HTML จะเขียนว่า **"ไม่มีในต้นแบบ"** ตรง ๆ

---

## §1 Design Tokens (สกัดจาก `:root` — ห้าม hardcode ค่าซ้ำ)

### สี — CI CUBE Warm Light

| token | ค่า | ใช้ที่ |
|---|---|---|
| `--c-primary` | `#FF3B30` | ปุ่มหลัก · ป้าย "แนะนำ" · แถบ active ของแถวคิว · `.vseg button.is-on` |
| `--c-primary-hover` | `#E62E24` | hover ของปุ่มหลัก |
| `--c-danger` | `#E62E24` | `.qty-in.is-bad` · `.tag.is-force` · `.warnbox.is-stop` |
| `--c-teal` / `--c-teal-light` | `#FF9A1F` / `#FFB763` | ป้ายกักกัน · จุดสี aging |
| `--c-ink` / `--c-navy` | `#111111` | ข้อความหลัก · sidebar |
| `--c-mute` / `-2` / `-3` | `#54565C` / `#73757B` / `#9A9CA2` | ข้อความรอง 3 ระดับ |
| `--c-line` / `-2` / `-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | เส้นคั่น 3 ระดับ |
| `--c-bg-off` | `#FAF8F5` | พื้นหลัง ivory |
| `--c-success` / `--c-warning` | `#1F9D55` / `#E8870F` | ป้ายสถานะ |

> **มี hex นอก token ตัวเดียวคือ `#E7E2DB`** = `.menu-fixed` ของ BASE-KIT (Rule #69 ห้ามแก้) · ไม่ใช่ของฟีเจอร์

### ขนาด · ระยะ · มุม

| กลุ่ม | tokens |
|---|---|
| โครง | `--sidebar-w: 232px` · `--shell-h: 52px` |
| ตัวอักษร | `--fs-h1 22` · `--fs-h2 17` · `--fs-h3 15` · `--fs-body 14` · `--fs-sub 13` · `--fs-meta 12` · `--fs-cap 11` · `--fs-kpi 28` |
| ระยะ | `--sp-xs 4` · `--sp-sm 8` · `--sp-md 12` · `--sp-lg 20` · `--sp-xl 28` |
| มุม | `--r-xs 4` · `--r-sm 6` · `--r-md 8` · `--r-lg 12` · `--r-full 999` |

**ฟอนต์:** `'Satoshi', 'Noto Sans Thai', system-ui` · `font_count = 8` (limit 8) · ไอคอน **Lucide เท่านั้น** (82 ตัว · `fontawesome = false`)

---

## §2 Z-Index Map (`#62` — ประกาศใต้ `END BASE-KIT` บรรทัด 1352)

```css
:root { --z-content:1; --z-sticky:10; --z-shell:20; --z-dropdown:30;
        --z-backdrop:50; --z-drawer:51; --z-modal:60; --z-toast:80; }
```

| ชั้น | ค่า | element | ยืนยัน runtime (`getComputedStyle`) |
|---|---|---|---|
| content | 1 | เนื้อหาหน้า | — |
| sticky | 10 | `.shell-bar` (sticky) | **10** ✅ |
| (table head) | 3 | `thead th` ใน `.table-scroll.is-sticky` | **3** ✅ |
| shell | 20 | sidebar | — |
| dropdown | 30 | `.menu-fixed` ของ kit | — |
| backdrop | 50 | `.modal-backdrop` (fixed) · `.ss-list` | **50** ✅ |
| drawer | 51 | (**ไม่ใช้** — ไม่มี drawer ใช้งานจริง) | — |
| modal | 60 | `.modal` | ทับได้ถูกชั้น — `elementFromPoint` กลางบน modal คืน element ในตัว modal ✅ |
| toast | 80 | `.toast` (fixed) | **80** ✅ |

> **`--z-*` ถูกใช้ 6 ตัว ประกาศ 8 ตัว → ครบทุกตัวที่ใช้** — ไม่ใช่บั๊ก `--z-*` ที่เคยเจอใน F-SEC-TRANS / F-SEC-LOCKOUT

---

## §3 Overlay Registry + dismiss rules

| overlay | element | ชั้น | เปิดด้วย | ปิดด้วย |
|---|---|---|---|---|
| search-select list | `#ss-list-<key>` (`.ss-list`) | z=50 · `position:absolute` · `max-height:280px` | คลิกช่อง / `ssOpen(key)` | เลือก option · คลิกนอก · **Esc** |
| modal (3 แบบ) | `.modal` + `.modal-backdrop` | z=60 / 50 · `position:fixed` | `askReverse()` / `askLockBin()` / `askUnlockBin()` | ปุ่มยกเลิก · คลิก backdrop · **Esc** · ปุ่มปิด |
| toast | `.toast` | z=80 · `position:fixed` ขวาล่าง | `showToast()` | หายเองใน 2800ms |
| user menu | `#userMenu` | — | `toggleUserMenu()` | คลิกซ้ำ |
| **drawer** | `#drawer` · `#drawerBackdrop` | z=51 / 50 | **ไม่มีโค้ดของฟีเจอร์เรียกเลย** | — |

### ⚠️ หมายเหตุสำคัญสำหรับงานจับภาพ / automation

| # | เรื่อง |
|---|---|
| OV-1 | **`#overlay-root` มีความสูง 0px** (`position:static` · ลูกเป็น `position:fixed`) — **ห้ามใช้เป็น container ตอน `Locator.screenshot()`** จะ timeout · ใช้ `.modal` / `.ss-list` โดยตรง |
| OV-2 | **`#drawer` / `#drawerBackdrop` มีอยู่ใน DOM แต่ไม่เคยถูกเปิด** — คงไว้เพราะ BASE-KIT JS อ้าง id (Rule #69) · **อย่าเข้าใจผิดว่าเป็นฟีเจอร์ที่พัง** |
| OV-3 | `.ss-list` ของ `actor` ล้นขอบล่าง ~17px ที่ 1440×900 เมื่อ input อยู่กลางจอ — **ไม่ใช่บั๊ก** (อยู่ใน pane ที่ scroll ได้ + `max-height:280px` ของ kit) แต่ต้องเลื่อนก่อนถ่ายภาพ |

### Esc chain
```
1. ปิด search-select ที่เปิดอยู่
2. ปิด modal ที่เปิดอยู่
(ไม่มีชั้นที่ 3 — ไม่มี drawer ใช้งานจริง)
```

---

## §4 Route map

| | |
|---|---|
| route | **ไม่มี hash route** (`hash_routes = []`) — ทั้งฟีเจอร์อยู่ URL เดียว |
| `document.title` | `Putaway — จัดเก็บเข้าที่ · CUBE NATIVE` |
| สลับมุมมอง | `setView('queue' \| 'bins' \| 'history')` → `state.view` |
| เลือกงาน | `pickTask(taskId)` → `state.taskId` (**ไม่เปลี่ยน URL**) |

> **Drift ที่ต้องตัดสินตอนทำจริง:** state ไม่ผูก URL → refresh แล้วกลับมาที่คิวเสมอ · ไม่มี deep-link ต่องาน (ดู Drift Log DR-U3)

---

## §5 Anatomy รายส่วน + selector anchors

### §5.1 Shell (Pattern N)

| ส่วน | selector | หมายเหตุ |
|---|---|---|
| sidebar | `.sidebar` (232px) | `.sb-module[data-module]` × 2 · header เป็น `<button>` + `aria-expanded` |
| เมนูย่อย | `.sb-features` > `[data-feature]` | เมนู active = `จัดเก็บเข้าที่` + badge `12` |
| shell bar | `.shell-bar` (52px · sticky z=10) | breadcrumb + กระดิ่ง + user chip |
| footer | `.sidebar` footer | ⚠️ `ต้นแบบ Phase A · 2026` — **ถอดก่อน production** (LD-06) |

### §5.2 Page header + KPI

| ส่วน | selector |
|---|---|
| header | `.ph` > `.ph-title-row` · `.ph-count` · `.ph-sub` · `.ph-actions` |
| tooltip ขอบเขต | `.info-tip[data-tip]` (2 ตัวในหน้า — คิว และ เกณฑ์แนะนำ) |
| KPI | `.stats` > 5 การ์ด (`--fs-kpi 28px`) |
| ตัวสลับมุมมอง | `.vseg` > `button.is-on` |

### §5.3 มุมมองคิว — split-pane (Pattern O)

```
.run-shell
├── .run-aside          ← คิวงาน
│   ├── .aside-head > .aside-head-row > .aside-t / .aside-n
│   ├── .bar > span                       (แถบความคืบหน้า · style="--pct:N%")
│   ├── .aside-tools                      (ค้นหา + ตัวกรอง + เรียง + ล้าง)
│   └── .aside-list
│       ├── .aside-grp > .aside-grp-n     ("คิวปกติ" / "ของกักกัน (รอคืนผู้ขาย)")
│       └── .qcase[.is-on]
│           ├── .rdot[.is-wait|.is-doing|.is-done|.is-hot|.is-off]
│           ├── .qc-main > .qc-t / .qc-m
│           └── .qc-r
└── .run-main           ← แผงทำงาน
    ├── .rh > .rh-top > .rh-name / .rh-sub / .rh-acts
    ├── .kv > .kv-i > .kv-l / .kv-v[.is-num|.is-hot]     (7 ช่อง)
    ├── .rsec (×4)
    │   ├── [1] .rsec-h "ช่องเก็บที่แนะนำ" + .sug-grid > .sug[.is-on]
    │   │        > .sug-top > .sug-code / .sug-rank · .sug-why · .sug-cap
    │   ├── [2] .rsec-h "เลือกช่องเก็บอื่น (ปลายทางที่ N)" + .ss-w-lg > searchSelect('binpick')
    │   ├── [3] .rsec-h "ปลายทางที่จะจัดเก็บ"
    │   │        > .dst-head (6 คอลัมน์ · grid เดียวกับ .dst-row)
    │   │        > .dst-row[.is-over] > .dst-code / .dst-zone / .qty-in[.is-bad]
    │   │                              / .mini-sel[.is-need] / .xbtn
    │   │        > .bin-acts > .cmini ("คงค้างหลังครั้งนี้ N")
    │   │        > .rsn-t (textarea หมายเหตุ)
    │   └── [4] .rsec-h "ผู้จัดเก็บ และ หมายเหตุ" + .ss-w > searchSelect('actor')
    ├── .warnbox[.is-stop]               (คำเตือน / เหตุที่ยืนยันไม่ได้)
    └── .cbar > .cbar-sum · .cmini · .footer-spacer · ปุ่ม 2 ตัว (#btnConfirm)
```

> **`.dst-head` และ `.dst-row` ใช้ grid template เดียวกัน** (ประกาศคู่กันใน CSS `.dst-head, .dst-row`) — **ห้ามแยกสองชุด** ไม่งั้นหัวตารางกับแถวเลื่อนไม่ตรงกัน

### §5.4 มุมมองผังช่องเก็บ (Pattern E)

```
.card > .filt (+ .info-tip) > .table > thead(7 คอลัมน์) > tbody
  └── tr.is-clickable                     onclick="toggleZoneRow('<wh>/<zone>')"
  └── tr.line-expanded > td.zrow-x > .zpanel > .bin-grid
        └── .bin-c[.is-lock]
            ├── .bin-top > .bin-code + .tag(ประเภท) + .pill(สถานะ)
            ├── .bin-meta   ("ความจุ N · ใช้ไป N · คงเหลือ N · ห้ามปนสินค้า")
            ├── .bin-items > .bin-item > span + b   (หรือ "ไม่มีสินค้าในช่องนี้")
            └── .bin-acts   (ล็อกช่อง/ปลดล็อก · ปรับยอด · ย้ายสินค้า)
.table-footer
```

> ★ **คีย์ของ `toggleZoneRow` คือ `<warehouse>/<zone>`** เช่น `'WH-BKK-01/B'` — **ไม่ใช่ `|`** (สำคัญสำหรับสคริปต์ automation)

### §5.5 มุมมองประวัติ (Pattern A + E)

```
.card > .filt (ทั้งหมด / เฉพาะที่ฝืนเกณฑ์ / เฉพาะกลับรายการ / ป้าย append-only / ล้างตัวกรอง)
      > .table-scroll.is-sticky > .table > thead(8 คอลัมน์) > tbody
          └── tr.is-clickable   onclick="toggleHistRow('<movementId>')"
          └── tr.line-expanded  (ที่มาการเลือก · เหตุผล · หมายเหตุ · ใบรับของ · งานที่ผูก · รายการที่ผูกกัน)
.table-footer
```
ปุ่มในแถว: `undo-2` (กลับรายการ) — **หายไปเมื่อ `revBy` ไม่ว่าง** → แสดง `—`

### §5.6 Modal

`.modal` (440px) + `.modal-backdrop` · `.field` > `.field-label` + `.req` · `.mstack` (meta ท้าย modal)
ปุ่มยืนยันเป็น `.is-disabled` จนกว่า `state.mReason` ไม่ว่าง

---

## §6 State-driven UI matrix

| state key | ค่า | ผลบนจอ |
|---|---|---|
| `state.view` | `queue` / `bins` / `history` | `.vseg button.is-on` + เนื้อหาในหน้า |
| `state.wh` | `all` / `<รหัสคลัง>` | กรองทั้งหน้า (**`WH-TRN` ไม่อยู่ในตัวเลือก**) |
| `state.taskId` | id / `null` | `null` → empty state "ยังไม่เลือกงาน" |
| `state.dests[]` | `{bin,qty,src,reason,note}` | แถวในตารางปลายทาง |
| `state.destIdx` | int | ปลายทางที่การค้นหาจะใช้ |
| `state.busy` | bool | ปุ่มยืนยัน `is-disabled` + `loader-2 spin` + `กำลังบันทึก…` |
| `state.mReason` | string | ปุ่มใน modal เปิด/ปิด |
| `state.zoneOpen` | `<wh>/<zone>` / `null` | แถวโซนที่กางอยู่ |
| `state.histOpen` | movementId / `null` | แถวประวัติที่กางอยู่ |
| `state.qf` / `state.hf` | object | ตัวกรองคิว / ประวัติ |

**คลาสสถานะที่ต้องคงความหมาย**

| class | ความหมาย |
|---|---|
| `.rdot.is-wait` / `.is-doing` / `.is-done` / `.is-hot` / `.is-off` | สถานะงานในคิว 5 แบบ (`is-hot` = ค้างเกินเกณฑ์ · `is-off` = ถอนออก) |
| `.qcase.is-on` | งานที่เลือกอยู่ (มี `::before` เป็นแถบสีซ้าย) |
| `.sug.is-on` | การ์ดช่องเก็บที่เลือก |
| `.dst-row.is-over` | จำนวนเกินความจุ — **เตือน ไม่บล็อก** (R15) |
| `.qty-in.is-bad` | จำนวนเกินยอดค้าง/ติดลบ — **บล็อก** (R12/R13) |
| `.mini-sel.is-need` | ต้องเลือกเหตุผล override ก่อน (R11) |
| `.tag.is-force` | ป้าย "ฝืนเกณฑ์" |
| `.tag.is-q` / `.is-tr` / `.is-dm` / `.is-st` | ป้ายกักกัน / ระหว่างทาง / ของเสีย / ในมือคุณ |
| `.bin-c.is-lock` | ช่องเก็บที่ถูกล็อก |
| `.warnbox.is-stop` | กล่องเหตุที่ยืนยันไม่ได้ / ไม่มีช่องที่ตรงเกณฑ์ |
| `.bar.is-full > span` | แถบความคืบหน้าเต็ม |

---

## §7 BACKEND anchors — จุดที่ต้องต่อ API จริง

| จุดบนจอ | ฟังก์ชันในต้นแบบ | → API (`02_API`) |
|---|---|---|
| โหลดคิว + ตัวกรอง + เรียง | `queueTasks()` · `qfSearch/qfSet/qfReset` | **API-01** |
| เลือกงาน → หัวงาน | `pickTask()` · `runnerHTML()` | **API-02** |
| ปุ่ม `รับงาน` | `claimTask()` | **API-03** |
| ปุ่ม `คืนงาน` | `releaseTask()` | **API-04** |
| ปุ่ม `ปลดล็อกงาน (หัวหน้าคลัง)` | `forceRelease()` | **API-05** |
| การ์ดช่องเก็บที่แนะนำ | `suggestBins()` | **API-06** → `ENG-PUT-SUGGEST` |
| ช่องค้นหาช่องเก็บ | `pickerOptions()` · `chooseBin()` | **API-07** |
| **ปุ่ม `ยืนยันจัดเก็บ`** | `confirmPutaway()` | **API-08** → `ENG-INV-MOVE` + ENG-CSQ |
| มุมมองผัง — ยอดราย bin | `usedOf()` · `stockAt()` · `freeOf()` | **API-09 / API-10** |
| ปุ่ม `ล็อกช่อง` / `ปลดล็อก` | `doLockBin()` / `doUnlockBin()` | **API-11 / API-12** |
| มุมมองประวัติ | `histRows()` · `hfSearch/hfSet` | **API-13** |
| ปุ่ม `กลับรายการ` | `doReverse()` | **API-14** |
| KPI 5 การ์ด | `kpi()` | **API-15** |
| ปุ่มเปิดใบรับของ | `openGrn()` — **mock** | **API-16** + หน้าจอ F079 |
| ปุ่ม `ปรับยอด` | `fwdAdjust()` — **mock** | **F-WH-STKADJ** (§2.8.2) |
| ปุ่ม `ย้ายสินค้า` | `fwdTransfer()` — **mock** | **F-WH-STKTRF** (§2.8.3) |
| ปุ่มคืนผู้ขาย (คิวกักกัน) | `fwdRtv()` — **mock** | **F-PUR-RTV** (§2.8.4) |
| จุดยิง 7C | `emitCsq()` (no-op) | **ENG-CSQ** (§2.8.5) |
| ค่าเกณฑ์ `NC` | `const NC = {...}` บรรทัด 2069 | **NC rules service** |
| เมนู sidebar อื่น | `navStub()` — toast นอกขอบเขต | หน้าจออื่นของโมดูล |
| กระดิ่งแจ้งเตือน | `notifyStub()` — toast นอกขอบเขต | **ไม่ทำในรอบนี้** (ไม่มีชิป `ntf`) |

---

## §8 Traceability 3 ทาง (Brief ↔ FRD ↔ HTML)

| เรื่อง | Brief (ไฟล์นี้) | FRD | HTML |
|---|---|---|---|
| โครงหน้า split-pane | §5.3 | `01_UI` §1.3/§1.4 | `.run-shell` / `.run-aside` / `.run-main` |
| เกณฑ์แนะนำ | §5.3 `.sug-*` | `03_LOGIC` FN-09/10/11 | `suggestBins()` 2220–2259 |
| ชนิดการฝืนเกณฑ์ | §6 `.tag.is-force` | `03_LOGIC` FN-13 · `05_RULES` R11/R15 | `violationOf()` 2262–2273 |
| เหตุที่ยืนยันไม่ได้ | §5.3 `.warnbox.is-stop` | `05_RULES` §5.2 · `01_UI` §1.11 | `destIssues()` 2488–2504 |
| movement append-only | §5.5 (ไม่มีปุ่มลบ) | `05_RULES` R16 · `04_DB` §4.2 | `MOVES.push()` เท่านั้น |
| คู่กลับรายการ | §5.5 "รายการที่ผูกกัน" | `03_LOGIC` FN-18 · DR-07 | `revOf` / `revBy` |
| location 5 ประเภท | §5.4 `.tag.is-tr` / `.is-dm` | `04_DB` §4.7.2 | `LTYPE` + `typeTag()` |
| ปี ค.ศ. | §1 | `05_RULES` R22 | `fmtD()` / `fmtDT()` |
| จุดยิง 7C | §7 | `05_RULES` §5.5 | `emitCsq()` 2901–2905 |

---

## §9 Drift Log — จุดที่ต้นแบบกับสเปคไม่ตรงกัน 100%

| # | Drift | รายละเอียด | ท่าที |
|---|---|---|---|
| **DR-U1** | **`PEOPLE[].ini` เป็น dead data** | ฟิลด์อักษรย่อ (`อพ` `สท` `พว` `วศ`) มีในข้อมูลแต่ **ไม่มีโค้ดไหนอ่าน** — option ของ `actor` ใช้ไอคอน Lucide `user` แทน · BRD R24 เขียนว่า "avatar + ตำแหน่ง + ชื่อ" | **เกรด ✅ พร้อมหมายเหตุ** — anatomy ที่ใช้เป็นไปตาม #102 และเจตนาหลัก (คนจริง ไม่ใช่ role ID) เป็นจริงครบ · **dev ตัดสินตอนทำจริง:** render initials avatar หรือลบฟิลด์ |
| **DR-U2** | **`.is-done` เป็น dead CSS** | คลาสเดียวใน page CSS (83 คลาส) ที่ไม่ถูกใช้ในมาร์กอัป | **WARN ไม่ใช่ให้ลบทันที** — ไฟล์มี dynamic class construction จริง ให้ตรวจซ้ำตอนทำจริง |
| **DR-U3** | **state ไม่ผูก URL** | refresh แล้วกลับมาที่คิวเสมอ · ไม่มี deep-link ต่องาน | **เจตนา** (console ไม่ใช่เอกสาร) · ถ้าต้องการ deep-link ให้เปิด change request |
| **DR-U4** | **`NC.softLockMinutes` ประกาศแต่ไม่ถูกใช้** | R18 วรรค c (auto-return) ยังไม่ implement | **ต้องทำฝั่งเซิร์ฟเวอร์** — `07_LOCKED` **LD-05** |
| **DR-U5** | **ชุด mock เดินไปไม่ถึงสาขา "ถือโดยคนอื่น"** | `PT-0011` ถือครองโดย `u-anucha` ซึ่งเป็น `ME` → `holderBtnHTML()` สาขาที่ 4 render ไม่ได้ | **โค้ดถูกต้อง ต้องคงไว้** · ข้อเสนอแก้ mock = `OQ-PUT-11` |
| **DR-U6** | **`#drawer` / `#drawerBackdrop` ค้างอยู่ใน DOM** | ไม่มีโค้ดของฟีเจอร์เรียกเลย | **คงไว้** — BASE-KIT JS อ้าง id (Rule #69 · L9) |
| **DR-U7** | **`#overlay-root` สูง 0px** | portal container ที่ลูกเป็น `position:fixed` | **ไม่ใช่บั๊ก** — แต่ห้ามใช้เป็น capture container (§3 OV-1) |
| **DR-U8** | **`PREBRIEF §8` `PT-0005` ไม่ตรงพฤติกรรมจริง** | ตั้งใจให้เป็นตัวอย่าง override ข้ามหมวด แต่เกณฑ์ R1 จับได้ก่อน (มีตลับหมึกอยู่ที่ `B-03-02-B` แล้ว) | **engine ถูกกว่า mock** — แก้ที่ PREBRIEF ไม่ใช่แก้โค้ด · `OQ-PUT-12` |
| **DR-U9** | **watermark + คำว่า `NC rules` บนจอ** | `ต้นแบบ Phase A · 2026` · `เกิน 24 ชม. (เกณฑ์จาก NC rules)` | **ถอด/ทบทวนก่อน production** — `07_LOCKED` LD-06 |
| **DR-U10** | **HTML ต่างจากต้นน้ำ 2 บรรทัด** | ถอด marker `FWD-WIRE:` ออกจากข้อความที่ผู้ใช้เห็น (บรรทัด 2561 · 2584) | **เจตนา อนุมัติแล้ว** — `07_LOCKED` **LD-03** · ถ้า BA ส่ง HTML ใหม่ ต้อง merge การแก้นี้เข้าไปด้วย |

---

## §10 สิ่งที่ **ไม่มี** ในต้นแบบ (ตรวจแล้ว — อย่าไปหา)

| ไม่มี | ยืนยันเชิงกล |
|---|---|
| wizard / stepper ที่ใช้งานจริง | `wizard_steps = []` · คลาส `.stepper*` มีแต่ใน BASE-KIT CSS (dead) |
| view-drawer แท็บเอกสาร | `view_tabs = []` · `custom_tabs = 0` · `tabBtn(` = 0 |
| line editor B2 | `line_tbl = false` · `calcLineVat` = 0 |
| PDF / A4 / ลายเซ็น | `a4 = false` · `renderSignTab` = 0 · `has_signProgress = false` |
| เลขที่เอกสาร / doccfg | `has_docPill = false` · `doccfg` = 0 · `ENG-DOC-NUM` = 0 |
| สายอนุมัติ / DOA slot | `slot_row = false` · `DOA` = 0 |
| ปุ่มลบ / ปุ่มแก้ movement | ไล่ทุกปุ่มใน 3 มุมมอง ด้วย regex `ลบ\|delete\|remove` = **0** |
| ปุ่มสร้างงาน putaway | ไม่มี — คิวสร้างโดยระบบเท่านั้น (DR-01) |
| ช่อง lot / serial / pallet | ไม่มีช่องกรอกใด ๆ |
| ตัวเลขเงิน / มูลค่า | ไม่มี — KPI ฝืนเกณฑ์นับ **รายการ** (`33% · 1 จาก 3 รายการที่จัดเก็บ`) |
| `PIPES_HIT` / คอลัมน์ผลรายท่อ 7C | `PIPES_HIT` = false |
| marker ภายในบนจอ | jargon sweep 13 สถานะ → **0 hit** (หลัง LD-03) |

# UX Check Report — F-HR-ESS (ESS Portal · ess.html)
- วันที่: 2026-09-10 · **Iteration: 3 (re-run after BA re-gate FIX-01..04 · C3.2 retrace)**
- Generator spec (Sync Read): `html-generator-v9` — `knowledge/iron-rules.md` (#1–#49 · #94–#105) · `layout-integrity.md` (#50–#62) · `component-contracts.md` (#63–#68·#74–#80) · `page-anatomy.md` (#70–#73) · `ci-tokens.md` · `microcopy.md`
- Passes run: **audit.sh** · **self_audit.py** (Pass G geometry) · **Pass R render (playwright — จริง รอบนี้)** · Pass D = **N/A** (is_document=false — portal ไม่ใช่เอกสารธุรกรรม) · golden compare (page-anatomy #70–73 · ไม่มี golden เฉพาะ portal-aggregate)
- ไฟล์ที่ตรวจ: outputs/F-HR-ESS/ess.html (**2710 บรรทัด** · 135 KB · +36 บรรทัดจาก FIX-01..04)
- Archetype: portal(aggregate) · **display-only** · deep-link-only action picker (ตอนนี้ 5 แถว)

## Verdict: 🟢 PASS (with 5 warnings · residual/cosmetic ทั้งหมด)
| BLOCK | WARN | INFO | NOT-CHECKED |
|---|---|---|---|
| 0 | 5 | 3 | 0 |
ประเมินเวลาแก้ (WARN ที่เหลือ = cosmetic/residual ล้วน ไม่บังคับก่อน handoff): ~0–10 นาที

**เกณฑ์ผ่าน gate = BLOCK 0 → ผ่าน.** audit.sh FAIL=0 · WARN=3 (residual base-kit) · self_audit residuals = ชุดเดิมที่ triaged แล้ว (ไม่มีตัวใหม่จาก FIX) · **Pass R render จริงยืนยัน 0 regression: ไม่มี h-scroll ทุก tab ที่ 1440/1024/768 · prod-strip สะอาด · DSP-01/DSP-02/Esc chain/display-only lock ครบ**

---

## 🔁 FIX-01..04 delta verification — 0 regression (Pass R render จริง)

| FIX | สิ่งที่เพิ่ม | ตรวจแล้วยังไง | ผล |
|---|---|---|---|
| **FIX-01** | apRow แถวที่ 5 "ขอหนังสือรับรอง" (`award` icon) + `LINKS.cert`=`#/cert/new` + ปุ่ม "ขอหนังสือ" บน section FN-06 | render จริง: action-picker = **5 แถว** (`['ขอลา','ขอ OT','ขอเบิก','ขอแก้ข้อมูล','ขอหนังสือรับรอง']`) · cert row ใช้ `apRow()` helper ตัวเดียวกับ 4 แถวเดิม (2-line ap-title/ap-sub) · ปุ่ม cert (L2417) = `btn btn-primary btn-sm`+`external-link`+`deepLink('cert')` = pattern เดียวกับ "ยื่นเบิก" (FN-05 L2407)/"ขอแก้ข้อมูล" (FN-08 L2450) เป๊ะ · `deepLink('cert')` → toast `กำลังนำทางไปหน้า "หนังสือรับรอง"` ไม่มี CRUD | ✅ **ไม่มี iron-rule break** — reuse helper/kit class ครบ |
| **FIX-02** | section read-only "ตารางกะของฉัน" (FN-04 · `DATA.shifts` · 7 วัน) ใน renderPay หลัง OT | ใช้ `sec()` helper + `table-scroll/table` แบบเดียวกับตาราง OT scans ด้านบน (L2386) · ไม่มี action แก้/บันทึก (chip CH_ASSUMED+CH_RO อ่านอย่างเดียว) · render tab `pay` ทุก width ไม่ error/ไม่ล้น | ✅ display-only intact · component consistent |
| **FIX-03** | 2 CSQ code-comment anchors (`accessDenied` L2657 · payslip render L2534) | เป็นคอมเมนต์ล้วน — ไม่ขึ้นจอ · self_audit `jargon_leak=0` | ✅ ไม่กระทบจอ |
| **FIX-04** | `.demo-only` class + `.demo-only{}` CSS rule (L1397) · reword copy (self-banner/accessDenied/toast) · ย้าย dev terms (`[ASSUMED]`/`SecC`/`PS-1`/`ENG-NOTIFY`) เข้าคอมเมนต์ | **prod-strip render test:** inject `.demo-only{display:none!important}` → demo-only nodes `visibleRects 3→0` (ซ่อนสะอาด) · **ไม่มี h-scroll** ทุก tab ที่ 1440/1024/768 (docSW ≤ docCW ทุกจุด) · ไม่มี page/console error · `SecC`/`PS-1`/`ENG-NOTIFY` เหลือเฉพาะในคอมเมนต์ (grep ยืนยัน) | ✅ layout intact ทั้ง as-is และ prod-strip |

**Component-consistency (Phase 3):** cert row/button + shift section **ไม่สร้าง component ใหม่** — เรียก `apRow()`/`sec()`/`table` เดิม → iron-rule #82 (JS จาก kit) ผ่าน · ไม่มี primary ปุ่มสองแบบ · ไม่มี badge สีเพี้ยน

---

## ✅ Invariants ยัง intact (render จริง ยืนยัน)

| Invariant | หลักฐาน (Pass R interaction test) |
|---|---|
| **DSP-01** modal เหนือ drawer | เปิด drawer (cert view) แล้ว `openModal('actionPicker')` → coexist `{drawer:true, modal:true}` · computed z: **modal 60 > drawer 55** (`.modal-backdrop{z-index:var(--z-portal)}` L1372 ไม่ถูก FIX แตะ) |
| **Esc chain** modal → drawer | Esc#1 → `{modal:false, drawer:true}` · Esc#2 → `{drawer:false}` (handler L1766-1768 · closeModal defer 200ms/closeDrawer 280ms = base-kit ปกติ) |
| **DSP-02** state ข้าม re-render | `preserveRenderState()/restoreRenderState()` (L2250/2262) + `state.tab/notif` persist (L2233-2235) ไม่ถูก FIX แตะ |
| **display-only lock** | action picker + ทุกปุ่ม = `deepLink()`→`showToast('กำลังนำทาง…')` navigate-out เท่านั้น · ไม่มี save/submit/CRUD ในไฟล์ · shift/cert section = read table ล้วน |
| **prod-strip clean** | `.demo-only{display:none}` → demo-strip + chips หายหมด (visibleRects 0) · read-only สื่อด้วยการไม่มีปุ่มแก้ (ตามคอมเมนต์ L2242) · ไม่มี h-scroll |

---

## 🟡 WARN (residual — cosmetic ล้วน · audit.sh FAIL=0 · ไม่มีตัวใหม่จาก FIX)

### UX-02′ · Rule #1 CI Tokens — off-palette tints (self_audit hex_off=6) · L1377/1381/1389/1402
- `#C5D9F7` (self-banner border) · `#12408F` (self-banner b) — เฉด blue เสริมของ info pill `#E6F0FF`/`#1A5FCC`
- `#B4B6BB` (demo-strip `.ds-label` L1389) — grey อ่อนบนพื้นเข้ม (จะถูก strip ใน prod อยู่แล้ว)
- `#F3D9AD` (chip-assumed border L1402) — เฉด orange ของ warning chip (chip นี้เป็น `.demo-only` → prod strip)
- `#104`/`#105` ใน hex list = **false-pos** (เลขกฎในคอมเมนต์ ไม่ใช่ hex)
- **แก้:** ยก tint ขึ้น CSS var/ใช้เฉด token ที่มี — ทั้งหมดอยู่บน component เฉพาะ ESS (2 ใน 4 เป็น demo-only) · audit.sh **ไม่** flag FAIL · **FIX ไม่ได้เพิ่ม hex ใหม่** (คงที่ 6 เท่า Iter-2)

### UX-03 · Token — hardcoded font-size (audit.sh WARN · self_audit font_count=13>8)
- px ตรง แทน `--fs-*` — บางส่วน BASE-KIT (L94/141/142/157/180 · ห้ามแตะ C3.7) · บางส่วน component ESS (11.5/13.5/14.5/22px)
- **แก้:** map component ESS เข้า `--fs-*` เท่าที่ทำได้ · BASE-KIT = residual · **คงเดิม ไม่ขยับจาก FIX** (11.5px ใน cert sub-line reuse ของเดิม)

### UX-04 · Rule #21 base-kit icons ไม่มี w-/h- class · L1327/1837/1952/2280/2325 (audit.sh WARN)
- `<i data-lucide>` บางตัวไม่มี `w-{N}/h-{N}` — จาก BASE-KIT render + icon คุมขนาดผ่าน CSS `[data-lucide]` selector → ไม่พังภาพ · residual

### UX-05 · Pass G inline-layout (self_audit=20) · หลายจุด
- ส่วนใหญ่ปลอดภัย: dynamic width `style="width:'+pct+'%"`, typography note `margin-top/bottom:14px`, id sub-line `font-size:11.5px` · layout จริง = `margin-left:auto` (L2288/2407/2448)
- **แก้:** ย้าย layout จริงเข้า class ใน `#page-late` · audit.sh FAIL=0 (tidiness) · **คงเดิม ไม่ขยับจาก FIX**

### UX-06 · Pass G flex-noalign (2) · `.nrow` · `.aud` (audit log)
- `display:flex` ไม่มี `align-items` — ตั้งใจ top-aligned · ภาพไม่เพี้ยน (render ยืนยัน) = ปล่อยได้

---

## ℹ️ INFO

### INFO-1 · read-only chips (CH_ASSUMED/CH_RO) ตอนนี้เป็น `.demo-only` — ตรวจแล้ว benign
- FIX-04 ติด `.demo-only` ให้ chip อ่านอย่างเดียว → prod strip แล้ว section header ที่มีแค่ chip (OT L2381 · welfare L2428 · notify L2484) จะเหลือ `.sh-right` เปล่า
- **render prod-strip ยืนยัน:** span เปล่าไม่ทำให้ layout พัง/ไม่มี h-scroll · read-only ยังสื่อด้วยการไม่มีปุ่มแก้/บันทึก (เจตนาในคอมเมนต์ L2242) → ไม่ใช่ WARN

### INFO-2 · PREFLIGHT stamp ค้าง (L2697 `hex-off=7`) vs นับจริง `hex_off=6` — pre-existing ไม่ใช่ผลจาก FIX
- stamp round1 ระบุ `hex-off=7` แต่ self_audit จริง=6 (ตกจาก launcher fix รอบ Iter-1→2 ที่เอา `#1C1C1C` ออก) — **stamp over-count (ฟ้องเกินจริง ไม่ใช่ซ่อน)** · counter อื่นตรงหมด (spacing 17 · font 13 · inline 20 · flex 2 · z 0)
- FIX-01..04 **ไม่ได้ขยับ hex count** (คงที่ 6) → mismatch นี้ตกทอดมาจากรอบก่อน ไม่ใช่ regression · authoritative gate audit.sh=FAIL 0 · **ข้อเสนอ (ไม่บังคับ):** ผู้เขียน refresh stamp ให้ตรง (`hex-off=6`) ตอนแตะไฟล์ครั้งหน้า

### INFO-3 · guard `stopPropagation()` L2684-2687 ยัง inert (bubble บน document) — ยกจาก Iter-2 ไม่กระทบ verdict
- overlay จัดการ inside/outside เอง + deepLink ปิด modal เอง → ไม่ก่อผลเสีย · cosmetic

---

## Passes summary (mechanical + render)
- **audit.sh:** FAIL=0 · WARN=3 (Rule#40 `.uc-email` base-kit · Rule#21 base-kit icons · token font-size) → **gate ผ่าน** · doc_archetype.is_document=false → Pass D N/A
- **self_audit.py:** RESULT FAIL (ไม่ใช่ zero-tolerance — gate = audit.sh FAIL=0) · residuals = ชุดเดิม triaged: hex_off=6 (`#104/#105` false-pos + 4 cosmetic tints) · spacing_off=17 · font_count=13 · flex_noalign=2 · inline_layout=20 · custom_tabs=4 (drawer-tab/seg-item = kit-style) · long_banners=2 (self-access SecC + OQ-HR-04 note · ตั้งใจยาว) · missing_ids `page-content`=false-pos (host จริง `appContent` L2251) · jargon_leak=0 (FIX-04 ย้าย dev terms เข้าคอมเมนต์แล้ว) · **ไม่มี counter ใหม่จาก FIX**
- **Pass R render (playwright · จริง):**
  - h-scroll: **0** ทุก tab (home/pay/docs/notify) × width (1440/1024/768) — as-is และ prod-strip (`.demo-only{display:none}`) · docSW ≤ docCW ทุกจุด
  - prod-strip: demo-only nodes visibleRects **3→0** (ซ่อนสะอาด) · ไม่มี page/console error ทั้งสอง variant
  - interaction: action-picker 5 แถว (cert อยู่ท้าย) · DSP-01 modal z60>drawer z55 coexist · Esc chain modal→drawer ทำงานถูก · `LINKS.cert=#/cert/new` · toast navigate-out เท่านั้น (ไม่มี mutation)
- **Delta:** FIX-01..04 = 4/4 ตรวจ regression แล้ว — **0 regression**

## Known accepted tension (ไม่นับเป็น finding)
- BR-05 "mobile" vs #97 desktop-base `min-width:768` — kit desktop-base เก็บไว้โดยเจตนา (ระบุใน brief) · ที่ 768px render ไม่มี h-scroll

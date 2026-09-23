# _UX_CHECK_REPORT — F-ACC-DN ใบลดหนี้ผู้ขาย (Debit Note)

| | |
|---|---|
| ไฟล์ | `outputs/F-ACC-DN/F-ACC-DN_debit-note.html` |
| Generator (Sync Read) | `html-generator-v9` (`.claude/skills/html-generator-v9`, v9.1) — Pattern Q + B2 v2 |
| ขั้นตอน | WF-01 step 3 — ตรวจ "ทำถูกมั้ย" (CI / iron rules / geometry / overlay / UX) |
| รอบ | **RE-GATE (C3.2) รอบ BA FIX 2026-09-23** — HTML ถูกแก้ตาม `feedback dn/FIX_PROMPT_F097` + `REVIEW_FIX_ORDER` (FIX-01 เครดิตคงเหลือ · FIX-02 ภาษีซื้อ vendorCn · FIX-03 anchors · FIX-04 demo-only) → ตรวจ step 3 ใหม่ |
| วันที่ | 2026-09-23 (Windows) |
| **Verdict** | 🟢 **PASS with 1 warning** — BLOCK = 0 · audit.sh **FAIL=0 · WARN=1** (baseline sidebar font-size = FIX-05 optional) · static_scan: ไม่มี BLOCK signal ใหม่ (emoji 0 · fontawesome no · external_scripts 0 · aria canonical · hex อยู่ใน PDF/base-kit) · self_audit hex_off=0 |

---

## สรุปหัว report

- **BLOCK = 0** · **WARN = 1** · **INFO = 0**
- Gate ที่ผูกพัน = `audit.sh` **FAIL=0** (ตาม memory `html-v8-self-audit-not-zero-tolerance`: self_audit เป็นตัวนับเสริม ไม่ใช่ gate) — **ผ่าน**
- ✅ **ไม่มี NEW BLOCK/WARN จาก batch fix** — โค้ดใหม่ (end-bill FN-19 + real file-input) สะอาด · **WARN-01 (hex_off) รอบก่อน = แก้แล้ว** (hex_off 2→0)

---

## Phase 1 — Mechanical (audit.sh = gate)

`bash .claude/skills/html-generator-v9/scripts/audit.sh <file>` → **FAIL = 0 · WARN = 1** · `doc_archetype`: **ไม่มี FAIL**

| WARN | สถานะ | เหตุผล |
|---|---|---|
| Token — hardcoded `font-size` (sidebar BASE-KIT, บรรทัด 73/123/125/139) | คงไว้ (baseline) | WARN ตัวเดียวกันยิงบน golden `file-skeleton.template.html` และ sibling CN ที่ผ่านแล้ว — ไม่ใช่ regression |

### self_audit.py (ตัวนับเสริม — non-zero-tolerance · **ไม่ใช่ gate**)
`RESULT: FAIL` — residual:
- **Canonical Pattern Q set (documented/accepted):** `inline_layout=242 · stopprop_blanket=6 · missing_ids=4 (combo-pop/item-input-/item-pop/row-menu) · custom_tabs=2 · long_banners=1 (cancelInfo)` — ทั้งชุดตรงกับ sibling CN
- **`hex_off = 0`** ✅ — WARN-01 (stale var fallback #0B5CFF/#0B1D3A) รอบก่อน **แก้แล้ว**
- **`spacing_off = 2` (`9`/`11`)** — tooltip `.hint::after { padding: 9px 11px }` ใน utility-shim block · inherited จาก shim เดิม เหมือน sibling CN เป๊ะ · ไม่ใช่ regression
- **inline_layout 233 → 242 (+9):** มาจากโค้ดใหม่ (การ์ด end-bill toggle + segmented + upload-zone + file-row) — **ทุกจุดใช้ var() tokens** ไม่มี off-token hex · ยังต่ำกว่า sibling CN (248) = ไม่ใช่ regression

---

## โฟกัสรอบนี้ — โค้ดใหม่จาก batch fix (2 การเปลี่ยน)

### ① ส่วนลดท้ายบิล FN-19 (user KEEP) — UI + summary rows
| ตรวจ | ผล |
|---|---|
| Toggle UI (renderStep3 บรรทัด 997–998) | ✅ ใช้ `.toggle` มาตรฐาน + segmented buttons (amount/percent) + `input.num` — โครงเดียวกับ B2 v2 VAT segmented · ทุก style = var() token |
| Summary rows (renderLineSummary บรรทัด 1025 · linesTableView tfoot บรรทัด 1044) | ✅ แถว "ส่วนลดท้ายบิล · ลดฐานภาษี / ฐานภาษีหลังหักส่วนลด / ภาษีซื้อ ม.86/10" ใช้ `var(--c-purple)/--c-text-mute/--c-border-soft` — ไม่มี hex นอก whitelist |
| Ref-tab JE + VAT impact (บรรทัด 921/931) + submit modal (907) | ✅ ใช้ `netVat`/`netBefore` สม่ำเสมอ |
| Over-cap warning (lineSummaryWarn บรรทัด 896) | ✅ ใช้ construct `.hard-warn` (บรรทัด 634 = `rgba(230,46,36,.08/.25)` = สี danger, **ไม่ใช่ off-token hex**) — เป็น hard-warn เชิงบล็อก ตรงหมวด #67.1 ① (ไม่ใช่ info/hint ลอย) |
| Max-cap helper "ลดได้สูงสุด ฿X" (บรรทัด 998) | ✅ ข้อความ contextual ติดกับ field (เปลี่ยนเป็น --c-danger เมื่อเกิน) = field-level validation หมวด #67.1 ② · `naked_hints=0` |

### ② เอกสารแนบ = `<input type="file">` จริง (mockUpload ถูกลบ)
| ตรวจ | ผล |
|---|---|
| renderStep4 (บรรทัด 1073–1078) | ✅ `<input type="file" multiple>` จริง + `.upload-zone` + `pickAttachments/triggerAttachPick/fmtFileSize` · ไฟล์โรว์ใช้ var() token · `event.stopPropagation()` เฉพาะโรว์ใน (canonical Q, นับใน stopprop_blanket=6 อยู่แล้ว) |
| Overlay/z-index | ✅ ไม่มี dropdown/overlay ใหม่ · `overlay_no_z=0 · menu_no_flip=0 · z_adhoc=0` |

---

## Pass D — Document Archetype (Pattern Q)

| ตรวจ | ผล |
|---|---|
| audit.sh `doc_archetype` | ✅ ไม่มี FAIL |
| Wizard 5 steps (#100) | ✅ `เลือกแหล่งที่มา › ข้อมูลหลัก › รายการสินค้า › เอกสารแนบ › ตรวจสอบและยืนยัน` (renderStepperItem บรรทัด 1060) |
| View tabs order (#101) | ✅ detail › [domain] › pdf › sign › history — ไม่มี tab attachments |
| B2 v2 line editor / VAT segmented / grid widths | ✅ `line-tbl` widths 26/—/64/92/92/78/72/104/54 (บรรทัด 995) คงเดิม |
| DOA chain hardcoded นอก mock | ✅ ไม่พบ · DOA tier ใช้ post-end-bill grand (step5Extra resolveDoa{lines,endbill} บรรทัด 900) |

## Iron rules #104 / #105 / #106 / #67.1 (v9.1)

| กฎ | ผล |
|---|---|
| #104 (sub-view = tab row มาตรฐาน) | ✅ `tabBtn(...)` ไม่ใช่ dropdown/ปุ่มขวาบน |
| #105 (persona switcher + `data-demo` + DEMO badge) | ✅ `data-demo="persona-switch"` ครบ |
| #106 (toolbar filter block มาตรฐาน) | ✅ `toolbar`/`search-box` · ไม่พบ `filter-row`/`filter-bar`/`input-search` |
| #67.1 (จำกัด on-screen message) | ✅ พบเฉพาะ construct ที่อนุญาต: hard-warn (over-cap DN + over-cap end-bill), field-error/max-cap helper, note.danger (cancel) · ไม่พบ info-banner/callout/ⓘ ที่ไม่มีแหล่ง |

> **หมายเหตุ governance (ส่งต่อ step 4/12):** hard-warn + max-cap helper ของ end-bill เป็นข้อความจอ **ใหม่** ที่ยังไม่อยู่ใน allow-list §6 ของ PREBRIEF (ซึ่งลิสต์ไว้ 3 ตัว) — **ไม่ใช่การละเมิด #67.1** (เป็น construct หมวด ①/② ที่ผูกกับ validation ของ FN-19 ไม่ใช่ hint ลอย) แต่ BA ควรขยาย §6 พร้อมกับรับ FN-19 เข้า PREBRIEF

---

## NOT-CHECKED

- **Pass R — Render Gate (playwright screenshots):** รอบ re-gate นี้ตรวจ mechanical + static + อ่านโค้ดโดยตรง ไม่ได้รัน render_shots — โครง Q archetype ไม่ต่างจาก sibling CN ที่ render ผ่าน · การเปลี่ยนเป็นการเพิ่มการ์ด/แถว summary + real file-input (ไม่มี overlay/geometry ใหม่) · แนะนำรัน render gate ก่อนส่ง dev ถ้าต้องการหลักฐานภาพครบชุด
- **business coverage / e2e:** อยู่นอกขอบเขต step 3 (งานของ qc-coverage + e2e — รายงานแยก)

---

## สรุป

**PASS with 1 warning · BLOCK = 0.** Gate ผูกพัน (audit.sh FAIL=0) ผ่าน · batch fix ไม่ก่อ NEW violation — end-bill FN-19 UI/summary + real file-input ใช้ var() token, hard-warn ที่อนุญาต, standard component ล้วน · WARN-01 (hex_off) รอบก่อนแก้แล้ว (hex_off=0) · self_audit residual = canonical Q set (≤ sibling CN) + spacing tooltip ที่ inherited. ไม่มีเหตุ BLOCK — เดินต่อ step 4 ได้

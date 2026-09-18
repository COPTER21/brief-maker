# _TECH_CHECK — F-WH-STKTRF · Stock Transfer

> Stage **S3c** Technical gate · 2026-09-10 · ไฟล์: `1_HTML/F-WH-STKTRF.html`

## VERDICT: **PASS** — FAIL = 0 · JS syntax ผ่าน · console error (นอก CDN) = 0

---

## 1. JS syntax (`node --check`)

```
สกัด <script> 2 บล็อก → /tmp/trf.js → node --check
ผลรอบสุดท้าย: ผ่าน (no output)
```

| รอบ | ผล | หมายเหตุ |
|---|---|---|
| 1 | ❌ `SyntaxError: Unexpected token ':'` ที่ footer ของ `renderCreateDrawer()` | ternary ขึ้นบรรทัดใหม่ด้วย `+ : '…'` |
| 2 | ✅ ผ่าน | ย้ายเครื่องหมาย `+` ให้อยู่หลัง string |
| 3 (หลังแก้ coverage/UX) | ✅ ผ่าน | ตรวจซ้ำหลังทุกครั้งที่แก้ไฟล์ |

## 2. `audit.sh` (hard gate — ต้อง FAIL = 0)

```
bash .claude/skills/html-generator-v9/scripts/audit.sh <html>
สรุป: FAIL=0 · WARN=1
```

| ระดับ | รายการ | การจัดการ |
|---|---|---|
| FAIL | — | **ไม่มี** |
| WARN | `Token — hardcoded font-size ที่ไม่ใช่ var` (ชี้ไปที่ `body{font-size:14px}` · `.sb-name` · `.sb-item` ฯลฯ) | **ยอมรับ** — ทั้งหมดอยู่ในบล็อก **BASE-KIT ที่ห้ามแก้ (Rule #69)** ซึ่งประกาศ px ตรง ๆ มาแต่เดิม |

**ส่วน `doc_archetype` (Rule #98–#101) ผ่านครบทุกข้อ** — ไม่มี FAIL แม้แต่รายการเดียว:
`class="tbl line-tbl"` · `calcLineVat` · `migrateLine` · `totals(` · `taxBadgeV` · `renderLineSummary` · `line-expand-panel-anchor` ·
VAT segmented 3 โหมด · step `ตรวจสอบและยืนยัน` / `'เอกสารแนบ'` / `'รายการสินค้า'` · `STEPH(` · `upload-zone` ·
`tabBtn('detail'/'pdf'/'sign'/'history'` · `SEC('paperclip', \`เอกสารแนบ…` · `renderSignProgress` · `docPill` · `class="a4"` · `slot-row` · `drawer-panel wide` ·
ไม่มี tab เอกสารแนบแยก · ไม่มี hardcoded approval chain

## 3. Render check (Playwright / Chromium)

```
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers · chromium headless
viewport 1440×900 (หลัก) + 1024×800 (responsive tier)
```

| # | หน้า/สถานะที่เปิด | ไฟล์ภาพ | ผล |
|---|---|---|---|
| 1 | List + KPI + filter + ตาราง 13 ใบ | `_shots/01_list.png` | ✅ |
| 2 | View drawer — tab รายละเอียด (`TRF-2026-0003`) | `_shots/02_view_detail.png` | ✅ |
| 3 | View drawer — **tab ระหว่างทางและการรับ** (2 ขา + สมการ invariant) | `_shots/03_view_transit.png` | ✅ |
| 4 | View drawer — tab PDF Preview (`.a4` 4 ช่องเซ็น) | `_shots/03_view_pdf.png` | ✅ |
| 5 | View drawer — tab ลายเซ็น/อนุมัติ | `_shots/03_view_sign.png` | ✅ |
| 6 | Wizard step 2 (ชิปโหมด + แถบเส้นทาง + in-transit readonly) | `_shots/04a_wizard_step2.png` | ✅ |
| 7 | Wizard step 3 — **B2 v2 line editor + แถวขยาย** | `_shots/04_wizard_step3.png` | ✅ |
| 8 | Wizard step 5 — review + สายอนุมัติ | `_shots/04b_wizard_step5.png` | ✅ |
| 9 | แผงยืนยันรับที่ปลายทาง | `_shots/05_receive_modal.png` | ✅ |
| 10 | แผงยืนยันรับ — **กรณีมีส่วนต่าง (ของหาย 20 ม้วน ฿23,000)** | `_shots/05b_receive_shortage.png` | ✅ |
| 11 | Submit modal — **DOA slot picker คนจริง** | `_shots/06_doa_slot_picker.png` | ✅ |
| 12 | List ที่ viewport 1024 | `_shots/07_list_1024.png` | ✅ |

**Console / page errors ที่จับได้:**

| ชนิด | จำนวน | รายละเอียด |
|---|---|---|
| `pageerror` (JS runtime) | **0** | — |
| `console.error` ของแอป | **0** | — |
| `console.error` เครือข่าย | 5 | `net::ERR_TUNNEL_CONNECTION_FAILED` — Google Fonts / Fontshare / Lucide CDN ถูกบล็อกใน sandbox |

**Responsive (Rule #97):** ที่ 1024px → `document.documentElement.scrollWidth > clientWidth` = **false** (ไม่มี body horizontal scroll) · sidebar เป็น off-canvas + `.nav-toggle` โผล่ · drawer = `min(กว้างเดิม,100vw)`

## 4. ★ ข้อจำกัดของ sandbox (บันทึกตาม `_RUNNER_BRIEF §2.12`)

> **sandbox บล็อก CDN (ERR_TUNNEL_CONNECTION_FAILED)** — ฟอนต์ Satoshi / Noto Sans Thai และ Lucide โหลดไม่ได้ตอน render check
> ⇒ **Rule #38 (Thai vertical rhythm — เทียบเส้นกึ่งกลางด้วยฟอนต์ไทยจริง) และ icon geometry ของ Lucide = `NOT-CHECKED (offline)`**
> ค่าที่ใช้เป็นชุดที่ระบุว่า verified แล้วใน BASE-KIT (`.btn 2px …0` · `.pill 3px 9px 2px` · `.table td 13px 14px 11px`)
> **ไม่วนแก้เรื่องนี้** — ทีม vibe ที่มีเน็ตต้องเปิดไฟล์แล้วตรวจด้วยตาอีกรอบ (ระบุไว้ใน HANDOFF §5)

## 5. ★ convention `FWD-WIRE:` แทน `TODO:` (บันทึกเหตุผลตาม `_RUNNER_BRIEF §2.11`)

`audit.sh` Rule #24 ตั้ง literal `TODO` = **FAIL** ซึ่งชนกับ S3c ที่บังคับ FAIL = 0
→ ในไฟล์ HTML จึงใช้ marker **`FWD-WIRE: <ชื่อ hook>`** แทน · ในเอกสาร `.md` ทุกฉบับยังใช้ `TODO:` ตามปกติ
**ทั้งสองอันคือรายการเดียวกัน** — HANDOFF §4 ผูกไว้ให้แล้ว

| marker ใน HTML | จำนวนจุด | คู่กับ `TODO:` ใน .md | เจ้าของ |
|---|---|---|---|
| `FWD-WIRE: JE posting` | 19 | `TODO: JE posting` | **W5** |
| `FWD-WIRE: valuation engine` | 3 | `TODO: valuation engine` | **W5** |
| `FWD-WIRE: ENG-NOTIFY` | 2 | (NTF_BRIEF) | **F-NOTIFY** |
| `FWD-WIRE: DOA engine` | 2 | (DOA_BRIEF) | **F-DLG-001** |
| `FWD-WIRE: ENG-DOC-NUM` | 1 | (DOCCFG_BRIEF) | **F-DOCCFG** |
| **รวม** | **27** | | |

`grep -c "TODO" F-WH-STKTRF.html` = **0** ✅

## 6. `self_audit.py` (Rule #60 preflight) — สรุป

ตราประทับ PREFLIGHT อยู่ท้ายไฟล์แล้ว (ตัวเลขจริง ไม่ใช่ตราเปล่า)
รายการที่ยังไม่เป็นศูนย์ **ทั้งหมดมาจากการลอก reference verbatim ตาม Rule #98/#99 ซึ่งห้ามแก้โครง** — รายละเอียดพร้อมเหตุผลรายข้ออยู่ใน `_UX_CHECK_REPORT.md §7`
(`inline_layout` 250 · `font_count` 12 · `custom_tabs` `.tabs/.tab` · `hex_off` เฉพาะ `.a4` งานพิมพ์ + CI teal token · `td_pad_fat` ที่ขัดกับค่าที่ #38 ระบุว่า verified)

## 7. ขนาด/โครงไฟล์

| ตัวชี้ | ค่า |
|---|---|
| ขนาด | ~206 KB (single file — เปิดจาก `file://` ได้ทันที) |
| บรรทัด | 2,291 |
| `<script>` ภายนอก | **0** (Lucide โหลดผ่าน loader ที่มี fallback 3 CDN + no-op เมื่อทุกตัวล่ม → UI ยังใช้งานได้) |
| `localStorage` / `sessionStorage` | **0** |
| Lucide icon | 142 |
| Combobox (Rule #94/#102) | 18 |
| Route | `#/list` · `#/view/:id` · `#/create` · `#/create/dup-:id` · `#/edit/:id` — refresh-safe ทุกเส้น |
